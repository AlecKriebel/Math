#!/usr/bin/env python3
"""Check actual saved receipt bodies and consistency before the public seal."""
from pathlib import Path
import datetime,hashlib,json,os,sys
D=Path(__file__).resolve().parent
def require(x,msg):
    if not x:raise RuntimeError(msg)
rows=[]
for p in sorted((D/'actual_operations').glob('*/execution.json')):
    r=json.loads(p.read_text());s=json.loads((p.parent/'started.json').read_text())
    require(r['UTC_start']==s['UTC_start'] and r['argv']==s['argv'],'receipt start mismatch')
    require(isinstance(r['child_PID'],int) and r['child_PID']>0,'actual child PID missing')
    for stream in ('stdout','stderr'):
        b=(p.parent/r[stream]['path']).read_bytes()
        require(len(b)==r[stream]['bytes'],'stream byte mismatch')
        require(hashlib.sha256(b).hexdigest()==r[stream]['sha256'],'stream full hash mismatch')
    rows.append({'label':p.parent.name,'child_PID':r['child_PID'],'exit_code':r['exit_code']})
expected={'download_GKR_spatial_final_alt':56,'extract_GKR_spatial_final':1,'download_Bialy_Mather':56}
failures={x['label']:x['exit_code'] for x in rows if x['exit_code']}
require(failures==expected,'documented failure set differs from actual')
ledger=json.loads((D/'SOURCE_READ_LEDGER.json').read_text())
require(len(ledger['primary_bodies'])==15,'source body count')
require(sum(x['entire'] for x in ledger['primary_bodies'])==5,'complete body count')
for source in ledger['primary_bodies']:
    for name in ('private_pdf_body_pin','private_extract_body_pin'):
        pin=source[name];b=(D/pin['path']).read_bytes()
        require(len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256'],'primary full body pin mismatch')
v=json.loads((D/'VERDICT.json').read_text())
require(v['combined_priority_clearance'] is False and v['publication_clearance'] is False,'invalid global clearance')
require(v['full_covering_prior_located'] is False and v['required_findings'][0]['id']=='M1','finding mismatch')
q=json.loads((D/'QUERY_LOG.json').read_text())
require(sum(len(b['queries']) for b in q['batches'])==63==q['query_count'],'query count')
checks=[]
for name,mode in [('TRANSFER_NORMAL.json',0),('TRANSFER_OPTIMIZED.json',1)]:
    r=json.loads((D/name).read_text());require(r['optimization']==mode and r['explicit_checks']==49 and r['status']=='passed','normal/O check mismatch')
    checks.append({'file':name,'actual_PID':r['actual_PID'],'explicit_checks':r['explicit_checks'],'optimization':mode})
result={'schema':'pr110-modern-preseal-artifact-check/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_PID':os.getpid(),'status':'passed','completed_receipts_checked':rows,'expected_failed_operations':failures,'controls':checks,'private_body_and_public_finding_consistency_checked':True,'note':'Own verification receipt is created by recorder after this child exits; public sealer independently includes and verifies it.'}
(D/'ARTIFACT_VERIFICATION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'passed','actual_PID':os.getpid(),'receipts_checked':len(rows),'private_primary_bodies':15,'essential_gap':'M1'}))
