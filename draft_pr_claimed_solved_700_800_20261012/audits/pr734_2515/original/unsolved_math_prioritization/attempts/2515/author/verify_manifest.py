#!/usr/bin/env python3
"""Verify every declared author artifact without relying on the current directory."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'AUTHOR_MANIFEST.json').read_text())
for row in manifest['files']:
    relative = Path(row['path'])
    if relative.is_absolute() or '..' in relative.parts:
        raise RuntimeError('Unsafe manifest path')
    content = (root / relative).read_bytes()
    if len(content) != row['bytes'] or hashlib.sha256(content).hexdigest() != row['sha256']:
        raise RuntimeError('Mismatch: ' + row['path'])
print(json.dumps({'status': 'PASS', 'verified_author_files': len(manifest['files'])}, sort_keys=True))
