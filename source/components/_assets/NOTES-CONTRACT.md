# Review-notes contract

Every component file `<slug>.html` must ship a companion `<slug>.notes.html`.

The build script wraps your component in a device frame and drops these notes beside it, so the
notes are what the client actually reads. They are an **HTML fragment** — no `<html>`, `<head>`,
`<style>` or `<script>`. Styling comes from the review shell; use only the elements below.

## Required structure

```html
<p class="dek">One or two sentences, plain English, describing what this screen is for and who
uses it. This sits under the page title.</p>

<section id="overview">
  <p class="rv-eyebrow">What you're looking at</p>
  <h2>A sentence-case headline making one point</h2>
  <p>Two or three short paragraphs. Write for a client, not a developer.</p>
</section>

<section id="anatomy">
  <p class="rv-eyebrow">Anatomy</p>
  <h2>Every element, top to bottom</h2>
  <div class="tablewrap">
    <table>
      <caption>Order matches the reading order on screen. Values as built.</caption>
      <thead><tr><th scope="col">Region</th><th scope="col">Element</th><th scope="col">Notes</th></tr></thead>
      <tbody>
        <tr><td>Hero</td><td>Banner</td><td class="t-note">…construction, sizes, <code>#HEX</code>…</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section id="states">
  <p class="rv-eyebrow">States</p>
  <h2>What varies</h2>
  <div class="tablewrap">
    <table>
      <thead><tr><th scope="col">State</th><th scope="col">Treatment</th></tr></thead>
      <tbody><tr><td>Default</td><td class="t-note">…</td></tr></tbody>
    </table>
  </div>
</section>

<section id="provenance">
  <p class="rv-eyebrow">Provenance</p>
  <h2>What is reused and what is new</h2>
  <div class="prov">
    <div class="prov__card">
      <h3>Reused from the Figma file</h3>
      <ul><li><b>Thing</b> — where it came from</li></ul>
    </div>
    <div class="prov__card prov--new">
      <h3>New in this proposal</h3>
      <ul><li><b>Thing</b> — what it does</li></ul>
    </div>
  </div>
</section>

<section id="decisions">
  <p class="rv-eyebrow">Decisions</p>
  <h2>What we need from you</h2>
  <ol class="qs">
    <li><h3>Question as a question?</h3><p>Why it matters and what we assumed. Mark the assumed
      value with <span class="flag">like this</span>.</p></li>
  </ol>
</section>
```

## Rules

- Sections must carry exactly these ids, in this order, and may be omitted only if genuinely
  not applicable: `overview`, `anatomy`, `states`, `provenance`, `decisions`.
  The build script generates the "On this page" menu from them.
- The `<h2>` in each section becomes the menu label, so keep it under ~40 characters.
- Available classes: `dek`, `rv-eyebrow`, `tablewrap`, `t-note`, `prov`, `prov__card`,
  `prov--new`, `qs`, `flag`. Plus plain `h2 h3 p ul ol li b strong em code table thead tbody tr th td caption`.
- Put every measurement and hex in `<code>`.
- No invented values. If you proposed something not in the Figma, it belongs in the
  "New in this proposal" column — that column is the most-read thing on the page.
- Write the decisions section even if you only have one question. If you truly have none, say
  what you'd want confirmed before build.
