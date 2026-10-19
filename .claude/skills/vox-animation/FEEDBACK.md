# Feedback & vývoj skillu

**Verze skillu: 0.8.0**

Tento soubor je paměť skillu. Pravidla níže mají **přednost** před
`references/style-guide.md`. Postup zápisu je v `SKILL.md` → „Smyčka zpětné vazby“.
Pravidla specifická pro organizaci KPZ (obsah, tón, slovník) jsou v
`brand/kpz/README.md`.

## Pravidla z feedbacku

- **[workflow]** Před výrobou obsahového videa nejdřív rešerše a ověření tvrzení; výroba až na výslovný pokyn. _(2026-10-14, kpz-telata)_
- **[workflow]** Před psaním scénáře pro KPZ si projít hodnotový rámec v `brand/kpz/README.md` (veganská etika). _(2026-10-14, kpz-telata)_
- **[formát]** Reely pro sítě: **9:16, 1080×1920**. Grafika v zóně y 260–1300, titulky kolem y 1470, spodek (>1560) a pravý okraj (x>960 v dolní polovině) nechat volný kvůli UI sítí. _(2026-10-14, kpz-telata)_
- **[titulky]** Titulky **ano** – vypálené, součást designu: kousky po 2–5 slovech, papírový pruh, klíčové slovo žlutě. Kde je věta už velkým textem v animaci, titulek vypnout (`cap: false`). _(2026-10-14, kpz-telata)_
- **[titulky]** Čísla s mezerou (9 500) se mezi titulky nedělí – číslo musí být celé v jednom kousku (`tts.py` → pevná mezera). _(2026-10-19, kpz-telata v5)_
- **[zvuk]** Voiceover: Piper, hlas `cs_CZ-jirka-medium` (`scripts/tts.py`). Bez patetické hudby. _(2026-10-14, kpz-telata)_
- **[branding]** Logo KPZ jako vodoznak vlevo nahoře + logo v outru (`brand/kpz/`). _(2026-10-14, kpz-telata)_
- **[data]** Na obrazovce u každého tvrzení drobný řádek „Zdroj: …“; plný seznam zdrojů do popisku příspěvku. _(2026-10-14, kpz-telata)_
- **[obsah]** Víc informací má přednost před krátkou stopáží – délka může přesáhnout 90 s. Hlídat jen limity platforem. _(2026-10-14, kpz-telata v2)_
- **[tempo]** Rychlost hlasu `length_scale` 0.83 je v pořádku – nezpomalovat. Když se text nevejde do limitu, smí se zrychlit (v4: 0.75 na pokyn KPZ). _(2026-10-14/15, kpz-telata)_
- **[workflow]** Úspornější iterace: exportovat text hlasu do `scenar-vN.md` (sekce = záběry), KPZ ho upraví a pošle zpět; text převzít, opravit jen pravopis a zjevné překlepy (a říct které), sladit kotvy ve scéně, jeden render. _(2026-10-15, kpz-telata v4)_
- **[workflow]** Drobné připomínky „do další verze“ zapisovat do `scenes/<projekt>/dalsi-verze.md` a nevyrábět, dokud KPZ neřekne. _(2026-10-19, kpz-telata)_
- **[komunikace]** S KPZ si **tykáme**. _(2026-10-19)_
- **[workflow]** Když KPZ upraví scénář, projít i **část B (texty v grafice)** a každou změnu propsat do scény – ne jen hlas. _(2026-10-19, kpz-telata v5)_
- **[vizuál]** Žádný záběr nenechat několik sekund „prázdný“ (jen nadpis) – doplnit ilustraci / výstřižek k tomu, co zrovna zní. _(2026-10-19, kpz-telata v5)_
- **[tón]** Komentář nesmí znít jako strojové odříkávání argumentů: vkládat doložené, lidsky srozumitelné momenty (co zvířata prožívají), ironii z kontrastu, krátké pointy na tmavém pozadí. _(2026-10-14, kpz-telata v2)_
- **[obsah]** Problémy pojmenovávat konkrétně („velkokapacitní kravín, spousta krav na malém prostoru“), ne abstraktně („systém“). _(2026-10-14, kpz-telata v2)_
- **[formát]** Pro Instagram držet reel **pod 3:00** (zkrácená varianta); plnou verzi lze dát jinam. Při zkracování nechat čísla a detaily na obrazovce a vypustit je jen z hlasu. _(2026-10-14, kpz-telata v2)_
- **[struktura]** Začínat **hookem** (nejsilnější konkrétní fakt), ne úvodním popisem. Kontext a citlivost zvířat až za hookem. _(2026-10-14, kpz-telata v3 – zadání)_
- **[technika]** Na tmavém pozadí zvýrazněný text musí být čitelný i před podbarvením (světlý → tmavý při zvýraznění). _(2026-10-14, kpz-telata v2)_
- **[vizuál]** Když klient pošle svou grafiku „ať je to podobné“: převzít **jen vizuál** (písmo, barvy, textury, tvary bloků, dekor, logo), ne obsah, hesla ani fotky – fotky jen ty, které klient dodá k videu. Styl zapsat jako téma do `brand/<klient>/`. _(2026-10-19, kpz-telata v4-kpz)_
- **[obsah]** Žádný samostatný detailní záběr na ušní známku. Na známkách **rozostřit jen samotné číslo** (`scripts/tag_retouch.py --rect` kolem čísla; plocha a tvar známky zůstanou ostré). Ne rozmazaný flek přes ucho („vypadá strašně“), ne přebarvení („nevypadá dobře“), ne celá plocha známky. Nečitelně malá čísla nechat být. _(2026-10-19, KPZ)_
- **[vizuál]** Textury („grunge“, špína) dávkovat střídmě – na blocích s textem a na písmu jen jemně, aby nešpinily čitelnost. _(2026-10-19, kpz-telata v4-kpz)_
- **[vizuál]** Skutečné fotky zvířat ve 4–6 klíčových momentech (hook, tele samo, hala, pastva, pouto), ilustrace na vysvětlování; ne rychlá montáž fotek na konci. _(2026-10-19, kpz-telata v5)_
- **[vizuál]** Fotky ne celé přes obraz, ale jako **papírové výstřižky**: zvíře vystřižené s okrajem z utrženého papíru (`scripts/cutout.py`), prostředí jako utržený kus fotky. _(2026-10-19, kpz-telata v5)_
- **[vizuál]** Ve výstřižcích jen **celá zvířata** – žádné useknuté půlky těla (fotka oříznutá okrajem = nepoužít). _(2026-10-19, kpz-telata v5)_
- **[technika]** Render snímků přes JPEG q95 (PNG zrnitých textur ~1 s/snímek); celoplošné SVG filtry kreslit jednou do canvasu, ne v každém snímku. _(2026-10-19)_

## ✅ Osvědčené (nechat tak)

- Hlas Jirka (Piper) při `length_scale` 0.83 – tempo „v pohodě“. _(kpz-telata v1)_
- Vizuální styl KPZ (Bebas Neue, bloky po řádcích, růžový papír, nálepky, titulky v blocích) – „Je to dobrý.“ _(kpz-telata v4-kpz)_
- Čísla na známkách rozostřená jen uvnitř známky – „jo, to vypadá líp.“ _(kpz-telata v5)_

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
| 2026-10-19 | 0.4.1 | kpz-telata v4-kpz | „Je to dobrý.“ Logo jako ve starších verzích (ne kulaté); bloky a text zbytečně špinavé – o 50 % míň. | `kpz-print` / `kpz-print-soft` poloviční síla (hrany i vybledlá místa); klasické logo `logo-kpz-svetle.png` jako vodoznak + v outru, na tmavých záběrech skryté; README KPZ upraveno. |
| 2026-10-19 | (v5 – scénář) | kpz-telata | KPZ poslali upravený scénář (drobné úpravy hlasu, nadpis „Krávy se dají zneužívat i „šetrněji““); zvažují skutečné fotky krav a telat – v průběhu videa, nebo 4s záblesk na konci. | Uloženo jako `scenar-v5.md` (opraveno: „krávámi“ → „kravami“, rovné uvozovky → české). Render čeká na rozhodnutí o fotkách. |
| 2026-10-19 | 0.5.0 | kpz-telata v5 | „…ale dej tam ‚a telata tam zůstávají‘“, „v drtivé většině (chovů)“; fotky zkusit najít na internetu provizorně (pak dodají vlastní), chtějí vidět, jak to vypadá. | Hlas v5 (`vo-v5.json`, `assets-v5/`, kratší pauzy → 2:58,7); scéna `reel-kpz-foto.html` s 6 provizorními fotkami (Unsplash přes HF), `.kpz-photo` v tématu, `scripts/hf_photos.py`, postup 2f v SKILL.md. |
| 2026-10-19 | 0.6.0 | kpz-telata v5 | „Zvládl bys zvířata oříznout a dát jim papírový okraj / utržený papír? Celé fotky jsou divné.“ | `scripts/cutout.py` (BiRefNet lite z HF + utržený okraj), `.kpz-cut` v tématu; scéna: kráva s teletem a tele v kreslené boudě jako výstřižky, hala a pastvina jako utržené kusy fotek, krávy na kreslené pastvě, pouto jako výstřižek. |
| 2026-10-19 | 0.6.1 | kpz-telata v5 | „Určitě nepoužívej krávy, které mají useklou půlku těla.“ | Výstřižky s oříznutými zvířaty vyřazeny; nové fotky s celými zvířaty z COCO (tele saje, tele olizuje matku, kráva s telaty, stádo s telaty); pravidlo do FEEDBACK, SKILL a README fotek. |
| 2026-10-19 | 0.6.2 | kpz-telata v5 | „Přes 9 500 litrů“ – devítka oddělená od 500, dát dohromady (nevadí o 0,5 s později); zapsat do další verze, zatím nic nevyrábět. | `tts.py`: čísla s mezerou drží pevná mezera (nedělí se mezi titulky); `scenes/kpz-telata/dalsi-verze.md` jako seznam úprav do příští verze. Nic nepřegenerováno. |
| 2026-10-19 | (do další verze) | kpz-telata v5 | 2:30 prázdná obrazovka – přidat „koření“; 2:16 „Jde to jinak“ zní jako schvalování → „Krávy se dají zneužívat i „šetrněji““; 0:28 karty argumentů sjednotit jednou barvou; fotky dodá KPZ. Zatím nevyrábět. | Zapsáno do `scenes/kpz-telata/dalsi-verze.md` (body 3–5). Poučení: text z části B scénáře propsat do scény hned (nadpis „Jde to jinak“ zůstal). |
| 2026-10-19 | 0.7.0 | kpz-telata v5 | KPZ dodali vlastní fotky (tele v boudě, řada boud, farma z výšky, kravín zevnitř, vrata kravínu); „líbí se mi tele fyzicky a za ním animovaná boudička – zkus i skutečnou“; „ořež to jako předtím“; „zadělávání známek vypadá strašně, vyser se na to“. | Fotky KPZ v `assets/foto-kpz/` (bez rozmazání), výstřižky; `cutout.py --largest --scale`; 4 varianty záběru „samo v boxu“ (A tele v kreslené boudě, B skutečná bouda, C řada boud, D farma z výšky) přepínané `BOX` ve scéně; hygiena = kravín KPZ; pravidlo: známky nerozmazávat. |
| 2026-10-19 | 0.7.1 | kpz-telata v5 | „Známky jdou zadělat tak, aby nesvítily – místo textu se dá barva známky.“ + fotka krávy se sajícím teletem (vlastní nález KPZ), „zkus podle sebe“. | `scripts/tag_retouch.py` (text uvnitř známky → místní barva známky, oblasti `--box`); fotky KPZ přebarveny, výstřižky znovu; úvod = kráva se sajícím teletem; bouda = varianta A. |
| 2026-10-19 | 0.7.2 | kpz-telata v5 | Přebarvení známek „taky nevypadá dobře – udělej gaussian blur, prostě číslo rozostříš“ → „jo, to vypadá líp“. | `tag_retouch.py --mode blur` (výchozí): rozostření jen uvnitř konvexního obrysu známky, sláma/ucho odfiltrované; fotky a výstřižky znovu. |
| 2026-10-19 | 0.8.0 | kpz-telata v6 | „Rozostři jen to číslo, ne celý prostor známky“; fotka masného skotu (KPZ) + „můžeš začít“; „tykej mi“. | `tag_retouch.py --rect` (obdélník čísla, oříznuto na plochu známky; `--hue/--sat` pro růžové známky, `--noclip`); ikony `cheese`, `yogurt`; **v6**: hlas přegenerován (9 500 v jednom titulku, 2:59,2), úvod kráva se sajícím teletem (KPZ), tele KPZ v kreslené boudě, kravín KPZ, pastva = masný skot KPZ, karty argumentů jednou barvou, nadpis „„Šetrnější“ chov? Pořád využívání.“, ve 2:30 mléko/sýr/jogurt. |
| 2026-10-19 | (do v7) | kpz-telata | „Teď ti budu dávat nápady, až je nahromadím, přidáš je do videa – ukládej si to.“ #1: do boudy v 0:18 dát nové tele (tele-studio). #2: někam vložit individuální boxy ze záběru z výšky (ořez kolem bud). | Sekce „Do v7“ v `dalsi-verze.md`; foto + výstřižek připraveny, scéna zatím beze změny. |
