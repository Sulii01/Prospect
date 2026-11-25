#!/usr/bin/env python3
"""
Generátor statického webu PROSPECT spol. s r.o. (česky + anglicky).

Načte obsah z data/obsah.json (čeština) a data/obsah.en.json (angličtina)
a vygeneruje hotové HTML stránky:
    • česká verze  → kořenová složka projektu (index.html, …)
    • anglická verze → složka en/ (en/index.html, …)
Nepotřebuje žádné knihovny – stačí Python 3.8+.

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
# Verze CSS/JS = otisk jejich obsahu. Změní se při každé úpravě souboru,
# takže prohlížeč i GitHub Pages vždy načtou aktuální styly a skripty.
import hashlib
VERSION = hashlib.md5((ROOT / "assets/css/style.css").read_bytes() + (ROOT / "assets/js/main.js").read_bytes()).hexdigest()[:10]

# --------------------------------------------------------------------------
# Jazykové verze
#   data  = soubor s obsahem
#   out   = kam se stránky uloží
#   P     = předpona cesty k assets/ (anglické stránky leží o složku níž)
# --------------------------------------------------------------------------
LANGS = {
    "cs": {"data": "data/obsah.json", "out": ROOT, "P": "", "dir": ""},
    "en": {"data": "data/obsah.en.json", "out": ROOT / "en", "P": "../", "dir": "en/"},
}

# --------------------------------------------------------------------------
# Texty uživatelského rozhraní (menu, tlačítka, nadpisy sekcí…)
# Obsah samotný (odstavce, reference) je v data/*.json.
# --------------------------------------------------------------------------
T = {
    "cs": {
        "html_lang": "cs", "og_locale": "cs_CZ",
        "skip": "Přeskočit na obsah", "home_aria": "úvodní stránka",
        "nav": ["Úvod", "Obory", "Činnosti", "Reference", "Dotované projekty", "Kontakt"],
        "nav_aria": "Hlavní navigace", "menu_open": "Otevřít menu",
        "other_lang": "EN", "other_lang_name": "English", "other_hreflang": "en",
        "contact_eyebrow": "Kontakt", "contact_h": "Pojďme spolu řídit vaši technologii.",
        "contact_lead": "Projekt, dodávka, program i servis. Ozvěte se nám – rádi s vámi probereme váš záměr.",
        "phone": "Telefon", "email": "E-mail – sekretariát", "address": "Adresa",
        "company": "Společnost", "ident": "Identifikace", "ic": "IČ", "dic": "DIČ", "fax": "Fax",
        "where": "Kde nás najdete", "postcode": "PSČ", "map": "Mapa",
        "footer_about": "Projekčně-inženýrská organizace v oblasti investiční výstavby od roku 1991.",
        "f_fields": "Obory", "f_services": "Činnosti", "f_company": "Společnost",
        "f_refs": "Reference", "f_grants": "Dotované projekty", "f_cert": "Certifikace ISM",
        "f_other": "English version", "to_top": "Nahoru ↑", "lb_close": "Zavřít", "lb_prev": "Předchozí", "lb_next": "Další",
        # úvod
        "cta_fields": "Naše obory", "cta_refs": "Reference",
        "hero_tags": ["PLC SIMATIC", "SCADA / vizualizace", "MaR", "Dálkový dohled", "Elektro NN / VN"],
        "stats_aria": "PROSPECT v číslech", "clients_aria": "Vybraní zákazníci", "clients_label": "Pracovali jsme pro",
        "about_eyebrow": "O společnosti", "about_h": 'Od projektu po dálkový dohled. <span class="hl">Od roku 1991.</span>',
        "strip_aria": "Ukázky realizací PROSPECT",
        "fields_eyebrow": "Obory", "fields_h": "Pět oborů. Jedna řídicí logika.",
        "fields_lead": "Automatizujeme technologie od úpraven vod po ocelárny – vždy s vlastním projektem, programem a servisem.",
        "field_more": "Více o oboru", "selected_refs": "Vybrané reference",
        "ctrl_eyebrow": "Řídicí systémy &amp; software", "ctrl_h": 'Srdce každé technologie je <span class="hl">řídicí systém</span>.',
        "ctrl_btn": "Řídicí systémy", "ctrl_btn2": "Software a vizualizace",
        "ctrl_alt": "Rozváděč s řídicím systémem SIMATIC",
        "ctrl_caption": "Rozváděče, PLC a operátorská pracoviště – navrženo, naprogramováno a oživeno u nás.",
        "svc_eyebrow": "Činnosti", "svc_h": "Celý životní cyklus zařízení pod jednou střechou.",
        "world_eyebrow": "Mezinárodní působnost", "world_h": 'Z Ostravy do <span class="hl">devíti zemí</span> Evropy.',
        "q_eyebrow": "Kvalita", "q_h": "Certifikovaný integrovaný systém managementu", "q_badges_alt": "Certifikační značky IQNet a CQS",
        "energo_eyebrow": "Skupina PROSPECT", "energo_alt": "Logo PROSPECT ENERGO",
        # podstránky
        "crumb_home": "Úvod", "crumb_fields": "Obory", "crumbs_aria": "Drobečková navigace",
        "specs": "specializace", "ref_actions": "referenčních akcí", "toc": "Na této stránce", "toc_aria": "Obsah stránky",
        "inquiry": "Poptat řešení", "refs_eyebrow": "Reference", "refs_h": "Vybrané reference – {}",
        "all_refs": "Všechny reference", "prev_field": "← Předchozí obor", "next_field": "Další obor →", "pager_aria": "Další obory",
        "actions": "akcí", "photo": "fotografie",
        "svc_title": "Činnosti", "refs_title": "Reference", "grants_title": "Dotované projekty",
        "listed": "uvedených akcí", "fields_n": "oborů", "countries_n": "zemí",
        "search_label": "Hledat v referencích", "search_ph": "Hledat – např. ČOV, Prazdroj, Třinec, kogenerační…",
        "filter_aria": "Filtr podle oboru", "all": "Vše", "other_refs": "Další reference",
        "empty": 'Nic jsme nenašli. Zkuste jiný výraz, nebo nám <a href="#kontakt">napište</a>.',
        "grant_eu": "EU", "recipient": "Příjemce", "corecipient": "Spolupříjemce", "duration": "Doba řešení",
        "grant_pdf": "Publicita projektu (PDF)", "grant_alt": "Publicita projektu",
        "nf_title": "Stránka nenalezena", "nf_lead": "Požadovaná stránka neexistuje nebo byla přesunuta. Nový web má jednodušší strukturu – zkuste některý z oborů.",
        "nf_back": "Zpět na úvod",
        # HMI panel
        "hmi": {"title": "ČERPACÍ STANICE", "online": "PLC-01 · ONLINE", "app": "HMI · Vodárenský dispečink",
                "well": "VRT V-1", "filter": "FILTR F-1", "res": "VDJ-1", "pump1": "Č-101", "pump2": "Č-102",
                "mode": "Režim", "auto": "Automat", "run": "Chod", "stby": "Záloha",
                "trend": "TREND FT-201 · m³/h", "note": "Ilustrační vizualizace řízeného procesu",
                "cap1": "(120 m³)", "cap2": "(450 m³)"},
    },
    "en": {
        "html_lang": "en", "og_locale": "en_GB",
        "skip": "Skip to content", "home_aria": "home page",
        "nav": ["Home", "Fields", "Services", "References", "EU projects", "Contact"],
        "nav_aria": "Main navigation", "menu_open": "Open menu",
        "other_lang": "CZ", "other_lang_name": "Čeština", "other_hreflang": "cs",
        "contact_eyebrow": "Contact", "contact_h": "Let's control your technology together.",
        "contact_lead": "Design, supply, programming and service. Get in touch – we will be glad to discuss your project.",
        "phone": "Phone", "email": "E-mail – office", "address": "Address",
        "company": "Company", "ident": "Company ID", "ic": "Reg. No.", "dic": "VAT No.", "fax": "Fax",
        "where": "How to find us", "postcode": "Postcode", "map": "Map",
        "footer_about": "Engineering and design company in the field of investment construction since 1991.",
        "f_fields": "Fields", "f_services": "Services", "f_company": "Company",
        "f_refs": "References", "f_grants": "EU-funded projects", "f_cert": "ISM certification",
        "f_other": "Česká verze", "to_top": "Back to top ↑", "lb_close": "Close", "lb_prev": "Previous", "lb_next": "Next",
        "cta_fields": "Our fields", "cta_refs": "References",
        "hero_tags": ["PLC SIMATIC", "SCADA / visualisation", "I&amp;C", "Remote monitoring", "LV / HV electrical"],
        "stats_aria": "PROSPECT in numbers", "clients_aria": "Selected clients", "clients_label": "We have worked for",
        "about_eyebrow": "About us", "about_h": 'From design to remote monitoring. <span class="hl">Since 1991.</span>',
        "strip_aria": "Examples of PROSPECT projects",
        "fields_eyebrow": "Fields", "fields_h": "Five fields. One control logic.",
        "fields_lead": "We automate technologies from water treatment plants to steelworks – always with our own design, software and service.",
        "field_more": "More about this field", "selected_refs": "Selected references",
        "ctrl_eyebrow": "Control systems &amp; software", "ctrl_h": 'At the heart of every technology is a <span class="hl">control system</span>.',
        "ctrl_btn": "Control systems", "ctrl_btn2": "Software &amp; visualisation",
        "ctrl_alt": "Switchboard with a SIMATIC control system",
        "ctrl_caption": "Switchboards, PLCs and operator workstations – designed, programmed and commissioned by us.",
        "svc_eyebrow": "Services", "svc_h": "The entire equipment life cycle under one roof.",
        "world_eyebrow": "International projects", "world_h": 'From Ostrava to <span class="hl">nine countries</span> in Europe.',
        "q_eyebrow": "Quality", "q_h": "Certified integrated management system", "q_badges_alt": "IQNet and CQS certification marks",
        "energo_eyebrow": "PROSPECT group", "energo_alt": "PROSPECT ENERGO logo",
        "crumb_home": "Home", "crumb_fields": "Fields", "crumbs_aria": "Breadcrumbs",
        "specs": "specialisations", "ref_actions": "reference projects", "toc": "On this page", "toc_aria": "Page contents",
        "inquiry": "Send an inquiry", "refs_eyebrow": "References", "refs_h": "Selected references – {}",
        "all_refs": "All references", "prev_field": "← Previous field", "next_field": "Next field →", "pager_aria": "Other fields",
        "actions": "projects", "photo": "photo",
        "svc_title": "Services", "refs_title": "References", "grants_title": "EU-funded projects",
        "listed": "listed projects", "fields_n": "fields", "countries_n": "countries",
        "search_label": "Search references", "search_ph": "Search – e.g. WWTP, Pilsner, Třinec, CHP…",
        "filter_aria": "Filter by field", "all": "All", "other_refs": "Other references",
        "empty": 'Nothing found. Try another term, or <a href="#kontakt">write to us</a>.',
        "grant_eu": "EU", "recipient": "Recipient", "corecipient": "Co-recipient", "duration": "Project period",
        "grant_pdf": "Project publicity (PDF, Czech)", "grant_alt": "Project publicity",
        "nf_title": "Page not found", "nf_lead": "The requested page does not exist or has been moved. Try one of our fields.",
        "nf_back": "Back to home",
        "hmi": {"title": "PUMPING STATION", "online": "PLC-01 · ONLINE", "app": "HMI · Water control centre",
                "well": "WELL W-1", "filter": "FILTER F-1", "res": "RES-1", "pump1": "P-101", "pump2": "P-102",
                "mode": "Mode", "auto": "Automatic", "run": "Run", "stby": "Standby",
                "trend": "TREND FT-201 · m³/h", "note": "Illustrative visualisation of a controlled process",
                "cap1": "(120 m³)", "cap2": "(450 m³)"},
    },
}

# Globální stav pro právě generovaný jazyk (nastavuje build_language)
DATA = F = L = None
LANG = "cs"
P = ""


def e(text):
    """Escapuje text pro bezpečné vložení do HTML."""
    return html.escape(str(text), quote=True)


def tel_href(num):
    return "tel:" + re.sub(r"[^\d+]", "", num)


def other_lang_href(filename):
    """Odkaz na stejnou stránku v druhém jazyce."""
    return f"en/{filename}" if LANG == "cs" else f"../{filename}"


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
    return (f'<img class="{cls}" src="{P}assets/img/foto/{foto_id}-sm.webp" '
            f'srcset="{P}assets/img/foto/{foto_id}-sm.webp 640w, {P}assets/img/foto/{foto_id}.webp 1200w" '
            f'sizes="{sizes}" alt="{e(alt)}" {load} decoding="async">')


def short(t, n):
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + "…"


# --------------------------------------------------------------------------
# Společné části: hlavička, menu, patička
# --------------------------------------------------------------------------
def header(active, filename):
    nav = L["nav"]
    items = [
        ("index.html", nav[0], "uvod"), ("index.html#obory", nav[1], "obory"),
        ("cinnosti.html", nav[2], "cinnosti"), ("reference.html", nav[3], "reference"),
        ("dotovane-projekty.html", nav[4], "dotace"), ("#kontakt", nav[5], "kontakt"),
    ]
    obory_menu = "".join(
        f'<li><a href="{o["id"]}.html">{icon(o["ikona"])}<span><strong>{e(o["nazev"])}</strong>'
        f'<small>{e(o["perex"])}</small></span></a></li>' for o in DATA["obory"])
    lis = []
    for href, label, key in items:
        cur = ' aria-current="page"' if key == active else ""
        if key == "obory":
            lis.append(
                f'<li class="has-mega"><button class="nav-link mega-toggle" aria-expanded="false" '
                f'aria-controls="mega">{label}{icon("chevron", "ico chev")}</button>'
                f'<div class="mega" id="mega"><ul>{obory_menu}</ul></div></li>')
        else:
            lis.append(f'<li><a class="nav-link" href="{href}"{cur}>{label}</a></li>')
    return f'''
<a class="skip" href="#obsah">{L["skip"]}</a>
<header class="site-header" data-header>
  <div class="wrap header-in">
    <a class="brand" href="index.html" aria-label="{e(F["nazev"])} – {L["home_aria"]}">
      <img src="{P}assets/img/logo-prospect.png" alt="PROSPECT" width="170" height="25">
      <span class="brand-tag">{e(F["slogan"])}</span>
    </a>
    <nav class="main-nav" aria-label="{L["nav_aria"]}" data-nav>
      <ul>{"".join(lis)}</ul>
      <div class="nav-extra">
        <a class="lang" href="{other_lang_href(filename)}" hreflang="{L["other_hreflang"]}" lang="{L["other_hreflang"]}" title="{L["other_lang_name"]}">{icon("globe")}{L["other_lang"]}</a>
        <a class="btn btn-sm btn-primary" href="{tel_href(F["telefony"][0])}">{icon("phone")}{e(F["telefony"][0])}</a>
      </div>
    </nav>
    <button class="burger" aria-label="{L["menu_open"]}" aria-expanded="false" data-burger><span></span><span></span><span></span></button>
  </div>
</header>'''


def footer(filename):
    tels = "".join(f'<a href="{tel_href(t)}">{e(t)}</a>' for t in F["telefony"])
    obory = "".join(f'<li><a href="{o["id"]}.html">{e(o["nazev"])}</a></li>' for o in DATA["obory"])
    cin = "".join(f'<li><a href="cinnosti.html#{c["id"]}">{e(c["nazev"])}</a></li>' for c in DATA["cinnosti"])
    return f'''
<section class="contact" id="kontakt" aria-labelledby="kontakt-h">
  <div class="wrap">
    <div class="contact-grid">
      <div class="contact-main reveal">
        <p class="eyebrow">{L["contact_eyebrow"]}</p>
        <h2 id="kontakt-h">{L["contact_h"]}</h2>
        <p class="lead">{L["contact_lead"]}</p>
        <div class="contact-cards">
          <a class="ccard" href="{tel_href(F["telefony"][0])}">{icon("phone")}<span><small>{L["phone"]}</small><strong>{e(F["telefony"][0])}</strong></span></a>
          <a class="ccard" href="mailto:{e(F["email"])}">{icon("mail")}<span><small>{L["email"]}</small><strong>{e(F["email"])}</strong></span></a>
          <a class="ccard" href="{e(F["mapa_odkaz"])}" target="_blank" rel="noopener">{icon("pin")}<span><small>{L["address"]}</small><strong>{e(F["ulice"])}, {e(F["mesto"])}</strong></span></a>
        </div>
      </div>
      <div class="contact-details reveal">
        <dl class="details">
          <div><dt>{L["company"]}</dt><dd><strong>{e(F["nazev"])}</strong><br>{e(F["ulice"])}<br>{e(F["mesto"])}<br>{L["postcode"]}: {e(F["psc"])}</dd></div>
          <div><dt>{L["ident"]}</dt><dd>{L["ic"]}: {e(F["ic"])}<br>{L["dic"]}: {e(F["dic"])}</dd></div>
          <div><dt>{L["phone"]}</dt><dd class="stack">{tels}<span>{L["fax"]}: {e(F["fax"])}</span></dd></div>
          <div><dt>{L["where"]}</dt><dd>{e(F["kancelar"])}</dd></div>
        </dl>
        <div class="map">
          <iframe title="{L["map"]} – {e(F["nazev"])}" src="{e(F["mapa_embed"])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        </div>
      </div>
    </div>
  </div>
</section>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <img src="{P}assets/img/logo-prospect-white.png" alt="PROSPECT" width="157" height="24" loading="lazy">
      <p class="muted">{e(F["slogan"]).capitalize()}. {L["footer_about"]}</p>
      <p class="muted small">{e(F["rejstrik"])}</p>
    </div>
    <nav aria-label="{L["f_fields"]}"><h3>{L["f_fields"]}</h3><ul>{obory}</ul></nav>
    <nav aria-label="{L["f_services"]}"><h3>{L["f_services"]}</h3><ul>{cin}</ul></nav>
    <nav aria-label="{L["f_company"]}"><h3>{L["f_company"]}</h3><ul>
      <li><a href="reference.html">{L["f_refs"]}</a></li>
      <li><a href="dotovane-projekty.html">{L["f_grants"]}</a></li>
      <li><a href="index.html#kvalita">{L["f_cert"]}</a></li>
      <li><a href="{e(DATA["uvod"]["energo_web"])}" target="_blank" rel="noopener">PROSPECT ENERGO a.s.</a></li>
      <li><a href="{other_lang_href(filename)}" hreflang="{L["other_hreflang"]}" lang="{L["other_hreflang"]}">{L["f_other"]}</a></li>
    </ul></nav>
  </div>
  <div class="wrap footer-bottom">
    <span>© <span data-year>{date.today().year}</span> {e(F["nazev"])}</span>
    <a href="#top" class="to-top">{L["to_top"]}</a>
  </div>
</footer>
<div class="lightbox" data-lightbox hidden>
  <button class="lb-close" aria-label="{L["lb_close"]}">×</button>
  <button class="lb-prev" aria-label="{L["lb_prev"]}">‹</button>
  <figure><img alt=""><figcaption></figcaption></figure>
  <button class="lb-next" aria-label="{L["lb_next"]}">›</button>
</div>'''


def page(filename, title, description, active, body, body_class=""):
    full_title = title if "PROSPECT" in title else f"{title} | {F['nazev']}"
    base = F["web"].rstrip("/") + "/"
    page_path = "" if filename == "index.html" else filename
    url_cs, url_en = base + page_path, base + "en/" + page_path
    canonical = url_cs if LANG == "cs" else url_en
    doc = f'''<!DOCTYPE html>
<html lang="{L["html_lang"]}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(description)}">
<meta name="author" content="{e(F["nazev"])}">
<meta name="theme-color" content="#0069aa">
<link rel="canonical" href="{e(canonical)}">
<link rel="alternate" hreflang="cs" href="{e(url_cs)}">
<link rel="alternate" hreflang="en" href="{e(url_en)}">
<link rel="alternate" hreflang="x-default" href="{e(url_cs)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:image" content="{e(base)}assets/img/og-image.jpg">
<meta property="og:locale" content="{L["og_locale"]}">
<link rel="icon" type="image/png" href="{P}assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap&subset=latin-ext" rel="stylesheet">
<link rel="stylesheet" href="{P}assets/css/style.css?v={VERSION}">
<script src="{P}assets/js/main.js?v={VERSION}" defer></script>
</head>
<body class="{body_class}" id="top">
{header(active, filename)}
<main id="obsah">
{body}
</main>
{footer(filename)}
</body>
</html>
'''
    out = LANGS[LANG]["out"]
    out.mkdir(exist_ok=True)
    (out / filename).write_text(doc, encoding="utf-8")
    return filename


# --------------------------------------------------------------------------
# HMI panel v úvodu – styl klasické SCADA vizualizace (tyrkysové pozadí,
# šedé nádrže, bílé potrubí, zelené motory „M“, ventily, bílé displeje hodnot).
# Hodnoty s atributem data-val a hladinu (data-level-rect) animuje main.js.
# --------------------------------------------------------------------------
def motor(x, y, on=True, cls=""):
    fill = "#22c55e" if on else "#9aa5a8"
    return (f'<g class="m-motor {cls}" transform="translate({x} {y})"><circle r="11" fill="{fill}" stroke="#123" stroke-width="1.2"/>'
            f'<text y="4" text-anchor="middle" class="m-letter">M</text></g>')


def valve(x, y, on=True, vertical=False):
    fill = "#22c55e" if on else "#9aa5a8"
    rot = ' rotate(90)' if vertical else ''
    return (f'<g transform="translate({x} {y}){rot}"><path d="M-10 -7 L0 0 L-10 7 Z M10 -7 L0 0 L10 7 Z" fill="{fill}" stroke="#123" stroke-width="1"/>'
            f'<path d="M0 0 V-12 M-5 -12 H5" stroke="#123" stroke-width="1.4"/></g>')


def display(x, y, w, key, value, unit):
    return (f'<g transform="translate({x} {y})"><rect width="{w}" height="18" class="s-disp"/>'
            f'<text x="{w - 5}" y="13.5" text-anchor="end" class="s-val" data-val="{key}">{value}</text>'
            f'<text x="{w + 5}" y="13.5" class="s-unit">{unit}</text></g>')


def instrument(x, y, tag):
    return (f'<g transform="translate({x} {y})"><circle r="11" class="s-inst"/>'
            f'<text y="3.5" text-anchor="middle" class="s-inst-t">{tag}</text></g>')


def tank(x, y, w, h, label, cap, idtag, show_name=True):
    """Šedá válcová nádrž s kopulí, štítkem a kuželovým dnem."""
    return f'''
    <g class="s-tank">
      <path d="M{x} {y + 12} Q{x + w / 2} {y - 10} {x + w} {y + 12} V{y + h} L{x + w / 2 + 10} {y + h + 22} H{x + w / 2 - 10} L{x} {y + h} Z" fill="url(#gSteel)" stroke="#2b3338" stroke-width="1.2"/>
      <rect x="{x + 2}" y="{y + 16}" width="{w - 4}" height="14" fill="#fff" stroke="#2b3338" stroke-width=".8"/>
      <text x="{x + w / 2}" y="{y + 27}" text-anchor="middle" class="s-id">{idtag}</text>
      {f'<text x="{x + w / 2 - 6}" y="{y + h / 2 + 18}" text-anchor="middle" class="s-name">{label}</text>' if show_name else ""}
      <text x="{x + w / 2}" y="{y + h / 2 + 30}" text-anchor="middle" class="s-cap">{cap if show_name else ""}</text>
      <circle cx="{x + w / 2}" cy="{y + 44}" r="4" fill="none" stroke="#2b3338"/>
    </g>'''


def hmi_panel():
    H = L["hmi"]
    return f'''
<div class="hmi" aria-hidden="true">
  <div class="hmi-bar">
    <span class="hmi-dot"></span><span>{H["online"]}</span>
    <span class="hmi-title">{H["app"]}</span>
    <span class="hmi-clock" data-clock>--:--:--</span>
  </div>
  <div class="hmi-screen">
  <svg class="hmi-svg" viewBox="0 0 640 360">
    <defs>
      <linearGradient id="gSteel" x1="0" x2="1"><stop offset="0" stop-color="#6f7a80"/><stop offset=".35" stop-color="#b9c1c5"/><stop offset=".6" stop-color="#9aa4a9"/><stop offset="1" stop-color="#5e686d"/></linearGradient>
      <linearGradient id="gWater" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4fb3ff"/><stop offset="1" stop-color="#1565c0"/></linearGradient>
      <clipPath id="cRes"><rect x="481" y="104" width="118" height="146"/></clipPath>
    </defs>
    <rect width="640" height="360" class="s-bg"/>
    <text x="320" y="30" text-anchor="middle" class="s-title">{H["title"]}</text>

    <!-- signálové vedení z PLC (zelená tečkovaná) -->
    <g class="s-sig">
      <path d="M232 66 H330 V258"/><path d="M232 74 H440 V68"/><path d="M232 58 H612 V60"/>
    </g>
    <g transform="translate(160 50)"><rect width="72" height="32" class="s-btn"/><text x="36" y="20" text-anchor="middle" class="s-btn-t">PLC-01</text><circle cx="64" cy="8" r="3.5" fill="#22c55e"/></g>

    <!-- potrubí -->
    <g class="s-pipe">
      <path d="M85 262 V300 H360 V262"/>
      <path d="M390 170 V90 H480"/>
      <path d="M540 272 V320 H640"/>
      <path d="M20 90 H40"/>
    </g>
    <g class="s-flow">
      <path d="M85 262 V300 H360 V262"/>
      <path d="M390 170 V90 H480"/>
      <path d="M540 272 V320 H640"/>
    </g>

    <!-- zdroj (vrt) -->
    {tank(40, 70, 90, 170, H["well"], H["cap1"], "1001")}
    <rect x="116" y="160" width="10" height="76" fill="#1d2a30"/>
    <rect x="117" y="190" width="8" height="45" fill="url(#gWater)"/>

    <!-- čerpadla -->
    <g transform="translate(190 300)">
      <circle r="15" fill="url(#gSteel)" stroke="#2b3338"/>
      <g class="impeller"><path d="M0-10 L3-2 L0 0 Z M10 0 L2 3 L0 0 Z M0 10 L-3 2 L0 0 Z M-10 0 L-2-3 L0 0 Z" fill="#123"/></g>
      <path d="M0 -15 V-26" stroke="#2b3338" stroke-width="3"/>
    </g>
    {motor(190, 262, True)}
    <text x="190" y="338" text-anchor="middle" class="s-lbl">{H["pump1"]}</text>
    <rect x="170" y="342" width="40" height="13" class="s-state on"/><text x="190" y="352" text-anchor="middle" class="s-state-t">{H["run"]}</text>

    <g transform="translate(270 300)">
      <circle r="15" fill="url(#gSteel)" stroke="#2b3338"/>
      <path d="M0 -15 V-26" stroke="#2b3338" stroke-width="3"/>
    </g>
    {motor(270, 262, False)}
    <text x="270" y="338" text-anchor="middle" class="s-lbl">{H["pump2"]}</text>
    <rect x="250" y="342" width="40" height="13" class="s-state"/><text x="270" y="352" text-anchor="middle" class="s-state-t">{H["stby"]}</text>
    {valve(130, 300, True)}{valve(230, 300, True)}{valve(310, 300, False)}

    <!-- filtr -->
    <g>
      <path d="M362 176 Q390 158 418 176 V236 L404 262 H376 L362 236 Z" fill="url(#gSteel)" stroke="#2b3338" stroke-width="1.2"/>
      <rect x="364" y="188" width="52" height="13" fill="#fff" stroke="#2b3338" stroke-width=".8"/>
      <text x="390" y="198" text-anchor="middle" class="s-id">F-1</text>
      <text x="390" y="224" text-anchor="middle" class="s-name small">{H["filter"]}</text>
    </g>
    {instrument(330, 270, "PT")}
    {display(290, 214, 46, "pressure", "4.20", "bar")}

    {valve(440, 90, True)}
    {instrument(440, 56, "FT")}
    {display(455, 36, 56, "flow", "128.4", "m³/h")}

    <!-- vodojem -->
    {tank(480, 80, 120, 170, H["res"], H["cap2"], "1002", show_name=False)}
    <g clip-path="url(#cRes)" opacity=".85"><rect x="481" y="160" width="118" height="90" fill="url(#gWater)" data-level-rect data-bottom="250" data-height="146"/></g>
    <text x="540" y="196" text-anchor="middle" class="s-name">{H["res"]}</text>
    <text x="540" y="208" text-anchor="middle" class="s-cap">{H["cap2"]}</text>
    {instrument(612, 70, "LT")}
    {display(560, 270, 46, "level", "72.0", "%")}
    {motor(600, 320, True)}{valve(570, 320, True)}

    <!-- režim -->
    <g transform="translate(20 22)"><text class="s-lbl dark" y="0">{H["mode"]}</text>
      <rect y="6" width="78" height="22" class="s-btn"/><text x="39" y="21" text-anchor="middle" class="s-btn-t">{H["auto"]}</text></g>
    <circle cx="150" cy="262" r="5" class="s-lamp"/><circle cx="510" cy="68" r="5" class="s-lamp"/><circle cx="440" cy="125" r="5" class="s-lamp"/>
  </svg>
  <canvas class="hmi-trend" data-trend data-label="{e(H["trend"])}" height="70"></canvas>
  </div>
  <p class="hmi-note">{H["note"]}</p>
</div>'''


# --------------------------------------------------------------------------
# Úvodní stránka
# --------------------------------------------------------------------------
def hero_title(t):
    # zvýrazní úvodní slova nadpisu (CZ „Řídicí systémy“, EN „Control systems“)
    for word in ("Řídicí systémy", "Control systems"):
        if word in t:
            return e(t).replace(word, f'<span class="hl">{word}</span>', 1)
    return e(t)


def build_index():
    U = DATA["uvod"]
    stats = "".join(
        f'<div class="stat reveal"><strong data-count="{s["hodnota"]}" data-suffix="{e(s["pripona"])}">'
        f'{s["hodnota"]}{e(s["pripona"])}</strong><span>{e(s["popis"])}</span></div>' for s in U["cisla"])
    klienti = "".join(f"<li>{e(k)}</li>" for k in U["klienti"])
    o_nas = "".join(f"<p>{e(p)}</p>" for p in U["o_nas"][:2])
    filozofie = e(U["o_nas"][2])
    dodavky = "".join(f"<p>{e(p)}</p>" for p in U["dodavky_text"])
    q_open, q_close = ("„", "“") if LANG == "cs" else ("“", "”")

    cards = []
    for i, o in enumerate(DATA["obory"]):
        subs = "".join(f'<li><a href="{o["id"]}.html#{s["id"]}">{e(s["nazev"])}</a></li>' for s in o["sekce"])
        subs = subs or f'<li><a href="{o["id"]}.html#reference">{L["selected_refs"]}</a></li>'
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
          <span class="more">{L["field_more"]} {icon("arrow")}</span>
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
        f'<a class="cert reveal" href="{P}{e(c["soubor"])}" target="_blank" rel="noopener">{icon("doc")}'
        f'<span><strong>{e(c["nazev"])}</strong><small>{e(c["popis"])}</small></span>{icon("external", "ico ext")}</a>'
        for c in U["certifikaty"])
    tags = "".join(f"<li>{t}</li>" for t in L["hero_tags"])

    body = f'''
<section class="hero">
  <div class="hero-bg" aria-hidden="true"><div class="glow g1"></div><div class="glow g2"></div><div class="grid-bg"></div></div>
  <div class="wrap hero-in">
    <div class="hero-text">
      <p class="eyebrow pulse">{e(U["hero_stitek"])}</p>
      <h1>{hero_title(U["hero_nadpis"])}</h1>
      <p class="lead">{e(U["hero_text"])}</p>
      <div class="hero-cta">
        <a class="btn btn-primary" href="#obory">{L["cta_fields"]} {icon("arrow")}</a>
        <a class="btn btn-ghost" href="reference.html">{L["cta_refs"]}</a>
      </div>
      <ul class="hero-tags">{tags}</ul>
    </div>
    {hmi_panel()}
  </div>
</section>

<section class="stats" aria-label="{L["stats_aria"]}">
  <div class="wrap stats-in">{stats}</div>
</section>

<section class="marquee" aria-label="{L["clients_aria"]}">
  <p class="marquee-label">{L["clients_label"]}</p>
  <div class="marquee-track"><ul>{klienti}</ul><ul aria-hidden="true">{klienti}</ul></div>
</section>

<section class="section about" id="o-nas">
  <div class="wrap about-grid">
    <div class="reveal">
      <p class="eyebrow">{L["about_eyebrow"]}</p>
      <h2>{L["about_h"]}</h2>
      {o_nas}
    </div>
    <div class="about-side reveal">
      <blockquote class="quote"><p>{q_open}{filozofie}{q_close}</p></blockquote>
      <div class="about-domains">
        <p>{e(U["obory_text"])}</p>
        <ul>{"".join(f'<li><a href="{o["id"]}.html">{icon(o["ikona"])}{e(o["nazev"])}</a></li>' for o in DATA["obory"])}</ul>
      </div>
    </div>
  </div>
  <div class="strip reveal" role="img" aria-label="{L["strip_aria"]}"><img src="{P}assets/img/pas-realizaci.webp" alt="" loading="lazy" width="2000" height="430"></div>
</section>

<section class="section" id="obory">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">{L["fields_eyebrow"]}</p>
      <h2>{L["fields_h"]}</h2>
      <p class="lead">{L["fields_lead"]}</p>
    </div>
    <div class="obory-grid">{"".join(cards)}</div>
  </div>
</section>

<section class="section control" id="ridici-systemy">
  <div class="wrap">
    <div class="control-grid">
      <div class="reveal">
        <p class="eyebrow">{L["ctrl_eyebrow"]}</p>
        <h2>{L["ctrl_h"]}</h2>
        <p class="lead">{e(ridici["odstavce"][0])}</p>
        <p>{e(software["odstavce"][2])}</p>
        <p>{e(ridici["odstavce"][2])}</p>
        <div class="btn-row">
          <a class="btn btn-primary" href="srtp-a-elektro.html#ridici-systemy">{L["ctrl_btn"]} {icon("arrow")}</a>
          <a class="btn btn-ghost" href="cinnosti.html#software">{L["ctrl_btn2"]}</a>
        </div>
      </div>
      <figure class="control-photo reveal">
        {img("ridici-systemy-4", L["ctrl_alt"], "", "(max-width: 900px) 100vw, 40vw")}
        <figcaption><span class="hmi-dot"></span>{L["ctrl_caption"]}</figcaption>
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
      <p class="eyebrow">{L["svc_eyebrow"]}</p>
      <h2>{L["svc_h"]}</h2>
      <p class="lead">{e(DATA["cinnosti_uvod"])}</p>
    </div>
    <ol class="steps">{steps}</ol>
    <div class="deliver reveal">{dodavky}</div>
  </div>
</section>

<section class="section world" id="zahranici">
  <div class="wrap world-grid">
    <div class="reveal">
      <p class="eyebrow">{L["world_eyebrow"]}</p>
      <h2>{L["world_h"]}</h2>
      <p class="lead">{e(U["zahranici_text"])}</p>
      <p class="muted">{e(U["prostredky_text"])}</p>
    </div>
    <ul class="countries reveal">{zeme}</ul>
  </div>
</section>

<section class="section quality" id="kvalita">
  <div class="wrap quality-grid">
    <div class="reveal">
      <p class="eyebrow">{L["q_eyebrow"]}</p>
      <h2>{L["q_h"]}</h2>
      <p>{e(U["ism_text"])}</p>
      <img class="badges" src="{P}assets/img/certifikace.png" alt="{L["q_badges_alt"]}" width="122" height="43" loading="lazy">
    </div>
    <div class="certs">{certs}</div>
  </div>
</section>

<section class="section energo">
  <div class="wrap">
    <a class="energo-card reveal" href="{e(U["energo_web"])}" target="_blank" rel="noopener">
      <div>
        <p class="eyebrow">{L["energo_eyebrow"]}</p>
        <h2>PROSPECT ENERGO a.s.</h2>
        <p>{e(U["energo_text"])}</p>
        <span class="more">prospect-energo.cz {icon("external")}</span>
      </div>
      <img src="{P}assets/img/prospect-energo.webp" alt="{L["energo_alt"]}" loading="lazy" width="1000" height="230">
    </a>
  </div>
</section>
'''
    page("index.html", DATA["seo"]["titulek"], DATA["seo"]["popis"], "uvod", body, "home")


# --------------------------------------------------------------------------
# Stránky oborů
# --------------------------------------------------------------------------
def gallery(fotos, title):
    if not fotos:
        return ""
    return '<div class="gallery">' + "".join(
        f'<a href="{P}assets/img/foto/{f}.webp" data-lb="{e(title)}" class="g-item">'
        f'{img(f, f"{title} – {L["photo"]} {i + 1}", "", "(max-width: 700px) 50vw, 25vw")}</a>'
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
            f'<header><h3>{e(r["nazev"])}</h3><span class="badge">{count} {L["actions"]}</span></header>'
            f'{uvod}<div class="ref-groups">{"".join(groups)}</div></article>')


def crumbs(*parts):
    links = [f'<a href="index.html">{L["crumb_home"]}</a>']
    for href, label in parts[:-1]:
        links.append(f'<a href="{href}">{label}</a>')
    links.append(f'<span aria-current="page">{parts[-1][1]}</span>')
    return f'<nav class="crumbs" aria-label="{L["crumbs_aria"]}">' + "<span>/</span>".join(links) + "</nav>"


def build_obor(o, idx):
    obory = DATA["obory"]
    prev_o, next_o = obory[idx - 1], obory[(idx + 1) % len(obory)]
    toc = "".join(f'<li><a href="#{s["id"]}">{e(s["nazev"])}</a></li>' for s in o["sekce"])
    toc += f'<li><a href="#reference">{L["selected_refs"]}</a></li>'
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
    {crumbs(("index.html#obory", L["crumb_fields"]), (None, e(o["nazev"])))}
    <span class="page-ico">{icon(o["ikona"])}</span>
    <h1>{e(o["nazev"])}</h1>
    <p class="lead">{e(o["perex"])}</p>
    <div class="hero-meta"><span><strong>{len(o["sekce"]) or "—"}</strong> {L["specs"]}</span><span><strong>{total}</strong> {L["ref_actions"]}</span></div>
  </div>
</section>
<div class="wrap page-layout">
  <aside class="toc" aria-label="{L["toc_aria"]}"><p>{L["toc"]}</p><ul data-scrollspy>{toc}</ul>
    <a class="btn btn-primary btn-sm" href="#kontakt">{L["inquiry"]} {icon("arrow")}</a></aside>
  <div class="page-content">
    <div class="intro reveal">{"".join(f'<p class="lead">{e(p)}</p>' for p in o["uvod"])}</div>
    {sections}
    <section class="refs" id="reference">
      <div class="section-head reveal"><p class="eyebrow">{L["refs_eyebrow"]}</p><h2>{L["refs_h"].format(e(o["nazev"]))}</h2></div>
      {refs}
      <a class="btn btn-ghost" href="reference.html?obor={o["id"]}">{L["all_refs"]} {icon("arrow")}</a>
    </section>
    <nav class="pager" aria-label="{L["pager_aria"]}">
      <a href="{prev_o["id"]}.html"><small>{L["prev_field"]}</small><strong>{e(prev_o["nazev"])}</strong></a>
      <a href="{next_o["id"]}.html" class="next"><small>{L["next_field"]}</small><strong>{e(next_o["nazev"])}</strong></a>
    </nav>
  </div>
</div>'''
    page(f'{o["id"]}.html', o["nazev"], short(" ".join(o["uvod"]), 155), "obory", body)


# --------------------------------------------------------------------------
# Činnosti
# --------------------------------------------------------------------------
def build_cinnosti():
    chips = "".join(f'<li><a href="#{c["id"]}">{icon(c["id"])}{e(c["nazev"])}</a></li>' for c in DATA["cinnosti"])
    secs = []
    for i, c in enumerate(DATA["cinnosti"]):
        secs.append(f'''
  <section class="activity reveal {'alt' if i % 2 else ''}" id="{c["id"]}">
    <div class="activity-text">
      <span class="step-n">{i + 1:02d}</span>
      <h2>{icon(c["id"])}{e(c["nazev"])}</h2>
      {"".join(f"<p>{e(p)}</p>" for p in c["odstavce"])}
    </div>
    <div class="activity-media">{gallery(c["foto"], c["nazev"])}</div>
  </section>''')
    body = f'''
<section class="page-hero slim">
  <div class="wrap">
    {crumbs((None, L["svc_title"]))}
    <h1>{L["svc_title"]}</h1>
    <p class="lead">{e(DATA["cinnosti_uvod"])}</p>
    <ul class="chips">{chips}</ul>
  </div>
</section>
<div class="wrap activities">{"".join(secs)}</div>'''
    page("cinnosti.html", L["svc_title"], DATA["cinnosti_uvod"], "cinnosti", body)


# --------------------------------------------------------------------------
# Reference (s vyhledáváním a filtrem)
# --------------------------------------------------------------------------
def build_reference():
    filters = [f'<button class="chip is-active" data-filter="vse">{L["all"]}</button>'] + [
        f'<button class="chip" data-filter="{o["id"]}">{icon(o["ikona"])}{e(o["nazev"])}</button>' for o in DATA["obory"]
    ] + [f'<button class="chip" data-filter="dalsi">{L["other_refs"]}</button>']
    blocks = []
    for o in DATA["obory"]:
        blocks.append(f'<h2 class="ref-obor" data-obor="{o["id"]}"><a href="{o["id"]}.html">{icon(o["ikona"])}{e(o["nazev"])}</a></h2>')
        blocks += [ref_block(r, o["id"]) for r in o["reference"]]
    blocks.append(f'<h2 class="ref-obor" data-obor="dalsi">{e(DATA["dalsi_reference"]["nazev"])}</h2>')
    blocks.append(ref_block(DATA["dalsi_reference"], "dalsi"))
    total = sum(len(g["polozky"]) for o in DATA["obory"] for r in o["reference"] for g in r["skupiny"])
    total += sum(len(g["polozky"]) for g in DATA["dalsi_reference"]["skupiny"])
    body = f'''
<section class="page-hero slim">
  <div class="wrap">
    {crumbs((None, L["refs_title"]))}
    <h1>{L["refs_title"]}</h1>
    <p class="lead">{e(DATA["reference_uvod"])}</p>
    <div class="hero-meta"><span><strong data-count="{total}">{total}</strong> {L["listed"]}</span><span><strong>5</strong> {L["fields_n"]}</span><span><strong>9</strong> {L["countries_n"]}</span></div>
  </div>
</section>
<div class="wrap ref-page" data-refs>
  <div class="ref-tools">
    <label class="search">{icon("search")}<span class="sr">{L["search_label"]}</span>
      <input type="search" placeholder="{e(L["search_ph"])}" data-ref-search></label>
    <div class="chips" role="group" aria-label="{L["filter_aria"]}">{"".join(filters)}</div>
    <p class="ref-count" aria-live="polite" data-ref-count></p>
  </div>
  <div class="ref-results">{"".join(blocks)}</div>
  <p class="empty" data-ref-empty hidden>{L["empty"]}</p>
</div>'''
    page("reference.html", L["refs_title"], DATA["reference_uvod"], "reference", body)


# --------------------------------------------------------------------------
# Dotované projekty
# --------------------------------------------------------------------------
def build_dotace():
    D = DATA["dotace"]
    cards = "".join(f'''
  <article class="grant reveal">
    <a class="grant-img" href="{P}{e(p["soubor"])}" target="_blank" rel="noopener"><img src="{P}{e(p["nahled"])}" alt="{L["grant_alt"]} – {e(p["nazev"])}" loading="lazy"></a>
    <div>
      <p class="eyebrow">{e(p["poskytovatel"])} · {L["grant_eu"]}</p>
      <h2>{e(p["nazev"])}</h2>
      <p class="mono">{e(p["kod"])}</p>
      <p>{e(p["popis"])}</p>
      <p><strong>{e(p["financovani"])}</strong></p>
      <dl class="grant-meta">
        <div><dt>{L["recipient"]}</dt><dd>{e(p["prijemce"])}</dd></div>
        <div><dt>{L["corecipient"]}</dt><dd>{e(p["spoluprijemce"])}</dd></div>
        <div><dt>{L["duration"]}</dt><dd>{e(p["doba"])}</dd></div>
      </dl>
      <a class="btn btn-ghost" href="{P}{e(p["soubor"])}" target="_blank" rel="noopener">{icon("doc")}{L["grant_pdf"]}</a>
    </div>
  </article>''' for p in D["projekty"])
    body = f'''
<section class="page-hero slim">
  <div class="wrap">
    {crumbs((None, L["grants_title"]))}
    <h1>{L["grants_title"]}</h1>
    <p class="lead">{e(D["uvod"])}</p>
  </div>
</section>
<div class="wrap grants">{cards}</div>'''
    page("dotovane-projekty.html", L["grants_title"], D["uvod"], "dotace", body)


def build_404():
    body = f'''
<section class="page-hero slim notfound">
  <div class="wrap">
    <p class="mono err">ERR 404 · SIGNAL LOST</p>
    <h1>{L["nf_title"]}</h1>
    <p class="lead">{L["nf_lead"]}</p>
    <ul class="chips">{"".join(f'<li><a href="{o["id"]}.html">{icon(o["ikona"])}{e(o["nazev"])}</a></li>' for o in DATA["obory"])}</ul>
    <p><a class="btn btn-primary" href="index.html">{L["nf_back"]} {icon("arrow")}</a></p>
  </div>
</section>'''
    page("404.html", L["nf_title"], L["nf_title"], "", body)


# --------------------------------------------------------------------------
# Sitemap, robots, .htaccess
# --------------------------------------------------------------------------
def build_sitemap(files):
    base = F["web"].rstrip("/")
    urls = ""
    for d in ("", "en/"):
        for f in files:
            urls += f"<url><loc>{base}/{d}{'' if f == 'index.html' else f}</loc><lastmod>{date.today().isoformat()}</lastmod></url>"
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


def build_htaccess(cs_data):
    redirects = dict(REDIRECTS)
    for o in cs_data["obory"]:
        for s in o["sekce"]:
            redirects.setdefault(s["id"], f'{o["id"]}.html#{s["id"]}')
    lines = ["# Vygenerováno skriptem build.py – neupravujte ručně, změny dělejte v REDIRECTS v build.py",
             "ErrorDocument 404 /404.html", "DirectoryIndex index.html", "RewriteEngine On", ""]
    for old, new in redirects.items():
        lines.append(f"RewriteRule ^{re.escape(old)}/?$ /{new} [R=301,L,NE]")
    lines += ["", "<IfModule mod_expires.c>", "  ExpiresActive On",
              '  ExpiresByType image/webp "access plus 1 year"', '  ExpiresByType text/css "access plus 1 month"',
              '  ExpiresByType application/javascript "access plus 1 month"', "</IfModule>", ""]
    (ROOT / ".htaccess").write_text("\n".join(lines), encoding="utf-8")


# --------------------------------------------------------------------------
def build_language(lang):
    global DATA, F, L, LANG, P
    LANG = lang
    DATA = json.loads((ROOT / LANGS[lang]["data"]).read_text(encoding="utf-8"))
    F, L, P = DATA["firma"], T[lang], LANGS[lang]["P"]
    build_index()
    for i, o in enumerate(DATA["obory"]):
        build_obor(o, i)
    build_cinnosti()
    build_reference()
    build_dotace()
    if lang == "cs":
        build_404()  # jedna stránka 404 pro celý web
    return DATA


if __name__ == "__main__":
    cs = build_language("cs")
    build_language("en")
    LANG, F = "cs", cs["firma"]
    pages = ["index.html"] + [f'{o["id"]}.html' for o in cs["obory"]] + \
            ["cinnosti.html", "reference.html", "dotovane-projekty.html"]
    build_sitemap(pages)
    build_htaccess(cs)
    print("Hotovo – čeština:", len(pages) + 1, "stránek, angličtina (en/):", len(pages),
          "stránek + sitemap.xml, robots.txt, .htaccess")
