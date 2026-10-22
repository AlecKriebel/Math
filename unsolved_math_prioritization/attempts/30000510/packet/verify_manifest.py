#!/usr/bin/env python3
"""Verify the frozen author packet against its enclosing AUTHOR_FREEZE.json."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent.parent
manifest = json.loads((root / 'AUTHOR_FREEZE.json').read_text())
expected = {entry['path']: entry for entry in manifest['files']}
actual = {p.name for p in (root / 'packet').iterdir() if p.is_file()}
assert actual == set(expected), (actual - set(expected), set(expected) - actual)
for name, entry in sorted(expected.items()):
    data = (root / 'packet' / name).read_bytes()
    assert len(data) == entry['bytes'], name
    assert hashlib.sha256(data).hexdigest() == entry['sha256'], name
print(json.dumps({'files_verified': len(expected), 'all_hashes_match': True}, sort_keys=True))
