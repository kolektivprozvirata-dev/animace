#!/usr/bin/env node
/*
 * render.mjs — vyrenderuje HTML scénu (postavenou na runtime/vox.js) do videa.
 *
 *   node render.mjs <scene.html> [volby]
 *
 * Volby:
 *   --out <soubor.mp4>      výstupní video (default: out/<scéna>.mp4)
 *   --from <s> --to <s>     jen část časové osy
 *   --still <s>             jeden snímek v čase s → PNG (--out <soubor.png>)
 *   --contact <N>           kontaktní arch N snímků rovnoměrně přes scénu → PNG
 *   --scale <k>             zmenšení výstupu (0.5 = 960×540, rychlé náhledy)
 *   --audio <soubor>        přimíchat zvukovou stopu (voiceover / hudba)
 *   --crf <n>               kvalita x264 (default 18)
 *
 * Grafika se kvantuje na animFps (12 fps). Snímky se stejným kvantovaným
 * časem se nerenderují znovu – použije se předchozí obrázek.
 */
import { spawn, execSync } from 'node:child_process';
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

function loadPlaywright() {
  const require = createRequire(import.meta.url);
  try { return require('playwright'); } catch {}
  const globalRoot = execSync('npm root -g').toString().trim();
  return require(path.join(globalRoot, 'playwright'));
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) args[key] = true;
      else { args[key] = next; i++; }
    } else args._.push(a);
  }
  return args;
}

function ffmpeg(argList) {
  const p = spawn('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', ...argList], { stdio: ['pipe', 'inherit', 'inherit'] });
  const done = new Promise((res, rej) => p.on('close', (c) => (c === 0 ? res() : rej(new Error('ffmpeg exit ' + c)))));
  return { stdin: p.stdin, done };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const scenePath = args._[0];
  if (!scenePath) {
    console.error('Použití: node render.mjs <scene.html> [--out f.mp4] [--still s] [--contact N] [--scale k] [--audio f]');
    process.exit(1);
  }
  const abs = path.resolve(scenePath);
  const name = path.basename(abs, path.extname(abs));
  const outDir = path.resolve('out');
  fs.mkdirSync(outDir, { recursive: true });

  const { chromium } = loadPlaywright();
  const browser = await chromium.launch();
  const scale = parseFloat(args.scale || '1');
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: scale });
  page.on('console', (m) => { if (m.type() === 'error') console.error('[scéna]', m.text()); });
  page.on('pageerror', (e) => console.error('[scéna]', e.message));

  await page.goto('file://' + abs);
  await page.waitForFunction(() => typeof window.__render === 'function', null, { timeout: 15000 });
  await page.evaluate(() => document.fonts.ready);
  const cfg = await page.evaluate(() => window.__VOX_CONFIG);
  await page.setViewportSize({ width: cfg.width, height: cfg.height });
  const stage = (await page.$('#stage')) || page;

  const shoot = async (t) => {
    await page.evaluate((tt) => window.__render(tt), t);
    // dva rAF, ať se filtry a fonty skutečně vykreslí
    await page.evaluate(() => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r))));
    return stage.screenshot({ type: 'png' });
  };

  try {
    if (args.still !== undefined) {
      const t = parseFloat(args.still);
      const out = path.resolve(args.out || path.join(outDir, `${name}_t${t}.png`));
      fs.writeFileSync(out, await shoot(t));
      console.log('still →', out);
      return;
    }

    if (args.contact !== undefined) {
      const n = parseInt(args.contact === true ? '12' : args.contact, 10);
      const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'vox-contact-'));
      const cols = cfg.width >= cfg.height ? Math.ceil(Math.sqrt(n)) : Math.min(n, Math.ceil(Math.sqrt(n * 2.5)));
      for (let i = 0; i < n; i++) {
        const t = (cfg.duration * (i + 0.5)) / n;
        fs.writeFileSync(path.join(tmp, `f${String(i).padStart(3, '0')}.png`), await shoot(t));
      }
      const rows = Math.ceil(n / cols);
      const out = path.resolve(args.out || path.join(outDir, `${name}_contact.png`));
      const f = ffmpeg([
        '-framerate', '1', '-i', path.join(tmp, 'f%03d.png'),
        '-vf', `scale=${cfg.width >= cfg.height ? 640 : 300}:-1,tile=${cols}x${rows}:padding=8:color=black`,
        '-frames:v', '1', out,
      ]);
      f.stdin.end();
      await f.done;
      fs.rmSync(tmp, { recursive: true, force: true });
      console.log(`contact sheet (${n} snímků, t = střed každého úseku) →`, out);
      return;
    }

    const fps = cfg.fps;
    const from = parseFloat(args.from || '0');
    const to = Math.min(parseFloat(args.to || String(cfg.duration)), cfg.duration);
    const total = Math.round((to - from) * fps);
    const out = path.resolve(args.out || path.join(outDir, `${name}.mp4`));
    const ff = ['-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'png', '-i', '-'];
    if (args.audio) ff.push('-ss', String(from), '-i', path.resolve(args.audio), '-c:a', 'aac', '-b:a', '192k', '-shortest');
    ff.push('-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', String(args.crf || 18), '-preset', 'medium', '-movflags', '+faststart', out);
    const f = ffmpeg(ff);

    let lastStep = null, lastBuf = null;
    const t0 = Date.now();
    for (let i = 0; i < total; i++) {
      const t = from + i / fps;
      const s = Math.floor(t * cfg.animFps + 1e-6);
      if (s !== lastStep) { lastBuf = await shoot(t); lastStep = s; }
      if (!f.stdin.write(lastBuf)) await new Promise((r) => f.stdin.once('drain', r));
      if (i % fps === 0) process.stdout.write(`\r  ${i}/${total} snímků`);
    }
    f.stdin.end();
    await f.done;
    console.log(`\rvideo (${total} snímků, ${((Date.now() - t0) / 1000).toFixed(1)} s) →`, out);
  } finally {
    await browser.close();
  }
}

main().catch((e) => { console.error(e); process.exit(1); });
