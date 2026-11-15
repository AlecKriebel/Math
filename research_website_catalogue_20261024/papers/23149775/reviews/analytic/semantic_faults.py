#!/usr/bin/env python3
"""In-memory faults in the independent exact/complex checks; no file mutation."""
from pathlib import Path
import sys,subprocess,json
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
cases=[('wrong double-pole sign','independent_exact.py','C=1-z*z/2','C=1+z*z/2','original double-pole leading x'),('wrong outer residue sign','independent_exact.py','x/(-br2*S)','x/(br2*S)','outer simple-pole residue'),('wrong triangular multiplier','independent_exact.py','bp-(t+1)**3*ap/(2*t)','bp-(t+1)**2*ap/(2*t)','general triangular multiplier for both foci'),('missing chord midpoint','independent_complex.py','q(w+v+j*d)','q(w+j*d)','actual chord feet equal midpoint trace'),('missing opposite-focus phase','independent_complex.py','w+(0 if sign==1 else 2*K)','w','actual chord feet equal midpoint trace')]
out=[]
for name,file,old,new,reason in cases:
 p=R/file;raw=p.read_text()
 if raw.count(old)!=1:raise RuntimeError('nonunique fault site '+name)
 changed=raw.replace(old,new)
 launch='import sys;sys.argv=['+repr(str(p))+'];exec(compile('+repr(changed)+','+repr(str(p))+',"exec"),{"__file__":'+repr(str(p))+',"__name__":"__main__"})'
 for opt in [False,True]:
  a=subprocess.run([sys.executable,'-B']+(['-O'] if opt else [])+['-c',launch],capture_output=True,text=True,timeout=30)
  last=a.stderr.splitlines()[-1] if a.stderr else ''
  if a.returncode==0 or last!='RuntimeError: '+reason:raise RuntimeError('unintended fault result '+name+' '+last)
  out.append({'fault':name,'optimized':opt,'exit_code':a.returncode,'expected_rejection':reason,'last_stderr_line':last,'stdout':a.stdout})
 if p.read_text()!=raw:raise RuntimeError('pristine payload changed')
print(json.dumps({'assessment':'SEMANTIC_POLE_PHASE_AND_MULTIPLIER_FAULTS_REJECTED','fault_sites':len(cases),'executions':len(out),'source_or_pristine_payloads_mutated':False,'records':out},indent=2,sort_keys=True))
