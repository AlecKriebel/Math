#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

p=Path(__file__).resolve().parent
excluded={'OUTPUT_MANIFEST.json','OUTPUT_MANIFEST_VERIFY.json'}
paths=sorted(f for f in p.rglob('*') if f.is_file() and str(f.relative_to(p)) not in excluded)
rows=[]
for f in paths:
    b=f.read_bytes()
    rows.append(dict(path=str(f.relative_to(p)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
m=dict(schema='reviewer-output-manifest-v1',frozen_candidate_head='967e8e489aa4599f712d5ddcde62e591827f7e38',
       generated_utc=datetime.now(timezone.utc).isoformat(),excluded=sorted(excluded),files=rows)
mp=p/'OUTPUT_MANIFEST.json'
mp.write_text(json.dumps(m,indent=2)+'\n')
actual={str(f.relative_to(p)) for f in p.rglob('*') if f.is_file() and str(f.relative_to(p)) not in excluded}
assert actual=={r['path'] for r in rows}
for r in rows:
    b=(p/r['path']).read_bytes()
    assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
receipt=dict(status='PASS',verified_utc=datetime.now(timezone.utc).isoformat(),files=len(rows),
             manifest_bytes=mp.stat().st_size,manifest_sha256=hashlib.sha256(mp.read_bytes()).hexdigest(),
             byte_lengths_and_sha256_verified=True,no_extra_unlisted_files=True,
             excluded=sorted(excluded))
(p/'OUTPUT_MANIFEST_VERIFY.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
