#!/usr/bin/env python3
"""Exact finite controls in the actual blowup intersection lattice; not a proof audit."""
import json
from fractions import Fraction

def add(a,b): return [x+y for x,y in zip(a,b)]
def scale(c,a): return [c*x for x in a]
def pair(a,b): return a[0]*b[0]-sum(x*y for x,y in zip(a[1:],b[1:]))

def check(d):
    n=d*d
    H=[1]+[0]*n
    E=[]
    for j in range(n):
        v=[0]*(n+1);v[j+1]=1;E.append(v)
    F=[d]+[-1]*n
    K=[-3]+[1]*n
    A=add(scale(2,F),E[0]); N=add(K,scale(2,F))
    assert pair(F,F)==0 and all(pair(F,e)==1 for e in E)
    assert pair(K,K)==9-n and pair(K,F)==d*(d-3)
    assert pair(A,A)==3 and pair(A,F)==1 and pair(A,E[0])==1
    assert all(pair(N,e)==1 for e in E)
    assert pair(N,N)==3*(d-1)*(d-3)
    k2=2*pair(N,N)
    assert k2==6*(d-1)*(d-3)
    assert 2*pair(A,A)==6
    # The lifted curve has degree one, not degree two, over its original fibre.
    assert pair(A,F)==1
    # Arithmetic genus of an unbranched lifted fibre and its ordinary singularity.
    pa=1+pair(N,F)//2
    delta=(d-1)*(d-2)//2
    assert pair(N,F)%2==0 and pa==delta
    # Negative numerical controls: d=6 does not yet violate the primary bound.
    violates=(d-3)**4>k2
    assert violates==(d>=7)
    if d>=7: assert Fraction(1,d-1)<Fraction(1,2) and k2>0
    return dict(d=d,basepoints=n,A_squared=pair(A,A),N_squared=pair(N,N),
                cover_K_squared=k2,cover_L_squared=6,L_dot_C=1,
                multiplicity=d-1,curve_arithmetic_genus=pa,
                strict_inequality_margin=(d-3)**4-k2,violates=violates)

if __name__=='__main__':
    rows=[check(d) for d in range(4,31)]
    print(json.dumps({'method':'integral diagonal blowup intersection pairing',
                      'checked_degrees':[4,30],'results':rows},indent=2))
