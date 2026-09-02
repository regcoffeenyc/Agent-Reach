# Gmail mechanics for the Hermes profile

The profile uses the Gmail AutoAuth MCP server (`@gongrzhe/server-gmail-autoauth-mcp`)
with a whitelist of six tools. Names as seen by the agent: `mcp_gmail_search_emails`,
`mcp_gmail_read_email`, `mcp_gmail_download_attachment`, `mcp_gmail_draft_email`,
`mcp_gmail_list_email_labels`, `mcp_gmail_modify_email`.

## Reading

- `search_emails` takes a Gmail-syntax `query` and `maxResults`. It returns ids,
  subject, from, date and a snippet. Snippets lie by omission: `read_email`
  every candidate.
- `read_email` returns headers (including `Message-ID`, `threadId`), the text
  body and an attachment list with attachment ids.
- Useful sweeps: `after:YYYY/MM/DD in:anywhere -category:promotions`,
  `from:accu-tac.com newer_than:7d`, `in:draft to:<counterparty address>`.

## Attachments

`download_attachment` with `messageId`, `attachmentId`, `savePath` (the
`gtm.work_dir` directory) and optional `filename`. This replaces the old
RAW-message extraction hack; `scripts/extract_gmail_attachments.py` is kept
only for a persisted RAW JSON you may still meet.

Parsing: `.xls` with `xlrd` (`pip install xlrd`), `.xlsx` with `openpyxl`,
PDFs with `pypdf` / `pdfplumber`. Price lists: find the header row first
(brand lists put it on row 3–6), then read the restriction / territory column
before anything else; it has already ruled brands in or out for Georgia.

## Drafting

`draft_email` fields: `to` (list), `cc` (list), `subject`, `body`,
`threadId`, `inReplyTo` (the counterparty's `Message-ID` header, angle
brackets included), optional `attachments` (list of local file paths; the
server reads the files itself, so there is no base64 payload limit in this
profile, but keep drafts under ~20 MB total).

- Subject must match theirs with `Re:` for threading to hold in every client.
- Plain text unless there is a reason for HTML.
- Sign as "Goderdzi Metreveli, Director, Geo-Tactical Market LLC (ID …)" using §0 data
  on LLC / dealer business. Mixed personas on one thread confused suppliers
  before.
- The returned draft id goes in the handoff doc's draft inventory.
- To neutralise a stale draft without deleting it: `modify_email` with
  `addLabelIds: ["TRASH"]` on the draft's message id (recoverable 30 days).
  There is no delete tool in this profile.

## Verifying "was it sent?"

Before trusting any "already sent" note, confirm on the thread: the message
appears with label `SENT` and a timestamp. Drafts are not on the thread; find
them with `in:draft`.

## AcroForm filling (worked example)

```python
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, BooleanObject
r = PdfReader(src); w = PdfWriter(); w.append(r)
for page, data in ((w.pages[0], p1), (w.pages[1], p2)):
    for k, v in data.items():
        try: w.update_page_form_field_values(page, {k: v})
        except Exception: pass   # widgets lacking /AP throw; the value still lands
w._root_object['/AcroForm'][NameObject('/NeedAppearances')] = BooleanObject(True)
```

Map junk field names to labels by dumping widget `/Rect` positions and
comparing against `pdfplumber` word coordinates on the same page. Then
`pdftoppm -png -r 80` and look at the PNGs. Shorten values rather than let
them clip.
