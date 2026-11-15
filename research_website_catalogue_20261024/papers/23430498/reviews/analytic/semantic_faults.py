#!/usr/bin/env python3
"""In-memory semantic faults; no source or pristine payload is modified."""
from pathlib import Path
import subprocess,sys,json,hashlib
sys.dont_write_bytecode=True
p=Path(__file__).with_name('independent_exact.py').resolve();original=p.read_text()
cases=[('wrong Artin conjugation','((i,i+1,-i),(i,))','((-i,i+1,i),(i,))','complete Artin conjugator identity'),('missing inverse Magnus quadratic term','gen[(abs(x),abs(x))]=1','gen[(abs(x),abs(x))]=0','full truncated Magnus polynomial'),('incorrect right multiplication order','range(len(w)-1,-1,-1)','range(len(w))','entire 128-term cyclic trace polynomial'),('wrong wheel coefficient',"('112212','2'):3","('112212','2'):2",'entire 128-term cyclic trace polynomial'),('collapsed component values','bottom=[[0,0,1],[1,5,0],[5,1,0]]','bottom=[[0,0,1],[1,1,0],[1,1,0]]','parametric six-row block determinant proof')]
records=[]
for name,old,new,reason in cases:
 if original.count(old)!=1:raise RuntimeError('mutation site not unique: '+name)
 changed=original.replace(old,new)
 launch='import sys;sys.argv=['+repr(str(p))+'];exec(compile('+repr(changed)+','+repr(str(p))+',"exec"),{"__name__":"__main__","__file__":'+repr(str(p))+'})'
 for opt in [False,True]:
  a=subprocess.run([sys.executable,'-B']+(['-O'] if opt else [])+['-c',launch],capture_output=True,text=True,timeout=30)
  last=a.stderr.splitlines()[-1] if a.stderr else ''
  if a.returncode==0 or last!='RuntimeError: '+reason:raise RuntimeError('unexpected mutation result: '+name+' '+last)
  records.append({'fault':name,'optimized':opt,'exit_code':a.returncode,'expected_check':reason,'last_stderr_line':last,'stdout':a.stdout})
if p.read_text()!=original:raise RuntimeError('pristine program changed')
print(json.dumps({'assessment':'SEMANTIC_ALGEBRAIC_MUTATIONS_REJECTED','fault_sites':len(cases),'executions':len(records),'payloads_modified':False,'records':records},indent=2,sort_keys=True))
