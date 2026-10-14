# Vizuální jazyk Vox – style guide

> Vychází z rešerše (references/sources.md) a z rozboru typických Vox
> explainerů. „Vox styl“ je zavedený pojem, **ne oficiální specifikace** Vox
> Media – oficiální interní style guide není veřejný. Hodnoty níže jsou naše
> výchozí volby; uživatelský feedback (FEEDBACK.md) je přepisuje.

## 1. Vyprávění je nad stylem

- **Jedna myšlenka na záběr.** Pokud záběr potřebuje dvě věty vysvětlení, jsou to dva záběry.
- **Vizuál odpovídá větě v komentáři.** Typická chyba napodobenin: mapa se
  objeví, zmizí, pak vyskočí graf „jen tak“. Každý pohyb musí odpovídat pointě.
- **Vede oko diváka.** Zvýraznit, ztlumit zbytek, přiblížit kamerou. Divák nikdy
  neřeší, kam se dívat.
- **Reálné podklady jako důkaz.** Výstřižky článků, dokumenty, archivní fotky,
  citace – Vox ukazuje zdroj, ne jen tvrzení. U každého čísla uveď zdroj.
- **Tempo:** střih / nová informace zhruba každé 3–6 s. Uvnitř záběru drobné
  „beaty“ (pop štítku, zvýraznění) každé 1–2 s.

## 2. Barvy

| token | hex | použití |
|-------|-----|---------|
| `--paper` | `#f3eee4` | výchozí podklad – teplý papír, nikdy čistě bílá |
| `--ink` | `#141414` | text, osy, obrysy – téměř černá |
| `--ink-soft` | `#4a4744` | popisky, vedlejší text |
| `--muted` | `#a8a29a` | „ostatní“ data, kontext |
| `--vox-yellow` | `#fff200` | zvýrazňovač, hlavní akcent značky |
| `--accent-red` | `#e4472b` | akcent pro data / „problém“ |
| `--accent-blue` | `#2f6db5` | akcent pro mapy / „srovnání“ |
| `--accent-teal` | `#2a9d8f` | doplňkový akcent |
| `--dark` | `#1b1a19` | tmavá varianta podkladu |

Pravidla:
- **Omezená paleta.** Papír + inkoust + **max. 1 dominantní akcent na záběr**.
- Kontext šedě, příběh barevně (graf: 1 barevná čára, zbytek `--muted`).
- Žlutá je vyhrazená pro zvýraznění textu / štítky – ne pro plochy grafů.
- Fotky černobíle / halftone / duotón, aby nesoupeřily s akcentem.

## 3. Typografie

| role | písmo (náhrada za Vox fonty) | velikost @1080p | styl |
|------|------------------------------|-----------------|------|
| headline | Inter Display Black (900) | 120–160 px | těsný tracking −0.025em, řádkování 0.96 |
| subhead | Inter Display ExtraBold | 64–80 px | |
| eyebrow / štítek | DejaVu Sans Mono Bold | 28–32 px | VERZÁLKY, tracking +0.14em |
| popisky grafů | mono | 26–30 px | verzálky, `--ink-soft` |
| dokumenty, citace | Charter (serif) | 42–50 px | jako tištěný článek |
| velké číslo | Inter Display Black | 170–260 px | tabular-nums |

- Vox web používá geometrický bold sans + serif + mono eyebrow; ve videích
  typografie často ustupuje **reálným dokumentům** a mění se podle období
  (historická pasáž → dobové písmo).
- Headline max. ~6–8 slov, zarovnání vlevo, velkoryse.
- Nikdy text pod 26 px ve FullHD.

## 4. Textury a materiál (koláž)

- **Papír:** teplý podklad + jemné zrno; nic není digitálně čisté.
- **Zrno přes celý obraz** (mění se každý animační krok) + lehká vinětace.
- **Výřezy (cut-outs):** archivní foto / objekt vyříznutý s **bílým papírovým
  okrajem**, mírně natočený (−4° až +4°), měkký stín „leží na papíře“.
- **Trhaný papír** na okrajích výřezů a pruhů.
- **Halftone / duotón** na fotkách (tiskový rastr, 45°).
- **Dokumenty:** článek / smlouva / tweet jako papír se stínem; text mimo
  pointu ztlumit (`.dim`), pointa zvýrazněná žlutě.
- Jemný „boil“ – výřez se o 1–2 px chvěje každý krok, ať působí fyzicky.

## 5. Pohyb

| prvek | výchozí hodnota |
|-------|-----------------|
| fps grafiky | **12 fps (na dvojky)** ve 24 fps videu – typický „stutter“ |
| vstup prvku | pop ze 0 % s překmitem (outBack), 0.3–0.45 s |
| vstup textu | posun 20–60 px + fade, 0.3–0.5 s, outCubic |
| zvýrazňovač | tah zleva doprava 0.5–0.9 s, inOutSine |
| kreslení čáry / trasy | 1–2 s, inOutCubic |
| kamera v záběru | stálý pomalý push-in 3–6 % (nebo pull-out) |
| přechod mezi záběry | rychlý pohyb kamery + **rozmazání přes střih** (vrchol blur ve střihu, ~0.25 s před, ~0.2 s po) |
| odchod prvků | rychlejší než příchod (0.2–0.3 s), inCubic |

- Nic se nehýbe lineárně (kromě pomalé kamery).
- Prvky naskakují **postupně** (stagger 0.1–0.2 s), ne všechny naráz.
- Kamera spíš vede oko (přiblížení na detail mapy/dokumentu) než efektuje.

## 6. Vizuální typy záběrů

1. **Titulková karta** – eyebrow (mono) + headline + jedno žlutě zvýrazněné slovo.
2. **Dokument / výstřižek** – serifový text na papíře, pointa zvýrazněná,
   kamera najede na zvýrazněnou větu. Zdroj ve štítku.
3. **Koláž** – archivní výřezy na papíře, parallax vrstev, popisky šipkou/štítkem.
4. **Mapa** – tlumená pevnina (papír/šedá), tenké hranice, zvýrazněný region
   akcentem (vyplní se), štítky mono verzálkami, trasy jako přerušovaná čára,
   která se „kreslí“; průlet kamerou s blur přechodem.
5. **Graf** – minimum os, žádná legenda (přímé popisky u čar), 1 barevná řada,
   ostatní šedě, čára se kreslí, číslo se odpočítává, anotace s šipkou.
6. **Velké číslo** – jedno číslo přes půl plochy + krátký popisek.
7. **Citát** – serif, velké uvozovky, fotka mluvčího jako výřez.

## 7. Časté chyby (anti-patterny)

- Moc barev / gradienty / 3D lesk → působí jako korporátní šablona.
- Plynulých 60 fps easingů všude → působí „softwarově“, ne papírově.
- Text na obrazovce opakuje doslova celý komentář.
- Legenda grafu místo přímých popisků.
- Statický záběr bez kamery (mrtvý obraz).
- Pohyb bez významu (věci poletují, protože můžou).
- Vymyšlená data prezentovaná jako skutečná.
