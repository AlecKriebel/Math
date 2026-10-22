#!/usr/bin/env python3
"""Verify exact package bytes and reject unmanifested files; read-only."""
from pathlib import Path
import hashlib
import json


def main():
    root=Path(__file__).resolve().parent
    manifest=json.loads((root/'MANIFEST.json').read_text())
    expected={entry['path']:entry for entry in manifest['files']}
    if any(p.is_symlink() for p in root.rglob('*')):
        raise SystemExit('Unexpected symbolic link in package')
    actual={p.relative_to(root).as_posix() for p in root.rglob('*')
            if p.is_file() and p != root/'MANIFEST.json'}
    if actual!=set(expected):
        raise SystemExit('File set mismatch: '+repr({'extra':sorted(actual-set(expected)),
                                                    'missing':sorted(set(expected)-actual)}))
    for relative,entry in expected.items():
        if Path(relative).is_absolute() or '..' in Path(relative).parts:
            raise SystemExit('Unsafe manifest path: '+relative)
        data=(root/relative).read_bytes()
        if len(data)!=entry['bytes'] or hashlib.sha256(data).hexdigest()!=entry['sha256']:
            raise SystemExit('Hash or length mismatch: '+relative)
    print(json.dumps({'status':'PASS','files_verified':len(expected),
                      'bytes_verified':sum(e['bytes'] for e in expected.values()),
                      'manifest_sha256':hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest()},
                     indent=2))


if __name__=='__main__':
    main()
