from pathlib import Path
import re
import subprocess
import sys

root = Path(__file__).resolve().parent
path = root / 'obsidian-vault' / 'Reference' / 'Comparative Lexicon.md'
if not path.exists():
    raise SystemExit(f'Cannot find {path}. Extract this update into the repository root.')
text = path.read_text(encoding='utf-8-sig')
old = '## ἀργυρέοιο βιοῖο · रजतधनुषः · Iliad 1.49'
new = '## ἀργυρέοιο βιοῖο (argureoio bioio) → रजतधनुषः'
if old in text:
    text = text.replace(old, new, 1)
elif new not in text:
    raise SystemExit('Cannot find the expected silver-bow entry. No files were changed.')
start = text.index(new)
end = text.find('\n## ', start+len(new))
if end == -1:
    end = len(text)
entry = text[start:end]
if '**Lines:** 1.49' not in entry:
    entry = entry.replace(new, new + '\n\n**Lines:** 1.49', 1)
    text = text[:start] + entry + text[end:]
path.write_text(text, encoding='utf-8')
print('Fixed silver-bow lexicon heading and line reference (Iliad 1.49).')
builder = root / 'scripts' / 'build.py'
if not builder.exists():
    raise SystemExit('Markdown fixed. Cannot find scripts/build.py; run your existing build-website.bat.')
subprocess.run([sys.executable, str(builder)], cwd=root, check=True)
import json
with (root/'site'/'passages.json').open(encoding='utf-8') as f:
    data=json.load(f)
notes = [n for n in data['notes'] if n.get('greek')=='ἀργυρέοιο βιοῖο' and '1.49' in n.get('lines','')]
if len(notes)!=1:
    raise SystemExit('Build ran but note is not correctly indexed; check Comparative Lexicon.md.')
print('VERIFIED: Rudra golden-bow note is indexed for Iliad 1.49.')
print('Commit and push the changed Markdown, site/passages.json, and site/index.html.')
