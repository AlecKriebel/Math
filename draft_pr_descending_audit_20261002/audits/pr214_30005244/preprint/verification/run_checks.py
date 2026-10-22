"""Offline portable replays. No network, repository, or provider writes."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

V = Path(__file__).resolve().parent
R = V.parent


def equivalent(actual, expected, path='root'):
    if isinstance(expected, dict):
        assert isinstance(actual, dict) and actual.keys() == expected.keys(), path
        for k in expected:
            equivalent(actual[k], expected[k], path + '.' + k)
    elif isinstance(expected, list):
        assert isinstance(actual, list) and len(actual) == len(expected), path
        for i, (a, b) in enumerate(zip(actual, expected)):
            equivalent(a, b, path + '.' + str(i))
    elif isinstance(expected, float):
        assert isinstance(actual, (int, float)) and math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-12), path
    else:
        assert actual == expected, (path, actual, expected)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', required=True)
    args = p.parse_args()
    package_manifest = R / 'PACKAGE_FILES.json'
    verified_members = None
    if package_manifest.exists():
        rows = json.loads(package_manifest.read_text())['files']
        for row in rows:
            f = R / row['path']
            assert f.resolve().is_relative_to(R.resolve())
            raw = f.read_bytes()
            assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'], row['path']
        verified_members = len(rows)
    original = R / 'pr_update/30005244/history/original_submission_20261015'
    checks = json.loads((V / 'ORIGINAL_CHECKS.json').read_text())
    reports = []
    with tempfile.TemporaryDirectory(prefix='dipole-verification-') as temp:
        t = Path(temp)
        for i, row in enumerate(checks):
            raw = (original / row['script']).read_bytes()
            assert hashlib.sha256(raw).hexdigest() == row['sha256']
            w = t / ('original' + str(i))
            w.mkdir()
            script = w / 'check.py'
            script.write_bytes(raw)
            result = subprocess.run([sys.executable, str(script)], cwd=w, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            equivalent(data, json.loads((V / row['expected']).read_text()))
            reports.append({'program': row['script'], 'sha256': row['sha256'], 'exact_assertions': data['exact_assertions'], 'expected_comparison_pass': True, 'result': data})
        for filename in ['ball_exact_controls.py', 'kernel_controls.py', 'spectral_illustration.py']:
            w = t / filename.removesuffix('.py')
            w.mkdir()
            (w / 'private').mkdir()
            script = w / filename
            shutil.copyfile(V / filename, script)
            cmd = [sys.executable, str(script)]
            if filename == 'kernel_controls.py':
                cmd += ['--output', str(w / 'result.json')]
            result = subprocess.run(cmd, cwd=w, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            if filename == 'ball_exact_controls.py':
                full = json.loads((w / 'private/exact_controls_output.json').read_text())
                assert full['count'] == 1244 and full['all_passed']
                assert data['negative_trace_coefficient'] == '-7831/15000'
                data.pop('output')
            elif filename == 'kernel_controls.py':
                assert data['exact']['exact_shells_checked'] == 427
                assert data['exact']['shell_numerator_sums_zero']
                assert data['exact']['exact_translated_h_scaling']
            else:
                assert data['all_assertions_passed']
            reports.append({'program': filename, 'sha256': hashlib.sha256(script.read_bytes()).hexdigest(), 'result': data})
    import numpy, sympy
    receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'all_programs_passed': True,
               'versions': {'python': platform.python_version(), 'numpy': numpy.__version__, 'sympy': sympy.__version__},
               'package_members_hash_verified': verified_members, 'original_reported_exact_assertions': sum(x['exact_assertions'] for x in reports[:4]),
               'limitations': 'Finite controls and floating illustrations supplement the written proof; no infinite limit or priority certification.',
               'programs': reports}
    Path(args.output).write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k: v for k, v in receipt.items() if k != 'programs'}, indent=2))


if __name__ == '__main__':
    main()
