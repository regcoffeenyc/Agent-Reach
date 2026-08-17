<?php
/**
 * Goderdzi Metreveli — theme bootstrap.
 *
 * Design constraints this theme is built around:
 *  - No SEO plugin. Titles, meta, canonicals, OG, JSON-LD, hreflang, robots and
 *    the XML sitemap are all emitted here so structured data stays in version
 *    control and cannot be silently contradicted by a plugin's own Person graph.
 *  - No external requests. No Google Fonts, no CDN scripts, no gravatar.
 *  - No page builder. Core blocks only.
 *
 * @package gm
 */

declare( strict_types = 1 );

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'GM_VERSION', '1.0.0' );
define( 'GM_DIR', get_template_directory() );
define( 'GM_URI', get_template_directory_uri() );

require_once GM_DIR . '/inc/helpers.php';
require_once GM_DIR . '/inc/seo.php';
require_once GM_DIR . '/inc/schema.php';
require_once GM_DIR . '/inc/hreflang.php';
require_once GM_DIR . '/inc/breadcrumbs.php';
require_once GM_DIR . '/inc/performance.php';
require_once GM_DIR . '/inc/sitemap.php';
require_once GM_DIR . '/inc/meta-boxes.php';

/**
 * Theme supports.
 */
function gm_setup(): void {
	load_theme_textdomain( 'gm', GM_DIR . '/languages' );

	add_theme_support( 'title-tag' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'html5', array(
		'search-form', 'comment-form', 'comment-list', 'gallery', 'caption', 'style', 'script',
	) );
	add_theme_support( 'responsive-embeds' );
	add_theme_support( 'editor-styles' );
	add_editor_style( 'assets/css/main.css' );

	// Wide/full alignment without a builder.
	add_theme_support( 'align-wide' );

	// Image sizes matched to the layout's breakpoints so srcset has useful candidates.
	add_image_size( 'gm-hero', 2000, 1125, true );
	add_image_size( 'gm-wide', 1400, 788, true );
	add_image_size( 'gm-card', 800, 600, true );
	add_image_size( 'gm-portrait', 900, 1125, true );

	register_nav_menus( array(
		'primary'     => __( 'Primary', 'gm' ),
		'footer_topics' => __( 'Footer — Topics', 'gm' ),
		'footer_about'  => __( 'Footer — About', 'gm' ),
	) );

	// Attachment pages are pure index bloat on a photo-heavy site. Kill them.
	add_filter( 'wp_sitemaps_enabled', '__return_false' ); // We ship our own sitemap.
}
add_action( 'after_setup_theme', 'gm_setup' );

/**
 * Redirect attachment pages to the parent post, or to the file.
 */
function gm_kill_attachment_pages(): void {
	if ( ! is_attachment() ) {
		return;
	}
	$parent = (int) get_post()->post_parent;
	wp_safe_redirect( $parent ? get_permalink( $parent ) : home_url( '/' ), 301 );
	exit;
}
add_action( 'template_redirect', 'gm_kill_attachment_pages' );

/**
 * Assets. One stylesheet, no JS framework. The only script is a ~1 KB
 * progressive enhancement for the mobile menu and nav dropdowns.
 */
function gm_assets(): void {
	$css = GM_DIR . '/assets/css/main.css';
	wp_enqueue_style(
		'gm-main',
		GM_URI . '/assets/css/main.css',
		array(),
		file_exists( $css ) ? (string) filemtime( $css ) : GM_VERSION
	);

	$js = GM_DIR . '/assets/js/nav.js';
	wp_enqueue_script(
		'gm-nav',
		GM_URI . '/assets/js/nav.js',
		array(),
		file_exists( $js ) ? (string) filemtime( $js ) : GM_VERSION,
		array( 'strategy' => 'defer', 'in_footer' => true )
	);
}
add_action( 'wp_enqueue_scripts', 'gm_assets' );

/**
 * Remove core output that costs bytes and gives nothing back here.
 */
function gm_trim_head(): void {
	remove_action( 'wp_head', 'wp_generator' );
	remove_action( 'wp_head', 'rsd_link' );
	remove_action( 'wp_head', 'wlwmanifest_link' );
	remove_action( 'wp_head', 'wp_shortlink_wp_head' );
	remove_action( 'wp_head', 'adjacent_posts_rel_link_wp_head' );
	remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
	remove_action( 'wp_print_styles', 'print_emoji_styles' );
	remove_action( 'admin_print_scripts', 'print_emoji_detection_script' );
	remove_action( 'admin_print_styles', 'print_emoji_styles' );

	// Core block library CSS is ~90 KB and this theme styles blocks itself.
	wp_dequeue_style( 'wp-block-library' );
	wp_dequeue_style( 'wp-block-library-theme' );
	wp_dequeue_style( 'global-styles' );
	wp_dequeue_style( 'classic-theme-styles' );
}
add_action( 'wp_enqueue_scripts', 'gm_trim_head', 100 );
add_action( 'init', function (): void {
	remove_action( 'wp_head', 'wp_generator' );
} );

/**
 * Disable XML-RPC and REST user enumeration.
 */
add_filter( 'xmlrpc_enabled', '__return_false' );

function gm_block_user_enumeration( $result ) {
	if ( ! empty( $result ) ) {
		return $result;
	}
	if ( ! is_user_logged_in() ) {
		$route = isset( $GLOBALS['wp']->query_vars['rest_route'] ) ? (string) $GLOBALS['wp']->query_vars['rest_route'] : '';
		if ( str_starts_with( $route, '/wp/v2/users' ) ) {
			return new WP_Error( 'rest_forbidden', __( 'Not available.', 'gm' ), array( 'status' => 401 ) );
		}
	}
	return $result;
}
add_filter( 'rest_authentication_errors', 'gm_block_user_enumeration' );

/**
 * Excerpt tuning.
 */
add_filter( 'excerpt_length', fn(): int => 32 );
add_filter( 'excerpt_more', fn(): string => '…' );

/**
 * Body classes that the stylesheet keys off.
 */
function gm_body_class( array $classes ): array {
	$classes[] = 'lang-' . gm_current_lang();
	if ( is_page_template( 'page-templates/pillar.php' ) ) {
		$classes[] = 'is-pillar';
	}
	if ( is_page_template( 'page-templates/case-study.php' ) ) {
		$classes[] = 'is-case-study';
	}
	return $classes;
}
add_filter( 'body_class', 'gm_body_class' );

/**
 * Georgian pages get lang/dir on <html> via this filter.
 */
function gm_language_attributes( string $output ): string {
	if ( 'ka' === gm_current_lang() ) {
		return 'lang="ka"';
	}
	return $output;
}
add_filter( 'language_attributes', 'gm_language_attributes' );
