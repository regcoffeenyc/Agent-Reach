<?php
/**
 * Default page template.
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

	<article class="gm-page">
		<header class="gm-pagehead">
			<div class="gm-container gm-container--narrow">
				<?php gm_breadcrumbs(); ?>
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
			<div class="gm-prose">
				<?php the_content(); ?>
			</div>
		</div>
	</article>

	<?php
endwhile;

get_footer();
