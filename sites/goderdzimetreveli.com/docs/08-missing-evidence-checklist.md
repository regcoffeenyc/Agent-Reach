# Missing Photographs and Supporting Documents

**Purpose:** everything the site needs but does not yet have. Items are ordered so
that clearing the first section unblocks the largest number of pages.

Legend: 🔴 blocks publication of a page or claim · 🟠 needed for credibility · 🟢 improves quality

---

## A. Documents that unblock held claims

These correspond directly to the **C** and **D** rows of the fact-verification report.

| # | Document | Unblocks | Priority |
|---|---|---|---|
| A1 | Land-registry extract or audited report separating **owned / leased / under cultivation** hectares | Home metrics, Udabno case study, About | 🔴 |
| A2 | Almond-processing **equipment specification sheet** + commissioning report | Processing page, capacity figure, value-chain case study | 🔴 |
| A3 | **Machine nameplate photograph** showing manufacturer and model | Manufacturer name (Borrell vs. Borelli) | 🔴 |
| A4 | **Employment records / appointment letters** for each claimed role, with start and end dates | Professional Experience page, JSON-LD `jobTitle` | 🔴 |
| A5 | **Company register extract** (National Agency of Public Registry) showing directorships and any board seat | Experience page, `affiliation` in schema | 🔴 |
| A6 | **Organic certificate** — number, certifying body, scope, validity | Every use of the word "organic" | 🔴 |
| A7 | **Export documentation** — customs declaration, phytosanitary certificate, or buyer confirmation for EU shipments | Export page, "shipped to Europe" claim | 🔴 |
| A8 | **Diploma and transcript** — exact institution, degree name, graduation year | About page, `alumniOf` | 🟠 |
| A9 | **Trainer programme evidence** — programme name, implementing organisation, dates, contract or certificate | Experience page, Speaking/Training page | 🟠 |
| A10 | **Deep-ripping work records** — dated job sheets, ripped area, depth achieved, machine used | Deep-ripping pillar + 5 articles | 🟠 |
| A11 | **Soil analysis reports / soil-profile descriptions** (pre- and post-ripping if available) | Deep-ripping page, regenerative page, measurable-results claims | 🟠 |
| A12 | Written **consent from any contractor or partner** to be named | Any third-party name on the site | 🔴 |
| A13 | Browser capture + web.archive.org snapshot of **S5** (UNGC spotlight) and **S8** (BM.ge) | Processing and export claims resting on those sources | 🟠 |
| A14 | Confirmed **official LinkedIn URL** | `sameAs` in JSON-LD | 🔴 |

---

## B. Photography

The design system is built around original project photography. Stock imagery is
explicitly excluded from the hero and case-study slots. Until originals arrive,
those slots render a neutral typographic treatment rather than a placeholder
stock image — the theme is written so that a missing image degrades gracefully
instead of embarrassing the site.

### B1. Portrait — 🔴 blocks homepage, About, Open Graph, `Person.image`

| Shot | Spec |
|---|---|
| Primary portrait, outdoors, in an orchard or field, natural light | Vertical 4:5 and horizontal 3:2, ≥ 2400 px long edge |
| Working portrait — in the field, wearing work clothing, ideally mid-task | 3:2 |
| Neutral head-and-shoulders for press and speaker use | 1:1 and 4:5 |
| Speaking or presenting to an audience | 3:2 |

*Guidance:* the positioning is "field practitioner, not corporate brochure". A
studio portrait against a grey backdrop actively works against that. Shoot on
site, early morning or late afternoon.

### B2. Orchard and landscape — 🔴 blocks pillar pages and case studies

- Aerial of the almond orchard showing row structure and scale (drone, 3:2 and 16:9)
- Ground-level orchard rows, mature trees, canopy filling
- Young orchard / recently established block, showing establishment stage
- Semi-arid land **before** development — undeveloped Udabno terrain
- The **same location after** development, matched framing and season if possible
- Almond bloom (spring), fruit set, and pre-harvest nut on tree
- Seasonal set: same block photographed across a year

*The before/after pair matched to the same viewpoint is the single most valuable
image on the site.* It communicates the entire proposition without a caption.

### B3. Soil and deep ripping — 🔴 blocks the deep-ripping cluster

- **Soil profile pit**, clean vertical face, with a scale rule or tape visible
- Close-up of a **restrictive/compacted layer** with the horizon boundary visible
- Deep ripper in work, showing shank engagement and soil heave
- Tractor and ripper combination, side-on, whole machine visible
- Soil surface immediately after ripping — fracture pattern and clod size
- Same ground after settlement and rainfall
- Root development in ripped vs. unripped ground, if available
- Penetrometer or soil-moisture measurement in progress
- Short video clips of the ripping operation

*Include a scale reference in every soil photograph.* A profile picture without a
tape measure cannot support any depth statement.

### B4. Irrigation and infrastructure — 🟠

- Water source: reservoir, pumping station, intake
- Mainline installation / trenching in progress
- Drip line on established rows, emitters visible
- Filtration and fertigation station
- Control and automation equipment
- Farm roads and operational infrastructure
- Erosion-control measures in place

### B5. Machinery — 🟠

- High-horsepower tractor fleet
- Trunk or canopy shaker harvesting almonds
- Sweeper and pick-up machinery
- Sprayers and orchard-management equipment
- Workshop and maintenance facility

### B6. Processing — 🔴 blocks the processing page

- Exterior of the processing facility
- Hulling / shelling line in operation
- Sorting and grading equipment
- Drying installation
- Finished product: in-shell, kernel, and any secondary products
- Packaging and palletised product ready for dispatch
- **Machine nameplate close-up** (also serves A3)
- Laboratory or quality-control activity

### B7. People and context — 🟢

- Team at work — field crews, machine operators, agronomists
- Metreveli with the team on site (supports the multidisciplinary disclaimer)
- Training or demonstration sessions
- Conference and event photographs, with dates and event names
- Partnership and site-visit photographs, with everyone identified

---

## C. Documents for the Evidence and Project Gallery

| Item | Notes | Priority |
|---|---|---|
| Downloadable professional biography (PDF) | Generated from `content/bios/biography-full.md` once verified | 🟠 |
| Downloadable executive CV (PDF) | Only after A4/A5/A8 resolve the dates and titles | 🔴 |
| Award documentation for the 2023 SDG 12 recognition | Certificate or official announcement — label clearly as **organisational** | 🟠 |
| Conference programmes listing him as a speaker | Establishes the Speaking page | 🟠 |
| Training certificates | Redact any personal identifiers | 🟢 |
| Presentation decks delivered publicly | Convert to PDF, confirm no confidential content | 🟢 |
| Published reports or company announcements | Link to originals where they exist online | 🟢 |
| Media clippings with dates and outlets | For the Media and Press page | 🟠 |

---

## D. Never upload

Hard exclusions, regardless of who requests them:

- Signed contracts, commercial agreements, or term sheets
- Employee names, photographs or personal data without written consent
- Personal home address, national ID, passport, or date of birth
- Scanned signatures — including on award or training certificates (redact them)
- Salary, shareholding or other commercially sensitive financial data
- Anything covered by a confidentiality obligation to a former employer
- Land-registry extracts containing third-party personal data (redact before use)
- Client or supplier lists

Where a document is needed for *verification* but must not be *published*, the
workflow is: review it privately, record the outcome in the verification report,
publish only the confirmed statement — not the document.

---

## E. Intake tracker

| Item | Requested | Received | Reviewed | Cleared for publication |
|---|---|---|---|---|
| A1 Land records |  |  |  |  |
| A2 Equipment spec |  |  |  |  |
| A3 Nameplate photo |  |  |  |  |
| A4 Employment records |  |  |  |  |
| A5 Register extract |  |  |  |  |
| A6 Organic certificate |  |  |  |  |
| A7 Export documents |  |  |  |  |
| A8 Diploma |  |  |  |  |
| A9 Trainer evidence |  |  |  |  |
| A10 Ripping records |  |  |  |  |
| A11 Soil reports |  |  |  |  |
| A12 Consents |  |  |  |  |
| A13 S5/S8 captures |  |  |  |  |
| A14 LinkedIn URL |  |  |  |  |
| B1 Portrait set |  |  |  |  |
| B2 Orchard set |  |  |  |  |
| B3 Soil/ripping set |  |  |  |  |
| B6 Processing set |  |  |  |  |
