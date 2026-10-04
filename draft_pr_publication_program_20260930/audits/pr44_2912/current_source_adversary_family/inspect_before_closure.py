"""Own final read-only closure inspection; no production or canonical mutation."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat

HERE = Path(__file__).absolute().parent
A = HERE.parent
R = A.parents[2]
def sha(b): return hashlib.sha256(b).hexdigest()
def regular(p):
    assert not p.is_symlink() and not any(q.is_symlink() for q in p.parents)
    assert stat.S_ISREG(p.stat().st_mode)
    return p.read_bytes()
def clock(s):
    t = dt.datetime.fromisoformat(s.replace('Z', '+00:00'))
    assert t.tzinfo is not None and t.utcoffset() == dt.timedelta(0)
    return t
result = json.loads(regular(HERE / 'RESULT.json'))
supp = json.loads(regular(HERE / 'SUPPLEMENTAL_GATE_RESULT.json'))
assert result['status'] == 'PASS_SOURCE_ONLY_INDEPENDENT_CONTROLS' and result['assertions'] == 20405 and len(result['rejected_mutants']) == 56
assert supp['status'] == 'PASS' and supp['assertions'] == 62 and len(supp['rejected_mutants']) == 51
for dirname, expected in [('INDEPENDENT_CONTROLS_ACTUAL_CAPTURE', 1), ('INDEPENDENT_CONTROLS_V2_ACTUAL_CAPTURE', 0), ('SUPPLEMENTAL_GATES_ACTUAL_CAPTURE', 0)]:
    root = HERE / dirname
    cap = json.loads(regular(root / 'CAPTURE.json'))
    assert cap['actual_execution'] is True and cap['completed'] is True and type(cap['pid']) is int and cap['pid'] > 0
    assert type(cap['exit_code']) is int and cap['exit_code'] == expected and cap['stdin_supplied'] is False
    assert cap['source_unchanged'] is True and cap['operator_unchanged'] is True
    assert cap['status'] == ('PASS' if expected == 0 else 'FAIL_PRESERVED')
    assert clock(cap['started_utc']) <= clock(cap['finished_utc']) <= dt.datetime.now(dt.timezone.utc)
    assert sha(regular(root / 'PRELAUNCH_SOURCE.py')) == cap['source_sha256']
    assert sha(regular(root / 'PRELAUNCH_OPERATOR.py')) == cap['operator_sha256']
    for k in ['stdout', 'stderr']:
        b = regular(root / cap[k]['path']); assert len(b) == cap[k]['bytes'] and sha(b) == cap[k]['sha256']
foreign = json.loads(regular(HERE / 'INDIVIDUAL_FOREIGN_INPUTS.json'))
assert foreign['foreign_input_count'] == len(foreign['files']) == 366
for row in foreign['files']:
    b = regular(R / row['path']); assert len(b) == row['bytes'] and sha(b) == row['sha256']
extra = []
bindings = json.loads(regular(A / 'current_preparation_family/STATIC_INPUT_BINDINGS.json'))
for key in ['template_source', 'template_operator']:
    row = bindings[key]; b = regular(R / row['path'])
    assert len(b) == row['bytes'] and sha(b) == row['sha256']; extra.append(dict(row, role='historical_template_source_not_current_authority'))
raw = json.loads(regular(A / 'root_original_actual_reproduction/ROOT_RAW_SQL_AUDIT.json'))
for row in raw['foreign_original_cache_inputs_individually_pinned_not_copied']:
    b = regular(R / row['path']); assert len(b) == row['bytes'] and sha(b) == row['sha256']; extra.append(dict(row, role='whole_native_cache_unchanged_individually_excluded'))
for name in ['FINAL_REPORT.md', 'VERDICT.json', 'RESEARCH_LOG.md']:
    assert regular(HERE / name)
verdict = json.loads(regular(HERE / 'VERDICT.json'))
assert verdict['mandatory_production_source_defects'] == [] and verdict['new_whole_current_gate'] == 'PENDING'
all_files = [p for p in HERE.rglob('*') if p.is_file()]
assert not any(p.is_symlink() for p in HERE.rglob('*'))
value = {'schema': 'pr44-source-adversary-final-own-inspection/v1', 'status': 'PASS', 'actual_pid': os.getpid(), 'utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'all366_foreign_inputs_still_byte_exact': True, 'additional_individual_foreign_refs': extra, 'files_read_before_own_final_capture_completion': len(all_files), 'complete_prior_captures_verified': 3, 'control_assertions': 20467, 'rejected_cases': 107, 'production_execution': False, 'new_whole_current_PASS_claimed': False}
(HERE / 'FINAL_INSPECTION_RESULT.json').write_text(json.dumps(value, indent=2) + '\n')
print(json.dumps({k: value[k] for k in ['status', 'actual_pid', 'files_read_before_own_final_capture_completion', 'control_assertions', 'rejected_cases']}))
