# Fotky KPZ (dodané 2026-10-19)

Na ušních známkách rozostřená jen samotná čísla (`scripts/tag_retouch.py --rect`, pokyn KPZ).
Výstřižky v `vystrizky/` vyrobené `.claude/skills/vox-animation/scripts/cutout.py`.

| soubor | popis | použití ve videu |
|---|---|---|
| telata-boudy-detail.jpg | telata v plastových boudách s ohrádkami (detail) | výstřižek `tele-kpz.png` (varianta A), kus `bouda-s-teletem-kus.png` (varianta B) |
| telata-boudy-rada.jpg | řada bud s telaty z dronu | kus `telata-boudy-rada.png` (varianta C) |
| farma-z-vysky.jpg | farma z výšky: sila, haly, řady bud | kus `farma-z-vysky.png` (varianta D) |
| kravin-uvnitr.jpg | krávy ležící ve slámě v hale | kus `kravin-uvnitr.png` – hygiena, „velkokapacitní hala“ |
| kravin-vrata.jpg | krávy za vraty velké haly | zatím nepoužito (rezerva: zalehnutí / bizarní kruh) |
| krava-s-teletem.jpg | kráva a sající tele na pastvě (našli KPZ, 612 px; práva k fotce ověřit před zveřejněním; číslo na známce nečitelné – bez úprav) | výstřižek `krava-s-teletem.png` – úvod („začíná porodem“) |
| tele-studio.jpg | tele celé na bílém pozadí, žluté známky bez čísel (KPZ, 2026-10-19) | výstřižek `tele-studio.png` – do v7 do boudy (0:18) |
| masny-skot.jpg | čtyři kusy tzv. masného skotu na pastvě (růžové známky) | utržený kus `masny-skot.png` – hygiena, „tzv. masné krávy na pastvě“ |

Příkazy (známky – originály 25.jpg / 26.jpg / 30.webp ze zpráv KPZ):

    T=.claude/skills/vox-animation/scripts/tag_retouch.py
    python3 $T 26.jpg telata-boudy-detail.jpg --rect 506,388,544,416 --rect 614,376,648,400 --rect 945,530,976,565 --rect 1086,530,1120,560 --rect 2,525,22,552 --rect 1474,394,1500,420
    python3 $T 25.jpg kravin-uvnitr.jpg --rect 400,712,458,764 --rect 694,684,748,740 --rect 251,513,272,534 --rect 369,508,386,529 --rect 1233,510,1250,555 --rect 1756,663,1777,688 --rect 1783,725,1800,748 --rect 1019,467,1044,488
    python3 $T 30.webp masny-skot.jpg --noclip --rect 196,186,212,198 --rect 325,186,340,200 --rect 391,172,415,185 --rect 515,172,535,188 --rect 622,208,640,222 --rect 748,210,768,224 --rect 830,214,848,230 --rect 945,228,965,242

Výstřižky:

    S=.claude/skills/vox-animation/scripts/cutout.py
    python3 $S telata-boudy-detail.jpg vystrizky/tele-kpz.png --crop 420,280,760,720 --scale 2 --largest
    python3 $S bouda-s-teletem.jpg vystrizky/bouda-s-teletem-kus.png --piece
    python3 $S telata-boudy-rada.jpg vystrizky/telata-boudy-rada.png --piece --crop 380,60,2000,1125
    python3 $S kravin-uvnitr.jpg vystrizky/kravin-uvnitr.png --piece --crop 260,240,1700,1080
    python3 $S farma-z-vysky.jpg vystrizky/farma-z-vysky.png --piece --crop 430,150,1530,920
    python3 $S krava-s-teletem.jpg vystrizky/krava-s-teletem.png --crop 60,90,560,395 --scale 2 --largest
    python3 $S masny-skot.jpg vystrizky/masny-skot.png --piece --crop 70,60,1060,600 --scale 1.5
    python3 $S tele-studio.jpg vystrizky/tele-studio.png --largest
