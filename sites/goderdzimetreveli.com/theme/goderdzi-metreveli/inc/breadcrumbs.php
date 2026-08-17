<?php
/**
 * Breadcrumbs — visible trail and the data behind the BreadcrumbList JSON-LD.
 *
 * gm_breadcrumb_items() is the single source; both the markup and the schema
 * read from it, so they can never disagree.
 *
 * @package gm
 */

declare( strict_types = 1 );

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * @return array<int, array{label:string, url:string}> Last item has an empty url.
 */
function gm_breadcrumb_items(): array {
	$ka   = 'ka' === gm_current_lang();
	$home = $ka ? 'მთავარი' : 'Home';

	$home_url = $ka
		? (string) ( ( $p = get_page_by_path( 'ka' ) ) ? get_permalink( $p ) : home_url( '/ka/' ) )
		: trailingslashit( home_url( '/' ) );

	$items = array( array( 'label' => $home, 'url' => $home_url ) );

	if ( is_front_page() ) {
		return array();
	}

	if ( is_singular( 'post' ) ) {
		$blog_id = (int) get_option( 'page_for_posts' );
		$items[] = array(
			'label' => $blog_id ? (string) get_the_title( $blog_id ) : ( $ka ? 'სტატიები' : 'Articles' ),
			'url'   => $blog_id ? (string) get_permalink( $blog_id ) : home_url( '/articles/' ),
		);
		$items[] = array( 'label' => wp_strip_all_tags( (string) get_the_title() ), 'url' => '' );
		return $items;
	}

	if ( is_page() ) {
		/*
		 * Georgian pages are children of the /ka/ page so that their URL paths
		 * nest correctly. That page IS the Georgian home, and it is already the
		 * first crumb — so walking ancestors naively renders "Home" twice, as
		 * "მთავარი › გოდერძი მეტრეველი › …". Skip any ancestor that is the
		 * language home, and skip the site front page for the same reason.
		 */
		$lang_home_id = 0;
		if ( $ka ) {
			$ka_home      = get_page_by_path( 'ka' );
			$lang_home_id = $ka_home ? (int) $ka_home->ID : 0;
		}
		$front_id = (int) get_option( 'page_on_front' );

		$ancestors = array_reverse( get_post_ancestors( (int) get_the_ID() ) );
		foreach ( $ancestors as $ancestor_id ) {
			$ancestor_id = (int) $ancestor_id;
			if ( $ancestor_id === $lang_home_id || $ancestor_id === $front_id ) {
				continue;
			}
			$items[] = array(
				'label' => wp_strip_all_tags( (string) get_the_title( $ancestor_id ) ),
				'url'   => (string) get_permalink( $ancestor_id ),
			);
		}

		/*
		 * Pillar pages sit under Expertise conceptually but live at the root for
		 * URL brevity. Insert the intermediate crumb so the trail matches the
		 * information architecture rather than the flat URL.
		 */
		$pillars = array(
			// English.
			'regenerative-agriculture', 'almond-orchards', 'deep-ripping',
			'irrigation-infrastructure', 'mechanization', 'almond-processing-export',
			// Georgian.
			'regeneratsiuli-sofmeurneoba', 'nushis-baghebi', 'ghrma-gafkhviereba',
			'irigatsia-infrastruktura', 'mekanizatsia', 'gadamushaveba-eksporti',
		);
		$slug = (string) get_post_field( 'post_name', (int) get_the_ID() );
		if ( in_array( $slug, $pillars, true ) ) {
			$expertise = get_page_by_path( $ka ? 'ka/spetsializatsia' : 'expertise' );
			if ( $expertise ) {
				$items[] = array(
					'label' => wp_strip_all_tags( (string) get_the_title( $expertise ) ),
					'url'   => (string) get_permalink( $expertise ),
				);
			}
		}

		$items[] = array( 'label' => wp_strip_all_tags( (string) get_the_title() ), 'url' => '' );
		return $items;
	}

	if ( is_home() ) {
		$items[] = array( 'label' => $ka ? 'სტატიები' : 'Articles', 'url' => '' );
		return $items;
	}

	if ( is_category() || is_tag() || is_tax() ) {
		$items[] = array( 'label' => wp_strip_all_tags( (string) single_term_title( '', false ) ), 'url' => '' );
		return $items;
	}

	if ( is_search() ) {
		$items[] = array( 'label' => ( $ka ? 'ძიება: ' : 'Search: ' ) . esc_html( (string) get_search_query() ), 'url' => '' );
		return $items;
	}

	if ( is_404() ) {
		$items[] = array( 'label' => $ka ? 'გვერდი ვერ მოიძებნა' : 'Page not found', 'url' => '' );
	}

	return $items;
}

/**
 * Visible breadcrumb trail.
 */
function gm_breadcrumbs(): void {
	$items = gm_breadcrumb_items();
	if ( count( $items ) < 2 ) {
		return;
	}

	$label = 'ka' === gm_current_lang() ? 'ნავიგაციის გზა' : 'Breadcrumb';

	echo '<nav class="gm-breadcrumbs" aria-label="' . esc_attr( $label ) . '"><ol>';
	foreach ( $items as $item ) {
		if ( $item['url'] ) {
			printf(
				'<li><a href="%s">%s</a></li>',
				esc_url( $item['url'] ),
				esc_html( $item['label'] )
			);
		} else {
			printf( '<li><span aria-current="page">%s</span></li>', esc_html( $item['label'] ) );
		}
	}
	echo '</ol></nav>';
}
