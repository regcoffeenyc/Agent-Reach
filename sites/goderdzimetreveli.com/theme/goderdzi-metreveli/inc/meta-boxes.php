<?php
/**
 * Editor fields for per-page SEO and the editorial metadata the templates use.
 *
 * Kept intentionally small — these are the only overrides the content strategy
 * actually needs. Everything else is derived.
 *
 * @package gm
 */

declare( strict_types = 1 );

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const GM_META_FIELDS = array(
	'seo_title'        => array( 'label' => 'SEO title',            'type' => 'text',     'help' => 'Aim for 50–60 characters. Overrides the generated <title>.' ),
	'meta_description' => array( 'label' => 'Meta description',     'type' => 'textarea', 'help' => 'Aim for 140–160 characters.' ),
	'canonical'        => array( 'label' => 'Canonical override',   'type' => 'url',      'help' => 'Leave empty unless this page genuinely duplicates another.' ),
	'primary_keyword'  => array( 'label' => 'Primary topic',        'type' => 'text',     'help' => 'One per page. See docs/09-keyword-map.md.' ),
	'last_reviewed'    => array( 'label' => 'Last reviewed (Y-m-d)','type' => 'text',     'help' => 'Shown on technical articles. Refresh at least annually.' ),
	'translation_of'   => array( 'label' => 'Translation of (post ID)', 'type' => 'text', 'help' => 'ID of the counterpart page in the other language. Drives hreflang if Polylang is not in use.' ),
	'noindex'          => array( 'label' => 'Exclude from search engines', 'type' => 'checkbox', 'help' => '' ),
	'is_profile_page'  => array( 'label' => 'Mark as ProfilePage',  'type' => 'checkbox', 'help' => 'Only the biography page should have this.' ),

	// Case-study template only.
	'cs_location'      => array( 'label' => 'Case study — location', 'type' => 'text', 'help' => '' ),
	'cs_period'        => array( 'label' => 'Case study — period',   'type' => 'text', 'help' => 'Only dates supported by documentation. See docs/07.' ),
	'cs_role'          => array( 'label' => 'Case study — role',     'type' => 'text', 'help' => 'Use only wording that published sources support.' ),
	'cs_scope'         => array( 'label' => 'Case study — scope',    'type' => 'text', 'help' => 'Figures must carry a source.' ),
);

function gm_add_meta_boxes(): void {
	add_meta_box(
		'gm_seo',
		__( 'Search and structured data', 'gm' ),
		'gm_render_meta_box',
		array( 'post', 'page' ),
		'normal',
		'high'
	);
}
add_action( 'add_meta_boxes', 'gm_add_meta_boxes' );

function gm_render_meta_box( WP_Post $post ): void {
	wp_nonce_field( 'gm_save_meta', 'gm_meta_nonce' );

	echo '<div class="gm-meta-fields" style="display:grid;gap:1rem;">';
	foreach ( GM_META_FIELDS as $key => $field ) {
		$value = (string) get_post_meta( $post->ID, '_gm_' . $key, true );
		$id    = 'gm_' . $key;

		echo '<p style="margin:0;">';
		printf( '<label for="%s"><strong>%s</strong></label><br />', esc_attr( $id ), esc_html( $field['label'] ) );

		switch ( $field['type'] ) {
			case 'textarea':
				printf(
					'<textarea id="%s" name="%s" rows="3" style="width:100%%;">%s</textarea>',
					esc_attr( $id ),
					esc_attr( $id ),
					esc_textarea( $value )
				);
				break;
			case 'checkbox':
				printf(
					'<input type="checkbox" id="%s" name="%s" value="on"%s />',
					esc_attr( $id ),
					esc_attr( $id ),
					checked( $value, 'on', false )
				);
				break;
			default:
				printf(
					'<input type="%s" id="%s" name="%s" value="%s" style="width:100%%;" />',
					esc_attr( 'url' === $field['type'] ? 'url' : 'text' ),
					esc_attr( $id ),
					esc_attr( $id ),
					esc_attr( $value )
				);
		}

		if ( $field['help'] ) {
			printf( '<br /><span class="description">%s</span>', esc_html( $field['help'] ) );
		}
		echo '</p>';
	}
	echo '</div>';
}

function gm_save_meta( int $post_id ): void {
	if ( ! isset( $_POST['gm_meta_nonce'] ) || ! wp_verify_nonce( sanitize_key( wp_unslash( $_POST['gm_meta_nonce'] ) ), 'gm_save_meta' ) ) {
		return;
	}
	if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
		return;
	}
	if ( ! current_user_can( 'edit_post', $post_id ) ) {
		return;
	}

	foreach ( GM_META_FIELDS as $key => $field ) {
		$input = 'gm_' . $key;
		$meta  = '_gm_' . $key;

		if ( 'checkbox' === $field['type'] ) {
			if ( isset( $_POST[ $input ] ) ) {
				update_post_meta( $post_id, $meta, 'on' );
			} else {
				delete_post_meta( $post_id, $meta );
			}
			continue;
		}

		$raw = isset( $_POST[ $input ] ) ? wp_unslash( $_POST[ $input ] ) : '';
		$raw = is_string( $raw ) ? $raw : '';

		$value = match ( $field['type'] ) {
			'url'      => esc_url_raw( $raw ),
			'textarea' => sanitize_textarea_field( $raw ),
			default    => sanitize_text_field( $raw ),
		};

		if ( '' === $value ) {
			delete_post_meta( $post_id, $meta );
		} else {
			update_post_meta( $post_id, $meta, $value );
		}
	}

	// Keep the hreflang pairing key in sync with the friendlier field name.
	$pair = (string) get_post_meta( $post_id, '_gm_translation_of', true );
	if ( ctype_digit( $pair ) && (int) $pair !== $post_id ) {
		update_post_meta( $post_id, '_gm_translation_of', (int) $pair );
	} else {
		delete_post_meta( $post_id, '_gm_translation_of' );
	}
}
add_action( 'save_post', 'gm_save_meta' );
