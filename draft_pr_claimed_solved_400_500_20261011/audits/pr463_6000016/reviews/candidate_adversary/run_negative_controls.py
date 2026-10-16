#!/usr/bin/env python3
"""Test actual candidate-checker guards using private, in-memory false claims."""
import hashlib,json,subprocess,sys
from pathlib import Path
here=Path(__file__).resolve().parent
checker=here/'check_candidate.py'
source=checker.read_text()
cases=[
 ('wrong_Codazzi_sign','B.diff(x)-A.diff(y)-t*C)','B.diff(x)-A.diff(y)+t*C)'),
 ('false_Jorgens_bound_limit','s.limit(24*(r0+t0)**2*r0**2/R**2,R,s.oo),0)','s.limit(24*(r0+t0)**2*r0**2/R**2,R,s.oo),1)'),
 ('false_given_metric_parallelism','s.simplify(nonparallel.diff(x)[0,0])!=0)','s.simplify(nonparallel.diff(x)[0,0])==0)'),
]
results=[]
for label,old,new in cases:
 if source.count(old)!=1:raise RuntimeError('Mutation target is not unique: '+label)
 changed=source.replace(old,new)
 wrapper='ns={"__file__":'+repr(str(checker))+'};exec(compile('+repr(changed)+','+repr(str(checker))+',"exec"),ns)'
 for mode in [[],['-O']]:
  r=subprocess.run([sys.executable,*mode,'-c',wrapper],cwd=here/'private_cases',capture_output=True)
  if r.returncode==0 or r.stdout or b'RuntimeError' not in r.stderr:raise RuntimeError('Invalid claim was not rejected: '+label)
  results.append({'case':label,'mode':'optimized' if mode else 'normal','exit_code':r.returncode,'success_stdout_bytes':len(r.stdout),'error_class':'RuntimeError'})
if checker.read_text()!=source:raise RuntimeError('Checker changed')
print(json.dumps({'status':'PASS','actual_rejections':len(results),'source_sha256':hashlib.sha256(source.encode()).hexdigest(),'results':results,'limitations':'These deliberately false controls exercise guards; they do not establish the historical PDE theorems or exhaust all possible defects.'},indent=2,sort_keys=True))
