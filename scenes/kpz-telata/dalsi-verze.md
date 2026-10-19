# Úpravy do další verze (zatím nevyrábět – čeká na pokyn KPZ)

Seznam změn, které se mají promítnout při příštím renderu reelu o telatech.

| # | datum | úprava | stav |
|---|---|---|---|
| 1 | 2026-10-19 | Titulky: „přes **9 500** litrů“ – devítka nesmí být oddělená od 500, číslo musí být v jednom titulku. Nevadí, když se 9 objeví o ~0,5 s později. | nástroj opraven (`tts.py` drží čísla s mezerou pohromadě); projeví se po přegenerování časování hlasu |
| 2 | 2026-10-19 | Fotky: nahradit provizorní fotky fotkami KPZ (zvířata vždy celá, známky rozmazat) – viz `assets/foto-provizorni/README.md`. | čeká na fotky |

Při další verzi: přegenerovat hlas a časování (`tts.py vo-v5.json --out-dir assets-v5`),
zkontrolovat délku pod 3:00 a kotvy slov ve scéně, pak jeden render.
