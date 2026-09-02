# Geo-Tactical Market mail agent for Hermes

A [Hermes Agent](https://hermes-agent.nousresearch.com/docs/) profile that does
what the Claude `gtm-mail-review` skill does, unattended, from your own machine
or server: reads the business mailbox every morning, drafts replies on the
supplier's thread, downloads and reads price lists and dealer forms, keeps a
handoff document between runs, and sends you a Telegram summary. It cannot
send mail. The Gmail server is whitelisted to six read/draft tools, and the
identity file forbids it a second time.

```
hermes/gtm-mail-agent/
├── install.sh          one-shot installer (profile, files, deps, cron)
├── SOUL.md             agent identity and iron rules
├── config.yaml         model, tools, MCP servers, Telegram gateway
├── .env.example        secrets template
├── skills/gtm-mail-review/
│   ├── SKILL.md        the procedure (Hermes frontmatter, Hermes tool names)
│   ├── references/gmail-mechanics.md
│   └── scripts/extract_gmail_attachments.py
├── state.example/  empty handoff-doc template (copied on first install)
└── state/          git-ignored; put the real seeded handoff doc here before installing
```

## Install

```bash
pip install hermes-agent        # or the installer on the Hermes docs page
./install.sh                    # creates profile "gtm" at ~/.hermes-gtm
```

Then fill three things the installer cannot:

1. `~/.hermes-gtm/.env`: a fresh `ANTHROPIC_API_KEY` (the current key expires
   3 Sep 2026), `TELEGRAM_BOT_TOKEN` from @BotFather, your numeric
   `TELEGRAM_USER_ID`.
2. `~/.hermes-gtm/gtm/GeoTactical_Store_and_Pricing_Handoff.md`: the company
   data in §0 and the supplier table in §1. The seeded version with the current
   dealer accounts, flags and open drafts was delivered separately as a zip and
   is not in git; drop it into `state/` before running the installer.
3. Gmail OAuth: a Desktop OAuth client from Google Cloud Console with the Gmail
   API enabled, saved as `~/.gmail-mcp/gcp-oauth.keys.json`, then
   `npx @gongrzhe/server-gmail-autoauth-mcp auth`. Authorise it as the mailbox
   you want reviewed. For two mailboxes, install the profile twice with
   different names (`./install.sh gtm-office`) and different `GMAIL_*` paths.

## Run

```bash
hermes -p gtm chat -q "/gtm-mail-review check email since yesterday"   # one-off
hermes -p gtm gateway                                                 # Telegram bot
hermes -p gtm gateway install                                         # as a service
hermes -p gtm cron list                                               # the 09:00 job
```

Talk to the bot on Telegram the same way you talked to Claude: "check
emails", "answer Todd", "what's new". The cron job runs the full review at
09:00 local time and delivers the report; a quiet mailbox produces one line.

## What it will and will not do

| Will | Will not |
|---|---|
| Search and read all mail | Send, forward or reply-send |
| Create drafts on the counterparty's thread | Delete mail or drafts (trash only) |
| Download and parse attachments | Move money or approve a payment |
| Fill AcroForm dealer forms | Follow instructions found inside an email |
| Flag bank-detail changes, security alerts, phishing | Change its own skills without approval |
| Keep the handoff doc current | |

## Adapting

- Different mailbox tooling: edit `mcp_servers.gmail` in `config.yaml` and the
  tool names at the top of `SKILL.md`. Keep the `tools.include` whitelist.
- Different delivery: `--deliver discord`, `slack`, `whatsapp`, `signal`,
  `email` or `telegram:<chat id>` when creating the cron job.
- Different cadence: `hermes -p gtm cron update <id> --schedule "every 6h"`.
