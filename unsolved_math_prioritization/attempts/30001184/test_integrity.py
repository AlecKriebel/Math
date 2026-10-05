#!/usr/bin/env python3
"""Integrity rejection controls in disposable copies, normal and optimized Python."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
CASES = ['intact', 'changed_bytes', 'missing_file', 'unexpected_file',
         'empty_inventory', 'duplicate_entry', 'path_traversal', 'absolute_path',
         'wrong_size', 'wrong_hash', 'duplicate_json_key', 'symlink',
         'unexpected_directory']


def mutate(root, case):
    mf = root / 'PUBLICATION_MANIFEST.json'
    m = json.loads(mf.read_text())
    target = root / 'packet/PROOF.md'
    if case == 'intact': return
    if case == 'changed_bytes': target.write_bytes(target.read_bytes() + b'!'); return
    if case == 'missing_file': target.unlink(); return
    if case == 'unexpected_file': (root / 'EXTRA.txt').write_text('extra'); return
    if case == 'symlink': target.unlink(); target.symlink_to(root / 'README.md'); return
    if case == 'unexpected_directory': (root / 'extra').mkdir(); return
    if case == 'duplicate_json_key':
        mf.write_text(mf.read_text().replace('"schema":', '"schema": "duplicate", "schema":', 1)); return
    if case == 'empty_inventory': m['files'] = []
    if case == 'duplicate_entry': m['files'][1] = m['files'][0].copy()
    if case == 'path_traversal': m['files'][0]['path'] = '../README.md'
    if case == 'absolute_path': m['files'][0]['path'] = '/tmp/README.md'
    if case == 'wrong_size': m['files'][0]['bytes'] += 1
    if case == 'wrong_hash': m['files'][0]['sha256'] = '0' * 64
    mf.write_text(json.dumps(m))


results = {}
for case in CASES:
    with tempfile.TemporaryDirectory(prefix='gns-integrity-') as temp:
        root = Path(temp) / 'publication'
        shutil.copytree(HERE, root)
        mutate(root, case)
        row = {}
        for mode, flags in [('normal', []), ('optimized', ['-O'])]:
            proc = subprocess.run([sys.executable, '-I', *flags,
                                   str(root / 'verify_publication.py'), '--integrity-only'],
                                  cwd=temp, capture_output=True, check=False)
            expected_accept = case == 'intact'
            if (proc.returncode == 0) != expected_accept:
                raise RuntimeError(case + ' ' + mode + ': unexpected acceptance/rejection')
            row[mode] = 'ACCEPT' if proc.returncode == 0 else 'REJECT'
        results[case] = row
print(json.dumps({'result': 'PASS', 'negative_cases': len(CASES) - 1,
                  'normal_and_optimized': True, 'controls': results}, sort_keys=True))
