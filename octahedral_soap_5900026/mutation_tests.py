#!/usr/bin/env python3
"""Adversarial integrity controls using a separately retained publication anchor."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--manifest-sha256', required=True)
    args = ap.parse_args()
    root = Path(__file__).resolve().parent
    if hashlib.sha256((root / 'PUBLIC_MANIFEST.json').read_bytes()).hexdigest() != args.manifest_sha256:
        raise RuntimeError('Supplied publication anchor does not match')
    cases = ['original_note', 'corrected_note', 'patch', 'audit_report', 'author_results', 'audit_results', 'author_manifest', 'audit_manifest', 'publication_manifest', 'missing_file', 'extra_file', 'extra_directory', 'symlink']
    targets = {'original_note': 'authored/MATHEMATICAL_NOTE.md', 'corrected_note': 'audit/MATHEMATICAL_NOTE_CORRECTED.md', 'patch': 'audit/CORRECTION.patch', 'audit_report': 'audit/AUDIT_REPORT.md', 'author_results': 'authored/CHECK_RESULTS.json', 'audit_results': 'audit/INDEPENDENT_RESULTS.json', 'author_manifest': 'authored/MANIFEST.json', 'audit_manifest': 'audit/AUDIT_MANIFEST.json', 'publication_manifest': 'PUBLIC_MANIFEST.json'}
    results = []
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env.pop('PYTHONPATH', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    for name in cases:
        with tempfile.TemporaryDirectory(prefix='octahedral-publication-mutation-') as td:
            copy = Path(td) / 'packet'
            shutil.copytree(root, copy)
            if name in targets:
                p = copy / targets[name]
                p.write_bytes(p.read_bytes() + b' ')
            elif name == 'missing_file':
                (copy / 'audit/SOURCE_VERIFICATION.json').unlink()
            elif name == 'extra_file':
                (copy / 'UNEXPECTED.txt').write_text('unexpected')
            elif name == 'extra_directory':
                (copy / 'UNEXPECTED').mkdir()
            elif name == 'symlink':
                p = copy / 'README.md'
                p.unlink()
                p.symlink_to(root / 'README.md')
            for opts in ([], ['-O']):
                completed = subprocess.run([sys.executable, '-B'] + opts + [str(copy / 'verify_publication.py'), '--manifest-sha256', args.manifest_sha256], cwd=td, env=env, capture_output=True, timeout=180)
                if completed.returncode == 0:
                    raise RuntimeError('Mutation incorrectly accepted: ' + name)
                if not completed.stderr.startswith(b'FAIL: '):
                    raise RuntimeError('Mutation failed for an unexpected reason: ' + name)
                results.append({'mutation': name, 'optimized': bool(opts), 'rejected': True})
    print(json.dumps({'result': 'PASS_PUBLICATION_MUTATION_CONTROLS', 'rejections': len(results), 'tests': results}, sort_keys=True, indent=2))

if __name__ == '__main__':
    main()
