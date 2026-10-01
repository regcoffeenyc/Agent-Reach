<?php
/**
 * Template Name: Pillar page
 *
 * A pillar page plus the cluster of supporting articles that link up to it.
 * Set the page's "Primary topic" field to the category slug of its cluster
 * (see docs/09-keyword-map.md) and the supporting articles list builds itself.
 *
 * @package gm
 */

declare( strict_types = 1 );

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();

$gm_ka = 'ka' === gm_current_lang();

/*
 * Map pillar slug → cluster category slug. Kept here rather than in a field so
 * the relationship is under version control alongside the keyword map.
 */
$gm_clusters = array(
	'regenerative-agriculture'  => 'regenerative-agriculture',
	'almond-orchards'           => 'almond-orchards',
	'deep-ripping'              => 'soil-preparation',
	'irrigation-infrastructure' => 'irrigation-infrastructure',
	'mechanization'             => 'irrigation-infrastructure',
	'almond-processing-export'  => 'processing-export',
);

while ( have_posts() ) :
	the_post();

	$gm_slug     = (string) get_post_field( 'post_name', (int) get_the_ID() );
	$gm_category = $gm_clusters[ $gm_slug ] ?? '';
	?>

	<article class="gm-page gm-page--pillar">

		<header class="gm-pagehead gm-pagehead--pillar">
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

		<?php
		if ( $gm_category ) :
			$gm_cluster = new WP_Query( array(
				'post_type'           => 'post',
				'posts_per_page'      => 12,
				'category_name'       => $gm_category,
				'ignore_sticky_posts' => true,
				'no_found_rows'       => true,
				'orderby'             => 'menu_order date',
				'order'               => 'ASC',
			) );

			if ( $gm_cluster->have_posts() ) :
				?>
				<section class="gm-section gm-section--alt" aria-labelledby="gm-cluster-title">
					<div class="gm-container">
						<h2 id="gm-cluster-title" class="gm-section__title">
							<?php echo esc_html( $gm_ka ? 'ამ თემის ტექნიკური სტატიები' : 'Technical articles on this topic' ); ?>
						</h2>
						<ul class="gm-grid gm-grid--3">
							<?php
							while ( $gm_cluster->have_posts() ) :
								$gm_cluster->the_post();
								?>
								<li class="gm-card gm-card--article">
									<p class="gm-card__meta">
										<time datetime="<?php echo esc_attr( (string) get_the_date( 'c' ) ); ?>"><?php echo esc_html( (string) get_the_date() ); ?></time>
									</p>
									<h3 class="gm-card__title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3>
									<p class="gm-card__text"><?php echo esc_html( wp_trim_words( (string) get_the_excerpt(), 22, '…' ) ); ?></p>
								</li>
								<?php
							endwhile;
							wp_reset_postdata();
							?>
						</ul>
					</div>
				</section>
				<?php
			endif;
		endif;
		?>

		<section class="gm-cta gm-cta--compact">
			<div class="gm-container gm-container--narrow">
				<h2 class="gm-cta__title"><?php echo esc_html( $gm_ka ? 'გაქვთ კითხვა ამ თემაზე?' : 'Working on something like this?' ); ?></h2>
				<p class="gm-cta__text">
					<?php
					echo esc_html(
						$gm_ka
							? 'კონსულტაციისა და ტრენინგის მიმართვები მიიღება ქართულ და ინგლისურ ენებზე.'
							: 'Consulting and training enquiries are welcome in Georgian and English.'
					);
					?>
				</p>
				<p><a class="gm-btn" href="<?php echo esc_url( $gm_ka ? home_url( '/ka/kontakti/' ) : home_url( '/contact/' ) ); ?>"><?php echo esc_html( $gm_ka ? 'დაკავშირება' : 'Get in touch' ); ?></a></p>
			</div>
		</section>

	</article>

	<?php
endwhile;

get_footer();
