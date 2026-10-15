#!/usr/bin/env python3
"""Replay exact original-head helpers privately; do not count new independence."""
from pathlib import Path
import hashlib,json,sys
from capture_command import run
HERE=Path(__file__).resolve().parent
O=HERE/'original';P=HERE/'private_replays';P.mkdir(exist_ok=False)
def pin(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def copy(src,dst):dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(src.read_bytes());assert dst.read_bytes()==src.read_bytes()
jobs=[('author_current',[(O/'verify.py','verify.py'),(O/'PARTIAL.md','PARTIAL.md')],
       'verify.py',['verification.json','sample_certificate.json']),
      ('old_independent',[(O/'review/independent_checks.py','independent_checks.py'),
                          (O/'review/submitted_sample_certificate.json','submitted_sample_certificate.json')],
       'independent_checks.py',['independent_results.json'])]
out=[]
for name,inputs,script,outputs in jobs:
    d=P/name;d.mkdir()
    for src,dst in inputs:copy(src,d/dst)
    sources=[d/dst for src,dst in inputs]
    cap,stdout,stderr=run(name,['/usr/bin/python3','-B',str(d/script)],cwd=d,sources=sources)
    assert cap['exit_code']==0,(name,cap,stderr)
    receipts=[]
    for fn in outputs:
        reference=O/fn if name=='author_current' else O/'review'/fn
        r=d/fn
        assert r.read_bytes()==reference.read_bytes(),('reproduction mismatch',name,fn)
        receipts.append({'private':pin(r),'exact_original_reference':pin(reference),'byte_equal':True})
    out.append({'name':name,'capture':str(HERE/'captures'/name/'CAPTURE.json'),
                'child_pid':cap['child_pid'],'utc_start':cap['utc_start'],'utc_end':cap['utc_end'],
                'argv':cap['argv'],'exit_code':cap['exit_code'],'sources':cap['sources'],
                'receipts':receipts,'new_mathematical_independence':False})
current=json.loads((O/'verification.json').read_text());frozen=json.loads((O/'review/submitted_verification.json').read_text())
delta={k:{'current':current.get(k),'archived':frozen.get(k)} for k in set(current)|set(frozen) if current.get(k)!=frozen.get(k)}
assert set(delta)=={'partial_sha256'}
assert (O/'sample_certificate.json').read_bytes()==(O/'review/submitted_sample_certificate.json').read_bytes()
assert current['partial_sha256']==hashlib.sha256((O/'PARTIAL.md').read_bytes()).hexdigest()
result={'schema':'pr54-historical-helper-reproduction/v1','scope':'Exact current original-head author helper and archived old independent helper; source preparation only.',
 'jobs':out,'current_vs_archived_author_receipt_delta':delta,
 'current_and_archived_sample_byte_equal':True,
 'missing_historical_inputs':['No separate frozen submitted_verify.py or frozen submitted PARTIAL.md is among the nineteen authenticated bodies.'],
 'qualification':'The current original-head author receipt is reproduced byte for byte. The old independent helper replays the archived certificate and reproduces its receipt byte for byte. The older author receipt has a different proof hash; no actual replay of unavailable older proof bytes is claimed.',
 'new_RESPONSE_COUNT':None,'new_route_increment':False,'ROOT_acceptance':False,'new_math_verdict':None}
(HERE/'REPRODUCTION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'HISTORICAL_HELPERS_REPRODUCED_SOURCE_ONLY','jobs':[{k:v for k,v in x.items() if k in ['name','child_pid','utc_start','utc_end','exit_code']} for x in out],
                  'author_assertions':current,'archived_receipt_delta':delta,'new_independence':False},indent=2))
