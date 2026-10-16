"""Close this independent family only; foreign bodies are never copied."""
from pathlib import Path, PurePosixPath
import datetime as dt, hashlib, json, os, stat
H=Path(__file__).resolve().parent
clock=lambda:dt.datetime.now(dt.timezone.utc).isoformat()
sha=lambda raw:hashlib.sha256(raw).hexdigest()
started=clock();mf=H/'OWN_CLOSED_MANIFEST.json'
if mf.exists():raise ValueError('Preserve existing closure')
result=json.loads((H/'RESULT.json').read_bytes())
control=json.loads((H/'CONTROL_RESULT.json').read_bytes())
if result['mandatory_defects'] or result['mandatory_corrections'] or control['status']!='PASS_SOURCE_ONLY':raise ValueError('Unclean source disposition')
for name in ['STATIC_ACTUAL_CAPTURE','STATIC_CORRECTED_ACTUAL_CAPTURE']:
    base=H/name;cap=json.loads((base/'CAPTURE.json').read_bytes())
    for channel in ['stdout','stderr']:
        z=cap[channel];raw=(base/z['path']).read_bytes()
        if len(raw)!=z['bytes'] or sha(raw)!=z['sha256']:raise ValueError('Actual stream changed')
    if sha((base/'PRELAUNCH_SOURCE.py').read_bytes())!=cap['source_sha256']:raise ValueError('Prelaunch source changed')
files=[];directories=set()
for p in H.rglob('*'):
    if p.is_symlink() or not(p.is_file() or p.is_dir()):raise ValueError('Unsafe own topology')
    n=p.relative_to(H).as_posix()
    if p.is_file():
        raw=p.read_bytes();files.append({'path':n,'bytes':len(raw),'sha256':sha(raw),'permission_mode':'0o444','classification':'own first-party audit artifact'})
    else:directories.add(n)
files.sort(key=lambda z:z['path'])
expected={d.as_posix() for z in files for d in PurePosixPath(z['path']).parents if d.as_posix()!='.'}
if expected!=directories:raise ValueError('Unexpected empty own directory')
manifest={'schema':'pr42-independent-acceptance-source-adversary-closure/v1','status':'CLOSED_PASS_SOURCE_ONLY','closure_pid':os.getpid(),'closure_started_utc':started,'closure_finished_utc':clock(),'self_excluded':['OWN_CLOSED_MANIFEST.json'],'files_count':len(files),'files':files,'foreign_copies_inside_family':[],'foreign_individual_read_rows':'FOREIGN_READ_ROWS.json','full_problem_solved':False,'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'proposed_helpers_imported_compiled_executed':False,'future_ROOT_execution_or_acceptance_claimed':False,'all_own_files_mode':'stat.S_IMODE0444'}
with mf.open('x') as f:json.dump(manifest,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
for p in H.rglob('*'):
    if p.is_file():p.chmod(0o444)
for z in files:
    p=H/z['path'];raw=p.read_bytes()
    if len(raw)!=z['bytes'] or sha(raw)!=z['sha256'] or stat.S_IMODE(p.stat().st_mode)!=0o444:raise ValueError('Closed own member changed')
if stat.S_IMODE(mf.stat().st_mode)!=0o444:raise ValueError('Closed own self mode differs')
print(json.dumps({'status':'CLOSED_PASS_SOURCE_ONLY','actual_closure_pid':os.getpid(),'owned_members':len(files),'manifest_sha256':sha(mf.read_bytes()),'utc':clock(),'all_own_members_and_self_S_IMODE':'0444'}))
