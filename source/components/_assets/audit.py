#!/usr/bin/env python3
"""Contract audit across every component. Modifier-aware."""
import glob, re, os, sys

def css_of(s):
    return "\n".join(re.findall(r"<style>(.*?)</style>", s, re.S))

def pos_classes(css):
    """class -> position value, for classes that declare one"""
    out={}
    for m in re.finditer(r"\.([A-Za-z0-9_-]+)[^{,]*\{([^}]*)\}", css):
        p=re.search(r"position:\s*([a-z-]+)", m.group(2))
        if p: out.setdefault(m.group(1), p.group(1))
    return out

rows=[]
for f in sorted(glob.glob("*.html")):
    # build outputs, not components
    if "-review" in f or f in ("index.html","prototype.html") or ".notes." in f: continue
    s=open(f).read(); css=css_of(s); iss=[]
    if "<link" in s: iss.append("has <link>")
    if not css: iss.append("no <style>")
    if not re.search(r"prefers-reduced-motion", s): iss.append("no reduced-motion guard")
    if not os.path.isfile(f[:-5]+".notes.html"): iss.append("no notes file")

    pc = pos_classes(css)
    main = re.search(r"<main\b.*?</main>", s, re.S)
    if main:
        for m in re.finditer(r'class="([^"]+)"', main.group(0)):
            names = m.group(1).split()
            # the winning position is the last declaring class in the element's list
            decl = [pc[n] for n in names if n in pc]
            if decl and decl[-1] == "fixed":
                iss.append(f"position:fixed inside <main>: .{names[0]}")
                break
    rows.append((f, iss))

bad=[(f,i) for f,i in rows if i]
for f,i in bad: print(f"  {f:24} {'; '.join(i)}")
print(f"\n  {len(rows)} components audited — {'all clean' if not bad else str(len(bad))+' with issues'}")
