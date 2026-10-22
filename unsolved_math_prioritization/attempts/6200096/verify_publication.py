#!/usr/bin/env python3
"""Strict publication inventory: reject changes, extras, missing files, symlinks."""
from pathlib import Path, PurePosixPath
import hashlib
import json

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'PUBLICATION_MANIFEST.json').read_text())
seen = set()
for item in manifest['files']:
    rel = item['path']
    q = PurePosixPath(rel)
    if q.is_absolute() or '..' in q.parts or rel in seen:
        raise SystemExit('FAIL: unsafe or duplicate path')
    p = root / rel
    if p.is_symlink() or not p.is_file():
        raise SystemExit('FAIL: missing or symlink ' + rel)
    data = p.read_bytes()
    if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
        raise SystemExit('FAIL: altered file ' + rel)
    seen.add(rel)
actual = {str(p.relative_to(root)) for p in root.rglob('*')
          if p.is_file() and p != root / 'PUBLICATION_MANIFEST.json'}
if actual != seen:
    raise SystemExit('FAIL: inventory')
print(json.dumps({'result': 'PASS', 'files': len(seen), 'target_id': 6200096}))
