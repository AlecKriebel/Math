#!/usr/bin/env python3
"""Independently rerun ideal-certificate scripts on an ignored copied tree."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

HERE=Path(__file__).resolve().parent
SCRATCH=HERE.parent.parents[2]/'tmp/reproduction/pr11_exact_family/certificate_copy'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    original=HERE/'ideal_certificate'
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    shutil.copytree(original,SCRATCH)
    outputs=[]
    for script,result in [('check_certificates.py','CHECK_RESULTS.json'),
            ('gorenstein_falsifier/verify_identities.py',
             'gorenstein_falsifier/verification_result.json')]:
        before=sha(original/script)
        process=subprocess.run([sys.executable,str(SCRATCH/script)],
            check=True,capture_output=True,text=True)
        old=json.loads((original/result).read_text())
        new=json.loads((SCRATCH/result).read_text())
        old.pop('timestamp_UTC',None)
        new.pop('timestamp_UTC',None)
        assert old==new
        assert before==sha(original/script)==sha(SCRATCH/script)
        outputs.append({'script':script,'script_sha256':before,
            'exit_code':process.returncode,'stderr':process.stderr,
            'mathematical_output_equal':True,
            'mathematical_payload_sha256':hashlib.sha256(
                json.dumps(new,sort_keys=True).encode()).hexdigest()})
    payload={'timestamp_utc':datetime.now(timezone.utc).isoformat(),
        'status':'PASS','scope':'Finite polynomial identities/models; exactness proved in reports.',
        'reruns':outputs}
    (HERE/'certificate_reproduction_results.json').write_text(json.dumps(payload,indent=2)+'\n')
    print('PASS 2 independently copied certificate reruns; mathematical outputs identical')

if __name__=='__main__':
    main()
