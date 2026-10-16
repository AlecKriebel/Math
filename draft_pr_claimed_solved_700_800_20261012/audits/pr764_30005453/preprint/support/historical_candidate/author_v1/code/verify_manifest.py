#!/usr/bin/env python3
"""Verify this frozen author's allowlist, sizes and hashes (standard library)."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root/'MANIFEST.json').read_text())
expected = {r['path']: r for r in manifest['files']}
actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
assert actual == set(expected)|{'MANIFEST.json'}, (actual-set(expected), set(expected)-actual)
for name, record in expected.items():
    p = root/name
    assert not p.is_symlink(), name
    b = p.read_bytes()
    assert len(b) == record['bytes'], name
    assert hashlib.sha256(b).hexdigest() == record['sha256'], name
print(json.dumps({'status': 'PASS', 'files': len(expected), 'scope': 'file integrity, not mathematical correctness'}, indent=2))
