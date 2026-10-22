"""Guarded eligible-intake credit repair, without local Git operations.

Do not rerun after an uncertain provider outcome: reconcile durable responses.
Main publication is a separate continuation after this PR result is verified.
"""
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import quote
import base64
import hashlib
import json
import subprocess

ROOT=Path('/Users/alec/Documents/Math')
P=ROOT/'draft_pr_descending_audit_20261002'
D=Path(__file__).resolve().parent
C=D/'corrected_packet'
OLD='0b4db59eb5515f2d90d8b8df33b6b729b78b48f1'
BASE='repos/AlecKriebel/Math/'
PREFIX='unsolved_math_prioritization/attempts/9700040/'
QPATH='unsolved_math_prioritization/QUEUE.md'
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
OUT=D/'classification_transport'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
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
        raise RuntimeError(f'Native call{seq} failed. Reconcile retained receipts before any mutation retry.')
    return json.loads(run.stdout)

def row_of(text):
    rows=[r for r in text.splitlines() if '9700040 / AMR-096-0040' in r]
    assert len(rows)==1
    return rows[0]

def blob_id(raw):
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()

assert not (D/'CLASSIFICATION_REPAIR_RECEIPT.json').exists(), 'A recorded repair must be reconciled, not repeated'
accept=json.loads((D/'ROOT_FINAL_CREDIT_PACKET_ACCEPTANCE.json').read_text())
assert accept['status']=='PASS' and accept['native_mutations_cleared'] is True
packet=json.loads((D/'PROPOSED_CURRENT_PACKET_MANIFEST.json').read_text())
assert len(packet['files'])==35
assert hashlib.sha256((D/'PROPOSED_CURRENT_PACKET_MANIFEST.json').read_bytes()).hexdigest()==accept['packet_manifest_sha256']
expected={}
for pin in packet['files']:
    f=C/pin['path']
    assert f.resolve().is_relative_to(C.resolve()) and not f.is_symlink()
    raw=f.read_bytes()
    assert len(raw)==pin['bytes'] and hashlib.sha256(raw).hexdigest()==pin['sha256']
    expected[pin['path']]=raw
assert set(expected)=={x.relative_to(C).as_posix() for x in C.rglob('*') if x.is_file()}
intake=json.loads((D/'INTAKE.json').read_text())
for pin in intake['original_source_files']:
    rel=pin['native_path'].removeprefix(PREFIX)
    raw=expected['original_submission/'+rel]
    assert len(raw)==pin['bytes'] and hashlib.sha256(raw).hexdigest()==pin['sha256'] and blob_id(raw)==pin['native_blob']

pr=api('GET','pulls/246')
assert pr['state']=='open' and pr['draft'] and not pr['merged'] and pr['head']['sha']==OLD
assert pr['head']['repo']['full_name']=='AlecKriebel/Math'
qobj=api('GET','contents/'+QPATH+'?ref='+OLD)
queue=base64.b64decode(qobj['content']).decode()
oldrow=row_of(queue)
assert oldrow.split('|')[8].strip()=='claimed_solved'
cols=oldrow.split('|')
assert len(cols)==14
cols[8]=' already_solved '
cols[9]=' 1/5 '
cols[11]=' 2026-10-15: Mathematics PASS; complete stationary law already covered by Aldous-Diaconis constructions plus explicit BO2004/Nica2014-2015 joint laws; independent LRW2001 determinant route also verified. Historical explicit acknowledgement of the2018 question is not claimed. Credited classification repair from eligible intake; skip corrected draft. [Priority audit](attempts/9700040/PRIORITY_AUDIT.md). '
newqueue=queue.replace(oldrow,'|'.join(cols),1)
assert sum(a!=b for a,b in zip(queue.splitlines(),newqueue.splitlines()))==1
request={'utc':datetime.now(timezone.utc).isoformat(),'PR':246,'old_head':OLD,'branch':pr['head']['ref'],
         'packet_manifest_sha256':accept['packet_manifest_sha256'],'old_row':oldrow,'new_row':'|'.join(cols),
         'scope':'One planned credit/classification repair from eligible claimed_solved intake, then immediate scope skip',
         'merge_close_comment_preprint_tracker':False}
(D/'CLASSIFICATION_REPAIR_REQUEST.json').write_text(json.dumps(request,indent=2)+'\n')
body='''The simultaneous stationary-law proof and exact rational certificate pass independent mathematical reproduction and adversarial review. The derivation and evaluator remain useful credited exposition; mathematical Sections1–7 and the code/checker/receipt are unchanged, with all20 original files archived byte for byte.

An extensive priority audit, including separate historical, Schur/Plancherel, recent-literature, bridge-falsification and novelty-saving challenges, establishes complete earlier mathematical coverage. Aldous–Diaconis's stationary-rank construction and published graphical geometry combine with the explicit Borodin–Olshanski2004 and Nica2014/2015 full joint laws to give the exact candidate formula. A separately checked Levikson–Rolski–Weiss2001 finite determinant also covers every simultaneous threshold event. PRIORITY_AUDIT.md gives all parameter bridges and source caveats.

Corrected classification: **already_solved**, author turn1/5. This means earlier complete mathematical coverage; it does not claim an earlier expressly acknowledged answer to the February2018 posting, proposer endorsement, or prior publication of the identical rational wrapper/software. The submission itself already disclaimed novelty. AI tools were used extensively; the audit is unrefereed and is not human peer review.

Under the active claimed_solved-only goal, skip this corrected open draft. No new preprint, Zenodo deposit, tracker row, merge, closure or PR comment accompanies the disposition. The broader goal remains active and incomplete.'''
api('PATCH','pulls/246',{'title':'9700040: credited stationary-law formula; complete earlier coverage','body':body})
assert api('GET','pulls/246')['head']['sha']==OLD
entries=[{'path':PREFIX+rel,'mode':'100644','type':'blob','content':raw.decode()} for rel,raw in sorted(expected.items())]
for pin in intake['original_source_files']:
    rel=pin['native_path'].removeprefix(PREFIX)
    if rel not in expected:
        entries.append({'path':pin['native_path'],'mode':'100644','type':'blob','sha':None})
entries.append({'path':QPATH,'mode':'100644','type':'blob','content':newqueue})
oldtree=api('GET','git/commits/'+OLD)['tree']['sha']
tree=api('POST','git/trees',{'base_tree':oldtree,'tree':entries})['sha']
commit=api('POST','git/commits',{'message':'Credit complete earlier stationary-law coverage and correct classification; preserve verified proof','tree':tree,'parents':[OLD]})['sha']
assert api('PATCH','git/refs/heads/'+quote(pr['head']['ref'],safe='/'),{'sha':commit,'force':False})['object']['sha']==commit
(D/'CLASSIFICATION_NATIVE_REF_RESULT.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'commit':commit,'old_head':OLD,'source_files':35,'transport':str(OUT)},indent=2)+'\n')

# Verify exact subtree, rather than a possibly truncated repository-wide tree.
subtree=tree
for part in PREFIX.strip('/').split('/'):
    t=api('GET','git/trees/'+subtree)
    assert not t['truncated']
    subtree=next(x['sha'] for x in t['tree'] if x['path']==part and x['type']=='tree')
native=api('GET','git/trees/'+subtree+'?recursive=1')
assert not native['truncated']
leaves={x['path']:x for x in native['tree'] if x['type']=='blob'}
assert set(leaves)==set(expected)
for rel,raw in expected.items():
    leaf=leaves[rel]
    assert leaf['mode']=='100644' and leaf['size']==len(raw) and leaf['sha']==blob_id(raw)
    obj=api('GET','git/blobs/'+leaf['sha'])
    assert obj['encoding']=='base64' and base64.b64decode(obj['content'])==raw
readq=base64.b64decode(api('GET','contents/'+QPATH+'?ref='+commit)['content']).decode()
assert readq==newqueue and row_of(readq).split('|')[8].strip()=='already_solved'
readpr=api('GET','pulls/246')
assert readpr['head']['sha']==commit and readpr['state']=='open' and readpr['draft'] and not readpr['merged']
receipt={'utc':datetime.now(timezone.utc).isoformat(),'status':'APPLIED_AND_VERIFIED','PR':246,'original_head':OLD,
         'corrected_head':commit,'original_status':'claimed_solved','corrected_status':'already_solved',
         'source_files_actually_fetched_and_byte_compared':35,'mathematics':'PASS_NO_REPAIR',
         'disposition':'skip_after_credit_classification_repair','open_draft':True,'merged':False,'closed':False,
         'comment':False,'preprint':False,'deposit':False,'tracker_append':False,'local_git_mutations':0,
         'transport_receipts':str(OUT)}
(D/'CLASSIFICATION_REPAIR_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
