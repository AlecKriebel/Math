#!/usr/bin/env python3
"""Run exact controls in a new isolated directory and emit a JSON report.

The scripts are copied by explicit allowlist. No source documents, datasets,
network access, external dependencies, or existing result files are needed.
"""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

SCRIPTS = ['check_transfer_and_mirror.py', 'check_signed_pencil.py',
           'verify_attempt_3.py', 'check_transition_and_mirror.py']

def main():
    package = Path(__file__).resolve().parent
    checks=[]
    with tempfile.TemporaryDirectory(prefix='quadrant-exact-replay-') as temp:
        work=Path(temp)
        for name in SCRIPTS:
            shutil.copyfile(package/name,work/name)
        for name in SCRIPTS:
            run=subprocess.run([sys.executable,'-I',name],cwd=work,
                env={'PATH':os.environ.get('PATH',''),'LC_ALL':'C.UTF-8'},
                capture_output=True,text=True,timeout=120,check=False)
            if run.returncode != 0:
                raise RuntimeError(f'{name} failed: {run.stderr}')
            if run.stderr:
                raise RuntimeError(f'{name} emitted stderr: {run.stderr}')
            if name=='check_transfer_and_mirror.py':
                data=json.loads(run.stdout)
                assert data['reverse_negation_pairs']==16
                assert data['negative_block_identity_lengths']==list(range(1,9))
                assert data['Q_n_coefficients_ascending_a']['1']==[2]
                assert data['Q_n_coefficients_ascending_a']['3']==[44,24,2]
            elif name=='check_signed_pencil.py':
                assert len(run.stdout.splitlines())==5
                assert run.stdout.count('exact agreement through length 14')==5
                assert '1, 2, 6, 22, 92, 424, 2108, 11134' in run.stdout
            elif name=='verify_attempt_3.py':
                assert 'coefficients in a+1=[210, -182, 13741]' in run.stdout
                assert 'NOT counterexamples to ABM Conjectures 10 or 11' in run.stdout
            else:
                data=json.loads(run.stdout)
                assert data['status']=='PASS'
                assert data['mirror_checks']['total_ordered_pairs']==85208
            checks.append({'script':name, 'script_sha256':hashlib.sha256((work/name).read_bytes()).hexdigest(),
                           'exit_code':run.returncode, 'stderr':run.stderr, 'stdout':run.stdout})
    print(json.dumps({'status':'PASS','checked_at_utc':datetime.now(timezone.utc).isoformat(),
                      'python_version':sys.version.split()[0], 'arithmetic':'exact integer and rational',
                      'execution':'Each allowlisted script ran with Python isolated mode in a fresh temporary directory.',
                      'claim_limit':'Finite checks support normalization and algebra; analytical proofs and audits establish the infinite results.',
                      'checks':checks},indent=2,ensure_ascii=False))

if __name__=='__main__':
    main()
