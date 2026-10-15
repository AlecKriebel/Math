"""Publish a new owned-case checkpoint, reusing unchanged verified native blobs.

No local Git/index/ref mutations; no queue, PR, deposit or tracker writes.
Stop on uncertainty or unexpected changes to owned files.
"""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import argparse, base64, hashlib, json, subprocess

ROOT=Path('/Users/alec/Documents/Math'); D=Path(__file__).resolve().parent
P=D.parents[2]; R=D.parent/'preprint'
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'; B='repos/AlecKriebel/Math/'
parser=argparse.ArgumentParser();parser.add_argument('--percent',type=int,required=True)
parser.add_argument('--label',required=True);parser.add_argument('--receipt',required=True)
parser.add_argument('--baseline',required=True);parser.add_argument('--review',action='append',default=[])
a=parser.parse_args();out=D/a.receipt
assert not out.exists() and Path(a.receipt).name==a.receipt and a.percent==100
baseline=json.loads((D/a.baseline).read_text())
prior={x['path']:x for x in baseline['owned_files']}
T=D/'private_transport'/datetime.now(timezone.utc).strftime('checkpoint_%Y%m%dT%H%M%S%fZ')
T.mkdir(parents=True,exist_ok=False);seq=0

def api(method,path,payload=None):
    global seq
    seq+=1;cmd=[GH,'api','--method',method,B+path]
    if payload is not None:
        q=T/f'{seq:03d}-request.json';q.write_text(json.dumps(payload));cmd+=['--input',str(q)]
    run=subprocess.run(cmd,capture_output=True,timeout=60)
    (T/f'{seq:03d}-stdout.json').write_bytes(run.stdout);(T/f'{seq:03d}-stderr.txt').write_bytes(run.stderr)
    if run.returncode:raise RuntimeError('Native call failed; reconcile saved outcome before another mutation')
    return json.loads(run.stdout)

intake=json.loads((D/'INTAKE.json').read_text());pr=api('GET','pulls/211')
merged=json.loads((D.parent/'publication/PR_MERGED.json').read_text())
prepared=json.loads((D.parent/'publication/PR_PREPARED.json').read_text())
assert pr['state']=='closed' and pr['merged'] and pr['head']['sha']==merged['reviewed_head'] and pr['merge_commit_sha']==merged['merge_commit']
q=api('GET','contents/'+intake['Queue_path']+'?ref='+intake['head']);assert q['sha']==intake['Queue_blob']
rows=[s for s in base64.b64decode(q['content']).decode().splitlines() if '5100063 / AMR-050-0063' in s]
assert len(rows)==1 and rows[0].split('|')[8].strip()=='claimed_solved'
paths=[p for p in D.iterdir() if p.is_file() and p!=out]
for folder in ['submitted','root_reproduction']:
    paths += [p for p in (D/folder).rglob('*') if p.is_file() and not set(p.parts)&{'private','private_reading','private_transport','__pycache__'}]
families=['source_scope_adversary_01','geometry_algebra_adversary_01','meromorphic_divisor_adversary_01',
          'priority_author_updates_01','priority_classical_general_01']+a.review
for family in families:
    f=D/family
    manifests=[p for p in [f/'AUTHORED_MANIFEST.json',f/'MANIFEST.json',f/'SAFE_AUTHORED_MANIFEST.json'] if p.exists()]
    assert len(manifests)==1
    manifest=manifests[0];m=json.loads(manifest.read_text());paths.append(manifest)
    for row in m.get('files',m.get('entries')):
        if 'relative_path' in row:p=f/row['relative_path']
        else:
            p=f/row['path']
            if not p.exists():p=D/row['path']
        assert p.resolve().is_relative_to(f.resolve()) and not p.is_symlink()
        raw=p.read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
        paths.append(p)
for name in ['manuscript.tex','manuscript.pdf','metadata.json','README.md','RESEARCH_LOG.md','ARTIFACT_OPERATION_STARTED.json',
             'RENDER_QA.json','build_bundle.py','SOURCE_MANIFEST.json','PACKAGE_MANIFEST.json','deposit.json','k904a-source-verification.zip','REVIEW01_RESOLUTION.json','NATIVE_RELEASE_PLAN.json','apply_review01_fixes.py']:
    paths.append(R/name)
for folder in ['verification','pr_update','manuscript_reviews','history']:
    paths += [p for p in (R/folder).rglob('*') if p.is_file()]
if (R/'FINAL_CLEARANCE.json').exists():paths.append(R/'FINAL_CLEARANCE.json')
paths += [p for p in (D.parent/'publication').iterdir() if p.is_file()]
paths += [P/'RESEARCH_LOG.md',P/'CURRENT_GOAL_SELECTION_20261013.json']
F=D.parent/'publication/native_current_source'
paths += [p for p in F.rglob('*') if p.is_file()]

assert json.loads((D/'CURRENT_AUDIT_STATE.json').read_text())['completion_percent']==a.percent
parent=api('GET','git/ref/heads/main')['object']['sha'];commit=api('GET','git/commits/'+parent)
baseline_tree=api('GET','git/commits/'+baseline['commit'])['tree']['sha']
queue=api('GET','contents/unsolved_math_prioritization/QUEUE.md?ref='+parent)
current_queue=base64.b64decode(queue['content']).decode()
assert [x for x in current_queue.splitlines() if '5100063 / AMR-050-0063' in x]==[prepared['target_queue_row']]

cache={}
def lookup(path,root_tree=None):
    sha=root_tree or commit['tree']['sha']
    for part in path.split('/'):
        if sha not in cache:
            tree=api('GET','git/trees/'+sha);assert not tree['truncated'];cache[sha]={x['path']:x for x in tree['tree']}
        row=cache[sha].get(part)
        if row is None:return None
        sha=row['sha']
    return sha

pins=[];entries=[];expected={};carried=[]
for p in sorted(set(paths)):
    assert not p.is_symlink() and p.resolve().is_relative_to(P.resolve())
    assert not any(x.startswith('private') or x=='__pycache__' for x in p.relative_to(P).parts)
    raw=p.read_bytes()
    rel=('unsolved_math_prioritization/attempts/5100063/'+p.relative_to(F).as_posix()) if p.is_relative_to(F) else p.relative_to(ROOT).as_posix()
    assert rel!='unsolved_math_prioritization/QUEUE.md'
    digest=hashlib.sha256(raw).hexdigest()
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    current=lookup(rel);old=prior.get(rel)
    if old:
        oldblob=old.get('git_blob_sha1')
        if oldblob is None:
            # Earlier checkpoint receipts bind actual byte readbacks by SHA256;
            # traverse their immutable native tree to recover blob identities.
            oldblob=lookup(rel,baseline_tree)
        assert current==oldblob,'Unexpected owned-file change on fresh main: '+rel
    else:assert current in (None,blob),'Unexpected existing new owned path: '+rel
    pin=dict(path=rel,bytes=len(raw),sha256=digest,git_blob_sha1=blob);pins.append(pin)
    if current==blob:
        carried.append(dict(path=rel,native_blob_sha1=blob,fresh_native_tree_identity_verified=True));continue
    expected[rel]=raw
    try:entry=dict(path=rel,mode='100644',type='blob',content=raw.decode())
    except UnicodeDecodeError:
        assert api('POST','git/blobs',dict(content=base64.b64encode(raw).decode(),encoding='base64'))['sha']==blob
        entry=dict(path=rel,mode='100644',type='blob',sha=blob)
    entries.append(entry)
assert entries
tree=api('POST','git/trees',dict(base_tree=commit['tree']['sha'],tree=entries))['sha']
new=api('POST','git/commits',dict(message='Checkpoint PR211 at'+str(a.percent)+'%: '+a.label,tree=tree,parents=[parent]))['sha']
assert api('PATCH','git/refs/heads/main',dict(sha=new,force=False))['object']['sha']==new
def readback(item):
    path,raw=item
    run=subprocess.run([GH,'api',B+'contents/'+path+'?ref='+new],capture_output=True,timeout=60);assert run.returncode==0
    obj=json.loads(run.stdout);remote=base64.b64decode(obj['content']);assert remote==raw
    return dict(path=path,sha256=hashlib.sha256(raw).hexdigest(),byte_identical=True)
with ThreadPoolExecutor(max_workers=6) as pool:actual=list(pool.map(readback,expected.items()))
latest=api('GET','git/ref/heads/main')['object']['sha']
if latest!=new:assert api('GET','compare/'+new+'...'+latest)['status']=='ahead'
pr=api('GET','pulls/211')
assert pr['state']=='closed' and pr['merged'] and pr['head']['sha']==merged['reviewed_head'] and pr['merge_commit_sha']==merged['merge_commit']
receipt=dict(utc=datetime.now(timezone.utc).isoformat(),commit=new,parent=parent,main_readback=latest,
    owned_files=pins,actual_native_byte_readbacks=actual,unchanged_fresh_tree_identity_readbacks=carried,
    prior_actual_byte_readback_checkpoint=baseline['commit'],case_completion_percent=a.percent,
    counts=[43,20,20,0],local_Git_or_index_mutations=0,preprint_upload_cleared=json.loads((D/'CURRENT_AUDIT_STATE.json').read_text())['preprint_upload_cleared'],
    actual_publication_tracker_native_merge_complete=True,full_goal_active_incomplete=True)
out.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in ['owned_files','actual_native_byte_readbacks','unchanged_fresh_tree_identity_readbacks']},indent=2))
