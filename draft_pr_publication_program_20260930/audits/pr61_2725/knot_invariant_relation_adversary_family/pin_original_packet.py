#!/usr/bin/env python3
"""Read-only dated authentication of final external original SOURCE metadata."""
import datetime,hashlib,json,os,pathlib,stat
root=pathlib.Path(__file__).resolve().parent
source=root.parent/'original_preparation_family'
expected={'SOURCE.json':'e08ae1c73e4af512abf8e99d8c4f618a698ced15549fad7b3137c06ba66c8564','READY.json':'5dd8aa25fa5eee89f9c95e45ca80b1ec4d4897a31df9d7b7731317d83c1fe1ce'}
files=[]
for name,want in expected.items():
 p=source/name;b=p.read_bytes();s=p.lstat()
 assert hashlib.sha256(b).hexdigest()==want and stat.S_IMODE(s.st_mode)==0o444
 files.append({'path':str(p),'bytes':len(b),'sha256':want,'full_mode_07777':oct(stat.S_IMODE(s.st_mode))})
ready=json.loads((source/'READY.json').read_bytes())
assert ready['head']=='b5a4829365f2a0bd5f42b7653c5cfacfa6b01d85'
assert ready['original_campaign_proof_attempts']==0 and ready['budget_limit']==5
assert ready['original_scientific_files']==10 and ready['changed_files']==11
assert ready['ROOT_custody_claimed'] is False and ready['ROOT_scientific_approval_claimed'] is False
record={'schema':'pr61-final-original-external-SOURCE-reference/v1','actual_reader_pid':os.getpid(),'read_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'external_files':files,'role':'SOURCE metadata reference only','no_mathematical_credit':True,'no_preparer_ROOT_closure_inferred':True,'no_ROOT_mathematical_approval_inferred':True,'no_historical_review_body_read':True}
body=json.dumps(record,indent=2)+'\n'
assert not (root/'SOURCE_PACKET_REFERENCE.json').exists()
(root/'SOURCE_PACKET_REFERENCE.json').write_text(body)
print(body,end='')
