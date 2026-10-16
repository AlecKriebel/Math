#!/usr/bin/env python3
"""Read-only replication, math and custody checked independently of adjacent files."""
import hashlib,json,subprocess,sys
from pathlib import Path

root=Path(__file__).absolute().parent
out={}
for optimized in (False,True):
    mode='optimized' if optimized else 'normal'
    prefix=[sys.executable,'-B']+(['-O'] if optimized else [])
    math_result=subprocess.run(prefix+[str(root/'exact_combinatorics.py'),str(root/'WITNESS_INPUT.json')],
                               check=True,capture_output=True).stdout
    if math_result!=(root/'EXACT_RESULTS.json').read_bytes():
        raise ValueError('finite results differ under '+mode)
    sep_result=subprocess.run(prefix+[str(root/'separated_controls.py')],check=True,capture_output=True).stdout
    control_result=subprocess.run(prefix+[str(root/'verify_custody.py'),'--selftest'],check=True,capture_output=True).stdout
    custody_result=subprocess.run(prefix+[str(root/'verify_custody.py')],check=True,capture_output=True).stdout
    out[mode]={'finite_sha256':hashlib.sha256(math_result).hexdigest(),
               'separated_sha256':hashlib.sha256(sep_result).hexdigest(),
               'positive_controls':json.loads(sep_result),
               'custody_controls':json.loads(control_result),
               'custody':json.loads(custody_result)}
if out['normal']!=out['optimized']:
    raise ValueError('normal and optimized results differ')
print(json.dumps({'status':'PASS','modes':out},sort_keys=True,indent=2))
