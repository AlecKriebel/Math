"""Native main checkpoint of owned intake/reproduction; no local Git mutations."""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import base64
import hashlib
import json
import subprocess

ROOT=Path('/Users/alec/Documents/Math')
P=ROOT/'draft_pr_descending_audit_20261002'
D=Path(__file__).resolve().parent
T=D/'private_transport'/datetime.now(timezone.utc).strftime('checkpoint_%Y%m%dT%H%M%S%fZ')
T.mkdir(parents=True,exist_ok=False)
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh';BASE='repos/AlecKriebel/Math/';seq=0


def api(method,path,payload=None):
    global seq
    seq+=1;args=[GH,'api','--method',method,BASE+path]
    if payload is not None:
        target=T/f'{seq:02d}-request.json';target.write_text(json.dumps(payload));args+=['--input',str(target)]
    run=subprocess.run(args,capture_output=True,timeout=60)
    (T/f'{seq:02d}-stdout.json').write_bytes(run.stdout);(T/f'{seq:02d}-stderr.txt').write_bytes(run.stderr)
    if run.returncode:raise RuntimeError(f'Native call{seq} failed; inspect retained outcome before mutation retry')
    return json.loads(run.stdout)


intake=json.loads((D/'INTAKE.json').read_text());pr=api('GET','pulls/211')
assert pr['state']=='open' and pr['draft'] and pr['head']['sha']==intake['head']
queue=api('GET','contents/'+intake['Queue_path']+'?ref='+intake['head'])
assert queue['sha']==intake['Queue_blob']
rows=[s for s in base64.b64decode(queue['content']).decode().splitlines() if '5100063 / AMR-050-0063' in s]
assert len(rows)==1 and rows[0].split('|')[8].strip()=='claimed_solved'
assert json.loads((D/'ROOT_AUTHOR_REPLAY_ACCEPTANCE.json').read_text())['semantic_exact_replay']
paths=[p for p in D.iterdir() if p.is_file() and p.name!='PREPRINT_PREPARATION_CHECKPOINT_PUBLICATION_RECEIPT.json']
paths += [p for p in (D/'submitted').rglob('*') if p.is_file() and '__pycache__' not in p.parts]
paths += [p for p in (D/'root_reproduction').rglob('*') if p.is_file() and not set(p.parts).intersection({'private','private_reading','__pycache__'})]
for family in ['source_scope_adversary_01','geometry_algebra_adversary_01','meromorphic_divisor_adversary_01']:
    review=D/family
    manifest=json.loads((review/'AUTHORED_MANIFEST.json').read_text())
    for row in manifest.get('files',manifest.get('entries')):
        q=(review/row['relative_path']) if 'relative_path' in row else (D/row['path'])
        raw=q.read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
        paths.append(q)
    paths.append(review/'AUTHORED_MANIFEST.json')
for family,manifest_name in [('priority_author_updates_01','AUTHORED_MANIFEST.json'),('priority_classical_general_01','MANIFEST.json')]:
    review=D/family;manifest=json.loads((review/manifest_name).read_text())
    for row in manifest['files']:
        q=review/row['path'];raw=q.read_bytes()
        assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
        paths.append(q)
    paths.append(review/manifest_name)
assert json.loads((D/'ROOT_PRIORITY_ACCEPTANCE.json').read_text())['completion_percent']==55
assert json.loads((D/'ROOT_PRIORITY_ACCEPTANCE.json').read_text())['preprint_preparation_cleared']
R=D.parent/'preprint'
for name in ['manuscript.tex','manuscript.pdf','metadata.json','README.md','RESEARCH_LOG.md','ARTIFACT_OPERATION_STARTED.json','RENDER_QA.json','build_bundle.py','SOURCE_MANIFEST.json','PACKAGE_MANIFEST.json','deposit.json','k904a-source-verification.zip']:
    paths.append(R/name)
for folder in ['verification','pr_update','history/review01_frozen']:
    paths += [p for p in (R/folder).rglob('*') if p.is_file()]
paths += [p for p in (D.parent/'publication').iterdir() if p.is_file()]
assert json.loads((D/'CURRENT_AUDIT_STATE.json').read_text())['completion_percent']==60
assert not json.loads((D/'CURRENT_AUDIT_STATE.json').read_text())['preprint_upload_cleared']

selection=P/'next_selection_after_pr212_20261015'
paths += [p for p in selection.iterdir() if p.is_file()]
paths += [P/'RESEARCH_LOG.md',P/'CURRENT_GOAL_SELECTION_20261013.json']
old=P/'audits/pr212_30005310/initial_review_20261015'
paths += [old/'FINAL_DISPOSITION_PUBLICATION_RECEIPT.json']
entries=[];pins=[];expected={}
for path in sorted(set(paths)):
    assert path.resolve().is_relative_to(P.resolve()) and not path.is_symlink()
    assert not set(path.parts).intersection({'private_reading','private_transport','private_revision_history','private_upstream','private'})
    raw=path.read_bytes();rel=path.relative_to(ROOT).as_posix();expected[rel]=raw
    try: entries.append(dict(path=rel,mode='100644',type='blob',content=raw.decode()))
    except UnicodeDecodeError:
        blob=api('POST','git/blobs',dict(content=base64.b64encode(raw).decode(),encoding='base64'))['sha']
        assert blob==hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        entries.append(dict(path=rel,mode='100644',type='blob',sha=blob))
    pins.append(dict(path=rel,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
for attempt in range(4):
    parent=api('GET','git/ref/heads/main')['object']['sha']
    tree=api('GET','git/commits/'+parent)['tree']['sha']
    newtree=api('POST','git/trees',dict(base_tree=tree,tree=entries))['sha']
    commit=api('POST','git/commits',dict(message='Checkpoint PR211 at60%: freeze six-page note, portable ten-job package and first fresh manuscript review inputs',tree=newtree,parents=[parent]))['sha']
    try:
        assert api('PATCH','git/refs/heads/main',dict(sha=commit,force=False))['object']['sha']==commit
        break
    except RuntimeError:
        error=json.loads((T/f'{seq:02d}-stdout.json').read_text());latest=api('GET','git/ref/heads/main')['object']['sha']
        if str(error.get('status'))!='422' or latest==parent or attempt==3:raise


def readback(row):
    run=subprocess.run([GH,'api',BASE+'contents/'+row['path']+'?ref='+commit],capture_output=True,timeout=60)
    assert run.returncode==0
    raw=base64.b64decode(json.loads(run.stdout)['content']);assert raw==expected[row['path']]
    return dict(path=row['path'],sha256=hashlib.sha256(raw).hexdigest(),byte_identical=True)


with ThreadPoolExecutor(max_workers=6) as pool:verified=list(pool.map(readback,pins))
main=api('GET','git/ref/heads/main')['object']['sha']
if main!=commit:assert api('GET','compare/'+commit+'...'+main)['status']=='ahead'
pr=api('GET','pulls/211');assert pr['state']=='open' and pr['draft'] and pr['head']['sha']==intake['head']
result=dict(utc=datetime.now(timezone.utc).isoformat(),commit=commit,parent=parent,main_readback=main,
            owned_files=pins,actual_native_byte_readbacks=verified,case_completion_percent=60,
            original_PR_head_unchanged=intake['head'],prior_PR239_held_uncompleted=True,
            full_goal_active_incomplete=True,counts=[42,19,19,0],local_Git_or_index_mutations=0,
            entire_third_party_reading_copies_excluded=True,unfinished_new_reviewer_artifacts_excluded=True,
            manuscript_prepared_not_released=True,deposit_tracker_PR_comment_closure_or_merge=False,transport_receipts=str(T))
(D/'PREPRINT_PREPARATION_CHECKPOINT_PUBLICATION_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['owned_files','actual_native_byte_readbacks']},indent=2))
