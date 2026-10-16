#!/usr/bin/env python3
"""Own closure-input inspection; production remains text-only."""
import hashlib
import json
from pathlib import Path
import stat
here=Path(__file__).absolute().parent
controls=json.loads((here/'PRIVATE_CONTRACT_CONTROL_RESULTS.json').read_bytes())
assert controls['status']=='PASS' and controls['assertions']==5208 and controls['bound_full_input_reads']==294
assert len(controls['rejected_mutants'])==17 and controls['production_import_compile_exec'] is False
for name,digest in controls['production_source_sha256'].items():
    assert hashlib.sha256((here/name).read_bytes()).hexdigest()==digest
for directory in ['AUTHORING_ACTUAL_CAPTURE','PRIVATE_CONTROLS_ACTUAL_CAPTURE']:
    cap=json.loads((here/directory/'CAPTURE.json').read_bytes())
    assert cap['actual_execution'] is True and cap['completed'] is True and cap['exit_code']==0
    assert cap['source_unchanged'] is True and cap['operator_unchanged'] is True
    for channel in ['stdout','stderr']:
        body=(here/directory/cap[channel]['path']).read_bytes()
        assert len(body)==cap[channel]['bytes'] and hashlib.sha256(body).hexdigest()==cap[channel]['sha256']
    assert hashlib.sha256((here/directory/'PRELAUNCH_SOURCE.py').read_bytes()).hexdigest()==cap['source_sha256']
    assert hashlib.sha256((here/directory/'PRELAUNCH_OPERATOR.py').read_bytes()).hexdigest()==cap['operator_sha256']
files=0;total=0
for path in here.rglob('*'):
    assert not path.is_symlink()
    if path.is_file():
        assert stat.S_ISREG(path.stat().st_mode)
        body=path.read_bytes();files+=1;total+=len(body)
print(json.dumps({'status':'PASS_OWN_CLOSURE_INPUT_INSPECTION','files_read_before_final_capture_completion':files,
                  'bytes_read':total,'production_executed':False,'source_controls_assertions':5208},indent=2))
