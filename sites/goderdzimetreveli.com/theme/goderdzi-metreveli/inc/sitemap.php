<?php
/**
 * XML sitemap index + child sitemaps, including an image sitemap.
 *
 * WordPress core sitemaps are disabled in functions.php because they cannot
 * express the indexation policy in docs/01-site-architecture.md §5 (they list
 * author and term archives that are deliberately noindex) and have no image
 * support. This implementation lists only indexable URLs.
 *
 *   /sitemap.xml           index
 *   /sitemap-pages.xml     English pages
 *   /sitemap-articles.xml  posts
 *   /sitemap-ka.xml        Georgian pages
 *   /sitemap-images.xml    images attached to published content
 *
 * @package gm
 */

declare( strict_types = 1 );

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const GM_SITEMAPS = array( 'pages', 'articles', 'ka', 'images' );

/**
 * Rewrite rules.
 */
function gm_sitemap_rewrites(): void {
	add_rewrite_rule( '^sitemap\.xml$', 'index.php?gm_sitemap=index', 'top' );
	add_rewrite_rule( '^sitemap-([a-z]+)\.xml$', 'index.php?gm_sitemap=$matches[1]', 'top' );
}
add_action( 'init', 'gm_sitemap_rewrites' );

add_filter( 'query_vars', function ( array $vars ): array {
	$vars[] = 'gm_sitemap';
	return $vars;
} );

/**
 * Flush rewrites once on theme activation.
 */
add_action( 'after_switch_theme', function (): void {
	gm_sitemap_rewrites();
	flush_rewrite_rules();
} );

/**
 * Posts that belong in a sitemap: published, indexable, correct language.
 */
function gm_sitemap_query( string $which ): array {
	$args = array(
		'post_status'            => 'publish',
		'posts_per_page'         => 2000,
		'orderby'                => 'modified',
		'order'                  => 'DESC',
		'no_found_rows'          => true,
		'ignore_sticky_posts'    => true,
		'update_post_term_cache' => false,
		'meta_query'             => array(
			'relation' => 'OR',
			array( 'key' => '_gm_noindex', 'compare' => 'NOT EXISTS' ),
			array( 'key' => '_gm_noindex', 'value' => 'on', 'compare' => '!=' ),
		),
	);

	$args['post_type'] = ( 'articles' === $which ) ? 'post' : 'page';

	$posts = get_posts( $args );

	// Split pages by language.
	if ( 'pages' === $which ) {
		return array_values( array_filter( $posts, static fn( $p ): bool => 'en' === gm_post_lang( (int) $p->ID ) ) );
	}
	if ( 'ka' === $which ) {
		return array_values( array_filter( $posts, static fn( $p ): bool => 'ka' === gm_post_lang( (int) $p->ID ) ) );
	}

	return $posts;
}

/**
 * Render.
 */
function gm_render_sitemap(): void {
	$which = get_query_var( 'gm_sitemap' );
	if ( ! $which ) {
		return;
	}

	// Never expose a sitemap on staging.
	if ( gm_is_non_production() ) {
		status_header( 404 );
		exit;
	}

	header( 'Content-Type: application/xml; charset=UTF-8' );
	header( 'X-Robots-Tag: noindex, follow', true );
	echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";

	if ( 'index' === $which ) {
		echo '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
		foreach ( GM_SITEMAPS as $name ) {
			$posts = 'images' === $name ? gm_sitemap_query( 'pages' ) : gm_sitemap_query( $name );
			if ( ! $posts ) {
				continue;
			}
			$latest = max( array_map( static fn( $p ): int => (int) strtotime( $p->post_modified_gmt ), $posts ) );
			printf(
				"  <sitemap>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n  </sitemap>\n",
				esc_url( home_url( '/sitemap-' . $name . '.xml' ) ),
				esc_html( gmdate( DATE_W3C, $latest ) )
			);
		}
		echo '</sitemapindex>';
		exit;
	}

	if ( 'images' === $which ) {
		gm_render_image_sitemap();
		exit;
	}

	if ( ! in_array( (string) $which, GM_SITEMAPS, true ) ) {
		status_header( 404 );
		exit;
	}

	$posts = gm_sitemap_query( (string) $which );

	echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">' . "\n";

	// The homepage belongs in the pages sitemap.
	if ( 'pages' === $which ) {
		printf(
			"  <url>\n    <loc>%s</loc>\n    <changefreq>weekly</changefreq>\n    <priority>1.0</priority>\n  </url>\n",
			esc_url( trailingslashit( home_url( '/' ) ) )
		);
	}

	foreach ( $posts as $post ) {
		$id = (int) $post->ID;

		// Homepage is emitted above; skip the page object that backs it.
		if ( (int) get_option( 'page_on_front' ) === $id ) {
			continue;
		}

		printf( "  <url>\n    <loc>%s</loc>\n", esc_url( (string) get_permalink( $id ) ) );
		printf( "    <lastmod>%s</lastmod>\n", esc_html( gmdate( DATE_W3C, (int) strtotime( $post->post_modified_gmt ) ) ) );

		// hreflang alternates inside the sitemap — a second, independent signal
		// alongside the <link> tags, and the one Search Console reports on.
		$other = gm_translation_id( $id );
		if ( $other && 'publish' === get_post_status( $other ) ) {
			foreach ( array( $id, $other ) as $variant ) {
				printf(
					'    <xhtml:link rel="alternate" hreflang="%s" href="%s" />' . "\n",
					esc_attr( gm_post_lang( (int) $variant ) ),
					esc_url( (string) get_permalink( (int) $variant ) )
				);
			}
		}

		echo "  </url>\n";
	}

	echo '</urlset>';
	exit;
}
add_action( 'template_redirect', 'gm_render_sitemap', 0 );

/**
 * Image sitemap — matters here because the site's differentiator is original
 * field photography, and image search is a real discovery channel for it.
 */
function gm_render_image_sitemap(): void {
	$posts = array_merge( gm_sitemap_query( 'pages' ), gm_sitemap_query( 'articles' ), gm_sitemap_query( 'ka' ) );

	echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' . "\n";

	foreach ( $posts as $post ) {
		$id     = (int) $post->ID;
		$images = array();

		if ( has_post_thumbnail( $id ) ) {
			$images[ (int) get_post_thumbnail_id( $id ) ] = true;
		}
		foreach ( get_attached_media( 'image', $id ) as $media ) {
			$images[ (int) $media->ID ] = true;
		}

		if ( ! $images ) {
			continue;
		}

		printf( "  <url>\n    <loc>%s</loc>\n", esc_url( (string) get_permalink( $id ) ) );
		foreach ( array_keys( $images ) as $image_id ) {
			$url = wp_get_attachment_url( $image_id );
			if ( ! $url ) {
				continue;
			}
			echo "    <image:image>\n";
			printf( "      <image:loc>%s</image:loc>\n", esc_url( $url ) );

			$alt     = trim( (string) get_post_meta( $image_id, '_wp_attachment_image_alt', true ) );
			$caption = trim( (string) wp_get_attachment_caption( $image_id ) );
			if ( $alt ) {
				printf( "      <image:title>%s</image:title>\n", esc_html( $alt ) );
			}
			if ( $caption ) {
				printf( "      <image:caption>%s</image:caption>\n", esc_html( $caption ) );
			}
			echo "    </image:image>\n";
		}
		echo "  </url>\n";
	}

	echo '</urlset>';
}
