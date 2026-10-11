#!/usr/bin/env python3
"""Retain exact first-party streams and complete fresh receipts, never foreign sources."""
from pathlib import Path
import datetime, hashlib, json, shutil
A=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
r=json.loads((A/'ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json').read_text())
assert r['status']=='PASS' and r['authored_members_verified_before_and_after']==364
p=Path(r['private_replica']);d=A/'root_actual_replay';d.mkdir(exist_ok=False)
copies={}
for f in (p.parent/'actual_streams').iterdir():
 assert f.is_file() and f.suffix in ('.stdout','.stderr')
 copies['streams/'+f.name]=f
for f in ['ACTUAL_RUNS.json','ACTUAL_SIX_PURE_QUEUE_SCORE_MUTANTS.json','PRIMARY_ROOT_REDIRECTION.patch']:
 copies[f]=p.parent/f
for c in r['full_structured_receipt_comparisons']:
 copies['receipts/'+c['file']]=p/'draft_pr_publication_program_20260930/audits/pr36_20001424'/c['file']
rows=[]
for rel,src in sorted(copies.items()):
 raw=src.read_bytes();dst=d/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw)
 assert dst.read_bytes()==raw
 rows.append({'path':dst.relative_to(A).as_posix(),'bytes':len(raw),'sha256':sha(raw)})
for run in r['actual_outer_program_runs']:
 for stream in ['stdout','stderr']:
  assert sha((d/'streams'/(run['label']+'.'+stream)).read_bytes())==run[stream+'_sha256']
obj={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','root_reproduction_receipt_sha256':sha((A/'ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json').read_bytes()),'scope':'Exact first-party actual streams, fresh full structured receipts, six actual queue.score mutant results and one private path-redirection patch. Foreign PDFs/text, raw corpus, temporary source copies and scratch trees are excluded.','files':rows,'authored_count':len(rows),'new_substantive_attempts':0}
(A/'ROOT_REPLAY_RETENTION.json').write_text(json.dumps(obj,indent=2)+'\n')
print(json.dumps({'retained_first_party_files':len(rows),'status':'PASS'}))
