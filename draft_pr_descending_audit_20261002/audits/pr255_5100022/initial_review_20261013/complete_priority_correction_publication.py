"""Guarded credit/classification repair from an eligible claimed_solved intake.
Native Git APIs preserve the shared checkout and foreign main changes.
"""
from pathlib import Path
from datetime import datetime, timezone
import base64, hashlib, json, subprocess
from urllib.parse import quote

ROOT=Path('/Users/alec/Documents/Math')
P=ROOT/'draft_pr_descending_audit_20261002'
D=Path(__file__).resolve().parent
C=D/'corrected_packet'
OUT=D/'classification_transport'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
OUT.mkdir(parents=True,exist_ok=False)
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
seq=0
BASE='repos/AlecKriebel/Math/'
OLD='a624d16a87c5ee67a3ab23621b891e5991794071'
QPATH='unsolved_math_prioritization/QUEUE.md'

def api(method,path,payload=None):
 global seq
 seq+=1
 args=[GH,'api','--method',method,BASE+path]
 if payload is not None:
  f=OUT/f'{seq:02d}-request.json';f.write_text(json.dumps(payload));args+=['--input',str(f)]
 r=subprocess.run(args,capture_output=True)
 (OUT/f'{seq:02d}-stdout.json').write_bytes(r.stdout)
 (OUT/f'{seq:02d}-stderr.txt').write_bytes(r.stderr)
 if r.returncode:raise RuntimeError(f'Native API {seq} failed; receipts retained')
 return json.loads(r.stdout)

def queue_at(ref):
 return base64.b64decode(api('GET','contents/'+QPATH+'?ref='+ref)['content']).decode()

def row_of(q):
 rows=[x for x in q.splitlines() if '5100022 / AMR-050-0022' in x]
 assert len(rows)==1
 return rows[0]

def repair_queue(q,proof_link):
 old=row_of(q);cols=old.split('|');assert len(cols)==14
 cols[8]=' already_solved ';cols[9]=' 1/5 '
 cols[11]=' 2026-10-13: Mathematics PASS; exact k404 target already follows from Ferudun DOI 10.5281/zenodo.23079799 Lemma 4 and earlier public PR250 k204 theorem, with positive focal denominator. Primitive N=2 mod4/all stars/signed original polygons verified. Current claimed_solved intake repaired to already_solved and skipped under the active scope; no new preprint or merge. [Priority audit]('+proof_link+'); [prior theorem](https://github.com/AlecKriebel/Math/blob/ea34ca1dd8e2693b58f615aa2a4b45bc548cacc3/unsolved_math_prioritization/attempts/5100013/PROOF.md). '
 new='|'.join(cols)
 assert sum(a!=b for a,b in zip(q.splitlines(),q.replace(old,new,1).splitlines()))==1
 return q.replace(old,new,1)

# Resume after a successful ref mutation and a transiently stale PR metadata read.
commit='c45c86b013b6f223b6a06029ac9817b004fb3eee'
readback=api('GET','pulls/255')
assert readback['head']['sha']==commit and readback['state']=='open' and readback['draft'] and not readback['merged']
assert row_of(queue_at(commit)).split('|')[8].strip()=='already_solved'
receipt={'utc':datetime.now(timezone.utc).isoformat(),'status':'APPLIED_AND_VERIFIED','PR':255,'original_head':OLD,'corrected_head':commit,'source_status':'claimed_solved','corrected_status':'already_solved','mathematics':'PASS_NO_REPAIR','disposition':'skip_after_classification_repair','open_draft_verified':True,'merged':False,'closed':False,'new_comment':False,'new_preprint':False,'deposit':False,'tracker_append':False,'transport_receipts':str(OUT),'shared_checkout_index_mutations':0}
(D/'CLASSIFICATION_REPAIR_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
now=receipt['utc']
selection=json.loads((P/'CURRENT_GOAL_SELECTION_20261013.json').read_text())
selection.update(utc=now,current_PR_head=commit,status_at_current_PR_head='already_solved',case_completion_percent=100,current_stage='priority_classification_repaired_scope_skip',mathematical_repairs_required=[],classification_repair_receipt=str(D/'CLASSIFICATION_REPAIR_RECEIPT.json'),next_descending_start_PR=254)
if 255 not in selection['skip_PRs']:selection['skip_PRs'].append(255)
selection['skip_reasons']={'255':'Exact earlier covering combination; already_solved after eligible-intake credit repair'}
(P/'CURRENT_GOAL_SELECTION_20261013.json').write_text(json.dumps(selection,indent=2)+'\n')
line='\n'+now+' — PR255 /5100022 scope disposition 100%. Mathematical proof accepted without repair; two priority families and fresh independent covering challenge establish earlier complete coverage. Original-source/provider checksums and all-star positive-denominator transfer verified, thirteen exact transfer checks root-replayed. Applied and verified credited priority repair on native head '+commit+'; current QUEUE status already_solved. Skip corrected open draft: no new paper/deposit/tracker/merge/close/comment. Counts remain 38 completed /15 preprints /15 native merges /0 tracker pending; held293/292/280 remain uncompleted. Next descending start254; persistent overall goal active/incomplete.\n'
for log in [D/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
 with log.open('a') as f:f.write(line)

# Publish only the eligible-intake audit result and one owned main QUEUE row.
# Full third-party reading copies and raw web extracts never enter this tree.
priority=json.loads((D/'FINAL_PRIORITY_MANIFEST.json').read_text())
paths=[P/'RESEARCH_LOG.md',P/'CURRENT_GOAL_SELECTION_20261013.json',D/'FINAL_PRIORITY_MANIFEST.json',D/'RESEARCH_LOG.md',D/'apply_priority_correction.py',D/'complete_priority_correction_publication.py',D/'CLASSIFICATION_REPAIR_RECEIPT.json']
paths += [D/x['path'] for x in priority['publishable_files']]
paths += [f for f in sorted(C.rglob('*')) if f.is_file()]
paths=list(dict.fromkeys(paths))
owned=[{'path':f.relative_to(ROOT).as_posix(),'mode':'100644','type':'blob','content':f.read_text()} for f in paths]
mainnote='../draft_pr_descending_audit_20261002/audits/pr255_5100022/initial_review_20261013/corrected_packet/PRIORITY_AUDIT.md'
for attempt in range(4):
 parent=api('GET','git/ref/heads/main')['object']['sha']
 mq=queue_at(parent);assert row_of(mq).split('|')[8].strip() in ['queued','claimed_solved','already_solved']
 mtree=api('GET','git/commits/'+parent)['tree']['sha']
 newtree=api('POST','git/trees',{'base_tree':mtree,'tree':owned+[{'path':QPATH,'mode':'100644','type':'blob','content':repair_queue(mq,mainnote)}]})['sha']
 maincommit=api('POST','git/commits',{'message':'Publish verified k404 prior-covering audit and classification correction','tree':newtree,'parents':[parent]})['sha']
 try:
  assert api('PATCH','git/refs/heads/main',{'sha':maincommit,'force':False})['object']['sha']==maincommit
  break
 except RuntimeError:
  rejection=json.loads((OUT/f'{seq:02d}-stdout.json').read_text())
  latest=api('GET','git/ref/heads/main')['object']['sha']
  if rejection.get('status')!='422' or latest==parent or attempt==3:raise
current=api('GET','git/ref/heads/main')['object']['sha']
if current!=maincommit:assert api('GET','compare/'+maincommit+'...'+current)['status']=='ahead'
assert row_of(queue_at(current)).split('|')[8].strip()=='already_solved'
receipt.update(main_checkpoint=maincommit,main_parent=parent,readback_main=current,owned_public_files=len(owned),case_completion_percent=100,copyright_reading_copies_excluded=True)
(D/'PRIORITY_DISPOSITION_PUBLICATION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
