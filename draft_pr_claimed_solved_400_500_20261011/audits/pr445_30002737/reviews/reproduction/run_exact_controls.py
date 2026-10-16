#!/usr/bin/env python3
"""Run the independent exception-based controls in both Python modes."""
from pathlib import Path
import json
import os
import subprocess
import sys

HERE = Path(__file__).resolve().parent
records = []
for variant in [None, 'marker', 'moments', 'normalization', 'flow', 'cocycle']:
    for optimize in [False, True]:
        env = os.environ.copy()
        env.pop('PYTHONOPTIMIZE', None)
        if optimize:
            env['PYTHONOPTIMIZE'] = '1'
        argv = [sys.executable, str(HERE / 'exact_controls.py')]
        if variant is not None:
            argv += ['--mutant', variant]
        process = subprocess.run(argv, capture_output=True, text=True, env=env, timeout=60)
        record = {'mutant': variant, 'inherited_PYTHONOPTIMIZE': env.get('PYTHONOPTIMIZE'),
                  'returncode': process.returncode, 'stdout': process.stdout, 'stderr': process.stderr,
                  'expected_rejection': variant is not None}
        if variant is None and process.returncode != 0:
            raise RuntimeError('Independent baseline failed')
        if variant is not None and process.returncode == 0:
            raise RuntimeError(f'Independent mutant falsely accepted: {variant}')
        records.append(record)
summary = {'baseline_runs': 2, 'baseline_stdout_identical': records[0]['stdout'] == records[1]['stdout'],
           'negative_runs': 10, 'negative_runs_rejected': 10,
           'runs': records}
if not summary['baseline_stdout_identical']:
    raise RuntimeError('Normal and optimized independent baseline output differs')
(HERE / 'records/independent_exact_controls.json').write_text(json.dumps(summary, indent=2)+'\n')
print(records[0]['stdout'])
print('All 10 new negative subprocess controls rejected in normal and optimized Python.')
