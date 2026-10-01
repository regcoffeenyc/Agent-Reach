<?php
/**
 * Technical article.
 *
 * Implements the per-article requirements from the brief: author name, link to
 * the biography, publication date, last-reviewed date, and related reading. The
 * "first-hand vs general guidance" separation is a content convention, supported
 * here by the .gm-firsthand block style.
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

	$gm_reviewed = gm_field( 'last_reviewed' );
	?>

	<article class="gm-article">

		<header class="gm-pagehead">
			<div class="gm-container gm-container--narrow">
				<?php gm_breadcrumbs(); ?>

				<?php
				$gm_terms = get_the_terms( get_the_ID(), 'category' );
				if ( $gm_terms && ! is_wp_error( $gm_terms ) ) :
					?>
					<p class="gm-article__kicker"><?php echo esc_html( $gm_terms[0]->name ); ?></p>
				<?php endif; ?>

				<h1 class="gm-pagehead__title"><?php the_title(); ?></h1>

				<?php if ( has_excerpt() ) : ?>
					<p class="gm-pagehead__standfirst"><?php echo esc_html( (string) get_the_excerpt() ); ?></p>
				<?php endif; ?>

				<div class="gm-byline">
					<p class="gm-byline__author">
						<?php echo esc_html( $gm_ka ? 'ავტორი: ' : 'By ' ); ?>
						<a href="<?php echo esc_url( gm_profile_url() ); ?>" rel="author">Goderdzi Metreveli</a>
					</p>
					<p class="gm-byline__dates">
						<time datetime="<?php echo esc_attr( (string) get_the_date( 'c' ) ); ?>">
							<?php echo esc_html( ( $gm_ka ? 'გამოქვეყნდა ' : 'Published ' ) . get_the_date() ); ?>
						</time>
						<?php if ( $gm_reviewed ) : ?>
							<span aria-hidden="true">·</span>
							<time datetime="<?php echo esc_attr( $gm_reviewed ); ?>">
								<?php echo esc_html( ( $gm_ka ? 'ბოლოს გადამოწმდა ' : 'Last reviewed ' ) . $gm_reviewed ); ?>
							</time>
						<?php endif; ?>
						<span aria-hidden="true">·</span>
						<span><?php printf( esc_html( $gm_ka ? '%d წთ კითხვა' : '%d min read' ), (int) gm_reading_time() ); ?></span>
					</p>
				</div>
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

			<?php /* Author box — every article links back to the ProfilePage. */ ?>
			<aside class="gm-authorbox">
				<h2 class="gm-authorbox__title"><?php echo esc_html( $gm_ka ? 'ავტორის შესახებ' : 'About the author' ); ?></h2>
				<p>
					<?php
					echo esc_html(
						$gm_ka
							? 'გოდერძი მეტრეველი არის სოფლის მეურნეობის ხელმძღვანელი და საინჟინრო პროფესიონალი, რომელიც მუშაობს ფართომასშტაბიან ბაღების გაშენებაზე, ნიადაგის მომზადებაზე, ირიგაციასა და მექანიზაციაზე საქართველოს ნახევრად მშრალ რეგიონებში.'
							: 'Goderdzi Metreveli is an agricultural executive and engineering professional working on large-scale orchard development, soil preparation, irrigation infrastructure and mechanization in semi-arid Georgia.'
					);
					?>
				</p>
				<p>
					<a class="gm-arrowlink" href="<?php echo esc_url( gm_profile_url() ); ?>">
						<?php echo esc_html( $gm_ka ? 'სრული ბიოგრაფია' : 'Read the full biography' ); ?>
					</a>
				</p>
			</aside>

			<?php
			// Related: same category, excluding this post.
			$gm_cats = wp_get_post_categories( (int) get_the_ID() );
			if ( $gm_cats ) :
				$gm_related = new WP_Query( array(
					'post_type'           => 'post',
					'posts_per_page'      => 3,
					'post__not_in'        => array( (int) get_the_ID() ),
					'category__in'        => $gm_cats,
					'ignore_sticky_posts' => true,
					'no_found_rows'       => true,
				) );
				if ( $gm_related->have_posts() ) :
					?>
					<aside class="gm-related">
						<h2 class="gm-related__title"><?php echo esc_html( $gm_ka ? 'დაკავშირებული სტატიები' : 'Related reading' ); ?></h2>
						<ul class="gm-grid gm-grid--3">
							<?php
							while ( $gm_related->have_posts() ) :
								$gm_related->the_post();
								?>
								<li class="gm-card gm-card--article">
									<h3 class="gm-card__title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3>
								</li>
								<?php
							endwhile;
							wp_reset_postdata();
							?>
						</ul>
					</aside>
					<?php
				endif;
			endif;
			?>
		</div>

	</article>

	<?php
endwhile;

get_footer();
