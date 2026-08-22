#!/usr/bin/env python3
from __future__ import annotations
import argparse,sys
from pathlib import Path
import sympy as sp
sys.path.insert(0,str(Path(__file__).resolve().parent))
from pareto_core import *

def assert_exact_minimum(values, candidate):
    """Certify a proposed minimum without numerical approximation."""
    assert all(sp.factor(value-candidate).is_nonnegative is True for value in values)

def assert_exact_maximum(values, candidate):
    """Certify a proposed maximum without numerical approximation."""
    assert all(sp.factor(candidate-value).is_nonnegative is True for value in values)

def verify(m:int):
    r=m-2;L=L0(m); hs=Hlist(m,L); ds=Dphys(m,L)
    # Exact endpoint identities.
    assert_exact_minimum(ds,ds[1])
    assert_exact_maximum(ds,ds[0])
    assert_exact_minimum(hs,sp.Integer(1))
    assert_exact_maximum(hs,hs[1])
    chiD=sp.factor(ds[0]/ds[1]);chiH=sp.factor(hs[1]);prod=sp.factor(chiD*chiH)
    kappa=endpoint_kappa(m)
    assert sp.factor(chiD-sp.Rational(2093,63)*kappa*sp.sqrt(r))==0
    assert sp.factor(chiH-sp.sqrt(r)/kappa*sp.Rational(91*r-1,91*r))==0
    assert prod==sp.Rational(23*(91*r-1),63)
    assert sp.factor(r*L**2-(sp.Rational(1,3) if r==1 else sp.Rational(5,4)))==0
    assert sp.factor(chiD*chiH-8*r).is_positive is True
    # The exact maximum certificate above identifies chiD as a physical
    # contrast; at the endpoint it already exceeds the minimax threshold.
    assert sp.factor(chiD-sp.sqrt(8*r)).is_positive is True
    return {'m':m,'chi_D':str(chiD),'chi_H':str(chiH),'product':str(prod)}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('m',type=int,nargs='*',default=[3,4,5,6,8,10]);a=p.parse_args()
    for m in a.m: print(verify(m))
    print('VERIFY_PARETO_PASS')
