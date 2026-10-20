"""Kráva s teletem jako dva papírové výstřižky: tele „vytržené“ z fotky (stejné plátno → sedí na sebe)."""
import sys, numpy as np
sys.path.insert(0, '/home/user/animace/.claude/skills/vox-animation/scripts')
import cutout as C
from PIL import Image, ImageDraw, ImageFilter
src, out_dir = sys.argv[1], sys.argv[2]
crop, scale, pad = (60, 90, 560, 395), 2, 60
poly = [(176,268),(186,250),(205,238),(228,232),(245,232),(270,222),(300,212),(340,203),(380,195),(420,193),(440,200),(452,215),(455,245),(452,280),(450,310),(447,340),(449,385),(435,390),(425,385),(420,345),(418,310),(405,300),(370,298),(330,300),(300,305),(292,330),(285,385),(262,390),(255,385),(262,340),(265,310),(250,300),(225,290),(200,282),(185,278)]
im = Image.open(src).convert('RGB').crop(crop)
im = im.resize((im.width * scale, im.height * scale), Image.LANCZOS)
w, h = im.size
a = C.keep_largest(C.matte(im))
pm = Image.new('L', (w, h), 0)
ImageDraw.Draw(pm).polygon([((x - crop[0]) * scale, (y - crop[1]) * scale) for x, y in poly], fill=255)
pm = pm.filter(ImageFilter.MaxFilter(5))
A = np.asarray(a, dtype=np.float32) / 255; P = np.asarray(pm, dtype=np.float32) / 255
# hrana trhu: nepravidelná (šum), aby nebyla vidět rovná čára polygonu
n = C.noise(w, h, 10, 81)
Pt = (np.asarray(pm.filter(ImageFilter.GaussianBlur(6)), dtype=np.float32) / 255 > 0.35 + 0.3 * (n - 0.5)).astype(np.float32)
calf = A * Pt; calf = np.asarray(C.keep_largest(Image.fromarray((calf * 255).astype(np.uint8))), dtype=np.float32) / 255; cow = A * (1 - Pt); cow = np.asarray(C.keep_largest(Image.fromarray((cow * 255).astype(np.uint8))), dtype=np.float32) / 255
W, H = w + 2 * pad, h + 2 * pad
def piece(mask, seed, name):
    M = Image.new('L', (W, H), 0); M.paste(Image.fromarray((mask * 255).astype(np.uint8)), (pad, pad))
    rgb = np.zeros((H, W, 3), dtype=np.float32) + (243, 233, 227) + (C.noise(W, H, 2, seed + 9)[..., None] - 0.5) * 14
    paper = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert('RGBA'); paper.putalpha(C.torn_edge(M, 22, seed))
    cv = Image.new('RGBA', (W, H), (0, 0, 0, 0)); cv.alpha_composite(paper)
    ph = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ph.paste(im, (pad, pad)); ph.putalpha(M)
    cv.alpha_composite(ph); return cv
cow_p, calf_p = piece(cow, 91, 'cow'), piece(calf, 92, 'calf')
bb = Image.alpha_composite(cow_p, calf_p).getbbox()
cow_p.crop(bb).save(f'{out_dir}/trh-krava.png'); calf_p.crop(bb).save(f'{out_dir}/trh-tele.png')
# samostatné ořezy pro řádky „→ Jatka“
cow_p.crop(cow_p.getbbox()).save(f'{out_dir}/trh-krava-samostatne.png'); calf_p.crop(calf_p.getbbox()).save(f'{out_dir}/trh-tele-samostatne.png')
print(bb, cow_p.crop(bb).size)
