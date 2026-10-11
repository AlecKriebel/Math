"""Close only this adversary family's own artifacts; no imported code execution."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import stat

F=Path(__file__).resolve().parent
M=F/'OWN_CLOSED_MANIFEST.json'
assert not M.exists()
files=[]
directories=[]
for p in sorted(F.rglob('*')):
    assert not p.is_symlink()
    name=p.relative_to(F).as_posix()
    if p.is_file():
        raw=p.read_bytes()
        files.append(dict(path=name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),permission_mode=oct(stat.S_IMODE(p.stat().st_mode)),classification='own authored source/report/manifest or genuine own generated forensic/control capture; contained original source bytes remain attributed foreign evidence'))
    else:
        assert p.is_dir()
        directories.append(name)
expected={x.as_posix() for row in files for x in Path(row['path']).parents if x.as_posix()!='.'}
empty_extras=sorted(set(directories)-expected)
assert empty_extras==['FINITE_CONTROL_SANDBOX_v2/empty_extra','FINITE_CONTROL_SANDBOX_v2/empty_extra/extra','FINITE_CONTROL_SANDBOX_v2/fifo','FINITE_CONTROL_SANDBOX_v2/symlink']
bindings=json.loads((F/'INSPECTION_RESULT.json').read_bytes())['all_bound_files']
manifest=dict(schema='PR42_CURRENT_SOURCE_ADVERSARY_EXACT_OWN_CLOSURE_v1',utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_closer_pid=os.getpid(),status='CLOSED_SOURCE_ONLY_NARROW_MODE_GUARD_REPAIR_REQUIRED',self_excluded=['OWN_CLOSED_MANIFEST.json'],files_count=len(files),files=files,directories=directories,explicitly_retained_own_empty_finite_control_directories=empty_extras,foreign_external_inputs_individually_bound_and_excluded_from_authorship=bindings,builder_or_scientific_helper_import_compile_execute=False,original_substantive_attempts=2,new_substantive_attempts=0,audit_turns=0,whole_current_gate='PENDING',full_problem_solved=False,own_failed_actual_inspector_attempt_retained=True,no_Git_native_canonical_remote_mutations=True,no_external_human_contact=True)
M.write_text(json.dumps(manifest,indent=2)+'\n')
assert {p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file()}=={x['path'] for x in files}|{'OWN_CLOSED_MANIFEST.json'}
for row in files:
    p=F/row['path'];raw=p.read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'] and oct(stat.S_IMODE(p.stat().st_mode))==row['permission_mode']
print(json.dumps(dict(status=manifest['status'],actual_closer_pid=os.getpid(),files_count=len(files),individual_foreign_external_inputs=len(bindings),manifest_sha256=hashlib.sha256(M.read_bytes()).hexdigest(),source_report_sha256=hashlib.sha256((F/'SOURCE_AUDIT_REPORT.md').read_bytes()).hexdigest(),builder_or_scientific_helper_import_compile_execute=False),indent=2))
