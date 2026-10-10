#!/usr/bin/env python3
"""Verify explicitly manifested audit files; optional replay output is ignored."""
import hashlib
import json
from pathlib import Path

base = Path(__file__).resolve().parent
manifest = json.loads((base/'AUDIT_MANIFEST.json').read_bytes())
seen = set()
for row in manifest['files']:
    path = Path(row['path'])
    if path.is_absolute() or '..' in path.parts or len(path.parts) != 1 or row['path'] in seen:
        raise ValueError('Unsafe or duplicate manifest member')
    seen.add(row['path'])
    file = base/path
    if file.is_symlink() or not file.is_file():
        raise ValueError('Not a regular file: '+row['path'])
    data = file.read_bytes()
    if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
        raise ValueError('Hash mismatch: '+row['path'])
print('PASS:',len(seen),'manifested independent-audit files')
