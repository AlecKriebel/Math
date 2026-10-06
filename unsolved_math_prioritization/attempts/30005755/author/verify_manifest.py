#!/usr/bin/env python3
"""Verify every frozen file and reject extra files in this release directory."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'manifest.json').read_text())
entries = manifest['files']
expected = {'manifest.json'} | {entry['path'] for entry in entries}
actual = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
if actual != expected:
    raise SystemExit('FAIL: file inventory differs: ' + repr(sorted(actual ^ expected)))
for item in entries:
    p = root / item['path']
    b = p.read_bytes()
    if len(b) != item['bytes'] or hashlib.sha256(b).hexdigest() != item['sha256']:
        raise SystemExit('FAIL: content mismatch for ' + item['path'])
print('PASS: all %d frozen files match; no extras' % len(entries))
