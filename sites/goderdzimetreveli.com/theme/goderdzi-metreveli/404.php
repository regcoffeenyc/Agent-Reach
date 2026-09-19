<?php
/**
 * @package gm
 */

declare( strict_types = 1 );

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();

$gm_ka = 'ka' === gm_current_lang();
?>

<div class="gm-container gm-container--narrow gm-404">
	<h1 class="gm-pagehead__title"><?php echo esc_html( $gm_ka ? 'გვერდი ვერ მოიძებნა' : 'Page not found' ); ?></h1>
	<p class="gm-prose">
		<?php
		echo esc_html(
			$gm_ka
				? 'შესაძლოა ბმული შეიცვალა. სცადეთ ქვემოთ მოცემული განყოფილებები.'
				: 'The link may have changed. These sections cover most of what is here.'
		);
		?>
	</p>

	<ul class="gm-404__links">
		<li><a href="<?php echo esc_url( $gm_ka ? home_url( '/ka/shesakheb/' ) : home_url( '/about/' ) ); ?>"><?php echo esc_html( $gm_ka ? 'ბიოგრაფია' : 'Biography' ); ?></a></li>
		<li><a href="<?php echo esc_url( $gm_ka ? home_url( '/ka/spetsializatsia/' ) : home_url( '/expertise/' ) ); ?>"><?php echo esc_html( $gm_ka ? 'სპეციალიზაცია' : 'Expertise' ); ?></a></li>
		<li><a href="<?php echo esc_url( home_url( '/articles/' ) ); ?>"><?php echo esc_html( $gm_ka ? 'სტატიები' : 'Articles' ); ?></a></li>
		<li><a href="<?php echo esc_url( $gm_ka ? home_url( '/ka/kontakti/' ) : home_url( '/contact/' ) ); ?>"><?php echo esc_html( $gm_ka ? 'კონტაქტი' : 'Contact' ); ?></a></li>
	</ul>

	<?php get_search_form(); ?>
</div>

<?php
get_footer();
