# RECAP V3 — Business Simulation "Marketplace" / Équipe AeroForge

> **À coller au début d'une nouvelle conversation** pour que Claude reprenne le contexte.
> Jeu : Marketplace Conscious Capitalism — Bikes, Company 6 « AeroForge », play.marketplace-simulation.com.
> État jeudi ~13h : **Q5 saisi et vérifié, PAS soumis (deadline 14h30). Q6 : vendredi 10h00.**

## ⚙️ Accès plateforme (procédure validée 2×)
- Login **hbsp.harvard.edu** (identifiants HBSP d'Aaron, email edu.devinci.fr — redonnés en début de conversation, jamais dans le repo) → My Coursepacks → **1405001** → **Run Simulation** (LTI).
- Env : Playwright + Chromium `/opt/pw-browsers/chromium`, `proxy: HTTPS_PROXY`, arg `--ssl-version-max=tls1.2`, profil persistant, CDP 9222 pour scripter.
- Navigation : `engine.php?tpl=student&tab=workspace&quarter=N&language=en-us&resource=<slug>`.
- Slugs utiles (nouveaux vérifiés) : `confirmrd` (R&D licensing), `ccconfidentialnewsletter` (in-basket), `fixedcapacity` (imprimantes), `overtime`, `extfactorysimulation` (production simulation), `improvementactions`, `followupstudy`, `hiresalespeople`, `opensalesoffice`, `industryworkerscompensation`, `industrysupervisorcompensation`.
- Édition : `#btnmodify` → champs → `#btnsave`, vérifier `saveResult:true`. ⚠️ Pages simulation/pro forma : bouton **`#btnloaddata` (minuscules)** → TOUJOURS vérifier que les revenus/prix se chargent (piège : revenus à 0 si la Production Simulation n'a pas eu son propre Load Data avant le pro forma).
- Règles : renommage forcé si composants modifiés (15 car. max) — le renommage de marque **cascade automatiquement** vers pubs/médias/web · 1 session par compte · pro forma à refaire EN DERNIER · claim « Highest rated » refusé en cas d'ex æquo.

## État après Q4 (résultats) — détail : Q4_RESULTS_ET_PLAN_Q5.md
- Total Perf 0,013 → 0,094 → **0,266** (dernier, moy 4,19) MAIS : **Investment in Future = max classe**, Financial Risk 1,000, Marketing Effectiveness 0,763 et Réputation > moyenne.
- Q4 : 550 vendus (proj. 498), demande 638 (**88 perdues, 3e rupture d'affilée**), CA 739,9k, net −849k (investissements), cash **3,02 M$**, parts 7,14 %.
- Judgments : **AeroSummit V2 = 68 → n°1 Mountain marché** (mais < min 70 CU, comme tout le monde) · Bolt 77 n°1 Speed ex æquo · Comfy 65. Pubs : 80/80/77 (best ads Speed & Rec).
- **News Q5 : carbone standard = danger sur Mountain, la solution est l'enriched carbon fiber (personne ne l'a). Fuites chimiques chez les 4 concurrents, pas nous.**
- **Carbon-Ride a aussi développé les pneus Racing sleek** (proposition de licence reçue 178 285 $ — inutile, on les a ; laissée sans réponse = rejet auto à la soumission).

## Q5 SAISI (détail + captures : Q5_DECISIONS_SAISIES.md, q5-saisies/)
1. ⭐ **R&D enriched carbon 1 023 325 $ → prêt Q6** (l'arme pour relancer Mountain en Q6).
2. **AeroSummit V3** (pneus super traction) · **AeroForgeBoltV2** (pneus racing sleek) — 2×30k.
3. Pub **Bolt-Outrun V3** (6k) : « Highest rated » retiré (recalé par Check Ad Claims, ex æquo), remplacé par « Lightning fast with sleek racing tires » + « wind-cheater ». 3 pubs truthful ✅.
4. Prix : BoltV2 **1 550**/0/p1 · Summit V3 **1 350**/50/p2 · Comfy 1 050/50/p3.
5. **Amsterdam : 7 vendeurs** (1 svc/1 rec/2 mtn/3 speed) — marché n°1 du jeu (3 789 u). NYC 6. 
6. **Bangalore ouvert** (84k+13k) → embauches Q6.
7. Rému : +1 sem congés et pension 5 % partout (ouvriers/superviseurs/vendeurs).
8. Capacité op. **16/j** (=fixe, 801 u effectives) + **overtime 2h** (973 u max) + **2 imprimantes 480k → fixe 32/j en Q6**.
9. Projection **900** (340/380/180), production sim OK, 0 perte projetée.
10. Improvements **~561k** : clean room air (mémos ouvriers malades !), respirateurs, cross-training, SPC, pistes cyclables. 5 études follow-up déjà achetées.
11. Reconduits : médias 13 insertions ~84,8k, 3 pages web, étude 15k, CD 200k, 0 emprunt.
12. **Pro forma refait en dernier : cash fin Q5 = 1 188 652 $, fin Q6 = 1 610 652 $** ✅.
13. Final Check : warning CD (permanent) + licence en attente (voulu) seulement.

## 🔴 Restait à faire (jeudi 14h30)
- **Aaron : relire Summary of Decisions et SOUMETTRE Q5.**
- Microsim **« Profitability »** due Q5 (équipe, 10-25 min) — pas faite par Claude.

## 🎯 Q6 (VENDREDI 10H00 — dernier trimestre noté !)
1. Analyser résultats Q5 dès traitement : Summit V3 ≥70 ? BoltV2 vs VelocisPro+sleek ? Amsterdam (objectif ~240) ? productivité (77 % ?) ; parts de marché.
2. **Redesign AeroSummit avec ENRICHED CARBON** (nouveau nom, 30k) → premier vélo Mountain sûr du marché. Ajuster pub si besoin.
3. **Embaucher Bangalore** (~4-5 : plutôt speed/rec).
4. Capacité : fixe 32/j → opérationnelle ~20-24/j selon Q5 réel ; overtime en appoint ; attention au ratio coûts (ne pas caler op = fixe cette fois).
5. **Cumulative Balanced Scorecard = la note** : optimiser métrique par métrique + garder de l'« Investment in Future » en Q6 (ex. R&D hybrid tires 254 694 $, prêt Q7 fictif) + Conscious Scorecard (santé/air fait en Q5).
6. Pro forma EN DERNIER (Load Data prod sim d'abord !).

## Livrables (rappel)
- **Q6 : vendredi 10h00** · **PPT 5-6 slides : vendredi 13h30** (20 %) · **Final Report 6-10 p : dimanche 20h00** (40 %).
- Narratif : Q2 raté → diagnostic brand judgment → Q3 Bolt 53→77 → Q4 corrections (Summit n°1 Mtn, pubs 80, capacité, salaires) + 2,5 M$ VC déployés selon BP → Q5 expansion (Amsterdam, features, enriched carbon) → Q6 relance Mountain. Investment in Future = max classe dès Q4.
- Équipe : Aaron Rainier (Président) · Luna Carballo (Mkt) · Justine Pellier (Analytics) · Patrick Yang (Fin) · Sarah Baraket (Sales) · Teysnim Abichou (HR).
