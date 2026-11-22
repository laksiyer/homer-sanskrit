# Homer in Sanskrit · होमेरकाव्यम्

A working comparative Greek–Sanskrit prose translation of the *Iliad*, with separate Obsidian text sources and a static website.

## Getting started on Windows

1. Extract this ZIP **into** `F:\github\homer-sanskrit` (do not nest a second `homer-sanskrit` directory). Back up your existing notes first if you have edited them since the starter ZIP.
2. In Obsidian, open `F:\github\homer-sanskrit\obsidian-vault` as a vault.
3. Edit `obsidian-vault\Iliad\Book-01\1-1-7.md` or `1-8-21.md`.
4. Double-click **`build-website.bat`**, or run `python scripts\build.py` in the repository.
5. Open `site\index.html` in a web browser. Commit and push the updated files using GitHub Desktop when ready.

The builder uses only the Python standard library. It does not require Markdown, Jinja, or Aksharamukha packages.

## Files and the source of truth

- `obsidian-vault/Iliad/Book-01/*.md`: editable Greek, Roman Greek, Sanskrit Devanāgarī, Sanskrit IAST, and English reading aids.
- `obsidian-vault/Reference/Comparative Lexicon.md`: editable scholarly glossary. Use an `## Greek (roman) → Sanskrit` heading followed by `**Status:**`, `**Lines:**`, and a prose paragraph.
- `scripts/build.py`: the Markdown-to-site-data compiler.
- `site/template.html`: HTML/CSS/JavaScript **template**, maintained by developers; it has the `__HOMER_DATA_JSON__` placeholder.
- `site/passages.json` and `site/index.html`: generated outputs. Do not manually edit these as your changes will be overwritten.

## Editing conventions

Each passage file should contain the headings exactly as presently given:

- `## Greek, reading transliteration` (numbered lines inside a `text` fenced code block)
- `## Greek, original polytonic` (numbered lines inside a `text` fenced code block)
- `## Sanskrit, Devanāgarī`
- `## Sanskrit, IAST`
- `## English reading aid (collapsible)` with an Obsidian `> [!note]-` callout

New passage files can use names such as `1-22-40.md` in `Iliad/Book-01/` and will be included in the navigation when built, provided both Greek sections contain exactly those verse numbers.

**Important:** Sanskrit IAST is currently a separate manually editable field, **not** automatically derived from Devanāgarī. If you correct a Sanskrit word, correct its IAST form too. Greek Roman is also independent of Greek polytonic. This prototype's script buttons display these stored forms rather than dynamically converting scripts. More script options can be added later.

The English passages are independent, close *reading aids*, **not quotations** from A. T. Murray. Murray (1924–25) serves as a reference edition only. If we later insert Murray's actual translated wording, we must attribute it accurately.

## Editorial principles

Prefer established Greek–Sanskrit Indo-European cognates where semantics allow. For Greek μῆνις use Sanskrit मन्यु in running prose; discuss Vedic मेनि only as a disputed possible connection. Do not substitute Indian mythological identities for Greek deities merely due to functional resemblance.

All passages remain scholarly **working drafts** requiring Greek textual and Sanskrit grammatical review. The website needs no server and works as a local HTML file.
