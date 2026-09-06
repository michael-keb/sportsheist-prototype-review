#!/usr/bin/env python3
"""Build desktop screenshot review pages from Branding -Desktop.

One HTML component per folder. Each PNG becomes one <section class="frame">
so the prototype shows one page per tab (no stacked scrolling).

Also copies/compresses images into components/desktop-shots/ for deploy.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from html import unescape
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent  # components/
SHOTS_SRC = ROOT.parent.parent / "Branding -Desktop" / "Desktop Screenshots"
SHOTS_OUT = ROOT / "desktop-shots"
MANIFEST_OUT = HERE / "desktop-shots-manifest.json"

APP_MAP = {
    "User": ("fan", "Fan app"),
    "Managment": ("management", "Management"),  # folder spelling as shipped
    "Management": ("management", "Management"),
    "DSC": ("dsc", "DSC Labs"),
}


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "page"


def titleize(name: str) -> str:
    name = re.sub(r"\.(png|jpg|jpeg|webp)$", "", name, flags=re.I)
    name = name.replace("_", " ").replace("-", " ")
    name = re.sub(r"\s+", " ", name).strip()
    # keep existing capitals where useful; otherwise title case
    if name != name.lower() and name != name.upper():
        return name
    return name.title()


def compress_to(src: Path, dest: Path, max_w: int = 1600) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    # Prefer JPEG for size; keep PNG if conversion fails.
    jpg = dest.with_suffix(".jpg")
    try:
        # Resize with sips then convert to jpeg
        tmp = dest.with_suffix(".tmp.png")
        shutil.copy2(src, tmp)
        subprocess.run(
            ["sips", "-Z", str(max_w), str(tmp)],
            check=True, capture_output=True,
        )
        subprocess.run(
            ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "70",
             str(tmp), "--out", str(jpg)],
            check=True, capture_output=True,
        )
        tmp.unlink(missing_ok=True)
        if dest.exists() and dest != jpg:
            dest.unlink(missing_ok=True)
    except Exception:
        shutil.copy2(src, dest)


REBRAND_MARK = "REBRANDED:"


def is_rebranded(path: Path) -> bool:
    """True once a page has been rebuilt by hand on the dark-mode kit.

    Rebuilt pages carry a `REBRANDED:` comment in their head. They keep the
    generated frame order and data-titles, so they stay drop-in compatible
    with the prototype — but regenerating them would throw the work away.
    """
    if not path.is_file():
        return False
    try:
        return REBRAND_MARK in path.read_text(encoding="utf-8")[:4000]
    except OSError:
        return False


def frame_titles(path: Path) -> list[str]:
    """The data-titles a hand-rebuilt page actually carries."""
    try:
        html = path.read_text(encoding="utf-8")
    except OSError:
        return []
    return [unescape(t) for t in
            re.findall(r'<section class="frame"[^>]*data-title="([^"]*)"', html)]


def collect():
    if not SHOTS_SRC.is_dir():
        raise SystemExit(f"Missing screenshots folder: {SHOTS_SRC}")

    groups = []  # for prototype manifest injection
    if SHOTS_OUT.exists():
        shutil.rmtree(SHOTS_OUT)
    SHOTS_OUT.mkdir(parents=True)

    for app_dir in sorted(SHOTS_SRC.iterdir()):
        if not app_dir.is_dir():
            continue
        app_key, app_label = APP_MAP.get(app_dir.name, (slugify(app_dir.name), app_dir.name))
        for section in sorted(app_dir.iterdir()):
            if not section.is_dir():
                continue
            images = sorted(
                [p for p in section.iterdir()
                 if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}],
                key=lambda p: p.name.lower(),
            )
            if not images:
                continue

            sec_slug = slugify(section.name)
            comp_slug = f"desktop-{app_key}-{sec_slug}"
            frames = []
            img_refs = []

            for i, img in enumerate(images):
                safe = slugify(img.stem) or f"screen-{i+1}"
                rel = f"{app_key}/{sec_slug}/{safe}.jpg"
                out = SHOTS_OUT / rel
                compress_to(img, out)
                # if jpeg written
                if out.with_suffix(".jpg").exists():
                    rel = f"{app_key}/{sec_slug}/{safe}.jpg"
                elif out.exists():
                    rel = f"{app_key}/{sec_slug}/{out.name}"
                title = titleize(img.name)
                frames.append(title)
                img_refs.append((title, rel))

            comp_path = ROOT / f"{comp_slug}.html"
            if is_rebranded(comp_path):
                # The page has been rebuilt on the dark-mode kit by hand.
                # Its frame order and data-titles match what this script
                # would emit, so prototype indices and flows.json still
                # line up — but the file itself must not be overwritten.
                frames = frame_titles(comp_path) or frames
                print(f"  {comp_slug:40} {len(frames):3} screens   REBRANDED — kept")
            else:
                html = build_html(app_label, titleize(section.name), img_refs)
                comp_path.write_text(html, encoding="utf-8")
                print(f"  {comp_slug:40} {len(frames):3} screens")

            groups.append({
                "app": app_key,
                "appLabel": app_label,
                "slug": comp_slug,
                "title": titleize(section.name),
                "frames": frames,
                "wide": True,
                "figma": "designed",
            })

    MANIFEST_OUT.write_text(json.dumps({"items": groups}, indent=2), encoding="utf-8")
    # size report
    total = sum(p.stat().st_size for p in SHOTS_OUT.rglob("*") if p.is_file())
    print(f"\n  desktop-shots/  {total/1048576:.1f} MB  ·  {len(groups)} components")
    return groups


def build_html(app_label: str, section_title: str, frames: list[tuple[str, str]]) -> str:
    parts = [
        "<!DOCTYPE html>",
        f'<html lang="en" data-component="desktop-shot">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>SportsHeist — {app_label} · {section_title}</title>",
        "<style>",
        "*{box-sizing:border-box}",
        "html,body{margin:0;background:#0B0D08;color:#F1F3EC;",
        "font:400 14px/1.4 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif}",
        "main.page{min-height:100vh}",
        "section.frame{min-height:100vh;padding:0;margin:0}",
        ".shot{",
        "  display:block;width:100%;max-width:1440px;margin:0 auto;",
        "  background:#111;border:0;vertical-align:top;",
        "}",
        ".shot-wrap{min-height:100vh;display:flex;justify-content:center;align-items:flex-start;",
        "  background:#0B0D08;padding:0}",
        "</style>",
        "</head>",
        "<body>",
        '<main class="page">',
    ]
    for title, rel in frames:
        # Absolute-from-root path so srcdoc rewrite / live file:// both can be handled
        src = f"desktop-shots/{rel}"
        parts += [
            f'<section class="frame" data-title="{html_esc(title)}">',
            '  <div class="shot-wrap">',
            f'    <img class="shot" src="{src}" alt="{html_esc(title)}" loading="lazy">',
            "  </div>",
            "</section>",
        ]
    parts += ["</main>", "</body>", "</html>"]
    return "\n".join(parts)


def html_esc(s: str) -> str:
    return (s.replace("&", "&amp;")
             .replace('"', "&quot;")
             .replace("<", "&lt;")
             .replace(">", "&gt;"))


if __name__ == "__main__":
    print("Building desktop screenshot pages…")
    collect()
