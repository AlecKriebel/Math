#!/usr/bin/env python3
"""Verify every file covered by this packet's SHA-256 inventory."""
import hashlib
import json
from pathlib import Path

base = Path(__file__).resolve().parent
manifest = json.loads((base / 'SHA256SUMS.json').read_text())
listed = set()
for item in manifest['files']:
    path = base / item['path']
    assert path.is_file(), item['path']
    data = path.read_bytes()
    assert len(data) == item['bytes'], item['path']
    assert hashlib.sha256(data).hexdigest() == item['sha256'], item['path']
    listed.add(item['path'])
actual = {str(p.relative_to(base)) for p in base.rglob('*') if p.is_file()
          and p.name != 'SHA256SUMS.json' and '__pycache__' not in p.parts}
assert actual == listed, {'unlisted': sorted(actual - listed),
                          'missing': sorted(listed - actual)}
print(json.dumps({'result': 'PASS', 'files': len(listed)}))
