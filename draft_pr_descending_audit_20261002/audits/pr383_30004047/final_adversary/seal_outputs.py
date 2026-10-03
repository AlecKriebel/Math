#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,datetime,sys
P=Path(__file__).resolve().parent;EXCLUDED={'OUTPUT_MANIFEST.json','OUTPUT_MANIFEST_VERIFY.json'};EXCLUDED_DIRS={'raw_primary','private_replay'}
def eligible(f):
 rel=f.relative_to(P);return f.is_file() and rel.parts[0] not in EXCLUDED_DIRS and str(rel) not in EXCLUDED
files=[f for f in sorted(P.rglob('*')) if eligible(f)]
rows=[{'path':str(f.relative_to(P)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in files]
mp=P/'OUTPUT_MANIFEST.json'
if '--verify' not in sys.argv:
 mp.write_text(json.dumps({'audit':'PR383 final independent adversary','head':'5f576c1b527f88730c7ee15fd204536069753f9a','sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mandatory_repairs':[],'original_disposition':'unsolved5/5','excluded_files':sorted(EXCLUDED),'excluded_private_directories':sorted(EXCLUDED_DIRS),'files':rows},indent=2)+'\n')
v=json.loads(mp.read_text());assert v['files']==rows
for e in v['files']:
 b=(P/e['path']).read_bytes();assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256']
# The initial source-first seal is independently immutable inside this final seal.
old=json.loads((P/'INDEPENDENT_SEAL.json').read_text())
for e in old['files']:
 b=(P/e['path']).read_bytes();assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256']
receipt={'status':'PASS','verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':len(rows),'manifest_bytes':mp.stat().st_size,'manifest_sha256':hashlib.sha256(mp.read_bytes()).hexdigest(),'initial_source_first_seal_preserved':True,'every_full_output_and_code_hash_verified':True,'no_unlisted_public_audit_files':True,'mandatory_repairs':[]}
(P/'OUTPUT_MANIFEST_VERIFY.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
