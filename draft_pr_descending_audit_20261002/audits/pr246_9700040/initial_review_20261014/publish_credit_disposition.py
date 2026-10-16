"""Publish the completed eligible-intake disposition and one owned main queue row.

This is bookkeeping for the already authorized correction, not a new review of
a non-claimed-solved PR. No shared checkout/index changes or PR merge/comment.
"""
from pathlib import Path
from datetime import datetime,timezone
import base64
import hashlib
import json
import subprocess

ROOT=Path('/Users/alec/Documents/Math')
P=ROOT/'draft_pr_descending_audit_20261002'
D=Path(__file__).resolve().parent
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
BASE='repos/AlecKriebel/Math/'
QPATH='unsolved_math_prioritization/QUEUE.md'
repair=json.loads((D/'CLASSIFICATION_REPAIR_RECEIPT.json').read_text())
assert repair['status']=='APPLIED_AND_VERIFIED' and repair['corrected_status']=='already_solved'
accept=json.loads((D/'ROOT_FINAL_CREDIT_PACKET_ACCEPTANCE.json').read_text())
assert accept['status']=='PASS'
OUT=D/'classification_completion_transport'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
OUT.mkdir(parents=True,exist_ok=False)
seq=0

def api(method,path,payload=None):
    global seq
    seq+=1
    args=[GH,'api','--method',method,BASE+path]
    if payload is not None:
        f=OUT/f'{seq:02d}-request.json'
        f.write_text(json.dumps(payload))
        args+=['--input',str(f)]
    run=subprocess.run(args,capture_output=True,timeout=90)
    (OUT/f'{seq:02d}-stdout.json').write_bytes(run.stdout)
    (OUT/f'{seq:02d}-stderr.txt').write_bytes(run.stderr)
    if run.returncode:
        raise RuntimeError(f'Native call{seq} failed; reconcile retained receipts before mutation retry')
    return json.loads(run.stdout)

def queue_at(ref):
    return base64.b64decode(api('GET','contents/'+QPATH+'?ref='+ref)['content']).decode()

def row_of(text):
    rows=[x for x in text.splitlines() if '9700040 / AMR-096-0040' in x]
    assert len(rows)==1
    return rows[0]

pr=api('GET','pulls/246')
assert pr['head']['sha']==repair['corrected_head'] and pr['state']=='open' and pr['draft'] and not pr['merged']
assert row_of(queue_at(repair['corrected_head'])).split('|')[8].strip()=='already_solved'
utc=datetime.now(timezone.utc).isoformat()
state=json.loads((D/'CURRENT_AUDIT_STATE.json').read_text())
state.update(utc=utc,head=repair['corrected_head'],QUEUE_status='already_solved',stage='credit_classification_repaired_scope_skip',
             completion_percent=100,native_classification_unchanged=False,preprint_upload_cleared=False,
             native_repair_receipt='CLASSIFICATION_REPAIR_RECEIPT.json',next_descending_start_PR=245)
(D/'CURRENT_AUDIT_STATE.json').write_text(json.dumps(state,indent=2)+'\n')
selection=json.loads((P/'CURRENT_GOAL_SELECTION_20261013.json').read_text())
selection.update(utc=utc,current_PR_head=repair['corrected_head'],status_at_current_PR_head='already_solved',
                 case_completion_percent=100,current_stage=state['stage'],next_descending_start_PR=245,
                 priority_classification_repairs_required=[],classification_repair_receipt=str(D/'CLASSIFICATION_REPAIR_RECEIPT.json'))
selection['skip_PRs']=sorted(set(selection['skip_PRs']+[246]),reverse=True)
selection['skip_reasons']['246']='Complete exact earlier stationary-law coverage; already_solved after eligible-intake credit repair'
(P/'CURRENT_GOAL_SELECTION_20261013.json').write_text(json.dumps(selection,indent=2)+'\n')
line=utc+' — PR246 eligible-intake scope disposition100% after full math,5 priority/coverage lanes and NEW final35-file credit-packet adversary. Applied and independently native-byte-verified credited already_solved head '+repair['corrected_head']+'. All20 originals preserved and mathematicalbody/code unchanged. Complete earlier coverage established; no earlier named2018acknowledgement/proposer endorsement/identical certificate priority claimed. Skip corrected open draft; no new paper/deposit/tracker/merge/close/comment. Counts40/17/17/0; held293/292/280 remain uncompleted. Next descending start245, overall goal active/incomplete. This checkpoint publishes the eligible-intake audit and one owned main queue row.'
for log in [D/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
    with log.open('a') as out:out.write('\n'+line+'\n')

paths=[P/'RESEARCH_LOG.md',P/'CURRENT_GOAL_SELECTION_20261013.json']
paths += [f for f in D.iterdir() if f.is_file() and f.suffix in ('.md','.json','.py') and f.name!='PRIORITY_DISPOSITION_PUBLICATION_RECEIPT.json']
paths += [f for f in (D/'corrected_packet').rglob('*') if f.is_file()]
paths += [f for f in (D/'root_priority_reproduction').rglob('*') if f.is_file() and '__pycache__' not in f.parts]
priority=json.loads((D/'ROOT_PRIORITY_PIN_VALIDATION.json').read_text())
for pin in priority['publishable_family_files']+accept['review_publishable_files']:
    f=D/pin['path']
    assert f.resolve().is_relative_to(D.resolve()) and 'private_reading' not in f.relative_to(D).parts
    b=f.read_bytes()
    assert len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256']
    paths.append(f)
entries=[]
pins=[]
for f in sorted(set(paths)):
    assert f.resolve().is_relative_to(P.resolve()) and not f.is_symlink()
    b=f.read_bytes()
    entries.append({'path':f.relative_to(ROOT).as_posix(),'mode':'100644','type':'blob','content':b.decode()})
    pins.append({'path':f.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})

for attempt in range(4):
    parent=api('GET','git/ref/heads/main')['object']['sha']
    mq=queue_at(parent)
    row=row_of(mq)
    assert row.split('|')[8].strip() in ['queued','claimed_solved','already_solved']
    cols=row.split('|')
    assert len(cols)==14
    cols[8]=' already_solved '
    cols[9]=' 1/5 '
    cols[11]=' 2026-10-15: Mathematics PASS; complete earlier stationary-law coverage (AD constructions; LRW2001 finite determinant; BO2004/Nica2014-2015 explicit joint laws). Credited correction from eligible claimed_solved intake, then scope skip; no new preprint/merge. Earlier expressly named2018resolution/proposer endorsement not established. [Priority audit](../draft_pr_descending_audit_20261002/audits/pr246_9700040/initial_review_20261014/corrected_packet/PRIORITY_AUDIT.md). '
    newq=mq.replace(row,'|'.join(cols),1)
    assert sum(a!=b for a,b in zip(mq.splitlines(),newq.splitlines()))==1
    base=api('GET','git/commits/'+parent)['tree']['sha']
    tree=api('POST','git/trees',{'base_tree':base,'tree':entries+[{'path':QPATH,'mode':'100644','type':'blob','content':newq}]})['sha']
    commit=api('POST','git/commits',{'message':'Publish verified stationary-law prior-coverage audit and credited classification correction','tree':tree,'parents':[parent]})['sha']
    try:
        assert api('PATCH','git/refs/heads/main',{'sha':commit,'force':False})['object']['sha']==commit
        break
    except RuntimeError:
        rejection=json.loads((OUT/f'{seq:02d}-stdout.json').read_text())
        latest=api('GET','git/ref/heads/main')['object']['sha']
        if str(rejection.get('status'))!='422' or latest==parent or attempt==3:
            raise
current=api('GET','git/ref/heads/main')['object']['sha']
if current!=commit:
    assert api('GET','compare/'+commit+'...'+current)['status']=='ahead'
assert row_of(queue_at(current)).split('|')[8].strip()=='already_solved'
result={**repair,'utc':datetime.now(timezone.utc).isoformat(),'main_checkpoint':commit,'main_parent':parent,
        'readback_main':current,'owned_public_files':pins,'case_completion_percent':100,
        'third_party_reading_objects_excluded':True,'main_queue_rows_changed':1,
        'completion_transport':str(OUT),'next_descending_start_PR':245,'overall_goal_active_incomplete':True}
(D/'PRIORITY_DISPOSITION_PUBLICATION_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='owned_public_files'},indent=2))
