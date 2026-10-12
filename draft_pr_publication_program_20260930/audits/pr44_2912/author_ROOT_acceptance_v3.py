"""ROOT: independently inspect closed source and complete only reviewed approval fields."""
from pathlib import Path, PurePosixPath
import datetime as dt, hashlib, json, os, stat, subprocess, sys
A=Path(__file__).resolve().parent; R=A.parents[2]
S=A/'acceptance_preparation_family'; F=A/'acceptance_source_adversary_family'
HIST={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
sha=lambda b:hashlib.sha256(b).hexdigest()
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def parse(b):
 def pairs(xs):
  o={}
  for k,v in xs:assert k not in o; o[k]=v
  return o
 return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def load(p):return parse(p.read_bytes())
def eq(a,b):
 if type(a)is not type(b):return False
 if type(a)is dict:return a.keys()==b.keys()and all(eq(a[k],b[k])for k in a)
 if type(a)is list:return len(a)==len(b)and all(eq(x,y)for x,y in zip(a,b))
 return a==b
def safe(base,n):
 assert type(n)is str and n and '\\'not in n and '\0'not in n
 q=PurePosixPath(n);assert not q.is_absolute()and q.as_posix()==n and not set(q.parts)&{'.','..','.git','__pycache__'}
 p=base/n;assert p.is_file()and not p.is_symlink()and p.resolve().is_relative_to(base.resolve())
 assert all(not t.is_symlink()for t in p.parents)
 return p
def ref(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
def check(base,z,override=None):
 assert type(z['bytes'])is int and z['bytes']>=0
 b=override if override is not None else safe(base,z['path']).read_bytes()
 assert len(b)==z['bytes']and sha(b)==z['sha256'];return b
def dump(n,o):
 with(A/n).open('x')as f:json.dump(o,f,indent=2,ensure_ascii=False);f.write('\n')
def closure(base,name,pinned):
 assert sha(safe(base,name).read_bytes())==pinned
 m=load(base/name); rows=m['files'];assert m['self_excluded']==[name]and type(m['files_count'])is int and m['files_count']==len(rows)
 names={z['path']for z in rows};assert len(names)==len(rows)and name not in names
 actual=set();dirs=set()
 for p in base.rglob('*'):
  assert not p.is_symlink()and(p.is_dir()or p.is_file())
  n=p.relative_to(base).as_posix()
  if p.is_file():actual.add(n);assert stat.S_IMODE(p.stat().st_mode)==0o444
  else:dirs.add(n)
 assert actual==names|{name}
 expected={p.as_posix()for n in actual for p in PurePosixPath(n).parents if p.as_posix()!='.'}
 assert dirs==expected
 for z in rows:check(base,z)
 return m
def capture(p):
 c=load(p);d=p.parent
 assert c['actual_execution']is True and c['completed']is True and type(c['pid'])is int and c['pid']>0 and type(c['exit_code'])is int
 assert dt.datetime.fromisoformat(c['started_utc'] if 'started_utc'in c else c['utc'])<=dt.datetime.fromisoformat(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc)
 for k in ['stdout','stderr']:
  z=c[k];base=R if z['path'].startswith('draft_pr_publication_program_20260930/') else F if z['path'].startswith('ACTUAL_GIT/') else d
  check(base,z)
 if 'prelaunch'in c:
  pre=c['prelaunch'];assert eq(load(d/'PRELAUNCH.json'),pre)
  for n,k in [('PRELAUNCH_SOURCE.py','source_sha256'),('PRELAUNCH_OPERATOR.py','operator_sha256')]:assert sha(safe(d,n).read_bytes())==pre[k]
  assert c['source_unchanged']is True and c['operator_unchanged']is True
 return ref(p)
def main():
 assert __debug__;expected=sys.argv[1];before={z['path']:ref(R/z['path'])for z in load(A/'ROOT_CURRENT_INPUT_PREIMAGES.json')['files']}
 prep=closure(S,'PREPARATION_MANIFEST.json','413ae6bab4142da7b611d910f801cf8ab92d7d085fad4ceed7203074538442de');assert len(prep['files'])==99
 fm=closure(F,'SELF_MANIFEST.json',expected)
 verdict=load(F/'VERDICT.json')
 assert verdict['schema']=='pr44-acceptance-source-adversary-verdict/v1'and verdict['verdict']=='PASS_SOURCE_ONLY_SCOPED'and verdict['mandatory_corrections']==[]
 assert verdict['preparation_manifest_sha256']=='413ae6bab4142da7b611d910f801cf8ab92d7d085fad4ceed7203074538442de'and verdict['production_imported_compiled_executed']is False and verdict['future_acceptance_approved']is False
 gitdir=A/'root_acceptance_source_native4_Git_v3';gitdir.mkdir();(gitdir/'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes());queries=[];bodies={}
 epoch=load(A/'ROOT_CURRENT_INPUT_PREIMAGES.json');head=epoch['current_head'];assert head=='2b9d0234b1396fa84c4b34055b5e8e14c873588b'
 frozen={z['path']:z for z in epoch['files']}
 for n in sorted(HIST):
  for kind,argv in [('tree',['git','ls-tree','-z',head,'--',n]),('body',['git','show',head+':'+n])]:
   d=gitdir/str(len(queries));d.mkdir();start=now();p=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'));out,err=p.communicate()
   c={'schema':'pr44-root-source-inspection-actual-Git/v1','operator_pid':os.getpid(),'pid':p.pid,'argv':argv,'cwd':str(R),'started_utc':start,'finished_utc':now(),'actual_execution':True,'completed':True,'exit_code':p.returncode,'stdin_supplied':False}
   for k,b in [('stdout',out),('stderr',err)]:(d/(k+'.bin')).write_bytes(b);c[k]=ref(d/(k+'.bin'))
   (d/'CAPTURE.json').write_text(json.dumps(c,indent=2)+'\n');queries.append(c);assert p.returncode==0 and err==b''
   if kind=='tree':
    chunks=out.decode().split('\0');assert len(chunks)==2 and chunks[-1]=='';fields,literal=chunks[0].split('\t');mode,t,blob=fields.split();assert mode=='100644'and t=='blob'and literal==n
   else:bodies[n]=out;assert len(out)==frozen[n]['bytes']and sha(out)==frozen[n]['sha256']
 inputs=load(F/'INDIVIDUAL_INPUTS.json');assert len(inputs['files'])==inputs['files_count']==1267 and len({z['path']for z in inputs['files']})==1267
 for z in inputs['files']:check(R,z)
 prepared=load(S/'INPUT_BINDINGS.json')
 for z in list(prepared['pins'].values())+[prepared[n]for n in ['closed_whole_manifest','closed_whole_report','closed_whole_result','closed_root_whole_inspection','previous_mirror','previous_post','previous_root_post']]:check(R,z)
 controls=load(S/'OWN_CONTROL_RESULTS.json');assert controls['status']=='PASS_PRIVATE_CONTROLS_ONLY'and controls['checks']==6061 and len(controls['rejected_hostile_cases'])==18 and controls['production_imported_compiled_executed']is False
 actual=[capture(p)for base in [S,F]for p in sorted(base.rglob('CAPTURE.json'))]
 rootpost=load(R/prepared['previous_root_post']['path']);post=load(R/prepared['previous_post']['path']);assert eq(rootpost['entire_post'],post)and post['primary_acceptances']==33 and post['targets']==34 and post['consumed_substantive_turns']==41
 operator=A/'capture_root_final_operation.py';assert not operator.exists();operator.write_bytes((S/'capture_root_final_operation.py').read_bytes());assert sha(operator.read_bytes())=='f4a1ae7322a048ee3bce39654928b07b72cbdae6d3d593bad1830664a4167ee1'
 utc=now();inspection={'schema':'pr44-root-complete-acceptance-source-inspection/v1','status':'PASS_ROOT_COMPLETE_ACCEPTANCE_SOURCE_INSPECTION','utc':utc,'all_prepared_source_and_controls_fully_read':True,'exact_preparation_closure_and_full_modes_checked':True,'all_individual_source_adversary_inputs_checked':True,'all_complete_actual_captures_checked':True,'complete_VERDICT_object':verdict,'preparation_manifest_sha256':sha((S/'PREPARATION_MANIFEST.json').read_bytes()),'acceptance_source_manifest':ref(F/'SELF_MANIFEST.json'),'acceptance_source_verdict':ref(F/'VERDICT.json'),'mandatory_corrections':[],'future_execution_approved':False,'all1267_individual_bodies_verified':True,'individual_source_adversary_native13_are_actual_present_inputs':True,'frozen_native4_checked_separately_without_overriding_present_input_refs':True,'first_ROOT_failed_epoch_substitution_preserved':ref(A/'root_complete_acceptance_source_inspection_actual_capture/CAPTURE.json'),'second_ROOT_failed_capture_schema_assumption_preserved':ref(A/'root_complete_acceptance_source_inspection_v2_actual_capture/CAPTURE.json'),'actual_dated_native4_queries':queries,'all_complete_source_captures':actual,'preparation_files':99,'adversary_files':len(fm['files']),'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False}
 dump('ROOT_SOURCE_ACCEPTANCE_REVIEW.json',inspection)
 bindings=load(S/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json');bindings.update(status='ROOT_APPROVED_CLOSED_WHOLE_SOURCE_AND_ACTUAL_PR43_EVIDENCE',created_utc=now(),root_full_current_read_completed=True,root_full_whole_read_completed=True,root_acceptance_source_review_completed=True,independent_whole_current_pass=True,root_actual_PR43_predecessor_read_completed=True)
 paths={'whole_manifest':A/'whole_current_source_first_family/SELF_MANIFEST.json','root_whole_inspection':A/'ROOT_WHOLE_CURRENT_REVIEW.json','root_capture_operator':operator,'acceptance_source_manifest':F/'SELF_MANIFEST.json','acceptance_source_verdict':F/'VERDICT.json','root_source_inspection':A/'ROOT_SOURCE_ACCEPTANCE_REVIEW.json'}
 for k in ['previous_mirror','previous_post','previous_root_post']:paths[k]=R/prepared[k]['path']
 for k,p in paths.items():bindings[k]=ref(p)
 dump('ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json',bindings)
 refs=list(prepared['pins'].values())+[ref(A/'reviewed_candidate/MANIFEST.json'),ref(A/'reviewed_candidate/CURRENT_DEPENDENCIES.json'),bindings['whole_manifest'],prepared['closed_whole_result'],prepared['closed_whole_report'],bindings['root_whole_inspection'],ref(A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json')]+[bindings[k]for k in ['previous_mirror','previous_post','previous_root_post','acceptance_source_manifest','acceptance_source_verdict','root_source_inspection','root_capture_operator']]
 dedup={}
 for z in refs:assert z['path']not in dedup or eq(z,dedup[z['path']]);dedup[z['path']]=z
 plan=load(S/'DRAFT_FINAL_PLAN.json');plan.update(plan_status='ROOT_REVIEWED_FOR_ACTUAL_RECONCILIATION',partial_valid=True,preparation_manifest_sha256=sha((S/'PREPARATION_MANIFEST.json').read_bytes()),whole_manifest_sha256=bindings['whole_manifest']['sha256'],root_bindings=ref(A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json')['path'],root_bindings_sha256=sha((A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json').read_bytes()),root_full_current_read_completed=True,root_full_whole_read_completed=True,root_acceptance_source_review_completed=True,root_actual_PR43_predecessor_read_completed=True,independent_whole_current_pass=True,immutable_evidence_references=sorted(dedup.values(),key=lambda z:z['path']))
 dump('ROOT_FINAL_PLAN.json',plan)
 fresh={'schema':'pr44-root-fresh-acceptance-input-preimages/v1','approved_by_root':True,'created_utc':now(),'reason_date_utc':now()[:10],'reason':'Fresh actual main and all13 bodies after independently verified PR43 acceptance and publication of PR44 whole/source audits govern present integration; original2b9 source epoch remains historical.','current_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),'files':[]}
 for z in epoch['files']:
  p=R/z['path'];fresh['files'].append({**ref(p),'worktree_mode':stat.S_IMODE(p.stat().st_mode)})
 assert all(eq(before[n],ref(R/n))for n in before);dump('ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json',fresh)
 print(json.dumps({'status':'PASS_ROOT_COMPLETE_SOURCE_AND_ACTUAL_PR43_BINDINGS','pid':os.getpid(),'preparation':99,'adversary':len(fm['files']),'individual_inputs':1267,'actual_captures':len(actual),'reference_count':len(dedup),'future_execution_certified':False}))
if __name__=='__main__':main()
