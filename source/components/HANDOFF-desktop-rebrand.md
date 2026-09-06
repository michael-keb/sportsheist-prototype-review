# Handoff — Desktop rebrand (133 screenshots → live branded pages)

> **STATUS — DONE, 6 September 2026.** All 28 desktop pages are hand-authored HTML on the
> Figma-exact kit (148 frames — every original screenshot state kept as its own frame at the
> client's request, no dedupe). The kit head lives in `desktop-fan-war-room.html`; page
> bodies, rails and the `mkpage.py` builder are preserved in `_assets/desktop-build/`, with
> full-res Figma frame renders in `_assets/desktop-build/figma-refs/`. `desktop-shots/` is
> deleted (repo + local); `desktop-shell.html` retired to `_assets/desktop-shell-reference.html`.
> Live: https://sportsheist-prototype-review.onrender.com (Desktop tab). The notes below are
> kept for context on sources and rules.

_Written 15 August 2026. Audience: whoever rebuilds the three desktop products in the SportsHeist dark-mode branding. This is the job, not a status note._

## Short version

The 133 files in `02-DOCUMENTATION/Branding -Desktop/Desktop Screenshots/` are **old product screenshots**. They show the shipped (or last-shipped) desktop apps in the **previous purple / white / gradient look**. They are **not** the target design.

They are the **content and information architecture** for three desktop products:

1. **Fan app** (`User/`) — member-facing web
2. **Management** (`Managment/` — folder is misspelled) — club-officer web
3. **DSC Labs** (`DSC/`) — platform-ops / admin web

The job is to **rebuild every distinct screen as a real HTML component** in the new branding, the same way mobile was rebuilt. Do **not** restyle the PNGs. Do **not** leave screenshot images in the prototype as the finished artefact.

**Target look** is already specified and partly built:

- Contract: `_assets/CONTRACT.md`
- Tokens / type / icons: `foundations.html`
- Desktop shell (Fan War Room, interactive): `desktop-shell.html` + `desktop-shell.notes.html`
- Figma (new branding): [SportHeist (Copy) Desktop](https://www.figma.com/design/X08VSCaMsUBinDph84Ayzw/SportHeist--Copy-?node-id=12926-4479) and `SportHeist (Copy) 2/` SVGs (`nav.svg`, War Room, Backchat, Get Started)
- Live review: https://sportsheist-prototype-review.onrender.com/ — Desktop tab, then Fan / Management / DSC Labs

Today the prototype shows compressed JPEGs of the old screens so the client can comment. That is a **holding pattern**. Replace each JPEG page with a branded HTML frame as you finish it.

---

## What “done” looks like

A screen is done when:

1. It is a `components/desktop-{fan|management|dsc}-{section}.html` file (or a new frame inside one), **not** an `<img>` of the old PNG.
2. It uses **only** sampled tokens from `CONTRACT.md`. No purple, no lavender, no orange gradient, no script wordmark, no white-canvas Management cards.
3. It is **one page per tab** in the prototype (`<section class="frame" data-title="…">` inside `<main class="page">`). Never stack states in one long scroll.
4. Layout is the **desktop shell**: left rail `230px` `#1C2129`, content cap `1240px`, rail collapse at `1180px`, mobile pill below `900px` (Fan only — Management and DSC Labs stay desktop).
5. Interior controls reuse **existing mobile components** (cards, forms, dialogs, sheets, status pills, idea cards, voting meters) at their measured sizes. Desktop changes **layout**, not the component kit.
6. Empty, loading, error, and populated states are separate frames if the screenshot set shows them.
7. The prototype Desktop → matching app tab navigates to the new HTML, and the old JPEG for that screen is removed from `desktop-shots/`.

---

## Current state (do not confuse these)

| Layer | What it is | Use it for |
|---|---|---|
| `Branding -Desktop/Desktop Screenshots/` | 133 PNGs, old branding, ~1920px wide | IA, copy, fields, flows, empty states |
| `components/desktop-shots/` | Compressed JPEGs served in the prototype | Temporary review only |
| `desktop-fan-*.html` / `desktop-management-*.html` / `desktop-dsc-*.html` | Thin wrappers that display those JPEGs | Replace with real markup |
| `desktop-shell.html` | **Only** interactive desktop page in new branding (Fan War Room: rail expanded / collapsed / detail panel) | Copy this shell; do not redesign it |
| `SportHeist (Copy) 2/` SVGs + Figma Desktop | New-brand Fan desktop for Get Started, Backchat, War Room, nav | Visual source of truth where it exists |
| Mobile `components/*.html` | Finished dark-mode kit | Steal interiors, do not redraw |

---

## Branding rules (non-negotiable)

Copied from `_assets/CONTRACT.md`. If a screenshot uses something else, **throw the colour away, keep the content**.

```
--bg            #030401
--section       #080A0C
--surface       #1C2129
--sunken        #13171E
--line          rgba(255,255,255,.075)
--acid          #9BE222
--acid-ink      #0B0E06     /* the only ink on acid */
--acid-wash     rgba(155,226,34,.12)
--hero-a        #0D3617
--hero-b        #17481C
--text          #FFFFFF
--muted         #99A0AE
--dim           #5B606B     /* decorative labels only */
--red           #E2564A     /* destructive / downward only */
```

**There is no other colour.** No silver, bronze, blue, purple, lavender, orange. White on acid is forbidden (1.58:1). Acid-ink on acid is the only accent text.

**Kill from the screenshots:**

- Purple sidebar, purple primary buttons, purple outlines
- White Management dashboard cards on a light grey page
- Script “Sports Heist” wordmark
- Purple→orange DSC login gradient and lavender Login button
- Neon-purple Fan Sign In CTA and athlete-collage marketing panel (replace with Get Started / auth from Figma + `auth.html`)
- “VIEW DETAILS” as purple text links — become the existing `View details ↗` pill
- Status as coloured words only (`Rejected` in red text on white) — become verdict chips from War Room / results-actions (`Let's do it!`, `Ruled out`, acid / red washes + icon)

**Keep from the screenshots:**

- Which nav items exist per product
- Field labels, empty-state copy, KPIs, table columns
- Flow order (sign-in → club select → payment → War Room, etc.)
- Which screens are list vs detail vs modal vs form
- Club-specific chrome (Barcelona as sample club) — crest as knockout prop, not a new colour

---

## Three products — different jobs, same kit

All three share tokens, type, cards, forms, and the left rail. They do **not** share the same destinations.

### 1. Fan app (`User/`) — 56 screens

Member / guest web. Destinations should match mobile: **War Room, Matches, Backchat, Settings** (and Profile / wallet as pushed routes). Figma `nav.svg` is the rail.

| Section (folder) | Screens | Rebuild as | Notes |
|---|---|---|---|
| War Room | 14 | Extend `desktop-shell.html` + new frames | Hub already exists in new branding. Rebuild All Ideas, My Ideas, Voting, Results, Actions, Create Idea, Become a member, Participation tokens from mobile `ideas-list`, `voting-card`, `results-actions`, `create-idea`, `wallet`. |
| Backchat | 5 | New `desktop-fan-backchat.html` | Figma already has Desktop Backchat, empty, locker rooms. Prefer Figma over the PNG. Reuse `backchat.html`, `locker-room.html`. |
| Matches | 1 | New `desktop-fan-matches.html` | Mobile `matches.html` is a proposal (tab is empty in code). Same content, desktop grid. |
| Profile | 17 | New `desktop-fan-profile.html` | Child accounts, add club, tokens, hall of fame, notifications, your clubs. Reuse `profile`, `child-account`, `clubs`, `hall-of-fame`, `wallet`, `alerts`. |
| Login / Sign up / Forgot | 18 | New `desktop-fan-auth.html` | **Do not copy the purple marketing split.** Use Figma **Desktop - Get Started** + mobile `auth.html` / `onboarding.html` / `club-selection.html`. Collapse duplicate SignIn(1)(2)(3) into real states (empty, filled, error). |
| Setting | 1 | Fold into profile/settings | Same as Account Settings. |

**Fan rail (from Figma `nav.svg`):** SportsHeist wordmark + acid monogram; War Room, Matches, Backchat, Settings; Profile at the bottom as the selected acid pill. Collapse control at the foot.

### 2. Management (`Managment/`) — 62 screens

Club officers. This is the largest rebuild and has **no** finished Figma desktop in the new brand yet. Invent nothing structurally — transcribe the screenshots’ IA onto the Fan desktop shell.

**Management rail (from the Dashboard screenshot, rebranded):**

- Dashboard (home)
- Club Proposals
- Ideas
- Proposals
- Veto Holds
- Results & Actions
- Matches
- Backchat
- Settings → Club Settings, Account Settings
- Footer: Log out

Top bar utilities from the screenshot (mic, notifications with count, avatar) become the same icon buttons as mobile (`38px` / `34px` circles, `--surface`). Primary CTA is acid (`New proposal`), secondary is surface (`Announcement`).

| Section | Screens | Rebuild as | Notes |
|---|---|---|---|
| Dashboard | 2 | `desktop-management-dashboard.html` | KPI row + eight modules. Empty states are first-class. Drop the duplicate analytics download PNG that was filed under Dashboard. |
| Ideas | 2 | `desktop-management-ideas.html` | List + lapsed. Same cards as Fan, extra officer filters. |
| Proposals | 5 | `desktop-management-proposals.html` | Collapse near-duplicates (approved / rejected status shots). |
| Club Proposals | 3 | `desktop-management-club-proposals.html` | Officer-originated vs member proposals — keep the distinction. |
| Create New Proposal | 5 | `desktop-management-create-proposal.html` | Form + posted + multiple options. Reuse `create-idea.html` / `forms.html`. |
| Results & Actions | 13 | `desktop-management-results-actions.html` | Largest set. Deduplicate `result` / `Results` / `Results&Actions`. Popups (`Approve`, `Rule out`, revoke slider, filters) are **dialogs**, not extra full pages — use `dialogs.html`. |
| Veto Holds | 4 | `desktop-management-veto.html` | Reuse `veto.html`. |
| Backchat | 4 | `desktop-management-backchat.html` | Same product as Fan Backchat with officer privileges (start a room). |
| Matches | 2 | `desktop-management-matches.html` | List + create match. |
| Analytics | 4 | `desktop-management-analytics.html` | Activity/revenue, match analytics, demographics, download report. Charts: acid + white + muted only; no extra series colours. |
| Announcement | 1 | `desktop-management-announcement.html` | Compose sheet/dialog. |
| Notifications | 3 | `desktop-management-notifications.html` | Reuse `alerts.html`. |
| Club Settings | 4 | `desktop-management-club-settings.html` | Collapse three near-identical “Club Settings” PNGs into default + directions. |
| Account Settings | 2 | Fold with Settings | One component. |
| Settings | 5 | `desktop-management-settings.html` | Payments, add/register child. Child flows already proposed on mobile. |
| Login | 2 | `desktop-management-auth.html` | Same Get Started language as Fan, labelled Management. |
| Log out | 1 | Dialog on the shell, not a destination | Reuse `dialogs.html`. |

### 3. DSC Labs (`DSC/`) — 15 screens

Platform ops. Smallest set; still a full product.

**DSC rail (from screenshots):**

- Login (pre-auth)
- Club Workspace (home)
- Configuration (sub-pages: Notification, Posting, Additional, Durations, Pricing, Reputation, Threshold)
- Token Manager (DSC lab, club management, gift to club, recovery option, recovery actions)
- Add Tokens

| Section | Screens | Rebuild as | Notes |
|---|---|---|---|
| Login | 1 | `desktop-dsc-auth.html` | Dark canvas, centred `--surface` card, acid Login. No gradient. |
| Club Workspace | 1 | `desktop-dsc-workspace.html` | Club list / switcher for labs staff. |
| Configuration | 7 | `desktop-dsc-configuration.html` | One frame per subsection. Range controls already exist conceptually in `02-DOCUMENTATION/specifications/thresholds/DSC Labs/`. Dark-mode those forms; do not import Ant Design. |
| Token Manager | 5 | `desktop-dsc-token-manager.html` | Tables + recovery dialogs. |
| Add Token | 1 | Frame or dialog on Token Manager | Prefer a dialog if it is a short form. |

---

## How to rebuild a screen (repeatable method)

Work **one section at a time**. Do not start a second product until Fan War Room + Auth + Backchat are HTML.

1. **Open the PNG** in `Branding -Desktop/Desktop Screenshots/{App}/{Section}/`.
2. **Name the states.** If two files are the same page with a popup, that is one frame + a dialog, not two destinations.
3. **Find the mobile counterpart** in `components/` (War Room, ideas-list, auth, backchat, veto, forms, dialogs, sheets, states). Copy token block and interiors verbatim.
4. **Wrap in the desktop shell** from `desktop-shell.html`: sticky rail, `--rail-w: 230px`, content column, hero if the screenshot has a page title banner.
5. **One `<section class="frame" data-title="Exact name">` per tab.** Title is what appears in the prototype left nav.
6. **Swap colours:** purple CTA → `--acid` + `--acid-ink`; white cards → `--surface` on `--bg`; light page → `#030401`; status text → existing verdict / status-pill patterns.
7. **Do not invent nav items** that are not in that product’s screenshot rail.
8. Rebuild: `python3 _assets/build-prototype.py`. Confirm Desktop → app tab → section shows **HTML**, not the JPEG.
9. Delete the corresponding files under `desktop-shots/` for that section so the old look cannot leak back in.

Target canvas: **1440 × 1024** (Figma desktop frames). Content still caps at **1240px**. Prototype already frames wide screens at `1180×760` scaled.

---

## Deduplicate before you build

The 133 files are not 133 unique screens. Collapse these on sight:

| Cluster | Treat as |
|---|---|
| Fan `SignIn`, `SignIn(1)(2)(3)` | Empty / filled / error / consent — 4 frames max |
| Fan `SignUp`, `SignUp(1)(2)(3)`, `SignUP(1)` | Same |
| Fan `Club_Selection` and `(1)` | Default + selected club |
| Fan `CreateIdea` and `(1)` | Form + confirm |
| Fan `Actions` / `Actions(1)`, `Results` / `Results(1)` / `Results2` | Distinct states only if content differs |
| Fan `ParticipationToken` / `ParticipationTokens`, `PuchaseToken` / `PurchaseTokens` | Typo duplicates — one flow |
| Management three Club Settings PNGs + `club-settings.png` | One settings page + directions |
| Management `Account Setting` / `AccountSetting` | One |
| Management `ClubProposals` / `Club_Proposals` | One list |
| Management `NewProposal_Posted` / `New_roposal_Posted` | One |
| Management `Notifications` / `Notifications (2)` | List vs unread vs view |
| Management Results & Actions ~13 files | Hub + needs-action + accepted + two dialogs + filter sheet + revoke + ruled-out. Aim for **≤ 8 frames**. |
| Dashboard `ClubAnalytics_Activity_Download Report.png` | Belongs to Analytics, not Dashboard |

Expect the branded HTML set to land around **70–90 frames**, not 133.

---

## Suggested build order

Ship in this order so the prototype is useful after each slice:

1. **Fan shell already done** — `desktop-shell.html` (War Room hub). Keep it.
2. **Fan Auth / Get Started** — Figma exists; unblocks every other product’s login.
3. **Fan Backchat** — Figma exists.
4. **Fan Profile + Settings + Matches** — mostly mobile lift.
5. **Management Dashboard + rail** — establishes the second product.
6. **Management Ideas / Proposals / Create / Results & Actions / Veto** — core officer job.
7. **Management Backchat / Matches / Notifications / Announcement**
8. **Management Analytics + Club / Account Settings**
9. **DSC Login + Club Workspace**
10. **DSC Configuration (7 subsections)**
11. **DSC Token Manager + Add Tokens**

Do not rebuild Management Auth until Fan Get Started is signed off — they should feel like the same door with a different product label.

---

## Prototype wiring (already there)

- Chrome: **Mobile | Desktop**, then **Fan app | Management | DSC Labs**.
- Screenshot components are injected at build from `_assets/desktop-shots-manifest.json` via `build-prototype.py`.
- Generator: `_assets/build-desktop-shots.py` (do not re-run as a substitute for HTML).
- Wide slugs start with `desktop-`. Fan screenshot slugs: `desktop-fan-*`. Management: `desktop-management-*`. DSC: `desktop-dsc-*`.
- Homes today: Fan `desktop-fan-war-room/0` (JPEG) — switch Fan home to `desktop-shell/0` once War Room screenshots are replaced; Management `desktop-management-dashboard/0`; DSC `desktop-dsc-login/0`.
- Live: https://sportsheist-prototype-review.onrender.com/ password `Cabramatta@123`
- Comments stay in the reviewer’s browser; they must **Export comments**.

When a section is HTML, update `load()` / the Desktop group so that section’s slug points at the new file, and drop it from `desktop-shots-manifest.json`.

---

## Open questions for the client (do not guess)

1. **Fan desktop destinations:** Figma nav is War Room / Matches / Backchat / Settings. Mobile also has Merits and Alerts. Which set does desktop ship?
2. **Management vs Fan Backchat / Matches:** same screens with extra permissions, or separate officer tools?
3. **DSC Labs visual:** no new-brand Figma yet. Confirm it uses the **same** acid/dark kit (recommended) rather than a distinct admin theme.
4. **Duplicates in the PNG dump:** confirm which Results & Actions and Club Settings files are canonical.
5. **Child account / add-club / payments:** mobile currently dead-ends to desktop. Desktop screenshots include those flows — they are in scope here even if mobile later absorbs them.

---

## File map

```
02-DOCUMENTATION/Branding -Desktop/Desktop Screenshots/
  User/          → Fan app (old PNGs)
  Managment/     → Management (old PNGs, folder spelling as shipped)
  DSC/           → DSC Labs (old PNGs)

02-DOCUMENTATION/Branding Designs/
  SportHeist (Copy) 2/     → new-brand Fan desktop SVGs
  components/
    _assets/CONTRACT.md
    foundations.html
    desktop-shell.html                 ← copy this
    desktop-fan-*.html                 ← replace JPEG wrappers
    desktop-management-*.html
    desktop-dsc-*.html
    desktop-shots/                     ← delete per section as HTML lands
    HANDOFF-desktop-rebrand.md         ← this file
```

Figma: https://www.figma.com/design/X08VSCaMsUBinDph84Ayzw/SportHeist--Copy-?node-id=12926-4479

---

## Definition of done for the whole job

- [ ] No purple/white/gradient screenshot remains as the visible prototype page for Desktop.
- [ ] Fan, Management, and DSC Labs each have a branded shell and every unique screenshot state as an HTML frame.
- [ ] Duplicate PNGs collapsed; dialogs are dialogs.
- [ ] Tokens match `CONTRACT.md`; interiors match existing mobile components.
- [ ] Prototype Desktop tabs switch products; left nav lists real screens, one page at a time.
- [ ] Render deploy updated; client can comment on HTML, not JPEGs.
