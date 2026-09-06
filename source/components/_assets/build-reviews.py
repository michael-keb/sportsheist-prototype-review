#!/usr/bin/env python3
"""
Build a review page for every component in the library, plus an index.

    python3 _assets/build-reviews.py            # build everything that exists
    python3 _assets/build-reviews.py merits     # build one

Each component `<slug>.html` becomes `<slug>-review.html`:
  * the component's CSS is scoped under `.mk` so it cannot collide with the shell
  * `<main>` is wrapped in a scroll container, so any pinned chrome outside it stays pinned
  * `<slug>.notes.html` supplies the review copy (see NOTES-CONTRACT.md)
  * the side menu is generated from manifest.json, with the current component marked
"""

import json, re, sys, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCOPE = ".mk"

FIGMA_LABEL = {
    "designed": "In Figma",
    "partial":  "Part in Figma",
    "new":      "New",
    "sampled":  "Sampled",
}

# ----------------------------------------------------------------- CSS scoping
def split_rules(text):
    out, i, n = [], 0, len(text)
    while i < n:
        while i < n and text[i] in " \t\r\n":
            i += 1
        if text.startswith("/*", i):
            j = text.find("*/", i)
            i = (j + 2) if j != -1 else n
            continue
        if i >= n:
            break
        brace = text.find("{", i)
        if brace == -1:
            break
        prelude = text[i:brace].strip()
        depth, j = 1, brace + 1
        while j < n and depth:
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
            j += 1
        inner = text[brace + 1:j - 1]
        out.append(("at", prelude, inner) if prelude.startswith("@") else ("rule", prelude, inner))
        i = j
    return out


def scope_selector(sel):
    parts = []
    for s in (x.strip() for x in sel.split(",")):
        if not s:
            continue
        if s in (":root", "body"):
            parts.append(SCOPE)
        elif s == "html":
            continue
        else:
            parts.append(f"{SCOPE} {s}")
    return parts


def emit(rules, indent=""):
    lines = []
    for kind, prelude, inner in rules:
        if kind == "at":
            if prelude.lstrip("@").split()[0] in ("keyframes", "font-face", "-webkit-keyframes"):
                lines.append(f"{indent}{prelude}{{{inner}}}")   # leave verbatim
                continue
            body = emit(split_rules(inner), indent + "  ")
            if body.strip():
                lines.append(f"{indent}{prelude}{{\n{body}{indent}}}")
        else:
            sels = scope_selector(prelude)
            if not sels:
                continue
            decls = re.sub(r"\s+", " ", " ".join(l.strip() for l in inner.strip().splitlines())).strip()
            if decls:
                lines.append(f"{indent}{','.join(sels)}{{{decls}}}")
    return "\n".join(lines) + ("\n" if lines else "")


# ----------------------------------------------------------------- manifest
def load_manifest():
    with open(os.path.join(HERE, "manifest.json")) as fh:
        return json.load(fh)


def all_items(man):
    for g in man["groups"]:
        for it in g["items"]:
            yield g, it


def exists(slug):
    return os.path.isfile(os.path.join(ROOT, f"{slug}.html"))


# ----------------------------------------------------------------- rendering
def sidebar(man, current):
    out = ['<nav class="side" aria-label="Component library">']
    out.append('  <div class="side__group">')
    out.append('    <p class="side__title">Library</p>')
    out.append('    <ul>')
    built_n = sum(1 for _, i in all_items(man) if exists(i["slug"]))
    if current is None:
        out.append(f'      <li><span class="side__item" aria-current="page">Overview'
                   f'<span class="side__tag side__tag--new">This page</span></span></li>')
    else:
        out.append(f'      <li><a class="side__item" href="index.html">Overview'
                   f'<span class="side__tag">{built_n} built</span></a></li>')
    out.append('    </ul>')
    out.append('  </div>')

    for g in man["groups"]:
        out.append('  <div class="side__group">')
        out.append(f'    <p class="side__title">{html.escape(g["name"])}</p>')
        out.append('    <ul>')
        for it in g["items"]:
            slug, title = it["slug"], html.escape(it["title"])
            tag = FIGMA_LABEL.get(it.get("figma", ""), "")
            if slug == current:
                out.append(f'      <li><span class="side__item" aria-current="page">{title}'
                           f'<span class="side__tag side__tag--new">This page</span></span></li>')
            elif exists(slug):
                out.append(f'      <li><a class="side__item" href="{slug}-review.html">{title}'
                           f'<span class="side__tag">{tag}</span></a></li>')
            else:
                out.append(f'      <li><span class="side__item side__item--muted">{title}'
                           f'<span class="side__tag">Not started</span></span></li>')
        out.append('    </ul>')
        out.append('  </div>')
    out.append('</nav>')
    return "\n".join(out)


def toc(notes_html):
    """Build the on-this-page menu from the notes' sections."""
    rows = re.findall(r'<section id="([^"]+)">(.*?)</section>', notes_html, re.S)
    items = []
    for sid, body in rows:
        m = re.search(r"<h2[^>]*>(.*?)</h2>", body, re.S)
        label = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else sid.title()
        if len(label) > 44:
            label = label[:42].rstrip() + "…"
        items.append(f'    <li><a class="side__item" href="#{sid}">{html.escape(label)}</a></li>')
    if not items:
        return ""
    return ('  <div class="side__group">\n'
            '    <p class="side__title">On this page</p>\n'
            '    <ul id="toc">\n' + "\n".join(items) + '\n    </ul>\n  </div>')


def default_notes(title):
    return (f'<p class="dek">{html.escape(title)} — review notes not written yet.</p>\n'
            '<section id="overview">\n'
            '  <p class="rv-eyebrow">What you\'re looking at</p>\n'
            f'  <h2>{html.escape(title)}</h2>\n'
            '  <p>This component is built but its review notes are outstanding. The screen beside '
            'this text is live and interactive.</p>\n'
            '</section>\n')


FRAME_CLS = ("frame",)   # only this marks a screen. never add a class a control might carry
                         # (`phone` used to be here and matched `class="ctl phone"`, emitting phantom devices)

def split_frames(markup):
    """Return [(title, html), …] for each screen, or [] when the component is one screen.

    A screen boundary is <section class="frame"> / class="phone">, optionally carrying
    data-title. Kits that stack specimens inside one screen have no such wrapper and
    stay a single device.
    """
    pat = re.compile(
        r'<(section|div)\b[^>]*class="[^"]*\b(?:' + "|".join(FRAME_CLS) + r')\b[^"]*"[^>]*>',
        re.I)
    starts = [m for m in pat.finditer(markup)]
    if len(starts) < 2:
        return []
    frames = []
    for i, m in enumerate(starts):
        tag = m.group(1)
        # walk to the matching close tag
        depth, j = 1, m.end()
        open_re = re.compile(r'<' + tag + r'\b', re.I)
        close_re = re.compile(r'</' + tag + r'\s*>', re.I)
        while depth and j < len(markup):
            o = open_re.search(markup, j); c = close_re.search(markup, j)
            if not c: break
            if o and o.start() < c.start():
                depth += 1; j = o.end()
            else:
                depth -= 1; j = c.end()
        inner = markup[m.end():j]
        inner = re.sub(r'</(?:section|div)\s*>\s*$', '', inner)
        t = re.search(r'data-title="([^"]*)"', m.group(0))
        if t:
            title = t.group(1)
        else:
            h = re.search(r'<(?:h1|h2|h3)[^>]*>(.*?)</(?:h1|h2|h3)>', inner, re.S)
            title = re.sub(r'<[^>]+>', '', h.group(1)).strip() if h else f"Screen {i+1}"
        title = re.sub(r'\s+', ' ', title)[:48]
        frames.append((title, inner))
    return frames


def screens_menu(frames):
    """The component's own screens, deep-linked. This is what makes each menu specific."""
    if not frames:
        return ""
    rows = "\n".join(
        f'      <li><a class="side__item" href="#scr-{i}">{html.escape(t)}'
        f'<span class="side__tag">{i:02d}</span></a></li>'
        for i, (t, _) in enumerate(frames, 1))
    return ('  <div class="side__group">\n'
            f'    <p class="side__title">Screens · {len(frames)}</p>\n'
            '    <ul>\n' + rows + '\n    </ul>\n  </div>')


def build_one(man, slug, title, figma, shell_css, wide=False):
    src = open(os.path.join(ROOT, f"{slug}.html")).read()

    css_blocks = re.findall(r"<style>(.*?)</style>", src, re.S)
    body_m = re.search(r"<body>(.*?)</body>", src, re.S)
    if not css_blocks or not body_m:
        raise SystemExit(f"{slug}.html: expected at least one <style> and a <body>")

    # concatenate every stylesheet — a component with two <style> blocks used to lose the second
    scoped = emit(split_rules("\n".join(css_blocks)))
    body = body_m.group(1)
    scripts = re.findall(r"<script>(.*?)</script>", body, re.S)
    markup = re.sub(r"<script>.*?</script>", "", body, flags=re.S).strip()

    # the scrolling region must exclude anything pinned to the bottom
    if "<main" in markup:
        markup = re.sub(r"(<main\b.*?</main>)", r'<div class="mk__scroll">\1</div>',
                        markup, count=1, flags=re.S)
    else:
        markup = f'<div class="mk__scroll">{markup}</div>'

    # chrome that sits outside <main> (tab bar, composer, dock) belongs in every frame
    pinned = ""
    outside = re.sub(r"<main\b.*?</main>", "", body_m.group(1), flags=re.S)
    outside = re.sub(r"<script>.*?</script>", "", outside, flags=re.S).strip()
    if outside:
        pinned = outside

    notes_path = os.path.join(ROOT, f"{slug}.notes.html")
    notes = open(notes_path).read() if os.path.isfile(notes_path) else default_notes(title)
    dek_m = re.search(r'<p class="dek">.*?</p>', notes, re.S)
    dek = dek_m.group(0) if dek_m else ""
    notes_body = notes.replace(dek, "", 1) if dek else notes

    frames = [] if wide else split_frames(markup)

    if frames:
        cards = []
        for i, (ftitle, fhtml) in enumerate(frames, 1):
            cards.append(
                f'      <figure class="scr" id="scr-{i}">\n'
                f'        <figcaption class="scr__cap"><span class="scr__n">{i:02d}</span>'
                f'{html.escape(ftitle)}</figcaption>\n'
                '        <div class="device device--multi">\n'
                '          <div class="device__island"></div>\n'
                '          <div class="device__screen">\n'
                f'<div class="mk"><div class="mk__scroll">{fhtml}</div>{pinned}</div>\n'
                '          </div>\n'
                '        </div>\n'
                '      </figure>\n')
        stage = ('    <div class="screens">\n'
                 f'      <p class="screens__lede">{len(frames)} screens · each shown in its own '
                 'frame, live and interactive.</p>\n'
                 '      <div class="screens__grid">\n' + "".join(cards) +
                 '      </div>\n    </div>\n')
    elif wide:
        stage = (
            '    <div class="widecol">\n'
            '      <div class="widestage">\n'
            '        <div class="mk mk--wide">\n' + markup + '\n</div>\n'
            '      </div>\n'
            '      <p class="stage__hint stage__hint--wide">Live and interactive. This is a '
            'full-width reference sheet, not a phone screen.</p>\n'
            '    </div>\n'
        )
    else:
        stage = (
            '    <div class="stagecol">\n'
            '      <div class="stage">\n'
            '        <div class="device" id="device">\n'
            '          <div class="device__island"></div>\n'
            '          <div class="device__screen">\n'
            '<div class="mk">\n' + markup + '\n</div>\n'
            '          </div>\n'
            '        </div>\n'
            '        <div class="stage__controls">\n'
            '          <div class="seg" role="group" aria-label="Device width">\n'
            '            <button type="button" data-w="375" aria-pressed="true">375</button>\n'
            '            <button type="button" data-w="414" aria-pressed="false">414</button>\n'
            '            <button type="button" data-w="430" aria-pressed="false">430</button>\n'
            '          </div>\n'
            '        </div>\n'
            '        <p class="stage__hint">Live and interactive — scroll the screen, tap the '
            'controls, switch width.</p>\n'
            '      </div>\n'
            '    </div>\n'
        )

    wide_cls = " layout--wide" if (wide or frames) else ""
    platform = "Desktop · responsive" if wide else "iOS 375×812"
    component_js = ""
    if scripts:
        component_js = "<script>\n" + "\n".join(x.strip() for x in scripts) + "\n</script>"

    side = sidebar(man, slug)
    sm = screens_menu(frames)
    if sm:
        side = side.replace('<nav class="side" aria-label="Component library">',
                            '<nav class="side" aria-label="Component library">\n' + sm, 1)
    t = toc(notes)
    if t:
        side = side.replace("</nav>", t + "\n</nav>")

    page = f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SportsHeist — {html.escape(title)} · component review</title>
<style>
{shell_css}
/* ============================================================
   COMPONENT — every selector scoped under .mk
   ============================================================ */
{scoped}
.mk{{position:absolute;inset:0;overflow:hidden}}
.mk--wide{{position:static;overflow:visible;border-radius:12px}}
.mk--wide .mk__scroll{{position:static;overflow:visible}}
.mk--wide .tabbar{{display:none}}
.mk__scroll{{
  position:absolute;inset:0;
  overflow-y:auto;overflow-x:hidden;-webkit-overflow-scrolling:touch;
  overscroll-behavior:contain;
}}
.mk__scroll::-webkit-scrollbar{{width:0}}
/* pinned chrome lives outside the scroller */
.mk .tabbar{{position:absolute;z-index:50}}
</style>

<header class="masthead">
  <div class="wrap">
    <div class="masthead__top">
      <span class="mark">SportsHeist</span>
      <span class="chip">For client review</span>
    </div>
    <h1>{html.escape(title)}</h1>
    {dek}
    <div class="meta">
      <span><b>Component</b> {html.escape(slug)}</span>
      <span><b>Figma</b> {FIGMA_LABEL.get(figma, "—")}</span>
      <span><b>Source</b> SportHeist (Copy) · dark mode</span>
      <span><b>Platform</b> {platform}</span>
    </div>
  </div>
</header>

<div class="wrap">
  <div class="layout{wide_cls}">
{side}

{stage}

    <div class="col">
{notes_body}
      <footer>
        <p>Built from the <code>SportHeist (Copy)</code> dark-mode exports. Colours and geometry are
        sampled from those frames, photography is lifted from them and embedded here, so this page
        works offline with no external requests. Comment against the anatomy row names.</p>
      </footer>
    </div>
  </div>
</div>

<script>
(function(){{
  'use strict';
  var device = document.getElementById('device');
  var seg = document.querySelector('.seg');
  if (seg) seg.addEventListener('click', function(e){{
    var b = e.target.closest('button'); if(!b) return;
    seg.querySelectorAll('button').forEach(function(x){{ x.setAttribute('aria-pressed', String(x===b)); }});
    device.style.width = b.dataset.w + 'px';
  }});

  var links = Array.prototype.slice.call(document.querySelectorAll('#toc a'));
  var byId = {{}}; links.forEach(function(a){{ byId[a.getAttribute('href').slice(1)] = a; }});
  var targets = links.map(function(a){{ return document.getElementById(a.getAttribute('href').slice(1)); }}).filter(Boolean);
  if ('IntersectionObserver' in window && targets.length){{
    var seen = {{}};
    var io = new IntersectionObserver(function(entries){{
      entries.forEach(function(e){{ seen[e.target.id] = e.isIntersecting ? e.intersectionRatio : 0; }});
      var best=null,bv=0;
      Object.keys(seen).forEach(function(k){{ if(seen[k]>bv){{bv=seen[k];best=k;}} }});
      links.forEach(function(a){{ a.removeAttribute('aria-current'); }});
      if (best && byId[best]) byId[best].setAttribute('aria-current','true');
    }}, {{ rootMargin:'-15% 0px -55% 0px', threshold:[0,.25,.5,1] }});
    targets.forEach(function(t){{ io.observe(t); }});
  }}
}})();
</script>
{component_js}
"""
    out = os.path.join(ROOT, f"{slug}-review.html")
    open(out, "w").write(page)
    return out, len(page)


def build_index(man, shell_css):
    built = [(g, i) for g, i in all_items(man) if exists(i["slug"])]
    total = sum(1 for _ in all_items(man))

    cards = []
    for g in man["groups"]:
        rows = []
        for it in g["items"]:
            slug, title = it["slug"], html.escape(it["title"])
            tag = FIGMA_LABEL.get(it.get("figma", ""), "")
            if exists(slug):
                rows.append(f'<li><a class="ix__row" href="{slug}-review.html"><span class="ix__name">{title}</span>'
                            f'<span class="ix__tag">{tag}</span></a></li>')
            else:
                rows.append(f'<li><span class="ix__row ix__row--todo"><span class="ix__name">{title}</span>'
                            f'<span class="ix__tag">Not started</span></span></li>')
        note = f'<p class="ix__note">{html.escape(g.get("note",""))}</p>'
        cards.append(f'<section class="ix__group"><h2>{html.escape(g["name"])}</h2>{note}'
                     f'<ul class="ix__list">{"".join(rows)}</ul></section>')

    page = f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SportsHeist — component library</title>
<style>
{shell_css}
.ix{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:22px 22px;align-items:start;padding:36px 0 80px}}
.ix__group h2{{margin:0 0 4px;font-size:17px;letter-spacing:-.015em}}
.ix__note{{margin:0 0 10px;font-size:13px;color:var(--ink-3);min-height:1.35em}}
.ix__list{{list-style:none;margin:0;padding:0;border:1px solid var(--rule);border-radius:10px;overflow:hidden;background:var(--panel)}}
.ix__list li + li .ix__row{{border-top:1px solid var(--rule-soft)}}
.ix__row{{display:flex;align-items:center;gap:10px;padding:11px 14px;text-decoration:none;color:var(--ink);font-size:14px}}
.ix__row:hover{{background:var(--paper)}}
.ix__row--todo{{color:var(--ink-3)}}
.ix__row--todo:hover{{background:transparent}}
.ix__name{{flex:1;min-width:0}}
.ix__tag{{font-family:var(--f-mono);font-size:9.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3)}}
</style>

<header class="masthead">
  <div class="wrap">
    <div class="masthead__top">
      <span class="mark">SportsHeist</span>
      <span class="chip">For client review</span>
    </div>
    <h1>Component library</h1>
    <p class="dek">{html.escape(man["subtitle"])}. Every screen below is a live, interactive build in
    the new dark-mode language, with colours and geometry sampled from the Figma exports rather than
    approximated. {len(built)} of {total} built.</p>
    <div class="meta">
      <span><b>Source</b> {html.escape(man["source"])}</span>
      <span><b>Built</b> {len(built)} of {total}</span>
      <span><b>Platform</b> iOS 375×812</span>
    </div>
  </div>
</header>

<div class="wrap">
  <div class="layout layout--wide">
{sidebar(man, None)}
    <div class="ix">{"".join(cards)}</div>
  </div>
</div>
"""
    out = os.path.join(ROOT, "index.html")
    open(out, "w").write(page)
    return out, len(built), total


def main():
    man = load_manifest()
    shell_css = open(os.path.join(HERE, "review-shell.css")).read()
    want = sys.argv[1:] or None

    ok, skipped = [], []
    for g, it in all_items(man):
        slug = it["slug"]
        if want and slug not in want:
            continue
        if not exists(slug):
            skipped.append(slug)
            continue
        try:
            path, size = build_one(man, slug, it["title"], it.get("figma", ""), shell_css,
                                   wide=bool(it.get("wide")))
            notes = "notes" if os.path.isfile(os.path.join(ROOT, f"{slug}.notes.html")) else "NO NOTES"
            ok.append(f"  {os.path.basename(path):<34} {size//1024:>4} KB  {notes}")
        except SystemExit as e:
            skipped.append(f"{slug} ({e})")

    idx, built, total = build_index(man, shell_css)
    print("built:")
    print("\n".join(ok) if ok else "  (none)")
    print(f"index: {os.path.basename(idx)} — {built}/{total} components")
    if skipped:
        print("not yet built:", ", ".join(skipped))


if __name__ == "__main__":
    main()
