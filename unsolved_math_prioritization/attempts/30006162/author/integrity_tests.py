#!/usr/bin/env python3
"""Rerun integrity negative controls without changing the supplied packet."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def run(verifier, root, pin, optimized, cwd):
    cmd = [sys.executable, '-I', '-B'] + (['-O'] if optimized else [])
    cmd += [str(verifier), '--root', str(root), '--manifest-sha256', pin]
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=60)


def rebind(root, filename):
    mp = root / 'MANIFEST.json'
    m = json.loads(mp.read_bytes())
    b = (root / filename).read_bytes()
    m['files'][filename] = {'bytes': len(b), 'sha256': sha(b)}
    mp.write_text(json.dumps(m, sort_keys=True, indent=2) + '\n')
    return sha(mp.read_bytes())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--manifest-sha256', required=True)
    args = ap.parse_args()
    original = Path(args.root).absolute()
    verifier = original / 'verify.py'
    pin = args.manifest_sha256
    cases = ['changed_report', 'changed_checker', 'changed_expected_result',
             'unexpected_regular_file', 'missing_file', 'empty_directory',
             'bytecode_cache_directory', 'loose_bytecode_file', 'payload_symlink',
             'directory_symlink', 'fifo', 'changed_manifest',
             'payload_and_manifest_rehashed_old_pin', 'verified_checker_must_execute']
    verdicts = []
    with tempfile.TemporaryDirectory(prefix='surface-gpp-integrity-') as td:
        td = Path(td)
        elsewhere = td / 'unrelated_cwd'
        elsewhere.mkdir()
        for optimized in (False, True):
            baseline = run(verifier, original, pin, optimized, elsewhere)
            require(baseline.returncode == 0, 'baseline failed: ' + baseline.stderr)
            relocated = td / ('relocated_O' if optimized else 'relocated_normal')
            shutil.copytree(original, relocated)
            relocation = run(relocated / 'verify.py', relocated, pin, optimized, elsewhere)
            require(relocation.returncode == 0, 'relocation failed: ' + relocation.stderr)
            require(json.loads(baseline.stdout) == json.loads(relocation.stdout),
                    'relocated result mismatch')
            for index, label in enumerate(cases):
                root = td / ('case_' + str(int(optimized)) + '_' + str(index))
                shutil.copytree(original, root)
                use_pin = pin
                if label == 'changed_report':
                    with (root / 'MATHEMATICAL_REPORT.md').open('a') as f:
                        f.write('\nAltered.\n')
                elif label == 'changed_checker':
                    with (root / 'checks.py').open('a') as f:
                        f.write('\n# Altered checker.\n')
                elif label == 'changed_expected_result':
                    p = root / 'EXPECTED_RESULTS.json'
                    obj = json.loads(p.read_text()); obj['exact_assertions'] += 1
                    p.write_text(json.dumps(obj))
                elif label == 'unexpected_regular_file':
                    (root / 'undeclared.txt').write_text('x')
                elif label == 'missing_file':
                    (root / 'README.md').unlink()
                elif label == 'empty_directory':
                    (root / 'extra').mkdir()
                elif label == 'bytecode_cache_directory':
                    (root / '__pycache__').mkdir()
                    (root / '__pycache__' / 'checks.cpython-312.pyc').write_bytes(b'stale')
                elif label == 'loose_bytecode_file':
                    (root / 'checks.pyc').write_bytes(b'stale')
                elif label == 'payload_symlink':
                    p = root / 'README.md'; p.unlink(); p.symlink_to(original / 'README.md')
                elif label == 'directory_symlink':
                    (root / 'extra').symlink_to(elsewhere, target_is_directory=True)
                elif label == 'fifo':
                    os.mkfifo(root / 'unexpected_fifo')
                elif label == 'changed_manifest':
                    with (root / 'MANIFEST.json').open('a') as f:
                        f.write(' ')
                elif label == 'payload_and_manifest_rehashed_old_pin':
                    with (root / 'README.md').open('a') as f:
                        f.write('\nAltered and rehashed.\n')
                    rebind(root, 'README.md')
                elif label == 'verified_checker_must_execute':
                    # The checker is deliberately rebound to a NEW trusted pin.
                    # A verifier that only compared stored receipts would pass;
                    # the correct verifier executes it and rejects the exception.
                    (root / 'checks.py').write_text("raise RuntimeError('SOURCE_EXECUTION_CONTROL')\n")
                    use_pin = rebind(root, 'checks.py')
                result = run(verifier, root, use_pin, optimized, elsewhere)
                require(result.returncode != 0, 'mutation accepted: ' + label)
                if label == 'verified_checker_must_execute':
                    require('SOURCE_EXECUTION_CONTROL' in result.stderr,
                            'verified-source execution marker was not observed')
                verdicts.append({'mutation': label, 'optimized': optimized, 'rejected': True})
    report = {'problem_id': 30006162, 'status': 'PASS',
              'normal_and_optimized_baselines': True,
              'normal_and_optimized_relocation': True,
              'mutations_rejected': len(verdicts), 'cases': verdicts,
              'scope': 'Packet integrity, source execution, and relocation controls only.'}
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        sys.exit(1)
