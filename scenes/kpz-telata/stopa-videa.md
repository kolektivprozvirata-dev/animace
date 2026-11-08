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

## Srovnání s člověkem (střihač/animátor, odhad)
| fáze | práce |
|---|---|
| rešerše a ověření tvrzení | 3–5 dní |
| scénář s klientem | 2–3 dny |
| styl, grafika, výřezy a retuše fotek | 3–5 dní |
| animace ~3 min (Vox styl, ~30 záběrů) | 10–15 dní |
| hlas (studio), střih, titulky | 2–3 dny |
| ~30 kol úprav (à 2–3 h, u hlasu nové nahrávání) | 8–10 dní |
| **celkem** | **~30–40 pracovních dní (6–8 týdnů)** |

Spotřeba: pracovní počítač + 2 monitory ~0,2 kW × 8 h × 35 dní ≈ **55 kWh ≈ 25 kg CO₂e** (česká síť ~0,45 kg/kWh).
S podílem kanceláře (topení, světlo) **+30–60 kg**, s dojížděním autem 20 km denně **+~100 kg**.
→ Člověk: **~25 kg** (jen počítač) až **~150–200 kg** CO₂e (s kanceláří a dojížděním) × video s AI **~4,5 kg**.

## Kritika odhadu očima odpůrce AI (2026-11-01)
1. **Odhaduje AI sama sebe** (Claude od Anthropicu) – střet zájmů; Anthropic data nezveřejňuje, nic se nedá ověřit.
2. **Přepočet energie je z cizích, menších modelů** (Epoch AI = odhad pro GPT-4o; Google = medián krátkého dotazu, sám si
   to měřil, nikdo neověřil). Claude Opus je větší model. **297 mil. tokenů z mezipaměti jsem v odhadu prakticky nepočítal** –
   nejsou zadarmo (dlouhý kontext zatěžuje každou odpověď). Bez úspory z mezipaměti by jen tato session vyšla až ~120 kWh;
   realistický pesimistický odhad celého projektu ~50–100 kWh → **20–45 kg CO₂e**, ne 4,5.
3. **Chybí výroba čipů a datacenter, trénink modelu, sítě** – u AI tvoří desítky % celkové stopy.
4. **Voda**: odhad pro AI míchá spotřebu a odběr; nezávislé studie (Li et al. 2023) dávají řádově víc vody na dotaz než Google.
   A hovězí v ČR je hlavně z dojených stád krmených bez závlah → **modrá voda je u nás mnohem nižší** než světové
   2 714 l/kg. „60–100× víc vody“ pro české hovězí neplatí.
5. **Srovnání s člověkem je zaujaté**: u člověka počítám dojíždění a topení kanceláře, u AI ne práci KPZ (týdny kontroly,
   32 stažených renderů, telefon, počítač). 30 kol úprav vzniklo, protože s AI je úprava snadná – člověk by jich dělal 3–5.
   Animátor s notebookem (~40 W) by spotřeboval ~10–15 kWh – **tedy zhruba stejně jako AI**, ne 5–40× víc.
6. **Srovnání s hovězím je odvádění pozornosti** – nikdo netvrdí, že video škodí víc než kilo masa; „zaplatí se, když
   přesvědčí jednoho člověka“ je nedoložená hypotéza.
7. **Falešná přesnost** – „4,5 kg“ s desetinným místem budí dojem měření.

**Co obstojí i při pesimistickém odhadu:** výroba videa (~5–45 kg CO₂e) je pod 1 kg hovězího z masného stáda (99 kg)
a řádově srovnatelná s 1 kg hovězího z dojeného stáda (33 kg). **Neobstojí:** „AI je 5–40× šetrnější než člověk“ – nepublikovat.

## Aktualizace 2026-11-08 (v34) a srovnání s hamburgerem
Do v34 přibylo práce: 712 volání modelu, 9,5 mil. nově zpracovaných a 367 mil. načtených tokenů, 0,61 mil. výstupních,
22 renderů (2,3 h) → odhad celého projektu **~5,5 kg CO₂e** (rozpětí ~2–13), pesimisticky **~25–55 kg**; voda ~30 l (10–70).

Hamburger (Poore & Nemecek 2018: hovězí z mléčného chovu 33 kg CO₂e/kg, z masného 99 kg/kg; + houska, sýr, zelenina ~0,5 kg):
| | CO₂e | voda (odběr) |
|---|---|---|
| burger v restauraci (150 g hovězího) | ~5,5 kg (mléčný chov) – ~15 kg (masný chov) | ~250–450 l |
| hamburger z fastfoodu (~45 g hovězího) | ~2 kg – ~5 kg | ~70–130 l |
| **celé video** | **~5,5 kg** (pesimisticky 25–55) | **~30 l** |
→ Video ≈ **1 burger v restauraci** (z hovězího z mléčného chovu, běžné v ČR) nebo **2–3 hamburgery z fastfoodu**;
pesimisticky 4–10 burgerů. Vody video spotřebovalo zhruba desetinu jednoho burgeru.

## Připravená odpověď do komentářů
„Přesná data o spotřebě AI firmy nezveřejňují, takže jde jen o odhad: výroba celého videa vychází řádově na jednotky až
nízké desítky kg CO₂ – zhruba jako 1 kg hovězího nebo cesta autem z Prahy do Brna. Jedno video za mnoho tisíc zhlédnutí.
Stopa toho, o čem video mluví, je v milionech litrů mléka a tun masa ročně.“

## Tip
Nový chat pro každé nové video (ne pokračovat v tomto) – kratší historie = výrazně méně zpracovaných tokenů.

## Odpověď na Instagram pro vegany (návrh KPZ + úpravy, 2026-11-08, 1843 znaků)

Dobrý den, takový komentář jsme čekali a je dobře, že přišel. Ekologický dopad AI je legitimní téma a nechceme ho zametat pod koberec. Takže jak to bylo:

Obsah je náš. Témata, argumenty, postoje i finální znění textu jsme připravili a mnohokrát přepisovali my. Zdroje jsme četli a ověřovali, protože chceme, aby každé tvrzení obstálo. Vizuální styl vychází z naší vlastní grafiky. AI nám pomohla hlavně s tím, na co nemáme lidi: s animací a hlasem. Polovinu práce tak odvedl člověk.

Nejde o brainrot ani o AI na zábavu. Je to video, které může změnit pohled spousty lidí na mléko a na to, co se děje telatům. Čím víc lidí ho uvidí, tím víc to dává smysl.

Nechali jsme AI spočítat i stopu tohoto videa. Přesná data firmy nezveřejňují, takže jde jen o odhad: výroba celého videa i se všemi verzemi a úpravami vyšla zhruba na tolik CO₂ jako jeden burger v restauraci a vody spotřebovala asi desetinu toho, co jeden burger. Ideální to není, katastrofa ale taky ne. Další videa budou mít podle tohoto odhadu stopu 3–5× menší, protože základ grafiky i postupy už máme hotové.

Klidně bychom animaci zadali člověku. Jsme ale dobrovolnická organizace o pár lidech a na profesionální animaci nemáme kapacitu, natož peníze. Bez těchto nástrojů by video nevzniklo vůbec.

Uvědomujeme si, že spousta našich sledujících řeší environmentální dopady různých odvětví, od živočišné výroby přes fast fashion až po dopravu. Řešíme je i my. Úplně bez dopadu ale fungovat nejde. Když stánkujeme ve městě, vozíme věci autem. Tiskneme papírové letáky pro starší lidi, kteří informace na internetu nenajdou. Snažíme se škodit co nejméně a vybírat, kde má naše stopa smysl.

Rozumné použití AI na video, které může pomoct zvířatům, proto nevnímáme jako prohřešek proti tomu, za čím stojíme. A největší dopad, a to zvířat i planety, má pořád to, co máme na talíři. 🌱
