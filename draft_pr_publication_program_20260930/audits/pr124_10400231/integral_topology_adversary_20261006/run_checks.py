#!/usr/bin/env python3
"""Run actual verifier children and record their PIDs, exit codes, outputs."""
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

root = pathlib.Path(__file__).resolve().parent
runs_dir = root / 'runs'
runs_dir.mkdir(exist_ok=True)
records = []
for optimized in (False, True):
    for mode in ('normal', 'false-arbitrary-module', 'mutant-drop-torsion',
                 'mutant-strengthen-by-one'):
        label = ('optimized' if optimized else 'normal') + '__' + mode
        command = [sys.executable] + (['-O'] if optimized else []) + [
            str(root / 'checks.py'), '--mode', mode]
        started = datetime.datetime.now(datetime.timezone.utc).isoformat()
        child = subprocess.Popen(command, cwd=root,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = child.communicate(timeout=120)
        out_path, err_path = runs_dir / (label + '.stdout.json'), runs_dir / (label + '.stderr.txt')
        out_path.write_bytes(stdout)
        err_path.write_bytes(stderr)
        expected = 0 if mode == 'normal' else 1
        parsed = json.loads(stdout)
        record = {'label': label, 'argv': command, 'pid': child.pid,
                  'started_utc': started,
                  'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'exit_code': child.returncode, 'expected_exit_code': expected,
                  'observed_expected_exit': child.returncode == expected,
                  'stdout': {'path': str(out_path.relative_to(root)), 'bytes': len(stdout),
                             'sha256': hashlib.sha256(stdout).hexdigest()},
                  'stderr': {'path': str(err_path.relative_to(root)), 'bytes': len(stderr),
                             'sha256': hashlib.sha256(stderr).hexdigest()},
                  'parsed_output': parsed}
        records.append(record)
        if child.returncode != expected or parsed['pid'] != child.pid:
            raise RuntimeError('Unexpected check run: ' + label)
result = {'executed_runs': records,
          'all_observed_expected_exit': all(r['observed_expected_exit'] for r in records),
          'execution_kind': 'Actual subprocess.Popen children; records are not command plans'}
(root / 'EXECUTIONS.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'runs': len(records), 'all_observed_expected_exit': True,
                  'normal_checks': records[0]['parsed_output']['total_checks'],
                  'optimized_checks': records[4]['parsed_output']['total_checks']}, sort_keys=True))
