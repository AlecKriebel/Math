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
    cases = ['author_report', 'audit_report', 'author_results', 'audit_results', 'author_manifest', 'audit_manifest', 'publication_manifest', 'author_zip', 'audit_zip', 'missing_file', 'extra_file', 'extra_directory', 'symlink', 'coherent_rehash', 'false_disposition']
    targets = {'author_report': 'author/MATHEMATICAL_REPORT.md', 'audit_report': 'audit/AUDIT_REPORT.md', 'author_results': 'author/RESULTS.json', 'audit_results': 'audit/checks/INDEPENDENT_RESULTS.json', 'author_manifest': 'author/MANIFEST.json', 'audit_manifest': 'audit/AUDIT_MANIFEST.json', 'publication_manifest': 'PUBLIC_MANIFEST.json', 'author_zip': 'AUTHOR_FREEZE.zip', 'audit_zip': 'AUDIT_PACKET.zip'}
    results = []
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env.pop('PYTHONPATH', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    for name in cases:
        with tempfile.TemporaryDirectory(prefix='high-genus-publication-mutation-') as td:
            copy = Path(td) / 'packet'
            shutil.copytree(root, copy)
            if name in targets:
                p = copy / targets[name]
                p.write_bytes(p.read_bytes() + b' ')
            elif name == 'missing_file':
                (copy / 'audit/AUDIT_SOURCE_VERIFICATION.json').unlink()
            elif name == 'extra_file':
                (copy / 'UNEXPECTED.txt').write_text('unexpected')
            elif name == 'extra_directory':
                (copy / 'UNEXPECTED').mkdir()
            elif name == 'symlink':
                p = copy / 'README.md'
                p.unlink()
                p.symlink_to(root / 'README.md')
            elif name == 'coherent_rehash':
                target = copy / 'author/MATHEMATICAL_REPORT.md'
                target.write_bytes(target.read_bytes() + b' ')
                metadata = {'bytes': target.stat().st_size, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest()}
                inner = copy / 'author/MANIFEST.json'
                inner_data = json.loads(inner.read_bytes())
                for record in inner_data['files']:
                    if record['path'] == 'MATHEMATICAL_REPORT.md':
                        record.update(metadata)
                inner.write_text(json.dumps(inner_data, indent=2) + '\n')
                public = copy / 'PUBLIC_MANIFEST.json'
                public_data = json.loads(public.read_bytes())
                public_data['files']['author/MATHEMATICAL_REPORT.md'] = metadata
                public_data['files']['author/MANIFEST.json'] = {'bytes': inner.stat().st_size, 'sha256': hashlib.sha256(inner.read_bytes()).hexdigest()}
                public.write_text(json.dumps(public_data, indent=2) + '\n')
            elif name == 'false_disposition':
                public = copy / 'PUBLIC_MANIFEST.json'
                public_data = json.loads(public.read_bytes())
                public_data['status'] = 'solved'
                public.write_text(json.dumps(public_data, indent=2) + '\n')
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
