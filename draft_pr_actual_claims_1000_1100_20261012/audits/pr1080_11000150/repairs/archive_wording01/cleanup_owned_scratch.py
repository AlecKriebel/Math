#!/usr/bin/env python3
"""Inventory exact owned disposable bytes before removing only this scratch."""
import datetime, hashlib, json, shutil
from pathlib import Path
W=Path(__file__).resolve().parent; S=W/'scratch'
if S.is_symlink() or not S.is_dir() or S.resolve().parent!=W:raise RuntimeError('Owned scratch boundary')
record=W/'OWNED_SCRATCH_CLEANUP.json'
if record.exists():raise RuntimeError('Never overwrite a cleanup receipt')
rows=[]
for p in sorted(S.rglob('*')):
    if p.is_symlink():raise RuntimeError('Unexpected scratch symlink; preserve instead')
    if p.is_file():rows.append({'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
data={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owned_root':str(S),'scope':'Exact absolute paths, sizes and hashes recorded before removing only repairs/archive_wording01/scratch. No canonical, other-worker, history or source-cache deletion. Earlier owned rebuilds were separately pinned in OWNED_EARLY_CLEANUP.jsonl.','files':rows,'total_bytes':sum(r['bytes'] for r in rows),'cleanup_completed':False}
record.write_text(json.dumps(data,indent=2)+'\n')
shutil.rmtree(S)
data['cleanup_completed']=not S.exists();data['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();record.write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'files_pinned_before_cleanup':len(rows),'bytes':data['total_bytes'],'only_owned_scratch_removed':data['cleanup_completed']}))
