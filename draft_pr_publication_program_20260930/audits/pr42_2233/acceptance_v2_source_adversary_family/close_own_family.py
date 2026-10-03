"""Seal this new adversary's authored files only, preserving individual outside references."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat
H=Path(__file__).resolve().parent
def sha(raw):return hashlib.sha256(raw).hexdigest()
start=dt.datetime.now(dt.timezone.utc).isoformat()
mf=H/'OWN_CLOSED_MANIFEST.json'
assert not mf.exists() and not mf.is_symlink()
result=json.loads((H/'CONTROL_RESULT.json').read_bytes())
verdict=json.loads((H/'VERDICT.json').read_bytes())
assert result['actual_pid']==verdict['own_actual_control_pid']==13786
assert result['status']=='PASS_OWN_SOURCE_ONLY_INDEPENDENT_CONTROLS'
assert verdict['mandatory_defects']==verdict['mandatory_corrections']==[]
assert result['proposed_native_candidate_helpers_imported_compiled_executed'] is False
cap=json.loads((H/'STATIC_ACTUAL_CAPTURE/CAPTURE.json').read_bytes())
assert cap['actual_execution'] is True and cap['completed'] is True and cap['exit_code']==0 and cap['pid']==13786
assert sha((H/'STATIC_ACTUAL_CAPTURE/PRELAUNCH_SOURCE.py').read_bytes())==cap['source_sha256']
for channel in ['stdout','stderr']:
    z=cap[channel];raw=(H/'STATIC_ACTUAL_CAPTURE'/z['path']).read_bytes()
    assert len(raw)==z['bytes'] and sha(raw)==z['sha256']
assert json.loads((H/'STATIC_ACTUAL_CAPTURE/stdout.bin').read_bytes())==result
reads=json.loads((H/'INDIVIDUAL_INPUT_READS.json').read_bytes())['files']
assert len(reads)==2126 and sum(z['bytes'] for z in reads)==368092959
foreign=[];seen=set()
for row in reads:
    key=(row['path'],row.get('authority','live_worktree'),row['sha256'],row.get('worktree_mode'))
    if key in seen:continue
    seen.add(key)
    assert not Path(row['path']).resolve().is_relative_to(H)
    foreign.append({k:v for k,v in row.items() if k!='reason'})
queries=json.loads((H/'READONLY_GIT_CAPTURE/QUERIES.json').read_bytes())['queries']
assert len(queries)==10
for query in queries:
    assert type(query['pid']) is int and query['pid']>0 and query['exit_code']==0 and query['completed'] is True
    for channel in ['stdout','stderr']:
        row=query[channel];raw=(H/'READONLY_GIT_CAPTURE'/row['path']).read_bytes()
        assert len(raw)==row['bytes'] and sha(raw)==row['sha256']
now=dt.datetime.now(dt.timezone.utc).isoformat()
with (H/'RESEARCH_LOG.md').open('a') as log:
    log.write('\n'+now+' — Own actual control13786 exited0 with33603 demands,2126 complete reads/368092959 bytes,34 mutants,925 whole rows/3 aliases/4 immutable historical Git native rows/921 live, and real private filesystem/full-mode probes. All production/native/candidate sources remain unexecuted. Mandatory defects and corrections empty. Source audit100%; mathematical discovery0%; original2/5,new0,audit0. Closing own self-only444 family at actual PID'+str(os.getpid())+'. ROOT approval and every operational outcome remain pending.\n')
files=[];directories=set()
for p in H.rglob('*'):
    assert not p.is_symlink()
    n=p.relative_to(H).as_posix()
    if p.is_file():
        raw=p.read_bytes();files.append({'path':n,'bytes':len(raw),'sha256':sha(raw),'permission_mode':'0o444','classification':'own_authored_report_control_source_or_actual_capture'})
    else:assert p.is_dir();directories.add(n)
files.sort(key=lambda z:z['path'])
expected={p.as_posix() for z in files for p in Path(z['path']).parents if p.as_posix()!='.'}
assert directories==expected
finish=dt.datetime.now(dt.timezone.utc).isoformat()
record={'schema':'PR42_NEW_DIFFERENT_V2_ACCEPTANCE_SOURCE_ADVERSARY_CLOSED_FAMILY_v1',
        'status':'CLOSED_PASS_NEW_DIFFERENT_V2_ACCEPTANCE_SOURCE_ONLY_ADVERSARY',
        'root':str(H),'closure_pid':os.getpid(),'closure_started_utc':start,'closure_finished_utc':finish,
        'self_excluded':['OWN_CLOSED_MANIFEST.json'],'files_count':len(files),'files':files,
        'foreign_files_individually_pinned_and_excluded':foreign,
        'foreign_primary_or_derivative_copies_inside_family':[],
        'historical_native_query_outputs_are_own_actual_captured_Git_streams':True,
        'all_own_files_mode':'stat.S_IMODE0444',
        'preparation_manifest_sha256':verdict['preparation_manifest_sha256'],
        'report_sha256':sha((H/'FINAL_REPORT.md').read_bytes()),'verdict_sha256':sha((H/'VERDICT.json').read_bytes()),
        'proposed_native_candidate_helpers_imported_compiled_executed':False,'ROOT_approval_authored':False,
        'future_runtime_or_acceptance_certified':False,'original_substantive_attempts':2,
        'substantive_attempt_limit':5,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False}
with mf.open('x') as stream:
    json.dump(record,stream,indent=2);stream.write('\n');stream.flush();os.fsync(stream.fileno())
for p in H.rglob('*'):
    if p.is_file():p.chmod(0o444)
for z in files:
    p=H/z['path'];raw=p.read_bytes()
    assert len(raw)==z['bytes'] and sha(raw)==z['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
assert stat.S_IMODE(mf.stat().st_mode)==0o444
print(json.dumps({'status':record['status'],'actual_closure_pid':os.getpid(),'own_members':len(files),'foreign_unique_individual_rows':len(foreign),'manifest_sha256':sha(mf.read_bytes()),'report_sha256':record['report_sha256'],'verdict_sha256':record['verdict_sha256'],'future_runtime_or_acceptance_certified':False}))
