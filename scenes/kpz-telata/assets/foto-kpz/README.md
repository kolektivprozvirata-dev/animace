# Fotky KPZ (dodané 2026-10-19)

Na ušních známkách rozostřená jen samotná čísla (`scripts/tag_retouch.py --rect`, pokyn KPZ).
Výstřižky v `vystrizky/` vyrobené `.claude/skills/vox-animation/scripts/cutout.py`.

| soubor | popis | použití ve videu |
|---|---|---|
| telata-boudy-detail.jpg | telata v plastových boudách s ohrádkami (detail) | výstřižek `tele-kpz.png` (varianta A), kus `bouda-s-teletem-kus.png` (varianta B) |
| telata-boudy-rada.jpg | řada bud s telaty z dronu | kus `telata-boudy-rada.png` (varianta C) |
| farma-z-vysky.jpg | farma z výšky: sila, haly, řady bud | kus `farma-z-vysky.png` (varianta D); ořez jen na řady bud `boudy-z-vysky.png` (do v7) |
| kravin-uvnitr.jpg | krávy ležící ve slámě v hale | kus `kravin-uvnitr.png` – hygiena, „velkokapacitní hala“ |
| kravin-vrata.jpg | krávy za vraty velké haly | zatím nepoužito (rezerva: zalehnutí / bizarní kruh) |
| krava-s-teletem.jpg | kráva a sající tele na pastvě (našli KPZ, 612 px; práva k fotce ověřit před zveřejněním; číslo na známce nečitelné – bez úprav) | výstřižek `krava-s-teletem.png` – úvod („začíná porodem“) |
| tele-studio.jpg | tele celé na bílém pozadí, žluté známky bez čísel (KPZ, 2026-10-19) | výstřižek `tele-studio.png` – do v7 do boudy (0:18) |
| pastva-stado.jpg | stádo na pastvině, v trávě ležící telata (KPZ, 745 px) | utržený kus `pastva-stado.png` – do v7 v 1:10 (zalehnutí, pastva) |
| pouto-krava-tele.jpg | holštýnka se sajícím teletem, bílé pozadí (KPZ, 2026-10-20) | výstřižek `pouto-krava-tele.png` – do v8 scéna pouto |
| masny-skot.jpg | čtyři kusy tzv. masného skotu na pastvě (růžové známky) | utržený kus `masny-skot.png` – hygiena, „tzv. masné krávy na pastvě“ |
| krava-tele-hol.webp | holštýnka s kojícím teletem, průhledné pozadí (KPZ 35.webp, 2026-10-21; práva ověřit) | `trh2-par.png` – v11 úvod (0–4 s) a hook před vytržením |
| krava-sama-hol.webp | stejná kráva bez telete, srovnaná s předchozí (KPZ 36.webp) | `trh2-mama.png` (celá kráva) + `trh2-tele.png` – v11 vytržení (0:09–0:11) |
| krava-tele-lezi.jpg | holštýnka, pod ní ležící tele („další kráva“, KPZ 38.webp, 2026-10-21; známky bez čísel) | výstřižek `krava-tele-lezi.png` – v11 přebytek mléka (~1:41, „pro tele“) |
| krava-cele-telo.jpg | holštýnka celá z boku („Celé tělo“, KPZ; známky bez čísel) | výstřižek `krava-cele-telo.png` – v11 řádek „Tzv. dojnice → jatka“ |
| tele-ruzove.jpg | tele (býček) s růžovými známkami bez čísel („Růžové“, KPZ; původně průhledné pozadí → bílé) | výstřižek `tele-ruzove.png` – v11 řádek „Býčci → jatka“ |

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
    python3 $S farma-z-vysky.jpg vystrizky/boudy-z-vysky.png --piece --crop 610,370,1480,900
    python3 $S pastva-stado.jpg vystrizky/pastva-stado.png --piece --scale 1.6
    python3 $S masny-skot.jpg vystrizky/masny-skot-tvar.png --shape blob --seed 62 --crop 70,60,1060,600 --scale 1.5
    python3 $S pastva-stado.jpg vystrizky/pastva-stado-tvar.png --shape blob --seed 64 --scale 1.6
    python3 $S pouto-krava-tele.jpg vystrizky/pouto-krava-tele.png --largest

Vytržení ze dvou fotek (v11; kousky na společném plátně 1003×662, `-samostatne` = ořez na zvíře):

    python3 .claude/skills/vox-animation/scripts/tear_swap.py krava-tele-hol.webp krava-sama-hol.webp vystrizky --prefix trh2- \
        --cut 497,655,604,655,604,912,556,942,490,944,486,912,493,870   # přední nohy krávy za teletem
    python3 $S krava-cele-telo.jpg vystrizky/krava-cele-telo.png --largest
    python3 $S tele-ruzove.jpg vystrizky/tele-ruzove.png --largest
    python3 $S krava-tele-lezi.jpg vystrizky/krava-tele-lezi.png
