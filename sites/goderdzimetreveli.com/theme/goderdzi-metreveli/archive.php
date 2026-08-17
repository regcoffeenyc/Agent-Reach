<?php
/**
 * Article index and any archive view.
 *
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
			if ( is_home() ) {
				$gm_blog = (int) get_option( 'page_for_posts' );
				echo esc_html( $gm_blog ? (string) get_the_title( $gm_blog ) : ( $gm_ka ? 'სტატიები' : 'Articles and Insights' ) );
			} else {
				the_archive_title();
			}
			?>
		</h1>
		<p class="gm-pagehead__standfirst">
			<?php
			echo esc_html(
				$gm_ka
					? 'ტექნიკური ჩანაწერები ნიადაგის მომზადების, ბაღის გაშენების, ირიგაციის, მექანიზაციისა და გადამუშავების შესახებ — საველე გამოცდილებიდან.'
					: 'Technical notes on soil preparation, orchard establishment, irrigation, mechanization and processing — written from field practice.'
			);
			?>
		</p>
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
					<?php if ( has_post_thumbnail() ) : ?>
						<a class="gm-card__media" href="<?php the_permalink(); ?>" tabindex="-1" aria-hidden="true">
							<?php the_post_thumbnail( 'gm-card', array( 'sizes' => '(max-width: 800px) 100vw, 380px', 'loading' => 'lazy' ) ); ?>
						</a>
					<?php endif; ?>

					<p class="gm-card__meta">
						<time datetime="<?php echo esc_attr( (string) get_the_date( 'c' ) ); ?>"><?php echo esc_html( (string) get_the_date() ); ?></time>
						<span aria-hidden="true">·</span>
						<span><?php printf( esc_html( $gm_ka ? '%d წთ' : '%d min read' ), (int) gm_reading_time() ); ?></span>
					</p>

					<h2 class="gm-card__title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
					<p class="gm-card__text"><?php echo esc_html( wp_trim_words( (string) get_the_excerpt(), 26, '…' ) ); ?></p>
				</li>
				<?php
			endwhile;
			?>
		</ul>

		<?php
		the_posts_pagination( array(
			'mid_size'  => 1,
			'prev_text' => $gm_ka ? '← წინა' : '← Previous',
			'next_text' => $gm_ka ? 'შემდეგი →' : 'Next →',
			'class'     => 'gm-pagination',
		) );
		?>
	<?php else : ?>
		<p class="gm-prose"><?php echo esc_html( $gm_ka ? 'სტატიები ჯერ არ არის.' : 'No articles yet.' ); ?></p>
	<?php endif; ?>
</div>

<?php
get_footer();
