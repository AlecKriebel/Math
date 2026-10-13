#!/usr/bin/env python3
"""Read-only portable replay: exact fields exact; two numeric summaries tolerant.

The tolerance is only for labeled floating corroboration. It never weakens
the exact polynomial identities or any exact control field. Complete native
cross-runtime streams and old-byte mismatches are retained in private/replays.
"""
from pathlib import Path
import json
import math
import os
import subprocess
import sys

folder=Path(__file__).resolve().parent
expected=json.loads((folder/'INDEPENDENT_CHECKS.json').read_bytes())
result=subprocess.run([sys.executable,str(folder/'check_backward_feedback.py')],
                      env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True)
if result.returncode:
    sys.stdout.buffer.write(result.stdout)
    sys.stderr.buffer.write(result.stderr)
    raise SystemExit(result.returncode)
assert result.stderr==b'', 'unexpected native checker stderr'
actual=json.loads(result.stdout)
floating={'maximum_numerical_ratio_squared','maximum_numerical_feedback_residual'}
assert set(actual)==set(expected)
for key in set(expected)-floating:
    assert actual[key]==expected[key], ('exact field differs',key)
for key in floating:
    assert isinstance(actual[key],(int,float)) and math.isfinite(actual[key])
    assert abs(actual[key]-expected[key])<=1e-12, ('numeric summary outside absolute tolerance',key)
assert actual['maximum_numerical_ratio_squared']<=0.7+1e-12
assert 0<=actual['maximum_numerical_feedback_residual']<1e-12
print(json.dumps({
    'status':'PASS',
    'exact_fields':'all identical',
    'exact_assertions':actual['exact_assertions'],
    'numerical_assertions':actual['numerical_assertions'],
    'numerical_fields_compared':sorted(floating),
    'absolute_numeric_summary_tolerance':'1e-12',
    'numeric_experiment_bounds':'ratio_squared<=0.7+1e-12 and feedback_residual<1e-12',
    'justification':'Only labeled binary floating summaries are tolerant; the residual tolerance equals the existing experiment bound, and the ratio tolerance is far below its observed margin. Exact polynomial certificates and all other fields remain exact.',
    'native_child_exit':result.returncode,
    'native_child_stderr_bytes':len(result.stderr)
},indent=2,sort_keys=True))
