#!/usr/bin/env python3
"""Independent exact controls for the scalar Legendre step, not a PDE verification."""
from fractions import Fraction as Q
import json
checks=0; cases=0
for T in [Q(1,4),Q(1,2),Q(3,4)]:
 for k0 in [Q(-1,4),Q(-1),Q(-2)]:
  for gap in [Q(1,4),Q(1),Q(2)]:
   b=k0-gap
   for L in [Q(-1),Q(-2),Q(-3)]:
    M=Q(-1)
    def a(t):
     x=t-T
     return k0*x+L*x*x/2 if t<=T else b*x+M*x*x/2
    def dual(k):
     tleft=max(Q(0),min(T,T+(k-k0)/L))
     tright=max(T,min(Q(1),T+(k-b)/M))
     pts={Q(0),T,Q(1),tleft,tright}
     vals={t:k+a(t)-t*k for t in pts}
     vmax=max(vals.values())
     return vmax,{t for t,v in vals.items() if v==vmax}
    eps=min(gap/4,T*(-L)/4)
    baseline=lambda k:(1-T)*k
    val,optimizers=dual(k0-eps)
    assert val==baseline(k0-eps);checks+=1
    assert optimizers=={T};checks+=1
    val,optimizers=dual(k0+eps)
    assert val-baseline(k0+eps)==-eps*eps/(2*L);checks+=1
    assert optimizers=={T+eps/L};checks+=1
    val0,optimizers0=dual(k0)
    assert val0==baseline(k0) and optimizers0=={T};checks+=1
    assert Q(0)<-1/L and k0<0;checks+=1
    cases+=1
print(json.dumps({'status':'PASS','cases':cases,'exact_assertions':checks,
 'method':'Rational piecewise-concave-quadratic functions; optimize both branches and endpoints exactly.',
 'scope':'Checks plateau direction, global maximizer, and unequal one-sided quadratic coefficients. Does not validate Hele-Shaw geometry, source inputs, or solve the PDE.'},indent=2))
