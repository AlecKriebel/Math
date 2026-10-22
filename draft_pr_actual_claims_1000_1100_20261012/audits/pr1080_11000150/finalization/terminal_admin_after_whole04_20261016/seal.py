#!/usr/bin/env python3
"""Close settled local terminal artifacts; no candidate or historical resealing."""
from pathlib import Path
import datetime,hashlib,json
W=Path(__file__).resolve().parent
if (W/'SEAL.json').exists() or (W/'OUTPUT_PINS.json').exists():raise RuntimeError('Never overwrite terminal seal')
if (W/'scratch').exists():raise RuntimeError('Own scratch must be explicitly closed first')
def row(p):return {'path':p.relative_to(W).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def dump(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
files=[]
for p in sorted(W.rglob('*')):
 if p.is_symlink():raise RuntimeError('Unexpected local output symlink')
 if p.is_file():files.append(row(p))
dump(W/'OUTPUT_PINS.json',{'utc':now,'scope':'Every enduring artifact of this bounded terminal administrative workspace, including original operative code, full actual receipts/failures, exact local before ZIP/snapshots and explicit transient cleanup/physical-backing records. Excludes only this inventory and separate seal. The old ZIP is private ignored/local-only and not newly public. No writes after separate seal.','files':files})
r=row(W/'OUTPUT_PINS.json');dump(W/'SEAL.json',{'utc':now,'status':'SEALED_TERMINAL_ADMIN_AFTER_ADOPTED_WHOLE04_PENDING_EXTERNAL_ROOT_FINAL_INTEGRITY','output_inventory':r,'output_files':len(files),'whole_reviews_completed':4,'minimum_whole_reviews':2,'latest_whole04_zero_findings':True,'root_whole04_adopted':True,'new_complete_review_currently_required':False,'root_final_integrity_required':True,'root_final_integrity_adopted':False,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_at':1032,'scope':'Nonself-hashing integrity bookkeeping, not authentication, human peer review or final ROOT adoption.'})
print(json.dumps({'status':'SEALED','outputs':len(files),'output_inventory':r},indent=2))
