#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys
P=Path(__file__).resolve().parent
RUNTIME=P.parent.parent/'pr200_5100007/math_algebra_family_01/runtime_packages'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(RUNTIME))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=['exact_low_period.py'] if '--only-exact' in sys.argv else (['physical_shooting.py'] if '--only-physical' in sys.argv else ['physical_shooting.py','exact_low_period.py'])
receipts=json.loads((P/'authored_execution_receipts.json').read_text()) if (P/'authored_execution_receipts.json').exists() else []
receipts=[r for r in receipts if not any(r['name'].startswith(Path(f).stem+'_') for f in files)]
for file in files:
 for false in [False,True]:
  for opt in [False,True]:
   name=Path(file).stem+('_false_identity' if false else '')+('_optimized' if opt else '_ordinary')
   cmd=[sys.executable]+(['-O'] if opt else [])+[str(P/file)]+(['--false-identity'] if false else [])
   start=datetime.now(timezone.utc).isoformat();r=subprocess.run(cmd,env=env,cwd=P,text=True,capture_output=True)
   (P/(name+'.stdout')).write_text(r.stdout);(P/(name+'.stderr')).write_text(r.stderr)
   if r.returncode!=(1 if false else 0):raise RuntimeError('Unexpected exit '+name+' '+r.stderr)
   receipt={'name':name,'UTC_start':start,'UTC_end':datetime.now(timezone.utc).isoformat(),'argv':cmd,'implementation_sha256':sha(P/file),'exit_code':r.returncode,'stdout_file':name+'.stdout','stdout_sha256':sha(P/(name+'.stdout')),'stderr_file':name+'.stderr','stderr_sha256':sha(P/(name+'.stderr')),'expected_false_mathematical_identity_rejected':false and r.returncode==1}
   receipts.append(receipt);(P/'authored_execution_receipts.json').write_text(json.dumps(receipts,indent=2)+'\n');print(name+' exit='+str(r.returncode),flush=True)
for file in ['physical_shooting','exact_low_period']:
 if (P/(file+'_ordinary.stdout')).read_bytes()!=(P/(file+'_optimized.stdout')).read_bytes():raise RuntimeError('Normal/-O valid output differs '+file)
print('All authored mode and false-identity controls agree.',flush=True)
