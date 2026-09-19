<?php
/**
 * hreflang for the EN (root) / KA (/ka/) pair.
 *
 * Rules enforced:
 *   - Annotations are reciprocal. A cluster is emitted only when the counterpart
 *     post actually exists and is published — a one-way or dangling annotation is
 *     ignored by search engines and can suppress the whole cluster.
 *   - Every page self-references.
 *   - x-default always points at the English URL.
 *
 * @package gm
 */

declare( strict_types = 1 );

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Build the hreflang map for the current request: [ 'en' => url, 'ka' => url ].
 */
function gm_hreflang_map(): array {
	$map = array();

	if ( is_front_page() ) {
		$map['en'] = trailingslashit( home_url( '/' ) );
		$ka        = get_page_by_path( 'ka' );
		if ( $ka && 'publish' === get_post_status( $ka ) ) {
			$map['ka'] = (string) get_permalink( $ka );
		}
		return $map;
	}

	if ( ! is_singular() ) {
		// Archives exist in English only for now; self-reference only.
		$map['en'] = gm_canonical_url();
		return $map;
	}

	$id   = (int) get_queried_object_id();
	$lang = gm_post_lang( $id );
	$map[ $lang ] = (string) get_permalink( $id );

	$other = gm_translation_id( $id );
	if ( $other && 'publish' === get_post_status( $other ) ) {
		$map[ gm_post_lang( $other ) ] = (string) get_permalink( $other );
	}

	return $map;
}

/**
 * Emit the link elements.
 */
function gm_hreflang_tags(): void {
	if ( is_404() || is_search() || gm_is_non_production() ) {
		return;
	}

	$map = gm_hreflang_map();
	if ( ! $map ) {
		return;
	}

	echo "\n<!-- gm:hreflang -->\n";
	foreach ( $map as $lang => $url ) {
		printf(
			'<link rel="alternate" hreflang="%s" href="%s" />' . "\n",
			esc_attr( $lang ),
			esc_url( $url )
		);
	}

	// x-default → the English URL when there is one, otherwise the only URL we have.
	$default = $map['en'] ?? reset( $map );
	printf( '<link rel="alternate" hreflang="x-default" href="%s" />' . "\n", esc_url( (string) $default ) );
	echo "<!-- /gm:hreflang -->\n";
}
add_action( 'wp_head', 'gm_hreflang_tags', 3 );

/**
 * Language switch markup for the header.
 *
 * Renders a link only when a real counterpart exists. When it does not, the
 * other language is shown as disabled rather than linking to a 404 or dumping
 * the visitor on the homepage — both of which are worse than saying "not
 * available".
 */
function gm_language_switch(): string {
	$map     = gm_hreflang_map();
	$current = gm_current_lang();
	$labels  = array( 'en' => 'EN', 'ka' => 'ქარ' );

	$out = '<div class="gm-langswitch" role="group" aria-label="' . esc_attr__( 'Language', 'gm' ) . '">';
	foreach ( $labels as $code => $label ) {
		if ( $code === $current ) {
			$out .= '<span class="gm-langswitch__item is-current" aria-current="true">' . esc_html( $label ) . '</span>';
		} elseif ( ! empty( $map[ $code ] ) ) {
			$out .= '<a class="gm-langswitch__item" hreflang="' . esc_attr( $code ) . '" href="' . esc_url( $map[ $code ] ) . '">' . esc_html( $label ) . '</a>';
		} else {
			$out .= '<span class="gm-langswitch__item is-unavailable" aria-disabled="true" title="' . esc_attr__( 'Not available in this language', 'gm' ) . '">' . esc_html( $label ) . '</span>';
		}
	}
	$out .= '</div>';

	return $out;
}
