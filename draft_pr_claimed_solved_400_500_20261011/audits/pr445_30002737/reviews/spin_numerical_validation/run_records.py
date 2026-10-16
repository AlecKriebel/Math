#!/usr/bin/env python3
"""Run and preserve the actual commands, stdout, stderr, return codes and times."""
import hashlib
import json
import pathlib
import subprocess
import sys
from datetime import datetime, timezone

HERE = pathlib.Path(__file__).resolve().parent
commands = [
    ('exact_small_N_checks', [sys.executable, '-O', str(HERE / 'validate_code.py')], 0),
    ('certificate_N13_M65536', [sys.executable, str(HERE / 'certify_integral.py'), '--N', '13', '--cells', '65536', '--bits', '100', '--output', str(HERE / 'certificate_N13_M65536.json')], 0),
    ('certificate_N12_M65536_O', [sys.executable, '-O', str(HERE / 'certify_integral.py'), '--N', '12', '--cells', '65536', '--bits', '100', '--output', str(HERE / 'certificate_N12_M65536_O.json')], 0),
    ('certificate_N13_M65536_80bits_O', [sys.executable, '-O', str(HERE / 'certify_integral.py'), '--N', '13', '--cells', '65536', '--bits', '80', '--output', str(HERE / 'certificate_N13_M65536_80bits_O.json')], 0),
    ('float_reproduction_M65536', [sys.executable, str(HERE / 'reproduce_float.py'), '--cells', '65536'], 0),
    ('float_reproduction_M262144', [sys.executable, str(HERE / 'reproduce_float.py'), '--cells', '262144'], 0),
    ('negative_guard_N_zero_O', [sys.executable, '-O', str(HERE / 'certify_integral.py'), '--N', '0'], 1),
    ('negative_guard_cells_O', [sys.executable, '-O', str(HERE / 'certify_integral.py'), '--N', '13', '--cells', '16384'], 1),
    ('negative_guard_bits_O', [sys.executable, '-O', str(HERE / 'certify_integral.py'), '--bits', '60'], 1),
]
records = []
for label, command, expected in commands:
    started = datetime.now(timezone.utc).isoformat()
    result = subprocess.run(command, cwd=HERE, text=True, capture_output=True)
    record = {'label': label, 'actual_argv': command, 'cwd': str(HERE), 'started_utc': started,
              'completed_utc': datetime.now(timezone.utc).isoformat(), 'returncode': result.returncode,
              'expected_returncode': expected, 'stdout': result.stdout, 'stderr': result.stderr}
    records.append(record)
    (HERE / 'RAW_RUN_RECORDS.json').write_text(json.dumps(records, indent=2) + '\n')
    print(label, 'exit', result.returncode, flush=True)
    if result.returncode != expected:
        raise RuntimeError('unexpected exit status; record preserved')
print('All executions and intentional negative guards match expected status.')
