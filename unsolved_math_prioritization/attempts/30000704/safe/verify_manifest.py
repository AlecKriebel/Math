#!/usr/bin/env python3
"""Verify exact frozen files, including extra-file and symlink rejection."""
import hashlib
import json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'SHA256SUMS.json').read_text())
expected=manifest['files']
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()
        and str(p.relative_to(root))!='SHA256SUMS.json'}
if actual!=set(expected):
    raise SystemExit('Inventory mismatch: '+repr({'extra':sorted(actual-set(expected)),
                                                'missing':sorted(set(expected)-actual)}))
for rel,want in sorted(expected.items()):
    p=root/rel
    if p.is_symlink(): raise SystemExit('Symlink rejected: '+rel)
    b=p.read_bytes()
    got={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    if got!=want: raise SystemExit('Byte/hash mismatch: '+rel)
print(json.dumps({'status':'PASS','files_checked':len(expected),'extra_files':0},sort_keys=True))
