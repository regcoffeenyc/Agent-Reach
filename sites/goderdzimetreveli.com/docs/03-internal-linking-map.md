# Internal Linking Map

Internal links do two jobs here: they distribute authority toward the pages meant
to rank, and they bind every technical article back to the person entity. The
second is what makes topical authority accrue to *Goderdzi Metreveli* rather than
dissipating across unrelated URLs.

---

## 1. Rules applied

1. **Every article links up to its pillar**, with the pillar's primary keyword or
   a close variant as anchor text.
2. **Every pillar links down to all its articles.** A pillar that does not link to
   its cluster is not a hub.
3. **Every article links to `/about/`** through the author byline and the author
   box. This is the entity binding, and it is also what `Article.author.url` in the
   JSON-LD points to — the visible link and the structured data agree.
4. **Articles cross-link within their cluster** where the reference is genuinely
   useful, not to manufacture link volume.
5. **Cross-cluster links only where the topics genuinely connect** — deep ripping
   to irrigation sequencing, almond orchards to processing capacity. These are the
   most valuable links on the site because they demonstrate that the author
   understands the system rather than isolated topics.
6. **Anchor text is descriptive and varied.** No "click here". No identical anchor
   text repeated across dozens of links, which reads as manipulation.
7. **Conversion pages are linked from every pillar** — `/contact/` and
   `/speaking/`, via the CTA block in `page-templates/pillar.php`.

---

## 2. Link authority flow

```
                    ┌──────────────────┐
     nav + footer   │  HOME  /         │  ← external links land here
     from all pages │  (entity gateway)│     and on /about/
                    └────────┬─────────┘
                             │
             ┌───────────────┼────────────────┐
             ▼               ▼                ▼
      ┌────────────┐  ┌─────────────┐  ┌────────────┐
      │  /about/   │  │ /expertise/ │  │ /projects/ │
      │ProfilePage │  │    (hub)    │  │   (hub)    │
      └──────▲─────┘  └──────┬──────┘  └─────┬──────┘
             │               │               │
             │        ┌──────┴──────┐        │
             │        ▼             ▼        ▼
             │   ┌─────────┐   ┌─────────────────┐
             │   │ PILLARS │◄──│  CASE STUDIES   │
             │   │  (×5)   │──►│      (×2)       │
             │   └────┬────┘   └─────────────────┘
             │        │  ▲
             │        ▼  │  (pillar ↔ article, both directions)
             │   ┌─────────────┐
             └───┤  ARTICLES   │
   author byline │    (×10)    │
   + author box  └─────────────┘
```

`/about/` receives inbound links from all 10 articles plus both case studies plus
the homepage plus site navigation — making it, by internal link volume, the
strongest page on the site after the homepage. That is deliberate: it is the
`ProfilePage`, the canonical entity page, and the target of every
`author.url` in the structured data.

---

## 3. Cluster maps

### Cluster 3 — Deep ripping and soil preparation

Pillar: **`/deep-ripping/`**

| From | To | Anchor text |
|---|---|---|
| `/deep-ripping/` | `/articles/deep-ripping-vs-subsoiling/` | Deep Ripping Versus Conventional Subsoiling |
| `/deep-ripping/` | `/articles/identify-restrictive-soil-layer/` | How to Identify a Restrictive Soil Layer |
| `/deep-ripping/` | `/articles/soil-moisture-for-deep-ripping/` | Correct Soil Moisture for Deep Ripping |
| `/deep-ripping/` | `/articles/ripping-depth-spacing-direction/` | Ripping Depth, Spacing and Direction |
| `/deep-ripping/` | `/articles/deep-ripping-mistakes/` | Common Deep-Ripping Mistakes |
| all 5 articles | `/deep-ripping/` | Deep-Ripping and Soil Preparation for Orchard Establishment |
| `/articles/deep-ripping-vs-subsoiling/` | `/articles/identify-restrictive-soil-layer/` | dig a pit |
| `/articles/soil-moisture-for-deep-ripping/` | `/articles/ripping-depth-spacing-direction/` | spacing |
| `/articles/ripping-depth-spacing-direction/` | `/articles/soil-moisture-for-deep-ripping/` | Correct Soil Moisture for Deep Ripping |
| `/articles/deep-ripping-mistakes/` | all 4 siblings | contextual, in each numbered mistake |
| `/articles/identify-restrictive-soil-layer/` | `/articles/soil-requirements-almond-orchards/` | cross-cluster |

### Cluster 2 — Almond orchards

Pillar: **`/almond-orchards/`**

| From | To | Anchor text |
|---|---|---|
| `/almond-orchards/` | `/articles/soil-requirements-almond-orchards/` | Soil Requirements for Commercial Almond Orchards |
| `/almond-orchards/` | `/articles/irrigation-planning-almond-orchards/` | Irrigation Planning for Almond Orchards |
| `/almond-orchards/` | `/articles/machinery-large-almond-operations/` | Machinery Requirements for Large Almond Operations |
| `/almond-orchards/` | `/articles/almonds-for-european-markets/` | Preparing Almond Production for European Markets |
| `/almond-orchards/` | `/deep-ripping/` | Deep-Ripping and Soil Preparation |
| `/almond-orchards/` | `/almond-processing-export/` | Almond Processing and Export Development |
| all 4 articles | `/almond-orchards/` | Almond Orchard Development |
| `/articles/soil-requirements-almond-orchards/` | `/deep-ripping/` | cross-cluster |
| `/articles/irrigation-planning-almond-orchards/` | `/articles/ripping-depth-spacing-direction/` | cross-cluster, sequencing |
| `/articles/machinery-large-almond-operations/` | `/mechanization/` | Agricultural Mechanization |

### Cluster 1 — Regenerative agriculture

Pillar: **`/regenerative-agriculture/`**

| From | To | Anchor text |
|---|---|---|
| `/regenerative-agriculture/` | `/articles/reducing-erosion-semi-arid-land/` | Reducing Erosion in Semi-Arid Agricultural Land |
| `/regenerative-agriculture/` | `/deep-ripping/` | Deep-Ripping and Soil Preparation |
| `/regenerative-agriculture/` | `/irrigation-infrastructure/` | Irrigation and Agricultural Infrastructure |
| `/articles/reducing-erosion-semi-arid-land/` | `/regenerative-agriculture/` | Regenerative Agriculture in Semi-Arid Georgia |
| `/articles/reducing-erosion-semi-arid-land/` | `/articles/ripping-depth-spacing-direction/` | cross-cluster, rip-line orientation |
| `/articles/reducing-erosion-semi-arid-land/` | `/articles/soil-requirements-almond-orchards/` | sodicity |

### Cluster 4 — Semi-arid engineering

Pillar: **`/irrigation-infrastructure/`** · Supporting page: **`/mechanization/`**

| From | To | Anchor text |
|---|---|---|
| `/irrigation-infrastructure/` | `/mechanization/` | Agricultural Mechanization |
| `/irrigation-infrastructure/` | `/articles/reducing-erosion-semi-arid-land/` | Reducing Erosion in Semi-Arid Agricultural Land |
| `/irrigation-infrastructure/` | `/articles/irrigation-planning-almond-orchards/` | Irrigation Planning for Almond Orchards |
| `/mechanization/` | `/deep-ripping/` | Deep-Ripping and Soil Preparation |
| `/mechanization/` | `/articles/machinery-large-almond-operations/` | Machinery Requirements for Large Almond Operations |
| `/mechanization/` | `/articles/soil-moisture-for-deep-ripping/` | Correct Soil Moisture for Deep Ripping |

### Cluster 5 — Processing and market access

Pillar: **`/almond-processing-export/`**

| From | To | Anchor text |
|---|---|---|
| `/almond-processing-export/` | `/articles/almonds-for-european-markets/` | Preparing Almond Production for European Markets |
| `/almond-processing-export/` | `/almond-orchards/` | Almond Orchard Development |
| `/almond-processing-export/` | `/projects/almond-value-chain/` | Building an Almond Value Chain |
| `/almond-processing-export/` | `/mechanization/` | Agricultural Mechanization |
| `/articles/almonds-for-european-markets/` | `/almond-processing-export/` | Almond Processing and Export Development |

---

## 4. Case studies

Case studies sit between the pillars and the biography — they are where abstract
technique becomes a specific project, so they link generously in both directions.

| From | To |
|---|---|
| `/projects/udabno-semi-arid-development/` | `/deep-ripping/`, `/irrigation-infrastructure/`, `/regenerative-agriculture/`, `/mechanization/`, `/articles/reducing-erosion-semi-arid-land/`, `/media/`, `/projects/almond-value-chain/` |
| `/projects/almond-value-chain/` | `/almond-orchards/`, `/almond-processing-export/`, `/articles/almonds-for-european-markets/`, `/projects/udabno-semi-arid-development/` |
| `/achievements/` | both case studies, all five pillars, `/media/` |
| `/projects/` | both case studies, `/evidence/` |

---

## 5. Entity-reinforcement links

The links whose purpose is entity resolution rather than topic authority.

| From | To | Mechanism |
|---|---|---|
| All 10 articles | `/about/` | Author byline (`rel="author"`) in `single.php` |
| All 10 articles | `/about/` | Author box below content |
| `/` | `/about/` | "Full biography" link in Section 2 |
| `/experience/`, `/achievements/`, `/expertise/` | `/about/` | Related links |
| `/media/` | external sources | `rel="nofollow noopener"` — these are citations, not endorsements |
| `/about/` | external sources | Source list at page foot |
| Site footer | `/about/`, `/experience/`, `/achievements/`, `/speaking/`, `/evidence/` | Footer — About column |

**On outbound links to media sources:** these carry `rel="nofollow noopener"` and
open in a new tab. They are attribution, which the site needs for credibility, and
nofollow prevents the site's own authority draining into third-party news
articles. Keeping them is more important than the small link-equity cost.

---

## 6. Orphan check

Every page must be reachable from the homepage in three clicks or fewer, and every
page must have at least one inbound internal link.

| Page | Inbound links from |
|---|---|
| `/` | Site-wide navigation |
| `/about/` | Nav, footer, homepage, all articles ×2, experience, achievements, expertise |
| `/experience/` | Nav, footer, about, achievements |
| `/achievements/` | Footer, experience, expertise |
| `/expertise/` | Nav, footer, homepage, breadcrumbs on all pillars |
| `/projects/` | Nav, footer, homepage features, breadcrumbs on case studies |
| Each pillar | Nav submenu, footer topics, expertise, homepage, its 2–5 articles, cross-cluster pillars |
| `/mechanization/` | Nav submenu, expertise, irrigation pillar, machinery article, almond orchards |
| Each article | Its pillar, `/articles/` index, sibling articles, homepage latest-articles block, related-reading block |
| Each case study | `/projects/`, homepage features, achievements, relevant pillar, the other case study |
| `/media/` | Nav, footer, homepage Section 8, about, achievements, evidence |
| `/articles/` | Nav, footer, homepage, all article breadcrumbs |
| `/speaking/` | Nav, footer, pillar CTA blocks, contact, expertise |
| `/evidence/` | Nav submenu, footer, projects, both case studies |
| `/contact/` | Nav, footer, all pillar CTA blocks, homepage Section 10, speaking |
| `/ka/*` | Language switcher on the paired EN page, `/ka/` nav and footer, hreflang |

**No orphans.** Verify with a crawl before launch (doc 06).

---

## 7. Georgian internal linking

The `/ka/` pages link **only to other `/ka/` pages** in body content. Mixing
languages in the internal link graph sends confusing signals and gives Georgian
readers a dead end in a language they may not read.

Cross-language movement happens only through the language switcher and the
hreflang annotations.

Because only 13 Georgian pages exist, the Georgian internal graph is flatter than
the English one: `/ka/` → `/ka/spetsializatsia/` → each Georgian pillar, with
pillars cross-linking to each other and all linking to `/ka/kontakti/`. Georgian
pillar pages do **not** link to English articles, so their cluster sections are
empty until the articles are translated.

---

## 8. Maintenance

When a new article is published:

1. Add a link to it from its pillar page (the pillar template lists cluster posts
   automatically, but the body text should reference the important ones explicitly).
2. Add 2–3 contextual links from existing articles where genuinely relevant.
3. Add 2–3 outbound links from the new article to existing pillars and siblings.
4. Confirm the author byline and author box render — they are template-driven, so
   this is a check rather than a task.
5. Re-run the orphan crawl quarterly.

Never add a link that a reader would not want to follow. Internal linking that
exists only for crawlers is visible to readers as clutter and to search engines as
a pattern.
