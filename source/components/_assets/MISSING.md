# What the prototype still does not have

Answers one question: **which screens are missing from the clickable prototype, and what should be done about each.**

Ordered by what the client should do, not by folder. Every claim carries a file and a line.
Paths are relative to `Sportsheist/`:

- `APP/` = `01-PROJECTS/sport-heist-mobile-main/`
- `SPECS/` = `02-DOCUMENTATION/Screen-Specs/`
- `BUILD/` = `02-DOCUMENTATION/Branding Designs/components/`

Baseline, regenerated from the filesystem by `BUILD/_assets/coverage.py` on this pass
(`SPECS/00-COVERAGE-AUDIT.md`, generated block):

> - Components built: **42**
> - Screens (frames) built: **156**
> - Routes deliberately not rebuilt: **8** (foreign scaffolding) + **2** with no widget at all

---

## Summary

| # | Category | Count | What it means for the review |
|---|---|---|---|
| 1 | **Not built, and should be** — reachable in the shipped app, no component | **5** | Small. Roughly a day's work in total. |
| 1b | Documented and captured, but neither coded nor built | **1** | `BC-02` Locker Room attendees. Decide: build it or retire the spec. |
| 2 | **Not built, deliberately** — foreign scaffolding and empty route strings | **10 routes** (8 + 2) | Correct as recorded, with two corrections below. |
| 2b | Routed but unreachable — no live navigation into them | **5 screens** | Not gaps. Do not demo them. |
| 3 | **Built, but a proposal rather than a rebrand** | **9 components = 48 frames**, plus 3 more frames inside otherwise-rebranded components |  The biggest risk in the review. Nothing behind these exists in code. |
| 4 | **States in code but not in the prototype** | **6 confirmed** across 5 sampled components | Small additions to existing components. |
| 4b | States in the prototype with no code behind them | **2 families** | Offline and permission-denied. Flag as proposals. |

**Read row 3 first.** 51 of the 156 frames (48 whole components + 3 partials) — Hall of Fame, Merits, Clubs registration and
payment, most of the child-account flow, the in-room Backchat experience, the Matches detail and
the AI drafting assistant — have no counterpart in `APP/lib` at all. They are good proposals. They
are not rebrands of working screens, and the review should say so out loud.

---

## 1. Not built, and should be

Screens a member can actually reach today that have no frame anywhere in the 42 components.
The list is short because the system components (`sheets`, `dialogs`, `forms`, `upload`,
`filters-pickers`, `media`) already cover the imperative sheets and dialogs thoroughly.

All five are the same shape: **the shipped screen is a dead-end that sends you to the desktop
site, and the prototype built the in-app flow instead.** They are cheap to add and they are the
screens most likely to embarrass the review, because a client tapping through the prototype will
believe these journeys complete in the app.

| # | Screen | Proof it is reachable | Size |
|---|---|---|---|
| 1.1 | **Forgot password — "go to website"** | `APP/lib/pages/access/forgot_password.dart:27` (the routed `ForgotPasswordScreen`), reached from `APP/lib/pages/access/login.dart:109`. Body is one line of copy plus a link that opens `${Environment.url}/en/auth/forgot-password` in the browser (`forgot_password.dart:53-56`) and returns to login. | 1 frame |
| 1.2 | **Sign-up leave-app confirm** | `APP/lib/pages/access/pre_login.dart:31` — `customSimpleDialog` on the Sign Up control, copy `"To sign up, you will need to go to the club's website. Do you want to proeed?"` (`assets/translations/en.json`, `pages.login.pre_login.exit_content`; typo is in the source). Confirming launches `${Environment.url}/en/auth/signup` (`pre_login.dart:37-40`). | 1 dialog frame |
| 1.3 | **Add-club confirmation sheet** | `APP/lib/pages/profile/club/add_club.dart:9`, shown from `APP/lib/pages/profile/club/pick_club.dart:210`. Reached: Profile → Current team → Change club → pick a crest. Renders club art plus `"To add this club, kindly log in to sports heist on desktop"` (`en.json`, `...userProfile.club adding`) and an OK button that pops (`add_club.dart:87`). No API call, no payment. | 1 frame |
| 1.4 | **Child accounts — the shipped list** | `APP/lib/pages/profile/child_account/child_account_screen.dart:36`, routed at `APP/lib/constants/src/routes.dart:256` and reachable from the Profile menu (`profile_body.dart:516-517`). Lists existing children, then `"To add a child account, please proceed to Sports Heist on Desktop"` (`child_account_screen.dart:112`). | 1 frame |
| 1.5 | **Child account — the dead Edit dialog** | `APP/lib/pages/profile/child_account/child_account_screen.dart:88`. Tapping **Edit** on any child opens an `ARE YOU SURE? / All changes will be lost.` dialog with **no confirm handler passed** — it is a confirmation for an action that does not exist. This is a bug the prototype should show a corrected answer to, not reproduce. | 1 frame + a decision note |

*Job size (inference, not measured):* five frames in three existing components
(`auth.html`, `launch.html`, `clubs.html`, `child-account.html`). Under a day. The value is not the
pixels — it is that the prototype stops implying four journeys finish in the app when they do not.

### 1b. Documented and captured, but neither coded nor built

**`SPECS/03-backchat/02-locker-room-attendees.md` (BC-02)** — a full-screen roster of a Locker
Room split into `HOSTS` and `AUDIENCE`, entered from the people glyph in the room bar.
`BUILD/locker-room.html:426` has the button (`aria-label="Everyone in the room, 220 people"`) but
it leads nowhere; there is no attendees frame in any component. The spec itself records the code
as *not located* in `APP/lib`, and that is right — see §3.5. So this is a design-only gap: the one
spec in the set with a device capture and no built counterpart. **Decide: build it, or retire the
spec.** It cannot be called a rebuild gap while the room it belongs to does not exist.

---

## 2. Not built, deliberately

The brief's three claims, checked individually. **Two need correcting.**

### 2.1 The `internalUser` / `customerUser` tree — confirmed foreign, with a caveat

`APP/lib/pages/user/` is admin CRUD from another product. Evidence:

- `'Farmer Side'` role option — `APP/lib/pages/user/create.dart:42`, `APP/lib/pages/user/_filter.dart:17`, and the status map at `APP/lib/constants/src/prefs.dart:58` and `:130`.
- Hardcoded Vietnamese throughout — `APP/lib/pages/user/index.dart:34` (`'Tài khoản ${isInternalUser ? 'nội bộ' : 'người dùng'}'`), `:67`, `:165`, `:167`, `:352`; `APP/lib/pages/user/details.dart:52-73` (commented-out `Hồ sơ Farmer` block).
- **No entry point.** Nothing outside `pages/user/` navigates to `CRoute.internalUser` or `CRoute.customerUser`; every `pushNamed` to the child routes originates inside the subtree (`pages/user/index.dart:132,148,295,311`; `pages/user/_popup.dart:71,101`).

**Caveat the brief did not cover:** the same scaffolding leaks into a *live-looking* auth screen.
`APP/lib/pages/access/register.dart` — the widget behind `CRoute.register`
(`routes.dart:156-160`) — carries `MOption(label: 'Farmer Side', value: 'FARMER')` at line 42 and
Vietnamese section headings at lines 21 (`'Thông tin đăng ký'`), 45 (`'Thông tin cá nhân'`) and
56 (`'Nữ'`). It is unreachable (§2b) but `coverage.py` still maps `register → onboarding`, so the
audit reads as though a real registration screen was rebranded. It was not — see §3.7.

### 2.2 `myAccountInfo` / `myAccountPass` — confirmed foreign; **the brief's "no widget" framing is wrong**

Both are real Vietnamese widgets, not empty strings:

- `APP/lib/pages/my_profile/my_account_info.dart:25` — `MyAccountInfo`, app bar `'Thông tin tài khoản'`.
- `APP/lib/pages/my_profile/my_account_pass.dart:43` — `MyAccountPass`, `'Đổi mật khẩu'`.

Neither has a `GoRoute`. `CRoute.myAccountInfo` (`routes.dart:59`) is **actively pushed** at
`APP/lib/core/src/drawer/index.dart:40`, which would throw `GoError: no routes for location` if
reached. It is not reached: the drawer's only consumer is `APP/lib/pages/home.dart:21`, and
`HomePage` (`home.dart:18`) is never constructed anywhere. So it is a latent crash inside dead
code, safe today, and it will bite whoever revives the drawer. Correct to delete with the tree.
`CRoute.myAccountPass` (`routes.dart:60`) is referenced nowhere at all.

### 2.3 `detailData` and `childAccountDetail` — confirmed exactly as stated

- `CRoute.detailData` — `routes.dart:68`. Declared, no `GoRoute`, zero other references in `APP/lib`.
- `CRoute.childAccountDetail` — `routes.dart:81`. Declared, no `GoRoute`, zero other references.

Both are dead strings. Nothing to build. ✅ claim correct as written.

### 2b. Routed but unreachable — five screens that are not gaps

These have routes and widgets but no live navigation into them. Do not demo them, and do not
count them against the build.

| Screen | Route | Why it is unreachable |
|---|---|---|
| `RegisterPage` | `routes.dart:156` | Only link is commented out at `APP/lib/pages/access/login.dart:227`. Sign-up goes to the web (`pre_login.dart:37`). |
| `OTPVerificationPage` | `routes.dart:131` | The only navigator to `CRoute.otpVerification` is `APP/lib/pages/access/forgot_password/index.dart:55`, inside `ForgotPassword` — a dead Vietnamese widget (`index.dart:12`, `'Quên mật khẩu?'` at `:26`) that nothing references. |
| `ResetPassword` | `routes.dart:141` | Reached only from `OTPVerificationPage` (`otp_verification.dart:125`), itself unreachable. |
| `Security` | `routes.dart:417` | Its only caller is commented out — `APP/lib/pages/profile/account_setting/profile_setting.dart:925`. |
| `User` / `CreateUser` / `UserDetails` | `routes.dart:360-415` | No entry point outside the subtree (§2.1). |

**Consequence for the review:** the whole password-reset journey — request, OTP, new password —
is *routed but dead*. What ships is the one-line "go to website" screen at §1.1.
`BUILD/auth.html` builds `Reset password` and `Check your email` frames. Those are proposals,
not rebrands (§3.7).

---

## 3. Built, but a proposal rather than a rebrand

Frames in the prototype with **no working code behind them**. Grouped by how far the gap goes.
This is the section the client most needs, because these frames look identical in quality to the
rebranded ones.

### 3.1 Matches tab — the tab renders nothing ✅ claim confirmed

`APP/lib/pages/access/app_bar/matches_body.dart:14` — `widgetBody: Container()`. The tab is wired
into the bottom nav (`APP/lib/pages/access/app_bar/main_body.dart:18`, `main_page.dart:114`) with
a real icon and label, and opens onto an empty background.

Built: `BUILD/matches.html` — 2 frames (`Fixture list`, `Finished match`), covering `MT-01`,
`MT-02` and `MT-03`. **All of it is new.** There is no fixture model, service or cubit in `APP/lib`.
The one trace of the domain elsewhere is `AlertGroupEnum.matches` (`APP/lib/constants/src/enum.dart:207`),
a notification grouping — not a data source.

> Correction to `SPECS/00-COVERAGE-AUDIT.md` prose (~line 173): it lists `MT-02`/`MT-03` as
> "documented but not rebuilt". They are built. The gap is code, not the rebuild.

### 3.2 Achievements — hardcoded mock data ✅ confirmed; **"navigation commented out" is wrong**

`APP/lib/pages/profile/achievement/achievement_screen.dart:88-101` renders `itemCount: 4` copies
of one literal award — `"MOST VALUED FAN OF THE MATCH"` / `"Feb 16, 2024"`. No cubit, no API call,
no state. The screen is routed (`routes.dart:249`).

The navigation is **not commented out.** The row was *removed from the menu list* —
`APP/lib/pages/profile/profile_body.dart:489-495`, where `profileRows` omits
`ProfileSettingEnums.achievement`. The handler still exists at `profile_body.dart:513-514`, and the
in-code note at `:484-488` records why. Functionally the same outcome, but anyone searching for a
commented-out line will not find one.

### 3.3 Hall of Fame — no route, no page ✅ confirmed, and stronger than stated

`grep -rni "hall.of.fame\|hallOfFame"` across `APP/lib` returns **exactly one hit**, and it is a
comment: `APP/lib/constants/src/enum.dart:96-100`, recording that `hallOfFame` was removed from the
Profile menu because it "had no route, no page and an empty handler". The only surviving string is
`'pages.login.home.userProfile.hall of fame' = 'HALL OF FAME'` in `en.json`.

Built: `BUILD/hall-of-fame.html` — **9 frames**, the second-largest component, covering `HF-01`–`HF-04`
and `AC-01`–`AC-02`.

### 3.4 Merits — no code of any kind

`grep -rni "merit"` across `APP/lib` returns **zero** matches outside a false positive on
`CDimensions.shimmerItems`. Built: `BUILD/merits.html` and `BUILD/merit-detail.html`, 1 frame each,
and neither has a spec.

This corroborates the standing note that there is no awards/honours endpoint — the only trace of
the domain in the whole app is the push type `member_honored`
(`APP/lib/constants/src/enum.dart:167`, `APP/lib/service/src/notification.dart:120`,
`APP/lib/models/src/notification_setting/notification_setting.dart:33`). A notification type is
not a data source.

### 3.5 The in-room Backchat experience — the room does not exist

`APP/lib/pages/back_chat/view/chat_body.dart` (74 lines) is the Backchat **tab**: a header, a
refresh indicator and `BackChatContentView` — a list of Live, Upcoming and Fan Stadium rooms. There
is no in-room screen anywhere in `APP/lib`. There is no audio or realtime stack: `grep` for
`agora|livekit|webrtc|rtc` returns nothing, and `APP/lib/service/src/socket.dart` is an 
unused-looking shell whose only handler is `socket.onError((err) => {})` at line 43.

Built: `BUILD/locker-room.html` (2 frames — `Live room`, `Before you join`) and `BUILD/chat.html`
(1 frame, `Text chat`). **Both are proposals for a runtime that has not been started.** The
attendees screen at §1b belongs to this same missing surface.

What *is* real: browsing, searching, filtering, sorting and scheduling rooms
(`all_locker_rooms/`, `locker_room_editor/`, `back_chat/`), which `all-locker-rooms.html` and
`locker-room-editor.html` rebrand faithfully.

### 3.6 Clubs and child accounts — the payment path ✅ confirmed

No payment code exists in `APP/lib`. There is no Stripe/checkout integration, and the only
payment-adjacent construct is `ErrorResEnum.paymentError = 'credit_not_enough'`
(`APP/lib/constants/src/enum.dart:223,233`), which is the **participation-credit deposit** for
posting an idea — an internal ledger, not money. Its handler is
`APP/lib/utils/src/api.dart:124-140`.

The app's own copy says so in three places:

- `'Registering is done on the Sports Heist website — there is no add-club form in the app.'` — `en.json`, `...no club.detail`, rendered at `APP/lib/pages/profile/profile_body.dart:360` (dispatch) / `:403` (widget).
- `'To add this club, kindly log in to sports heist on desktop'` — rendered at `APP/lib/pages/profile/club/add_club.dart:65`.
- `'To add a child account, please proceed to Sports Heist on Desktop'` — rendered at `APP/lib/pages/profile/child_account/child_account_screen.dart:112`.

Against that, the build contains:

- `BUILD/clubs.html` — **11 frames**, including `Register with a club` (cost, payment method, renewal), `Registered` and `Payment declined`.
- `BUILD/child-account.html` — **17 frames**, the largest component: guest/member fork, details form, verification channel, OTP, set-password, club cascade, membership-ID dialog, `Fee and payment`, ID-check consent, camera permission, ID upload, and the close-account pair.

In code, `child_account_screen.dart` has exactly **two** readings: `ProfileStatus.success` at
line 73, and a shimmer for everything else at line 122. Seventeen frames against two.

Only `BUILD/profile.html:1177` carries the desktop-punt copy. Nothing in `clubs.html` or
`child-account.html` acknowledges that the shipped app hands these journeys to the desktop site.
That is the single most likely misreading in the review.

### 3.7 Auth and onboarding — partly a proposal

| Frames | Reality |
|---|---|
| `auth.html` — `Reset password`, `Check your email` | The routed reset screens are unreachable (§2b); the shipped screen is the "go to website" dead-end. **Proposal.** |
| `launch.html` — `Everything runs off one account` (Log in / Sign up fork) | Sign-up opens the browser (`pre_login.dart:37`). The in-app path is a **proposal**. |
| `onboarding.html` — 4 frames (`Choose your pathway`, `Your details`, `Your identity`, stepper) | Mapped by `coverage.py` to `register`, whose widget is unreachable Vietnamese scaffolding (§2.1). **Proposal**, not a rebrand. |
| `auth.html` — `Get started`, `Log in` | Genuine rebrands. `LoginPage` is live. |

### 3.8 Create Idea — the AI assistant panel

`BUILD/create-idea.html` frame 1 (`Compose`) contains a **"Draft it with the assistant"** block.
`grep -rniE "\bai\b|assistant|openai|gpt"` across `APP/lib` returns **zero** hits, and
`SPECS/02-war-room/02-create-idea-ai-assistant.md` says so itself: *"The AI-assistant panel is
**not located** in the repo."* The rest of `create-idea.html` (compliance, timing, deposit dialog,
posted, error) rebrands `APP/lib/pages/ideas/create_idea.dart` faithfully.

### 3.9 Fourteen built components have no spec at all

`veto`, `action-detail`, `wallet`, `idea-gate`, `merits`, `merit-detail`, `media`, `states`,
`foundations`, `desktop-shell`, `filters-pickers`, `sheets`, plus `all-locker-rooms` and
`locker-room-editor` (atlas-documented only). Most are backed by real code and are fine; the point
is that **nothing checks spec↔component in either direction.** `coverage.py` reads
`manifest.json` and counts `class="frame"` — it never opens a `.md` file. Its `ROUTE_SLUGS` map is
route→component. Treat the audit's *prose* on spec coverage as unverified; it is measurably
stale (it still claims `launch`, `all-locker-rooms`, `locker-room-editor` and `action-detail` are
unbuilt, and that there is no Hall-of-Fame component — all four exist, and `hall-of-fame.html`
has 9 frames).

---

## 4. States a screen has in code but not in the prototype

**Sampled 5 of 42 components**, chosen by size and by tab importance:
`child-account` (17 frames), `clubs` (11), `profile` (4), `war-room` (1), `alerts` (1).
Not exhaustive. The remaining 37 were not checked for state parity.

| # | Component | State present in code | Evidence | Present in build? |
|---|---|---|---|---|
| 4.1 | `profile` | **Load-failed, with a retry button** — icon, `'Something went wrong while loading your profile…'`, `TRY AGAIN` | `APP/lib/pages/profile/profile_body.dart:68` dispatches it; the widget is `buildErrorState()` at `:447-478` | **No.** `BUILD/profile.html:1086` still states *"the only non-success branch is the skeleton, so a failed load shimmers forever"*. That was true; the code has since been fixed. The build is stale against the code. **1 new frame.** |
| 4.2 | `war-room` | **Loading** — full-body shimmer with per-rail card skeletons | `APP/lib/pages/access/app_bar/proposal_body.dart:114`, dispatched at `:203`; per-rail variants at `:558`, `:926` | **No.** `war-room.html` is 1 frame, the populated state only. |
| 4.3 | `war-room` | **Failed** — `WarRoomStatus.fails` | `APP/lib/cubit/index.dart:9` | **No**, and note the code has no explicit branch for it either: it falls through to the shimmer. Worth designing rather than copying. |
| 4.4 | `alerts` | **Loading** — shimmer | `APP/lib/pages/alert/alert_body.dart:145`, dispatched at `:518` | **No.** `alerts.html` covers populated and empty (`Nothing to report`) only. |
| 4.5 | `clubs` / `child-account` | **The desktop-punt terminal state** | §3.6 | **No.** Covered as items 1.3 and 1.4 above. |
| 4.6 | `backchat` (bonus, unsampled tab) | `BackChatRoomStatus.failure` is **declared and never checked** | Declared `APP/lib/cubit/index.dart:101`; every comparison in `pages/back_chat/**` tests only `inProcess` or `success` | Neither in code nor in build. A room-list load failure currently shows nothing. |

`child-account` and `clubs` produced no code-side states the build lacks, for the plain reason
that the code has almost no states: `child_account_screen.dart` has exactly two
(`:73` success, `:122` shimmer). The build is far ahead, not behind.

### 4b. States in the prototype with nothing behind them

The reverse direction, and worth flagging so the client is not told the app degrades gracefully:

- **Offline.** `BUILD/states.html` has an `Offline and stale data` section and a `You're offline`
  error. `BUILD/launch.html` has `We can't reach the server`. **There is no connectivity handling
  anywhere in `APP/lib`** — no `connectivity_plus`, no `SocketException` handling, no offline
  branch. `grep -rniE "connectivity|offline|SocketException"` returns 3 hits, all of them
  unrelated (`main.dart:42,45` global error hooks; `service/src/socket.dart:43` an empty handler).
- **Permission-denied.** `BUILD/upload.html` has `Camera permission`; `BUILD/child-account.html`
  has `Allow the camera`; `BUILD/launch.html` has `Alerts are off`. In code the only permission
  path is `APP/lib/core/src/qr_view.dart:138-142`, which shows a raw `SnackBar` reading
  `'no Permission'` — and `WQRScan` (`qr_view.dart:33`) is never instantiated. The upload picker
  (`APP/lib/core/src/form/src/upload.dart:475`) has no denied branch at all.

Both are good proposals. Neither is a rebrand.

---

## Method and limits

- **Code:** read `APP/lib/constants/src/routes.dart` in full (438 lines, 33 routed widgets), then
  swept `APP/lib/**` for `MaterialPageRoute`, `CupertinoPageRoute`, `PageRouteBuilder`,
  `Navigator.push*`, `showDialog`, `showModalBottomSheet`, `showGeneralDialog`, `showDatePicker`,
  `showTimePicker`. Result worth recording: **`Navigator.push` appears zero times.** Only two
  imperative full-screen pushes exist, both in `APP/lib/core/src/image_widget.dart` (`:34` single
  photo, `:150` gallery), both building anonymous inline `Scaffold`s — and both are already
  rebuilt in `BUILD/media.html` (9 frames). Everything else imperative is sheets and dialogs,
  nearly all through `UDialog` (`APP/lib/utils/src/dialogs.dart:15`), and the `sheets`, `dialogs`,
  `forms`, `upload` and `filters-pickers` components cover them well.
- **Specs:** all 79 screen specs mapped by hand against the 42 components. One screen spec has no
  component (`BC-02`). `03-backchat/00-backchat-component-atlas.md` is a reference document, not a
  screen, and is correctly uncovered. Superseded/duplicate specs found: `WR-21`≡`WR-19`,
  `NT-02`≡`PA-02`, `MT-03`/`PA-04`/`PR-02`/`HF-04`/`AU-12` are scroll or fill states of their
  siblings, `WR-09`/`WR-10`≡`WR-01`, `CL-01`≡`CA-11`, `CL-03`≡`CA-12`.
- **Build:** `coverage.py` re-run this pass; it reported *"Rebuilt? column was already current"*.
  Only the generated block of `SPECS/00-COVERAGE-AUDIT.md` is trusted. The prose above it is
  demonstrably stale and is not used here except where explicitly corrected.
- **Marked as inference, not verified:** all job-size estimates in §1; the reading that §1's five
  screens are "cheap"; the judgement that `BC-02` should be deferred rather than built.
- **Not checked:** state parity for the 37 components outside the §4 sample; the desktop web app;
  anything outside `APP/lib` (native iOS/Android shells, backend).
