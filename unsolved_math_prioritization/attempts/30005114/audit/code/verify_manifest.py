#!/usr/bin/env python3
"""Verify exact payload closure, safe file types, and both package manifests."""
import hashlib
from pathlib import Path

root=Path(__file__).resolve().parents[1]
expected={}
for line in (root/'MANIFEST.sha256').read_text().splitlines():
    checksum,name=line.split('  ',1)
    assert name not in expected
    assert not Path(name).is_absolute() and '..' not in Path(name).parts
    expected[name]=checksum
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
assert actual==set(expected)|{'MANIFEST.sha256'}, (actual-set(expected),set(expected)-actual)
for name,checksum in expected.items():
    p=root/name
    assert p.suffix in {'.md','.json','.py','.sha256'},name
    assert not p.is_symlink(),name
    assert hashlib.sha256(p.read_bytes()).hexdigest()==checksum,name
for line in (root/'author_frozen/MANIFEST.sha256').read_text().splitlines():
    checksum,name=line.split('  ',1)
    assert hashlib.sha256((root/'author_frozen'/name).read_bytes()).hexdigest()==checksum,name
print('PASS: '+str(len(expected))+' payload files; both manifests and safe extension closure verified.')
