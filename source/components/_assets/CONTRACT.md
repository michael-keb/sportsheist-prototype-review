# Component build contract — SportsHeist dark-mode rebrand

Every component file in `components/` follows this contract so any of them can be dropped
into the shared review page by `build-reviews.py` without edits.

## Reference implementation

`../merits.html` — read it before writing anything. Copy its token block verbatim.

## Sampled tokens — do not invent values

```
--bg            #030401   screen canvas
--section       #080A0C   bordered section container
--surface       #1C2129   cards, controls, tab bar
--sunken        #13171E   inner panels, dark pills
--line          rgba(255,255,255,.075)
--line-soft     rgba(255,255,255,.045)
--acid          #9BE222   accent
--acid-ink      #0B0E06   text/icon on accent
--acid-wash     rgba(155,226,34,.12)   translucent pill / active row
--hero-a        #0D3617   hero field gradient start
--hero-b        #17481C   hero field gradient end
--text          #FFFFFF
--muted         #99A0AE   secondary text
--dim           #5B606B   tertiary text
--r-card        16px
--r-panel       12px
--r-pill        999px
--gutter        16px
```

Semantic red for downward movement / destructive: `#E2564A`. Nothing else.

**There is no other colour.** No silver, no bronze, no blue, no purple. If a design needs
a distinction, use scale, weight, ring opacity or the accent wash — not a new hue.

## Type

System stack, no webfonts:
```
--font: "Inter", -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto,
        Helvetica, Arial, sans-serif;
```
Measured scale: screen title 34/800/-.025em uppercase · section label 18/600/-.015em ·
card title 15–17/600 · body 13/400 · meta 11.5–12.5 · tracked micro-label 10.5–11/700/.14em
uppercase. Use `font-variant-numeric: tabular-nums` on every figure that sits in a column.

## Established patterns — reuse, don't reinvent

| Pattern | Construction |
|---|---|
| **Hero banner** | 138 px, `--r-card`, gradient `--hero-a`→`--hero-b` at 112deg; faint white triangles at 2.4–3% opacity in the field; three acid peaks bottom-right (54% × 38%); knockout prop **in front of** the peaks; title left, uppercase, no strapline |
| **Section label** | 18/600 white at the gutter, no adornment |
| **Section header** | label + `View all ↗` pill (`--surface`, 34 px, R pill) |
| **Section container** | `--section` fill, 1 px `--line`, `--r-card`, 12 px padding; holds a status pill + circular icon buttons above its content |
| **Status pill** | `--acid-wash` fill, 32 px, accent text 11/700/.11em uppercase, 6 px leading dot |
| **Icon button** | 38 px circle, `--surface`, white 1.9-stroke icon |
| **Card** | `--surface`, `--r-card`, 16 px padding |
| **Row** | 10–11 px vertical padding, 1 px `--line-soft` top border, `:first-child` no border |
| **Tab bar** | floating pill `--surface`, 58 px, 10 px inner padding, 5 tabs; active = accent pill with icon **and** label; inactive = outline icon only |
| **Avatar** | circle, `background-size:cover`, `background-position:center 22%` |

Icons: inline SVG only, 24-box viewBox, round caps and joins. Stroke weight is **optical, not
fixed** — measured across the export it runs `1.5–3.2`, heavier as the rendered size drops:
tab glyphs 1.7, search / filter / timer 1.9, plus 2.4, delta arrows 2.8–3.2, large empty-state
art 1.5. Match the weight to the size you are drawing at.
No icon fonts, no emoji.

## Contrast — measured, obey these

| Pair | Ratio | Rule |
|---|---|---|
| `--acid-ink` on `--acid` | 12.31:1 | **The only ink allowed on an accent fill** |
| white on `--acid` | **1.58:1** | Never. Fails even the 3:1 non-text floor |
| white on `--surface` | 14.5:1 | Body and titles |
| `--muted` on `--surface` | ~5.0:1 | Secondary copy — the floor for anything readable |
| `--dim` on `--surface` | **2.56:1** | Decorative tracked micro-labels only. Never body copy, never a value |
| `--acid` on `--surface` | 9.6:1 | Figures, links, active labels |
| `#E2564A` on `--surface` | **4.36:1** | Passes AA large only. Always pair red with an icon and a sign |
| white on `#E2564A` | **3.71:1** | Never. If red becomes a fill, ink is `--acid-ink` |
| `--bg` → `--section` | 1.04:1 | Invisible on its own — the 1 px `--line` is doing the work, so never omit it |

State must never rest on colour alone: pair it with an icon, a word, a sign, weight or position.

## Tap targets — one open system-wide decision

The Figma export's controls are **34 px and 38 px**, both under the 44 px platform minimum. The
export gets away with it because surrounding padding absorbs the difference, but nothing enforces
that, and several components have had to break ranks:

- `forms.html` set every control and button to **52 px**
- `comments.html` built its send button at **44 px** rather than the kit's 38
- `create-idea.html` keeps the 38 px disc but adds an `::after` expansion to a 44 px hit area

The `::after` expansion is the pattern to copy — it keeps the sampled 38 px visual while meeting
the minimum:

```css
.icon-btn{position:relative}
.icon-btn::after{content:"";position:absolute;inset:-3px;border-radius:inherit}
```

⚠️ **Needs a decision:** either adopt the invisible hit-area expansion everywhere and keep the
38 px look, or raise the visual size and accept a departure from the export. Do not leave a
component with a bare sub-44 px target.

## The paused state — canonical, settled in `veto.html`

The palette has two hues, so a third *state* is expressed as a different kind of mark, not a
different colour:

| Mark | Means |
|---|---|
| Filled plate | Settled — accent for approved, `#E2564A` for rejected |
| **Accent bars struck at 135°** | **Held — nothing is decided yet** |
| Dashed stroke | A figure that has stopped moving |

- On dark planes: `rgba(155,226,34,.11)` bars, 5 px on / 6 px off, over `--sunken`, with a
  `rgba(155,226,34,.30)` ring and a `⊘` glyph in accent.
- On an accent fill: the same bars inverted to `rgba(3,4,1,.62)`, so held reads as held on a
  bright plate too.
- On a ring gauge: `pathLength="100"` with an enumerated dash list.

**The hatch is static.** An animated barber-pole reads as "in progress", which is the opposite
of held.

**Reserve the hatch for genuinely paused states only** — never loading, disabled, pending or
scheduled. Its force comes from meaning one thing.

Related: a held clock keeps **full-contrast white digits**. Greying it reads as disabled, which
is wrong — held is loud, finished is quiet.

## Control height — two measurements, one open decision

| Value | Where it comes from |
|---|---|
| **52 px** | `forms.html` standardised every control and button here, derived from the `idea-card.html` CTA. Most components follow it. |
| **64 px** | `auth.html` measured it off the **button component on the Get Started Figma page** — 353 × 64, R32 track, with a 46 px acid disc inset 9 px. A 46 px disc inside a 9 px inset cannot fit in 52 px, so the Get Started CTA is physically 64. |

64 px is the better-sourced number; 52 px has the wider adoption. ⚠️ **Needs a decision** — and
whichever wins, the auth frames and the forms kit have to agree, because `auth.html` uses
`forms.html`'s controls.

Same file also measured the auth frames' gutter at **20 px** (353 in 393), against the kit's
`--gutter: 16px`. Declared there as `--pad` with its provenance in a comment.

### Verb pair — also open
`auth.html` settled on **Log in / Sign up**, reasoning that both words appear on the same screen
so near-identical verbs do the most damage there. An earlier build of the same screen chose
**Sign in / Sign up**. The library label now reads "Log in" to match the component. Settle it
library-wide before build.

## Club crest plate — canonical, settled in `club-selection.html`

Third-party crests come in every colour, so never composite them straight onto our surfaces:
measured against the dark card, a yellow crest hits ~15:1 while a blue one drops to ~1.4:1.
The plate makes that constant by measuring **the plate**, not the crest, against the surface.

```
--plate:      rgba(255,255,255,.94)   /* fixed, never per-club */
--plate-edge: rgba(0,0,0,.13)         /* inner hairline, reads as a bevel */
radius:  calc(size * .28)
padding: calc(size * .125)            /* all sides */
fit:     object-fit:contain into the padded SQUARE
```

Light is the correct ground, not an arbitrary one — crests are authored for light grounds (kit,
print, letterhead), so compositing on light preserves the contrast their own designers signed off.
The plate measures ~14.4:1 on `--surface` and ~18.3:1 on `--bg`, identically for every club.

**Three sizes only:** `28px` dense/secondary rows · `40px` selects and club rows · `64px` headers
and confirmation lockups. Fitting to the square rather than the height is what kills the
roundel-vs-shield weight variance.

**Fallback:** the plate holding a 2–4 character club code, uppercase 800, `-.03em`,
`var(--acid-ink)`, at `calc(size * .30)`. Use it for missing artwork, failed ingest, **and as the
loading placeholder** so a row never reflows.

Never ship a dark-plate variant for pale crests — two plate tones in one list destroys the
constant optical weight the plate exists to create.

⚠️ **Reconciliation outstanding:** `matches.html` built a `--sunken` dark plate at 56/40/24 and
`merits.html` uses a 17 px inline code chip. Both predate this spec and need bringing onto it.

## One screen per device — required

**Never stack two screens in one scroll.** If a component covers more than one screen, wrap each
in its own frame and the review page will give each its own phone:

```html
<main class="screen">
  <section class="frame" data-title="Compose">        …screen 1… </section>
  <section class="frame" data-title="Compliance">     …screen 2… </section>
  <section class="frame" data-title="Deposit">        …screen 3… </section>
</main>
```

- `class="frame"` is the screen boundary. `data-title` names it; without one the builder falls
  back to the frame's first heading.
- Two or more frames ⇒ the review page switches to a device grid, one phone per frame, numbered
  and captioned. One frame or none ⇒ a single sticky device.
- Chrome that lives outside `<main>` (tab bar, composer, dock) is **replayed into every frame**
  automatically, so write it once.
- Each frame must stand alone at 375 × 812. Don't rely on a sibling frame for context.
- **Anything shared between frames must live outside `<main>`.** Each frame is emitted into its own
  device, so a resource declared inside `<main>` exists only in the frame that declares it.
  A shared `<svg><defs>` sprite inside `<main>` will leave every later frame's icons blank —
  this actually happened in `merit-detail.html`. Put shared `<defs>`, sprites and templates
  alongside the tab bar, outside `<main>`, where they are replayed into every frame.
- Bottom padding belongs **inside** each frame. The `.frame` element itself is not emitted, so
  padding set on it is lost; put a spacer or padding on the frame's inner wrapper.
- **Clear the device island.** The review device draws a 96 × 26 island at `top:8px`, which covers
  the first **26 px** of the content area. Whatever sits at the top of a frame — app bar, eyebrow,
  caption — needs ~`34px` of top clearance or it renders behind the island. The library value is
  `margin:34px var(--gutter) 14px` on the top bar; `ideas-list.html` and `voting-list.html` are the
  reference. This was missed in `all-locker-rooms.html` and `linked-member.html` and fixed after the
  fact — check it before shipping a component.

**Kits are the exception.** A specimen sheet — dialogs, sheets, forms, states, foundations — is
genuinely one page showing many variants, so it stays a single device and uses `class="spec"` (not
`frame`) for its specimens.

## Structural contract — required

```html
<style> …single stylesheet, :root token block first… </style>

<main class="screen">   <!-- everything that scrolls -->
  …
</main>

<nav class="tabbar">…</nav>   <!-- optional; must be OUTSIDE <main> -->

<script> …single IIFE, optional… </script>
```

Rules:
- `.screen{max-width:420px;margin:0 auto;padding:12px 0 110px}`
- Anything pinned to the bottom of the viewport lives **outside** `<main>`, or it will scroll
  away when the file is embedded in the review page's device frame.
- One `<style>` and at most one `<script>`. No `<link>` tags — the review page is published
  to a host that blocks external requests, so **all** assets must be inline data URIs.
- Target 375 × 812; must not break at 430.
- Include `@media (prefers-reduced-motion:reduce){*{transition:none!important}}`.

## Assets

- `avatars.css` — 18 portraits from the exports as `--av-01` … `--av-18`. Paste the
  custom properties you use into your own `:root`; don't link the file.
- `hero-prop-athlete.b64` — base64 PNG of the knockout athlete, alpha already cut.
  Use as `<img class="hero__prop" src="data:image/png;base64,…">`.
- Need a different prop? Say so in your report rather than drawing clip-art. A hand-drawn
  pseudo-3D object is worse than no object.

## Building a review page

```bash
python3 _assets/build-reviews.py              # every component that exists
python3 _assets/build-reviews.py my-component # just yours
```

It scopes every selector under `.mk`, wraps `<main>` in a scroll container so pinned chrome
stays pinned, emits your `<script>` so the frame is interactive, generates the side menu from
`manifest.json`, and builds the on-this-page menu from your notes' section headings.

`@keyframes`, `@font-face` and `@media` all survive scoping — verified. CSS animation is fine;
you don't need to reach for SVG SMIL to dodge the scoper.

Add your component to `manifest.json` if it isn't already there, or the page won't be linked
from the index or the side menu.

## Class naming

Prefix nothing globally, but **avoid these names** — they collide with the review shell:
`eyebrow` is already handled, but do not introduce `chip`, `meta`, `mark`, `token`, `side`,
`stage`, `device`, `col`, `wrap`, `layout`, `prov`, `qs`, `flag`, `dek`, `seg`.

## Honesty rules

- Never invent a token, a tier system, a colour or an icon style.
- Real content only — no lorem, no `Label 1`.
- If the design needs a product decision you can't make (what a currency is called, whether
  tiers exist), build the most defensible option and **report the open question**.
