#!/usr/bin/env python3
"""Exact finite controls for PROOFS.md. These checks supplement its proofs."""
from itertools import product
from fractions import Fraction
from pathlib import Path
import json
import random

COUNTS = {}
def check(label, condition):
    assert condition, label
    COUNTS[label] = COUNTS.get(label, 0) + 1

def clean(f,p): return {a:c%p for a,c in f.items() if c%p}
def mul(f,g,p,cap=None):
    out={}
    for a,c in f.items():
        for b,d in g.items():
            t=tuple(x+y for x,y in zip(a,b))
            if cap is not None and any(x>=cap for x in t): continue
            out[t]=(out.get(t,0)+c*d)%p
    return clean(out,p)
def power(f,n,p,cap=None):
    out={(0,0):1}
    while n:
        if n%2:out=mul(out,f,p,cap)
        n//=2
        if n:f=mul(f,f,p,cap)
    return out
def frobenius(f,Q): return {tuple(Q*x for x in a):c for a,c in f.items()}
def outside(f,q): return any(all(x<q for x in a) for a in f)

# Full polynomial controls include terms outside the small Frobenius boxes.
mons=[(0,0),(1,0),(0,1),(1,1),(2,0),(0,2),(2,2)]
polys=[{m:1 for i,m in enumerate(mons) if mask>>i&1} for mask in range(1,1<<len(mons))]
for u in polys:
    for v in polys:
        if outside(u,2) and outside(v,2):
            check('separator_exhaustive_F2',outside(mul(frobenius(u,2),v,2),4))

rng=random.Random(20000276)
for p,q,Q in [(2,2,4),(2,4,8),(3,3,9),(3,9,3),(5,5,5)]:
    for _ in range(400):
        u=clean({(rng.randrange(2*q+1),rng.randrange(2*q+1)):rng.randrange(1,p) for _ in range(12)},p)
        v=clean({(rng.randrange(2*Q+1),rng.randrange(2*Q+1)):rng.randrange(1,p) for _ in range(12)},p)
        if outside(u,q) and outside(v,Q):
            check('separator_sparse_exact',outside(mul(frobenius(u,Q),v,p),q*Q))

# Negative control: same-scale ordinary multiplication does not work.
x={(1,0):1}
check('negative_same_scale',outside(x,2) and not outside(mul(x,x,2),2))

# Actual binomial witnesses for the fixed-factor proof, all arithmetic in F2.
g={(1,0):1,(0,1):1}
f={(2,0):1,(0,3):1}
for q in [2,4,8]:
    a=q-1
    u=power(g,a,2)
    check('base_binomial_noncontainment',outside(u,q))
    for k in [4*a+1,4*a+3,8*a+1]: # c(f)>=1/4 since f notin (x^4,y^4)
        check('strict_fixed_factor_margin',Fraction(a,k)<Fraction(1,4))
        for Q in [8,16,32,64]:
            h=a*Q//k
            v=power(f,h,2,q*Q)
            check('fixed_factor_small_scale',outside(v,Q))
            witness=mul(frobenius(u,Q),v,2,q*Q)
            check('fixed_factor_large_scale',outside(witness,q*Q))
            check('fixed_factor_ideal_exponent',a*Q>=k*h)
            check('fixed_factor_floor_error',Fraction(a,k)-Fraction(1,Q)<Fraction(h,Q)<=Fraction(a,k))

# The node ring has monomial basis x^a y^b z^c with a*b=0.
def node_mul(a,b):
    if a is None or b is None:return None
    t=tuple(x+y for x,y in zip(a,b))
    return None if t[0]*t[1] else t

def node_map(a,q,r):
    if a is None:return None
    x,y,z=a
    if x%q or y%q or z%q!=r:return None
    return (x//q,y//q,(z-r)//q)

for q in [2,3,4,5,8,9]:
    for r in range(q):
        check('node_map_z_splits',node_map((0,0,r),q,r)==(0,0,0))
        for a in range(2*q+2):
            for b in range(2*q+2):
                if a*b:continue
                for c in range(2*q+2):
                    v=(a,b,c)
                    for j in range(3):
                        scalar=tuple(int(i==j) for i in range(3))
                        scalarq=tuple(q*t for t in scalar)
                        check('node_map_linearity',node_map(node_mul(scalarq,v),q,r)==node_mul(scalar,node_map(v,q,r)))
        for a in range(1,21):
            nu=(q-1)//a
            check('node_power_threshold_crossing',a*nu<q<=a*(nu+1))

# (h^epsilon(n) z^ceil(n/2)) product inclusion and two-generator Rees form.
for n in range(1,301):
    check('node_rees_degrees',n==2*(n//2)+n%2)
    check('node_rees_z_exponent',(n+1)//2==n//2+n%2)
    for m in range(1,301):
        check('node_family_h_inclusion',n%2+m%2>=(n+m)%2)
        check('node_family_z_inclusion',(n+1)//2+(m+1)//2>=(n+m+1)//2)
    if n%2==0:check('node_even_value',Fraction(n,n//2)==2)

# Rational ceilings supply exact monomial controls for the limit and inclusions.
for alpha in [Fraction(1,7),Fraction(3,2),Fraction(17,5),Fraction(21,13)]:
    ceil=lambda z:-(-z.numerator//z.denominator)
    for n in range(1,101):
        a=ceil(alpha*n)
        check('ceiling_fpt_error',Fraction(n,a)<=1/alpha and Fraction(n,a)>Fraction(n,alpha*n+1))
        for m in range(1,101):
            check('ceiling_multiplicativity',ceil(alpha*(n+m))<=a+ceil(alpha*m))

out={'status':'PASS','seed':20000276,'assertions':sum(COUNTS.values()),'counts':COUNTS,
     'scope':'Finite exact controls only; unbounded-index and arbitrary-ring claims are proved in PROOFS.md.'}
print(json.dumps(out,indent=2,sort_keys=True))
