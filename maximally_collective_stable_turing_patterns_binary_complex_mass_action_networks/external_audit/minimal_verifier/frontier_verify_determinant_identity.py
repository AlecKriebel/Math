#!/usr/bin/env python3
from __future__ import annotations
import argparse,sys
from pathlib import Path
import sympy as sp
sys.path.insert(0,str(Path(__file__).resolve().parent))
from pareto_core import *

def verify(m:int):
    lam,t=sp.symbols('lambda t',positive=True)
    L=sp.symbols('L',positive=True) if m<=4 else sp.Rational(1,2)
    A0=A(m);de=sp.diag(*Deff(m));hs=Hlist(m,L);Hm=sp.diag(*hs)
    lhs=sp.factor((lam*sp.eye(m+1)-Hm*(A0-t*de)).det()/sp.prod(hs))
    g1=lam+2+t*sp.Rational(23,63);gm=lam+5+t*sp.Rational(1,7);gz=lam+4+t*sp.Rational(16,45)
    F=sp.expand(g1*gm*gz-4*g1-4*gm+gz);G=sp.expand(gz*(4*g1+gm)-36)
    Q=sp.prod(sp.factor(lam/hs[i]+1+t/sp.Integer(K(m,i+1))) for i in range(1,m-1))
    rhs=sp.factor(Q*F-G)
    assert sp.factor(lhs-rhs)==0
    return {'m':m,'degree':sp.Poly(lhs,lam).degree()}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('m',type=int,nargs='*',default=[3,4,5]);a=p.parse_args()
 for m in a.m:print(verify(m))
 print('VERIFY_DETERMINANT_IDENTITY_PASS')
