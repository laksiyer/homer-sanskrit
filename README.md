# Clickable Sanskrit lexicon update

Extract into `F:\github\homer-sanskrit` preserving directories. Run `INSTALL-WORD-LINKS.bat` **once**. The installer patches your existing `site/template.html` and `scripts/build.py` in place, builds the site, and makes `.wordlinks-backup` copies of files it modifies. It does not overwrite passage manuscripts.

Sanskrit words with matching lexicon entries appear in a contrasting color with a dotted underline. Clicking filters the comparative lexicon to the matching entry and scrolls there. Greek line clicks remain unchanged. Only words with confirmed spellings are linked. The first release highlights Devanagari; IAST can be added when corresponding forms are provided.

For inflected forms, in Obsidian's `Reference/Comparative Lexicon.md` put a new line below `**Lines:** ...` for an entry:

`**Forms:** मन्युं, मन्युः`

Only list forms actually present in your Sanskrit prose. Use comma-separated values. The installer will attempt to add `रजतधनुषो` to the silver-bow entry automatically when that entry is correctly formatted.

After testing `site/index.html`, commit and push all relevant changed files to GitHub Desktop. The backup files need not be committed.
