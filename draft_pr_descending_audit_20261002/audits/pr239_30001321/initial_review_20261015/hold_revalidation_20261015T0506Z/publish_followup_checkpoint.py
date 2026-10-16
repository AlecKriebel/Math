"""Push only this owned source-review follow-up on fresh native main."""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import base64
import hashlib
import json
import subprocess

ROOT=Path('/Users/alec/Documents/Math')
P=ROOT/'draft_pr_descending_audit_20261002'
H=Path(__file__).resolve().parent
D=H.parent
OUT=H/'checkpoint_transport'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
OUT.mkdir(parents=True,exist_ok=False)
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
BASE='repos/AlecKriebel/Math/'
seq=0


def api(method,path,payload=None):
    global seq
    seq+=1
    args=[GH,'api','--method',method,BASE+path]
    if payload is not None:
        request=OUT/f'{seq:02d}-request.json'
        request.write_text(json.dumps(payload))
        args+=['--input',str(request)]
    run=subprocess.run(args,capture_output=True,timeout=60)
    (OUT/f'{seq:02d}-stdout.json').write_bytes(run.stdout)
    (OUT/f'{seq:02d}-stderr.txt').write_bytes(run.stderr)
    if run.returncode:
        raise RuntimeError(f'Native call{seq} failed; inspect retained outcome before retry')
    return json.loads(run.stdout)


head='7f17eef77c52b2d9b2ec3ad0803c016267fa6496'
pr=api('GET','pulls/239')
assert pr['state']=='open' and pr['draft'] and pr['head']['sha']==head
assert json.loads((D/'CURRENT_AUDIT_STATE.json').read_text())['QUEUE_status']=='claimed_solved'
validation=json.loads((H/'ROOT_FOLLOWUP_VALIDATION.json').read_text())
assert validation['status']=='PASS'
paths=[p for p in H.iterdir() if p.is_file() and p.name!='FOLLOWUP_PUBLICATION_RECEIPT.json']
A=H/'thesis_source_adversary_01'
manifest=json.loads((A/'checks_manifest.json').read_text())
assert hashlib.sha256((A/'checks_manifest.json').read_bytes()).hexdigest()==validation['current_adversary_manifest_sha256']
paths.append(A/'checks_manifest.json')
for row in manifest['artifacts']:
    path=Path(row['path'])
    assert path.resolve().is_relative_to(A.resolve())
    raw=path.read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
    paths.append(path)
paths += [D/name for name in ['CURRENT_AUDIT_STATE.json','RESEARCH_LOG.md','ROOT_SOURCE_HOLD_NATIVE_READBACK.json','verify_native_source_hold_checkpoint.py']]
paths += [P/'RESEARCH_LOG.md',P/'CURRENT_GOAL_SELECTION_20261013.json']
entries=[]
pins=[]
expected={}
for path in sorted(set(paths)):
    assert path.resolve().is_relative_to(P.resolve()) and not path.is_symlink()
    assert not set(path.parts).intersection({'private_reading','private_revision_history','checkpoint_transport'})
    raw=path.read_bytes()
    rel=path.relative_to(ROOT).as_posix()
    expected[rel]=raw
    entries.append(dict(path=rel,mode='100644',type='blob',content=raw.decode()))
    pins.append(dict(path=rel,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
for attempt in range(4):
    parent=api('GET','git/ref/heads/main')['object']['sha']
    base_tree=api('GET','git/commits/'+parent)['tree']['sha']
    tree=api('POST','git/trees',dict(base_tree=base_tree,tree=entries))['sha']
    commit=api('POST','git/commits',dict(message='Checkpoint PR239 new institutional source audit; original-source priority hold retained',tree=tree,parents=[parent]))['sha']
    try:
        assert api('PATCH','git/refs/heads/main',dict(sha=commit,force=False))['object']['sha']==commit
        break
    except RuntimeError:
        rejection=json.loads((OUT/f'{seq:02d}-stdout.json').read_text())
        latest=api('GET','git/ref/heads/main')['object']['sha']
        if str(rejection.get('status'))!='422' or latest==parent or attempt==3:raise


def readback(row):
    run=subprocess.run([GH,'api',BASE+'contents/'+row['path']+'?ref='+commit],capture_output=True,timeout=60)
    assert run.returncode==0
    remote=base64.b64decode(json.loads(run.stdout)['content'])
    assert remote==expected[row['path']]
    return dict(path=row['path'],sha256=hashlib.sha256(remote).hexdigest(),byte_identical=True)


with ThreadPoolExecutor(max_workers=6) as pool:verified=list(pool.map(readback,pins))
main=api('GET','git/ref/heads/main')['object']['sha']
if main!=commit:assert api('GET','compare/'+commit+'...'+main)['status']=='ahead'
pr=api('GET','pulls/239')
assert pr['state']=='open' and pr['draft'] and pr['head']['sha']==head
result=dict(utc=datetime.now(timezone.utc).isoformat(),commit=commit,parent=parent,
            native_main_readback=main,owned_files=pins,actual_native_byte_readbacks=verified,
            original_PR_head_unchanged=head,case_completion_percent=60,
            goal_active_incomplete=True,consecutive_turns_same_material_source_hold=2,
            no_local_Git_or_index_changes=True,whole_source_and_raw_account_metadata_excluded=True,
            new_preprint_deposit_tracker_row_comment_close_or_merge=False,transport_receipts=str(OUT))
(H/'FOLLOWUP_PUBLICATION_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['owned_files','actual_native_byte_readbacks']},indent=2))
