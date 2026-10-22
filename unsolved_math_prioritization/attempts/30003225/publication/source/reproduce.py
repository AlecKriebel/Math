"""Read source integrity and execute complete exact diagnostics in 3 modes.

No service or network operation; suppresses bytecode writes. Optional package
rebuilding is a separate explicit invocation of build_package.py.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys


def require(ok,message):
    if not ok:
        raise RuntimeError(message)


def main():
    root=Path(__file__).resolve().parent
    raw=(root/'build_package.py').read_bytes()
    scope={'__file__':str(root/'build_package.py'),'__name__':'local_integrity_checker'}
    exec(compile(raw,str(root/'build_package.py'),'exec'),scope)
    members=scope['validate'](root)
    receipts=[]
    for program,expected in [('exact_checks.py','CHECK_RESULTS.json'),('run_mutations.py','MUTATIONS.json')]:
        wanted=(root/'verification'/expected).read_bytes()
        for mode in [[],['-O'],['-OO']]:
            result=subprocess.run([sys.executable,'-I','-S','-B',*mode,str(root/'verification'/program)],capture_output=True)
            require(result.returncode==0 and result.stdout==wanted and result.stderr==b'',program+' complete execution mismatch '+str(mode))
        receipts.append({'program':program,'normal_O_OO_complete_equal':True,'stdout_bytes':len(wanted),'stdout_sha256':hashlib.sha256(wanted).hexdigest()})
    print(json.dumps({'status':'PASS','source_members_including_manifest':len(members)+1,'executions':receipts,'fresh_typesetting_performed':False,'scope':'Exact finite diagnostics and source integrity; universal proofs and priority require independent mathematical/source reading.'},sort_keys=True,indent=2))


if __name__=='__main__':
    main()
