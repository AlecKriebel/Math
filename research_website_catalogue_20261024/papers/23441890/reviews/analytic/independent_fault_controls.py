#!/usr/bin/env python3
"""Execute five semantic mutations in memory; never modify a target file."""
from pathlib import Path
import hashlib,json,subprocess,sys
sys.dont_write_bytecode=True
here=Path(__file__).resolve().parent
target=here/'independent_exact.py'
original=target.read_text()
mutants=[
 ('reversed full-piece composition','self(g(x))','g(self(x))','conjugated full support preimage'),
 ('reversed alpha conjugation','return h.inverse().compose(f.compose(h))','return h.compose(f.compose(h.inverse()))','conjugated full support preimage'),
 ('wrong segment mixture','(up-ratio)/(up-lo)','(up-ratio)/(2*up-lo)','segment dyadic slopes'),
 ('identity bump midpoint','a+2*d/3','a+d/3','exact bump support and first germ'),
 ('wrong next-cell exponent','hn1=h.power(n+1)','hn1=h.power(n)','exact bilateral next-cell conjugation diagram'),
]
out=[]
for name,old,new,reason in mutants:
 if original.count(old)!=1:raise RuntimeError('mutation site not unique: '+name)
 source=original.replace(old,new)
 launcher='import sys;sys.argv=['+repr(str(target))+'];exec(compile('+repr(source)+','+repr(str(target))+',"exec"),{"__file__":'+repr(str(target))+',"__name__":"__main__"})'
 for optimized in [False,True]:
  args=[sys.executable,'-B']+(['-O'] if optimized else [])+['-c',launcher]
  p=subprocess.run(args,text=True,capture_output=True,timeout=30)
  if p.returncode==0 or ('RuntimeError: '+reason) not in p.stderr:raise RuntimeError('mutant not rejected for expected mathematical reason: '+name+' '+p.stderr)
  out.append({'mutation':name,'optimized':optimized,'exit_code':p.returncode,'expected_rejection':reason,'stdout':p.stdout,'last_stderr_line':p.stderr.splitlines()[-1]})
if hashlib.sha256(target.read_bytes()).hexdigest()!=hashlib.sha256(original.encode()).hexdigest():raise RuntimeError('target changed')
print(json.dumps({'assessment':'SEMANTIC_CONSTRUCTION_MUTATIONS_REJECTED','executions':len(out),'mutation_sites':len(mutants),'source_files_modified':False,'records':out},indent=2,sort_keys=True))
