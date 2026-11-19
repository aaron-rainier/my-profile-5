// Rend des calques transparents 1080×1920 (bandeau, sous-titres) en PNG.
//   echo '[{"out":"bandeau.png","html":"<div class=\"tag\">INFO</div>"}]' | node engine/overlay.mjs
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { fontCss } from './fonts.mjs';

const { chromium } = createRequire(import.meta.url)('playwright');
const CSS = `
html,body{margin:0;width:1080px;height:1920px;background:transparent;overflow:hidden}
.anton{font-family:'Anton',sans-serif;text-transform:uppercase;line-height:1}
.tag{position:absolute;left:60px;top:1196px;background:#E1001A;color:#fff;font-size:54px;letter-spacing:3px;padding:12px 28px 14px}
.title{position:absolute;left:60px;top:1282px;background:rgba(255,255,255,.97);color:#0A0F1F;font-size:56px;letter-spacing:1px;padding:13px 28px 15px;white-space:nowrap}
.cap{position:absolute;left:90px;width:900px;bottom:748px;display:flex;justify-content:center}
.cap span{font-family:'Inter',sans-serif;font-weight:800;font-size:48px;line-height:1.22;color:#fff;text-align:center;
  background:rgba(0,0,0,.62);padding:12px 26px 14px;border-radius:16px}
`;
const jobs = JSON.parse(readFileSync(0, 'utf8'));
const browser = await chromium.launch({ args: ['--font-render-hinting=none'] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
for (const job of jobs) {
  await page.setContent(`<!doctype html><meta charset="utf-8"><style>${fontCss()}${CSS}</style><body>${job.html}</body>`);
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: job.out, omitBackground: true });
}
await browser.close();
