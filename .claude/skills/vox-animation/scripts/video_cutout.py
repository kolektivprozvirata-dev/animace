#!/usr/bin/env python3
"""
video_cutout.py — krátký úsek videa jako utržený papírový kus (stejný styl jako cutout.py --shape blob).

  python3 video_cutout.py klip.mp4 out_dir/ --start 0.5 --dur 7.4 --crop 0,240,540,720 --size 600x800 [--seed 81] [--tight 0.6]

Výstup do out_dir/:
  f001.jpg …   snímky výřezu (12 fps = animFps scény, bez zvuku), velikost --size
  paper.png    papír s utrženým okrajem (pod snímky), plátno = size + 2×pad
  mask.png     maska tvaru (bílá s alfou) pro CSS mask-image nad snímky
  meta.json    {fps, frames, w, h, pad, W, H}

Ve scéně: <div class="kpz-cut kpz-vid" id="…" style="width:<W>px"><img src="…/paper.png"><canvas class="vidc"></canvas></div>
a v VOX.scene vykreslit snímek do canvasu (viz scenes/kpz-telata/reel-kpz-foto.html → vidCut()).
"""
import argparse, json, os, subprocess, sys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cutout import blob_mask, torn_edge, noise  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('out')
    ap.add_argument('--start', type=float, default=0); ap.add_argument('--dur', type=float, required=True)
    ap.add_argument('--crop', default=None, help='x,y,w,h ve zdrojovém videu')
    ap.add_argument('--size', default='600x800'); ap.add_argument('--fps', type=float, default=12)
    ap.add_argument('--seed', type=int, default=81); ap.add_argument('--tight', type=float, default=0.6)
    ap.add_argument('--pad', type=int, default=60); ap.add_argument('--border', type=int, default=26)
    a = ap.parse_args()
    w, h = (int(v) for v in a.size.split('x'))
    os.makedirs(a.out, exist_ok=True)
    for f in os.listdir(a.out):
        if f.startswith('f') and f.endswith('.jpg'): os.remove(os.path.join(a.out, f))
    crop = ''
    if a.crop:
        x, y, cw, ch = a.crop.split(',')
        crop = f'crop={cw}:{ch}:{x}:{y},'   # ffmpeg chce w:h:x:y
    vf = crop + f'scale={w}:{h}:flags=lanczos,fps={a.fps}'
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-ss', str(a.start), '-t', str(a.dur),
                    '-i', a.src, '-an', '-vf', vf, '-q:v', '3', os.path.join(a.out, 'f%03d.jpg')], check=True)
    frames = len([f for f in os.listdir(a.out) if f.startswith('f') and f.endswith('.jpg')])
    A0 = blob_mask(w, h, a.seed, a.tight)
    W, H = w + 2 * a.pad, h + 2 * a.pad
    A = Image.new('L', (W, H), 0); A.paste(A0, (a.pad, a.pad))
    rgb = np.zeros((H, W, 3), dtype=np.float32) + (243, 233, 227) + (noise(W, H, 2, a.seed + 9)[..., None] - 0.5) * 14
    paper = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert('RGBA')
    paper.putalpha(torn_edge(A, a.border, a.seed)); paper.save(os.path.join(a.out, 'paper.png'))
    m = Image.new('RGBA', (w, h), (255, 255, 255, 0)); m.putalpha(A0); m.save(os.path.join(a.out, 'mask.png'))
    meta = {'fps': a.fps, 'frames': frames, 'w': w, 'h': h, 'pad': a.pad, 'W': W, 'H': H}
    json.dump(meta, open(os.path.join(a.out, 'meta.json'), 'w'))
    print(a.out, meta)


if __name__ == '__main__':
    main()
