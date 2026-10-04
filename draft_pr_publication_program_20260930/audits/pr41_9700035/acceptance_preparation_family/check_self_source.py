#!/usr/bin/env python3
"""Own read/static-only final check. Never imports or executes proposed helpers."""
import ast
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path,PurePosixPath

P=Path(__file__).resolve().parent;A=P.parent;R=A.parents[2]
SHA=lambda b:hashlib.sha256(b).hexdigest()
READ={}
def parse(b):
 def pairs(v):
  o={}
  for k,z in v:
   assert k not in o,'Duplicate JSON key';o[k]=z
  return o
 def floating(v):
  z=float(v);assert math.isfinite(z);return z
 return json.loads(b,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))
def read(p):
 assert p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
 b=p.read_bytes();READ[p.relative_to(R).as_posix()]={'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':SHA(b)}
 if p.suffix=='.json':parse(b)
 return b
def exact(root,names):
 files=set();dirs=set()
 for q in root.rglob('*'):
  assert not q.is_symlink()
  if q.is_file():files.add(q.relative_to(root).as_posix())
  else:assert q.is_dir();dirs.add(q.relative_to(root).as_posix())
 assert files==set(names)
 assert dirs=={q.as_posix() for n in files for q in PurePosixPath(n).parents if q.as_posix()!='.'}
def rows(root,rr):
 assert len(rr)==len({z['path'] for z in rr})
 for z in rr:
  n=z['path'];q=PurePosixPath(n)
  assert not q.is_absolute() and not {'.','..','.git','__pycache__'}.intersection(q.parts) and q.as_posix()==n
  b=read(root/n);assert len(b)==z.get('bytes',z.get('size')) and SHA(b)==z['sha256']
def typed_same(a,b):
 return type(a) is type(b) and (a.keys()==b.keys() and all(typed_same(a[k],b[k]) for k in a) if type(a) is dict else len(a)==len(b) and all(typed_same(x,y) for x,y in zip(a,b)) if type(a) is list else a==b)

helpers=['pr41_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']
texts={}
for n in helpers:
 b=read(P/n);ast.parse(b);texts[n]=b.decode()
for q in sorted(P.rglob('*')):
 if q.is_file():
  b=read(q)
  if q.suffix=='.py':ast.parse(b)
inputs=parse(read(P/'INPUT_BINDINGS.json'));assert inputs['source_only'] is True
for z in inputs['pins'].values():rows(R,[z])
for c in inputs['closures']:
 root=A/c['directory'];assert SHA(read(root/c['manifest_name']))==c['manifest_sha256']
 rr=c['members']+c['foreign_members'];rows(root,rr);exact(root,{z['path'] for z in rr}|{c['manifest_name']})
c=A/'reviewed_candidate';raw=read(c/'MANIFEST.json');assert SHA(raw)=='3431ca2dfb332500f3815ea1e61f089744b3bacd9c3659018537016b9396fbfa'
cm=parse(raw);assert len(cm['files'])==547;rows(c,cm['files']);exact(c,{z['path'] for z in cm['files']}|{'MANIFEST.json'})
assert all(q.stat().st_mode&0o777==0o444 for q in c.rglob('*') if q.is_file())
d=parse(read(c/'CURRENT_PROOF_DEPENDENCIES.json'));assert len(d['files'])==469;rows(A,d['files'])
assert SHA((c/'CURRENT_PROOF_DEPENDENCIES.json').read_bytes())=='ade2f6fe9890f1038810158a284f4a8924e34d6d2f95b3a07654d78fa6501ff6'
w=A/'whole_current_source_first_family';wm=inputs['whole_observed_only'];rows(R,[wm]);wo=parse(read(w/'FIRST_PARTY_MANIFEST.json'))
assert len(wo['files'])==143 and len(wo['foreign_files'])==17
rows(w,wo['files']+wo['foreign_files']);exact(w,{z['path'] for z in wo['files']+wo['foreign_files']}|{'FIRST_PARTY_MANIFEST.json'})
assert all(q.stat().st_mode&0o777==0o444 for q in w.rglob('*') if q.is_file())
rows(R,[inputs['root_whole_observed']]);rv=parse(read(R/inputs['root_whole_observed']['path']))
assert rv['status']=='PASS' and rv['authored_members']==143 and rv['separately_bound_foreign_members']==17 and typed_same(rv['whole_independent_verdict'],parse(read(w/'RESULT.json')))
plan=parse(read(P/'DRAFT_FINAL_PLAN.json'));bindings=parse(read(P/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json'));future=parse(read(P/'DRAFT_FUTURE_GATE_PINS.json'));science=parse(read(P/'SCIENTIFIC_SCOPE.json'))
for q in [plan,bindings]:
 for n in ['root_full_current_read_completed','root_full_whole_read_completed','independent_whole_current_pass']:assert q[n] is False
 assert q['new_substantive_attempts']==0 and type(q['new_substantive_attempts']) is int and q['audit_turns']==0 and type(q['audit_turns']) is int
assert plan['partial_valid'] is False and plan['immutable_evidence_references']==[]
for n in ['whole_manifest_sha256','preparation_manifest_sha256','root_bindings','root_bindings_sha256']:assert plan[n] is None
assert bindings['created_utc'] is None and bindings['whole_manifest'] is None and bindings['root_whole_inspection'] is None
for n,v in future.items():
 if n!='status':assert v is (False if n=='actual_execution' else None)
assert typed_same(plan['scientific_scope'],science)
assert science['literal_target_status']=='UNSOLVED' and science['full_problem_solved'] is False and science['novelty_claimed'] is False
assert science['source_preparation_actual_acceptance_execution']=='NOT_PERFORMED_IN_THIS_SOURCE_PREPARATION'
for n in ['current_model','current_reasoning_effort','current_deadline_utc']:assert science[n] is None and plan[n] is None
guards=texts['pr41_guards.py'];integration=texts['integrate_reviewed_partial.py'];seal=texts['seal_final_evidence.py'];mirror=texts['state_mirror_reconciliation.py'];post=texts['verify_post_acceptance.py']
for n in ['root_whole_observed','whole_observed_only','worktree_mode','def native_modes','mode==\'100644\'','entries==b\'\'','Exact complete accepted ledger/budget required; no inference','len(stream_names)==2','Exactly four distinct capture members required','started<=utc_clock(receipt[\'utc\']','len(ledger[\'root_flags\'])==8']:
 assert n in guards,n
for n in ['g.native_modes(fresh[\'files\'])','target.parent.mkdir(parents=True,exist_ok=True)','g.A/\'ROOT_RESEARCH_LOG.md\'','integration_log_preimages','CURRENT_CONTEXT_PRESENT.md','g.tree(merge,pre,overlay,after)']:assert n in integration,n
assert "g.git('branch','--show-current')=='main'" in seal
assert "plan['primary_count']==31" in mirror and "len(plan['state_after'])==32" in mirror and "==39" in mirror and "len(plan['history_append'])==1" in mirror
assert "replay['history_append']==[]" in post and "set(current)==set(old)|{g.ID}" in post
admin={'status.json','attempt.json','readiness.json','review/verdict.json'}
overlay={z['path'] for z in cm['files']}|{'reviewed_pending_administration/'+n for n in admin}|{'reviewed_pending_administration/MANIFEST.json','ACCEPTED_QUEUE_PATCH.json','CURRENT_ACCEPTANCE_SCOPE.md','CURRENT_CONTEXT_PRESENT.md','CURRENT_AUDIT_SCOPE_PRESENT.md'}
assert len(overlay)==556 and len(overlay|{'acceptance.json','ACCEPTANCE.md','MANIFEST.json'})==559
for name in ['source_author_actual_capture','contracts_author_actual_capture']:
 root=P/name;cap=parse(read(root/'CAPTURE.json'));assert type(cap['pid']) is int and cap['pid']>0 and type(cap['exit_code']) is int and cap['exit_code']==0 and cap['completed'] is True and cap['actual_execution'] is True and cap['stdin_supplied'] is False
 rows(root,[cap['stdout'],cap['stderr']]);assert SHA(read(root/'prelaunch_source.py'))==cap['source_sha256']
 exact(root,{'CAPTURE.json','prelaunch_source.py',cap['stdout']['path'],cap['stderr']['path']})
for n in ['README.md','CONTRACT.md','READ_EXPECTATIONS.md','SOURCE_CHANGE_RECORD.md','RESEARCH_LOG.md']:assert read(P/n).strip()
now=dt.datetime.now(dt.timezone.utc).isoformat()
result={'status':'PASS_OWN_FULL_SOURCE_READ_AND_STATIC_ONLY_CHECK','utc':now,'actual_pid':os.getpid(),'helper_sources':[READ[(P/n).relative_to(R).as_posix()] for n in helpers],'files':sorted(READ.values(),key=lambda z:z['path']),'unique_full_files':len(READ),'full_bytes':sum(z['bytes'] for z in READ.values()),'current_members':547,'dependency_members':469,'whole_authored':143,'whole_foreign':17,'overlay_files':556,'accepted_authored_files_excluding_root_self':558,'proposed_helpers_imported_or_executed':False,'own_scientific_reexecution_claimed':False,'native_canonical_Git_index_remote_shared_writes':False,'future_gate_PASS_claimed':False,'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'source_preparation_estimate_percent':100,'unconditional_discovery_estimate_percent':0,'new_independent_review_and_ROOT_full_read':'STILL_REQUIRED'}
out=P/'FINAL_STATIC_INSPECTION.json';assert not out.exists();out.write_text(json.dumps(result,indent=2)+'\n')
status={k:v for k,v in result.items() if k not in {'files','helper_sources','unique_full_files','full_bytes'}};status['status']='SOURCE_ONLY_SELF_REVIEW_COMPLETE_PENDING_INDEPENDENT_REVIEW_AND_ROOT_EXECUTION';(P/'SOURCE_STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in {'files','helper_sources'}},indent=2))
