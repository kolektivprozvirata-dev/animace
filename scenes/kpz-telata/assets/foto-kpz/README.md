# Fotky KPZ (dodané 2026-10-19)

Originály bez úprav (známky se nerozmazávají – pokyn KPZ). Výstřižky v `vystrizky/`
vyrobené `.claude/skills/vox-animation/scripts/cutout.py`.

| soubor | popis | použití ve videu |
|---|---|---|
| telata-boudy-detail.jpg | telata v plastových boudách s ohrádkami (detail) | výstřižek `tele-kpz.png` (varianta A), kus `bouda-s-teletem-kus.png` (varianta B) |
| telata-boudy-rada.jpg | řada bud s telaty z dronu | kus `telata-boudy-rada.png` (varianta C) |
| farma-z-vysky.jpg | farma z výšky: sila, haly, řady bud | kus `farma-z-vysky.png` (varianta D) |
| kravin-uvnitr.jpg | krávy ležící ve slámě v hale | kus `kravin-uvnitr.png` – hygiena, „velkokapacitní hala“ |
| kravin-vrata.jpg | krávy za vraty velké haly | zatím nepoužito (rezerva: zalehnutí / bizarní kruh) |
| krava-s-teletem.jpg | kráva a sající tele na pastvě (našli KPZ, 612 px; práva k fotce ověřit před zveřejněním) | výstřižek `krava-s-teletem.png` – úvod („začíná porodem“) |

Příkazy:

    S=.claude/skills/vox-animation/scripts/cutout.py
    python3 $S telata-boudy-detail.jpg vystrizky/tele-kpz.png --crop 420,280,760,720 --scale 2 --largest
    python3 $S bouda-s-teletem.jpg vystrizky/bouda-s-teletem-kus.png --piece
    python3 $S telata-boudy-rada.jpg vystrizky/telata-boudy-rada.png --piece --crop 380,60,2000,1125
    python3 $S kravin-uvnitr.jpg vystrizky/kravin-uvnitr.png --piece --crop 260,240,1700,1080
    python3 $S farma-z-vysky.jpg vystrizky/farma-z-vysky.png --piece --crop 430,150,1530,920
    python3 $S krava-s-teletem.jpg vystrizky/krava-s-teletem.png --crop 60,90,560,395 --scale 2 --largest
