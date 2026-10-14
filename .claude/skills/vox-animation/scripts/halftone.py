#!/usr/bin/env python3
"""
halftone.py — připraví fotku do Vox koláže: černobílá / duotón + skutečný
rastr (halftone) a zachování průhlednosti u vyříznutých PNG.

  python3 halftone.py vstup.jpg vystup.png [--cell 8] [--angle 45]
                      [--ink "#141414"] [--paper none|"#f3eee4"]
                      [--duotone "#2f6db5"] [--contrast 1.3] [--mix 1.0]

  --cell     velikost rastrové buňky v px (menší = jemnější; 6–10 pro FullHD)
  --angle    úhel rastru (klasika 45°)
  --ink      barva teček
  --paper    barva podkladu; "none" = průhledné (pro výřezy na papír ve scéně)
  --duotone  místo čistého halftone obarví střední tóny touto barvou
  --mix      0..1 – kolik halftonu smíchat s plynulou šedou (1 = jen tečky)
"""
import argparse
import math

from PIL import Image, ImageDraw, ImageEnhance, ImageOps


def hex_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def halftone_mask(gray, cell, angle):
    """Vrátí masku L (255 = inkoust) s kulatými tečkami podle jasu."""
    w, h = gray.size
    diag = int(math.hypot(w, h)) + cell * 2
    # otočíme obraz, rastrujeme v pravoúhlé mřížce, otočíme zpět
    big = Image.new('L', (diag, diag), 255)
    big.paste(gray, ((diag - w) // 2, (diag - h) // 2))
    rot = big.rotate(angle, resample=Image.BICUBIC, fillcolor=255)
    small = rot.resize((diag // cell, diag // cell), Image.BOX)
    scale = 4  # supersampling pro hladké tečky
    mask = Image.new('L', (diag * scale, diag * scale), 0)
    d = ImageDraw.Draw(mask)
    px = small.load()
    for j in range(small.size[1]):
        for i in range(small.size[0]):
            darkness = 1 - px[i, j] / 255
            r = cell * scale * 0.5 * math.sqrt(darkness) * 1.42
            if r < 0.6:
                continue
            cx = (i + 0.5) * cell * scale
            cy = (j + 0.5) * cell * scale
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
    mask = mask.resize((diag, diag), Image.LANCZOS)
    mask = mask.rotate(-angle, resample=Image.BICUBIC, fillcolor=0)
    left, top = (diag - w) // 2, (diag - h) // 2
    return mask.crop((left, top, left + w, top + h))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('dst')
    ap.add_argument('--cell', type=int, default=8)
    ap.add_argument('--angle', type=float, default=45)
    ap.add_argument('--ink', default='#141414')
    ap.add_argument('--paper', default='none')
    ap.add_argument('--duotone', default=None)
    ap.add_argument('--contrast', type=float, default=1.3)
    ap.add_argument('--mix', type=float, default=1.0)
    a = ap.parse_args()

    img = Image.open(a.src)
    img = ImageOps.exif_transpose(img).convert('RGBA')
    alpha = img.getchannel('A')
    gray = ImageOps.grayscale(img.convert('RGB'))
    gray = ImageEnhance.Contrast(gray).enhance(a.contrast)

    dots = halftone_mask(gray, a.cell, a.angle)
    if a.mix < 1:
        smooth = ImageOps.invert(gray)
        dots = Image.blend(smooth, dots, a.mix)

    ink = Image.new('RGB', img.size, hex_rgb(a.ink))
    if a.duotone:
        # duotón: podklad = barva tónovaná jasem, tečky = inkoust
        base = ImageOps.colorize(gray, black=hex_rgb(a.duotone), white='#f3eee4')
        out = Image.composite(ink, base, dots).convert('RGBA')
        out.putalpha(alpha)
    elif a.paper == 'none':
        out = ink.convert('RGBA')
        out.putalpha(Image.composite(dots, Image.new('L', img.size, 0), alpha))
    else:
        base = Image.new('RGB', img.size, hex_rgb(a.paper))
        out = Image.composite(ink, base, dots).convert('RGBA')
        out.putalpha(alpha)

    out.save(a.dst)
    print('halftone →', a.dst)


if __name__ == '__main__':
    main()
