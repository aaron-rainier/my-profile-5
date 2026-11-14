// Prépare les visuels d'un épisode (silhouettes, drapeaux) et les écrit en JSON sur la sortie standard.
//   node engine/assets.mjs episodes/001-formes-pays.json
import { readFileSync } from 'node:fs';
import { countryShape, flagSvg } from './geo.mjs';

const episode = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const levels = episode.levels.map((lv) => {
  const out = {};
  if (lv.cc) out.flag = flagSvg(lv.cc);
  if (episode.mode === 'shape') {
    const s = countryShape(lv.iso, { w: 820, h: 560, bbox: lv.bbox ?? null });
    // Coordonnées arrondies au dixième de pixel : tracé bien plus léger, rendu identique.
    out.shape = { w: s.w, h: s.h, d: s.d.replace(/-?\d+\.\d+/g, (n) => String(Math.round(Number(n) * 10) / 10)) };
  }
  return out;
});
process.stdout.write(JSON.stringify({ levels }));
