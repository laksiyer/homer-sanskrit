# Homer in Sanskrit: Reader v2 update

This package updates only the website and its builder. It intentionally DOES NOT contain an `obsidian-vault` folder, so it cannot overwrite your Sanskrit, Greek or English notes.

## Installation

1. Keep a backup or use GitHub Desktop to commit your present working files first.
2. Extract the *contents* of this ZIP into `F:\github\homer-sanskrit\` and accept replacements for `scripts\build.py`, `site\template.html`, `site\index.html`, and `site\passages.json`.
3. In the root folder, run the existing `build-website.bat` (or `python scripts\build.py`).
4. Open `site\index.html` locally. If everything looks correct, commit and push in GitHub Desktop. GitHub Actions will deploy the website automatically.

## What's new

- Click/tap a Greek line with lexical notes to filter to that line's entries; click it again to restore all notes.
- Search lexicon entries by Greek, Roman, Sanskrit or note text.
- Two independent reading toggles: Roman/Greek; Devanagari/IAST.
- English closed by default, using the existing independent close reading aid. This is NOT yet the verbatim A. T. Murray translation.
- A passage's URL hash (`#1-1-7` or `#1-8-21`) identifies its location.
- More readable responsive layout and keyboard-accessible line notes.

## Editorial cautions

This remains a working edition. The transliterations are stored in the Markdown as separate fields, and the script does not perform Aksharamukha conversion. If you edit Devanagari, also update IAST in the same Obsidian note. Greek names and cognate claims need review. The website's A. T. Murray link is an external reference, not the source of the displayed English prose.

## Source-of-truth reminder

Edit the manuscript only under `obsidian-vault`. The Python script reads the current Markdown files and regenerates `site/index.html` and `site/passages.json`. Never edit the generated files directly.
