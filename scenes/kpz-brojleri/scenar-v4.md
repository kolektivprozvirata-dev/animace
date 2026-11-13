# Scénář v4 – „Válí se vaše jídlo ve výkalech?“ (2:37,1)

Z v3 (`scenar-v3.md`). Změny KPZ (2026-11-13): „v3 už moc pomalý – mezi v2 a v3“ → stejné nahrávky jako v3 + `tempo` 1.05
(atempo, výška beze změny), pauzy přesně mezi v2 a v3 (−0,075 s), u čárek 0,19 s; „Jenže v hale je stále…“;
„S tím tenhle systém… nepočítá“ důrazněji, jako skutečný konec věty → take s předchozí otázkou a bez další věty, seed 5
(konec −4,5 půltónu místo 0,0; 11 verzí, 4 vyslovovaly „zaměřenej“ – kontrola přepisem); před koloběh nabídka–poptávka
znovu hlavní sdělení: „A většina z nich se předtím týdny válí ve vlastních výkalech.“ (seed 2 – nejpomalejší, nejširší melodie).
*hvězdičky* = slovo zvýrazněné v titulcích. Ověření tvrzení: `overeni-tvrzeni.md`.

# A · HLAS A TITULKY

## ÚVOD
Válí se vaše jídlo ve svých vlastních *výkalech?*
Než kuře skončí na talíři, žije ve většině případů v hale s *desítkami tisíc* dalších.
Celý jeho život trvá jen kolem *30 dní.*
A celou tu dobu žije na *stejné podestýlce*, která se nemění.

## FOTKY Z HAL
Možná znáte fotky z hal, které vám ukazují prodejci tzv. kuřecího: roztomilá malá žlutá kuřátka na *čisté podestýlce*, kde má každé kuřátko spoustu prostoru.
Tak ale hala vypadá *jen na začátku.*

## RŮST
Kuřata jsou vyšlechtěná na rychlý růst. Za pár týdnů z malého kuřátka vyroste kuře kolem *dvou kil.*
Jenže v hale je stále stejný počet kuřat. Jen víc a víc rostou. Ke konci má každé zhruba plochu *listu A4.*
A čím jsou větší, tím víc trusu vyprodukují. Za celý výkrm odhadem *dvě kila* – skoro tolik, kolik kuře samo váží.

## PODESTÝLKA SE NEMĚNÍ
Všechen ten trus padá do *stejné podestýlky.* Ta se po celou dobu výkrmu *nemění.*
Některé zdroje uvádějí, že se na ni přisype další. V praxi se to ale podle našich zkušeností nejspíše *neděje.*
Podestýlka se vyklidí až po tzv. vyskladnění těchto živých tvorů, když kuřata odvezou na jatka.
Měnit podestýlku zvířatům, která za pár týdnů stejně pojedou na jatka?
S tím tenhle systém zaměřený na zisk *nepočítá.*

## POSLEDNÍ TÝDNY
V posledních týdnech kuřata *většinu dne leží.* A leží v tom, co se za celý výkrm nahromadilo.
Přitom se kuřata přirozeně koupou v suchém prachu – tak si čistí peří.
Tady se *válí ve vlastních výkalech.*
To, co se na konci z haly vyveze, už se ani nepočítá jako podestýlka, ale jako *hnojivo.*

## DŮSLEDKY
Z trusu se uvolňuje *čpavek.* Dráždí kuřatům oči a dýchací cesty.
A kůže, která je dlouho ve vlhkém trusu, se zanítí. Kuřata mají bolestivé *popáleniny* na chodidlech, hleznech i na hrudi.

## POINTA (tmavá obrazovka)
Ty reklamní fotky a videa s kuřátky na čisté podestýlce nelžou.
Jen jsou z prvních dnů jejich pobytu v této obří hale.
Kdyby vám měli zemědělci ukázat, jak vypadá hala pár dní před odvozem na jatka, moc lichotivé by to nebylo.
Kdybyste měli stát v té hale a cítit puch z výkalů, možná by vás chuť na toto zneužívané zvíře přešla.

## ZÁVĚR
V Česku jich ročně skončí na jatkách přes *110 milionů.*
A většina z nich se předtím týdny *válí ve vlastních výkalech.*
Celý ten systém ale neběží sám od sebe. Běží, protože kuřecí maso *kupujeme.*
Vystoupit z něj ale můžeme. *Rostlinných alternativ* je spousta.
Kolektiv pro zvířata. Zdroje v popisku.

# B · ZMĚNY V GRAFICE PROTI v3

- Závěr: pod počítadlem 110 000 000 při „A většina z nich…“ fotka kuřete v podestýlce (stejná jako v úvodu – návrat k hookovi)
  a štítek „Týdny ve vlastních výkalech“; obojí zmizí s číslem při „neběží sám od sebe“. Zdroj u čísla doplněn o VÚŽV.

# B (v3) · ZMĚNY V GRAFICE PROTI v2

- Řez podestýlkou: při „přisype další“ spadne navrch nová vrstva se štítkem „Nová vrstva navrch?“; při „V praxi…“ vrstva
  zase odletí, štítek se přeškrtne a objeví se „V praxi spíš ne“; štítek „Stará zůstává pod ní“ vypuštěn;
  „Vyklízí se až po odvozu na jatka“ při „Podestýlka se vyklidí“.
- Titulky (`tts.py`): kousek nikdy nepřeteče do další věty („…uvolňuje *čpavek.*“ | „Dráždí kuřatům oči“) a nekončí
  jednopísmennou předložkou/spojkou („…případů“ | „v hale s…“).
- Ostatní grafika beze změny – časy se řídí hlasem, takže se celé video roztáhlo s ním.

# B (v2) · ZMĚNY V GRAFICE PROTI v1

- Úvod: číslo „≈ 30 dní“, pod ním „celý život kuřete · ČR: 30–35 dní“.
- Fotky z hal: štítek „Z reklam prodejců“ na polaroidu, „Čistá podestýlka“ → „Spousta prostoru“.
- Pointa (tmavá): polaroid „DEN 1“ + prázdná fotka „?“ „PÁR DNÍ PŘED JATKY“; texty „Ty reklamní fotky a videa / s kuřátky na čisté
  podestýlce / nelžou.“ a „Jen jsou z / prvních dnů.“; při „Kdyby vám měli zemědělci ukázat…“ se prázdná fotka zvětší doprostřed,
  při „puch z výkalů“ z ní stoupá zápach + štítek „Puch z výkalů“ (titulky zapnuté).
- Záběr „Čistší hala? / Kuře není jídlo. / Je to někdo.“ vypuštěn (věta není v hlase).
- Závěr: počítadlo 110 000 000 „Kuřat poražených ročně · Česko“ až do „neběží sám od sebe“, pak kruh nabídka – poptávka.
