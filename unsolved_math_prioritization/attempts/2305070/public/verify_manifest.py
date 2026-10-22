#!/usr/bin/env python3
"""Verify the public-file allowlist, byte lengths, and SHA-256 hashes."""
import hashlib
import json
from pathlib import Path

base = Path(__file__).resolve().parent
manifest = json.loads((base / 'SHA256SUMS.json').read_text())
actual = {str(p.relative_to(base)) for p in base.rglob('*')
          if p.is_file() and p.name != 'SHA256SUMS.json'
          and '__pycache__' not in p.parts}
expected = set(manifest['files'])
assert actual == expected, {'extra': sorted(actual-expected), 'missing': sorted(expected-actual)}
for name, record in manifest['files'].items():
    data = (base/name).read_bytes()
    assert len(data) == record['bytes'], name
    assert hashlib.sha256(data).hexdigest() == record['sha256'], name
print(json.dumps({'passed': True, 'verified_files': len(expected)}, sort_keys=True))
