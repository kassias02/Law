# deportationdefenselaw.com

Sitio estático bilingüe (español en la raíz, inglés en /en/). Sin framework: markdown → HTML con un script de Python.

## Estructura

```
content/es/*.md     páginas en español  →  /slug/
content/en/*.md     páginas en inglés   →  /en/slug/
static/             style.css, favicon.svg  (se copian tal cual)
build.py            generador
dist/               salida (no editar a mano, se regenera)
netlify.toml        configuración de Netlify
```

## Construir en local

```bash
pip install markdown
python3 build.py      # genera dist/
python3 -m http.server -d dist 8000
```

## Publicar

**Opción A — Netlify Drop (rápido, manual).** Arrastre la carpeta `dist/` a https://app.netlify.com/drop, o suba `ddl-dist.zip` al proyecto existente.

**Opción B — GitHub + Netlify (recomendado).** Suba este repo a GitHub y conéctelo al proyecto `lovely-muffin-831585`. Netlify ya está configurado por `netlify.toml`:
- build command: `python3 build.py`
- publish directory: `dist`

Cada commit publica automáticamente.

## Añadir un artículo

Cree `content/es/mi-slug.md` (y su espejo `content/en/my-slug.md`):

```markdown
---
title: Título completo, como aparece en el <h1> y en Google
nav: Texto corto para el menú
description: Meta description, 150–160 caracteres.
slug: mi-slug
mirror: my-slug          # slug de la versión en el otro idioma
order: 6                 # orden en el menú
date: 2026-09-20
updated: 2026-09-20
summary:
  - Punto clave 1
  - Punto clave 2
sources:
  - Nombre de la fuente|https://url-oficial
faq:
  - ¿Pregunta?|Respuesta breve para el schema FAQPage.
---
Cuerpo en markdown.

<div class="btn-row">{{CONTACT_BUTTONS}}</div>
```

`{{CONTACT_BUTTONS}}` inserta los botones de contacto. `{{EMAIL}}` inserta el correo.

Tipos de página: sin `type` = guía (con autor, fecha, resumen, fuentes). `type: page` = página simple (sobre, legal). `type: index` = portada.

## Teléfono y WhatsApp

Están ocultos hasta que existan. Para activarlos, defina variables de entorno en Netlify (Site settings → Environment variables):

- `DDL_PHONE` = `+1 713 555 0100`
- `DDL_WHATSAPP` = `17135550100`

Y vuelva a desplegar.

## Formularios

Usan Netlify Forms (`data-netlify="true"`), ya activados en el proyecto. Los envíos aparecen en el panel de Netlify, pestaña Forms. Hay un campo trampa antispam (honeypot).
