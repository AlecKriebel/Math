#!/usr/bin/env python3
"""Own full-byte/static and isolated finite specification models; no candidate load."""
import ast
import copy
import datetime as dt
import difflib
import hashlib
import json
import math
import os
import stat
from pathlib import Path,PurePosixPath
P=Path(__file__).resolve().parent;A=P.parent;R=A.parents[2]
READ={};CHECKS=[];TYPED=0
sha=lambda b:hashlib.sha256(b).hexdigest()
def parse(b):
 def pairs(rr):
  o={}
  for k,v in rr:
   assert k not in o,'Duplicate JSON key';o[k]=v
  return o
 def floating(v):
  n=float(v);assert math.isfinite(n);return n
 return json.loads(b,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))
def nodes(x):
 global TYPED
 TYPED+=1
 if type(x) is dict:
  for v in x.values():nodes(v)
 elif type(x) is list:
  for v in x:nodes(v)
def read(p):
 assert p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
 b=p.read_bytes();key=p.relative_to(R).as_posix();first=key not in READ
 READ[key]={'path':key,'bytes':len(b),'sha256':sha(b),'worktree_mode':stat.S_IMODE(p.stat().st_mode)}
 if first and p.suffix=='.json':nodes(parse(b))
 if first and p.suffix=='.jsonl':
  assert not b or b.endswith(b'\n')
  for line in b.splitlines():nodes(parse(line))
 return b
def same(a,b):
 if type(a) is not type(b):return False
 if type(a) is dict:return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
 if type(a) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
def exact(root,names):
 files=set();dirs=set()
 for q in root.rglob('*'):
  assert not q.is_symlink()
  if q.is_file():files.add(q.relative_to(root).as_posix())
  else:assert q.is_dir();dirs.add(q.relative_to(root).as_posix())
 assert files==set(names)
 assert dirs=={q.as_posix() for n in files for q in PurePosixPath(n).parents if q.as_posix()!='.'}
def checked_rows(root,rr,mode=None):
 assert len(rr)==len({z['path'] for z in rr})
 for z in rr:
  n=z['path'];q=PurePosixPath(n);assert not q.is_absolute() and q.as_posix()==n and not {'.','..','.git','__pycache__'}.intersection(q.parts)
  b=read(root/n);assert len(b)==z.get('bytes',z.get('size')) and sha(b)==z['sha256']
  if mode is not None:assert stat.S_IMODE((root/n).stat().st_mode)==mode
def put(n,obj):
 q=P/n;assert not q.exists();q.write_text(json.dumps(obj,indent=2)+'\n')
def control(n,observed,expected,kind):
 assert observed is expected,n
 CHECKS.append({'name':n,'observed':observed,'expected':expected,'kind':kind,'status':'PASS_OWN_PRIVATE_SPECIFICATION_CONTROL'})

helpers=['pr41_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py'];source={}
for n in helpers:
 b=read(P/n);ast.parse(b);source[n]=b.decode()
pins=parse(read(P/'REVISION_SOURCE_BINDINGS.json'));checked_rows(P,pins['repaired_sources'])
delta=[]
for n in helpers:
 old=read(A/'acceptance_preparation_family'/n).decode();delta.extend(difflib.unified_diff(old.splitlines(True),source[n].splitlines(True),fromfile='closed_v1/'+n,tofile='proposed_v2/'+n))
assert ''.join(delta).encode()==read(P/'SOURCE_DELTAS.patch')
inputs=parse(read(P/'INPUT_BINDINGS.json'))
for z in inputs['pins'].values():checked_rows(R,[z])
for c in inputs['closures']:
 root=A/c['directory'];assert sha(read(root/c['manifest_name']))==c['manifest_sha256'];rr=c['members']+c['foreign_members']
 checked_rows(root,rr,0o444 if c.get('requires_all_members_0444') else None);exact(root,{z['path'] for z in rr}|{c['manifest_name']})
 if c.get('requires_all_members_0444'):assert stat.S_IMODE((root/c['manifest_name']).stat().st_mode)==0o444
adv=A/'acceptance_static_adversary_family';am=parse(read(adv/'FIRST_PARTY_MANIFEST.json'));assert sha((adv/'FIRST_PARTY_MANIFEST.json').read_bytes())=='31c82a50855cf621859d6bfa182541ec07d77a3727d621ce4adc99597620c6c0'
foreign=am['individual_external_foreign_dependencies_excluded_from_authored_copy'];assert len(foreign)==46;checked_rows(R,foreign)
for z in foreign:assert stat.S_IMODE((R/z['path']).stat().st_mode)==z['worktree_mode']
read(adv/'REPORT.md');ar=parse(read(adv/'RESULT.json'));assert [z['id'] for z in ar['mandatory_repairs']]==['S1','S2','S3']
falsifiers=parse(read(adv/'FINITE_CONTROLS_RESULT.json'));assert falsifiers['checks_count']==25 and len(falsifiers['inventory_mutants'])==7
c=A/'reviewed_candidate';cm=parse(read(c/'MANIFEST.json'));assert len(cm['files'])==547;checked_rows(c,cm['files'],0o444);exact(c,{z['path'] for z in cm['files']}|{'MANIFEST.json'});assert stat.S_IMODE((c/'MANIFEST.json').stat().st_mode)==0o444
deps=parse(read(c/'CURRENT_PROOF_DEPENDENCIES.json'));assert len(deps['files'])==469;checked_rows(A,deps['files'])
w=A/'whole_current_source_first_family';wm=parse(read(w/'FIRST_PARTY_MANIFEST.json'));assert len(wm['files'])==143 and len(wm['foreign_files'])==17;checked_rows(w,wm['files']+wm['foreign_files'],0o444);assert stat.S_IMODE((w/'FIRST_PARTY_MANIFEST.json').stat().st_mode)==0o444
checked_rows(R,[inputs['root_whole_observed']]);root_whole=parse(read(R/inputs['root_whole_observed']['path']));assert same(root_whole['whole_independent_verdict'],parse(read(w/'RESULT.json')))
for n in ['SCIENTIFIC_SCOPE.json','DRAFT_FINAL_PLAN.json','DRAFT_ROOT_IMMUTABLE_BINDINGS.json','DRAFT_FUTURE_GATE_PINS.json']:assert read(P/n)==read(A/'acceptance_preparation_family'/n)
for q in sorted(P.rglob('*')):
 if q.is_file():
  b=read(q)
  if q.suffix=='.py':ast.parse(b)
g=source['pr41_guards.py'];i=source['integrate_reviewed_partial.py'];m=source['state_mirror_reconciliation.py'];post=source['verify_post_acceptance.py'];s=source['seal_final_evidence.py']
for n in ['def derive_inventory','def expected_acceptance','def finalization','stat.S_IMODE(regular(base,n).stat().st_mode)==0o444','if frozen:frozen_files(base,rr,name)','Complete typed external ROOT bindings schema/value equality required',"set(obj)=={'path','bytes','sha256'}",'require(equal(o,expected)','requires_all_members_0444',"manifest(C,'MANIFEST.json',CURRENT_SHA,547,frozen=True)","frozen_files(w,authored+foreign,'FIRST_PARTY_MANIFEST.json')","manifest(HERE,'PREPARATION_MANIFEST.json',a.preparation_manifest_sha256,frozen=True)",'a.final_manifest_sha256,2,frozen=True)']:assert n in g,n
assert 'g.derive_inventory(before_inv,observation,now)' in i and 'accept=g.expected_acceptance(pins,pre)' in i and 'integration_finalization.json' in i
assert "inventory_guard(g.load(g.A/'integration_inventory_before.json'),inv,retained_remote,final['utc'])" in m and 'audit=True' in m and 'frozen=True' in m
assert 'g.derive_inventory(' in post and "inventory['program_completion_estimate_percent']" in post and 'frozen=True' in s
for body in source.values():assert '&0o777==' not in body and '& 0o777==' not in body

# Isolated finite specification fixtures, not extracted/executed candidate functions.
before=copy.deepcopy(falsifiers['inventory_baseline']);present={z['number'] for z in before['items']}
before['items'] += [{'number':n,'stage':'pending'} for n in range(1,181) if n not in present]
assert len(before['items'])==180
good=copy.deepcopy(before);good.update(completed_count=31,current_pr=42,updated_at_utc='2026-10-02T23:00:00+00:00',last_checkpoint_utc='2026-10-02T23:00:00+00:00',program_completion_estimate_percent=31/180*100,completion_estimate_percent=31/180*100)
chosen=next(z for z in good['items'] if z['number']==41);chosen.update(copy.deepcopy(next(z for z in falsifiers['authorized_after_fixture']['items'] if z['number']==41)));chosen['merged_at']='2026-10-02T22:59:00+00:00'
control('S1_complete_baseline',same(copy.deepcopy(good),good),True,'positive artificial180-item fixture')
for z in falsifiers['inventory_mutants']:
 altered=copy.deepcopy(good)
 if z['field'].startswith('items/41/'):next(q for q in altered['items'] if q['number']==41)['workflow_completion_estimate_percent']=z['value']
 else:altered[z['field']]=z['value']
 control('S1_reject_'+z['name'],same(altered,good),False,'original exact adversary mutant')
for name,change in [('missing_clock',lambda q:q.pop('updated_at_utc')),('wrong_UTC',lambda q:q.update(last_checkpoint_utc='not-a-clock')),('unknown_root_authority',lambda q:q.update(human_peer_review_asserted=True)),('changed_unselected',lambda q:q['items'][0].update(stage='pending')),('missing_workflow',lambda q:next(z for z in q['items'] if z['number']==41).pop('workflow_completion_estimate_percent')),('float_workflow',lambda q:next(z for z in q['items'] if z['number']==41).update(workflow_completion_estimate_percent=100.0))]:
 altered=copy.deepcopy(good);change(altered);control('S1_reject_'+name,same(altered,good),False,'complete type/key/value specification')
science=parse(read(P/'SCIENTIFIC_SCOPE.json'));expected={'schema':'pr41-accepted-qualified-conditional-partial/v1','utc':'2026-10-02T23:00:00+00:00','full_problem_solved':False,'partial_valid':True,'novelty_claimed':False,'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'scientific_scope':science}
control('S2_canonical_fixture',same(copy.deepcopy(expected),expected),True,'isolated schema fixture, not a runtime receipt')
for name,change in [('conflicting_peer_review',lambda q:q.update(human_peer_review_asserted=True)),('meaningful_solution',lambda q:q.update(solved=True)),('missing_null',lambda q:q.pop('current_model')),('numeric_false',lambda q:q.update(full_problem_solved=0)),('bool_budget',lambda q:q.update(original_substantive_attempts=True))]:
 altered=copy.deepcopy(expected);change(altered);control('S2_reject_'+name,same(altered,expected),False,'complete recognized schema')
audit_expected={**expected,'canonical_manifest_sha256':'a'*64,'canonical_manifest_entries':558};altered={**audit_expected,'human_peer_review_asserted':True}
control('S2_exact_audit_two_extensions',same(copy.deepcopy(audit_expected),audit_expected),True,'recognized audit-only fields')
control('S2_audit_reject_third_extension',same(altered,audit_expected),False,'unknown audit authority field')
ref={k:inputs['whole_observed_only'][k] for k in ['path','bytes','sha256']};root_fixture=parse(read(P/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json'));root_fixture.update(status='ROOT_APPROVED_CLOSED_WHOLE_EVIDENCE',created_utc='2026-10-02T23:00:00+00:00',root_full_current_read_completed=True,root_full_whole_read_completed=True,independent_whole_current_pass=True,whole_manifest=ref,root_whole_inspection=inputs['root_whole_observed'])
control('S2_ROOT_fixture_keyset',same(copy.deepcopy(root_fixture),root_fixture),True,'artificial fixture, not ROOT approval')
for name,change in [('ROOT_extra_claim',lambda q:q.update(human_peer_review_asserted=True)),('ROOT_missing_nulls',lambda q:q.pop('created_utc')),('whole_reference_extension',lambda q:q['whole_manifest'].update(full_problem_solved=True)),('root_reference_extension',lambda q:q['root_whole_inspection'].update(size=q['root_whole_inspection']['bytes'])),('reference_bool_bytes',lambda q:q['whole_manifest'].update(bytes=True))]:
 altered=copy.deepcopy(root_fixture);change(altered);control('S2_reject_'+name,same(altered,root_fixture),False,'exact ROOT/ref recognized schema')
mode_results=[]
for mode in [0o444,0o2444,0o4444,0o1444,0o644,0o400]:
 observed=stat.S_IMODE(mode)==0o444;control('S3_mode_'+oct(mode),observed,mode==0o444,'isolated integer permission predicate; no reviewed chmod')
 mode_results.append({'mode':oct(mode),'exact_0444':observed})
frozen_fixture={'PREPARATION_MANIFEST.json':0o444,'member.json':0o444,'FINAL_MANIFEST.json':0o444,'ROOT_REVIEWED_SCOPE.json':0o444,'ROOT_FINAL_RECONCILIATION.json':0o444}
for name in frozen_fixture:
 altered=copy.deepcopy(frozen_fixture);altered[name]=0o644
 control('S3_reject_permission_only_'+name,all(stat.S_IMODE(v)==0o444 for v in altered.values()),False,'manifest-self and final/preparation member coverage fixture')
now=dt.datetime.now(dt.timezone.utc).isoformat()
put('PRIVATE_FINITE_FIXTURES.json',{'status':'PASS_OWN_ISOLATED_SPECIFICATION_FIXTURES','utc':now,'actual_pid':os.getpid(),'checks':CHECKS,'checks_count':len(CHECKS),'artificial_before_inventory':before,'artificial_expected_inventory':good,'artificial_receipt_subset_fixture':expected,'artificial_ROOT_fixture':root_fixture,'mode_results':mode_results,'candidate_helpers_imported_compiled_or_executed':False,'fixtures_are_not_actual_future_inputs_or_approval':True,'future_runtime_PASS_claimed':False,'scientific_reexecution_claimed':False})
put('FINAL_STATIC_INSPECTION.json',{'status':'PASS_OWN_FULL_BYTE_READ_AND_STATIC_V2_SOURCE_INSPECTION','utc':now,'actual_pid':os.getpid(),'files':sorted(READ.values(),key=lambda z:z['path']),'unique_full_files':len(READ),'full_bytes':sum(z['bytes'] for z in READ.values()),'typed_nodes_seen':TYPED,'final_helper_sources':[READ[(P/n).relative_to(R).as_posix()] for n in helpers],'preserved_V1_members':35,'preserved_adversary_members':35,'individual_adversary_foreign_dependencies':foreign,'whole_current_members':547,'dependencies':469,'whole_authored':143,'whole_foreign':17,'repaired_mandatory_source_findings':['S1','S2','S3'],'private_specification_controls':len(CHECKS),'candidate_helpers_imported_compiled_or_executed':False,'native_canonical_Git_index_remote_shared_writes':False,'future_runtime_PASS_claimed':False,'scientific_reexecution_claimed':False,'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'source_preparation_completion_estimate_percent':100,'actual_acceptance_execution_estimate_percent':0,'unconditional_discovery_estimate_percent':0,'new_independent_review_and_ROOT_full_read':'STILL_REQUIRED'})
print(json.dumps({'status':'PASS_OWN_PRIVATE_READ_STATIC_AND_SPECIFICATION_CHECKS','pid':os.getpid(),'files_read':len(READ),'full_bytes_read':sum(z['bytes'] for z in READ.values()),'typed_nodes_seen':TYPED,'isolated_specification_controls':len(CHECKS),'candidate_helpers_imported_compiled_or_executed':False,'future_runtime_PASS_claimed':False,'current547_and_math_unchanged':True,'original2_new0_audit0':True},indent=2))
