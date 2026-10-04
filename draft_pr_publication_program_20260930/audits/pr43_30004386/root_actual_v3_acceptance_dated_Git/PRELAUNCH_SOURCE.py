"""ROOT independently closes actual repaired-source evidence and binds completed PR42."""
from pathlib import Path
import datetime as dt,hashlib,json,stat,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];S=A/'acceptance_preparation_family_v2';F=A/'acceptance_v2_source_adversary_family';V=A/'acceptance_preparation_family';sha=lambda b:hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def ref(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
def eq(a,b):
 if type(a)is not type(b):return False
 if type(a)is dict:return set(a)==set(b)and all(eq(a[k],b[k])for k in a)
 if type(a)is list:return len(a)==len(b)and all(eq(x,y)for x,y in zip(a,b))
 return a==b
def dump(name,obj):
 with(A/name).open('x')as f:json.dump(obj,f,indent=2);f.write('\n')
def closure(d,name,h,count):
 assert sha((d/name).read_bytes())==h;m=load(d/name);assert len(m['files'])==count
 assert {q.relative_to(d).as_posix()for q in d.rglob('*')if q.is_file()}=={z['path']for z in m['files']}|{name}
 if 'directories'in m:assert {q.relative_to(d).as_posix()for q in d.rglob('*')if q.is_dir()}==set(m['directories'])
 for q in d.rglob('*'):assert not q.is_symlink()and(q.is_dir()or(q.is_file()and stat.S_IMODE(q.stat().st_mode)==0o444))
 for z in m['files']:
  b=(d/z['path']).read_bytes();assert type(z['bytes'])is int and len(b)==z['bytes']and sha(b)==z['sha256']
 return m
def main():
 assert __debug__;D=A/'root_actual_v3_acceptance_dated_Git';D.mkdir();(D/'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
 closure(S,'PREPARATION_MANIFEST.json','11f39e9d890bc1a65efb4fe64bd8bd1612774c746c42c3cafa9883629fe58e91',45)
 fm=closure(F,'SELF_MANIFEST.json','412b6812b0089716e7acb14da8c9c00dd5c54b625929af9b3e2d89bc04b4e29a',118)
 old=closure(V,'PREPARATION_MANIFEST.json','4161032794d175f8e0cfc3b62b3d1567f172ca93abe590f43ef81576d6cd20f9',108)
 closure(A/'acceptance_source_adversary_family','SELF_MANIFEST.json','7c200634012ac198fbd643143e145a374837318a493d5d94e2e815faa3e096f2',119)
 queries=[];historical={};native4=['draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'];dated='c61dc0cb572de281b871264819c8b80d647d0373'
 for n in native4:
  for kind,argv in [('tree',['git','ls-tree','-z',dated,'--',n]),('body',['git','show',dated+':'+n])]:
   idx=len(queries);start=dt.datetime.now(dt.timezone.utc).isoformat();c=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);b,e=c.communicate();assert c.returncode==0 and not e
   (D/(str(idx)+'.stdout')).write_bytes(b);(D/(str(idx)+'.stderr')).write_bytes(e)
   queries.append({'argv':argv,'cwd':str(R),'pid':c.pid,'started_utc':start,'finished_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_execution':True,'completed':True,'exit_code':0,'stdout':ref(D/(str(idx)+'.stdout')),'stderr':ref(D/(str(idx)+'.stderr'))})
   if kind=='tree':assert b.decode().startswith('100644 blob ')and b.decode().split('\t')[1]==n+'\0'
   else:historical[n]=b
 (D/'QUERIES.json').write_text(json.dumps(queries,indent=2)+'\n')
 assert len(fm['external_individually_excluded_inputs'])==1067
 for z in fm['external_individually_excluded_inputs']:
  p=Path(z['path']);assert p.is_absolute()and p.is_relative_to(R)and not p.is_symlink()and all(not q.is_symlink()for q in p.parents)
  rel=p.relative_to(R).as_posix();b=historical[rel]if rel in historical else p.read_bytes();assert len(b)==z['bytes']and sha(b)==z['sha256']
 deltas={'integrate_reviewed_partial.py':(b'snapshot_manifest_v2.json',b'snapshot_manifest.json'),'state_mirror_reconciliation.py':(b'PR43; source-status correction;',b'PR43 source-status correction;')}
 for n in ['pr43_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']:
  b=(V/n).read_bytes()
  if n in deltas:x,y=deltas[n];assert b.count(x)==1;b=b.replace(x,y,1)
  assert (S/n).read_bytes()==b
 for n in ['SCIENTIFIC_SCOPE.json','DRAFT_FINAL_PLAN.json','DRAFT_ROOT_IMMUTABLE_BINDINGS.json','EXPECTED_CURRENT_ADMIN.json','EXPECTED_WHOLE_VERDICT.json','EXPECTED_ROOT_WHOLE_REVIEW.json']:assert (S/n).read_bytes()==(V/n).read_bytes()
 assert sha((A/'capture_root_final_operation_v2.py').read_bytes())=='9376c9c2d972f3ae4950ddb6b46300c2cd1cc36db89bc6ced6627fe8801e71a4'
 verdict=load(F/'VERDICT.json');assert verdict['verdict']=='PASS_EXACT_CLOSED_REPAIRED_V2_SOURCE_ONLY'and verdict['mandatory_defects']==[]
 # Every genuine source reader/control/closure capture is independently rechecked.
 actual=[]
 for q in sorted(F.rglob('CAPTURE.json')):
  c=load(q);d=q.parent
  if c.get('actual_execution')is not True:continue
  if c.get('schema')=='PR43_V2_SOURCE_ADVERSARY_ACTUAL_OWN_CAPTURE_v1':
   assert c['completed_after_child_exit']is True and type(c['actual_child_pid'])is int and c['actual_child_pid']>0 and c['exit_code']==0 and c['source_unchanged']is True
  else:assert c['completed']is True and type(c['pid'])is int and c['pid']>0 and c['exit_code']==0
  for k in ['stdout','stderr']:
   b=(d/c[k]['path']).read_bytes();assert len(b)==c[k]['bytes']and sha(b)==c[k]['sha256']
  if (d/'PRELAUNCH_SOURCE.py').exists():assert sha((d/'PRELAUNCH_SOURCE.py').read_bytes())==c['prelaunch_source_sha256'];assert sha((d/'PRELAUNCH_OPERATOR.py').read_bytes())==c['prelaunch_operator_sha256']
  assert dt.datetime.fromisoformat(c['started_utc'])<=dt.datetime.fromisoformat(c['finished_utc']);actual.append(ref(q))
 p42=A.parent/'pr42_2233';post=load(p42/'post_acceptance_verification.json');rootpost=load(p42/'ROOT_ACTUAL_POST_INSPECTION.json');assert rootpost['status']=='PASS'and eq(rootpost['entire_post'],post)and post['primary_acceptances']==32 and post['targets']==33 and post['consumed_substantive_turns']==41
 now=dt.datetime.now(dt.timezone.utc).isoformat();assert dt.datetime.fromisoformat(now)>dt.datetime.fromisoformat(rootpost['utc'])
 bindings=load(S/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json');bindings.update(status='ROOT_APPROVED_CLOSED_WHOLE_AND_ACTUAL_PR42_EVIDENCE',created_utc=now,root_full_current_read_completed=True,root_full_whole_read_completed=True,root_acceptance_source_review_completed=True,independent_whole_current_pass=True,root_actual_PR42_predecessor_read_completed=True)
 for key,p in [('whole_manifest',A/'whole_current_source_first_family/SELF_MANIFEST.json'),('root_whole_inspection',A/'ROOT_WHOLE_CURRENT_REVIEW.json'),('root_capture_operator',A/'capture_root_final_operation_v2.py'),('previous_mirror',p42/'state_mirror_bindings.json'),('previous_post',p42/'post_acceptance_verification.json'),('previous_root_post',p42/'ROOT_ACTUAL_POST_INSPECTION.json')]:bindings[key]=ref(p)
 dump('ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS_V2.json',bindings)
 inputs=load(S/'INPUT_BINDINGS.json');refs=[inputs['pins'][n]for n in sorted(inputs['pins'])]
 for z in refs:b=(R/z['path']).read_bytes();assert len(b)==z['bytes']and sha(b)==z['sha256']
 refs += [ref(A/'reviewed_candidate/MANIFEST.json'),ref(A/'reviewed_candidate/CURRENT_DEPENDENCIES.json'),bindings['whole_manifest'],inputs['closed_whole_result'],inputs['closed_whole_report'],bindings['root_whole_inspection'],ref(A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS_V2.json')]+[bindings[n]for n in ['previous_mirror','previous_post','previous_root_post']]
 assert len({z['path']for z in refs})==len(refs)
 plan=load(S/'DRAFT_FINAL_PLAN.json');plan.update(plan_status='ROOT_REVIEWED_FOR_ACTUAL_RECONCILIATION',partial_valid=True,preparation_manifest_sha256=sha((S/'PREPARATION_MANIFEST.json').read_bytes()),root_bindings=ref(A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS_V2.json')['path'],root_bindings_sha256=sha((A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS_V2.json').read_bytes()),whole_manifest_sha256=bindings['whole_manifest']['sha256'],root_full_current_read_completed=True,root_full_whole_read_completed=True,root_acceptance_source_review_completed=True,independent_whole_current_pass=True,root_actual_PR42_predecessor_read_completed=True,immutable_evidence_references=sorted(refs,key=lambda z:z['path']))
 dump('ROOT_FINAL_PLAN_V2.json',plan)
 fresh=load(p42/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES_V4.json');fresh.update(schema='pr43-root-fresh-acceptance-input-preimages/v1',created_utc=now,reason_date_utc=now[:10],reason='Actual current main and all thirteen complete native bodies after verified PR42 acceptance and published owned checkpoint govern PR43 integration; the immutable c61 source epoch remains historical evidence only.',current_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip())
 for z in fresh['files']:
  p=R/z['path'];b=p.read_bytes();z.update(bytes=len(b),sha256=sha(b),worktree_mode=stat.S_IMODE(p.stat().st_mode))
 dump('ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES_V2.json',fresh)
 inspection={'schema':'pr43-root-complete-repaired-acceptance-source-inspection/v1','status':'PASS','utc':now,'source_preparation':ref(S/'PREPARATION_MANIFEST.json'),'new_source_adversary':ref(F/'SELF_MANIFEST.json'),'entire_new_verdict':verdict,'foreign_individual_full_bodies_verified':1067,'historical4_full_actual_Git_queries':ref(D/'QUERIES.json'),'all_actual_own_source_captures':actual,'full_delta_exact_two_tokens':True,'old_failed_V1_preserved':True,'personal_complete_reports_verdict_contract_operator_and_source_controls_read':True,'actual_PR42_root_post':ref(p42/'ROOT_ACTUAL_POST_INSPECTION.json'),'future_PR43_execution_success_certified':False,'new_substantive_attempts':0,'audit_turns':0}
 dump('ROOT_ACCEPTANCE_V2_SOURCE_INSPECTION.json',inspection)
 print(json.dumps({'status':'PASS_REAL_ROOT_BINDINGS_PLAN_AND_CURRENT13','references':len(refs),'plan':ref(A/'ROOT_FINAL_PLAN_V2.json'),'root_bindings':ref(A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS_V2.json')}))
if __name__=='__main__':main()
