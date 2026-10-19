#!/usr/bin/env python3
"""
Zakrytí čísel na ušních známkách. Výchozí (--mode blur): gaussovsky se rozostří jen
samotné písmo uvnitř známky – plocha i tvar známky zůstanou ostré (pokyn KPZ).
Barva známky: --hue lo,hi --sat (žlutá výchozí; růžová: --hue 235,14 --sat 40).
--mode fill: text se přebarví barvou známky (KPZ se nelíbilo – „nevypadá dobře“).

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


def component_masks(mask):
    from collections import deque
    h, w = mask.shape; seen = np.zeros_like(mask, bool); out = []
    for y0, x0 in zip(*np.nonzero(mask)):
        if seen[y0, x0]: continue
        m = np.zeros_like(mask, bool); q = deque([(y0, x0)]); seen[y0, x0] = True
        while q:
            y, x = q.popleft(); m[y, x] = True
            for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True; q.append((ny, nx))
        out.append(m)
    return out


def bbox(m):
    ys, xs = np.nonzero(m)
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


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


def hue_mask(hsv, hue=(24, 52), sat=95, val=70):
    """Barva známky v HSV (PIL 0–255). hue=(lo, hi); lo > hi = přes nulu (růžová: 235,14)."""
    h = hsv[..., 0]; lo, hi = hue
    hm = (h >= lo) & (h <= hi) if lo <= hi else (h >= lo) | (h <= hi)
    return hm & (hsv[..., 1] > sat) & (hsv[..., 2] > val)


def blur_box(img, box, radius=None, hue=(24, 52), sat=95):
    """Gaussovské rozostření jen samotného čísla/písma uvnitř známky – plocha známky zůstane ostrá."""
    x0, y0, x1, y1 = box
    reg = img.crop(box); hsv = np.asarray(reg.convert('HSV')).astype(int)
    tag = hue_mask(hsv, hue, sat)
    hi = Image.fromarray((tag * 255).astype(np.uint8))
    tag = np.asarray(hi.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))) > 0   # pryč drobná sláma
    # řádek textu dělí známku na části → spojit, vybrat největší a vzít jen její barevné px
    joined = np.asarray(Image.fromarray((tag * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(11))) > 0
    masks = component_masks(joined)
    if not masks: return 0
    core = max(masks, key=lambda m: int((m & tag).sum())) & tag
    if core.sum() < 8: return 0
    cb = bbox(core)
    hull = convex_hull([tuple(map(int, p)) for p in np.argwhere(core)[:, ::-1]])
    if len(hull) < 3: return 0
    hm = Image.new('L', reg.size, 0); ImageDraw.Draw(hm).polygon(hull, fill=255)
    inside = np.asarray(hm.filter(ImageFilter.MinFilter(3))) > 0
    # písmo = výrazně tmavší tahy uvnitř známky (ne stíny na známce)
    inner = np.asarray(hm.filter(ImageFilter.MinFilter(5))) > 0
    v = hsv[..., 2]; ref = np.percentile(v[core], 75)
    sat = hsv[..., 1]
    text = inner & ((v < 0.58 * ref) | ((v < 0.8 * ref) & (sat < 0.6 * np.median(sat[core]))))   # černý tisk, ne stín na známce
    text = np.asarray(Image.fromarray((text * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(3))) > 0
    if text.sum() < 4: return 0
    tx0, ty0, tx1, ty1 = bbox(text)
    r = radius or float(np.clip((ty1 - ty0) / 7, 1.5, 3.5))
    arr = np.asarray(reg).astype(np.float32)
    tag_col = np.median(arr[core], axis=0)
    base = np.where(inside[..., None], arr, tag_col)          # do rozostření nezatéká okolí (ucho, srst)
    bl = np.asarray(Image.fromarray(base.astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))).astype(np.float32)
    # rozostřit jen obdélník kolem čísla (se změkčeným okrajem), nikdy ven ze známky
    rm = Image.new('L', reg.size, 0); ImageDraw.Draw(rm).rectangle((tx0 - 2, ty0 - 2, tx1 + 1, ty1 + 1), fill=255)
    rm = rm.filter(ImageFilter.GaussianBlur(1.2))
    m = (np.asarray(rm, dtype=np.float32) / 255.0 * inside)[..., None]
    out = arr * (1 - m) + bl * m
    img.paste(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)), (x0, y0))
    return int(text.sum())


def blur_rect(img, rect, radius=None, hue=(24, 52), sat=95, clip=True):
    """Rozostří obdélník čísla. clip=True: jen tam, kde je plocha známky (barva --hue) –
    rozostření nepřeteče na ucho a do okolí; když se známka nenajde, rozostří celý obdélník."""
    x0, y0, x1, y1 = rect; pad = 6
    box = (x0 - pad, y0 - pad, x1 + pad, y1 + pad)
    reg = img.crop(box); arr = np.asarray(reg).astype(np.float32)
    r = radius or float(np.clip(min(x1 - x0, y1 - y0) / 6, 1.5, 4))
    rm = Image.new('L', reg.size, 0); ImageDraw.Draw(rm).rounded_rectangle((pad, pad, pad + x1 - x0, pad + y1 - y0), radius=3, fill=255)
    m = np.asarray(rm.filter(ImageFilter.GaussianBlur(1.2)), dtype=np.float32) / 255.0
    base = arr
    if clip:
        hsv = np.asarray(reg.convert('HSV')).astype(int)
        tag = hue_mask(hsv, hue, sat)
        tag = np.asarray(Image.fromarray((tag * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))) > 0
        joined = np.asarray(Image.fromarray((tag * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9))) > 0
        masks = [mm for mm in component_masks(joined) if (mm & tag).sum() > 6]
        if masks:
            core = max(masks, key=lambda mm: int((mm & tag).sum())) & tag
            hull = convex_hull([tuple(map(int, p_)) for p_ in np.argwhere(core)[:, ::-1]])
            if len(hull) >= 3:
                hm = Image.new('L', reg.size, 0); ImageDraw.Draw(hm).polygon(hull, fill=255)
                inside = np.asarray(hm.filter(ImageFilter.MinFilter(3))) > 0
                if inside.sum() > 0.3 * (x1 - x0) * (y1 - y0):
                    tag_col = np.median(arr[core], axis=0)
                    base = np.where(inside[..., None], arr, tag_col)
                    m = m * np.asarray(hm.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8)), dtype=np.float32) / 255.0
    bl = np.asarray(Image.fromarray(base.astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))).astype(np.float32)
    out = arr * (1 - m[..., None]) + bl * m[..., None]
    img.paste(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)), box[:2])
    return (x1 - x0) * (y1 - y0)


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
    ap.add_argument('--box', action='append', default=[], help='oblast známky (číslo se najde samo)')
    ap.add_argument('--rect', action='append', default=[], help='přesný obdélník čísla k rozostření')
    ap.add_argument('--min', type=int, default=60, help='min. velikost známky v px (auto režim)')
    ap.add_argument('--debug', default=None)
    ap.add_argument('--mode', choices=['blur', 'fill'], default='blur',
                    help='blur = rozostřit číslo uvnitř známky (výchozí, KPZ), fill = přebarvit barvou známky')
    ap.add_argument('--radius', type=float, default=None, help='síla rozostření (px), výchozí ~1/14 známky')
    ap.add_argument('--hue', default='24,52', help='barva známky: HSV odstín lo,hi (PIL 0–255); růžová 235,14')
    ap.add_argument('--sat', type=int, default=95, help='min. sytost barvy známky (růžová ~40)')
    ap.add_argument('--noclip', action='store_true', help='--rect: rozostřit celý obdélník (malé známky, barva splývá se srstí)')
    a = ap.parse_args()
    img = Image.open(a.src).convert('RGB')
    for rc in a.rect:
        blur_rect(img, tuple(int(v) for v in rc.split(',')), a.radius,
                  tuple(int(v) for v in a.hue.split(',')), a.sat, clip=not a.noclip)
    if a.rect and not a.box:
        img.save(a.out, quality=93); print(a.out, 'čísel rozostřeno:', len(a.rect)); return
    if a.box:
        boxes = [tuple(int(v) for v in b.split(',')) for b in a.box]
    else:
        ym = Image.fromarray((yellow_mask(np.asarray(img)) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7))
        boxes = components(np.asarray(ym) > 0, a.min)   # rozšířeno, ať se známka rozdělená textem spojí
    pad = 4; done = []
    for (x0, y0, x1, y1) in boxes:
        b = (max(0, x0 - pad), max(0, y0 - pad), min(img.width, x1 + pad), min(img.height, y1 + pad))
        if a.mode == 'blur':
            n = blur_box(img, b, a.radius, tuple(int(v) for v in a.hue.split(',')), a.sat)
        else:
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
