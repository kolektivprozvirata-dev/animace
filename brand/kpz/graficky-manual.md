# Grafický manuál – Kolektiv pro zvířata (KPZ), styl videí a grafiky

Samostatný popis stylu, ve kterém vznikl reel o telatech (2026). Dá se vložit do jiného chatu jako zadání.
K manuálu patří obrázkový vzorník `vzornik.png` (vyrenderovaný z `brand/kpz/vzornik.html`).

## Repozitář s podklady

**https://github.com/kolektivprozvirata-dev/animace** (výchozí větev `claude/vox-animation-skill-jpemkh`).
Repozitář je soukromý – číst ho umí jen chat / session s přístupem k GitHubu KPZ (např. Claude Code s tímto repem).
Jinému chatu bez přístupu stačí tento manuál + vzorník.

| co | kde v repu |
|---|---|
| tento manuál a vzorník | `brand/kpz/graficky-manual.md`, `brand/kpz/vzornik.html` |
| téma KPZ (barvy, bloky, štítky, titulky, výstřižky) | `brand/kpz/kpz-theme.css`, `brand/kpz/kpz-theme.js` |
| písmo Bebas Neue (OFL) | `brand/kpz/fonts/` |
| loga | `brand/kpz/logo-kpz-svetle.png` (výchozí), `logo-kpz-tmave.png`, `logo-kpz-text-tmave.png` |
| hodnoty, tón, slovník KPZ, postup nového videa | `brand/kpz/README.md` |
| šablona celého reelu | `scenes/kpz-telata/reel-kpz-foto.html` (obálka: `scenes/kpz-telata/thumbnail.html`) |
| fotky a výstřižky + příkazy, jak vznikly | `scenes/kpz-telata/assets/foto-kpz/` (README.md) |
| nástroje (render, výstřižky, rozostření známek, hlas) | `.claude/skills/vox-animation/` (začít `SKILL.md`, pravidla `FEEDBACK.md`) |

---

## 1. Princip v jedné větě

**Papírová koláž, která vysvětluje:** sytě růžový zrnitý papír, text v plných barevných blocích verzálkami,
skutečné fotky zvířat jako vystřižené kusy papíru, jednoduché kresby jen pro věci a schémata.
Každý záběr nese jednu myšlenku; grafika nezdobí, ale ukazuje, co zrovna zní.

---

## 2. Formát a rozvržení

- **Reel / story: 1080 × 1920 (9:16).** Video 24 fps, grafika se hýbe na dvojky (12 fps).
- **Zóna grafiky:** y 260–1300 px. Nahoře nad 260 jen logo a drobný dekor.
- **Titulky:** kolem y 1470 (střed obrazu vodorovně).
- **Řádek se zdrojem:** y ≈ 1322, vlevo x 64, šířka 900.
- **Volné místo kvůli UI sítí:** spodek pod y 1560 a pravý okraj x > 960 v dolní polovině – nic důležitého.
- **Obálka (thumbnail):** 1080 × 1920, ale vše podstatné uvnitř středového výřezu **3:4 (y 240–1680)** – tak ji Instagram ukáže v mřížce profilu.
- Odsazení od okrajů: obsah obvykle od x 70–90 px.

---

## 3. Barvy

| název | hex | k čemu |
|---|---|---|
| růžová (pozadí) | `#e05d73` (světlejší `#ef7c8e`, tmavší `#c94862`) | papír pod vším, zrnitý se skvrnami |
| teal | `#115c61` | výchozí textový blok, pozitivní / alternativa, zelené štítky |
| tmavý teal | `#0b3f43` | text na krémové, nadtitulky; tmavé pozadí pointy `#0d4a4f` |
| krémová | `#efe4dd` | druhá barva bloků, karty, titulky, štítky |
| oranžová | `#d26c11` | **zvýraznění** jednoho slova (blok jiné barvy) |
| vínová | `#920637` | nebezpečí, krutost, „špatné řešení“, škrty a šipky štětcem |
| hořčicová | `#d38f03` (text černý `#120a06`) | čísla kapitol, zvýraznění na krémové kartě, žluté štítky |
| malinová | `#c63f58` | doplňková |
| tmavě modrá | `#17323d` | obrysy kreseb, linorytové nálepky |
| zelená z loga | `#00c800` | **jen v logu**, nikde jinde |

Papír výstřižků (okraj fotek): `#f3e9e3`.
Kresby: obrys `#17323d`, výplň krémová `#f3e9e3`, stín `#e0cfc6`, růžová (čumák) `#eaa3aa`,
nákazy/bakterie `#d26c11`, list `#3f877c`, stonek `#2a6a63`.

**Význam barev se nemění:** vínová = špatně / krutost, teal = jde to jinak, oranžová = na tohle se dívej.
Žádné přechody, lesky ani 3D.

---

## 4. Písmo

- **Nadpisy, štítky, čísla, titulky: Bebas Neue**, vždy VERZÁLKAMI, normální řez (bez umělého tučného), prostrkání ~0,01 em.
  (Google Fonts, licence OFL.)
- **Drobný text** (zdroje, poznámky, „Ilustrační záběr“): Inter (Inter Display), tučný 700, prostrkání 0,04 em, normální velikost písmen.
- Velikosti v 1080 × 1920:
  - velký nadpis `h1` 128–150 px (řádkování bloků 1,42)
  - nadpis kapitoly `h2` 86 px
  - menší nadpis / karta `h3` 54–58 px
  - velké číslo 200 px
  - štítek 44–66 px (běžně 52 px)
  - nadtitulek (eyebrow) 46 px, tmavý teal, prostrkání 0,05 em
  - titulky 76 px
  - řádek se zdrojem 21 px
- Nikdy kurzíva, nikdy obrysové písmo, nikdy stín pod textem.

---

## 5. Textové bloky (hlavní znak stylu)

Text leží v **plných obdélníkových blocích po řádcích**; každý řádek je samostatný blok, mezi řádky je mezera,
barvy bloků se střídají (teal / krémová). Jedno klíčové slovo dostane **blok jiné barvy (oranžový)** – žádný žlutý zvýrazňovač.

Příklad nadpisu: `KRABICE MLÉKA` (teal) / `Z OBCHODU` (krémová) / `ZAČÍNÁ` (teal) + `PORODEM.` (oranžová).

```css
.kb { background: #115c61; color: #efe4dd; padding: .05em .2em 0;
      -webkit-box-decoration-break: clone; box-decoration-break: clone; }
.kb.cream  { background: #efe4dd; color: #0b3f43; }
.kb.orange { background: #d26c11; color: #efe4dd; }
.kb.maroon { background: #920637; color: #f7eef1; }
.kblocks   { line-height: 1.42; }           /* mezera mezi řádky bloků */
```

- **Číslo kapitoly:** hořčicový čtverec 84 px s černou číslicí, natočený −3°, vedle nadpis v bloku (`1  HYGIENA`).
- **Štítky (tags):** krátký text v bloku, mírně natočený (−5° až +3°). Krémový (neutrální), teal (dobře / alternativa),
  vínový (problém), hořčicový (upozornění). Max. ~6 slov.
- **Karta:** krémový obdélník, tmavě tealový text, odsazení 34/40 px; uvnitř může být hořčicové zvýraznění s černým textem.
- **Schéma „Problém → Řešení“:** nadtitulek PROBLÉM, blok s problémem, šipka štětcem dolů, nadtitulek ŘEŠENÍ,
  rozumné řešení **přeškrtnuté vínovým tahem štětce**, pod ním vínový štítek s tím, co se reálně dělá („ODEBRAT TELE“).

---

## 6. Pozadí a textura

- **Pozadí:** sytě růžový papír `#e05d73` se světlejšími a tmavšími skvrnami a jemným zrnem, lehká vinětace.
- **Tmavé záběry (pointa, řečnická otázka):** stejná textura v tmavém tealu `#0d4a4f`, krémový text,
  zvýraznění oranžové (text při podbarvení ztmavne). Logo se na tmavých záběrech skrývá.
- **Tiskový „grunge“** na blocích a písmu jen **jemně** (KPZ: „o 50 % míň špinavé“) – čitelnost má přednost.
- Fotky nikdy celé přes obraz – vždy jako kus papíru na růžovém pozadí.

---

## 7. Fotky

- **Výstřižek:** zvíře vystřižené s **krémovým okrajem z utrženého papíru** (~26 px), měkký stín „leží na papíře“,
  mírně teplý tón (sepia ~0,14, sytost 0,9), lehce natočené (−4° až +4°).
- **Prostředí (hala, pastva, kravín):** utržený kus fotky – obdélník s trhaným okrajem, krajiny jako nepravidelný „blob“.
- **Jen celá zvířata** – žádné useknuté půlky těla; žádná díra po „vytrženém“ zvířeti (použít dvojici fotek s ním a bez něj).
- **Zvíře = fotka, kresba = jen věci a schémata.** Stejné zvíře neukazovat jednou fotkou a jindy kresbou.
- **Plemena podle tématu:** mléčné chovy = holštýnky / český strakatý skot; masný skot jen tam, kde se o něm mluví.
- Stejnou fotku zvířete nepoužívat ve více záběrech.
- **Ušní známky:** rozostřit **jen samotné číslo** (tvar a barva známky zůstanou). Žádný detail na známku.
- **Loga a názvy podniků** na fotkách z farem rozmazat – kritizujeme systém, ne jednu farmu.
- Skutečné fotky z farem nesou drobný nápis **„Ilustrační záběr“** vpravo dole (Inter 600, 24 px, světlý text na
  poloprůhledném tmavém obdélníku `rgba(30,20,26,.55)`, rádius 3 px).
- Přepálené fotky stáhnout ve světlech (nic nad ~230/255), ať bílá zeď ani nebe nesvítí.
- Fotky jen od KPZ nebo s jasným svolením; autory, kteří nechtějí být uvedeni, neuvádět.

---

## 8. Kresby a dekor

- **Kresby** (boudy, hala z výšky, krávy shora, bakterie, šipky, grafy): plochá výplň krémová, silný obrys tmavě modrý `#17323d`
  se zaoblenými konci, žádné stíny ani přechody.
- **Linorytové nálepky:** větvička, klasy, srdce – tmavě modré s krémovými rytinami; po 1–2 kusech v rohu záběru, natočené.
- **Šipky a škrty:** tah štětcem (nerovný okraj), vínově nebo tmavě modře.
- **Grafy:** minimum os, přímé popisky místo legendy, jeden sloupec / řada barevně (vínová), ostatní tlumeně (šedozelená `#8fa9a7`),
  čísla se odpočítávají.

---

## 9. Logo

- Ve videu **klasické logo KPZ** (zelený list + černé „KPZ“) na světlém podkladu: vodoznak **vlevo nahoře** (x 56, y 96, šířka 132 px), na tmavých záběrech skrýt.
- Outro: velké logo uprostřed + web www.kolektivprozvirata.cz.
- Kulaté černé logo z grafiky na sítích ve videích **nepoužívat**.

---

## 10. Titulky a zdroje

- **Titulky vypálené do obrazu:** kousky po 2–5 slovech, každý úsek krémový blok s tmavě tealovým textem,
  klíčové slovo v **oranžovém bloku**. Čísla s mezerou (9 500) nikdy nerozdělit. Kde je věta už velkým textem v grafice, titulek vynechat.
- **Řádek „Zdroj: …“** u každého tvrzení: Inter tučně 21 px, barva `#3a0f1d`, průhlednost 0,9, vidět **jen po dobu tvrzení**.
  České zdroje přednostně (u chovu v ČR hlavně české, u etologie zahraniční v pořádku). Plný seznam do popisku příspěvku.

---

## 11. Pohyb (u videa)

| prvek | hodnota |
|---|---|
| snímky grafiky | 12 fps (na dvojky) ve 24 fps videu |
| vstup prvku | „pop“ z 0 s překmitem, 0,3–0,45 s |
| vstup textu | posun 20–60 px + objevení, 0,3–0,5 s |
| zvýraznění slova | blok se přebarví zleva doprava, 0,5–0,9 s |
| fotky / panely | zajedou zprava, odjedou doleva, 0,45 s (rychlé střídání 0,3 s) |
| kamera | stálé pomalé přiblížení 3–6 % během záběru |
| střih | rychlý přechod s rozmazáním (vrchol ve střihu) |
| odchod | rychlejší než příchod, 0,2–0,3 s |
| „papír“ | výstřižky se jemně chvějí (≈2 px, 0,6°, 6× za s), nálepky taky |

Prvky naskakují postupně (rozestup 0,1–0,2 s) a vždy na slovo, které ilustrují. Žádný záběr nesmí být několik sekund
„prázdný“ (jen nadpis) – vždy fotka, kresba nebo schéma k tomu, co zní.

---

## 12. Typy záběrů

1. **Hook:** nadpis z bloků + výstřižek zvířete (otázka / šokující fakt).
2. **Velké číslo:** „DO 12 H“ v tealovém bloku 200 px + krémový štítek s vysvětlením a zdrojem.
3. **Kapitola argumentu:** hořčicové číslo + nadpis, pod tím fotka / kresba, štítky, nakonec schéma Problém → Řešení.
4. **Karta studie:** krémová karta s větou ze studie a zdrojem drobným písmem.
5. **Graf:** dva až tři sloupce, popisky přímo u nich.
6. **Tmavá pointa:** krátká věta na tmavém tealu, jedno slovo oranžově.
7. **Outro:** logo, web, „Zdroje v popisku“.

---

## 13. Tón (stručně)

- Věcně, přesně, přesvědčivě i pro nevegany; data a logika před citovým vydíráním.
- Bez samoúčelně drastických obrazů.
- S KPZ si tykáme.
- Každé tvrzení musí mít zdroj; „často“ vs. „většinou“ podle toho, co je opravdu změřené.

---

## 14. Rychlý kontrolní seznam

- [ ] 1080 × 1920, důležité v y 260–1300, titulky ~1470, nic pod 1560
- [ ] Bebas Neue verzálkami, text v blocích po řádcích, jedno slovo oranžově
- [ ] Růžový zrnitý papír, grunge jen jemně
- [ ] Fotky jako utržené výstřižky, celá zvířata, čísla známek rozostřená, „Ilustrační záběr“
- [ ] Kresby jen věci a schémata, obrys tmavě modrý
- [ ] Vínová = problém, teal = alternativa, oranžová = zvýraznění
- [ ] Logo vlevo nahoře (na tmavém skrýt), zdroj u každého tvrzení
