#!/usr/bin/env python3
"""Validate _assets/journeys.json against the screens that actually exist.

A journey step names a screen id: `slug` for a single-page component, `slug/N` for a
framed one. Components gain and lose frames as they are built, so a hand-written step
goes stale silently — the prototype just skips it and the client sees a journey with a
hole in it. This fails loudly instead.

  python3 _assets/check-journeys.py           # validate
  python3 _assets/check-journeys.py --ids     # print every valid screen id
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def screen_ids():
    """{id: human label} for every screen the prototype can show."""
    man = json.load(open(os.path.join(HERE, "manifest.json")))
    out = {}
    for g in man["groups"]:
        for it in g["items"]:
            slug = it["slug"]
            p = os.path.join(ROOT, f"{slug}.html")
            if not os.path.exists(p):
                continue
            # Must mirror frames_of() in build-prototype.py exactly. A stricter regex here
            # (requiring class="frame") missed components using class="fr frame", so this
            # reported ids the prototype then silently dropped mid-journey.
            markup = open(p, encoding="utf-8").read()
            _m = re.search(r"<main[^>]*>(.*)</main>", markup, re.S)
            markup = _m.group(1) if _m else markup   # frames live in <main>; a
            # `<section class="frame">` inside a script comment is not a screen
            titles = []
            for m in re.finditer(r'<section[^>]*class="[^"]*\bframe\b[^"]*"[^>]*>', markup):
                d = re.search(r'data-title="([^"]*)"', m.group(0))
                titles.append(d.group(1) if d else f"Screen {len(titles)+1}")
            if titles:
                for i, t in enumerate(titles):
                    out[f"{slug}/{i}"] = f"{it['title']} — {t}"
            else:
                out[slug] = it["title"]
    return out


def main():
    ids = screen_ids()
    if "--ids" in sys.argv:
        for k in sorted(ids):
            print(f"  {k:28} {ids[k]}")
        print(f"\n  {len(ids)} screen ids")
        return 0

    p = os.path.join(HERE, "journeys.json")
    if not os.path.exists(p):
        print("  journeys.json absent")
        return 0
    data = json.load(open(p))
    groups = data.get("groups", []) if isinstance(data, dict) else data

    bad, dupes, empty, steps, seen = [], [], [], 0, set()
    njourneys = 0
    for g in groups:
        for j in g.get("journeys", []):
            njourneys += 1
            jid = j.get("id", "(no id)")
            if jid in seen:
                dupes.append(jid)
            seen.add(jid)
            ss = j.get("steps", [])
            if len(ss) < 2:
                empty.append(f"{jid} ({len(ss)} step)")
            for s in ss:
                steps += 1
                if s.get("screen") not in ids:
                    bad.append(f"{g.get('name','?')} / {jid} -> {s.get('screen')!r}")

    print(f"  {len(groups)} groups · {njourneys} journeys · {steps} steps")
    ok = True
    if bad:
        ok = False
        print(f"  {len(bad)} step(s) point at a screen that does not exist:")
        for b in bad[:40]:
            print("    " + b)
        if len(bad) > 40:
            print(f"    … and {len(bad)-40} more")
    if dupes:
        ok = False
        print(f"  duplicate journey ids: {', '.join(sorted(set(dupes)))}")
    if empty:
        ok = False
        print(f"  {len(empty)} journey(s) with fewer than 2 steps: {', '.join(empty[:10])}")
    if ok:
        print("  every step resolves · no duplicate ids · no stubs")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
