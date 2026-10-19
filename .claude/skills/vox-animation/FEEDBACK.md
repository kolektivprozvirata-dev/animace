# Feedback & vývoj skillu

**Verze skillu: 0.4.0**

Tento soubor je paměť skillu. Pravidla níže mají **přednost** před
`references/style-guide.md`. Postup zápisu je v `SKILL.md` → „Smyčka zpětné vazby“.
Pravidla specifická pro organizaci KPZ (obsah, tón, slovník) jsou v
`brand/kpz/README.md`.

## Pravidla z feedbacku

- **[workflow]** Před výrobou obsahového videa nejdřív rešerše a ověření tvrzení; výroba až na výslovný pokyn. _(2026-10-14, kpz-telata)_
- **[workflow]** Před psaním scénáře pro KPZ si projít hodnotový rámec v `brand/kpz/README.md` (veganská etika). _(2026-10-14, kpz-telata)_
- **[formát]** Reely pro sítě: **9:16, 1080×1920**. Grafika v zóně y 260–1300, titulky kolem y 1470, spodek (>1560) a pravý okraj (x>960 v dolní polovině) nechat volný kvůli UI sítí. _(2026-10-14, kpz-telata)_
- **[titulky]** Titulky **ano** – vypálené, součást designu: kousky po 2–5 slovech, papírový pruh, klíčové slovo žlutě. Kde je věta už velkým textem v animaci, titulek vypnout (`cap: false`). _(2026-10-14, kpz-telata)_
- **[zvuk]** Voiceover: Piper, hlas `cs_CZ-jirka-medium` (`scripts/tts.py`). Bez patetické hudby. _(2026-10-14, kpz-telata)_
- **[branding]** Logo KPZ jako vodoznak vlevo nahoře + logo v outru (`brand/kpz/`). _(2026-10-14, kpz-telata)_
- **[data]** Na obrazovce u každého tvrzení drobný řádek „Zdroj: …“; plný seznam zdrojů do popisku příspěvku. _(2026-10-14, kpz-telata)_
- **[obsah]** Víc informací má přednost před krátkou stopáží – délka může přesáhnout 90 s. Hlídat jen limity platforem. _(2026-10-14, kpz-telata v2)_
- **[tempo]** Rychlost hlasu `length_scale` 0.83 je v pořádku – nezpomalovat. Když se text nevejde do limitu, smí se zrychlit (v4: 0.75 na pokyn KPZ). _(2026-10-14/15, kpz-telata)_
- **[workflow]** Úspornější iterace: exportovat text hlasu do `scenar-vN.md` (sekce = záběry), KPZ ho upraví a pošle zpět; text převzít, opravit jen pravopis a zjevné překlepy (a říct které), sladit kotvy ve scéně, jeden render. _(2026-10-15, kpz-telata v4)_
- **[tón]** Komentář nesmí znít jako strojové odříkávání argumentů: vkládat doložené, lidsky srozumitelné momenty (co zvířata prožívají), ironii z kontrastu, krátké pointy na tmavém pozadí. _(2026-10-14, kpz-telata v2)_
- **[obsah]** Problémy pojmenovávat konkrétně („velkokapacitní kravín, spousta krav na malém prostoru“), ne abstraktně („systém“). _(2026-10-14, kpz-telata v2)_
- **[formát]** Pro Instagram držet reel **pod 3:00** (zkrácená varianta); plnou verzi lze dát jinam. Při zkracování nechat čísla a detaily na obrazovce a vypustit je jen z hlasu. _(2026-10-14, kpz-telata v2)_
- **[struktura]** Začínat **hookem** (nejsilnější konkrétní fakt), ne úvodním popisem. Kontext a citlivost zvířat až za hookem. _(2026-10-14, kpz-telata v3 – zadání)_
- **[technika]** Na tmavém pozadí zvýrazněný text musí být čitelný i před podbarvením (světlý → tmavý při zvýraznění). _(2026-10-14, kpz-telata v2)_
- **[vizuál]** Když klient pošle svou grafiku „ať je to podobné“: převzít **jen vizuál** (písmo, barvy, textury, tvary bloků, dekor, logo), ne obsah, hesla ani fotky – fotky jen ty, které klient dodá k videu. Styl zapsat jako téma do `brand/<klient>/`. _(2026-10-19, kpz-telata v4-kpz)_
- **[obsah]** Žádné detaily ušních známek ani čitelná čísla na známkách. _(2026-10-19, KPZ)_
- **[technika]** Render snímků přes JPEG q95 (PNG zrnitých textur ~1 s/snímek); celoplošné SVG filtry kreslit jednou do canvasu, ne v každém snímku. _(2026-10-19)_

## ✅ Osvědčené (nechat tak)

- Hlas Jirka (Piper) při `length_scale` 0.83 – tempo „v pohodě“. _(kpz-telata v1)_

## Otevřené otázky na uživatele

- Hudební podkres: žádný (výchozí), nebo jemný rytmický?

## Log

| datum | verze | projekt | feedback | změna ve skillu |
|-------|-------|---------|----------|-----------------|
| 2026-10-14 | 0.1.0 | — | — | Založení skillu z rešerše (viz references/sources.md), runtime, renderer, demo. |
| 2026-10-14 | 0.2.0 | kpz-telata | Chce český hlas a titulky; reel 9:16; logo KPZ; úhel „bizár systému“; „krutý“ používat; zalehnutí = důsledek těsna (postoj KPZ); „často hned po porodu“; nastudovat veganskou etiku. | `scripts/tts.py` (Piper → vo.wav + vo-timing.js + vo.srt), `VOX.captions/vo/wordT`, `runtime/vox-icons.js` (kráva, tele, ikony), svislý kontaktní arch, `brand/kpz/` (loga, etika, slovník). |
| 2026-10-14 | 0.3.0 | kpz-telata v2 | „tzv. masné krávy / tzv. dojnice“; masné krávy jen u hygieny a zalehnutí; místo EFSA veganský pohled; „často hned“; „několik argumentů, nejčastější…“; hygiena = celý kravín, hustota; pojmenovat problémy; chovy s kontaktem nejsou ideál (býčci, tzv. dojnice na jatka, zvíře není stroj ani zboží); 4. argument přebytek mléka; víc informací, delší OK; citlivost krav; tempo hlasu OK. | Pravidla KPZ do `brand/kpz/README.md`; obecná pravidla sem; `hlDark` vzor pro tmavé scény; scénář a scéna v2. |
| 2026-10-14 | 0.3.1 | kpz-telata v2 | Instagram – zvolena varianta pod 3:00. | Zkrácený scénář (177 s), plná verze zálohována (`vo-plna.json`, `reel-plna.html`, `assets-plna/`). Renderer kopíruje zvuk do temp a snese předčasný konec ffmpeg (dřív přepsání `vo.wav` během renderu rozbilo plnou verzi). SKILL.md: Piper není deterministický, limity platforem. |
| 2026-10-14 | (v3 – zadání) | kpz-telata | Hook na začátek místo popisu krav; hygiena = podlaha, moč, bakterie; „jak jinak než tele a jeho máma“; „velkokapacitní haly“ místo stájí; pouto „údajně“; „Není to bizarní?“; farmy s kontaktem přísněji + zabíjení; článek KPZ jako podklad. | Pravidla do `brand/kpz/README.md`, článek do `brand/kpz/clanky/`; obecné pravidlo „hook první“ sem. Video v3 čeká na odpovědi na otázky. |
| 2026-10-15 | 0.3.2 | kpz-telata v4 | KPZ upravili scénář v textu (hook „Věděli jste…“, „tzv. chovatelů“, bez věty „počítá s tím…“, „bizarní důsledek systému“, „mašina“ bez „krutá“, „bere mléko pro lidi“); pokud se nevejde, zrychlit. | Workflow „scénář v textu“ do pravidel; hlas 0.75; scéna v4 (zálohy v3-ig). |
| 2026-10-19 | 0.4.0 | kpz-telata v4-kpz | KPZ poslali svou grafiku (font Bebas Neue): „zkus to udělat podobně“; inspirovat se jen vizuální stránkou, obsah neřešit; fotky z grafiky nebrat – jde o font, barvy a styl; detail známky nikam (čísla). | Téma `brand/kpz/kpz-theme.css/js` (bloky po řádcích, růžový papír, grunge, linoryt nálepky, štětec, kulaté logo, titulky v blocích), `VOXI.palette`, titulky dělené na úseky `.cap-run/.cap-hl`, `render.mjs`: JPEG snímky (5× rychlejší) a `--stills`; scéna `reel-kpz.html`; pravidlo o srovnání s lidskými tragédiemi → rozhoduje KPZ. |
