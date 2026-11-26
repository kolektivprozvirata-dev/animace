#!/usr/bin/env python3
"""
make-wide.py – z reelu na výšku (reel-kpz-foto.html, 1080×1920) udělá verzi pro plátno 16:9 (1920×1080).

  cd scenes/kpz-telata && python3 make-wide.py && node ../../.claude/skills/vox-animation/scripts/render.mjs \
      reel-kpz-foto-16x9.html --audio assets-platno/vo.wav --out ../../out/kpz-telata-platno-16x9.mp4

Svislá scéna zůstává zdrojem pravdy (texty, časování, animace). Tento skript jen:
  - přepne časování na hlas pro plátno (assets-platno: přirozenější tempo, bez „Zdroje v popisku“),
  - nastaví plátno 1920×1080, titulky níž a širší,
  - přidá wide.css (nové pozice prvků: text vlevo, obraz vpravo) a window.WIDE (delší odjezdy prvků),
  - přepíše pár SVG cest, které mají v svislé verzi pevné souřadnice.
Výsledek reel-kpz-foto-16x9.html neupravovat ručně – změny dělat ve svislé scéně, ve wide.css nebo tady.
"""
SRC, DST = 'reel-kpz-foto.html', 'reel-kpz-foto-16x9.html'
TIMING = 'assets-platno/vo-timing.js'

s = open(SRC, encoding='utf-8').read()
import re
s, n = re.subn(r'<script src="assets-[^"]+/vo-timing\.js"></script>', f'<script src="{TIMING}"></script>', s)
assert n == 1, 'časování nenalezeno'

reps = [
    ('<link rel="stylesheet" href="../../brand/kpz/kpz-theme.css">',
     '<link rel="stylesheet" href="../../brand/kpz/kpz-theme.css">\n<link rel="stylesheet" href="wide.css">\n<script>window.WIDE = true;</script>'),
    ('<body class="kpz">', '<body class="kpz wide">'),
    ("VOX.setup({ width: 1080, height: 1920,", "VOX.setup({ width: 1920, height: 1080,"),
    ("VOX.captions(t, { y: 1470,", "VOX.captions(t, { y: 975,"),
    # šipka „vystoupit z kruhu“ → k rostlinným alternativám vpravo
    ('<svg class="abs" width="1080" height="1920" style="left:0;top:0"><path id="d-exit" d="M600,990 C640,1060 660,1110 650,1170"',
     '<svg class="abs" width="1920" height="1080" style="left:0;top:0"><path id="d-exit" d="M880,640 C930,620 980,560 1030,520"'),
    # časová osa s nůžkami: delší, ať vyplní šířku
    ('<title>KPZ – telata (reel 9:16, styl KPZ, v12)</title>', '<title>KPZ – telata (plátno 16:9, VeganFest)</title>'),
]
for old, new in reps:
    assert s.count(old) == 1, old[:60]
    s = s.replace(old, new)

s = s.replace('<head>', '<head>\n<!-- VYGENEROVÁNO make-wide.py z reel-kpz-foto.html – neupravovat ručně -->', 1)
open(DST, 'w', encoding='utf-8').write(s)
print('→', DST)
