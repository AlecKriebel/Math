#!/usr/bin/env python3
"""Check audit inventory and bytes. External ZIP receipt authenticates the manifest."""
import hashlib
import json
from pathlib import Path, PurePosixPath


def verify(root):
    root = Path(root)
    mp = root / 'AUDIT_MANIFEST.json'
    if mp.is_symlink() or not mp.is_file():
        raise ValueError('Invalid audit manifest')
    m = json.loads(mp.read_text())
    expected = {'AUDIT_MANIFEST.json'}
    for row in m['files']:
        name = row['path']
        if not isinstance(name, str) or name != PurePosixPath(name).name or name in expected:
            raise ValueError('Invalid inventory name')
        p = root / name
        if p.is_symlink() or not p.is_file():
            raise ValueError('Invalid file: ' + name)
        blob = p.read_bytes()
        if len(blob) != row['bytes'] or hashlib.sha256(blob).hexdigest() != row['sha256']:
            raise ValueError('Audit file mismatch: ' + name)
        expected.add(name)
    if {p.name for p in root.iterdir()} != expected:
        raise ValueError('Audit inventory mismatch')
    return {'status': 'PASS_AUDIT_MANIFEST', 'files': len(expected)}


if __name__ == '__main__':
    print(json.dumps(verify(Path(__file__).resolve().parent), sort_keys=True))
