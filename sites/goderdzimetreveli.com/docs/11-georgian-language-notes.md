# Georgian Language Notes

**Status: the `/ka/` pages require a native Georgian proofread before publication.**
This is a blocking launch item (doc 06, doc 10 §6).

---

## 1. Why this document exists

The Georgian pages in `content/ka/` were drafted as part of this build. They are
substantive, terminologically considered translations rather than placeholders,
and they are internally consistent. They have **not** been reviewed by a native
speaker, and on a site whose entire purpose is credibility under scrutiny, that
gap matters more than it would elsewhere: a Georgian-language page with awkward
register or a wrong technical term undermines exactly the professional standing
the site is built to establish — and it does so in front of the audience most
likely to notice.

Treat the drafts as a strong first version that saves the reviewer most of the
work, not as finished copy.

---

## 2. Terminology decisions made, and why

These are the choices a reviewer should check first, since they propagate across
every page.

| English | Used here | Alternatives considered | Note |
|---|---|---|---|
| Regenerative agriculture | რეგენერაციული სოფლის მეურნეობა | აღმდგენელი სოფლის მეურნეობა | The loanword form is what Georgian agricultural discourse actually uses. The calque reads as an unfamiliar coinage. |
| Expertise (areas of) | სპეციალიზაცია | ექსპერტიზა, კომპეტენციები | **ექსპერტიზა was rejected** — in Georgian it means expert *examination* or appraisal, not a person's field of expertise. Using it would be a visible error. |
| Deep ripping | ღრმა გაფხვიერება | ღრმა მოშლა, რიპინგი | Confirm against what contractors and machinery dealers in Georgia actually say. If the trade uses a transliteration, prefer the trade usage. |
| Subsoiling | ქვენიადაგის გაფხვიერება | — | |
| Restrictive layer | შემზღუდავი ფენა | მკვრივი ფენა | |
| Semi-arid | ნახევრად მშრალი | ნახევრადუდაბნო | Latter carries a landscape-zone meaning that may be too specific. |
| Almond orchard | ნუშის ბაღი | — | |
| In-shell / unshelled | ნაჭუჭიანი | გაუტეხავი | Confirm which the Georgian nut trade uses for the traded commodity. |
| Distribution uniformity | განაწილების თანაბრობა | განაწილების ერთგვაროვნება | |
| Fertigation | ფერტიგაცია | — | Loanword, standard. |
| Value chain | ღირებულების ჯაჭვი | — | |
| Managing Director | მმართველი დირექტორი | — | Quoted title from the USAID brief; keep as is. |
| CEO | აღმასრულებელი დირექტორი | — | Only in the "awaiting documentation" table, where the point is that sources say *director*, not CEO. Preserve that distinction in Georgian. |
| `[VERIFICATION REQUIRED]` | `[საჭიროა გადამოწმება]` | — | Must remain visibly consistent across all `/ka/` pages. |

---

## 3. What the reviewer should check, in priority order

1. **The verification markers.** Every `[საჭიროა გადამოწმება]` block must survive
   translation review intact and read as clearly as the English. These are the
   site's honesty mechanism; softening them in Georgian would defeat the point.
2. **Names, titles and quoted material.** Verify against doc 07:
   - "Managing Director, Adjara Group" — as quoted in the USAID/Chemonics brief
   - "Director of Udabno" / "Director of Udabno Shelling"
   - The SDG 12 award wording — it must stay **organisational**, never personal
   - The GeoGAP quotations — these are back-translations into Georgian of an
     English-language publication. If a Georgian-language original of that quote
     exists, use it; otherwise mark the Georgian rendering as a translation.
3. **Register.** The target is an experienced practitioner writing for
   professional peers — confident, plain, technical. Not academic, not
   promotional, not officialese.
4. **Technical accuracy.** Terminology in the deep-ripping, irrigation and
   processing pages, ideally checked by someone with Georgian agricultural
   sector experience rather than a general translator.
5. **Numbers and units.** Hectares, tonnes, mm, metres — consistent formatting,
   and every figure still carrying its source.

---

## 4. Back-translated quotations — handle carefully

Two GeoGAP quotations appear in Georgian on `/ka/shesakheb/`,
`/ka/gadamushaveba-eksporti/` and elsewhere. The published source
(Chemonics/USAID, October 2021) is in **English**.

The Georgian text on those pages is therefore a translation of an English
publication, not a quotation of a Georgian original. Two acceptable resolutions:

1. **Preferred:** find whether Metreveli gave those remarks in Georgian
   originally, and if a Georgian-language record exists, quote that.
2. Otherwise, label the Georgian rendering explicitly as a translation —
   e.g. `(თარგმანი ინგლისურიდან)` — so no reader assumes it is the original
   wording.

Quoting a back-translation as though it were the original is a small
inaccuracy of exactly the kind this site's whole approach is designed to avoid.

---

## 5. Technical requirements already handled in the theme

The reviewer does not need to worry about these; they are implemented.

- `<html lang="ka">` on `/ka/` pages (`functions.php`, `gm_language_attributes`)
- `hreflang` en / ka / x-default, reciprocal and self-referencing, emitted only
  when the counterpart page actually exists (`inc/hreflang.php`)
- Georgian font stack — Noto Sans/Serif Georgian, then Sylfaen, before Latin
  fallbacks (`assets/css/main.css`)
- Georgian type set ~3% larger, since Mkhedruli reads small at the same nominal
  size as Latin
- Georgian UI strings in header, footer, breadcrumbs, article furniture, search
  and 404
- Language switcher that shows an unavailable language as disabled rather than
  linking to a 404 or dumping the reader on the homepage
- Latin-transliterated slugs (`/ka/shesakheb/`, not percent-encoded Georgian
  script) — see doc 01 §3 for the reasoning

---

## 6. Pages drafted in Georgian

13 principal pages, paired to their English counterparts via `translation_of`:

| Georgian | URL | EN counterpart |
|---|---|---|
| მთავარი | `/ka/` | `/` |
| გოდერძი მეტრეველის შესახებ | `/ka/shesakheb/` | `/about/` |
| პროფესიული გამოცდილება | `/ka/gamotsdileba/` | `/experience/` |
| რჩეული მიღწევები | `/ka/mightsevebi/` | `/achievements/` |
| სპეციალიზაცია | `/ka/spetsializatsia/` | `/expertise/` |
| რეგენერაციული სოფლის მეურნეობა | `/ka/regeneratsiuli-sofmeurneoba/` | `/regenerative-agriculture/` |
| ნუშის ბაღები | `/ka/nushis-baghebi/` | `/almond-orchards/` |
| ღრმა გაფხვიერება | `/ka/ghrma-gafkhviereba/` | `/deep-ripping/` |
| ირიგაცია და ინფრასტრუქტურა | `/ka/irigatsia-infrastruktura/` | `/irrigation-infrastructure/` |
| მექანიზაცია | `/ka/mekanizatsia/` | `/mechanization/` |
| ნუშის გადამუშავება და ექსპორტი | `/ka/gadamushaveba-eksporti/` | `/almond-processing-export/` |
| მედია და პრესა | `/ka/media/` | `/media/` |
| კონტაქტი | `/ka/kontakti/` | `/contact/` |

**Not translated:** the ten technical articles, the two case studies, and the
Speaking / Evidence / Projects pages. English-only initially is a deliberate
choice — those pages emit `hreflang="en"` and `x-default` only, with no dangling
annotation. Translate them as capacity allows; the editorial calendar (doc 05)
schedules the first batch.

---

## 7. Sign-off

- [ ] Native Georgian speaker has reviewed all 13 pages
- [ ] Terminology table in §2 confirmed or corrected
- [ ] All `[საჭიროა გადამოწმება]` markers intact and clear
- [ ] Quoted titles and the award wording verified against doc 07
- [ ] Back-translated quotations resolved per §4
- [ ] Reviewer has agricultural-sector familiarity, or a second technical reviewer used

Reviewed by: ______________________  Date: ____________
