#!/usr/bin/env python3
"""
tts.py — český voiceover přes Piper + časování pro animaci a titulky.

  python3 tts.py vo.json [--out-dir assets/] [--length-scale 0.95]

Vstup (vo.json):
  {
    "voice": "cs_CZ-jirka-medium",       # volitelné
    "length_scale": 0.95,                # <1 = rychleji
    "gap": 0.35,                         # pauza mezi segmenty (s)
    "lead_in": 0.4,                      # ticho na začátku
    "tail": 1.5,                         # ticho na konci
    "segments": [
      {"id": "hook", "say": "text pro hlas", "text": "text *titulku*",
       "pause": 0.6, "cap": true}
    ]
  }
  - "say"  = co se namluví (čísla slovy, výslovnost); když chybí, použije se "text"
  - "text" = co se zobrazí v titulcích; *hvězdičky* = zvýrazněné slovo
  - "pause" = pauza po segmentu (přepíše "gap")
  - "cap": false = titulek se pro tento segment nezobrazí (text je v animaci)

Výstup do --out-dir:
  vo.wav       – normalizovaný voiceover (-16 LUFS, vhodné pro sítě)
  vo-timing.js – window.VO = {duration, segments: [{id, t0, t1, text, cap, chunks: [{t0, t1, text}]}]}
  vo.srt       – titulky jako samostatný soubor

Model se hledá v .cache/piper/ v kořeni repa; chybí-li, stáhne se z Hugging Face.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request
import wave

from piper import PiperVoice
from piper.config import SynthesisConfig

HF = 'https://huggingface.co/rhasspy/piper-voices/resolve/main'


def repo_root():
    try:
        return subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip()
    except Exception:
        return os.getcwd()


def ensure_voice(name):
    cache = os.path.join(repo_root(), '.cache', 'piper')
    os.makedirs(cache, exist_ok=True)
    lang = name.split('-')[0]            # cs_CZ
    family = lang.split('_')[0]          # cs
    speaker, quality = name.split('-')[1], name.split('-')[2]
    for ext in ('.onnx', '.onnx.json'):
        path = os.path.join(cache, name + ext)
        if not os.path.exists(path):
            url = f'{HF}/{family}/{lang}/{speaker}/{quality}/{name}{ext}'
            print('stahuji', url, file=sys.stderr)
            urllib.request.urlretrieve(url, path)
    return os.path.join(cache, name + '.onnx')


NBSP = '\u00a0'


def keep_numbers(text):
    """„9 500“ → pevná mezera, aby se číslo v titulcích nerozdělilo na „9“ | „500“."""
    return re.sub(r'(?<=\d) (?=\d{3}\b)', NBSP, text)


def mark_words(text):
    """*více slov* → *více* *slov*, aby zvýraznění přežilo dělení na kousky.
    Dělí se jen běžnou mezerou – pevná mezera (čísla) drží slova pohromadě."""
    return re.sub(r'\*([^*]+)\*', lambda m: ' '.join(f'*{w}*' for w in m.group(1).split(' ') if w), text)


def chunk_text(text, max_chars=26, max_words=5):
    """Rozdělí titulek na krátké kousky; láme přednostně za interpunkcí. Čísla nedělí."""
    words = [w for w in mark_words(keep_numbers(text)).split(' ') if w]
    chunks, cur = [], []
    for w in words:
        trial = ' '.join(cur + [w])
        plain = trial.replace('*', '')
        if cur and (len(plain) > max_chars or len(cur) >= max_words):
            chunks.append(' '.join(cur))
            cur = [w]
        else:
            cur.append(w)
        if re.search(r'[.,!?…:;–]$', w.replace('*', '')) and len(' '.join(cur).replace('*', '')) >= 10:
            chunks.append(' '.join(cur))
            cur = []
    if cur:
        # krátký zbytek přilepit k předchozímu, ať nevisí jedno slovo
        if chunks and len(' '.join(cur).replace('*', '')) < 8 and len(chunks[-1].replace('*', '')) < 20:
            chunks[-1] = chunks[-1] + ' ' + ' '.join(cur)
        else:
            chunks.append(' '.join(cur))
    return chunks


def weight(s):
    """Odhad délky vyslovení: znaky + pauzy za interpunkcí."""
    s = s.replace('*', '')
    return len(s) + 6 * len(re.findall(r'[.!?…]', s)) + 3 * len(re.findall(r'[,;:–]', s))


def srt_time(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('spec')
    ap.add_argument('--out-dir', default=None)
    ap.add_argument('--length-scale', type=float, default=None)
    a = ap.parse_args()

    spec = json.load(open(a.spec, encoding='utf-8'))
    out_dir = a.out_dir or os.path.join(os.path.dirname(os.path.abspath(a.spec)), 'assets')
    os.makedirs(out_dir, exist_ok=True)
    voice = PiperVoice.load(ensure_voice(spec.get('voice', 'cs_CZ-jirka-medium')))
    ls = a.length_scale or spec.get('length_scale', 1.0)
    gap = spec.get('gap', 0.35)
    lead_in = spec.get('lead_in', 0.4)
    tail = spec.get('tail', 1.5)

    tmp = tempfile.mkdtemp(prefix='vox-tts-')
    files, segs = [], []
    sr = None
    t = lead_in

    def silence(sec, idx):
        p = os.path.join(tmp, f's{idx:03}.wav')
        with wave.open(p, 'wb') as wf:
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
            wf.writeframes(b'\x00\x00' * int(sec * sr))
        return p

    for i, seg in enumerate(spec['segments']):
        say = seg.get('say') or seg['text'].replace('*', '')
        p = os.path.join(tmp, f'v{i:03}.wav')
        with wave.open(p, 'wb') as wf:
            voice.synthesize_wav(say, wf, syn_config=SynthesisConfig(length_scale=ls))
        with wave.open(p) as wf:
            sr = wf.getframerate()
            dur = wf.getnframes() / sr
        if i == 0 and lead_in > 0:
            files.append(silence(lead_in, 999))
        files.append(p)
        text = seg.get('text', say)
        chunks = chunk_text(text, spec.get('cap_max_chars', 26), spec.get('cap_max_words', 5))
        total_w = sum(weight(c) for c in chunks)
        ct, cks = t, []
        for c in chunks:
            d = dur * weight(c) / total_w
            cks.append({'t0': round(ct, 3), 't1': round(ct + d, 3), 'text': c})
            ct += d
        segs.append({'id': seg['id'], 't0': round(t, 3), 't1': round(t + dur, 3), 'text': text,
                     'cap': seg.get('cap', True), 'chunks': cks})
        pause = seg.get('pause', gap)
        t += dur
        if i < len(spec['segments']) - 1:
            files.append(silence(pause, i))
            t += pause
    files.append(silence(tail, 998))
    duration = t + tail

    lst = os.path.join(tmp, 'list.txt')
    with open(lst, 'w') as f:
        for p in files:
            f.write(f"file '{p}'\n")
    raw = os.path.join(tmp, 'raw.wav')
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0',
                    '-i', lst, '-c', 'copy', raw], check=True)
    wav = os.path.join(out_dir, 'vo.wav')
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', raw,
                    '-af', 'highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,'
                           'loudnorm=I=-16:TP=-1.5:LRA=9',
                    '-ar', '48000', '-ac', '2', wav], check=True)

    data = {'duration': round(duration, 3), 'segments': segs}
    with open(os.path.join(out_dir, 'vo-timing.js'), 'w', encoding='utf-8') as f:
        f.write('// vygenerováno scripts/tts.py – neupravovat ručně\n')
        f.write('window.VO = ' + json.dumps(data, ensure_ascii=False, indent=1) + ';\n')
    with open(os.path.join(out_dir, 'vo.srt'), 'w', encoding='utf-8') as f:
        n = 1
        for s in segs:
            for c in s['chunks']:
                f.write(f"{n}\n{srt_time(c['t0'])} --> {srt_time(c['t1'])}\n{c['text'].replace('*', '')}\n\n")
                n += 1

    print(f'voiceover {duration:.1f} s, {len(segs)} segmentů →', out_dir)
    for s in segs:
        print(f"  {s['t0']:6.2f}–{s['t1']:6.2f}  {s['id']:<10} {s['text'][:60]}")


if __name__ == '__main__':
    main()
