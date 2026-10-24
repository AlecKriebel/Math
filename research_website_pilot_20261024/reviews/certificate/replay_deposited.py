#!/usr/bin/env python3
"""Replay inspected deposited verifiers from private copies; preserve originals."""
from pathlib import Path
from datetime import datetime,timezone
import sys,subprocess,json,shutil,hashlib
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[1]/'sources'/'published-release'
DEST=HERE/'deposited_replay'
DEST.mkdir(exist_ok=True)
names=['verify_currents.py','check_reductions.py','square_flow_certificate.json.gz']
for name in names:
    shutil.copyfile(SOURCE/name,DEST/name)
records=[]
for script,expected in [('verify_currents.py','CURRENT_RESULTS.json'),('check_reductions.py','REDUCTION_RESULTS.json')]:
    wanted=(SOURCE/expected).read_bytes()
    for optimized in [False,True]:
        args=[sys.executable,'-I','-S','-B']+(['-O'] if optimized else [])+[script]
        proc=subprocess.run(args,cwd=DEST,capture_output=True,timeout=60,check=True)
        if proc.stdout!=wanted or proc.stderr:
            raise RuntimeError('deposited output mismatch '+script)
        label=script.replace('.py','')+('_optimized' if optimized else '')
        (DEST/(label+'.json')).write_bytes(proc.stdout)
        records.append({'script':script,'optimized':optimized,'exit_code':proc.returncode,
                        'stdout_byte_equal_deposited_result':True,'stderr_bytes':len(proc.stderr),
                        'output_sha256':hashlib.sha256(proc.stdout).hexdigest()})
result={'status':'PASS','timestamp_utc':datetime.now(timezone.utc).isoformat(),
        'python_version':sys.version,'executed_from_private_copies':True,'replays':records}
print(json.dumps(result,sort_keys=True,indent=2))
