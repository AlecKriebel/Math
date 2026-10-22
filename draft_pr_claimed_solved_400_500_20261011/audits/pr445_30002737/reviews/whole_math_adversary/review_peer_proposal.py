#!/usr/bin/env python3
"""Read-only independent replay of the proposed peer finite-control code."""
from pathlib import Path
import ast
import hashlib
import json
import os
import subprocess
import sys

HERE = Path(__file__).resolve().parent
PEER = HERE.parent/'reproduction/exact_controls.py'
COPY = HERE/'private/fixtures/peer_exact_controls.py'
COPY.parent.mkdir(parents=True, exist_ok=True)
data = PEER.read_bytes()
COPY.write_bytes(data)
if any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(data))):
    raise ValueError('Proposed finite controls contain assert')
records = []
for mutant in [None, 'marker', 'moments', 'normalization', 'flow', 'cocycle']:
    for optimized in [False, True]:
        env = os.environ.copy()
        env.pop('PYTHONOPTIMIZE', None)
        if optimized:
            env['PYTHONOPTIMIZE'] = '1'
        cmd = [sys.executable, str(COPY)] + (['--mutant', mutant] if mutant else [])
        run = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=60)
        record = {'mutant': mutant, 'optimized': optimized, 'returncode': run.returncode,
                  'stdout': run.stdout, 'stderr': run.stderr, 'command': cmd}
        records.append(record)
        if mutant is None and run.returncode != 0:
            raise ValueError('Proposed baseline failed')
        if mutant is not None and (run.returncode == 0 or run.stdout):
            raise ValueError('Proposed invalid input issued success/output')
if records[0]['stdout'] != records[1]['stdout']:
    raise ValueError('Proposal baseline mode mismatch')
if PEER.read_bytes() != data:
    raise ValueError('Exposed proposed code changed')
result = {'pr': 445, 'problem_id': 30002737, 'reviewer': '/root/pr445_whole_math_adversary',
          'peer_code_sha256': hashlib.sha256(data).hexdigest(),
          'baseline_runs': 2, 'baseline_identical': True, 'negative_runs': 10,
          'negative_rejections_without_success_output': 10,
          'acceptance_scope': 'Fresh finite mathematical-control PASS guards accepted. No frozen-source integrity or saved-result replay entry point supplied by this code.',
          'original_publication_RR1_fully_repaired': False, 'records': records}
(HERE/'records/peer_proposal_replay.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k: v for k, v in result.items() if k != 'records'}, indent=2))
