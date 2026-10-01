<?php
/**
 * Titles, meta descriptions, canonicals, robots directives and Open Graph.
 *
 * Replaces an SEO plugin entirely. Nothing here writes to the database except
 * the per-post fields in inc/meta-boxes.php.
 *
 * @package gm
 */

declare( strict_types = 1 );

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Document title.
 *
 * Uses the hand-written SEO title when one is set, so the titles in
 * docs/02-seo-titles-and-meta.md are what actually ship. Falls back to
 * "Post Title | Goderdzi Metreveli" only when no override exists.
 */
function gm_document_title( array $parts ): array {
	$override = gm_field( 'seo_title' );
	if ( $override ) {
		return array( 'title' => $override );
	}

	if ( is_front_page() ) {
		return array(
			'title' => 'ka' === gm_current_lang()
				? 'გოდერძი მეტრეველი | რეგენერაციული სოფლის მეურნეობა და ნუშის წარმოება'
				: 'Goderdzi Metreveli | Regenerative Agriculture & Almond Farming',
		);
	}

	$parts['site'] = 'Goderdzi Metreveli';
	unset( $parts['tagline'] );
	return $parts;
}
add_filter( 'document_title_parts', 'gm_document_title' );
add_filter( 'document_title_separator', fn(): string => '|' );

/**
 * The description used for <meta name="description">, og:description and schema.
 */
function gm_meta_description(): string {
	$override = gm_field( 'meta_description' );
	if ( $override ) {
		return $override;
	}

	if ( is_front_page() ) {
		return gm_default_description();
	}

	if ( is_singular() ) {
		$excerpt = has_excerpt() ? get_the_excerpt() : wp_trim_words( wp_strip_all_tags( strip_shortcodes( (string) get_the_content() ) ), 30, '…' );
		$excerpt = trim( (string) $excerpt );
		if ( $excerpt ) {
			return $excerpt;
		}
	}

	if ( is_post_type_archive() || is_home() ) {
		return 'ka' === gm_current_lang()
			? 'ტექნიკური სტატიები ნიადაგის მომზადების, ირიგაციის, მექანიზაციისა და ნუშის ბაღების შესახებ.'
			: 'Technical articles on orchard soil preparation, irrigation, mechanization and almond production.';
	}

	return gm_default_description();
}

/**
 * Canonical URL. Self-referencing everywhere; paginated pages point at themselves.
 */
function gm_canonical_url(): string {
	$override = gm_field( 'canonical' );
	if ( $override ) {
		return $override;
	}

	if ( is_front_page() ) {
		return trailingslashit( home_url( '/' ) );
	}
	if ( is_singular() ) {
		$url  = (string) get_permalink();
		$page = (int) get_query_var( 'page' );
		return $page > 1 ? trailingslashit( $url ) . 'page/' . $page . '/' : $url;
	}
	if ( is_post_type_archive() || is_home() ) {
		$url    = (string) get_permalink( (int) get_option( 'page_for_posts' ) );
		$paged  = (int) get_query_var( 'paged' );
		return $paged > 1 ? trailingslashit( $url ) . 'page/' . $paged . '/' : $url;
	}

	return home_url( add_query_arg( array() ) );
}

/**
 * Robots directives.
 *
 * Indexation policy per docs/01-site-architecture.md §5: only pages, articles
 * and the article index are indexed. Every archive form is noindex,follow —
 * thin, duplicative of the pillar pages, and the pillars are what should rank.
 */
function gm_robots( array $robots ): array {
	if ( gm_is_non_production() ) {
		return array( 'noindex' => true, 'nofollow' => true, 'noarchive' => true );
	}

	$noindex =
		is_search()
		|| is_404()
		|| is_author()
		|| is_date()
		|| is_category()
		|| is_tag()
		|| is_tax()
		|| is_attachment()
		|| ( is_paged() && ( is_home() || is_post_type_archive() ) )
		|| 'on' === gm_field( 'noindex' );

	if ( $noindex ) {
		$robots['noindex'] = true;
		$robots['follow']  = true;
		unset( $robots['index'] );
		return $robots;
	}

	$robots['index']              = true;
	$robots['follow']             = true;
	$robots['max-image-preview']  = 'large';
	$robots['max-snippet']        = '-1';
	$robots['max-video-preview']  = '-1';
	return $robots;
}
add_filter( 'wp_robots', 'gm_robots' );

/**
 * Head output: description, canonical, Open Graph, Twitter card.
 */
function gm_head_meta(): void {
	$desc      = gm_meta_description();
	$canonical = gm_canonical_url();
	$lang      = gm_current_lang();
	$image     = gm_social_image();
	$title     = wp_get_document_title();

	echo "\n<!-- gm:seo -->\n";

	if ( $desc ) {
		printf( '<meta name="description" content="%s" />' . "\n", esc_attr( wp_strip_all_tags( $desc ) ) );
	}
	if ( $canonical ) {
		printf( '<link rel="canonical" href="%s" />' . "\n", esc_url( $canonical ) );
	}

	// Open Graph.
	printf( '<meta property="og:locale" content="%s" />' . "\n", 'ka' === $lang ? 'ka_GE' : 'en_US' );
	printf( '<meta property="og:type" content="%s" />' . "\n", is_singular( 'post' ) ? 'article' : 'website' );
	printf( '<meta property="og:site_name" content="%s" />' . "\n", esc_attr( 'Goderdzi Metreveli' ) );
	printf( '<meta property="og:title" content="%s" />' . "\n", esc_attr( $title ) );
	printf( '<meta property="og:description" content="%s" />' . "\n", esc_attr( wp_strip_all_tags( $desc ) ) );
	printf( '<meta property="og:url" content="%s" />' . "\n", esc_url( $canonical ) );

	if ( $image ) {
		printf( '<meta property="og:image" content="%s" />' . "\n", esc_url( $image ) );
		printf( '<meta property="og:image:alt" content="%s" />' . "\n", esc_attr( $title ) );
	}

	if ( is_singular( 'post' ) ) {
		printf( '<meta property="article:published_time" content="%s" />' . "\n", esc_attr( (string) get_the_date( DATE_W3C ) ) );
		printf( '<meta property="article:modified_time" content="%s" />' . "\n", esc_attr( (string) get_the_modified_date( DATE_W3C ) ) );
		printf( '<meta property="article:author" content="%s" />' . "\n", esc_url( gm_profile_url() ) );
	}

	// Twitter/X — summary_large_image, no site handle asserted unless confirmed.
	echo '<meta name="twitter:card" content="summary_large_image" />' . "\n";
	printf( '<meta name="twitter:title" content="%s" />' . "\n", esc_attr( $title ) );
	printf( '<meta name="twitter:description" content="%s" />' . "\n", esc_attr( wp_strip_all_tags( $desc ) ) );
	if ( $image ) {
		printf( '<meta name="twitter:image" content="%s" />' . "\n", esc_url( $image ) );
	}

	echo "<!-- /gm:seo -->\n\n";
}
add_action( 'wp_head', 'gm_head_meta', 2 );

/**
 * Send X-Robots-Tag on non-production so noindex survives even if the HTML is
 * cached or served from a snapshot.
 */
function gm_robots_header(): void {
	if ( gm_is_non_production() && ! headers_sent() ) {
		header( 'X-Robots-Tag: noindex, nofollow', true );
	}
}
add_action( 'template_redirect', 'gm_robots_header', 1 );

/**
 * robots.txt.
 */
function gm_robots_txt( string $output, $public ): string {
	if ( gm_is_non_production() || ! $public ) {
		return "User-agent: *\nDisallow: /\n";
	}

	$lines = array(
		'User-agent: *',
		'Allow: /',
		'Disallow: /wp-admin/',
		'Allow: /wp-admin/admin-ajax.php',
		'Disallow: /wp-login.php',
		'Disallow: /?s=',
		'Disallow: /search/',
		'Disallow: /*?replytocom=',
		'',
		'Sitemap: ' . home_url( '/sitemap.xml' ),
		'',
	);

	return implode( "\n", $lines );
}
add_filter( 'robots_txt', 'gm_robots_txt', 10, 2 );
