# RECAP V2 — Business Simulation "Marketplace" / Équipe AeroForge

> **À coller au début d'une nouvelle conversation** pour que Claude reprenne le contexte.
> Jeu : Marketplace Conscious Capitalism — Bikes (vélos carbone 3D), Company 6 « AeroForge », play.marketplace-simulation.com.
> État au jeudi matin : **Q4 saisi et vérifié, prêt à être soumis (traitement jeudi 11h00)**.

## ⚙️ ACCÈS DIRECT À LA PLATEFORME (Claude sait le faire — mode d'emploi)
- **Pas de login direct Marketplace** (compte LTI sans mot de passe). Chemin : se connecter sur **hbsp.harvard.edu** avec les identifiants HBSP d'Aaron (email école edu.devinci.fr — Aaron les redonne en début de conversation, ne PAS les stocker dans le repo) → coursepack **1405001** « Business simulation Captsone - MAEMDF4A0025 » → bouton **Run Simulation** → arrivée LTI dans le jeu.
- Prérequis environnement : **accès internet complet** (réglage claude.ai/code) + Chromium/Playwright avec `proxy: HTTPS_PROXY` et l'argument **`--ssl-version-max=tls1.2`** (sinon ERR_CONNECTION_RESET via le proxy TLS). Profil persistant pour garder la session.
- Navigation par URL : `engine.php?tpl=student&tab=workspace&quarter=N&language=en-us&resource=<slug>` — slugs sans tirets : `balancedscorecard, brandjudgment, adjudgment, pricejudgment, competitorsbrands, competitorsads, competitorsprices, marketshare, sales, incomestatement, cashflow, balancesheet, resultcheck (top concerns), ccnewsletter (news), modifybrand, modifyad, pricing, featurerd, regionalmedia, designwebpage, opensalesoffice, hiresalespeople, workerscompensation, executivecompensation, salesforcecompensation, improvementactions, followupstudy, operatingcapacity, extfactorysimulation, demandprojection, proformacashflow, buymarketresearch, finalcheck, summaryofdecisions, stock`.
- Édition : cliquer l'onglet **WORKSPACE** (`#workspaceTitle`), puis `#btnmodify` → champs → `#btnsave` (clics JS si un overlay intercepte). Vérifier `"saveResult":true` dans la réponse `backend-json.php`.
- **Règles du jeu découvertes** : modifier les composants d'une marque (ou d'une pub existante) **oblige à changer son nom** (max **15 caractères**) · **1 seule session par compte** (si Aaron est connecté, Claude l'éjecte et vice-versa — coordonner) · les vendeurs ne s'embauchent que dans les villes au magasin **opérationnel** (ville ouverte en Q(n) → embauches en Q(n+1)) · warning pro forma se réarme à chaque modification de décision (re-save du pro forma cash flow EN DERNIER) · warning CD = permanent et inoffensif.

## Équipe & stratégie
Président : Aaron Rainier · VP Marketing : Luna Carballo · VP Analytics : Justine Pellier · VP Finance : Patrick Yang · VP Sales : Sarah Baraket · VP HR : Teysnim Abichou.
Segments cibles : **Mountain (1) + Speed (2)** ; positionnement premium/value-driven/conscious capitalism ; 1 magasin NYC + **Amsterdam en ouverture (Q4)**. WTP : Recreation 1100 · Mountain 1365 · Speed 1580.

## Historique scores
- Q2 : Total Perf **0,013** (moy 0,229) — dernier. Brand judgments 62/53, ventes 161, net −150,7k.
- Q3 : Total Perf **0,094** (min 0,079/moy 0,943/max 1,774) ; cumulé 0,045 (min 0,042/moy 0,422). Ventes 267 (+42 perdues en rupture de stock), net −105,9k. **Bolt 77 = n°1 Speed ex æquo** ✅ ; Summit 65 < minimum 70 ❌ ; pub Bolt-Outrun 35/100 ❌ (claims Mountain dedans) ; pub Summit 70 ✓. Productivité 68,6 % ↓ (salaires marché ont monté), turnover 32 %. Réputation 61 = dernière. Meilleure note de la classe en Manufacturing Productivity (0,730).
- Concurrents : NatuRide 26 % et Carbon-Ride 25 % de parts ; nous 7 %. Leaders Mountain : Mountain WBB 71, TheSummit 70. Leaders Speed à 77 : Speed sport WBB, The Apex, notre Bolt.
- **VC : 2 500 000 $ crédités en Q4** (25 000 actions à 100 $) → ~3,85 M$ de cash. Business Plan rendu ✅ (2,5 M$ demandés : Amsterdam Q4 + Bangalore Q5, +2 imprimantes, R&D features, pubs, vendeurs).

## Q4 — TOUT EST SAISI (détail complet : Q4_DECISIONS_SAISIES.md)
1. **AeroSummit V2** (Summit renommée, règle des 15 car.) : guidon → Basic straight, selle → all-purpose = config identique aux leaders Mountain. Bolt intouchée.
2. **AeroForgeComfy** : 3e marque **créée par l'équipe** (Recreation : Comfort/hybride/7v/selle+guidon confort). **Décision d'équipe : ON LA GARDE** (coûts engagés, marge 658 $/u, capacité libre, Recreation = plus gros gisement). À présenter au Final Report comme « extension opportuniste à coût marginal », pas comme pivot stratégique.
3. **Pubs** : **Bolt-Outrun V2** refaite 100 % Speed (brand 1, photo road race 2, fast&furious 3, racing tires 4, elite look 5, carbon quality 6, highest rated Speed 7 — véridique) ; **SummitConquerV2** calquée sur la pub à 80 (steep trail, steep climbs, tough carbon, high tread, adventure, mountains no longer difficult) ; **Comfy-Ride** (équipe) : claim mensonger « Highest rated Recreation » retiré (risque FTC détecté au Final Check) → remplacé par comfort seat + price rebate. Les 3 passent Check Ad Claims ✅.
4. **Prix** : Bolt 1500/0/prio1 · AeroSummit V2 1300/50/prio2 · Comfy 1050/50/prio3 — tous « Available for Sale » ✓.
5. **Amsterdam OUVERT** (136k, statut « Opening ») — vendeurs embauchables seulement en Q5. **NYC : 6 vendeurs** (+1 Recreation formé).
6. **Salaires** (marché avait monté) : ouvriers 12 500 + Expanded + 2 sem + 4 % (~15,6k, niveau WBB) · superviseurs 17 000 + Expanded + 4 % · vendeurs 20 500 + Full + 4 % (~27k, top marché). Productivité projetée 74 %.
7. **R&D** : pneus **Mountain super traction** + **Racing sleek** (254 694 $ chacun, 509 388 $ total), **prêts Q5** — news : nouvelles marques partout en Q5.
8. **System improvements 243 400 $** : formation opérateurs (fiabilité 93) + collecte chimique (moral 92) + plantes filtrantes + consortium recyclage. **+ 3 follow-up studies achetées** (Involvement, Efficiency, Good Neighbor — 60k) → débloquent des actions en Q5.
9. **Capacité : 6 → 11/jour (715/trim)**, effective ~529 à 74 % ; coûts unitaires ↓ (labor 108→84, overhead 108→58). Overtime 0. Pas d'imprimante (fixe 1 040 >> besoin).
10. **Projection saisie : 498** (Summit 210 / Bolt 230 / Comfy 60, 83/vendeur). Production simulation lancée ✓.
11. **Médias : 13 insertions, 84 752 $** selon Media Preferences (Summit : Biking 3/Sport 1/GenNews 1 · Bolt : Biking 3/Sport 1/Business 1 · Comfy : Leisure 1/H&F 2). 3 pages web actives. Étude de marché 15k ✓.
12. **Pro forma cash flow rempli Q4-Q6** (Q4 : op ~−810k + 2,5 M VC → cash fin ~3,0 M ; Q5 ~+58k avec Bangalore+2 imprimantes ; Q6 ~+419k — aligné BP). Pas d'emprunt (Financial Risk 1,000 à préserver) ; CD 200k conservé (3k d'intérêts/trim).
13. **Final Check** : seul reste le warning CD (permanent, inoffensif). Aaron vérifie et soumet.

## 🎯 PRIORITÉS Q5 (jeudi 14h30 !)
1. **Analyser les résultats Q4 dès traitement** (11h) : brand judgment AeroSummit V2 (attendu ≥70), ad judgments (Bolt attendu ~75), ventes vs 498 projetés, Comfy accueil marché, productivité (attendu ~74 %), parts de marché, réactions concurrents.
2. **Embaucher les vendeurs Amsterdam** (magasin devient opérationnel) : ~7 dont 1 service/1 rec/2 mtn/3 speed (Amsterdam = Speed 745, Rec 666, Mtn 489 ; 3 concurrents seulement : WBB, Spe3d, NatuRide).
3. **Intégrer les features R&D** (pneus super traction → nouveau design Summit ; racing sleek → nouveau design Bolt) = nouveaux noms de marques (15 car. max) + nouveaux noms de pubs si claims changent + racheter les redesigns (30k/marque).
4. **Bangalore** : BP promet ouverture Q5 (84k + 13k lease) + **2 imprimantes (480k)** — à valider selon demande Q4 réelle (embauches Bangalore alors possibles en Q6 seulement — anticiper !).
5. **Capacité** : recaler (~14-15/jour si Amsterdam + features montent la demande vers 750-850).
6. Prix : ne pas baisser sans signal (news : acheteurs stables sur les prix). Vérifier salaires marché (concurrents vont réagir).
7. **Refaire le pro forma EN DERNIER** (Load Data → Save) pour éteindre le warning.

## Livrables notés (rappel)
- **Q5 jeudi 14h30 · Q6 vendredi 10h00** (heure du jeu GMT+1).
- **PPT** 5-6 slides, 10 min (20 %) → **vendredi 13h30**.
- **Final Report** 6-10 p (40 %) → **dimanche 20h00** : expliquer POURQUOI/COMMENT, comparaison chiffrée vs concurrents, recos « si on recommençait ». Narratif gagnant : Q2 raté → diagnostic (brand judgment) → Q3 Bolt réparé (53→77) → Q4 corrections chirurgicales (Summit, pub Speed, capacité, salaires) + déploiement des 2,5 M$ VC conforme au BP → trajectoire de redressement.
- Bonus balanced scorecard (+1,5/+1/+0,5).

## Fichiers dans le repo (branche `claude/recap-internet-access-xic4ph`, dossier business-simulation/)
- **Q3_RESULTS_ET_PLAN_Q4.md** (analyse Q3 complète) · **Q4_DECISIONS_SAISIES.md** (chaque saisie + justification) · **RECAP_AeroForge.md** (V1 historique) · ce fichier.
- **q3-results/** (9 captures : scorecard, judgments, ventes, prix concurrents…) · **q4-saisies/** (11 captures de vérification dont Summary of Decisions).
- Templates : Business_Plan (rendu ✅ AeroForge_Business_Plan_FINAL.docx), Final_Report_Template.docx, Final_Presentation_Skeleton.pptx, PLAN_DE_LA_SEMAINE.md, logos, pubs PNG.
