"""Read-only body recovery for the already-pushed b109 research checkpoint; every native mutation forbidden."""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,subprocess,base64,gzip,os
D=Path(__file__).resolve().parent;ROOT=D.parents[2].parent;C=D.parent
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh';BASE='repos/AlecKriebel/Math/'
OLD=D/'private_transport/progress65review02retry03_20261016T071007496784Z'
# Resolve the unique terminated attempt from its exact rejected commit evidence.
matches=[]
for p in (D/'private_transport').glob('progress65review02retry03_*'):
 f=p/'204-stdout.json'
 if f.exists() and json.loads(f.read_bytes()).get('sha')=='b21565368ea732b4f61038a1a8d7913c1c774edb':matches.append(p)
assert len(matches)==1;OLD=matches[0]
rejected=json.loads((OLD/'205-stdout.json').read_bytes());assert rejected.get('status')=='422' and rejected.get('message')=='Update is not a fast forward'
OUT=D/'PROGRESS_65_REVIEW02_CHECKPOINT_RECEIPT.json';assert not OUT.exists()
T=D/'private_transport'/datetime.now(timezone.utc).strftime('progress65review02readonlyretry02_%Y%m%dT%H%M%S%fZ');T.mkdir()
seq=0
def sha(raw):return hashlib.sha256(raw).hexdigest()
def blob(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def write(p,raw):
 with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
def api(method,path,payload=None):
 global seq
 assert method=='GET','READONLY RECOVERY forbids every native write'
 seq+=1;n=seq;args=[GH,'api','--method',method,BASE+path];raw=None
 if payload is not None:
  raw=json.dumps(payload).encode();packed=gzip.compress(raw,mtime=0);write(T/f'{n:04d}-request.json.gz',packed);assert gzip.decompress(packed)==raw;args+=['--input','-']
 r=subprocess.run(args,input=raw,capture_output=True,timeout=90)
 write(T/f'{n:04d}-stdout.json',r.stdout);write(T/f'{n:04d}-stderr.txt',r.stderr)
 if r.returncode:raise RuntimeError('Retained native response requires inspection; no automatic write retry')
 return json.loads(r.stdout)
def claim():
 p=api('GET','pulls/209');assert p['state']=='open' and p['draft'] and p['head']['sha']=='fd09a95b479f376234835a4494693bb1316c85ec'
 q=api('GET','contents/unsolved_math_prioritization/QUEUE.md?ref='+p['head']['sha']);b=base64.b64decode(q['content']);i=json.loads((D/'INTAKE.json').read_bytes())
 assert q['sha']==i['Queue_blob'] and sha(b)==i['Queue_sha256'] and i['queue_row'] in b.decode().splitlines() and i['queue_row'].split('|')[8].strip()=='claimed_solved'
cache={}
def rows(tree):
 if tree not in cache:
  x=api('GET','git/trees/'+tree);assert x.get('truncated') is False;cache[tree]={r['path']:{k:r[k] for k in ['mode','type','sha']} for r in x['tree']}
 return cache[tree]
def at(tree,path):
 for p in path.split('/'):
  x=rows(tree).get(p)
  if x is None:return None
  tree=x['sha']
 return x
def delta(a,b,prefix=''):
 if a==b:return []
 left=rows(a) if a else {};right=rows(b) if b else {};out=[]
 for n in sorted(set(left)|set(right)):
  x,y=left.get(n),right.get(n)
  if x==y:continue
  if (x is None or x['type']=='tree') and (y is None or y['type']=='tree'):out+=delta(x['sha'] if x else None,y['sha'] if y else None,prefix+n+'/')
  else:out.append(dict(path=prefix+n,old=x,new=y))
 return out
requests=[]
for p in OLD.glob('*request.json*'):
 if p.suffix not in ['.gz','.json']:continue
 try:x=json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes())
 except:continue
 if type(x) is dict and 'base_tree'in x and type(x.get('tree')) is list:requests.append((p,x))
assert len(requests)==1;tree_request=requests[0][1];entries=tree_request['tree'];expected={}
scope='draft_pr_descending_audit_20261002/'
for e in entries:
 path=e['path'];assert path.startswith(scope) and not any(p.startswith('private') or p=='__pycache__' for p in path.split('/'))
 raw=e['content'].encode() if e.get('content') is not None else (ROOT/path).read_bytes();assert e['mode']=='100644' and e['type']=='blob'
 assert (e.get('content') is not None and e['content'].encode()==raw) or e.get('sha')==blob(raw)
 expected[path]=raw
assert len(entries)==len(expected)
claim();known=api('GET','git/commits/b21565368ea732b4f61038a1a8d7913c1c774edb')
assert len(known['parents'])==1;oldparent=api('GET','git/commits/'+known['parents'][0]['sha'])
assert oldparent['tree']['sha']==tree_request['base_tree']
old_delta=delta(oldparent['tree']['sha'],known['tree']['sha'])
assert all(r['new']==dict(mode='100644',type='blob',sha=blob(expected[r['path']])) for r in old_delta)
for path,raw in expected.items():assert at(known['tree']['sha'],path)==dict(mode='100644',type='blob',sha=blob(raw))
# Publish the recovery source and coordinated implementation-freeze record too.
for p in [D/'publish_progress_65_review02_rebase02.py',D/'ROOT_RELEASE_HELPER_REPAIR02_SOURCE_FREEZE.json']:
 expected[p.relative_to(ROOT).as_posix()]=p.read_bytes()
target='b109028ff024f7b4df8cbc684c4773a4dd300ae0'
actual=api('GET','git/commits/'+target)
parent=actual['parents'][0]['sha'];assert [x['sha'] for x in actual['parents']]==['0c0ef219dd5aa4547ad7ee47ac1ab5b08ca232f0']
base=api('GET','git/commits/'+parent);tree=actual['tree']['sha']
changes=delta(base['tree']['sha'],tree);assert all(x['new']==dict(mode='100644',type='blob',sha=blob(expected[x['path']])) for x in changes)
for path,raw in expected.items():assert at(tree,path)==dict(mode='100644',type='blob',sha=blob(raw))
prior=json.loads((D/'PROGRESS_65_CHECKPOINT_RECEIPT.json').read_bytes())
oldpins={x['path']:x for x in prior['owned_files']}
oldreads={x['path']:x for x in prior['actual_native_byte_readbacks']}
inherited=[];fresh=[]
for path,raw in expected.items():
 p=oldpins.get(path);v=oldreads.get(path)
 if p and v and p['git_blob_sha1']==blob(raw) and p['sha256']==sha(raw) and p['bytes']==len(raw) and v['sha256']==sha(raw) and v['actual_body_byte_identical']:
  inherited.append(dict(path=path,sha256=sha(raw),actual_body_byte_identical=True,body_readback_inherited_from_unchanged_git_blob=prior['commit'],current_native_tree_identity_rechecked=True))
 else:fresh.append((path,raw))
def verify(item):
 path,raw=item;key=sha(path.encode())[:20]
 for attempt in range(3):
  p=subprocess.run([GH,'api',BASE+'git/blobs/'+blob(raw)],capture_output=True,timeout=90)
  if p.returncode:
   write(T/(key+'-'+str(attempt)+'-FAILED.stdout'),p.stdout);write(T/(key+'-'+str(attempt)+'-FAILED.stderr'),p.stderr)
   if attempt<2:continue
   raise RuntimeError('Read-only body GET failed after3 retained attempts')
  x=json.loads(p.stdout);assert x['sha']==blob(raw) and x.get('encoding')=='base64' and base64.b64decode(x['content'])==raw
  result=dict(path=path,sha256=sha(raw),actual_body_byte_identical=True,fresh_body_GET=True,git_blob_sha1=blob(raw))
  write(T/(key+'-VERIFIED.json'),(json.dumps(result,indent=2)+'\n').encode());return result
with ThreadPoolExecutor(max_workers=3) as pool:verified=list(pool.map(verify,fresh))
assert all(at(tree,path)==dict(mode='100644',type='blob',sha=blob(raw)) for path,raw in expected.items())
claim();latest=api('GET','git/ref/heads/main')['object']['sha']
if latest!=target:
 a=api('GET','compare/'+target+'...'+latest);assert a['status']=='ahead' and a['merge_base_commit']['sha']==target
pins=[dict(path=p,bytes=len(b),sha256=sha(b),git_blob_sha1=blob(b)) for p,b in sorted(expected.items())]
r=dict(utc=datetime.now(timezone.utc).isoformat(),commit=target,parent=parent,main_readback=latest,case_completion_percent=65,owned_files=pins,actual_native_byte_readbacks=verified+inherited,actual_changed_paths=[x['path'] for x in changes],fresh_main_sole_parent_verified=True,full_native_changed_path_scope_verified=True,native_PR_original_unchanged_and_still_claimed=True,preprint_preparation_cleared=True,preprint_upload_cleared=False,counts=[44,21,21,0],local_Git_index_ref_mutations=0,goal_active_incomplete=True,fresh_actual_native_body_GETs=len(verified),inherited_authenticated_same_blob_readbacks=len(inherited),all_current_native_tree_body_identities_rechecked=len(pins),postpush_recovery='READONLY ONLY; initial threaded body GET returnednonzero with unavailable rawfailurestreams; no body mismatch inferred, fresh reads retained failures before boundedreadretry',known_rejected_attempt='b21565368ea732b4f61038a1a8d7913c1c774edb')
write(OUT,(json.dumps(r,indent=2)+'\n').encode())
print(json.dumps({k:v for k,v in r.items() if k not in ['owned_files','actual_native_byte_readbacks','actual_changed_paths']},indent=2))
