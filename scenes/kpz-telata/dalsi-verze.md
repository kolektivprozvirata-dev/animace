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

## Do v11 (sbírá se – nevyrábět, dokud KPZ neřekne)

| # | datum | úprava | stav |
|---|---|---|---|
| 1 | 2026-10-21 | **0:09–0:11 vytržení telete** – po odtržení krávě chybí kus těla (díra po teleti), působí divně. KPZ dodali dvojici srovnaných fotek holštýnky: s kojícím teletem (`foto-kpz/krava-tele-hol.jpg`) a stejnou krávu bez telete (`krava-sama-hol.jpg`). Postup: před vytržením `vystrizky/trh2-par.png` (kráva + tele), v okamžiku trhnutí výměna za `trh2-mama.png` (celá kráva) + `trh2-tele.png` odjíždí pryč (`scripts/tear_swap.py`, plátno 1003×662). Návrh k tomu: (a) úvodní fotka 0–4 s (`#h0-photo`) taky tahle holštýnka, ať je to stejná kráva; (b) v řádcích „→ Jatka“ (~2:30) použít `trh2-tele-samostatne` / `trh2-mama-samostatne`. Fotky ověřit práva před zveřejněním. | připraveno (výstřižky hotové), čeká na render |

