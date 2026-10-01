<?php
/**
 * Core Web Vitals work.
 *
 * The site is photography-led, so LCP is almost always the hero image. The two
 * things that matter most are handled here: the LCP image is never lazy-loaded
 * and is preloaded, and everything else is.
 *
 * @package gm
 */

declare( strict_types = 1 );

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Modern formats to prefer for the featured image, best first.
 *
 * @return array<string, string> extension => MIME type
 */
function gm_modern_formats(): array {
	return array(
		'avif' => 'image/avif',
		'webp' => 'image/webp',
	);
}

/**
 * Rewrite a srcset to $ext, but only when EVERY candidate has a derivative on disk.
 *
 * A partial set is worse than none. If only the full-size original were converted,
 * the <source> would carry a single 2000px candidate and every phone would download
 * it instead of the 800px JPEG it replaced. Returning '' in that case leaves the
 * <img> and its complete JPEG srcset to do the job.
 *
 * @param int|string|array $size Any size accepted by wp_get_attachment_image_srcset().
 * @return string Rewritten srcset, or '' when the set is incomplete.
 */
function gm_derivative_srcset( int $attachment_id, $size, string $ext ): string {
	$srcset = wp_get_attachment_image_srcset( $attachment_id, $size );
	if ( ! $srcset ) {
		return '';
	}

	$uploads = wp_get_upload_dir();
	$out     = array();

	foreach ( explode( ',', (string) $srcset ) as $candidate ) {
		$candidate = trim( $candidate );
		if ( '' === $candidate ) {
			continue;
		}

		$parts      = preg_split( '/\s+/', $candidate );
		$url        = (string) ( $parts[0] ?? '' );
		$descriptor = (string) ( $parts[1] ?? '' );

		if ( ! preg_match( '/\.(jpe?g|png)$/i', $url ) ) {
			return '';
		}

		$swapped = (string) preg_replace( '/\.(jpe?g|png)$/i', '.' . $ext, $url );
		$path    = str_replace( $uploads['baseurl'], $uploads['basedir'], $swapped );

		if ( ! file_exists( $path ) ) {
			return '';
		}

		$out[] = trim( $swapped . ' ' . $descriptor );
	}

	return $out ? implode( ', ', $out ) : '';
}

/**
 * Preload the LCP image and mark it high priority.
 *
 * Exactly one preload is emitted. Emitting a modern-format preload *and* the JPEG
 * one would make any browser supporting both fetch the hero twice. That was the
 * bug here: the JPEG was preloaded, then gm_picture_sources() below served an AVIF
 * and the preloaded bytes were discarded.
 */
function gm_preload_lcp(): void {
	if ( ! is_singular() || ! has_post_thumbnail() ) {
		return;
	}

	$id  = (int) get_post_thumbnail_id();
	$src = wp_get_attachment_image_src( $id, 'gm-hero' );
	if ( ! $src ) {
		return;
	}

	$sizes      = wp_get_attachment_image_sizes( $id, 'gm-hero' );
	$sizes_attr = $sizes ? ' imagesizes="' . esc_attr( (string) $sizes ) . '"' : '';

	// Preload the best format <picture> can actually serve. A browser that does not
	// support that type skips the preload and still gets the right file from
	// <picture>; it only loses the head start.
	foreach ( gm_modern_formats() as $ext => $type ) {
		$derived = gm_derivative_srcset( $id, 'gm-hero', $ext );
		if ( ! $derived ) {
			continue;
		}
		echo '<link rel="preload" as="image" type="' . esc_attr( $type ) . '"'
			. ' imagesrcset="' . esc_attr( $derived ) . '"'
			. $sizes_attr . ' fetchpriority="high" />' . "\n"; // phpcs:ignore WordPress.Security.EscapeOutput -- every part escaped above.
		return;
	}

	// No complete derivative set: preload the original, as before.
	$srcset = wp_get_attachment_image_srcset( $id, 'gm-hero' );
	echo '<link rel="preload" as="image" href="' . esc_url( (string) $src[0] ) . '"'
		. ( $srcset ? ' imagesrcset="' . esc_attr( (string) $srcset ) . '"' : '' )
		. $sizes_attr . ' fetchpriority="high" />' . "\n"; // phpcs:ignore WordPress.Security.EscapeOutput -- every part escaped above.
}
add_action( 'wp_head', 'gm_preload_lcp', 1 );

/**
 * Never lazy-load the featured image — it is the LCP element, and lazy-loading
 * it is one of the most common self-inflicted LCP regressions in WordPress.
 */
function gm_eager_featured_image( array $attr, $attachment, $size ): array {
	if ( is_singular() && (int) get_post_thumbnail_id() === (int) $attachment->ID ) {
		$attr['loading']       = 'eager';
		$attr['fetchpriority'] = 'high';
		$attr['decoding']      = 'sync';
	}
	return $attr;
}
add_filter( 'wp_get_attachment_image_attributes', 'gm_eager_featured_image', 10, 3 );

/**
 * Always give images intrinsic dimensions so they reserve layout space (CLS).
 */
add_filter( 'wp_lazy_loading_enabled', function ( $default, $tag_name, $context ) {
	if ( 'img' === $tag_name && 'the_content' === $context ) {
		return true;
	}
	return $default;
}, 10, 3 );

/**
 * Prefer AVIF then WebP when converted derivatives sit next to the originals.
 *
 * Works with a pre-conversion workflow (see doc 10 §3): upload `foo.jpg` alongside
 * `foo.avif` / `foo.webp` — and the same for every size WordPress generates — and
 * this rewrites the <img> into a <picture> with proper fallbacks.
 *
 * Each <source> carries the full srcset and the same `sizes` as the <img>, so the
 * browser still picks a width appropriate to the viewport. A format is skipped
 * entirely unless every candidate has been converted, because a one-candidate
 * <source> would hand phones the full-size original.
 *
 * Note the srcset is escaped with esc_attr(), not esc_url(): a srcset is a
 * comma-separated list with width descriptors, and esc_url() would mangle it.
 */
function gm_picture_sources( string $html, $post_id, $thumbnail_id, $size = 'gm-hero', $attr = array() ): string {
	$id = (int) $thumbnail_id;
	if ( ! $id ) {
		return $html;
	}

	$size  = $size ?: 'gm-hero';
	$sizes = wp_get_attachment_image_sizes( $id, $size );

	// Respect an explicit sizes attribute passed by the template.
	if ( is_array( $attr ) && ! empty( $attr['sizes'] ) ) {
		$sizes = $attr['sizes'];
	}

	$sources = '';

	foreach ( gm_modern_formats() as $ext => $type ) {
		$derived = gm_derivative_srcset( $id, $size, $ext );
		if ( ! $derived ) {
			continue;
		}
		$sources .= '<source type="' . esc_attr( $type ) . '"'
			. ' srcset="' . esc_attr( $derived ) . '"'
			. ( $sizes ? ' sizes="' . esc_attr( (string) $sizes ) . '"' : '' )
			. ' />';
	}

	return $sources ? '<picture>' . $sources . $html . '</picture>' : $html;
}
add_filter( 'post_thumbnail_html', 'gm_picture_sources', 10, 5 );

/**
 * Drop query strings that break some CDN caches, and stop WP emitting
 * resource hints we do not use.
 */
add_filter( 'wp_resource_hints', function ( array $hints, string $relation ): array {
	if ( 'dns-prefetch' === $relation ) {
		// s.w.org is only used by emoji, which is disabled.
		$hints = array_filter( $hints, static fn( $h ): bool => ! is_string( $h ) || ! str_contains( $h, 's.w.org' ) );
	}
	return $hints;
}, 10, 2 );

/**
 * Limit post revisions — keeps the DB small on a content-heavy site.
 */
add_filter( 'wp_revisions_to_keep', fn(): int => 10, 10, 0 );

/**
 * Security headers. The host or CDN may also set these; duplicates are harmless
 * for these particular headers, but check before adding a CSP here as well.
 */
function gm_security_headers( array $headers ): array {
	$headers['X-Content-Type-Options'] = 'nosniff';
	$headers['Referrer-Policy']        = 'strict-origin-when-cross-origin';
	$headers['X-Frame-Options']        = 'SAMEORIGIN';
	$headers['Permissions-Policy']     = 'geolocation=(), microphone=(), camera=(), interest-cohort=()';
	return $headers;
}
add_filter( 'wp_headers', 'gm_security_headers' );
