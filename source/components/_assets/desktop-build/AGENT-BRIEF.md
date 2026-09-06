# Desktop rebrand build brief — read fully before writing anything

You are rebuilding old desktop screenshots as hand-authored HTML pages in the SportsHeist
dark-mode design system, exactly like the finished examples. The Figma look is already
encoded in the kit — your job is to transcribe each old screen's INFORMATION (nav, copy,
fields, states) onto the kit. Never copy the old screenshots' colors or styling
(purple/white/gradients are all forbidden).

## Finished reference examples — STUDY THESE FIRST (read the actual files)

- `/Users/mk/Documents/Sportsheist/02-DOCUMENTATION/Branding Designs/components/desktop-fan-war-room.html`
  ← THE KIT. Its `<style>` block + icon sprite + rail is copied into every page you build.
  Read its CSS class names and frame structure carefully. (Skip the base64 blobs.)
- `/private/tmp/claude-501/-Users-mk-Documents-Sportsheist/ac9fa6d2-8833-4e57-a64e-d17d1c9259a5/scratchpad/build/backchat-body.html` + `backchat-css.css` — how a page body + page-specific css is written.
- `/private/tmp/claude-501/-Users-mk-Documents-Sportsheist/ac9fa6d2-8833-4e57-a64e-d17d1c9259a5/scratchpad/build/auth-body.html` + `auth-css.css` — the no-rail auth split layout, dialogs, forms, club rows/crest plates.

## Workflow per page

1. Look at every old PNG for your section (Read tool):
   `/Users/mk/Documents/Sportsheist/02-DOCUMENTATION/Branding -Desktop/Desktop Screenshots/...`
   Extract: which screens exist, exact field labels, table columns, empty-state copy,
   KPI names, flow order, which are popups (popup = dialog/panel frame, NOT a new page).
2. Write `<slug>-body.html` and (if needed) `<slug>-css.css` in
   `/private/tmp/claude-501/-Users-mk-Documents-Sportsheist/ac9fa6d2-8833-4e57-a64e-d17d1c9259a5/scratchpad/build/`.
3. Build:
   `cd /private/tmp/claude-501/-Users-mk-Documents-Sportsheist/ac9fa6d2-8833-4e57-a64e-d17d1c9259a5/scratchpad/build && python3 mkpage.py <slug>-body.html "/Users/mk/Documents/Sportsheist/02-DOCUMENTATION/Branding Designs/components/<slug>.html" "<title>" <active> <css-file|-> [<rail-file> "<Active label>"]`
   - Fan pages: `<active>` = war|merits|backchat|alerts|profile (or a non-matching word for none highlighted); omit rail-file.
   - Management pages: `<active>` = `x`, rail-file = `mgmt-rail.html`, active label e.g. `"Dashboard"` (must match the rail item text exactly; use `Results &amp; Actions` for that one).
   - DSC pages: rail-file = `dsc-rail.html`, label e.g. `"Configuration"`.
   - Auth/login pages (no rail): `<active>` = `none`, no rail-file.
4. Confirm the command prints `unresolved: none`. Do NOT open a browser.

## Structure rules (hard requirements)

- One screen state per `<section class="frame" data-title="...">`. `min-height:1024px`
  on the frame (taller via inline style only when content needs it).
- Frame content goes in `<div class="content content--flow" style="min-height:1024px">`.
- Never stack two screens in one frame. A popup in the screenshots = same page dimmed
  (`opacity:.35` on the content div) + `.scrim` + `.dlg` (centered dialog) or
  `.panelwrap/.panel` (right-side sheet — copy the pattern & CSS classes from backchat-css.css into your css file).
- Extra icons: add a `<svg hidden><defs>` block at the top of your body file with new
  `<g id="i-...">` icons (24-box, stroke 1.7, round caps). Reuse existing sprite ids first.
- Keep old frame `data-title`s where the screen survives; collapse duplicates
  (e.g. `Foo(1)`/`Foo(2)` become one frame or one frame + a dialog frame).

## Kit classes you already have (from the war-room head — do not redefine)

rail / hero (hero, hero__title, hero__sep, hero__strap, hero__field+`url(#chev)`, hero__slash+`#hero-slashes`)
sect/sect__t · btn-plus · btn-ico · pill-view · sect__arrows · band · band__row · band--empty · empty
card, card__by/duo/t/p/meta/clock/cat · ava/ava--sm · tag · likes+ring · cta--go/--done/--line
opt (voting option panel) · chip--stop/--go · bar/bar__f/--stop/--go/bar__k/bar__marks
plate/--go/--stop/--hold · pagehead/pagehead__t · seg/seg__b/--on · toolrow · grid · pager/pg/--on
formcard · f__l/f__in/f__ta/f__hint/f__count · radio/radio__o/--on · scrim · dlg (badge/t/p)
bal (gradient balance banner) · rows/rowi (icon+title+para rows)
Avatars: `--av-a` … `--av-h` (use as `style="background-image:var(--av-a)"`).
Sprite icons: i-war i-cup i-mic i-bell i-user i-out i-plus i-sort i-funnel i-search i-chl i-chr
i-ext i-timer i-thumb i-thumb-f i-gavel i-eye i-info i-check i-hold i-run i-no i-back i-coin
i-shield i-field i-brief i-grid i-bulb i-doc i-cal i-gear i-sliders i-flag i-chart i-mega.

## Design rules (from the contract — non-negotiable)

- Colors: ONLY the tokens in the kit `:root`. Verdict/state colors: acid `var(--acid)` for
  approved/go, `var(--stop)` #FB3748 for rejected/destructive, `var(--hold)` #FF8C11 for
  veto-hold ONLY. No purple, blue, silver, orange gradients, no other hues. Charts: acid +
  white + muted only.
- Text on acid fill is ALWAYS `var(--acid-ink)`, never white.
- Real content only — transcribe the screenshots' copy (fix typos), or reuse the Barcelona
  sample-club content from the finished mobile components in
  `/Users/mk/Documents/Sportsheist/02-DOCUMENTATION/Branding Designs/components/` (e.g.
  matches.html, alerts.html, profile.html, veto.html, hall-of-fame.html, merits.html,
  clubs.html, child-account.html, account-settings.html, wallet.html). No lorem, no "Label 1".
- Club crests: use the `.crest` white plate with 2–4 letter codes (BAR, RMA…) — pattern in
  auth-css.css. Never colored crest art.
- Numbers in columns: `font-variant-numeric:tabular-nums` (`.card__clock` etc. already do).
- Do not invent nav items; the rails are fixed. Do not redesign the rail/hero.
- Buttons/pills: acid CTA = primary, `--surface` pill = secondary, outline `.cta--line` = tertiary.
- Tables (management/DSC): build as `.rows`-style list rows or a simple table styled with
  `--section` container + `--line-soft` row borders + 13px body + muted headers
  (11px/700/.1em uppercase). Keep it consistent with the kit.

Deliver at the end: one line per built page — slug, frame count, frame titles.
