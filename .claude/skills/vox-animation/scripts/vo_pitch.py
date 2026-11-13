#!/usr/bin/env python3
"""
vo_pitch.py — výška a tempo hlasu po větách: najde větu, která „uletí“ výš/níž, a změří, jestli otázka stoupá.

  pip install praat-parselmouth        # jednou (Praat v Pythonu)
  python3 vo_pitch.py assets-vN/vo.wav assets-vN/vo-timing.js [id …]

Na řádek segmentu: medián F0 (Hz a půltóny vůči celému hlasu), 90. percentil, „konec“ = posledních 0,35 s
proti předchozí ~0,85 s (otázka má stoupat aspoň o ~+3 pt), tempo ve znacích za sekundu (bez mezer).
Orientačně (hlas KPZ dSBy): věty v řadě drží ±1,5 pt; skok ≥ 3 pt proti sousedům je slyšet
(kuřata v2: řečnická otázka v eleven_v3 +3,8 pt – „hlas je víc ve výškách“). Tempo ~12 zn/s = v pohodě, 13,5+ = spěchá.
"""
import json, math, re, sys
import numpy as np
import parselmouth

wav, timing = sys.argv[1], sys.argv[2]
only = set(sys.argv[3:])
src = open(timing, encoding='utf-8').read()
VO = json.loads(src[src.index('{'):src.rindex('}') + 1])
p = parselmouth.Sound(wav).to_pitch(time_step=0.01, pitch_floor=70, pitch_ceiling=400)
ts, f0 = p.xs(), p.selected_array['frequency']
ref = float(np.median(f0[f0 > 0]))
st = lambda hz: 12 * math.log2(hz / ref)
print(f'celkový medián F0 {ref:.0f} Hz; délka {VO["duration"]:.1f} s')
for s in VO['segments']:
    if only and s['id'] not in only:
        continue
    m = (ts >= s['t0']) & (ts <= s['t1']) & (f0 > 0)
    v, tt = f0[m], ts[m]
    if len(v) < 5:
        continue
    tail, body = v[tt >= tt[-1] - 0.35], v[(tt >= tt[-1] - 1.2) & (tt < tt[-1] - 0.35)]
    rise = 12 * math.log2(np.median(tail) / np.median(body)) if len(body) and len(tail) else float('nan')
    rate = len(re.sub(r'[*\s]', '', s['text'])) / (s['t1'] - s['t0'])
    print(f"{s['id']:7} {s['t0']:7.2f}  F0 {np.median(v):5.0f} Hz ({st(np.median(v)):+5.1f} pt)  p90 {st(np.percentile(v, 90)):+5.1f}"
          f"  konec {rise:+5.1f} pt  {rate:5.1f} zn/s")
