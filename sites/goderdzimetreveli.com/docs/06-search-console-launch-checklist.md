# Search Console and Launch Checklist

Work top to bottom. Items marked **BLOCKING** must be cleared before the site is
made publicly indexable.

---

## Phase 1 — Before anything goes live

### Factual and legal

- [ ] **BLOCKING** — Fact-verification report (doc 07) reviewed and signed off
- [ ] **BLOCKING** — Every **C**, **D** and **E** graded claim confirmed as held, revised or removed
- [ ] **BLOCKING** — No claim of achieved organic certification anywhere on the site
- [ ] **BLOCKING** — SDG 12 award described as organisational on every page it appears
- [ ] **BLOCKING** — No statement or implication that Metreveli signed the USAID MOU
- [ ] **BLOCKING** — No third party (contractor, partner, employee) named without written consent
- [ ] Confirmed LinkedIn URL set in Customizer → Entity and structured data
- [ ] Contact details supplied and placed on `/contact/` and `/ka/kontakti/`
- [ ] Privacy statement accurate for the analytics actually installed

### Language

- [ ] **BLOCKING** — Native Georgian proofread of all 13 `/ka/` pages complete (doc 11)
- [ ] Georgian terminology table (doc 11 §2) confirmed or corrected
- [ ] Back-translated GeoGAP quotations resolved (doc 11 §4)
- [ ] All `[საჭიროა გადამოწმება]` markers intact

### Content and media

- [ ] Original portrait uploaded; homepage no longer showing the typographic fallback
- [ ] Case-study photography in place, or the case studies' evidence gaps stated
- [ ] Every image has descriptive alt text
- [ ] Every image filename descriptive before upload — not `IMG_4821.jpg`
- [ ] AVIF/WebP derivatives generated
- [ ] Hero images under ~200 KB at 2000 px
- [ ] Downloadable biography PDF generated
- [ ] Executive CV **withheld** until employment dates and titles are documented

---

## Phase 2 — Technical, on staging

### Indexation safety

- [ ] Staging is HTTP-password-protected **and** sends `X-Robots-Tag: noindex`
- [ ] `blog_public` is `0` on staging
- [ ] `gm_is_non_production()` correctly detects the staging host — verify by
      viewing source and confirming `noindex` is present
- [ ] `/sitemap.xml` returns 404 on staging
- [ ] Search `site:staging-host` on Google and Bing — nothing indexed

### Structure

- [ ] Permalinks set to `/articles/%postname%/`
- [ ] All 17 English pages published at the URLs in doc 01 §2
- [ ] Both case studies published under `/projects/`
- [ ] All 10 articles published, each in exactly one category
- [ ] All 13 Georgian pages published under `/ka/`
- [ ] Every Georgian page paired to its English counterpart via `translation_of`
- [ ] Pillar pages assigned the "Pillar page" template
- [ ] Case studies assigned the "Case study" template
- [ ] `/about/` has "Mark as ProfilePage" checked — and no other page does
- [ ] `/articles/` set as the Posts page in Settings → Reading
- [ ] Primary, Footer Topics and Footer About menus built and assigned

### On-page

- [ ] Exactly one `<h1>` per page — crawl to confirm, do not spot-check
- [ ] Heading hierarchy has no skipped levels
- [ ] Every page has its SEO title and meta description from doc 02
- [ ] No duplicate titles or descriptions
- [ ] Canonical URL self-references on every page
- [ ] Breadcrumbs render on every page except the homepage
- [ ] Verification labels present beside every homepage metric

### hreflang

- [ ] EN pages emit `hreflang="en"`, `hreflang="ka"`, `hreflang="x-default"`
- [ ] KA pages emit the same cluster, reciprocally
- [ ] `x-default` points at the **English** URL on both
- [ ] Pages with no counterpart emit only `en` + `x-default` — no dangling annotation
- [ ] hreflang alternates also present in the sitemaps
- [ ] Language switcher shows unavailable languages as disabled, not as broken links

### Structured data

- [ ] `Person`, `WebSite`, `WebPage` present on all pages
- [ ] `ProfilePage` with `mainEntity` → Person on `/about/` only
- [ ] `Article` on all posts, with `author.url` → `/about/`
- [ ] `BreadcrumbList` on all non-homepage pages, last item without `item`
- [ ] **`alumniOf` absent** (education unverified)
- [ ] **`award` absent from Person** (organisational award)
- [ ] **`worksFor` / `affiliation` absent** (roles unverified)
- [ ] `sameAs` contains only the confirmed LinkedIn URL — or is absent
- [ ] Validated in [Rich Results Test](https://search.google.com/test/rich-results)
- [ ] Validated in [Schema.org validator](https://validator.schema.org/)
- [ ] Every structured-data property corresponds to something visible on the page

### Performance and accessibility

- [ ] Lighthouse mobile performance ≥ 90
- [ ] Lighthouse accessibility ≥ 95
- [ ] LCP under 2.5 s on mobile
- [ ] CLS under 0.1
- [ ] INP under 200 ms
- [ ] LCP image preloaded and **not** lazy-loaded
- [ ] No render-blocking external requests — confirm zero third-party font or script hosts
- [ ] Keyboard navigation works through nav, submenus and language switcher
- [ ] Visible focus indicators throughout
- [ ] Colour contrast meets WCAG AA
- [ ] Renders correctly at 320 px width with no horizontal scroll

### Crawl

- [ ] Full crawl of staging (Screaming Frog or equivalent)
- [ ] Zero 404s, zero broken internal links
- [ ] Zero orphan pages (doc 03 §6)
- [ ] Zero redirect chains
- [ ] No page more than three clicks from the homepage
- [ ] Robots directives as intended on every URL type

---

## Phase 3 — Go live

- [ ] Push staging to production
- [ ] SSL active; HTTPS forced
- [ ] `www` → apex redirect working (or the reverse — one canonical host)
- [ ] `.ge` domain 301-redirecting to the `.com`
- [ ] `blog_public` set to `1`
- [ ] View source on production and confirm `index, follow` is now present
- [ ] `/robots.txt` shows the production version with the sitemap line
- [ ] `/sitemap.xml` returns valid XML
- [ ] Spot-check five URLs for correct canonical, hreflang and structured data
- [ ] Off-site backup taken and a restore tested

---

## Phase 4 — Google Search Console

1. [ ] Add property — **Domain property** (`goderdzimetreveli.com`), so all
       subdomains and protocols are covered by one property
2. [ ] Verify by DNS TXT record
3. [ ] Add the `.ge` domain as a separate property, to confirm the redirect is
       seen and that it is not accumulating impressions of its own
4. [ ] Submit `/sitemap.xml`
5. [ ] Confirm all four child sitemaps are discovered and read
6. [ ] URL Inspection → request indexing for `/` and `/about/` — the two entity
       pages, indexed first
7. [ ] Check the Page Indexing report for unexpected exclusions
8. [ ] International Targeting → confirm no hreflang errors
9. [ ] Core Web Vitals → confirm data collection has begun (field data takes ~28 days)
10. [ ] Manual Actions → confirm none
11. [ ] Security Issues → confirm none
12. [ ] Set email notification preferences

### Verifying entity resolution

- [ ] Search the exact name in an incognito window and record what ranks
- [ ] Search `site:goderdzimetreveli.com` and confirm the indexed set matches the
      intended set — no tag, author, date or staging URLs
- [ ] Note whether a knowledge panel appears. It cannot be forced; it grows from
      consistent `sameAs`, independent media coverage and time (doc 09 §5)

---

## Phase 5 — Bing Webmaster Tools

1. [ ] Add site
2. [ ] Verify — importing from Search Console is fastest
3. [ ] Submit `/sitemap.xml`
4. [ ] Use URL Submission for `/` and `/about/`
5. [ ] Check the SEO Reports section
6. [ ] Confirm IndexNow is not needed (no plugin required at this content volume)

Bing matters here beyond its own traffic share: it feeds several AI-assisted
search products, which is one of the brief's stated objectives.

---

## Phase 6 — Analytics and monitoring

- [ ] Privacy-respecting analytics installed (Plausible or Fathom)
- [ ] Confirm no consent banner is required for the configuration chosen
- [ ] Confirm no third-party tracking cookies are set
- [ ] Uptime monitoring configured
- [ ] SSL expiry monitoring configured
- [ ] Domain expiry reminder set — for both `.com` and `.ge`
- [ ] Core Web Vitals field monitoring in place

---

## Phase 7 — First 30 days

Change nothing structural during this period. Let the site be crawled and indexed
before adding variables.

| Day | Action |
|---|---|
| 1 | Confirm homepage and `/about/` indexed |
| 3 | Check indexed count; investigate any exclusions |
| 7 | Full coverage review; confirm all pillars indexed |
| 7 | First name-query ranking check, recorded |
| 14 | Confirm all 10 articles indexed; check Georgian pages specifically |
| 14 | Review Performance report for first impressions and queries |
| 21 | Check for hreflang errors now that both language sets are indexed |
| 28 | Core Web Vitals field data should now be available |
| 30 | Full review; only now begin publishing to the editorial calendar (doc 05) |

**Do not** request indexing repeatedly for the same URL, add and remove pages,
change URLs, or install SEO plugins during this window. Each of those resets or
confuses the signal you are trying to read.

---

## Ongoing

| Task | Frequency |
|---|---|
| Search Console coverage and manual-action check | Weekly |
| Name-query position check, recorded | Weekly initially, then monthly |
| Core Web Vitals field data | Monthly |
| hreflang errors | Monthly |
| Core, theme and plugin updates — staging first | Weekly |
| Backup restore test | Monthly |
| Broken-link crawl | Quarterly |
| "Last reviewed" date refresh on technical articles | Annually per article |
| Verification report review as documents arrive | Ongoing |
| Publish per editorial calendar | Per doc 05 |
