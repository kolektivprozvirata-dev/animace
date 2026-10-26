# Úpravy do další verze

**v6 (2026-10-19) – body 1–5 zapracovány** (`reel-kpz-foto.html`, hlas `assets-v5/`, render `out/kpz-telata-reel-v6.mp4`).
Nové připomínky přidávat pod tabulku; nevyrábět bez pokynu KPZ.

Seznam změn, které se mají promítnout při příštím renderu reelu o telatech.

| # | datum | úprava | stav |
|---|---|---|---|
| 1 | 2026-10-19 | Titulky: „přes **9 500** litrů“ – devítka nesmí být oddělená od 500, číslo musí být v jednom titulku. Nevadí, když se 9 objeví o ~0,5 s později. | hotovo v6 |
| 2 | 2026-10-19 | Fotky: KPZ dodali tele v boudách, řadu boud, farmu z výšky a kravín (zevnitř, vrata) – zapracováno do `reel-kpz-foto.html` (hygiena = kravín KPZ, „samo v boxu“ = varianta podle volby A/B/C/D). Čísla na známkách rozostřená uvnitř známky. „Samo v boxu“ = **varianta A** (tele KPZ v kreslené boudě, `BOX = 'a'`); úvod = kráva se sajícím teletem od KPZ. Zbývá provizorní: pastviny (hygiena, zalehnutí) a pouto. | hotovo v6 (pastva u hygieny = masný skot KPZ; provizorní zůstává zalehnutí a pouto) |
| 3 | 2026-10-19 | **2:30** („Pokud ale konzumujete mateřské mléko nebo sýry…“, ~2:28–2:33) – obrazovka je prázdná, nahoře jen „Ani tady nehledejte útěchu“. Přidat „koření“: při slovech „mateřské mléko nebo sýry“ naskočí výstřižky / ilustrace mléka, sýra a jogurtu (+ linoryt nálepka), pak je vystřídají řádky Býčci → Jatka, Tzv. dojnice → Jatka. | hotovo v6 |
| 4 | 2026-10-19 | **2:16** – nadpis nad kartou farem „Jde to jinak“ zní, jako bychom to schvalovali → nový text (původní návrh „Krávy se dají zneužívat i „šetrněji““ stál ve scénáři v5, část B – ve scéně nebyl propsán). KPZ vybrali alternativu: **„„Šetrnější“ chov? Pořád využívání.“** | hotovo v6 |
| 5 | 2026-10-19 | **0:28** – karty 4 argumentů (Hygiena, Zalehnutí, Pouto, Přebytek mléka) mají každá jinou barvu → **všechny stejnou barvou**. | hotovo v6 |

Při další verzi: přegenerovat hlas a časování (`tts.py vo-v5.json --out-dir assets-v5`),
zkontrolovat délku pod 3:00 a kotvy slov ve scéně, pak jeden render.

## v7 (2026-10-19) – body 1–5 zapracovány, render `out/kpz-telata-reel-v7.mp4`

| # | datum | úprava | stav |
|---|---|---|---|
| 1 | 2026-10-19 | **0:18** „samo v boxu“ – do kreslené boudy dát nové tele od KPZ (`assets/foto-kpz/tele-studio.jpg`, celé, žluté známky bez čísel). Výstřižek připraven: `vystrizky/tele-studio.png` (ve scéně vyměnit `#h-bcalf` img; tele je vyšší a štíhlejší → doladit šířku/pozici). | hotovo v7 |
| 2 | 2026-10-19 | **Individuální boxy z výšky** (záběr z dronu, ořez kolem řad boud): utržený kus `vystrizky/boudy-z-vysky.png` (z `farma-z-vysky.jpg`). Umístění (KPZ potvrdili): 0:13–0:15 při „Tele pak **v drtivé většině chovů**…“ naskočí boudy z výšky se štítkem **„Desítky boxů, v každém jedno tele bez mámy“** (text KPZ), při „samo v boxu“ je vystřídá detail – nové tele v kreslené boudě (bod 1). | hotovo v7 |
| 3 | 2026-10-19 | **1:10** (zalehnutí, „U tzv. masných krav na pastvě se to prakticky neděje.“, ~1:07–1:11) – místo provizorní kreslené pastvy s krávou galloway dát fotku KPZ: stádo na pastvině s ležícími telaty (`assets/foto-kpz/pastva-stado.jpg`) jako utržený kus `vystrizky/pastva-stado.png` (panel `#z-past`; štítek „Tzv. masné krávy: prostor“ nechat). Fotka má jen 745 px → ve videu trochu měkká. | hotovo v7 |
| 4 | 2026-10-19 | **Fotky z pastvy ne jako pravidelný obdélník**, ale nepravidelný utržený kus (KPZ vybrali variantu **B**, `cutout.py --shape blob`). Připraveno: `vystrizky/masny-skot-tvar.png` (hygiena) a `vystrizky/pastva-stado-tvar.png` (1:10, zalehnutí). Platí i pro další krajinné fotky. | hotovo v7 |
| 5 | 2026-10-19 | Vyřezané fotky se lehce třesou jako papír (nápad KPZ, „nechám to na tobě“) – `jiggle()` ve scéně: 2 px / 0,6°, 6× za sekundu. | hotovo v7 |

## v8 (2026-10-20) – zapracováno, render `out/kpz-telata-reel-v8.mp4`, scénář `scenar-v8.md`

| # | datum | úprava | stav |
|---|---|---|---|
| 1 | 2026-10-19 | **Oprava faktu (~2:12, alt1):** „Přitom v Evropě je přes sto mléčných farem…“ je zavádějící – 104 je počet farem **dotázaných v jedné studii** (Eriksson et al. 2022: AT 15, CH 11, DE 21, FR 26, IT 19, SE 12; nereprezentativní vzorek, celkový počet takových farem nikdo neeviduje). Návrh hlasu: „Přitom **jen jedna studie popsala** přes sto mléčných farem, kde tele zůstává s matkou týdny až měsíce.“ Karta: „Jedna studie · 6 zemí Evropy · 104 farem“. Hlídat délku pod 3:00 (+~0,6 s). | hotovo v8 |
| 2 | 2026-10-19 | **Opravy z ověření tvrzení** – viz `overeni-tvrzeni.md`, tabulka „Shrnutí“ (#2 důvod vyřazení dojnic, #3 12 hodin = praxe 87,5 % farem, #4 pouto doložené, #5 zalehnutí, #6 1989: 3 982 l, #7 zdrojové řádky a popisek). Formulace schvaluje KPZ. | hotovo v8 |
| 3 | 2026-10-20 | **Rozhodnutí KPZ k ověření:** (a) dojnice: „…a tzv. dojnice taky, když přestanou být **pro lidi výnosné**.“ (text KPZ); řádek „Tzv. dojnice – nemoci, neplodnost, nízký výkon → Jatka (ČR: vyřazena průměrně ve 3.–4. laktaci)“. (b) 104 farem: „Přitom **jen jedna studie popsala** přes sto mléčných farem, kde tele zůstává s matkou týdny až měsíce.“ + karta „Jedna studie · 6 zemí Evropy · 104 farem“. (c) 12 h: návrh „Na naprosté většině českých farem se tele odebírá matce do 12 hodin po porodu. Často je to ale hned.“ + štítek „Do 12 h – 87,5 % farem“, zdroj Staněk et al. 2014 (VÚŽV) – čeká na potvrzení. (d) pouto: KPZ se ptali na nezávislost studií – odpovězeno (3 nezávislé týmy + EFSA), formulace čeká. (e) zalehnutí: argument zůstává (farmáři ho uvádějí na sociálních sítích, o zalehnutí na pastvě nejsou zprávy); návrh zpřesnit „…se o zalehnutí prakticky neslyší“ a „Mezi ty, které slýcháme nejčastěji, patří tyto čtyři“ – čeká. **Délka:** změny dají ~+1 s → 2:59–3:00, zkrátit pauzy. | hotovo v8 |
| 4 | 2026-10-20 | **Rozhodnuto KPZ:** (c) 12 h = varianta **A**: „Na naprosté většině českých farem se tele odebírá matce do 12 hodin po porodu. Často je to ale hned.“, štítek „Do 12 h – 87,5 % farem“, zdroj Staněk et al. 2014 (VÚŽV). (d) pouto: „Pozdější oddělení podle výzkumů bolí víc.“ (KPZ chtějí „bolí“ – psychická bolest; bez „prý“/„některých zdrojů“); graf „1. den“ / „později (4.–14. den)“, zdroj „Stěhulová et al. 2008 (VÚŽV) · Weary & Chua 2000 · Flower & Weary 2001“. (e) zalehnutí: „Mezi ty, které slýcháme nejčastěji, patří tyto čtyři.“ + „U tzv. masných krav na pastvě, kde je dost místa, se o zalehnutí prakticky neslyší.“ **Hlas zrychlit o ~3 %** (length_scale 0.75 → 0.73), cíl **max. 2:58** (nejistota, zda IG bere přesně 3:00). | hotovo v8 |
| 5 | 2026-10-20 | **Fotka mateřského pouta** od KPZ: kráva se sajícím teletem (holštýnka) – `assets/foto-kpz/pouto-krava-tele.jpg`, výstřižek `vystrizky/pouto-krava-tele.png`; nahradí provizorní „tele olizuje matku“ (scéna pouto, ~1:17). Známka bez čísla – bez úprav. | hotovo v8 |
| 6 | 2026-10-20 | **Nápad KPZ: zmínit studie o škodách.** Návrh do pouta za „Pozdější oddělení podle výzkumů bolí víc.“: „**Přitom výzkumy zároveň ukazují, že tele, které zůstane s mámou déle, lépe roste a je společenštější.**“ (Flower & Weary 2001; Meagher 2019), pak „Takže aby je odloučení nebolelo, odloučí je dřív.“ Štítek „S mámou déle: rychlejší růst, víc společenské“. +~3 s → hlídat 2:58. | hotovo v8 |

## v9 (2026-10-20) – zapracováno, render `out/kpz-telata-reel-v9.mp4`, scénář `scenar-v9.md`

| # | datum | úprava | stav |
|---|---|---|---|
| 1 | 2026-10-20 | **Hygiena: porodna + hala** (KPZ: „pojmi to do videa“; haly nechat – kdyby tele šlo s mámou do haly, je tam hnůj a moč). Návrh hyg2: „Jenže krávy často rodí ve společných porodnách, kde se nákazy snadno šíří. A s mámou by tele muselo do velkokapacitní haly: spousta krav na malé ploše, výkaly a moč přibývají průběžně. A i když bývají většinou uklízeny, bakteriím se tam logicky daří.“ Obraz: kreslená společná porodna (víc krav) + štítek „Společná porodna: 2/3 farem“ → foto haly + „Výkaly + moč = bakterie“. Zdroj: Staněk 2014 · VÚŽV 2023 („infekční agens v porodním kotci“) · EFSA 2023 (oddělení nenahrazuje hygienu porodny). Délka +~3,5 s → hlas 0.72 → 0.71 + kratší pauzy, cíl ≤ 2:58. | hotovo v9 (hlas 0.705, kratší pauzy → 2:56,9) |

## v10 (2026-10-20) – render `out/kpz-telata-reel-v10.mp4` (hlas v9 beze změny)

| # | datum | úprava | stav |
|---|---|---|---|
| 1 | 2026-10-20 | **Pravidlo: zvíře = fotka, kresba = věci a schémata** (KPZ: „není divné, že je tam občas fotka a občas animace?“ → „zkus to“). Úvod: kreslená kráva + tele + nůžky → výstřižek krávy s teletem, při „hned“ se tele **vytrhne** (díra ve tvaru telete; `scripts/tear_pair.py`); hygiena: tele = tele-studio; přebytek mléka: fotka pouta (tele saje) + šipka „Pro tele“; řádky → Jatka: vytržené tele a máma s dírou z úvodu; společná porodna jako schéma shora (jako hala). | hotovo v10 |

## v11 (2026-10-21) – render `out/kpz-telata-reel-v11.mp4`, hlas `vo-v11.json` → `assets-v11/` (2:56,3), scénář `scenar-v11.md`

| # | datum | úprava | stav |
|---|---|---|---|
| 1 | 2026-10-21 | **0:09–0:11 vytržení telete** – po odtržení krávě chybí kus těla (díra po teleti), působí divně. KPZ dodali dvojici srovnaných fotek holštýnky: s kojícím teletem (`foto-kpz/krava-tele-hol.webp`) a stejnou krávu bez telete (`krava-sama-hol.webp`). Postup: před vytržením `vystrizky/trh2-par.png` (kráva + tele), v okamžiku trhnutí výměna za `trh2-mama.png` (celá kráva) + `trh2-tele.png` odjíždí pryč (`scripts/tear_swap.py` – maska z průhledného pozadí fotek, nohy krávy za teletem vyříznuté `--cut`; plátno 994×656). Fotky ověřit práva před zveřejněním. | hotovo v11 |
| 2 | 2026-10-21 | **Úvod 0–4 s:** místo tzv. masné krávy (hnědá, `krava-s-teletem`) dvojfotka holštýnky s teletem (`trh2-par`) – mluvíme o mléčných kravách. Fotka pak plynule přejede na místo v hooku (stejná kráva). | hotovo v11 |
| 3 | 2026-10-21 | **0:18 časová osa s nůžkami:** vyřadit „Měsíce“ (o tom by se dalo diskutovat); zbylé 4 body (Hned · 12 h · 1 den · Týden) roztáhnout přes celou osu, nůžky naskakují pomaleji přes celou větu. | hotovo v11 |
| 4 | 2026-10-21 | **1:41 přebytek mléka:** jiná fotka než pouto (to už je ve videu několikrát) → „další kráva“: holštýnka, pod ní ležící tele (`krava-tele-lezi`); šipka „Pro tele“ vede k hlavě telete. | hotovo v11 |
| 5 | 2026-10-21 | **1:42 hlas:** „Kráva ale dává mléko pro tele.“ → KPZ: „…primárně pro tele“, nebo varianta „Jako každá máma, tak i kráva dává mléko primárně pro tele.“ (mateřská nota). Zvoleno: „**Jako každá máma, i kráva dává mléko *primárně pro tele.***“ | hotovo v11 |
| 6 | 2026-10-21 | **2:26 hlas:** „…přebytek mléka je výmluva chovatelů, ne důvod.“ → „…výmluva chovatelů, **která se jim hodí**, ne důvod.“ Délka: hlas 0.705 → 0.69 (~2 % rychleji) → 2:56,3. | hotovo v11 |
| 7 | 2026-10-21 | **2:36 řádek „Tzv. dojnice → Jatka“:** fotka krávy s celým tělem („Celé tělo“, `krava-cele-telo`). | hotovo v11 |
| 8 | 2026-10-21 | **2:40 řádek „Býčci → Jatka“:** fotka „Růžové“ – býček s růžovými známkami (`tele-ruzove`). | hotovo v11 |

## v12 (2026-10-23) – render `out/kpz-telata-reel-v12.mp4`, hlas `vo-v12.json` → `assets-v12/` (2:56,7), scénář `scenar-v12.md`

| # | datum | úprava | stav |
|---|---|---|---|
| 1 | 2026-10-21 | **~0:59 zalehnutí – neprůstřelnost** (KPZ: telata v hale v ČR nikdy nejsou, jak můžeme tvrdit, že tam hrozí?). Rešerše (`overeni-tvrzeni.md` B5+): riziko se ve zdrojích váže na tlačenici (společné porodny, přeplněné haly), ne na matku; „hlavně“ nikdo nezměřil. Varianty s porodnou a halou („A prý taky v hale, kam by tele muselo, kdyby zůstalo s mámou“) vyšly dlouhé a složité → KPZ: zjednodušit. **Schválené cru2:** „To údajně hrozí **tam, kde je moc krav na malém prostoru.** Na pastvě u tzv. masných krav se o zalehnutí prakticky neslyší.“ Délka ≈ jako dosud (bez zrychlení). Obraz beze změny (přeplněná hala s teletem); kotva štítku `W('cru2','moc krav')`. | hotovo v12 |

## v13 (2026-10-24) – render `out/kpz-telata-reel-v13.mp4`, hlas ElevenLabs `vo-v13.json` → `assets-v13/` (2:55,4), nahrávky v `el-cache/`

| # | datum | úprava | stav |
|---|---|---|---|
| 1 | 2026-10-24 | **Hlas ElevenLabs** místo Piperu – hlas KPZ `7JbZPqJGWUfXXBim0T8U`. Předpoklad: KPZ přidají network secret (Allowed websites `api.elevenlabs.io`, hlavička `xi-api-key` bez prefixu). Postup: `tts.py vo-v12.json --engine elevenlabs --voice-id 7JbZPqJGWUfXXBim0T8U --out-dir assets-v13`, poslech výslovnosti (tzv., 9 500, 12 h), délka ≤ 2:58 (`speed`/pauzy), render. | hotovo v13: hlas **dSByRdUbTGloB7TFA1qD** (KPZ: „jo dobrý“; zkoušeny i 7JbZ a Fpj3 – ten o 60 % pomalejší), nádechy vystřižené (`debreath`), pauzy na koncích vět +0,15 s; úvodní otázka hook0 = varianta **E** (`eleven_v3`, bez kontextu – „nejlepší“, víc zní jako otázka); délka 2:55,4; text beze změny proti v12 (`scenar-v12.md`). |

## v14 (2026-10-24) – render `out/kpz-telata-reel-v14.mp4`, hlas `vo-v14.json` → `assets-v14/` (2:57,1), scénář `scenar-v14.md`

| # | datum | úprava | stav |
|---|---|---|---|
| 1 | 2026-10-24 | **2:42 „Zvíře není stroj ani zboží.“** (alt3) – říct důrazněji / důsledněji. Návrh: pár verzí jen této věty (`eleven_v3` jako u otázky, příp. „Zvíře. Není stroj. Ani zboží.“ jen v `say`, titulek beze změny), poslat na výběr, vybranou zapsat jako `"el"` u alt3. Rezerva do 2:58 ≈ 2,6 s. | KPZ: místo jiného podání **ticho ~0,5 s před i za větou**, ať vynikne jako heslo/slogan („šel bych do této verze“ → původní nahrávka alt3) → `pause` u alt2b a alt3 tak, aby skutečné ticho bylo ~0,5 s | hotovo v14 |
| 2 | 2026-10-24 | **Propad zvuku po vystřižených nádeších** (ve sluchátkách je slyšet „uříznutí“ – úplné digitální ticho proti „vzduchu“ v řeči). Návrh: pod celý hlas velmi tichý „room tone“ (šum prostoru podle tichých míst nahrávky), nádechy neřezat do nuly, ale ztlumit o ~20–25 dB s delšími přechody (~40 ms); ukázka A/B na poslech. Z cache, bez placení. KPZ: slyšet hlavně v **0:25** před „Za prvé: hygiena“ + „něco divnýho“ → rozbor: na konci věty „…tyto čtyři.“ (why) je v nahrávce ElevenLabs po 0,3 s ticha krátké lupnutí (10 ms, −26 dB, uříznutý začátek dalšího zvuku – není to nádech, debreath ho nechal). Totéž v **1:14,5** na konci „…tele a jeho máma.“ (cru3, 20 ms). Jinde po úpravě nic. Oprava: za posledním slovem segmentu po tichu (≥ 50 ms) zbytek odříznout s fade; pak room tone. | **oprava hotová v `tts.py`** (2026-10-24, KPZ znovu: „v 1:14 jde slyšet, že je to násilně střihlý“): `clean_edges` ztlumí zvuk za posledním / před prvním slovem segmentu (lupnutí 0:25 −34 dB a 1:14 −18 dB pryč, délka beze změny), přechody u nádechů 20 ms, `room_tone` −66 dBFS pod celým hlasem (nikde digitální ticho; tvrdé skoky 171 → 13 přirozených náběhů). Ukázka A/B `out/zvuk-*.mp3` poslána → hotovo v14 |
| 3 | 2026-10-24 | **~1:09 cru3 hlas:** „Problém je opět v malém prostoru, který vytvořili chovatelé.“ – KPZ: prostor není malý (kravíny jsou obrovské, jen je v nich hodně krav), „tlačenice“ je moc silná, „haly“ vynechávají porodny. Zvoleno (KPZ: „nechám to na tobě“): **„Problém je opět v tom, kolik krav chovatelé nahromadí na jedno místo.“** (porodny i haly, chovatelé jako ti, kdo to dělají; refrén „Problém je… / Odnese to… tele a jeho máma“ zůstává). Varianta „…moc krav na jednom místě. A to je rozhodnutí chovatelů.“ zamítnuta (druhá pointa těsně před „Odnese to zase…“, +1,5 s). Ostatní „moc krav **na** malém prostoru“ (hyg2, cru2, štítky) nechat – vyjadřuje hustotu, ne malý kravín. Sousední věty (cru2, bon1) nechat beze změny – při generování držet jejich kontext (stejný previous/next text), ať se nepřegenerují. | hotovo v14 (nová nahrávka jen cru3; cru2 a bon1 s pevným starým kontextem = beze změny) |
| 4 | 2026-10-24 | **0:04 hook1 „Na naprosté většině…“** – po otázce zní „chcíple“, má začít silněji jako nová věta (hlasitost je stejná, jde o podání: v2 s kontextem navazuje na otázku). Varianty v kontextu (`out/veta2-*.mp3`); KPZ: **E** – `eleven_v3` bez kontextu („není to dokonalý, ale jde to“) → u hook1 `"el": {"model_id": "eleven_v3", "context": false}`; +0,7 s. | hotovo v14 |
| 5 | 2026-10-24 | **~2:38 alt2b „…mají možná o trochu lépe.“** – „lépe“ nezní jako konec věty (hlas navazoval na další větu). Varianty v kontextu i s tichem kolem hesla (`out/lepe-*.mp3`): A původní (−3,5 půltónu na konci), **B** pevný kontext `"next_text": ""` – zná předchozí větu, ví, že tu věta končí (−5,7, nejvíc klesá; doporučeno), D bez kontextu (−2,6). | KPZ: **D** (bez kontextu) → `"el": {"context": false}` | hotovo v14 |

Ticho kolem hesla vyšlo samo (alt2b bez kontextu končí delší pauzou): před 0,59 s, za 0,56 s.

## v15 (2026-10-25) – render `out/kpz-telata-reel-v15.mp4`, hlas `vo-v15.json` → `assets-v15/` (2:56,3), scénář `scenar-v15.md`

| # | datum | úprava | stav |
|---|---|---|---|
| 1 | 2026-10-24 | **2:15 alt1** – „Přitom **jen** jedna studie popsala…“ → **„Přitom jedna studie popsala přes sto mléčných farem, kde tele zůstává s matkou týdny až měsíce.“** (KPZ: „nevím, proč je tam to ‚jen‘“). „Jen“ pochází z opravy ve v8 (zdůraznit, že 104 je vzorek jedné studie); bez něj je věta pořád přesná – karta „Jedna studie · mléčné farmy · 6 zemí Evropy“ zůstává. Hlas + titulek; přegeneruje se jen alt1, sousedům (loop, alt1b) držet starý kontext (`next_text`/`previous_text`). Délka −0,2 s. | hotovo v15 (nová nahrávka jen alt1; 2:56,3) |
| 2 | 2026-10-24 | **Outro (poslední záběr, ~2:52)** – přidat adresu **www.kolektivprozvirata.cz**. Návrh: pod název „Kolektiv pro zvířata“ (y ≈ 1150) jako blok v tématu KPZ, naskočí chvíli po názvu; „Zdroje v popisku“ posunout níž (y ≈ 1250, pořád v zóně grafiky do 1300). Jen grafika, hlas beze změny (adresu neříká). | hotovo v15 (`#o-web`, krémový blok pod názvem, y 1160; „Zdroje v popisku“ y 1262) |

## v16 (2026-10-25) – render `out/kpz-telata-reel-v16.mp4`, hlas `vo-v16.json` → `assets-v16/` (2:56,4), scénář `scenar-v16.md`

| # | datum | úprava | stav |
|---|---|---|---|
| 1 | 2026-10-25 | **2:13 karta 104 farem** – číslo stojí ~1,5 s na „0 farem“ (počítá až od slova „sto“) → může vypadat jako „žádná farma“. KPZ: **nechat naskočit se začátkem věty** – `count(| **zrušeno** – KPZ: „Beru zpět to s tou nulou. Líbí se mi, jak to z nuly nabíhá na to číslo farem.“ |
| 2 | 2026-10-25 | **0:48 hygiena – fotka tzv. masných krav** (`#g-past`, teď `masny-skot-tvar.png`) vyměnit; KPZ pošlou několik fotek, vybrat jednu a vystřihnout stejně: čísla na známkách rozostřit (`tag_retouch.py --rect`), `cutout.py --shape blob` (nepravidelný utržený kus, šířka ~940 px). Výběr: celá zvířata, pastva s prostorem, ideálně krávy s telaty (věta: „telata tam zůstávají s matkami měsíce“). | ve scéně: KPZ poslali 4 fotky (`masne-pastva-rada/lezi/celem/kojeni.jpg`); 0:48 = **kojeni** (tele pije u krávy, ležící tele, hodně prostoru) → `vystrizky/masne-pastva-kojeni-tvar.png` (blob, crop 225,200,1105,610, ×1,4), `#g-past` šířka 1000, štítek `#g-tag2` y 950. Čísla na známkách nečitelně malá → bez úprav. | hotovo v16 |
| 3 | 2026-10-25 | **1:06 zalehnutí – fotka tzv. masných krav na pastvě** („v 1:06 uděláš to samý“) → **lezi** (tele leží těsně u stojící krávy – k větě „na pastvě se o zalehnutí prakticky neslyší“; býk vpravo mimo výřez) → `vystrizky/masne-pastva-lezi-tvar.png` (blob, crop 110,140,990,650, ×1,3), `#z-past`. Jiná fotka než v 0:48 (pravidlo neopakovat). | hotovo v16 |
| 4 | 2026-10-25 | **1:36 bon5 „Není to bizarní důsledek systému?“** – má znít víc jako otázka. Varianty v kontextu (`out/bizarni-*.mp3`): A původní (konec +0,2 půltónu), C v3 seed 11, **E** bez kontextu (+3,2), **F** bez kontextu seed 33 (+6,4, stoupá nejvíc). | hotovo v16: KPZ „na základě tohoto jdi do další verze“ bez písmene → vybráno **F** (stoupá nejvíc), `"el": {"context": false, "seed": 33}`; po otázce 0,8 s ticha. Na požádání vyměnit za E/C/A. |

## v17 (2026-10-26) – render `out/kpz-telata-reel-v17.mp4`, hlas beze změny (`assets-v16/`, 2:56,4), scénář `scenar-v16.md`

| # | datum | úprava | stav |
|---|---|---|---|
| 1 | 2026-10-25 | **1:06–1:08 zalehnutí – jiná fotka** (KPZ poslali novou: stádo tzv. masných krav, tele leží mezi pasoucími se kravami, další tele u ležící krávy) → `foto-kpz/masne-pastva-lezi2.webp` → `vystrizky/masne-pastva-lezi2-tvar.png` (blob, crop 70,90,1456,700, `--tight 0.8`, seed 66 – zvířata u krajů fotky; nová volba `cutout.py --tight`), `#z-past` šířka 1000, top 450; štítek `#z-tag2` y 960. Zvířata menší (stádo přes celou šířku). Čísla na známkách nečitelná. | hotovo v17 |

## v18 (2026-10-26) – render `out/kpz-telata-reel-v18.mp4`, hlas beze změny (`assets-v16/`, 2:56,4), scénář `scenar-v18.md`

| # | datum | úprava | stav |
|---|---|---|---|
| 1 | 2026-10-26 | **0:36 velkokapacitní hala – 2 fotky KPZ za sebou** místo `kravin-uvnitr`. Vývoj: „vedle sebe, nebo se prostřídají“ → „mohly by být tři“ (koláž hala + 2 bloby) → KPZ: „chci, aby ta vlevo dole byla vidět celá… nebo se vysrat na tu vpravo dole a prostě prostřídat“. Výsledek: při „…do velkokapacitní haly“ **hala zhora** (`#g-photo`, `hala-stan-zhora.png`, logo družstva a DeLaval rozmazané), při „spousta krav“ ji vystřídá **celá fotka krav ve slámě** (`#g-photo2`, `hala-kravy-slama-cela.png`, čísla rozostřená), štítek „Spousta krav na malé ploše“ pod ní; schéma haly až při „přibývají“. Fotka u krmného žlabu = rezerva (`hala-krmny-zlab.png`). Práva k fotkám ověřit. | hotovo v18 |
| 2 | 2026-10-26 | **0:37 štítek pod fotkou krav ve slámě:** „Spousta krav na malé ploše“ → **„Spousta krav pod jednou střechou“** (KPZ: krávy se v hale pohnou, „je to kumulovaně moc krav“ – „relativně“ by znělo jako vytáčka; pro hygienu je podstatné nahromadění, ne plocha; sedí k obří hale). Hlas beze změny („spousta krav na malé ploše“ = hustota). | hotovo v18 |
| 3 | 2026-10-26 | **0:41 schéma haly (kreslené krávy shora)** – KPZ: na fotkách krávy nejsou jedna na druhé, ve schématu ~o 30 % víc místa. Návrh: `herdRows()` – 22 krav v posunutých řadách 6/5/6/5 místo mřížky 4×7 = 28 (~+27 % místa na krávu). Schéma zalehnutí (`#z-herd`, „Hodně zvířat, málo prostoru“) zatím beze změny. | 1. návrh 22 krav → KPZ „ještě o trošku víc místa“ → 20 krav → KPZ „ještě 10 % místa navíc“ → 18 krav → KPZ „dej tam 14 krav“ → **14 krav** (řady 4/3/4/3, kratší posunuté do mezer; 2× víc místa proti 28) – hotovo v18 |

## v19 (2026-10-26) – render `out/kpz-telata-reel-v19.mp4`, hlas `vo-v19.json` → `assets-v19/` (2:56,3), scénář `scenar-v19.md`

| # | datum | úprava | stav |
|---|---|---|---|
| 1 | 2026-10-26 | **1:52 mil3:** „dá v průměru“ → **„tvoří v průměru“** (hlas i titulek); nová nahrávka jen mil3, mil2/mil4 s pevným kontextem. | hotovo v19 |
| 2 | 2026-10-26 | **0:37 hyg2 hlas:** „spousta krav na malé ploše“ → **„spousta krav pod jednou střechou“** (sladit se štítkem); nová nahrávka jen hyg2, hyg1/hyg3 s pevným kontextem; kotvy ve scéně beze změny. | hotovo v19 |
| 3 | 2026-10-26 | **1:00 schéma zalehnutí:** **14 krav** (řady 4/3/4/3 jako v hale, `herdRows`) + **2 telata** v mezerách – jedno v kroužku (ohrožené, `#zh-calf`/`#zh-ring`), druhé vpravo nahoře (`#zh-calf2`, naskočí o 0,3 s později). Štítek „Hodně zvířat, málo prostoru“ beze změny. | hotovo v19 |

## Do v20 (sbírá se – nevyrábět, dokud KPZ neřekne)

| # | datum | úprava | stav |
|---|---|---|---|
