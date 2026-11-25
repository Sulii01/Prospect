#!/usr/bin/env python3
"""
Generátor statického webu PROSPECT spol. s r.o.

Načte veškerý obsah z data/obsah.json a vygeneruje hotové HTML stránky
do kořenové složky projektu. Nepotřebuje žádné knihovny – stačí Python 3.8+.

Použití:
    python3 build.py

Podrobný návod k úpravám najdete v souboru poznámky.md.
"""
import json
import html
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "data" / "obsah.json").read_text(encoding="utf-8"))
F = DATA["firma"]
VERSION = date.today().strftime("%Y%m%d")  # přidává se k CSS/JS kvůli cache


def e(text):
    """Escapuje text pro bezpečné vložení do HTML."""
    return html.escape(str(text), quote=True)


def tel_href(num):
    return "tel:" + re.sub(r"[^\d+]", "", num)


# --------------------------------------------------------------------------
# Ikony (vlastní lineární SVG, 24×24, barva = currentColor)
# --------------------------------------------------------------------------
ICONS = {
    "voda": '<path d="M12 2.7s-6.5 7.1-6.5 11.6a6.5 6.5 0 0 0 13 0C18.5 9.8 12 2.7 12 2.7z"/><path d="M8.6 14.6a3.5 3.5 0 0 0 3.4 3.1"/>',
    "teplo": '<path d="M12 22a6 6 0 0 0 6-6c0-3.4-2.3-5.4-3.6-7.6-.7 1.7-1.6 2.6-2.9 3.1.4-3.7-1.4-6.6-3.7-8.5.2 3.2-1.9 5.6-3 7.6A7.6 7.6 0 0 0 6 16a6 6 0 0 0 6 6z"/><path d="M12 22a2.6 2.6 0 0 1-2.6-2.6c0-1.6 1.6-2.6 2.6-4.4 1 1.8 2.6 2.8 2.6 4.4A2.6 2.6 0 0 1 12 22z"/>',
    "hute": '<path d="M3 21h18"/><path d="M4 21V11l5 3V11l5 3V8l6 3v10"/><path d="M17 5V2.5"/><path d="M14.5 6V4"/><path d="M8 18h2M13 18h2"/>',
    "plyn": '<path d="M5 9h14v6H5z"/><path d="M2 12h3M19 12h3"/><path d="M12 9V5"/><path d="M8.5 5h7"/><circle cx="12" cy="18.5" r="2.5"/><path d="M12 15v1"/>',
    "srtp": '<rect x="6" y="6" width="12" height="12" rx="1.5"/><rect x="9.5" y="9.5" width="5" height="5" rx=".5"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
    "projektovani": '<path d="M3 3h12l6 6v12H3z"/><path d="M15 3v6h6"/><path d="M7 13h10M7 17h6"/>',
    "vyvoj": '<path d="M9 2h6"/><path d="M10 2v6.5L4.6 18.2A2.5 2.5 0 0 0 6.8 22h10.4a2.5 2.5 0 0 0 2.2-3.8L14 8.5V2"/><path d="M7 15h10"/>',
    "dodavky": '<path d="M2 7h11v10H2z"/><path d="M13 10h4.5L21 13.5V17h-8"/><circle cx="6" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>',
    "montaze": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.2L3 17.8 6.2 21l6.3-6.3a4 4 0 0 0 5.2-5.4l-2.6 2.6-2.3-.6-.6-2.3z"/>',
    "software": '<rect x="2" y="4" width="20" height="14" rx="2"/><path d="M8 21h8"/><path d="M9 9l-2.5 2.5L9 14M15 9l2.5 2.5L15 14"/>',
    "servis": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>',
    "obchodni-cinnost": '<path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "doc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M9 15l2 2 4-4"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "chevron": '<path d="m6 9 6 6 6-6"/>',
    "external": '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><path d="M15 3h6v6M10 14 21 3"/>',
}


def icon(name, cls="ico"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            f'{ICONS[name]}</svg>')


def img(foto_id, alt, cls="", sizes="(max-width: 700px) 100vw, 50vw", eager=False):
    """Obrázek s náhledem (-sm) a velkou verzí. foto_id = název souboru bez přípony."""
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img class="{cls}" src="assets/img/foto/{foto_id}-sm.webp" '
            f'srcset="assets/img/foto/{foto_id}-sm.webp 640w, assets/img/foto/{foto_id}.webp 1200w" '
            f'sizes="{sizes}" alt="{e(alt)}" {load} decoding="async">')


# --------------------------------------------------------------------------
# Společné části: hlavička, menu, patička
# --------------------------------------------------------------------------
NAV = [
    ("index.html", "Úvod", "uvod"),
    ("index.html#obory", "Obory", "obory"),  # rozbalovací menu oborů
    ("cinnosti.html", "Činnosti", "cinnosti"),
    ("reference.html", "Reference", "reference"),
    ("dotovane-projekty.html", "Dotované projekty", "dotace"),
    ("#kontakt", "Kontakt", "kontakt"),
]


def header(active):
    obory_menu = "".join(
        f'<li><a href="{o["id"]}.html">{icon(o["ikona"])}<span><strong>{e(o["nazev"])}</strong>'
        f'<small>{e(o["perex"])}</small></span></a></li>' for o in DATA["obory"])
    items = []
    for href, label, key in NAV:
        cur = ' aria-current="page"' if key == active else ""
        if key == "obory":
            items.append(
                f'<li class="has-mega"><button class="nav-link mega-toggle" aria-expanded="false" '
                f'aria-controls="mega">{label}{icon("chevron", "ico chev")}</button>'
                f'<div class="mega" id="mega"><ul>{obory_menu}</ul></div></li>')
        else:
            items.append(f'<li><a class="nav-link" href="{href}"{cur}>{label}</a></li>')
    return f'''
<a class="skip" href="#obsah">Přeskočit na obsah</a>
<header class="site-header" data-header>
  <div class="wrap header-in">
    <a class="brand" href="index.html" aria-label="{e(F["nazev"])} – úvodní stránka">
      <img src="assets/img/logo-prospect-white.png" alt="PROSPECT" width="157" height="24">
      <span class="brand-tag">{e(F["slogan"])}</span>
    </a>
    <nav class="main-nav" aria-label="Hlavní navigace" data-nav>
      <ul>{"".join(items)}</ul>
      <div class="nav-extra">
        <a class="lang" href="{e(F["web_en"])}" hreflang="en" lang="en">{icon("globe")}EN</a>
        <a class="btn btn-sm btn-primary" href="{tel_href(F["telefony"][0])}">{icon("phone")}{e(F["telefony"][0])}</a>
      </div>
    </nav>
    <button class="burger" aria-label="Otevřít menu" aria-expanded="false" data-burger><span></span><span></span><span></span></button>
  </div>
</header>'''


def footer():
    tels = "".join(f'<a href="{tel_href(t)}">{e(t)}</a>' for t in F["telefony"])
    obory = "".join(f'<li><a href="{o["id"]}.html">{e(o["nazev"])}</a></li>' for o in DATA["obory"])
    cin = "".join(f'<li><a href="cinnosti.html#{c["id"]}">{e(c["nazev"])}</a></li>' for c in DATA["cinnosti"])
    return f'''
<section class="contact" id="kontakt" aria-labelledby="kontakt-h">
  <div class="wrap">
    <div class="contact-grid">
      <div class="contact-main reveal">
        <p class="eyebrow">Kontakt</p>
        <h2 id="kontakt-h">Pojďme spolu řídit vaši technologii.</h2>
        <p class="lead">Projekt, dodávka, program i servis. Ozvěte se nám – rádi s vámi probereme váš záměr.</p>
        <div class="contact-cards">
          <a class="ccard" href="{tel_href(F["telefony"][0])}">{icon("phone")}<span><small>Telefon</small><strong>{e(F["telefony"][0])}</strong></span></a>
          <a class="ccard" href="mailto:{e(F["email"])}">{icon("mail")}<span><small>E-mail – sekretariát</small><strong>{e(F["email"])}</strong></span></a>
          <a class="ccard" href="{e(F["mapa_odkaz"])}" target="_blank" rel="noopener">{icon("pin")}<span><small>Adresa</small><strong>{e(F["ulice"])}, {e(F["mesto"])}</strong></span></a>
        </div>
      </div>
      <div class="contact-details reveal">
        <dl class="details">
          <div><dt>Společnost</dt><dd><strong>{e(F["nazev"])}</strong><br>{e(F["ulice"])}<br>{e(F["mesto"])}<br>PSČ: {e(F["psc"])}</dd></div>
          <div><dt>Identifikace</dt><dd>IČ: {e(F["ic"])}<br>DIČ: {e(F["dic"])}</dd></div>
          <div><dt>Telefon</dt><dd class="stack">{tels}<span>Fax: {e(F["fax"])}</span></dd></div>
          <div><dt>Kde nás najdete</dt><dd>{e(F["kancelar"])}</dd></div>
        </dl>
        <div class="map">
          <iframe title="Mapa – {e(F["nazev"])}" src="{e(F["mapa_embed"])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        </div>
      </div>
    </div>
  </div>
</section>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <img src="assets/img/logo-prospect-white.png" alt="PROSPECT" width="157" height="24" loading="lazy">
      <p class="muted">{e(F["slogan"]).capitalize()}. Projekčně-inženýrská organizace v oblasti investiční výstavby od roku 1991.</p>
      <p class="muted small">{e(F["rejstrik"])}</p>
    </div>
    <nav aria-label="Obory"><h3>Obory</h3><ul>{obory}</ul></nav>
    <nav aria-label="Činnosti"><h3>Činnosti</h3><ul>{cin}</ul></nav>
    <nav aria-label="Další odkazy"><h3>Společnost</h3><ul>
      <li><a href="reference.html">Reference</a></li>
      <li><a href="dotovane-projekty.html">Dotované projekty</a></li>
      <li><a href="index.html#kvalita">Certifikace ISM</a></li>
      <li><a href="{e(DATA["uvod"]["energo_web"])}" target="_blank" rel="noopener">PROSPECT ENERGO a.s.</a></li>
      <li><a href="{e(F["web_en"])}" hreflang="en" lang="en">English version</a></li>
    </ul></nav>
  </div>
  <div class="wrap footer-bottom">
    <span>© <span data-year>{date.today().year}</span> {e(F["nazev"])}</span>
    <a href="#top" class="to-top">Nahoru ↑</a>
  </div>
</footer>
<div class="lightbox" data-lightbox hidden>
  <button class="lb-close" aria-label="Zavřít">×</button>
  <button class="lb-prev" aria-label="Předchozí">‹</button>
  <figure><img alt=""><figcaption></figcaption></figure>
  <button class="lb-next" aria-label="Další">›</button>
</div>'''


def page(filename, title, description, active, body, body_class=""):
    full_title = title if "PROSPECT" in title else f"{title} | {F['nazev']}"
    canonical = F["web"].rstrip("/") + "/" + ("" if filename == "index.html" else filename)
    doc = f'''<!DOCTYPE html>
<html lang="cs" class="no-js">
<head>
<meta charset="utf-8">
{'<base href="/">' if filename == "404.html" else ""}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(description)}">
<meta name="author" content="{e(F["nazev"])}">
<meta name="theme-color" content="#050b14">
<link rel="canonical" href="{e(canonical)}">
<link rel="alternate" hreflang="en" href="{e(F["web_en"])}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:image" content="{e(F["web"].rstrip("/"))}/assets/img/og-image.jpg">
<meta property="og:locale" content="cs_CZ">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap&subset=latin-ext" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css?v={VERSION}">
<script src="assets/js/main.js?v={VERSION}" defer></script>
</head>
<body class="{body_class}" id="top">
{header(active)}
<main id="obsah">
{body}
</main>
{footer()}
</body>
</html>
'''
    (ROOT / filename).write_text(doc, encoding="utf-8")
    return filename


# --------------------------------------------------------------------------
# Úvodní stránka
# --------------------------------------------------------------------------
HMI = '''
<div class="hmi" aria-hidden="true">
  <div class="hmi-bar">
    <span class="hmi-dot"></span><span>PLC-01 · ONLINE</span>
    <span class="hmi-title">HMI · Čerpací stanice</span>
    <span class="hmi-clock" data-clock>--:--:--</span>
  </div>
  <svg class="hmi-svg" viewBox="0 0 520 300" role="img">
    <defs>
      <linearGradient id="gWater" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#00bdf2" stop-opacity=".95"/><stop offset="1" stop-color="#0069aa" stop-opacity=".9"/></linearGradient>
      <pattern id="gGrid" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0v20" fill="none" stroke="rgba(120,180,255,.07)"/></pattern>
    </defs>
    <rect width="520" height="300" fill="url(#gGrid)"/>
    <!-- zdroj / studna -->
    <g class="hmi-label"><text x="22" y="40">VRT V-1</text></g>
    <rect x="22" y="52" width="70" height="150" rx="6" class="hmi-tank"/>
    <rect x="24" y="110" width="66" height="90" rx="4" fill="url(#gWater)" opacity=".55"/>
    <!-- potrubí -->
    <path d="M92 180 H170" class="pipe"/><path d="M92 180 H170" class="flow"/>
    <path d="M230 180 H300 V90 H360" class="pipe"/><path d="M230 180 H300 V90 H360" class="flow"/>
    <path d="M440 200 V250 H500" class="pipe"/><path d="M440 200 V250 H500" class="flow"/>
    <!-- čerpadlo -->
    <g transform="translate(200 180)">
      <circle r="30" class="pump"/>
      <g class="impeller"><path d="M0-20 L5-4 L0 0 Z M20 0 L4 5 L0 0 Z M0 20 L-5 4 L0 0 Z M-20 0 L-4-5 L0 0 Z" fill="#00bdf2"/></g>
      <circle r="4" fill="#e6eef8"/>
    </g>
    <text x="178" y="235" class="hmi-tag">Č-101 <tspan class="ok">RUN</tspan></text>
    <!-- ventil -->
    <g transform="translate(300 135)"><path d="M-10-10 L10 10 M-10 10 L10-10" stroke="#3cf0a0" stroke-width="2"/><path d="M-10-10 V10 M10-10 V10" stroke="#3cf0a0" stroke-width="2" opacity=".5"/></g>
    <!-- vodojem -->
    <g class="hmi-label"><text x="360" y="40">VODOJEM VDJ-1</text></g>
    <rect x="360" y="52" width="140" height="150" rx="8" class="hmi-tank"/>
    <rect x="362" y="96" width="136" height="104" rx="6" fill="url(#gWater)" data-level-rect/>
    <path d="M362 96 q17 -5 34 0 t34 0 t34 0 t34 0" class="wave" data-wave/>
    <line x1="352" y1="70" x2="358" y2="70" class="tick"/><line x1="352" y1="110" x2="358" y2="110" class="tick"/><line x1="352" y1="150" x2="358" y2="150" class="tick"/><line x1="352" y1="190" x2="358" y2="190" class="tick"/>
    <!-- čidla -->
    <g class="sensor" transform="translate(130 150)"><circle r="13"/><text y="4">PT</text></g>
    <g class="sensor" transform="translate(265 150)"><circle r="13"/><text y="4">FT</text></g>
    <g class="sensor" transform="translate(430 30)"><circle r="13"/><text y="4">LT</text></g>
  </svg>
  <div class="hmi-values">
    <div><small>Tlak PT-101</small><strong data-val="pressure">4.20</strong><em>bar</em></div>
    <div><small>Průtok FT-201</small><strong data-val="flow">128.4</strong><em>m³/h</em></div>
    <div><small>Hladina LT-301</small><strong data-val="level">72.0</strong><em>%</em></div>
  </div>
  <canvas class="hmi-trend" data-trend height="70"></canvas>
  <p class="hmi-note">Ilustrační vizualizace řízeného procesu</p>
</div>'''


def build_index():
    U = DATA["uvod"]
    stats = "".join(
        f'<div class="stat reveal"><strong data-count="{s["hodnota"]}" data-suffix="{e(s["pripona"])}">'
        f'{s["hodnota"]}{e(s["pripona"])}</strong><span>{e(s["popis"])}</span></div>' for s in U["cisla"])
    klienti = "".join(f"<li>{e(k)}</li>" for k in U["klienti"])
    o_nas = "".join(f"<p>{e(p)}</p>" for p in U["o_nas"][:2])
    filozofie = e(U["o_nas"][2])
    dodavky = "".join(f"<p>{e(p)}</p>" for p in U["dodavky_text"])

    cards = []
    for i, o in enumerate(DATA["obory"]):
        subs = "".join(f'<li><a href="{o["id"]}.html#{s["id"]}">{e(s["nazev"])}</a></li>' for s in o["sekce"])
        subs = subs or f'<li><a href="{o["id"]}.html#reference">Vybrané reference</a></li>'
        cards.append(f'''
      <article class="obor-card reveal" style="--d:{i * 70}ms">
        <a class="obor-link" href="{o["id"]}.html" aria-label="{e(o["nazev"])}"></a>
        {img(o["cover"], o["nazev"], "obor-img")}
        <div class="obor-body">
          <span class="obor-ico">{icon(o["ikona"])}</span>
          <span class="obor-num">0{i + 1}</span>
          <h3>{e(o["nazev"])}</h3>
          <p>{e(o["perex"])}</p>
          <ul class="obor-subs">{subs}</ul>
          <span class="more">Více o oboru {icon("arrow")}</span>
        </div>
      </article>''')

    rs = DATA["ridici_systemy"]
    ridici = next(s for o in DATA["obory"] for s in o["sekce"] if s["id"] == "ridici-systemy")
    software = next(c for c in DATA["cinnosti"] if c["id"] == "software")
    tech = "".join(
        f'<div class="tech reveal"><h4>{e(g["nazev"])}</h4><ul>' +
        "".join(f"<li>{e(x)}</li>" for x in g["polozky"]) + "</ul></div>" for g in rs["skupiny"])

    steps = "".join(
        f'<li class="reveal" style="--d:{i * 60}ms"><a href="cinnosti.html#{c["id"]}">'
        f'<span class="step-n">{i + 1:02d}</span>{icon(c["id"])}<strong>{e(c["nazev"])}</strong>'
        f'<small>{e(short(c["odstavce"][0], 110))}</small></a></li>'
        for i, c in enumerate(DATA["cinnosti"]))

    zeme = "".join(f"<li>{e(z)}</li>" for z in U["zeme"])
    certs = "".join(
        f'<a class="cert reveal" href="{e(c["soubor"])}" target="_blank" rel="noopener">{icon("doc")}'
        f'<span><strong>{e(c["nazev"])}</strong><small>{e(c["popis"])}</small></span>{icon("external", "ico ext")}</a>'
        for c in U["certifikaty"])

    body = f'''
<section class="hero">
  <div class="hero-bg" aria-hidden="true"><div class="glow g1"></div><div class="glow g2"></div><div class="grid-bg"></div></div>
  <div class="wrap hero-in">
    <div class="hero-text">
      <p class="eyebrow pulse">{e(U["hero_stitek"])}</p>
      <h1>{hero_title(U["hero_nadpis"])}</h1>
      <p class="lead">{e(U["hero_text"])}</p>
      <div class="hero-cta">
        <a class="btn btn-primary" href="#obory">Naše obory {icon("arrow")}</a>
        <a class="btn btn-ghost" href="reference.html">Reference</a>
      </div>
      <ul class="hero-tags">
        <li>PLC SIMATIC</li><li>SCADA / vizualizace</li><li>MaR</li><li>Dálkový dohled</li><li>Elektro NN / VN</li>
      </ul>
    </div>
    {HMI}
  </div>
</section>

<section class="stats" aria-label="PROSPECT v číslech">
  <div class="wrap stats-in">{stats}</div>
</section>

<section class="marquee" aria-label="Vybraní zákazníci">
  <p class="marquee-label">Pracovali jsme pro</p>
  <div class="marquee-track"><ul>{klienti}</ul><ul aria-hidden="true">{klienti}</ul></div>
</section>

<section class="section about" id="o-nas">
  <div class="wrap about-grid">
    <div class="reveal">
      <p class="eyebrow">O společnosti</p>
      <h2>Od projektu po dálkový dohled. <span class="hl">Od roku 1991.</span></h2>
      {o_nas}
    </div>
    <div class="about-side reveal">
      <blockquote class="quote"><p>„{filozofie}“</p></blockquote>
      <div class="about-domains">
        <p>{e(U["obory_text"])}</p>
        <ul>{"".join(f'<li><a href="{o["id"]}.html">{icon(o["ikona"])}{e(o["nazev"])}</a></li>' for o in DATA["obory"])}</ul>
      </div>
    </div>
  </div>
  <div class="strip reveal" role="img" aria-label="Ukázky realizací PROSPECT"><img src="assets/img/pas-realizaci.webp" alt="" loading="lazy" width="2000" height="430"></div>
</section>

<section class="section" id="obory">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Obory</p>
      <h2>Pět oborů. Jedna řídicí logika.</h2>
      <p class="lead">Automatizujeme technologie od úpraven vod po ocelárny – vždy s vlastním projektem, programem a servisem.</p>
    </div>
    <div class="obory-grid">{"".join(cards)}</div>
  </div>
</section>

<section class="section control" id="ridici-systemy">
  <div class="wrap">
    <div class="control-grid">
      <div class="reveal">
        <p class="eyebrow">Řídicí systémy &amp; software</p>
        <h2>Srdce každé technologie je <span class="hl">řídicí systém</span>.</h2>
        <p class="lead">{e(ridici["odstavce"][0])}</p>
        <p>{e(software["odstavce"][2])}</p>
        <p>{e(ridici["odstavce"][2])}</p>
        <div class="btn-row">
          <a class="btn btn-primary" href="srtp-a-elektro.html#ridici-systemy">Řídicí systémy {icon("arrow")}</a>
          <a class="btn btn-ghost" href="cinnosti.html#software">Software a vizualizace</a>
        </div>
      </div>
      <figure class="control-photo reveal">
        {img("ridici-systemy-4", "Rozváděč s řídicím systémem SIMATIC", "", "(max-width: 900px) 100vw, 40vw")}
        <figcaption><span class="hmi-dot"></span>Rozváděče, PLC a operátorská pracoviště – navrženo, naprogramováno a oživeno u nás.</figcaption>
      </figure>
    </div>
    <h3 class="sub-h reveal">{e(rs["nadpis"])}</h3>
    <p class="muted reveal">{e(rs["text"])}</p>
    <div class="tech-grid">{tech}</div>
  </div>
</section>

<section class="section" id="cinnosti">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Činnosti</p>
      <h2>Celý životní cyklus zařízení pod jednou střechou.</h2>
      <p class="lead">{e(DATA["cinnosti_uvod"])}</p>
    </div>
    <ol class="steps">{steps}</ol>
    <div class="deliver reveal">{dodavky}</div>
  </div>
</section>

<section class="section world" id="zahranici">
  <div class="wrap world-grid">
    <div class="reveal">
      <p class="eyebrow">Mezinárodní působnost</p>
      <h2>Z Ostravy do <span class="hl">devíti zemí</span> Evropy.</h2>
      <p class="lead">{e(U["zahranici_text"])}</p>
      <p class="muted">{e(U["prostredky_text"])}</p>
    </div>
    <ul class="countries reveal">{zeme}</ul>
  </div>
</section>

<section class="section quality" id="kvalita">
  <div class="wrap quality-grid">
    <div class="reveal">
      <p class="eyebrow">Kvalita</p>
      <h2>Certifikovaný integrovaný systém managementu</h2>
      <p>{e(U["ism_text"])}</p>
      <img class="badges" src="assets/img/certifikace.png" alt="Certifikační značky IQNet a CQS" width="122" height="43" loading="lazy">
    </div>
    <div class="certs">{certs}</div>
  </div>
</section>

<section class="section energo">
  <div class="wrap">
    <a class="energo-card reveal" href="{e(U["energo_web"])}" target="_blank" rel="noopener">
      <div>
        <p class="eyebrow">Skupina PROSPECT</p>
        <h2>PROSPECT ENERGO a.s.</h2>
        <p>{e(U["energo_text"])}</p>
        <span class="more">prospect-energo.cz {icon("external")}</span>
      </div>
      <img src="assets/img/prospect-energo.webp" alt="Logo PROSPECT ENERGO" loading="lazy" width="1000" height="230">
    </a>
  </div>
</section>
'''
    page("index.html", DATA["seo"]["titulek"], DATA["seo"]["popis"], "uvod", body, "home")


def hero_title(t):
    # zvýrazní slovo „Řídicí systémy“ v hlavním nadpisu
    return e(t).replace("Řídicí systémy", '<span class="hl">Řídicí systémy</span>', 1)


def short(t, n):
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + "…"


# --------------------------------------------------------------------------
# Stránky oborů
# --------------------------------------------------------------------------
def gallery(fotos, title):
    if not fotos:
        return ""
    return '<div class="gallery">' + "".join(
        f'<a href="assets/img/foto/{f}.webp" data-lb="{e(title)}" class="g-item">'
        f'{img(f, f"{title} – fotografie {i + 1}", "", "(max-width: 700px) 50vw, 25vw")}</a>'
        for i, f in enumerate(fotos)) + "</div>"


def ref_block(r, obor=None):
    """Vykreslí jeden referenční blok (nadpis, úvod, skupiny položek)."""
    groups = []
    for g in r["skupiny"]:
        head = f'<h4>{e(g["nazev"])}</h4>' if g.get("nazev") else ""
        popis = f'<p class="muted">{e(g["popis"])}</p>' if g.get("popis") else ""
        items = "".join(f"<li>{e(x)}</li>" for x in g["polozky"])
        lst = f'<ul class="ref-list">{items}</ul>' if items else ""
        groups.append(f'<div class="ref-group">{head}{popis}{lst}</div>')
    count = sum(len(g["polozky"]) for g in r["skupiny"])
    uvod = "".join(f'<p class="muted">{e(p)}</p>' for p in r["uvod"])
    data_obor = f' data-obor="{obor}"' if obor else ""
    return (f'<article class="ref-block reveal"{data_obor} id="ref-{r["id"]}">'
            f'<header><h3>{e(r["nazev"])}</h3><span class="badge">{count} akcí</span></header>'
            f'{uvod}<div class="ref-groups">{"".join(groups)}</div></article>')


def build_obor(o, idx):
    obory = DATA["obory"]
    prev_o, next_o = obory[idx - 1], obory[(idx + 1) % len(obory)]
    toc = "".join(f'<li><a href="#{s["id"]}">{e(s["nazev"])}</a></li>' for s in o["sekce"])
    toc += '<li><a href="#reference">Vybrané reference</a></li>'
    sections = "".join(f'''
    <section class="topic reveal" id="{s["id"]}">
      <span class="topic-n">{idx + 1}.{j + 1}</span>
      <h2>{e(s["nazev"])}</h2>
      {"".join(f"<p>{e(p)}</p>" for p in s["odstavce"])}
      {gallery(s["foto"], s["nazev"])}
    </section>''' for j, s in enumerate(o["sekce"]))
    if o.get("foto"):
        sections += f'<section class="topic reveal">{gallery(o["foto"], o["nazev"])}</section>'
    refs = "".join(ref_block(r) for r in o["reference"])
    total = sum(len(g["polozky"]) for r in o["reference"] for g in r["skupiny"])
    body = f'''
<section class="page-hero">
  <div class="page-hero-img">{img(o["cover"], "", "", "100vw", eager=True)}</div>
  <div class="wrap">
    <nav class="crumbs" aria-label="Drobečková navigace"><a href="index.html">Úvod</a><span>/</span><a href="index.html#obory">Obory</a><span>/</span><span aria-current="page">{e(o["nazev"])}</span></nav>
    <span class="page-ico">{icon(o["ikona"])}</span>
    <h1>{e(o["nazev"])}</h1>
    <p class="lead">{e(o["perex"])}</p>
    <div class="hero-meta"><span><strong>{len(o["sekce"]) or "—"}</strong> specializace</span><span><strong>{total}</strong> referenčních akcí</span></div>
  </div>
</section>
<div class="wrap page-layout">
  <aside class="toc" aria-label="Obsah stránky"><p>Na této stránce</p><ul data-scrollspy>{toc}</ul>
    <a class="btn btn-primary btn-sm" href="#kontakt">Poptat řešení {icon("arrow")}</a></aside>
  <div class="page-content">
    <div class="intro reveal">{"".join(f'<p class="lead">{e(p)}</p>' for p in o["uvod"])}</div>
    {sections}
    <section class="refs" id="reference">
      <div class="section-head reveal"><p class="eyebrow">Reference</p><h2>Vybrané reference – {e(o["nazev"])}</h2></div>
      {refs}
      <a class="btn btn-ghost" href="reference.html?obor={o["id"]}">Všechny reference {icon("arrow")}</a>
    </section>
    <nav class="pager" aria-label="Další obory">
      <a href="{prev_o["id"]}.html"><small>← Předchozí obor</small><strong>{e(prev_o["nazev"])}</strong></a>
      <a href="{next_o["id"]}.html" class="next"><small>Další obor →</small><strong>{e(next_o["nazev"])}</strong></a>
    </nav>
  </div>
</div>'''
    desc = short(" ".join(o["uvod"]), 155)
    page(f'{o["id"]}.html', o["nazev"], desc, "obory", body)


# --------------------------------------------------------------------------
# Činnosti
# --------------------------------------------------------------------------
def build_cinnosti():
    chips = "".join(f'<li><a href="#{c["id"]}">{icon(c["id"])}{e(c["nazev"])}</a></li>' for c in DATA["cinnosti"])
    secs = []
    for i, c in enumerate(DATA["cinnosti"]):
        main_f = c["foto"][0] if c["foto"] else None
        secs.append(f'''
  <section class="activity reveal {'alt' if i % 2 else ''}" id="{c["id"]}">
    <div class="activity-text">
      <span class="step-n">{i + 1:02d}</span>
      <h2>{icon(c["id"])}{e(c["nazev"])}</h2>
      {"".join(f"<p>{e(p)}</p>" for p in c["odstavce"])}
    </div>
    <div class="activity-media">{gallery(c["foto"], c["nazev"]) if main_f else ""}</div>
  </section>''')
    body = f'''
<section class="page-hero slim">
  <div class="wrap">
    <nav class="crumbs" aria-label="Drobečková navigace"><a href="index.html">Úvod</a><span>/</span><span aria-current="page">Činnosti</span></nav>
    <h1>Činnosti</h1>
    <p class="lead">{e(DATA["cinnosti_uvod"])}</p>
    <ul class="chips">{chips}</ul>
  </div>
</section>
<div class="wrap activities">{"".join(secs)}</div>'''
    page("cinnosti.html", "Činnosti", DATA["cinnosti_uvod"], "cinnosti", body)


# --------------------------------------------------------------------------
# Reference (s vyhledáváním a filtrem)
# --------------------------------------------------------------------------
def build_reference():
    filters = ['<button class="chip is-active" data-filter="vse">Vše</button>'] + [
        f'<button class="chip" data-filter="{o["id"]}">{icon(o["ikona"])}{e(o["nazev"])}</button>' for o in DATA["obory"]
    ] + ['<button class="chip" data-filter="dalsi">Další reference</button>']
    blocks = []
    for o in DATA["obory"]:
        blocks.append(f'<h2 class="ref-obor" data-obor="{o["id"]}"><a href="{o["id"]}.html">{icon(o["ikona"])}{e(o["nazev"])}</a></h2>')
        blocks += [ref_block(r, o["id"]) for r in o["reference"]]
    blocks.append('<h2 class="ref-obor" data-obor="dalsi">Další reference</h2>')
    blocks.append(ref_block(DATA["dalsi_reference"], "dalsi"))
    total = sum(len(g["polozky"]) for o in DATA["obory"] for r in o["reference"] for g in r["skupiny"])
    total += sum(len(g["polozky"]) for g in DATA["dalsi_reference"]["skupiny"])
    body = f'''
<section class="page-hero slim">
  <div class="wrap">
    <nav class="crumbs" aria-label="Drobečková navigace"><a href="index.html">Úvod</a><span>/</span><span aria-current="page">Reference</span></nav>
    <h1>Reference</h1>
    <p class="lead">{e(DATA["reference_uvod"])}</p>
    <div class="hero-meta"><span><strong data-count="{total}">{total}</strong> uvedených akcí</span><span><strong>5</strong> oborů</span><span><strong>9</strong> zemí</span></div>
  </div>
</section>
<div class="wrap ref-page" data-refs>
  <div class="ref-tools">
    <label class="search">{icon("search")}<span class="sr">Hledat v referencích</span>
      <input type="search" placeholder="Hledat – např. ČOV, Prazdroj, Třinec, kogenerační…" data-ref-search></label>
    <div class="chips" role="group" aria-label="Filtr podle oboru">{"".join(filters)}</div>
    <p class="ref-count" aria-live="polite" data-ref-count></p>
  </div>
  <div class="ref-results">{"".join(blocks)}</div>
  <p class="empty" data-ref-empty hidden>Nic jsme nenašli. Zkuste jiný výraz, nebo nám <a href="#kontakt">napište</a>.</p>
</div>'''
    page("reference.html", "Reference", DATA["reference_uvod"], "reference", body)


# --------------------------------------------------------------------------
# Dotované projekty
# --------------------------------------------------------------------------
def build_dotace():
    D = DATA["dotace"]
    cards = "".join(f'''
  <article class="grant reveal">
    <a class="grant-img" href="{e(p["soubor"])}" target="_blank" rel="noopener"><img src="{e(p["nahled"])}" alt="Publicita projektu {e(p["nazev"])}" loading="lazy"></a>
    <div>
      <p class="eyebrow">{e(p["poskytovatel"])} · EU</p>
      <h2>{e(p["nazev"])}</h2>
      <p class="mono">{e(p["kod"])}</p>
      <p>{e(p["popis"])}</p>
      <p><strong>{e(p["financovani"])}</strong></p>
      <dl class="grant-meta">
        <div><dt>Příjemce</dt><dd>{e(p["prijemce"])}</dd></div>
        <div><dt>Spolupříjemce</dt><dd>{e(p["spoluprijemce"])}</dd></div>
        <div><dt>Doba řešení</dt><dd>{e(p["doba"])}</dd></div>
      </dl>
      <a class="btn btn-ghost" href="{e(p["soubor"])}" target="_blank" rel="noopener">{icon("doc")}Publicita projektu (PDF)</a>
    </div>
  </article>''' for p in D["projekty"])
    body = f'''
<section class="page-hero slim">
  <div class="wrap">
    <nav class="crumbs" aria-label="Drobečková navigace"><a href="index.html">Úvod</a><span>/</span><span aria-current="page">Dotované projekty</span></nav>
    <h1>Dotované projekty</h1>
    <p class="lead">{e(D["uvod"])}</p>
  </div>
</section>
<div class="wrap grants">{cards}</div>'''
    page("dotovane-projekty.html", "Dotované projekty", D["uvod"], "dotace", body)


def build_404():
    body = f'''
<section class="page-hero slim notfound">
  <div class="wrap">
    <p class="mono err">ERR 404 · SIGNAL LOST</p>
    <h1>Stránka nenalezena</h1>
    <p class="lead">Požadovaná stránka neexistuje nebo byla přesunuta. Nový web má jednodušší strukturu – zkuste některý z oborů.</p>
    <ul class="chips">{"".join(f'<li><a href="{o["id"]}.html">{icon(o["ikona"])}{e(o["nazev"])}</a></li>' for o in DATA["obory"])}</ul>
    <p><a class="btn btn-primary" href="index.html">Zpět na úvod {icon("arrow")}</a></p>
  </div>
</section>'''
    page("404.html", "Stránka nenalezena", "Stránka nenalezena.", "", body)


def build_sitemap(files):
    base = F["web"].rstrip("/")
    urls = "".join(
        f"<url><loc>{base}/{'' if f == 'index.html' else f}</loc><lastmod>{date.today().isoformat()}</lastmod></url>"
        for f in files)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n',
        encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n", encoding="utf-8")


# Přesměrování adres starého webu (www.prospect.cz/…) na nové stránky.
# Zapisuje se do .htaccess (Apache). Klíč = stará adresa, hodnota = nová.
REDIRECTS = {
    "cinnosti": "cinnosti.html", "reference": "reference.html", "dotovane-projekty": "dotovane-projekty.html",
    "projektovani": "cinnosti.html#projektovani", "vyvoj": "cinnosti.html#vyvoj", "dodavky": "cinnosti.html#dodavky",
    "montaze": "cinnosti.html#montaze", "software": "cinnosti.html#software", "servis": "cinnosti.html#servis",
    "obchodni-cinnost": "cinnosti.html#obchodni-cinnost",
    "vodni-hospodarstvi": "vodni-hospodarstvi.html", "teplo-a-klimatizace": "teplo-a-klimatizace.html",
    "hute-a-strojirenstvi": "hute-a-strojirenstvi.html", "plynova-zarizeni": "plynova-zarizeni.html",
    "srtp-a-elektro": "srtp-a-elektro.html",
    "vybrane-reference-1": "vodni-hospodarstvi.html#reference", "vybrane-reference-2": "teplo-a-klimatizace.html#reference",
    "vybrane-reference-3": "hute-a-strojirenstvi.html#reference", "vybrane-reference-4": "plynova-zarizeni.html#reference",
    "vybrane-reference": "srtp-a-elektro.html#reference",
    "oblast-vodniho-hospodarstvi": "reference.html?obor=vodni-hospodarstvi",
    "oblast-tepelnych-hospodarstvi-a-klimatizacnich-zarizeni": "reference.html?obor=teplo-a-klimatizace",
    "oblast-hutnich-a-strojirenskych-provozu": "reference.html?obor=hute-a-strojirenstvi",
    "oblast-plynovych-zarizeni": "reference.html?obor=plynova-zarizeni",
    "oblast-srtp-a-elektro": "reference.html?obor=srtp-a-elektro",
    "dalsi-reference": "reference.html?obor=dalsi",
    "reference-v-oblasti-vodnich-zdroju-a-upraven-vod": "reference.html#ref-reference-v-oblasti-vodnich-zdroju-a-upraven-vod",
    "reference-v-oblasti-cerpacich-stanic-a-distribuce-pitne-vody-1": "reference.html#ref-reference-v-oblasti-cerpacich-stanic-a-distribuce-pitne-vody-1",
    "reference-v-oblasti-cerpacich-stanic-technologicke-vody": "reference.html#ref-reference-v-oblasti-cerpacich-stanic-technologicke-vody",
    "reference-v-oblasti-cistiren-odpadnich-vod-cov-a-kanalizacnich-cerpacich-stanic-cs": "reference.html#ref-reference-v-oblasti-cistiren-odpadnich-vod-cov-a-kanalizacnich-cerpacich-stanic-cs",
    "srtp-reference": "reference.html#ref-srtp-reference", "silnoprouda-elektrotechnika": "reference.html#ref-silnoprouda-elektrotechnika",
    "trafostanice-reference": "reference.html#ref-trafostanice-reference",
}
for o in DATA["obory"]:
    for s in o["sekce"]:
        REDIRECTS.setdefault(s["id"], f'{o["id"]}.html#{s["id"]}')


def build_htaccess():
    lines = ["# Vygenerováno skriptem build.py – neupravujte ručně, změny dělejte v REDIRECTS v build.py",
             "ErrorDocument 404 /404.html", "DirectoryIndex index.html", "RewriteEngine On", ""]
    for old, new in REDIRECTS.items():
        lines.append(f"RewriteRule ^{re.escape(old)}/?$ /{new} [R=301,L,NE]")
    lines += ["", "<IfModule mod_expires.c>", "  ExpiresActive On",
              '  ExpiresByType image/webp "access plus 1 year"', '  ExpiresByType text/css "access plus 1 month"',
              '  ExpiresByType application/javascript "access plus 1 month"', "</IfModule>", ""]
    (ROOT / ".htaccess").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    build_index()
    for i, o in enumerate(DATA["obory"]):
        build_obor(o, i)
    build_cinnosti()
    build_reference()
    build_dotace()
    build_404()
    pages = ["index.html"] + [f'{o["id"]}.html' for o in DATA["obory"]] + \
            ["cinnosti.html", "reference.html", "dotovane-projekty.html"]
    build_sitemap(pages)
    build_htaccess()
    print("Hotovo – vygenerováno:", ", ".join(pages + ["404.html", "sitemap.xml", "robots.txt", ".htaccess"]))
