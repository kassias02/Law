---
title: Talk to an immigration lawyer
slug: contact
mirror: contacto
type: page
description: Send your case to a licensed immigration attorney. Free, no obligation. This site is not a law firm.
date: 2026-09-16
updated: 2026-09-16
---
<div class="notice">
<p><strong>If you have a hearing within 72 hours or a relative in detention, call an attorney directly.</strong> A form can take hours to be answered. Free legal help is listed on the <a href="https://www.justice.gov/eoir/list-pro-bono-legal-service-providers" rel="noopener nofollow">official EOIR list of pro bono providers</a>.</p>
</div>

Tell us the basics and we pass your case to a licensed immigration attorney covering your area. There is no cost to you and no obligation to hire anyone.

<form name="case" method="POST" data-netlify="true" netlify-honeypot="company" action="/en/thank-you/">
  <input type="hidden" name="form-name" value="case">
  <p class="hp"><label>Leave this empty: <input name="company"></label></p>

  <label for="name">Name</label>
  <input id="name" name="name" type="text" autocomplete="name" required>

  <label for="phone">Phone or WhatsApp</label>
  <input id="phone" name="phone" type="tel" autocomplete="tel" required>

  <label for="state">Which state are you or your relative in?</label>
  <input id="state" name="state" type="text" required>

  <label for="situation">What is the situation?</label>
  <select id="situation" name="situation" required>
    <option value="">Choose one</option>
    <option>I received a Notice to Appear</option>
    <option>I have a court date</option>
    <option>A relative is detained by ICE</option>
    <option>I have a removal order</option>
    <option>Other</option>
  </select>

  <label for="date">Hearing date, if you know it</label>
  <input id="date" name="hearing_date" type="text" placeholder="e.g. November 12, or not sure">

  <label for="details">Tell us briefly</label>
  <textarea id="details" name="details"></textarea>

  <label class="check" for="consent">
    <input id="consent" name="consent" type="checkbox" value="yes" required>
    <span>I authorize my information to be sent to a licensed immigration law firm so they can contact me by phone, WhatsApp or email. I understand this site is not a law firm and that submitting this form does not create an attorney-client relationship.</span>
  </label>

  <button class="btn btn-primary" type="submit">Send my case</button>
</form>

<p style="margin-top:2rem"><strong>Do not put sensitive details here</strong> (document numbers, full criminal history). Save those for your conversation with the attorney.</p>
