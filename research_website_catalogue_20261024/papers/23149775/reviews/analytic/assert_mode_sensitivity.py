#!/usr/bin/env python3
"""Document original assert semantics with a wrong scalar, without editing bytes."""
from pathlib import Path
import subprocess,sys,json
sys.dont_write_bytecode=True
p=Path(__file__).resolve().parent/'cache/replay/verify_exact.py';raw=p.read_text();old='s.Rational(125,24)*Aq';new='s.Rational(126,24)*Aq'
if raw.count(old)!=1:raise RuntimeError('nonunique native fault site')
launch='exec(compile('+repr(raw.replace(old,new))+','+repr(str(p))+',"exec"),{"__file__":'+repr(str(p))+',"__name__":"__main__"})'
records=[]
for opt in [False,True]:
 a=subprocess.run([sys.executable,'-B']+(['-O'] if opt else [])+['-c',launch],capture_output=True,text=True,timeout=30)
 if not opt and not(a.returncode!=0 and 'AssertionError' in a.stderr):raise RuntimeError('native normal guard did not reject wrong multiplier')
 if opt and not(a.returncode==0 and json.loads(a.stdout)['status']=='PASS'):raise RuntimeError('native optimized behavior differed from assert semantics')
 records.append({'optimized':opt,'exit_code':a.returncode,'wrong_scalar_rejected':a.returncode!=0,'last_stderr_line':a.stderr.splitlines()[-1] if a.stderr else None,'literal_stdout_status':json.loads(a.stdout)['status'] if a.returncode==0 else None})
if p.read_text()!=raw:raise RuntimeError('native isolated copy changed')
print(json.dumps({'assessment':'NATIVE_ASSERT_CHECKER_VALIDATION_REQUIRES_NORMAL_MODE','records':records,'source_program_modified':False,'optimized_output_is_not_mathematical_validation':True,'scope':'The published instructions use normal Python. This documents an execution-mode limitation; it is not a mathematical counterexample or a manuscript repair.'},indent=2,sort_keys=True))
