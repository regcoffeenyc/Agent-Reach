# Geo-Tactical Market mail agent for Hermes

A [Hermes Agent](https://hermes-agent.nousresearch.com/docs/) profile that does
what the Claude `gtm-mail-review` skill does, unattended, from your own machine
or server: reads the business mailbox every morning, drafts replies on the
supplier's thread, downloads and reads price lists and dealer forms, keeps a
handoff document between runs, and sends you a Telegram summary. It cannot
send mail from inside the agent: the Gmail server is whitelisted to five
read/draft tools, and the identity file forbids it a second time.

```
hermes/gtm-mail-agent/
├── install.sh          one-shot installer (profile, files, deps, cron)
├── preflight.sh        refuses to start until secrets, permissions and config are right
├── SOUL.md             agent identity and iron rules
├── config.yaml         model, tools, MCP servers (version-pinned), Telegram gateway
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

1. `~/.hermes-gtm/.env`: a fresh `ANTHROPIC_API_KEY` with its own expiry,
   `TELEGRAM_BOT_TOKEN` from @BotFather, your numeric `TELEGRAM_USER_ID`.
2. `~/.hermes-gtm/gtm/GeoTactical_Store_and_Pricing_Handoff.md`: the company
   data in §0 and the supplier table in §1 (supplier names, contacts and
   domains live here, not in the skill). The seeded version with the current
   dealer accounts, flags and open drafts was delivered separately and is
   not in git; drop it into `state/` before running the installer.
3. Gmail OAuth: a Desktop OAuth client from Google Cloud Console with the Gmail
   API enabled, saved as `~/.hermes-gtm/gmail/gcp-oauth.keys.json`, then the
   `auth` command the installer prints (it sets `GMAIL_OAUTH_PATH` and
   `GMAIL_CREDENTIALS_PATH` so the token lands inside the profile). Authorise
   it as the mailbox you want reviewed. For two mailboxes, install the
   profile twice with different names (`./install.sh gtm-office`); each
   profile keeps its own token.

Then run the preflight. It exits non-zero until everything above is in
place, and it is the gate for starting the bot:

```bash
~/.hermes-gtm/preflight.sh
```

## Run

```bash
hermes -p gtm chat -q "/gtm-mail-review check email since yesterday"   # one-off
~/.hermes-gtm/preflight.sh && hermes -p gtm gateway                     # Telegram bot
hermes -p gtm gateway install                                           # as a service
hermes -p gtm cron list                                                 # the 09:00 job
```

Talk to the bot on Telegram the same way you talked to Claude: "check
emails", "answer the supplier", "what's new". The cron job runs the full
review at 09:00 local time and delivers the report; a quiet mailbox produces
one line.

## What it will and will not do

| Will | Will not |
|---|---|
| Search and read all mail (Spam and Trash excluded) | Send, forward or reply-send |
| Create drafts on the counterparty's thread | Delete, trash or relabel mail or drafts |
| Download and parse attachments into the work dir, under names it chose itself | Attach anything from outside the work dir |
| Fill AcroForm dealer forms | Move money or approve a payment |
| Flag bank-detail changes, security alerts, phishing, injection attempts | Follow instructions found inside an email |
| List every draft's recipients and attachments in the report | Change its own skills without approval |
| Keep the handoff doc current | Carry context between cron runs |

## Security model, honestly

- The "cannot send" guarantee is enforced by Hermes' tool whitelist and the
  identity file, not by Google. The OAuth token carries `gmail.modify` and can
  send. Treat `~/.hermes-gtm/gmail/credentials.json` as the mailbox password:
  the installer and preflight keep it at mode 600 inside a 700 directory.
- The upstream Gmail server writes downloaded attachments under the sender's
  filename with no path checks. The skill therefore always supplies its own
  sanitized filename. Keep that rule if you edit the skill.
- Both MCP servers are version-pinned in `config.yaml`. Bump the pins on
  purpose after reading the upstream changes, never by removing them.
- Every cron run starts clean from the handoff doc (no `--continuity`), so an
  injected instruction cannot persist across days.

## Adapting

- Different mailbox tooling: edit `mcp_servers.gmail` in `config.yaml` and the
  tool names at the top of `SKILL.md`. Keep the `tools.include` whitelist,
  the version pin and the filename rule.
- Different delivery: `--deliver discord`, `slack`, `whatsapp`, `signal`,
  `email` or `telegram:<chat id>` when creating the cron job.
- Different cadence: `hermes -p gtm cron update <id> --schedule "every 6h"`.
