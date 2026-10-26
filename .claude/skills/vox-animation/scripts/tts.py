#!/usr/bin/env python3
"""
tts.py — český voiceover (Piper zdarma, nebo placený ElevenLabs) + časování pro animaci a titulky.

  python3 tts.py vo.json [--out-dir assets/] [--length-scale 0.95]
  python3 tts.py vo.json --engine elevenlabs --voice-id <ID> [--speed 1.0] [--out-dir assets-el/]

Vstup (vo.json):
  {
    "voice": "cs_CZ-jirka-medium",       # volitelné
    "length_scale": 0.95,                # <1 = rychleji
    "gap": 0.35,                         # pauza mezi segmenty (s)
    "lead_in": 0.4,                      # ticho na začátku
    "tail": 1.5,                         # ticho na konci
    "segments": [
      {"id": "hook", "say": "text pro hlas", "text": "text *titulku*",
       "pause": 0.6, "cap": true, "el": {"seed": 22}}
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

ElevenLabs („engine“: „elevenlabs“ ve vo.json, nebo --engine):
  - klíč: v cloudu jako network secret prostředí (Add secret → Allowed websites api.elevenlabs.io,
    Custom header xi-api-key bez prefixu „Bearer“) – proxy ho přidá sama, session ho nevidí a doménu
    není třeba povolovat; jinde proměnná ELEVENLABS_API_KEY. Nikdy do repa ani chatu;
  - „voice_id“, „model_id“ (výchozí eleven_multilingual_v2), „speed“ (0.7–1.2, místo length_scale),
    „voice_settings“ (stability, similarity_boost, style…), „language_code“ (jen u modelů, které ho berou);
  - endpoint /with-timestamps vrací časy znaků → kousky titulků (a tím i VOX.wordT) sedí na skutečnou řeč;
  - odpovědi se ukládají do .cache/elevenlabs/ (klíč = hlas + model + nastavení + text + kontext),
    takže nezměněné segmenty se znovu neplatí. „el_cache“: „el-cache“ ve vo.json = cache vedle vo.json
    (commitnout – nahrávky jsou placené a nedeterministické, vybraný take by se jinak ztratil). Kontext sousedních vět (previous/next_text) zlepšuje
    intonaci; vypnout „el_context“: false (pak změna věty nepřegeneruje sousedy);
  - segment může mít „el“: {…} = vlastní nastavení jen pro něj, např. vybraný take
    {"seed": 22} nebo {"voice_settings": {"stability": 0.3}, "model_id": …}; pevný kontext
    {"previous_text": "…", "next_text": ""} („“ = hlas ví, že tu věta končí / začíná);
  - nádechy mezi slovy a na konci vět se vystřihnou (debreath, podle časů slov) – místo nich ticho
    nejvýš „breath_pause“ s (výchozí 0,15), na konci segmentu jen pauza „pause“/„gap“; nechat je:
    „debreath“: false ve vo.json nebo --keep-breaths. Funguje i nad cache – nic se znovu neplatí.
  - zvuk před prvním / za posledním slovem segmentu se ztlumí (clean_edges – lupnutí na konci
    nahrávek; „clean_edges“: false); pod celý hlas jde tichý šum prostoru „room_tone“ (dBFS RMS,
    výchozí -66 u ElevenLabs, null = vypnout), ať mezi slovy není digitální ticho („střih“).
"""
import argparse
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import wave

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


EL_API = 'https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128'


def el_request(body, voice_id, key):
    """Jeden požadavek na ElevenLabs; vrací JSON {audio_base64, alignment}."""
    headers = {'Content-Type': 'application/json'}
    if key:   # jinak klíč přidá proxy prostředí (network secret s hlavičkou xi-api-key)
        headers['xi-api-key'] = key
    req = urllib.request.Request(EL_API.format(voice=voice_id), data=json.dumps(body).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        hint = (' – chybí klíč: network secret pro api.elevenlabs.io (hlavička xi-api-key, bez prefixu) '
                'nebo proměnná ELEVENLABS_API_KEY') if e.code == 401 else ''
        sys.exit(f'ElevenLabs HTTP {e.code}{hint}: {e.read().decode("utf-8", "replace")[:400]}')
    except urllib.error.URLError as e:
        sys.exit(f'ElevenLabs nedostupný ({e.reason}) – je api.elevenlabs.io povolená v síti prostředí?')


def el_synth(say, prev_text, next_text, cfg, cache_dir, fallback=()):
    """Namluví segment přes ElevenLabs (s cache). Vrací (mp3 bytes, alignment dict | None).
    Hledá v cache_dir, pak ve fallback složkách (nalezené zkopíruje do cache_dir)."""
    body = {'text': say, 'model_id': cfg['model_id']}
    vs = dict(cfg.get('voice_settings') or {})
    if cfg.get('speed') is not None:
        vs['speed'] = cfg['speed']
    if vs:
        body['voice_settings'] = vs
    if cfg.get('language_code'):
        body['language_code'] = cfg['language_code']
    if cfg.get('seed') is not None:
        body['seed'] = cfg['seed']
    prev_text = cfg.get('previous_text', prev_text)   # „el“: {"previous_text": …} = pevný kontext
    next_text = cfg.get('next_text', next_text)       # ("" = věta končí; jiný text = sousedé se nepřegenerují)
    if cfg.get('context', True):
        if prev_text: body['previous_text'] = prev_text
        if next_text: body['next_text'] = next_text
    h = hashlib.sha1(json.dumps([cfg['voice_id'], body], ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()
    cp = os.path.join(cache_dir, h + '.json')
    old = next((os.path.join(d, h + '.json') for d in fallback if os.path.exists(os.path.join(d, h + '.json'))), None)
    if os.path.exists(cp):
        res = json.load(open(cp, encoding='utf-8'))
    elif old:
        res = json.load(open(old, encoding='utf-8'))
        with open(cp, 'w', encoding='utf-8') as f:
            json.dump(res, f)
    else:
        key = os.environ.get('ELEVENLABS_API_KEY')   # volitelné; v cloudu ho přidává proxy (network secret)
        print('  ElevenLabs:', say[:60], file=sys.stderr)
        res = el_request(body, cfg['voice_id'], key)
        with open(cp, 'w', encoding='utf-8') as f:
            json.dump(res, f)
    return base64.b64decode(res['audio_base64']), res.get('alignment') or res.get('normalized_alignment')


def debreath(path, al, max_pause=0.15):
    """Vystřihne nádechy v mezerách mezi slovy (časy slov z alignmentu ElevenLabs).
    Nádech = šum bez hlasu (víc než polovina energie nad 2 kHz), tišší než řeč, aspoň 60 ms. Když na
    slovo zakončené sykavkou / „v z h ř“ navazuje bez ticha, je to konec slova („dřív“ = [dřif]), ne nádech.
    Konce a začátky slov zůstanou – hledá se jen mezi nimi. Místo nádechu zůstane ticho
    nejvýš max_pause s (na konci segmentu jen 0,03 s – pauzu dá „pause“/„gap“), časy znaků
    v al se posunou. Vrací (počet nádechů, posunutý alignment)."""
    import numpy as np
    with wave.open(path) as wf:
        sr, params = wf.getframerate(), wf.getparams()
        x = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(np.float64)
    ch, st, en = al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']
    words, cur = [], None
    for k, c in enumerate(ch):
        if c.isalnum():
            cur = [st[k], en[k], c] if cur is None else [cur[0], en[k], c]
        elif cur:
            words.append(cur); cur = None
    if cur:
        words.append(cur)
    if not words:
        return 0, al
    # slovo končí hláskou, která na konci zní jako šum („dřív“ [f], „ves“, „muž“ [š], „bůh“ [ch], „keř“)
    fric = set('fvszšžhřcčx')
    dur = len(x) / sr
    gaps = [(0.0, words[0][0] - 0.015, '')] + [(words[j][1], words[j + 1][0] - 0.015, words[j][2]) for j in range(len(words) - 1)] \
        + [(words[-1][1], dur, words[-1][2])]
    def level(f):
        return 20 * np.log10(np.sqrt(np.mean(f ** 2)) / 32768 + 1e-9)

    n = int(0.01 * sr)
    win = np.hanning(n)
    fr = np.fft.rfftfreq(n, 1 / sr)
    gain = np.ones(len(x))
    fade = int(0.02 * sr)
    count = 0
    cuts = []         # (od, do) ve vzorcích – vystřižené ticho
    for gi, (a, b, last) in enumerate(gaps):
        if b - a < 0.06:
            continue
        o0, o1 = int(a * sr), int(b * sr)
        run = []          # rámce nádechu za sebou
        for o in list(range(o0, o1 - n + 1, n)) + [None]:
            if o is not None:
                f = x[o:o + n]
                lvl = level(f)
                sp = np.abs(np.fft.rfft(f * win))
                hi = sp[fr > 2000].sum() / (sp.sum() + 1e-9)
                if hi > 0.5 and -58 < lvl < -25:
                    run.append(o)
                    continue
            # šum navazující bez ticha na slovo zakončené sykavkou / „v z h ř“ je konec slova
            # („dřív“ → [dřif]), ne nádech – ten se nestříhá
            dip = run and any(level(x[q:q + n]) < -50 for q in range(o0, run[0], n))
            if len(run) >= 6 and (dip or last.lower() not in fric):
                # rozšířit přes tiché okolí: dozvuk nádechu (< -30 dB) a ticho před ním (< -50 dB)
                s0, s1 = run[0], run[-1] + n
                while s1 + n <= o1 and level(x[s1:s1 + n]) < -30:
                    s1 += n
                while s0 - n >= o0 and level(x[s0 - n:s0]) < -50:
                    s0 -= n
                s1 = min(o1, s1 + n)
                gain[s0:s1] = 0
                gain[max(0, s0 - fade):s0] = np.minimum(gain[max(0, s0 - fade):s0], np.linspace(1, 0, s0 - max(0, s0 - fade)))
                e = min(len(x), s1 + fade)
                gain[s1:e] = np.minimum(gain[s1:e], np.linspace(0, 1, e - s1))
                count += 1
                keep = int((0.03 if gi == len(gaps) - 1 else max_pause) * sr)
                if s1 - s0 > keep:
                    cuts.append((s0 + keep // 2, s1 - (keep - keep // 2)))
            run = []
    if not count:
        return 0, al
    y = x * gain
    if cuts:
        mask = np.ones(len(y), bool)
        for c0, c1 in cuts:
            mask[c0:c1] = False
        y = y[mask]

    def shift(t):
        ts = t * sr
        return (ts - sum(min(c1, ts) - c0 for c0, c1 in cuts if c0 < ts)) / sr
    al = dict(al, character_start_times_seconds=[shift(t) for t in st],
              character_end_times_seconds=[shift(t) for t in en])
    with wave.open(path, 'wb') as wf:
        wf.setparams(params)
        wf.writeframes(y.astype(np.int16).tobytes())
    return count, al


def _level(f):
    import numpy as np
    return 20 * np.log10(np.sqrt(np.mean(np.asarray(f, float) ** 2)) / 32768 + 1e-9)


def clean_edges(path, al):
    """Ztlumí zvuk před prvním a za posledním slovem segmentu – ElevenLabs občas na konec nahrávky
    přidá uříznutý začátek dalšího zvuku (lupnutí). Konec slova se nechá doznít (> -60 dB), pak
    30ms doběh do ticha; na začátku 10ms náběh. Délka se nemění – časování titulků zůstává."""
    import numpy as np
    with wave.open(path) as wf:
        sr, params = wf.getframerate(), wf.getparams()
        x = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(np.float64)
    t = [(s_, e_) for c, s_, e_ in zip(al['characters'], al['character_start_times_seconds'],
                                       al['character_end_times_seconds']) if c.isalnum()]
    if not t:
        return
    n = int(0.01 * sr)
    e = min(len(x), int(t[-1][1] * sr))
    lim = min(len(x), e + int(0.4 * sr))
    while e + n <= lim and _level(x[e:e + n]) > -60:
        e += n
    s = int(t[0][0] * sr)
    lim0 = max(0, s - int(0.15 * sr))
    while s - n >= lim0 and _level(x[s - n:s]) > -55:
        s -= n
    g = np.ones(len(x))
    fo, fi = min(int(0.03 * sr), e), int(0.01 * sr)
    g[e:] = 0
    g[e - fo:e] *= np.linspace(1, 0, fo)
    g[:s] = 0
    g[s:s + fi] *= np.linspace(0, 1, len(g[s:s + fi]))
    with wave.open(path, 'wb') as wf:
        wf.setparams(params)
        wf.writeframes((x * g).astype(np.int16).tobytes())


def room_tone(path, db, seed=7):
    """Pod celý hlas přimíchá tichý šum prostoru (růžový, 80 Hz–4 kHz, db = RMS v dBFS), aby mezi
    slovy a větami nebylo úplné digitální ticho – ve sluchátkách to jinak zní jako střih."""
    import numpy as np
    with wave.open(path) as wf:
        params, sr, ch = wf.getparams(), wf.getframerate(), wf.getnchannels()
        x = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(np.float64).reshape(-1, ch)
    n = len(x)
    sp = np.fft.rfft(np.random.default_rng(seed).standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / sr)
    sp *= np.where((f > 80) & (f < 4000), 1 / np.sqrt(np.maximum(f, 1)), 0)
    noise = np.fft.irfft(sp, n)
    noise *= 32768 * 10 ** (db / 20) / np.sqrt(np.mean(noise ** 2))
    with wave.open(path, 'wb') as wf:
        wf.setparams(params)
        wf.writeframes(np.clip(x + noise[:, None], -32768, 32767).astype(np.int16).tobytes())


def norm(s):
    return re.sub(r'\s+', ' ', s.replace('*', '').replace(NBSP, ' ')).strip()


def char_time(al, idx, offset):
    """Čas začátku znaku idx podle alignmentu ElevenLabs (+ posun segmentu)."""
    st = al['character_start_times_seconds']
    idx = max(0, min(idx, len(st) - 1))
    return offset + st[idx]


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
    ap.add_argument('--engine', choices=['piper', 'elevenlabs'], default=None)
    ap.add_argument('--voice-id', default=None, help='ElevenLabs voice_id')
    ap.add_argument('--model-id', default=None, help='ElevenLabs model (výchozí eleven_multilingual_v2)')
    ap.add_argument('--speed', type=float, default=None, help='ElevenLabs rychlost 0.7–1.2')
    ap.add_argument('--keep-breaths', action='store_true', help='ElevenLabs: nechat nádechy (jinak se ztlumí)')
    a = ap.parse_args()

    spec = json.load(open(a.spec, encoding='utf-8'))
    out_dir = a.out_dir or os.path.join(os.path.dirname(os.path.abspath(a.spec)), 'assets')
    os.makedirs(out_dir, exist_ok=True)
    engine = a.engine or spec.get('engine', 'piper')
    if engine == 'piper':
        from piper import PiperVoice
        from piper.config import SynthesisConfig
        voice = PiperVoice.load(ensure_voice(spec.get('voice', 'cs_CZ-jirka-medium')))
    else:
        el = {'voice_id': a.voice_id or spec.get('voice_id'),
              'model_id': a.model_id or spec.get('model_id', 'eleven_multilingual_v2'),
              'speed': a.speed if a.speed is not None else spec.get('speed'),
              'voice_settings': spec.get('voice_settings'), 'language_code': spec.get('language_code'),
              'context': spec.get('el_context', True),
              'debreath': spec.get('debreath', True) and not a.keep_breaths}
        if not el['voice_id']:
            sys.exit('ElevenLabs: chybí voice_id (ve vo.json nebo --voice-id).')
        el_cache = os.path.join(repo_root(), '.cache', 'elevenlabs')
        el_fallback = ()
        if spec.get('el_cache'):     # cache u projektu (commitnutá) – placené nahrávky se neztratí
            el_fallback = (el_cache,)
            el_cache = os.path.join(os.path.dirname(os.path.abspath(a.spec)), spec['el_cache'])
        os.makedirs(el_cache, exist_ok=True)
    ls = a.length_scale or spec.get('length_scale', 1.0)
    gap = spec.get('gap', 0.35)
    lead_in = spec.get('lead_in', 0.4)
    tail = spec.get('tail', 1.5)

    tmp = tempfile.mkdtemp(prefix='vox-tts-')
    files, segs = [], []
    sr = None
    t = lead_in
    breaths = 0

    def silence(sec, idx):
        p = os.path.join(tmp, f's{idx:03}.wav')
        with wave.open(p, 'wb') as wf:
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
            wf.writeframes(b'\x00\x00' * int(sec * sr))
        return p

    says = [seg.get('say') or seg['text'].replace('*', '') for seg in spec['segments']]
    for i, seg in enumerate(spec['segments']):
        say = says[i]
        p = os.path.join(tmp, f'v{i:03}.wav')
        al = None
        if engine == 'piper':
            with wave.open(p, 'wb') as wf:
                voice.synthesize_wav(say, wf, syn_config=SynthesisConfig(length_scale=ls))
        else:
            ov = seg.get('el') or {}      # přepsání pro jeden segment (jiný „take“: seed, voice_settings…)
            cfg = {**el, **ov}
            if 'voice_settings' in ov:
                cfg['voice_settings'] = {**(el['voice_settings'] or {}), **ov['voice_settings']}
            mp3, al = el_synth(say, says[i - 1] if i else '', says[i + 1] if i + 1 < len(says) else '', cfg, el_cache, el_fallback)
            mp = os.path.join(tmp, f'v{i:03}.mp3')
            with open(mp, 'wb') as f:
                f.write(mp3)
            subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', mp,
                            '-ar', '44100', '-ac', '1', '-sample_fmt', 's16', p], check=True)
            if el['debreath'] and al and al.get('character_end_times_seconds'):
                nb, al = debreath(p, al, spec.get('breath_pause', 0.15))
                breaths += nb
            if al and al.get('character_end_times_seconds') and spec.get('clean_edges', True):
                clean_edges(p, al)
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
        if al and al.get('character_start_times_seconds'):
            # kousky titulků podle skutečných časů znaků; když se titulek liší od namluveného textu
            # (tzv. × takzvaných, 12 × dvanácti), mapuje se podílem délky
            n_say = len(al['character_start_times_seconds'])
            same = norm(text) == norm(say)
            pos, acc = 0, 0
            for k, c in enumerate(chunks):
                if same:
                    idx = pos
                    pos += len(norm(c)) + 1
                else:
                    idx = int(round(n_say * acc / total_w))
                    acc += weight(c)
                cks.append({'t0': round(char_time(al, idx, t), 3), 'text': c})
            for k, c in enumerate(cks):
                c['t1'] = cks[k + 1]['t0'] if k + 1 < len(cks) else round(t + dur, 3)
            cks[0]['t0'] = round(t, 3)
        else:
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
    rt = spec.get('room_tone', -66 if engine == 'elevenlabs' else None)
    if rt is not None:
        room_tone(wav, rt)

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

    print(f'voiceover ({engine}) {duration:.1f} s, {len(segs)} segmentů →', out_dir)
    if breaths:
        print(f'  ztlumeno nádechů: {breaths}')
    for s in segs:
        print(f"  {s['t0']:6.2f}–{s['t1']:6.2f}  {s['id']:<10} {s['text'][:60]}")


if __name__ == '__main__':
    main()
