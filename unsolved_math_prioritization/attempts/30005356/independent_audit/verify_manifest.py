#!/usr/bin/env python3
"""Verify this exact flat packet, its member set, and every file hash."""
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parent
m=json.loads((root/'MANIFEST.json').read_text())
paths=[v['path'] for v in m['files']]
assert len(paths)==len(set(paths))
assert all('/' not in p and '\\' not in p and p not in ['.','..','MANIFEST.json'] for p in paths)
assert {p.name for p in root.iterdir()}==set(paths)|{'MANIFEST.json'}
for p in root.iterdir():
    assert p.is_file() and not p.is_symlink()
for entry in m['files']:
    b=(root/entry['path']).read_bytes()
    assert len(b)==entry['bytes']
    assert hashlib.sha256(b).hexdigest()==entry['sha256']
print('PASS:',len(paths),'manifested files verified; no extras')
