#!/usr/bin/env python3
"""Verify this closed authored scope addendum."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'REVIEW_MANIFEST.json').read_text())
entries = manifest['files']
names = [entry['path'] for entry in entries]
if len(names) != len(set(names)):
    raise ValueError('Duplicate path')
if any('/' in name or '\\' in name or name in ['', '.', '..', 'REVIEW_MANIFEST.json'] for name in names):
    raise ValueError('Unsafe path')
if {p.name for p in root.iterdir()} != set(names) | {'REVIEW_MANIFEST.json'}:
    raise ValueError('Unexpected or missing entry')
for path in root.iterdir():
    if not path.is_file() or path.is_symlink():
        raise ValueError('Nonregular entry')
for entry in entries:
    data = (root / entry['path']).read_bytes()
    if len(data) != entry['bytes'] or hashlib.sha256(data).hexdigest() != entry['sha256']:
        raise ValueError('Fingerprint mismatch: ' + entry['path'])
print('PASS:', len(entries) + 1, 'closed authored scope-addendum files')
