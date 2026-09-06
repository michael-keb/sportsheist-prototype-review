#!/usr/bin/env python3
"""Check flows.json against the components as they are now.

Hotspot destinations are `slug/frameIndex`. Appending a frame is harmless, but
INSERTING one shifts every later index, so a hotspot silently starts pointing at
the wrong screen — it still navigates, it just lands somewhere wrong, which is
worse than a dead link because nothing looks broken.

First run writes _assets/flows.lock.json recording what each destination resolved
to. Later runs compare against it and report drift.

  python3 _assets/check-flows.py          # check, and report drift
  python3 _assets/check-flows.py --bless   # accept the current state as correct
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FLOWS = os.path.join(HERE, "flows.json")
LOCK = os.path.join(HERE, "flows.lock.json")


def titles(slug):
    p = os.path.join(ROOT, f"{slug}.html")
    if not os.path.exists(p):
        return None
    out = []
    for m in re.finditer(r'<section[^>]*class="[^"]*\bframe\b[^"]*"[^>]*>', open(p, encoding="utf-8").read()):
        t = re.search(r'data-title="([^"]*)"', m.group(0))
        out.append(t.group(1) if t else "")
    return out


def resolve(dest, cache):
    """dest -> (ok, description)"""
    slug, _, idx = dest.partition("/")
    if slug not in cache:
        cache[slug] = titles(slug)
    ts = cache[slug]
    if ts is None:
        return False, "NO SUCH COMPONENT"
    if idx == "":
        return True, "(single page)" if not ts else f"(whole component, {len(ts)} frames)"
    if not idx.isdigit():
        return False, f"bad index {idx!r}"
    i = int(idx)
    if i >= len(ts):
        return False, f"index {i} out of range ({len(ts)} frames)"
    return True, ts[i]


def main():
    if not os.path.exists(FLOWS):
        print("  flows.json absent"); return 0
    flows = json.load(open(FLOWS))
    lock = json.load(open(LOCK)) if os.path.exists(LOCK) else {}

    cache, cur, broken = {}, {}, []
    n = 0
    for key, hs in flows.items():
        for h in hs:
            n += 1
            dest = h["to"]
            ok, what = resolve(dest, cache)
            if not ok:
                broken.append(f"    {key} -> {dest}: {what}")
            else:
                cur[dest] = what

    drift = [(d, lock[d], cur[d]) for d in sorted(cur) if d in lock and lock[d] != cur[d]]

    print(f"  {len(flows)} screens wired · {n} hotspots · {len(cur)} distinct destinations")
    if broken:
        print(f"  {len(broken)} BROKEN destination(s):")
        print("\n".join(broken))
    if drift:
        print(f"  {len(drift)} destination(s) now point at a DIFFERENT screen:")
        for d, was, now in drift:
            print(f"    {d}: was {was!r} -> now {now!r}")
    if not lock:
        print("  no lock file yet — run with --bless to record the current state")
    elif not broken and not drift:
        print("  no drift — every destination still resolves to the same screen")

    if "--bless" in sys.argv:
        json.dump(cur, open(LOCK, "w"), indent=1, sort_keys=True)
        open(LOCK, "a").write("\n")
        print(f"  blessed {len(cur)} destinations into flows.lock.json")
        return 0

    return 1 if (broken or drift) else 0


if __name__ == "__main__":
    sys.exit(main())
