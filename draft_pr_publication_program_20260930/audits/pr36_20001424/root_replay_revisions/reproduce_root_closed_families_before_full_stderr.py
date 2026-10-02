#!/usr/bin/env python3
"""Actually replay the five closed PR36 audit families in an isolated replica.

This never rewrites a closed family or the live queue. One hard-coded ROOT in
the source/provenance helper is redirected, with its exact patch retained.
Only timestamps, explicitly recorded workspace HEAD, and private filesystem
prefixes may vary in comparisons. Derived stderr hashes are checked against
the complete actual sidecar before path-normalized stderr comparison.
"""
from pathlib import Path, PurePosixPath
import copy, datetime, difflib, hashlib, importlib.util, json, shutil, subprocess, sys
sys.dont_write_bytecode = True
A = Path(__file__).resolve().parent
R = A.parents[2]
Q = R/'unsolved_math_prioritization'
PREFIX = A.relative_to(R)
FAMILIES = {
 'graph_family':('authored_manifest.json','3b14dc707a10811165c418fb0faacedfbf7082598cb1e5eb663a24e506d5a1cd',190),
 'algebraic_family':('authored_manifest.json','df1065f83fa64f9ee685638b9b115baefe3e9d9fa7c06a2cb1f02b1f63f58176',50),
 'primary_scope_family':('AUTHORED_MANIFEST.json','75cd9b1704194a2adbd451cf0af4c8f24c9bf0fbf9cb6f9139be3369a90a6fb2',27),
 'arithmetic_graph_priority_family':('AUTHORED_MANIFEST.json','f66e249bc5a60d619fedf3390b826f4e19640b5da5a7c1d4385f0180805c88bb',18),
 'antipodal_priority_family':('AUTHORED_MANIFEST.json','4a7bb26fe5d32af8df445264a4f54e0bb65c6f13a5c176c6c88b577b6e063d75',79),
}
sha = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(p.read_text())
utc = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(p,obj):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')
def rows(m):
 fs=m['files']
 return [dict(v,path=k) for k,v in fs.items()] if isinstance(fs,dict) else fs
def closure():
 out=[]; parses=0
 for family,(name,pin,count) in FAMILIES.items():
  base=A/family;data=(base/name).read_bytes();assert sha(data)==pin,family
  members=rows(json.loads(data));assert len(members)==count
  seen=set()
  for row in members:
   rel=row['path'];p=PurePosixPath(rel)
   assert not p.is_absolute() and '..' not in p.parts and rel==p.as_posix() and rel not in seen and rel!=name
   seen.add(rel);f=base/rel;assert f.is_file() and not f.is_symlink()
   b=f.read_bytes();assert sha(b)==row['sha256'] and len(b)==row.get('size',row.get('bytes')),(family,rel)
   if f.suffix=='.json':json.loads(b);parses+=1
   elif f.suffix=='.jsonl':
    for line in b.splitlines():
     if line.strip():json.loads(line);parses+=1
  out.append({'family':family,'manifest':name,'manifest_sha256':pin,'authored_members':count})
 assert sum(x['authored_members'] for x in out)==364
 return out,parses
def main():
 before,parse_count=closure()
 stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
 private=A/'tmp'/('root_closed_family_replay_'+stamp)/'repository'
 private.mkdir(parents=True,exist_ok=False);pa=private/PREFIX;pa.mkdir(parents=True)
 for f,(m,_,_) in FAMILIES.items():
  for row in rows(load(A/f/m))+[{'path':m}]:
   dst=pa/f/row['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(A/f/row['path'],dst)
 for d in ['source_snapshot','pr_input']:
  shutil.copytree(A/d,pa/d)
 shutil.copyfile(A/'snapshot_manifest.json',pa/'snapshot_manifest.json')
 (private/'.git').symlink_to(R/'.git',target_is_directory=True)
 pq=private/'unsolved_math_prioritization';pq.mkdir()
 for f in ['manifest.json','policy.json','catalog.json','assessments.json','state.json','QUEUE.md','queue.py']:
  shutil.copyfile(Q/f,pq/f)
 shutil.copytree(Q/'review_v2',pq/'review_v2')
 (pq/'cache').symlink_to(Q/'cache',target_is_directory=True)
 foreign=[]
 for f in ['hlushchanka.pdf','hlushchanka.txt']:
  src=A/'graph_family/private_sources'/f;dst=pa/'graph_family/private_sources'/f
  dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
  foreign.append({'path':str(src.relative_to(A)),'sha256':sha(src.read_bytes()),'foreign_input_only':True})
 live={str(p.relative_to(R)):sha(p.read_bytes()) for p in [Q/'QUEUE.md',Q/'state.json',Q/'history.jsonl']}
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
 runs=[];comparisons=[];qualifications=[]
 def run(label,argv,expected=0):
  cp=subprocess.run([sys.executable,*map(str,argv)],cwd=private,capture_output=True,timeout=180)
  sd=private.parent/'actual_streams';sd.mkdir(exist_ok=True)
  (sd/(label+'.stdout')).write_bytes(cp.stdout);(sd/(label+'.stderr')).write_bytes(cp.stderr)
  rec={'label':label,'command':[sys.executable,*map(str,argv)],'exit':cp.returncode,'expected_exit':expected,'stdout_sha256':sha(cp.stdout),'stderr_sha256':sha(cp.stderr)}
  runs.append(rec);save(private.parent/'ACTUAL_RUNS.json',runs)
  assert cp.returncode==expected,(label,cp.returncode,cp.stderr.decode()[-3000:])
  return cp
 def normalize(o):
  if isinstance(o,dict):
   return {k:normalize(v) for k,v in o.items() if k not in ('utc','at_utc')}
  if isinstance(o,list):return [normalize(v) for v in o]
  if isinstance(o,str):return o.replace(str(private),'<REPOSITORY>').replace(str(R),'<REPOSITORY>')
  return o
 def compare(f,name,derived_stderr=False,workspace_head=False):
  old=load(A/f/name);new=load(pa/f/name)
  if derived_stderr:
   for obj,base in [(old,A/f),(new,pa/f)]:
    for row in obj['runs']:
     assert row['stderr_sha256']==sha((base/'results'/(row['name']+'.stderr')).read_bytes())
     assert row['stdout_sha256']==sha((base/'results'/(row['name']+'.stdout')).read_bytes())
     row.pop('stderr_sha256')
   qualifications.append({'file':f+'/'+name,'difference':'Only derived stderr hashes differ with private traceback paths; both complete stderr sidecars were hash-checked and normalized stderr_tail is compared.'})
  if workspace_head:
   oldhead=old['workspace_head_observed'];assert new['workspace_head_observed']==head
   new['workspace_head_observed']=oldhead
   qualifications.append({'file':f+'/'+name,'old_workspace_head':oldhead,'actual_workspace_head':head,'difference':'Dated workspace observation only; pinned PR head/base and all original Git bindings remain identical.'})
  no,nn=normalize(old),normalize(new)
  if no!=nn:
   save(private.parent/'COMPARISON_FAILURE.json',{'file':f+'/'+name,'old_normalized':no,'new_normalized':nn})
   raise AssertionError('Full structured receipt mismatch: '+f+'/'+name)
  comparisons.append({'file':f+'/'+name,'full_structured_comparison':'PASS','original_sha256':sha((A/f/name).read_bytes()),'actual_sha256':sha((pa/f/name).read_bytes())})
 g='graph_family'
 run('graph_manifest',[A/g/'manifest_closure.py','--verify'])
 run('graph_exact',[pa/g/'independent_graph_audit.py'])
 run('graph_binding',[pa/g/'replay_and_binding.py'])
 run('graph_packet_controls',[pa/g/'packet_coverage_controls.py'])
 for name in ['independent_graph_results.json','original_binding_and_replay.json','packet_coverage_results.json']:compare(g,name)
 g='algebraic_family'
 run('algebra_manifest',[A/g/'verify_authored_manifest.py'])
 run('algebra_replays_and_mutants',[pa/g/'replay_and_bind.py'])
 compare(g,'git_binding_results.json');compare(g,'replay_mutation_results.json',derived_stderr=True)
 g='primary_scope_family'
 script=pa/g/'audit_provenance_replay.py';old=script.read_text();anchor="ROOT=Path('/Users/alec/Documents/Math')"
 assert old.count(anchor)==1
 altered=old.replace(anchor,'ROOT=Path('+repr(str(private))+')',1);script.write_text(altered)
 patch=''.join(difflib.unified_diff(old.splitlines(True),altered.splitlines(True),fromfile='frozen_original',tofile='private_redirect'))
 (private.parent/'PRIMARY_ROOT_REDIRECTION.patch').write_text(patch)
 qualifications.append({'file':g+'/audit_provenance_replay.py','original_sha256':sha(old.encode()),'private_sha256':sha(altered.encode()),'patch_sha256':sha(patch.encode()),'difference':'One literal ROOT-path redirection; all mathematical, provenance and audit-predicate instructions unchanged.'})
 run('primary_full_corpus_git_replays_mutants',[script])
 for name in ['corpus_queue_receipt.json','actual_git_receipt.json','unchanged_private_replay.json','executable_mutant_receipts.json','source_accounting_mutant_receipts.json','prose_coverage_receipt.json']:
  compare(g,name,workspace_head=name=='actual_git_receipt.json')
 spec=importlib.util.spec_from_file_location('root_pr36_pure_queue',Q/'queue.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 frozen=load(A/'source_snapshot/source_record.json');cfg=load(Q/'policy.json');mut=load(A/g/'actual_queue_score_mutant_receipts.json')
 assert mut['queue_module_sha256']==sha((Q/'queue.py').read_bytes())
 newmut=[]
 for row in mut['mutants']:
  p=copy.deepcopy(frozen['problem']);r=copy.deepcopy(frozen['upstream_prior_report'])
  (p if row['where']=='p' else r)[row['key']]=row['value']
  actual=mod.score(p,r,cfg);assert actual==row['result'],row['label']
  newmut.append({'label':row['label'],'actual_score_called':True,'result':actual})
 save(private.parent/'ACTUAL_SIX_PURE_QUEUE_SCORE_MUTANTS.json',newmut)
 g='arithmetic_graph_priority_family'
 run('arithmetic_manifest',[A/g/'check_authored_manifest.py'])
 run('arithmetic_manifest_controls',[pa/g/'check_authored_manifest.py','--controls'])
 compare(g,'AUTHORED_MANIFEST_CONTROL_RESULTS.json')
 run('arithmetic_silverman',[pa/g/'verify_silverman.py'])
 compare(g,'SILVERMAN_EXACT_CHECK_RESULTS.json')
 g='antipodal_priority_family'
 run('antipodal_manifest',[A/g/'seal_authored.py','--verify'])
 for receipt in ['CONTROL_RESULTS.json','EXECUTABLE_MUTANT_RESULTS.json']:
  for row in load(A/g/receipt)['records']:
   argv=[private/x if x.startswith('draft_pr_publication_program_20260930/') else x for x in row['command'][1:]]
   cp=run('antipodal_'+row['case'],argv,row['exit'])
   expected=A/g/'controls'/(row['case']+'.stdout')
   assert cp.stdout==expected.read_bytes(),row['case']
   assert normalize(cp.stderr.decode())==normalize((A/g/'controls'/(row['case']+'.stderr')).read_text()),row['case']
 cp=run('antipodal_positive_optimized',['-O',pa/g/'verify_silverman.py',pa/g/'silverman_degree3.json'])
 assert cp.stdout==(A/g/'controls/positive_degree3_optimized.stdout').read_bytes()
 cp=run('antipodal_independent_child',[pa/g/'silverman_independent_verifier/exact_checks.py'])
 assert cp.stdout==(A/g/'controls/independent_checker_replay.stdout').read_bytes()
 after,afterparses=closure();assert before==after and parse_count==afterparses
 assert live=={str(p.relative_to(R)):sha(p.read_bytes()) for p in [Q/'QUEUE.md',Q/'state.json',Q/'history.jsonl']}
 result={'utc':utc(),'status':'PASS','closed_family_count':5,'authored_members_verified_before_and_after':364,'full_authored_json_jsonl_parses_per_pass':parse_count,'new_substantive_attempts':0,'original_substantive_turns':1,'turn_limit':5,'root_script_sha256':sha(Path(__file__).read_bytes()),'private_replica':str(private),'actual_outer_program_runs':runs,'full_structured_receipt_comparisons':comparisons,'six_actual_pure_queue_score_mutants':newmut,'qualifications':qualifications,'foreign_inputs':foreign,'closed_manifests':before,'live_queue_state_history_unchanged':live,'limitations':'No finite diagnostic certifies source theorem prose or novelty. Root separately reconstructed the universal proof and read primary operative source pages. Historical -O assertion bypass and prose blind spots are retained as successful negative controls, not hidden.'}
 save(A/'ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json',result)
 print(json.dumps({'status':'PASS','closed_families':5,'authored_members_before_and_after':364,'outer_runs':len(runs),'structured_comparisons':len(comparisons),'new_attempts':0,'receipt':str(A/'ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json')},indent=2))
if __name__=='__main__':main()
