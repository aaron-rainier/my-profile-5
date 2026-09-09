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
const ICE   = "C3DDE3";
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
    x, y, w: 0.30, h: 0.30, fill: { color: AMBER }, line: { color: AMBER, width: 0 }
  });
  slide.addText(String(n), {
    x, y, w: 0.30, h: 0.30, isTextBox: true, margin: 0,
    align: "center", valign: "middle", fontFace: BODY, fontSize: 12, bold: true, color: BG
  });
}

function blockHead(slide, n, title, secs, x, y, titleW) {
  chip(slide, n, x, y);
  slide.addText(title, {
    x: x + 0.40, y: y - 0.02, w: titleW, h: 0.34, isTextBox: true, margin: 0,
    valign: "middle", fontFace: HEAD, fontSize: 13.5, bold: true, color: WHITE
  });
  slide.addText(secs, {
    x: x + 0.44 + titleW, y: y - 0.02, w: 0.55, h: 0.34, isTextBox: true, margin: 0,
    valign: "middle", align: "left", fontFace: BODY, fontSize: 9, color: MUTED
  });
}

function label(slide, txt, x, y, w, color) {
  slide.addText(txt, {
    x, y, w, h: 0.17, isTextBox: true, margin: 0, valign: "middle",
    fontFace: BODY, fontSize: 8, bold: true, charSpacing: 0.8, color: color || AMBER
  });
}

function bullets(slide, items, x, y, w, h, size) {
  const runs = items.map((t, i) => ({
    text: t,
    options: { bullet: { indent: 11 }, breakLine: i !== items.length - 1 }
  }));
  slide.addText(runs, {
    x, y, w, h, isTextBox: true, margin: 0, valign: "top",
    fontFace: BODY, fontSize: size || 9.5, color: ICE,
    lineSpacingMultiple: 1.02, paraSpaceAfter: 4
  });
}

function para(slide, lead, rest, x, y, w, h, size, leadColor) {
  slide.addText([
    { text: lead, options: { bold: true, color: leadColor || AMBER } },
    { text: rest, options: { color: ICE } }
  ], {
    x, y, w, h, isTextBox: true, margin: 0, valign: "top",
    fontFace: BODY, fontSize: size || 9, lineSpacingMultiple: 1.03
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
    fontFace: BODY, fontSize: 10, color: MUTED
  });
  slide.addText(tag, {
    x: 8.9, y: 0.30, w: 3.9, h: 0.24, isTextBox: true, margin: 0, align: "right", valign: "middle",
    fontFace: BODY, fontSize: 8.5, bold: true, charSpacing: 0.8, color: AMBER
  });
  slide.addText("MERIDIAN COLD CHAIN SOLUTIONS  ·  COMPLEX SALES, LESSON 2  ·  M2 NDC, EMLV  ·  " + num,
    { x: 8.9, y: 0.58, w: 3.9, h: 0.24, isTextBox: true, margin: 0, align: "right", valign: "middle",
      fontFace: BODY, fontSize: 7.5, color: MUTED });
}

/* ==========================================================================
   SLIDE 1 — reading the field  (speakers 1-3)
   ========================================================================== */
const s1 = pres.addSlide();
slideFrame(s1, "The ABP Project", "€ 78 m · 60,000 coolers · five years · the RFP has not been written yet",
  "TASKS 1 & 2  ·  COMPETITOR ANALYSIS AND APPROACH", "1 / 2");

const statX = [8.92, 10.30, 11.68];
const statVals = [["70 %", "of the estate is Frostline’s"], ["3 wks", "since we heard, second-hand"], ["8–10", "weeks left to shape it"]];
statVals.forEach((sv, i) => {
  s1.addText(sv[0], { x: statX[i], y: 0.88, w: 1.28, h: 0.30, isTextBox: true, margin: 0,
    fontFace: HEAD, fontSize: 16, bold: true, color: AMBER, align: "right" });
  s1.addText(sv[1], { x: statX[i], y: 1.16, w: 1.28, h: 0.30, isTextBox: true, margin: 0,
    fontFace: BODY, fontSize: 7, color: MUTED, align: "right", lineSpacingMultiple: 0.95 });
});

const TOP = 1.52, CH = 5.52;   // cards 1.52 -> 7.04

// ---- column 1 : where we stand
card(s1, 0.55, TOP, 3.55, CH);
blockHead(s1, 1, "WHERE WE STAND", "45 s", 0.75, TOP + 0.16, 2.15);
bullets(s1, [
  "Frostline: incumbent since 2004, ~70 % of the estate, lowest unit price in the market.",
  "Meridian: one 900-unit pilot, Portugal 2021, rated “good”. No relationship above middle management.",
  "Last meeting seven months ago. We heard about the programme three weeks ago, from a consultancy."
], 0.75, TOP + 0.60, 3.15, 1.32, 9.5);

label(s1, "WHAT ACTUALLY FORCED THE DECISION", 0.75, TOP + 2.00, 3.15, MINT);
s1.addText("Not equipment failure. The F-gas phase-down (EU 2024/573) and a published 2030 emissions target — approved by the executive committee in March.",
  { x: 0.75, y: TOP + 2.20, w: 3.15, h: 0.70, isTextBox: true, margin: 0, fontFace: BODY,
    fontSize: 9, color: ICE, lineSpacingMultiple: 1.03 });

card(s1, 0.75, TOP + 3.10, 3.15, 1.12, TINT);
s1.addText([
  { text: "The tender is not the contest.", options: { color: WHITE, bold: true, breakLine: true } },
  { text: "The eight weeks before it is. After the RFP is issued, we are answering someone else’s document.", options: { color: ICE } }
], { x: 0.92, y: TOP + 3.24, w: 2.81, h: 0.86, isTextBox: true, margin: 0,
     fontFace: BODY, fontSize: 9.5, italic: true, lineSpacingMultiple: 1.05 });

label(s1, "SO WE ARE NOT SELLING AGAINST A COMPETITOR", 0.75, TOP + 4.52, 3.15, CORAL);
s1.addText("We are selling against an arrangement that works — twenty-two years of it, and 400 technicians who have never had a reason to question it.",
  { x: 0.75, y: TOP + 4.72, w: 3.15, h: 0.70, isTextBox: true, margin: 0, fontFace: BODY,
    fontSize: 9, color: ICE, lineSpacingMultiple: 1.03 });

// ---- column 2 : battle card
card(s1, 4.35, TOP, 4.35, CH);
blockHead(s1, 2, "BATTLE CARD  ·  FROSTLINE", "75 s", 4.55, TOP + 0.16, 3.30);

s1.addText([
  { text: "How they will position themselves:  ", options: { bold: true, color: AMBER } },
  { text: "“Continuity at the lowest cost. We know the estate, we are already inside your maintenance scheduling, and we will phase the swap without breaking service.”", options: { color: ICE, italic: true } }
], { x: 4.55, y: TOP + 0.58, w: 3.95, h: 0.62, isTextBox: true, margin: 0,
     fontFace: BODY, fontSize: 9, lineSpacingMultiple: 1.03 });

label(s1, "THEIR TWO STRONGEST CLAIMS", 4.55, TOP + 1.26, 3.95, MINT);
bullets(s1, [
  "Lowest unit price, and already integrated with ABP’s maintenance scheduling — the cheapest and the least disruptive bid.",
  "The only supplier that has swapped units across 48,000 outlets without stopping the sale of chilled product."
], 4.55, TOP + 1.46, 3.95, 0.92, 9);

label(s1, "THEIR TWO REAL VULNERABILITIES", 4.55, TOP + 2.42, 3.95, CORAL);
bullets(s1, [
  "Two of their three refrigerant platforms are hit by the F-gas phase-down. Over five years, the “safe” bid is the one carrying regulatory and residual-value risk.",
  "No telemetry beyond a basic alarm contact — and their account team has not met anyone above Rousseau in four years."
], 4.55, TOP + 2.62, 3.95, 1.16, 9);

label(s1, "THREE DISCOVERY QUESTIONS — WITHOUT NAMING THE WEAKNESS", 4.55, TOP + 3.60, 3.95, AMBER);
bullets(s1, [
  "“Which refrigerant platform will the units delivered in year four sit on — and who carries the cost if it is restricted?”",
  "“How do you find out today that a cooler has failed, and how long is it down first?”",
  "“How will compliance and emissions be weighted against unit price — and who sets that weighting?”"
], 4.55, TOP + 3.79, 3.95, 1.12, 9);

label(s1, "THE ONE PROOF POINT WE MUST HAVE", 4.55, TOP + 4.96, 3.95, MINT);
s1.addText("Audited uptime and lost-volume data from our own 900-unit Portugal estate, cross-checked against ABP’s own service records.",
  { x: 4.55, y: TOP + 5.15, w: 3.95, h: 0.34, isTextBox: true, margin: 0, fontFace: BODY,
    fontSize: 9, color: ICE, lineSpacingMultiple: 1.02 });

// ---- column 3 : four corners + approach
card(s1, 8.95, TOP, 3.85, CH);
blockHead(s1, 3, "FOUR CORNERS", "70 s", 9.15, TOP + 0.16, 1.85);

label(s1, "WHAT FROSTLINE ASSUMES", 9.15, TOP + 0.60, 3.45, AMBER);
bullets(s1, [
  "About itself: field operations decide, and price won in 2019, so price wins in 2026.",
  "About ABP: this is a repeat equipment purchase, and Rousseau speaks for the estate."
], 9.15, TOP + 0.80, 3.45, 0.86, 9);

label(s1, "WHERE THOSE ASSUMPTIONS BREAK", 9.15, TOP + 1.72, 3.45, CORAL);
bullets(s1, [
  "The decision was forced by regulation and a board-level emissions target — not by equipment failure.",
  "The people who forced it — Diallo, Beck, the board — are people Frostline has not met in four years.",
  "Awareness, motivation, capability: twenty-two years of winning is why they will not see it coming."
], 9.15, TOP + 1.92, 3.45, 1.34, 9);

card(s1, 9.15, TOP + 3.32, 3.45, 1.10, TINT);
s1.addText("OUR APPROACH  ·  DISRUPTION", { x: 9.32, y: TOP + 3.42, w: 3.11, h: 0.24, isTextBox: true,
  margin: 0, fontFace: HEAD, fontSize: 12, bold: true, color: AMBER });
s1.addText("We cannot win on today’s criteria, so we change them before they are written: from lowest unit price to five-year, compliance-adjusted cost per outlet-day of availability.",
  { x: 9.32, y: TOP + 3.68, w: 3.11, h: 0.66, isTextBox: true, margin: 0, fontFace: BODY,
    fontSize: 8.5, color: ICE, lineSpacingMultiple: 1.02 });

label(s1, "WE ARE WRONG IF — AND THEN WE SEGMENT", 9.15, TOP + 4.54, 3.45, CORAL);
s1.addText("Beck and Marchand have already fixed the evaluation on unit price, or Diallo’s mandate carries no weight in the scoring. Then we stop reframing and bid a carve-out: the 20,000 highest-failure outlets in the countries where we own the engineers.",
  { x: 9.15, y: TOP + 4.74, w: 3.45, h: 0.76, isTextBox: true, margin: 0, fontFace: BODY,
    fontSize: 8.5, color: ICE, lineSpacingMultiple: 1.02 });

s1.addNotes(
"7 minutes, 6 speakers. Slide 1 = speakers 1-3 (about 3:10).\n\n" +
"SPEAKER 1 (45s) - WHERE WE STAND. Meridian is the account director on a 78 million euro, 60,000-cooler programme. Frostline has held this estate for twenty-two years and seventy per cent of it. We have one 900-unit pilot from 2021 and no relationship above middle management; our last meeting was seven months ago and we heard about the programme three weeks ago, second-hand. The point of the slide: two things forced this decision - the F-gas phase-down and a published 2030 emissions target - and neither of them is about coolers. Which is why the tender is not the contest. The eight weeks before it is.\n\n" +
"SPEAKER 2 (75s) - BATTLE CARD, FROSTLINE. Their pitch is continuity at the lowest cost. Two genuinely strong claims: cheapest unit price plus existing integration with ABP's maintenance scheduling, and the only proven ability to swap units across 48,000 outlets without stopping chilled sales. Two real vulnerabilities: two of their three refrigerant platforms are hit by F-gas, so over five years the safe bid is the one carrying the regulatory risk; and they have no telemetry beyond an alarm contact, with an account team that has not been above Rousseau in four years. We surface both without naming them - read the three discovery questions. And the one proof point we must have before any of this lands: audited uptime and lost-volume data from our own Portugal estate, cross-checked against ABP's own service records.\n\n" +
"SPEAKER 3 (70s) - FOUR CORNERS AND OUR APPROACH. Porter's harder question. Frostline assumes field operations decide and that price won in 2019 so price wins in 2026; and that ABP is buying coolers, not data. Both are wrong, because the decision was not triggered by equipment failure - it was triggered by regulation and a board emissions target, and the people who forced it are people Frostline has not met in four years. Their strength is their blind spot. So our approach is disruption, not domination - we do not have the resources for domination, and we are not the incumbent, so blocking is not available to us. We change the criteria before they are written: from unit price to five-year compliance-adjusted cost per outlet-day of availability. We are wrong if Beck and Marchand have already fixed the basis on price, or if Diallo's mandate carries no weight in the scoring. If we find that out, we switch to segmentation and bid a carve-out."
);

/* ==========================================================================
   SLIDE 2 — winning the field  (speakers 4-6)
   ========================================================================== */
const s2 = pres.addSlide();
slideFrame(s2, "Who actually decides — and the eight weeks",
  "Ten people, six votes, one document — and only one of them writes it",
  "TASKS 3, 4 & 5  ·  BUYING CENTRE, MENTOR, PLAN", "2 / 2");

const T2 = 1.25, H2 = 3.62;   // top row 1.25 -> 4.87

// ---- buying centre
card(s2, 0.55, T2, 7.05, H2);
blockHead(s2, 4, "THE BUYING CENTRE", "70 s", 0.75, T2 + 0.13, 2.55);

s2.addText("POWER →", { x: 0.08, y: 2.72, w: 1.60, h: 0.24, isTextBox: true, margin: 0,
  rotate: 270, align: "center", valign: "middle", fontFace: BODY, fontSize: 7.5, bold: true,
  charSpacing: 0.8, color: MUTED });

const QX = [1.10, 4.35], QY = [1.75, 2.86], QW = 3.05, QH = 1.02;
const quads = [
  [0, 0, "HIGH POWER  ·  LOW INTEREST", CORAL, [
    ["Marchand", " — chairs it; ran the 2019 award to Frostline"],
    ["Rousseau", " — 400 technicians; “it works fine”"],
    ["Fontaine", " — one signature, at the very end"]
  ]],
  [1, 0, "HIGH POWER  ·  HIGH INTEREST", MINT, [
    ["Beck", " — owns the budget; no supplier view yet"],
    ["Diallo", " — board mandate on F-gas; no budget, no vote"],
    ["Sanchez", " — writes the RFP, the Q&A, the bidder list"]
  ]],
  [0, 1, "LOW POWER  ·  LOW INTEREST", MUTED, [
    ["Haddad", " — data terms; a veto that arrives late"],
    ["Franchisor", " — no vote, and an absolute veto"]
  ]],
  [1, 1, "LOW POWER  ·  HIGH INTEREST", AMBER, [
    ["Kovač", " — pilot budget only; 14 months in"],
    ["Lefebvre", " — a cooler down on a Friday in July"]
  ]]
];
quads.forEach(q => {
  const x = QX[q[0]], y = QY[q[1]];
  card(s2, x, y, QW, QH, TINT);
  s2.addText(q[2], { x: x + 0.14, y: y + 0.08, w: QW - 0.28, h: 0.16, isTextBox: true, margin: 0,
    valign: "middle", fontFace: BODY, fontSize: 7, bold: true, charSpacing: 0.6, color: q[3] });
  const runs = [];
  q[4].forEach((p, i) => {
    runs.push({ text: p[0], options: { bold: true, color: WHITE } });
    runs.push({ text: p[1], options: { color: ICE, breakLine: i !== q[4].length - 1 } });
  });
  s2.addText(runs, { x: x + 0.14, y: y + 0.28, w: QW - 0.28, h: QH - 0.36, isTextBox: true,
    margin: 0, valign: "top", fontFace: BODY, fontSize: 8, lineSpacingMultiple: 1.02, paraSpaceAfter: 2 });
});

s2.addText("INTEREST IN CHANGING THE CURRENT ARRANGEMENT →",
  { x: 1.10, y: 3.94, w: 6.30, h: 0.18, isTextBox: true, margin: 0, align: "center", valign: "middle",
    fontFace: BODY, fontSize: 7.5, bold: true, charSpacing: 0.8, color: MUTED });

label(s2, "WHERE THE ORG CHART AND THE MAP DISAGREE", 0.75, 4.22, 6.65, AMBER);
s2.addText([
  { text: "Sanchez", options: { bold: true, color: WHITE } },
  { text: " sits four levels down and writes the requirement.   ", options: { color: ICE } },
  { text: "Rousseau", options: { bold: true, color: WHITE } },
  { text: " has no budget authority and can still kill the winner in evaluation.   ", options: { color: ICE } },
  { text: "Diallo", options: { bold: true, color: WHITE } },
  { text: " has no vote and no budget, and is the reason the programme exists.", options: { color: ICE } }
], { x: 0.75, y: 4.41, w: 6.65, h: 0.36, isTextBox: true, margin: 0, valign: "top",
     fontFace: BODY, fontSize: 8.5, lineSpacingMultiple: 1.02 });

// ---- mentor
card(s2, 7.80, T2, 5.00, H2);
blockHead(s2, 5, "OUR MENTOR", "70 s", 8.00, T2 + 0.13, 1.60);

s2.addText([
  { text: "AMARA DIALLO", options: { bold: true, color: AMBER, fontSize: 13, fontFace: HEAD } },
  { text: "   Director of Sustainability & ESG", options: { color: MUTED, fontSize: 9, fontFace: BODY } }
], { x: 8.00, y: T2 + 0.56, w: 4.60, h: 0.26, isTextBox: true, margin: 0, valign: "middle" });

para(s2, "Wants, and cannot get — ",
  "a costed, credible path to the 2030 target. She owns the outcome, holds no budget and no vote, and the chair of the committee was not in the room for her January board presentation.",
  8.00, T2 + 0.86, 4.60, 0.50, 9);
para(s2, "We ask her for — ",
  "the two criteria that must sit in the document: lifetime refrigerant compliance, and measured emissions per outlet. And an introduction to Beck.",
  8.00, T2 + 1.40, 4.60, 0.50, 9);
para(s2, "We give her — ",
  "an estate-level F-gas and emissions cost model she tables in her own name.",
  8.00, T2 + 1.94, 4.60, 0.34, 9);

card(s2, 8.00, T2 + 2.34, 4.60, 1.18, TINT);
label(s2, "LOOKS LIKE A MENTOR AND IS NOT  ·  ELENA KOVAČ", 8.16, T2 + 2.44, 4.28, CORAL);
s2.addText([
  { text: "Fourteen months in, enthusiastic, has twice asked her own IT team about joining cooler data to outlet sales — and never raised it with procurement. Pilot budget, no estate budget.", options: { color: ICE, breakLine: true } },
  { text: "The test: ask her to spend capital, not time. A mentor puts the telemetry requirements to Sanchez in writing; a fan gives you a meeting.", options: { color: WHITE, italic: true } }
], { x: 8.16, y: T2 + 2.64, w: 4.28, h: 0.84, isTextBox: true, margin: 0, valign: "top",
     fontFace: BODY, fontSize: 8.5, lineSpacingMultiple: 1.02, paraSpaceAfter: 3 });

// ---- eight weeks
card(s2, 0.55, 5.00, 12.25, 2.04);
blockHead(s2, 6, "THE EIGHT WEEKS BEFORE THE RFP", "70 s", 0.75, 5.08, 3.60);
s2.addText("Anything that does not change the document is time we have to justify.",
  { x: 7.20, y: 5.06, w: 5.40, h: 0.30, isTextBox: true, margin: 0, align: "right", valign: "middle",
    fontFace: BODY, fontSize: 8.5, italic: true, color: MUTED });

const steps = [
  ["1", "WEEKS 1–2", "Diallo first", "Build the F-gas and 2030 cost-of-inaction model for the estate — in her name, not ours.", "→ MAKES COMPLIANCE A SCORED CRITERION", MINT],
  ["2", "WEEKS 2–3", "Test Kovač, then use her", "Co-author the data spec: open API, door-open events, outlet-level sales join.", "→ WRITES IN WHAT AN ALARM CONTACT CANNOT MEET", MINT],
  ["3", "WEEKS 3–5", "Neutralise Rousseau", "Not a pitch. His technicians, our Portugal uptime record, read on his terms.", "→ CHANGES NO TEXT — IT PROTECTS THE OTHER FOUR", CORAL],
  ["4", "WEEKS 4–6", "Re-base Beck’s economics", "Cost per outlet-day of availability over five years, not price per unit.", "→ MOVES THE EVALUATION TO FIVE-YEAR COST", MINT],
  ["5", "WEEKS 6–8", "Sanchez, and Haddad early", "Bidder list, Q&A rules, and a data-processing annex offered before Legal is asked to block.", "→ THE TEXT, THE WEIGHTS, AND WHO ANSWERS", MINT]
];
steps.forEach((st, i) => {
  const x = 0.75 + i * 2.40;
  s2.addText(st[0], { x, y: 5.46, w: 0.28, h: 0.26, isTextBox: true, margin: 0, valign: "middle",
    fontFace: HEAD, fontSize: 15, bold: true, color: AMBER });
  s2.addText(st[1], { x: x + 0.30, y: 5.46, w: 1.95, h: 0.26, isTextBox: true, margin: 0, valign: "middle",
    fontFace: BODY, fontSize: 7.5, bold: true, charSpacing: 0.6, color: MUTED });
  s2.addText(st[2], { x, y: 5.76, w: 2.25, h: 0.24, isTextBox: true, margin: 0, valign: "middle",
    fontFace: BODY, fontSize: 10, bold: true, color: WHITE });
  s2.addText(st[3], { x, y: 6.02, w: 2.25, h: 0.58, isTextBox: true, margin: 0, valign: "top",
    fontFace: BODY, fontSize: 8.5, color: ICE, lineSpacingMultiple: 1.02 });
  s2.addText(st[4], { x, y: 6.62, w: 2.25, h: 0.34, isTextBox: true, margin: 0, valign: "top",
    fontFace: BODY, fontSize: 7.5, bold: true, color: st[5], lineSpacingMultiple: 1.0 });
});

s2.addText("Porter (1980) · Chen (1996) · Zahra & Chaples (1993) · Webster & Wind (1972) · Kohli (1989) · Ronchetto, Hutt & Reingen (1989) · Mitchell, Agle & Wood (1997) · Burnham, Frels & Mahajan (2003)",
  { x: 0.55, y: 7.12, w: 12.25, h: 0.22, isTextBox: true, margin: 0, valign: "middle",
    fontFace: BODY, fontSize: 7, color: MUTED });

s2.addNotes(
"Slide 2 = speakers 4-6 (about 3:30).\n\n" +
"SPEAKER 4 (70s) - THE BUYING CENTRE. Ten people, six formal votes - so the committee is not the buying centre. Power on one axis, interest in CHANGING the current arrangement on the other. Top left, high power and no interest in change: Marchand chairs the committee and ran the 2019 tender that awarded Frostline, so change means her own decision was wrong, and she is publicly committed to six per cent cost reduction; Rousseau has 400 technicians and says openly the estate works fine; Fontaine sees the recommendation once. Top right: Beck owns the budget and has not formed a view - he is the prize; Diallo has a board-level, non-negotiable mandate; Sanchez writes the document. Bottom right, high interest and little power: Kovac has a pilot budget, Lefebvre has the Friday-in-July problem and is our best source of evidence. Bottom left, the two late vetoes: Haddad on data terms, and the franchisor, who is not on the org chart at all and can veto anything that touches how the cooler looks. Three places the org chart is wrong: Sanchez sits four levels down and writes the requirement; Rousseau has no budget authority and can still kill us in evaluation; Diallo has no vote and is the reason the programme exists.\n\n" +
"SPEAKER 5 (70s) - THE MENTOR. Amara Diallo. What she wants and cannot currently get: a costed, credible path to the 2030 target and the F-gas transition. She owns the outcome and holds neither budget nor vote - and note the detail in the case: she presented to the board in January, Beck was in the room, Marchand was not. The person chairing the evaluation was absent for the reason the programme exists. We ask her for two things: the two criteria that must be in the document, and an introduction to Beck. We give her something she can use internally - an estate-level F-gas and emissions cost model she tables in her own name. Now the trap. Kovac looks exactly like a mentor: enthusiastic, technical, already building a telemetry case, and she will take every meeting. But she is fourteen months in, has a pilot budget only, and has twice asked her own IT team about joining cooler data to outlet sales without ever raising it with procurement. Enthusiasm is not influence. How we find out: we ask her to spend capital, not time. Will you put the telemetry requirements to Sanchez in writing and co-sign them? A mentor spends internal capital; a fan gives you a meeting.\n\n" +
"SPEAKER 6 (70s) - THE EIGHT WEEKS. Five moves, in order. One, Diallo: build the F-gas and cost-of-inaction model in her name - that makes compliance and emissions scored criteria rather than preferences. Two, test Kovac and then co-author the data specification - open API, door-open events, outlet-level join - which writes in requirements a basic alarm contact cannot meet. Three, neutralise Rousseau: not a pitch, his own technicians reading our Portugal uptime data on his terms. This one changes nothing in the document, and we have to justify it: without him neutral, the user buyer kills the winner during evaluation, so it protects the value of the other four. Four, re-base Beck's economics onto cost per outlet-day of availability over five years, which moves the evaluation off unit price. Five, Sanchez and Haddad: the bidder list, the Q&A rules, and a data-processing annex offered before Legal is asked to block. Four of the five change the document. If we are still explaining our telemetry to Sanchez in week nine, we have already lost."
);

pres.writeFile({ fileName: "The_ABP_Project_Meridian.pptx" }).then(f => console.log("wrote", f));
