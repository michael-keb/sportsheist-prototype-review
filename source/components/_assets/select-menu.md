# The select menu — canonical, working

The closed select was fully branded everywhere in the library, but tapping it opened
the OS option popup — grey system chrome that ignores every token and, at mobile
widths, draws over the field's own label. The popup is the one piece of a native
`<select>` that CSS cannot reach, so this is the one implementation that replaces it.
Paste it whole; do not write a second one.

## How it works

The `<select>` **stays in the DOM as the state holder** — its `id`, `.value`,
`aria-invalid` and every `change` listener keep working (the child-account age gate
and the country→region cascade read it unchanged). It is hidden off-interaction
(`1px`, `opacity:0`, `pointer-events:none`, `tabindex="-1"`), and two generated
elements do the showing:

- a **face button** carrying the selected option's text, `aria-haspopup="listbox"`,
  `aria-expanded`, labelled by the field label plus itself
- a **`.dd` popover** — `role="listbox"`, option buttons with `aria-selected` and an
  accent tick — using the same panel recipe as the date picker: `--surface` fill,
  1 px `--line`, `--r-panel`, shadow `0 18px 44px rgba(0,0,0,.55)`, anchored
  `top:calc(100% + 8px)` to the `position:relative` control shell

Choosing an option sets `selectedIndex` on the native select and fires `input` +
`change` (bubbling), so existing validation and dependent selects re-run on their own.

## Behaviour rules

- Open: tap the face, or ArrowUp/ArrowDown on it. Focus lands on the selected option.
- Close: Escape (returns focus to the face), a tap away, Tab, or choosing.
- Arrows move through options, Home/End jump, `scrollIntoView({block:'nearest'})`
  keeps the active one visible; the panel caps at `max-height:288px` and scrolls.
- A `value=""` placeholder option ("Choose a stage") is a prompt, not a choice — it
  shows on the face in `--dim` via `.ctl--placeholder`, and is **not** offered as a
  row in the menu.
- Disabled selects and `.is-disabled` / `.field--locked` shells are left native —
  nothing opens, so nothing needs replacing.
- In the **right column of a `.two-up`** the panel right-anchors (`.dd--r`) so a
  `width:max-content` menu grows toward the middle of the screen, not off the edge.
- The chevron rotates 180° while open and the shell takes the focus ring
  (`.is-open` mirrors `:focus-within`).
- Panel width: `min-width:100%` of the control, `width:max-content`, capped at
  `276px` — the date picker's width, so the two popovers read as one family.

## Where it lives

| File | Adapter |
|---|---|
| `child-account.html` | `.ctl` shell — reference implementation, plus the country→region cascade |
| `forms.html` | `.ctl` shell — kit page; the "Focus — picker open" specimen draws the panel statically (`.dd--spec`), and Reset all specimens closes any open menu |
| `account-settings.html` | `.field--edit` row — face reuses `.field__value` type, chevron sits in `.field__aff` |
| `linked-member.html` | `.field__box` shell |
| `foundations.html` | **left native deliberately** — its selects are forced-state swatches (Default / Hover / Focus / Disabled shown side by side), not controls a member uses |

## Rules

- **One implementation.** If a component needs a select, paste the engine and adapt
  only the three shell hooks: what to hide, where the face sits, what takes `.is-open`.
- **Never rebuild the menu as a `<div>` dropdown detached from a native select.**
  The hidden select is what keeps forms honest — value, validation, reset and any
  scripted cascade all stay real.
- Options come from the select's `<option>` list at open time, so scripts may rewrite
  the options (the cascade does) and the menu stays correct without extra wiring.
