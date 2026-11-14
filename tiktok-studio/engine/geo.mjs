// Fabrique les visuels d'un pays : silhouette (tracé SVG) et drapeau (SVG).
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { feature } from 'topojson-client';
import { geoAzimuthalEqualArea, geoPath, geoCentroid, geoBounds } from 'd3-geo';

const require = createRequire(import.meta.url);
const NM = new URL('../node_modules/', import.meta.url).pathname;

let countries = null;
function loadCountries() {
  if (!countries) {
    const topo = require('world-atlas/countries-10m.json');
    countries = feature(topo, topo.objects.countries).features;
  }
  return countries;
}

// Liste des polygones d'une entité, un par un.
function polygonsOf(f) {
  const g = f.geometry;
  return g.type === 'Polygon' ? [g.coordinates] : g.coordinates;
}

/**
 * Silhouette d'un pays, centrée et ajustée dans une boîte w × h.
 * numericId : code ISO 3166-1 numérique (ex. "250" pour la France).
 * bbox      : [ouest, sud, est, nord] facultatif, pour ne garder que les
 *             polygones dont le centre tombe dedans (métropole, île principale…).
 */
export function countryShape(numericId, { w = 820, h = 600, bbox = null } = {}) {
  const f = loadCountries().find((c) => String(c.id).padStart(3, '0') === String(numericId).padStart(3, '0'));
  if (!f) throw new Error(`Pays introuvable : ${numericId}`);

  let polys = polygonsOf(f);
  if (bbox) {
    const [w0, s0, e0, n0] = bbox;
    polys = polys.filter((p) => {
      const [lon, lat] = geoCentroid({ type: 'Polygon', coordinates: p });
      return lon >= w0 && lon <= e0 && lat >= s0 && lat <= n0;
    });
  }
  if (!polys.length) throw new Error(`Aucun polygone gardé pour ${numericId}`);

  const geom = { type: 'MultiPolygon', coordinates: polys };
  const [lon, lat] = geoCentroid(geom);
  const projection = geoAzimuthalEqualArea().rotate([-lon, -lat]).fitSize([w, h], geom);
  const d = geoPath(projection)(geom);
  const [[x0, y0], [x1, y1]] = geoPath(projection).bounds(geom);
  return { d, w, h, box: [x0, y0, x1, y1], bounds: geoBounds(geom), name: f.properties.name };
}

/** Drapeau SVG 4:3 (flag-icons, licence MIT). alpha2 en minuscules : "fr". */
export function flagSvg(alpha2) {
  return readFileSync(`${NM}flag-icons/flags/4x3/${alpha2.toLowerCase()}.svg`, 'utf8');
}
