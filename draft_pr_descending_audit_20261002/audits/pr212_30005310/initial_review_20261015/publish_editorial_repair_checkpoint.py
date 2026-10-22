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


intake=json.loads((D/'INTAKE.json').read_text());pr=api('GET','pulls/212')
assert pr['state']=='open' and pr['draft'] and pr['head']['sha']==intake['head']
queue=api('GET','contents/'+intake['Queue_path']+'?ref='+intake['head'])
assert queue['sha']==intake['Queue_blob']
rows=[s for s in base64.b64decode(queue['content']).decode().splitlines() if '30005310 / OWR-11695865-009' in s]
assert len(rows)==1 and rows[0].split('|')[8].strip()=='claimed_solved'
assert all(x['semantic_exact_replay'] for x in json.loads((D/'ROOT_REPLAY_RECEIPT.json').read_text())['isolated_replays'])
paths=[p for p in D.iterdir() if p.is_file() and p.name!='EDITORIAL_REPAIR_CHECKPOINT_PUBLICATION_RECEIPT.json']
paths += [p for p in (D/'submitted').rglob('*') if p.is_file() and '__pycache__' not in p.parts]
paths += [p for p in (D/'root_reproduction').rglob('*') if p.is_file()]
for name in ['source_scope_adversary_01','elimination_dominance_adversary_01','likelihood_threshold_adversary_01']:
    review=D/name
    manifest=json.loads((review/'SAFE_AUTHORED_MANIFEST.json').read_text())
    manifest=manifest if isinstance(manifest,list) else manifest['safe_authored_files']
    for row in manifest:
        q=review/row['path'];raw=q.read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
        paths.append(q)
    paths.append(review/'SAFE_AUTHORED_MANIFEST.json')
paths += [q for q in (D/'root_fresh_replays').rglob('*') if q.is_file()]
for name in ['priority_classical_01','priority_author_update_01']:
    folder=D/name;manifest=json.loads((folder/'MANIFEST.json').read_text());paths.append(folder/'MANIFEST.json')
    for row in manifest['files']:
        q=folder/row.get('path',row.get('relative_path'));raw=q.read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'];paths.append(q)
    paths.append(folder/('SEAL.sha256' if name=='priority_classical_01' else 'FINAL_SEAL.json'))
for row in json.loads((D/'PROPOSED_CURRENT_PACKET_MANIFEST.json').read_text())['files']:
    q=D/'corrected_packet'/row['path'];assert hashlib.sha256(q.read_bytes()).hexdigest()==row['sha256'];paths.append(q)
paths += [q for q in (D/'root_priority_replays').rglob('*') if q.is_file()]
paths += [q for q in (D/'credit_packet_revision_history').rglob('*') if q.is_file()]
selection=P/'next_selection_after_pr214_20261015'
paths += [p for p in selection.iterdir() if p.is_file()]
paths += [P/'RESEARCH_LOG.md',P/'CURRENT_GOAL_SELECTION_20261013.json']
old=P/'audits/pr214_30005244/initial_review_20261015'
paths += [old/'COMPLETION_CHECKPOINT_PUBLICATION_RECEIPT.json']
entries=[];pins=[];expected={}
for path in sorted(set(paths)):
    assert path.resolve().is_relative_to(P.resolve()) and not path.is_symlink()
    assert not set(path.parts).intersection({'private_reading','private_transport','private_revision_history','private_upstream','private'})
    raw=path.read_bytes();rel=path.relative_to(ROOT).as_posix();expected[rel]=raw
    entries.append(dict(path=rel,mode='100644',type='blob',content=raw.decode()))
    pins.append(dict(path=rel,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
for attempt in range(4):
    parent=api('GET','git/ref/heads/main')['object']['sha']
    tree=api('GET','git/commits/'+parent)['tree']['sha']
    newtree=api('POST','git/trees',dict(base_tree=tree,tree=entries))['sha']
    commit=api('POST','git/commits',dict(message='Checkpoint PR212 at75%: restore equation reference and globally rebind credit packet before final review',tree=newtree,parents=[parent]))['sha']
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
pr=api('GET','pulls/212');assert pr['state']=='open' and pr['draft'] and pr['head']['sha']==intake['head']
result=dict(utc=datetime.now(timezone.utc).isoformat(),commit=commit,parent=parent,main_readback=main,
            owned_files=pins,actual_native_byte_readbacks=verified,case_completion_percent=75,
            original_PR_head_unchanged=intake['head'],prior_PR239_held_uncompleted=True,
            full_goal_active_incomplete=True,counts=[42,19,19,0],local_Git_or_index_mutations=0,
            entire_third_party_reading_copies_excluded=True,unfinished_new_reviewer_artifacts_excluded=True,
            manuscript_deposit_tracker_PR_comment_closure_or_merge=False,transport_receipts=str(T))
(D/'EDITORIAL_REPAIR_CHECKPOINT_PUBLICATION_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['owned_files','actual_native_byte_readbacks']},indent=2))
