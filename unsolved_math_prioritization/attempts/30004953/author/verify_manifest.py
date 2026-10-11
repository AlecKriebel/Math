#!/usr/bin/env python3
"""Read-only, standard-library verification of the frozen authored packet."""
from pathlib import Path, PurePosixPath
import hashlib
import json

ROOT = Path(__file__).resolve().parent

def require(test, message):
    if not test:
        raise RuntimeError(message)

def main():
    manifest = json.loads((ROOT/'MANIFEST.json').read_text())
    require(manifest['problem_id']==30004953,'Wrong problem identity')
    require(manifest['full_problem_solved'] is False,'Overstated full-problem result')
    expected={'MANIFEST.json'}
    for item in manifest['files']:
        name=item['path']; p=PurePosixPath(name)
        require(not p.is_absolute() and '..' not in p.parts,'Unsafe manifest path')
        require(name not in expected,'Duplicate manifest path')
        expected.add(name)
        target=ROOT/name
        require(target.is_file() and not target.is_symlink(),'Missing or linked file: '+name)
        data=target.read_bytes()
        require(len(data)==item['bytes'],'Byte-count mismatch: '+name)
        require(hashlib.sha256(data).hexdigest()==item['sha256'],'SHA-256 mismatch: '+name)
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    require(actual==expected,'File set mismatch: '+str(sorted(actual^expected)))
    print('PASS: exact frozen authored file set, lengths and SHA-256 hashes')

if __name__=='__main__':
    main()
