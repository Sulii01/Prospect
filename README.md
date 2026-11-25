# PROSPECT spol. s r.o. – nový web

https://sulii01.github.io/Prospect/

Moderní web společnosti **PROSPECT spol. s r.o.** (Ostrava, od roku 1991), projekčně-inženýrské organizace zaměřené na **řídicí systémy, automatizaci, MaR a elektro** pro technologické celky.

Web nahrazuje původní stránky [www.prospect.cz](https://www.prospect.cz/) (redakční systém Eliška). Veškerý obsah původního webu je převzatý: texty, reference, fotografie, certifikáty, kontakty i dotovaný projekt. Nový web ho podává v moderním světlém vzhledu ve firemních barvách, s animovaným operátorským HMI panelem.

Web je **dvojjazyčný**: česká verze leží v kořeni webu a kompletní **anglická verze** ve složce `en/`. Přepínač CZ / EN v hlavičce vede vždy na stejnou stránku v druhém jazyce.

---

## Rychlý start

```bash
python3 build.py          # vygeneruje české (z data/obsah.json) i anglické (z data/obsah.en.json) stránky
python3 -m http.server    # náhled na http://localhost:8000
```

Web je **čistě statický**. Stačí nahrát obsah složky na libovolný webhosting (Apache, Nginx, GitHub Pages, Netlify…). Nepotřebuje databázi, PHP ani Node.js. Generátor `build.py` potřebuje jen Python 3.8+ bez dalších knihoven.

Návod, co je kde a jak co upravit, je v souboru **[poznámky.md](poznámky.md)**.

---

## Co web obsahuje

### Stránky

| Soubor | Obsah |
|---|---|
| `index.html` | **Úvodní stránka.** Hero s animovaným HMI panelem ve stylu klasické SCADA vizualizace (čerpací stanice: vrt, čerpadla s motory „M“, filtr, vodojem, ventily, živé hodnoty tlaku, průtoku a hladiny, trend), čísla firmy (1991, 100+ projektů ročně, ~50 % realizujeme, 9 zemí), běžící pás zákazníků, O společnosti a filozofie firmy, 5 oborů jako velké foto-karty, sekce **Řídicí systémy** s přehledem technologií (PLC, SCADA, měniče, čidla, přenosy, projekce), životní cyklus 7 činností, mezinárodní působnost, certifikace ISM (ISO 9001, 14001, OHSAS 18001), dceřiná firma PROSPECT ENERGO a.s. |
| `vodni-hospodarstvi.html` | Obor: vodní zdroje a úpravny vod, čerpací stanice pitné a technologické vody, ČOV a kanalizační ČS. Texty, galerie a 4 referenční seznamy. |
| `teplo-a-klimatizace.html` | Obor: kotelny a výměníkové stanice, klimatizační zařízení. Reference. |
| `hute-a-strojirenstvi.html` | Obor: hutě a strojírenství. Text, galerie a 40 referencí. |
| `plynova-zarizeni.html` | Obor: distribuční plynárenská soustava, plynojemy a kompresorové stanice. Reference. |
| `srtp-a-elektro.html` | Obor: **řídicí systémy**, provozní rozvody silnoproudu, energetika, stavební elektroinstalace. Reference SŘTP, silnoproud a trafostanice. |
| `cinnosti.html` | 7 činností: Projektování, Vývoj (vč. FISHMONITOR), Dodávky, Montáže, Software, Servis, Obchodní činnost. Každá má text a galerii. |
| `reference.html` | **Všechny reference (261 akcí)** na jednom místě. Fulltextové vyhledávání (funguje i bez diakritiky), filtr podle oboru a zvýraznění nalezeného textu. Filtr jde zadat odkazem, např. `reference.html?obor=plynova-zarizeni`. |
| `dotovane-projekty.html` | Projekt EU / MPO „Speciální regulované rotační pohony průmyslových agregátů“ s PDF publicitou. |
| `404.html` | Chybová stránka „signal lost“ s rozcestníkem oborů. |
| `en/*.html` | **Anglická verze** všech 9 stránek se stejnými názvy souborů, např. `en/index.html` nebo `en/reference.html`. |

Na konci každé stránky je **kontaktní sekce**: telefon, e-mail, adresa, IČ/DIČ, popis cesty a mapa Google.

### Funkce a efekty
- Animovaný **HMI / SCADA panel** v úvodu, navržený ve stylu klasických operátorských obrazovek (WinCC): tyrkysové pozadí, šedé nádrže se štítky, bílé potrubí, zelené motory „M“ a ventily, bílé displeje hodnot a zelené tečkované signálové vedení z PLC. Animuje se proudění v potrubí, točící se oběžné kolo čerpadla, hladina ve vodojemu, hodnoty tlaku, průtoku a hladiny, hodiny a trend na canvasu. Data jsou jen ilustrační, ve stránce je to uvedené.
- **Dvojjazyčnost (CZ / EN):** přepínač v hlavičce i patičce vede na stejnou stránku v druhém jazyce. Stránky mají správně nastavené `lang`, `hreflang` a `canonical`.
- Lepicí hlavička s rozmazaným pozadím a **mega menu oborů**. Na mobilu se z menu stane výsuvný panel.
- Plynulé animace sekcí při scrollování a **počítadla čísel**.
- **Galerie s lightboxem**: šipky, klávesnice, Esc a swipe na mobilu.
- Na stránkách oborů je **postranní obsah se zvýrazněním aktuální sekce** (scrollspy) a navigace na předchozí a další obor.
- Respektuje nastavení „omezit pohyb“ (`prefers-reduced-motion`). Obsah je přístupný i bez JavaScriptu.
- Responzivní od 320 px po velké monitory, bez vodorovného posouvání.
- SEO: popisky stránek, canonical, Open Graph obrázek, `sitemap.xml`, `robots.txt`, odkaz na anglickou verzi (`hreflang`).
- **Přesměrování starých adres** (`.htaccess`). Např. `/ridici-systemy` vede na `srtp-a-elektro.html#ridici-systemy`, takže staré odkazy a výsledky ve vyhledávačích dál fungují.

### Vzhled
- **Světlý vzhled ve firemních barvách** z loga a původního webu: bílé a světle modrošedé (#EEF4F9) pozadí, firemní modrá **#0069AA** (tlačítka, odkazy, pruh s čísly, hlavičky podstránek), světle modrá **#00BDF2** z loga na zvýraznění a tmavě modrá patička (#0B2A44). V bílé hlavičce je původní barevné logo. Zelená **#22C55E** je stavová barva „RUN / ONLINE“.
- Písma (Google Fonts): **Space Grotesk** pro nadpisy, **Inter** pro text a **JetBrains Mono** pro technické popisky.
- Ikony oborů a činností jsou vlastní lineární SVG vložené přímo v HTML, takže se nenačítají žádné další soubory.

---

## Struktura projektu

```
├── index.html, *.html        ← VYGENEROVANÉ české stránky (neupravovat ručně)
├── en/                       ← VYGENEROVANÉ anglické stránky
├── 404.html, sitemap.xml, robots.txt, .htaccess   ← také generované
├── build.py                  ← generátor: šablony stránek, texty menu/tlačítek (CZ+EN), HMI panel, přesměrování
├── data/
│   ├── obsah.json            ← VEŠKERÝ OBSAH webu česky (texty, reference, kontakty)
│   └── obsah.en.json         ← totéž anglicky
├── assets/
│   ├── css/style.css         ← vzhled (barvy, písma, rozvržení)
│   ├── js/main.js            ← interaktivita (menu, HMI, galerie, filtr referencí)
│   ├── img/
│   │   ├── foto/             ← fotografie realizací (WebP, velké + náhled -sm)
│   │   ├── obory/            ← původní ikony oborů (záloha)
│   │   ├── logo-prospect.png / logo-prospect-white.png
│   │   ├── prospect-energo.webp, pas-realizaci.webp, certifikace.png
│   │   ├── og-image.jpg      ← náhled při sdílení na sociálních sítích
│   │   └── favicon.png
│   └── docs/                 ← PDF a skeny certifikátů, publicita dotace
├── README.md                 ← tento soubor
└── poznámky.md               ← návod: co je kde a jak to upravit
```

---

## Co se oproti původnímu webu změnilo

- **Vzhled:** moderní světlý design ve firemních barvách místo šablony z roku ~2015.
- **Struktura:** 45 původních podstránek se slilo do 9 přehledných stránek. Podkategorie oborů jsou sekce na stránce oboru a duplicitní stránky „Vybrané reference“ se sloučily do jedné stránky Reference s vyhledáváním.
- **Obsah:** všechny texty jsou zachované. Opravily se jen zjevné překlepy, např. „manamegentu“ → „managementu“, „WinnCC“ → „WinCC“, „Rossemound“ → „Rosemount“, „řídící“ → „řídicí“ nebo „Kompesorová“ → „Kompresorová“. Úvodní stránka má navíc úderné nadpisy, čísla a přehled technologií sestavené z původních textů.
- **Fotografie:** všech 80 fotografií je převedeno do WebP ve dvou velikostech pro rychlé načítání.
- **Výkon:** žádný jQuery ani CMS, jen jeden CSS a jeden JS soubor.
- **Vynechané:** odkaz „Administrace“, lišta cookies a Google Analytics. Bez analytiky web cookies nepotřebuje. Jak analytiku případně vrátit, popisuje `poznámky.md`.

---

## Kontakt na firmu

**PROSPECT spol. s r.o.**, Výstavní 2224/8, 709 00 Ostrava – Mariánské Hory
IČ 14616688 · DIČ CZ14616688 · tel. +420 596 616 500, +420 596 616 606 · prospect@prospect.cz
