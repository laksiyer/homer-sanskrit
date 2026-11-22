#!/usr/bin/env python3
"""Build the static Homer website from the existing Obsidian Markdown notes.

Uses only Python's standard library. Run from anywhere:
    python scripts/build.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VAULT = ROOT / "obsidian-vault"
SITE = ROOT / "site"
TEMPLATE = SITE / "template.html"


def section(text: str, heading: str) -> str:
    pattern = rf"(?m)^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, text, flags=re.S | re.M)
    if not match:
        raise ValueError(f"Missing section: {heading}")
    return match.group(1).strip()


def fenced_lines(text: str, heading: str) -> tuple[list[int], list[str]]:
    block = section(text, heading)
    match = re.search(r"```(?:text)?\s*\n(.*?)\n```", block, flags=re.S)
    if not match:
        raise ValueError(f"Missing fenced text under: {heading}")
    nums: list[int] = []
    lines: list[str] = []
    for raw in match.group(1).splitlines():
        row = re.match(r"^\s*(\d+)\.\s+(.*)$", raw)
        if not row:
            raise ValueError(f"Greek line lacks a number under {heading}: {raw!r}")
        nums.append(int(row.group(1)))
        lines.append(row.group(2))
    return nums, lines


def english_from_callout(body: str) -> str:
    # Accept the existing Obsidian [!note]- convention; the disclosure starts closed.
    content = section(body, "English reading aid (collapsible)")
    quote_lines = [x[2:] for x in content.splitlines() if x.startswith("> ")]
    if not quote_lines or not quote_lines[0].startswith("[!note]"):
        raise ValueError("English must be an Obsidian > [!note]- callout")
    paragraphs = [x.strip() for x in quote_lines[1:] if x.strip()]
    # Credit is metadata, not part of the English text shown in the website.
    paragraphs = [p for p in paragraphs if not p.startswith("Independent close translation") and not p.startswith("Reference editions:")]
    return "\n".join(paragraphs)


def parse_passage(path: Path) -> dict:
    body = path.read_text(encoding="utf-8-sig")
    if body.startswith("---\n"):
        body = body.split("\n---\n", 1)[1]
    title_match = re.search(r"(?m)^# (.+)$", body)
    if not title_match:
        raise ValueError(f"No passage title: {path}")
    title = title_match.group(1)
    name = path.stem
    match = re.fullmatch(r"(\d+)-(\d+)-(\d+)", name)
    if not match:
        raise ValueError(f"Passage filename must be book-first-last.md: {path}")
    book, first, last = (int(x) for x in match.groups())
    roman_numbers, roman = fenced_lines(body, "Greek, reading transliteration")
    greek_numbers, greek = fenced_lines(body, "Greek, original polytonic")
    expected = list(range(first, last+1))
    if roman_numbers != expected or greek_numbers != expected:
        raise ValueError(f"Line numbers mismatch in {path.name}: expected {first}–{last}")
    sanskrit = section(body, "Sanskrit, Devanāgarī").strip()
    iast = section(body, "Sanskrit, IAST").strip()
    english = english_from_callout(body)
    sources = []
    if re.search(r"(?m)^## Sources\s*$", body):
        for label, url in re.findall(r"\[([^]\n]+)\]\((https?://[^)\s]+)\)", section(body, "Sources")):
            sources.append({"label":label,"url":url})
    # Editing Devanagari does not automatically update manually maintained IAST.
    return {"id":name,"title":title.split(" | ",1)[-1],"range":f"{book}.{first}–{last}",
            "greek":greek,"roman":roman,"sanskrit":sanskrit,"iast":iast,"english":english,
            "book":book,"first":first,"last":last,"sources":sources}


def parse_lexicon(path: Path) -> list[dict]:
    body = path.read_text(encoding="utf-8-sig")
    entries = []
    for block in re.split(r"(?m)^## ", body)[1:]:
        first_line, _, rest = block.partition("\n")
        match = re.fullmatch(r"(.+?) \((.+?)\) → (.+)", first_line.strip())
        if not match:
            raise ValueError(f"Malformed lexicon heading: {first_line}")
        gk, roman, sanskrit = match.groups()
        st = re.search(r"\*\*Status:\*\*\s*(.+)", rest)
        lines = re.search(r"\*\*Lines:\*\*\s*(.+)", rest)
        if not st or not lines:
            raise ValueError(f"Status or lines missing for lexicon entry: {gk}")
        explanation = re.sub(r"(?m)^\*\*(?:Status|Lines):\*\*.*$", "", rest).strip()
        source_links = [{"label":label,"url":url} for label,url in re.findall(r"\[([^]\n]+)\]\((https?://[^)\s]+)\)", rest)]
        entries.append({"sources":source_links,"greek":gk,"roman":roman,"sanskrit":sanskrit,
                        "status":st.group(1).strip(),"lines":lines.group(1).strip(),
                        "explain":explanation})
    return entries


def main():
    paths = sorted((VAULT / "Iliad").glob("Book-*/*.md"),
                   key=lambda p: tuple(map(int,p.stem.split('-'))))
    if not paths:
        raise SystemExit("No passages found under obsidian-vault/Iliad/Book-*/*.md")
    passages = [parse_passage(p) for p in paths]
    notes = parse_lexicon(VAULT / "Reference" / "Comparative Lexicon.md")
    data = {"passages":passages,"notes":notes}
    SITE.mkdir(parents=True,exist_ok=True)
    (SITE / "passages.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    template = TEMPLATE.read_text(encoding="utf-8")
    if template.count("__HOMER_DATA_JSON__") != 1:
        raise ValueError("Expected exactly one data insertion marker in site/template.html")
    # Prevent a malicious or accidental </script> in a note from breaking the HTML script tag.
    dataset = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    html = template.replace("__HOMER_DATA_JSON__", dataset)
    (SITE / "index.html").write_text(html, encoding="utf-8")
    print(f"Built {SITE / 'index.html'} from {len(passages)} Obsidian passages and {len(notes)} glossary entries.")
    print("Open site/index.html in a browser. Commit both Markdown and generated site files.")


if __name__ == "__main__":
    main()
