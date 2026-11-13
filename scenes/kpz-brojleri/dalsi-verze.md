# Úpravy do další verze – reel o kuřatech

Nové připomínky přidávat pod tabulku; nevyrábět bez pokynu KPZ.

## v1 (2026-10-29) – render `out/kpz-brojleri-reel-v1.mp4`, hlas `vo-v1.json` → `assets-v1/` (1:57,5), scénář `scenar-v1.md`

Scénář schválen KPZ („potvrzuju ti vše“), u otázek ze scénáře platí doporučení: 30–40 dní, investigace KPZ jen v popisku,
vykání divákům, ironická otázka místo „nevyplatí se“, provizorní fotky.

## v2 (2026-10-29) – render `out/kpz-brojleri-reel-v2.mp4`, hlas `vo-v2.json` → `assets-v2/` (2:18,7), scénář `scenar-v2.md`

Text KPZ (`hlas-v1.txt` → upravený). Viz hlavička `scenar-v2.md` (opravy pravopisu a věta o 110 milionech).

## v3 (2026-11-13) – render `out/kpz-brojleri-reel-v3.mp4`, hlas `vo-v3.json` → `assets-v3/` (2:42,8), scénář `scenar-v3.md`

Hlas pomaleji (`speed` 0.9, pauzy +0,15 s, čárky 0,22 s – celý namluvený znovu, hook0 beze změny), věta o přisypávání
podle KPZ (+ „Podestýlka se vyklidí…“ jako samostatný segment `pod2b`), řečnická otázka v `eleven_multilingual_v2` (seed 2)
místo `eleven_v3` (byla o 3,8 půltónu výš). Kontrola přepisem (ElevenLabs Scribe): text sedí slovo od slova.

## v4 (2026-11-13) – render `out/kpz-brojleri-reel-v4.mp4`, hlas `vo-v4.json` → `assets-v4/` (2:37,1), scénář `scenar-v4.md`

Tempo mezi v2 a v3 (`tempo` 1.05 nad nahrávkami v3, pauzy −0,075 s), „Jenže v hale je stále…“, důrazný konec „…nepočítá.“,
nová věta „A většina z nich se předtím týdny válí ve vlastních výkalech.“ + fotka a štítek v závěru. Přepis sedí na 393 slovech.

## Do v5 (sbírá se – nevyrábět, dokud KPZ neřekne)

| # | datum | úprava | stav |
|---|---|---|---|
| 1 | 2026-10-29 | **Fotky KPZ** místo provizorních (`assets/foto-provizorni/README.md`): (a) malá kuřátka v čisté hale – polaroid „Den 1“ a pointa, (b) hala na konci výkrmu – hook nebo „leží“ (zatím jen schéma), (c) kuře ležící v podestýlce – hook + „leží“ + závěr (v4), (d) dospělé kuře celé, vidět nohy – popáleniny. Přidat „Ilustrační záběr“. | čeká na fotky |
| 2 | 2026-10-29 | (z v1) Řečnická otázka „Měnit podestýlku zvířatům…?“ zní skoro oznamovacím tónem (z 9 verzí nejlepší původní). Když vadí: kratší otázka, např. „Proč ji měnit, když za pár týdnů jedou na jatka?“ – zeptat se KPZ. | v3: nový take stoupá +3,7 půltónu, výška jako okolí – čeká na poslech KPZ |
| 3 | 2026-10-29 | (z v2) KPZ vypustili „Kuře není jídlo. Je to někdo.“ – vrátit? | k rozhodnutí |
| 4 | 2026-11-13 | (z v3) Bezpečnější varianta přisypávání: „…nejspíše neděje. A i když ano, ta stará zůstává pod ní.“ – na námitku „přistýláme“ (viz `overeni-tvrzeni.md`). | k rozhodnutí |
