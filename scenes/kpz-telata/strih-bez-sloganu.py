#!/usr/bin/env python3
"""
v35b: vystřihne slogan „Zvíře není stroj ani zboží.“ (segment alt3) z hotového hlasu v29 – bez nového generování.

  cd scenes/kpz-telata && python3 strih-bez-sloganu.py

Vstup:  assets-v29/vo.wav, assets-v29/vo-timing.js  (vo.wav je gitignored → nejdřív tts.py s vo-v29.json, bere z el-cache)
Výstup: assets-v35b/vo.wav, vo-timing.js, vo.srt  +  reel-kpz-foto-bez-sloganu.html (kopie scény s časováním v35b)

Střih je v tichu (room tone) před a po sloganu: 166,80 → 168,55 s, prolnutí 20 ms. Pauza mezi „…o trochu lépe.“
a „Celý ten kruh…“ pak vychází ~0,8 s. Scéna sama pozná chybějící alt3 (HAS) a záběr 11 přeskočí.
"""
import json, os, wave
import numpy as np

CUT0, CUT1, XF = 166.80, 168.55, 0.02
D = CUT1 - CUT0
SRC, DST = 'assets-v29', 'assets-v35b'
os.makedirs(DST, exist_ok=True)

# --- zvuk ---
w = wave.open(f'{SRC}/vo.wav'); p = w.getparams(); sr = w.getframerate(); ch = w.getnchannels()
a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, ch).astype(np.float32)
i0, i1, xf = int(CUT0 * sr), int(CUT1 * sr), int(XF * sr)
head, tail = a[:i0 + xf], a[i1:]
ramp = np.linspace(0, 1, xf)[:, None]
out = np.concatenate([head[:-xf], head[-xf:] * (1 - ramp) + tail[:xf] * ramp, tail[xf:]])
o = wave.open(f'{DST}/vo.wav', 'wb'); o.setparams(p)
o.writeframes(np.clip(out, -32768, 32767).astype(np.int16).tobytes()); o.close()

# --- časování ---
src = open(f'{SRC}/vo-timing.js', encoding='utf-8').read()
V = json.loads(src[src.index('{'):src.rstrip().rstrip(';').rindex('}') + 1])
sh = lambda t: round(t - D, 3) if t >= CUT1 else t
segs = []
for s in V['segments']:
    if s['id'] == 'alt3':
        continue
    s['t0'], s['t1'] = sh(s['t0']), sh(s['t1'])
    for c in s.get('chunks', []):
        c['t0'], c['t1'] = sh(c['t0']), sh(c['t1'])
    segs.append(s)
V['segments'], V['duration'] = segs, round(V['duration'] - D, 3)
open(f'{DST}/vo-timing.js', 'w', encoding='utf-8').write(
    f'// vygenerováno strih-bez-sloganu.py z {SRC} (vystřižen slogan {CUT0}–{CUT1} s) – neupravovat ručně\n'
    'window.VO = ' + json.dumps(V, ensure_ascii=False, indent=1) + ';\n')


def ts(t):
    ms = int(round(t * 1000))
    return f'{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}'


lines, n = [], 1
for s in segs:
    if not s.get('cap', True):
        continue
    for c in s['chunks']:
        lines += [str(n), f"{ts(c['t0'])} --> {ts(c['t1'])}", c['text'].replace('*', ''), '']
        n += 1
open(f'{DST}/vo.srt', 'w', encoding='utf-8').write('\n'.join(lines))

# --- kopie scény ---
html = open('reel-kpz-foto.html', encoding='utf-8').read()
v = html.replace(f'<script src="{SRC}/vo-timing.js"></script>', f'<script src="{DST}/vo-timing.js"></script>')
assert v != html, 'scéna nenačítá časování z ' + SRC
v = v.replace('<head>', '<head>\n<!-- v35b: kopie reel-kpz-foto.html s časováním assets-v35b (bez sloganu). '
              'Vzniká strih-bez-sloganu.py, neupravovat ručně. -->', 1)
open('reel-kpz-foto-bez-sloganu.html', 'w', encoding='utf-8').write(v)
print('délka', V['duration'], 's; zvuk', round(len(out) / sr, 3), 's')
