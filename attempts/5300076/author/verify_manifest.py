#!/usr/bin/env python3
"""Verify the explicitly frozen authored-file allowlist."""
import hashlib
import json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'SHA256SUMS.json').read_text())
expected={x['path'] for x in manifest['files']} | {'SHA256SUMS.json'}
actual={str(x.relative_to(root)) for x in root.rglob('*') if x.is_file()}
if actual!=expected:
    raise SystemExit(f'File-set mismatch: extra={actual-expected}, missing={expected-actual}')
for entry in manifest['files']:
    path=Path(entry['path'])
    if path.is_absolute() or '..' in path.parts:
        raise SystemExit('Unsafe path')
    data=(root/path).read_bytes()
    if len(data)!=entry['bytes'] or hashlib.sha256(data).hexdigest()!=entry['sha256']:
        raise SystemExit(f'Hash or size mismatch: {path}')
print(f"PASS: {len(manifest['files'])} frozen files")
