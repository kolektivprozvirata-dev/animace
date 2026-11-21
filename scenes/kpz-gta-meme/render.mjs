#!/usr/bin/env node
// Render statického memu: node scenes/kpz-gta-meme/render.mjs [a b c]  →  out/kpz-gta-meme-<v>.png
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';

const require = createRequire(import.meta.url);
let pw; try { pw = require('playwright'); } catch { pw = require(path.join(execSync('npm root -g').toString().trim(), 'playwright')); }
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const out = path.join(root, 'out'); fs.mkdirSync(out, { recursive: true });
const variants = process.argv.slice(2).length ? process.argv.slice(2) : ['a', 'b', 'c'];

const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
for (const v of variants) {
  const own = path.join(here, 'meme-' + v + '.html');
  await page.goto(pathToFileURL(fs.existsSync(own) ? own : path.join(here, 'meme.html')).href + '?v=' + v);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForFunction(() => window.__layout);
  await page.waitForFunction(() => !document.querySelector('.kpz-bg img'), null, { timeout: 10000 }).catch(() => {});
  await page.waitForTimeout(300);
  const lay = await page.evaluate(() => window.__layout);
  const file = path.join(out, `kpz-gta-meme-${v}.png`);
  await (await page.$('#stage')).screenshot({ path: file });
  console.log(file, JSON.stringify(lay));
}
await browser.close();
