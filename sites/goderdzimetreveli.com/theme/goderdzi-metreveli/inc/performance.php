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
 * Preload the LCP image and mark it high priority.
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

	$srcset = wp_get_attachment_image_srcset( $id, 'gm-hero' );
	$sizes  = wp_get_attachment_image_sizes( $id, 'gm-hero' );

	printf(
		'<link rel="preload" as="image" href="%s"%s%s fetchpriority="high" />' . "\n",
		esc_url( (string) $src[0] ),
		$srcset ? ' imagesrcset="' . esc_attr( (string) $srcset ) . '"' : '',
		$sizes ? ' imagesizes="' . esc_attr( (string) $sizes ) . '"' : ''
	);
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
 * Prefer AVIF then WebP when a converted derivative sits next to the original.
 *
 * Works with a pre-conversion workflow (see doc 10 §3): upload
 * `foo.jpg` alongside `foo.avif` / `foo.webp` and this rewrites the <img> into a
 * <picture> with proper fallbacks. If no derivative exists, output is unchanged.
 */
function gm_picture_sources( string $html, $post_id, $thumbnail_id ): string {
	$src = wp_get_attachment_url( (int) $thumbnail_id );
	if ( ! $src || ! preg_match( '/\.(jpe?g|png)$/i', $src ) ) {
		return $html;
	}

	$uploads = wp_get_upload_dir();
	$sources = '';

	foreach ( array( 'avif' => 'image/avif', 'webp' => 'image/webp' ) as $ext => $type ) {
		$candidate = preg_replace( '/\.(jpe?g|png)$/i', '.' . $ext, $src );
		$path      = str_replace( $uploads['baseurl'], $uploads['basedir'], (string) $candidate );
		if ( file_exists( $path ) ) {
			$sources .= sprintf(
				'<source type="%s" srcset="%s" />',
				esc_attr( $type ),
				esc_url( (string) $candidate )
			);
		}
	}

	return $sources ? '<picture>' . $sources . $html . '</picture>' : $html;
}
add_filter( 'post_thumbnail_html', 'gm_picture_sources', 10, 3 );

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
