#!/usr/bin/env python3
"""Authenticate full payload and actual separate sealer/recorder after completion."""
from pathlib import Path
import hashlib,json,datetime,os
D=Path(__file__).resolve().parent
def check(v,msg):
    if not v:raise RuntimeError(msg)
def pin(p):
    b=p.read_bytes();return {'path':str(p.relative_to(D)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def matched(p,expected):
    a=pin(p);check(a['bytes']==expected['bytes'] and a['sha256']==expected['sha256'],'pin mismatch '+str(p));return a
m=json.loads((D/'OUTPUT_MANIFEST.json').read_text());s=json.loads((D/'SEAL_RECEIPT.json').read_text())
matched(D/'OUTPUT_MANIFEST.json',s['manifest'])
for row in m['payload']:matched(D/row['path'],row)
E=D/'actual_operations/final_seal';e=json.loads((E/'execution.json').read_text());start=json.loads((E/'started.json').read_text());o=json.loads((E/'stdout.bin').read_text())
check(e['exit_code']==0 and e['child_PID']==s['actual_sealer_PID']==m['actual_sealer_PID']==o['actual_sealer_PID'],'real sealer child')
check(e['child_PID']!=e['recorder_PID']==start['recorder_PID'],'separate recorder')
check(e['argv']==start['argv'] and e['cwd']==start['cwd'] and e['UTC_start']==start['UTC_start'],'start/end process')
check(datetime.datetime.fromisoformat(e['UTC_start'])<=datetime.datetime.fromisoformat(s['UTC'])<=datetime.datetime.fromisoformat(e['UTC_end']),'UTC sealer interval')
for stream in ['stdout','stderr']:matched(E/e[stream]['path'],e[stream])
for key in ['manifest','report','verdict']:matched(D/s[key]['path'],s[key]);check(o[key+'_sha256']==s[key]['sha256'],'stdout key pin')
result={'schema':'pr110-cross-family-closing-authentication/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_verifier_PID':os.getpid(),'actual_sealer_PID':e['child_PID'],'actual_closing_recorder_PID':e['recorder_PID'],'closing_exit_code':e['exit_code'],'full_payload_body_hashes_verified':len(m['payload']),'manifest':pin(D/'OUTPUT_MANIFEST.json'),'seal_receipt':pin(D/'SEAL_RECEIPT.json'),'actual_closing_execution':pin(E/'execution.json'),'excluded_from_manifest_as_closing_envelope':True,'priority_clearance':False,'publication_clearance':False}
(D/'CLOSING_AUTHENTICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':True,'actual_verifier_PID':os.getpid(),'actual_sealer_PID':e['child_PID'],'actual_recorder_PID':e['recorder_PID'],'payload_count':len(m['payload'])}))
