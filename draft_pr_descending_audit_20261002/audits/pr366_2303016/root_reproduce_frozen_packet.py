"""Complete frozen scope/history/manifest validation and whole output replay."""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import base64,concurrent.futures,hashlib,json,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];P='unsolved_math_prioritization/attempts/2303016/';Q='unsolved_math_prioritization/QUEUE.md'
D=A/'snapshot'/P;S=A/'root_original_streams';S.mkdir(exist_ok=True);V=A/'root_replay_private';V.mkdir(exist_ok=True)
PY=R/'draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
checks=[];sha=lambda b:hashlib.sha256(b).hexdigest();blob=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def ck(v,name):checks.append({'name':name,'passed':bool(v)});assert v,name
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def get(rev,p):return git('show',rev+':'+p)
def tree(rev):
 return {row.split(b'\t',1)[1].decode():row.split(b'\t',1)[0].decode() for row in git('ls-tree','-rz','--full-tree',rev).split(b'\0') if row}
m=json.loads((A/'snapshot_manifest.json').read_bytes());H=m['head'];B=m['base'];C='2a14016d7e62d1b044bb63cad51a25e5747e7cd1'
ck(H=='f4039c9c093b10e651ee7fd2e6379073b84238c7' and B=='efd29c05204703acca9a0860812f54b94fae54b1','literal frozen pair')
bt,ht=tree(B),tree(H);expected={e['path'] for e in m['files']}
ck(len(expected)==22 and expected=={p for p in bt.keys()|ht.keys() if bt.get(p)!=ht.get(p)},'all22 whole-repository mode/type/blob changes')
ck({p for p in ht if p.startswith(P)}==expected-{Q},'all21 actual target paths')
ck({P+f.relative_to(D).as_posix() for f in D.rglob('*') if f.is_file()}==expected-{Q},'all21 snapshot target paths')
def remote(e):
 p=e['path'];r=subprocess.run(['gh','api','repos/AlecKriebel/Math/contents/'+p+'?ref='+H],cwd=R,capture_output=True)
 tag=p.replace('/','__');(V/(tag+'.stdout')).write_bytes(r.stdout);(V/(tag+'.stderr')).write_bytes(r.stderr)
 assert r.returncode==0 and not r.stderr,p
 o=json.loads(r.stdout);raw=base64.b64decode(o['content'])
 return {'path':p,'bytes':len(raw),'sha256':sha(raw),'git_blob':blob(raw),'entry':ht[p],'passed':raw==(A/'snapshot'/p).read_bytes()==get(H,p) and len(raw)==e['bytes']==o['size'] and sha(raw)==e['sha256'] and blob(raw)==e['git_blob_sha']==o['sha'] and ht[p].split()==['100644','blob',blob(raw)]}
with concurrent.futures.ThreadPoolExecutor(4) as pool:rr=list(pool.map(remote,m['files']))
for row in rr:ck(row['passed'],'whole actual Git/API/disk '+row['path'])
bindings=[]
for name in ['TURN_1_MANIFEST.json','FINAL_FROZEN_MANIFEST.json','final_review/REVIEW_MANIFEST.json','PUBLICATION_MANIFEST.json']:
 mf=D/name;o=json.loads(mf.read_bytes());seen=set()
 for e in o['files']:
  q=PurePosixPath(e['path']);ck(not q.is_absolute() and '..' not in q.parts and q.as_posix()==e['path'] and e['path'] not in seen,'safe nested path '+name+'/'+e['path']);seen.add(e['path'])
  f=mf.parent/q;raw=f.read_bytes();ck(len(raw)==e['bytes'] and sha(raw)==e['sha256'],'whole nested binding '+name+'/'+e['path']);bindings.append({'manifest':name,'path':f.relative_to(D).as_posix(),**e,'passed':True})
ck(len(bindings)==48,'all48 nested manifest instances')
pub=json.loads((D/'PUBLICATION_MANIFEST.json').read_bytes());ck({e['path'] for e in pub['files']}=={p.removeprefix(P) for p in expected-{Q,P+'PUBLICATION_MANIFEST.json'}},'publication full20 self-excluded paths')
ck(pub['author_manifest_sha256']==sha((D/'FINAL_FROZEN_MANIFEST.json').read_bytes()) and pub['review_manifest_sha256']==sha((D/'final_review/REVIEW_MANIFEST.json').read_bytes()),'publication author and review anchors')
ck(git('show','-s','--format=%P',C).decode().strip()==B,'real one-turn checkpoint parent')
ck(git('show','-s','--format=%P',H).decode().strip().split()==[B,C],'actual original head parents')
author={e['path'] for e in json.loads((D/'FINAL_FROZEN_MANIFEST.json').read_bytes())['files']}|{'FINAL_FROZEN_MANIFEST.json'}
ck(len(author)==14,'all14 actual author files')
ck(set(git('diff','--name-only',B,C).decode().splitlines())=={P+p for p in author},'one author checkpoint exactly14 files')
for p in sorted(author):ck(get(C,P+p)==(D/p).read_bytes()==get(H,P+p),'whole historical author '+p)
ledger=[json.loads(l) for l in (D/'TURN_1_LEDGER.jsonl').read_text().splitlines()];st=json.loads((D/'TURN_1_STATE.json').read_bytes())
ck([e['turns_used'] for e in ledger]==[0,1] and ledger[-1]==st and ledger[-1]['event']=='proof_attempt_turn','actual one-turn ledger/state exact')
catalog=json.loads(get(B,'unsolved_math_prioritization/catalog.json'));row=next(x for x in catalog if x['id']=='2303016')
ck(row['statement_hash']==st['statement_hash'] and row['review_hash']==st['review_hash'] and row['problem_number']=='AMR-022-3016','frozen base catalog exact statement/review anchors')
baseq=get(B,Q);lines=baseq.splitlines(keepends=True);ix=[i for i,l in enumerate(lines) if len(l.split(b'|'))>9 and l.split(b'|')[2].strip().split(b' / ')[0]==b'2303016'];ck(len(ix)==1,'unique original queue row')
i=ix[0];cells=lines[i].split(b'|');ck([cells[j].strip() for j in [8,9]]==[b'queued',b'0/5'],'original queued0 cells');cells[8:10]=[b' already_solved ',b' 1/5 '];lines[i]=b'|'.join(cells);ck(b''.join(lines)==get(H,Q),'whole original queue only own two cells')
sources=[]
for e in json.loads((D/'SOURCE_MANIFEST.json').read_bytes())['primary_pdfs']:
 b=(A/'root_primary_private'/e['file']).read_bytes();ck(len(b)==e['bytes'] and sha(b)==e['sha256'],'fresh whole primary '+e['file']);sources.append({**e,'passed':True})
seal=json.loads((A/'ROOT_BASELINE_SEAL.json').read_bytes())
for e in seal['files']:ck(len((A/e['path']).read_bytes())==e['bytes'] and sha((A/e['path']).read_bytes())==e['sha256'],'root pre-candidate baseline unchanged '+e['path'])
replays=[]
for label,args,exp in [('author',[str(PY),str(D/'verify_turn1.py')],D/'TURN_1_CHECKS.json'),('historical_review',[str(PY),str(D/'final_review/check.py'),str(D)],D/'final_review/CHECKS.json')]:
 r=subprocess.run(args,cwd=V,capture_output=True);(S/(label+'.stdout')).write_bytes(r.stdout);(S/(label+'.stderr')).write_bytes(r.stderr)
 ck(r.returncode==0 and not r.stderr,'replay exit '+label);ck(r.stdout==exp.read_bytes(),'whole exact output '+label)
 replays.append({'label':label,'args':args,'exit':r.returncode,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr),'complete_output':r.stdout.decode()})
ck(json.loads(replays[0]['complete_output'])['assertions']==2690 and json.loads(replays[1]['complete_output'])['independent_assertions']==1909,'exact author2690 and independent1909 controls')
out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','frozen_head':H,'original_base':B,'checks':checks,'check_count':len(checks),'remote_files':rr,'nested_bindings':bindings,'binding_count':48,'actual_author_checkpoint':C,'author_files':14,'primary_sources':sources,'replays':replays,'historical_dataset_revision_object_available':False,'historical_negative_all_refs_search_reproduced':False,'source_method_novelty_certified':False,'continuum_proof_established_by_finite_controls':False,'program_sha256':sha(Path(__file__).read_bytes())}
(A/'root_original_reproduction_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','check_count','binding_count','actual_author_checkpoint','author_files']},indent=2))
