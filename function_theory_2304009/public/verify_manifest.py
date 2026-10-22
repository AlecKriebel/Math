#!/usr/bin/env python3
"""Verify the exact public artifact inventory and byte hashes."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
manifest = json.loads((root/'SHA256SUMS.json').read_text())
expected = set(manifest['files']) | {'SHA256SUMS.json'}
actual = {p.name for p in root.iterdir() if p.is_file()}
assert actual == expected, {'missing': sorted(expected-actual),
                            'unexpected': sorted(actual-expected)}
for name, meta in manifest['files'].items():
    data = (root/name).read_bytes()
    assert len(data) == meta['bytes'], name + ': byte count'
    assert hashlib.sha256(data).hexdigest() == meta['sha256'], name + ': hash'
print(json.dumps({'result': 'PASS', 'files_checked': len(manifest['files']),
                  'manifest_self_hash': 'bound by external author freeze receipt'},
                 sort_keys=True))
