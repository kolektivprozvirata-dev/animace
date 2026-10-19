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
