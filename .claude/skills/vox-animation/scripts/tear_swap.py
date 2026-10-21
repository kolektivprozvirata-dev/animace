#!/usr/bin/env python3
"""
„Vytržení“ telete se dvěma fotkami: A = máma s teletem, B = stejná máma bez telete
(zarovnané, stejná velikost). Vyrobí 3 výstřižky na stejném plátně:
  par.png (A celé) · mama.png (B – kráva celá) · tele.png (jen tele z A)
Ve scéně: do trhu ukázat par.png, při trhu ho schovat a ukázat mama.png + tele.png (tele odjede).

  python3 tear_swap.py A.jpg B.jpg out_dir [--prefix trh2-] [--scale 0.66]
"""
import argparse, os, sys, numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
import cutout as C

ap = argparse.ArgumentParser()
ap.add_argument('a'); ap.add_argument('b'); ap.add_argument('out')
ap.add_argument('--prefix', default='trh2-'); ap.add_argument('--scale', type=float, default=0.66)
ap.add_argument('--border', type=int, default=22); ap.add_argument('--thr', type=int, default=30)
a = ap.parse_args()
A = Image.open(a.a).convert('RGB'); B = Image.open(a.b).convert('RGB').resize(A.size, Image.LANCZOS)
if a.scale != 1:
    A = A.resize((int(A.width * a.scale), int(A.height * a.scale)), Image.LANCZOS); B = B.resize(A.size, Image.LANCZOS)
w, h = A.size
mA = np.asarray(C.keep_largest(C.matte(A)), dtype=np.float32) / 255
mB = np.asarray(C.keep_largest(C.matte(B)), dtype=np.float32) / 255
diff = np.abs(np.asarray(A, dtype=np.float32) - np.asarray(B, dtype=np.float32)).max(axis=2)
calf = ((diff > a.thr) & (mA > 0.5)).astype(np.uint8) * 255
outside = ((mA > 0.5) & (mB < 0.5)).astype(np.uint8) * 255          # tele mimo tělo krávy
calf = np.maximum(calf, outside)
cm = Image.fromarray(calf).filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.MinFilter(15))
cm = C.keep_largest(cm)
# vyplnit díry (bílé tele na bílé krávě se od sebe neliší)
from PIL import ImageDraw, ImageOps
inv = ImageOps.invert(cm).copy(); ImageDraw.floodfill(inv, (0, 0), 0)
cm = Image.fromarray(np.maximum(np.asarray(cm), np.asarray(inv)))
calf = np.minimum(np.asarray(cm, dtype=np.float32) / 255, mA)
pad = 60; W, H = w + 2 * pad, h + 2 * pad
def piece(img, mask, seed):
    M = Image.new('L', (W, H), 0); M.paste(Image.fromarray((np.clip(mask, 0, 1) * 255).astype(np.uint8)), (pad, pad))
    rgb = np.zeros((H, W, 3), dtype=np.float32) + (243, 233, 227) + (C.noise(W, H, 2, seed + 9)[..., None] - 0.5) * 14
    paper = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert('RGBA'); paper.putalpha(C.torn_edge(M, a.border, seed))
    cv = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cv.alpha_composite(paper)
    ph = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ph.paste(img, (pad, pad)); ph.putalpha(M)
    cv.alpha_composite(ph); return cv
P = piece(A, mA, 101); M_ = piece(B, mB, 102); T = piece(A, calf, 103)
bb = P.getbbox()
for name, im in (('par', P), ('mama', M_), ('tele', T)):
    im.crop(bb).save(os.path.join(a.out, f'{a.prefix}{name}.png'))
T.crop(T.getbbox()).save(os.path.join(a.out, f'{a.prefix}tele-samostatne.png'))
M_.crop(M_.getbbox()).save(os.path.join(a.out, f'{a.prefix}mama-samostatne.png'))
print('plátno', P.crop(bb).size)
