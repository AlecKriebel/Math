#!/usr/bin/env python3
"""Seal every public complete body; keep copyrighted sources private."""
from pathlib import Path
import datetime,hashlib,json,os
D=Path(__file__).resolve().parent
private={'private_sources','private_review_materials'}
closing={'OUTPUT_MANIFEST.json','SEAL_RECEIPT.json'}
closing_operation='actual_operations/seal_public_payload'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
    b=p.read_bytes();return {'path':str(p.relative_to(D)),'bytes':len(b),'sha256':sha(b)}
def excluded(rel):
    return rel.parts[0] in private or str(rel) in closing or str(rel)==closing_operation or str(rel).startswith(closing_operation+'/')
# Verify all completed genuine process streams before including their metadata.
receipt_count=0
for p in sorted((D/'actual_operations').glob('*/execution.json')):
    if p.parent.name=='seal_public_payload':continue
    r=json.loads(p.read_text())
    for stream in ('stdout','stderr'):
        b=(p.parent/r[stream]['path']).read_bytes()
        if len(b)!=r[stream]['bytes'] or sha(b)!=r[stream]['sha256']:
            raise RuntimeError('process stream changed '+str(p))
    receipt_count+=1
rows=[]
for p in sorted(D.rglob('*')):
    if not p.is_file():continue
    rel=p.relative_to(D)
    if excluded(rel):continue
    if p.is_symlink():raise RuntimeError('unexpected public symlink')
    if p.suffix in {'.pdf','.png','.jpg','.jpeg','.webp','.html','.tex'}:
        raise RuntimeError('unexpected private/body/artifact format in public payload '+str(rel))
    rows.append(pin(p))
utc=datetime.datetime.now(datetime.timezone.utc).isoformat();pid=os.getpid()
manifest={
 'schema':'pr110-modern-public-full-body-manifest/v1','UTC':utc,'actual_sealer_PID':pid,
 'public_payload_count':len(rows),'public_payload_bytes':sum(x['bytes'] for x in rows),
 'public_payload_bodies':rows,
 'private_folders_excluded':sorted(private),
 'closing_envelope_excluded':['OUTPUT_MANIFEST.json','SEAL_RECEIPT.json','actual_operations/seal_public_payload/**'],
 'closing_note':'Manifest and receipt cannot contain their own hashes. Recorder closing execution data is written only after this actual sealer child exits; root must independently authenticate that closing envelope.',
 'actual_completed_operation_receipts_verified':receipt_count,
 'priority_clearance':False,'publication_clearance':False,'essential_unread_final_gap':'M1'
}
mp=D/'OUTPUT_MANIFEST.json'
mp.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
receipt={
 'schema':'pr110-modern-public-seal-receipt/v1','UTC':utc,'actual_sealer_PID':pid,
 'manifest_body_pin':pin(mp),'report_body_pin':pin(D/'REPORT.md'),'verdict_body_pin':pin(D/'VERDICT.json'),
 'private_metadata_pin':pin(D/'PRIVATE_MATERIAL_PINS.json'),
 'public_payload_count':len(rows),'all_public_payload_full_bodies_hashed':True,
 'private_source_text_pixels_and_raw_web_results_redistributed':False,
 'essential_unread_final_gap':'M1','combined_priority_clearance':False,'publication_clearance':False,
 'closing_envelope_rule':manifest['closing_note']
}
(D/'SEAL_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
# Re-read every payload after all sealing writes.
for row in rows:
    p=D/row['path'];b=p.read_bytes()
    if len(b)!=row['bytes'] or sha(b)!=row['sha256']:raise RuntimeError('postseal mismatch')
print(json.dumps({'status':'sealed','actual_sealer_PID':pid,'UTC':utc,'public_payload_count':len(rows),
'report_sha256':receipt['report_body_pin']['sha256'],'verdict_sha256':receipt['verdict_body_pin']['sha256'],
'manifest_sha256':receipt['manifest_body_pin']['sha256'],'priority_clearance':False,'essential_gap':'M1'}))
