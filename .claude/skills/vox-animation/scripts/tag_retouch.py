#!/usr/bin/env python3
"""
Zakrytí čísel na ušních známkách: text ve známce se přebarví barvou známky
(známka zůstane vidět, jen bez čísel – nesvítí jako rozmazaný flek).

  python3 tag_retouch.py foto.jpg out.jpg                 # automaticky najde žluté známky
  python3 tag_retouch.py foto.jpg out.jpg --box 488,360,556,436 --box ...   # jen dané oblasti
  volby: --debug náhled.png (zvýrazní nalezené známky)

Známka = největší žlutá plocha v oblasti; text = vše tmavší / nežluté uvnitř jejího obrysu.
Text se vyplní místní barvou známky. Venku (tráva) zadávej oblasti ručně --box.
"""
import argparse
import numpy as np
from PIL import Image, ImageFilter, ImageDraw


def yellow_mask(arr):
    r, g, b = arr[..., 0].astype(int), arr[..., 1].astype(int), arr[..., 2].astype(int)
    # žlutá známka: R ≈ G, obojí vysoko, B nízko (tráva má G výrazně nad R → nevezme se)
    return (r > 140) & (g > 115) & (b < 120) & (r - b > 75) & (g - b > 55) & (r >= g - 18)


def components(mask, min_px):
    from collections import deque
    h, w = mask.shape; seen = np.zeros_like(mask, bool); boxes = []
    ys, xs = np.nonzero(mask)
    for y0, x0 in zip(ys, xs):
        if seen[y0, x0]: continue
        q = deque([(y0, x0)]); seen[y0, x0] = True; pts = []
        while q:
            y, x = q.popleft(); pts.append((y, x))
            for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True; q.append((ny, nx))
        if len(pts) >= min_px:
            py, px = zip(*pts); boxes.append((int(min(px)), int(min(py)), int(max(px)) + 1, int(max(py)) + 1))
    return boxes


def convex_hull(points):
    """Konvexní obal (monotone chain)."""
    pts = sorted(set(points))
    if len(pts) <= 2: return pts
    cross = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0: lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0: upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def box_blur(a, r):
    """Rychlé rozmazání čtvercem (2× za sebou ≈ Gauss), funguje i pro float pole."""
    r = max(1, int(r)); p = np.pad(a, r, mode='edge')
    c = np.cumsum(np.cumsum(p, 0), 1); c = np.pad(c, ((1, 0), (1, 0)))
    n = 2 * r + 1; h, w = a.shape
    return (c[n:n + h, n:n + w] - c[:h, n:n + w] - c[n:n + h, :w] + c[:h, :w]) / (n * n)


def retouch_box(img, box, close=None):
    x0, y0, x1, y1 = box
    reg = img.crop(box); arr = np.asarray(reg).astype(np.float32)
    hsv = np.asarray(reg.convert('HSV')).astype(int)
    # žlutý odstín (známka i rozmazaná tištěná čísla mají stejný odstín, liší se jasem)
    hue = (hsv[..., 0] >= 22) & (hsv[..., 0] <= 52) & (hsv[..., 1] > 95) & (hsv[..., 2] > 70)
    if hue.sum() < 10: return 0
    # největší souvislá žlutá plocha = známka (ne ucho, ne sláma)
    comps = components(hue, 10)
    if not comps: return 0
    def area(b): return int(hue[b[1]:b[3], b[0]:b[2]].sum())
    cb = max(comps, key=area)
    core = np.zeros_like(hue); core[cb[1]:cb[3], cb[0]:cb[2]] = hue[cb[1]:cb[3], cb[0]:cb[2]]
    pts = np.argwhere(core)[:, ::-1]
    hull = convex_hull([tuple(map(int, p)) for p in pts])
    if len(hull) < 3: return 0
    hm = Image.new('L', reg.size, 0); ImageDraw.Draw(hm).polygon(hull, fill=255)
    inside = np.asarray(hm.filter(ImageFilter.MinFilter(3))) > 0
    v = hsv[..., 2]
    ref = np.percentile(v[inside & hue], 80)
    clean = inside & hue & (v >= 0.92 * ref)          # čistá plocha známky
    text = inside & ~clean                            # čísla, písmena, stíny písma
    if text.sum() == 0: return 0
    k = int(close or max(3, int(min(x1 - x0, y1 - y0)) // 6))
    blur = lambda a2: box_blur(box_blur(a2.astype(np.float32), k), k)
    w = clean.astype(np.float32)
    fill = np.stack([blur(arr[..., c] * w) for c in range(3)], axis=-1) / (blur(w)[..., None] + 1e-4)
    tm = Image.fromarray((text * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3))
    soft = np.asarray(tm.filter(ImageFilter.GaussianBlur(0.7)), dtype=np.float32)[..., None] / 255.0
    soft *= inside[..., None]
    fill = fill + np.random.default_rng(x0 * 7 + y0).normal(0, 3.0, fill.shape[:2])[..., None]   # zrno fotky
    out = arr * (1 - soft) + fill * soft
    img.paste(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)), (x0, y0))
    return int(text.sum())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('out')
    ap.add_argument('--box', action='append', default=[])
    ap.add_argument('--min', type=int, default=60, help='min. velikost známky v px (auto režim)')
    ap.add_argument('--debug', default=None)
    a = ap.parse_args()
    img = Image.open(a.src).convert('RGB')
    if a.box:
        boxes = [tuple(int(v) for v in b.split(',')) for b in a.box]
    else:
        ym = Image.fromarray((yellow_mask(np.asarray(img)) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7))
        boxes = components(np.asarray(ym) > 0, a.min)   # rozšířeno, ať se známka rozdělená textem spojí
    pad = 4; done = []
    for (x0, y0, x1, y1) in boxes:
        b = (max(0, x0 - pad), max(0, y0 - pad), min(img.width, x1 + pad), min(img.height, y1 + pad))
        n = retouch_box(img, b)
        n += retouch_box(img, b)   # druhý průchod dočistí zbytky písma
        if n: done.append((b, n))
    img.save(a.out, quality=93)
    print(a.out, 'známek upraveno:', len(done), done)
    if a.debug:
        dbg = img.copy(); d = ImageDraw.Draw(dbg)
        for b, _ in done: d.rectangle(b, outline=(255, 0, 255), width=3)
        dbg.save(a.debug)


if __name__ == '__main__':
    main()
