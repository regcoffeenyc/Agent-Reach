<?php
/**
 * Template Name: Case study
 *
 * Adds a project metadata block and a standing note that the work described was
 * delivered by a team. Both are mandatory on this template — a case study that
 * reads as a solo achievement is the specific failure mode this site avoids.
 *
 * Project metadata is read from post meta so it can be edited without code:
 *   _gm_cs_location, _gm_cs_period, _gm_cs_role, _gm_cs_scope, _gm_cs_status
 *
 * @package gm
 */

declare( strict_types = 1 );

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();

$gm_ka = 'ka' === gm_current_lang();

while ( have_posts() ) :
	the_post();

	$gm_facts = array_filter( array(
		( $gm_ka ? 'ადგილმდებარეობა' : 'Location' ) => gm_field( 'cs_location' ),
		( $gm_ka ? 'პერიოდი' : 'Period' )           => gm_field( 'cs_period' ),
		( $gm_ka ? 'როლი' : 'Role' )                 => gm_field( 'cs_role' ),
		( $gm_ka ? 'მასშტაბი' : 'Scope' )            => gm_field( 'cs_scope' ),
	) );
	?>

	<article class="gm-page gm-page--case">

		<header class="gm-pagehead gm-pagehead--case">
			<div class="gm-container gm-container--narrow">
				<?php gm_breadcrumbs(); ?>
				<p class="gm-article__kicker"><?php echo esc_html( $gm_ka ? 'შემთხვევის ანალიზი' : 'Case study' ); ?></p>
				<h1 class="gm-pagehead__title"><?php the_title(); ?></h1>
				<?php if ( has_excerpt() ) : ?>
					<p class="gm-pagehead__standfirst"><?php echo esc_html( (string) get_the_excerpt() ); ?></p>
				<?php endif; ?>
			</div>
		</header>

		<?php if ( has_post_thumbnail() ) : ?>
			<figure class="gm-featured gm-container">
				<?php the_post_thumbnail( 'gm-hero', array( 'sizes' => '(max-width: 1200px) 100vw, 1200px' ) ); ?>
				<?php if ( wp_get_attachment_caption( (int) get_post_thumbnail_id() ) ) : ?>
					<figcaption><?php echo esc_html( (string) wp_get_attachment_caption( (int) get_post_thumbnail_id() ) ); ?></figcaption>
				<?php endif; ?>
			</figure>
		<?php endif; ?>

		<div class="gm-container gm-container--narrow">

			<?php if ( $gm_facts ) : ?>
				<dl class="gm-projectmeta">
					<?php foreach ( $gm_facts as $gm_label => $gm_value ) : ?>
						<div class="gm-projectmeta__row">
							<dt><?php echo esc_html( (string) $gm_label ); ?></dt>
							<dd><?php echo esc_html( (string) $gm_value ); ?></dd>
						</div>
					<?php endforeach; ?>
				</dl>
			<?php endif; ?>

			<div class="gm-prose">
				<?php the_content(); ?>
			</div>

			<aside class="gm-teamnote">
				<p>
					<?php
					echo esc_html(
						$gm_ka
							? 'აქ აღწერილი სამუშაო შესრულდა მრავალდისციპლინური გუნდის მიერ — აგრონომების, ინჟინრების, ოპერატორების, კონტრაქტორებისა და პარტნიორი ორგანიზაციების ჩართულობით. აღწერილია გოდერძი მეტრეველის როლი ამ საერთო სამუშაოში.'
							: 'The work described here was carried out by a multidisciplinary team of agronomists, engineers, machine operators, contractors and partner organisations. What is described is Goderdzi Metreveli’s role within that shared effort.'
					);
					?>
				</p>
			</aside>

		</div>

	</article>

	<?php
endwhile;

get_footer();
