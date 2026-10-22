#!/usr/bin/env python3
"""Bounded diagnostic scan; output is not a proof certificate."""
import numpy as np
from numpy.polynomial import Polynomial as P
from pathlib import Path
import json,random
rng=random.Random(30003518)
x=P([0.,1.]);found=[];maxcount=0
for trial in range(12000):
 # All rates are positive rational powers of two; original rates recovered below.
 exponents=[rng.randrange(-8,9) for _ in range(10)]
 a0,a1,q0,q1,d0,d1,d2,Et,Rt,kappa=[2.**a for a in exponents];Mt=Rt
 e=Et*x;Q=d1+q1*e;g=a0*Q+a1*q0*e;h=Q+q0*e+(q0*q1/d2)*e*e+e*g
 A=Rt*e*g-(Et-e)*h;F=kappa*A*A-(d0+q0*e)*(Et-e)*Q*e*g
 roots=F.roots();physical=[]
 for root in roots:
  if abs(root.imag)>1e-7 or not 0<root.real<1:continue
  ee=Et*root.real;gg=a0*(d1+q1*ee)+a1*q0*ee
  c0=(Et-ee)*(d1+q1*ee)/(ee*gg);c1=(Et-ee)*q0/gg;c2=(Et-ee)*q0*q1*ee/(d2*gg)
  b0=a0*ee*c0;b1=a1*ee*c1;W=c0+c1+c2+b0+b1
  if not 0<W<Rt:continue
  rr=Rt-W;res=kappa*rr*rr-(d0+q0*ee)*c0
  if abs(res)>1e-5*max(1,kappa*rr*rr,(d0+q0*ee)*c0):continue
  physical.append({'e':ee,'C':[c0,c1,c2],'B':[b0,b1],'free':rr,'residual':res})
 if len(physical)>maxcount:maxcount=len(physical)
 if len(physical)>=3:
  result={'trial':trial,'exponents':exponents,'parameters':dict(zip(['a0','a1','q0','q1','d0','d1','d2','Et','Rt','kappa'],[a0,a1,q0,q1,d0,d1,d2,Et,Rt,kappa])),'physical_roots':physical,'status':'NUMERICAL_DIAGNOSTIC_ONLY'}
  found.append(result);print(json.dumps(result),flush=True)
  if len(found)>=3:break
out={'trials_completed':trial+1,'maximum_detected_physical_roots':maxcount,'witnesses':found,'certificate':False}
Path(__file__).with_name('two_step_scan.json').write_text(json.dumps(out,indent=2)+'\n')
