<?php
/**
 * Template Name: Wide (evidence gallery)
 *
 * Full-width content column for the evidence and project gallery, where image
 * grids need more room than the reading measure allows.
 *
 * @package gm
 */

declare( strict_types = 1 );

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();

while ( have_posts() ) :
	the_post();
	?>

	<article class="gm-page gm-page--wide">

		<header class="gm-pagehead">
			<div class="gm-container gm-container--narrow">
				<?php gm_breadcrumbs(); ?>
				<h1 class="gm-pagehead__title"><?php the_title(); ?></h1>
				<?php if ( has_excerpt() ) : ?>
					<p class="gm-pagehead__standfirst"><?php echo esc_html( (string) get_the_excerpt() ); ?></p>
				<?php endif; ?>
			</div>
		</header>

		<div class="gm-container">
			<div class="gm-prose gm-prose--wide">
				<?php the_content(); ?>
			</div>
		</div>

	</article>

	<?php
endwhile;

get_footer();
