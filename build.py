#!/usr/bin/env python3
"""Build GitHub Pages output from artifact-style page sources.

Each file in src/ is written the way a Claude Artifact expects: no doctype,
<html>, <head> or <body>, with <title>, font <link>s and <style> at the top.
This script wraps each one in a full document so it can be served as-is:

    src/index.html        -> index.html
    src/<name>.html       -> <name>/index.html

Usage: ./build.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

# Pages differ in language; the MemKV page also switches it at runtime.
LANG = {"index": "en", "ec-simulator": "ko", "memkv-recall": "en"}

HEAD_TAG = re.compile(
    r"\s*(<title>.*?</title>|<link\b[^>]*>|<meta\b[^>]*>|<style\b[^>]*>.*?</style>)",
    re.S | re.I,
)

TEMPLATE = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
{head}
</head>
<body>
{body}
</body>
</html>
"""


def split_head(text: str) -> tuple[str, str]:
    """Move the leading <title>/<link>/<meta>/<style> blocks into <head>."""
    head, pos = [], 0
    while (m := HEAD_TAG.match(text, pos)):
        head.append(m.group(1))
        pos = m.end()
    return "\n".join(head), text[pos:].strip()


def main() -> None:
    for src in sorted(SRC.glob("*.html")):
        name = src.stem
        head, body = split_head(src.read_text(encoding="utf-8"))
        out = ROOT / "index.html" if name == "index" else ROOT / name / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(TEMPLATE.format(lang=LANG.get(name, "en"), head=head, body=body), encoding="utf-8")
        print(f"{src.relative_to(ROOT)} -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
