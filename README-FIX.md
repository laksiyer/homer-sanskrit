# Clickable Sanskrit: repaired installer

This replaces the earlier `INSTALL-WORD-LINKS.bat` and `scripts/install_word_links.py` installer only. It does **not** replace your Obsidian notes, existing web template, or build.py.

## Steps
1. Extract these files into `F:\github\homer-sanskrit`, allowing replacement of the prior installer files.
2. Double-click `INSTALL-WORD-LINKS.bat`.
3. Look for `SUCCESS: Clickable Sanskrit lexicon words installed.`
4. Open `site\index.html` locally and test linked Sanskrit terms.
5. Commit and push through GitHub Desktop after successful testing.

To include an inflected Sanskrit surface form, add it as metadata in the corresponding `obsidian-vault/Reference/Comparative Lexicon.md` entry:

`**Forms:** रजतधनुषो, रजतधनुषः`

The underlying note must also have the standard Greek (Roman) → Sanskrit heading and the `**Lines:**` field to be included in the web lexicon. The updater will not repair malformed lexicon headings.

The installer makes `.wordlinks-backup` copies of changed files. If its earlier version printed `expected one insertion point, found 0`, no changes were made by that run.
