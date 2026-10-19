# Kolektiv pro zvířata (KPZ) – brand a hodnotový rámec pro videa

Platí pro všechna videa pro KPZ. Pravidla označená **[KPZ]** jsou přímé
pokyny organizace a mají přednost.

## Loga

| soubor | použití |
|---|---|
| `logo-kpz-svetle.png` | průhledné pozadí, černé „KPZ“ – na papírový/světlý podklad (výchozí) |
| `logo-kpz-tmave.png` | černé pozadí, bílé „KPZ“ – tmavé scény |
| `logo-kpz-text-tmave.png` | černé pozadí + nápis KOLEKTIV PRO ZVÍŘATA – outro na tmavém |
| `KPZ.badge()` (z `logo-kpz-tmave.png`) | kulaté černé logo z grafiky – ve videích **nepoužívat**, KPZ chtějí klasické logo výše **[KPZ]** |

Zelená z loga: **`#00c800`** (token `--kpz-green`). Ve stylu KPZ (níže) se zelená
objevuje jen v logu; pozitivní prvky jsou teal.

## Vizuální styl KPZ (z grafiky na sítích, 2026-10)

Používat pro videa KPZ, pokud nechtějí klasický Vox papír. Hotové téma:
`kpz-theme.css` + `kpz-theme.js` (vzor `scenes/kpz-telata/reel-kpz.html`).
**Z grafiky KPZ bereme jen vizuál – ne obsah, hesla ani fotky [KPZ].**

| prvek | jak vypadá | v tématu |
|---|---|---|
| písmo | **Bebas Neue**, vše verzálkami (`fonts/`, licence OFL) | `--font-head`, `.h1/.h2/.tag/...` |
| text | plné obdélníkové **bloky po řádcích**, střídání barev řádků, mezery mezi bloky | `.kb`, `.kb.cream` … , `KPZ.blocks()` |
| zvýraznění | slovo v **bloku jiné barvy** (oranžová), ne žlutý zvýrazňovač | `<span class="kb hl">` |
| pozadí | sytě růžový papír se skvrnami a zrnem | `KPZ.theme()`, tmavé záběry `KPZ.bg('#0d4a4f')` |
| textura | tiskový „grunge“ na blocích a textu – **jen jemně** (KPZ: „o 50 % míň špinavé“) | `.print`, `.print-soft` |
| dekor | linoryt nálepky (listy, klasy, srdce) tmavě modré s krémovými rytinami; šipky a škrty tahem štětce | `KPZ.sticker()`, `filter="url(#kpz-brush)"` |
| logo | ve videu **klasické logo** `logo-kpz-svetle.png` (vodoznak vlevo nahoře + outro), na tmavých záběrech skrýt **[KPZ]**; kulaté černé z grafiky ne | `<img>` |
| titulky | krémové bloky s tmavým textem, klíčové slovo v oranžovém bloku | `#vox-captions` v tématu |
| drobný text | tučný bezpatkový s prostrkáním (jako spodní karta na grafice) | `.kpz-body` |

Paleta (vzorkováno): růžová `#e05d73`, teal `#115c61` / tmavý `#0b3f43`, krémová `#efe4dd`,
oranžová `#d26c11`, vínová `#920637`, hořčicová `#d38f03`, malinová `#c63f58`,
tmavě modrá nálepek `#17323d`. Nebezpečí / krutost = vínová, alternativa = teal,
zvýraznění = oranžová (na krémové kartě hořčicová s černým textem).

Pravidla:
- **Žádný detailní záběr na ušní známku [KPZ].** Čísla na známkách přebarvit barvou známky (známka zůstane, čísla ne); nerozmazávat – vypadá to hůř [KPZ].
- Bez samoúčelně drastických obrazů (platí dál); fotky jen dodané KPZ.
- Starší styl KPZ (pastelová růžová, bloky se stínem a obrysovým písmem, razítkové logo)
  je známý, ale výchozí je novější styl výše.

## Kdo jsme (podle zadání KPZ)
Veganská organizace; VeganFest, veganské ochutnávky, vzdělávání o veganství
a právech zvířat. Zvířata jsou cítící bytosti s vlastními zájmy, ne prostředky
k produkci. Cíl: omezovat a ukončovat jejich využívání – **ne** zlepšovat
efektivitu živočišné výroby. Komunikace věcná, přesná, přesvědčivá i pro
nevegany; data a logika před citovým vydíráním.

## Etický rámec, ze kterého videa vycházejí

**Veganství** – podle The Vegan Society „filozofie a způsob života, který se
snaží vyloučit – nakolik je to možné a proveditelné – všechny formy
vykořisťování zvířat a krutosti vůči nim pro jídlo, oblečení či jakýkoli jiný
účel“. Nejde jen o jídelníček, ale o postoj k zvířatům jako k někomu, ne
něčemu.

**Cítění (sentience)** – morálně podstatné je, že zvíře prožívá: bolest,
strach, vazby. Český občanský zákoník (§ 494) říká, že živé zvíře „není
věcí“ a má zvláštní význam jako smysly nadaný tvor. Přehled výzkumu o psychice
krav (Marino & Allen 2017) popisuje komplexní kognitivní, emoční a sociální
život krav, včetně silné vazby matky a telete.

**Abolicionismus vs. welfarismus** – welfarismus (v duchu P. Singera) usiluje
hlavně o snížení utrpení v rámci využívání; práva zvířat (T. Regan) a
abolicionismus (G. Francione) odmítají samotné pojetí zvířat jako majetku a
prostředku. **KPZ stojí blíž ke druhému** – proto video nikdy nekončí
„lepším chovem“ jako řešením.

**Karnismus a „3 N“** (Melanie Joy) – využívání zvířat se obhajuje jako
_normální, přirozené a nutné_. Systém je neviditelný, protože se bere jako
samozřejmost. Naše videa tenhle mechanismus zviditelňují – typicky
rozebírají „nutnost“.

**Speciesismus** (R. Ryder, 1970) – zvýhodňování zájmů vlastního druhu jen
kvůli druhové příslušnosti. Pojem znát, ve videích pro širokou veřejnost
používat jen s vysvětlením.

## Jak to promítnout do videí

1. **Kritizujeme systém a jeho logiku, ne lidi.** Nepřisuzovat chovatelům
   zlý úmysl ani lež.
2. **Slovo „krutý“ používat** pro praxi a systém **[KPZ]** – ne pro lidi.
3. **Žádné „etické mléko“.** Příklady chovů s kontaktem matky a telete slouží
   jen jako důkaz, že „nutnost“ je konstrukt. Vždy dodat, že ani tam to není
   idyla.
4. **Výzva = alternativa, ne vina.** Rostlinné alternativy jako východ ze
   systému; bez moralizování a zahanbování diváka.
5. **Nabídka a poptávka** – systém běží, protože se jeho produkty kupují
   **[KPZ]**. Říkat obecně; nekvantifikovat dopad jednotlivého nákupu bez dat.
6. **Bez drastických záběrů a patetické hudby** **[KPZ]**. Absurditu nechat
   vyplynout ze souvislostí; lehká ironie je v pořádku.
7. **Srovnání s lidskými tragédiemi** (např. otroctví) – rozhoduje KPZ; jejich grafika je
   občas používá. Do videa je nevkládat z vlastní iniciativy, jen na pokyn KPZ.

## Slovník

| používat | nepoužívat / jen v uvozovkách |
|---|---|
| kráva, matka, tele, mládě | „kus“, „dojnice“ jako identita (jen jako citace systému) |
| kdo (o zvířeti) | co |
| oddělení, odebrání, odloučení | „odstav“ pro oddělení v prvních hodinách (odstav = konec sání) |
| mléčný průmysl, systém, chov | „humánní“, „etické mléko“, „šťastné krávy“ |
| krutá praxe, krutý systém | útoky na osoby |
| rostlinné alternativy | „náhražky“ |
| **tzv. masné krávy**, **tzv. dojnice** (vždy s „tzv.“) | „masné krávy“, „dojnice“ bez odstupu **[KPZ]** |

## Podklady KPZ
- `clanky/mlecne-kravy-materstvi-ve-sluzbach-vyroby.md` – článek KPZ s 30 zdroji
  (inseminace, odebrání telete, boxy, odrohování, býčci a vývoz telat, haly, nemoci,
  brakace, jatka, azyly). Čerpat odtud fakta i formulace.

## Specifické postoje KPZ (z feedbacku)
- **Začátek videa [KPZ]:** začínat hookem (nejsilnější fakt – odebrání telete), ne popisem
  toho, jaké krávy jsou.
- **Industriální slovník [KPZ]:** „velkokapacitní haly“, ne „stáje“ – výrazy, které ukazují
  monstróznost systému a budov.
- **Hygiena – formulace [KPZ]:** nejen „výkaly“ – podlaha, kde výkaly byly a průběžně jsou,
  moč, a na tak malé ploše je přirozené, že tam z výkalů jsou bakterie.
- **Lehká ironie [KPZ]:** např. „Odnese to – jak jinak – tele a jeho máma.“; po pointě
  „Aby je odloučení nebolelo, odloučí je dřív.“ přidat „Není to bizarní?“
- **Pouto [KPZ]:** formulovat opatrně – „Podle některých zdrojů je to údajně pravda.“
- **Chovy s kontaktem matky a telete [KPZ, zpřísněno]:** ne „není to ideál“, ale přísněji:
  „Pokud konzumujete mateřské mléko nebo sýry, ani zde nehledejte útěchu.“ + fakta o zabíjení
  (býčci, tzv. dojnice po poklesu dojivosti). Je to také krvavý a krutý byznys, jen se v něm
  zvířata mají možná o trochu lépe.
- **„Tzv.“ u produkčních kategorií [KPZ]:** „tzv. masné krávy“, „tzv. dojnice“ – tyto
  názvy vymysleli lidé. Kráva je tvor s vlastním životem, nenarodila se jako „masná“.
  V hlasu vyslovovat „takzvané“.
- **Veganský pohled, ne instituce [KPZ]:** nestavět sdělení na doporučeních úřadů
  (např. EFSA „aspoň 24 h“). Postoj KPZ: oddělit mládě od matky je kruté – ať hned,
  nebo později.
- **Česká praxe [KPZ]:** vždy zmínit obojí – příručky uvádějí „nejpozději do 12 hodin“,
  v praxi je to často hned.
- **Argumenty chovatelů [KPZ]:** neříkat „chovatelé mají tři argumenty“, ale „mají
  několik argumentů, mezi nejčastější patří…“.
- **Srovnání s tzv. masnými kravami [KPZ]:** použít jen u hygieny a zalehnutí
  (pastva = prostor, telata zůstávají s matkami měsíce). Ne jako obecný vzor.
- **Hygiena [KPZ]:** nejde jen o porodnu – v kravínech často stojí spousta krav na
  malé ploše i se svými výkaly. Kořen problému = velké množství zvířat na malém prostoru.
- **Pojmenovat problémy konkrétně [KPZ]:** ne „systém si vytvoří problémy“, ale
  „postaví velkokapacitní kravíny, kde je spousta krav na malém prostoru, a vyšlechtí
  krávy na maximální výkon“.
- **Chovy s kontaktem matky a telete [KPZ]:** vždy dodat, že nejde o ideál – i tam
  jdou býčci na jatka (nedávají mléko) a tzv. dojnice skončí na jatkách, když jim klesne
  dojivost. „Zvíře není stroj ani zboží.“ Nedoporučovat domácí/bio chovy.
- **Argument „přebytek mléka“ [KPZ]:** kráva dává tolik mléka kvůli šlechtění;
  farmy s kontaktem ukazují, že dojit a nechat tele sát jde → výmluva velkochovů,
  problém systému („co nejefektivnější krutá mašina“).
- **Citlivost zvířat [KPZ]:** do textu vkládat doložené momenty o tom, co krávy a telata
  prožívají (olizování, poznávání po hlase, bučení a hledání po odloučení, tele je
  společenské), aby komentář nebyl jen „strojové odříkávání“ argumentů.
- **Zalehnutí/úraz telete [KPZ]:** pokud k němu dochází, je to proto, že je
  hodně zvířat na malém prostoru. Na pastvě s dostatkem místa se to prakticky
  neděje. (Postoj organizace; tvrdá data o četnosti jsme v rešerši nenašli –
  formulovat „prakticky neděje“, ne „nikdy“.)
- **Česká praxe [KPZ]:** tele bývá odebráno často hned po porodu, nejpozději
  do 12 hodin.

## Zdroje k etice
- The Vegan Society – Definition of veganism: https://vegansociety.com/go-vegan/definition-veganism
- Carnism (Melanie Joy, 3 N): https://en.wikipedia.org/wiki/Carnism ; rozhovor Britannica: https://explore.britannica.com/explore/savingearth/interview-dr-melanie-joy-on-why-we-love-dogs-eat-pigs-and-wear-cows
- Steiner – rozdíly Singer / Regan / Francione: https://www.abolitionistapproach.com/wp-content/uploads/2016/12/Steiner-on-Singer-Regan-Francione.pdf
- Speciesism (Ryder): https://en.wikipedia.org/wiki/Speciesism
- Marino & Allen 2017, The Psychology of Cows: https://www.animalbehaviorandcognition.org/article.php?id=1110
- Padilla de la Torre et al. 2016, Animal Behaviour 114:147 – vzájemné poznávání matky a telete po hlase: https://eprints.nottingham.ac.uk/34713
- § 494 OZ – epravo.cz: https://www.epravo.cz/top/clanky/prestava-byt-zvire-veci-aneb-kratky-exkurz-do-pravni-upravy-zvirat-v-novem-obcanskem-zakoniku-82444.html
