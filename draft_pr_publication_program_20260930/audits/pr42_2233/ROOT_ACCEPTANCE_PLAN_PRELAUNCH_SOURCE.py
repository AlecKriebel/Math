"""ROOT's actual completed-source approval; no proposed helper import or execution."""
from pathlib import Path
import copy
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess

A = Path(__file__).resolve().parent
R = A.parents[2]
H = A / 'acceptance_preparation_family'
S = A / 'acceptance_source_adversary_family'
W = A / 'whole_current_source_first_family'
def sha(raw): return hashlib.sha256(raw).hexdigest()
def load(p): return json.loads(p.read_bytes())
def pin(p):
    raw=p.read_bytes()
    return {'path':p.relative_to(R).as_posix(),'bytes':len(raw),'sha256':sha(raw)}
def output(name,obj):
    with (A/name).open('x') as f:
        json.dump(obj,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
def regular(p):
    assert p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
    return p.read_bytes()
reads=[]
def check(base,z,frozen=False):
    p=base/z['path'];raw=regular(p)
    assert type(z['bytes']) is int and len(raw)==z['bytes'] and sha(raw)==z['sha256']
    mode=stat.S_IMODE(p.stat().st_mode)
    if frozen: assert mode==0o444
    reads.append({**pin(p),'observed_full_mode':mode})
def closure(base,name,digest,count):
    raw=regular(base/name);assert sha(raw)==digest
    o=json.loads(raw);assert o['self_excluded']==[name] and o['files_count']==len(o['files'])==count
    for z in o['files']:check(base,z,True)
    names={z['path'] for z in o['files']}|{name}
    assert {p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_file()}==names
    assert {p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_dir()}=={q.as_posix() for n in names for q in Path(n).parents if str(q)!='.'}
    assert not any(p.is_symlink() for p in base.rglob('*')) and stat.S_IMODE((base/name).stat().st_mode)==0o444
    return o
assert __debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0')
source=Path(__file__).read_bytes()
with (A/'ROOT_ACCEPTANCE_PLAN_PRELAUNCH_SOURCE.py').open('xb') as f:f.write(source)
prep_sha='48358afc32922caefd8cb0fad5a59c52352d86261c5da3429e33c627c8afbe31'
source_sha='a8dac6d97ef72071a03763b4ee1ed3ce873f8e241b1a14dd35af10e0445c7bef'
closure(H,'PREPARATION_MANIFEST.json',prep_sha,27)
closure(S,'OWN_CLOSED_MANIFEST.json',source_sha,18)
inp=load(H/'INPUT_BINDINGS.json')
whole=closure(W,'OWN_CLOSED_MANIFEST.json',inp['closed_whole_manifest']['sha256'],25)
closure(A/'reviewed_candidate','MANIFEST.json',inp['current_manifest_sha256'],385)
for z in inp['pins'].values():check(R,z)
for k in ['closed_whole_result','closed_whole_report','closed_root_whole_inspection','root_capture_operator']:check(R,inp[k])
deps=load(A/'reviewed_candidate/CURRENT_DEPENDENCIES.json')
assert len(deps['files'])==517
for z in deps['files']:check(A,z)
assert len(whole['foreign_files_individually_pinned_and_excluded'])==925
for z in whole['foreign_files_individually_pinned_and_excluded']:
    p=Path(z['path']);assert p.is_relative_to(R)
    check(R,{**z,'path':p.relative_to(R).as_posix()})
verdict=load(S/'RESULT.json')
assert verdict['status']=='PASS_INDEPENDENT_ACCEPTANCE_SOURCE_ONLY_ADVERSARY'
assert verdict['mandatory_defects']==verdict['mandatory_corrections']==[]
assert verdict['source_read_completed'] is True and verdict['future_execution_or_acceptance_certified'] is False
for folder,pid,exit_code in [(S/'STATIC_ACTUAL_CAPTURE',88258,1),(S/'STATIC_CORRECTED_ACTUAL_CAPTURE',88742,0),(H/'AUTHORING_ACTUAL_CAPTURE',66343,0),(H/'CONTROLS_ACTUAL_CAPTURE',79620,0)]:
    cap=load(folder/'CAPTURE.json')
    assert cap['pid']==pid and cap['exit_code']==exit_code and cap['completed'] is True
    for channel in ['stdout','stderr']:check(folder,cap[channel])
    pre=regular(folder/'PRELAUNCH_SOURCE.py')
    assert sha(pre)==cap['source_sha256']
control=load(H/'OWN_CONTROL_RESULTS.json')
assert control['actual_pid']==79620 and control['demands']==4261 and len(control['finite_mutants_rejected'])==19
assert control['proposed_helpers_imported_compiled_executed'] is False
root=load(A/'ROOT_WHOLE_CURRENT_REVIEW.json')
assert root['status']=='PASS_ROOT_COMPLETE_CLOSED_WHOLE_INSPECTION' and root['personal_report_and_result_fully_read'] is True
assert root['complete_RESULT_object']==load(W/'RESULT.json') and root['future_execution_approved'] is False
operator=A/'capture_root_final_operation.py'
assert sha(regular(operator))=='9dee720b79e452f3ab7f945e1cac970cb9a552a42e722aadc4c254dccc365bb1'
assert pin(operator)==inp['root_capture_operator']
now=dt.datetime.now(dt.timezone.utc).isoformat()
approved=copy.deepcopy(load(H/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json'))
approved.update(status='ROOT_APPROVED_CLOSED_WHOLE_EVIDENCE',created_utc=now,root_full_current_read_completed=True,root_full_whole_read_completed=True,root_acceptance_source_review_completed=True,independent_whole_current_pass=True,whole_manifest=inp['closed_whole_manifest'],root_whole_inspection=inp['closed_root_whole_inspection'],root_capture_operator=inp['root_capture_operator'])
output('ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json',approved)
approved_pin=pin(A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json')
refs=list(inp['pins'].values())+[pin(A/'reviewed_candidate/MANIFEST.json'),pin(A/'reviewed_candidate/CURRENT_DEPENDENCIES.json'),inp['closed_whole_manifest'],inp['closed_whole_result'],inp['closed_whole_report'],inp['closed_root_whole_inspection'],inp['root_capture_operator'],approved_pin]
assert len({z['path'] for z in refs})==len(refs)==22
plan=copy.deepcopy(load(H/'DRAFT_FINAL_PLAN.json'))
plan.update(plan_status='ROOT_REVIEWED_FOR_ACTUAL_RECONCILIATION',partial_valid=True,preparation_manifest_sha256=prep_sha,root_bindings=approved_pin['path'],root_bindings_sha256=approved_pin['sha256'],whole_manifest_sha256=inp['closed_whole_manifest']['sha256'],root_full_current_read_completed=True,root_full_whole_read_completed=True,root_acceptance_source_review_completed=True,independent_whole_current_pass=True,immutable_evidence_references=sorted(refs,key=lambda z:z['path']))
assert plan['scientific_scope']==load(H/'SCIENTIFIC_SCOPE.json')
output('ROOT_FINAL_PLAN.json',plan)
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
assert subprocess.check_output(['git','branch','--show-current'],cwd=R).decode().strip()=='main'
assert subprocess.check_output(['git','diff','--cached','--name-only'],cwd=R)==b''
native=[]
for z in load(A/'ROOT_CURRENT_INPUT_PREIMAGES.json')['files']:
    p=R/z['path'];regular(p);native.append({**pin(p),'worktree_mode':stat.S_IMODE(p.stat().st_mode)})
assert len(native)==13 and len({z['path'] for z in native})==13
fresh={'schema':'pr42-root-fresh-acceptance-input-preimages/v1','approved_by_root':True,'created_utc':now,'reason_date_utc':now[:10],'reason':'ROOT completed full scientific, whole-current and acceptance-source reading; fresh actual native inputs and latest main are pinned before the authorized partial acceptance.','current_head':head,'files':native}
output('ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json',fresh)
inspection={'schema':'pr42-root-actual-acceptance-source-inspection/v1','status':'PASS_ROOT_PERSONAL_SOURCE_REVIEW_AND_ACTUAL_BOUND_INPUT_INSPECTION','created_utc':now,'actual_pid':os.getpid(),'personally_read_all_five_production_sources':True,'personally_read_entire_new_source_adversary_report_and_result':True,'preparation_manifest_sha256':prep_sha,'new_source_adversary_manifest_sha256':source_sha,'complete_source_adversary_RESULT':verdict,'all_owned_closures_and_full_modes_checked':True,'individual_actual_reads':reads,'root_immutable_bindings':approved_pin,'root_final_plan':pin(A/'ROOT_FINAL_PLAN.json'),'root_fresh13':pin(A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json'),'actual_current_main':head,'mandatory_defects':[],'mandatory_corrections':[],'proposed_helpers_executed':False,'future_runtime_PASS_claimed':False,'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False}
output('ROOT_ACCEPTANCE_SOURCE_INSPECTION.json',inspection)
assert Path(__file__).read_bytes()==source
print(json.dumps({'status':inspection['status'],'pid':os.getpid(),'actual_individual_reads':len(reads),'main':head,'bindings':approved_pin,'final_plan':pin(A/'ROOT_FINAL_PLAN.json'),'fresh13':pin(A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json'),'future_runtime_PASS_claimed':False}))
