# Provizorní fotky (jen náhled – nahradit fotkami KPZ)

Fotobanky jsou z prostředí blokované, proto fotky z veřejného datasetu na Hugging Face:
**`xiannovoa/poultry-weight-dataset`** (licence MIT; fotky brojlerů při vážení, zřejmě pokusný chov).
Nejsou z českých hal a neukazují konec výkrmu – slouží jen k tomu, aby bylo vidět rozvržení záběrů.

| soubor | zdroj (řádek datasetu) | úprava | kde ve videu | čím nahradit (fotka KPZ) |
|---|---|---|---|---|
| kuratko-stoji.jpg → `vystrizky/kuratko-stoji.png` | 87 | výstřižek | růst – Den 1 | jednodenní kuře celé (výstřižek) |
| kuratko-cista-podestylka.jpg → `vystrizky/kuratko-cista-podestylka.png` | 93 | utržený kus | „fotka z haly“ – Den 1 (polaroid), pointa | **(a) malá kuřátka v čisté hale** |
| kure-velke-vaha.jpg → `vystrizky/kure-velke-vaha.png` | 30 | výstřižek i s váhou | růst – „kolem dvou kil“ | dospělé kuře (váha může zůstat) |
| kure-velke-vaha.jpg → `vystrizky/kure-velke.png` | 30 | výstřižek, váha vymaskovaná | důsledky – šipky chodidla / hlezna / hruď | **(d) dospělé kuře celé, vidět nohy** |
| kure-sedi-podestylka.jpg → `-upr.jpg` → `vystrizky/kure-sedi-tvar.png` | 65 | váha přemalovaná slámou, nepravidelný kus | hook + „leží většinu dne“ (záměrná návaznost) | **(c) kuře ležící v podestýlce na konci výkrmu** |
| — | — | — | hala (schéma shora, kresba) | **(b) hala na konci výkrmu** (utržený kus) |

Postup výstřižků:

    python3 .claude/skills/vox-animation/scripts/cutout.py kuratko-stoji.jpg vystrizky/kuratko-stoji.png --largest
    python3 .claude/skills/vox-animation/scripts/cutout.py kuratko-cista-podestylka.jpg vystrizky/kuratko-cista-podestylka.png --piece --crop 0,330,722,1330 --seed 3
    python3 .claude/skills/vox-animation/scripts/cutout.py kure-velke-vaha.jpg vystrizky/kure-velke-vaha.png --largest
    python3 .claude/skills/vox-animation/scripts/cutout.py kure-sedi-podestylka-upr.jpg vystrizky/kure-sedi-tvar.png --piece --shape blob --crop 470,110,1185,722 --seed 5

(`kure-velke.png`: matte z `cutout.py` s vymaskovanou plošinou váhy – nohy a kroužek ponechané podle barvy.)
