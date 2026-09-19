#!/usr/bin/env bash
# Preflight for the Geo-Tactical Market Hermes profile. Run before `hermes gateway`
# or the first chat, and any time something looks off. Exits non-zero on any
# failure so it can gate a service start:  ./preflight.sh && hermes -p gtm gateway
set -euo pipefail

PROFILE="${1:-gtm}"
HOME_DIR="${HERMES_HOME:-$HOME/.hermes-$PROFILE}"
fail=0
say()  { printf '   %s\n' "$*"; }
bad()  { printf 'FAIL %s\n' "$*"; fail=1; }
mode_of() { stat -c '%a' "$1" 2>/dev/null || stat -f '%Lp' "$1"; }

echo "== preflight: profile $PROFILE ($HOME_DIR)"

# 1. .env present, restricted, and filled
ENV_FILE="$HOME_DIR/.env"
if [ ! -f "$ENV_FILE" ]; then
  bad ".env missing at $ENV_FILE (run install.sh)"
else
  m=$(mode_of "$ENV_FILE")
  [ "$m" = "600" ] || bad ".env is mode $m; run: chmod 600 $ENV_FILE"
  # shellcheck disable=SC1090
  set -a; . "$ENV_FILE"; set +a
  [ -n "${ANTHROPIC_API_KEY:-}" ]  || bad "ANTHROPIC_API_KEY is empty"
  [ -n "${TELEGRAM_BOT_TOKEN:-}" ] || bad "TELEGRAM_BOT_TOKEN is empty"
  if [ -z "${TELEGRAM_USER_ID:-}" ]; then
    bad "TELEGRAM_USER_ID is empty: the gateway allowlist would be blank. Never start the bot like this."
  elif ! [[ "${TELEGRAM_USER_ID}" =~ ^[0-9]+$ ]]; then
    bad "TELEGRAM_USER_ID must be your numeric id, got '${TELEGRAM_USER_ID}'"
  fi
fi

# 2. Gmail OAuth files inside the profile, not world-readable
GMAIL_DIR="$HOME_DIR/gmail"
if [ ! -d "$GMAIL_DIR" ]; then
  bad "$GMAIL_DIR missing (run install.sh)"
else
  m=$(mode_of "$GMAIL_DIR")
  [ "$m" = "700" ] || bad "$GMAIL_DIR is mode $m; run: chmod 700 $GMAIL_DIR"
  for f in gcp-oauth.keys.json credentials.json; do
    p="$GMAIL_DIR/$f"
    if [ ! -f "$p" ]; then
      bad "$p missing (see README: Gmail OAuth)"
    else
      m=$(mode_of "$p")
      [ "$m" = "600" ] || bad "$p is mode $m; run: chmod 600 $p"
    fi
  done
fi

# 3. config.yaml still carries the safety properties this profile depends on
CFG="$HOME_DIR/config.yaml"
if [ ! -f "$CFG" ]; then
  bad "config.yaml missing"
else
  grep -q 'server-gmail-autoauth-mcp@[0-9]' "$CFG" || bad "Gmail MCP server is not version-pinned in config.yaml"
  for t in send_email delete_email batch_delete_emails modify_email; do
    grep -qE "^\s*-\s*$t\s*$" "$CFG" && bad "config.yaml whitelists $t; remove it"
  done
  # web_search must appear only under tools.disabled
  if awk '/^tools:/{t=1;next} t&&/^[^ ]/{t=0} t' "$CFG" | awk '/enabled:/{e=1} /disabled:/{e=0} e' | grep -q web_search; then
    bad "web_search is under tools.enabled; move it to tools.disabled"
  fi
fi

# 4. handoff doc present and not the empty template
DOC="$HOME_DIR/gtm/GeoTactical_Store_and_Pricing_Handoff.md"
if [ ! -f "$DOC" ]; then
  bad "handoff doc missing at $DOC"
elif grep -qE '^\| Company ID / VAT number \| *\|$' "$DOC"; then
  bad "handoff doc §0 is unfilled (Company ID cell is empty)"
fi

# 5. work dir exists and is writable
mkdir -p "$HOME_DIR/gtm/work" 2>/dev/null || bad "cannot create $HOME_DIR/gtm/work"
[ -w "$HOME_DIR/gtm/work" ] || bad "$HOME_DIR/gtm/work is not writable"

if [ "$fail" -ne 0 ]; then
  echo "== preflight FAILED: fix the lines above before starting the gateway or the cron job"
  exit 1
fi
say "all checks passed"
