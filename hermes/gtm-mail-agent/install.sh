#!/usr/bin/env bash
# Installs the Geo-Tactical Market mail agent as a Hermes profile named "gtm".
# Idempotent: re-running updates SOUL.md, config.yaml and the skill in place and
# never overwrites .env or the handoff doc.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROFILE="${1:-gtm}"
HOME_DIR="${HERMES_HOME:-$HOME/.hermes-$PROFILE}"

command -v hermes >/dev/null || { echo "hermes CLI not found. Install Hermes Agent first: https://hermes-agent.nousresearch.com/docs/"; exit 1; }
command -v npx    >/dev/null || { echo "npx not found. Install Node.js 18+ (the Gmail MCP server runs via npx)."; exit 1; }

echo "== profile: $PROFILE  ($HOME_DIR)"
if ! hermes profile list 2>/dev/null | grep -qw "$PROFILE"; then
  hermes profile create "$PROFILE"
fi
mkdir -p "$HOME_DIR/skills/gtm-mail-review" "$HOME_DIR/gtm/work" "$HOME_DIR/memories"

echo "== identity, config, skill"
cp  "$HERE/SOUL.md"      "$HOME_DIR/SOUL.md"
cp  "$HERE/config.yaml"  "$HOME_DIR/config.yaml"
cp -R "$HERE/skills/gtm-mail-review/." "$HOME_DIR/skills/gtm-mail-review/"

if [ ! -f "$HOME_DIR/.env" ]; then
  cp "$HERE/.env.example" "$HOME_DIR/.env"
  echo "   wrote $HOME_DIR/.env — FILL IT IN before the first run"
fi
if [ ! -f "$HOME_DIR/gtm/GeoTactical_Store_and_Pricing_Handoff.md" ]; then
  if [ -f "$HERE/state/GeoTactical_Store_and_Pricing_Handoff.md" ]; then
    cp "$HERE/state/GeoTactical_Store_and_Pricing_Handoff.md" "$HOME_DIR/gtm/"
    echo "   seeded handoff doc from state/ — fill the [FILL IN] cells in §0"
  else
    cp "$HERE/state.example/GeoTactical_Store_and_Pricing_Handoff.md" "$HOME_DIR/gtm/"
    echo "   created an EMPTY handoff doc — fill §0 and §1 before the first run"
  fi
fi

echo "== python deps for form filling and price lists"
python3 -m pip install --quiet --user pypdf pdfplumber openpyxl xlrd 2>/dev/null || true

echo "== Gmail OAuth (opens a browser once; token is cached under ~/.gmail-mcp)"
if [ ! -f "$HOME/.gmail-mcp/credentials.json" ]; then
  echo "   put your Google OAuth client file at ~/.gmail-mcp/gcp-oauth.keys.json first"
  echo "   (Google Cloud Console → APIs & Services → Credentials → OAuth client, Desktop app,"
  echo "    with the Gmail API enabled), then run:  npx @gongrzhe/server-gmail-autoauth-mcp auth"
else
  echo "   token present, skipping"
fi

echo "== daily cron (09:00 local, delivered to Telegram)"
if ! hermes -p "$PROFILE" cron list 2>/dev/null | grep -q "gtm-mail-review"; then
  hermes -p "$PROFILE" cron create "every day at 9am" \
    "Run the daily Geo-Tactical Market mailbox review. Read the handoff doc first, sweep mail since the last-run date in its header, draft replies on-thread, download attachments, update the handoff doc, and report. Never send. If nothing new arrived, reply QUIET." \
    --skill gtm-mail-review --name gtm-mail-review --deliver telegram \
    --continuity --reasoning-effort medium
else
  echo "   job exists, skipping"
fi

cat <<MSG

Done. Next:
  1. Fill $HOME_DIR/.env  (ANTHROPIC_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_USER_ID)
  2. Fill $HOME_DIR/gtm/GeoTactical_Store_and_Pricing_Handoff.md (§0 company data, §1 suppliers)
  3. Gmail auth (see above) if not done
  4. Test:   hermes -p $PROFILE chat -q "/gtm-mail-review check email since yesterday"
  5. Run the bot:   hermes -p $PROFILE gateway     (or: hermes -p $PROFILE gateway install)
MSG
