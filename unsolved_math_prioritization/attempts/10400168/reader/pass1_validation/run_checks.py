#!/usr/bin/env python3
"""Replay normal/optimized checks, including intentional explicit-guard failures."""
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / 'verify_examples.py'


def metadata(path):
    data = path.read_bytes()
    return {'filename': path.name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def run():
    reports = []
    expected = None
    for name, flags in [('normal', []), ('O', ['-O']), ('OO', ['-OO'])]:
        completed = subprocess.run([sys.executable, *flags, str(SCRIPT)], capture_output=True, check=False)
        if completed.returncode != 0 or completed.stderr:
            raise RuntimeError(f'{name} failed: {completed.stderr.decode()}')
        result = json.loads(completed.stdout)
        if result['status'] != 'PASS':
            raise RuntimeError(f'{name} missing PASS')
        if expected is not None and completed.stdout != expected:
            raise RuntimeError('optimization changed output')
        expected = completed.stdout
        path = ROOT / f'RESULTS.{name}.json'
        path.write_bytes(completed.stdout)
        probe = subprocess.run([sys.executable, *flags, '-c',
                                'import runpy; n=runpy.run_path("verify_examples.py"); n["check"](False,"intentional guard probe")'],
                               cwd=ROOT, capture_output=True, check=False)
        if probe.returncode == 0 or b'RuntimeError: intentional guard probe' not in probe.stderr:
            raise RuntimeError(f'{name}: explicit test guard did not fail')
        reports.append({'mode': name, 'exit_code': completed.returncode,
                        'explicit_guard_failure_confirmed': True,
                        'explicit_checks_completed': result['explicit_checks_completed'],
                        'output': metadata(path)})
    receipt = {'status': 'PASS', 'python': platform.python_version(),
               'script': metadata(SCRIPT), 'runner': metadata(Path(__file__)),
               'all_outputs_byte_identical': True, 'runs': reports,
               'external_data_or_packages_used': False}
    (ROOT / 'RUN_RECEIPT.json').write_text(json.dumps(receipt, indent=2, sort_keys=True)+'\n')
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == '__main__':
    run()
