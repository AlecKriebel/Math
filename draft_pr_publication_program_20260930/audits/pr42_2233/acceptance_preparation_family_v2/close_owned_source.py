"""Close only this adjacent source family; no proposed helper execution."""
from pathlib import Path
import datetime as dt,hashlib,json,os,stat
H=Path(__file__).resolve().parent
def sha(raw):return hashlib.sha256(raw).hexdigest()
mf=H/'PREPARATION_MANIFEST.json'
if mf.exists():raise ValueError('Already closed: preserve and inspect')
controls=json.loads((H/'OWN_CONTROL_RESULTS.json').read_bytes())
if controls['status']!='PASS_OWN_SOURCE_ONLY_REPAIR_CONTROLS' or controls['proposed_helpers_imported_compiled_executed'] is not False:raise ValueError('Own actual repair controls incomplete')
for name in ['AUTHORING_ACTUAL_CAPTURE','DATED_NATIVE_REVISION_ACTUAL_CAPTURE','CONTROLS_ACTUAL_CAPTURE']:
    root=H/name;rec=json.loads((root/'CAPTURE.json').read_bytes())
    if rec['completed'] is not True or rec['exit_code']!=0 or type(rec['pid']) is not int or rec['pid']<=0:raise ValueError('Actual own source capture failed')
    for key in ['stdout','stderr']:
        z=rec[key];raw=(root/z['path']).read_bytes()
        if len(raw)!=z['bytes'] or sha(raw)!=z['sha256']:raise ValueError('Actual own full stream changed')
    if sha((root/'PRELAUNCH_SOURCE.py').read_bytes())!=rec['source_sha256']:raise ValueError('Own actual prelaunch source changed')
queries=json.loads((H/'DATED_GIT_NATIVE4_ACTUAL_QUERY_CAPTURE/QUERY_RECEIPTS.json').read_bytes())['queries']
if len(queries)!=8:raise ValueError('Actual complete historical Git queries required')
for rec in queries:
    if rec['completed'] is not True or rec['exit_code']!=0 or type(rec['pid']) is not int or rec['pid']<=0:raise ValueError('Actual historical Git query failed')
    for key in ['stdout','stderr']:
        z=rec[key];raw=(H/'DATED_GIT_NATIVE4_ACTUAL_QUERY_CAPTURE'/z['path']).read_bytes()
        if len(raw)!=z['bytes'] or sha(raw)!=z['sha256']:raise ValueError('Historical Git full stream changed')
status_path=H/'SOURCE_STATUS.json';status=json.loads(status_path.read_bytes());status['source_preparation_complete']=True;status['independent_V2_acceptance_source_verdict']=None
status_path.write_text(json.dumps(status,indent=2)+'\n')
utc=dt.datetime.now(dt.timezone.utc).isoformat()
with (H/'RESEARCH_LOG.md').open('a') as out:
    out.write('\n'+utc+' — Actual closure PID'+str(os.getpid())+' sealed this adjacent own source family. Own actual controls'+str(controls['actual_pid'])+' passed'+str(controls['demands'])+' demands/'+str(len(controls['rejected_mutants']))+' rejected mutants; original925 rows, actual3 aliases, dated native4 and other921 live rows checked. Preparation100%; full mathematical discovery0%. New different adversary/ROOT personal V2 source approval remain pending. No proposed helper or native/Git/remote/people mutation executed.\n')
files=[];dirs=set()
for p in H.rglob('*'):
    if p.is_symlink() or not (p.is_file() or p.is_dir()):raise ValueError('Unsafe own topology')
    if p.is_file():
        raw=p.read_bytes();files.append({'path':p.relative_to(H).as_posix(),'bytes':len(raw),'sha256':sha(raw)})
    else:dirs.add(p.relative_to(H).as_posix())
files.sort(key=lambda z:z['path']);expected={q.as_posix() for z in files for q in Path(z['path']).parents if q.as_posix()!='.'}
if dirs!=expected:raise ValueError('Unexpected empty directories')
record={'schema':'pr42-acceptance-source-closure/v1','status':'CLOSED_SOURCE_ONLY','utc':utc,'self_excluded':['PREPARATION_MANIFEST.json'],'files_count':len(files),'files':files,'source_only':True,'proposed_helpers_imported_compiled_executed':False,'future_acceptance_or_ROOT_approval_claimed':False}
with mf.open('x') as out:json.dump(record,out,indent=2);out.write('\n');out.flush();os.fsync(out.fileno())
for p in H.rglob('*'):
    if p.is_file():p.chmod(0o444)
for z in files:
    p=H/z['path'];raw=p.read_bytes()
    if len(raw)!=z['bytes'] or sha(raw)!=z['sha256'] or stat.S_IMODE(p.stat().st_mode)!=0o444:raise ValueError('Own closure changed')
if stat.S_IMODE(mf.stat().st_mode)!=0o444:raise ValueError('Own literal self mode differs')
print(json.dumps({'status':'CLOSED_SOURCE_ONLY','actual_closure_pid':os.getpid(),'utc':utc,'own_members':len(files),'manifest_sha256':sha(mf.read_bytes()),'all_own_members_and_self_stat_S_IMODE':'0444','proposed_helpers_imported_compiled_executed':False,'future_ROOT_approval_or_acceptance_claimed':False}))
