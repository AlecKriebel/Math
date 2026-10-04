#!/usr/bin/env python3
"""Validate complete actual capture streams and prelaunch/source consistency."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import sys
from reproduce_original import strict_load

assert __debug__ and sys.flags.optimize == 0
FAMILY = Path(__file__).resolve().parent
AUDIT = FAMILY.parent
rows = []
mf = strict_load((AUDIT / 'ORIGINAL_PREPARATION_MANIFEST.json').read_bytes())
for recorded in mf['complete_prior_actual_captures']:
    cap_path = AUDIT / recorded['path']
    folder = cap_path.parent
    cap = strict_load(cap_path.read_bytes())
    pre = strict_load((folder / 'PRELAUNCH.json').read_bytes())
    operator = (folder / 'prelaunch_operator.py').read_bytes()
    assert hashlib.sha256(operator).hexdigest() == cap['operator_sha256'] == pre['operator_sha256']
    assert cap['argv'] == pre['argv'] == recorded['argv']
    assert cap['cwd'] == pre['cwd'] == recorded['cwd']
    assert cap['actual_execution'] is True and cap['completed'] is True and cap['operator_unchanged'] is True
    assert pre['actual_execution'] is False and pre['completed'] is False and pre['pid'] is None and pre['exit_code'] is None
    assert type(cap['pid']) is int and cap['pid'] > 0
    assert type(cap['exit_code']) is int
    start, finish = datetime.fromisoformat(cap['started_utc']), datetime.fromisoformat(cap['finished_utc'])
    assert start.utcoffset().total_seconds() == 0 and finish >= start
    assert pre['started_utc'] == cap['started_utc']
    for stream in ['stdout', 'stderr']:
        entry = cap[stream]
        assert entry['path'] == stream + '.bin'
        body = (folder / entry['path']).read_bytes()
        assert len(body) == entry['bytes'] and hashlib.sha256(body).hexdigest() == entry['sha256']
    if 'target_source' in cap:
        assert cap['target_source'] == pre['target_source'] and cap['target_unchanged'] is True
        child = Path(cap['target_source']['path'])
        assert child.parent == AUDIT
        body = child.read_bytes()
        assert len(body) == cap['target_source']['bytes']
        assert hashlib.sha256(body).hexdigest() == cap['target_source']['sha256']
    rows.append({'path': recorded['path'], 'child_pid': cap['pid'], 'exit_code': cap['exit_code'],
                 'complete_streams_and_actual_prelaunch_checked': True})
assert len(rows) == 103

own = []
for cap_path in sorted((FAMILY / 'captures').glob('*/CAPTURE.json')):
    if cap_path.parent.name == 'complete_capture_consistency':
        continue  # Its genuine outer CAPTURE does not exist until this child exits.
    cap = strict_load(cap_path.read_bytes())
    pre = strict_load((cap_path.parent / 'PRELAUNCH.json').read_bytes())
    assert cap['argv'] == pre['argv'] and cap['cwd'] == pre['cwd']
    assert type(cap['child_pid']) is int and cap['child_pid'] > 0
    assert cap['exit_code'] == pre['expected_exit'] == cap['expected_exit']
    assert cap['status'] == 'PASS_EXPECTED_EXIT'
    for key in ['operator', 'prelaunch', 'stdout', 'stderr']:
        ref = cap[key]
        body = Path(ref['path']).read_bytes()
        assert len(body) == ref['bytes'] and hashlib.sha256(body).hexdigest() == ref['sha256']
    assert (cap_path.parent / 'prelaunch_operator.py').read_bytes() == Path(cap['operator']['path']).read_bytes()
    if cap['child_source'] is not None:
        ref = cap['child_source']
        body = (cap_path.parent / 'prelaunch_child_source.py').read_bytes()
        assert len(body) == ref['bytes'] and hashlib.sha256(body).hexdigest() == ref['sha256']
    a, b = datetime.fromisoformat(cap['started_utc']), datetime.fromisoformat(cap['finished_utc'])
    assert datetime.fromisoformat(pre['created_utc']) <= a <= b
    own.append({'path': cap_path.relative_to(FAMILY).as_posix(), 'child_pid': cap['child_pid'],
                'exit_code': cap['exit_code'], 'complete_source_prelaunch_streams_checked': True})
result = {'schema': 'pr48-algebra-family-complete-actual-capture-consistency/v1', 'status': 'PASS',
          'actual_pid': os.getpid(), 'created_utc': datetime.now(timezone.utc).isoformat(),
          'original_actual_captures': rows, 'own_complete_actual_captures_before_child_exit': own,
          'own_outer_capture_completion': 'Only after the actual child exit; never inserted into this frozen prefix by the outer operator.',
          'future_ROOT_or_merge_authority': False}
(FAMILY / 'CAPTURE_CONSISTENCY_RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': 'PASS', 'original_captures': len(rows), 'own_completed_captures': len(own)}, indent=2))
