#!/usr/bin/env python3
"""Run positive exact checks and deliberate failures in normal and -O modes."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import signal
import subprocess
import sys
import time

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-dir', type=Path, required=True,
                    help='Fresh directory for actual reproduction records')
args = parser.parse_args()
destination = args.output_dir.resolve()
destination.mkdir(parents=True, exist_ok=False)
work = destination / 'empty_working_directory'
work.mkdir()
packet = Path(__file__).resolve().parent

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def digest(body):
    return hashlib.sha256(body).hexdigest()

def group_empty(process):
    if os.name != 'posix':
        return process.poll() is not None
    try:
        os.killpg(process.pid, 0)
    except ProcessLookupError:
        return True
    return False

cases = [
    ('author', 'author_exact.py', None, 686292, None),
    ('independent', 'independent_exact.py', None, 12846, None),
    ('boundary', 'exact_repeated_odd_boundary.py', None, 19, None),
    ('author_false', 'author_exact.py', 'false-guard', None, 'RuntimeError: Exact verification check failed'),
    ('independent_corrupt', 'independent_exact.py', 'corrupt-focal-identity', None, 'RuntimeError: universal_focal_pair_identity'),
    ('independent_singular', 'independent_exact.py', 'singular-line', None, 'RuntimeError: Singular antipedal line system'),
    ('boundary_false', 'exact_repeated_odd_boundary.py', 'false-guard', None, 'RuntimeError: forced_false_guard'),
]
report = {'schema': 'pr140-portable-verification-actual-reproduction/v1',
          'UTC_start': utc(), 'actual_runner_PID': os.getpid(),
          'python': platform.python_version(), 'python_implementation': platform.python_implementation(),
          'scope': 'Exact supplemental algebra and finite controls; no numerical dynamics or priority certificate.',
          'actual_argv_representation': 'Portable spelling of the actual invocation: python3 denotes this runner\'s sys.executable; scripts and output paths were resolved absolutely at execution. No private local path is distributed.',
          'working_directory': 'empty_working_directory, containing no proof or verifier files',
          'source_sha256': {p.name: digest(p.read_bytes()) for p in sorted(packet.glob('*.py'))},
          'runs': [], 'status': 'RUNNING'}
failure = None
try:
    for name, script, negative, expected_count, diagnostic in cases:
        for optimized in (False, True):
            mode = 'optimized' if optimized else 'normal'
            result_name = f'{name}_{mode}.json'
            result_path = destination / result_name
            switches = ['-B'] + (['-O'] if optimized else [])
            tail = ['--output', str(result_path)]
            if negative:
                tail += ['--negative-control', negative]
            actual_argv = [sys.executable, *switches, str(packet / script), *tail]
            start = utc()
            began = time.monotonic()
            process = subprocess.Popen(actual_argv, cwd=work, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, start_new_session=(os.name == 'posix'))
            timed_out = False
            try:
                stdout, stderr = process.communicate(timeout=30)
            except subprocess.TimeoutExpired:
                timed_out = True
                if os.name == 'posix':
                    os.killpg(process.pid, signal.SIGTERM)
                else:
                    process.terminate()
                try:
                    stdout, stderr = process.communicate(timeout=1)
                except subprocess.TimeoutExpired:
                    if os.name == 'posix':
                        os.killpg(process.pid, signal.SIGKILL)
                    else:
                        process.kill()
                    stdout, stderr = process.communicate(timeout=2)
            row = {'case': name, 'mode': mode, 'actual_PID': process.pid,
                   'UTC_start': start, 'UTC_end': utc(),
                   'elapsed_seconds': round(time.monotonic() - began, 6),
                   'argv_portable': ['python3', *switches, script, '--output', result_name] +
                                    (['--negative-control', negative] if negative else []),
                   'exit_code': process.returncode, 'child_reaped': process.poll() is not None,
                   'process_group_empty': group_empty(process), 'timed_out': timed_out,
                   'stdout_bytes': len(stdout), 'stdout_sha256': digest(stdout),
                   'stderr_bytes': len(stderr), 'stderr_sha256': digest(stderr),
                   'expected_negative_control': negative is not None}
            report['runs'].append(row)
            if timed_out or not row['child_reaped'] or not row['process_group_empty']:
                raise RuntimeError(f'{name} {mode}: child custody or deadline failure')
            if negative:
                # Full traceback hashes are retained; private source paths are omitted.
                lines = stderr.decode('utf-8', errors='replace').strip().splitlines()
                row['failure_diagnostic'] = lines[-1] if lines else None
                row['output_receipt_absent'] = not result_path.exists()
                if process.returncode != 1 or row['failure_diagnostic'] != diagnostic or stdout or result_path.exists():
                    raise RuntimeError(f'{name} {mode}: deliberate failure was not rejected as expected')
                row['outcome'] = 'EXPECTED_FAILURE_REJECTED'
            else:
                if process.returncode != 0 or stderr:
                    raise RuntimeError(f'{name} {mode}: positive exact reproduction failed')
                parsed = json.loads(stdout)
                count = parsed.get('assertions', parsed.get('checks'))
                if count != expected_count or parsed['mode'] != mode or parsed['proof_hash_requested'] is not False:
                    raise RuntimeError(f'{name} {mode}: expected count/mode/proof-independent execution disagrees')
                body = result_path.read_bytes()
                if json.loads(body) != parsed:
                    raise RuntimeError(f'{name} {mode}: result-file readback differs from stdout')
                row.update({'outcome': 'PASS', 'exact_conditions': count,
                            'result_file': result_name, 'result_bytes': len(body),
                            'result_sha256': digest(body), 'dependencies': parsed['dependencies']})
    for path in packet.glob('*.py'):
        if digest(path.read_bytes()) != report['source_sha256'][path.name]:
            raise RuntimeError('Verifier source changed during reproduction')
    report['status'] = 'PASS'
except Exception as error:
    failure = error
    report['status'] = 'FAIL'
    report['failure'] = str(error)
finally:
    report['UTC_end'] = utc()
    report['positive_runs'] = sum(r.get('outcome') == 'PASS' for r in report['runs'])
    report['negative_runs_rejected'] = sum(r.get('outcome') == 'EXPECTED_FAILURE_REJECTED' for r in report['runs'])
    report['all_children_reaped_and_groups_empty'] = all(r['child_reaped'] and r['process_group_empty'] for r in report['runs'])
    (destination / 'REPRODUCTION.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
print(json.dumps({'status': report['status'], 'UTC_start': report['UTC_start'], 'UTC_end': report['UTC_end'],
                  'actual_runner_PID': report['actual_runner_PID'], 'positive_runs': report['positive_runs'],
                  'negative_runs_rejected': report['negative_runs_rejected'],
                  'all_children_reaped_and_groups_empty': report['all_children_reaped_and_groups_empty']}))
if failure is not None:
    raise failure
