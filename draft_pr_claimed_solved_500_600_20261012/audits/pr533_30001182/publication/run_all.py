#!/usr/bin/env python3
"""Offline integrity and exact-control replay; frozen files are never edited."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def inventory():
    result = {}
    for p in ROOT.rglob('*'):
        rel = p.relative_to(ROOT)
        if '.venv' in rel.parts or '__pycache__' in rel.parts:
            continue
        if p.is_symlink():
            raise RuntimeError(f'Unexpected symlink: {rel}')
        if p.is_file():
            data = p.read_bytes()
            result[rel.as_posix()] = {
                'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    return result


def nested_manifests(before):
    seals = ['original/public/FROZEN_MANIFEST.json',
             'original/audit/AUDIT_MANIFEST.json'] + [
                 f'reviews/{family}/MANIFEST.json'
                 for family in ('operator01', 'extension01', 'source01')]
    checked = 0
    for seal in seals:
        base = PurePosixPath(seal).parent
        records = json.loads((ROOT / seal).read_text())['files']
        for item in records:
            rel = PurePosixPath(item['path'])
            if rel.is_absolute() or '..' in rel.parts:
                raise RuntimeError(f'Invalid nested path: {seal}: {rel}')
            name = (base / rel).as_posix()
            expected = {'bytes': item.get('bytes', item.get('size')),
                        'sha256': item['sha256']}
            if before.get(name) != expected:
                raise RuntimeError(f'Nested manifest mismatch: {seal}: {rel}')
            checked += 1
    return checked


def main():
    if not __debug__ or os.environ.get('PYTHONOPTIMIZE'):
        raise RuntimeError('Run without Python optimization: controls use assertions')
    manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
    for name in manifest['files']:
        p = PurePosixPath(name)
        if p.is_absolute() or '..' in p.parts:
            raise RuntimeError(f'Invalid manifest path: {name}')
    before = inventory()
    expected = set(manifest['files']) | {'MANIFEST.json'}
    if set(before) != expected:
        raise RuntimeError(f'Inventory mismatch: extra={set(before)-expected}, '
                           f'missing={expected-set(before)}')
    for name, item in manifest['files'].items():
        if before[name] != item:
            raise RuntimeError(f'Integrity mismatch: {name}')
    nested_checked = nested_manifests(before)
    jobs = [
        ('original/public/verify.py', 'original/public/checks.json'),
        ('original/verify_package.py', 'root_reproduction/package.stdout.json'),
        ('reviews/operator01/independent_verify.py',
         'reviews/operator01/independent_results.json'),
        ('reviews/extension01/verify_extension.py', 'reviews/extension01/CHECKS.json'),
        ('reviews/source01/verify_scope.py', 'root_reproduction/source_scope_rerun.json'),
        ('root_reproduction/verify_weighted_family.py',
         'root_reproduction/weighted_family_results.json'),
    ]
    with tempfile.TemporaryDirectory(prefix='.verify-', dir=ROOT) as folder:
        scratch = Path(folder)
        # Several preserved scripts write a neighboring report. Run copies.
        for name in ('original', 'reviews', 'root_reproduction'):
            shutil.copytree(ROOT / name, scratch / name)
        for script, record in jobs:
            p = subprocess.run([sys.executable, str(scratch / script)],
                               cwd=(scratch / script).parent,
                               env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'),
                               capture_output=True, text=True)
            if p.returncode:
                raise RuntimeError(f'{script} failed:\n{p.stderr}')
            actual = json.loads(p.stdout)
            if actual != json.loads((ROOT / record).read_text()):
                raise RuntimeError(f'Replay mismatch: {script}')
            print(json.dumps({'check': script, 'status': 'PASS'}))
    if inventory() != before:
        raise RuntimeError('Frozen files changed during replay')
    print(json.dumps({'status': 'PASS',
                      'manifest_files_verified': len(manifest['files']),
                      'nested_manifest_files_verified': nested_checked,
                      'offline': True, 'frozen_files_unchanged': True,
                      'limits': 'Finite controls supplement written universal proofs; '
                                'historical priority and formal certification are not implied.'}))


if __name__ == '__main__':
    main()
