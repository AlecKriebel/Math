#!/usr/bin/env python3
"""Exact finite reduction for one shielded linkage in a two-active chart.

For A,B active and C bounded, every linkage classified as shielded by the
certified top-complex alternative has one of two forms:

1. its complex differences admit a rational invariant q with q_A,q_B>0;
2. up to exchange of A and B, its complex set is one of four subsets of
   {0,A,2A,B+C}; then B-C is invariant and the linkage has only A as an
   uncontrolled active coordinate.

The enumeration is a finite verification of the analytic linear-algebra
lemma, not a replacement for the stochastic proof.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import product

NAMES=('0','A','B','C','2A','2B','2C','AB','AC','BC')
V=((0,0,0),(1,0,0),(0,1,0),(0,0,1),(2,0,0),(0,2,0),(0,0,2),(1,1,0),(1,0,1),(0,1,1))
WORKLOADS=((1,1,0),(2,3,0),(1,2,0),(1,3,0))
SPECIAL={
    ('0','A','BC'),
    ('0','2A','BC'),
    ('A','2A','BC'),
    ('0','A','2A','BC'),
}

def dot(a,b): return sum(x*y for x,y in zip(a,b))

def classify_shielded(mask:int,h:tuple[int,int,int])->bool:
    ys=[i for i in range(10) if mask>>i&1]
    vals={i:dot(h,V[i]) for i in ys}; top={i for i in ys if vals[i]==max(vals.values())}
    if len(top)==len(ys): return True
    if any(V[y][0]+V[y][1]>=2 for y in top): return False
    K={i for y in top for i in (0,1) if V[y][i]}
    q=lambda y:sum(V[y][i] for i in K)
    if all(q(y)==1 for y in ys): return True
    if any(sum(V[y])==1 for y in top): return False
    D={2 for y in top if V[y][2]}
    lower=set(ys)-top
    if D and any(V[y][2] for y in lower): return False
    return True

def rref(rows):
    A=[list(map(Fraction,r)) for r in rows if any(r)]; rr=0
    for c in range(3):
        p=next((i for i in range(rr,len(A)) if A[i][c]),None)
        if p is None: continue
        A[rr],A[p]=A[p],A[rr]
        z=A[rr][c]; A[rr]=[x/z for x in A[rr]]
        for i in range(len(A)):
            if i!=rr and A[i][c]:
                z=A[i][c]; A[i]=[A[i][j]-z*A[rr][j] for j in range(3)]
        rr+=1
    return tuple(tuple(x for x in row) for row in A[:rr])

def rows(mask):
    ys=[i for i in range(10) if mask>>i&1]; root=V[ys[0]]
    return tuple(tuple(V[y][j]-root[j] for j in range(3)) for y in ys[1:])

def positive_active_invariant(mask:int):
    R=rref(rows(mask)); rank=len(R)
    if rank==0: return (Fraction(1),Fraction(1),Fraction(0))
    if rank==3: return None
    if rank==1:
        a,b,c=R[0]
        if c:
            return (Fraction(1),Fraction(1),-(a+b)/c)
        if not a and not b: return (Fraction(1),Fraction(1),Fraction(0))
        if a*b<0: return (abs(b),abs(a),Fraction(0))
        return None
    u,v=R
    n=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
    if n[0] and n[1] and n[0]*n[1]>0:
        if n[0]<0:n=tuple(-x for x in n)
        return n
    return None

def swap_ab(names):
    mp={'A':'B','B':'A','2A':'2B','2B':'2A','AC':'BC','BC':'AC','AB':'AB','0':'0','C':'C','2C':'2C'}
    return tuple(sorted((mp[x] for x in names), key=NAMES.index))

def audit():
    shielded=0; positive=0; special=[]
    for h in WORKLOADS:
        for mask in range(1,1<<10):
            if mask.bit_count()<2 or not classify_shielded(mask,h): continue
            shielded+=1
            q=positive_active_invariant(mask)
            if q is not None:
                assert q[0]>0 and q[1]>0
                assert all(dot(q,r)==0 for r in rows(mask))
                positive+=1; continue
            names=tuple(NAMES[i] for i in range(10) if mask>>i&1)
            canonical=min(names,swap_ab(names))
            if canonical not in SPECIAL:
                raise AssertionError((h,names,canonical,rref(rows(mask))))
            # B-C for the displayed A-special form; A-C after exchange.
            ell=(0,1,-1) if names in SPECIAL else (1,0,-1)
            assert all(dot(ell,r)==0 for r in rows(mask))
            special.append((h,names,ell))
    assert special
    return {'shielded_instances':shielded,'positive_active_invariant':positive,
            'signed_one_active_instances':len(special),
            'signed_unique_masks':sorted({x[1] for x in special})}

def self_test():
    out=audit()
    assert out['signed_one_active_instances']==6

if __name__=='__main__':
    self_test(); print(audit())
    print('shielded_linkage_reduction.py self-test: OK')
