"""Verify only own already-created audit inputs, before exact self manifest."""
import hashlib
import json
import os
from pathlib import Path
import stat
F=Path(__file__).resolve().parent
assert not (F/'OWN_CLOSED_MANIFEST.json').exists()
capture=json.loads((F/'ACTUAL_INSPECTOR_CAPTURE/CAPTURE.json').read_bytes())
assert capture['actual_execution'] is True and capture['completed'] is True
assert capture['pid']==33351 and capture['exit_code']==0
assert capture['source_unchanged'] is True and capture['operator_unchanged'] is True
for channel in ['stdout','stderr']:
    row=capture[channel];raw=(F/'ACTUAL_INSPECTOR_CAPTURE'/row['path']).read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
raw=(F/'ACTUAL_INSPECTOR_CAPTURE/PRELAUNCH_SOURCE.py').read_bytes()
assert hashlib.sha256(raw).hexdigest()==capture['source_sha256']
result=json.loads((F/'INSPECTION_RESULT.json').read_bytes())
assert result['checks_count']==840 and len(result['checks'])==840
assert len(result['foreign_external_inputs_individually_bound_and_excluded_from_authorship'])==528
assert result['builder_or_mathematical_helper_import_compile_execute'] is False
assert result['whole_current_verdict'] is None and result['NEW_whole_current_gate']=='PENDING'
commands=json.loads((F/'GIT_COMMANDS.json').read_bytes())
assert len(commands)==39
for cmd in commands:
    assert cmd['actual_execution'] is True and cmd['completed'] is True and type(cmd['pid']) is int and cmd['pid']>0 and cmd['exit_code']==0
    for channel in ['stdout','stderr']:
        row=cmd[channel];raw=(F/row['path']).read_bytes()
        assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
assert (F/'FINITE_CONTROLS/retained_failed_stage/member').read_bytes()==b'own permanently retained rejected stage'
assert (F/'FINITE_CONTROLS/existing_destination/sentinel').read_bytes()==b'unchanged sentinel'
assert (F/'SOURCE_AUDIT_REPORT.md').is_file() and (F/'FAMILY_VERDICT.json').is_file()
for p in F.rglob('*'):
    assert not p.is_symlink()
    assert p.is_file() or p.is_dir()
    if p.is_file(): assert p.stat().st_size<100*1024*1024
print(json.dumps(dict(status='OWN_RETAINED_CAPTURE_AND_CLOSURE_INPUTS_CHECKED',actual_pid=os.getpid(),inspector_pid=33351,checks=840,foreign_rows=528,read_only_Git=39,builder_or_helper_import_compile_execute=False,whole_current_verdict=None),indent=2))
