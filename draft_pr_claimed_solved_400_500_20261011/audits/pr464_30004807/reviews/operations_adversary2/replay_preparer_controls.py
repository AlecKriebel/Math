#!/usr/bin/env python3
"""Replay preparer's current controls without changing preparer's files."""
import contextlib
import io
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent.parent
sys.path.insert(0, str(AUDIT / 'operations'))
import check_operations as control

control.OPERATIONS = HERE
with contextlib.redirect_stdout(io.StringIO()):
    control.main()
suffix = 'OPTIMIZED' if not __debug__ else 'NORMAL'
source = HERE / ('OFFLINE_CONTROLS_' + suffix + '.json')
result = json.loads(source.read_text())
if result.get('all_passed') is not True or type(result.get('case_count')) is not int or result['case_count'] != 158:
    raise RuntimeError('Unexpected preparer control aggregate')
if type(result.get('real_external_calls')) is not int or result['real_external_calls'] != 0:
    raise RuntimeError('Preparer replay had real external calls')
if len(result['cases']) != 158 or not all(x.get('passed') is True and type(x.get('real_external_calls')) is int
                                          and x['real_external_calls'] == 0 for x in result['cases']):
    raise RuntimeError('Preparer replay did not independently pass every case')
destination = HERE / ('PREPARER_REPLAY_' + suffix + '.json')
source.rename(destination)
print(json.dumps({'all_passed': True, 'case_count': 158, 'real_external_calls': 0}, sort_keys=True))
