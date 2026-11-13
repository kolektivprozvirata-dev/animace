#!/usr/bin/env python3
"""
vo_takes.py — namluví několik verzí („takes“) jedné věty přes ElevenLabs se stejným kontextem jako v celém hlasu
a každou změří (výška, stoupnutí na konci, délka). Vybraný seed pak zapiš k segmentu: "el": {"seed": N}.

  pip install praat-parselmouth
  python3 vo_takes.py scenes/x/vo-vN.json <segment_id> <out_dir> <seed …> [--ref-wav scenes/x/assets-vN/vo.wav]

Nahrávky jdou do stejné cache jako tts.py („el_cache“ ve vo.json), takže vybraný take se při dalším tts.py už neplatí.
Platí se jen nové verze (≈ délka věty ve znacích za každou). Na otázku: vybírat výšku do ±1 pt od sousedních vět
(vo_pitch.py) a „konec“ aspoň ~+3 pt; důrazný konec oznamovací věty = „konec“ ≤ ~−4 pt, větší rozsah a hlasitost.
"""
import argparse, json, math, os, subprocess, sys
import numpy as np
import parselmouth

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tts  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument('spec'); ap.add_argument('seg'); ap.add_argument('out')
ap.add_argument('seeds', nargs='+', type=int)
ap.add_argument('--ref-wav', default=None, help='celý hlas – výška takes v půltónech vůči jeho mediánu')
ap.add_argument('--el', default=None, help='JSON přepsání „el“ pro všechny takes, např. {"context": true, "next_text": ""}')
a = ap.parse_args()

spec = json.load(open(a.spec, encoding='utf-8'))
says = [s.get('say') or s['text'].replace('*', '') for s in spec['segments']]
ids = [s['id'] for s in spec['segments']]
i = ids.index(a.seg)
el = {'voice_id': spec['voice_id'], 'model_id': spec.get('model_id', 'eleven_multilingual_v2'), 'speed': spec.get('speed'),
      'voice_settings': spec.get('voice_settings'), 'language_code': spec.get('language_code'),
      'context': spec.get('el_context', True)}
cache = os.path.join(os.path.dirname(os.path.abspath(a.spec)), spec.get('el_cache') or '.')
os.makedirs(a.out, exist_ok=True)


def f0(path):
    p = parselmouth.Sound(path).to_pitch(time_step=0.01, pitch_floor=70, pitch_ceiling=400)
    t, f = p.xs(), p.selected_array['frequency']
    return t[f > 0], f[f > 0]


ref = float(np.median(f0(a.ref_wav)[1])) if a.ref_wav else None
for seed in a.seeds:
    ov = {**(spec['segments'][i].get('el') or {}), **(json.loads(a.el) if a.el else {})}
    cfg = {**el, **ov, 'seed': seed}
    if 'voice_settings' in ov:
        cfg['voice_settings'] = {**(el['voice_settings'] or {}), **ov['voice_settings']}
    mp3, _ = tts.el_synth(says[i], says[i - 1] if i else '', says[i + 1] if i + 1 < len(says) else '', cfg, cache)
    mp, wv = os.path.join(a.out, f'{a.seg}-s{seed}.mp3'), os.path.join(a.out, f'{a.seg}-s{seed}.wav')
    open(mp, 'wb').write(mp3)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mp, '-ac', '1', wv], check=True)
    tt, v = f0(wv)
    tail, body = v[tt >= tt[-1] - 0.35], v[(tt >= tt[-1] - 1.2) & (tt < tt[-1] - 0.35)]
    med = float(np.median(v))
    rel = f' ({12 * math.log2(med / ref):+4.1f} pt vůči celku)' if ref else ''
    rng = 12 * math.log2(np.percentile(v, 90) / np.percentile(v, 10))
    x = parselmouth.Sound(wv).values[0]
    rms = 20 * math.log10(math.sqrt(float(np.mean(x[np.abs(x) > 0.01] ** 2))) + 1e-9)
    print(f'seed {seed:4}: F0 {med:5.0f} Hz{rel}  konec {12 * math.log2(np.median(tail) / np.median(body)):+4.1f} pt'
          f'  rozsah {rng:4.1f} pt  hlasitost {rms:5.1f} dB  délka {tt[-1]:.2f} s  → {mp}')
