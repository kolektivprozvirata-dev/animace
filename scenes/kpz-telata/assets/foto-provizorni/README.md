# Provizorní fotky (jen náhled – nahradit fotkami KPZ)

Fotobanky jsou z prostředí blokované, proto fotky z veřejných datasetů na Hugging Face:
- **Unsplash** (licence Unsplash) – kopie v `wtcherr/unsplash_20k`,
- **COCO 2017** (fotky z Flickru, licence CC dle jednotlivých fotek) – kopie v `Multimodal-Fatima/COCO_captions_train`.

Úpravy: ušní známky rozmazané, ořez, zvětšeno 2× (originály mají 512–640 px → ve videu měkké).
**Pravidlo KPZ: zvířata ve výstřižcích vždy celá – žádné useknuté půlky těla.**

| soubor | zdroj (soubor_rowgroup_řádek) | popis | kde ve videu |
|---|---|---|---|
| tele-saje.jpg | COCO 00006_0_0887 | tele saje u matky na pastvě | úvod („začíná porodem“) |
| tele-samo.jpg | Unsplash 00000_0_727 | tele v dece samo v hale | „samo v boxu“ (v kreslené boudě) |
| hala-krmeni.jpg | Unsplash 00000_0_865 | krávy u krmného žlabu v hale | hygiena – utržený kus fotky haly |
| pastva-stado-telata.jpg | COCO 00028_0_0690 | krávy s telaty na pastvině | hygiena – utržený kus fotky |
| pastva-matka-telata.jpg | COCO 00011_1_0183 | kráva (galloway) se dvěma telaty | zalehnutí – na kreslené pastvě |
| tele-olizuje-matku.jpg | COCO 00032_2_0091 | tele olizuje ležící matku | pouto |

## Výstřižky (`vystrizky/`)

Zvířata vystřižená s okrajem z utrženého papíru, prostředí jako utržený kus fotky:

    python3 .claude/skills/vox-animation/scripts/cutout.py tele-saje.jpg vystrizky/tele-saje.png
    python3 .claude/skills/vox-animation/scripts/cutout.py hala-krmeni.jpg vystrizky/hala-krmeni.png --piece --crop 0,380,1024,1110

Po výměně za fotky KPZ stačí výstřižky vyrobit znovu (známky rozmazat předem).
