"""Fresh-main, sole-parent progress checkpoint; no local Git or PR writes."""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import base64,hashlib,json,subprocess

D=Path(__file__).resolve().parent
P=D.parents[2]
ROOT=P.parent
G=P/'next_selection_after_pr210_20261016'
OLD=P/'audits/pr210_5100033/initial_review_20261015'
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
BASE='repos/AlecKriebel/Math/'
OUT=D/'PROGRESS_15_CHECKPOINT_RECEIPT.json'
assert not OUT.exists()
prior=json.loads((OLD/'FINAL_COMPLETION_CHECKPOINT_PUBLICATION_RECEIPT.json').read_text())
prior_files={x['path']:x for x in prior['owned_files']}
assert prior['commit']=='1a702f8807e00af02d0eed244f0bc27df98f6079'
state=json.loads((D/'CURRENT_AUDIT_STATE.json').read_text())
assert state['completion_percent']==15 and state['preprint_preparation_cleared'] is False
assert state['counts']==[44,21,21,0]
T=D/'private_transport'/datetime.now(timezone.utc).strftime('progress15_%Y%m%dT%H%M%S%fZ')
T.mkdir(parents=True,exist_ok=False)
seq=0

def api(method,path,payload=None):
    global seq
    seq+=1
    args=[GH,'api','--method',method,BASE+path]
    if payload is not None:
        q=T/f'{seq:03d}-request.json'
        q.write_text(json.dumps(payload))
        args+=['--input',str(q)]
    run=subprocess.run(args,capture_output=True,timeout=60)
    (T/f'{seq:03d}-stdout.json').write_bytes(run.stdout)
    (T/f'{seq:03d}-stderr.txt').write_bytes(run.stderr)
    if run.returncode:raise RuntimeError('Native call failed; inspect recorded result before retry')
    return json.loads(run.stdout)

def current_claim():
    pr=api('GET','pulls/209')
    assert pr['state']=='open' and pr['draft'] and pr['head']['sha']=='fd09a95b479f376234835a4494693bb1316c85ec'
    q=api('GET','contents/unsolved_math_prioritization/QUEUE.md?ref='+pr['head']['sha'])
    body=base64.b64decode(q['content'])
    intake=json.loads((D/'INTAKE.json').read_text())
    assert q['sha']==intake['Queue_blob'] and hashlib.sha256(body).hexdigest()==intake['Queue_sha256']
    rows=[x for x in body.decode().splitlines() if '5100015 / AMR-050-0015' in x]
    assert rows==[intake['queue_row']] and [x.strip() for x in rows[0].split('|')][8]=='claimed_solved'

current_claim()
parent=api('GET','git/ref/heads/main')['object']['sha']
commit=api('GET','git/commits/'+parent)
cache={}

def lookup(path):
    sha=commit['tree']['sha']
    for part in path.split('/'):
        if sha not in cache:
            obj=api('GET','git/trees/'+sha)
            assert not obj['truncated']
            cache[sha]={x['path']:x for x in obj['tree']}
        row=cache[sha].get(part)
        if row is None:return None
        sha=row['sha']
    return sha

paths=[q for q in D.iterdir() if q.is_file() and q!=OUT]
for name in ['submitted','root_reproduction_01']:
    paths += [q for q in (D/name).rglob('*') if q.is_file()]
paths += [q for q in G.iterdir() if q.is_file()]
paths += [q for q in (G/'history').rglob('*') if q.is_file()]
families=[]
for name in ['source_domain_adversary_01','meromorphic_divisor_adversary_01']:
    folder=D/name
    manifest=folder/'AUTHORED_MANIFEST.json'
    obj=json.loads(manifest.read_text())
    paths.append(manifest)
    for row in obj['files']:
        q=folder/row['path']
        assert q.resolve().is_relative_to(folder.resolve()) and not q.is_symlink()
        raw=q.read_bytes()
        assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
        paths.append(q)
    families.append(dict(family=name,manifest_sha256=hashlib.sha256(manifest.read_bytes()).hexdigest(),root_final_acceptance_pending=True))
paths += [OLD/'FINAL_COMPLETION_CHECKPOINT_PUBLICATION_RECEIPT.json',OLD/'CURRENT_AUDIT_STATE.json',OLD/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md',P/'CURRENT_GOAL_SELECTION_20261013.json']
entries=[]
expected={}
pins=[]
for q in sorted(set(paths)):
    assert q.resolve().is_relative_to(P.resolve()) and not q.is_symlink()
    assert not any(x.startswith('private') or x=='__pycache__' for x in q.relative_to(P).parts)
    rel=q.relative_to(ROOT).as_posix()
    assert rel!='unsolved_math_prioritization/QUEUE.md'
    raw=q.read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    old=prior_files.get(rel)
    actual=lookup(rel)
    if old:assert actual==old['git_blob_sha1'],'Concurrent owned file change: '+rel
    else:assert actual in (None,blob),'Unexpected occupied owned path: '+rel
    pins.append(dict(path=rel,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),git_blob_sha1=blob))
    expected[rel]=raw
    entries.append(dict(path=rel,mode='100644',type='blob',content=raw.decode()))
assert len(entries)<250
for row in pins:
    assert hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()==row['sha256']
tree=api('POST','git/trees',dict(base_tree=commit['tree']['sha'],tree=entries))['sha']
new=api('POST','git/commits',dict(message='Checkpoint PR209 at15%: frozen source and exact verification replays, independent audits pending',tree=tree,parents=[parent]))['sha']
assert api('PATCH','git/refs/heads/main',dict(sha=new,force=False))['object']['sha']==new
actual=api('GET','git/commits/'+new)
assert [x['sha'] for x in actual['parents']]==[parent] and actual['tree']['sha']==tree
delta=api('GET','compare/'+parent+'...'+new)
assert delta['status']=='ahead' and delta['total_commits']==1 and len(delta['files'])<300
assert {x['filename'] for x in delta['files']}<=set(expected)
assert all(x['status']!='removed' for x in delta['files'])

def readback(item):
    rel,raw=item
    run=subprocess.run([GH,'api',BASE+'contents/'+rel+'?ref='+new],capture_output=True,timeout=60)
    assert run.returncode==0
    obj=json.loads(run.stdout)
    assert obj['sha']==hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    assert base64.b64decode(obj['content'])==raw
    return dict(path=rel,sha256=hashlib.sha256(raw).hexdigest(),actual_body_byte_identical=True)

with ThreadPoolExecutor(max_workers=6) as pool:
    verified=list(pool.map(readback,expected.items()))
for row in pins:
    assert hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()==row['sha256']
current_claim()
latest=api('GET','git/ref/heads/main')['object']['sha']
if latest!=new:assert api('GET','compare/'+new+'...'+latest)['status']=='ahead'
result=dict(utc=datetime.now(timezone.utc).isoformat(),commit=new,parent=parent,main_readback=latest,case_completion_percent=15,owned_files=pins,actual_native_byte_readbacks=verified,actual_changed_paths=[x['filename'] for x in delta['files']],fresh_main_sole_parent_verified=True,full_native_changed_path_scope_verified=True,native_PR_original_unchanged_and_still_claimed=True,retained_sealed_families=families,preprint_preparation_cleared=False,counts=[44,21,21,0],local_Git_index_ref_mutations=0,goal_active_incomplete=True)
OUT.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['owned_files','actual_native_byte_readbacks','actual_changed_paths']},indent=2))
