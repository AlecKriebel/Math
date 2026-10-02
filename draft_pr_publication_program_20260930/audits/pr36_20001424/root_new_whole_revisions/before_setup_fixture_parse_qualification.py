#!/usr/bin/env python3
"""Root actual NEW whole audit replay. Closed authors remain byte-exact."""
from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys, traceback
sys.dont_write_bytecode=True
A=Path(__file__).resolve().parent
R=A.parents[2]
W=A/'whole_current_source_first_family'
C=A/'reviewed_candidate'
PIN='93399cc5c589fc8421cd622d86062550645ab9955d709bed846cfdb58d2b9712'
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
def need(c,m):
 if not c:raise ValueError(m)
def rows(p):
 x=load(p)['files'];return [dict(v,path=k) for k,v in x.items()] if isinstance(x,dict) else x
def verify(base,mp,strict=False):
 seen=set();parsed=0
 for x in rows(mp):
  rel=x['path'];p=Path(rel);need(not p.is_absolute() and '..' not in p.parts and rel not in seen,'unsafe/duplicate');seen.add(rel)
  q=base/rel;need(q.is_file() and not q.is_symlink(),'nonregular');b=q.read_bytes()
  need(len(b)==x.get('bytes',x.get('size')) and sha(b)==x['sha256'],'changed '+rel)
  if q.suffix=='.json':json.loads(b);parsed+=1
  if q.suffix=='.jsonl':
   for line in b.splitlines():json.loads(line)
   parsed+=1
 if strict:
  actual={str(p.relative_to(base)) for p in base.rglob('*') if p.is_file() and not {'tmp','__pycache__'}&set(p.relative_to(base).parts)}
  need(actual==seen|{mp.name},'strict inventory')
 return len(seen),parsed
def main():
 need(sha((W/'AUTHORED_MANIFEST.json').read_bytes())==PIN,'whole pin')
 count,parsed=verify(W,W/'AUTHORED_MANIFEST.json',True);need(count==1795,'count1795')
 verify(C,C/'MANIFEST.json',True);verify(A,C/'CURRENT_PROOF_DEPENDENCIES.json')
 stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
 private=A/'tmp'/('root_new_whole_'+stamp)/'repository';pa=private/A.relative_to(R);pw=pa/W.name
 pa.mkdir(parents=True)
 # Copy every bound byte and its exact anchor; no implementation edits.
 copies={}
 def copy(base,mp,target):
  for x in [*rows(mp),{'path':str(mp.relative_to(base))}]:
   source=base/x['path'];dest=target/x['path'];dest.parent.mkdir(parents=True,exist_ok=True)
   if dest.exists():need(dest.read_bytes()==source.read_bytes(),'overlap')
   else:shutil.copyfile(source,dest)
   copies[str(source.relative_to(A))]=sha(source.read_bytes())
 copy(A,C/'CURRENT_PROOF_DEPENDENCIES.json',pa)
 copy(C,C/'MANIFEST.json',pa/'reviewed_candidate')
 copy(W,W/'AUTHORED_MANIFEST.json',pw)
 runs=[]
 def run(label,argv):
  cp=subprocess.run(argv,cwd=private,capture_output=True,timeout=180)
  for ext,b in [('stdout',cp.stdout),('stderr',cp.stderr)]:
   p=pa/'root_new_whole_streams'/(label+'.'+ext);p.parent.mkdir(exist_ok=True);p.write_bytes(b)
  rec={'label':label,'command':argv,'exit':cp.returncode,'stdout_sha256':sha(cp.stdout),'stderr_sha256':sha(cp.stderr)};runs.append(rec)
  need(cp.returncode==0,label+' failed '+cp.stderr.decode()[-1800:]);return cp
 run('strict_closed_whole_verify',[sys.executable,str(pw/'replay_current_packet.py'),'--verify'])
 run('actual_new_whole_replay',[sys.executable,str(pw/'replay_current_packet.py'),'--run'])
 run('actual_support_relations',[sys.executable,str(pw/'verify_support_relations.py')])
 fresh=list(pw.glob('ACTUAL_REPLAY_*.json'));latest=max(fresh,key=lambda p:p.name)
 need(latest.name not in {p.name for p in W.glob('ACTUAL_REPLAY_*.json')},'not fresh')
 old=W/'ACTUAL_REPLAY_20261002T081248401131Z.json'
 before=load(old);after=load(latest)
 # Normalize ONLY clocks and exact allocated roots; every other scalar is compared.
 def norm(x):
  if isinstance(x,dict):return {k:norm(v) for k,v in x.items() if k!='utc'}
  if isinstance(x,list):return [norm(v) for v in x]
  if isinstance(x,str):
   x=x.replace(str(pw/'actual_replay'/latest.stem.removeprefix('ACTUAL_REPLAY_')),str(W/'actual_replay'/'20261002T081248401131Z')).replace(str(private),str(R))
  return x
 comparable=json.loads(json.dumps(after))
 stream_comparisons=[]
 for oldrow,newrow,cmp in zip(before['actual_runs'],after['actual_runs'],comparable['actual_runs']):
  need(oldrow['label']==newrow['label'],'run order')
  op=Path(oldrow['command'][2] if oldrow['optimized'] else oldrow['command'][1]).parent
  np=Path(newrow['command'][2] if newrow['optimized'] else newrow['command'][1]).parent
  for ext in ['stdout','stderr']:
   ob=(op/('actual.'+ext)).read_bytes();nb=(np/('actual.'+ext)).read_bytes()
   need(sha(ob)==oldrow[ext+'_sha256'] and sha(nb)==newrow[ext+'_sha256'],'full stream hash')
   need(norm(nb.decode())==norm(ob.decode()),'complete normalized stream '+oldrow['label']+' '+ext)
   cmp[ext+'_sha256']=oldrow[ext+'_sha256']
   stream_comparisons.append({'label':oldrow['label'],'stream':ext,'old_sha256':sha(ob),'fresh_sha256':sha(nb),'complete_normalized_bytes_equal':True})
 need(norm(before)==norm(comparable),'full whole receipt mismatch')
 need(len(after['actual_runs'])==27 and all(x['exit']==x['expected_exit'] for x in after['actual_runs']),'actual27 exits')
 support_old=W/'SUPPORT_RELATION_RESULTS.json';support_new=pw/'SUPPORT_RELATION_RESULTS.json'
 need(norm(load(support_old))==norm(load(support_new)),'full support receipt mismatch')
 # Read actual original Git blobs and live entire queue. Original diff remains frozen.
 sm=load(A/'snapshot_manifest.json');head=sm['head'];prefix='unsolved_math_prioritization/attempts/20001424/'
 for x in sm['files']:
  b=subprocess.check_output(['git','show',head+':'+prefix+x['path']],cwd=R,timeout=30)
  need(b==(A/'source_snapshot'/x['path']).read_bytes(),'live original Git '+x['path'])
 q=(R/'unsolved_math_prioritization/QUEUE.md').read_bytes();patch=load(C/'CURRENT_QUEUE_PATCH.json')
 need(sha(q)==patch['whole_queue_preimage_sha256'],'live whole queue preimage')
 need(q.count(patch['row_before'].encode())==1,'unique live selected row')
 need(subprocess.check_output(['git','branch','--show-current'],cwd=R).strip()==b'main','main')
 need(verify(W,W/'AUTHORED_MANIFEST.json',True)==(count,parsed),'closed whole changed')
 verify(C,C/'MANIFEST.json',True);verify(A,C/'CURRENT_PROOF_DEPENDENCIES.json')
 for rel,h in copies.items():need(sha((A/rel).read_bytes())==h,'source copy changed '+rel)
 # Retain fresh first-party complete streams and receipts, never foreign downloads.
 retained=[]
 out=A/'root_new_whole_replay';out.mkdir(exist_ok=False)
 for source,rel in [(latest,'ACTUAL_REPLAY.json'),(support_new,'SUPPORT_RELATION_RESULTS.json')]+[(p,'streams/'+p.name) for p in sorted((pa/'root_new_whole_streams').iterdir())]:
  dest=out/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest);b=dest.read_bytes();retained.append({'path':str(dest.relative_to(A)),'bytes':len(b),'sha256':sha(b)})
 # Preserve all actual inner output streams/source patches/specs for fresh reproduction.
 actual=pw/'actual_replay'/latest.stem.removeprefix('ACTUAL_REPLAY_')
 for source in sorted(actual.rglob('*')):
  if not source.is_file():continue
  dest=out/'actual'/source.relative_to(actual);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest);b=dest.read_bytes();retained.append({'path':str(dest.relative_to(A)),'bytes':len(b),'sha256':sha(b)})
 retention={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'self_excluded':['ROOT_NEW_WHOLE_RETENTION.json'],'files':retained,'member_count':len(retained)}
 (A/'ROOT_NEW_WHOLE_RETENTION.json').write_text(json.dumps(retention,indent=2)+'\n')
 receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','pr':36,'problem_id':20001424,'original_head':head,'reviewed_candidate_manifest_sha256':sha((C/'MANIFEST.json').read_bytes()),'current_proof_dependencies_sha256':sha((C/'CURRENT_PROOF_DEPENDENCIES.json').read_bytes()),'whole_manifest_sha256':PIN,'queue_status':'already_solved','priority_classification':'PRIOR_APPLICATION','mandatory_corrections':[],'entire_current_packet_checked':True,'root_actual_reproduction':True,'original_substantive_attempts':1,'new_substantive_attempts':0,'verification_attempts_added':0,'paper_or_new_doi_or_tracker':False,'whole_authored_members_verified_before_and_after':count,'whole_json_jsonl_full_parses_per_pass':parsed,'actual_outer_program_runs':runs,'actual_inner_program_runs':after['actual_runs'],'complete_actual_stream_comparisons':stream_comparisons,'full_structured_receipt_comparisons':[{'old':str(old.relative_to(A)),'fresh':str((out/'ACTUAL_REPLAY.json').relative_to(A)),'normalization':'Only utc dictionary keys, exact private repository root, exact fresh allocated round name; stream hash changes accepted only after complete normalized stderr/stdout bytes matched; every other scalar identical.','equal':True},{'old':str(support_old.relative_to(A)),'fresh':str((out/'SUPPORT_RELATION_RESULTS.json').relative_to(A)),'normalization':'Only utc keys.','equal':True}],'live_original_git16_byte_equality':True,'live_whole_queue_preimage_sha256':sha(q),'retention_manifest_sha256':sha((A/'ROOT_NEW_WHOLE_RETENTION.json').read_bytes()),'root_script_sha256':sha(Path(__file__).read_bytes()),'root_scientific_assessment':'Complete cubic proof and exact printed primary source manually checked independently; graph mechanism verified under stated established imports. Original optimized/prose/output-label blind spots retained. No earliest-worldwide or narrower-degree11 priority assertion.'}
 (A/'ROOT_FINAL_NEW_WHOLE_ACTUAL_REPRODUCTION.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps({'status':'PASS','whole_members':count,'actual_inner_runs':27,'retained_members':len(retained)},indent=2))
if __name__=='__main__':
 try:main()
 except Exception:
  p=A/('ROOT_NEW_WHOLE_FAILURE_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'.json')
  p.write_text(json.dumps({'status':'FAIL','root_script_sha256':sha(Path(__file__).read_bytes()),'traceback':traceback.format_exc()},indent=2)+'\n')
  raise
