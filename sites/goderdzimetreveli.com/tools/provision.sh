#!/usr/bin/env bash
#
# Post-import provisioning for goderdzimetreveli.com.
#
# The WXR import creates pages and posts but NOT navigation menus, the front-page
# assignment, or the removal of WordPress's default sample content. Without this
# step the site renders with no navigation at all, and "Hello world!" appears in
# the homepage's latest-articles block.
#
# Usage, from the WordPress root:
#     bash /path/to/tools/provision.sh
#
# Requires wp-cli on PATH (or set WP=/path/to/wp-cli.phar). Idempotent: safe to
# re-run — menus are deleted and rebuilt rather than duplicated.

set -euo pipefail

WP="${WP:-wp}"
if [[ "$WP" == *.phar ]]; then WP="php $WP"; fi
WPX=( $WP )
[[ "${ALLOW_ROOT:-0}" == "1" ]] && WPX+=( --allow-root )

wpx() { "${WPX[@]}" "$@"; }

say() { printf '\n\033[1m%s\033[0m\n' "$*"; }

# Resolve a page ID from its full slug path, e.g. "ka/shesakheb".
pid() {
  wpx eval "\$p = get_page_by_path('$1'); echo \$p ? \$p->ID : 0;" 2>/dev/null || echo 0
}

say "1. Permalinks"
wpx option update permalink_structure '/articles/%postname%/' >/dev/null
wpx option update blogname 'Goderdzi Metreveli' >/dev/null
wpx option update blogdescription 'Regenerative Agriculture and Almond Farming' >/dev/null
echo "   /articles/%postname%/"

say "2. Front page and posts page"
HOME_ID=$(pid home)
if [[ "$HOME_ID" == "0" ]]; then
  # Fallback for imports made before the home page had an explicit slug: the
  # importer generates one from the title, so match on the title instead.
  HOME_ID=$(wpx eval '
    $q = new WP_Query([
      "post_type"      => "page",
      "post_status"    => "publish",
      "title"          => "Goderdzi Metreveli",
      "posts_per_page" => 1,
      "fields"         => "ids",
    ]);
    echo $q->posts ? (int) $q->posts[0] : 0;')
fi
ART_ID=$(pid articles)
if [[ "$HOME_ID" == "0" || "$ART_ID" == "0" ]]; then
  echo "   ERROR: could not find the home page (empty slug) or /articles/." >&2
  echo "   Has the WXR been imported? Aborting." >&2
  exit 1
fi
wpx option update show_on_front page >/dev/null
wpx option update page_on_front "$HOME_ID" >/dev/null
wpx option update page_for_posts "$ART_ID" >/dev/null
echo "   front page = $HOME_ID, posts page = $ART_ID"

say "3. Remove WordPress default content"
# These otherwise appear in the sitemap and in the homepage latest-articles block.
for slug in sample-page hello-world; do
  ID=$(wpx eval "\$p = get_page_by_path('$slug','OBJECT',['page','post']); echo \$p ? \$p->ID : 0;")
  if [[ "$ID" != "0" ]]; then
    wpx post delete "$ID" --force >/dev/null
    echo "   deleted $slug (#$ID)"
  fi
done
wpx eval '
  $n = 0;
  foreach ( get_comments(["status"=>"all"]) as $c ) { wp_delete_comment($c->comment_ID, true); $n++; }
  echo "   deleted $n default comment(s)\n";'
# Privacy Policy draft ships with core and is harmless but pointless here.
PP=$(wpx option get wp_page_for_privacy_policy 2>/dev/null || echo 0)
if [[ "${PP:-0}" != "0" ]]; then
  wpx post delete "$PP" --force >/dev/null 2>&1 && echo "   deleted privacy policy draft (#$PP)" || true
fi

say "4. Navigation menus"
for m in Primary "Footer Topics" "Footer About" \
         "Primary KA" "Footer Topics KA" "Footer About KA"; do
  wpx menu delete "$m" >/dev/null 2>&1 || true
done

wpx menu create "Primary"           >/dev/null
wpx menu create "Footer Topics"     >/dev/null
wpx menu create "Footer About"      >/dev/null
wpx menu create "Primary KA"        >/dev/null
wpx menu create "Footer Topics KA"  >/dev/null
wpx menu create "Footer About KA"   >/dev/null

# add() <menu> <slug-path> <nav-label> [parent-item-id] -> prints new item id
#
# The nav label is set explicitly rather than inherited from the page title.
# Page titles here are deliberately long and descriptive for search results —
# "Deep-Ripping and Soil Preparation for Orchard Establishment" is right in a
# <title> and unusable in a navigation bar.
add() {
  local menu="$1" slug="$2" label="$3" parent="${4:-}"
  local id item
  id=$(pid "$slug")
  [[ "$id" == "0" ]] && { echo "   warn: page '$slug' not found, skipped" >&2; echo 0; return; }
  if [[ -n "$parent" && "$parent" != "0" ]]; then
    item=$(wpx menu item add-post "$menu" "$id" --parent-id="$parent" --porcelain)
  else
    item=$(wpx menu item add-post "$menu" "$id" --porcelain)
  fi
  wpx menu item update "$item" --title="$label" >/dev/null
  echo "$item"
}

# --- Primary ---
add Primary about      "About"      >/dev/null
add Primary experience "Experience" >/dev/null
EXP=$(add Primary expertise "Expertise")
add Primary regenerative-agriculture  "Regenerative Agriculture"    "$EXP" >/dev/null
add Primary almond-orchards           "Almond Orchards"             "$EXP" >/dev/null
add Primary deep-ripping              "Deep Ripping"                "$EXP" >/dev/null
add Primary irrigation-infrastructure "Irrigation & Infrastructure" "$EXP" >/dev/null
add Primary mechanization             "Mechanization"               "$EXP" >/dev/null
add Primary almond-processing-export  "Processing & Export"         "$EXP" >/dev/null
PRJ=$(add Primary projects "Projects")
add Primary projects/udabno-semi-arid-development "Udabno Semi-Arid Development" "$PRJ" >/dev/null
add Primary projects/almond-value-chain           "Almond Value Chain"           "$PRJ" >/dev/null
add Primary evidence                              "Evidence & Gallery"           "$PRJ" >/dev/null
add Primary articles "Articles" >/dev/null
add Primary media    "Media"    >/dev/null
add Primary contact  "Contact"  >/dev/null

# --- Footer: Topics ---
add "Footer Topics" regenerative-agriculture  "Regenerative Agriculture"    >/dev/null
add "Footer Topics" almond-orchards           "Almond Orchards"             >/dev/null
add "Footer Topics" deep-ripping              "Deep Ripping"                >/dev/null
add "Footer Topics" irrigation-infrastructure "Irrigation & Infrastructure" >/dev/null
add "Footer Topics" mechanization             "Mechanization"               >/dev/null
add "Footer Topics" almond-processing-export  "Processing & Export"         >/dev/null

# --- Footer: About ---
add "Footer About" about        "Biography"    >/dev/null
add "Footer About" experience   "Experience"   >/dev/null
add "Footer About" achievements "Achievements" >/dev/null
add "Footer About" speaking     "Speaking"     >/dev/null
add "Footer About" evidence     "Evidence"     >/dev/null

# --- Georgian: Primary ---
# Georgian nav links only to Georgian pages. Pages with no Georgian counterpart
# (Projects, Speaking, Evidence, the articles) are deliberately absent rather than
# linking a Georgian reader into English.
add "Primary KA" ka/shesakheb     "შესახებ"     >/dev/null
add "Primary KA" ka/gamotsdileba  "გამოცდილება" >/dev/null
EXPKA=$(add "Primary KA" ka/spetsializatsia "სპეციალიზაცია")
add "Primary KA" ka/regeneratsiuli-sofmeurneoba "რეგენერაციული მეურნეობა"  "$EXPKA" >/dev/null
add "Primary KA" ka/nushis-baghebi             "ნუშის ბაღები"             "$EXPKA" >/dev/null
add "Primary KA" ka/ghrma-gafkhviereba         "ღრმა გაფხვიერება"         "$EXPKA" >/dev/null
add "Primary KA" ka/irigatsia-infrastruktura   "ირიგაცია და ინფრასტრუქტურა" "$EXPKA" >/dev/null
add "Primary KA" ka/mekanizatsia               "მექანიზაცია"              "$EXPKA" >/dev/null
add "Primary KA" ka/gadamushaveba-eksporti     "გადამუშავება და ექსპორტი" "$EXPKA" >/dev/null
add "Primary KA" ka/mightsevebi "მიღწევები" >/dev/null
add "Primary KA" ka/media       "მედია"     >/dev/null
add "Primary KA" ka/kontakti    "კონტაქტი"  >/dev/null

# --- Georgian: Footer ---
add "Footer Topics KA" ka/regeneratsiuli-sofmeurneoba "რეგენერაციული მეურნეობა"    >/dev/null
add "Footer Topics KA" ka/nushis-baghebi             "ნუშის ბაღები"               >/dev/null
add "Footer Topics KA" ka/ghrma-gafkhviereba         "ღრმა გაფხვიერება"           >/dev/null
add "Footer Topics KA" ka/irigatsia-infrastruktura   "ირიგაცია და ინფრასტრუქტურა" >/dev/null
add "Footer Topics KA" ka/mekanizatsia               "მექანიზაცია"                >/dev/null
add "Footer Topics KA" ka/gadamushaveba-eksporti     "გადამუშავება და ექსპორტი"   >/dev/null

add "Footer About KA" ka/shesakheb    "ბიოგრაფია"   >/dev/null
add "Footer About KA" ka/gamotsdileba "გამოცდილება" >/dev/null
add "Footer About KA" ka/mightsevebi  "მიღწევები"   >/dev/null

wpx menu location assign Primary primary                    >/dev/null
wpx menu location assign "Footer Topics" footer_topics       >/dev/null
wpx menu location assign "Footer About"  footer_about        >/dev/null
wpx menu location assign "Primary KA" primary_ka             >/dev/null
wpx menu location assign "Footer Topics KA" footer_topics_ka >/dev/null
wpx menu location assign "Footer About KA"  footer_about_ka  >/dev/null
echo "   6 menus created and assigned (3 English, 3 Georgian)"

say "5. Discussion + media settings"
wpx option update default_comment_status closed >/dev/null
wpx option update default_ping_status closed    >/dev/null
wpx option update comment_registration 1        >/dev/null
# Attachment pages are redirected by the theme; also stop core generating them.
wpx option update wp_attachment_pages_enabled 0 >/dev/null 2>&1 || true

say "6. Flush rewrites"
wpx rewrite flush >/dev/null 2>&1 || true

say "Done."
cat <<'EOF'

Remaining manual steps (these need your input, not a script):

  * Customizer -> Entity and structured data
      - Confirmed LinkedIn URL   (sameAs stays empty until you set it)
      - Professional portrait    (hero shows a typographic mark until then)
      - Default social sharing image

  * Contact details on /contact/ and /ka/kontakti/

  * Settings -> Reading: leave "Discourage search engines" UNCHECKED on
    production, CHECKED on staging.

  * Confirm WP_ENVIRONMENT_TYPE is set correctly in wp-config.php. The theme
    treats an explicit 'production' as authoritative; on staging set
    'staging' so noindex, Disallow: / and 404 sitemaps all engage.
EOF
