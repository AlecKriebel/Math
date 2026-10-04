#!/usr/bin/env python3
"""Check exact file inventory and SHA-256 hashes of the frozen author packet."""
import hashlib
import json
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
manifest_path = root/'SHA256SUMS.json'
m = json.loads(manifest_path.read_text())
expected = m['files']
actual = {p.name for p in root.iterdir() if p.is_file() and p.name != manifest_path.name}
if actual != set(expected):
    raise SystemExit(f'File inventory mismatch: missing={set(expected)-actual}, extra={actual-set(expected)}')
for name, metadata in sorted(expected.items()):
    data = (root/name).read_bytes()
    if len(data) != metadata['bytes'] or hashlib.sha256(data).hexdigest() != metadata['sha256']:
        raise SystemExit(f'Hash mismatch: {name}')
print(json.dumps({'status':'PASS','files_checked':len(expected)}, sort_keys=True))
