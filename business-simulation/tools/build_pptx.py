"""Build AeroForge final presentation (6 slides, 16:9) per skeleton structure."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = "/home/user/my-profile-5/business-simulation"
LOGO = f"{REPO}/logo/aeroforge_logo.png"
CHARTS = f"{HERE}/charts"

INK = RGBColor(0x0B, 0x0B, 0x0B)
SEC = RGBColor(0x52, 0x51, 0x4E)
MUT = RGBColor(0x89, 0x87, 0x81)
ORANGE = RGBColor(0xEB, 0x68, 0x34)
NAVY = RGBColor(0x25, 0x30, 0x3B)
GOOD = RGBColor(0x00, 0x63, 0x00)
FONT = "Calibri"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

def add_text(slide, x, y, w, h, runs_lines, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
             space_after=6):
    """runs_lines: list of paragraphs; each = list of (text, size, bold, color, italic)."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    first = True
    for line in runs_lines:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = align
        p.space_after = Pt(space_after)
        for (text, size, bold, color, italic) in line:
            r = p.add_run()
            r.text = text
            r.font.name = FONT
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.italic = italic
            r.font.color.rgb = color
    return tb

def accent_bar(slide):
    bar = slide.shapes.add_shape(1, Inches(0), Inches(0), prs.slide_width, Inches(0.09))
    bar.fill.solid(); bar.fill.fore_color.rgb = ORANGE
    bar.line.fill.background()

def footer(slide, page, speaker, timing):
    add_text(slide, 0.55, 7.02, 6.5, 0.4,
             [[("AEROFORGE — BUSINESS SIMULATION · JULY 2026", 9, False, MUT, False)]])
    add_text(slide, 8.2, 7.02, 4.6, 0.4,
             [[(f"{speaker} · {timing}   ", 9, True, ORANGE, False),
               (f"{page}/6", 9, False, MUT, False)]], align=PP_ALIGN.RIGHT)

def kicker_title(slide, kicker, title):
    add_text(slide, 0.55, 0.32, 12.2, 0.4, [[(kicker.upper(), 12, True, ORANGE, False)]])
    add_text(slide, 0.55, 0.66, 12.2, 0.9, [[(title, 30, True, INK, False)]])

def bullets(slide, x, y, w, h, items, size=15, gap=10):
    lines = []
    for head, body in items:
        line = []
        if head:
            line.append((head + "  —  " if body else head, size, True, INK, False))
        if body:
            line.append((body, size, False, SEC, False))
        lines.append(line)
    add_text(slide, x, y, w, h, lines, space_after=gap)

def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text

# ================================================================ SLIDE 1
s = prs.slides.add_slide(BLANK)
accent_bar(s)
s.shapes.add_picture(LOGO, Inches(5.03), Inches(0.55), height=Inches(3.3))
add_text(s, 1.0, 3.95, 11.33, 0.8,
         [[("Business Simulation — Our Story", 34, True, INK, False)]], align=PP_ALIGN.CENTER)
add_text(s, 1.0, 4.75, 11.33, 0.5,
         [[("Marketplace® Conscious Capitalism · Bikes · July 2026", 15, False, SEC, False)]],
         align=PP_ALIGN.CENTER)
add_text(s, 1.0, 5.35, 11.33, 0.55,
         [[("“We lost the race — and built the machine that would win the next one.”",
            17, False, ORANGE, True)]], align=PP_ALIGN.CENTER)
add_text(s, 1.0, 6.1, 11.33, 0.8,
         [[("Aaron Rainier President · Luna Carballo Marketing · Justine Pellier Analytics · "
            "Patrick Yang Finance · Sarah Baraket Sales · Teysnim Abichou HR",
            12.5, False, MUT, False)]], align=PP_ALIGN.CENTER)
footer(s, 1, "Aaron", "0:45")
notes(s, "AARON (0:45)\n"
         "Bonjour, nous sommes AeroForge — vélos carbone imprimés en 3D. "
         "Spoiler : nous n'avons pas gagné la course au scorecard. Mais nous avons construit, "
         "trimestre après trimestre, la machine qui aurait gagné la suivante. En 10 minutes, "
         "on ne va pas vous raconter ce qui s'est passé — on va vous montrer ce qu'on a appris, "
         "pourquoi c'est arrivé, et ce qu'on ferait différemment. [Passe à Sarah]")

# ================================================================ SLIDE 2
s = prs.slides.add_slide(BLANK)
accent_bar(s)
kicker_title(s, "Who we were", "Strategy & ambition")
bullets(s, 0.7, 1.85, 11.9, 4.6, [
    ("Mission", "Elite carbon performance within everyone's reach — creating value for riders, "
     "employees, communities and the planet we ride through."),
    ("Targets & positioning", "Primary: Mountain · Secondary: Speed. Premium, value-driven, "
     "conscious-capitalism positioning — win on product quality, never on price."),
    ("Footprint", "New York City → Amsterdam (Q4, the game's largest market) → Bangalore (Q5). "
     "Funded by a $2.5M venture round backed by our business plan."),
    ("Organization", "A real executive committee: 6 VPs with clear ownership. "
     "Every decision argued with data; the President arbitrates."),
], size=16, gap=16)
footer(s, 2, "Sarah", "1:30")
notes(s, "SARAH (1:30)\n"
         "Notre mission : la performance carbone d'élite, accessible — en créant de la valeur pour "
         "les riders, nos employés, les communautés et la planète. Deux segments cibles : Mountain "
         "en primaire, Speed en secondaire, positionnement premium value-driven — on gagne sur la "
         "qualité produit, jamais sur le prix. Expansion : New York, puis Amsterdam au Q4 — le plus "
         "gros marché du jeu — et Bangalore au Q5, financés par 2,5 M$ de capital-risque obtenus "
         "sur notre business plan. Et une vraie organisation de comité exécutif : six VPs, chaque "
         "décision argumentée par la donnée, le Président arbitre. [Passe à Justine]")

# ================================================================ SLIDE 3
s = prs.slides.add_slide(BLANK)
accent_bar(s)
kicker_title(s, "What happened", "Key results — the honest version")
s.shapes.add_picture(f"{CHARTS}/chart_totalperf.png", Inches(0.55), Inches(1.75), width=Inches(6.05))
s.shapes.add_picture(f"{CHARTS}/chart_finance.png", Inches(6.75), Inches(1.75), width=Inches(6.05))
add_text(s, 0.7, 6.05, 12.0, 0.9, [
    [("Cumulative scorecard: last. ", 13.5, True, INK, False),
     ("A cumulative index never forgives a failed test market — our Q2 hole followed us to the end.",
      13.5, False, SEC, False)],
    [("Conscious scorecard: ", 13.5, True, INK, False),
     ("only firm never cited for toxic leaks · employee satisfaction 88% · turnover 32%→11% · "
      "reputation above class average.", 13.5, False, SEC, False)],
], space_after=4)
footer(s, 3, "Justine", "2:00")
notes(s, "JUSTINE (2:00)\n"
         "Les faits, sans filtre. À gauche : notre Total Performance ×70 en trois trimestres — mais "
         "partie de si bas qu'au cumul nous finissons derniers : un index cumulatif ne pardonne pas "
         "un Q2 raté. À droite : le chiffre d'affaires a quasiment doublé chaque trimestre, de 226 k$ "
         "à 2,5 M$ projetés. Les deux creux de cash-flow en Q4-Q5 ne sont pas des pertes subies : "
         "c'est le déploiement volontaire des 2,5 M$ de capital-risque — R&D, capacité, magasins — "
         "exactement comme promis au business plan. Résultat : premier trimestre rentable en Q6, "
         "+446 k$. Et côté Conscious Capitalism : seule entreprise jamais citée pour fuites toxiques, "
         "satisfaction employés 88 %, turnover divisé par trois. [Passe à Luna]")

# ================================================================ SLIDE 4
s = prs.slides.add_slide(BLANK)
accent_bar(s)
kicker_title(s, "Why it happened", "One failure, one success, one new method")
bullets(s, 0.7, 1.8, 5.7, 4.8, [
    ("Failure — designed by intuition",
     "Q2 test market: a Speed ad built on Mountain claims (35/100) and “comfort” parts on a "
     "mountain bike (62 < the 70 recommendation threshold). Demand starved for two quarters."),
    ("Success — designed from data",
     "From Q3: copy the revealed component matrices and leader ad structures. Bolt 53→77 (#1 Speed), "
     "ad 35→80 (best Speed ad), Summit #1 Mountain (Q4)."),
    ("The method change, mid-week",
     "Buy every study, justify every field with a number, verify every save — "
     "Check Ad Claims · Final Check · pro forma last."),
], size=14, gap=14)
s.shapes.add_picture(f"{CHARTS}/chart_fixes.png", Inches(6.55), Inches(1.9), width=Inches(6.3))
footer(s, 4, "Luna", "2:15")
notes(s, "LUNA (2:15)\n"
         "Pourquoi ce trou au Q2 ? Nous avons designé à l'intuition. Notre pub Speed utilisait des "
         "arguments Mountain — 35/100. Notre VTT avait un guidon « confort » : logique en apparence, "
         "faux dans les données — 62, sous le seuil de recommandation de la Customer Union. Résultat : "
         "demande étouffée pendant deux trimestres. Le déclic : à partir du Q3, plus aucune décision "
         "sans donnée. Toutes les études achetées, les matrices de composants copiées, nos pubs "
         "restructurées sur les meilleures. Regardez le graphe : chaque métrique corrigée a bougé — "
         "marque Bolt 53→77 numéro 1 Speed, pub 35→81 meilleure pub Speed, Summit numéro 1 Mountain, "
         "productivité +14 points, satisfaction vendeurs 88 %. La méthode a changé au milieu de la "
         "semaine : acheter la donnée, justifier chaque champ, tout vérifier. [Passe à Teysnim]")

# ================================================================ SLIDE 5
s = prs.slides.add_slide(BLANK)
accent_bar(s)
kicker_title(s, "What we learned", "Three lessons we'll keep")
bullets(s, 0.7, 1.9, 11.9, 4.6, [
    ("1 · Business disciplines are one system",
     "A 35/100 ad starves a factory; below-market pay cut productivity to 68.6% and helped cap our "
     "factory — 88 sales lost to stock-outs in Q4. "
     "We never lost money “in finance” — we lost it in marketing and HR first."),
    ("2 · Under time pressure, intuition is a hypothesis — not a decision",
     "The test market exists to buy data before you bet. The ~$45k of studies we skipped in Q2 "
     "cost us two quarters of momentum."),
    ("3 · Play the scorecard like an engineer",
     "Learn how each metric is computed, then work backwards. The ones winnable from day 1, we won: "
     "#1 in class on Investment in Future and Financial Risk. The cumulative one punishes early "
     "mistakes forever."),
    ("+ People tell you first",
     "In-basket memos about sick workers → clean-room investment → morale up, satisfaction 88%. "
     "Listen to the weak signals."),
], size=15, gap=14)
footer(s, 5, "Teysnim", "1:45")
notes(s, "TEYSNIM (1:45)\n"
         "Trois leçons. Un : les disciplines ne forment qu'un seul système — une pub à 35 affame "
         "l'usine ; des salaires sous le marché font chuter la productivité à 68 % et nous coûtent "
         "88 ventes. Nous n'avons jamais perdu d'argent « en finance » : nous l'avons perdu d'abord "
         "en marketing et en RH. Deux : sous pression, l'intuition est une hypothèse, pas une "
         "décision — le test market sert à acheter la donnée avant de parier. Trois : jouer le "
         "scorecard en ingénieur : comprendre comment chaque métrique est calculée, puis remonter. "
         "Celles qu'on pouvait gagner dès le premier jour, on les a gagnées : premiers de la classe "
         "en Investment in Future et en Financial Risk. Et une leçon humaine : les mémos d'ouvriers "
         "malades nous ont fait investir dans la salle blanche — satisfaction 88 %. Écoutez les "
         "signaux faibles. [Passe à Patrick]")

# ================================================================ SLIDE 6
s = prs.slides.add_slide(BLANK)
accent_bar(s)
kicker_title(s, "What we'd share with other teams", "If we started over")
bullets(s, 0.7, 1.85, 11.9, 3.4, [
    ("Top recommendation",
     "Spend your first dollar on information: buy every market study in Q2 and design from the "
     "component matrices — never from instinct. One failed quarter costs 50× the studies."),
    ("One thing we'd never do again",
     "Ship anything unbenchmarked — an ad, a salary, a price. The market had already published "
     "the right answer; we just hadn't bought it."),
], size=16, gap=16)
# exit stats strip
strip = s.shapes.add_shape(1, Inches(0.7), Inches(4.55), Inches(11.9), Inches(0.85))
strip.fill.solid(); strip.fill.fore_color.rgb = RGBColor(0xF6, 0xF1, 0xEC)
strip.line.fill.background()
add_text(s, 0.95, 4.72, 11.4, 0.6,
         [[("AeroForge exits Q6:  ", 13.5, True, NAVY, False),
           ("100% enriched-carbon range · first profitable quarter (+$446k) · zero debt · "
            "#1 in class on Investment in Future & Financial Risk", 13.5, False, SEC, False)]])
add_text(s, 0.7, 5.75, 11.9, 0.9,
         [[("Our question for you:  ", 18, True, ORANGE, False),
           ("your scorecard is cumulative too — which “Q2 mistake” are you still paying for, "
            "and have you actually diagnosed it?", 18, False, INK, True)]])
footer(s, 6, "Patrick + Aaron", "1:45")
notes(s, "PATRICK (1:30)\n"
         "Si nous recommencions : notre premier dollar irait à l'information. Toutes les études dès "
         "le Q2 — environ 45 000 $ — et designer depuis les matrices, jamais à l'instinct : un "
         "trimestre raté coûte cinquante fois le prix des études. Ce que nous ne referons jamais : "
         "lancer quoi que ce soit sans benchmark — une pub, un salaire, un prix. Le marché avait "
         "déjà publié la bonne réponse ; nous ne l'avions simplement pas achetée. Nous sortons du "
         "jeu avec une gamme 100 % enriched carbon, le produit Mountain le mieux noté, un premier "
         "trimestre rentable et zéro dette.\n\n"
         "AARON (0:15, conclusion)\n"
         "On vous laisse avec une question : votre scorecard à vous aussi est cumulatif. Quelle est "
         "l'erreur de Q2 que vous payez encore — et l'avez-vous vraiment diagnostiquée ? Merci.\n\n"
         "=== PRÉPA Q&A ===\n"
         "« Vous êtes derniers, que s'est-il passé ? » → Nous avons perdu la partie au Q2, sur trois "
         "erreurs de conception faites à l'aveugle avant les données du test market. Le scorecard "
         "étant cumulatif, elles nous ont suivis. Ensuite : chaque trimestre a corrigé une cause "
         "racine mesurable (53→77, 35→81, 68→84 %), premier cash-flow positif en Q6, deux métriques "
         "n°1 de la classe. Nous avons perdu la course, appris à piloter.\n"
         "« Pourquoi garder Comfy (3e marque hors cible) ? » → extension opportuniste à coût "
         "marginal : marge 658 $/u, capacité disponible, Recreation = plus gros gisement de demande.\n"
         "« Pourquoi ne pas avoir vendu votre techno en licence ? » → Carbon-Ride nous a proposé "
         "d'acheter LEUR licence sur des pneus que nous avions déjà développés — refusé. Vendre les "
         "nôtres aurait armé nos concurrents pour le dernier trimestre noté.\n"
         "« Pourquoi des prix en hausse au Q5 ? » → demande > capacité de production : convertir la "
         "rareté en marge (features neuves à l'appui), plutôt que des ruptures de stock plus grosses.")

prs.save(f"{REPO}/AeroForge_Final_Presentation.pptx")
print("saved", f"{REPO}/AeroForge_Final_Presentation.pptx")
