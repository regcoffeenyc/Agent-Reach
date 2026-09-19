<?php
/**
 * @package gm
 */

declare( strict_types = 1 );

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

$gm_ka = 'ka' === gm_current_lang();
?>
</main>

<footer class="gm-footer" role="contentinfo">
	<div class="gm-container">

		<div class="gm-footer__cols">

			<div class="gm-footer__col">
				<h2 class="gm-footer__heading"><?php echo esc_html( $gm_ka ? 'თემები' : 'Topics' ); ?></h2>
				<?php
				wp_nav_menu( array(
					'theme_location' => gm_menu_location( 'footer_topics' ),
					'container'      => false,
					'menu_class'     => 'gm-footer__list',
					'depth'          => 1,
					'fallback_cb'    => false,
				) );
				?>
			</div>

			<div class="gm-footer__col">
				<h2 class="gm-footer__heading"><?php echo esc_html( $gm_ka ? 'შესახებ' : 'About' ); ?></h2>
				<?php
				wp_nav_menu( array(
					'theme_location' => gm_menu_location( 'footer_about' ),
					'container'      => false,
					'menu_class'     => 'gm-footer__list',
					'depth'          => 1,
					'fallback_cb'    => false,
				) );
				?>
			</div>

			<div class="gm-footer__col">
				<h2 class="gm-footer__heading"><?php echo esc_html( $gm_ka ? 'კონტაქტი' : 'Contact' ); ?></h2>
				<p class="gm-footer__text">
					<?php
					echo esc_html(
						$gm_ka
							? 'კონსულტაცია, ტრენინგები, საჯარო გამოსვლები და მედია მიმართვები.'
							: 'Consulting, training, speaking and media enquiries.'
					);
					?>
				</p>
				<p>
					<a class="gm-btn gm-btn--ghost" href="<?php echo esc_url( $gm_ka ? home_url( '/ka/kontakti/' ) : home_url( '/contact/' ) ); ?>">
						<?php echo esc_html( $gm_ka ? 'დაკავშირება' : 'Get in touch' ); ?>
					</a>
				</p>
				<?php echo gm_language_switch(); // phpcs:ignore WordPress.Security.EscapeOutput ?>
			</div>

		</div>

		<?php
		/*
		 * Section 11 of the brief. Appears site-wide rather than on the homepage
		 * only — the claim it qualifies (that project outcomes were team
		 * outcomes) is made on every page that describes a project, so the
		 * qualifier belongs everywhere too.
		 */
		?>
		<div class="gm-disclaimer">
			<h2 class="gm-disclaimer__heading"><?php echo esc_html( $gm_ka ? 'პროფესიული განმარტება' : 'Professional note' ); ?></h2>
			<p>
				<?php
				echo esc_html(
					$gm_ka
						? 'ამ საიტზე აღწერილი პროექტები განხორციელდა მრავალდისციპლინური გუნდების მიერ — თანამშრომლების, აგრონომების, ინჟინრების, კონტრაქტორების, კონსულტანტებისა და პარტნიორი ორგანიზაციების ჩათვლით. აქ აღწერილია გოდერძი მეტრეველის როლი ამ საერთო სამუშაოში და არა ინდივიდუალური ავტორობა. ორგანიზაციული მიღწევები აღნიშნულია, როგორც ორგანიზაციული.'
						: 'The projects described on this site were delivered by multidisciplinary teams — employees, agronomists, engineers, contractors, consultants and partner organisations. What is described here is Goderdzi Metreveli’s role within that shared work, not individual authorship of it. Achievements belonging to an organisation are identified as organisational.'
				);
				?>
			</p>
		</div>

		<div class="gm-footer__bottom">
			<p class="gm-footer__copy">
				&copy; <?php echo esc_html( (string) gmdate( 'Y' ) ); ?> Goderdzi Metreveli
			</p>
			<p class="gm-footer__meta">
				<?php
				echo esc_html(
					$gm_ka
						? 'ყველა ციფრი მითითებულია წყაროსთან ან გადამოწმების სტატუსთან ერთად.'
						: 'Every figure on this site is published with a source or a verification status.'
				);
				?>
			</p>
		</div>

	</div>
</footer>

<?php wp_footer(); ?>
</body>
</html>
