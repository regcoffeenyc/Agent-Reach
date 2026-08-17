# Hosting, Domain and Deployment

Everything in this document requires an account holder with payment credentials.
None of it has been executed from this repository — the build environment has no
billing access, and provisioning infrastructure on someone's behalf is not
something to do unattended. Follow the steps in order.

---

## 1. Domain

### Primary — `goderdzimetreveli.com`

**Check availability and register.** Registrars that support the requirements
below: Cloudflare Registrar (at-cost pricing, free WHOIS privacy), Porkbun,
Namecheap.

Requirements:
- WHOIS privacy **on**
- Registrar lock **on**
- Auto-renew **on**, registered for 3–5 years (longer registration is a weak
  trust signal, and it removes an expiry risk on a reputation-critical asset)
- 2FA on the registrar account

**If the exact `.com` is taken:** check whether it resolves to anything. If it is
parked, an anonymous broker offer is usually cheaper than a named one. Fallbacks
in order of preference — `goderdzimetreveli.net`, `metreveli.ag`,
`goderdzimetreveli.co`. Avoid hyphenated variants and avoid `.info`/`.biz`,
which carry spam associations.

### Secondary — `goderdzimetreveli.ge`

`.ge` is administered by the Georgian registry (nic.ge) through accredited
registrars. Register it defensively and **301-redirect the whole domain** to the
`.com`. Do not serve the Georgian-language site from `.ge` — the `/ka/`
subdirectory on the primary domain consolidates all authority on one host, which
is the whole point of the hreflang setup in doc 01.

Redirect, at the DNS/host level rather than in WordPress:

```nginx
server {
    server_name goderdzimetreveli.ge www.goderdzimetreveli.ge;
    return 301 https://goderdzimetreveli.com$request_uri;
}
```

Also register the `www` variant of the `.com` and redirect it to the apex (or the
reverse — pick one canonical host and be consistent everywhere: sitemap,
canonicals, Search Console, internal links).

---

## 2. Hosting

**Requirement from the brief: managed WordPress hosting.** Shared cPanel hosting
will not hold Core Web Vitals on a photography-heavy site.

| Option | Notes |
|---|---|
| **Kinsta** | GCP premium tier, per-site edge caching, staging built in. Strong default choice. |
| **WP Engine** | Comparable; good staging and transferable installs. |
| **Cloudways** (Vultr HF) | Cheaper, slightly more hands-on. |
| **SiteGround GoGeek** | Budget option; adequate but weaker at scale. |

Whichever is chosen, confirm it provides: PHP 8.2+, HTTP/2 or HTTP/3, free
auto-renewing SSL, a staging environment, daily automatic backups with off-site
retention, server-level page caching, and an object cache (Redis/Memcached).

**Server location:** choose an EU region (Frankfurt or Warsaw) — closest to both
the Georgian and the European audiences, and it keeps data handling within a
GDPR-aligned jurisdiction.

---

## 3. CDN and images

Put **Cloudflare** in front of the host (free tier is sufficient to start):

- Proxied DNS (orange cloud)
- SSL/TLS mode **Full (strict)**
- **Always Use HTTPS** on
- **Automatic HTTPS Rewrites** on
- HSTS on, `max-age=31536000`, once HTTPS is confirmed stable
- Brotli on
- Early Hints on
- Cache rule: bypass cache for `/wp-admin/*` and `wp-login.php`

**Images.** The theme ships with `<picture>` output preferring AVIF, then WebP,
then the original. Either:

- enable Cloudflare Polish + Mirage (Pro plan), **or**
- convert at upload time with an optimiser plugin, **or**
- pre-convert before upload — best quality control, recommended for the hero and
  case-study photography.

Target: hero images under 200 KB at 2000 px wide in AVIF. Everything below the
fold is lazy-loaded by the theme; the LCP image is explicitly **not** lazy-loaded
and is preloaded (see `inc/performance.php`).

Filenames must be descriptive before upload — `almond-orchard-udabno-aerial-2021.avif`,
not `IMG_4821.jpg`. This is not cosmetic; it is one of the few remaining
filename-level ranking signals in image search.

---

## 4. WordPress installation

```bash
# 1. Install WordPress via the host's installer, then:

# 2. Theme
cd wp-content/themes/
# copy sites/goderdzimetreveli.com/theme/goderdzi-metreveli/ here
wp theme activate goderdzi-metreveli

# 3. Permalinks
wp option update permalink_structure '/articles/%postname%/'

# 4. Discourage indexing OFF only at launch (keep ON while staging)
wp option update blog_public 1

# 5. Site identity
wp option update blogname 'Goderdzi Metreveli'
wp option update blogdescription 'Regenerative Agriculture and Almond Farming'

# 6. Content
wp plugin install wordpress-importer --activate
wp import ../../../sites/goderdzimetreveli.com/import/goderdzi-metreveli.wxr.xml --authors=create

# 7. Menus, after import
wp menu create "Primary"
wp menu location assign Primary primary
```

Regenerate the WXR from the markdown at any time:

```bash
python3 sites/goderdzimetreveli.com/tools/build_wxr.py
```

### Hardening

```php
// wp-config.php
define( 'DISALLOW_FILE_EDIT', true );
define( 'WP_AUTO_UPDATE_CORE', 'minor' );
define( 'FORCE_SSL_ADMIN', true );
```

Plus: unique admin username (never `admin`), 2FA on all admin accounts, XML-RPC
disabled unless needed, and the REST API user-enumeration endpoint restricted.

---

## 5. Staging discipline

Keep a staging site permanently. Two rules:

1. Staging must be **password-protected at HTTP level** *and* carry
   `X-Robots-Tag: noindex`. A staging copy of a reputation site that gets indexed
   creates duplicate-content competition against the real site under the person's
   own name — the exact failure this project exists to prevent.
2. `blog_public` stays `0` on staging permanently.

The theme detects a non-production hostname and forces `noindex` as a second
safety net (`inc/seo.php`), but do not rely on that alone.

---

## 6. Launch sequence

1. Build on staging, fully populated, with real photography.
2. Complete the fact-verification sign-off (doc 07 §7). **Blocking.**
3. Native Georgian proofread of all `/ka/` pages. **Blocking.**
4. Validate structured data — Rich Results Test + Schema.org validator.
5. Lighthouse: mobile performance ≥ 90, accessibility ≥ 95.
6. Crawl staging (Screaming Frog) — zero broken links, zero orphan pages, one H1 per page.
7. Push to production, set `blog_public 1`.
8. Confirm HTTPS, redirects (`www`, `.ge`), and canonical host.
9. Submit `/sitemap.xml` to Search Console and Bing (doc 06).
10. Monitor for 30 days before adding new content.

---

## 7. Ongoing operations

| Task | Frequency |
|---|---|
| WordPress core, theme, plugin updates | Weekly, on staging first |
| Off-site backup verification (restore test) | Monthly |
| Search Console coverage and manual-action check | Weekly |
| Core Web Vitals field data review | Monthly |
| Broken-link crawl | Quarterly |
| "Last reviewed" date refresh on technical articles | Every 12 months |
| Verification-report review as new documents arrive | Ongoing |
| SSL and domain expiry check | Quarterly |

---

## 8. Analytics — privacy-respecting

Use **Plausible** or **Fathom** (both cookieless, EU-hosted, no consent banner
required under most readings of GDPR/ePrivacy for strictly aggregate analytics).

Avoid Google Analytics 4 here. It requires a consent banner in the EU, adds
client-side weight, and provides far more than this site needs. Search Console
supplies the search data that actually matters.

Do not add heatmap or session-recording tools — on a personal reputation site
they create a disproportionate privacy footprint for negligible benefit.

---

## 9. GitHub

Per the brief: GitHub is a **private code repository and technical backup only**,
never the public website. GitHub Pages must not serve this content — a
`github.io` or Pages-hosted copy would compete with the real domain for the
person's own name.

- Keep the theme, content markdown and docs in version control.
- Deploy the theme to the host via SFTP, the host's Git integration, or a
  deployment action.
- **Never** enable GitHub Pages on this repository path.
- Ensure `robots.txt` on any preview host disallows everything.
