#!/usr/bin/env python3
"""Validate exactly the public files listed in SHA256SUMS.json."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'SHA256SUMS.json').read_text())
for name,expected in manifest['files'].items():
    p=root/name
    if not p.is_file(): raise SystemExit('Missing: '+name)
    got=hashlib.sha256(p.read_bytes()).hexdigest()
    if got!=expected: raise SystemExit('Hash mismatch: '+name)
extras={p.name for p in root.iterdir() if p.is_file()}-set(manifest['files'])-{'SHA256SUMS.json'}
if extras:raise SystemExit('Unmanifested public files: '+', '.join(sorted(extras)))
print(json.dumps({'status':'passed','verified_files':len(manifest['files'])},sort_keys=True))
