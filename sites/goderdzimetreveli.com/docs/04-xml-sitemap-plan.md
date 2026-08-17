# XML Sitemap Plan

Implemented in `theme/goderdzi-metreveli/inc/sitemap.php`. WordPress core
sitemaps are disabled because they list author and term archives that this site
deliberately keeps out of the index, and they have no image support — which
matters on a site whose differentiator is original field photography.

---

## 1. Structure

```
/sitemap.xml                 ← index
├── /sitemap-pages.xml       ← English pages + homepage
├── /sitemap-articles.xml    ← technical articles (posts)
├── /sitemap-ka.xml          ← Georgian pages
└── /sitemap-images.xml      ← images attached to published content
```

Splitting by type rather than dumping everything into one file makes Search
Console's coverage reporting useful: if Georgian pages are not being indexed, or
articles are being dropped, the report shows it per sitemap instead of averaging it
away.

---

## 2. What each contains

### `/sitemap-pages.xml`

The homepage plus all published English pages: About, Experience, Achievements,
Expertise, Projects, the five pillars, Mechanization, Media, Articles index,
Speaking, Evidence, Contact, and both case studies.

Includes `<lastmod>` from `post_modified_gmt`, and `<xhtml:link>` hreflang
alternates for any page with a published Georgian counterpart.

### `/sitemap-articles.xml`

All published posts. `<lastmod>` reflects the last modification, which for
technical articles is meaningful — the "last reviewed" discipline means these
dates change and should be seen to change.

### `/sitemap-ka.xml`

The 13 Georgian pages, each with reciprocal hreflang alternates back to its
English counterpart.

### `/sitemap-images.xml`

Every image attached to published content, with `<image:loc>`, plus
`<image:title>` from the alt text and `<image:caption>` from the attachment
caption where present.

This file is the reason the sitemap is custom. The site's evidence value is
photographic — soil profiles, before/after landscape pairs, machinery in work —
and image search is a real discovery channel for that material. Descriptive
filenames and accurate alt text (doc 08, doc 10 §3) are what make it work.

---

## 3. Excluded, and why

| Excluded | Reason |
|---|---|
| Category archives | Thin, and duplicative of the pillar pages, which are the pages meant to rank |
| Tag archives | Tags not used |
| Author archives | One author; `/about/` is the canonical author entity |
| Date archives | No value for this content |
| Search results | Never indexable |
| Attachment pages | Redirected to parent (`gm_kill_attachment_pages`) |
| Paginated archive pages | Only page 1 of `/articles/` is submitted |
| Any page with `_gm_noindex` set | Editor-level opt-out, respected by the sitemap query |
| Everything, on non-production hosts | `gm_render_sitemap()` returns 404 when `gm_is_non_production()` — a staging sitemap is an invitation to index a duplicate of the site under the person's own name |

The sitemap and the `noindex` policy in `inc/seo.php` are driven by the same
conditions, so they cannot drift apart.

---

## 4. Deliberate omissions from the markup

**No `<priority>`** except `1.0` on the homepage. Google has stated it ignores
the field. Populating it across 50 URLs is busywork that also invites the
temptation to fiddle with it instead of improving pages.

**No `<changefreq>`** except `weekly` on the homepage, for the same reason.
`<lastmod>` is the field that is actually used, and it is populated accurately
from the database rather than guessed.

Accurate `lastmod` matters more than most people assume: a sitemap where every
`lastmod` updates on every deploy trains crawlers to distrust the field entirely.
Because these values come from `post_modified_gmt`, they change only when content
actually changes.

---

## 5. hreflang in the sitemap

Emitted for any page with a published counterpart, as `<xhtml:link>` entries
listing **both** URLs in **each** URL's entry — reciprocal, which is required for
the annotation to be honoured.

This duplicates the `<link rel="alternate">` tags in the page `<head>`. That
duplication is intentional: the two mechanisms are independent, Search Console's
International Targeting report reads the sitemap version, and having both means a
templating error in one does not silently disable the annotation.

---

## 6. Scale

Current: roughly 50 URLs plus images. The sitemap protocol's limits are 50,000
URLs and 50 MB uncompressed per file, so no splitting or compression is needed
now.

`gm_sitemap_query()` caps at 2,000 posts per type. If the site ever approaches
that, paginate per type rather than raising the cap — a single enormous sitemap is
slow to generate on every request and awkward to diagnose.

---

## 7. robots.txt

Emitted by `gm_robots_txt()` in `inc/seo.php`:

```
User-agent: *
Allow: /
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
Disallow: /wp-login.php
Disallow: /?s=
Disallow: /search/
Disallow: /*?replytocom=

Sitemap: https://goderdzimetreveli.com/sitemap.xml
```

On any non-production host this becomes `User-agent: * / Disallow: /` instead.

Note that `Disallow` is not `noindex` — the crawl directives above prevent
crawling of admin and search URLs, while the indexation policy is enforced
separately via `wp_robots` and `X-Robots-Tag`. A URL blocked in robots.txt can
still be indexed if linked externally, which is why both mechanisms exist.

---

## 8. Submission and monitoring

Submission steps are in doc 06. Ongoing:

| Check | Frequency |
|---|---|
| Sitemap read successfully, no parse errors | Weekly for the first month, then monthly |
| Submitted vs. indexed count per sitemap | Weekly for the first month |
| `lastmod` values updating when content changes | After each content update |
| Image sitemap being read; images appearing in image search | Monthly |
| hreflang errors in the International Targeting report | Monthly |
| Nothing indexed that should be excluded (search `site:` for staging hosts, tag URLs) | Monthly |

A persistent gap between submitted and indexed on `/sitemap-ka.xml` specifically
is the signal to watch — it usually means either the hreflang cluster is broken or
the Georgian content is being treated as duplicative.
