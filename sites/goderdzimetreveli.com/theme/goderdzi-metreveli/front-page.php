<?php
/**
 * Homepage — the 11 sections specified in the brief.
 *
 * Editable content lives in three places:
 *   - Section 2 biography: the Home page's own editor content.
 *   - Section 4 metrics: the $gm_metrics array below. Every entry MUST carry a
 *     verification label; gm_verification_label() is the only way to render one,
 *     and there is deliberately no path that renders a bare number.
 *   - Everything else: menus, the latest-articles query, and the strings here.
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
 * Section 4 — selected project metrics.
 *
 * Sourced directly from docs/07-fact-verification-report.md. Read that document
 * before changing a number here.
 *
 * Note what is absent: no total-landholding figure, because published sources
 * range from 4,000 to 20,000 hectares and the 20,000 figure is self-reported
 * and uncorroborated (report §3.2). No processing-capacity figure, because the
 * only published figure (2.5 t/h) contradicts the supplied record (14–15 t/h)
 * by roughly six times (report §3.4). Those numbers return here only when
 * primary documentation resolves them.
 */
$gm_metrics = array(
	array(
		'value'  => $gm_ka ? '≈2,300 ჰა' : '≈2,300 ha',
		'label'  => $gm_ka ? 'ნუშის ბაღი' : 'Almond orchard',
		'status' => 'sourced',
		'note'   => $gm_ka ? 'EastFruit, 2021 · Investor.ge, 2022' : 'EastFruit 2021 · Investor.ge 2022',
		'url'    => 'https://east-fruit.com/en/news/almonds-harvesting-in-georgias-largest-orchard-video/',
	),
	array(
		'value'  => '675,000+',
		'label'  => $gm_ka ? 'დარგული ნუშის ხე' : 'Almond trees planted',
		'status' => 'attributed',
		'note'   => $gm_ka ? 'Investor.ge, 2022' : 'Reported by Investor.ge, 2022',
		'url'    => 'https://www.investor.ge/2022/04/18/the-changing-landscape-of-georgian-agriculture/',
	),
	array(
		'value'  => $gm_ka ? '800 ტ' : '800 t',
		'label'  => $gm_ka ? '2021 წლის მოსავალი (გაუტეხავი)' : '2021 crop, in-shell',
		'status' => 'attributed',
		'note'   => $gm_ka ? 'Investor.ge, 2022 — კომპანიის მონაცემი' : 'Reported by Investor.ge, 2022',
		'url'    => 'https://www.investor.ge/2022/04/18/the-changing-landscape-of-georgian-agriculture/',
	),
	array(
		'value'  => 'SDG 12',
		'label'  => $gm_ka ? '2023 — ორგანიზაციული ჯილდო' : '2023 award — organisational',
		'status' => 'sourced',
		'note'   => $gm_ka ? 'UN Global Compact Network Georgia' : 'UN Global Compact Network Georgia',
		'url'    => 'https://unglobalcompact.ge/en/korporaciuli-mdgradobis-jildo-biznesi-mdgradi-ganvitarebistvis-gamarjvebulebi-cnobilia/',
	),
);

/* Section 3 — four areas of expertise. */
$gm_expertise = array(
	array(
		'title' => $gm_ka ? 'რეგენერაციული და ნახევრად მშრალი მეურნეობა' : 'Regenerative and Semi-Arid Agriculture',
		'text'  => $gm_ka
			? 'ნიადაგის ფუნქციის აღდგენა და ეროზიის შემცირება მცირე ნალექიან, დაბალი ორგანული ნივთიერების მქონე მიწებზე — კომერციულ მასშტაბში.'
			: 'Restoring soil function and reducing erosion on low-rainfall, low-organic-matter land — at commercial scale, under commercial constraints.',
		'url'   => $gm_ka ? '/ka/regeneratsiuli-sofmeurneoba/' : '/regenerative-agriculture/',
	),
	array(
		'title' => $gm_ka ? 'ფართომასშტაბიანი ნუშის ბაღები' : 'Large-Scale Almond Orchards',
		'text'  => $gm_ka
			? 'ბაღის დაგეგმვა, ჯიშების შერჩევა, დარგვა და მოსავლის ლოგისტიკა ათასობით ჰექტარზე.'
			: 'Orchard planning, variety selection, establishment and harvest logistics across thousands of hectares.',
		'url'   => $gm_ka ? '/ka/nushis-baghebi/' : '/almond-orchards/',
	),
	array(
		'title' => $gm_ka ? 'ნიადაგის მომზადება და ღრმა გაფხვიერება' : 'Soil Preparation and Deep Ripping',
		'text'  => $gm_ka
			? 'შემზღუდავი ფენების იდენტიფიცირება და მათი გახსნა დარგვამდე — სწორ ტენიანობაზე, სწორი სიღრმით.'
			: 'Identifying restrictive layers and opening them before planting — at the right moisture, to the right depth, in the right direction.',
		'url'   => $gm_ka ? '/ka/ghrma-gafkhviereba/' : '/deep-ripping/',
	),
	array(
		'title' => $gm_ka ? 'ირიგაცია, მექანიზაცია და გადამუშავება' : 'Irrigation, Mechanization and Processing',
		'text'  => $gm_ka
			? 'წყლის ინფრასტრუქტურა, მაღალი სიმძლავრის ტექნიკის შერჩევა და მოსავლიდან პროდუქტამდე ჯაჭვის აწყობა.'
			: 'Water infrastructure, high-horsepower fleet selection, and building the chain from harvest to finished product.',
		'url'   => $gm_ka ? '/ka/gadamushaveba-eksporti/' : '/almond-processing-export/',
	),
);
?>

<?php /* ---------- Section 1: portrait, name, positioning ---------- */ ?>
<section class="gm-hero" aria-labelledby="gm-hero-title">
	<div class="gm-container gm-hero__inner">

		<div class="gm-hero__text">
			<p class="gm-hero__eyebrow">
				<?php
				echo esc_html(
					$gm_ka
						? 'სოფლის მეურნეობის ხელმძღვანელი · საინჟინრო პროფესიონალი'
						: 'Agricultural Executive · Engineering Professional'
				);
				?>
			</p>

			<h1 id="gm-hero-title" class="gm-hero__title">
				<?php
				echo esc_html(
					$gm_ka
						? 'გოდერძი მეტრეველი — რეგენერაციული სოფლის მეურნეობა, ნუშის ბაღები და ნახევრად მშრალი მიწების ათვისება'
						: 'Goderdzi Metreveli — Regenerative Agriculture, Almond Orchards and Semi-Arid Land Development'
				);
				?>
			</h1>

			<p class="gm-hero__tagline">
				<?php
				echo esc_html(
					$gm_ka
						? 'რთული მიწის გარდაქმნა პროდუქტიულ, მდგრად და კომერციულად სიცოცხლისუნარიან სასოფლო-სამეურნეო სისტემად.'
						: 'Transforming challenging land into productive, resilient and commercially sustainable agricultural systems.'
				);
				?>
			</p>

			<p class="gm-hero__actions">
				<a class="gm-btn" href="<?php echo esc_url( $gm_ka ? home_url( '/ka/shesakheb/' ) : home_url( '/about/' ) ); ?>">
					<?php echo esc_html( $gm_ka ? 'ბიოგრაფია' : 'Read the biography' ); ?>
				</a>
				<a class="gm-btn gm-btn--ghost" href="<?php echo esc_url( $gm_ka ? home_url( '/ka/spetsializatsia/' ) : home_url( '/expertise/' ) ); ?>">
					<?php echo esc_html( $gm_ka ? 'სპეციალიზაცია' : 'Areas of expertise' ); ?>
				</a>
			</p>
		</div>

		<?php $gm_portrait = (string) get_theme_mod( 'gm_portrait_url', '' ); ?>
		<?php if ( $gm_portrait ) : ?>
			<figure class="gm-hero__portrait">
				<img
					src="<?php echo esc_url( $gm_portrait ); ?>"
					alt="<?php esc_attr_e( 'Goderdzi Metreveli photographed in an almond orchard', 'gm' ); ?>"
					width="900" height="1125"
					fetchpriority="high" decoding="sync" />
			</figure>
		<?php else : ?>
			<?php /* Degrades to a typographic mark rather than a stock photo — see docs/08. */ ?>
			<div class="gm-hero__portrait gm-hero__portrait--placeholder" aria-hidden="true"><span>GM</span></div>
		<?php endif; ?>

	</div>
</section>

<?php /* ---------- Section 2: short biography (120–160 words) ---------- */ ?>
<section class="gm-section gm-section--bio" aria-labelledby="gm-bio-title">
	<div class="gm-container gm-container--narrow">
		<h2 id="gm-bio-title" class="gm-section__title"><?php echo esc_html( $gm_ka ? 'მოკლედ' : 'In brief' ); ?></h2>
		<div class="gm-prose gm-prose--lead">
			<?php
			// The Home page's editor content holds the 120–160 word biography.
			while ( have_posts() ) {
				the_post();
				the_content();
			}
			?>
		</div>
		<p>
			<a class="gm-arrowlink" href="<?php echo esc_url( $gm_ka ? home_url( '/ka/shesakheb/' ) : home_url( '/about/' ) ); ?>">
				<?php echo esc_html( $gm_ka ? 'სრული ბიოგრაფია' : 'Full biography' ); ?>
			</a>
		</p>
	</div>
</section>

<?php /* ---------- Section 3: four areas of expertise ---------- */ ?>
<section class="gm-section gm-section--alt" aria-labelledby="gm-expertise-title">
	<div class="gm-container">
		<h2 id="gm-expertise-title" class="gm-section__title"><?php echo esc_html( $gm_ka ? 'სპეციალიზაცია' : 'Areas of expertise' ); ?></h2>
		<ul class="gm-grid gm-grid--4">
			<?php foreach ( $gm_expertise as $gm_item ) : ?>
				<li class="gm-card">
					<h3 class="gm-card__title">
						<a href="<?php echo esc_url( home_url( $gm_item['url'] ) ); ?>"><?php echo esc_html( $gm_item['title'] ); ?></a>
					</h3>
					<p class="gm-card__text"><?php echo esc_html( $gm_item['text'] ); ?></p>
				</li>
			<?php endforeach; ?>
		</ul>
	</div>
</section>

<?php /* ---------- Section 4: metrics, each with a verification label ---------- */ ?>
<section class="gm-section" aria-labelledby="gm-metrics-title">
	<div class="gm-container">
		<h2 id="gm-metrics-title" class="gm-section__title"><?php echo esc_html( $gm_ka ? 'შერჩეული მაჩვენებლები' : 'Selected project metrics' ); ?></h2>

		<p class="gm-section__intro">
			<?php
			echo esc_html(
				$gm_ka
					? 'თითოეულ ციფრს თან ახლავს წყარო ან გადამოწმების სტატუსი. ზოგიერთი მაჩვენებელი განზრახ არ არის გამოქვეყნებული, სანამ პირველადი დოკუმენტაცია არ დაადასტურებს.'
					: 'Every figure carries its source. Some figures that appear in the press are deliberately not shown here, because published accounts disagree and primary documentation has not yet resolved them.'
			);
			?>
		</p>

		<ul class="gm-metrics">
			<?php foreach ( $gm_metrics as $gm_metric ) : ?>
				<li class="gm-metric">
					<span class="gm-metric__value"><?php echo esc_html( $gm_metric['value'] ); ?></span>
					<span class="gm-metric__label"><?php echo esc_html( $gm_metric['label'] ); ?></span>
					<?php
					// phpcs:ignore WordPress.Security.EscapeOutput -- escaped inside the helper.
					echo gm_verification_label( $gm_metric['status'], $gm_metric['note'], $gm_metric['url'] );
					?>
				</li>
			<?php endforeach; ?>
		</ul>

		<p class="gm-note">
			<?php
			echo esc_html(
				$gm_ka
					? 'აღნიშნული მაჩვენებლები ეხება კომპანიის ოპერაციას, რომლის ხელმძღვანელობაშიც გოდერძი მეტრეველი მონაწილეობდა, და არა ინდივიდუალურ შედეგებს.'
					: 'These figures describe the agricultural operation within which Goderdzi Metreveli held a senior role. They are not presented as individual results.'
			);
			?>
		</p>
	</div>
</section>

<?php
/* ---------- Sections 5, 6, 7: featured case studies and article ---------- */
$gm_features = array(
	array(
		'kicker' => $gm_ka ? 'შემთხვევის ანალიზი' : 'Case study',
		'title'  => $gm_ka
			? 'კომერციული სოფლის მეურნეობის განვითარება საქართველოს ნახევრად მშრალ უდაბნოს რეგიონში'
			: 'Developing Commercial Agriculture in Georgia’s Semi-Arid Udabno Region',
		'text'   => $gm_ka
			? 'როგორ გადაიქცა დაბალი ნალექიანობის, ეროზიისკენ მიდრეკილი მიწა მუშა სასოფლო-სამეურნეო ოპერაციად — მიწის მომზადება, წყალი, ინფრასტრუქტურა და ის, რაც არ იმუშავა.'
			: 'How low-rainfall, erosion-prone land became a working agricultural operation — land preparation, water, infrastructure, and the things that did not work first time.',
		'url'    => '/projects/udabno-semi-arid-development/',
	),
	array(
		'kicker' => $gm_ka ? 'შემთხვევის ანალიზი' : 'Case study',
		'title'  => $gm_ka
			? 'ნუშის ფართომასშტაბიანი წარმოებისა და გადამუშავების ჯაჭვის აშენება'
			: 'Building a Large-Scale Almond Production and Processing Value Chain',
		'text'   => $gm_ka
			? 'ბაღიდან პირველად და მეორად გადამუშავებამდე: რატომ განსაზღვრავს გადამუშავების სიმძლავრე მოსავლის აღების გრაფიკს და არა პირიქით.'
			: 'From orchard to primary and secondary processing: why processing capacity dictates the harvest calendar, not the other way round.',
		'url'    => '/projects/almond-value-chain/',
	),
	array(
		'kicker' => $gm_ka ? 'ტექნიკური სტატია' : 'Technical article',
		'title'  => $gm_ka
			? 'ღრმა გაფხვიერება ნუშის ბაღის გასაშენებლად: ნიადაგის პირობები, სიღრმე და ოპერაციული დაგეგმვა'
			: 'Deep Ripping for Almond Orchard Establishment: Soil Conditions, Depth and Operational Planning',
		'text'   => $gm_ka
			? 'როდის ამართლებს ღრმა გაფხვიერება, როდის არის ფულის ფლანგვა და როდის აზიანებს ნიადაგს, რომლის გაუმჯობესებასაც ცდილობთ.'
			: 'When ripping earns its cost, when it is wasted money, and when it damages the soil you are trying to improve.',
		'url'    => '/deep-ripping/',
	),
);
?>

<?php foreach ( $gm_features as $gm_i => $gm_feature ) : ?>
	<section class="gm-feature <?php echo 0 === $gm_i % 2 ? '' : 'gm-feature--alt'; ?>">
		<div class="gm-container gm-container--narrow">
			<p class="gm-feature__kicker"><?php echo esc_html( $gm_feature['kicker'] ); ?></p>
			<h2 class="gm-feature__title">
				<a href="<?php echo esc_url( home_url( $gm_feature['url'] ) ); ?>"><?php echo esc_html( $gm_feature['title'] ); ?></a>
			</h2>
			<p class="gm-feature__text"><?php echo esc_html( $gm_feature['text'] ); ?></p>
			<p>
				<a class="gm-arrowlink" href="<?php echo esc_url( home_url( $gm_feature['url'] ) ); ?>">
					<?php echo esc_html( $gm_ka ? 'გაგრძელება' : 'Continue reading' ); ?>
				</a>
			</p>
		</div>
	</section>
<?php endforeach; ?>

<?php /* ---------- Section 8: independent media ---------- */ ?>
<section class="gm-section gm-section--alt" aria-labelledby="gm-media-title">
	<div class="gm-container">
		<h2 id="gm-media-title" class="gm-section__title"><?php echo esc_html( $gm_ka ? 'დამოუკიდებელი მედია' : 'Independent coverage' ); ?></h2>
		<p class="gm-section__intro">
			<?php
			echo esc_html(
				$gm_ka
					? 'გარე პუბლიკაციები, რომლებშიც მოხსენიებულია გოდერძი მეტრეველი ან უდაბნოს ოპერაცია. ბმულები მიემართება ორიგინალ წყაროებზე.'
					: 'Independent publications referring to Goderdzi Metreveli or the Udabno operation. Links go to the original sources.'
			);
			?>
		</p>

		<ul class="gm-medialist">
			<?php
			$gm_press = array(
				array( 'Chemonics / USAID', $gm_ka ? 'GeoGAP-ის ტექნიკური მიმოხილვა, 2021 — პირდაპირი ციტატა' : 'GeoGAP technical brief, 2021 — quoted directly', 'https://www.chemonics.com/wp-content/uploads/2025/03/A-Local-Certification-System-in-Georgia_Steppingstones-to-Meeting-Market-Demands.pdf' ),
				array( 'EastFruit', $gm_ka ? 'ნუშის მოსავალი, 2021' : 'Almond harvest report, 2021', 'https://east-fruit.com/en/news/almonds-harvesting-in-georgias-largest-orchard-video/' ),
				array( 'Investor.ge', $gm_ka ? 'ქართული აგროსექტორის ცვლილება, 2022' : 'The changing landscape of Georgian agriculture, 2022', 'https://www.investor.ge/2022/04/18/the-changing-landscape-of-georgian-agriculture/' ),
				array( 'Caucasus Business Week', $gm_ka ? 'ინტერვიუ' : 'Interview', 'https://cbw.ge/business/turning-desert-into-an-agricultural-oasis-an-interview-with-goderdzi-metreveli' ),
				array( 'UN Global Compact Network Georgia', $gm_ka ? 'კორპორაციული პასუხისმგებლობის ჯილდო, 2023' : 'Corporate Responsibility Award, 2023', 'https://unglobalcompact.ge/en/korporaciuli-mdgradobis-jildo-biznesi-mdgradi-ganvitarebistvis-gamarjvebulebi-cnobilia/' ),
			);
			foreach ( $gm_press as $gm_p ) :
				?>
				<li class="gm-medialist__item">
					<span class="gm-medialist__outlet"><?php echo esc_html( $gm_p[0] ); ?></span>
					<a class="gm-medialist__link" href="<?php echo esc_url( $gm_p[2] ); ?>" rel="nofollow noopener" target="_blank"><?php echo esc_html( $gm_p[1] ); ?></a>
				</li>
			<?php endforeach; ?>
		</ul>

		<p>
			<a class="gm-arrowlink" href="<?php echo esc_url( $gm_ka ? home_url( '/ka/media/' ) : home_url( '/media/' ) ); ?>">
				<?php echo esc_html( $gm_ka ? 'ყველა პუბლიკაცია' : 'All coverage' ); ?>
			</a>
		</p>
	</div>
</section>

<?php /* ---------- Section 9: latest technical articles ---------- */ ?>
<?php
$gm_latest = new WP_Query( array(
	'post_type'           => 'post',
	'posts_per_page'      => 3,
	'ignore_sticky_posts' => true,
	'no_found_rows'       => true,
) );
?>
<?php if ( $gm_latest->have_posts() ) : ?>
	<section class="gm-section" aria-labelledby="gm-latest-title">
		<div class="gm-container">
			<h2 id="gm-latest-title" class="gm-section__title"><?php echo esc_html( $gm_ka ? 'ბოლო ტექნიკური სტატიები' : 'Latest technical articles' ); ?></h2>
			<ul class="gm-grid gm-grid--3">
				<?php
				while ( $gm_latest->have_posts() ) :
					$gm_latest->the_post();
					?>
					<li class="gm-card gm-card--article">
						<p class="gm-card__meta">
							<time datetime="<?php echo esc_attr( (string) get_the_date( 'c' ) ); ?>"><?php echo esc_html( (string) get_the_date() ); ?></time>
							<span aria-hidden="true">·</span>
							<span><?php printf( esc_html( $gm_ka ? '%d წთ' : '%d min read' ), (int) gm_reading_time() ); ?></span>
						</p>
						<h3 class="gm-card__title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3>
						<p class="gm-card__text"><?php echo esc_html( wp_trim_words( (string) get_the_excerpt(), 24, '…' ) ); ?></p>
					</li>
					<?php
				endwhile;
				wp_reset_postdata();
				?>
			</ul>
			<p>
				<a class="gm-arrowlink" href="<?php echo esc_url( home_url( '/articles/' ) ); ?>">
					<?php echo esc_html( $gm_ka ? 'ყველა სტატია' : 'All articles' ); ?>
				</a>
			</p>
		</div>
	</section>
<?php endif; ?>

<?php /* ---------- Section 10: consulting / speaking / media invitation ---------- */ ?>
<section class="gm-cta" aria-labelledby="gm-cta-title">
	<div class="gm-container gm-container--narrow">
		<h2 id="gm-cta-title" class="gm-cta__title">
			<?php echo esc_html( $gm_ka ? 'კონსულტაცია, ტრენინგი და საჯარო გამოსვლები' : 'Consulting, training and speaking' ); ?>
		</h2>
		<p class="gm-cta__text">
			<?php
			echo esc_html(
				$gm_ka
					? 'ბაღის გაშენება რთულ ნიადაგზე, ნიადაგის მომზადების დაგეგმვა, ირიგაციისა და მექანიზაციის სტრატეგია, ან გადამუშავების ჯაჭვის შეფასება — მიმართვები მიიღება ქართულ და ინგლისურ ენებზე.'
					: 'Orchard establishment on difficult soils, soil-preparation planning, irrigation and mechanization strategy, or an assessment of a processing value chain. Enquiries welcome in Georgian and English.'
			);
			?>
		</p>
		<p>
			<a class="gm-btn" href="<?php echo esc_url( $gm_ka ? home_url( '/ka/kontakti/' ) : home_url( '/contact/' ) ); ?>">
				<?php echo esc_html( $gm_ka ? 'დაკავშირება' : 'Get in touch' ); ?>
			</a>
			<a class="gm-btn gm-btn--ghost" href="<?php echo esc_url( home_url( '/speaking/' ) ); ?>">
				<?php echo esc_html( $gm_ka ? 'გამოსვლები და ტრენინგები' : 'Speaking and training' ); ?>
			</a>
		</p>
	</div>
</section>

<?php
/* Section 11 — the multidisciplinary disclaimer — is rendered site-wide by footer.php. */
get_footer();
