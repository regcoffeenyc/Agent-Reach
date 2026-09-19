# Structured Data

The theme generates all JSON-LD at runtime (`theme/goderdzi-metreveli/inc/schema.php`).
The files here are the **reference specimens** — what the theme should output for
each page type. Use them to review changes and to diff against live output, not as
files to paste into a page.

## Files

| File | Page type |
|---|---|
| `homepage.jsonld` | `/` — Person + WebSite + WebPage |
| `profilepage.jsonld` | `/about/` — Person + WebSite + ProfilePage |
| `article.jsonld` | any post — Person + WebSite + WebPage + BreadcrumbList + Article |
| `pillar.jsonld` | a pillar page — Person + WebSite + WebPage + BreadcrumbList |

## Properties deliberately absent

These omissions are required by `docs/07-fact-verification-report.md` §6 and are
not oversights. Do not add them without a documented verification.

| Property | Why absent |
|---|---|
| `alumniOf` | Education unverified — no institution, degree or date documented |
| `award` on `Person` | The 2023 SDG 12 recognition went to Udabno Group and its project team. It appears in visible page text, described as organisational, and nowhere in the Person graph |
| `worksFor` | Current employment unverified; the relationships described are historical |
| `affiliation` | Board membership at Adjara Group Holding unverified |
| `jobTitle` beyond a generic descriptor | Specific titles and dates are unverified; the graph carries only "Agricultural Executive", which every source supports |
| `sameAs` entries beyond LinkedIn | Only the confirmed official profile is permitted. An incorrect or duplicate `sameAs` damages entity resolution rather than helping it |

`sameAs` is populated from Customizer → Entity and structured data. Until a URL
is set there, the key is **omitted entirely** rather than emitted empty.

## The rule that governs all of this

**Structured data must match visible page content.** Every property in the graph
corresponds to something a reader can see on the page. This is a requirement for
rich-results eligibility, and independently it is the only defensible position for
a site whose purpose is to be checkable.

Adding a property the page does not state is the same error as putting an
unverified claim in the body copy — it is just less visible, which makes it worse.

## Validation

Before launch and after any change to `inc/schema.php`:

1. [Rich Results Test](https://search.google.com/test/rich-results)
2. [Schema.org validator](https://validator.schema.org/)
3. Manually diff live output against the specimens here
4. Confirm `@id` values resolve consistently — one `Person` node referenced by
   `@id` everywhere, never duplicated inline

## Why no SEO plugin

Yoast, RankMath and AIOSEO all emit their own `Person` or `Organization` graph.
Running one alongside this theme would produce two Person nodes — the theme's,
carefully limited to verified properties, and the plugin's, populated from whatever
is in its settings. The second would very likely contradict the verification report
and would not be under version control.

Keeping schema in the theme means it is reviewable in a diff, and it means there is
exactly one place where a claim can enter the graph.
