#!/usr/bin/env python3
"""Mutate disposable copies to test rejection; never alter the frozen input."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('publication', HERE / 'verify_publication.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

def change_manifest(root, change):
    path = root / v.MANIFEST
    obj = json.loads(path.read_text())
    change(obj)
    path.write_text(json.dumps(obj))

def rehash_file(root, name):
    raw = (root / name).read_bytes()
    change_manifest(root, lambda m: [row.update(bytes=len(raw), sha256=v.digest(raw)) for row in m['files'] if row['path'] == name])

def tamper_author_manifest(root):
    path = root / 'author/MANIFEST.json'
    path.write_bytes(path.read_bytes() + b' ')
    rehash_file(root, 'author/MANIFEST.json')

def tamper_status(root):
    path = root / 'PUBLICATION_STATUS.json'
    data = json.loads(path.read_text())
    data['novelty_claim'] = True
    path.write_text(json.dumps(data))
    rehash_file(root, 'PUBLICATION_STATUS.json')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('expected_manifest_sha256')
    args = parser.parse_args()
    root = args.root.resolve()
    v.verify(root, args.expected_manifest_sha256)
    controls = [
        ('changed proof', lambda p: (p / 'author/PROOF.md').write_bytes((p / 'author/PROOF.md').read_bytes() + b'X'), False),
        ('missing audit', lambda p: (p / 'independent_audit/AUDIT.md').unlink(), False),
        ('extra file', lambda p: (p / 'EXTRA.txt').write_text('extra'), False),
        ('payload symlink', lambda p: ((p / 'README.md').unlink(), (p / 'README.md').symlink_to('PUBLICATION_STATUS.json')), False),
        ('directory symlink', lambda p: (p / 'link').symlink_to('.', target_is_directory=True), False),
        ('manifest symlink', lambda p: ((p / v.MANIFEST).unlink(), (p / v.MANIFEST).symlink_to('PUBLICATION_STATUS.json')), False),
        ('changed external manifest', lambda p: (p / v.MANIFEST).write_bytes((p / v.MANIFEST).read_bytes() + b' '), False),
        ('duplicate manifest path', lambda p: change_manifest(p, lambda m: m['files'].append(m['files'][0].copy())), True),
        ('traversal path', lambda p: change_manifest(p, lambda m: m['files'][0].update(path='../escape')), True),
        ('absolute path', lambda p: change_manifest(p, lambda m: m['files'][0].update(path='/escape')), True),
        ('duplicate JSON key', lambda p: (p / v.MANIFEST).write_text('{"files":[],"files":[]}'), True),
        ('tampered author manifest with outer rehash', tamper_author_manifest, True),
        ('unsupported novelty with outer rehash', tamper_status, True),
    ]
    results = []
    for label, mutation, reanchor in controls:
        with tempfile.TemporaryDirectory(prefix='biclique-corruption-') as tmp:
            copied = Path(tmp) / 'package'
            shutil.copytree(root, copied)
            mutation(copied)
            expected = v.digest((copied / v.MANIFEST).read_bytes()) if reanchor else args.expected_manifest_sha256
            try:
                v.verify(copied, expected)
            except Exception as error:
                results.append({'mutation': label, 'rejected': True, 'reason': str(error)})
            else:
                raise ValueError('accepted mutation: ' + label)
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    bad = subprocess.run([sys.executable, '-E', '-B', '-O', str(root / 'verify_publication.py'), str(root), args.expected_manifest_sha256], env=env, text=True, capture_output=True)
    v.require(bad.returncode != 0 and 'assertions must be enabled' in bad.stderr, 'optimized execution must be rejected')
    env['PYTHONOPTIMIZE'] = '1'
    bad_env = subprocess.run([sys.executable, '-B', str(root / 'verify_publication.py'), str(root), args.expected_manifest_sha256], env=env, text=True, capture_output=True)
    v.require(bad_env.returncode != 0 and 'assertions must be enabled' in bad_env.stderr, 'environment optimization must be rejected')
    v.verify(root, args.expected_manifest_sha256)
    print(json.dumps({'status': 'PASS', 'control_count': len(results), 'controls': results,
                      'optimized_execution_rejected': True, 'environment_optimization_rejected': True,
                      'scope': 'integrity controls only; not mathematical proof'}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
