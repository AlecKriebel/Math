#!/usr/bin/env python3
from __future__ import annotations
import argparse,sys
from pathlib import Path
import sympy as sp
sys.path.insert(0,str(Path(__file__).resolve().parent))
from pareto_core import *

def verify(m:int):
    L=L0(m); A0=A(m); r=rcrit(m); de=sp.diag(*Deff(m)); hs=Hlist(m,L); Hmat=sp.diag(*hs); ell=ellref(m); q=Hmat.inv()*ell
    assert (A0-de)*r==sp.zeros(m+1,1)
    assert (Hmat*(A0-de)).T*q==sp.zeros(m+1,1)
    hsum=Hsum(m); wref=w0ref(m); rh=rhovec(m); cv=cvec(m)
    cinv=Hmat.inv()*cv
    tau=sp.factor(-cinv.dot(wref)/cinv.dot(rh))
    assert sp.factor(tau-tau_formula(m,hsum,L))==0
    w0=sp.simplify(wref+tau*rh); w2=w2ref(m)
    rhs=-sp.Rational(1,4)*Hessian(m,r,r)
    assert sp.simplify(A0*w0-rhs)==sp.zeros(m+1,1)
    assert sp.factor(cinv.dot(w0))==0
    assert sp.simplify((A0-4*de)*w2-rhs)==sp.zeros(m+1,1)
    den=sp.factor(q.dot(r)); assert sp.factor(den-den_formula(m,L))==0 and den<0
    etanum=sp.factor(q.dot(Hmat*de*r)); assert sp.factor(etanum-eta_num(m,hsum))==0 and etanum<0
    N=sp.factor(q.dot(Hmat*(Hessian(m,r,w0)+sp.Rational(1,2)*Hessian(m,r,w2))))
    Nclosed=sp.factor(N0(m,hsum)+tau*Sterm(m,hsum))
    assert sp.factor(N-Nclosed)==0 and N>0
    eta=sp.factor(etanum/den); cubic=sp.factor(N/den)
    assert eta>0 and cubic<0
    return {'m':m,'tau':str(tau),'eta':str(eta),'cubic':str(cubic)}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('m',type=int,nargs='*',default=[3,4,5,6,8,10]);a=p.parse_args()
    for m in a.m: print(verify(m))
    print('VERIFY_NORMAL_FORM_PASS')
