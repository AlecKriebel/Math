"""Capture own closure verifier, freeze own files0444, author exact self closure."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import traceback
F=Path(__file__).resolve().parent
M=F/'OWN_CLOSED_MANIFEST.json'
assert not M.exists()
D=F/'ACTUAL_CLOSURE_INPUT_CAPTURE';D.mkdir(exist_ok=False)
S=F/'verify_own_closure_inputs.py';source=S.read_bytes();operator=Path(__file__).read_bytes()
(D/'PRELAUNCH_SOURCE.py').write_bytes(source);(D/'PRELAUNCH_OPERATOR.py').write_bytes(operator)
rec=dict(schema='PR42_V2_OWN_ACTUAL_CLOSURE_INPUT_CAPTURE_v1',operator_pid=os.getpid(),argv=['/usr/bin/python3','-B',str(S)],cwd=str(F),started_utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_execution=False,completed=False,pid=None,exit_code=None,stdin_supplied=False,source_sha256=hashlib.sha256(source).hexdigest(),operator_sha256=hashlib.sha256(operator).hexdigest(),builder_or_mathematical_helper_import_compile_execute=False)
try:
    with (D/'stdout.bin').open('xb') as out,(D/'stderr.bin').open('xb') as err:
        child=subprocess.Popen(rec['argv'],cwd=F,stdin=subprocess.DEVNULL,stdout=out,stderr=err)
        rec.update(actual_execution=True,pid=child.pid)
        try: rec['exit_code']=child.wait(timeout=45);rec['completed']=True
        except BaseException: child.kill();rec['exit_code']=child.wait();raise
except BaseException: rec['failure']=traceback.format_exc()
finally:
    rec['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
    for channel in ['stdout','stderr']:
        p=D/(channel+'.bin')
        if p.exists():
            raw=p.read_bytes();rec[channel]=dict(path=p.name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
    rec['source_unchanged']=S.read_bytes()==source;rec['operator_unchanged']=Path(__file__).read_bytes()==operator
    (D/'CAPTURE.json').write_text(json.dumps(rec,indent=2)+'\n')
if not (rec['completed'] and rec['exit_code']==0 and 'failure' not in rec):
    print(json.dumps(rec,indent=2));sys.exit(1)
files,dirs=[],[]
for p in sorted(F.rglob('*')):
    assert not p.is_symlink()
    name=p.relative_to(F).as_posix()
    if p.is_file():
        p.chmod(0o444);raw=p.read_bytes()
        assert len(raw)<100*1024*1024 and stat.S_IMODE(p.stat().st_mode)==0o444
        files.append(dict(path=name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),permission_mode='0o444',classification='own authored audit/source or genuine own forensic/finite capture; any embedded original source remains attributed foreign evidence'))
    else:
        assert p.is_dir();dirs.append(name)
expected={q.as_posix() for row in files for q in Path(row['path']).parents if q.as_posix()!='.'}
empty=sorted(set(dirs)-expected)
assert empty==['FINITE_CONTROLS/intentional_empty','FINITE_CONTROLS/intentional_empty/extra','FINITE_CONTROLS/removed_fifo_control','FINITE_CONTROLS/removed_symlink_control']
result=json.loads((F/'INSPECTION_RESULT.json').read_bytes())
manifest=dict(schema='PR42_V2_NEW_SOURCE_ADVERSARY_EXACT_OWN_CLOSURE_v1',utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_closer_pid=os.getpid(),actual_closure_input_verifier_pid=rec['pid'],status='CLOSED_SOURCE_ONLY_NO_NEW_MANDATORY_CORRECTION',self_excluded=['OWN_CLOSED_MANIFEST.json'],files_count=len(files),files=files,directories=dirs,explicitly_retained_own_empty_finite_control_directories=empty,foreign_external_inputs_individually_bound_and_excluded_from_authorship=result['foreign_external_inputs_individually_bound_and_excluded_from_authorship'],foreign_rows_count=528,all_first_party_full_permission_mode='0444',operative_preparation_manifest_sha256='c77fbc8effa07391977ed49a161001625f81bdcf1f0e647537fdae441d0b2071',operative_builder_sha256='ec426a4207c57645fe33b58b7f67acb20c45da455bf9d959077ff6f191d76a76',builder_or_mathematical_helper_import_compile_execute=False,whole_current_verdict=None,NEW_whole_current_gate='PENDING',future_ROOT_reading_or_execution_attested=False,original_substantive_attempts=2,turn_limit=5,new_substantive_attempts=0,audit_turns=0,full_problem_solved=False,actual_finite_failed_publication_stage_preserved=True,all_writes_within_own_family=True,no_Git_native_canonical_remote_mutation=True,no_external_human_contact=True)
M.write_text(json.dumps(manifest,indent=2)+'\n');M.chmod(0o444)
assert {p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file()}=={r['path'] for r in files}|{M.name}
assert sorted(p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_dir())==dirs
for row in files:
    p=F/row['path'];raw=p.read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
assert stat.S_IMODE(M.stat().st_mode)==0o444
print(json.dumps(dict(status=manifest['status'],actual_closer_pid=os.getpid(),actual_closure_verifier_pid=rec['pid'],files_count=len(files),foreign_rows=528,all_own_files_mode='0444',manifest_sha256=hashlib.sha256(M.read_bytes()).hexdigest(),report_sha256=hashlib.sha256((F/'SOURCE_AUDIT_REPORT.md').read_bytes()).hexdigest(),whole_current_verdict=None,builder_or_helper_import_compile_execute=False),indent=2))
