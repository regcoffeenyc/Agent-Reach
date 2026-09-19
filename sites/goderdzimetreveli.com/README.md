# goderdzimetreveli.com

Complete WordPress build for the professional site of **Goderdzi Metreveli** —
agricultural executive, regenerative farming practitioner, and specialist in
large-scale almond orchard and semi-arid land development.

Bilingual (English at root, Georgian under `/ka/`), custom theme, self-contained
SEO and structured data, no page builder, no external font or script requests.

---

## Read this first

**`docs/07-fact-verification-report.md` is the governing document.** Every factual
claim on the site was checked against the eight public sources during the build.
Several figures supplied in the original brief are **not published**, because
independently published reporting contradicts them:

| Claim in the brief | What the sources say | Status |
|---|---|---|
| Almond orchard ~2,000 ha | **2,300 ha** — *EastFruit* 2021 **and** *Investor.ge* 2022 | **Revised upward** and published |
| ~20,000 ha total farmland | Self-reported in one interview. Other sources: 4,000 ha (USAID/Chemonics), 5,000 ha (UNGC) | **Held** — no total-area figure in any headline claim |
| Processing capacity 14–15 t/h | **2.5 t/h** — *EastFruit* 2021. A ~6× discrepancy | **Removed** |
| USD 15 m processing investment | No source isolates processing capex | **Held** |
| Equipment maker "Borrell" | Source spells it "Borelli"; two real manufacturers match | **Held** |
| Organic production | Certification unverified; sources describe it as *planned* | **Removed** — "organic" is legally protected |
| Almonds sold in Europe | Export-*oriented* production documented; shipments not | **Held** |
| SDG 12 award | Went to **Udabno Group and its project team** | Published as **organisational**, never personal |
| Signed the USAID MOU | He is **not named** in the announcement | **Removed** |
| CEO / board titles, 2010–2024 dates | Sources say "Director" and "Managing Director"; no dates corroborated | **Held** |
| Deep-ripping depths, horsepower, contractors | No public source | **Held** — the technical pages carry the reasoning, not the parameters |

One genuinely strong new source was found during the build: a **USAID-funded
Chemonics technical brief (October 2021) quotes Goderdzi Metreveli twice by name,
as "Managing Director, Adjara Group"**. That is the best independent documentation
available and is used prominently.

Nothing here should go live until the report's sign-off (§7) is complete.

---

## Layout

```
docs/                     Strategy and operations
  01-site-architecture.md          URL map, templates, indexation policy, plugins
  02-seo-titles-and-meta.md        Every title and description, EN + KA
  03-internal-linking-map.md       Link graph, anchor text, orphan check
  04-xml-sitemap-plan.md           Sitemap structure and what is excluded
  05-editorial-calendar-12-month.md
  06-search-console-launch-checklist.md   Phased, with BLOCKING items marked
  07-fact-verification-report.md   ← governing document
  08-missing-evidence-checklist.md Photography brief + documents needed
  09-keyword-map.md                One primary topic per page; realistic expectations
  10-hosting-and-domain-setup.md   Domain, hosting, CDN, deployment, staging
  11-georgian-language-notes.md    Terminology decisions; native-review sign-off

content/
  bios/                   Full, 100-word, and 50-word speaker biographies
  en/pages/               12 core pages
  en/pillars/             5 pillar pages
  en/case-studies/        2 case studies
  en/articles/            10 technical articles
  ka/pages/               13 Georgian principal pages

theme/goderdzi-metreveli/    Custom theme (22 PHP files, all php -l clean)
  inc/seo.php                Titles, meta, canonical, robots, Open Graph
  inc/schema.php             JSON-LD — Person, WebSite, WebPage/ProfilePage, Article
  inc/hreflang.php           en / ka / x-default, reciprocal only
  inc/breadcrumbs.php        Trail + BreadcrumbList, one source of truth
  inc/sitemap.php            Sitemap index + pages/articles/ka/images
  inc/performance.php        LCP preload, AVIF/WebP <picture>, security headers
  inc/meta-boxes.php         Per-page SEO fields
  inc/helpers.php            Language detection, verification labels

structured-data/          Reference JSON-LD specimens per page type
tools/build_wxr.py        Generates the WordPress import from content/*.md
import/                   Generated WXR (42 items, 32 pages + 10 posts)
```

---

## Deploy

Full instructions in `docs/10-hosting-and-domain-setup.md`. Summary:

```bash
# 1. Theme
cp -r theme/goderdzi-metreveli /path/to/wp-content/themes/
wp theme activate goderdzi-metreveli

# 2. Content
wp plugin install wordpress-importer --activate
wp import import/goderdzi-metreveli.wxr.xml --authors=create

# 3. Provisioning — REQUIRED
#    The import creates pages and posts but no menus, no front-page assignment,
#    and leaves WordPress's default content in place.
bash tools/provision.sh

# 4. wp-config.php — REQUIRED
#    define( 'WP_ENVIRONMENT_TYPE', 'production' );   // 'staging' on staging

# 5. Customizer > Entity and structured data
#    Set the CONFIRMED LinkedIn URL and the portrait image.
```

## Verification status

The full sequence above has been executed end-to-end against **WordPress 7.0 on a
clean database**, not just linted:

| Check | Result |
|---|---|
| Import | 42/42 items, no errors |
| URLs returning 200 | **48 / 48** (38 pages, 5 sitemaps, robots.txt, search, 404) |
| PHP notices, warnings, fatals | **zero** across every template |
| One `<h1>` per page | 42/42 |
| Canonical + `x-default` present | 42/42 |
| JSON-LD parses, Person node present | 42/42 |
| `alumniOf` / `award` / `worksFor` / `affiliation` absent | 42/42 |
| hreflang reciprocal on all 13 pairs | pass |
| No dangling hreflang on unpaired pages | pass |
| robots policy (5 indexed, 6 noindex cases) | 11/11 correct |
| `<title>` matches `docs/02` | pass |
| External hosts requested | **none** — 1 stylesheet, 1 script, all self-hosted |

Four real bugs were found by running it and are fixed:

1. **Environment detection** — the hostname heuristic overrode an explicit
   `WP_ENVIRONMENT_TYPE = 'production'`. A live site on a `*.kinsta.cloud` or
   `*.wpengine.com` domain would have been permanently `noindex` with
   `Disallow: /` and 404 sitemaps, with nothing in wp-admin explaining why.
2. **Georgian pages served English navigation** — one menu location for both
   languages, so every Georgian nav link led to an English page. Now per-language
   menu locations with a fallback.
3. **Duplicate breadcrumb** — Georgian pages showed "Home" twice
   (`მთავარი › გოდერძი მეტრეველი › …`) because the `/ka/` parent page is itself
   the Georgian home.
4. **No navigation at all after import**, plus WordPress's "Hello world!" post
   appearing in the homepage latest-articles block and the sitemap. Fixed by
   `tools/provision.sh`, which did not previously exist.

Regenerate the import after editing any markdown:

```bash
python3 tools/build_wxr.py
```

The build script is dependency-free. It parses the front matter, converts the
markdown subset used by this content, resolves `translation_of` keys to real post
IDs for hreflang pairing, and sets page parents from nested slug paths.

---

## Design decisions worth knowing

**No SEO plugin.** Yoast/RankMath/AIOSEO each emit their own `Person` graph.
Running one alongside this theme would produce a second, competing entity node
populated from plugin settings rather than from the verification report — and it
would live in the database, outside version control. All SEO output is in the
theme instead.

**No page builder.** Elementor and similar inject significant CSS/JS and would
undermine the Core Web Vitals requirement on a photography-led site.

**No external requests.** System font stacks including Georgian faces (Noto
Sans/Serif Georgian, Sylfaen), no Google Fonts, no CDN scripts. Zero
render-blocking third-party requests, and no visitor IPs sent to a font host.

**Verification labels are structural.** `gm_verification_label()` is the only way
to render a metric, and it requires a status and a source. There is deliberately no
code path that renders a bare number.

**Missing photography degrades gracefully.** With no portrait uploaded, the hero
renders a typographic mark rather than a stock business photo. The brief excludes
stock imagery where original photography should be; the theme enforces it.

**Georgian slugs are transliterated** (`/ka/shesakheb/`, not percent-encoded
Mkhedruli), so URLs stay readable in search results and analytics.

**Structured data omits `alumniOf`, `award`, `worksFor` and `affiliation`** — see
`structured-data/README.md`. Each omission traces to a specific unverified claim.

---

## What still needs a human

Nothing in this repository can register a domain, buy hosting, or publish
anything — that needs payment credentials and an account.

**Blocking before launch:**

1. Fact-verification sign-off (`docs/07`, §7)
2. Native Georgian proofread of all 13 `/ka/` pages (`docs/11`)
3. Original photography — portrait at minimum (`docs/08` §B1)
4. Confirmed LinkedIn URL for `sameAs`
5. Contact details for `/contact/` and `/ka/kontakti/`
6. Domain registration and managed hosting (`docs/10`)

**Highest-value verification tasks**, in order of impact:

1. Land records separating owned / leased / cultivated hectares
2. Processing equipment specification and nameplate photograph
3. Employment records and company register extract
4. Organic certification status
5. Export documentation

Clearing items 1 and 2 would let the site publish the scale figures it currently
has to withhold — which is the single biggest improvement available to it.

---

## Repository note

Per the brief, GitHub is a private code repository and technical backup only.
**Do not enable GitHub Pages on this path** — a Pages-hosted copy would compete
with the real domain for the person's own name, which is precisely the outcome
this site exists to prevent.
