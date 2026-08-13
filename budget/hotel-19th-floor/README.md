# Hotel 19th Floor Renovation Budget — Tbilisi, Georgia

Professional-grade rebuild of the renovation cost estimate for hotel rooms 1901–1919
(14 standard + 4 executive/business) plus the corridor. All figures in **GEL (₾), VAT (18%) inclusive**.

| File | What it is |
|---|---|
| `Calculation_for_holi_v2.xlsx` | **The deliverable** — 12-sheet budget workbook, 214 live formulas, zero errors |
| `Calculation_for_holi_ORIGINAL.xlsx` | The original file, kept for reference/diffing |
| `build_budget.py` | Reproducible generator for the workbook |
| `research/*.md` | Raw market-price research with sources and URLs |

## Headline numbers

| Figure | Amount |
|---|---|
| Current stage (A) — committed + incurred | **69,966.72 ₾** |
| — of which already paid | 52,083.90 ₾ |
| — remaining to pay | 17,882.82 ₾ |
| Full rollout forecast (B) — 18 rooms + corridor, incl. 10% contingency | **267,113.04 ₾** (≈ 88,433 €) |
| Identified overpricing vs. today's market | **8,452.40 ₾** |

A and B are **different scopes** and must not be added together: A is the actual/committed
spend on work already underway; B is a market-priced forecast for the complete refurbishment.

## Errors found in the original file and corrected here

1. **The cost-summary sheet lost the entire materials total.** `ხარჯაღრიცხვა!C3` referenced
   `მასალები!F69`, an empty cell, while the real total sat in `F70` (30,302.89 ₾). The summary
   therefore understated materials by roughly **26,500 ₾**.
2. **A paint line was excluded from the standard-room total.** `standard!F21` (5 l × 25 ₾ = 125 ₾)
   had no value, so the room total was 10,513 ₾ instead of 10,638 ₾ — repeated across 14 rooms.
3. **Twelve material rows carried quantities but no price at all** (2K paint, drill bits, roller
   heads, 2-component grout, sanding discs, 12 W bulbs, nails, 35/40 mm screws, black grout).
   All are now priced at verified market rates.
4. **The carpet line was a hardcoded `=2533.33*3`** with no link to an exchange rate. It is now
   driven by the live EUR/GEL rate.
5. **Mirror replacement was left as "awaiting invoice"** with no number. Now estimated at
   140 ₾/m² × 10.84 m² = 1,517.82 ₾, flagged as an estimate.
6. No VAT treatment, no contingency, no FX assumptions, and **no sources anywhere**.

## Workbook structure

| Sheet | Purpose |
|---|---|
| `შეჯამება` | Executive summary — scope A, scope B, identified savings, methodology |
| `დაშვებები` | Assumptions + **price book**: every unit price with source, URL and verified/estimated status |
| `standard` / `executive` / `corridor` | Per-unit bills of quantities; unit prices link to the price book |
| `Total` | Rollout: 14 × standard, 4 × executive, corridor, waste removal, contingency |
| `სამუშაო` | Works log — statuses normalised, in-house labour shown at 0 ₾ cash cost |
| `მასალები` | Materials log — all 63 rows priced, PAID/estimate split |
| `ინსტრუმენტები` | Tools, repriced to official DeWalt Georgia list |
| `შემსრულებლები` | Contractors, with double-count against the works log removed |
| `განზომილებები` | Quantity takeoffs — room floors, bathroom floors, mirrors |
| `წყაროები` | Full source bibliography, 27 entries |

**Colour convention:** blue = input/actual · black = formula · green = cross-sheet link ·
yellow = key assumption or total.

## Market data

Prices verified **13 August 2026** against Georgian retailers: gorgia.ge, domino.com.ge,
parketi.ge, ecowood.ge, bona.com.ge, dewaltshop.ge, veli.store, nova.ge, kshop.ge, keremont.ge,
goodbuild.ge, grandmall.ge, shop.wurth.com.ge, espano.ge, serwish.ge, demontaji.ge,
plus Tbilisi labour-rate sources (remonti-mshenebloba.ge, euroremonti.ge, servisebi.ge, gurus.ge)
and EU retailers for Artemide lighting.

Exchange rates from the **National Bank of Georgia**, 13.08.2026: **1 EUR = 3.0205 ₾**,
**1 USD = 2.6181 ₾**. Georgian CPI inflation ~4.3% YoY (Mar 2026); contingency set at 10%,
within the 5–15% norm for hotel refurbishment with imported materials.

Every price line is tagged `გადამოწმებული` (verified on a live page), `ნაწილობრივ`
(partially verified) or `შეფასება` (estimated from comparables) — no number is presented as
harder than the evidence behind it.

## Biggest pricing gaps found

| Item | In budget | Market | Note |
|---|---|---|---|
| Aerosol gloss lacquer, 86 cans | 81.40 ₾/can | 23 ₾ (17 ₾ at 6+) | Verify the spec — largest single gap |
| Hand shower, 18 rooms | 300 ₾ | 180 ₾ Grohe Vitalio set | |
| DeWalt perforators (2) | 3,685 ₾ | 2,840 ₾ | Official dewaltshop.ge price; already corrected |
| Basin siphon, 10 pcs | 114 ₾ | 87 ₾ Geberit | |
| Cement 25 kg | 14 ₾ | 8.80–9.10 ₾ | |

Under-budgeted in the original: WD-40 (12 ₾ vs 15–18 ₾), heavy-duty bin bags
(0.60 ₾ vs 1.10–2.50 ₾), nightstands (120 ₾ vs ~230 ₾), and small Artemide lamps
(633 ₾ vs ~937 ₾ landed).

## Regenerating

```bash
pip install openpyxl
python build_budget.py
python /path/to/recalc.py Calculation_for_holi_v2.xlsx 180   # requires libreoffice-calc
```
