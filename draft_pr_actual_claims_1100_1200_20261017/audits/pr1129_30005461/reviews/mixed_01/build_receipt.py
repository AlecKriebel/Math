#!/usr/bin/env python3
"""Fingerprint authored review files, excluding this receipt and private/intermediate trees."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json

here=Path(__file__).resolve().parent
receipt=here/'AUTHOR_ARTIFACT_RECEIPT.json'
excluded_prefixes=('sources/private/','tmp/','__pycache__/')
files=[]
for p in sorted(here.rglob('*')):
    if not p.is_file() or p==receipt:
        continue
    relative=p.relative_to(here).as_posix()
    if relative.startswith(excluded_prefixes):
        continue
    raw=p.read_bytes()
    files.append({'path':relative,'bytes':len(raw),'sha256':sha256(raw).hexdigest()})
expected={
'CREDITED_MIXED_EXPONENT_PROOF.md':(7385,'be068e1471372383675640c282109ae82c2c74d3856a4e6bedf046dead97473c'),
'PROOF.md':(10963,'46af7394ebfee7b0de9861693f84ab684502da3be208c626411f24e2538c7d15'),
'MATHEMATICAL_AUDIT.md':(13253,'f9faede12ad50034f5620f4576c621dc275a6ddbbf29bb3e13096d778a094cce')}
inputs=[]
for name,(size,digest) in expected.items():
    raw=(here.parent.parent/'inputs'/name).read_bytes()
    if len(raw)!=size or sha256(raw).hexdigest()!=digest:
        raise RuntimeError('frozen input identity changed: '+name)
    inputs.append({'path':'../../inputs/'+name,'bytes':size,'sha256':digest,'matches_assigned_pin':True})
checks=json.loads((here/'RUN_VALIDATION.json').read_text())
if checks.get('status')!='PASS' or not checks.get('normal_optimized_results_byte_identical'):
    raise RuntimeError('verification receipt is not PASS')
ledger=json.loads((here/'FETCH_LEDGER.json').read_text())
private=[]
for record in ledger['records']:
    if record.get('status')!=200:
        raise RuntimeError('failed source retrieval: '+record['key'])
    p=here/record['stored_path'];raw=p.read_bytes()
    if len(raw)!=record['bytes'] or sha256(raw).hexdigest()!=record['sha256']:
        raise RuntimeError('private source changed: '+record['key'])
    private.append({'key':record['key'],'identity_matches_fetch_ledger':True})
out={'schema_version':1,'created_utc':datetime.now(timezone.utc).isoformat(),
     'review':'PR1129/problem30005461/OWR-12697710-007 credited mixed odd SOS clause',
     'verdict':'PASS','completion_estimate_percent':100,
     'assigned_frozen_head':'26fed29c1130e539ba018a37200f133870f0e036',
     'head_identity_boundary':'Assigned snapshot identity; no Git references were inspected.',
     'input_pins':inputs,'authored_artifacts':files,
     'exclusions':['AUTHOR_ARTIFACT_RECEIPT.json',*excluded_prefixes],
     'private_source_identity_validation':private,
     'verification_result_sha256':checks['result_sha256'],
     'scope':'Complete arbitrary-real-polynomial mixed odd SOS exponent clause, source corrections, homogeneous reduction, and BKR threshold notation interface. Separate principal geometry and exhaustive priority are outside this verdict.',
     'external_actions':'None. No human/outside communication, Git ref/index/remote, PR, tracker, publication or release write.'}
receipt.write_text(json.dumps(out,indent=2)+'\n')
for item in files:
    if sha256((here/item['path']).read_bytes()).hexdigest()!=item['sha256']:
        raise RuntimeError('authored file changed during receipt build: '+item['path'])
print(json.dumps({'report':next(x for x in files if x['path']=='REPORT.md'),
                  'receipt':{'path':receipt.name,'bytes':receipt.stat().st_size,
                             'sha256':sha256(receipt.read_bytes()).hexdigest()},
                  'authored_artifact_count':len(files),'status':'PASS'},indent=2))
