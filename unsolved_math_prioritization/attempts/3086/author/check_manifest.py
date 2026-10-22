#!/usr/bin/env python3
"""Verify the frozen allowlist, lengths and SHA-256 digests."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
manifest = json.loads((root/'manifest.json').read_text())
entries = manifest['files']
assert len({x['path'] for x in entries}) == len(entries)
expected = {x['path'] for x in entries} | {'manifest.json'}
actual = {p.name for p in root.iterdir() if p.is_file()}
assert expected == actual, {'missing': sorted(expected-actual), 'extra': sorted(actual-expected)}
assert not any(p.is_dir() for p in root.iterdir())
for e in entries:
    assert '/' not in e['path'] and e['path'] not in ('.', '..')
    b = (root/e['path']).read_bytes()
    assert len(b) == e['bytes'], e['path']
    assert hashlib.sha256(b).hexdigest() == e['sha256'], e['path']
print(json.dumps({'status': 'PASS', 'frozen_files': len(entries)}))
