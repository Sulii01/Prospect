# Poznámky – co je kde a jak to upravit

Praktický návod pro správu webu PROSPECT. Celkový popis webu je v [README.md](README.md).

---

## 0. Zlaté pravidlo

> **Texty se upravují v `data/obsah.json` (česky) a `data/obsah.en.json` (anglicky), ne v HTML souborech.**
> Po každé úpravě spusťte v kořeni projektu:
>
> ```bash
> python3 build.py
> ```
>
> Skript přepíše všechny `*.html` stránky (české v kořeni, anglické ve složce `en/`), `sitemap.xml`, `robots.txt` a `.htaccess`. Ruční změny v HTML by se tím ztratily.

| Co chci změnit | Kde |
|---|---|
| Texty, reference, kontakty, čísla, seznam zákazníků | `data/obsah.json` (CZ) a `data/obsah.en.json` (EN) |
| Texty menu, tlačítek a nadpisů sekcí (CZ i EN) | slovník `T` v `build.py` |
| Vzhled a popisky HMI panelu v úvodu | funkce `hmi_panel()` a `T[…]["hmi"]` v `build.py` |
| Barvy, písma, mezery, velikosti, rozvržení | `assets/css/style.css` |
| Chování (menu, animace, HMI panel, filtr, galerie) | `assets/js/main.js` |
| Rozložení stránek, pořadí sekcí, menu, ikony, přesměrování | `build.py` |
| Fotografie | `assets/img/foto/` + odkaz v `data/obsah.json` |
| PDF a certifikáty | `assets/docs/` |

Náhled v prohlížeči: `python3 -m http.server`, pak otevřete http://localhost:8000. Stačí i dvojklik na `index.html`, jen mapa Google se tak nemusí načíst.

**Pozor na JSON:** texty musí být v uvozovkách `"…"`, položky se oddělují čárkou a za poslední položkou v seznamu čárka **není**. Uvozovku uvnitř textu pište jako `\"`, nebo raději použijte české „uvozovky“. Pokud `build.py` skončí chybou `JSONDecodeError`, ukáže číslo řádku, kde je chyba. Soubor můžete zkontrolovat i na https://jsonlint.com.

---

## 1. `data/obsah.json` – mapa obsahu

```
{
  "firma":          kontaktní údaje, adresa, IČ/DIČ, mapa, odkaz na EN web
  "seo":            titulek a popis úvodní stránky pro Google
  "uvod":           vše pro úvodní stránku (hero, čísla, o nás, země, certifikáty, zákazníci…)
  "ridici_systemy": sekce „Technologie, se kterými pracujeme“ na úvodu
  "obory":          5 oborů – každý = jedna stránka (texty, sekce, fotky, reference)
  "cinnosti_uvod":  úvodní věta stránky Činnosti
  "cinnosti":       7 činností (Projektování … Obchodní činnost)
  "reference_uvod": úvodní věta stránky Reference
  "dalsi_reference":„Další reference“ (neobvyklé zakázky)
  "dotace":         dotované projekty
}
```

### 1.1 Kontakty – `firma`
```json
"telefony": ["+420 596 616 500", "+420 596 616 606"],
"email": "prospect@prospect.cz",
```
Změna se projeví v hlavičce (tlačítko s telefonem), v kontaktní sekci i v patičce na všech stránkách.
- `mapa_embed` je adresa mapy pro vložení. Novou získáte v Google Maps přes Sdílet → Vložit mapu → zkopírujte jen hodnotu `src="…"`.
- `mapa_odkaz` se otevře po kliknutí na adresu.
- `web` je hlavní adresa webu, používá se pro sitemap a canonical. Při přesunu na jinou doménu ji změňte.

### 1.2 Úvodní stránka – `uvod`
| Klíč | Kde se zobrazí |
|---|---|
| `hero_stitek` | malý zelený štítek nad hlavním nadpisem („Ostrava · od roku 1991“) |
| `hero_nadpis` | hlavní nadpis. Slova „Řídicí systémy“ se automaticky zvýrazní barevným přechodem. |
| `hero_text` | odstavec pod nadpisem |
| `cisla` | pruh se 4 čísly. `hodnota` je číslo, které se při zobrazení „napočítá“, `pripona` např. `"+"` nebo `" %"`. |
| `o_nas` | 3 odstavce: první dva jsou text sekce O společnosti, třetí je citát filozofie firmy v rámečku |
| `obory_text`, `dodavky_text`, `zahranici_text`, `prostredky_text`, `ism_text`, `energo_text` | texty příslušných sekcí |
| `zeme` | dlaždice zemí. Číslo 9 v nadpisu „devíti zemí“ je v `build.py`. |
| `certifikaty` | karty certifikátů (`soubor` = cesta k PDF nebo JPG v `assets/docs/`) |
| `klienti` | jména v běžícím pásu „Pracovali jsme pro“. Stačí přidat nebo smazat řádek. |

Nadpisy sekcí úvodní stránky („Pět oborů. Jedna řídicí logika.“, „Srdce každé technologie…“ apod.) jsou ve funkci `build_index()` v `build.py`.

### 1.3 Obory – `obory`
Každý obor je jeden objekt a vznikne z něj stránka `<id>.html`:
```json
{
  "id": "vodni-hospodarstvi",        ← název souboru stránky (bez diakritiky a mezer!)
  "nazev": "Vodní hospodářství",
  "ikona": "voda",                   ← voda | teplo | hute | plyn | srtp (viz ICONS v build.py)
  "perex": "Krátký popis…",          ← karta na úvodu, menu, hlavička stránky
  "cover": "cerpaci-stanice-a-distribuce-pitne-vody-2",  ← fotka karty a pozadí hlavičky
  "uvod": ["odstavec", "…"],
  "sekce": [ { "id", "nazev", "odstavce": [...], "foto": ["…-1", "…-2", …] } ],
  "foto": [...],                     ← volitelné: galerie pro obor bez sekcí (Hutě)
  "reference": [ referenční blok, … ]
}
```
- **Nová sekce v oboru:** přidejte objekt do `sekce`. Sám se objeví v postranním obsahu stránky, v menu karty na úvodu a dostane kotvu `#id`.
- **Pořadí oborů** se řídí pořadím v poli. Mění se tím úvodní karty, menu, patička i tlačítka Předchozí a Další.
- Na úvodní stránce mají první dva obory velké karty a zbylé tři menší.

### 1.4 Reference
Referenční blok vypadá takto (stejný formát mají `obory[].reference[]` i `dalsi_reference`):
```json
{
  "id": "trafostanice-reference",
  "nazev": "Trafostanice",
  "uvod": ["Úvodní věta bloku…"],
  "skupiny": [
    { "nazev": "Ostravské vodárny a kanalizace a.s.",   ← nepovinné (podnadpis skupiny)
      "popis": "Volitelný delší text skupiny",           ← nepovinné
      "polozky": ["Akce 1", "Akce 2", "…"] }
  ]
}
```
- **Nová reference:** připište řádek do `polozky` příslušné skupiny. Počet „xx akcí“ se přepočítá sám.
- Každá reference se zobrazí na stránce oboru **i** na stránce `reference.html`, kde funguje vyhledávání a filtr.

### 1.5 Činnosti – `cinnosti`
```json
{ "id": "servis", "nazev": "Servis", "odstavce": ["…"], "foto": ["servis-1", "servis-2", "servis-3", "servis-4"] }
```
Ikona se vybírá podle `id` (v `ICONS` v `build.py` musí existovat klíč se stejným názvem). Pro novou činnost proto přidejte i ikonu, nebo použijte existující `id`. První fotka se zobrazí velká, další tři pod ní.

Krátký text pro dlaždici na úvodní stránce je prvních ~110 znaků prvního odstavce.

### 1.6 Dotované projekty – `dotace.projekty`
Každý projekt má `nazev`, `kod`, `popis`, `financovani`, `prijemce`, `spoluprijemce`, `doba`, `poskytovatel`, `soubor` (PDF) a `nahled` (obrázek). Pro další projekt zkopírujte celý objekt `{ … }` a oddělte ho čárkou.

### 1.7 Anglická verze – `data/obsah.en.json`
- Soubor má **úplně stejnou strukturu** jako `obsah.json`, jen s anglickými texty. Hodnoty `id`, `foto`, `cover`, `soubor` a `ikona` musí zůstat stejné jako v české verzi. Podle nich se páruje přepínač jazyků, filtr referencí a fotografie.
- **Když přidáte nebo změníte obsah v češtině, udělejte stejnou změnu i v `obsah.en.json`.** Jinak bude anglická verze neúplná, protože se nepřekládá automaticky.
- Texty, které nejsou v JSON (menu, tlačítka, nadpisy sekcí úvodu, popisky HMI panelu), jsou ve slovníku `T` na začátku `build.py`: část `"cs"` pro češtinu a `"en"` pro angličtinu.
- Anglické stránky se ukládají do složky `en/` se stejnými názvy souborů jako české (`en/vodni-hospodarstvi.html` atd.). Přepínač CZ / EN tak vždy vede na odpovídající stránku.
- Jednotné anglické termíny: ČOV = *WWTP*, ÚČOV = *Central WWTP*, ČS = *PS (pumping station)*, MaR = *I&C*, SŘTP = *process control*, ATS = *booster station*, VZT = *HVAC*, VN/NN = *HV/LV*, EOP = *EAF*.
- Publicita dotace (PDF) existuje jen česky, v angličtině je to u odkazu uvedené.

---

## 2. Fotografie

- Složka: `assets/img/foto/`
- Každá fotka existuje **ve dvou velikostech**:
  - `nazev.webp` – velká (max. 1600 px), otevírá se v galerii
  - `nazev-sm.webp` – náhled (max. 640 px), zobrazuje se ve stránce
- V `obsah.json` se fotka uvádí **bez přípony a bez `-sm`**, např. `"servis-2"`.
- Fotky jsou pojmenované podle původní stránky a pořadí (`energetika-1` až `energetika-4`).

**Přidání nové fotky (příklad):**
```bash
# potřebuje Pillow: pip install pillow
python3 -c "
from PIL import Image, ImageOps
im = ImageOps.exif_transpose(Image.open('moje-foto.jpg')).convert('RGB')
big = im.copy(); big.thumbnail((1600,1600)); big.save('assets/img/foto/energetika-5.webp', quality=80)
sm  = im.copy(); sm.thumbnail((640,640));   sm.save('assets/img/foto/energetika-5-sm.webp', quality=74)
"
```
Pak přidejte `"energetika-5"` do pole `foto` a spusťte `python3 build.py`. Bez Pythonu lze WebP vytvořit např. na https://squoosh.app. Uložte dvě velikosti se stejnými názvy.

Ostatní obrázky:
| Soubor | Použití |
|---|---|
| `assets/img/logo-prospect-white.png` | logo v hlavičce a patičce (bílá verze pro tmavé pozadí) |
| `assets/img/logo-prospect.png` | původní modré logo (pro světlé pozadí, záloha) |
| `assets/img/pas-realizaci.webp` | pás 6 fotografií pod sekcí O společnosti |
| `assets/img/prospect-energo.webp` | logo dceřiné společnosti |
| `assets/img/certifikace.png` | značky IQNet / CQS |
| `assets/img/og-image.jpg` | náhled při sdílení odkazu (1200×630) |
| `assets/img/favicon.png` | ikona v záložce prohlížeče |
| `assets/img/obory/*.png` | původní ikony oborů. Nový web používá SVG ikony, tyto jsou jen záloha. |

---

## 3. Vzhled – `assets/css/style.css`

Soubor je rozdělený do číslovaných bloků (1 Proměnné, 2 Základ, 3 Komponenty, 4 Úvod, 5 Podstránky, 6 Patička, 7 Animace, 8 Responzivita).

**Nejčastější změny jsou v bloku 1 (`:root`):**
```css
--bg: #050b14;      /* pozadí stránky */
--cyan: #00bdf2;    /* hlavní akcentová barva (tlačítka, odkazy, zvýraznění) */
--blue: #0069aa;    /* druhá firemní barva */
--ok: #3cf0a0;      /* zelená „ONLINE/RUN“ */
--radius: 18px;     /* zaoblení karet */
--wrap: 1240px;     /* maximální šířka obsahu */
--font-head / --font-body / --font-mono   /* písma */
```
- **Jiná písma:** upravte odkaz na Google Fonts v `build.py` (funkce `page()`, řádek `fonts.googleapis.com`) a proměnné `--font-*`.
- **Vypnutí animace nadpisů** (lesk na zvýrazněném textu): v `.hl` smažte řádek `animation: shine…`.
- **Rychlost běžícího pásu zákazníků:** `.marquee-track { animation: marquee 60s … }`. Vyšší číslo znamená pomalejší pás.
- Hranice pro mobil a tablet jsou na konci souboru: `@media (max-width: 1024px)` a `(max-width: 700px)`.

---

## 4. Interaktivita – `assets/js/main.js`

Čistý JavaScript bez knihoven, rozdělený do 7 bloků:
1. **Menu:** burger na mobilu a rozbalovací „Obory“.
2. **Animace při scrollu:** prvky s třídou `reveal` se plynule objeví. Prodlevu určuje `style="--d:120ms"`.
3. **Počítadla:** prvek s `data-count="100" data-suffix="+"`.
4. **HMI panel:** ilustrační hodnoty. Výchozí čísla a rozsah kolísání jsou ve funkci `updateHmi()`, např. `vals.flow = 128 + Math.sin(t / 4) * 6`. JS mění texty s atributem `data-val` (pressure, flow, level) a výšku vody v obdélníku `data-level-rect`. Vzhled panelu (nádrže, potrubí, motory, ventily, displeje) je SVG ve funkci `hmi_panel()` v `build.py`. Pomocné funkce `tank()`, `motor()`, `valve()`, `display()` a `instrument()` kreslí jednotlivé prvky, takže jdou snadno přidat další. Barvy SCADA obrazovky jsou v `style.css` u tříd `.s-…` (např. `.s-bg` = tyrkysové pozadí).
5. **Lightbox:** každý odkaz s třídou `g-item` uvnitř `.gallery`.
6. **Filtr referencí:** hledá bez ohledu na diakritiku a velikost písmen. Parametr `?obor=` v adrese předvolí filtr.
7. **Scrollspy:** zvýraznění v postranním obsahu stránek oborů.

---

## 5. `build.py` – co v něm najdete

| Část | K čemu |
|---|---|
| `LANGS`, `T` | jazykové verze (kam se ukládají) a texty rozhraní v češtině a angličtině |
| `ICONS` | SVG ikony (24×24). Novou přidáte jako `"nazev": '<path d="…"/>'`. Lze použít ikony z https://lucide.dev, stačí obsah tagu `<svg>`. |
| `header()` | položky hlavního menu (pořadí; názvy jsou v `T[…]["nav"]`) |
| `header()`, `footer()` | hlavička a patička. **Kontaktní sekce** a mapa jsou ve `footer()`. |
| `page()` | společná kostra stránky: `<head>`, SEO meta tagy, písma, CSS a JS |
| `hmi_panel()` | SVG animovaného SCADA panelu na úvodu (+ pomocné `tank()`, `motor()`, `valve()`, `display()`, `instrument()`) |
| `build_index()` | úvodní stránka (pořadí a nadpisy sekcí) |
| `build_obor()` | šablona stránky oboru |
| `build_cinnosti()`, `build_reference()`, `build_dotace()`, `build_404()` | ostatní stránky |
| `REDIRECTS` | přesměrování starých adres na nové (zapisuje se do `.htaccess`) |

**Přidání úplně nové stránky** (např. „Kariéra“):
1. Do `obsah.json` i `obsah.en.json` přidejte data, např. `"kariera": {...}`.
2. V `build.py` vytvořte funkci `build_kariera()` podle vzoru `build_dotace()` a zavolejte `page("kariera.html", "Kariéra", "popis…", "kariera", body)`.
3. Funkci zavolejte v bloku `if __name__ == "__main__":` a přidejte `"kariera.html"` do seznamu `pages` kvůli sitemapě.
4. Do menu ve funkci `header()` přidejte položku a do `T["cs"]["nav"]` a `T["en"]["nav"]` její název.

---

## 6. Nasazení na hosting

Nahrajte na server **vše kromě** `build.py`, `data/`, `README.md` a `poznámky.md` (jejich nahrání ale ničemu nevadí).

- **Apache** (většina českých hostingů): soubor `.htaccess` zajistí stránku 404, přesměrování starých adres (301) a cache obrázků.
- **Nginx:** `.htaccess` nefunguje. Přesměrování je třeba přepsat do konfigurace serveru, seznam je v `REDIRECTS` v `build.py`.
- **GitHub Pages / Netlify:** fungují bez úprav. Pro Netlify lze přesměrování převést do souboru `_redirects`.
- Po nasazení zkontrolujte, že `firma.web` v `obsah.json` odpovídá skutečné doméně, a znovu spusťte `build.py`.

### Přesměrování starých adres (výběr)
| Stará adresa | Nová |
|---|---|
| `/ridici-systemy` | `srtp-a-elektro.html#ridici-systemy` |
| `/projektovani`, `/servis`, … | `cinnosti.html#projektovani`, … |
| `/vybrane-reference-1` | `vodni-hospodarstvi.html#reference` |
| `/oblast-plynovych-zarizeni` | `reference.html?obor=plynova-zarizeni` |
| `/srtp-reference` | `reference.html#ref-srtp-reference` |

Kompletní seznam je v `.htaccess`.

---

## 7. Co z původního webu chybí nebo je potřeba doplnit

- Původní anglický web `en.prospect.cz` už není potřeba, protože nová anglická verze je ve složce `en/`. Pokud doména `en.prospect.cz` dál existuje, doporučujeme ji přesměrovat na `www.prospect.cz/en/`.
- **Google Analytics:** původní web používal měření `G-0JM7X8EGJ8` s lištou souhlasu s cookies. Nový web žádné cookies nepoužívá. Pokud chcete měření vrátit, je nutné doplnit **i lištu souhlasu** (GDPR), např. open-source [CookieConsent](https://cookieconsent.orestbida.com/), a měřicí kód vložit do `<head>` ve funkci `page()` v `build.py`.
- **Administrace (Eliška CMS)** už není. Obsah se spravuje přes `obsah.json`.
- Fotografie v sekcích oborů a činností převzaly původní fotky ve stejném pořadí. Pokud máte novější nebo kvalitnější snímky, stačí je vyměnit (viz kap. 2).
- Kontaktní formulář nový web nemá (původní také ne). Kontakt vede přes telefon a e-mail.

---

## 8. Rychlá kontrola po úpravách
- [ ] `python3 build.py` proběhl bez chyby
- [ ] úvodní stránka i stránky oborů se zobrazí, obrázky se načtou
- [ ] na mobilu (zúžené okno prohlížeče) funguje menu
- [ ] vyhledávání v `reference.html` najde novou položku
- [ ] změny jsou nahrané na server, včetně nových fotek v `assets/img/foto/`
