from pathlib import Path
root=Path(__file__).resolve().parent
htmlpath=root/'site/comparative/vaka-dalbhya.html'
mdpath=root/'obsidian-vault/Comparative Studies/Vaka Dalbhya - Chryses and Rudra.md'
html_links='<section class="panel" id="full-source-translations"><h2>Original Sanskrit with English translations</h2><p>Full Vaka Dālbhi narrative from the Kāṭhaka Saṃhitā and all 11 Vāmana Purāṇa verses, Sanskrit with English panels.</p><ul><li><a href="kathaka-10-6-vaka.html">Kāṭhaka Saṃhitā 10.6: Sanskrit with English</a></li><li><a href="vamana-39-25-35-vaka.html">Vāmana Purāṇa 39.25–35: Sanskrit with English</a></li></ul></section>'
md_links='\n## Full primary passages with English translation\n\n- [[Kāṭhaka 10.6 - Vaka Dālbhi - Sanskrit and English]]\n- [[Vāmana Purāṇa 39.25-35 - Vaka Dālbhi - Sanskrit and English]]\n'
if htmlpath.exists():
 txt=htmlpath.read_text(encoding='utf-8')
 if 'id="full-source-translations"' not in txt:
  if '</body>' not in txt: raise SystemExit('HTML closing body not found; no change made')
  htmlpath.write_text(txt.replace('</body>',html_links+'</body>',1),encoding='utf-8')
 print('OK: comparative HTML links present')
else: print('NOTICE: old comparative HTML missing; new pages are still available')
if mdpath.exists():
 txt=mdpath.read_text(encoding='utf-8')
 if '## Full primary passages with English translation' not in txt:
  mdpath.write_text(txt.rstrip()+md_links,encoding='utf-8')
 print('OK: Obsidian study links present')
else: print('NOTICE: old comparative Obsidian study missing; source notes available')
print('SUCCESS: Vaka translation links ready')
