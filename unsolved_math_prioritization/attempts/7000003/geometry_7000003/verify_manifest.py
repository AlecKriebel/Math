#!/usr/bin/env python3
"""Validate the frozen authored file set against its manifest."""
from pathlib import Path
import hashlib
import json

base = Path(__file__).resolve().parent
manifest = json.loads((base/'MANIFEST.json').read_text())
expected = {entry['path'] for entry in manifest['files']}
actual = {str(p.relative_to(base)) for p in base.rglob('*') if p.is_file()}
assert actual == expected | {'MANIFEST.json'}, 'Unexpected or missing file'
for entry in manifest['files']:
    path = base/entry['path']
    assert not path.is_symlink(), 'Symlink is not part of the safe freeze'
    data = path.read_bytes()
    assert len(data) == entry['bytes'], 'Byte count mismatch: '+entry['path']
    assert hashlib.sha256(data).hexdigest() == entry['sha256'], 'Hash mismatch: '+entry['path']
print(json.dumps({'manifest_files_verified':len(expected),'manifest_self_hashed':False,'status':'pass'},sort_keys=True))
