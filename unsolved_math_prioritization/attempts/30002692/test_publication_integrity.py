#!/usr/bin/env python3
"""Actual mutations of disposable package copies; no mathematical search."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('publication', ROOT / 'verify_publication.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

def change_manifest(root, change):
    path = root / v.MANIFEST
    obj = json.loads(path.read_text())
    change(obj)
    path.write_text(json.dumps(obj))

def replace_archive_rehash(root):
    name = v.ANCHORS['release'][0]
    path = root / name
    path.write_bytes(path.read_bytes() + b'X')
    change_manifest(root, lambda obj: [row.update(bytes=path.stat().st_size, sha256=v.digest(path.read_bytes())) for row in obj['files'] if row['path'] == name])

def change_status_rehash(root, key, value):
    name = 'PUBLICATION_STATUS.json'
    path = root / name
    obj = json.loads(path.read_text())
    obj[key] = value
    path.write_text(json.dumps(obj))
    change_manifest(root, lambda obj: [row.update(bytes=path.stat().st_size, sha256=v.digest(path.read_bytes())) for row in obj['files'] if row['path'] == name])

def main():
    anchor = v.digest((ROOT / v.MANIFEST).read_bytes())
    v.verify(ROOT, anchor)
    controls = [
        ('empty extra directory', lambda p: (p / 'extra_directory').mkdir(), False),
        ('coherent novelty upgrade', lambda p: change_status_rehash(p, 'novelty_claim', True), True),
        ('coherent aggregator upgrade', lambda p: change_status_rehash(p, 'aggregator_statement_verified', True), True),
        ('coherent approach count', lambda p: change_status_rehash(p, 'substantive_approaches_used', 5), True),
        ('changed proof', lambda p: (p / 'release/PROOF.md').write_bytes((p / 'release/PROOF.md').read_bytes() + b'X'), False),
        ('missing audit', lambda p: (p / 'audit_release/AUDIT.md').unlink(), False),
        ('extra file', lambda p: (p / 'EXTRA.txt').write_text('extra'), False),
        ('payload symlink', lambda p: ((p / 'README.md').unlink(), (p / 'README.md').symlink_to('PUBLICATION_STATUS.json')), False),
        ('directory symlink', lambda p: (p / 'link').symlink_to('.', target_is_directory=True), False),
        ('manifest symlink', lambda p: ((p / v.MANIFEST).unlink(), (p / v.MANIFEST).symlink_to('PUBLICATION_STATUS.json')), False),
        ('changed external manifest', lambda p: (p / v.MANIFEST).write_bytes((p / v.MANIFEST).read_bytes() + b' '), False),
        ('duplicate path, reanchored test', lambda p: change_manifest(p, lambda m: m['files'].append(m['files'][0].copy())), True),
        ('traversal path, reanchored test', lambda p: change_manifest(p, lambda m: m['files'][0].update(path='../escape')), True),
        ('absolute path, reanchored test', lambda p: change_manifest(p, lambda m: m['files'][0].update(path='/escape')), True),
        ('duplicate JSON key, reanchored test', lambda p: (p / v.MANIFEST).write_text('{"schema":"sha256-bytes-v1","schema":"sha256-bytes-v1","files":[]}'), True),
        ('changed archive with outer rehash, reanchored test', replace_archive_rehash, True),
    ]
    results = []
    for label, mutation, reanchor in controls:
        with tempfile.TemporaryDirectory(prefix='pe-boundary-corruption-') as tmp:
            copied = Path(tmp) / 'package'
            shutil.copytree(ROOT, copied)
            mutation(copied)
            expected = v.digest((copied / v.MANIFEST).read_bytes()) if reanchor else anchor
            try:
                v.verify(copied, expected)
            except Exception as error:
                results.append({'mutation': label, 'rejected': True, 'reason': str(error)})
            else:
                raise ValueError('accepted mutation: ' + label)
    print(json.dumps({'status': 'PASS', 'controls': results, 'control_count': len(results), 'scope': 'integrity only; not a mathematical proof'}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
