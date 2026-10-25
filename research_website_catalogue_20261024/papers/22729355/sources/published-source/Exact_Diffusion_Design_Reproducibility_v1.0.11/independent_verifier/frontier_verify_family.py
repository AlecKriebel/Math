#!/usr/bin/env python3
from __future__ import annotations

if not __debug__:
    raise SystemExit(
        "Exact verifier requires assertions; unset PYTHONOPTIMIZE and do not use python -O"
    )

import argparse,sys
from pathlib import Path
import sympy as sp
sys.path.insert(0,str(Path(__file__).resolve().parent))
from pareto_core import *

def verify(m:int):
    rr=reactions(m); G,Y=gamma_y(m); c=cvec(m); rho=rhovec(m)
    assert all(sum(q.source)<=2 and sum(q.target)<=2 and q.source!=q.target for q in rr)
    assert G.rank()==m and G.T.nullspace()==[c]
    ker=G.nullspace(); assert len(ker)==2
    e1=sp.Matrix([1]*m+[0,0]);e2=sp.Matrix([0]*m+[1,1])
    assert G*e1==sp.zeros(m+1,1) and G*e2==sp.zeros(m+1,1)
    assert A(m)*rho==sp.zeros(m+1,1)
    L=L0(m); hs=Hlist(m,L); ds=Dphys(m,L)
    assert all(sp.ask(sp.Q.positive(x)) for x in hs+ds)
    # Exact realization: x*=H^{-1}, unit flux, rates=1/x*^source.
    x=[sp.factor(sp.Integer(1)/h) for h in hs]
    rates=[]
    for q in rr:
        mon=sp.prod(x[i]**q.source[i] for i in range(m+1)); rates.append(sp.factor(1/mon))
    assert all(sp.ask(sp.Q.positive(k)) for k in rates)
    # Jacobian from rates and equilibrium equals A H.
    v=sp.Matrix([sp.factor(rates[k]*sp.prod(x[i]**rr[k].source[i] for i in range(m+1))) for k in range(len(rr))])
    assert v==sp.ones(m+2,1)
    J=G*sp.diag(*list(v))*Y.T*sp.diag(*hs)
    assert sp.simplify(J-A(m)*sp.diag(*hs))==sp.zeros(m+1)
    # Physical diffusion is H Delta.
    assert sp.simplify(sp.diag(*ds)-sp.diag(*hs)*sp.diag(*Deff(m)))==sp.zeros(m+1)
    return {'m':m,'rank':G.rank(),'reactions':len(rr),'L':str(L)}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('m',type=int,nargs='*',default=[3,4,5,6,8,10]);a=p.parse_args()
    for m in a.m: print(verify(m))
    print('VERIFY_FAMILY_PASS')
