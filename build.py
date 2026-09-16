#!/usr/bin/env python3
"""Build deportationdefenselaw.com from content/*.md into dist/.

Usage: python3 build.py
Add an article: drop a .md file in content/es/ (and its mirror in content/en/)
with front matter: title, description, slug, date, updated, mirror (slug of the
other-language page), summary (list), sources (list), order (nav order, optional).
"""
import os, re, shutil, json, datetime, html
import markdown

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content")
DIST = os.path.join(ROOT, "dist")
SITE = "https://deportationdefenselaw.com"
AUTHOR = "Hassan Benmouloud"
PHONE = os.environ.get("DDL_PHONE", "")        # e.g. "+1 713 555 0100" (empty = hidden)
WHATSAPP = os.environ.get("DDL_WHATSAPP", "")  # e.g. "17135550100" (digits, empty = hidden)
EMAIL = "contact@deportationdefenselaw.com"

UI = {
    "es": dict(lang="es", dir="/", other="en", other_label="English", nav_home="Inicio",
               about="Sobre este sitio", contact="Hablar con un abogado", legal="Aviso legal",
               essentials="Lo esencial", sources="Fuentes", updated="Última revisión",
               by="Escrito por", read_more="Guías", cta_title="¿Necesita un abogado ahora?",
               cta_text="Le conectamos con abogados de inmigración con licencia que atienden en español. Este sitio no es un bufete.",
               cta_btn="Hablar con un abogado", call="Llamar", wa="WhatsApp",
               disclaimer="Este sitio es un recurso informativo. No es un bufete de abogados, no somos abogados ni notarios y no damos asesoría legal. Le conectamos con abogados con licencia en Estados Unidos.",
               footer_nav="Guías", skip="Ir al contenido", not_found="Página no encontrada",
               not_found_text="La página que busca no existe. Vuelva al inicio o use una de las guías."),
    "en": dict(lang="en", dir="/en/", other="es", other_label="Español", nav_home="Home",
               about="About this site", contact="Talk to a lawyer", legal="Legal notice",
               essentials="The essentials", sources="Sources", updated="Last reviewed",
               by="Written by", read_more="Guides", cta_title="Need a lawyer now?",
               cta_text="We connect you with licensed immigration lawyers. This site is not a law firm.",
               cta_btn="Talk to a lawyer", call="Call", wa="WhatsApp",
               disclaimer="This site is an informational resource. It is not a law firm, we are not lawyers or notarios, and nothing here is legal advice. We connect you with licensed U.S. attorneys.",
               footer_nav="Guides", skip="Skip to content", not_found="Page not found",
               not_found_text="That page does not exist. Go back home or open one of the guides."),
}

def parse(path):
    raw = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    meta, body = {}, raw
    if m:
        body = m.group(2)
        key = None
        for line in m.group(1).splitlines():
            if re.match(r"^\s+- ", line) and key:
                meta.setdefault(key, []).append(line.strip()[2:].strip())
            elif ":" in line:
                key, _, val = line.partition(":")
                key = key.strip(); val = val.strip()
                meta[key] = val if val else []
    return meta, body

def md(text):
    return markdown.markdown(text, extensions=["extra", "sane_lists", "toc"], output_format="html5")

def esc(s): return html.escape(s, quote=True)

def url_for(lang, slug):
    base = UI[lang]["dir"]
    return base if slug == "index" else f"{base}{slug}/"

def load_lang(lang):
    pages = []
    for fn in sorted(os.listdir(os.path.join(CONTENT, lang))):
        if fn.endswith(".md"):
            meta, body = parse(os.path.join(CONTENT, lang, fn))
            meta["slug"] = meta.get("slug") or fn[:-3]
            meta["lang"] = lang
            meta["body"] = body
            meta["url"] = url_for(lang, meta["slug"])
            pages.append(meta)
    return pages

def guides(pages):
    g = [p for p in pages if p.get("type", "guide") == "guide" and p["slug"] != "index"]
    return sorted(g, key=lambda p: int(p.get("order", 99)))

def contact_buttons(ui, big=False):
    out = []
    cls = "btn btn-primary" if big else "btn btn-primary"
    out.append(f'<a class="{cls}" href="{ui["dir"]}{"contacto" if ui["lang"]=="es" else "contact"}/">{ui["cta_btn"]}</a>')
    if PHONE:
        out.append(f'<a class="btn btn-ghost" href="tel:{re.sub(r"[^0-9+]", "", PHONE)}">{ui["call"]} {esc(PHONE)}</a>')
    if WHATSAPP:
        out.append(f'<a class="btn btn-ghost" href="https://wa.me/{WHATSAPP}" rel="noopener">{ui["wa"]}</a>')
    return "\n".join(out)

def layout(page, pages, all_pages):
    lang = page["lang"]; ui = UI[lang]
    other = UI[ui["other"]]
    mirror = page.get("mirror") or page["slug"]
    mirror_url = url_for(ui["other"], mirror)
    canonical = SITE + page["url"]
    title = page["title"]
    desc = page.get("description", "")
    is_index = page["slug"] == "index"
    updated = page.get("updated") or page.get("date") or datetime.date.today().isoformat()
    date = page.get("date") or updated

    nav_guides = "".join(f'<li><a href="{p["url"]}"{" aria-current=\"page\"" if p["slug"]==page["slug"] else ""}>{esc(p.get("nav") or p["title"])}</a></li>' for p in guides(pages))

    # JSON-LD
    ld = [{
        "@context": "https://schema.org", "@type": "WebSite", "name": "Deportation Defense Law",
        "url": SITE, "inLanguage": ["es", "en"],
        "publisher": {"@type": "Organization", "name": "Deportation Defense Law", "url": SITE}
    }]
    if not is_index and page.get("type", "guide") == "guide":
        ld.append({
            "@context": "https://schema.org", "@type": "Article", "headline": title,
            "description": desc, "inLanguage": lang, "url": canonical,
            "datePublished": date, "dateModified": updated,
            "author": {"@type": "Person", "name": AUTHOR, "url": SITE + ("/sobre/" if lang=="es" else "/en/about/")},
            "publisher": {"@type": "Organization", "name": "Deportation Defense Law", "url": SITE},
            "mainEntityOfPage": canonical
        })
        if page.get("faq"):
            ld.append({"@context": "https://schema.org", "@type": "FAQPage",
                       "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                                      for q, a in [x.split("|", 1) for x in page["faq"]]]})

    body_html = md(page["body"])
    body_html = body_html.replace("{{CONTACT_BUTTONS}}", contact_buttons(ui))
    body_html = body_html.replace("{{EMAIL}}", EMAIL)

    essentials = ""
    if page.get("summary"):
        essentials = f'<aside class="essentials" aria-label="{ui["essentials"]}"><h2>{ui["essentials"]}</h2><ul>' + \
            "".join(f"<li>{md(s)[3:-4]}</li>" for s in page["summary"]) + "</ul></aside>"
    sources = ""
    if page.get("sources"):
        items = []
        for s in page["sources"]:
            name, _, link = s.partition("|")
            items.append(f'<li><a href="{esc(link.strip())}" rel="noopener nofollow">{esc(name.strip())}</a></li>' if link else f"<li>{esc(name)}</li>")
        sources = f'<section class="sources"><h2>{ui["sources"]}</h2><ul>{"".join(items)}</ul></section>'

    if is_index:
        main = body_html
    elif page.get("type") == "page":
        main = f'<article class="page"><h1>{esc(title)}</h1>{body_html}</article>'
    else:
        meta_line = f'<p class="meta">{ui["by"]} <a href="{"/sobre/" if lang=="es" else "/en/about/"}">{AUTHOR}</a> · {ui["updated"]}: <time datetime="{updated}">{updated}</time></p>'
        main = f'<article class="guide"><header><h1>{esc(title)}</h1>{meta_line}</header>{essentials}{body_html}{sources}</article>'

    cta = "" if page.get("type") == "page" and page["slug"] in ("contacto", "contact") else f'''
<section class="cta" aria-labelledby="cta-h">
  <h2 id="cta-h">{ui["cta_title"]}</h2>
  <p>{ui["cta_text"]}</p>
  <div class="btn-row">{contact_buttons(ui, big=True)}</div>
</section>'''

    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}{"" if is_index else " | Deportation Defense Law"}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="{lang}" href="{canonical}">
<link rel="alternate" hreflang="{ui["other"]}" href="{SITE}{mirror_url}">
<link rel="alternate" hreflang="x-default" href="{SITE}{url_for("es", mirror if lang=="en" else page["slug"])}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="{"website" if is_index else "article"}">
<meta property="og:locale" content="{"es_US" if lang=="es" else "en_US"}">
<meta name="author" content="{AUTHOR}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">{ui["skip"]}</a>
<header class="site-head">
  <a class="brand" href="{ui["dir"]}"><span class="brand-mark" aria-hidden="true"></span>Deportation Defense Law</a>
  <nav class="site-nav" aria-label="{ui["read_more"]}">
    <ul>
      <li><a href="{ui["dir"]}">{ui["nav_home"]}</a></li>
      {nav_guides}
      <li><a href="{"/sobre/" if lang=="es" else "/en/about/"}">{ui["about"]}</a></li>
      <li><a class="lang" href="{mirror_url}" lang="{ui["other"]}" hreflang="{ui["other"]}">{ui["other_label"]}</a></li>
    </ul>
  </nav>
</header>
<main id="main">
{main}
{cta}
</main>
<footer class="site-foot">
  <p class="disclaimer">{ui["disclaimer"]}</p>
  <nav aria-label="{ui["footer_nav"]}"><ul>{nav_guides}<li><a href="{"/aviso-legal/" if lang=="es" else "/en/legal-notice/"}">{ui["legal"]}</a></li><li><a href="{mirror_url}" hreflang="{ui["other"]}">{ui["other_label"]}</a></li></ul></nav>
  <p class="fine">© {datetime.date.today().year} Deportation Defense Law · Loom Digital LLC · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
</footer>
<div class="sticky-cta"><a class="btn btn-primary" href="{ui["dir"]}{"contacto" if lang=="es" else "contact"}/">{ui["cta_btn"]}</a></div>
</body>
</html>'''

def build():
    if os.path.exists(DIST): shutil.rmtree(DIST)
    os.makedirs(DIST)
    for fn in os.listdir(os.path.join(ROOT, "static")):
        shutil.copy(os.path.join(ROOT, "static", fn), DIST)
    all_pages = {}
    urls = []
    for lang in ("es", "en"):
        pages = load_lang(lang)
        all_pages[lang] = pages
    for lang, pages in all_pages.items():
        for p in pages:
            out_dir = os.path.join(DIST, p["url"].strip("/"))
            os.makedirs(out_dir, exist_ok=True)
            open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(layout(p, pages, all_pages))
            urls.append((p["url"], p.get("updated") or p.get("date") or datetime.date.today().isoformat(), p))
    # 404
    ui = UI["es"]
    p404 = dict(title=ui["not_found"], description="", slug="404", lang="es", type="page", url="/404/",
                body=f'<p>{ui["not_found_text"]}</p><p><a href="/">Inicio</a> · <a href="/en/">English</a></p>')
    open(os.path.join(DIST, "404.html"), "w", encoding="utf-8").write(layout(p404, all_pages["es"], all_pages))
    # sitemap
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for url, lastmod, p in urls:
        mirror = p.get("mirror") or p["slug"]
        alt = url_for(UI[p["lang"]]["other"], mirror)
        sm.append(f'<url><loc>{SITE}{url}</loc><lastmod>{lastmod}</lastmod>'
                  f'<xhtml:link rel="alternate" hreflang="{p["lang"]}" href="{SITE}{url}"/>'
                  f'<xhtml:link rel="alternate" hreflang="{UI[p["lang"]]["other"]}" href="{SITE}{alt}"/></url>')
    sm.append("</urlset>")
    open(os.path.join(DIST, "sitemap.xml"), "w").write("\n".join(sm))
    open(os.path.join(DIST, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    print(f"built {len(urls)} pages → {DIST}")

if __name__ == "__main__":
    build()
