# Ekologická stopa výroby reelu o telatech (odhad, 2026-11-01)

Odhad pro případné útoky v komentářích („AI video škodí planetě víc než kráva“). Přesná čísla nikdo nezveřejňuje
(Anthropic, Midjourney ani ElevenLabs) – proto rozpětí a střední hodnota.

## Co je změřené (tato session, v12 → v32)
- Claude: 621 volání modelu; 304 mil. vstupních tokenů, z toho 297 mil. načteno z mezipaměti (nezpracovává se znovu),
  7,1 mil. nově zpracovaných, 0,54 mil. výstupních. Dlouhý chat = každá odpověď znovu čte celou historii.
- Render a úpravy v kontejneru: 20 renderů = 2,1 h na 4 vCPU (+ náhledy, výřezy, hlas).
- ElevenLabs: 5 484 znaků.
- Starší sessions (rešerše, v1–v12) změřené nemám → odhad: podobný rozsah jako tato.

## Odhad celého projektu
| část | elektřina | CO₂e | voda |
|---|---|---|---|
| Claude (AI text) | ~10 kWh (3–25) | ~4 kg (1–10) | ~10–50 l |
| Midjourney (~100–300 obrázků × ~3 Wh) | ~0,5 kWh | ~0,2 kg | ~1–3 l |
| Rendery, náhledy, výřezy (kontejner) | ~0,5 kWh | ~0,2 kg | ~1–3 l |
| ElevenLabs (hlas) | < 0,1 kWh | < 0,05 kg | < 0,5 l |
| **Celkem** | **~11 kWh (4–26)** | **~4,5 kg (1,5–11)** | **~10–55 l (střed ~25 l)** |

Předpoklady: 0,1–0,4 Wh na 1 000 nově zpracovaných tokenů a 0,6–6 Wh na 1 000 výstupních tokenů (podle Epoch AI 2025:
~0,3 Wh běžný dotaz, ~2,5 Wh při 10 000 tokenech vstupu); obrázek ~2,9 Wh (Luccioni et al. 2023, průměr generování obrázků);
elektřina ~0,4 kg CO₂e/kWh; voda ~1–5 l/kWh (chlazení datacenter + výroba elektřiny; Google uvádí 0,26 ml na 0,24 Wh = ~1 l/kWh
jen na chlazení). Nepočítá se výroba počítačů ani čas lidí u obrazovek.

## Srovnání (Poore & Nemecek 2018, Science; data Our World in Data – ověřeno jen přes vyhledávání)
| | CO₂e | sladká voda (odběr) |
|---|---|---|
| **celé video** | **~4,5 kg** | **~25 l** |
| 1 kg hovězího z dojeného stáda | 33 kg | 2 714 l |
| 1 kg hovězího z masného stáda | 99 kg | 1 451 l |
| 1 l kravského mléka | 3,2 kg | 628 l |

→ 1 kg hovězího ≈ **7× až 22×** víc CO₂ a **60× až 100×** víc vody než celé video.
→ Celé video ≈ CO₂ z **1,5 litru mléka**, ale vody jako **4 deci mléka**.
→ ~4,5 kg CO₂ ≈ **~30 km autem** (benzín).

## Připravená odpověď do komentářů
„Spočítali jsme to: výroba celého videa vč. AI odpovídá zhruba 4–5 kg CO₂ a pár desítkám litrů vody – asi jako 30 km autem.
Jedno kilo hovězího je 33–99 kg CO₂ a 1 500–2 700 litrů vody, litr mléka 3 kg CO₂ a 600 litrů vody.
Pokud video přesvědčí jediného člověka vynechat kilo hovězího, je ‚zaplacené‘ několikrát.“

## Tip
Nový chat pro každé nové video (ne pokračovat v tomto) – kratší historie = výrazně méně zpracovaných tokenů.
