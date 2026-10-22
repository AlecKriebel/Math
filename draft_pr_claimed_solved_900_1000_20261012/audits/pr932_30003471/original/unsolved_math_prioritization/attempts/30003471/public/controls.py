#!/usr/bin/env python3
"""Finite diagnostics only; these do not verify the analytic candidate proof."""
import itertools
import json
import math

class DiagnosticError(Exception):
    pass

def require(test, label):
    if not test:
        raise DiagnosticError(label)

I = ((1, 0), (0, 1))
Z = ((0, 0), (0, 0))
C = (((0, -1j), (-1j, 0)), ((0, -1), (1, 0)), ((-1j, 0), (0, 1j)))

def add(a,b):
    return tuple(tuple(a[i][j]+b[i][j] for j in range(2)) for i in range(2))
def scale(t,a):
    return tuple(tuple(t*a[i][j] for j in range(2)) for i in range(2))
def mul(a,b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def cv(v):
    out=Z
    for t,c in zip(v,C):out=add(out,scale(t,c))
    return out

def run():
    counts={}
    def check(category, value, label):
        require(value,label)
        counts[category]=counts.get(category,0)+1
    check('clifford_volume',mul(mul(C[0],C[1]),C[2])==scale(-1,I),'odd Clifford volume convention')
    vectors=list(itertools.product(range(-1,2),repeat=3))
    for v in vectors:
        for w in vectors:
            left=add(mul(cv(v),cv(w)),mul(cv(w),cv(v)))
            check('clifford_exact',left==scale(-2*sum(x*y for x,y in zip(v,w)),I),'Clifford anticommutator')
    mats=[((a,b),(c,d)) for a,b,c,d in itertools.product(range(-1,2),repeat=4)]
    for a in mats:
        commutes=all(mul(a,c)==mul(c,a) for c in C)
        scalar=a[0][1]==a[1][0]==0 and a[0][0]==a[1][1]
        check('commutant_finite',commutes==scalar,'sample commutant')
    axes=[tuple(s if j==k else 0 for j in range(3)) for k in range(3) for s in (-1,1)]
    for v in axes:
        for w in axes:
            def chi(a):return scale(-1,mul(mul(cv(v),a),cv(w)))
            for a in mats:check('chirality_exact',chi(chi(a))==a,'chirality square')
    bases=[((1,0),(0,0)),((0,1),(0,0)),((0,0),(1,0)),((0,0),(0,1))]
    for j in range(3):
        for k in range(3):
            if j==k:continue
            for w in axes:
                L=scale(1j,mul(C[j],C[k]))
                def chi(a):return scale(-1,mul(mul(C[j],a),cv(w)))
                for a in bases:
                    check('boundary_symbol_exact',add(chi(mul(L,a)),mul(L,chi(a)))==Z,'symbol anticommutation')
    for j in range(1,51):
        theta=(math.pi/2-0.001)*j/50
        for k in range(21):
            t=k/20
            ratio=math.sin(t*theta)/math.sin(theta)
            check('spherical_dilation_numeric',0<=ratio<=1+1e-14 and 0<=t<=1,'hemisphere derivative bound')
    for ds in itertools.product((-1,0,1),repeat=4):
        weak=any(x<=0 for x in ds)
        equality=all(x==0 for x in ds)
        check('target_logic_exact',weak==(not all(x>0 for x in ds)) and weak==(weak or equality),'target quantifier')
    previous=math.inf
    for k in range(1,65):
        logdelta=-float(k)
        squared_weight=2*math.pi*(-logdelta)/(logdelta*logdelta)
        check('cutoff_rate_numeric',0<squared_weight<previous and math.exp(-4*k)<math.exp(-2*k),'log cutoff decay')
        previous=squared_weight
    return {'finite_diagnostics':'pass','counts':counts,'total':sum(counts.values()),'analytic_proof_certified':False,'numerical_checks_are_proof':False}

if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True))
