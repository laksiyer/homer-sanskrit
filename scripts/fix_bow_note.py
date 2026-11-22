#!/usr/bin/env python3
"""Repair the existing silver-bow lexicon entry in place, then validate build output."""
from pathlib import Path
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / 'obsidian-vault' / 'Reference' / 'Comparative Lexicon.md'
if not PATH.exists():
    sys.exit(f'Cannot find lexicon: {PATH}')
text = PATH.read_text(encoding='utf-8-sig')

replacement = '''## ἀργυρέοιο βιοῖο (argureoio bioio) → रजतधनुषः

**Status:** Vedic poetic and religious parallel; not an established lexical cognate
**Lines:** 1.49

**Apollo's silver bow and Rudra's golden bow**

Homer describes Apollo's **silver bow** (ἀργυρέοιο βιοῖο) in *Iliad* 1.49. Our Sanskrit preserves this as **रजतधनुषः** (in context, **रजतधनुषो**).

Atharvaveda (Śaunaka) 11.2.12 describes Rudra carrying a **golden bow**:

> धनुर्बिभर्षि हरितं हिरण्ययं सहस्रघ्नि शतवधं शिखण्डिन् ।
> रुद्रस्येषुश्चरति देवहेतिस्तस्यै नमो यतमस्यां दिशीतः ॥

Both Apollo and Rudra are depicted as formidable divine archers. Homer's bow is silver; Rudra's in this Atharvavedic verse is golden. This is a **poetic and religious comparison**, not an assertion that Apollo and Rudra are identical or that the epithets are inherited cognates.

Sources: [Homer, Iliad 1.49](https://homer.johnhboyer.com/iliad/book/1/?loc=1.49) · [Atharvaveda (Śaunaka) 11.2](https://www.vedicsamhita.in/vedas/atharvaveda/11/2)
'''

# Recognize both the malformed old heading and the corrected heading, replacing only this one entry.
heading = re.compile(r'(?m)^## (?:ἀργυρέοιο βιοῖο[^\n]*)$')
matches = list(heading.finditer(text))
if len(matches) != 1:
    sys.exit(f'Expected one silver-bow entry; found {len(matches)}. No changes made.')
start = matches[0].start()
next_head = re.search(r'(?m)^## ', text[matches[0].end():])
end = matches[0].end() + next_head.start() if next_head else len(text)
updated = text[:start].rstrip() + '\n\n' + replacement.rstrip() + '\n' + (('\n' + text[end:]) if next_head else '')
PATH.write_text(updated, encoding='utf-8')
print('Repaired the silver-bow entry in:', PATH)

build = ROOT / 'scripts' / 'build.py'
if not build.exists():
    sys.exit(f'Missing {build}; cannot rebuild website.')
subprocess.run([sys.executable, str(build)], cwd=ROOT, check=True)

datafile = ROOT / 'site' / 'passages.json'
data = json.loads(datafile.read_text(encoding='utf-8'))
found = [n for n in data['notes'] if n.get('greek') == 'ἀργυρέοιο βιοῖο']
if len(found) != 1:
    sys.exit(f'Build validation failed: expected 1 silver-bow note, found {len(found)}.')
entry = found[0]
assert '1.49' in entry['lines'], entry['lines']
assert 'हिरण्ययं' in entry['explain'], 'Missing Atharvaveda verse'
assert any('vedicsamhita.in' in s['url'] for s in entry['sources']), 'Missing linked Vedic source'
assert (ROOT / 'site' / 'index.html').exists(), 'Missing built site HTML'
print('SUCCESS: Bow note is in site/passages.json, linked to Iliad 1.49.')
print('Next: commit changed lexicon, site/passages.json, and site/index.html; then Push origin.')
