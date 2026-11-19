# Fotky KPZ ke karuselu „Živočišná výroba a planeta“ (dodané 2026-11-19)

Na ušních známkách nejsou čitelná čísla, loga ani názvy podniků nejsou vidět – bez retuše.
Tmavé fotky jen zesvětlené (jas/kontrast, `-upr.jpg`), obsah beze změny. Na slajdech vždy „Ilustrační záběr“.

| soubor | popis | použití |
|---|---|---|
| prasnice-klece.webp → -upr.jpg | řady prasnic v klecích (kotce s krmítky) | kus `vystrizky/prasnice-klece.png` (`--piece --crop 520,400,2000,1071`) – 5. slajd „Tzv. hospodářská zvířata váží 30× víc“ (místo haly s kravami) |
| kurata-hala.webp → -upr.jpg | hala s tisíci kuřaty | kus `vystrizky/kurata-hala.png` (`--piece --crop 250,180,1850,1070`) – 6. slajd „Chov zvířat = 12 % všech emisí“ (místo opakovaného velkého „12 %“) |
| prasnice-selata.webp | prasnice v porodní kleci se selaty, dívá se do objektivu („KOJ 23“ = označení kotce) | kus `vystrizky/prasnice-selata.png` připraven, **zatím nepoužito** (zkoušeno na slajdu s prasetem – moc malé) |
| prasata-vykrm.webp | výkrm prasat v kotcích, tmavá hala | kus `vystrizky/prasata-vykrm.png` připraven, **zatím nepoužito** (malý výřez nečitelný) |

    S=.claude/skills/vox-animation/scripts/cutout.py
    python3 $S prasnice-klece-upr.jpg vystrizky/prasnice-klece.png --piece --crop 520,400,2000,1071 --seed 11
    python3 $S kurata-hala-upr.jpg vystrizky/kurata-hala.png --piece --crop 250,180,1850,1070 --seed 13
    python3 $S prasata-vykrm.webp vystrizky/prasata-vykrm.png --piece --crop 980,380,2000,1074 --seed 12
    python3 $S prasnice-selata.webp vystrizky/prasnice-selata.png --piece --crop 200,180,1700,1072 --seed 14
