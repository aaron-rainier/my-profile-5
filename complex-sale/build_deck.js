const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";            // 13.333 x 7.5
pres.author = "M2 NDC — EMLV";
pres.title  = "The ABP Project — Complex Sales";

// ---------- palette ----------
const BG    = "0B2B33";
const CARD  = "123C48";
const TINT  = "0E3641";
const WHITE = "FFFFFF";
const ICE   = "C9E2E8";
const MUTED = "8FB4BE";
const AMBER = "F2A33C";
const CORAL = "F0736C";
const MINT  = "5AD9B3";

const HEAD = "Cambria";
const BODY = "Calibri";

// ---------- helpers ----------
function card(slide, x, y, w, h, fill) {
  slide.addShape(pres.ShapeType.roundRect, {
    x, y, w, h, rectRadius: 0.09,
    fill: { color: fill || CARD }, line: { color: fill || CARD, width: 0 }
  });
}

function chip(slide, n, x, y) {
  slide.addShape(pres.ShapeType.ellipse, {
    x, y, w: 0.32, h: 0.32, fill: { color: AMBER }, line: { color: AMBER, width: 0 }
  });
  slide.addText(String(n), {
    x, y, w: 0.32, h: 0.32, isTextBox: true, margin: 0,
    align: "center", valign: "middle", fontFace: BODY, fontSize: 13, bold: true, color: BG
  });
}

function blockHead(slide, n, title, secs, x, y, titleW) {
  chip(slide, n, x, y);
  slide.addText(title, {
    x: x + 0.44, y: y - 0.02, w: titleW, h: 0.36, isTextBox: true, margin: 0,
    valign: "middle", fontFace: HEAD, fontSize: 14.5, bold: true, color: WHITE
  });
  slide.addText(secs, {
    x: x + 0.48 + titleW, y: y - 0.02, w: 0.60, h: 0.36, isTextBox: true, margin: 0,
    valign: "middle", align: "left", fontFace: BODY, fontSize: 9.5, color: MUTED
  });
}

function label(slide, txt, x, y, w, color) {
  slide.addText(txt, {
    x, y, w, h: 0.18, isTextBox: true, margin: 0, valign: "middle",
    fontFace: BODY, fontSize: 8.5, bold: true, charSpacing: 0.9, color: color || AMBER
  });
}

function bullets(slide, items, x, y, w, h, size, italic) {
  const runs = items.map((t, i) => ({
    text: t,
    options: { bullet: { indent: 12 }, breakLine: i !== items.length - 1 }
  }));
  slide.addText(runs, {
    x, y, w, h, isTextBox: true, margin: 0, valign: "top",
    fontFace: BODY, fontSize: size || 10.5, color: ICE, italic: !!italic,
    lineSpacingMultiple: 1.03, paraSpaceAfter: 5
  });
}

function para(slide, lead, rest, x, y, w, h, size, leadColor) {
  slide.addText([
    { text: lead, options: { bold: true, color: leadColor || AMBER } },
    { text: rest, options: { color: ICE } }
  ], {
    x, y, w, h, isTextBox: true, margin: 0, valign: "top",
    fontFace: BODY, fontSize: size || 10, lineSpacingMultiple: 1.03
  });
}

function slideFrame(slide, title, kicker, tag, num) {
  slide.background = { color: BG };
  slide.addText(title, {
    x: 0.55, y: 0.28, w: 8.2, h: 0.48, isTextBox: true, margin: 0, valign: "middle",
    fontFace: HEAD, fontSize: 27, bold: true, color: WHITE
  });
  slide.addText(kicker, {
    x: 0.56, y: 0.76, w: 8.2, h: 0.26, isTextBox: true, margin: 0, valign: "middle",
    fontFace: BODY, fontSize: 10.5, color: MUTED
  });
  slide.addText(tag, {
    x: 8.9, y: 0.30, w: 3.9, h: 0.24, isTextBox: true, margin: 0, align: "right", valign: "middle",
    fontFace: BODY, fontSize: 8.5, bold: true, charSpacing: 0.8, color: AMBER
  });
  slide.addText("MERIDIAN COLD CHAIN SOLUTIONS  ·  M2 NDC, EMLV  ·  " + num,
    { x: 8.9, y: 0.58, w: 3.9, h: 0.24, isTextBox: true, margin: 0, align: "right", valign: "middle",
      fontFace: BODY, fontSize: 8, color: MUTED });
}

/* ==========================================================================
   SLIDE 1 — reading the field  (speakers 1-3)
   ========================================================================== */
const s1 = pres.addSlide();
slideFrame(s1, "The ABP Project", "€ 78 m · 60,000 coolers · and the RFP has not been written yet",
  "TASKS 1 & 2  ·  COMPETITOR ANALYSIS AND APPROACH", "1 / 2");

const statX = [8.92, 10.30, 11.68];
const statVals = [["70 %", "of the estate is Frostline’s"], ["3 wks", "since we heard of it"], ["8–10", "weeks left to shape it"]];
statVals.forEach((sv, i) => {
  s1.addText(sv[0], { x: statX[i], y: 0.86, w: 1.28, h: 0.32, isTextBox: true, margin: 0,
    fontFace: HEAD, fontSize: 17, bold: true, color: AMBER, align: "right" });
  s1.addText(sv[1], { x: statX[i], y: 1.16, w: 1.28, h: 0.30, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 7.5, color: MUTED, align: "right", lineSpacingMultiple: 0.95 });
});

const TOP = 1.52, CH = 5.52;   // cards 1.52 -> 7.04

// ---- column 1 : where we stand
card(s1, 0.55, TOP, 3.55, CH);
blockHead(s1, 1, "WHERE WE STAND", "45 s", 0.75, TOP + 0.18, 2.30);
bullets(s1, [
  "Frostline: 22 years, ~70 % of the estate, the lowest unit price.",
  "Meridian: one 900-unit pilot. Nothing above middle management.",
  "We heard about the programme three weeks ago, second-hand."
], 0.75, TOP + 0.70, 3.15, 1.35, 10.5);

card(s1, 0.75, TOP + 2.16, 3.15, 1.06, TINT);
label(s1, "WHAT FORCED THE DECISION", 0.92, TOP + 2.29, 2.81, MINT);
s1.addText("The F-gas phase-down and a published 2030 emissions target. Neither is about coolers.",
  { x: 0.92, y: TOP + 2.51, w: 2.81, h: 0.60, isTextBox: true, margin: 0, fontFace: BODY,
    fontSize: 10, color: ICE, lineSpacingMultiple: 1.03 });

card(s1, 0.75, TOP + 3.38, 3.15, 1.26, TINT);
s1.addText([
  { text: "The tender is not the contest.", options: { color: AMBER, bold: true, fontSize: 12.5, breakLine: true } },
  { text: "The eight weeks before it is. After the RFP is issued, we are answering someone else’s document.", options: { color: ICE, fontSize: 10, italic: true } }
], { x: 0.92, y: TOP + 3.52, w: 2.81, h: 0.98, isTextBox: true, margin: 0,
     fontFace: BODY, lineSpacingMultiple: 1.06 });

label(s1, "SO WE ARE NOT SELLING AGAINST A COMPETITOR", 0.75, TOP + 4.82, 3.15, CORAL);
s1.addText("An arrangement that works — and 400 technicians who have never had a reason to question it.",
  { x: 0.75, y: TOP + 5.04, w: 3.15, h: 0.38, isTextBox: true, margin: 0, fontFace: BODY,
    fontSize: 9.5, color: ICE, lineSpacingMultiple: 1.03 });

// ---- column 2 : battle card
card(s1, 4.35, TOP, 4.35, CH);
blockHead(s1, 2, "BATTLE CARD  ·  FROSTLINE", "75 s", 4.55, TOP + 0.18, 3.35);

s1.addText([
  { text: "Their pitch:  ", options: { bold: true, color: AMBER } },
  { text: "“Continuity at the lowest cost.”", options: { color: ICE, italic: true } }
], { x: 4.55, y: TOP + 0.70, w: 3.95, h: 0.22, isTextBox: true, margin: 0,
     fontFace: BODY, fontSize: 9.5, lineSpacingMultiple: 1.03 });

label(s1, "TWO STRONGEST CLAIMS", 4.55, TOP + 1.00, 3.95, MINT);
bullets(s1, [
  "Cheapest, and already integrated with ABP’s maintenance scheduling.",
  "Proven at 48,000-outlet scale without stopping chilled sales."
], 4.55, TOP + 1.22, 3.95, 0.80, 10);

label(s1, "TWO REAL VULNERABILITIES", 4.55, TOP + 2.13, 3.95, CORAL);
bullets(s1, [
  "Two of their three refrigerant platforms are hit by F-gas.",
  "No telemetry beyond an alarm contact — and no contact above Rousseau in four years."
], 4.55, TOP + 2.35, 3.95, 0.80, 10);

label(s1, "THREE DISCOVERY QUESTIONS — WITHOUT NAMING THE WEAKNESS", 4.55, TOP + 3.26, 3.95, AMBER);
bullets(s1, [
  "“Which platform will the year-four units sit on — and who pays if it is restricted?”",
  "“How do you find out a cooler has failed, and how long is it down?”",
  "“How will compliance be weighted against price — and who decides that?”"
], 4.55, TOP + 3.48, 3.95, 1.30, 10, true);

label(s1, "THE PROOF POINT WE MUST HAVE", 4.55, TOP + 4.84, 3.95, MINT);
s1.addText("Audited uptime from our own Portugal estate, checked against ABP’s own service records.",
  { x: 4.55, y: TOP + 5.06, w: 3.95, h: 0.40, isTextBox: true, margin: 0, fontFace: BODY,
    fontSize: 10, color: ICE, lineSpacingMultiple: 1.02 });

// ---- column 3 : four corners + approach
card(s1, 8.95, TOP, 3.85, CH);
blockHead(s1, 3, "FOUR CORNERS", "70 s", 9.15, TOP + 0.18, 1.95);

label(s1, "WHAT FROSTLINE ASSUMES", 9.15, TOP + 0.70, 3.45, AMBER);
bullets(s1, [
  "Field operations decide, and price won in 2019.",
  "ABP is buying coolers, not data."
], 9.15, TOP + 0.92, 3.45, 0.72, 10.5);

label(s1, "WHY THAT IS WRONG", 9.15, TOP + 1.72, 3.45, CORAL);
bullets(s1, [
  "Regulation and a board target forced this — not equipment failure.",
  "The people who forced it, Frostline has not met in four years."
], 9.15, TOP + 1.94, 3.45, 0.92, 10.5);

card(s1, 9.15, TOP + 2.98, 3.45, 1.30, TINT);
s1.addText("OUR APPROACH  ·  DISRUPTION", { x: 9.32, y: TOP + 3.10, w: 3.11, h: 0.26, isTextBox: true,
  margin: 0, fontFace: HEAD, fontSize: 13, bold: true, color: AMBER });
s1.addText("We cannot win on today’s criteria, so we change them before they are written: from unit price to five-year, compliance-adjusted cost per outlet-day.",
  { x: 9.32, y: TOP + 3.40, w: 3.11, h: 0.76, isTextBox: true, margin: 0, fontFace: BODY,
    fontSize: 9.5, color: ICE, lineSpacingMultiple: 1.03 });

label(s1, "WE ARE WRONG IF", 9.15, TOP + 4.44, 3.45, CORAL);
s1.addText("The evaluation basis is already fixed on unit price. Then we stop reframing and segment: bid the 20,000 highest-failure outlets where we own the engineers.",
  { x: 9.15, y: TOP + 4.66, w: 3.45, h: 0.80, isTextBox: true, margin: 0, fontFace: BODY,
    fontSize: 9.5, color: ICE, lineSpacingMultiple: 1.03 });

s1.addNotes(
"7 minutes, 6 speakers. Slide 1 = speakers 1-3 (about 3:10). Everything below is spoken, not written on the slide.\n\n" +
"SPEAKER 1 (45s) - WHERE WE STAND. We are Meridian, account director on a 78 million euro programme: 60,000 coolers replaced over five years, plus telemetry. Frostline has held this estate for twenty-two years and seventy per cent of it, at the lowest unit price in the market. We have one 900-unit pilot in Portugal from 2021, rated good - and no relationship above middle management. Our last meeting was seven months ago; we heard about the programme three weeks ago, and we heard it second-hand, from a consultancy. Now the important part: two things forced this decision at the same time - the F-gas phase-down and a published 2030 emissions target the group cannot reach on its current estate. Neither of them is about coolers. Which is why the tender is not the contest: the eight weeks before it is. After the RFP is issued we are answering someone else's document, and we are not selling against a competitor - we are selling against an arrangement that works.\n\n" +
"SPEAKER 2 (75s) - BATTLE CARD, FROSTLINE. Their pitch will be continuity at the lowest cost, and it is a strong pitch. Two claims we cannot dismiss: they are the cheapest and they are already inside ABP's maintenance scheduling, so they are also the least disruptive; and they are the only bidder who has actually moved units across 48,000 outlets without stopping the sale of chilled product. But two real vulnerabilities. First, two of their three refrigerant platforms are hit by the F-gas phase-down - over a five-year rollout the safe bid is the one carrying regulatory and residual-value risk. Second, they have no telemetry beyond a basic alarm contact, and their account team has not met anyone above Rousseau in four years. We do not name either weakness. We ask three questions and let ABP find them: which platform will the year-four units sit on and who pays if it is restricted; how do you find out today that a cooler has failed and how long is it down; and how will compliance be weighted against price, and who decides that weighting. None of this lands without one proof point: audited uptime and lost-volume data from our own Portugal estate, cross-checked against ABP's own service records.\n\n" +
"SPEAKER 3 (70s) - FOUR CORNERS AND OUR APPROACH. Porter's harder question is not what a competitor can do, it is what they assume. Frostline assumes field operations decide, and that price won in 2019 so price wins in 2026. And they assume ABP is buying coolers, not data. Both assumptions are wrong, for the same reason: this decision was not triggered by equipment failure, it was triggered by regulation and a board-level emissions target - and the people who forced it are people Frostline has not met in four years. Twenty-two years of winning is exactly why they will not see it coming. So our approach is disruption. Not domination - we have never won an estate this size. Not blocking - we are not the incumbent. We change the criteria before they are written: from lowest unit price to five-year, compliance-adjusted cost per outlet-day of availability. And we say what would make us wrong: if Beck and Marchand have already fixed the evaluation on unit price, or if Diallo's mandate carries no weight in the scoring, then reframing burns eight weeks. In that case we segment and bid a carve-out - the 20,000 highest-failure outlets in the countries where we own the engineers."
);

/* ==========================================================================
   SLIDE 2 — winning the field  (speakers 4-6)
   ========================================================================== */
const s2 = pres.addSlide();
slideFrame(s2, "Who actually decides — and the eight weeks",
  "Ten people, six votes, one document — and only one of them writes it",
  "TASKS 3, 4 & 5  ·  BUYING CENTRE, MENTOR, PLAN", "2 / 2");

const T2 = 1.30, H2 = 3.60;   // top row 1.30 -> 4.90

// ---- buying centre
card(s2, 0.55, T2, 7.05, H2);
blockHead(s2, 4, "THE BUYING CENTRE", "70 s", 0.75, T2 + 0.15, 2.70);

s2.addText("POWER →", { x: 0.08, y: 2.78, w: 1.60, h: 0.24, isTextBox: true, margin: 0,
  rotate: 270, align: "center", valign: "middle", fontFace: BODY, fontSize: 8, bold: true,
  charSpacing: 0.8, color: MUTED });

const QX = [1.10, 4.35], QY = [1.82, 2.90], QW = 3.05, QH = 0.99;
const quads = [
  [0, 0, "HIGH POWER  ·  LOW INTEREST", CORAL, [
    ["Marchand", " — chairs it; chose Frostline in 2019"],
    ["Rousseau", " — 400 technicians; “it works fine”"],
    ["Fontaine", " — signs once, at the very end"]
  ]],
  [1, 0, "HIGH POWER  ·  HIGH INTEREST", MINT, [
    ["Beck", " — owns the budget, no view yet"],
    ["Diallo", " — board mandate; no budget, no vote"],
    ["Sanchez", " — writes the RFP and the bidder list"]
  ]],
  [0, 1, "LOW POWER  ·  LOW INTEREST", MUTED, [
    ["Haddad", " — data terms; a late veto"],
    ["Franchisor", " — no vote, absolute veto"]
  ]],
  [1, 1, "LOW POWER  ·  HIGH INTEREST", AMBER, [
    ["Kovač", " — pilot budget only; 14 months in"],
    ["Lefebvre", " — the Friday-in-July problem"]
  ]]
];
quads.forEach(q => {
  const x = QX[q[0]], y = QY[q[1]];
  card(s2, x, y, QW, QH, TINT);
  s2.addText(q[2], { x: x + 0.14, y: y + 0.08, w: QW - 0.28, h: 0.16, isTextBox: true, margin: 0,
    valign: "middle", fontFace: BODY, fontSize: 7.5, bold: true, charSpacing: 0.6, color: q[3] });
  const runs = [];
  q[4].forEach((p, i) => {
    runs.push({ text: p[0], options: { bold: true, color: WHITE } });
    runs.push({ text: p[1], options: { color: ICE, breakLine: i !== q[4].length - 1 } });
  });
  s2.addText(runs, { x: x + 0.14, y: y + 0.28, w: QW - 0.28, h: QH - 0.36, isTextBox: true,
    margin: 0, valign: "top", fontFace: BODY, fontSize: 9, lineSpacingMultiple: 1.04, paraSpaceAfter: 2 });
});

s2.addText("INTEREST IN CHANGING THE CURRENT ARRANGEMENT →",
  { x: 1.10, y: 3.96, w: 6.30, h: 0.18, isTextBox: true, margin: 0, align: "center", valign: "middle",
    fontFace: BODY, fontSize: 8, bold: true, charSpacing: 0.8, color: MUTED });

label(s2, "WHERE THE ORG CHART AND THE MAP DISAGREE", 0.75, 4.24, 6.65, AMBER);
s2.addText([
  { text: "Sanchez", options: { bold: true, color: WHITE } },
  { text: " writes the requirement, four levels down.   ", options: { color: ICE } },
  { text: "Rousseau", options: { bold: true, color: WHITE } },
  { text: " has no budget and can still kill the winner.   ", options: { color: ICE } },
  { text: "Diallo", options: { bold: true, color: WHITE } },
  { text: " has no vote and is the reason the programme exists.", options: { color: ICE } }
], { x: 0.75, y: 4.46, w: 6.65, h: 0.34, isTextBox: true, margin: 0, valign: "top",
     fontFace: BODY, fontSize: 9.5, lineSpacingMultiple: 1.03 });

// ---- mentor
card(s2, 7.80, T2, 5.00, H2);
blockHead(s2, 5, "OUR MENTOR", "70 s", 8.00, T2 + 0.15, 1.70);

s2.addText([
  { text: "AMARA DIALLO", options: { bold: true, color: AMBER, fontSize: 14, fontFace: HEAD } },
  { text: "   Sustainability & ESG", options: { color: MUTED, fontSize: 9.5, fontFace: BODY } }
], { x: 8.00, y: T2 + 0.62, w: 4.60, h: 0.28, isTextBox: true, margin: 0, valign: "middle" });

para(s2, "Wants, cannot get — ",
  "a costed path to the 2030 target. She owns the outcome and holds no budget and no vote.",
  8.00, T2 + 0.96, 4.60, 0.40, 10);
para(s2, "We ask for — ",
  "two criteria in the document: refrigerant compliance and measured emissions. And an introduction to Beck.",
  8.00, T2 + 1.42, 4.60, 0.40, 10);
para(s2, "We give — ",
  "an F-gas cost model she tables in her own name.",
  8.00, T2 + 1.88, 4.60, 0.24, 10);

card(s2, 8.00, T2 + 2.24, 4.60, 1.26, TINT);
label(s2, "LOOKS LIKE A MENTOR AND IS NOT  ·  ELENA KOVAČ", 8.16, T2 + 2.36, 4.28, CORAL);
s2.addText([
  { text: "Pilot budget only, 14 months in, and she has never raised telemetry with procurement.", options: { color: ICE, breakLine: true } },
  { text: "The test: a mentor puts the requirements to Sanchez in writing. A fan gives you a meeting.", options: { color: WHITE, italic: true } }
], { x: 8.16, y: T2 + 2.58, w: 4.28, h: 0.84, isTextBox: true, margin: 0, valign: "top",
     fontFace: BODY, fontSize: 9.5, lineSpacingMultiple: 1.04, paraSpaceAfter: 4 });

// ---- eight weeks
card(s2, 0.55, 5.04, 12.25, 2.00);
blockHead(s2, 6, "THE EIGHT WEEKS BEFORE THE RFP", "70 s", 0.75, 5.12, 3.85);
s2.addText("Anything that does not change the document is time we have to justify.",
  { x: 7.20, y: 5.10, w: 5.40, h: 0.30, isTextBox: true, margin: 0, align: "right", valign: "middle",
    fontFace: BODY, fontSize: 9, italic: true, color: MUTED });

const steps = [
  ["1", "WEEKS 1–2", "Diallo first", "Build the F-gas cost-of-inaction model, in her name.", "→ MAKES COMPLIANCE A SCORED CRITERION", MINT],
  ["2", "WEEKS 2–3", "Test Kovač, then use her", "Co-author the data spec: open API, door-open events.", "→ WRITES IN WHAT AN ALARM CONTACT CANNOT MEET", MINT],
  ["3", "WEEKS 3–5", "Neutralise Rousseau", "His technicians, our uptime record, on his terms.", "→ CHANGES NO TEXT — IT PROTECTS THE OTHER FOUR", CORAL],
  ["4", "WEEKS 4–6", "Re-base Beck’s economics", "Cost per outlet-day over five years, not price per unit.", "→ MOVES THE EVALUATION TO FIVE-YEAR COST", MINT],
  ["5", "WEEKS 6–8", "Sanchez, and Haddad early", "Bidder list, Q&A rules, data terms before Legal blocks.", "→ THE TEXT, THE WEIGHTS, AND WHO ANSWERS", MINT]
];
steps.forEach((st, i) => {
  const x = 0.75 + i * 2.40;
  s2.addText(st[0], { x, y: 5.50, w: 0.28, h: 0.26, isTextBox: true, margin: 0, valign: "middle",
    fontFace: HEAD, fontSize: 16, bold: true, color: AMBER });
  s2.addText(st[1], { x: x + 0.32, y: 5.50, w: 1.93, h: 0.26, isTextBox: true, margin: 0, valign: "middle",
    fontFace: BODY, fontSize: 8, bold: true, charSpacing: 0.6, color: MUTED });
  s2.addText(st[2], { x, y: 5.80, w: 2.25, h: 0.24, isTextBox: true, margin: 0, valign: "middle",
    fontFace: BODY, fontSize: 10.5, bold: true, color: WHITE });
  s2.addText(st[3], { x, y: 6.08, w: 2.25, h: 0.50, isTextBox: true, margin: 0, valign: "top",
    fontFace: BODY, fontSize: 9, color: ICE, lineSpacingMultiple: 1.03 });
  s2.addText(st[4], { x, y: 6.62, w: 2.25, h: 0.32, isTextBox: true, margin: 0, valign: "top",
    fontFace: BODY, fontSize: 7.5, bold: true, color: st[5], lineSpacingMultiple: 1.0 });
});

s2.addText("Porter (1980) · Chen (1996) · Zahra & Chaples (1993) · Webster & Wind (1972) · Kohli (1989) · Ronchetto, Hutt & Reingen (1989) · Mitchell, Agle & Wood (1997)",
  { x: 0.55, y: 7.12, w: 12.25, h: 0.22, isTextBox: true, margin: 0, valign: "middle",
    fontFace: BODY, fontSize: 7, color: MUTED });

s2.addNotes(
"Slide 2 = speakers 4-6 (about 3:30). Everything below is spoken, not written on the slide.\n\n" +
"SPEAKER 4 (70s) - THE BUYING CENTRE. The evaluation committee has six formal members, but there are ten people on this map - because the committee is not the buying centre. Power on one axis, interest in CHANGING the current arrangement on the other. Top left, powerful and with no reason to change: Marchand chairs the committee and ran the 2019 tender that awarded Frostline - change means her own decision was wrong - and she is publicly committed to six per cent annual cost reduction. Rousseau has 400 technicians and says openly that the estate works fine. Fontaine signs once, at the end. Top right, powerful and open to change: Beck owns the budget and has not yet formed a view - he is the prize. Diallo carries a board-level, non-negotiable mandate. Sanchez writes the document. Bottom right, high interest and little power: Kovac has a pilot budget, Lefebvre has the Friday-in-July problem and is our best source of evidence. Bottom left, the two late vetoes: Haddad on telemetry data terms, and the franchisor, who is not on the org chart at all and can veto anything touching how the cooler looks. Three places the org chart is simply wrong: Sanchez sits four levels down and writes the requirement - process power beats position. Rousseau has no budget authority and can still kill the winner during evaluation. And Diallo has no vote and no budget, and she is the reason the programme exists.\n\n" +
"SPEAKER 5 (70s) - THE MENTOR. Amara Diallo. What she wants and cannot currently get: a costed, credible path to the 2030 target and the F-gas transition. She owns the outcome and holds neither budget nor vote. And note the detail in the case: she presented the F-gas plan to the board in January. Beck was in the room. Marchand was not. The person chairing the evaluation was absent for the reason the programme exists - that gap is our opening. We ask her for two things: the two criteria that must appear in the document, and an introduction to Beck. We give her something she can use internally - an estate-level F-gas and emissions cost model she tables in her own name, not ours. Now the trap. Kovac looks exactly like a mentor: enthusiastic, technical, already building a telemetry business case, and she will take every meeting we offer. But she is fourteen months in, has budget for a pilot and not for a rollout, and has twice asked her own IT team about joining cooler data to outlet sales without ever raising it with procurement. Enthusiasm is not influence. So we test her: we ask her to spend capital, not time. Will you put the telemetry requirements to Sanchez in writing and co-sign them? A mentor spends internal capital. A fan gives you a meeting.\n\n" +
"SPEAKER 6 (70s) - THE EIGHT WEEKS. Five moves, in order. One, Diallo: build the F-gas and cost-of-inaction model in her name, which makes compliance and emissions scored criteria rather than preferences. Two, test Kovac and then co-author the data specification - open API, door-open events, outlet-level sales join - which writes in requirements a basic alarm contact cannot meet. Three, neutralise Rousseau: not a pitch, his own technicians reading our Portugal uptime data on his terms. This one changes nothing in the document, and the case asks us to justify that: without Rousseau neutral, the user buyer kills the winner during evaluation, so this move protects the value of the other four. Four, re-base Beck's economics onto cost per outlet-day of availability over five years, which moves the evaluation off unit price and disarms Frostline's strongest claim. Five, Sanchez and Haddad: the bidder list, the Q&A rules, and a data-processing annex offered before Legal is ever asked to block. Four of the five change the document. And the test of the whole plan is simple - if we are still explaining our telemetry to Sanchez in week nine, we have already lost."
);

pres.writeFile({ fileName: "The_ABP_Project_Meridian.pptx" }).then(f => console.log("wrote", f));
