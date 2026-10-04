"""ROOT's genuine closed whole-current inspection, after personal report reading."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess

A=Path(__file__).resolve().parent
R=A.parents[2]
F=A/'whole_current_source_first_family'
PIN='ea6416b54945bf80d0a706cf878c8de707464ddcdaea66ae0e812868ff547c9f'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def pairs(rows):
    o={}
    for k,v in rows:
        if k in o:raise ValueError('Duplicate JSON key')
        o[k]=v
    return o
def parse(raw):return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
def read(p,digest=None,size=None):
    assert p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
    assert p.resolve(strict=True).is_relative_to(R.resolve())
    raw=p.read_bytes()
    if digest is not None:assert sha(raw)==digest
    if size is not None:assert type(size) is int and len(raw)==size
    return raw
def clock(value):
    t=dt.datetime.fromisoformat(value.replace('Z','+00:00'))
    assert t.utcoffset()==dt.timedelta(0)
    return t
assert __debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0')
source=Path(__file__).read_bytes()
with (A/'ROOT_CLOSED_WHOLE_INSPECTION_PRELAUNCH_SOURCE_V2.py').open('xb') as f:f.write(source)
mf=parse(read(F/'SELF_MANIFEST.json',PIN))
assert mf['schema']=='pr44-whole-current-source-first-self-only-closure/v1'
assert mf['files_count']==len(mf['files'])==96 and mf['self_excluded']==['SELF_MANIFEST.json']
names={z['path'] for z in mf['files']}|{'SELF_MANIFEST.json'}
assert len(names)==97
assert {p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file()}==names
dirs={p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_dir()}
assert dirs=={q.as_posix() for n in names for q in Path(n).parents if str(q)!='.'}==set(mf['directories'])
assert not any(p.is_symlink() for p in F.rglob('*'))
own_bytes=0
for z in mf['files']:
    raw=read(F/z['path'],z['sha256'],z['bytes']);own_bytes+=len(raw)
    assert stat.S_IMODE((F/z['path']).stat().st_mode)==0o444
    if z['path'].endswith('.json'):parse(raw)
assert stat.S_IMODE((F/'SELF_MANIFEST.json').stat().st_mode)==0o444
foreign=parse(read(F/mf['foreign_inputs_manifest']))['files']
assert len(foreign)==len({z['path'] for z in foreign})==964
foreign_bytes=0
dated_changes=[]
dated_git_captures=[]
dated_head='2b9d0234b1396fa84c4b34055b5e8e14c873588b'
dated_four={'unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl','draft_pr_publication_program_20260930/inventory.json'}
freeze=parse(read(A/'ROOT_CURRENT_INPUT_PREIMAGES.json'))
assert freeze['current_head']==dated_head
dated_pins={z['path']:z for z in freeze['files']}
for z in foreign:
    p=R/z['path'];assert not p.resolve().is_relative_to(F.resolve())
    canonical=p.resolve(strict=True).relative_to(R.resolve()).as_posix()
    if canonical in dated_four:
        expected=dated_pins[canonical]
        assert expected['bytes']==z['bytes'] and expected['sha256']==z['sha256']
        argv=['git','show',dated_head+':'+canonical]
        started=dt.datetime.now(dt.timezone.utc).isoformat()
        child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        raw,err=child.communicate()
        assert child.returncode==0 and len(raw)==z['bytes'] and sha(raw)==z['sha256']
        capture=A/('root_closed_whole_v2_dated_'+Path(canonical).name.replace('.','_'))
        capture.mkdir(exist_ok=False)
        (capture/'stdout.bin').write_bytes(raw);(capture/'stderr.bin').write_bytes(err)
        dated_git_captures.append({'argv':argv,'pid':child.pid,'started_utc':started,'finished_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'exit_code':child.returncode,'stdout':{'path':(capture/'stdout.bin').relative_to(R).as_posix(),'bytes':len(raw),'sha256':sha(raw)},'stderr':{'path':(capture/'stderr.bin').relative_to(R).as_posix(),'bytes':len(err),'sha256':sha(err)}})
        actual=read(p)
        if actual!=raw:dated_changes.append({'path':canonical,'historical_bytes':len(raw),'historical_sha256':sha(raw),'present_bytes':len(actual),'present_sha256':sha(actual),'qualification':'Dated immutable Git source input, not present shared-state authority; fresh integration must retain and protect actual present inputs separately.'})
        foreign_bytes+=len(raw)
    else:foreign_bytes+=len(read(p,z['sha256'],z['bytes']))
verdict=parse(read(F/'VERDICT.json','f6f534bd886a333220b854cf095c2887d37650dcf3dfe914929a140aa1b93788'))
read(F/'REPORT.md','eddf2f62d50112d6c090f806bf13353c8e28426050da593b8d7c501ad95fa6ca')
assert verdict['verdict']=='PASS_SCOPED_ACTUAL_WHOLE_CURRENT_STANDARD_PARTIAL_ONLY'
assert all(verdict[k]==[] for k in ['mandatory_mathematical_corrections','mandatory_source_scope_corrections','mandatory_current_contract_corrections'])
assert verdict['full_problem_solved'] is verdict['novelty_claimed'] is False
assert verdict['candidate_manifest_sha256']=='169f2825a8f730735627bdc33a43366c05e317fdf7ec4df4cd96a31e37329eb0'
assert (verdict['original_substantive_attempts'],verdict['new_substantive_attempts'],verdict['audit_turns'])==(2,0,0)
assert verdict['future_ROOT_reconciliation_acceptance_or_merge_approved'] is False
captures=[]
for folder,pid,code in [('actual_controls_20261003T022840.304448Z',77312,1),('actual_controls_20261003T022907.830918Z',77659,0),('actual_controls_20261003T023052.188930Z',79792,0),('FINAL_INSPECTION_ACTUAL_CAPTURE',86002,0),('FINAL_INSPECTION_TIME_PRECISION_ACTUAL_CAPTURE',87613,1),('FINAL_INSPECTION_CORRECTED_CLOSURE_ACTUAL_CAPTURE',88925,0)]:
    cap=parse(read(F/folder/'CAPTURE.json'))
    assert cap['pid']==pid and cap['exit_code']==code and cap['actual_execution'] is True and cap['completed'] is True
    assert clock(cap['started_utc'])<=clock(cap['finished_utc'])<=dt.datetime.now(dt.timezone.utc)
    read(F/folder/'PRELAUNCH_SOURCE.py',cap['source_sha256']);read(F/folder/'PRELAUNCH_OPERATOR.py',cap['operator_sha256'])
    pre=parse(read(F/folder/'PRELAUNCH.json'));assert all(pre[k]==cap[k] for k in ['schema','operator_pid','argv','cwd','started_utc','source_sha256','operator_sha256','stdin_supplied'])
    assert pre['actual_execution'] is pre['completed'] is False and pre['pid'] is pre['exit_code'] is None
    for channel in ['stdout','stderr']:
        z=cap[channel];read(F/folder/z['path'],z['sha256'],z['bytes'])
    captures.append(cap)
result=parse(read(F/'RESULT.json'))
assert result['actual_pid']==79792 and result['own_assertions']==75769 and result['rejected_count']==51 and result['full_SQL_rows']==15458 and result['full_raw_bytes']==149266659 and result['prior_key_present'] is False
own_git=parse(read(F/'IMMUTABLE_GIT_COMMANDS.json'))
for cap in own_git:
    assert cap['actual_execution'] is cap['completed'] is True and type(cap['pid']) is int and cap['pid']>0 and cap['exit_code']==0
    for k in ['stdout','stderr']:z=cap[k];read(F/z['path'],z['sha256'],z['bytes'])
obj={'schema':'pr44-root-complete-closed-whole-inspection/v1','status':'PASS_ROOT_COMPLETE_CLOSED_WHOLE_INSPECTION','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'candidate_manifest_sha256':verdict['candidate_manifest_sha256'],'closed_whole_manifest_sha256':PIN,'first_party_members':96,'individually_bound_foreign_inputs':964,'complete_VERDICT_object':verdict,'personal_report_and_verdict_fully_read':True,'all_first_party_whole_bytes_and_modes_checked':True,'all_foreign_individual_whole_bytes_checked':True,'exact_self_only_recursive_closure_checked':True,'complete_actual_captures_checked':captures,'mandatory_defects':[],'mandatory_corrections':[],'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'full_target_resolved_in_prior_published_literature':False,'full_problem_solved_by_project':False,'future_execution_approved':False}
obj.update(dated_four_native_source_head=dated_head,complete_dated_git_captures=dated_git_captures,legitimate_dated_native_changes=dated_changes,source_and_failure_qualification='Every original own failure and positive metadata defect is preserved; actual79792 and final88925 are operative. Four native bodies are checked from immutable frozen2b9d023 Git, the other960 individually pinned inputs live. No rebind to present main; actual present preimages require a separate acceptance epoch. Full report/verdict personally read; finite controls do not prove the missing geometric realization.')
with (A/'ROOT_WHOLE_CURRENT_REVIEW.json').open('x') as f:json.dump(obj,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
assert Path(__file__).read_bytes()==source
print(json.dumps({'status':obj['status'],'own_member_bytes':own_bytes,'foreign_input_bytes':foreign_bytes,'first_party_members':96,'foreign_inputs':964,'actual_pid':os.getpid(),'future_execution_approved':False}))
