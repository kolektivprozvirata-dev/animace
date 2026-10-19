#!/usr/bin/env python3
"""
Výstřižek z fotky s okrajem z utrženého papíru (koláž).

  python3 cutout.py foto.jpg vystrizek.png            # vystřihne zvíře/objekt (BiRefNet)
  python3 cutout.py foto.jpg kus.png --piece           # utržený kus celé fotky (obdélník)
  python3 cutout.py foto.jpg kus.png --piece --crop 0,380,1024,1110
  volby: --border 26 (šířka papíru v px) --seed 7 --paper f3e9e3

Model BiRefNet lite (MIT, onnx-community/BiRefNet_lite-ONNX, 224 MB) se při prvním
spuštění stáhne do .cache/birefnet/. Potřebuje: pip install onnxruntime numpy pillow.
Ušní známky s čísly rozmaž dřív (ve zdrojové fotce).
"""
import argparse, os, urllib.request
import numpy as np
from PIL import Image, ImageFilter

MODEL_URL = 'https://huggingface.co/onnx-community/BiRefNet_lite-ONNX/resolve/main/onnx/model.onnx'
CACHE = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '.cache', 'birefnet', 'model.onnx')

def session():
    import onnxruntime as ort
    path = os.path.abspath(CACHE)
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        print('stahuji model BiRefNet lite …'); urllib.request.urlretrieve(MODEL_URL, path)
    return ort.InferenceSession(path, providers=['CPUExecutionProvider'])

def matte(im):
    s = session()
    x = np.asarray(im.convert('RGB').resize((1024, 1024), Image.BILINEAR), dtype=np.float32) / 255.0
    x = ((x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]).transpose(2, 0, 1)[None].astype(np.float32)
    out = s.run(None, {s.get_inputs()[0].name: x})[-1][0, 0]
    a = Image.fromarray((255 / (1 + np.exp(-out))).astype(np.uint8)).resize(im.size, Image.BILINEAR)
    return a.point(lambda v: 0 if v < 40 else (255 if v > 200 else int((v - 40) * 255 / 160)))

def noise(w, h, scale, seed):
    small = np.random.default_rng(seed).random((max(2, h // scale), max(2, w // scale)))
    return np.asarray(Image.fromarray((small * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), dtype=np.float32) / 255.0

def torn_edge(mask, border, seed):
    """Papír kolem masky: rozmazání + nepravidelný práh = utržená hrana."""
    w, h = mask.size
    soft = np.asarray(mask.filter(ImageFilter.GaussianBlur(border * 0.55)), dtype=np.float32) / 255.0
    n = 0.55 * noise(w, h, 40, seed) + 0.3 * noise(w, h, 9, seed + 1) + 0.15 * noise(w, h, 3, seed + 2)
    return Image.fromarray(((soft > 0.04 + 0.16 * n) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))

def piece_mask(w, h, seed):
    m = Image.new('L', (w, h), 0); inset = int(min(w, h) * 0.03)
    m.paste(255, (inset, inset, w - inset, h - inset))
    sm = np.asarray(m.filter(ImageFilter.GaussianBlur(6)), dtype=np.float32) / 255.0
    return Image.fromarray(((sm > 0.35 + 0.3 * (noise(w, h, 14, seed + 5) - 0.5)) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7))

def make(src, out, piece=False, border=26, seed=7, paper=(243, 233, 227), crop=None, pad=60):
    im = Image.open(src).convert('RGB')
    if crop: im = im.crop(crop)
    w, h = im.size
    a = piece_mask(w, h, seed) if piece else matte(im)
    W, H = w + 2 * pad, h + 2 * pad
    A = Image.new('L', (W, H), 0); A.paste(a, (pad, pad))
    rgb = np.zeros((H, W, 3), dtype=np.float32) + paper + (noise(W, H, 2, seed + 9)[..., None] - 0.5) * 14
    paper_img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert('RGBA'); paper_img.putalpha(torn_edge(A, border, seed))
    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0)); canvas.alpha_composite(paper_img)
    photo = Image.new('RGBA', (W, H), (0, 0, 0, 0)); photo.paste(im, (pad, pad)); photo.putalpha(A)
    canvas.alpha_composite(photo)
    canvas = canvas.crop(canvas.getbbox()); canvas.save(out)
    print(out, canvas.size)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('out')
    ap.add_argument('--piece', action='store_true'); ap.add_argument('--border', type=int, default=26)
    ap.add_argument('--seed', type=int, default=7); ap.add_argument('--paper', default='f3e9e3')
    ap.add_argument('--crop', default=None, help='x0,y0,x1,y1')
    a = ap.parse_args()
    make(a.src, a.out, a.piece, a.border, a.seed, tuple(int(a.paper[i:i + 2], 16) for i in (0, 2, 4)),
         tuple(int(v) for v in a.crop.split(',')) if a.crop else None)
