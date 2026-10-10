#!/usr/bin/env python3
"""Exact form/rescaling controls; not a proof of the classical topology inputs."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from math import comb
import hashlib,json
checks=0

def check(b):
    global checks
    checks+=1
    assert b

def clean(p): return {m:F(c) for m,c in p.items() if c}
def add(p,q):
    r=p.copy()
    for m,c in q.items():r[m]=r.get(m,0)+c
    return clean(r)
def scale(p,c):return clean({m:c*v for m,v in p.items()})
def mul(p,q):
    r={}
    for m,c in p.items():
        for n,d in q.items():
            k=tuple(x+y for x,y in zip(m,n));r[k]=r.get(k,0)+c*d
    return clean(r)
def der(p,i):
    r={}
    for m,c in p.items():
        if m[i]:
            n=list(m);n[i]-=1;r[tuple(n)]=c*m[i]
    return clean(r)
def subz(p,a,l):
    # old z=(new z-a)/l
    r={}
    for (i,j,k),c in p.items():
        for h in range(k+1):
            m=(i,j,h);r[m]=r.get(m,0)+c*comb(k,h)*(-a)**(k-h)/l**k
    return clean(r)
def integ(p,a,b):
    # x,y from 0 to 1 and z from a to b
    return sum((c*(b**(k+1)-a**(k+1))/F((i+1)*(j+1)*(k+1)) for (i,j,k),c in p.items()),F(0))
def faclean(w):return {m:clean(p) for m,p in w.items() if clean(p)}
def wadd(a,b):
    r=a.copy()
    for m,p in b.items():r[m]=add(r.get(m,{}),p)
    return faclean(r)
def wedge(a,b):
    r={}
    for m,p in a.items():
        for n,q in b.items():
            if set(m)&set(n):continue
            sign=(-1)**sum(i>j for i in m for j in n)
            k=tuple(sorted(m+n));r[k]=add(r.get(k,{}),scale(mul(p,q),sign))
    return faclean(r)
def exterior(a):
    r={}
    for m,p in a.items():
        for i in range(3):r=wadd(r,wedge({(i,):der(p,i)},{m:{(0,0,0):F(1)}}))
    return faclean(r)
one={(0,0,0):F(1)}
def make(seed):
    terms=[(0,0,0),(1,0,0),(0,1,0),(0,0,1),(1,1,1),(1,0,2),(0,1,3),(0,0,4)]
    return clean({m:F(((seed+1)*(j+3)+j*j)%11-5,j%3+1) for j,m in enumerate(terms)})
for k in range(120):
    p,q=make(2*k),make(2*k+1)
    alpha={(0,):p,(1,):q,(2,):one}
    pz,qz=der(p,2),der(q,2)
    eta=faclean({(0,):pz,(1,):qz})
    frob=add(add(der(q,0),scale(der(p,1),-1)),add(mul(q,pz),scale(mul(p,qz),-1)))
    density=add(mul(qz,der(pz,2)),scale(mul(pz,der(qz,2)),-1))
    check(wedge(alpha,exterior(alpha))==faclean({(0,1,2):frob}))
    check(wedge(eta,exterior(eta))==faclean({(0,1,2):density}))
    check(exterior(exterior(alpha))=={})
    for a,l in [(F(1,7),F(1,11)),(F(2,9),F(3,17)),(F(1,5),F(2,5))]:
        pn,qn=scale(subz(p,a,l),l),scale(subz(q,a,l),l)
        en=faclean({(0,):der(pn,2),(1,):der(qn,2)})
        check(der(pn,2)==subz(pz,a,l))
        check(der(qn,2)==subz(qz,a,l))
        check(wedge(en,exterior(en))==faclean({(0,1,2):scale(subz(density,a,l),1/l)}))
        check(integ(scale(subz(density,a,l),1/l),a,a+l)==integ(density,F(0),F(1)))
        fn=add(add(der(qn,0),scale(der(pn,1),-1)),add(mul(qn,der(pn,2)),scale(mul(pn,der(qn,2)),-1)))
        check(fn==scale(subz(frob,a,l),l))
# Explicit finite disjoint slabs, with collars/gaps and an abstract positive mass.
for n in range(1,101):
    slabs=[(F(2*j+1,2*n+2),F(2*j+2,2*n+2)) for j in range(n)]
    check(F(0)<slabs[0][0] and slabs[-1][1]<1)
    check(all(a<b for a,b in slabs))
    check(all(slabs[j][1]<slabs[j+1][0] for j in range(n-1)))
    a=F(7,13)
    check(sum((a for _ in slabs),F(0))==n*a)
# Closed-form/product-foliation diagnostic, including arbitrary base potentials.
for k in range(50):
    f=make(k)
    df=exterior({():f})
    check(exterior(df)=={})
    check(wedge(df,exterior(df))=={})
root=Path(__file__).resolve().parent
print(json.dumps({"assertions":checks,"polynomial_form_cases":120,"affine_rescalings":360,
 "stack_sizes":100,"scope":"Exact algebraic controls only; no numerical realization of the classical nonzero suspension or hyperbolic metric",
 "artifact_sha256":hashlib.sha256((root/'CANDIDATE.md').read_bytes()).hexdigest(),
 "verifier_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2,sort_keys=True))
