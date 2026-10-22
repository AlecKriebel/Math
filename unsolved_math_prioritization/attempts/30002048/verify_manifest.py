#!/usr/bin/env python3
"""Strict inventory/hash check only; not a mathematical proof verifier."""
import hashlib,re,stat,sys
from pathlib import Path,PurePosixPath


def verify(root):
    root=Path(root)
    if root.is_symlink() or not root.is_dir():raise ValueError('invalid root')
    manifest=root/'MANIFEST.sha256'
    if manifest.is_symlink() or not manifest.is_file():raise ValueError('invalid manifest')
    expected={}
    for line in manifest.read_text(encoding='utf-8').splitlines():
        if not re.fullmatch(r'[0-9a-f]{64}  .+',line):raise ValueError('invalid manifest line')
        digest,name=line.split('  ',1)
        path=PurePosixPath(name)
        if path.is_absolute() or str(path)!=name or any(t in ('','.', '..') for t in name.split('/')) or '\\' in name or name=='MANIFEST.sha256':raise ValueError('unsafe manifest path')
        if name in expected:raise ValueError('duplicate path')
        expected[name]=digest
    actual={}
    for p in root.rglob('*'):
        if p.is_symlink():raise ValueError('symlink forbidden')
        mode=p.stat().st_mode
        if stat.S_ISDIR(mode):continue
        if not stat.S_ISREG(mode):raise ValueError('nonregular file')
        name=p.relative_to(root).as_posix()
        if name=='MANIFEST.sha256':continue
        actual[name]=hashlib.sha256(p.read_bytes()).hexdigest()
    if actual!=expected:raise ValueError('inventory or SHA256 mismatch')
    return len(expected)


if __name__=='__main__':
    try:
        count=verify(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parent)
        print(f'PASS: exact inventory and SHA256 for {count} files.')
    except (ValueError,OSError) as e:
        print('FAIL:',e,file=sys.stderr);sys.exit(1)
