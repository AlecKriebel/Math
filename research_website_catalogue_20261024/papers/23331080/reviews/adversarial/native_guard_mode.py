#!/usr/bin/env python3
"""Observe native assert semantics on a wrong initial weight, in memory."""
from pathlib import Path
import json, subprocess, sys
sys.dont_write_bytecode=True
p=Path(__file__).resolve().parent/'cache/replay/author/verify.py';raw=p.read_text()
old='d*u/(1+u)*(v/(1+v))**2';new='d*u/(1+u)*(v/(1+v))**3'
if raw.count(old)!=1:raise RuntimeError('nonunique native wrong-weight fault site')
launch='exec(compile('+repr(raw.replace(old,new))+','+repr(str(p))+',"exec"),{"__name__":"__main__","__file__":'+repr(str(p))+'})'
records=[]
for opt in [False,True]:
 r=subprocess.run([sys.executable,'-B']+(['-O'] if opt else [])+['-c',launch],capture_output=True,text=True,timeout=30)
 if not opt and not(r.returncode!=0 and 'AssertionError' in r.stderr):raise RuntimeError('native normal wrong-weight guard failed')
 if opt and not(r.returncode==0 and json.loads(r.stdout)['status']=='PASS'):raise RuntimeError('native optimized assert semantics changed')
 records.append({'optimized':opt,'exit_code':r.returncode,'wrong_initial_weight_rejected':r.returncode!=0,'literal_stdout_status':json.loads(r.stdout)['status'] if r.returncode==0 else None,'last_stderr_line':r.stderr.splitlines()[-1] if r.stderr else None})
if p.read_text()!=raw:raise RuntimeError('native isolated copy changed')
print(json.dumps({'assessment':'NATIVE_ASSERT_GUARDS_REQUIRE_NORMAL_EXECUTION_FOR_MATHEMATICAL_VALIDATION','records':records,'optimized_literal_PASS_is_validation':False,'source_modified':False,'scope':'Native instructions use normal Python; a wrong initial-weight exponent is rejected normally but receives literal PASS after optimization removes assert. This documents an execution-mode limitation, not a target counterexample or source repair.'},indent=2,sort_keys=True))
