// Rend une timeline (JSON) en vidéo muette 1080×1920, image par image, avec Chromium.
//   node engine/render.mjs <timeline.json> <sortie.mp4>
//   node engine/render.mjs <timeline.json> --stills <dossier> 0,1.5,12   (images de contrôle)
import { readFileSync, writeFileSync, mkdirSync, rmSync } from 'node:fs';
import { spawn, execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { cpus } from 'node:os';
import { fontCss } from './fonts.mjs';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(HERE, '..');

function pageHtml(timeline) {
  return readFileSync(join(HERE, 'template.html'), 'utf8')
    .replace('/*__FONTS__*/', () => fontCss())
    .replace('/*__DATA__*/null', () => JSON.stringify(timeline).replace(/</g, '\\u003c'));
}

async function openPage(browser, html) {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on('pageerror', (e) => { console.error('Erreur dans la page :', e.message); process.exitCode = 1; });
  await page.setContent(html, { waitUntil: 'load' });
  await page.evaluate(() => window.init());
  return page;
}

const [tlPath, target, ...rest] = process.argv.slice(2);
if (!tlPath || !target) { console.error('usage : render.mjs <timeline.json> <sortie.mp4> | --stills <dossier> <t1,t2,…>'); process.exit(2); }
const timeline = JSON.parse(readFileSync(tlPath, 'utf8'));
const html = pageHtml(timeline);
const fps = timeline.fps;
const total = Math.round(timeline.duration * fps);
const browser = await chromium.launch({ args: ['--font-render-hinting=none', '--disable-lcd-text'] });

if (target === '--stills') {
  const [dir, list] = rest;
  mkdirSync(dir, { recursive: true });
  const page = await openPage(browser, html);
  for (const t of list.split(',').map(Number)) {
    await page.evaluate((x) => window.renderAt(x), t);
    await page.screenshot({ path: join(dir, `t${t.toFixed(2).padStart(6, '0')}.png`) });
  }
  await browser.close();
  process.exit(process.exitCode ?? 0);
}

// Rendu complet : plusieurs pages en parallèle, chacune encode son tronçon.
const workers = Math.max(1, Math.min(cpus().length, 4));
const tmp = join(dirname(resolve(target)), `.parts-${process.pid}`);
mkdirSync(tmp, { recursive: true });
const chunk = Math.ceil(total / workers);
let done = 0;
const started = Date.now();

async function renderPart(k) {
  const from = k * chunk, to = Math.min(total, from + chunk);
  if (from >= to) return null;
  const out = join(tmp, `part${String(k).padStart(2, '0')}.mp4`);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', '-g', String(fps * 2),
    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const closed = new Promise((res, rej) => ff.on('close', (code) => (code === 0 ? res() : rej(new Error(`ffmpeg a échoué (${code})`)))));
  const page = await openPage(browser, html);
  for (let f = from; f < to; f++) {
    await page.evaluate((x) => window.renderAt(x), f / fps);
    const buf = await page.screenshot({ type: 'jpeg', quality: 96 });
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
    if (++done % 150 === 0) console.log(`  ${done}/${total} images (${((Date.now() - started) / 1000).toFixed(0)} s)`);
  }
  ff.stdin.end();
  await closed;
  await page.close();
  return out;
}

const parts = (await Promise.all(Array.from({ length: workers }, (_, k) => renderPart(k)))).filter(Boolean);
await browser.close();
if (process.exitCode) { rmSync(tmp, { recursive: true, force: true }); process.exit(process.exitCode); }
const listFile = join(tmp, 'list.txt');
writeFileSync(listFile, parts.map((p) => `file '${p}'`).join('\n'));
execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', listFile, '-c', 'copy', '-movflags', '+faststart', target]);
rmSync(tmp, { recursive: true, force: true });
console.log(`Vidéo muette : ${target} (${total} images, ${((Date.now() - started) / 1000).toFixed(0)} s de rendu)`);
