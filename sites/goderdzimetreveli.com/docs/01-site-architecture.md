# Site Architecture

**Domain:** goderdzimetreveli.com (primary, English at root)
**Secondary:** goderdzimetreveli.ge → 301 redirect to the .com
**Platform:** WordPress (self-hosted on managed hosting), custom theme, no page builder

---

## 1. Design principle

The site is a **hub-and-spoke topical architecture** with a person entity at the
centre. Five pillar pages carry the topical weight; supporting articles link up
to their pillar and across to the biography. Every article's `author.url` points
at the ProfilePage, so topical authority accrues to the named entity rather than
scattering.

```
                        ┌─────────────────────┐
                        │       HOME          │
                        │  (entity gateway)   │
                        └──────────┬──────────┘
                                   │
        ┌──────────────┬───────────┼───────────┬──────────────┐
        │              │           │           │              │
   ┌────▼────┐   ┌─────▼─────┐  ┌──▼───┐  ┌────▼────┐   ┌─────▼─────┐
   │  ABOUT  │   │EXPERIENCE │  │ACHV. │  │EXPERTISE│   │ PROJECTS  │
   │(Profile │   │           │  │      │  │  (hub)  │   │(case std) │
   │  Page)  │   └───────────┘  └──────┘  └────┬────┘   └─────┬─────┘
   └────┬────┘                                 │              │
        │            ┌────────────────────────┼──────────────┘
        │            │                        │
        │     ┌──────▼──────┬─────────┬───────┴──────┬──────────────┐
        │     │             │         │              │              │
        │  ┌──▼───┐   ┌─────▼───┐ ┌───▼────┐  ┌──────▼─────┐  ┌─────▼──────┐
        │  │PILLAR│   │ PILLAR  │ │ PILLAR │  │   PILLAR   │  │   PILLAR   │
        │  │  1   │   │    2    │ │   3    │  │     4      │  │     5      │
        │  │Regen │   │ Almond  │ │  Deep  │  │ Irrigation │  │ Processing │
        │  │ Ag   │   │Orchards │ │Ripping │  │  & Infra   │  │  & Export  │
        │  └──┬───┘   └────┬────┘ └───┬────┘  └─────┬──────┘  └─────┬──────┘
        │     │            │          │             │               │
        │   articles     articles   articles      articles        articles
        │     └────────────┴──────────┴─────────────┴───────────────┘
        │                             │
        └─────────────────────────────┘
              every article links author → ABOUT (ProfilePage)
```

---

## 2. URL map — English (root)

| # | Page | URL | Type | Role |
|---|---|---|---|---|
| 1 | Home | `/` | front-page | Entity gateway |
| 2 | About Goderdzi Metreveli | `/about/` | ProfilePage | **Canonical entity page** |
| 3 | Professional Experience | `/experience/` | page | Career record |
| 4 | Selected Achievements | `/achievements/` | page | Evidence-led achievements |
| 5 | Expertise | `/expertise/` | page | Hub → 5 pillars |
| 6 | Projects and Case Studies | `/projects/` | page | Hub → case studies |
| 7 | Regenerative Agriculture | `/regenerative-agriculture/` | **Pillar 1** | Cluster 1 hub |
| 8 | Almond Orchard Development | `/almond-orchards/` | **Pillar 2** | Cluster 2 hub |
| 9 | Deep-Ripping and Soil Preparation | `/deep-ripping/` | **Pillar 3** | Cluster 3 hub |
| 10 | Irrigation and Agricultural Infrastructure | `/irrigation-infrastructure/` | **Pillar 4** | Cluster 4 hub |
| 11 | Agricultural Mechanization | `/mechanization/` | page | Supports Pillar 4 |
| 12 | Almond Processing and Export Development | `/almond-processing-export/` | **Pillar 5** | Cluster 5 hub |
| 13 | Media and Press | `/media/` | page | Independent coverage |
| 14 | Articles and Insights | `/articles/` | archive | Article index |
| 15 | Speaking, Training and Consulting | `/speaking/` | page | Conversion |
| 16 | Evidence and Project Gallery | `/evidence/` | page | Documentation library |
| 17 | Contact | `/contact/` | page | Conversion |

### Case studies

| Page | URL |
|---|---|
| Developing Commercial Agriculture in Georgia's Semi-Arid Udabno Region | `/projects/udabno-semi-arid-development/` |
| Building a Large-Scale Almond Production and Processing Value Chain | `/projects/almond-value-chain/` |

### Articles

| # | Article | URL | Cluster |
|---|---|---|---|
| 1 | Deep Ripping Versus Conventional Subsoiling | `/articles/deep-ripping-vs-subsoiling/` | 3 |
| 2 | How to Identify a Restrictive Soil Layer | `/articles/identify-restrictive-soil-layer/` | 3 |
| 3 | Correct Soil Moisture for Deep Ripping | `/articles/soil-moisture-for-deep-ripping/` | 3 |
| 4 | Ripping Depth, Spacing and Direction | `/articles/ripping-depth-spacing-direction/` | 3 |
| 5 | Common Deep-Ripping Mistakes and When Ripping Damages Soil | `/articles/deep-ripping-mistakes/` | 3 |
| 6 | Soil Requirements for Commercial Almond Orchards | `/articles/soil-requirements-almond-orchards/` | 2 |
| 7 | Irrigation Planning for Almond Orchards | `/articles/irrigation-planning-almond-orchards/` | 2 |
| 8 | Machinery Requirements for Large Almond Operations | `/articles/machinery-large-almond-operations/` | 2 |
| 9 | Reducing Erosion in Semi-Arid Agricultural Land | `/articles/reducing-erosion-semi-arid-land/` | 1 |
| 10 | Preparing Almond Production for European Markets | `/articles/almonds-for-european-markets/` | 5 |

---

## 3. URL map — Georgian (`/ka/`)

Georgian pages live under `/ka/` and are **separate pages**, not toggled
translations on the same URL. English and Georgian text never appear side by
side on one page.

| Georgian page | URL | EN counterpart |
|---|---|---|
| მთავარი | `/ka/` | `/` |
| გოდერძი მეტრეველის შესახებ | `/ka/shesakheb/` | `/about/` |
| პროფესიული გამოცდილება | `/ka/gamotsdileba/` | `/experience/` |
| რჩეული მიღწევები | `/ka/mightsevebi/` | `/achievements/` |
| სპეციალიზაცია | `/ka/spetsializatsia/` | `/expertise/` |
| რეგენერაციული სოფლის მეურნეობა | `/ka/regeneratsiuli-sofmeurneoba/` | `/regenerative-agriculture/` |
| ნუშის ბაღების განვითარება | `/ka/nushis-baghebi/` | `/almond-orchards/` |
| ღრმა გაფხვიერება და ნიადაგის მომზადება | `/ka/ghrma-gafkhviereba/` | `/deep-ripping/` |
| ირიგაცია და ინფრასტრუქტურა | `/ka/irigatsia-infrastruktura/` | `/irrigation-infrastructure/` |
| სოფლის მეურნეობის მექანიზაცია | `/ka/mekanizatsia/` | `/mechanization/` |
| ნუშის გადამუშავება და ექსპორტი | `/ka/gadamushaveba-eksporti/` | `/almond-processing-export/` |
| მედია და პრესა | `/ka/media/` | `/media/` |
| კონტაქტი | `/ka/kontakti/` | `/contact/` |

**Slug policy:** Latin transliteration, not Georgian script, in URLs. Georgian-script
URLs become percent-encoded (`%E1%83%9B...`), which is unreadable in search
results, breaks in some link contexts, and makes analytics harder to read. Page
titles, headings and body copy are in Georgian script; only the slug is
transliterated.

---

## 4. hreflang

Every page carries a three-way cluster. Self-referencing and bidirectional —
if EN points to KA, KA must point back to EN, or the annotation is ignored.

```html
<link rel="alternate" hreflang="en" href="https://goderdzimetreveli.com/about/" />
<link rel="alternate" hreflang="ka" href="https://goderdzimetreveli.com/ka/shesakheb/" />
<link rel="alternate" hreflang="x-default" href="https://goderdzimetreveli.com/about/" />
```

- `x-default` always points at the **English** URL (the international default).
- Pages with no counterpart (e.g. most articles, initially English-only) emit
  **only** a self-referencing `hreflang="en"` and `x-default`. Never point
  hreflang at a page that does not exist.
- Implemented in `theme/inc/hreflang.php`, driven by the `_gm_translation_of`
  post-meta pairing. Nothing is hardcoded.

---

## 5. WordPress configuration

### Content types

Only two are needed. Custom post types are deliberately avoided — extra types
here add taxonomy and template complexity without SEO benefit.

| Type | Used for |
|---|---|
| **Page** | Items 1–17, case studies, all `/ka/` pages |
| **Post** | The 10 technical articles, and everything in the editorial calendar |

Pages use `page-attributes` hierarchy for the `/projects/` parent. Posts use a
single `Topic` category aligned to the five clusters.

### Permalinks

`Settings → Permalinks → Custom Structure: /articles/%postname%/`

### Categories (one per cluster)

`regenerative-agriculture`, `almond-orchards`, `soil-preparation`,
`irrigation-infrastructure`, `processing-export`

Category archives are **noindex** (thin, duplicative of the pillar pages, which
are the pages meant to rank). The pillar pages do the hub work that a category
archive would otherwise do badly.

### Indexation policy

| Indexed | Not indexed (`noindex, follow`) |
|---|---|
| Home, all 17 pages, case studies, all articles, `/ka/` pages | Tag archives (tags not used), author archives, date archives, category archives, search results, attachment pages, paginated duplicates beyond page 1 of `/articles/`, any staging host |

Author archives are redundant here — there is one author, and `/about/` is the
canonical author entity. Attachment pages are disabled outright (they generate a
thin page per uploaded image, which is pure index bloat on a photo-heavy site).

### Required plugins (kept deliberately few)

| Plugin | Purpose | Notes |
|---|---|---|
| **Polylang** (or WPML) | EN/KA page pairing | Theme reads its pairing; falls back to `_gm_translation_of` meta if absent |
| **A performance/caching plugin** provided by the host | Page cache | Prefer the host's own (Kinsta/WP Engine/SiteGround) over a third-party |
| **An image optimiser** with WebP/AVIF conversion | Media pipeline | Or handle at CDN level |
| **Wordfence** or host-level WAF | Security | |
| **UpdraftPlus** or host-level backups | Backups | Off-site destination required |

**Deliberately not installed:** Yoast/RankMath/AIOSEO. All SEO output — titles,
meta descriptions, canonicals, Open Graph, JSON-LD, breadcrumbs, hreflang,
robots directives — is produced by the theme (`inc/seo.php`, `inc/schema.php`,
`inc/hreflang.php`, `inc/breadcrumbs.php`). This avoids a plugin emitting a
second, conflicting `Person` graph that contradicts the verification report, and
keeps structured data under version control rather than in the database. An
XML sitemap is generated by the theme at `/sitemap.xml`.

**No page builder.** Elementor/Divi/WPBakery are excluded — they inject
significant CSS/JS and degrade Core Web Vitals, which is the opposite of the
brief's requirement.

---

## 6. Navigation

**Primary menu**

```
About  ·  Experience  ·  Expertise ▾  ·  Projects ▾  ·  Articles  ·  Media  ·  Contact
```

`Expertise ▾` → Regenerative Agriculture · Almond Orchards · Deep Ripping ·
Irrigation & Infrastructure · Mechanization · Processing & Export

`Projects ▾` → Udabno Semi-Arid Development · Almond Value Chain · Evidence & Gallery

**Footer** — three columns: Topics (5 pillars) · About (bio, experience,
achievements, speaking, evidence) · Contact + language switch + the
multidisciplinary disclaimer.

**Breadcrumbs** on every page except the homepage, emitting `BreadcrumbList`
JSON-LD:
`Home › Expertise › Deep-Ripping and Soil Preparation`

---

## 7. Templates

| File | Serves |
|---|---|
| `front-page.php` | Homepage, 11 sections |
| `page.php` | Default page |
| `page-templates/pillar.php` | The 5 pillar pages — adds cluster article listing |
| `page-templates/case-study.php` | Case studies — adds project metadata block |
| `page-templates/wide.php` | Evidence gallery |
| `single.php` | Technical articles — author box, dates, references, related |
| `archive.php` | `/articles/` index |
| `404.php`, `search.php` | |

---

## 8. What is delivered vs. what needs the owner

| Delivered in this repository | Requires the owner / an account holder |
|---|---|
| Complete custom theme | Domain registration and DNS |
| All page and article copy, EN + KA | Managed hosting account and SSL |
| SEO titles and meta descriptions | Original photography (see doc 08) |
| JSON-LD templates and samples | Verification documents (see doc 07) |
| Internal-linking map | Google Search Console / Bing verification |
| XML sitemap plan + generator | Analytics account |
| 12-month editorial calendar | Confirmed LinkedIn URL |
| Launch checklist | Native Georgian proofread |
| WXR import file + build script | Final legal/factual sign-off |

**Not done here, and cannot be:** registering `goderdzimetreveli.com`, buying
hosting, or publishing anything live. Those need payment credentials and an
account, which this environment does not have and should not have. Doc 10 gives
the exact steps.
