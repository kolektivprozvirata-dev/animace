---
name: vox-animation
description: Tvorba vysvětlujících animací a motion graphics ve stylu Vox (papírová koláž, zvýrazňovač, animace na dvojky 12 fps, mapy, grafy, dokumenty, kamerové přechody s rozmazáním). Použij vždy, když uživatel chce animaci, explainer, motion graphics, animovaný graf/mapu/titulek "jako Vox", "ve Vox stylu", "vysvětlující video", nebo když dává zpětnou vazbu k dřívější animaci z tohoto skillu. Renderuje HTML/SVG scény přes Playwright + ffmpeg do MP4.
---

# Vox animace

Skill pro tvorbu animací ve stylu Vox explainerů. **Je živý** – zlepšuje se
podle zpětné vazby uživatele (viz „Smyčka zpětné vazby“). Před prací vždy
přečti:

1. `FEEDBACK.md` → sekci **Pravidla z feedbacku** (mají přednost před vším ostatním).
   U videí pro Kolektiv pro zvířata navíc `brand/kpz/README.md` (hodnoty, tón, slovník, loga).
2. `references/style-guide.md` – vizuální jazyk (barvy, typo, textury, pohyb).
3. `references/techniques.md` – jak jednotlivé efekty postavit v našem runtime.

`references/sources.md` obsahuje rešerši, ze které styl vychází.

## Princip Vox stylu v jedné větě

**Grafika nezdobí, vysvětluje.** Každý záběr nese jednu myšlenku, která přesně
odpovídá tomu, co v tu chvíli říká komentář. Styl (papír, koláž, žlutý
zvýrazňovač, trhavý pohyb na dvojky) je až druhý krok.

## Pracovní postup

### 1. Scénář → záběry (shot list)
Než napíšeš kód, rozepiš animaci do tabulky a ukaž ji uživateli, pokud je
zadání větší než jeden záběr:

| # | čas | komentář (VO) | jedna myšlenka | vizuál | hlavní pohyb | přechod |
|---|-----|---------------|----------------|--------|--------------|---------|

- záběr 3–6 s, jedna myšlenka, max. 1 akcentová barva
- vizuál vybírej z „vizuálních typů“ ve style-guide (titulek, dokument,
  koláž, mapa, graf, velké číslo, citát)
- prvek naskakuje se slovem v komentáři (0–2 snímky před slovem)
- pokud není komentář, napiš pracovní text, ať má animace rytmus

### 2. Scéna = HTML soubor
- Projektové scény ukládej do `scenes/<projekt>/<nazev>.html` v kořeni repa,
  podklady (fotky, VO, hudba) do `scenes/<projekt>/assets/`.
- Začni kopií `examples/demo.html`, uprav cesty k runtime
  (`../../.claude/skills/vox-animation/runtime/vox.css|js`).
- Veškerý pohyb počítej v `VOX.scene((t) => …)` z času `t`.
  **Žádné CSS animace ani transitions** – nebyly by deterministické.
- Barvy/písma ber z tokenů ve `runtime/vox.css`; když je potřeba nový token,
  přidej ho tam (a pokud jde o feedback, zapiš ho i do FEEDBACK.md).
- Fotky do koláže připrav přes `scripts/halftone.py` (halftone / duotón).

### 2b. Voiceover a titulky (český hlas)
1. Napiš `scenes/<projekt>/vo.json` – segmenty `{id, text, say?, pause?, cap?}`
   (`say` = výslovnost, čísla slovy; `*slovo*` = zvýraznění v titulku).
2. `python3 .claude/skills/vox-animation/scripts/tts.py scenes/<projekt>/vo.json`
   → `assets/vo.wav`, `assets/vo-timing.js`, `assets/vo.srt`. Vypíše časy segmentů –
   zkontroluj celkovou délku proti zadání a případně zkracuj text / `length_scale`.
   (Piper ~11 znaků/s při `length_scale` 0.85.)
3. Ve scéně načti `assets/vo-timing.js` a časuj podle hlasu:
   `VOX.vo('id').t0`, `VOX.wordT('id', 'slovo')` (odhad času slova), titulky
   `VOX.captions(t, { y: 1470 })`. `VOX.setup({ duration: VO.duration })`.
4. Render se zvukem: `render.mjs scena.html --audio assets/vo.wav`.
   **Pozor:** Piper není deterministický – `vo.wav` a `vo-timing.js` patří k sobě a vznikají
   vždy spolu. Nikdy nepřegenerovávej hlas, když běží render, který ho používá. Víc verzí
   jedné scény (např. plná a zkrácená) drž v oddělených složkách (`tts.py --out-dir assets-plna`).
5. Limity platforem: Instagram Reels obvykle **max. 3:00** (některé účty víc) – při delším
   scénáři počítej s variantou pod 3:00 nebo sérií.
   Model hlasu se stahuje z huggingface.co do `.cache/piper/` (gitignored).

### 2c. Ilustrace
`runtime/vox-icons.js`: `VOXI.cow()`, `VOXI.cow({calf:true, facing:'right', spots:false})`,
`VOXI.cowTop()`, `VOXI.icon('germ'|'scissors'|'milk'|'cart'|'plant'|'tag'|'barn')`.
Papírový výřez s trhaným okrajem je zabudovaný. Nové ilustrace přidávej sem, ať jsou znovupoužitelné.
Barvy ilustrací lze přepnout pro celou scénu: `VOXI.palette({ ink, paper, border, red, blue, … })`
(volat před kreslením).

### 2e. Vizuální styl značky (brand theme)
Když má klient vlastní vizuál, nepřepisuj `vox.css` – přidej téma do `brand/<klient>/`:
CSS (`body.<klient>` přemapuje tokeny a třídy) + JS (filtry, pozadí, prvky). Pohyb a postup
zůstávají Vox, mění se písmo, barvy, textury a tvary. Hotové téma: **KPZ**
(`brand/kpz/kpz-theme.css` + `kpz-theme.js`, popis v `brand/kpz/README.md` → Vizuální styl),
vzor scény `scenes/kpz-telata/reel-kpz.html`. Z grafiky klienta přebírej jen vizuál, ne obsah.

### 2f. Skutečné fotky
Ilustrace nech na vysvětlování (schémata, grafy, kruhy), skutečné fotky dej do momentů
„tohle je skutečné“ (hook, zvíře samo, hala, pastva, pouto) – 4–6 fotek, ne montáž na konci.
Výchozí podoba = **papírový výstřižek**: `scripts/cutout.py foto.jpg out.png` vystřihne zvíře
(model BiRefNet, stáhne se z Hugging Face) a dá mu okraj z utrženého papíru; `--piece` udělá
utržený kus celé fotky (hala, krajina). Ve scéně `<div class="kpz-cut"><img src=out.png></div>`
+ `cutout()` boil. Celé fotky přes celou šířku (`.kpz-photo fade-y`) KPZ nechtějí („je to divné“).
Ušní známky: čísla **rozostřit jen uvnitř obrysu známky** – `scripts/tag_retouch.py foto.jpg
out.jpg --box x0,y0,x1,y1 …` (výchozí `--mode blur`; oblasti známek zadat ručně, automatika
bez `--box` venku plete suchou trávu). Ne rozmazaný flek přes ucho, ne plné přebarvení. Nedělat detail známky jako samostatný záběr. Výřez se ulétlými kousky pozadí: `--largest`, malá fotka: `--scale 2`. Vystřihovat jen **celá zvířata** – fotku,
kde okraj usekne část těla, nepoužít. Fotky s kravami a telaty: `hf_photos.py` nad COCO
(`Multimodal-Fatima/COCO_captions_train`, sloupec `sentences_raw`). Provizorní fotky,
když klient ještě nedodal své: `scripts/hf_photos.py` (Unsplash z Hugging Face, fotobanky
jsou z prostředí blokované) – jen na náhled, zdroj zapsat do README u fotek.

### 2d. Svislý formát (reels)
`VOX.setup({ width: 1080, height: 1920 })`. Zóny viz FEEDBACK.md → [formát].
Vzor: `scenes/kpz-telata/reel.html` (Vox papír), `scenes/kpz-telata/reel-kpz.html` (styl KPZ).

### 3. Kontrola vlastníma očima (povinné před odevzdáním)
```bash
S=.claude/skills/vox-animation/scripts
node $S/render.mjs scenes/x/scena.html --contact 12      # kontaktní arch
node $S/render.mjs scenes/x/scena.html --still 3.5        # jeden snímek
node $S/render.mjs scenes/x/scena.html --stills 3.5,9,17 --out out/kontrola   # víc snímků najednou
```
Kontaktní arch si **otevři (Read) a zkontroluj** podle checklistu níže.
Teprve pak renderuj celé video:
```bash
node $S/render.mjs scenes/x/scena.html --out out/scena.mp4 [--audio vo.mp3]
```
Render trvá cca 2–3 s na 1 s videa (12 fps grafika = poloviční počet unikátních snímků;
snímky jdou do ffmpeg jako JPEG q95 – PNG kódování zrnitých textur bylo 5× pomalejší,
`--png` vrátí bezeztrátové). Pro rychlý náhled `--scale 0.5`, pro výřez `--from/--to`.
Náhled v prohlížeči: otevři HTML s `?t=2.5` nebo `?play`.

### 4. Checklist před odevzdáním
- [ ] Každý záběr má jednu myšlenku a je čitelný za 1 s (test: zakryj text komentáře)
- [ ] Max. 1 akcentová barva na záběr; ostatní data šedě
- [ ] Zvýrazňovač jen na klíčovou frázi (2–6 slov), ne na celý odstavec
- [ ] Nic není „plovoucí bez důvodu“ – každý pohyb odpovídá pointě
- [ ] Grafika jede na dvojky (12 fps), vstupy pop/overshoot, ne lineární
- [ ] Kamera se pořád trochu hýbe (push-in 3–6 % za záběr), střihy maskuje blur
- [ ] Texty se nevejdou mimo safe area (90 % plochy), nic se nezalamuje divně
- [ ] Písmo min. 28 px ve FullHD, kontrast textu dostatečný
- [ ] Data jsou označená (zdroj / „ilustrační data“) – nikdy nevymýšlej čísla
      a nevydávej je za skutečná

### 5. Odevzdání a sběr feedbacku
Pošli uživateli video (`SendUserFile`) + kontaktní arch a **vždy se zeptej na
zpětnou vazbu**, ideálně konkrétně: tempo, barvy, typografie, textury,
čitelnost, „co ti nepřipadá jako Vox“.

## Smyčka zpětné vazby (jak se skill zlepšuje)

Když uživatel dá zpětnou vazbu:

1. **Oprav aktuální animaci.**
2. **Zobecni** – je to jednorázová preference, nebo pravidlo pro všechny
   budoucí animace? Pokud nevíš, zeptej se jednou krátkou otázkou.
3. **Zapiš do `FEEDBACK.md`**:
   - do **Logu** vždy (datum, projekt, co uživatel řekl, co se změnilo),
   - obecná pravidla navíc do **Pravidla z feedbacku** jako krátké,
     ověřitelné pravidlo („Headline max. 6 slov“, ne „lepší titulky“).
4. **Propiš změnu do zdroje pravdy**: tokeny → `runtime/vox.css`,
   pohybové výchozí hodnoty → `runtime/vox.js`, styl → `style-guide.md`,
   postup → tento soubor. Pravidlo, které je jen v FEEDBACK.md a ne v kódu,
   se snadno ztratí.
5. Pokud pravidlo odporuje style-guide, **uprav style-guide** (feedback
   uživatele vyhrává nad rešerší) a v logu uveď, co bylo přepsáno.
6. Zvyš verzi v `FEEDBACK.md` (minor = nové pravidlo, patch = doladění)
   a commitni zprávou `vox-skill: <co se změnilo>`.

Pozitivní feedback („tohle je přesně ono“) zapisuj taky – jako
„✅ osvědčené“, ať se to neztratí při dalších změnách.

## Struktura skillu

```
.claude/skills/vox-animation/
├── SKILL.md                  ← tento postup
├── FEEDBACK.md               ← pravidla z feedbacku + log + verze
├── references/
│   ├── style-guide.md        ← vizuální jazyk Vox
│   ├── techniques.md         ← recepty: jak udělat efekt X
│   └── sources.md            ← rešerše a zdroje
├── runtime/
│   ├── vox.js                ← deterministický animační runtime (VOX.*, titulky)
│   ├── vox-icons.js          ← papírové ilustrace (kráva, tele, ikony)
│   └── vox.css               ← tokeny, typografie, koláž, dokument, grafy
├── scripts/
│   ├── render.mjs            ← HTML → MP4 / PNG / kontaktní arch
│   ├── tts.py                ← český voiceover (Piper) + časování + titulky
│   ├── hf_photos.py          ← provizorní fotky z datasetů Hugging Face
│   ├── cutout.py             ← výstřižek z fotky s okrajem z utrženého papíru
│   ├── tag_retouch.py        ← čísla na ušních známkách rozostřit uvnitř známky
│   └── halftone.py           ← fotka → halftone / duotón PNG
└── examples/demo.html        ← ukázka: titulek, dokument, graf
```

## Omezení prostředí
- Render potřebuje Playwright (Chromium) a ffmpeg – v cloudovém prostředí jsou
  předinstalované. Lokálně: `npm i -g playwright && npx playwright install chromium`.
- Písma: lokálně Inter / Charter / DejaVu Mono (podporují češtinu). Google Fonts
  lze ve scéně načíst `<link>`em; renderer čeká na `document.fonts.ready`.
- Výřez postavy z fotky (odstranění pozadí) umí `scripts/cutout.py` (BiRefNet); u zvířat
  oříznutých okrajem fotky vznikne rovná hrana – vybírat fotky s celým zvířetem.
