#!/usr/bin/env python3
"""Verify the byte integrity of the frozen public author packet."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
manifest = json.loads((root/'SHA256SUMS.json').read_text())
assert manifest['algorithm'] == 'sha256'
for entry in manifest['files']:
    relative = Path(entry['path'])
    assert not relative.is_absolute() and '..' not in relative.parts
    data = (root/relative).read_bytes()
    assert len(data) == entry['bytes'], entry['path']
    assert hashlib.sha256(data).hexdigest() == entry['sha256'], entry['path']
print(json.dumps({'status': 'PASS', 'verified_files': len(manifest['files'])}, sort_keys=True))
