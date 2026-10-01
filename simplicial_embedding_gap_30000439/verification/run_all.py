#!/usr/bin/env python3
"""Reproduce pinned finite checks without modifying any pinned input."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
JOBS = [
    ('original_bounds', 'check_bounds.py', 'check_results.json', False),
    ('historical_independent', 'independent_checks.py', 'independent_checks.json', False),
    ('probability', 'independent_probability_checks.py', 'independent_probability_receipt.json', False),
    ('primary', 'independent_checks.py', 'independent_check_results.json', True),
    ('geometry', 'verify_exact.py', 'exact_stress_result.json', False),
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    receipts = []
    for folder, script, expected_name, dated in JOBS:
        source = ROOT / folder / script
        expected_path = ROOT / folder / expected_name
        before = (digest(source), digest(expected_path))
        expected = json.loads(expected_path.read_text())
        with tempfile.TemporaryDirectory(prefix='embedding-gap-check-') as work:
            isolated = Path(work) / script
            shutil.copyfile(source, isolated)
            result = subprocess.run([sys.executable, str(isolated)], cwd=work,
                                    capture_output=True, text=True, timeout=300)
            if result.returncode:
                raise RuntimeError(folder + ': ' + result.stdout + result.stderr)
            generated = Path(work) / expected_name
            actual = json.loads(generated.read_text() if generated.exists()
                                else result.stdout)
        if dated:
            assert 'timestamp_utc' in expected and 'timestamp_utc' in actual
            expected.pop('timestamp_utc')
            actual.pop('timestamp_utc')
        if actual != expected:
            raise AssertionError('Pinned receipt mismatch: ' + folder)
        assert before == (digest(source), digest(expected_path))
        receipts.append({'family': folder, 'status': 'PASS',
                         'script_sha256': before[0],
                         'expected_receipt_sha256': before[1],
                         'timestamp_only_ignored': dated})
        print(folder + ': PASS (pinned inputs unchanged)', flush=True)
    print(json.dumps({'status': 'PASS', 'programs': len(receipts),
                      'receipts': receipts,
                      'scope': 'Finite checks only; no enormous witness enumeration, '
                               'formal proof certification, or priority certificate.'},
                     indent=2))


if __name__ == '__main__':
    main()
