"""After actual PR210 merge, publish factual completion with fresh native main.

No local Git, Queue, PR, DOI or spreadsheet mutations. Fail on concurrent owned
file changes; preserve unrelated main work through a sole-parent base-tree delta.
"""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import base64,hashlib,json,subprocess
ROOT=Path('/Users/alec/Documents/Math');D=Path(__file__).resolve().parent
P=D.parents[2];R=D.parent/'preprint';PUB=D.parent/'publication'
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh';BASE='repos/AlecKriebel/Math/'
out=D/'FINAL_COMPLETION_CHECKPOINT_PUBLICATION_RECEIPT.json'
assert not out.exists()
merged=json.loads((PUB/'PR_MERGED.json').read_text())
prepared=json.loads((PUB/'PR_PREPARED.json').read_text())
state=json.loads((D/'CURRENT_AUDIT_STATE.json').read_text())
assert merged['merged'] is True and state['completion_percent']==100
assert merged['program_counts']==state['counts']==[44,21,21,0]
baseline_name='NATIVE_GUARD_REPAIR_CHECKPOINT_PUBLICATION_RECEIPT.json' if (D/'NATIVE_GUARD_REPAIR_CHECKPOINT_PUBLICATION_RECEIPT.json').exists() else 'FINAL_CLEARANCE_CHECKPOINT_PUBLICATION_RECEIPT.json'
prior_checkpoint=json.loads((D/baseline_name).read_text())
prior={x['path']:x for x in prior_checkpoint['owned_files']}
prior.update({x['path']:x for x in prepared['included_owned_pins']})
T=D/'private_transport'/datetime.now(timezone.utc).strftime('final_checkpoint_%Y%m%dT%H%M%S%fZ')
T.mkdir(parents=True,exist_ok=False);seq=0
def api(method,path,payload=None):
    global seq
    seq+=1;args=[GH,'api','--method',method,BASE+path]
    if payload is not None:
        q=T/f'{seq:03d}-request.json';q.write_text(json.dumps(payload));args+=['--input',str(q)]
    run=subprocess.run(args,capture_output=True,timeout=60)
    (T/f'{seq:03d}-stdout.json').write_bytes(run.stdout)
    (T/f'{seq:03d}-stderr.txt').write_bytes(run.stderr)
    if run.returncode:raise RuntimeError('Native call failed; inspect saved outcome before retry')
    return json.loads(run.stdout)

pr=api('GET','pulls/210')
assert pr['merged'] and pr['state']=='closed' and pr['head']['sha']==merged['reviewed_head']
assert pr['merge_commit_sha']==merged['merge_commit']
parent=api('GET','git/ref/heads/main')['object']['sha']
commit=api('GET','git/commits/'+parent)
queue=api('GET','contents/unsolved_math_prioritization/QUEUE.md?ref='+parent)
target=[x for x in base64.b64decode(queue['content']).decode().splitlines() if '5100033 / AMR-050-0033' in x]
assert target==[prepared['target_queue_row']]
baseline_tree=api('GET','git/commits/'+prior_checkpoint['commit'])['tree']['sha']
cache={}
def lookup(path,tree=None):
    sha=tree or commit['tree']['sha']
    for part in path.split('/'):
        if sha not in cache:
            obj=api('GET','git/trees/'+sha);assert not obj['truncated']
            cache[sha]={x['path']:x for x in obj['tree']}
        row=cache[sha].get(part)
        if row is None:return None
        sha=row['sha']
    return sha

paths=[q for q in D.iterdir() if q.is_file() and q!=out]
for name in ['submitted','root_reproduction','history']:
    paths += [q for q in (D/name).rglob('*') if q.is_file() and not any(x.startswith('private') or x=='__pycache__' for x in q.relative_to(D).parts)]
families=['source_domain_adversary_01','physical_geometry_adversary_01','meromorphic_divisor_adversary_01',
    'priority_author_updates_01','priority_classical_general_01','whole_manuscript_adversary_01',
    'whole_manuscript_adversary_02','whole_manuscript_adversary_03','release_helpers_adversary_01',
    'release_helpers_adversary_02','release_helpers_adversary_03','release_helpers_adversary_04','release_helpers_adversary_05']
for family in families:
    folder=D/family;manifest=folder/'AUTHORED_MANIFEST.json';obj=json.loads(manifest.read_text());paths.append(manifest)
    for row in obj.get('files',obj.get('authored_files',obj.get('entries',[]))):
        q=folder/row.get('path',row.get('relative_path'))
        assert q.resolve().is_relative_to(folder.resolve()) and not q.is_symlink()
        raw=q.read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
        paths.append(q)
paths += [q for q in R.iterdir() if q.is_file() and q.suffix not in {'.log','.aux','.out'}]
for folder in ['verification','pr_update','history']:
    paths += [q for q in (R/folder).rglob('*') if q.is_file()]
paths += [q for q in PUB.iterdir() if q.is_file()]
paths += [P/'RESEARCH_LOG.md',P/'CURRENT_GOAL_SELECTION_20261013.json']
F=PUB/'native_current_source'
paths += [q for q in F.rglob('*') if q.is_file()]
entries=[];pins=[];expected={};carried=[]
for q in sorted(set(paths)):
    assert q.resolve().is_relative_to(P.resolve()) and not q.is_symlink()
    assert not any(x.startswith('private') or x=='__pycache__' for x in q.relative_to(P).parts)
    rel='unsolved_math_prioritization/attempts/5100033/'+q.relative_to(F).as_posix() if q.is_relative_to(F) else q.relative_to(ROOT).as_posix()
    assert rel!='unsolved_math_prioritization/QUEUE.md'
    raw=q.read_bytes();digest=hashlib.sha256(raw).hexdigest()
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    actual=lookup(rel);old=prior.get(rel)
    if old:
        oldblob=old.get('git_blob_sha1') or lookup(rel,baseline_tree)
        assert actual==oldblob,'Unexpected owned main change: '+rel
    else:assert actual in (None,blob),'Unexpected new owned path: '+rel
    pins.append(dict(path=rel,bytes=len(raw),sha256=digest,git_blob_sha1=blob))
    if actual==blob:
        carried.append(dict(path=rel,native_blob_sha1=blob,fresh_native_tree_identity_verified=True));continue
    expected[rel]=raw
    try:entry=dict(path=rel,mode='100644',type='blob',content=raw.decode())
    except UnicodeDecodeError:
        assert api('POST','git/blobs',dict(content=base64.b64encode(raw).decode(),encoding='base64'))['sha']==blob
        entry=dict(path=rel,mode='100644',type='blob',sha=blob)
    entries.append(entry)
assert entries
tree=api('POST','git/trees',dict(base_tree=commit['tree']['sha'],tree=entries))['sha']
new=api('POST','git/commits',dict(message='Checkpoint PR210 at100%: exact preprint, single tracker row and reviewed native merge verified',tree=tree,parents=[parent]))['sha']
assert api('PATCH','git/refs/heads/main',dict(sha=new,force=False))['object']['sha']==new
actual_commit=api('GET','git/commits/'+new)
assert [x['sha'] for x in actual_commit['parents']]==[parent] and actual_commit['tree']['sha']==tree
delta=api('GET','compare/'+parent+'...'+new)
assert delta['status']=='ahead' and delta['total_commits']==1 and len(delta['files'])<300
assert {x['filename'] for x in delta['files']}<=set(expected) and all(x['status']!='removed' for x in delta['files'])
def readback(item):
    path,raw=item;run=subprocess.run([GH,'api',BASE+'contents/'+path+'?ref='+new],capture_output=True,timeout=60)
    assert run.returncode==0 and base64.b64decode(json.loads(run.stdout)['content'])==raw
    return dict(path=path,sha256=hashlib.sha256(raw).hexdigest(),byte_identical=True)
with ThreadPoolExecutor(max_workers=6) as pool:verified=list(pool.map(readback,expected.items()))
latest=api('GET','git/ref/heads/main')['object']['sha']
if latest!=new:assert api('GET','compare/'+new+'...'+latest)['status']=='ahead'
pr=api('GET','pulls/210')
assert pr['merged'] and pr['state']=='closed' and pr['merge_commit_sha']==merged['merge_commit'] and pr['head']['sha']==merged['reviewed_head']
result=dict(utc=datetime.now(timezone.utc).isoformat(),commit=new,parent=parent,main_readback=latest,
    owned_files=pins,actual_native_byte_readbacks=verified,unchanged_fresh_tree_identity_readbacks=carried,
    prior_actual_byte_readback_checkpoint=prior_checkpoint['commit'],case_completion_percent=100,
    actual_native_sole_parent_verified=True,full_native_changed_path_scope_verified=True,
    actual_changed_paths=[x['filename'] for x in delta['files']],counts=[44,21,21,0],
    actual_publication_tracker_native_merge_complete=True,doi_url=merged['doi_url'],tracker_range=merged['tracker_range'],
    actual_PR_merge_commit=merged['merge_commit'],local_Git_or_index_mutations=0,full_goal_active_incomplete=True)
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['owned_files','actual_native_byte_readbacks','unchanged_fresh_tree_identity_readbacks','actual_changed_paths']},indent=2))
