<?php
/**
 * @package gm
 */

declare( strict_types = 1 );

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

$gm_id = 'gm-search-' . wp_rand();
$gm_ka = 'ka' === gm_current_lang();
?>
<form role="search" method="get" class="gm-searchform" action="<?php echo esc_url( home_url( '/' ) ); ?>">
	<label for="<?php echo esc_attr( $gm_id ); ?>" class="screen-reader-text">
		<?php echo esc_html( $gm_ka ? 'ძიება საიტზე' : 'Search this site' ); ?>
	</label>
	<input
		id="<?php echo esc_attr( $gm_id ); ?>"
		type="search"
		class="gm-searchform__input"
		placeholder="<?php echo esc_attr( $gm_ka ? 'ძიება…' : 'Search…' ); ?>"
		value="<?php echo esc_attr( (string) get_search_query() ); ?>"
		name="s" />
	<button type="submit" class="gm-btn gm-btn--small">
		<?php echo esc_html( $gm_ka ? 'ძიება' : 'Search' ); ?>
	</button>
</form>
