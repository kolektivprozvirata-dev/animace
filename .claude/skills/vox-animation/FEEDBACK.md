# Feedback & vývoj skillu

**Verze skillu: 0.2.0**

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

## ✅ Osvědčené (nechat tak)

_Zatím nic – čeká na feedback k reelu kpz-telata v1._

## Otevřené otázky na uživatele

- Délka reelu: v1 má ~107 s (všechny 3 argumenty). Vyhovuje, nebo chystat zkrácenou ≤ 90 s verzi / sérii?
- Hlas Jirka (Piper) – je kvalita dostačující, nebo hledat jiný hlas / nahrávat?
- Hudební podkres: žádný (výchozí), nebo jemný rytmický?

## Log

| datum | verze | projekt | feedback | změna ve skillu |
|-------|-------|---------|----------|-----------------|
| 2026-10-14 | 0.1.0 | — | — | Založení skillu z rešerše (viz references/sources.md), runtime, renderer, demo. |
| 2026-10-14 | 0.2.0 | kpz-telata | Chce český hlas a titulky; reel 9:16; logo KPZ; úhel „bizár systému“; „krutý“ používat; zalehnutí = důsledek těsna (postoj KPZ); „často hned po porodu“; nastudovat veganskou etiku. | `scripts/tts.py` (Piper → vo.wav + vo-timing.js + vo.srt), `VOX.captions/vo/wordT`, `runtime/vox-icons.js` (kráva, tele, ikony), svislý kontaktní arch, `brand/kpz/` (loga, etika, slovník). |
