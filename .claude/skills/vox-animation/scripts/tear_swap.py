#!/usr/bin/env python3
"""
„Vytržení“ telete se dvěma fotkami: A = máma s teletem, B = stejná máma bez telete
(zarovnané, stejná velikost; s průhledným pozadím je maska přesnější). Vyrobí 3 výstřižky na stejném plátně:
  par.png (A celé) · mama.png (B – kráva celá) · tele.png (jen tele z A)
Ve scéně: do trhu ukázat par.png, při trhu ho schovat a ukázat mama.png + tele.png (tele odjede).

  python3 tear_swap.py A.jpg B.jpg out_dir [--prefix trh2-] [--scale 0.66] [--cut x,y,x,y,…] [--debug maska.png]
"""
import argparse, os, sys, numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
import cutout as C

ap = argparse.ArgumentParser()
ap.add_argument('a'); ap.add_argument('b'); ap.add_argument('out')
ap.add_argument('--prefix', default='trh2-'); ap.add_argument('--scale', type=float, default=0.66)
ap.add_argument('--border', type=int, default=22); ap.add_argument('--thr', type=int, default=30)
ap.add_argument('--open', type=int, default=11, help='otevření masky – smaže tenké proužky na obrysu krávy (lichá px)')
ap.add_argument('--cut', action='append', default=[], help='x,y,x,y,… polygon v px fotky A, který z telete vyřízne (např. nohy krávy za teletem)')
ap.add_argument('--debug', help='uložit náhled masky telete přes fotku A (na úpravu --cut)')
a = ap.parse_args()
def load(path, size=None):
    """RGB na bílé + maska: průhledné pozadí (PNG/WebP) = hotová maska, jinak BiRefNet."""
    im = Image.open(path)
    if size: im = im.resize(size, Image.LANCZOS)
    if a.scale != 1 and size is None: im = im.resize((int(im.width * a.scale), int(im.height * a.scale)), Image.LANCZOS)
    if im.mode in ('RGBA', 'LA', 'P') and im.convert('RGBA').getextrema()[3][0] < 250:
        im = im.convert('RGBA'); rgb = Image.new('RGB', im.size, (255, 255, 255)); rgb.paste(im, mask=im.split()[3])
        return rgb, C.keep_largest(im.split()[3])
    rgb = im.convert('RGB'); return rgb, C.keep_largest(C.matte(rgb))
A, mA = load(a.a); B, mB = load(a.b, A.size)
w, h = A.size
mA = np.asarray(mA, dtype=np.float32) / 255; mB = np.asarray(mB, dtype=np.float32) / 255
diff = np.abs(np.asarray(A, dtype=np.float32) - np.asarray(B, dtype=np.float32)).max(axis=2)
calf = ((diff > a.thr) & (mA > 0.5)).astype(np.uint8) * 255
outside = ((mA > 0.5) & (mB < 0.5)).astype(np.uint8) * 255          # tele mimo tělo krávy
calf = np.maximum(calf, outside)
cm = Image.fromarray(calf).filter(ImageFilter.MedianFilter(5))
if a.open > 1:   # obrys krávy se mezi fotkami o pixel posune → tenké proužky v rozdílu; otevření je smaže
    cm = cm.filter(ImageFilter.MinFilter(a.open)).filter(ImageFilter.MaxFilter(a.open))
cm = cm.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.MinFilter(15))
cm = C.keep_largest(cm)
# vyplnit díry (bílé tele na bílé krávě se od sebe neliší)
from PIL import ImageDraw, ImageOps
inv = ImageOps.invert(cm).copy(); ImageDraw.floodfill(inv, (0, 0), 0)
cm = Image.fromarray(np.maximum(np.asarray(cm), np.asarray(inv)))
if a.cut:   # ruční oprava: části krávy, které generátor u druhé fotky překreslil (rozdíl je i mimo tele)
    k = a.scale; cd = ImageDraw.Draw(cm)
    for poly in a.cut:
        v = [float(x) * k for x in poly.split(',')]; cd.polygon(list(zip(v[0::2], v[1::2])), fill=0)
    cm = C.keep_largest(cm)
calf = np.minimum(np.asarray(cm, dtype=np.float32) / 255, mA)
if a.debug:
    dbg = np.asarray(A, dtype=np.float32) * 0.45; dbg[..., 0] += calf * 140; dbg[..., 1] += (mA - calf).clip(0, 1) * 60
    Image.fromarray(dbg.clip(0, 255).astype(np.uint8)).resize((int(w / a.scale), int(h / a.scale))).save(a.debug)
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
