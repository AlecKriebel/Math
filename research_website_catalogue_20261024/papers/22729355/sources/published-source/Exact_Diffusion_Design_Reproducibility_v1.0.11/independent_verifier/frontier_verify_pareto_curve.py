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

def direct(m,L):
    A0=A(m); r=rcrit(m); de=sp.diag(*Deff(m)); hs=Hlist(m,L); Hm=sp.diag(*hs); ell=ellref(m); q=Hm.inv()*ell
    assert (Hm*(A0-de))*r==sp.zeros(m+1,1)
    assert sp.simplify((Hm*(A0-de)).T*q)==sp.zeros(m+1,1)
    hh=Hsum(m);tau=tau_formula(m,hh,L);w0=w0ref(m)+tau*rhovec(m);w2=w2ref(m)
    rhs=-sp.Rational(1,4)*Hessian(m,r,r)
    assert sp.simplify(A0*w0-rhs)==sp.zeros(m+1,1)
    assert sp.factor((Hm.inv()*cvec(m)).dot(w0))==0
    assert sp.simplify((A0-4*de)*w2-rhs)==sp.zeros(m+1,1)
    den=sp.factor(q.dot(r));N=sp.factor(q.dot(Hm*(Hessian(m,r,w0)+sp.Rational(1,2)*Hessian(m,r,w2))))
    eta=sp.factor(q.dot(Hm*de*r)/den);cub=sp.factor(N/den)
    assert den<0 and eta>0 and cub<0
    return eta,cub

def verify(m):
    lo=L0(m);hi=L1(m);mid=sp.factor((lo+hi)/2)
    out=[]
    for name,L in [('L0',lo),('mid',mid),('L1',hi)]:
        eta,c=direct(m,L);out.append((name,str(eta),str(c)))
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('m',type=int,nargs='*',default=[3,4,5,6,8,10]);a=p.parse_args()
    for m in a.m: print(m,verify(m))
    print('VERIFY_PARETO_CURVE_PASS')
