#!/usr/bin/env python3
"""Verify exact inventory and SHA-256 hashes; optional root directory argument."""
import hashlib
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
manifest = json.loads((root/'MANIFEST.json').read_text())
expected = {x['path']: x for x in manifest['files']}
if len(expected) != len(manifest['files']):
    raise SystemExit('duplicate manifest path')
if any(p.is_symlink() for p in root.rglob('*')):
    raise SystemExit('symlink in packet')
actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
if actual != set(expected) | {'MANIFEST.json'}:
    raise SystemExit('file inventory mismatch')
for name, row in expected.items():
    path = Path(name)
    if path.is_absolute() or '..' in path.parts:
        raise SystemExit('unsafe path')
    b = (root/path).read_bytes()
    if len(b) != row['bytes'] or hashlib.sha256(b).hexdigest() != row['sha256']:
        raise SystemExit('content mismatch: '+name)
print(json.dumps({'result':'PASS','files_verified':len(expected),'strict_inventory':True},sort_keys=True))
