"""Use the pinned progress publisher with explicit case25-only substitutions."""
from pathlib import Path
import hashlib,json

D=Path(__file__).resolve().parent
template=D/'publish_progress_15.py'
receipt=json.loads((D/'PROGRESS_15_CHECKPOINT_RECEIPT.json').read_text())
rel='draft_pr_descending_audit_20261002/audits/pr209_5100015/initial_review_20261016/publish_progress_15.py'
pin=next(x for x in receipt['owned_files'] if x['path']==rel)
raw=template.read_bytes()
assert hashlib.sha256(raw).hexdigest()==pin['sha256']
source=raw.decode()
changes=[
 ("OUT=D/'PROGRESS_15_CHECKPOINT_RECEIPT.json'","OUT=D/'PROGRESS_25_CHECKPOINT_RECEIPT.json'"),
 ("prior=json.loads((OLD/'FINAL_COMPLETION_CHECKPOINT_PUBLICATION_RECEIPT.json').read_text())","prior=json.loads((D/'PROGRESS_15_CHECKPOINT_RECEIPT.json').read_text())"),
 ("assert prior['commit']=='1a702f8807e00af02d0eed244f0bc27df98f6079'","assert prior['commit']=='c57d85b1d0ea456801c0bd77ea7846088e9cef9d'"),
 ("assert state['completion_percent']==15","assert state['completion_percent']==25"),
 ("strftime('progress15_%Y%m%dT%H%M%S%fZ')","strftime('progress25_%Y%m%dT%H%M%S%fZ')"),
 ("for name in ['submitted','root_reproduction_01']:","for name in ['submitted','root_reproduction_01','root_reproduction_02']:"),
 ("for name in ['source_domain_adversary_01','meromorphic_divisor_adversary_01']:","for name in ['source_domain_adversary_01','meromorphic_divisor_adversary_01','physical_geometry_adversary_01']:"),
 ("root_final_acceptance_pending=True","root_final_acceptance_pending=False"),
 ("paths += [OLD/'FINAL_COMPLETION_CHECKPOINT_PUBLICATION_RECEIPT.json'","paths += [q for q in (D/'priority_public_chronology_01').iterdir() if q.is_file()]\npaths += [OLD/'FINAL_COMPLETION_CHECKPOINT_PUBLICATION_RECEIPT.json'"),
 ("entries.append(dict(path=rel,mode='100644',type='blob',content=raw.decode()))","try:\n        entry=dict(path=rel,mode='100644',type='blob',content=raw.decode())\n    except UnicodeDecodeError:\n        assert api('POST','git/blobs',dict(content=base64.b64encode(raw).decode(),encoding='base64'))['sha']==blob\n        entry=dict(path=rel,mode='100644',type='blob',sha=blob)\n    entries.append(entry)"),
 ("Checkpoint PR209 at15%: frozen source and exact verification replays, independent audits pending","Checkpoint PR209 at25%: three mathematical audits and exact root replays accepted; priority pending"),
 ("case_completion_percent=15","case_completion_percent=25"),
]
for old,new in changes:
    assert source.count(old)==1,old
    source=source.replace(old,new)
assert not (D/'PROGRESS_25_CHECKPOINT_RECEIPT.json').exists()
exec(compile(source,str(D/'publish_progress_25.py')+'[pinned-template]','exec'),{'__file__':str(D/'publish_progress_25.py'),'__name__':'__main__'})
