#!/usr/bin/env python3
"""Verify the closed authored-only priority audit without source payloads."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'REVIEW_MANIFEST.json').read_text())
entries = manifest['files']
names = [e['path'] for e in entries]
if len(names) != len(set(names)):
    raise ValueError('Duplicate path')
if any('/' in n or '\\' in n or n in ['', '.', '..', 'REVIEW_MANIFEST.json'] for n in names):
    raise ValueError('Unsafe path')
actual = {p.name for p in root.iterdir()}
if actual != set(names) | {'REVIEW_MANIFEST.json'}:
    raise ValueError('Unexpected or missing entry')
for p in root.iterdir():
    if not p.is_file() or p.is_symlink():
        raise ValueError('Nonregular file or source directory')
for entry in entries:
    data = (root / entry['path']).read_bytes()
    if len(data) != entry['bytes'] or hashlib.sha256(data).hexdigest() != entry['sha256']:
        raise ValueError('Fingerprint mismatch: ' + entry['path'])
if manifest['source_payloads_included'] or manifest['external_communications'] or manifest['remote_mutations']:
    raise ValueError('Research boundary overstated')
print('PASS:', len(entries) + 1, 'closed authored-only files; fingerprints match; private inputs absent')
