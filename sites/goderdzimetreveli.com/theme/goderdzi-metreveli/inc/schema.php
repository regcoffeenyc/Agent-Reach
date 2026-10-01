<?php
/**
 * JSON-LD structured data.
 *
 * Constraints applied here come directly from docs/07-fact-verification-report.md §6:
 *   - `alumniOf`  omitted — education unverified.
 *   - `award`     omitted from Person — the 2023 SDG 12 recognition went to the
 *                 organisation, not to the individual. It appears in visible page
 *                 text only.
 *   - `worksFor` / `affiliation` omitted — current roles unverified and the
 *                 relationships are historical.
 *   - `sameAs`    contains ONLY the confirmed official LinkedIn profile. It is
 *                 empty until that URL is set, and an empty array is omitted
 *                 rather than emitted.
 *
 * Structured data must match visible content. Do not add a property here that
 * the page does not say.
 *
 * @package gm
 */

declare( strict_types = 1 );

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * URL of the canonical ProfilePage — the entity's home on this site.
 */
function gm_profile_url(): string {
	$page = get_page_by_path( 'about' );
	return $page ? (string) get_permalink( $page ) : home_url( '/about/' );
}

/** Stable @id fragments. */
function gm_id( string $fragment ): string {
	return trailingslashit( home_url( '/' ) ) . '#' . $fragment;
}

/**
 * The Person node. Single source of truth — referenced by @id everywhere else.
 */
function gm_person_node(): array {
	$node = array(
		'@type'       => 'Person',
		'@id'         => gm_id( 'person' ),
		'name'        => 'Goderdzi Metreveli',
		'url'         => gm_profile_url(),
		'description' => 'Georgian agricultural executive and engineering professional working in large-scale orchard development, soil preparation, irrigation infrastructure, agricultural mechanization and regenerative farming in semi-arid conditions.',
		'jobTitle'    => 'Agricultural Executive',
		'knowsAbout'  => array(
			'Regenerative agriculture',
			'Almond orchard development',
			'Semi-arid land development',
			'Deep ripping and subsoil preparation',
			'Orchard soil preparation',
			'Irrigation infrastructure',
			'Agricultural mechanization',
			'Erosion control',
			'Almond processing',
			'Agricultural export standards',
		),
		'nationality' => array( '@type' => 'Country', 'name' => 'Georgia' ),
	);

	$portrait = (string) get_theme_mod( 'gm_portrait_url', '' );
	if ( $portrait ) {
		$node['image'] = array(
			'@type' => 'ImageObject',
			'@id'   => gm_id( 'portrait' ),
			'url'   => $portrait,
			'caption' => 'Goderdzi Metreveli',
		);
	}

	/*
	 * sameAs — confirmed profiles ONLY.
	 *
	 * Set gm_linkedin_url in the Customizer once the official profile URL is
	 * confirmed (doc 08, item A14). Never add a duplicate, unclaimed or
	 * lookalike profile: a wrong sameAs actively damages entity resolution
	 * rather than helping it.
	 */
	$same_as = array_values( array_filter( array_map(
		'trim',
		array( (string) get_theme_mod( 'gm_linkedin_url', '' ) )
	) ) );

	if ( $same_as ) {
		$node['sameAs'] = $same_as;
	}

	return $node;
}

/**
 * WebSite node.
 */
function gm_website_node(): array {
	return array(
		'@type'    => 'WebSite',
		'@id'      => gm_id( 'website' ),
		'url'      => trailingslashit( home_url( '/' ) ),
		'name'     => 'Goderdzi Metreveli',
		'description' => gm_default_description(),
		'publisher' => array( '@id' => gm_id( 'person' ) ),
		'inLanguage' => 'ka' === gm_current_lang() ? 'ka' : 'en',
	);
}

/**
 * Emit the graph.
 */
function gm_structured_data(): void {
	if ( is_404() || is_search() ) {
		return;
	}

	$lang      = 'ka' === gm_current_lang() ? 'ka' : 'en';
	$canonical = gm_canonical_url();
	$graph     = array( gm_person_node(), gm_website_node() );

	$is_profile = is_page( 'about' ) || 'on' === gm_field( 'is_profile_page' );

	// WebPage / ProfilePage.
	$page = array(
		'@type'      => $is_profile ? 'ProfilePage' : 'WebPage',
		'@id'        => $canonical . '#webpage',
		'url'        => $canonical,
		'name'       => wp_get_document_title(),
		'description' => wp_strip_all_tags( gm_meta_description() ),
		'isPartOf'   => array( '@id' => gm_id( 'website' ) ),
		'inLanguage' => $lang,
	);

	if ( $is_profile ) {
		// On a ProfilePage, mainEntity is the person the page is about.
		$page['mainEntity'] = array( '@id' => gm_id( 'person' ) );
	} else {
		$page['about'] = array( '@id' => gm_id( 'person' ) );
	}

	if ( is_singular() ) {
		$page['datePublished'] = get_the_date( DATE_W3C );
		$page['dateModified']  = get_the_modified_date( DATE_W3C );
	}

	$crumbs = gm_breadcrumb_items();
	if ( count( $crumbs ) > 1 ) {
		$page['breadcrumb'] = array( '@id' => $canonical . '#breadcrumb' );
		$graph[] = array(
			'@type'           => 'BreadcrumbList',
			'@id'             => $canonical . '#breadcrumb',
			'itemListElement' => array_map(
				static function ( array $c, int $i ): array {
					$item = array(
						'@type'    => 'ListItem',
						'position' => $i + 1,
						'name'     => $c['label'],
					);
					// The last crumb is the current page; omit `item` per Google guidance.
					if ( ! empty( $c['url'] ) ) {
						$item['item'] = $c['url'];
					}
					return $item;
				},
				$crumbs,
				array_keys( $crumbs )
			),
		);
	}

	$graph[] = $page;

	// Article node for technical posts.
	if ( is_singular( 'post' ) ) {
		$article = array(
			'@type'            => 'Article',
			'@id'              => $canonical . '#article',
			'isPartOf'         => array( '@id' => $canonical . '#webpage' ),
			'mainEntityOfPage' => array( '@id' => $canonical . '#webpage' ),
			'headline'         => wp_strip_all_tags( (string) get_the_title() ),
			'description'      => wp_strip_all_tags( gm_meta_description() ),
			'datePublished'    => get_the_date( DATE_W3C ),
			'dateModified'     => get_the_modified_date( DATE_W3C ),
			'inLanguage'       => $lang,
			// author.url points at the ProfilePage, per the brief — this is what
			// binds topical authority to the named entity rather than to the URL.
			'author'           => array(
				'@type' => 'Person',
				'@id'   => gm_id( 'person' ),
				'name'  => 'Goderdzi Metreveli',
				'url'   => gm_profile_url(),
			),
			'publisher'        => array( '@id' => gm_id( 'person' ) ),
		);

		if ( has_post_thumbnail() ) {
			$src = wp_get_attachment_image_src( (int) get_post_thumbnail_id(), 'gm-hero' );
			if ( $src ) {
				$article['image'] = array(
					'@type'  => 'ImageObject',
					'url'    => $src[0],
					'width'  => $src[1],
					'height' => $src[2],
				);
			}
		} else {
			/*
			 * Google requires an image for Article rich results, so an article
			 * published before its photography is ready was ineligible. Falls back
			 * to the share image; gm_social_image() returns '' when none is on disk.
			 */
			$fallback = gm_social_image();
			if ( $fallback ) {
				$article['image'] = $fallback;
			}
		}

		$terms = get_the_terms( get_the_ID(), 'category' );
		if ( $terms && ! is_wp_error( $terms ) ) {
			$article['articleSection'] = wp_list_pluck( $terms, 'name' );
		}

		$graph[] = $article;
	}

	$payload = array(
		'@context' => 'https://schema.org',
		'@graph'   => array_values( $graph ),
	);

	echo "\n<script type=\"application/ld+json\">\n";
	echo wp_json_encode( $payload, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT );
	echo "\n</script>\n";
}
add_action( 'wp_head', 'gm_structured_data', 20 );

/**
 * Customizer settings for the few values that must not be hardcoded.
 */
function gm_customizer( WP_Customize_Manager $wp_customize ): void {
	$wp_customize->add_section( 'gm_entity', array(
		'title'       => __( 'Entity and structured data', 'gm' ),
		'priority'    => 30,
		'description' => __( 'Only add a profile URL that has been confirmed as official. An incorrect sameAs damages entity resolution.', 'gm' ),
	) );

	$wp_customize->add_setting( 'gm_linkedin_url', array(
		'default'           => '',
		'sanitize_callback' => 'esc_url_raw',
		'transport'         => 'refresh',
	) );
	$wp_customize->add_control( 'gm_linkedin_url', array(
		'label'       => __( 'Confirmed LinkedIn profile URL', 'gm' ),
		'description' => __( 'Leave empty until confirmed. Do not add other profiles.', 'gm' ),
		'section'     => 'gm_entity',
		'type'        => 'url',
	) );

	$wp_customize->add_setting( 'gm_portrait_url', array(
		'default'           => '',
		'sanitize_callback' => 'esc_url_raw',
	) );
	$wp_customize->add_control( new WP_Customize_Image_Control( $wp_customize, 'gm_portrait_url', array(
		'label'   => __( 'Professional portrait', 'gm' ),
		'section' => 'gm_entity',
	) ) );

	$wp_customize->add_setting( 'gm_default_share_image', array(
		'default'           => '',
		'sanitize_callback' => 'esc_url_raw',
	) );
	$wp_customize->add_control( new WP_Customize_Image_Control( $wp_customize, 'gm_default_share_image', array(
		'label'   => __( 'Default social sharing image', 'gm' ),
		'section' => 'gm_entity',
	) ) );
}
add_action( 'customize_register', 'gm_customizer' );
