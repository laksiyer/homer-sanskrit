# Homer in Sanskrit: Iliad 1.22–60 + deity comparisons + linked sources

This is an incremental patch for your existing `F:\github\homer-sanskrit` repository.

**Contents:** the two Obsidian passages `1-22-42.md` and `1-43-60.md`, the comparative lexicon, updated website template and build script, plus a generated preview (`site/index.html` and `site/passages.json`). The package does **not** overwrite `1-1-7.md`, `1-8-21.md`, or your other Obsidian notes.

1. Back up any files you have personally edited, particularly the lexicon or passage 1.22–42 if previously installed.
2. Unzip the contents into `F:\github\homer-sanskrit`, retaining the existing folder structure.
3. Run `build-website.bat`, or `python scripts\build.py` from the project folder. This regenerates the website from **your local Markdown files**.
4. Open `site\index.html`. You should now see passages 1.1–7, 1.8–21, 1.22–42, and 1.43–60, in ascending order.
5. Inspect the **Vedic comparisons** cards for Apollo/Rudra, Hera/Śacī–Indrāṇī and Leto/Aditi; click the source hyperlinks.
6. Commit and push from GitHub Desktop to publish.

**Editorial cautions:** Sanskrit and Roman Greek are draft transcriptions. Greek divine names are retained; comparisons with Vedic deities are annotated by type and are *not* asserted cognates. The English text is an independent close reading aid, **not Murray's verbatim translation**, though Murray is linked as a reference. Line 60 ends in the middle of a sentence which continues in 1.61. Sanskrit IAST is currently maintained separately from Devanāgarī.
