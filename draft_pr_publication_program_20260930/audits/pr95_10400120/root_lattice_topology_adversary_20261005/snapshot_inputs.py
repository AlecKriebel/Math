#!/usr/bin/env python3
import hashlib, json
from pathlib import Path
root=Path(__file__).resolve().parent
src=root.parent/'original_source_authentication_20261005'/'original_attempt'
dst=root/'incoming_snapshots'
names=['COUNTEREXAMPLE.md','verify.py','README.md','verification.json','source_record.json','source_manifest.json','independent_review/REVIEW.md','independent_review/independent_checks.py']
records=[]
for name in names:
    data=(src/name).read_bytes()
    out=dst/name
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_bytes(data)
    records.append(dict(original_path=str((src/name).resolve()),snapshot_path=str(out.relative_to(root)),sha256=hashlib.sha256(data).hexdigest(),size=len(data)))
(root/'INCOMING_SNAPSHOT_MANIFEST.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(dict(copied=len(records),all_preserved=True),indent=2))
