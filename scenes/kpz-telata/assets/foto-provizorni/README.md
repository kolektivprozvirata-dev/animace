# Provizorní fotky (jen náhled – nahradit fotkami KPZ)

Zdroj: fotky z Unsplash (licence Unsplash), kopie v datasetu Hugging Face
`wtcherr/unsplash_20k` (fotobanky jsou z prostředí blokované). Upraveno: ušní známky
rozmazané, zvětšeno 2× (originál má jen 512 px na kratší straně → ve videu měkké).

| soubor | dataset (soubor_rowgroup_řádek) | popis | kde ve videu |
|---|---|---|---|
| krava-s-teletem.jpg | 00005_2_093 | kráva a ležící tele na pastvě | úvod („začíná porodem“) |
| tele-samo.jpg | 00000_0_727 | tele v dece samo v hale s boxy | „samo v boxu“ |
| hala-krmeni.jpg | 00000_0_865 | krávy u krmného žlabu v hale | hygiena – velkokapacitní hala |
| pastva-stado.jpg | 00005_2_830 | stádo na široké pastvině | hygiena – tzv. masné krávy, prostor |
| pastva-kravy.jpg | 00004_0_250 | tři krávy na horské pastvě | zalehnutí – pastva |
| pouto.jpg | 00001_0_452 | dvě krávy hlavou k sobě | pouto |

Výměna: stačí nahradit soubor stejným názvem (ideálně ≥ 1500 px, na výšku) – scéna
`reel-kpz-foto.html` si ho načte sama; případně upravit `object-position` u `<img>`.

## Výstřižky (`vystrizky/`)

Ve videu se fotky nepoužívají celé, ale jako **papírové výstřižky**: zvíře vystřižené
z fotky s okrajem z utrženého papíru, prostředí (hala, pastvina) jako utržený kus fotky.
Vyrobeno skriptem skillu:

    python3 .claude/skills/vox-animation/scripts/cutout.py tele-samo.jpg vystrizky/tele-samo.png
    python3 .claude/skills/vox-animation/scripts/cutout.py hala-krmeni.jpg vystrizky/hala-krmeni.png --piece --crop 0,380,1024,1110

Po výměně za fotky KPZ stačí výstřižky vyrobit znovu stejnými příkazy (známky rozmazat předem).
