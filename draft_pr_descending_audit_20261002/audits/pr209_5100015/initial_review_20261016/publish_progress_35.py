"""Publish qualified priority checkpoint using pinned scoped publisher mechanics."""
from pathlib import Path
import hashlib,json

D=Path(__file__).resolve().parent
template=D/'publish_progress_15.py'
receipt=json.loads((D/'PROGRESS_25_CHECKPOINT_RECEIPT.json').read_text())
rel='draft_pr_descending_audit_20261002/audits/pr209_5100015/initial_review_20261016/publish_progress_15.py'
pin=next(x for x in receipt['owned_files'] if x['path']==rel)
raw=template.read_bytes()
assert hashlib.sha256(raw).hexdigest()==pin['sha256']
source=raw.decode()
supplement="""paths += [q for q in (D/'priority_public_chronology_01').iterdir() if q.is_file()]
folder=D/'priority_author_updates_01'
supp=folder/'AUTHORED_MANIFEST_SUPPLEMENT_TIMESTAMP_CORRECTION.json'
obj=json.loads(supp.read_text());paths.append(supp)
for row in [obj['original_manifest'],*obj['original_payloads_unchanged'],*obj['supplemental_payloads']]:
    q=folder/row['path'];raw=q.read_bytes()
    assert q.resolve().is_relative_to(folder.resolve()) and not q.is_symlink()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
    paths.append(q)
"""
fallback="""if obj.get('encoding')=='base64':
        actual=base64.b64decode(obj['content'])
    else:
        blobrun=subprocess.run([GH,'api',BASE+'git/blobs/'+obj['sha']],capture_output=True,timeout=60)
        assert blobrun.returncode==0
        blobobj=json.loads(blobrun.stdout)
        assert blobobj['sha']==obj['sha'] and blobobj['encoding']=='base64'
        actual=base64.b64decode(blobobj['content'])
    assert actual==raw"""
changes=[
 ("OUT=D/'PROGRESS_15_CHECKPOINT_RECEIPT.json'","OUT=D/'PROGRESS_35_CHECKPOINT_RECEIPT.json'"),
 ("prior=json.loads((OLD/'FINAL_COMPLETION_CHECKPOINT_PUBLICATION_RECEIPT.json').read_text())","prior=json.loads((D/'PROGRESS_25_CHECKPOINT_RECEIPT.json').read_text())"),
 ("assert prior['commit']=='1a702f8807e00af02d0eed244f0bc27df98f6079'","assert prior['commit']=='80ca3a950e762ee4a10fbaaa19ebecd06399bba1'"),
 ("assert state['completion_percent']==15 and state['preprint_preparation_cleared'] is False","assert state['completion_percent']==35 and state['preprint_preparation_cleared'] is True"),
 ("strftime('progress15_%Y%m%dT%H%M%S%fZ')","strftime('progress35_%Y%m%dT%H%M%S%fZ')"),
 ("for name in ['submitted','root_reproduction_01']:","for name in ['submitted','root_reproduction_01','root_reproduction_02','root_reproduction_03']:"),
 ("for name in ['source_domain_adversary_01','meromorphic_divisor_adversary_01']:","for name in ['source_domain_adversary_01','meromorphic_divisor_adversary_01','physical_geometry_adversary_01','priority_author_updates_01','priority_classical_general_01']:"),
 ("for row in obj['files']:","for row in obj.get('files',obj.get('payloads')):"),
 ("root_final_acceptance_pending=True","root_final_acceptance_pending=False"),
 ("paths += [OLD/'FINAL_COMPLETION_CHECKPOINT_PUBLICATION_RECEIPT.json'",supplement+"paths += [OLD/'FINAL_COMPLETION_CHECKPOINT_PUBLICATION_RECEIPT.json'"),
 ("entries.append(dict(path=rel,mode='100644',type='blob',content=raw.decode()))","try:\n        entry=dict(path=rel,mode='100644',type='blob',content=raw.decode())\n    except UnicodeDecodeError:\n        assert api('POST','git/blobs',dict(content=base64.b64encode(raw).decode(),encoding='base64'))['sha']==blob\n        entry=dict(path=rel,mode='100644',type='blob',sha=blob)\n    entries.append(entry)"),
 ("assert base64.b64decode(obj['content'])==raw",fallback),
 ("Checkpoint PR209 at15%: frozen source and exact verification replays, independent audits pending","Checkpoint PR209 at35%: qualified priority audit, exact contemporary and classical credit, writing clearance"),
 ("case_completion_percent=15","case_completion_percent=35"),
 ("preprint_preparation_cleared=False","preprint_preparation_cleared=True"),
]
for old,new in changes:
    assert source.count(old)==1,old
    source=source.replace(old,new)
assert not (D/'PROGRESS_35_CHECKPOINT_RECEIPT.json').exists()
exec(compile(source,str(D/'publish_progress_35.py')+'[pinned-template]','exec'),{'__file__':str(D/'publish_progress_35.py'),'__name__':'__main__'})
