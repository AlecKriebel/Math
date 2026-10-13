#!/usr/bin/env python3
"""Verify the complete portable package inventory and SHA-256 checksums."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'PACKAGE_MANIFEST.json').read_text())
expected = manifest['files']
actual = set()
for path in root.rglob('*'):
    if path.is_symlink():
        raise SystemExit(f'Symlink rejected: {path.relative_to(root)}')
    if path.is_file():
        actual.add(path.relative_to(root).as_posix())
if actual != set(expected) | {'PACKAGE_MANIFEST.json'}:
    raise SystemExit(f'Inventory mismatch: {actual ^ (set(expected) | {"PACKAGE_MANIFEST.json"})}')
for name, details in expected.items():
    path = root / name
    if path.stat().st_size != details['size']:
        raise SystemExit(f'Size mismatch: {name}')
    if hashlib.sha256(path.read_bytes()).hexdigest() != details['sha256']:
        raise SystemExit(f'Checksum mismatch: {name}')
print(json.dumps({'result': 'PASS', 'files': len(expected), 'purpose': 'corruption detection; not signed authenticity'}, indent=2))

