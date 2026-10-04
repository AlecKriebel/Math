#!/usr/bin/env python3
"""Private byte-exact historical stdout diagnostics; no new math independence."""
from pathlib import Path
import hashlib,json
from capture_command import HERE,run
O=HERE/'original';P=HERE/'private_replays';P.mkdir(exist_ok=False)
def pin(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
jobs=[]
for name,code,reference,context in [('author_current','verify_product_vectors.py','product_verification.json',['CANDIDATE.md']),
                                  ('old_independent','review/independent_checks.py','review/independent_results.json',[])]:
    d=P/name;d.mkdir();target=d/Path(code).name;target.write_bytes((O/code).read_bytes());sources=[target]
    for n in context:
        p=d/n;p.write_bytes((O/n).read_bytes());sources.append(p)
    cap,out,err=run(name,['/usr/bin/python3','-B',str(target)],cwd=d,sources=sources)
    assert cap['exit_code']==0,(name,cap,err)
    receipt=d/Path(reference).name;receipt.write_bytes(out)
    assert out==(O/reference).read_bytes(),('receipt mismatch',name)
    result=json.loads(out);expected=1227 if name=='author_current' else 8093
    assert result['status']=='PASS' and result['exact_assertions']==expected
    jobs.append({'name':name,'capture':str(HERE/'captures'/name/'CAPTURE.json'),
                 'child_pid':cap['child_pid'],'utc_start':cap['utc_start'],'utc_end':cap['utc_end'],'argv':cap['argv'],
                 'exit_code':cap['exit_code'],'exact_assertions':expected,'sources':cap['sources'],
                 'private_stdout_receipt':pin(receipt),'exact_original_reference':pin(O/reference),'byte_equal':True,
                 'new_mathematical_independence':False})
result={'schema':'pr55-historical-helper-reproduction/v1','jobs':jobs,
 'scope':'Original-head author and archived old independent diagnostic programs, executed as private copies. Both emit receipts entirely to stdout.',
 'candidate_current_sha256':pin(O/'CANDIDATE.md')['sha256'],
 'missing_historical_inputs':['No separate earlier frozen proof or submitted verifier bodies are among the sixteen authenticated files. The exact current-head candidate still says review pending; no reconstructed older version or historical state transition is asserted.'],
 'limits':['1227 and 8093 count repeated finite diagnostic assertions, not universal theorems or new independent families.',
           'No historical source PDF hash reproduction, full GKZ audit, proof-type verdict, priority conclusion or human peer review.'],
 'new_RESPONSE_COUNT':None,'new_route_increment':False,'ROOT_acceptance':False,'new_math_verdict':None}
(HERE/'REPRODUCTION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'HISTORICAL_DIAGNOSTICS_REPRODUCED_SOURCE_ONLY','jobs':[{k:j[k] for k in ['name','child_pid','utc_start','utc_end','exit_code','exact_assertions']} for j in jobs],'new_independence':False},indent=2))
