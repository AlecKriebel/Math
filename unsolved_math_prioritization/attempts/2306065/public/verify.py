#!/usr/bin/env python3
"""Execute exact verifiers and two simple rejection controls."""
import json, tempfile, shutil, subprocess, sys
from pathlib import Path
from verify_witness import verify as witness
from verify_upper import verify as upper
from verify_algebra import verify as algebra


def rejected(script,target,mutate):
    base=Path(__file__).parent
    with tempfile.TemporaryDirectory() as d:
        d=Path(d)
        for name in [script,target]:shutil.copy2(base/name,d/name)
        obj=json.loads((d/target).read_text());mutate(obj);(d/target).write_text(json.dumps(obj))
        r=subprocess.run([sys.executable,str(d/script)],capture_output=True,text=True,timeout=60)
        assert r.returncode!=0, 'invalid fixture was accepted'
        return True

if __name__=='__main__':
    result={'witness':witness(),'upper':upper(),'algebra':algebra()}
    result['negative_controls']={
      'zero_witness_rejected':rejected('verify_witness.py','WITNESS.json',lambda o:o.update(coefficient_numerators=[0]*40)),
      'missing_upper_slab_rejected':rejected('verify_upper.py','UPPER_CERTIFICATE.json',lambda o:o['rows'].pop())}
    result['limits']='Exact arithmetic checks for the encoded partial bounds only; no mechanical verification of complex-analysis dependencies or global sharpness.'
    print(json.dumps(result,indent=2))
