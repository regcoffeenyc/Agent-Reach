# Keyword Architecture and Page Assignment

**Rule enforced throughout:** one primary topic per page, plus a small set of
closely related secondary terms. No page targets more than one primary term, and
no term is targeted by two pages. Where two pages could plausibly compete, the
weaker one links to the stronger with the target phrase as anchor text.

---

## 1. Two intents, two strategies

| | **Entity intent** | **Topical intent** |
|---|---|---|
| Query looks like | "Goderdzi Metreveli", "Goderdzi Metreveli Udabno" | "deep ripping for almond orchards", "semi-arid agriculture" |
| Volume | Very low | Low to moderate |
| Competition | Low, but contested by news articles and social profiles | Moderate, contested by universities and extension services |
| Goal | **Own the SERP.** Be the top result plus a knowledge panel | Rank for long-tail technical queries; earn citations |
| Carried by | Home, About (ProfilePage), Experience, Achievements, Media | 5 pillars + 10 articles |
| Wins because of | Consistent entity markup, `sameAs`, independent media links | Genuine first-hand technical depth |

The entity work is winnable within months. The topical work compounds over years
and is what makes the site credible to a human reader who arrives from a name
search — which is the actual conversion path for consulting and speaking
enquiries.

---

## 2. Name-keyword assignment

| Keyword | Owning page | Notes |
|---|---|---|
| Goderdzi Metreveli | `/` | Exact-match H1 and title |
| Goderdzi Metreveli agriculture | `/` | Natural in positioning statement |
| Goderdzi Metreveli biography | `/about/` | ProfilePage; canonical entity |
| Goderdzi Metreveli Udabno | `/projects/udabno-semi-arid-development/` | Case study carries the project association |
| Goderdzi Metreveli regenerative agriculture | `/regenerative-agriculture/` | |
| Goderdzi Metreveli almond orchards | `/almond-orchards/` | |
| Goderdzi Metreveli agricultural engineer | `/experience/` | Use "engineering professional" in copy — see doc 07 §3.11 |
| Goderdzi Metreveli Georgia | `/about/` | |
| Goderdzi Metreveli interview / press | `/media/` | |
| Goderdzi Metreveli speaker / consultant | `/speaking/` | |

**Anti-pattern avoided:** repeating the full name in every H2. The name appears in
the title, H1, first paragraph, author byline and structured data — that is
sufficient for entity resolution. Beyond that it reads as manipulation to both
readers and spam classifiers.

---

## 3. Topical keyword assignment

### Cluster 1 — Regenerative agriculture · pillar `/regenerative-agriculture/`

| Page | Primary | Secondary |
|---|---|---|
| `/regenerative-agriculture/` | regenerative agriculture Georgia | regenerative farming Georgia, semi-arid agriculture, soil health commercial farm |
| `/articles/reducing-erosion-semi-arid-land/` | erosion control in commercial orchards | wind erosion semi-arid, cover crops orchards, contour management |
| *(calendar)* Regenerative Agriculture at Commercial Farm Scale | regenerative agriculture at scale | commercial regenerative farming |
| *(calendar)* Organic Transition in Large Commercial Orchards | organic transition orchard | conversion period, input substitution |
| *(calendar)* Measuring Soil Improvement Beyond Yield | measuring soil health | soil organic matter, infiltration testing |

### Cluster 2 — Almond orchards · pillar `/almond-orchards/`

| Page | Primary | Secondary |
|---|---|---|
| `/almond-orchards/` | almond orchard development | commercial almond farming, almond farming in Georgia, large-scale orchard planning |
| `/articles/soil-requirements-almond-orchards/` | soil requirements for almond orchards | almond soil depth, drainage, pH, salinity |
| `/articles/irrigation-planning-almond-orchards/` | irrigation systems for almond orchards | almond water requirement, drip design, ETc |
| `/articles/machinery-large-almond-operations/` | machinery for almond orchards | trunk shaker, sweeper, harvest fleet sizing |
| *(calendar)* Almond Variety Selection in Continental and Semi-Arid Conditions | almond variety selection | Guara, Supernova, self-fertile varieties, frost risk |

### Cluster 3 — Deep ripping · pillar `/deep-ripping/`

The strongest genuine opportunity on the site. Search results for these terms are
dominated by generic equipment-vendor copy and a handful of extension PDFs; a
practitioner-written treatment competes well.

| Page | Primary | Secondary |
|---|---|---|
| `/deep-ripping/` | deep-ripping soil preparation | orchard soil preparation, deep ripping for almond orchards |
| `/articles/deep-ripping-vs-subsoiling/` | deep ripping versus subsoiling | subsoiling for orchards, tillage depth |
| `/articles/identify-restrictive-soil-layer/` | how to identify a restrictive soil layer | hardpan, plough pan, penetrometer, soil pit |
| `/articles/soil-moisture-for-deep-ripping/` | soil moisture for deep ripping | brittle failure, plastic limit, when to rip |
| `/articles/ripping-depth-spacing-direction/` | ripping depth and spacing | shank spacing, ripping direction, orchard row alignment |
| `/articles/deep-ripping-mistakes/` | deep ripping mistakes | when not to deep rip, smearing, subsoil damage |

### Cluster 4 — Semi-arid engineering · pillar `/irrigation-infrastructure/`

| Page | Primary | Secondary |
|---|---|---|
| `/irrigation-infrastructure/` | agricultural water infrastructure | irrigation efficiency, water supply for large farms, semi-arid irrigation |
| `/mechanization/` | agricultural mechanization | high-horsepower tractors, farm machinery selection |
| *(calendar)* Erosion and Drainage Planning | agricultural drainage planning | surface drainage, waterway design |
| *(calendar)* Converting Pilot Projects into Commercial Operations | agricultural pilot to scale | phased orchard development |

### Cluster 5 — Processing and market access · pillar `/almond-processing-export/`

| Page | Primary | Secondary |
|---|---|---|
| `/almond-processing-export/` | almond processing Georgia | almond value chain, hulling and shelling, regional processing |
| `/articles/almonds-for-european-markets/` | almond export to Europe | EU food standards, aflatoxin limits, traceability |
| *(calendar)* GeoGAP and Commercial Market Access | GeoGAP agriculture Georgia | Georgian Good Agricultural Practices, certification |
| *(calendar)* Supporting Independent Farmers Through Regional Processing | regional processing cooperative | smallholder market access |

---

## 4. Cannibalisation controls

Pairs at genuine risk of competing, and the rule applied:

| Risk pair | Resolution |
|---|---|
| `/regenerative-agriculture/` vs `/articles/reducing-erosion-semi-arid-land/` | Pillar owns "regenerative"; article owns "erosion". Pillar links down with anchor "reducing erosion in semi-arid land" |
| `/almond-orchards/` vs `/articles/soil-requirements-almond-orchards/` | Pillar covers planning end-to-end at low depth; article goes deep on soil only and never restates orchard planning |
| `/deep-ripping/` vs `/articles/ripping-depth-spacing-direction/` | Pillar answers *whether and when*; article answers *how much and which way* |
| `/irrigation-infrastructure/` vs `/articles/irrigation-planning-almond-orchards/` | Infrastructure = water source, delivery, storage, headworks. Article = in-orchard scheduling and design. Explicit cross-links |
| `/mechanization/` vs `/articles/machinery-large-almond-operations/` | Page = fleet strategy and selection principles. Article = the specific almond harvest chain |
| `/experience/` vs `/about/` | About is the entity page and the only `ProfilePage`. Experience is a chronological record with no biographical narrative |

---

## 5. Realistic expectations

Stated plainly so results are judged against something honest:

- **Name queries:** a well-marked-up site on an exact-match domain should reach
  position 1 for the exact name within 4–12 weeks of indexing, assuming no strong
  competing entity shares the name. A knowledge panel is *not* guaranteed and
  cannot be bought — it depends on Google's confidence in the entity, which grows
  from consistent `sameAs`, independent media coverage, and time.
- **Technical long-tail:** 6–18 months for the deep-ripping cluster to earn
  meaningful impressions, longer for competitive head terms. "Regenerative
  agriculture" as a bare head term is not winnable and is not targeted.
- **AI-assisted search:** cited when content is specific, attributable and
  well-structured. The article template's explicit separation of first-hand
  observation from general guidance exists partly for this reason — it gives a
  model a clean, quotable, attributable claim.
- **What will not work:** volume for its own sake. Ten genuinely expert articles
  outperform fifty thin ones, and thin content on a personal-reputation domain is
  actively harmful.

---

## 6. Terms deliberately not targeted

| Term | Why |
|---|---|
| "best agricultural consultant" and similar superlatives | Unsupportable; brief forbids it |
| "largest almond orchard in Europe" | Sources say "Georgia's largest orchard" (EastFruit) — a Europe claim has no evidence |
| "organic almonds Georgia" | Certification unverified (doc 07 §3.5). Do not build pages on a legally protected term without a certificate |
| Generic head terms ("agriculture", "farming") | No realistic path; no commercial intent |
| Competitor or company brand names | Not appropriate on a personal site |
