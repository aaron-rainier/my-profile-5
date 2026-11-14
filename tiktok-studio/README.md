# Studio TikTok — série « Niveau 10 »

Générateur de vidéos quiz verticales (1080×1920, environ 80 s) : dix niveaux, du plus facile à
l'impossible, avec compte à rebours, indice, révélation, voix et bande-son. Tout est produit par
le code, sans service payant.

## Fabriquer une vidéo

```bash
cd tiktok-studio
npm install                      # cartes, drapeaux, police
pip install -r requirements.txt  # son et voix
python3 engine/build.py episodes/001-formes-pays.json
```

Il faut aussi `ffmpeg` et Chromium avec Playwright. Le modèle de voix (environ 350 Mo) se
télécharge au premier lancement dans `.cache/`.

Le résultat arrive dans `out/` :

- `<id>.mp4` : la vidéo à publier ;
- `<id>-couverture.jpg` : l'image de couverture ;
- `<id>-legende.txt` : la légende et les hashtags.

Options utiles :

- `--stills 0,5.5,9.4` : n'écrit que des images de contrôle à ces instants (rapide) ;
- `--audio-only` : refait la bande-son en gardant les images déjà rendues.

## Écrire un nouvel épisode

Un épisode est un fichier JSON dans `episodes/`. Trois modes :

| Mode | Ce que le joueur voit | Champs propres à chaque niveau |
|---|---|---|
| `shape` | la silhouette du pays | `iso` (code ISO numérique), `cc`, `bbox` facultatif |
| `flag` | le drapeau | `cc` (code pays à deux lettres) |
| `text` | une question écrite et le drapeau | `cc`, `qsmall`, `question` |

Chaque niveau a aussi `name` (réponse affichée), `say` (réponse lue par la voix), `hint`
(indice à mi-chrono), `fact` (anecdote sous la réponse) et `timer` (4 ou 5 secondes).

`say` peut s'écrire autrement que `name` quand la voix prononce mal un nom étranger
(par exemple `"Ouélinntonne !"` pour Wellington).

`bbox` (`[ouest, sud, est, nord]`) ne garde que les terres dont le centre tombe dans la zone :
utile pour la France métropolitaine ou la Norvège sans le Svalbard.

## Sources et licences

- Contours des pays : Natural Earth (domaine public), via `world-atlas`.
- Drapeaux : `flag-icons` (MIT).
- Polices : Anton et Inter (OFL).
- Voix : Kokoro (Apache 2.0).
- Musique et bruitages : synthétisés par `engine/build.py`.
