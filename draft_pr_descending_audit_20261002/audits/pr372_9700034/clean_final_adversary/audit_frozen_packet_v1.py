#!/usr/bin/env python3
"""Read-only exhaustive historical packet verification; writes only an own receipt."""
from pathlib import Path, PurePosixPath
import argparse,hashlib,json,subprocess,datetime,sys,shutil
p=argparse.ArgumentParser();p.add_argument('--snapshot',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);p.add_argument('--sources',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
T='problems/9700034_sirsn_maximal_routes';H='f30fb696da92fd4b998d61859d6ed06012ce78d4';B='efd29c05204703acca9a0860812f54b94fae54b1';W='6f29bc5129f519ef5d6cb8901f5abb35868c4d03';Q='unsolved_math_prioritization/QUEUE.md'
turns=['35cc2c374ea854e21e6beb50210bb087ceea0cdd','c4169ccae93d60469db1ddfa508946e8e427a6b3','9654de1e3f96dc6ee92b273afb4e2d56cd81f912','a50223882a24011ac53ea0283ebf34fcd578fd4d',W]
checks=[]
def ck(condition,label,detail=None):
 checks.append({'label':label,'pass':bool(condition),'detail':detail})
 if not condition:raise RuntimeError(label)
def git(*args):return subprocess.check_output(['git','-C',str(a.repo),*args])
def blob(rev,path):return git('show',rev+':'+path)
def tree(rev):
 out={}
 for item in git('ls-tree','-rz','--full-tree',rev).split(b'\0'):
  if item:
   meta,path=item.split(b'\t',1);mode,typ,sha=meta.decode().split();out[path.decode()]={'mode':mode,'type':typ,'sha':sha}
 return out
try:
 d=a.snapshot/T; actual={str(f.relative_to(d)):f.read_bytes() for f in d.rglob('*') if f.is_file()};ck(len(actual)==48,'literal target snapshot has 48 paths',len(actual))
 htree=tree(H);btree=tree(B);wtree=tree(W);expected={T+'/'+n for n in actual}|{Q};changed={n for n in htree.keys()|btree.keys() if htree.get(n)!=btree.get(n)};ck(changed==expected,'complete root tree change set exactly target48 plus queue',sorted(changed))
 for n,b in actual.items():ck(blob(H,T+'/'+n)==b,'snapshot literal bytes equal Git head: '+n)
 hb=blob(H,Q);bb=blob(B,Q);lines=bb.splitlines(keepends=True);rows=[i for i,s in enumerate(lines) if b'| 397 | 9700034 / AMR-096-0034 |' in s];ck(len(rows)==1,'exact own queue row occurrence')
 i=rows[0];before=lines[i];after=before.replace(b'| queued | 0/5 |',b'| unsolved | 5/5 |');ck(after!=before,'queue literal two-cell substitution');lines[i]=after;ck(hb==b''.join(lines),'complete queue equals sole two-cell substitution');ck((a.snapshot/Q).read_bytes()==hb,'snapshot queue bytes equal Git head')
 ck(git('show','-s','--format=%P',H).decode().strip().split()==[B,W],'historical head ordered parents')
 prev=B;historical=[];allbound=[]
 for k,rev in enumerate(turns,1):
  ck(git('show','-s','--format=%P',rev).decode().strip().split()==[prev],'checkpoint sole exact previous parent '+str(k));tr=tree(rev);chg={n for n in tr.keys()|tree(prev).keys() if tr.get(n)!=tree(prev).get(n)};ck(all(n.startswith(T+'/') for n in chg),'checkpoint scope target only '+str(k),sorted(chg))
  manifest=json.loads(blob(rev,T+f'/TURN_{k}_MANIFEST.json'));ck(manifest['author_turns_used']==k,'historical turn count '+str(k))
  for f in manifest['files']:
   n=f['path'];b=blob(rev,T+'/'+n);ck(len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],'historical binding '+str(k)+' '+n);ck(actual[n]==b,'historical bound bytes preserved '+str(k)+' '+n);allbound.append((k,n))
  if k>1:ck(manifest['previous_manifest_sha256']==hashlib.sha256(blob(turns[k-2],T+f'/TURN_{k-1}_MANIFEST.json')).hexdigest(),'historical chain link '+str(k))
  historical.append({'turn':k,'sha':rev,'parent':prev,'changed_paths':sorted(chg),'target_paths':sorted(n[len(T)+1:] for n in tr if n.startswith(T+'/'))});prev=rev
 ck(len(allbound)==27,'all27 historical bindings')
 binding_counts={}
 for mn,base in [(f'TURN_{k}_MANIFEST.json',d) for k in range(1,6)]+[('FINAL_AUTHOR_MANIFEST.json',d),('PUBLICATION_MANIFEST.json',d),('review/REVIEW_MANIFEST.json',d/'review')]:
  m=json.loads((d/mn).read_bytes());seen=set()
  for f in m['files']:
   q=PurePosixPath(f['path']);ck(not q.is_absolute() and '..' not in q.parts and f['path'] not in seen,'safe unique manifest path '+mn+' '+f['path']);seen.add(f['path']);b=(base/f['path']).read_bytes();ck(len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],'full manifest binding '+mn+' '+f['path'])
  binding_counts[mn]=len(seen)
  if mn=='PUBLICATION_MANIFEST.json':ck(seen|{mn}==set(actual),'complete publication closure all48 paths')
  if mn=='FINAL_AUTHOR_MANIFEST.json':ck({T+'/'+n for n in seen|{mn}}=={n for n in wtree if n.startswith(T+'/')},'actual WIP exactly38 author files and final manifest closure');ck(all(blob(W,T+'/'+n)==actual[n] for n in seen|{mn}),'all38 actual WIP bytes preserved')
 for f in json.loads((d/'SOURCE_MANIFEST.json').read_bytes())['files']:
  b=(a.sources/f['name']).read_bytes();ck(len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],'fresh primary binding '+f['name'])
 author=a.output.parent/'private_replay'/'actual_wip';author.mkdir(exist_ok=False)
 for n in wtree:
  if n.startswith(T+'/'):
   rel=n[len(T)+1:];q=author/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(blob(W,n))
 r=subprocess.run([sys.executable,str(d/'review/replay_author.py'),str(author)],capture_output=True);(a.output.parent/'private_replay'/'review_author_actual_wip.stdout').write_bytes(r.stdout);(a.output.parent/'private_replay'/'review_author_actual_wip.stderr').write_bytes(r.stderr);ck(r.returncode==0 and not r.stderr and r.stdout==(d/'review/AUTHOR_REPLAY.json').read_bytes(),'historical review replay complete stdout exact on actual WIP',{'exit':r.returncode,'stdout_bytes':len(r.stdout),'stderr_bytes':len(r.stderr),'whole_json':json.loads(r.stdout) if r.stdout else None})
 final=json.loads((d/'FINAL_REPLAY.json').read_bytes());ck(final['historical_bindings_checked']==27 and final['historical_chain_links_checked']==4 and final['source_files_checked']==4,'complete FINAL_REPLAY counts');ck(final['total_exact_assertions']==503419,'FINAL_REPLAY total')
 for k,entry in enumerate(final['replays'],1):
  b=(d/f'TURN_{k}_CHECKS.json').read_bytes();v=json.loads(b);ck(entry=={'turn':k,'exact_assertions':v['exact_assertions'],'stdout_byte_exact':True,'receipt_sha256':hashlib.sha256(b).hexdigest()},'complete FINAL_REPLAY row '+str(k))
 result={'status':'PASS_HISTORICAL_SCOPE_ONLY','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':H,'base':B,'final_author_wip':W,'target_paths':48,'changed_paths':49,'checks':checks,'binding_counts':binding_counts,'historical_checkpoints':historical,'own_queue_before_utf8':before.decode(),'own_queue_after_utf8':after.decode(),'claim_scope':'Historical packet provenance and byte integrity; no current live PR readiness/merge/novelty acceptance.'}
except Exception as e:result={'status':'FAIL','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'error':repr(e),'checks':checks}
a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'checks':len(checks),'output':str(a.output)}));sys.exit(0 if result['status'].startswith('PASS') else 1)
