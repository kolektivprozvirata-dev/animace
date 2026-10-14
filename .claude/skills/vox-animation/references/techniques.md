# Techniky – recepty v našem runtime

Všechny příklady předpokládají scénu postavenou jako `examples/demo.html`:

```html
<link rel="stylesheet" href="…/runtime/vox.css">
<script src="…/runtime/vox.js"></script>
<div id="stage"> … vrstvy … </div>
<script>
  VOX.setup({ duration: 10 /*, background: 'dark', grain: 0.07, vignette: 0.18 */ });
  const { set, prog, pop, boil, highlight, draw, count, camera, cutBlur, push, shot, ease } = VOX;
  VOX.scene((t, raw) => { … });
</script>
```

## API runtime (`VOX.*`)

| funkce | co dělá |
|--------|---------|
| `setup({duration, width, height, fps, animFps, grain, vignette, background})` | konfigurace, vloží SVG filtry + papír/zrno/vinětu |
| `scene((t, raw) => …)` | registrace renderu; `t` kvantovaný na 12 fps, `raw` plynulý |
| `prog(t, t0, dur, easing)` | průběh 0..1 |
| `inOut(t, t0, t1, durIn, durOut)` | náběh a odchod (0→1→0) |
| `set(el, {x, y, s, sx, sy, r, o, blur, origin})` | transform + opacity + blur |
| `pop(t, t0, dur=0.33, overshoot)` | scale s překmitem (Vox „pop“) |
| `boil(t, seed, amp, rot)` | chvění výřezu po krocích → `{x, y, r}` |
| `highlight(el, p)` | žlutý zvýrazňovač na `.hl` |
| `draw(pathEl, p)` | kreslení SVG cesty |
| `typeOn(el, p)` | psací stroj |
| `count(el, from, to, p, fmt)` | odpočítávané číslo |
| `camera(worldEl, t, keys)` | kamera nad „světem“ (klíče `{t, x, y, s, r, e}`) |
| `cutBlur(t, cutT, peak)` | blur přes střih |
| `push(t, t0, t1, s0, s1)` | pomalý push-in |
| `shot(el, t, t0, t1)` | zobrazí záběr jen v intervalu, vrací bool |
| `ease.*` | linear, outCubic, inCubic, inOutCubic, outExpo, inOutSine, outBack |

## Animace na dvojky (12 fps stutter)
Výchozí. `t` uvnitř `scene` se mění jen 12× za sekundu; renderer duplikuje
snímky do 24 fps. Pro plynulý prvek (např. pomalý camera drift) použij `raw`.
Pro jiný rytmus: `VOX.setup({ animFps: 8 })` (trhanější) nebo `24` (plynulé).

## Pop s překmitem
```js
const s = pop(t, 1.2);           // 0 → 1.1 → 1
set('#tag', { s, o: s > 0 ? 1 : 0 });
```

## Zvýrazňovač
```html
<span class="hl" id="k">klíčová fráze</span>      <!-- plocha -->
<span class="hl hl-under" id="k2">podtržení</span>
```
```js
highlight('#k', prog(t, 2.0, 0.7, ease.inOutSine));
```
Barvu změníš `style="--hl-color: var(--accent-red)"`. Víceřádkové
zvýraznění: rozděl na víc `<span class="hl">` a spusť je postupně.

## Dokument s kamerou na pointu
1. `.doc` s `.doc-source`, `.doc-title`, odstavec; vedlejší text `.dim`.
2. Kamera začne celkem, pak `camera('#world', t, [{t:0, x:960, y:540, s:1}, {t:2, x:900, y:620, s:1.6}])`.
3. Až kamera dojede, `highlight()` na pointu.

## Papírový výřez (koláž)
```html
<div class="cutout bw" id="photo" style="left:200px;top:180px;width:520px;height:640px">
  <img src="assets/osoba_ht.png">
</div>
```
- bílý trhaný okraj a stín dělá `.cutout` (`.clean` = rovný okraj)
- `.bw` = černobílá; skutečný rastr: `python3 -I scripts/halftone.py in.jpg out.png --cell 8`
- duotón: `--duotone "#2f6db5"`; průhledné PNG zůstane průhledné
- vstup: `pop` + mírné natočení; po dobu záběru `boil(t, 'photo', 1, .2)`

## Parallax vrstev
Každá vrstva dostane jiný násobek posunu kamery:
```js
const cx = VOX.lerp(0, -120, prog(t, 0, 6, ease.inOutSine));
set('#bg',  { x: cx * 0.3 });
set('#mid', { x: cx * 0.7 });
set('#fg',  { x: cx * 1.2 });
```

## Kamerový blur přechod
Pohyb kamery zrychlí do střihu, blur vrcholí ve střihu:
```js
const b = cutBlur(t, CUT, 22);          // na obou záběrech kolem střihu
set('#w1', { s: push(t, 0, CUT, 1, 1.08), blur: b });
```
Blur má být **mnohem kratší** než pohyb kamery. Pro dramatičtější přechod
přidej v posledních 0.25 s záběru rychlý `x` posun nebo scale ×1.3.

## Graf
- SVG ve `world`; osy `.axis`, mřížka `.grid`, čáry `.line` / `.line.accent`.
- Pořadí: osa → kontextová (šedá) data → hlavní čára (`draw`) → bod (`pop`)
  → číslo (`count`) → anotace.
- Popisky přímo u konce čar, ne legenda.
- Sloupce: `set(bar, { sy: prog(...), origin: 'bottom' })` + `transform-box: fill-box`
  pro SVG prvky.

## Mapa
- Podklad: SVG s regiony (`<path>`), pevnina `--paper-shade`, hranice `--ink` 1.5 px, voda `--paper`.
  Zdroj tvarů: Natural Earth (public domain) → převod na SVG (mapshaper).
- Region se zvýrazní: `fill` interpoluj do akcentu, nebo maska, která se „rozlije“.
- Trasa: přerušovaná čára, která se kreslí → `.route` má vlastní dasharray,
  proto kresli **masku**: plná cesta v `<mask>` animovaná `draw()`, přerušovaná
  cesta pod ní maskou odhalená.
- Štítky měst: mono verzálky + tečka, naskakují `pop`.
- Průlet: `camera()` mezi klíči + `cutBlur` při velkých skocích.

## Zvuk
`render.mjs --audio vo.mp3` přimíchá stopu. Časování: změř v audiu čas
klíčových slov (např. `ffmpeg -i vo.mp3 -af silencedetect=n=-35dB:d=0.25 -f null -`
pro pauzy) a začátek animace prvku dej 0–2 snímky (0–0.08 s) před slovo.

## Výkon
- ~10 s renderu na 1 s FullHD videa. Velké blur hodnoty a hodně
  `filter` prvků render zpomalují.
- Iteruj přes `--contact` / `--still` / `--scale 0.5`, celé video až na konec.
