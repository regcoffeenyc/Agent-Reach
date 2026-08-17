<?php
/**
 * @package gm
 */

declare( strict_types = 1 );

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}
?>
<!doctype html>
<html <?php language_attributes(); ?>>
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>" />
	<meta name="viewport" content="width=device-width, initial-scale=1" />
	<?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<a class="gm-skip" href="#main"><?php esc_html_e( 'Skip to content', 'gm' ); ?></a>

<header class="gm-header" role="banner">
	<div class="gm-header__inner gm-container">

		<p class="gm-brand">
			<a href="<?php echo esc_url( 'ka' === gm_current_lang() ? home_url( '/ka/' ) : home_url( '/' ) ); ?>">
				<span class="gm-brand__name">Goderdzi Metreveli</span>
				<span class="gm-brand__role">
					<?php
					echo esc_html(
						'ka' === gm_current_lang()
							? 'რეგენერაციული სოფლის მეურნეობა · ნუშის ბაღები'
							: 'Regenerative Agriculture · Almond Orchards'
					);
					?>
				</span>
			</a>
		</p>

		<button class="gm-navtoggle" type="button" aria-expanded="false" aria-controls="gm-primary-nav">
			<span class="gm-navtoggle__bars" aria-hidden="true"></span>
			<span class="screen-reader-text"><?php esc_html_e( 'Menu', 'gm' ); ?></span>
		</button>

		<nav id="gm-primary-nav" class="gm-nav" aria-label="<?php esc_attr_e( 'Primary', 'gm' ); ?>">
			<?php
			wp_nav_menu( array(
				'theme_location' => gm_menu_location( 'primary' ),
				'container'      => false,
				'menu_class'     => 'gm-nav__list',
				'depth'          => 2,
				'fallback_cb'    => false,
			) );
			?>
			<?php echo gm_language_switch(); // phpcs:ignore WordPress.Security.EscapeOutput -- built from escaped parts. ?>
		</nav>

	</div>
</header>

<main id="main" class="gm-main" role="main">
