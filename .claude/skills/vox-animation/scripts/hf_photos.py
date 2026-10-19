#!/usr/bin/env python3
"""
Provizorní fotky z datasetů na Hugging Face (když jsou fotobanky z prostředí blokované).

Prohledá popisky (textový sloupec) parquet datasetu, stáhne jen potřebné row-groupy
obrázků a uloží shody. Výchozí dataset: wtcherr/unsplash_20k (Unsplash, ~20k fotek, 512 px).

  python3 hf_photos.py "cow|cows|calf|cattle" out/foto [--dataset wtcherr/unsplash_20k]
          [--text prompt] [--image image] [--exclude "statue|skull"]

Potřebuje: pip install pyarrow huggingface_hub pillow (ideálně ve venv).
Fotky jsou jen na náhled – pro zveřejnění použít fotky klienta nebo ověřit licenci.
"""
import argparse, io, os, re
import pyarrow.parquet as pq
from huggingface_hub import HfFileSystem
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument('pattern'); ap.add_argument('out')
ap.add_argument('--dataset', default='wtcherr/unsplash_20k')
ap.add_argument('--text', default='prompt'); ap.add_argument('--image', default='image')
ap.add_argument('--exclude', default=None)
a = ap.parse_args()
pat = re.compile(rf'\b({a.pattern})\b', re.I); exc = re.compile(a.exclude, re.I) if a.exclude else None
fs = HfFileSystem(); os.makedirs(a.out, exist_ok=True)
files = sorted(f for f in fs.find(f'datasets/{a.dataset}') if f.endswith('.parquet'))
for fi, f in enumerate(files):
    with fs.open(f, 'rb', block_size=2**22) as fh:
        pf = pq.ParquetFile(fh)
        for rg in range(pf.num_row_groups):
            texts = pf.read_row_group(rg, columns=[a.text]).column(a.text).to_pylist()
            texts = [' | '.join(t) if isinstance(t, list) else t for t in texts]   # více popisků (COCO)
            idx = [i for i, t in enumerate(texts) if t and pat.search(t) and not (exc and exc.search(t))]
            if not idx: continue
            imgs = pf.read_row_group(rg, columns=[a.image]).column(a.image).to_pylist()
            for i in idx:
                b = imgs[i]['bytes'] if isinstance(imgs[i], dict) else imgs[i]; im = Image.open(io.BytesIO(b))
                name = f'{fi:02d}_{rg}_{i:04d}.{(im.format or "jpg").lower().replace("jpeg", "jpg")}'
                open(os.path.join(a.out, name), 'wb').write(b)
                print(name, im.size, texts[i][:90])
