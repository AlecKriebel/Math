#!/usr/bin/env python3
"""Falsify six relevant mistakes in memory; pristine files never mutated."""
from pathlib import Path
import json, subprocess, sys
sys.dont_write_bytecode=True
p=Path(__file__).resolve().parent/'independent_exact.py'; raw=p.read_text()
faults=[
 ('same-convention rank-two reaction','reaction=s.Integer(1)','reaction=s.Integer(2)','stationary product constant jet calibration'),
 ('omitted evolving integral','def mean(a):return s.integrate(a,(x,0,1))','def mean(a):return s.Integer(0)','stationary product constant jet calibration'),
 ('nonuniform probability pushforward','def mean(a):return s.integrate(a,(x,0,1))','def mean(a):return s.integrate(2*x*a,(x,0,1))','normalized first-moment neutral mode'),
 ('discarded mixed curvature','Q=4*d*d*p*(1-p)*x**3*(1-x)','Q=s.Integer(0)','all-phase chart mixed Hessian'),
 ('wrong second-mode decay','eq(-2*q*s.diff(w,q),G(w),','eq(-3*q*s.diff(w,q),G(w),','exact nonlinear-family closed jet equation'),
 ('untransformed infinity chart','pp=1/(1+uu) if bi else uu/(1+uu)','pp=uu/(1+uu)','all-phase chart base Hessian')]
records=[]
for name,old,new,why in faults:
 if raw.count(old)!=1:raise RuntimeError('nonunique fault site '+name)
 altered=raw.replace(old,new)
 launch='exec(compile('+repr(altered)+','+repr(str(p))+',"exec"),{"__name__":"__main__","__file__":'+repr(str(p))+'})'
 for opt in [False,True]:
  r=subprocess.run([sys.executable,'-B']+(['-O'] if opt else [])+['-c',launch],capture_output=True,text=True,timeout=30)
  if r.returncode==0 or 'RuntimeError: '+why not in r.stderr:raise RuntimeError('fault not rejected as intended '+name)
  records.append({'fault':name,'optimized':opt,'exit_code':r.returncode,'expected_rejection':why,'last_stderr_line':r.stderr.splitlines()[-1],'stdout':r.stdout})
if p.read_text()!=raw:raise RuntimeError('pristine independent checker changed')
print(json.dumps({'assessment':'SIX_NORMALIZATION_PROBABILITY_MIXED_ATLAS_AND_RATE_FAULTS_REJECTED_IN_BOTH_MODES','fault_sites':6,'executions':12,'records':records,'source_or_pristine_files_mutated':False},indent=2,sort_keys=True))
