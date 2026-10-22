#!/usr/bin/env python3
"""Run real independent Python processes; preserve diagnostics and exact hashes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,subprocess,sys
base=Path(__file__).resolve().parent
sys.path.insert(0,str(base))
import verify_symbols
rows=[];positive=[]
for optimized in (False,True):
 flags=['-O'] if optimized else []
 cmd=[sys.executable,*flags,str(base/'verify_symbols.py')]
 r=subprocess.run(cmd,capture_output=True)
 if r.returncode:raise RuntimeError(r.stderr.decode())
 output=base/('CHECKS_OPTIMIZED.json' if optimized else 'CHECKS_NORMAL.json')
 output.write_bytes(r.stdout);positive.append(r.stdout)
 rows.append({'mode':'optimized' if optimized else 'normal','case':'correct','exit_code':r.returncode,'stdout_bytes':len(r.stdout),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_bytes':len(r.stderr)})
 for name in verify_symbols.WRONG:
  neg=subprocess.run([*cmd,'--wrong',name],capture_output=True)
  if neg.returncode==0:raise RuntimeError('Wrong alternative passed: '+name)
  if b'ValueError: CHECK FAILED:' not in neg.stderr:raise RuntimeError('Unexpected failure, not an actual check: '+neg.stderr.decode())
  rows.append({'mode':'optimized' if optimized else 'normal','case':name,'exit_code':neg.returncode,'stderr_bytes':len(neg.stderr),'stderr_sha256':hashlib.sha256(neg.stderr).hexdigest(),'failure_diagnostic':neg.stderr.decode().splitlines()[-1]})
if positive[0]!=positive[1]:raise RuntimeError('normal/optimized output differs')
obj={'utc':datetime.now(timezone.utc).isoformat(),'normal_optimized_positive_outputs_identical':True,'actual_wrong_result_process_failures':len(rows)-2,'runs':rows,'limit':'Negative alternatives test representative differential/algebra identities. None is a general Kato-cohomology decision algorithm or arbitrary algorithm-mutation coverage.'}
(base/'EXECUTION_RECEIPT.json').write_text(json.dumps(obj,indent=2)+'\n')
print(json.dumps({'positive_modes':2,'actual_wrong_result_process_failures':len(rows)-2,'positive_output_bytes':len(positive[0]),'positive_output_sha256':hashlib.sha256(positive[0]).hexdigest()},indent=2))
