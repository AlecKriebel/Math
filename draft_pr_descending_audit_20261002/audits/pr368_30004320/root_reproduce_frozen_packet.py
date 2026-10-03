"""Root complete frozen Git/API/history/source validation and full-stream replay."""
from pathlib import Path,PurePosixPath
import base64,concurrent.futures,datetime,hashlib,json,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];PREFIX='problems/30004320_laurent_descent/';Q='unsolved_math_prioritization/QUEUE.md'
D=A/'snapshot'/PREFIX;PRIVATE=A/'tmp/root_original';PRIVATE.mkdir(parents=True,exist_ok=True)
STREAMS=A/'root_original_streams';STREAMS.mkdir(exist_ok=True)
PY=R/'draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
checks=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def ck(v,name):checks.append({'name':name,'pass':bool(v)});assert v,name
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def get(rev,path):return git('show',rev+':'+path)
def tree(rev):
 out={}
 for row in git('ls-tree','-rz','--full-tree',rev).split(b'\0'):
  if row:
   meta,path=row.split(b'\t',1);out[path.decode()]=meta.decode()
 return out
m=json.loads((A/'snapshot_manifest.json').read_bytes());HEAD=m['head'];BASE=m['base']
ck(HEAD=='74617174ddfb3ea726cea343a4ba915613724bdc','literal original head')
ck(BASE=='efd29c05204703acca9a0860812f54b94fae54b1','literal original base')
bt=tree(BASE);ht=tree(HEAD);expected={x['path'] for x in m['files']}
ck(len(expected)==54 and expected=={p for p in bt.keys()|ht.keys() if bt.get(p)!=ht.get(p)},'complete54 all-root mode/type/blob delta')
ck({p for p in ht if p.startswith(PREFIX)}==expected-{Q},'complete53 actual target paths')
ck({PREFIX+p.relative_to(D).as_posix() for p in D.rglob('*') if p.is_file()}==expected-{Q},'complete53 disk target paths')
def remote(row):
 path=row['path'];r=subprocess.run(['gh','api','repos/AlecKriebel/Math/contents/'+path+'?ref='+HEAD],cwd=R,capture_output=True)
 tag=path.replace('/','__');(PRIVATE/(tag+'.stdout')).write_bytes(r.stdout);(PRIVATE/(tag+'.stderr')).write_bytes(r.stderr)
 assert r.returncode==0 and not r.stderr,path
 obj=json.loads(r.stdout);raw=base64.b64decode(obj['content'])
 return {'path':path,'bytes':len(raw),'sha256':sha(raw),'git_blob':blob(raw),'git_entry':ht[path],'pass':raw==(A/'snapshot'/path).read_bytes()==get(HEAD,path) and len(raw)==row['bytes']==obj['size'] and sha(raw)==row['sha256'] and blob(raw)==row['git_blob_sha']==obj['sha'] and ht[path].split()==['100644','blob',blob(raw)]}
remote_rows=list(concurrent.futures.ThreadPoolExecutor(6).map(remote,m['files']))
for row in remote_rows:ck(row['pass'],'literal frozen Git/API/disk '+row['path'])
bindings=[];manifests=[]
for name in [*[f'TURN_{i}_MANIFEST.json' for i in range(1,6)],'FINAL_AUTHOR_MANIFEST.json','review/REVIEW_MANIFEST.json','PUBLICATION_MANIFEST.json']:
 mf=D/name;obj=json.loads(mf.read_bytes());seen=set()
 for e in obj['files']:
  rel=PurePosixPath(e['path']);ck(not rel.is_absolute() and '..' not in rel.parts and rel.as_posix()==e['path'] and e['path'] not in seen,'safe nested path '+name+'/'+e['path']);seen.add(e['path'])
  f=mf.parent/rel;raw=f.read_bytes();ck(len(raw)==e['bytes'] and sha(raw)==e['sha256'],'full nested binding '+name+'/'+e['path'])
  bindings.append({'manifest':name,'path':f.relative_to(D).as_posix(),'bytes':len(raw),'sha256':sha(raw),'pass':True})
 if name.startswith('TURN_') and int(name.split('_')[1])>1:
  i=int(name.split('_')[1]);ck(sha((D/f'TURN_{i-1}_MANIFEST.json').read_bytes())==obj['previous_manifest_sha256'],'unchanged full historical chain '+name)
 manifests.append({'path':name,'bytes':len(mf.read_bytes()),'sha256':sha(mf.read_bytes()),'bound_files':len(seen)})
ck(len(bindings)==130 and len(manifests)==8,'complete8 manifests130 nested instances')
pub=json.loads((D/'PUBLICATION_MANIFEST.json').read_bytes());ck({e['path'] for e in pub['files']}=={p.removeprefix(PREFIX) for p in expected-{Q,PREFIX+'PUBLICATION_MANIFEST.json'}},'self-excluded52 literal publication paths')
commits=['5e2eb63fd571f2f660ff9ebb436440029b5d1268','d7d898ba23e9d024e79b938e3e0e305d91bb125b','c800217d22d329d6ca397f3c18e5115c77688fb9','24ecf1f2f0ab62082f328545180e4b2ba1640ab7','b08662a16499edf37f0c0eae850cfa00b7778ed6']
checkpoint_rows=[]
for i,c in enumerate(commits,1):
 ck(git('show','-s','--format=%P',c).decode().strip()==(BASE if i==1 else commits[i-2]),'real author checkpoint parent '+str(i))
 obj=json.loads((D/f'TURN_{i}_MANIFEST.json').read_bytes());paths={e['path'] for e in obj['files']}|{f'TURN_{i}_MANIFEST.json'}
 for p in sorted(paths):ck(get(c,PREFIX+p)==(D/p).read_bytes(),'actual author checkpoint '+str(i)+'/'+p)
 checkpoint_rows.append({'turn':i,'commit':c,'bound_files_plus_manifest':len(paths),'pass':True})
author_paths={e['path'] for e in json.loads((D/'FINAL_AUTHOR_MANIFEST.json').read_bytes())['files']}|{'FINAL_AUTHOR_MANIFEST.json'}
ck(len(author_paths)==42,'all42 final author files')
for p in sorted(author_paths):ck(get(commits[-1],PREFIX+p)==get(HEAD,PREFIX+p),'actual42 final author anchor '+p)
rb=json.loads((D/'review/REMOTE_BINDING.json').read_bytes());ck(rb['head']==commits[-1] and rb['folder']==PREFIX.rstrip('/') and len(rb['files'])==42,'literal historical remote42 claim')
for row in rb['files']:
 raw=get(rb['head'],PREFIX+row['path']);ck(len(raw)==row['size'] and blob(raw)==row['git_blob_sha'] and raw==(D/row['path']).read_bytes(),'actual historical raw author blob '+row['path'])
ck(git('show','-s','--format=%P',HEAD).decode().strip().split()==[BASE,commits[-1]],'original head actual parent order')
review=json.loads((D/'review/REVIEW_MANIFEST.json').read_bytes());ck(review['author_manifest_sha256']==sha((D/'FINAL_AUTHOR_MANIFEST.json').read_bytes()),'historical review author manifest anchor')
review_paths={e['path'] for e in review['files']}|{'REVIEW_MANIFEST.json'}
for p in sorted(review_paths):
 r=subprocess.run(['git','cat-file','-e',commits[-1]+':'+PREFIX+'review/'+p],cwd=R,capture_output=True);ck(r.returncode!=0,'historical review absent actual author checkpoint '+p)
before=get(BASE,Q);lines=before.splitlines(keepends=True);matches=[i for i,l in enumerate(lines) if len(l.split(b'|'))>9 and l.split(b'|')[2].strip().split(b' / ')[0]==b'30004320']
ck(len(matches)==1,'unique actual original queue row');idx=matches[0];ck(idx+1==399,'actual physical original queue line399')
cells=lines[idx].split(b'|');ck([cells[j].strip() for j in [8,9]]==[b'queued',b'0/5'],'actual original queued0 cells');cells[8:10]=[b' unsolved ',b' 5/5 '];lines[idx]=b'|'.join(cells);ck(b''.join(lines)==get(HEAD,Q),'complete queue only own status and turns')
source_rows=[]
for name in ['SOURCE_MANIFEST.json','SOURCE_ADDITION_T1.json','SOURCE_ADDITION_T4.json','SOURCE_ADDITION_T5.json']:
 for e in json.loads((D/name).read_bytes())['files']:
  raw=(A/'raw_sources'/e['name']).read_bytes();ck(len(raw)==e['bytes'] and sha(raw)==e['sha256'],'fresh original exact primary '+e['name']);source_rows.append({**e,'pass':True})
ck(len(source_rows)==11 and len({e['name'] for e in source_rows})==11,'all11 unique fresh primary identities')
seal=json.loads((A/'ROOT_MATHEMATICAL_SEAL.json').read_bytes());ck(sha((A/seal['file']).read_bytes())==seal['sha256'] and len((A/seal['file']).read_bytes())==seal['bytes'],'root pre-code proof seal unchanged')
commands=[(f'author{i}',[str(PY),str(D/f'check_turn_{i}.py')],(D/f'TURN_{i}_CHECKS.json').read_bytes()) for i in range(1,6)]
commands += [('historical_review',[str(PY),str(D/'review/independent_checks.py')],(D/'review/INDEPENDENT_CHECKS.json').read_bytes())]
source_stdout=(D/'review/AUTHOR_REPLAY.json').read_bytes();no_source=json.loads(source_stdout);no_source.update(source_check='not requested; raw sources are not distributed',source_pdfs_checked=0);no_stdout=(json.dumps(no_source,indent=2,sort_keys=True)+'\n').encode()
review_stdout=b'PASS: review hashes, frozen author/remote binding, and independent replay\n'
end=b'PASS: all publication bytes, frozen author proofs and independent review; original unsolved 5/5\n'
commands += [('packet_with_sources',[str(PY),str(D/'verify_packet.py'),'--source-dir',str(A/'raw_sources')],source_stdout),('packet_without_sources',[str(PY),str(D/'verify_packet.py')],no_stdout),('review_wrapper',[str(PY),str(D/'review/verify_review.py'),'--author-dir',str(D)],review_stdout),('publication_with_sources',[str(PY),str(D/'verify_publication.py'),'--source-dir',str(A/'raw_sources')],source_stdout+review_stdout+end),('publication_without_sources',[str(PY),str(D/'verify_publication.py')],no_stdout+review_stdout+end)]
replays=[]
for label,args,expected_stdout in commands:
 r=subprocess.run(args,cwd=PRIVATE,capture_output=True);(STREAMS/(label+'.stdout')).write_bytes(r.stdout);(STREAMS/(label+'.stderr')).write_bytes(r.stderr)
 ck(r.returncode==0 and not r.stderr,'full replay exit '+label);ck(r.stdout==expected_stdout,'full byte-exact replay '+label)
 replays.append({'label':label,'exit':r.returncode,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr),'complete_output':r.stdout.decode()})
ck(sum(json.loads(r['complete_output'])['exact_assertions'] for r in replays[:5])==128694 and json.loads(replays[5]['complete_output'])['exact_assertions']==8664,'all author128694 and prior8664 assertions')
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','frozen_head':HEAD,'original_base':BASE,'check_count':len(checks),'checks':checks,'remote_files':remote_rows,'manifests':manifests,'nested_bindings':bindings,'nested_binding_instances':130,'actual_author_checkpoints':checkpoint_rows,'final_author_files':42,'review_files_plus_manifest':7,'historical_review_earlier_git_anchor_claimed':False,'primary_sources':source_rows,'replays':replays,'author_assertions':128694,'historical_review_assertions':8664,'root_math_sealed_utc':seal['sealed_utc'],'program_sha256':sha(Path(__file__).read_bytes()),'historical_all_refs_search_reproduced':False,'full_foundational_Giraud_classification_reproved':False}
(A/'root_original_reproduction_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','check_count','nested_binding_instances','final_author_files','author_assertions','historical_review_assertions']},indent=2))
