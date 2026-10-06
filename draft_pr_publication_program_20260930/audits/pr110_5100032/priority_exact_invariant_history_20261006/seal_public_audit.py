#!/usr/bin/env python3
"""Seal this family's public audit payload using actual process identity and bytes."""
from pathlib import Path
import os, datetime, json, hashlib
W=Path(__file__).resolve().parent
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
pid=os.getpid()
def digest(b): return hashlib.sha256(b).hexdigest()
with (W/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n'+utc+': Seal checkpoint by actual processPID'+str(pid)+': bounded-family report/artifact work100% complete; novelty assessment remains explicitly bounded, root publication clearance still pending. No prior full cover found; final-book/source-version and recorded partial-reading gaps retained.\n')
excluded_roots={'private_sources','private_review_materials'}
excluded_files={'OUTPUT_MANIFEST.json','SEAL_RECEIPT.json'}
excluded_operation_roots={'actual_operations/seal_public_audit_final','actual_operations/verify_public_seal_final'}
rows=[]
for p in sorted(W.rglob('*')):
    if not p.is_file(): continue
    rel=p.relative_to(W).as_posix()
    if rel.split('/')[0] in excluded_roots or rel in excluded_files or any(rel==x or rel.startswith(x+'/') for x in excluded_operation_roots): continue
    if p.is_symlink(): raise RuntimeError('Unexpected public symlink '+rel)
    b=p.read_bytes(); rows.append({'path':rel,'bytes':len(b),'sha256':digest(b)})
names={r['path'] for r in rows}
required={'REPORT.md','VERDICT.json','QUERY_LOG.json','SOURCE_COVERAGE.json','INPUT_PINS.json','PRIVATE_SOURCE_PINS.json','IMPA_AUTHOR_SOURCE_CUSTODY.json','RESEARCH_LOG.md'}
if not required<=names: raise RuntimeError('Missing public required inputs '+repr(required-names))
manifest={'schema':'pr110-exact-history-public-output-manifest/v1','UTC':utc,'actual_sealer_PID':pid,
    'public_payload_files':len(rows),'public_payload_bytes':sum(r['bytes'] for r in rows),'payload':rows,
    'exclusions':['private_sources/**','private_review_materials/**','OUTPUT_MANIFEST.json','SEAL_RECEIPT.json','actual_operations/seal_public_audit_final/**','actual_operations/verify_public_seal_final/**'],
    'exclusion_reason':'Private copyrighted/full primary bodies and evolving/self-referential closing receipts excluded. Private metadata/hash lists remain public.'}
mb=(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n').encode()
(W/'OUTPUT_MANIFEST.json').write_bytes(mb)
byname={r['path']:r for r in rows}
receipt={'schema':'pr110-exact-history-public-seal-receipt/v1','UTC':utc,'actual_sealer_PID':pid,'public_payload_files':len(rows),'public_payload_bytes':manifest['public_payload_bytes'],
    'OUTPUT_MANIFEST':{'path':'OUTPUT_MANIFEST.json','bytes':len(mb),'sha256':digest(mb)},
    'key_pins':{n:byname[n] for n in ('REPORT.md','VERDICT.json','SOURCE_COVERAGE.json','PRIVATE_SOURCE_PINS.json')},
    'all_payload_hashes_rechecked':False,'publication_authorized':False}
for r in rows:
    b=(W/r['path']).read_bytes()
    if len(b)!=r['bytes'] or digest(b)!=r['sha256']: raise RuntimeError('Seal recheck mismatch '+r['path'])
receipt['all_payload_hashes_rechecked']=True
(W/'SEAL_RECEIPT.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(receipt,ensure_ascii=False))
