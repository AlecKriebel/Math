#!/usr/bin/env python3
"""Verify exact public payload bytes; the manifest itself is externally hashed."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'SHA256SUMS.json').read_text())
actual = {p.name for p in root.iterdir() if p.is_file() and p.name != 'SHA256SUMS.json'}
assert actual == set(manifest['files']), (actual, set(manifest['files']))
for name, entry in manifest['files'].items():
    raw = (root / name).read_bytes()
    assert len(raw) == entry['bytes'], name
    assert hashlib.sha256(raw).hexdigest() == entry['sha256'], name
print(json.dumps({'passed': True, 'files_checked': len(actual)}, indent=2))
