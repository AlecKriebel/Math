#!/usr/bin/env python3
"""Run positive and materially broken controls in ordinary and optimized Python."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import platform
import subprocess
import sys


class HarnessFailure(Exception):
    pass


def require(condition, message):
    if not condition:
        raise HarnessFailure(message)


base = Path(__file__).resolve().parent
checker = base / 'check_resolution.py'
mutations = ['none', 'trivial_module', 'swapped_module', 'omit_x_right',
             'zero_high_comparison', 'factorial_shuffle', 'omit_e_scalar',
             'characteristic_three']
results = []
env = dict(os.environ)
env['PYTHONDONTWRITEBYTECODE'] = '1'
for optimized in [False, True]:
    for mutation in mutations:
        command = [sys.executable] + (['-O'] if optimized else []) + [str(checker), '--mutation', mutation]
        run = subprocess.run(command, text=True, capture_output=True, cwd=base, env=env)
        try:
            output = json.loads(run.stdout)
        except json.JSONDecodeError as error:
            raise HarnessFailure('Checker did not return structured diagnostics') from error
        require(not run.stderr, 'Unexpected checker stderr')
        require(output['optimized'] == optimized, 'Python optimization mode not exercised')
        expected = 0 if mutation == 'none' else 1
        require(run.returncode == expected, 'Unexpected exit for ' + mutation)
        require(output['status'] == ('pass' if mutation == 'none' else 'diagnostic_failure'),
                'Control status incorrect for ' + mutation)
        if mutation != 'none':
            require(output.get('exception') == 'DiagnosticFailure', 'Control failed accidentally')
        results.append({'command': command, 'exit_code': run.returncode,
                        'stdout_sha256': hashlib.sha256(run.stdout.encode()).hexdigest(),
                        'stderr_sha256': hashlib.sha256(run.stderr.encode()).hexdigest(),
                        'output': output})
for mutation in mutations:
    ordinary = next(r['output'] for r in results if r['output']['mutation'] == mutation and not r['output']['optimized'])
    optimized = next(r['output'] for r in results if r['output']['mutation'] == mutation and r['output']['optimized'])
    ordinary = {k: v for k, v in ordinary.items() if k != 'optimized'}
    optimized = {k: v for k, v in optimized.items() if k != 'optimized'}
    require(ordinary == optimized, 'Ordinary and optimized outcomes differ for ' + mutation)
report = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'checker_sha256': hashlib.sha256(checker.read_bytes()).hexdigest(),
          'harness_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'python_executable': sys.executable, 'python_version': platform.python_version(),
          'bounded_evidence_only': True,
          'correctness_gate': 'Explicit require -> exceptions; no assert gates.',
          'runs': results, 'positive_runs': 2, 'negative_controls_rejected': 14,
          'status': 'all_expected_outcomes_verified'}
(base/'TEST_RUNS.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({'status': report['status'], 'positive_runs': 2,
                  'negative_controls_rejected': 14,
                  'positive_checks_per_mode': results[0]['output']['checks']}, sort_keys=True))
