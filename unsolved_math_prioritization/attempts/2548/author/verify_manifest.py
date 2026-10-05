#!/usr/bin/env python3
"""Verify the frozen authored payload, without opening any private source files."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import sys

root = Path(__file__).resolve().parent
manifest_path = root / 'AUTHOR_MANIFEST.json'
manifest = json.loads(manifest_path.read_text())
expected = set()
for entry in manifest['files']:
    name = entry['path']
    p = PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or str(p) != name:
        raise SystemExit('Unsafe manifest path')
    f = root / name
    if f.is_symlink() or not f.is_file():
        raise SystemExit('Missing or symlinked file: ' + name)
    b = f.read_bytes()
    if len(b) != entry['bytes'] or hashlib.sha256(b).hexdigest() != entry['sha256']:
        raise SystemExit('Hash or byte mismatch: ' + name)
    if name in expected:
        raise SystemExit('Duplicate manifest path: ' + name)
    expected.add(name)
actual = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
if actual != expected | {'AUTHOR_MANIFEST.json'}:
    raise SystemExit('Unexpected file inventory: ' + repr(sorted(actual ^ (expected | {'AUTHOR_MANIFEST.json'}))))
print(json.dumps({'status': 'pass', 'files_verified': len(expected),
                  'problem_id': manifest['problem_id']}, sort_keys=True))
