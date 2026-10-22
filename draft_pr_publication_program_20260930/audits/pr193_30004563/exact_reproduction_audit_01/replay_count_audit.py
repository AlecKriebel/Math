#!/usr/bin/env python3
"""Count successful author verify() returns by caller; run owned reviewed code."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import runpy
import sys

BASE = Path(__file__).resolve().parent
TARGET = BASE / 'submitted_replay/certify_five_centers.py'
EXPECTED = '09b5db2b625b00e2c20f9c41ea1922733b1b6ab04f404c2e37ba8f0e6ef1e585'
if hashlib.sha256(TARGET.read_bytes()).hexdigest() != EXPECTED:
    raise ArithmeticError('reviewed source changed')
if sys.flags.optimize != 0:
    raise ArithmeticError('author verifier requires active assertions; use ordinary Python without -O')
calls = Counter()


def trace(frame, event, arg):
    if event == 'return' and frame.f_code.co_name == 'verify' and frame.f_code.co_filename == str(TARGET):
        calls[frame.f_back.f_lineno] += 1


sys.setprofile(trace)
try:
    result = runpy.run_path(str(TARGET), run_name='__main__')
finally:
    sys.setprofile(None)
if sum(calls.values()) != result['checks']:
    raise ArithmeticError('dynamic count disagrees')
lines = TARGET.read_text().splitlines()
output = {
    'status': 'PASS', 'verify_successful_calls': result['checks'],
    'root_precondition_and_bound_calls': sum(count for line, count in calls.items()
                                            if 'verify(q>=0)' in lines[line - 1]
                                            or 'verify(lo**8<=q<hi**8)' in lines[line - 1]),
    'python_version': sys.version,
    'python_optimization_flag': sys.flags.optimize,
    'by_callsite': [{'line': line, 'calls': count, 'source': lines[line - 1].strip()}
                    for line, count in sorted(calls.items())],
    'meaning': 'Dynamic successful verify() invocations. Constructor and division assertions are excluded. Repeated root arithmetic dominates; this is not a count of independent theorems.',
}
(BASE / 'replay_count_results.json').write_text(json.dumps(output, indent=2) + '\n')
print('COUNT_AUDIT', sum(calls.values()))
