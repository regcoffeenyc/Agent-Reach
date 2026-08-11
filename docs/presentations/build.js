const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");

const DARK = "23272B";
const DARK2 = "2F353B";
const ORANGE = "F26419";
const ORANGE_SOFT = "FDEBDF";
const CARD = "F2F3F4";
const TEXT = "23272B";
const MUTED = "6B7280";
const WHITE = "FFFFFF";
const FONT = "Arial";

const SECTIONS = [
  {
    n: "01", icon: "FaShieldAlt", title: "უსაფრთხოება",
    desc: "სასროლეთის უპირველესი პრიორიტეტი — წესები, ზედამხედველობა და მზადყოფნა",
    items: [
      { m: "Range Rules", s: "სასროლეთის წესები" },
      { m: "Safety Briefing", s: "უსაფრთხოების ინსტრუქტაჟი ყველა სტუმრისთვის" },
      { m: "RSO კონტროლი", s: "Range Safety Officer-ის მუდმივი ზედამხედველობა" },
      { m: "Cold / Hot Range", s: "რეჟიმების მკაცრი პროცედურები" },
      { m: "სამედიცინო გეგმა", s: "საგანგებო სიტუაციების გეგმა" },
      { m: "First Aid / Trauma", s: "პირველადი დახმარების აღჭურვილობა" },
      { m: "Incident Report", s: "ინციდენტების აღრიცხვა და ანალიზი" },
    ],
  },
  {
    n: "02", icon: "FaClipboardList", title: "ოპერაციები",
    desc: "ყოველდღიური სამუშაო პროცესი — მიღებიდან დღის დახურვამდე",
    items: [
      { m: "სამუშაო საათები", s: "გრაფიკი და სეზონური რეჟიმი" },
      { m: "ჯავშნები", s: "წინასწარი დაჯავშნის სისტემა" },
      { m: "სტუმრების მიღება", s: "დახვედრა და რეგისტრაცია" },
      { m: "Check-in", s: "დოკუმენტების და Waiver-ის გადამოწმება" },
      { m: "Bay Assignment", s: "ტირის განაწილება სტუმრებზე" },
      { m: "ინვენტარის გაცემა", s: "აღჭურვილობის გაცემა-დაბრუნება" },
      { m: "დღის დახურვა", s: "შემოწმება, აღრიცხვა, უსაფრთხო დახურვა" },
    ],
  },
  {
    n: "03", icon: "FaUsers", title: "პერსონალი",
    desc: "გუნდი, რომელიც უზრუნველყოფს უსაფრთხო და ეფექტურ მუშაობას",
    items: [
      { m: "Range Manager", s: "საერთო მართვა და პასუხისმგებლობა" },
      { m: "RSO", s: "Range Safety Officer — უსაფრთხოების კონტროლი" },
      { m: "ინსტრუქტორები", s: "სწავლება და კურსების ჩატარება" },
      { m: "ადმინისტრატორი", s: "მიღება, ჯავშნები, ანგარიშსწორება" },
      { m: "ტექნიკური პერსონალი", s: "ინფრასტრუქტურის მოვლა" },
      { m: "დაცვის თანამშრომელი", s: "ტერიტორიის და ქონების დაცვა" },
    ],
  },
  {
    n: "04", icon: "FaWarehouse", title: "ინფრასტრუქტურა",
    desc: "ფიზიკური გარემო — ტირები, დაცვითი ნაგებობები და კომუნიკაციები",
    items: [
      { m: "Shooting Bays", s: "სასროლი სექციები" },
      { m: "Long Range", s: "შორი დისტანციის სექცია" },
      { m: "Berms", s: "დამცავი მიწაყრილები" },
      { m: "გზები / პარკინგი", s: "მისასვლელი და სადგომი" },
      { m: "CCTV", s: "ვიდეომეთვალყურეობა" },
      { m: "განათება", s: "ტერიტორიის და ტირების განათება" },
      { m: "Storage", s: "საწყობი და შენახვა" },
      { m: "Maintenance Plan", s: "მოვლა-შენახვის გეგმა" },
    ],
  },
  {
    n: "05", icon: "FaBoxes", title: "ინვენტარი",
    desc: "აღჭურვილობა და მისი აღრიცხვა",
    items: [
      { m: "სამიზნეები", s: "ქაღალდის და მუყაოს სამიზნეები" },
      { m: "Steel Targets", s: "ლითონის სამიზნეები" },
      { m: "Stands", s: "სამიზნეების სადგამები" },
      { m: "Timer / Equipment", s: "ტაიმერები და აღჭურვილობა" },
      { m: "PPE", s: "დაცვის საშუალებები — სათვალე, ყურსაცმები" },
      { m: "Radios", s: "რაციები კომუნიკაციისთვის" },
      { m: "Tools", s: "ხელსაწყოები" },
      { m: "Inventory Log", s: "აღრიცხვის ჟურნალი" },
    ],
  },
  {
    n: "06", icon: "FaCoins", title: "ფინანსები",
    desc: "შემოსავლების ნაკადები, ხარჯები და ბიუჯეტირება",
    items: [
      { m: "შემოსავლები", s: "ყველა წყაროს აღრიცხვა" },
      { m: "წევრობის საფასური", s: "წლიური / თვიური წევრობა" },
      { m: "Range Fee", s: "ერთჯერადი ვიზიტის საფასური" },
      { m: "კურსები", s: "სასწავლო პროგრამების შემოსავალი" },
      { m: "ღონისძიებები", s: "შეჯიბრებები და ივენთები" },
      { m: "ტურისტული პაკეტები", s: "პაკეტები ვიზიტორებისთვის" },
      { m: "ხარჯები", s: "საოპერაციო და კაპიტალური" },
      { m: "ბიუჯეტი / Cash Flow", s: "დაგეგმვა და ფულადი ნაკადები" },
    ],
  },
  {
    n: "07", icon: "FaUserFriends", title: "მომხმარებლები",
    desc: "სამიზნე სეგმენტები — ვინ სარგებლობს სასროლეთით",
    items: [
      { m: "წევრები", s: "მუდმივი წევრები" },
      { m: "სტუმრები", s: "ერთჯერადი ვიზიტორები" },
      { m: "ტურისტები", s: "უცხოელი და ადგილობრივი ტურისტები" },
      { m: "კორპორატიული ჯგუფები", s: "თიმბილდინგი და ჯგუფური ვიზიტები" },
      { m: "სპორტსმენები", s: "შემეჯიბრო მიმართულების მოსროლეები" },
      { m: "VIP / Partners", s: "განსაკუთრებული სტუმრები და პარტნიორები" },
    ],
  },
  {
    n: "08", icon: "FaGraduationCap", title: "სწავლება",
    desc: "სასწავლო პროგრამები დამწყებიდან ინსტრუქტორამდე",
    items: [
      { m: "Beginner Course", s: "დამწყებთა კურსი" },
      { m: "Safety Course", s: "უსაფრთხოების კურსი" },
      { m: "Dynamic Shooting", s: "დინამიკური სროლის კურსი" },
      { m: "Instructor Program", s: "ინსტრუქტორთა მომზადება" },
      { m: "Certification", s: "სერტიფიცირება" },
      { m: "Training Records", s: "სწავლების აღრიცხვა" },
    ],
  },
  {
    n: "09", icon: "FaTrophy", title: "სპორტი / Events",
    desc: "შემეჯიბრო კალენდარი — კლუბური მატჩებიდან ჩემპიონატებამდე",
    items: [
      { m: "IPSC", s: "პრაქტიკული სროლის შეჯიბრებები" },
      { m: "Tactical Games", s: "ტაქტიკური თამაშები" },
      { m: "PRS / Long Range", s: "შორ დისტანციაზე სროლის მატჩები" },
      { m: "Club Matches", s: "საკლუბო შეჯიბრებები" },
      { m: "Championships", s: "ჩემპიონატები" },
      { m: "Event Calendar", s: "ღონისძიებების კალენდარი" },
    ],
  },
  {
    n: "10", icon: "FaFileAlt", title: "ადმინისტრაცია",
    desc: "დოკუმენტაცია, სამართლებრივი ბაზა და პროცედურები",
    items: [
      { m: "დოკუმენტაცია", s: "ოფიციალური დოკუმენტების მართვა" },
      { m: "კონტრაქტები", s: "ხელშეკრულებები პარტნიორებთან" },
      { m: "დაზღვევა", s: "პასუხისმგებლობის და ქონების დაზღვევა" },
      { m: "წევრთა ბაზა", s: "წევრების მონაცემთა ბაზა" },
      { m: "Consent / Waiver", s: "თანხმობის ფორმები" },
      { m: "Incident Archive", s: "ინციდენტების არქივი" },
      { m: "SOP-ები", s: "სტანდარტული ოპერაციული პროცედურები" },
    ],
  },
  {
    n: "11", icon: "FaBullhorn", title: "მარკეტინგი",
    desc: "ცნობადობა და მომხმარებელთა მოზიდვის არხები",
    items: [
      { m: "Website", s: "ვებგვერდი და ონლაინ ჯავშნები" },
      { m: "Facebook / Instagram", s: "სოციალური მედია" },
      { m: "Google Business", s: "ონლაინ ხილვადობა და შეფასებები" },
      { m: "ტურიზმის პარტნიორები", s: "ტუროპერატორები" },
      { m: "Hotels / Guides", s: "სასტუმროები და გიდები" },
      { m: "Sponsors", s: "სპონსორები" },
      { m: "Content Plan", s: "კონტენტის გეგმა" },
    ],
  },
  {
    n: "12", icon: "FaChartLine", title: "კონტროლი / KPI",
    desc: "შედეგების გაზომვა — რას ვაკვირდებით ყოველთვიურად",
    items: [
      { m: "Visitors / Month", s: "ვიზიტორები თვეში" },
      { m: "Revenue / Month", s: "შემოსავალი თვეში" },
      { m: "Membership Growth", s: "წევრობის ზრდა" },
      { m: "Course Attendance", s: "კურსების დასწრება" },
      { m: "Incident Rate", s: "ინციდენტების მაჩვენებელი" },
      { m: "Bay Utilization", s: "ტირების დატვირთვა" },
      { m: "Customer Rating", s: "მომხმარებელთა შეფასება" },
    ],
  },
  {
    n: "13", icon: "FaRocket", title: "განვითარება",
    desc: "ზრდის გეგმა — ახალი მიმართულებები და ინფრასტრუქტურა",
    items: [
      { m: "ახალი Bays", s: "სასროლი სექციების გაფართოება" },
      { m: "1,000m+ Range", s: "ულტრა-შორი დისტანციის ტირი" },
      { m: "Training Center", s: "სასწავლო ცენტრი" },
      { m: "Pro Shop", s: "აქსესუარების მაღაზია" },
      { m: "Café / Lounge", s: "დასასვენებელი სივრცე" },
      { m: "საერთაშორისო Events", s: "საერთაშორისო შეჯიბრებების მასპინძლობა" },
    ],
  },
  {
    n: "14", icon: "FaHandshake", title: "პარტნიორები",
    desc: "სტრატეგიული თანამშრომლობა სექტორებს შორის",
    items: [
      { m: "ფედერაციები", s: "სპორტული ფედერაციები" },
      { m: "სახელმწიფო უწყებები", s: "თანამშრომლობა უწყებებთან" },
      { m: "სპონსორები", s: "კორპორატიული მხარდაჭერა" },
      { m: "იარაღის ბრენდები", s: "ბრენდებთან პარტნიორობა" },
      { m: "ტურისტული სააგენტოები", s: "ტურისტული ნაკადები" },
      { m: "ადგილობრივი ბიზნესი", s: "რეგიონული თანამშრომლობა" },
    ],
  },
];

async function iconPng(name, hexColor) {
  const Comp = fa[name];
  if (!Comp) throw new Error("no icon " + name);
  const svg = ReactDOMServer.renderToStaticMarkup(
    React.createElement(Comp, { color: "#" + hexColor, size: 512 })
  );
  const buf = await sharp(Buffer.from(svg)).resize(512, 512, { fit: "contain", background: { r: 0, g: 0, b: 0, alpha: 0 } }).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

function targetRings(slide, cx, cy, maxR, color, lineW) {
  // decorative concentric target rings (circles centered at cx,cy)
  const rings = [maxR, maxR * 0.75, maxR * 0.5, maxR * 0.25];
  rings.forEach((r) => {
    slide.addShape("ellipse", {
      x: cx - r, y: cy - r, w: r * 2, h: r * 2,
      fill: { type: "none" },
      line: { color, width: lineW, transparency: 55 },
    });
  });
  slide.addShape("ellipse", {
    x: cx - 0.06, y: cy - 0.06, w: 0.12, h: 0.12,
    fill: { color }, line: { type: "none" },
  });
}

(async () => {
  const icons = {};
  for (const s of SECTIONS) {
    if (!icons[s.icon]) {
      icons[s.icon] = {
        white: await iconPng(s.icon, WHITE),
        orange: await iconPng(s.icon, ORANGE),
      };
    }
  }
  const bullseyeWhite = await iconPng("FaBullseye", ORANGE);

  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5

  // ---------- Slide 1: Title ----------
  {
    const s = pres.addSlide();
    s.background = { color: DARK };
    targetRings(s, 11.1, 3.75, 2.9, ORANGE, 1.5);
    s.addImage({ data: bullseyeWhite, x: 0.75, y: 1.25, w: 0.85, h: 0.85 });
    s.addText("სასროლეთის მენეჯმენტი", {
      x: 0.7, y: 2.35, w: 8.6, h: 1.6, fontFace: FONT, fontSize: 44, bold: true,
      color: WHITE, align: "left", margin: 0,
    });
    s.addText("მართვის სრული სისტემა — 14 ძირითადი მიმართულება", {
      x: 0.72, y: 3.85, w: 7.6, h: 0.6, fontFace: FONT, fontSize: 18,
      color: "C9CDD2", align: "left", margin: 0,
    });
    s.addText([
      { text: "უსაფრთხოება", options: { color: ORANGE, bold: true } },
      { text: "  ·  ოპერაციები  ·  სწავლება  ·  სპორტი  ·  განვითარება", options: { color: "9AA0A6" } },
    ], {
      x: 0.72, y: 6.5, w: 8.5, h: 0.4, fontFace: FONT, fontSize: 13, align: "left", margin: 0,
    });
  }

  // ---------- Slide 2: Overview ----------
  {
    const s = pres.addSlide();
    s.background = { color: WHITE };
    s.addText("სტრუქტურის მიმოხილვა", {
      x: 0.6, y: 0.42, w: 9.0, h: 0.65, fontFace: FONT, fontSize: 30, bold: true, color: TEXT, margin: 0,
    });
    s.addText("14 მიმართულება, ერთი სისტემა", {
      x: 0.6, y: 1.06, w: 9.0, h: 0.4, fontFace: FONT, fontSize: 13, color: MUTED, margin: 0,
    });
    const cols = 4, gw = 0.18, gh = 0.18;
    const x0 = 0.6, y0 = 1.68;
    const tw = (13.33 - 1.2 - (cols - 1) * gw) / cols; // ~2.9
    const th = (7.5 - y0 - 0.45 - 3 * gh) / 4; // 4 rows
    SECTIONS.forEach((sec, i) => {
      const r = Math.floor(i / cols), c = i % cols;
      const x = x0 + c * (tw + gw), y = y0 + r * (th + gh);
      s.addShape("roundRect", {
        x, y, w: tw, h: th, rectRadius: 0.06,
        fill: { color: CARD }, line: { type: "none" },
      });
      s.addShape("ellipse", {
        x: x + 0.16, y: y + (th - 0.5) / 2, w: 0.5, h: 0.5,
        fill: { color: DARK }, line: { type: "none" },
      });
      s.addImage({ data: icons[sec.icon].white, x: x + 0.285, y: y + (th - 0.5) / 2 + 0.125, w: 0.25, h: 0.25 });
      s.addText(sec.n, {
        x: x + 0.78, y: y + 0.13, w: tw - 0.9, h: 0.3, fontFace: FONT, fontSize: 11, bold: true, color: ORANGE, margin: 0,
      });
      s.addText(sec.title, {
        x: x + 0.78, y: y + 0.4, w: tw - 0.9, h: th - 0.5, fontFace: FONT, fontSize: 12.5, bold: true, color: TEXT, margin: 0, valign: "top",
      });
    });
  }

  // ---------- Content slides ----------
  SECTIONS.forEach((sec, si) => {
    const dark = si === SECTIONS.length - 1; // closing slide dark
    const s = pres.addSlide();
    s.background = { color: dark ? DARK : WHITE };
    const tcol = dark ? WHITE : TEXT;
    const mcol = dark ? "AEB4BA" : MUTED;
    const cardFill = dark ? DARK2 : CARD;

    // header
    s.addShape("ellipse", {
      x: 0.6, y: 0.5, w: 0.78, h: 0.78, fill: { color: ORANGE }, line: { type: "none" },
    });
    s.addImage({ data: icons[sec.icon].white, x: 0.6 + 0.2, y: 0.5 + 0.2, w: 0.38, h: 0.38 });
    s.addText([
      { text: sec.n + "  ", options: { color: ORANGE, bold: true } },
      { text: sec.title, options: { color: tcol, bold: true } },
    ], {
      x: 1.6, y: 0.42, w: 9.6, h: 0.62, fontFace: FONT, fontSize: 29, margin: 0, valign: "middle",
    });
    s.addText(sec.desc, {
      x: 1.62, y: 1.06, w: 9.8, h: 0.38, fontFace: FONT, fontSize: 12.5, color: mcol, margin: 0, valign: "middle",
    });
    s.addText(sec.n + " / 14", {
      x: 11.7, y: 0.5, w: 1.05, h: 0.35, fontFace: FONT, fontSize: 11, bold: true, color: mcol, align: "right", margin: 0,
    });

    const items = sec.items;
    const useCards = si % 2 === 0; // alternate layouts
    const x0 = 0.6, y0 = 1.72, availH = 7.5 - y0 - 0.42;
    const cols = 2, gw = 0.22;
    const cw = (13.33 - 1.2 - gw) / 2; // ~5.955
    const rows = Math.ceil(items.length / cols);
    const gh = 0.16;
    const ch = (availH - (rows - 1) * gh) / rows;

    items.forEach((it, i) => {
      // column-major fill so left column fills first
      const c = Math.floor(i / rows), r = i % rows;
      const x = x0 + c * (cw + gw), y = y0 + r * (ch + gh);
      if (useCards) {
        s.addShape("roundRect", {
          x, y, w: cw, h: ch, rectRadius: 0.05,
          fill: { color: cardFill }, line: { type: "none" },
        });
      } else {
        s.addShape("line", {
          x, y: y + ch, w: cw, h: 0,
          line: { color: dark ? "3C434A" : "E3E5E8", width: 1 },
        });
      }
      const pad = useCards ? 0.24 : 0.05;
      s.addShape("ellipse", {
        x: x + pad, y: y + ch / 2 - 0.055, w: 0.11, h: 0.11,
        fill: { color: ORANGE }, line: { type: "none" },
      });
      const txX = x + pad + 0.28;
      const txW = cw - pad - 0.28 - 0.15;
      const runs = [{ text: it.m, options: { fontSize: 14.5, bold: true, color: tcol, breakLine: true } }];
      if (it.s) runs.push({ text: it.s, options: { fontSize: 10.5, color: mcol } });
      s.addText(runs, {
        x: txX, y, w: txW, h: ch,
        fontFace: FONT, margin: 0, valign: "middle", align: "left",
        lineSpacingMultiple: 1.12,
      });
    });

    if (dark) {
      targetRings(s, 13.05, 7.35, 1.05, ORANGE, 1.2);
    }
  });

  await pres.writeFile({ fileName: "sasroleti-management.pptx" });
  console.log("written");
})().catch((e) => { console.error(e); process.exit(1); });
