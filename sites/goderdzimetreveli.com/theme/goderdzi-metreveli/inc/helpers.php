<?php
/**
 * Shared helpers.
 *
 * @package gm
 */

declare( strict_types = 1 );

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Current language for the request: 'en' or 'ka'.
 *
 * Prefers Polylang/WPML when present; otherwise falls back to the URL prefix,
 * so the theme works before a multilingual plugin is configured.
 */
function gm_current_lang(): string {
	if ( function_exists( 'pll_current_language' ) ) {
		$lang = pll_current_language( 'slug' );
		if ( is_string( $lang ) && '' !== $lang ) {
			return 'ka' === $lang ? 'ka' : 'en';
		}
	}
	if ( defined( 'ICL_LANGUAGE_CODE' ) ) {
		return 'ka' === ICL_LANGUAGE_CODE ? 'ka' : 'en';
	}

	$path = (string) wp_parse_url( add_query_arg( array() ), PHP_URL_PATH );
	return str_starts_with( ltrim( $path, '/' ), 'ka/' ) || 'ka' === trim( $path, '/' ) ? 'ka' : 'en';
}

/**
 * Language of a specific post.
 */
function gm_post_lang( int $post_id ): string {
	if ( function_exists( 'pll_get_post_language' ) ) {
		$lang = pll_get_post_language( $post_id, 'slug' );
		if ( is_string( $lang ) && '' !== $lang ) {
			return 'ka' === $lang ? 'ka' : 'en';
		}
	}
	$stored = get_post_meta( $post_id, '_gm_lang', true );
	if ( 'ka' === $stored ) {
		return 'ka';
	}
	return str_contains( (string) get_permalink( $post_id ), '/ka/' ) ? 'ka' : 'en';
}

/**
 * The counterpart post in the other language, or 0.
 *
 * Uses Polylang when available, then the `_gm_translation_of` meta pairing,
 * which the WXR import sets. Pairing is treated as bidirectional: a post
 * either points at its counterpart, or is pointed at by it.
 */
function gm_translation_id( int $post_id ): int {
	if ( function_exists( 'pll_get_post' ) ) {
		$target = 'ka' === gm_post_lang( $post_id ) ? 'en' : 'ka';
		$found  = pll_get_post( $post_id, $target );
		if ( $found ) {
			return (int) $found;
		}
	}

	$linked = (int) get_post_meta( $post_id, '_gm_translation_of', true );
	if ( $linked && 'publish' === get_post_status( $linked ) ) {
		return $linked;
	}

	// Reverse lookup: someone else points at us.
	$reverse = get_posts( array(
		'post_type'        => array( 'page', 'post' ),
		'post_status'      => 'publish',
		'numberposts'      => 1,
		'fields'           => 'ids',
		'meta_key'         => '_gm_translation_of',
		'meta_value'       => (string) $post_id,
		'suppress_filters' => false,
	) );

	return $reverse ? (int) $reverse[0] : 0;
}

/**
 * A single-line site-wide fallback description.
 */
function gm_default_description(): string {
	return 'ka' === gm_current_lang()
		? 'გოდერძი მეტრეველი — სოფლის მეურნეობის ხელმძღვანელი და საინჟინრო პროფესიონალი: რეგენერაციული მეურნეობა, ნუშის ბაღები, ნახევრად მშრალი მიწების ათვისება, ირიგაცია და მექანიზაცია.'
		: 'Goderdzi Metreveli is an agricultural executive focused on regenerative farming, almond orchards, semi-arid land development, irrigation, mechanization and soil preparation.';
}

/**
 * Per-post SEO fields set from the editor sidebar (inc/meta-boxes.php).
 */
function gm_field( string $key, ?int $post_id = null ): string {
	$post_id = $post_id ?: get_queried_object_id();
	if ( ! $post_id ) {
		return '';
	}
	return trim( (string) get_post_meta( $post_id, '_gm_' . $key, true ) );
}

/**
 * True when this install should never be indexed (staging, local, dev).
 *
 * A second safety net behind the host-level protections described in doc 10 —
 * an indexed staging copy would compete with the live site for the person's own
 * name, which is the exact failure this project exists to prevent.
 */
function gm_is_non_production(): bool {
	if ( defined( 'WP_ENVIRONMENT_TYPE' ) && in_array( WP_ENVIRONMENT_TYPE, array( 'local', 'development', 'staging' ), true ) ) {
		return true;
	}
	if ( function_exists( 'wp_get_environment_type' ) && 'production' !== wp_get_environment_type() ) {
		return true;
	}

	$host = strtolower( (string) wp_parse_url( home_url(), PHP_URL_HOST ) );
	foreach ( array( 'staging', 'dev.', '.test', '.local', 'localhost', 'kinsta.cloud', 'wpengine.com', 'cloudwaysapps.com' ) as $needle ) {
		if ( str_contains( $host, $needle ) ) {
			return true;
		}
	}
	return false;
}

/**
 * Escaped, absolute URL of the image to use for social sharing / schema.
 */
function gm_social_image(): string {
	if ( is_singular() && has_post_thumbnail() ) {
		$src = wp_get_attachment_image_src( (int) get_post_thumbnail_id(), 'gm-wide' );
		if ( $src ) {
			return (string) $src[0];
		}
	}
	$fallback = (string) get_theme_mod( 'gm_default_share_image', '' );
	return $fallback ?: GM_URI . '/assets/img/share-default.jpg';
}

/**
 * Reading time in minutes, for the article header.
 */
function gm_reading_time( ?int $post_id = null ): int {
	$post_id = $post_id ?: get_the_ID();
	$words   = str_word_count( wp_strip_all_tags( (string) get_post_field( 'post_content', $post_id ) ) );
	return max( 1, (int) ceil( $words / 220 ) );
}

/**
 * Render a verification label next to a figure.
 *
 * Every number shown on this site must carry either a source or a verification
 * state. This is the single function that enforces it — there is deliberately
 * no way to render a metric without passing one.
 *
 * @param string $status One of: sourced, attributed, unverified.
 * @param string $note   Short source name or what is needed.
 * @param string $url    Optional source URL.
 */
function gm_verification_label( string $status, string $note, string $url = '' ): string {
	$classes = array(
		'sourced'    => 'gm-vlabel gm-vlabel--sourced',
		'attributed' => 'gm-vlabel gm-vlabel--attributed',
		'unverified' => 'gm-vlabel gm-vlabel--unverified',
	);
	$class = $classes[ $status ] ?? $classes['unverified'];

	$inner = esc_html( $note );
	if ( $url ) {
		$inner = '<a href="' . esc_url( $url ) . '" rel="nofollow noopener" target="_blank">' . $inner . '</a>';
	}

	return '<span class="' . esc_attr( $class ) . '">' . $inner . '</span>';
}
