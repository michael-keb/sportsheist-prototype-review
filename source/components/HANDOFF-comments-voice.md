# Handoff — speech-to-text in the prototype comments panel

_Written 1 August 2026. Subject: the comments/feedback panel on the right-hand side of
`prototype.html`._

## Short version

**Speech-to-text is already built and working. Nothing was added this session.**

The comments panel has had two voice controls since the last build of
`_assets/build-prototype.py` (31 July, 22:31 — same timestamp as `prototype.html`, so the
served build is current):

| Control | What it does | Survives export? |
|---|---|---|
| **Dictate** | Live speech-to-text. Transcript lands in the comment box; you can edit it before saving. | **Yes** — it is ordinary text |
| **Record** | Attaches an audio voice note to the comment. | **No** — see the gap below |

If the goal is "address the comments and feedback", tell reviewers to use **Dictate**, not
Record. Dictation produces text that comes back to you in the export. A voice note does not.

## Verified live, this session

Loaded `http://localhost:8912/prototype.html?v=50#war-room/0` and checked the running page:

- Origin is `http:` on localhost and reports as a secure context
- `SpeechRecognition`, `MediaRecorder` and `getUserMedia` are all present
- Both buttons render enabled, with no capability warning shown

I did not speak into a microphone, so this confirms availability and wiring, not a live
transcription run. Someone should press Dictate once and say a sentence before it goes to a
client.

## How a reviewer uses it

1. Open the prototype via **`Open prototype.command`** (double-click it). This matters: it
   serves the folder over `http://localhost` because browsers refuse microphone access to
   pages opened straight from disk. Opening `prototype.html` by double-clicking gives you a
   `file://` page where both buttons are disabled and a hint explains why. Typing still works.
2. Navigate to the screen being commented on.
3. Press **Dictate**, speak, press **Stop**. Text appears in the box and can be edited.
4. Add a name, press **Add comment**. `Cmd/Ctrl+Enter` in the box does the same.
5. Click a comment to strike it through as done. The `×` deletes it.
6. **Export comments** (top bar) downloads `sportsheist-comments.md`.

## The gap that matters

> **Update 1 Aug:** largely closed — Record now captures a live transcript that travels in
> the export (see the update under "Suggested next step"). The audio itself still stays
> local; the rest of this section describes the pre-fix behaviour.

**Voice notes never leave the reviewer's machine.** Audio is stored in IndexedDB locally, and
the markdown export writes only a placeholder:

> `· voice note 0:12 (in the browser, not in this file)`

So if a client records ten voice notes and sends the export, you receive ten lines telling you
audio exists somewhere you cannot reach. Options, in order of effort:

- **Cheapest, do this now:** change the Record button's copy so it says the note stays on this
  machine, and lead the reviewer toward Dictate. The placeholder text is honest but only
  appears after the fact, in the export.
- **Medium:** run the recorded blob back through `SpeechRecognition` (or a transcription API)
  at save time so every voice note also produces text.
- **Heavy:** base64 the audio into the export, or post comments to a real endpoint. The export
  is a plain markdown file today, which is the reason it is easy to hand around.

Related, worth knowing before it surprises someone:

- Comments live in `localStorage` per browser profile. Two reviewers on two machines produce
  two separate sets and **each must export separately** — there is no merge.
- Clearing site data wipes comments and voice notes. Export early.
- Dictation language is hard-coded `en-GB` (`build-prototype.py:758`).
- Firefox does not ship `SpeechRecognition`; the button disables itself there with a title
  explaining why. Chrome, Edge and Safari are fine.
- Chrome and Safari transcribe **in the cloud**, not on-device — spoken audio leaves the
  machine. Fine for design feedback; flag it if anything confidential gets discussed.

## Where the code is

Everything lives in the builder, not in a component file. `prototype.html` is generated
output — **edit the builder, never the HTML.**

`_assets/build-prototype.py`:

| Lines | What |
|---|---|
| 242–268 | CSS — `.vrow`, `.vbtn`, `.vbtn.on` recording state, `.vhint`, `.pend`, `.cmt__play` |
| 398–417 | Composer markup — textarea, both buttons, hint line, pending-audio row, name + add |
| 716–752 | `ADB` IndexedDB wrapper, capability detection, `vhint()` |
| 755–781 | Dictation — writes into the textarea so it stays editable |
| 783–812 | `MediaRecorder` capture, timer, permission errors |
| 815–830 | Save path — audio to IndexedDB, comment to localStorage |
| 833–851 | Markdown export |

Storage:

- `localStorage['sportsheist-prototype-comments']` — `{ screenId: [comment, …] }`, screen id
  looks like `war-room/0`
- IndexedDB `sh-proto-audio`, store `clips`, key `` `${screenId}|${ts}` ``

Audio was deliberately kept out of localStorage — a minute of Opus is roughly 100 KB against a
~5 MB string quota shared with the comments themselves. Deleting a comment also deletes its
clip.

Rebuild after any edit:

```bash
python3 "/Users/mk/Documents/Sportsheist/02-DOCUMENTATION/Branding Designs/components/_assets/build-prototype.py"
```

Then hard-refresh, or bump the `?v=` in the URL — the query string is a cache-buster, which is
why the link in play is `?v=50`.

## Suggested next step

Decide whether Record stays. It is the control most likely to be pressed by a client who
assumes we will hear it, and today we will not. Either wire transcription behind it or retitle
it so the limitation is visible at the moment of pressing rather than at export.

**Update, 1 Aug (later session):** both the cheapest and the medium options are done.

- Honest copy first: tooltip + press-time hints saying the audio stays in this browser.
- Then live transcription: `SpeechRecognition` cannot transcribe a saved blob, so a second
  recogniser now runs **alongside** `MediaRecorder` while the reviewer speaks. On save, the
  transcript becomes the comment text if the box was empty, or is stored as `audio.tx` and
  exported as `· voice note 0:12 (audio stays in the browser; transcript: "…")` if the
  reviewer also typed. Firefox (no `SpeechRecognition`) degrades to the old behaviour with
  the honest-copy warning intact; hints and the Record tooltip adapt per browser.
- If dictation is already running when Record is pressed, the transcript recogniser is
  skipped (one `SpeechRecognition` instance per page) and the old warning hint shows.

Rebuilt and verified in the build served on port 8912: page loads with no console errors,
buttons enabled, tooltip correct. **Not yet done: a live end-to-end run with a real voice** —
press Record, say a sentence, save, export, and confirm the transcript appears in the
markdown. Same caveat as Dictate. Cloud-transcription privacy note above now applies to
Record too.
