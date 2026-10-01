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

<header class="gm-pagehead">
	<div class="gm-container gm-container--narrow">
		<?php gm_breadcrumbs(); ?>
		<h1 class="gm-pagehead__title">
			<?php
			printf(
				esc_html( $gm_ka ? 'ძიების შედეგები: %s' : 'Search results for “%s”' ),
				esc_html( (string) get_search_query() )
			);
			?>
		</h1>
		<?php get_search_form(); ?>
	</div>
</header>

<div class="gm-container">
	<?php if ( have_posts() ) : ?>
		<ul class="gm-grid gm-grid--3 gm-archive">
			<?php
			while ( have_posts() ) :
				the_post();
				?>
				<li class="gm-card gm-card--article">
					<h2 class="gm-card__title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
					<p class="gm-card__text"><?php echo esc_html( wp_trim_words( (string) get_the_excerpt(), 26, '…' ) ); ?></p>
				</li>
				<?php
			endwhile;
			?>
		</ul>
		<?php the_posts_pagination( array( 'mid_size' => 1, 'class' => 'gm-pagination' ) ); ?>
	<?php else : ?>
		<p class="gm-prose"><?php echo esc_html( $gm_ka ? 'შედეგები ვერ მოიძებნა.' : 'No results found.' ); ?></p>
	<?php endif; ?>
</div>

<?php
get_footer();
