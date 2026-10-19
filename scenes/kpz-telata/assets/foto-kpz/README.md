# Fotky KPZ (dodané 2026-10-19)

Čísla na ušních známkách přebarvená barvou známky (`scripts/tag_retouch.py`, pokyn KPZ – ne rozmazání).
Výstřižky v `vystrizky/` vyrobené `.claude/skills/vox-animation/scripts/cutout.py`.

| soubor | popis | použití ve videu |
|---|---|---|
| telata-boudy-detail.jpg | telata v plastových boudách s ohrádkami (detail) | výstřižek `tele-kpz.png` (varianta A), kus `bouda-s-teletem-kus.png` (varianta B) |
| telata-boudy-rada.jpg | řada bud s telaty z dronu | kus `telata-boudy-rada.png` (varianta C) |
| farma-z-vysky.jpg | farma z výšky: sila, haly, řady bud | kus `farma-z-vysky.png` (varianta D) |
| kravin-uvnitr.jpg | krávy ležící ve slámě v hale | kus `kravin-uvnitr.png` – hygiena, „velkokapacitní hala“ |
| kravin-vrata.jpg | krávy za vraty velké haly | zatím nepoužito (rezerva: zalehnutí / bizarní kruh) |
| krava-s-teletem.jpg | kráva a sající tele na pastvě (našli KPZ, 612 px; práva k fotce ověřit před zveřejněním) | výstřižek `krava-s-teletem.png` – úvod („začíná porodem“) |

Příkazy (známky – originály 25.jpg/26.jpg/29.png ze zprávy KPZ):

    T=.claude/skills/vox-animation/scripts/tag_retouch.py
    python3 $T 26.jpg telata-boudy-detail.jpg --box 488,360,556,436 --box 600,352,664,416 --box 928,496,992,584 --box 1068,504,1136,580 --box 0,515,25,560 --box 1470,385,1505,428
    python3 $T 25.jpg kravin-uvnitr.jpg --box 385,690,470,780 --box 680,665,760,760 --box 240,500,285,545 --box 358,495,400,540 --box 1025,455,1060,495 --box 1222,500,1262,565 --box 1748,650,1790,695 --box 1775,712,1812,760
    python3 $T 29.png krava-s-teletem.jpg --box 425,118,452,146

Výstřižky:

    S=.claude/skills/vox-animation/scripts/cutout.py
    python3 $S telata-boudy-detail.jpg vystrizky/tele-kpz.png --crop 420,280,760,720 --scale 2 --largest
    python3 $S bouda-s-teletem.jpg vystrizky/bouda-s-teletem-kus.png --piece
    python3 $S telata-boudy-rada.jpg vystrizky/telata-boudy-rada.png --piece --crop 380,60,2000,1125
    python3 $S kravin-uvnitr.jpg vystrizky/kravin-uvnitr.png --piece --crop 260,240,1700,1080
    python3 $S farma-z-vysky.jpg vystrizky/farma-z-vysky.png --piece --crop 430,150,1530,920
    python3 $S krava-s-teletem.jpg vystrizky/krava-s-teletem.png --crop 60,90,560,395 --scale 2 --largest
