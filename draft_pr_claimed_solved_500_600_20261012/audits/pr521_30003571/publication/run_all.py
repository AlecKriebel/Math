#!/usr/bin/env python3
"""Verify extracted package integrity and run exact checks without network access."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def main():
    if not __debug__ or os.environ.get('PYTHONOPTIMIZE'):
        raise RuntimeError('Run without Python optimization: archived checks use assertions')
    manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
    expected = set(manifest['files']) | {'MANIFEST.json'}
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*')
              if p.is_file() and '.venv' not in p.parts and '__pycache__' not in p.parts}
    if actual != expected:
        raise RuntimeError(f'Archive inventory mismatch: extra={actual-expected}, missing={expected-actual}')
    for name, info in manifest['files'].items():
        p = ROOT / name
        if p.stat().st_size != info['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest() != info['sha256']:
            raise RuntimeError(f'Integrity mismatch: {name}')
    jobs = [
        [str(ROOT / 'original/public/verify.py')],
        [str(ROOT / 'original/audit/audit_verify.py'), str(ROOT / 'original/public')],
        [str(ROOT / 'reviews/geometry01/verify_independent.py')],
        [str(ROOT / 'reviews/flow01/check_exact.py')],
    ]
    with tempfile.TemporaryDirectory(prefix='verification-tmp-', dir=ROOT) as scratch:
        for args in jobs:
            label = str(Path(args[0]).relative_to(ROOT))
            # The preserved geometry script writes a report beside itself.
            # Run a copy so repeated verification cannot change frozen files.
            if label in {'reviews/geometry01/verify_independent.py', 'reviews/flow01/check_exact.py'}:
                copy = Path(scratch) / Path(args[0]).name
                shutil.copyfile(args[0], copy)
                args = [str(copy)]
            p = subprocess.run([sys.executable, *args], cwd=ROOT,
                               capture_output=True, text=True, check=True)
            report = json.loads(p.stdout)
            status = report.get('status', '')
            if label == 'reviews/flow01/check_exact.py' and report.get('verdict') == 'all exact algebraic checks passed':
                status = 'PASS'
            if not str(status).startswith('PASS'):
                raise RuntimeError(f'Non-passing report for {label}')
            print(json.dumps({'check': label, 'status': status,
                              'identities': report.get('symbolic_identities',
                                  report.get('independent_exact_checks', report.get('exact_checks', report.get('number_of_checks'))))}))
    print(json.dumps({'status': 'PASS', 'manifest_files_verified': len(manifest['files']),
                      'limits': 'Integrity and algebra; cited analytic existence and written proof remain essential.'}))


if __name__ == '__main__':
    main()
