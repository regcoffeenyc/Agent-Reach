# -*- coding: utf-8 -*-
"""Rebuild Calculation_for_holi.xlsx as a professional-grade, source-backed
hotel renovation budget (19th floor, rooms 1901-1919), GEL, VAT-inclusive.

Conventions: blue font = hardcoded input / actual; black = formula;
green = cross-sheet link; yellow fill = key assumption.
All unit prices researched 13-Aug-2026 from Georgian retailers (see წყაროები).
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUT = 'Calculation_for_holi_v2.xlsx'

GE = 'Sylfaen'
BLUE, GREEN, BLACK, WHITE, NAVY = '0000FF', '008000', '000000', 'FFFFFF', '1F3864'

F_TITLE = Font(name=GE, size=16, bold=True, color=NAVY)
F_SEC   = Font(name=GE, size=12, bold=True, color=NAVY)
F_HDR   = Font(name=GE, size=10, bold=True, color=WHITE)
F_BODY  = Font(name=GE, size=10)
F_BOLD  = Font(name=GE, size=10, bold=True)
F_IN    = Font(name=GE, size=10, color=BLUE)          # input
F_IN_B  = Font(name=GE, size=10, bold=True, color=BLUE)
F_LNK   = Font(name=GE, size=10, color=GREEN)         # cross-sheet link
F_TOT   = Font(name=GE, size=11, bold=True)
F_NOTE  = Font(name=GE, size=9, italic=True, color='595959')

FILL_HDR = PatternFill('solid', fgColor='305496')
FILL_KEY = PatternFill('solid', fgColor='FFF2CC')     # key assumption
FILL_SUB = PatternFill('solid', fgColor='D9E2F3')     # subtotal band
FILL_TOT = PatternFill('solid', fgColor='FFE699')     # grand total band

THIN = Side(style='thin', color='BFBFBF')
BOX  = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

MONEY = '#,##0.00'
QTY   = '#,##0.##'
PCT   = '0%'

wb = openpyxl.Workbook()
wb.remove(wb.active)


def put(ws, coord, value, font=F_BODY, fmt=None, fill=None, align=None,
        border=False, wrap=False):
    c = ws[coord]
    c.value = value
    c.font = font
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    a = Alignment(wrap_text=wrap)
    if align:
        a = Alignment(horizontal=align, vertical='center', wrap_text=wrap)
    c.alignment = a
    if border:
        c.border = BOX
    return c


def header_row(ws, row, cols_labels, start_col=1):
    for i, lab in enumerate(cols_labels):
        col = get_column_letter(start_col + i)
        put(ws, f'{col}{row}', lab, font=F_HDR, fill=FILL_HDR,
            align='center', border=True, wrap=True)


def widths(ws, spec):
    for col, w in spec.items():
        ws.column_dimensions[col].width = w


# ============================================================ 1. დაშვებები
A = wb.create_sheet('დაშვებები')
widths(A, {'A': 5, 'B': 52, 'C': 9, 'D': 13, 'E': 44, 'F': 15, 'G': 46})
put(A, 'B1', 'დაშვებები და ფასების ცნობარი / Assumptions & Price Book', F_TITLE)
put(A, 'B2', 'ყველა ფასი — ლარი (GEL), დღგ (18%) ჩათვლით. გადამოწმებულია 13.08.2026.',
    F_NOTE)

put(A, 'B4', '1. გლობალური დაშვებები', F_SEC)
header_row(A, 5, ['N', 'პარამეტრი', 'განზ.', 'მნიშვნ.', 'წყარო', 'სტატუსი', 'შენიშვნა'])
glob_rows = [
    # row, label, unit, value, fmt, source, status, note, keyfill
    (6, 'ვალუტის კურსი EUR/GEL', 'ლარი', 3.0205, '0.0000',
     'საქართველოს ეროვნული ბანკი (nbg.gov.ge API)', 'გადამოწმებული',
     'ოფიციალური კურსი 13.08.2026', True),
    (7, 'ვალუტის კურსი USD/GEL', 'ლარი', 2.6181, '0.0000',
     'საქართველოს ეროვნული ბანკი (nbg.gov.ge API)', 'გადამოწმებული',
     'ოფიციალური კურსი 13.08.2026', True),
    (8, 'დღგ (VAT)', '%', 0.18, PCT, 'საგადასახადო კოდექსი', 'კანონით',
     'საცალო ფასები დღგ-ს უკვე მოიცავს — ცალკე არ ემატება', False),
    (9, 'გაუთვალისწინებელი ხარჯი (contingency)', '%', 0.10, PCT,
     'დარგობრივი ნორმა: 5–10%; სასტუმროსთვის იმპორტით — 10–15%',
     'შეფასება', 'გამოიყენება Total ფურცელზე', True),
    (10, 'იმპორტის ფრახტი/მოსაკრებელი (EU საქონელი)', '%', 0.10, PCT,
     'ტიპური დანამატი EU ონლაინ-ფასზე (ფრახტი+განბაჟება)', 'შეფასება',
     'ემატება Artemide-ს და LANO ხალიჩას', True),
    (11, 'მასალის დანაკარგი — პარკეტი (waste)', '%', 0.07, PCT,
     'სამონტაჟო პრაქტიკა (ჭრა/წუნი 5–10%)', 'შეფასება',
     'ემატება პარკეტის რაოდენობას BOQ-ში', False),
]
for r, lab, unit, val, fmt, src, st, note, key in glob_rows:
    put(A, f'A{r}', r - 5, border=True, align='center')
    put(A, f'B{r}', lab, border=True)
    put(A, f'C{r}', unit, border=True, align='center')
    put(A, f'D{r}', val, font=F_IN_B, fmt=fmt, border=True, align='center',
        fill=FILL_KEY if key else None)
    put(A, f'E{r}', src, border=True, wrap=True)
    put(A, f'F{r}', st, border=True, align='center')
    put(A, f'G{r}', note, font=F_NOTE, border=True, wrap=True)

put(A, 'B13', '2. ფასების ცნობარი (ერთეულის ფასები, ლარი დღგ-ით)', F_SEC)
header_row(A, 14, ['N', 'დასახელება', 'განზ.', 'ფასი (₾)', 'წყარო', 'სტატუსი', 'შენიშვნა'])
# (row, name, unit, price-or-formula, source, status, note)
price_rows = [
    (15, 'პარკეტი მუხის მასიური, Exclusive ხარისხი', 'კვ.მ', 140,
     'parketi.ge — Oak Parquet Exclusive', 'გადამოწმებული',
     'Rustic 75 ₾ / Select 99 ₾ / Exclusive 140 ₾; სამშრიანი ინჟინრული 179–269 ₾'),
    (16, 'პარკეტის დაგება (სამუშაო)', 'კვ.მ', 45,
     'homeis.ge; ბაზრის დიაპაზონი 25–65 ₾', 'გადამოწმებული',
     'კომპანია 30–65 ₾, კერძო ოსტატი 25–60 ₾'),
    (17, 'იატაკის ლაქი Bona Mega EVO', 'ლიტრი', 76,
     'bona.com.ge — ოფიც. დისტრიბუტორი (380 ₾ / 5ლ)', 'გადამოწმებული',
     '2K Traffic კლასი ~100 ₾/ლ — დერეფნებისთვის'),
    (18, 'ფანერა არყის 10მმ, 1525×1525', 'ცალი', 34,
     'ecowood.ge', 'გადამოწმებული', '8მმ — 29 ₾, 12მმ — 41 ₾'),
    (19, 'პლინტუსი MDF თეთრი — მასალა+მონტაჟი+შეღებვა', 'მეტრი', 25,
     'domino.com.ge (მასალა 10–15 ₾/მ) + სამუშაო', 'გადამოწმებული',
     'მხოლოდ მასალა 10–15 ₾/მ; 25 ₾ = სრული ღირებულება'),
    (20, 'ლოგინის გვერდითა ტუმბო', 'ცალი', 230,
     'veli.store (SONGMICS 2ც — 459.95 ₾); liva.ge 200 ₾', 'გადამოწმებული',
     'ძველი ბიუჯეტის 120 ₾ საცალო ფასზე დაბალია'),
    (21, 'ტელევიზორის სადგამი მაგიდა', 'ცალი', 250,
     'liva.ge (~200 ₾); embawood.ge', 'ნაწილობრივ', 'დიაპაზონი 200–450 ₾'),
    (22, 'დუში დიდი (ზედა შხაპი 250მმ)', 'ცალი', 389,
     'domino.com.ge — AM.PM Like 250×250', 'გადამოწმებული',
     'Rubineta 131 ₾; Grohe სისტემა 599–959 ₾'),
    (23, 'დუში პატარა (ხელის, Grohe კომპლექტი)', 'ცალი', 180,
     'domino.com.ge — Grohe Vitalio Comfort ბარით', 'გადამოწმებული',
     'ყურმილი ცალკე 63–103 ₾ (gorgia.ge); ძველი 300 ₾ — ~2×-ით მაღალი'),
    (24, 'შემრევი ონკანი (Grohe Get)', 'ცალი', 306,
     'gorgia.ge — Grohe Get 23454000 (305.50 ₾)', 'გადამოწმებული',
     'StartEdge 187 ₾, Eurosmart S 254 ₾, Get 306–379 ₾'),
    (25, 'ARTEMIDE სანათი დიდი (Tolomeo Terra)', 'ცალი',
     '=ROUND(488*$D$6*(1+$D$10),0)',
     'light11.eu 488 € (RRP 610 €) + ფრახტი 10%', 'გადამოწმებული (EU)',
     'EU ფასი × EUR კურსი × (1+ფრახტი); LED ვერსია 644 €'),
    (26, 'ARTEMIDE სანათი პატარა (Tolomeo Micro Parete)', 'ცალი',
     '=ROUND(282*$D$6*(1+$D$10),0)',
     'light11.eu 282 € + ფრახტი 10%', 'გადამოწმებული (EU)',
     'ძველი ბიუჯეტის 633 ₾ დღეს 10–20%-ით ნაკლებია რეალურზე'),
    (27, 'კარი ოთახის (MDF ბლოკი კოლოფით + ფურნიტურა)', 'ცალი', 750,
     'domino.com.ge — KMF 649–699 ₾ + სახელური/საკეტი ~50–150 ₾',
     'გადამოწმებული', 'პრემიუმ Terminus 1029–1499 ₾'),
    (28, 'კარი აბაზანის (700მმ, ტენმედეგი PVC-MDF)', 'ცალი', 359,
     'domino.com.ge — Flydoors LA STELLA', 'გადამოწმებული',
     'ეკონომ 179–199 ₾; KMF 649 ₾'),
    (29, 'სამღებრო სამუშაოები (მოშპაკვლა+შეღებვა)', 'კვ.მ', 20,
     'remonti-mshenebloba.ge; euroremonti.ge; servisebi.ge', 'გადამოწმებული',
     'დიაპაზონი 12–20 ₾/კვ.მ; 20 ₾ = სასტუმროს ხარისხი სრული მომზადებით'),
    (30, 'საღებავი StoColor In (ინტერიერის)', 'ლიტრი', 25,
     'sto.ge (ფასი მოთხოვნით); EU საცალო ~15–18 ₾/ლ + იმპორტი', 'შეფასება',
     'უსაფრთხო საბიუჯეტო ფასი საქართველოსთვის 20–28 ₾/ლ'),
    (31, 'ხალიჩა LANO (სასტუმროს კლასი, 19 €/კვ.მ)', 'კვ.მ',
     '=ROUND(19*$D$6*(1+$D$10),2)',
     'LANO — საპროექტო იმპორტი; domino.com.ge ბელგიური 10.5–119 ₾', 'ნაწილობრივ',
     '19 € × EUR კურსი × (1+ფრახტი)'),
    (32, 'ხალიჩის დაგება (სამუშაო)', 'კვ.მ', 15,
     'gurus.ge (ლამინატი 10–25 ₾ — პროქსი)', 'შეფასება', 'წებოზე დაგება ≤ ლამინატის ტარიფი'),
    (33, 'სარკე ზომაზე ჭრით + მონტაჟი', 'კვ.მ', 140,
     'serwish.ge (მასალა 40–50 ₾-დან; დამუშავება+მონტაჟი)', 'შეფასება',
     'რეალური სრული ფასი თბილისში 100–180 ₾/კვ.მ'),
    (34, 'სამშენებლო ნაგვის გატანა', 'მ³', 370,
     'demontaji.ge — 2026 წლის ტარიფი', 'გადამოწმებული',
     'პარკეტის აყრა ცალკე — 2 ₾/კვ.მ'),
    (35, 'მოციკლოვება + გალაქვა (სამუშაო)', 'კვ.მ', 20,
     'shop.glimtrex.ge (გერმანული აპარატი)', 'გადამოწმებული',
     'სრული ციკლი მასალით 40–45 ₾/კვ.მ'),
]
for r, name, unit, price, src, st, note in price_rows:
    put(A, f'A{r}', r - 14, border=True, align='center')
    put(A, f'B{r}', name, border=True, wrap=True)
    put(A, f'C{r}', unit, border=True, align='center')
    if isinstance(price, str):
        put(A, f'D{r}', price, font=F_BODY, fmt=MONEY, border=True, align='center')
    else:
        put(A, f'D{r}', price, font=F_IN, fmt=MONEY, border=True, align='center')
    put(A, f'E{r}', src, border=True, wrap=True)
    put(A, f'F{r}', st, border=True, align='center')
    put(A, f'G{r}', note, font=F_NOTE, border=True, wrap=True)
put(A, 'B37', 'ლეგენდა: ლურჯი — შესაყვანი მონაცემი/ფაქტი · შავი — ფორმულა · '
              'მწვანე — ბმული სხვა ფურცელზე · ყვითელი ფონი — საკვანძო დაშვება.',
    F_NOTE)
A.freeze_panes = 'A15'

PB = "'დაშვებები'"   # price book sheet ref
# price cell shortcuts
P = {k: f"{PB}!$D${r}" for k, r in dict(
    parquet=15, laying=16, lacquer=17, plywood=18, skirting=19, nightstand=20,
    tvstand=21, shower_big=22, shower_small=23, mixer=24, artemide_l=25,
    artemide_s=26, door_room=27, door_bath=28, painting=29, paint=30,
    carpet=31, carpet_lay=32, mirror=33, waste_out=34, sanding=35).items()}
WASTE = f"{PB}!$D$11"
CONT = f"{PB}!$D$9"
EUR = f"{PB}!$D$6"


# ============================================================ room BOQ helper
def boq_sheet(name, title, rows, note=None):
    """rows: list of (label, unit, qty (num or formula), price_ref, note)"""
    ws = wb.create_sheet(name)
    widths(ws, {'A': 5, 'B': 46, 'C': 9, 'D': 11, 'E': 13, 'F': 14, 'G': 52})
    put(ws, 'B1', title, F_TITLE)
    put(ws, 'B2', 'ფასები: ლარი, დღგ-ით — წყაროები ფურცელზე „დაშვებები“ და „წყაროები“.',
        F_NOTE)
    header_row(ws, 4, ['N', 'დასახელება', 'განზ.', 'რაოდ.', 'ერთ. ფასი (₾)',
                       'ღირებულება (₾)', 'შენიშვნა'])
    r = 5
    for i, (label, unit, qty, pref, nt) in enumerate(rows, 1):
        put(ws, f'A{r}', i, border=True, align='center')
        put(ws, f'B{r}', label, border=True, wrap=True)
        put(ws, f'C{r}', unit, border=True, align='center')
        if isinstance(qty, str):
            put(ws, f'D{r}', qty, fmt=QTY, border=True, align='center')
        else:
            put(ws, f'D{r}', qty, font=F_IN, fmt=QTY, border=True, align='center')
        put(ws, f'E{r}', f'={pref}', font=F_LNK, fmt=MONEY, border=True, align='center')
        put(ws, f'F{r}', f'=D{r}*E{r}', fmt=MONEY, border=True, align='center')
        put(ws, f'G{r}', nt or '', font=F_NOTE, border=True, wrap=True)
        r += 1
    put(ws, f'B{r}', 'ჯამი', F_TOT, fill=FILL_TOT, border=True)
    for col in 'ACDE':
        put(ws, f'{col}{r}', '', fill=FILL_TOT, border=True)
    put(ws, f'F{r}', f'=SUM(F5:F{r-1})', F_TOT, fmt=MONEY, fill=FILL_TOT,
        border=True, align='center')
    put(ws, f'G{r}', '', fill=FILL_TOT, border=True)
    if note:
        put(ws, f'B{r+2}', note, F_NOTE)
    ws.freeze_panes = 'A5'
    return ws, r  # total row


std_rows = [
    ('პარკეტის დაგება', 'კვ.მ', 18, P['laying'], 'ოთახის ფართობი'),
    ('პარკეტი მუხის Exclusive', 'კვ.მ', f'=ROUND(D5*(1+{WASTE}),1)', P['parquet'],
     'ფართობი + 7% დანაკარგი'),
    ('ლაქი იატაკის Bona Mega EVO', 'ლიტრი', 6, P['lacquer'], ''),
    ('ფანერა არყის 10მმ', 'ცალი', 7, P['plywood'], ''),
    ('პლინტუსი MDF (მასალა+მონტაჟი+შეღებვა)', 'მეტრი', 15, P['skirting'], ''),
    ('ლოგინის გვერდითა ტუმბოები', 'ცალი', 2, P['nightstand'], ''),
    ('ტელევიზორის სადგამი მაგიდა', 'ცალი', 1, P['tvstand'], ''),
    ('დუში დიდი (250მმ)', 'ცალი', 1, P['shower_big'], ''),
    ('დუში პატარა (ხელის)', 'ცალი', 1, P['shower_small'], ''),
    ('შემრევი ონკანი Grohe', 'ცალი', 1, P['mixer'], ''),
    ('ARTEMIDE სანათი დიდი', 'ცალი', 1, P['artemide_l'], 'EUR ფასი — კურსზეა მიბმული'),
    ('ARTEMIDE სანათი პატარა', 'ცალი', 2, P['artemide_s'], 'EUR ფასი — კურსზეა მიბმული'),
    ('კარი ოთახის', 'ცალი', 1, P['door_room'], ''),
    ('კარი აბაზანის', 'ცალი', 1, P['door_bath'], ''),
    ('სამღებრო სამუშაოები', 'კვ.მ', 40, P['painting'], 'კედლები+ჭერი'),
    ('საღებავი StoColor', 'ლიტრი', 5, P['paint'],
     'ძველ ფაილში ეს სტრიქონი ჯამში არ იყო ჩართული — გასწორებულია'),
]
ws_std, STD_TOT = boq_sheet(
    'standard', 'STANDARD ROOM — ერთი ოთახის ხარჯთაღრიცხვა', std_rows,
    note='×14 ოთახი — იხ. ფურცელი „Total“.')

exe_rows = [
    ('პარკეტის დაგება', 'კვ.მ', 28, P['laying'], 'ოთახის ფართობი'),
    ('პარკეტი მუხის Exclusive', 'კვ.მ', f'=ROUND(D5*(1+{WASTE}),1)', P['parquet'],
     'ფართობი + 7% დანაკარგი'),
    ('ლაქი იატაკის Bona Mega EVO', 'ლიტრი', 8, P['lacquer'], ''),
    ('ფანერა არყის 10მმ', 'ცალი', 10, P['plywood'], ''),
    ('პლინტუსი MDF (მასალა+მონტაჟი+შეღებვა)', 'მეტრი', 22, P['skirting'], ''),
    ('ლოგინის გვერდითა ტუმბოები', 'ცალი', 2, P['nightstand'], ''),
    ('ტელევიზორის სადგამი მაგიდა', 'ცალი', 1, P['tvstand'], ''),
    ('დუში დიდი (250მმ)', 'ცალი', 1, P['shower_big'], ''),
    ('დუში პატარა (ხელის)', 'ცალი', 1, P['shower_small'], ''),
    ('შემრევი ონკანი Grohe', 'ცალი', 2, P['mixer'], ''),
    ('ARTEMIDE სანათი დიდი', 'ცალი', 1, P['artemide_l'], ''),
    ('ARTEMIDE სანათი პატარა', 'ცალი', 2, P['artemide_s'], ''),
    ('კარი ოთახის', 'ცალი', 1, P['door_room'], ''),
    ('კარი აბაზანის', 'ცალი', 1, P['door_bath'], ''),
    ('სამღებრო სამუშაოები', 'კვ.მ', 60, P['painting'], 'კედლები+ჭერი'),
    ('საღებავი StoColor', 'ლიტრი', 7.5, P['paint'], ''),
]
ws_exe, EXE_TOT = boq_sheet(
    'executive', 'EXECUTIVE ROOM — ერთი ოთახის ხარჯთაღრიცხვა', exe_rows,
    note='×4 ოთახი — იხ. ფურცელი „Total“.')

cor_rows = [
    ('სამღებრო სამუშაოები', 'კვ.მ', 250, P['painting'], 'კედლები+ჭერი'),
    ('საღებავი StoColor', 'ლიტრი', 30, P['paint'], ''),
    ('ხალიჩა LANO (19 €/კვ.მ)', 'კვ.მ', 108, P['carpet'], 'EUR კურსზეა მიბმული'),
    ('ხალიჩის დაგება', 'კვ.მ', 108, P['carpet_lay'], ''),
]
ws_cor, COR_TOT = boq_sheet('corridor', 'CORRIDOR — დერეფნის ხარჯთაღრიცხვა', cor_rows)


# ============================================================ Total (rollout)
T = wb.create_sheet('Total')
widths(T, {'A': 5, 'B': 46, 'C': 9, 'D': 11, 'E': 14, 'F': 15, 'G': 52})
put(T, 'B1', 'სრული განახლების საპროგნოზო ბიუჯეტი — მე-19 სართული', F_TITLE)
put(T, 'B2', '14 standard + 4 executive + დერეფანი. ფასები: ლარი, დღგ-ით, 13.08.2026.',
    F_NOTE)
header_row(T, 4, ['N', 'დასახელება', 'განზ.', 'რაოდ.', 'ერთ. ფასი (₾)',
                  'ღირებულება (₾)', 'შენიშვნა'])
t_rows = [
    ('standard room', 'ოთახი', 14, f"='standard'!F{STD_TOT}", ''),
    ('executive room', 'ოთახი', 4, f"='executive'!F{EXE_TOT}", ''),
    ('corridor', 'კომპლ.', 1, f"='corridor'!F{COR_TOT}", ''),
]
r = 5
for i, (label, unit, qty, pref, nt) in enumerate(t_rows, 1):
    put(T, f'A{r}', i, border=True, align='center')
    put(T, f'B{r}', label, border=True)
    put(T, f'C{r}', unit, border=True, align='center')
    put(T, f'D{r}', qty, font=F_IN, fmt=QTY, border=True, align='center')
    put(T, f'E{r}', pref, font=F_LNK, fmt=MONEY, border=True, align='center')
    put(T, f'F{r}', f'=D{r}*E{r}', fmt=MONEY, border=True, align='center')
    put(T, f'G{r}', nt, font=F_NOTE, border=True)
    r += 1
put(T, f'A{r}', 4, border=True, align='center')
put(T, f'B{r}', 'სამშენებლო ნაგვის გატანა (დემონტაჟის ნარჩენი)', border=True, wrap=True)
put(T, f'C{r}', 'მ³', border=True, align='center')
put(T, f'D{r}', 15, font=F_IN, fmt=QTY, border=True, align='center')
put(T, f'E{r}', f"={P['waste_out']}", font=F_LNK, fmt=MONEY, border=True, align='center')
put(T, f'F{r}', f'=D{r}*E{r}', fmt=MONEY, border=True, align='center')
put(T, f'G{r}', 'შეფასება: ~0.05 მ³/კვ.მ დემონტაჟის ნარჩენი; ტარიფი demontaji.ge',
    font=F_NOTE, border=True, wrap=True)
r += 1
SUB = r
put(T, f'B{r}', 'შუალედური ჯამი', F_BOLD, fill=FILL_SUB, border=True)
for col in 'ACDE':
    put(T, f'{col}{r}', '', fill=FILL_SUB, border=True)
put(T, f'F{r}', f'=SUM(F5:F{r-1})', F_BOLD, fmt=MONEY, fill=FILL_SUB,
    border=True, align='center')
put(T, f'G{r}', '', fill=FILL_SUB, border=True)
r += 1
put(T, f'B{r}', 'გაუთვალისწინებელი ხარჯი (10%)', border=True)
put(T, f'F{r}', f'=F{SUB}*{CONT}', fmt=MONEY, border=True, align='center')
put(T, f'G{r}', 'იხ. დაშვება N4 — დარგობრივი ნორმა', font=F_NOTE, border=True)
for col in 'ACDE':
    put(T, f'{col}{r}', '', border=True)
r += 1
GRAND = r
put(T, f'B{r}', 'სულ ჯამი (GRAND TOTAL)', F_TOT, fill=FILL_TOT, border=True)
for col in 'ACDE':
    put(T, f'{col}{r}', '', fill=FILL_TOT, border=True)
put(T, f'F{r}', f'=F{SUB}+F{SUB+1}', F_TOT, fmt=MONEY, fill=FILL_TOT,
    border=True, align='center')
put(T, f'G{r}', 'დღგ ჩათვლით', font=F_NOTE, fill=FILL_TOT, border=True)
r += 1
put(T, f'B{r}', 'ექვივალენტი EUR', border=True)
put(T, f'F{r}', f'=F{GRAND}/{EUR}', fmt='#,##0.00\\ "€"', border=True, align='center')
for col in 'ACDE':
    put(T, f'{col}{r}', '', border=True)
put(T, f'G{r}', 'NBG კურსით 13.08.2026', font=F_NOTE, border=True)
r += 2
put(T, f'B{r}', 'შენიშვნა: ძველი ვერსიის ჯამი იყო 216,216 ₾. სხვაობა აიხსნება: '
                'ნაგვის გატანა (ადრე საერთოდ არ იყო), 10% გაუთვალისწინებელი ხარჯი, '
                'standard ოთახის საღებავის სტრიქონი (ადრე ჯამში არ შედიოდა) და '
                'ერთეულის ფასების განახლება 13.08.2026 ბაზარზე.', F_NOTE, wrap=True)
T.row_dimensions[r].height = 30


# ============================================================ განზომილებები
TK = wb.create_sheet('განზომილებები')
widths(TK, {'A': 14, 'B': 34, 'C': 10, 'D': 8, 'E': 12, 'F': 12, 'G': 40})
put(TK, 'B1', 'განზომილებები (takeoffs) — იატაკები და სარკეები', F_TITLE)

put(TK, 'A3', '1. ნომრის იატაკი', F_SEC)
header_row(TK, 4, ['ტიპი', 'ოთახები', 'კვ.მ/ოთახი', 'რაოდ.', 'სულ კვ.მ', 'ფანერა (ც)'])
tk1 = [('Executive', '1907; 1910', 26, 2, 20),
       ('Standard', '1901; 1902; 1909; 1916; 1918', 17, 5, 35),
       ('Business', '1919', 25, 1, 9)]
r = 5
for typ, rooms, sqm, qty, ply in tk1:
    put(TK, f'A{r}', typ, border=True)
    put(TK, f'B{r}', rooms, border=True)
    put(TK, f'C{r}', sqm, font=F_IN, fmt=QTY, border=True, align='center')
    put(TK, f'D{r}', qty, font=F_IN, border=True, align='center')
    put(TK, f'E{r}', f'=C{r}*D{r}', fmt=QTY, border=True, align='center')
    put(TK, f'F{r}', ply, font=F_IN, border=True, align='center')
    r += 1
put(TK, f'A{r}', 'ჯამი', F_BOLD, fill=FILL_SUB, border=True)
put(TK, f'B{r}', '', fill=FILL_SUB, border=True)
put(TK, f'C{r}', '', fill=FILL_SUB, border=True)
put(TK, f'D{r}', '=SUM(D5:D7)', F_BOLD, fill=FILL_SUB, border=True, align='center')
put(TK, f'E{r}', '=SUM(E5:E7)', F_BOLD, fmt=QTY, fill=FILL_SUB, border=True, align='center')
put(TK, f'F{r}', '=SUM(F5:F7)', F_BOLD, fill=FILL_SUB, border=True, align='center')
ROOMFLOOR = f"'განზომილებები'!$E$8"

put(TK, 'A10', '2. აბაზანის იატაკი', F_SEC)
header_row(TK, 11, ['ტიპი', 'ოთახები', 'კვ.მ/ოთახი', 'რაოდ.', 'სულ კვ.მ'])
tk2 = [('Executive', '1904; 1907; 1910; 1917', 4.6, 4),
       ('Standard', '1903; 1906; 1908; 1912; 1916', 2.4, 5),
       ('Business', '1919', 2.4, 1),
       ('Standard', '1901', 2, 1)]
r = 12
for typ, rooms, sqm, qty in tk2:
    put(TK, f'A{r}', typ, border=True)
    put(TK, f'B{r}', rooms, border=True)
    put(TK, f'C{r}', sqm, font=F_IN, fmt=QTY, border=True, align='center')
    put(TK, f'D{r}', qty, font=F_IN, border=True, align='center')
    put(TK, f'E{r}', f'=C{r}*D{r}', fmt=QTY, border=True, align='center')
    r += 1
put(TK, f'A{r}', 'ჯამი', F_BOLD, fill=FILL_SUB, border=True)
put(TK, f'B{r}', '', fill=FILL_SUB, border=True)
put(TK, f'C{r}', '', fill=FILL_SUB, border=True)
put(TK, f'D{r}', '=SUM(D12:D15)', F_BOLD, fill=FILL_SUB, border=True, align='center')
put(TK, f'E{r}', '=SUM(E12:E15)', F_BOLD, fmt=QTY, fill=FILL_SUB, border=True,
    align='center')
BATHFLOOR = f"'განზომილებები'!$E$16"

put(TK, 'A19', '3. სარკეების შეცვლა', F_SEC)
header_row(TK, 20, ['ტიპი', 'ოთახები', 'ზომა (მ)', 'რაოდ.', 'სულ კვ.მ'])
tk3 = [('Standard', '1902; 1909', '1.14 × 2.42', 2, '=1.14*2.42*D21'),
       ('Standard', '1901; 1916', '1.10 × 2.42', 2, '=1.10*2.42*D22')]
r = 21
for typ, rooms, size, qty, area in tk3:
    put(TK, f'A{r}', typ, border=True)
    put(TK, f'B{r}', rooms, border=True)
    put(TK, f'C{r}', size, font=F_IN, border=True, align='center')
    put(TK, f'D{r}', qty, font=F_IN, border=True, align='center')
    put(TK, f'E{r}', area, fmt=QTY, border=True, align='center')
    r += 1
put(TK, f'A{r}', 'ჯამი', F_BOLD, fill=FILL_SUB, border=True)
put(TK, f'B{r}', '', fill=FILL_SUB, border=True)
put(TK, f'C{r}', '', fill=FILL_SUB, border=True)
put(TK, f'D{r}', '=SUM(D21:D22)', F_BOLD, fill=FILL_SUB, border=True, align='center')
put(TK, f'E{r}', '=SUM(E21:E22)', F_BOLD, fmt=QTY, fill=FILL_SUB, border=True,
    align='center')
MIRROR_AREA = f"'განზომილებები'!$E$23"


# ============================================================ სამუშაო (works)
W = wb.create_sheet('სამუშაო')
widths(W, {'A': 5, 'B': 56, 'C': 8, 'D': 11, 'E': 10, 'F': 13, 'G': 12,
           'H': 13, 'I': 46})
put(W, 'B1', 'შესრულებული და მიმდინარე სამუშაოები (ფაქტი/ვალდებულებები)', F_TITLE)
put(W, 'B2', 'IN-HOUSE = სასტუმროს პერსონალი — ფულადი ხარჯი 0 ₾. '
             'PAID სტრიქონები — ფაქტობრივი (ისტორიული) ფასები.', F_NOTE)
header_row(W, 4, ['N', 'სამუშაოს დასახელება', 'განზ.', 'ერთ. ღირ. (₾)', 'რაოდ.',
                  'ღირებულება (₾)', 'გადახდა', 'სტატუსი', 'შენიშვნა'])
# (label, unit, unit_price, qty, F_mode, pay, cond, note)
# F_mode: 'calc' =D*E ; number = fixed contract price ; 0 = in-house
IH = 'IN-HOUSE'
works = [
    ('თეთრი პანელების დაშპაკვლა, შეღებვა', 'კვ.მ', None, None, 0, IH, 'IN PROCESS', ''),
    ('მაგიდების, კარადების, ნალიშნიკების შეღებვა', 'ც.', None, None, 0, IH, 'IN PROCESS', ''),
    ('სილიკონის მოჭრა, დაფუგვა აბაზანის', '', None, None, 0, IH, 'DONE', ''),
    ('ჭერის ჩამოჭრა', 'კვ.მ', None, None, 0, IH, 'DONE', ''),
    ('შეღებვა აბაზანის და ნომრის ჭერის', 'ნომ.', None, 18, 0, IH, 'DONE', ''),
    ('აქსესუარების გადამაგრება ნომერში', 'ნომ.', None, 18, 0, IH, 'IN PROCESS', ''),
    ('ხელსაბანის ნიჟარის პანელების გალაქვა', '', None, None, 0, IH, 'IN PROCESS', ''),
    ('დერეფნის შეღებვა', 'ნომ.', None, 18, 0, IH, 'IN PROCESS', ''),
    ('ხალიჩის აღება', '', None, None, 0, IH, 'IN PROCESS', ''),
    ('ხალიჩის დაგება', 'სართ.', None, 1, 1000, 'UNPAID', 'IN PROCESS',
     'ფიქსირებული შეთანხმებული ფასი (მე-19 სართული)'),
    ('ფანკოილის ძრავების შეცვლა', '', None, None, 0, IH, 'DONE', ''),
    ('კონდენსატორების შეცვლა', '', None, None, 0, IH, 'DONE', ''),
    ('მინი ბარების უკან ამოჭრა და გაწმენდა', '', None, None, 0, IH, 'IN PROCESS', ''),
    ('იმპულსორების გადამოწმება, ელექტროობის', '', None, None, 0, IH, 'DONE', ''),
    ('იატაკის მოციკლოვება, გალაქვა', '', None, None, 0, IH, 'IN PROCESS', ''),
    ('პარკეტის დაფის იატაკის დემონტაჟი (1901; 1902; 1907; 1909; 1910; 1916; 1918; 1919)',
     'კვ.მ', None, 162, 500, 'PAID', 'DONE',
     'ფაქტი: 500 ₾ კონტრაქტი (≈3.1 ₾/კვ.მ; ბაზარი 2 ₾/კვ.მ — demontaji.ge)'),
    ('პლინტუსის შეღებვა', '', None, None, 0, IH, 'IN PROCESS', ''),
    ('მარაცის ქვის დაგება', 'კვ.მ', 80, 30, 'calc', 'PAID', 'DONE',
     'ფაქტი; ბაზარი: სტანდარტი 30–60 ₾, პრემიუმ მარმარილო ~80 ₾ (servisebi.ge)'),
    ('მაგიდის დემონტაჟი, მონტაჟი', '', None, None, 0, IH, 'IN PROCESS', ''),
    ('ფანჯრების შემოწმება, შეკეთება', 'ც.', 50, 8, 'calc', 'UNPAID', 'IN PROCESS', ''),
    ('საფარდე კარნიზის გადამაგრება', '', None, None, 0, IH, 'DONE', ''),
    ('კარადის კარის პეტლების შეკეთება', '', None, None, 0, IH, 'DONE', ''),
    ('ფანკოილის რადიატორის გაწმენდა', '', None, None, 0, IH, 'DONE', ''),
    ('სამსვლიანების დაზეთვა', '', None, None, 0, IH, 'IN PROCESS', ''),
    ('სალნიკების შეცვლა', '', None, None, 0, IH, 'IN PROCESS', ''),
    ('პარკეტის აღება აბაზანაში', 'კვ.მ', None, f'={BATHFLOOR}', 0, IH, 'DONE',
     'რაოდ. — იხ. „განზომილებები“ (34.8 კვ.მ); შიდა რესურსით'),
    ('ნომრის და აბაზანის კარის დემონტაჟი, მონტაჟი', 'ც.', None, 37, 0, IH, 'DONE', ''),
    ('კარის (209×83×4.5სმ) დაშპონვა, შეღებვა (რესტავრაცია)', 'ც.', 560, 19, 'calc',
     'PAID', 'IN PROCESS',
     'ფაქტობრივი კონტრაქტი; ბაზრის ორიენტირი სრული რესტავრაცია 250–500 ₾/კარი'),
    ('კარის (209×70×4.5სმ) შეღებვა, რესტავრაცია', 'ც.', 343, 18, 'calc', 'PAID',
     'IN PROCESS', 'ფაქტობრივი კონტრაქტი'),
    ('შეღებილი MDF-ის პლინტუსი 15×1.6სმ (მასალა+მონტაჟი)', 'მეტრი', 20.7, 150, 'calc',
     'PAID', 'IN PROCESS', 'ფაქტი'),
    ('იატაკის დაგება (ფანერის და პარკეტის მონტაჟი)', 'კვ.მ', 40, 165, 'calc',
     'UNPAID', 'DONE', 'შეთანხმებული 40 ₾/კვ.მ; ბაზარი: მხოლოდ პარკეტი 25–65 ₾'),
    ('საწოლის თავთან პანელების გადამაგრება', '', None, None, 0, IH, 'DONE', ''),
    ('მილების შეფუთვა კონდენსატისთვის', '', None, None, 0, IH, 'DONE', ''),
    ('სიფონის გაწმენდა', '', None, None, 0, IH, 'IN PROCESS', ''),
    ('უნიტაზის რეზინის შეცვლა', '', None, None, 0, IH, 'IN PROCESS', ''),
    ('გერმეტიული სანათების მოხსნა, გაწმენდა', '', None, None, 0, IH, 'IN PROCESS', ''),
    ('შხაპის კაბინის დამზადება (1901)', 'კვ.მ', 300, 2.66, 'calc', 'UNPAID',
     'IN PROCESS', 'შეთანხმებული ≈800 ₾ (300 ₾/კვ.მ × 2.66 კვ.მ)'),
    ('გატეხილი სარკეების შეცვლა', 'კვ.მ', f"={P['mirror']}", f'={MIRROR_AREA}',
     'calc', 'UNPAID', 'IN PROCESS',
     'შეფასება ინვოისამდე: 140 ₾/კვ.მ × 10.84 კვ.მ (serwish.ge); ძველში — „ინვოისს ველოდებით“'),
]
r = 5
for i, (label, unit, up, qty, mode, pay, cond, note) in enumerate(works, 1):
    put(W, f'A{r}', i, border=True, align='center')
    put(W, f'B{r}', label, border=True, wrap=True)
    put(W, f'C{r}', unit, border=True, align='center')
    if up is not None:
        f = F_LNK if isinstance(up, str) else F_IN
        put(W, f'D{r}', up, font=f, fmt=MONEY, border=True, align='center')
    else:
        put(W, f'D{r}', '—', border=True, align='center')
    if qty is not None:
        f = F_LNK if isinstance(qty, str) else F_IN
        put(W, f'E{r}', qty, font=f, fmt=QTY, border=True, align='center')
    else:
        put(W, f'E{r}', '', border=True)
    if mode == 'calc':
        put(W, f'F{r}', f'=D{r}*E{r}', fmt=MONEY, border=True, align='center')
    elif mode == 0:
        put(W, f'F{r}', 0, font=F_IN, fmt=MONEY, border=True, align='center')
    else:
        put(W, f'F{r}', mode, font=F_IN, fmt=MONEY, border=True, align='center')
    put(W, f'G{r}', pay, border=True, align='center')
    put(W, f'H{r}', cond, border=True, align='center')
    put(W, f'I{r}', note, font=F_NOTE, border=True, wrap=True)
    r += 1
LAST_W = r - 1
put(W, f'B{r}', 'ჯამი', F_TOT, fill=FILL_TOT, border=True)
for col in 'ACDEGH':
    put(W, f'{col}{r}', '', fill=FILL_TOT, border=True)
put(W, f'F{r}', f'=SUM(F5:F{LAST_W})', F_TOT, fmt=MONEY, fill=FILL_TOT,
    border=True, align='center')
put(W, f'I{r}', '', fill=FILL_TOT, border=True)
W_TOT = r
r += 2
put(W, f'B{r}', 'ჯამის გაშლა სტატუსების მიხედვით', F_SEC)
r += 1
W_PAID = r          # first row of the breakdown block
W_UNPAID = r + 1
for lab, crit, col in [('გადახდილი (PAID)', 'PAID', 'G'),
                       ('გადასახდელი (UNPAID)', 'UNPAID', 'G'),
                       ('შიდა რესურსით (IN-HOUSE) — ფულადი ხარჯის გარეშე', IH, 'G'),
                       ('დასრულებული (DONE)', 'DONE', 'H'),
                       ('მიმდინარე (IN PROCESS)', 'IN PROCESS', 'H')]:
    W.merge_cells(f'B{r}:E{r}')
    put(W, f'B{r}', lab, F_BOLD, border=True)
    for c in 'CDE':
        W[f'{c}{r}'].border = BOX
    put(W, f'F{r}', f'=SUMIF({col}5:{col}{LAST_W},"{crit}",F5:F{LAST_W})',
        fmt=MONEY, border=True, align='center')
    r += 1
W.freeze_panes = 'A5'


# ============================================================ მასალები
M = wb.create_sheet('მასალები')
widths(M, {'A': 5, 'B': 52, 'C': 10, 'D': 11, 'E': 9, 'F': 13, 'G': 12,
           'H': 12, 'I': 50})
put(M, 'B1', 'მასალები (შესყიდვები — ფაქტი და შეფასებები)', F_TITLE)
put(M, 'B2', 'PAID სტრიქონები — ფაქტობრივი ფასები; ცარიელი სტატუსით — შეფასება '
             'ბაზრის ფასით (13.08.2026).', F_NOTE)
header_row(M, 4, ['N', 'მასალის დასახელება', 'განზ.', 'ერთ. ფასი (₾)', 'რაოდ.',
                  'ღირებულება (₾)', 'გადახდა', 'სტატუსი', 'წყარო / შენიშვნა'])
# (name, unit, price, qty, pay, cond, note) ; price None + fixed -> special
mats = [
    ('თაბაშირმუყაო', 'ცალი', 17.5, 12, 'PAID', 'DONE',
     'ფაქტი; ბაზარი: Knauf სტანდ. 15 ₾, ტენმედეგი 22.6 ₾ (domino.com.ge)'),
    ('შურუფი 2×5', 'ყუთი', 26, 1, 'PAID', 'DONE', ''),
    ('შურუფი 3×5', 'ყუთი', 32, 1, 'PAID', 'DONE', ''),
    ('ცელოფანი', 'რულონი', 15, 40, 'PAID', 'DONE', 'ბაზარი 6–27 ₾/რულონი'),
    ('კუთხოვანა თაბაშირმუყაოს კუთხისთვის', 'ცალი', 4, 20, 'PAID', 'DONE', ''),
    ('საფითხნი Knauf (სუფთა პირი)', 'ტომარა', 18, 2, 'PAID', 'DONE',
     'ბაზარი: Fugagips 25კგ 20.35 ₾ (gorgia.ge)'),
    ('სავარძლის და პუფის ქეჩები', 'მეშოკი', 2, 30, 'PAID', 'DONE', ''),
    ('მაკლავიცა დიდი იზოლაციისთვის', 'ცალი', 15, 1, 'PAID', 'DONE', ''),
    ('ქაღალდის სკოჩი', 'ცალი', 5.5, 30, 'PAID', 'DONE',
     'ბაზარი 3–8 ₾ (domino.com.ge); რაოდენობა დასაზუსტებელია'),
    ('ფილტრები ემლაიმიდან', 'მეტრი', 9, 20, 'PAID', 'DONE', ''),
    ('თეთრი საღებავი პანელისთვის (2.5 კგ)', 'ცალი', 75, 4, 'PAID', 'DONE', ''),
    ('მაგიდების შავი საღებავი (2-კომპონენტიანი)', 'კგ', 45, 6, '', '',
     'შეფასება: 2K საღებავი ~36–60 ₾/ლ (grandmall.ge Novakril 2K); ძველში — „ველოდებით ფასს“'),
    ('გერმანული აპარატის შკურკა 40-იანი', 'ცალი', 2.8, 100, 'PAID', 'DONE',
     'ბაზარი: ზოგადი 1.05–1.95 ₾, Festool-კლასი ~4–5.5 ₾'),
    ('გერმანული აპარატის შკურკა 60-იანი', 'ცალი', 2.8, 100, 'PAID', 'DONE', ''),
    ('გერმანული აპარატის შკურკა 80-იანი', 'ცალი', 2.8, 50, 'PAID', 'DONE', ''),
    ('გერმანული აპარატის შკურკა 120-იანი', 'ცალი', 2.8, 50, 'PAID', 'DONE', ''),
    ('სმესი შპაკლი', 'ბალონი', 18, 2, '', '', ''),
    ('პარანიტის სალნიკები 20-ანი ფირატის', 'ცალი', 0.7, 100, 'PAID', 'DONE', ''),
    ('სილიკონი Würth გამჭვირვალე (SILSEAL 310მლ)', 'ცალი', 29, 20, 'PAID', 'DONE',
     'ფაქტი; მიმდინარე ფასი 32 ₾ (shop.wurth.com.ge)'),
    ('დანა', 'ცალი', 6, 10, 'PAID', 'DONE', 'ბაზარი 1.75–9.95 ₾'),
    ('პირები', 'ყუთი', 3, 20, 'PAID', 'DONE', 'ბაზარი 1.85–4.5 ₾/10ც'),
    ('ზეთი სპრეი (პეტლებისთვის)', 'ცალი', 32, 2, 'PAID', 'DONE', ''),
    ('ჟანგის მოსაშორებელი სპრეი WD-40', 'ცალი', 12, 3, 'PAID', 'DONE',
     'ფაქტი; მიმდინარე: 400მლ 18.1 ₾ (domino), 200მლ 15.2 ₾ (gorgia)'),
    ('იზოლენტა', 'ცალი', 3, 10, 'PAID', 'DONE', 'ბაზარი 0.7–3.4 ₾'),
    ('ჟანგის მოსაცილებელი', 'ცალი', 12, 1, 'PAID', 'DONE', ''),
    ('დეკორის გრძელბეწვიანი სატკეპნი', 'ცალი', 4, 2, '', '', ''),
    ('ჩოთქები 5-ანი', 'ცალი', 6, 4, 'PAID', 'DONE', 'ბაზარი 2.5–5.95 ₾ (Color Expert)'),
    ('იახტლაქი (შუშის ძირების და პადონისთვის)', 'კგ', 60, 4, 'PAID', 'DONE',
     'ფაქტი — პრემიუმ კლასი; ბაზარი 24–50 ₾/კგ (gorgia, grandmall)'),
    ('პატარა სატკეპნის პირები (დაბალი ბეწვით)', 'ცალი', 4, 15, 'PAID', 'DONE', ''),
    ('ფანკოილის მილების შესაფუთი ქეჩები (25-ანი)', 'ცალი', 8, 10, 'PAID', 'DONE', ''),
    ('შავი შესაფუთზე დასახვევი იზოლაცია', 'ცალი', 40, 2, 'PAID', 'DONE', ''),
    ('იმპულსური რელეები', 'ცალი', 75, 10, 'PAID', 'DONE',
     'EU ფასი 47–62 ₾ + იმპორტი → 60–110 ₾; 75 ₾ რეალისტურია'),
    ('წებო ცემენტი Kerakoll', 'ტომარა', 35, 15, 'PAID', 'DONE',
     'იტალიური საცალო ≈38–39 ₾; დილერი — Espano (espano.ge)'),
    ('ლაქი პრიალა (აეროზოლი)', 'ბალონი', 81.4, 86, 'PAID', 'DONE',
     'ფაქტი; ⚠ ბაზარი: აეროზოლი 20–32 ₾ (Novol 23 ₾, 17 ₾ 6+ ც.) — მომავალში დიდი ეკონომიაა შესაძლებელი'),
    ('იზოლაცია Kerakoll (ჰიდროიზოლაცია 20კგ)', 'ტომარა', 230, 2, 'PAID', 'DONE',
     'UK საცალო £67–73 ≈ 235–255 ₾ — ფასი რეალისტურია'),
    ('პეპელა 4-ანი საფარდისთვის (რკინის)', 'ცალი', 0.85, 50, 'PAID', 'DONE', ''),
    ('პროფილი UD', 'ყუთი', 6, 24, 'PAID', 'DONE', ''),
    ('Akfix თეთრი სილიკონი', 'ყუთი', 14, 24, 'PAID', 'DONE',
     'ბაზარი 12.5 ₾ (goodbuild.ge); რაოდენობა დაემატება'),
    ('Sista გამჭვირვალე სილიკონი', 'ყუთი', 20, 20, 'PAID', 'DONE',
     'ფაქტი; მიმდინარე ბაზარი 12.2–14 ₾ — მომავალში ეკონომია'),
    ('აბაზანის ნიჟარის სიფონი', 'ცალი', 114, 10, 'UNPAID', '',
     'შეკვეთილია; ალტერნატივა: Geberit 87 ₾ (gorgia.ge) — ეკონომია ~270 ₾'),
    ('ფიცარი (ლისტვენიცა, 2-იანი სიგანე)', 'ცალი', 59.5, 12, 'PAID', '', ''),
    ('პარკეტის ფანერა (8-ანი)', 'ცალი', 35, 65, 'PAID', 'DONE',
     'ბაზარი: არყის 8მმ 29 ₾ (ecowood.ge)'),
    ('დუბელ-შურუფი (10-ანი)', 'ცალი', 1, 3000, 'PAID', 'DONE', 'ბაზარი 0.7–2.5 ₾'),
    ('წებო ცემენტი Kerakoll', 'ტომარა', 35, 5, 'PAID', 'DONE', ''),
    ('სომხური პევეა (17-18 ლ)', 'ბალონი', 185, 6, 'PAID', 'DONE',
     'ბაზარი: Crown (სომხეთი) 17კგ 170 ₾ (domino.com.ge)'),
    ('სვერლო პატარა პერფორატორისთვის (10-ანი)', 'ცალი', 15, 2, 'PAID', 'DONE', ''),
    ('ნაგვის დიდი ტომარა', 'ცალი', 0.6, 200, 'PAID', 'DONE',
     'ფაქტი; მიმდინარე 240ლ გამძლე 1.1–2.5 ₾/ც — მომავალ შესყიდვაში გაითვალისწინეთ'),
    ('აგური შხაპის ძირისთვის', 'ცალი', 1, 30, 'PAID', 'DONE', ''),
    ('რეზინის შუასადები სიფონისთვის', 'ცალი', 1.5, 18, 'PAID', 'DONE', ''),
    ('ცემენტი (25კგ)', 'ტომარა', 14, 1, 'PAID', 'DONE',
     'ფაქტი; მიმდინარე: Heidelberg M300 8.8–9.1 ₾'),
    ('ყვითელი საჩხერის ქვიშა', 'ტომარა', 1.5, 4, 'PAID', 'DONE', 'ბაზარი 2.5 ₾/ტომარა'),
    ('წებო ცემენტი Kerakoll', 'ტომარა', 35, 12, 'PAID', 'DONE', ''),
    ('ხალიჩა სართულისთვის (~134 კვ.მ, 19 €/კვ.მ)', 'კვ.მ', None, 134, 'PAID', 'DONE',
     'ფაქტობრივი გადახდა 7,600 ₾; დღევანდელი კურსით იქნებოდა ≈8,459 ₾ (63.13 ₾/კვ.მ)'),
    ('სმესი', 'ბალონი', 18, 1, 'PAID', 'DONE', 'ფასი შევსებულია №17-ის ანალოგიით'),
    ('პატარა პერფორატორის 10-ანი სვერლო', 'ცალი', 15, 1, '', '',
     'შეფასება №46-ის ფაქტით'),
    ('პატარა სატკეპნის პირები (დაბალი ბეწვით)', 'ცალი', 4, 10, '', '',
     'შეფასება №29-ის ფაქტით'),
    ('2-კომპონენტიანი ფუგა', 'კგ', 28, 5, '', '',
     'შეფასება: Kerakoll Fugabella ≈25–30 ₾/კგ (espano.ge — ფასი მოთხოვნით)'),
    ('პატარა ბალგარკის დიდი შკურკის ფხრიწი', 'ცალი', 3, 6, 'PAID', 'DONE',
     'შეფასება: ბაზარი 1.05–5.5 ₾'),
    ('ნათურა 12W თბილი ნათებით', 'ცალი', 19, 10, '', '',
     'V-TAC/Philips კლასი 19–26 ₾; ეკონომ Ledolet 4.4 ₾ (domino.com.ge)'),
    ('ლურსმანი', 'კგ', 4, 5, 'PAID', 'DONE', 'შეფასება — საბაზრო ფასი'),
    ('შურუფი 35-ანი', 'ყუთი', 31, 1, '', '',
     'Knauf TN35 1000ც: 31 ₾ (kshop.ge ოფიც.), 18.65 ₾ (keremont.ge)'),
    ('შურუფი 40-ანი', 'ყუთი', 32, 1, '', '', 'შეფასება TN35-ის ანალოგიით'),
    ('ფუგა შავი 1-კომპონენტიანი', 'ცალი', 25, 1, '', '', 'შეფასება'),
]
r = 5
for i, (name, unit, price, qty, pay, cond, note) in enumerate(mats, 1):
    put(M, f'A{r}', i, border=True, align='center')
    put(M, f'B{r}', name, border=True, wrap=True)
    put(M, f'C{r}', unit, border=True, align='center')
    if price is None:  # carpet actual
        put(M, f'D{r}', '', border=True)
        put(M, f'E{r}', qty, font=F_IN, fmt=QTY, border=True, align='center')
        put(M, f'F{r}', 7600, font=F_IN, fmt=MONEY, border=True, align='center')
    else:
        put(M, f'D{r}', price, font=F_IN, fmt=MONEY, border=True, align='center')
        put(M, f'E{r}', qty, font=F_IN, fmt=QTY, border=True, align='center')
        put(M, f'F{r}', f'=D{r}*E{r}', fmt=MONEY, border=True, align='center')
    put(M, f'G{r}', pay, border=True, align='center')
    put(M, f'H{r}', cond, border=True, align='center')
    put(M, f'I{r}', note, font=F_NOTE, border=True, wrap=True)
    r += 1
LAST_M = r - 1
put(M, f'B{r}', 'ჯამი', F_TOT, fill=FILL_TOT, border=True)
for col in 'ACDEGH':
    put(M, f'{col}{r}', '', fill=FILL_TOT, border=True)
put(M, f'F{r}', f'=SUM(F5:F{LAST_M})', F_TOT, fmt=MONEY, fill=FILL_TOT,
    border=True, align='center')
put(M, f'I{r}', '', fill=FILL_TOT, border=True)
M_TOT = r
r += 2
M.merge_cells(f'B{r}:E{r}')
put(M, f'B{r}', 'გადახდილი (PAID)', F_BOLD, border=True)
for c in 'CDE':
    M[f'{c}{r}'].border = BOX
put(M, f'F{r}', f'=SUMIF(G5:G{LAST_M},"PAID",F5:F{LAST_M})', fmt=MONEY,
    border=True, align='center')
M_PAID = r
r += 1
M.merge_cells(f'B{r}:E{r}')
put(M, f'B{r}', 'გადასახდელი / ჯერ შეუსყიდავი (შეფასება)', F_BOLD, border=True)
for c in 'CDE':
    M[f'{c}{r}'].border = BOX
put(M, f'F{r}', f'=F{M_TOT}-F{M_PAID}', fmt=MONEY, border=True, align='center')
M.freeze_panes = 'A5'


# ============================================================ ინსტრუმენტები
I_ = wb.create_sheet('ინსტრუმენტები')
widths(I_, {'A': 5, 'B': 50, 'C': 9, 'D': 12, 'E': 9, 'F': 13, 'G': 12, 'H': 50})
put(I_, 'B1', 'ინსტრუმენტები', F_TITLE)
header_row(I_, 3, ['N', 'დასახელება', 'განზ.', 'ერთ. ფასი (₾)', 'რაოდ.',
                   'ღირებულება (₾)', 'გადახდა', 'წყარო / შენიშვნა'])
tools = [
    ('პერფორატორი DeWalt პატარა (D25133K, SDS-Plus)', 'ცალი', 445, 1, 'UNPAID',
     'ოფიც. ფასი dewaltshop.ge (13.08.2026); ძველ ბიუჯეტში 695 ₾ — ეკონომია 250 ₾'),
    ('პერფორატორი DeWalt დიდი (D25733K, SDS-Max)', 'ცალი', 2395, 1, 'UNPAID',
     'ოფიც. ფასი dewaltshop.ge, მარაგშია; ძველში 2,990 ₾ — ეკონომია 595 ₾'),
    ('პიკა პატარა პერფორატორისთვის (ბეტონის ასაფხეკი)', 'ცალი', 45, 2, 'PAID',
     'ფაქტი; მიმდინარე ბაზარი: Raider 4.8–11 ₾, DeWalt SDS-Max 19–30 ₾'),
]
r = 4
for i, (name, unit, price, qty, pay, note) in enumerate(tools, 1):
    put(I_, f'A{r}', i, border=True, align='center')
    put(I_, f'B{r}', name, border=True, wrap=True)
    put(I_, f'C{r}', unit, border=True, align='center')
    put(I_, f'D{r}', price, font=F_IN, fmt=MONEY, border=True, align='center')
    put(I_, f'E{r}', qty, font=F_IN, border=True, align='center')
    put(I_, f'F{r}', f'=D{r}*E{r}', fmt=MONEY, border=True, align='center')
    put(I_, f'G{r}', pay, border=True, align='center')
    put(I_, f'H{r}', note, font=F_NOTE, border=True, wrap=True)
    r += 1
LAST_I = r - 1
put(I_, f'B{r}', 'ჯამი', F_TOT, fill=FILL_TOT, border=True)
for col in 'ACDEG':
    put(I_, f'{col}{r}', '', fill=FILL_TOT, border=True)
put(I_, f'F{r}', f'=SUM(F4:F{LAST_I})', F_TOT, fmt=MONEY, fill=FILL_TOT,
    border=True, align='center')
put(I_, f'H{r}', '', fill=FILL_TOT, border=True)
I_TOT = r


# ============================================================ შემსრულებლები
C_ = wb.create_sheet('შემსრულებლები')
widths(C_, {'A': 5, 'B': 20, 'C': 52, 'D': 12, 'E': 14, 'F': 24, 'G': 40})
put(C_, 'B1', 'შემსრულებლები (გუნდები/ოსტატები)', F_TITLE)
put(C_, 'B2', 'ზოგი პოზიცია უკვე ასახულია „სამუშაო“ ფურცელში — ჯამში ორმაგად არ ითვლება.',
    F_NOTE)
header_row(C_, 4, ['N', 'შემსრულებელი', 'საგანი', 'დღეები', 'ღირებულება (₾)',
                   'სამუშაო ცხრილში?', 'შენიშვნა'])
crew = [
    ('ლომსაძე დ.', 'ნომრებში ხის იატაკის დემონტაჟი', 8, 500, 'კი — სამუშაო №16',
     'იგივე 500 ₾ კონტრაქტი'),
    ('მურვანიძე კ.', 'აბაზანის იატაკის დემონტაჟი, აბაზანის ჭერის შეღებვა', 10, 1000,
     'არა', ''),
    ('', 'მალიარის დამხმარე', 10, 1000, 'არა', ''),
    ('ჯანგიძე გ.', 'დურგალი (პადონის და შუშის ძირების შეცვლა)', 16, 800, 'არა', ''),
    ('', 'ხალიჩის დაგება (მე-19 სართული)', '', 1000, 'კი — სამუშაო №10',
     'იგივე 1,000 ₾ კონტრაქტი'),
    ('მიშა', 'ფანჯრების სახელურების შემოწმება, შეკეთება', 8, 400, 'კი — სამუშაო №20',
     'იგივე 400 ₾ კონტრაქტი'),
]
r = 5
for i, (who, what, days, amt, overlap, note) in enumerate(crew, 1):
    put(C_, f'A{r}', i, border=True, align='center')
    put(C_, f'B{r}', who, border=True)
    put(C_, f'C{r}', what, border=True, wrap=True)
    put(C_, f'D{r}', days, font=F_IN, border=True, align='center')
    put(C_, f'E{r}', amt, font=F_IN, fmt=MONEY, border=True, align='center')
    put(C_, f'F{r}', overlap, border=True, align='center')
    put(C_, f'G{r}', note, font=F_NOTE, border=True, wrap=True)
    r += 1
LAST_C = r - 1
put(C_, f'C{r}', 'ჯამი', F_BOLD, fill=FILL_SUB, border=True)
put(C_, f'E{r}', f'=SUM(E5:E{LAST_C})', F_BOLD, fmt=MONEY, fill=FILL_SUB,
    border=True, align='center')
for col in 'ABDFG':
    put(C_, f'{col}{r}', '', fill=FILL_SUB, border=True)
C_SUM = r
r += 1
put(C_, f'C{r}', 'აქედან უკვე „სამუშაო“ ცხრილშია', border=True)
put(C_, f'E{r}', f'=SUMIF(F5:F{LAST_C},"კი*",E5:E{LAST_C})', fmt=MONEY,
    border=True, align='center')
C_OVR = r
r += 1
put(C_, f'C{r}', 'დამატებით ასახული ჯამურ ბიუჯეტში', F_TOT, fill=FILL_TOT, border=True)
put(C_, f'E{r}', f'=E{C_SUM}-E{C_OVR}', F_TOT, fmt=MONEY, fill=FILL_TOT,
    border=True, align='center')
for col in 'ABDFG':
    put(C_, f'{col}{r}', '', fill=FILL_TOT, border=True)
C_NET = r


# ============================================================ შეჯამება
S = wb.create_sheet('შეჯამება', 0)
widths(S, {'A': 3, 'B': 56, 'C': 17, 'D': 17, 'E': 52})
put(S, 'B1', 'სასტუმროს მე-19 სართულის რემონტი — ბიუჯეტის შეჯამება', F_TITLE)
put(S, 'B2', 'ოთახები 1901–1919 (14 standard, 4 executive/business) + დერეფანი · '
             'ვალუტა: ლარი (GEL), დღგ 18% ჩათვლით', F_NOTE)
put(S, 'B3', 'ფასები გადამოწმებულია 13.08.2026 · კურსი: 1 EUR = 3.0205 ₾, '
             '1 USD = 2.6181 ₾ (ეროვნული ბანკი) · იხ. „დაშვებები“ და „წყაროები“',
    F_NOTE)

put(S, 'B5', 'A. მიმდინარე სარემონტო სამუშაოები — ფაქტი და ვალდებულებები', F_SEC)
header_row(S, 6, ['', 'მუხლი', 'თანხა (₾)', 'აქედან გადახდილი (₾)', 'შენიშვნა'], 1)
sec_a = [
    ('სამუშაოები', f"='სამუშაო'!F{W_TOT}", f"='სამუშაო'!F{W_PAID}",
     'IN-HOUSE სამუშაოები = 0 ₾ (სასტუმროს პერსონალი)'),
    ('შემსრულებლები (სამუშაოს ცხრილს გარეთ)', f"='შემსრულებლები'!E{C_NET}", '',
     'გადაფარვის გარეშე — იხ. ფურცელი „შემსრულებლები“'),
    ('მასალები', f"='მასალები'!F{M_TOT}", f"='მასალები'!F{M_PAID}",
     'შეიცავს შეფასებულ (ჯერ შეუსყიდავ) პოზიციებსაც'),
    ('ინსტრუმენტები', f"='ინსტრუმენტები'!F{I_TOT}",
     f'=SUMIF(ინსტრუმენტები!G4:G{LAST_I},"PAID",ინსტრუმენტები!F4:F{LAST_I})',
     'DeWalt-ის ფასები განახლებულია ოფიციალურ ფასებზე — ეკონომია 845 ₾'),
]
r = 7
for lab, tot, paid, note in sec_a:
    put(S, f'B{r}', lab, border=True)
    put(S, f'C{r}', tot, font=F_LNK, fmt=MONEY, border=True, align='center')
    if paid:
        put(S, f'D{r}', paid, font=F_LNK, fmt=MONEY, border=True, align='center')
    else:
        put(S, f'D{r}', 0, font=F_IN, fmt=MONEY, border=True, align='center')
    put(S, f'E{r}', note, font=F_NOTE, border=True, wrap=True)
    r += 1
A_TOT = r
put(S, f'B{r}', 'სულ მიმდინარე ეტაპი (A)', F_TOT, fill=FILL_TOT, border=True)
put(S, f'C{r}', f'=SUM(C7:C{r-1})', F_TOT, fmt=MONEY, fill=FILL_TOT,
    border=True, align='center')
put(S, f'D{r}', f'=SUM(D7:D{r-1})', F_TOT, fmt=MONEY, fill=FILL_TOT,
    border=True, align='center')
put(S, f'E{r}', '', fill=FILL_TOT, border=True)
r += 1
put(S, f'B{r}', 'დარჩენილი გადასახდელი (A)', F_BOLD, border=True)
put(S, f'C{r}', f'=C{A_TOT}-D{A_TOT}', F_BOLD, fmt=MONEY, border=True, align='center')
put(S, f'D{r}', '', border=True)
put(S, f'E{r}', '', border=True)

put(S, 'B14', 'B. სრული განახლების საპროგნოზო ბიუჯეტი (18 ოთახი + დერეფანი)', F_SEC)
header_row(S, 15, ['', 'მუხლი', 'თანხა (₾)', '', 'შენიშვნა'], 1)
sec_b = [
    ('შუალედური ჯამი (ოთახები + დერეფანი + ნაგვის გატანა)', f"='Total'!F{SUB}",
     '14 × standard, 4 × executive, დერეფანი'),
    ('გაუთვალისწინებელი ხარჯი (10%)', f"='Total'!F{SUB+1}", 'დარგობრივი ნორმა'),
]
r = 16
for lab, ref, note in sec_b:
    put(S, f'B{r}', lab, border=True, wrap=True)
    put(S, f'C{r}', ref, font=F_LNK, fmt=MONEY, border=True, align='center')
    put(S, f'D{r}', '', border=True)
    put(S, f'E{r}', note, font=F_NOTE, border=True, wrap=True)
    r += 1
put(S, f'B{r}', 'სულ საპროგნოზო ბიუჯეტი (B)', F_TOT, fill=FILL_TOT, border=True)
put(S, f'C{r}', f"='Total'!F{GRAND}", F_TOT, fmt=MONEY, fill=FILL_TOT,
    border=True, align='center')
put(S, f'D{r}', '', fill=FILL_TOT, border=True)
put(S, f'E{r}', f'=C{r}/{EUR}', font=F_NOTE, fmt='"≈ "#,##0" €"', fill=FILL_TOT,
    border=True, align='left')
B_TOT = r

put(S, 'B20', 'C. გამოვლენილი ეკონომია — სად იხდით საბაზროზე მეტს', F_SEC)
header_row(S, 21, ['', 'პოზიცია', 'ბიუჯეტში (₾)', 'ბაზარზე (₾)', 'პოტენციური ეკონომია'], 1)
savings = [
    ('პერფორატორი DeWalt პატარა + დიდი (1+1 ც.)', 3685, 2840,
     'dewaltshop.ge ოფიციალური ფასი — უკვე გასწორებულია ამ ფაილში'),
    ('ლაქი პრიალა აეროზოლი (86 ბალონი)', 6999.4, 1978,
     '81.4 ₾ vs Novol 23 ₾ (17 ₾ 6+ ც.) — შესყიდვამდე გადაამოწმეთ სპეციფიკაცია'),
    ('დუში პატარა, ხელის (18 ნომერი)', 5400, 3240,
     '300 ₾ vs Grohe Vitalio კომპლექტი 180 ₾ (domino.com.ge)'),
    ('Sista გამჭვირვალე სილიკონი (20 ყუთი)', 400, 244,
     '20 ₾ vs Soudal/Sista 12.2–14 ₾'),
    ('აბაზანის ნიჟარის სიფონი (10 ც.)', 1140, 870,
     '114 ₾ vs Geberit 87 ₾ (gorgia.ge)'),
    ('ცემენტი, ნაგვის ტომრები, WD-40 და სხვ. წვრილმანი', 0, 0,
     'ნაწილი ძვირია, ნაწილი იაფად არის ჩადებული — დეტალები „მასალები“ ფურცელზე'),
]
r = 22
for lab, old, new, note in savings:
    put(S, f'B{r}', lab, border=True, wrap=True)
    put(S, f'C{r}', old if old else '', font=F_IN, fmt=MONEY, border=True, align='center')
    put(S, f'D{r}', new if new else '', font=F_IN, fmt=MONEY, border=True, align='center')
    put(S, f'E{r}', note, font=F_NOTE, border=True, wrap=True)
    r += 1
put(S, f'B{r}', 'სულ პოტენციური ეკონომია', F_TOT, fill=FILL_TOT, border=True)
put(S, f'C{r}', f'=SUM(C22:C{r-1})', F_TOT, fmt=MONEY, fill=FILL_TOT, border=True,
    align='center')
put(S, f'D{r}', f'=SUM(D22:D{r-1})', F_TOT, fmt=MONEY, fill=FILL_TOT, border=True,
    align='center')
put(S, f'E{r}', f'=C{r}-D{r}', F_TOT, fmt='#,##0.00" ₾"', fill=FILL_TOT, border=True,
    align='center')
SAVE_ROW = r

put(S, f'B{r+2}', 'მეთოდოლოგია და შენიშვნები', F_SEC)
notes = [
    'A და B სხვადასხვა მოცულობაა: A — მიმდინარე ეტაპის ფაქტობრივი/ნაკისრი ხარჯები; '
    'B — მომავალი სრული განახლების საბაზრო შეფასება (მასალა + სამუშაო).',
    'ყველა ერთეულის ფასი გადამოწმებულია 13.08.2026 ქართულ საცალო წყაროებზე '
    '(gorgia.ge, domino.com.ge, parketi.ge, bona.com.ge, dewaltshop.ge და სხვ.) — '
    'სრული სია ფურცელზე „წყაროები“.',
    'გასწორებულია ძველი ფაილის შეცდომები: (1) ხარჯაღრიცხვის ფურცელი მასალების ჯამს '
    'კარგავდა (ცარიელ F69-ს იშველიებდა) — მასალები ≈30,303 ₾ ჯამში არ ჯდებოდა; '
    '(2) standard ოთახში საღებავის სტრიქონი (125 ₾) ჯამში არ იყო; '
    '(3) 12 პოზიციას ფასი საერთოდ არ ჰქონდა — შევსებულია საბაზრო შეფასებით.',
    'ლეგენდა: ლურჯი — შესაყვანი/ფაქტობრივი მონაცემი · შავი — ფორმულა · '
    'მწვანე — ბმული სხვა ფურცელზე · ყვითელი ფონი — საკვანძო დაშვება ან ჯამი.',
]
r = SAVE_ROW + 3
for n in notes:
    S.merge_cells(f'B{r}:E{r}')
    put(S, f'B{r}', '• ' + n, font=F_NOTE, wrap=True)
    S.row_dimensions[r].height = 26 + 13 * (len(n) // 150)
    r += 1


# ============================================================ წყაროები
SRC = wb.create_sheet('წყაროები')
widths(SRC, {'A': 5, 'B': 24, 'C': 34, 'D': 52, 'E': 46, 'F': 13})
put(SRC, 'B1', 'წყაროები — ფასების გადამოწმება (ბიბლიოგრაფია)', F_TITLE)
put(SRC, 'B2', 'ყველა წყარო შემოწმდა 13.08.2026. „გადამოწმებული“ = ფასი ნანახია '
               'ცოცხალ გვერდზე; „შეფასება“ = მიახლოება შედარებადი პოზიციებით.', F_NOTE)
header_row(SRC, 4, ['N', 'კატეგორია', 'წყარო', 'URL', 'რა გადამოწმდა', 'სტატუსი'])
sources = [
    ('მაკრო', 'საქართველოს ეროვნული ბანკი', 'nbg.gov.ge/gw/api/ct/monetarypolicy/currencies/en/json',
     'EUR/GEL 3.0205; USD/GEL 2.6181 (13.08.2026)', 'გადამოწმებული'),
    ('მაკრო', 'Geostat / TradingEconomics', 'geostat.ge · tradingeconomics.com/georgia/inflation-cpi',
     'ინფლაცია ~4.3–5.5%; სამშენებლო ხარჯების ინდექსი', 'გადამოწმებული'),
    ('იატაკი', 'parketi.ge', 'parketi.ge/en/collections/oak-parquet',
     'მუხის მასიური პარკეტი: Rustic 75 / Select 99 / Exclusive 140 ₾/კვ.მ; ინჟინრული 179–269 ₾',
     'გადამოწმებული'),
    ('იატაკი', 'ecowood.ge', 'ecowood.ge',
     'ფანერა არყის 1525×1525: 8მმ 29 ₾, 10მმ 34 ₾, 12მმ 41 ₾; მასიური მუხა Extra 179 ₾',
     'გადამოწმებული'),
    ('იატაკი', 'Bona Georgia (ოფიც.)', 'bona.com.ge/parketis-laqi/',
     'ლაქი Bona Mega EVO 380 ₾/5ლ ≈76 ₾/ლ; ხაზი 240–500 ₾', 'გადამოწმებული'),
    ('იატაკი', 'shop.glimtrex.ge', 'shop.glimtrex.ge/ciklovka',
     'მოციკლოვება 20 ₾/კვ.მ; სრული ციკლი ლაქით 40–45 ₾/კვ.მ', 'გადამოწმებული'),
    ('იატაკი', 'homeis.ge', 'homeis.ge/iatakis-dageba/',
     'პარკეტის დაგება: კომპანია 30–65 ₾, ოსტატი 25–60 ₾/კვ.მ', 'ნაწილობრივ'),
    ('იატაკი', 'demontaji.ge', 'demontaji.ge (2026 ტარიფები)',
     'პარკეტის აყრა 2 ₾/კვ.მ; ნაგვის გატანა ~370 ₾/მ³', 'გადამოწმებული'),
    ('იატაკი', 'domino.com.ge', 'domino.com.ge — carpeting, mdf-plinth',
     'ბელგიური ხალიჩა 10.5–119 ₾/კვ.მ; MDF პლინტუსი 10–15.2 ₾/მ', 'გადამოწმებული'),
    ('იატაკი', 'gurus.ge', 'gurus.ge/remonti/laminatis-dageba',
     'ლამინატის დაგება 10–25 ₾/კვ.მ (ხალიჩის პროქსი)', 'შეფასება'),
    ('სანტექნიკა', 'gorgia.ge', 'gorgia.ge/ka/grohe/',
     'Grohe შემრევები 187–306 ₾; ხელის შხაპი 63–103 ₾; Geberit სიფონი 70.5–87 ₾',
     'გადამოწმებული'),
    ('სანტექნიკა', 'domino.com.ge', 'domino.com.ge/en/grohe/',
     'ზედა შხაპი AM.PM 250მმ 389 ₾; Grohe სისტემები 599–1275 ₾; Grohe კომპლექტი 159–180 ₾',
     'გადამოწმებული'),
    ('განათება', 'light11.eu / AmbienteDirect / smow', 'light11.eu · ambientedirect.com · smow.com',
     'Artemide Tolomeo Terra 488–549 €; Micro/Parete 225–314 €', 'გადამოწმებული (EU)'),
    ('კარები', 'domino.com.ge', 'domino.com.ge — interior-doors',
     'ოთახის კარი: ეკონომ 149–359 ₾, KMF 649–699 ₾, Terminus 1029–1499 ₾; აბაზანის PVC 359 ₾',
     'გადამოწმებული'),
    ('ავეჯი', 'veli.store / liva.ge / embawood.ge', 'veli.store · liva.ge · embawood.ge',
     'ტუმბო 200–300 ₾; TV მაგიდა 200–450 ₾', 'ნაწილობრივ'),
    ('სარკე', 'serwish.ge', 'serwish.ge — სარკეები შეკვეთით',
     'მასალა 40–50 ₾/კვ.მ-დან; სრული (ჭრა+მონტაჟი) 100–180 ₾/კვ.მ', 'შეფასება'),
    ('საღებავი', 'Sto Georgia', 'sto.ge (ფასი მოთხოვნით)',
     'StoColor In: EU საცალო ~15–18 ₾/ლ → საქართველოში 20–28 ₾/ლ', 'შეფასება'),
    ('საღებავი', 'remonti-mshenebloba.ge / euroremonti.ge / servisebi.ge',
     'remonti-mshenebloba.ge · euroremonti.ge · servisebi.ge',
     'სამღებრო: შეღებვა 8–15 ₾ + მოშპაკვლა 4–5 ₾ = 12–20 ₾/კვ.მ; ქვის დაგება 30–60 ₾ '
     '(პრემიუმ ~80 ₾); კარის რესტავრაცია 120–500 ₾', 'გადამოწმებული'),
    ('მასალები', 'gorgia.ge / kshop.ge / keremont.ge', 'gorgia.ge · kshop.ge · keremont.ge',
     'Knauf Fugagips 25კგ 20.35 ₾; შურუფი TN35 1000ც 18.65–31 ₾', 'გადამოწმებული'),
    ('მასალები', 'domino.com.ge / nova.ge', 'domino.com.ge · nova.ge',
     'თაბაშირმუყაო Knauf 15 ₾ (ტენმედეგი 22.6 ₾); ცემენტი Heidelberg M300 8.8–9.1 ₾; '
     'Crown PVA 17კგ 170 ₾; Soudal სილიკონი 8.3–12.2 ₾', 'გადამოწმებული'),
    ('მასალები', 'Espano (Kerakoll-ის დილერი)', 'espano.ge/brand/57',
     'Kerakoll: წებო ≈38–39 ₾ (იტალიური საცალოდან); ჰიდროიზოლაცია 20კგ ≈235–255 ₾',
     'შეფასება'),
    ('მასალები', 'shop.wurth.com.ge / goodbuild.ge / mihouse.ge',
     'shop.wurth.com.ge · goodbuild.ge · mihouse.ge',
     'Würth SILSEAL 32 ₾; Akfix 100E 12.5 ₾; Sista 14 ₾', 'გადამოწმებული'),
    ('მასალები', 'grandmall.ge', 'grandmall.ge',
     'აეროზოლური ლაქი Novol 23 ₾ (17 ₾ 6+ ც.); იახტლაქი MOBEL 24–31 ₾/კგ', 'გადამოწმებული'),
    ('ინსტრუმენტები', 'dewaltshop.ge (ოფიც. DeWalt)', 'dewaltshop.ge',
     'D25133K 445 ₾; D25733K 2,395 ₾ (მარაგში)', 'გადამოწმებული'),
    ('ინსტრუმენტები', 'domino.com.ge', 'domino.com.ge — chisels, abrasives',
     'პიკები: Raider 4.8–11 ₾, DeWalt SDS-Max 18.85–29.7 ₾; შკურკა 1.05–1.95 ₾',
     'გადამოწმებული'),
    ('შრომა', 'gancxadebebi.ge / worldsalaries.com', 'gancxadebebi.ge · worldsalaries.com',
     'მუშა 60–70 ₾/დღე; კვალიფიციური ოსტატი 100–150 ₾/დღე; Geostat მშენებლობის '
     'საშ. ხელფასი ~3,939 ₾/თვე', 'გადამოწმებული'),
    ('ელექტრო', 'lasma.eu / profelektro.lv (EU)', 'lasma.eu · profelektro.lv',
     'იმპულსური რელე Acti9 iTL 14.8–19.7 € → 60–110 ₾ იმპორტით (საქ. ლისტინგი არ მოიძებნა)',
     'შეფასება'),
]
r = 5
for i, (cat, src, url, what, st) in enumerate(sources, 1):
    put(SRC, f'A{r}', i, border=True, align='center')
    put(SRC, f'B{r}', cat, border=True, align='center')
    put(SRC, f'C{r}', src, border=True, wrap=True)
    put(SRC, f'D{r}', url, border=True, wrap=True)
    put(SRC, f'E{r}', what, font=F_NOTE, border=True, wrap=True)
    put(SRC, f'F{r}', st, border=True, align='center')
    r += 1
SRC.freeze_panes = 'A5'

# sheet order + tab colours + print setup
order = ['შეჯამება', 'დაშვებები', 'standard', 'executive', 'corridor', 'Total',
         'სამუშაო', 'მასალები', 'ინსტრუმენტები', 'შემსრულებლები',
         'განზომილებები', 'წყაროები']
wb._sheets = [wb[n] for n in order]

TABS = {'შეჯამება': '1F3864', 'დაშვებები': 'FFC000', 'standard': '2E75B6',
        'executive': '2E75B6', 'corridor': '2E75B6', 'Total': '1F3864',
        'სამუშაო': '548235', 'მასალები': '548235', 'ინსტრუმენტები': '548235',
        'შემსრულებლები': '548235', 'განზომილებები': '7F7F7F',
        'წყაროები': '7F7F7F'}
for nm, colour in TABS.items():
    ws = wb[nm]
    ws.sheet_properties.tabColor = colour
    ws.page_setup.orientation = 'landscape'
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_options.horizontalCentered = True
    ws.oddFooter.right.text = "&P / &N"
    ws.oddFooter.left.text = nm

wb.properties.title = 'სასტუმროს მე-19 სართულის რემონტის ბიუჯეტი'
wb.properties.subject = 'Hotel 19th floor renovation budget — Tbilisi, GEL'
wb.properties.keywords = 'budget; renovation; Tbilisi; GEL; 2026'

wb.save(OUT)
print('saved', OUT)
print('markers:', dict(STD_TOT=STD_TOT, EXE_TOT=EXE_TOT, COR_TOT=COR_TOT,
                       SUB=SUB, GRAND=GRAND, W_TOT=W_TOT, M_TOT=M_TOT,
                       I_TOT=I_TOT, C_NET=C_NET, B_TOT=B_TOT))
