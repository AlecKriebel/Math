#!/usr/bin/env python3
"""Verify closed authored-file inventory without writing to the review."""
from pathlib import Path
import hashlib
import json
import stat

BASE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def check():
    manifest = json.loads((BASE / 'MANIFEST.json').read_text())
    entries = manifest['authored_files']
    names = [entry['path'] for entry in entries]
    require(len(names) == len(set(names)), 'Duplicate manifest path')
    require('MANIFEST.json' not in names, 'Manifest must exclude itself')
    actual = {str(p.relative_to(BASE)) for p in BASE.rglob('*') if p.is_file() or p.is_symlink()}
    require(actual == set(names) | {'MANIFEST.json'}, 'Closed inventory mismatch')
    for entry in entries:
        rel = Path(entry['path'])
        require(not rel.is_absolute() and '..' not in rel.parts, 'Unsafe path')
        path = BASE / rel
        require(stat.S_ISREG(path.lstat().st_mode), 'Nonregular member')
        data = path.read_bytes()
        require(len(data) == entry['bytes'], 'Size mismatch: ' + entry['path'])
        require(hashlib.sha256(data).hexdigest() == entry['sha256'], 'Hash mismatch: ' + entry['path'])
    verdict = json.loads((BASE / 'VERDICT.json').read_text())
    require(verdict['verdict'] == 'PASS_FOR_POSITIVE_EQUILIBRIUM_STOCHASTIC_THEOREM', 'Wrong verdict')
    require(verdict['analytic_gap_count'] == 0, 'Unresolved analytic gap')
    require(verdict['literal_nonnegative_uniqueness'] == 'FALSE', 'Lost boundary distinction')
    return {'result': 'PASS', 'verified_authored_files': len(entries), 'manifest_excludes_self': True, 'source_bodies_included': False}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2, sort_keys=True))
