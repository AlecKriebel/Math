"""Additional handwritten SOURCE countermodels; all fixtures are private, never ROOT authority."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone, timedelta
import copy, hashlib, json, os, stat, sys
from capture_private import capture
assert __debug__ and sys.flags.optimize==0
F=Path(__file__).absolute().parent;A=F.parent;R=A.parents[2];P=A/'acceptance_preparation_family';START=datetime.now(timezone.utc).isoformat();checks=0;negative=[]
def need(ok,msg):
 global checks
 checks+=1
 if not ok:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def equal(a,b):
 if type(a)!=type(b):return False
 if isinstance(a,dict):return set(a)==set(b) and all(equal(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
 return a==b
def reject(label,fn):
 try:fn()
 except (ValueError,KeyError,TypeError):negative.append(label);return
 raise ValueError('accepted '+label)
def clock(v):
 if type(v)!=str:raise ValueError('clock type')
 t=datetime.fromisoformat(v)
 if t.tzinfo is None or t.utcoffset()!=timedelta(0) or t>datetime.now(timezone.utc):raise ValueError('aware actual UTC')
 return t

def main():
 inputs=load(P/'INPUT_BINDINGS.json');native={z['path']:z for z in inputs['dated_native13']};need(len(native)==13,'exact13')
 old4={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
 external=load(F/'EXTERNAL_INPUT_BINDINGS.json');rows={z['path']:z for z in external['files']};need(not set(rows)&old4,'dated mutable4 excluded from immutable live closure deps')
 for n in set(native)-old4:need(equal(native[n],rows[n]),'stable9 complete hash/fullmode already genuinely read')
 git_records=[];historical=[];epoch='e491808c3544ff44e8526d9b24857b5c9ca64208'
 for i,n in enumerate(sorted(old4)):
  body=capture('historical_native4_body_'+str(i),['git','show',epoch+':'+n],R);mode=capture('historical_native4_tree_'+str(i),['git','ls-tree','-z',epoch,'--',n],R);git_records.extend([body,mode])
  b=Path(body['stdout']['path']).read_bytes();entry=Path(mode['stdout']['path']).read_bytes().decode();need(len(b)==native[n]['bytes'] and sha(b)==native[n]['sha256'],'full historical native body')
  parts=entry.rstrip('\0').split('\t');need(len(parts)==2 and parts[1]==n and parts[0].split()[:2]==['100644','blob'] and entry.endswith('\0') and entry.count('\0')==1,'exact Git historical blob100644')
  historical.append({'path':n,'historical_commit':epoch,'bytes':len(b),'sha256':sha(b),'git_entry':entry,'body_child_pid':body['child_pid'],'mode_child_pid':mode['child_pid']})
 diff=capture('original_diff',['git','diff','--no-ext-diff','--no-textconv','--binary','c6975ca76f9f667f1250ba403d0e6da2aafe14d0','487327b2412c436ae69e8c52bf353a9a1fb7594e','--'],R);git_records.append(diff)
 b=Path(diff['stdout']['path']).read_bytes();need(b==(A/'original_diff.patch').read_bytes() and len(b)==59460 and sha(b)=='17a6b488f85b54d22af865a5e0c9644b016211c3c985bd352631b46632dedc27','full original17path59460binarydiff')
 paths=capture('original_diff_paths',['git','diff','--no-ext-diff','--no-textconv','--name-only','-z','c6975ca76f9f667f1250ba403d0e6da2aafe14d0','487327b2412c436ae69e8c52bf353a9a1fb7594e','--'],R);git_records.append(paths)
 names=Path(paths['stdout']['path']).read_bytes().decode().split('\0');need(names[-1]=='' and len(names[:-1])==17 and len(set(names[:-1]))==17,'actual17 unique changed paths')
 # Immutable plan oracle written from full actual draft, not selected fields.
 draft=load(P/'DRAFT_FINAL_PLAN.json')
 def immutable_plan(candidate):
  if not equal(candidate,draft):raise ValueError('full typed pending plan changed')
 immutable_plan(copy.deepcopy(draft))
 for key,val in [('pr',45),('original_substantive_attempts',True),('audit_turns',1),('current_model','historical-model'),('full_problem_solved',True),('prior_publication_doi','10.5281/zenodo.fake'),('root_actual_PR46_predecessor_read_completed',True),('immutable_evidence_references',[{}])]:
  z=copy.deepcopy(draft);z[key]=val;reject('plan/'+key,lambda z=z:immutable_plan(z))
 z=copy.deepcopy(draft);z['scientific_scope']['realized_example_instanton_rank_computed']=True;reject('plan/nestedIsharp',lambda:immutable_plan(z))
 z=copy.deepcopy(draft);z['unrequested_extension']=True;reject('plan/unknownfield',lambda:immutable_plan(z))
 # Future completed ROOT22 contract is tested as a private memory-only typed oracle.
 contract=load(P/'ROOT_POST_CONTRACT.json');keys=set(contract['future47_required_ROOT_complete_keyset']);values=contract['future47_required_completed_values'];postvalues=contract['future47_required_entire_post_values']
 fixture={k:None for k in keys};fixture.update(copy.deepcopy(values));fixture.update(schema=contract['future47_required_ROOT_schema'],utc=START,entire_post=copy.deepcopy(postvalues),all_six_real_phase_captures=['PRIVATE MODEL '+str(i) for i in range(6)],current13=['PRIVATE MODEL '+str(i) for i in range(13)],final_sealer_actual_capture='PRIVATE MODEL ONLY')
 def whole_contract(z):
  if type(z)!=dict or set(z)!=keys:raise ValueError('full22 keyset')
  if z['schema']!=contract['future47_required_ROOT_schema']:raise ValueError('schema')
  for k,v in values.items():
   if not equal(z[k],v):raise ValueError('entire typed ROOT value')
  if not equal(z['entire_post'],postvalues):raise ValueError('whole post no abbreviation')
  if type(z['all_six_real_phase_captures'])!=list or len(z['all_six_real_phase_captures'])!=6 or len(set(z['all_six_real_phase_captures']))!=6:raise ValueError('six phases no Boolean')
  if type(z['current13'])!=list or len(z['current13'])!=13:raise ValueError('native13 no Boolean')
  clock(z['utc'])
 whole_contract(fixture)
 for k in keys:
  z=copy.deepcopy(fixture);del z[k];reject('ROOT22/missing/'+k,lambda z=z:whole_contract(z))
 for k,v in values.items():
  z=copy.deepcopy(fixture);z[k]=int(v) if type(v)==bool else True if type(v)==int else 0 if type(v)==float else False;reject('ROOT22/type/'+k,lambda z=z:whole_contract(z))
 for k in postvalues:
  z=copy.deepcopy(fixture);del z['entire_post'][k];reject('ROOT22/postmissing/'+k,lambda z=z:whole_contract(z))
 for k,v in [('all_six_real_phase_captures',True),('current13',True),('utc','2099-01-01T00:00:00+00:00')]:
  z=copy.deepcopy(fixture);z[k]=v;reject('ROOT22/substitute/'+k,lambda z=z:whole_contract(z))
 # Preserve179 full inventory objects and every nondeclared top-level value.
 inv={'items':[{'number':i,'stage':'complete' if i<=36 else 'pending','details':{'x':i,'untouched':None}} for i in range(1,181)],'excluded_prs':[8],'preserved':{'typed':True},'current_pr':47,'completed_count':36}
 after=copy.deepcopy(inv);selected=next(x for x in after['items'] if x['number']==47);selected.update(stage='complete',outcome='unsolved_accepted_partial',original_attempts='1/5',new_substantive_attempts=0);after.update(current_pr=48,completed_count=37,program_completion_estimate_percent=37*100/180)
 need(len(after['items'])==180 and sum(x['stage']=='complete' for x in after['items'])==37,'private180 inventory model37')
 need(all(equal(before,end) for before,end in zip(inv['items'],after['items']) if before['number']!=47) and equal(after['excluded_prs'],inv['excluded_prs']) and equal(after['preserved'],inv['preserved']),'private179 full items/toptyped preserved')
 need(after['program_completion_estimate_percent']==20.555555555555557 and after['program_completion_estimate_percent']!=37/180*100,'exact declared floating computation')
 # Actual own child/result/outer capture triple uses containment, not equality.
 observed=load(F/'PRIVATE_CONTROL_RESULT.json');outer=load(F/'captures/source_controls_v1/CAPTURE.json');pre=load(F/'captures/source_controls_v1/PRELAUNCH.json')
 def actual_triple(child,cap,launch):
  if type(child['actual_pid'])!=int or child['actual_pid']!=cap['child_pid']:raise ValueError('actual child identity')
  if not(clock(launch['created_utc'])<=clock(cap['started_utc'])<=clock(child['started_utc'])<=clock(child['finished_utc'])<=clock(cap['finished_utc'])):raise ValueError('actual child/operator containment')
 actual_triple(observed,outer,pre)
 for field,val in [('actual_pid',True),('started_utc',pre['created_utc']),('finished_utc',datetime.now(timezone.utc).isoformat())]:
  z=copy.deepcopy(observed);z[field]=val;reject('actualtriple/'+field,lambda z=z:actual_triple(z,outer,pre))
 observation=[]
 for n in sorted(old4):
  p=R/n;b=p.read_bytes();observation.append({'path':n,'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode),'observation_utc':datetime.now(timezone.utc).isoformat(),'future_live_authority':False})
 result={'schema':'pr47-source-adversary-supplemental-models/v1','status':'PASS_SOURCE_ONLY_PRIVATE_MODELS','actual_pid':os.getpid(),'started_utc':START,'finished_utc':datetime.now(timezone.utc).isoformat(),'assertions':checks,'malformed_private_models_rejected':len(negative),'negative_labels':negative,'read_only_actual_Git_children':len(git_records),'historical_native4':historical,'actual_original_diff_paths':names[:-1],'dated_live_native4_observation_only':observation,'production_imported_compiled_executed':False,'future_acceptance_approved':False,'private_ROOT22_fixture_is_actual_approval':False,'PR46_actual_predecessor_completed':False,'new_substantive_attempts':0,'audit_turns':0}
 (F/'SUPPLEMENTAL_MODEL_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['negative_labels','historical_native4','actual_original_diff_paths','dated_live_native4_observation_only']},sort_keys=True))
if __name__=='__main__':main()
