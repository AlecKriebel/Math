#!/usr/bin/env python3
from pathlib import Path
import os, json, datetime, hashlib
W=Path(__file__).resolve().parent
m=json.loads((W/'OUTPUT_MANIFEST.json').read_text()); s=json.loads((W/'SEAL_RECEIPT.json').read_text())
for r in m['payload']:
    p=W/r['path']; b=p.read_bytes()
    if len(b)!=r['bytes'] or hashlib.sha256(b).hexdigest()!=r['sha256']: raise RuntimeError('Mismatch '+r['path'])
b=(W/'OUTPUT_MANIFEST.json').read_bytes()
if hashlib.sha256(b).hexdigest()!=s['OUTPUT_MANIFEST']['sha256']: raise RuntimeError('Manifest pin mismatch')
if any(r['path'].startswith(('private_sources/','private_review_materials/')) for r in m['payload']): raise RuntimeError('Private body in public payload')
print(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_verifier_PID':os.getpid(),'checked_payload_files':len(m['payload']),'manifest_SHA256':hashlib.sha256(b).hexdigest(),'all_ok':True}))
