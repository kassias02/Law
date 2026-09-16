---
title: Hablar con un abogado de inmigración
slug: contacto
mirror: contact
type: page
description: Formulario para que un abogado de inmigración con licencia le contacte sobre su caso de deportación. Gratis y sin compromiso. Este sitio no es un bufete de abogados.
date: 2026-09-16
updated: 2026-09-16
---
<div class="notice">
<p><strong>Si tiene una audiencia en menos de 72 horas o un familiar detenido, llame directamente a un abogado.</strong> Un formulario puede tardar horas en responderse. Puede encontrar organizaciones que dan ayuda gratuita en la <a href="https://www.justice.gov/eoir/list-pro-bono-legal-service-providers" rel="noopener nofollow">lista oficial de EOIR</a>.</p>
</div>

Cuéntenos lo básico y pasamos su caso a un abogado de inmigración con licencia que atienda su zona. No cobramos nada y usted no queda obligado a contratar a nadie.

<form name="caso" method="POST" data-netlify="true" netlify-honeypot="empresa" action="/gracias/">
  <input type="hidden" name="form-name" value="caso">
  <p class="hp"><label>No llenar: <input name="empresa"></label></p>

  <label for="nombre">Nombre</label>
  <input id="nombre" name="nombre" type="text" autocomplete="name" required>

  <label for="telefono">Teléfono o WhatsApp</label>
  <input id="telefono" name="telefono" type="tel" autocomplete="tel" required>

  <label for="estado">¿En qué estado está usted o su familiar?</label>
  <input id="estado" name="estado" type="text" required>

  <label for="situacion">¿Cuál es la situación?</label>
  <select id="situacion" name="situacion" required>
    <option value="">Elija una</option>
    <option>Recibí un Notice to Appear</option>
    <option>Tengo fecha de corte</option>
    <option>Un familiar está detenido por ICE</option>
    <option>Tengo una orden de deportación</option>
    <option>Otra</option>
  </select>

  <label for="fecha">¿Tiene fecha de audiencia? (si la sabe)</label>
  <input id="fecha" name="fecha" type="text" placeholder="Ej.: 12 de noviembre, o no sé">

  <label for="detalles">Cuéntenos brevemente</label>
  <textarea id="detalles" name="detalles"></textarea>

  <label class="check" for="consent">
    <input id="consent" name="consentimiento" type="checkbox" value="si" required>
    <span>Autorizo que mi información se transmita a un bufete de inmigración con licencia para que me contacte por teléfono, WhatsApp o correo. Entiendo que este sitio no es un bufete de abogados y que enviar este formulario no crea una relación abogado-cliente.</span>
  </label>

  <button class="btn btn-primary" type="submit">Enviar mi caso</button>
</form>

<p style="margin-top:2rem"><strong>No escriba aquí detalles sensibles</strong> (números de documentos, antecedentes penales completos). Guárdelos para su conversación con el abogado.</p>
