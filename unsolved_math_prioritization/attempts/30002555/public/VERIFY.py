#!/usr/bin/env python3
"""Verify an externally anchored flat inventory and exact arithmetic receipts."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


def need(value, message):
    if not value:
        raise RuntimeError(message)


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        need(key not in obj, 'Duplicate JSON key: ' + key)
        obj[key] = value
    return obj


def main():
    need(len(sys.argv) == 2, 'Supply the independent expected manifest SHA-256.')
    expected = sys.argv[1]
    need(re.fullmatch(r'[0-9a-f]{64}', expected) is not None, 'Invalid expected hash.')
    root = Path(__file__).resolve().parent
    manifest_path = root / 'MANIFEST.json'
    need(not manifest_path.is_symlink(), 'Manifest symlink forbidden.')
    raw = manifest_path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == expected, 'Manifest anchor mismatch.')
    manifest = json.loads(raw, object_pairs_hook=unique_object)
    need(manifest['schema'] == 'veech-ends-author-v1', 'Unexpected schema.')
    members = manifest['files']
    need(isinstance(members, list) and members, 'Missing inventory.')
    names = []
    for member in members:
        name = member['path']
        need(isinstance(name,str) and re.fullmatch(r'[A-Za-z0-9_.-]+',name) is not None and name not in ('.','..','MANIFEST.json'), 'Unsafe inventory member.')
        need(name not in names, 'Duplicate inventory member.')
        names.append(name)
        size = member['bytes']
        need(type(size) is int and size >= 0, 'Invalid size.')
        digest = member['sha256']
        need(isinstance(digest,str) and re.fullmatch(r'[0-9a-f]{64}',digest) is not None, 'Invalid digest.')
        path = root / name
        need(not path.is_symlink() and path.is_file(), 'Missing, linked or non-file member: '+name)
        data = path.read_bytes()
        need(len(data) == size, 'Size mismatch: '+name)
        need(hashlib.sha256(data).hexdigest() == digest, 'Digest mismatch: '+name)
    actual = {p.name for p in root.iterdir()}
    need(actual == set(names)|{'MANIFEST.json'}, 'Exact inventory mismatch.')
    receipt = (root / 'CHECK_RESULTS.json').read_bytes()
    runs = []
    for flags in [[], ['-O']]:
        proc = subprocess.run([sys.executable,*flags,'-B',str(root/'CHECKS.py')],cwd=root,capture_output=True)
        need(proc.returncode == 0, 'Arithmetic replay failed: '+proc.stderr.decode(errors='replace'))
        need(proc.stdout == receipt, 'Arithmetic receipt mismatch.')
        runs.append('optimized' if flags else 'ordinary')
    parsed = json.loads(receipt)
    print(json.dumps({'status':'PASS','manifest_sha256':expected,'verified_member_count':len(names),'replay_modes':runs,'total_exact_checks_per_mode':parsed['total_exact_checks']},sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
