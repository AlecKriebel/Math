#!/usr/bin/env python3
"""Actual private repeats of original diagnostics; no new math independence."""
from pathlib import Path
import hashlib,json,sys
from capture_command import HERE,run
O=HERE/'original';P=HERE/'private_replays';P.mkdir(exist_ok=False)
def pin(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
frozen=[]
for name in ['CANDIDATE.md','verify.py','verification.json']:
    a=O/name;b=O/'independent_review/author_replay'/name
    assert a.read_bytes()==b.read_bytes(),('current versus frozen differs',name)
    frozen.append({'current':pin(a),'archived_author_replay':pin(b),'byte_equal':True})
jobs=[]
for name,code,reference,context in [('author_current','verify.py','verification.json',['CANDIDATE.md']),
                                  ('old_independent','independent_review/independent_checks.py','independent_review/independent_results.json',[])]:
    d=P/name;d.mkdir();target=d/Path(code).name;target.write_bytes((O/code).read_bytes());sources=[target]
    for n in context:
        p=d/n;p.write_bytes((O/n).read_bytes());sources.append(p)
    cap,out,err=run(name,['/usr/bin/python3','-B',str(target)],cwd=d,sources=sources)
    if cap['exit_code']!=0:raise RuntimeError((name,'actual nonzero exit; complete capture retained'))
    receipt=d/Path(reference).name;receipt.write_bytes(out)
    assert out==(O/reference).read_bytes(),('receipt mismatch',name)
    result=json.loads(out);key='assertions' if name=='author_current' else 'exact_assertions';expected=90 if name=='author_current' else 136
    assert result['status']=='PASS' and result[key]==expected and result['sympy_version']=='1.14.0'
    jobs.append({'name':name,'capture':str(HERE/'captures'/name/'CAPTURE.json'),
      'child_pid':cap['child_pid'],'utc_start':cap['utc_start'],'utc_end':cap['utc_end'],'argv':cap['argv'],
      'exit_code':cap['exit_code'],'bounded_assertion_key':key,'bounded_assertions':expected,'sources':cap['sources'],
      'private_stdout_receipt':pin(receipt),'exact_original_reference':pin(O/reference),'byte_equal':True,
      'new_mathematical_independence':False})
result={'schema':'pr57-historical-helper-reproduction/v1','jobs':jobs,
 'actual_orchestration_python':sys.version,'sympy_version_in_both_outputs':'1.14.0',
 'scope':'Original-head author and historical reviewer code executed as private copies; complete output is stdout.',
 'frozen_author_replay_body_comparison':frozen,'separate_archived_author_replay_process_claimed':False,
 'artifact_current_sha256':pin(O/'CANDIDATE.md')['sha256'],
 'historical_missing_inputs':['No earlier differing proof/helper body is reconstructed; complete archived author-replay proof, verifier and receipt are actually present and byte-identical to current original bodies.'],
 'limits':['90 and 136 count repeated bounded symbolic/algebraic controls, not a new independent family or universal analytic proof.',
 'Finite homogeneity/jet ranges and 98 scaled profile samples do not establish all-r estimates, nonlinear uniform curvature positivity, completeness, source scope or priority.',
 'No historical PDF checksum reproduction, complete published proof audit, formal verification or human peer review.'],
 'new_response_or_route_increment':False,'ROOT_acceptance':False,'new_math_verdict':None}
with (HERE/'REPRODUCTION.json').open('x') as f:f.write(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'HISTORICAL_DIAGNOSTICS_REPRODUCED_SOURCE_ONLY','jobs':[{k:j[k] for k in ['name','child_pid','utc_start','utc_end','exit_code','bounded_assertions']} for j in jobs],
 'frozen_author_replay_bodies_byte_identical':True,'new_independence':False},indent=2))
