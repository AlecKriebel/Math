"""Apply only a separately cleared, exact eligible-intake credit correction.

No local Git operations. Never restart after an uncertain provider outcome:
reconcile saved responses and the live branch first.
"""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote
import base64,hashlib,json,subprocess

D=Path(__file__).resolve().parent
C=D/'corrected_packet'
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
BASE='repos/AlecKriebel/Math/'
PREFIX='unsolved_math_prioritization/attempts/30005310/'
QPATH='unsolved_math_prioritization/QUEUE.md'
OLD='c697b4a5cc62f3b8836d8c37d82b71a1d1c53fb7'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
blob=lambda raw:hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()

assert not (D/'CLASSIFICATION_REPAIR_RECEIPT.json').exists(), 'Reconcile a recorded operation; never repeat blindly'
assert not (D/'CLASSIFICATION_REPAIR_REQUEST.json').exists(), 'A prior attempt exists; reconcile it read-only before any further action'
accept=json.loads((D/'ROOT_FINAL_CREDIT_PACKET_ACCEPTANCE.json').read_text())
assert accept['status']=='PASS' and accept['native_mutations_cleared'] is True
assert sha(D/'PROPOSED_CURRENT_PACKET_MANIFEST.json')==accept['packet_manifest_sha256']
assert sha(D/'PROPOSED_NATIVE_CHANGES.json')==accept['native_plan_sha256']
plan=json.loads((D/'PROPOSED_NATIVE_CHANGES.json').read_text())
packet=json.loads((D/'PROPOSED_CURRENT_PACKET_MANIFEST.json').read_text())
assert plan['original_head']==OLD and plan['PR']==212
assert plan['packet_manifest_sha256']==accept['packet_manifest_sha256']
assert len(packet['files'])==plan['planned_source_files']
expected={}
for row in packet['files']:
    q=C/row['path'];raw=q.read_bytes()
    assert q.resolve().is_relative_to(C.resolve()) and not q.is_symlink()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
    expected[row['path']]=raw
assert set(expected)=={q.relative_to(C).as_posix() for q in C.rglob('*') if q.is_file()}
intake=json.loads((D/'INTAKE.json').read_text())
for row in intake['original_source_files']:
    rel=row['native_path'].removeprefix(PREFIX);raw=expected['original_submission/'+rel]
    assert blob(raw)==row['native_blob'] and hashlib.sha256(raw).hexdigest()==row['sha256']
core=lambda raw:raw.split(b'## 2. Model, statistics and sample convention',1)[1].split(b'## 8.',1)[0]
assert core(expected['PROOF.md'])==core(expected['original_submission/PROOF.md'])

T=D/'private_transport'/datetime.now(timezone.utc).strftime('classification_%Y%m%dT%H%M%S%fZ')
T.mkdir(parents=True,exist_ok=False)
seq=0

def api(method,path,payload=None):
    global seq
    seq+=1;args=[GH,'api','--method',method,BASE+path]
    if payload is not None:
        q=T/f'{seq:02d}-request.json';q.write_text(json.dumps(payload));args+=['--input',str(q)]
    run=subprocess.run(args,capture_output=True,timeout=60)
    (T/f'{seq:02d}-stdout.json').write_bytes(run.stdout);(T/f'{seq:02d}-stderr.txt').write_bytes(run.stderr)
    if run.returncode:raise RuntimeError(f'Native call{seq} failed; inspect durable responses and live state before any mutation retry')
    return json.loads(run.stdout)

pr=api('GET','pulls/212')
assert pr['state']=='open' and pr['draft'] and not pr['merged'] and pr['head']['sha']==OLD
assert pr['head']['repo']['full_name']=='AlecKriebel/Math' and pr['head']['ref']==plan['branch']
qobj=api('GET','contents/'+QPATH+'?ref='+OLD)
assert qobj['sha']==intake['Queue_blob']
queue=base64.b64decode(qobj['content']).decode()
assert queue.count(plan['old_row'])==1 and plan['old_row'].split('|')[8].strip()=='claimed_solved'
newqueue=queue.replace(plan['old_row'],plan['new_row'],1)
assert len(queue.splitlines())==len(newqueue.splitlines())
assert sum(a!=b for a,b in zip(queue.splitlines(),newqueue.splitlines()))==1
assert plan['new_row'].split('|')[8].strip()=='already_solved'
(D/'CLASSIFICATION_REPAIR_REQUEST.json').write_text(json.dumps(dict(
    utc=datetime.now(timezone.utc).isoformat(),PR=212,original_head=OLD,
    packet_manifest_sha256=accept['packet_manifest_sha256'],native_plan_sha256=accept['native_plan_sha256'],
    classification_meaning='Exact earlier negative coverage of full literal numerical question; bare mechanisms alternative unresolved',
    prior_exact_tied_variant_anticipation=False,native_transport=str(T)),indent=2)+'\n')
entries=[dict(path=PREFIX+rel,mode='100644',type='blob',content=raw.decode()) for rel,raw in sorted(expected.items())]
for row in intake['original_source_files']:
    if row['native_path'].removeprefix(PREFIX) not in expected:
        entries.append(dict(path=row['native_path'],mode='100644',type='blob',sha=None))
entries.append(dict(path=QPATH,mode='100644',type='blob',content=newqueue))
oldtree=api('GET','git/commits/'+OLD)['tree']['sha']
tree=api('POST','git/trees',dict(base_tree=oldtree,tree=entries))['sha']
commit=api('POST','git/commits',dict(
    message='Credit prior negative coverage of literal threshold scenarios; preserve verified counterexample and all original evidence',
    tree=tree,parents=[OLD]))['sha']
assert api('PATCH','git/refs/heads/'+quote(plan['branch'],safe='/'),dict(sha=commit,force=False))['object']['sha']==commit
(D/'CLASSIFICATION_NATIVE_REF_RESULT.json').write_text(json.dumps(dict(
    utc=datetime.now(timezone.utc).isoformat(),commit=commit,original_head=OLD,
    source_files=len(expected),native_transport=str(T),readback_and_PR_metadata_pending=True),indent=2)+'\n')

# Verify the exact attempt subtree rather than any truncated repository listing.
subtree=tree
for part in PREFIX.strip('/').split('/'):
    obj=api('GET','git/trees/'+subtree);assert not obj['truncated']
    subtree=next(x['sha'] for x in obj['tree'] if x['path']==part and x['type']=='tree')
obj=api('GET','git/trees/'+subtree+'?recursive=1');assert not obj['truncated']
leaves={r['path']:r for r in obj['tree'] if r['type']=='blob'}
assert set(leaves)==set(expected)

def readback(item):
    rel,raw=item;r=leaves[rel]
    assert r['mode']=='100644' and r['size']==len(raw) and r['sha']==blob(raw)
    run=subprocess.run([GH,'api',BASE+'git/blobs/'+r['sha']],capture_output=True,timeout=60)
    assert run.returncode==0
    obj=json.loads(run.stdout);assert obj['encoding']=='base64'
    actual=base64.b64decode(obj['content']);assert actual==raw
    (T/('readback-'+r['sha']+'.json')).write_bytes(run.stdout)
    return dict(path=rel,sha256=hashlib.sha256(actual).hexdigest(),bytes=len(actual),native_blob=r['sha'],byte_identical=True)

with ThreadPoolExecutor(max_workers=6) as pool:readbacks=list(pool.map(readback,sorted(expected.items())))
readq=base64.b64decode(api('GET','contents/'+QPATH+'?ref='+commit)['content']).decode()
assert readq==newqueue
pr=api('GET','pulls/212')
assert pr['state']=='open' and pr['draft'] and not pr['merged'] and pr['head']['sha']==commit
# Finish the same pre-reviewed logical credit repair; no new audit at the corrected status.
api('PATCH','pulls/212',dict(title=plan['title'],body=plan['body']))
pr=api('GET','pulls/212')
assert pr['head']['sha']==commit and pr['state']=='open' and pr['draft'] and not pr['merged']
assert pr['title']==plan['title'] and pr['body']==plan['body']
out=dict(utc=datetime.now(timezone.utc).isoformat(),status='APPLIED_AND_VERIFIED',PR=212,
    original_head=OLD,corrected_head=commit,original_status='claimed_solved',corrected_status='already_solved',
    qualification='Earlier primary results cover literal numerical negative answer; bare mechanisms alternative unresolved',
    exact_tied_variant_anticipation_and_first_error_recognition='not established',mathematics='PASS_NO_REPAIR',author_turns=1,
    source_files_actually_fetched_and_byte_compared=len(expected),original_archive_files=20,
    mathematical_core_bytes_unchanged=len(core(expected['PROOF.md'])),actual_native_byte_readbacks=readbacks,
    disposition='immediate_scope_skip_after_qualified_historical_credit_repair',open_draft=True,
    merged=False,closed=False,PR_comment=False,preprint=False,deposit=False,tracker_append=False,
    local_Git_or_index_mutations=0,counts=[42,19,19,0],native_transport=str(T))
(D/'CLASSIFICATION_REPAIR_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='actual_native_byte_readbacks'},indent=2))
