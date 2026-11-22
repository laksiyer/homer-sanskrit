from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent
lex = ROOT / 'obsidian-vault' / 'Reference' / 'Comparative Lexicon.md'
entry_path = ROOT / 'LEXICON-ENTRY-TO-APPEND.md'
if not lex.exists():
    sys.exit('ERROR: Comparative Lexicon.md not found. Extract this ZIP to the project root.')
original = lex.read_text(encoding='utf-8-sig')
entry = entry_path.read_text(encoding='utf-8')
marker = '## Χρύσης (Khrusēs) → क्रूसेसः'
if marker in original:
    print('Comparison entry is already installed; no duplicate added.')
else:
    backup = lex.with_suffix('.md.before-vaka-backup')
    if not backup.exists(): backup.write_text(original,encoding='utf-8')
    lex.write_text(original.rstrip()+'\n\n'+entry.rstrip()+'\n',encoding='utf-8')
    print('Added comparison entry to Comparative Lexicon.md; backup saved.')
print('Study page: site/comparative/vaka-dalbhya.html')
print('Obsidian: obsidian-vault/Comparative Studies/Vaka Dalbhya - Chryses and Rudra.md')
