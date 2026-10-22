#!/usr/bin/env python3
"""Read-only standard-library integrity check for the safe audit packet."""
from pathlib import Path, PurePosixPath
import hashlib
import json

ROOT=Path(__file__).resolve().parent


def require(ok,msg):
    if not ok:
        raise RuntimeError(msg)


def main():
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    require(manifest['problem_id']==30004953,'Wrong target')
    require(manifest['full_target_solved'] is False,'Overstated result')
    expected={'MANIFEST.json'}
    for row in manifest['files']:
        name=row['path'];rel=PurePosixPath(name)
        require(not rel.is_absolute() and '..' not in rel.parts,'Unsafe path')
        require(name not in expected,'Duplicate path');expected.add(name)
        p=ROOT/name
        require(p.is_file() and not p.is_symlink(),'Missing or linked file: '+name)
        b=p.read_bytes()
        require(len(b)==row['bytes'],'Size mismatch: '+name)
        require(hashlib.sha256(b).hexdigest()==row['sha256'],'Hash mismatch: '+name)
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
            if p.is_file() and '__pycache__' not in p.parts}
    require(actual==expected,'File-set mismatch')
    source=json.loads((ROOT/'SOURCE_AUDIT.json').read_text())
    require(source['author_freeze']['sha256']==manifest['reviewed_author_zip_sha256'],
            'Author binding mismatch')
    require(source['novelty_verified'] is False,'Novelty overclaim')
    print('PASS: exact safe audit file set and hashes; scoped verdict preserved')


if __name__=='__main__':
    main()
