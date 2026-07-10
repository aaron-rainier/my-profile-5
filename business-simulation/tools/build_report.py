# -*- coding: utf-8 -*-
"""AeroForge Final Report — follows Final_Report_Template.docx structure."""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = "/home/user/my-profile-5/business-simulation"
CH = f"{HERE}/charts"

ORANGE = RGBColor(0xEB, 0x68, 0x34)
INK = RGBColor(0x0B, 0x0B, 0x0B)
SEC = RGBColor(0x52, 0x51, 0x4E)

doc = Document()
st = doc.styles["Normal"]
st.font.name = "Calibri"; st.font.size = Pt(10.5)
for h in ("Heading 1", "Heading 2"):
    doc.styles[h].font.name = "Calibri"
    doc.styles[h].font.color.rgb = INK
doc.styles["Heading 1"].font.size = Pt(15)
doc.styles["Heading 2"].font.size = Pt(12)

def P(text, bold=False, italic=False, size=10.5, color=None, align=None, space_after=6):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.bold = bold; r.font.italic = italic; r.font.size = Pt(size)
    if color: r.font.color.rgb = color
    if align: p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    return p

def H1(t): doc.add_heading(t, level=1)
def H2(t): doc.add_heading(t, level=2)

def table(headers, rows, widths=None, highlight_col=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Light Grid Accent 6"
    for j, h in enumerate(headers):
        cell = t.rows[0].cells[j]
        cell.text = ""
        r = cell.paragraphs[0].add_run(h)
        r.font.bold = True; r.font.size = Pt(9.5)
    for row in rows:
        cells = t.add_row().cells
        for j, v in enumerate(row):
            cells[j].text = ""
            r = cells[j].paragraphs[0].add_run(str(v))
            r.font.size = Pt(9.5)
            if highlight_col is not None and j == highlight_col:
                r.font.bold = True
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t

def fig(path, width, caption):
    doc.add_picture(path, width=Inches(width))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    P(caption, italic=True, size=9, color=SEC, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)

# ================= Title
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("AeroForge — Final Report"); r.font.size = Pt(24); r.font.bold = True
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Business Simulation Capstone — Marketplace® Conscious Capitalism (Bikes) · July 2026")
r.font.size = Pt(11); r.font.color.rgb = SEC
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Team: Aaron Rainier (President) · Luna Carballo (VP Marketing) · Justine Pellier (VP Analytics) · "
              "Patrick Yang (VP Finance) · Sarah Baraket (VP Sales) · Teysnim Abichou (VP HR)")
r.font.size = Pt(10); r.font.color.rgb = SEC
P("", space_after=4)

# ================= 1
H1("1. Mission Statement and Vision")
P("AeroForge exists to put elite carbon performance within everyone's reach. We forge custom-fitted, "
  "3D-printed carbon fiber bikes that empower riders to conquer any trail and win any race — while "
  "creating value for our employees, our communities, and the planet we ride through.", italic=True)
P("Did the mission actually guide us? Partly at first, fully at the end. In quarters 1–2 it was a statement; "
  "from quarter 3 onward it became an operating rule with measurable consequences: we never entered a price "
  "war (premium positioning held even when we were last in market share); we kept investing in employees and "
  "the environment during loss-making quarters (clean-room air filtration, chemical containment, top-of-market "
  "compensation); and when the industry's safety crisis hit — standard carbon fiber frames injuring mountain "
  "riders — the mission made the decision for us: we invested $1.02M in enriched carbon fiber, the largest "
  "single bet of our game, to sell a bike that is actually safe to ride. By Q6, our entire range was built on it.")

# ================= 2
H1("2. Business Strategy Summary")
P("Target segments: Mountain (primary) and Speed (secondary), with an opportunistic Recreation extension "
  "(AeroForgeComfy) added by the team in Q4 at marginal cost. Positioning: premium, value-driven, conscious-"
  "capitalism — win on product quality and integrity, never on price. Distribution: New York City, then "
  "Amsterdam (opened Q4 — the game's largest market at 3,789 units/quarter when we committed), then Bangalore "
  "(opened Q5). Funding: $1.5M founding equity plus $1.0M team tranches, then a $2.5M venture round obtained "
  "on our business plan and deployed exactly as promised (R&D, production capacity, stores).")
P("The strategy unfolded in five phases: (1) Q1–Q2 set-up and test market — where we failed, by designing on "
  "intuition; (2) Q3 repair — rebuilt the Bolt from the revealed data, #1 Speed product within one quarter; "
  "(3) Q4 investment — VC funds into R&D features, capacity ×1.5, Amsterdam, compensation catch-up; "
  "(4) Q5 expansion — sales force doubled to 13 across two cities, Bangalore opened, proprietary tire features shipped, and "
  "the enriched-carbon bet placed; (5) Q6 harvest — the whole range relaunched on enriched carbon, first "
  "profitable quarter of the company's history (+$708k net income on $3.0M revenue).")

# ================= 3
H1("3. Performance Review: Financial, Market, Operational, HR and CSR")

H2("3.1 Financial performance")
P("Revenue grew ×13 from the test market to Q6 (226k → 373k → 740k → 1,440k → 3,018k). Net income traced the "
  "strategy: −257k, −151k, −106k (repair), −849k (Q4: planned VC deployment), −1,246k (Q5: enriched carbon R&D "
  "$1.08M plus $561k of system improvements), then +708k in Q6 — the first profitable quarter, at a 62.5% gross "
  "margin (up from 53% in Q2). We financed the entire game with equity: zero conventional loans, zero emergency "
  "loans, ending with $2.06M cash and a Financial Risk score of 1.000 — the class maximum, every single quarter. "
  "Why we still scored last on cumulative Financial Performance (14.4 vs class average 40.0): the index rewards "
  "accumulated profit, and our profits arrived one quarter before the game ended. Our Wealth score (0.620, class "
  "minimum) tells the same story — −$1.9M of retained earnings against $5.0M of paid-in equity. This was the "
  "accounting shadow of a deliberate long-term strategy plus one genuinely failed quarter.")
fig(f"{CH}/chart_finance.png", 5.6, "Figure 1 — Revenue and operating cash flow by quarter ($ thousands). "
    "The Q4–Q5 troughs are the planned deployment of the $2.5M venture round.")

H2("3.2 Market performance")
P("Market share went 7.0% (Q3) → 7.1% (Q4) → 5.4% (Q5, as the whole market tripled) → 8.9% (Q6). Cumulative "
  "Market Performance finished last (0.071 vs average 0.159). The root causes are documented and split cleanly "
  "in two: first, two quarters of unrecommended product (our Mountain bike sat below the Customer Union's "
  "minimum rating until Q4, so the largest distribution channel of demand simply ignored us); second, chronic "
  "under-capacity — we lost sales to stock-outs in every quarter from Q3 onward (42, 88, 79, then 1,083 units in Q6). "
  "The product itself ended the game top-tier: brand judgments rose from 53/62/65 (Q2–Q3) to 87 Speed, 83 "
  "Mountain (top-2), 78 Recreation (top-2) in Q6; our ads scored 80–81 after the Q3 rebuild; price judgments "
  "were at or near 100 throughout. Q6 demand of 3,318 units — 84% above our own projection — proves the offer "
  "was right; we could manufacture only 2,235. We finished the game demand-rich and capacity-poor, the exact "
  "mirror of how we started.")
fig(f"{CH}/chart_fixes.png", 5.6, "Figure 2 — Diagnose → fix → measure: every metric we corrected moved.")

H2("3.3 Operations")
P("Production capacity scaled 6 → 11 → 16 → 32 units/day across Q3–Q6 (two 3D-printer purchases, $960k), with "
  "worker productivity up from 68.6% to 82.4% and unit labour cost down from $108 to $84. Quality investments "
  "(SPC, operator training, supplier programs) raised reliability steadily. Our recurring operational failure "
  "was demand planning: after every product fix, demand responded non-linearly and we projected linearly — four "
  "consecutive quarters of stock-outs, culminating in 1,083 lost sales in Q6 (≈$1.4M of revenue left on the "
  "table). We treated capacity as a cost to be minimised when it was in fact our binding constraint.")

H2("3.4 Human resources")
P("In Q2–Q3 we paid below market (worker satisfaction 71.9%, turnover 32%/quarter, productivity falling) — a "
  "false economy that starved the factory. From Q4 we moved every package to the top of the market (workers "
  "$13.2k + expanded health + 3 weeks vacation + 5% pension; equivalent upgrades for supervisors and the sales "
  "force). Results: satisfaction 88%, turnover 11%, productivity +14 points, and the sales force among the "
  "best-compensated in the industry. Cumulative HR Management finished at 0.790 vs a 0.801 average — the two "
  "cheap early quarters cost us an above-average final score.")

H2("3.5 CSR / Conscious Capitalism")
P("We ran sixteen system-improvement programs by Q6: chemical collection and containment, a clean-room "
  "reverse-flow air-filtration facility (a direct response to worker memos about carbon dust and epoxy vapour "
  "— our people told us before any metric did), protective equipment, air-filtering plants, a carbon-recycling "
  "consortium, cross-training, SPC, supplier quality programs, a fitness centre, daycare, school grants and "
  "community bike trails. AeroForge was never cited for toxic leaks — the "
  "newsletter repeatedly named four of our five competitors. Ethics showed up in small decisions too: we withdrew two "
  "advertising claims the moment the truth-in-advertising check flagged them, and we declined to buy a licence "
  "for technology we already owned rather than burn shareholder cash. Cumulative Reputation finished at 0.679 "
  "vs a 0.690 average — the cost of investing nothing in improvements before Q4.")

# ================= 4
H1("4. Main Results vs. Other Teams")
P("Final standings — cumulative Total Performance by company (the official ranking):")
table(
    ["Rank", "Company", "Cumulative Total Perf.", "Q6 Total Perf. (final quarter)"],
    [
        ("1", "WBB", "54.121", "357.724"),
        ("2", "NatuRide", "22.149", "101.200"),
        ("3", "Spe3d", "8.662", "31.720"),
        ("4", "Carbon-Ride", "2.918", "4.534"),
        ("5", "The Bike Yard", "0.968", "3.318"),
        ("6", "AeroForge", "0.703", "3.494"),
    ],
)
P("Two readings of this table matter. First, the honest one: we finished sixth of six. Second, the "
  "trajectory one: the gap to fifth place is 0.27 points — while fourth place sits at 2.9 and first at "
  "54 — and on the final quarter taken alone we were no longer last (3.494 vs The Bike Yard's 3.318). "
  "The turnaround had already begun overtaking a competitor when the game ended.")
P("Final cumulative balanced scorecard, AeroForge vs class:")
table(
    ["Cumulative metric", "Class min", "Class avg", "Class max", "AeroForge"],
    [
        ("Total Performance", "0.703", "14.920", "54.121", "0.703 — last"),
        ("Financial Performance", "14.380", "39.963", "74.217", "14.380 — last"),
        ("Market Performance", "0.071", "0.159", "0.271", "0.071 — last"),
        ("Marketing Effectiveness", "0.619", "0.743", "0.799", "0.745 — above avg"),
        ("Investment in Future", "4.228", "5.223", "7.874", "7.874 — 1st in class"),
        ("Wealth", "0.620", "1.053", "1.460", "0.620 — last"),
        ("HR Management", "0.766", "0.801", "0.854", "0.790"),
        ("Asset Management", "0.487", "0.771", "1.185", "0.487 — last"),
        ("Manufacturing Productivity", "0.636", "0.701", "0.738", "0.720 — above avg"),
        ("Financial Risk", "0.914", "0.986", "1.000", "1.000 — 1st (tied)"),
        ("Reputation", "0.635", "0.690", "0.752", "0.679"),
    ],
    highlight_col=4,
)
P("Quarterly Total Performance — the trajectory behind the cumulative number:")
table(
    ["", "Q2", "Q3", "Q4", "Q5", "Q6"],
    [
        ("AeroForge", "0.013", "0.094", "0.266", "0.957", "3.494"),
        ("Class average", "0.229", "0.943", "4.190", "n/a", "83.7"),
    ],
    highlight_col=None,
)
fig(f"{CH}/chart_totalperf.png", 5.4, "Figure 3 — AeroForge quarterly Total Performance: ×269 in four quarters, "
    "from 6% of the class average in Q2 to a level that would have been mid-pack two quarters earlier.")
P("Q6 market share by company: WBB 36.0%, NatuRide 21.3%, Spe3d 17.0%, Carbon-Ride 9.8%, AeroForge 8.9%, "
  "The Bike Yard 7.0%. Reading the two tables together explains our final ranking honestly: the cumulative "
  "index is dominated by accumulated financial performance, and a 17× gap to the class average in Q2, "
  "compounded quarterly, is mathematically unrecoverable in four quarters — even while posting the steepest "
  "relative improvement in the class and finishing first on the two metrics that were winnable from any "
  "starting position: Investment in Future and Financial Risk.")

# ================= 5
H1("5. Lessons Learnt")
P("Lesson 1 — Under uncertainty, intuition is a hypothesis, not a decision. Our Q2 failure had three specific, "
  "avoidable causes: a Speed advertisement built on Mountain imagery and claims (scored 35/100 — it actually "
  "rated higher with Mountain customers than Speed customers); 'comfort' components on a mountain bike that "
  "felt logical and scored 62, below the Customer Union's recommendation threshold; and a brand architecture "
  "chosen before buying the market research that would have falsified all of it. The ~$45k of studies we "
  "skipped cost us two quarters of momentum and, through the cumulative scorecard, the game.", space_after=8)
P("Lesson 2 — The business disciplines are one system. A 35-point ad starved the factory; below-market pay cut "
  "productivity, which capped output, which turned marketing wins into stock-outs. We never lost money 'in "
  "finance' — every financial loss originated upstream in a marketing or HR decision. The pro forma only "
  "reported it.", space_after=8)
P("Lesson 3 — Learn how the scorecard computes before playing, not after. Metrics winnable from day one "
  "regardless of sales volume — Investment in Future, Financial Risk — we eventually won, but only started "
  "managing deliberately from Q4. The cumulative Total Performance metric punishes one bad quarter forever; "
  "protecting the floor matters more than raising the ceiling.", space_after=8)
P("Lesson 4 — When product quality jumps, demand responds non-linearly. We under-projected demand in all four "
  "post-repair quarters (Q6: 3,318 actual vs 1,800 projected) because we extrapolated linearly from the "
  "previous quarter. Capacity should be built ahead of proven product quality, not behind realised sales.",
  space_after=8)
P("Lesson 5 — People signal problems before metrics do. Worker memos about carbon dust preceded any measurable "
  "morale drop; acting on them (clean room, protective equipment) preceded the productivity and satisfaction "
  "gains. The in-basket was our cheapest and fastest market research.", space_after=8)
P("How we changed our working methods mid-week: from Q3 every decision required a number from a purchased "
  "study or a revealed competitor matrix; every advertisement passed the truth-in-advertising check before "
  "submission; every quarter ended with the same discipline — Final Check, then the pro forma recomputed last; "
  "and each VP owned one function with the President arbitrating trade-offs. The rhythm turned a failing "
  "start-up into a machine that improved every metric it touched, every quarter, for four consecutive quarters.")

# ================= 6
H1("6. Preparing the Firm to Compete in the Future")
P("The game's own metric answers this: AeroForge finished first in class on cumulative Investment in Future. "
  "Concretely, a hypothetical Q7 would open with: (1) the industry's only fully enriched-carbon range, rated "
  "87/83/78, one quarter after competitors began converting theirs; (2) proprietary R&D in the pipeline — "
  "hybrid comfort tires paid for and ready in Q7 for the Recreation line; (3) a modern factory at 32 units/day "
  "of fixed capacity with an 82% productive, 88%-satisfied, 11%-turnover workforce; (4) three stores covering "
  "the three largest markets with 21 trained sales and service people; (5) $2.06M of cash, a $200k certificate "
  "of deposit, zero debt and an intact borrowing capacity; and (6) sixteen running system improvements "
  "protecting quality, the environment and the community. Proven Q6 demand of 3,318 units against 2,235 "
  "produced means the first Q7 decision is already written: one more printer and a third production shift.")

# ================= 7
H1("7. Top Recommendations If We Were to Start Over")
P("1. Spend the first dollar on information. Buy every market study from the test market onward and design "
  "brands, ads and prices from the component matrices and revealed leader structures — never from instinct. "
  "One failed quarter costs fifty times the price of the studies.", space_after=6)
P("2. Benchmark everything before shipping — an ad against the truth-check, a salary against the industry "
  "tables, a price against willingness-to-pay. The market has usually already published the right answer.",
  space_after=6)
P("3. Build capacity ahead of product quality, not behind sales. Once judgments are top-tier, demand arrives "
  "non-linearly; four quarters of stock-outs converted our best marketing into our competitors' revenue.",
  space_after=6)
P("4. Pay people at the top of the market from quarter one. The morale→productivity→output loop compounds "
  "slowly; started late, it cannot catch up.", space_after=6)
P("5. Read the scorecard's formulas on day one and protect the cumulative floor: never let a single quarter "
  "crater, because the index never forgets.", space_after=6)
P("6. Keep the financial discipline we kept: no emergency borrowing, investments financed by equity actually "
  "raised on a credible plan. Financial Risk was the one perfect score available to everyone; most teams "
  "dropped it.", space_after=6)
P("We lost the race, and we know precisely why — which is the one outcome this simulation is designed to "
  "produce. Given a seventh quarter, the machine we built in the last four would have been the most dangerous "
  "company in the industry.", italic=True)

doc.save(f"{REPO}/AeroForge_Final_Report.docx")
print("saved", f"{REPO}/AeroForge_Final_Report.docx")
