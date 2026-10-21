"""Rebase a known rejected research checkpoint; retain concurrent main; no PR release."""
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
T=D/'private_transport'/datetime.now(timezone.utc).strftime('progress65review02rebase_%Y%m%dT%H%M%S%fZ');T.mkdir()
seq=0
def sha(raw):return hashlib.sha256(raw).hexdigest()
def blob(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def write(p,raw):
 with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
def api(method,path,payload=None):
 global seq
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
 raw=(ROOT/path).read_bytes();assert e['mode']=='100644' and e['type']=='blob'
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
for p in [Path(__file__),D/'ROOT_RELEASE_HELPER_REPAIR02_SOURCE_FREEZE.json']:
 expected[p.relative_to(ROOT).as_posix()]=p.read_bytes()
parent=api('GET','git/ref/heads/main')['object']['sha'];main=api('GET','git/commits/'+parent)
newentries=[]
for path,raw in expected.items():
 old=at(oldparent['tree']['sha'],path);fresh=at(main['tree']['sha'],path);want=dict(mode='100644',type='blob',sha=blob(raw))
 assert fresh in (old,want),'Concurrent owned-file change: '+path
 if fresh!=want:
  if path in {str(Path(__file__).relative_to(ROOT)),str((D/'ROOT_RELEASE_HELPER_REPAIR02_SOURCE_FREEZE.json').relative_to(ROOT))}:newentries.append(dict(path=path,mode='100644',type='blob',content=raw.decode()))
  else:newentries.append(dict(path=path,mode='100644',type='blob',sha=want['sha']))
for path,raw in expected.items():assert (ROOT/path).read_bytes()==raw
tree=api('POST','git/trees',dict(base_tree=main['tree']['sha'],tree=newentries))['sha']
changes=delta(main['tree']['sha'],tree);assert {r['path'] for r in changes}=={r['path'] for r in newentries}
for r in changes:assert r['new']==dict(mode='100644',type='blob',sha=blob(expected[r['path']]))
new=api('POST','git/commits',dict(message='Checkpoint PR209 at65%: sealed second release audit and reproduced defects; publication held',tree=tree,parents=[parent]))['sha']
write(T/'MAIN_UPDATE_INTENT.json',(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),parent=parent,target=new,tree=tree,force=False,known_prior_rejected_commit=known['sha'],counts=[44,21,21,0],case_completion_percent=65),indent=2)+'\n').encode())
assert api('PATCH','git/refs/heads/main',dict(sha=new,force=False))['object']['sha']==new
actual=api('GET','git/commits/'+new);assert [r['sha'] for r in actual['parents']]==[parent] and actual['tree']['sha']==tree
def verify(item):
 path,raw=item
 p=subprocess.run([GH,'api',BASE+'git/blobs/'+blob(raw)],capture_output=True,timeout=90);assert p.returncode==0
 x=json.loads(p.stdout);assert x['sha']==blob(raw) and x.get('encoding')=='base64' and base64.b64decode(x['content'])==raw
 assert at(tree,path)==dict(mode='100644',type='blob',sha=blob(raw))
 return dict(path=path,sha256=sha(raw),actual_body_byte_identical=True)
# Populate tree cache first; no concurrent mutation of API sequence/caches.
for path in expected:assert at(tree,path)['sha']==blob(expected[path])
with ThreadPoolExecutor(max_workers=6) as pool:verified=list(pool.map(verify,expected.items()))
for path,raw in expected.items():assert (ROOT/path).read_bytes()==raw
claim();latest=api('GET','git/ref/heads/main')['object']['sha']
if latest!=new:
 a=api('GET','compare/'+new+'...'+latest);assert a['status']=='ahead' and a['merge_base_commit']['sha']==new
pins=[dict(path=p,bytes=len(b),sha256=sha(b),git_blob_sha1=blob(b)) for p,b in sorted(expected.items())]
r=dict(utc=datetime.now(timezone.utc).isoformat(),commit=new,parent=parent,main_readback=latest,case_completion_percent=65,owned_files=pins,actual_native_byte_readbacks=verified,actual_changed_paths=[x['path'] for x in changes],fresh_main_sole_parent_verified=True,full_native_changed_path_scope_verified=True,native_PR_original_unchanged_and_still_claimed=True,preprint_preparation_cleared=True,preprint_upload_cleared=False,counts=[44,21,21,0],local_Git_index_ref_mutations=0,goal_active_incomplete=True,known_rejected_attempt=known['sha'],source_packet_rebased_without_reuploading_binary_blobs=True)
write(OUT,(json.dumps(r,indent=2)+'\n').encode());print(json.dumps({k:v for k,v in r.items() if k not in ['owned_files','actual_native_byte_readbacks','actual_changed_paths']},indent=2))
