#!/usr/bin/env python3
"""Exact rational/residue diagnostics for the all-prime written obstruction."""
from fractions import Fraction as F
from itertools import product
from collections import Counter
from pathlib import Path
import hashlib,json
C=Counter()
def ck(test,group):
    assert test,group
    C[group]+=1

def val(x,p):
    x=F(x)
    if x==0:return None
    a,b=abs(x.numerator),x.denominator;k=0
    while a%p==0:a//=p;k+=1
    while b%p==0:b//=p;k-=1
    return k

def H(x,p,a,u):
    return F(0) if x==0 else F(u)**(val(x,p)//a)*x

def residue(x,p,m):
    x=F(x);mod=p**m
    assert x.denominator%p
    return x.numerator*pow(x.denominator,-1,mod)%mod

primes=[2,3,5,7,11]
for p in primes:
    unit=F(1+p*p)
    samples=[F(0)]+[F(p)**k*r for k in range(-5,6) for r in (F(1),F(-1),F(1+p),F(1,1+p),F(1+p*p))]
    samples=sorted(set(samples))
    for a in (-3,-2,-1,1,2,3):
        lam=F(p)**a*(1+p);mu=lam*unit
        for x in samples:
            hx=H(x,p,a,unit)
            ck(val(hx,p)==val(x,p),'valuation_preservation')
            ck(H(hx,p,a,1/unit)==x,'exact_inverse')
            ck(H(lam*x,p,a,unit)==mu*hx,'general_conjugacy')
        for x,y in product(samples,repeat=2):
            ck(val(H(x,p,a,unit)-H(y,p,a,unit),p)==val(x-y,p),'distance_preservation')
    for x in samples:
        ck(H(p*x,p,1,unit)==p*unit*H(x,p,1,unit),'concrete_contraction')
        ck(H(x/p,p,1,unit)==H(x,p,1,unit)/(p*unit),'inverse_expansion')
    ck(H(F(1),p,1,unit)+H(F(p-1),p,1,unit)!=H(F(p),p,1,unit),'not_additive')
    # All-prime valuation inequalities are proved in the text. These exact
    # finite series certify the indicated leading residue in sampled cases.
    total=F(0)
    for n in range(1,81):
        term=F((-1)**(n+1)*p**(2*n),n)
        total+=term
        ck(val(term,p)==2*n-val(F(n),p),'log_term_valuation')
        if n>=2:ck(val(term,p)>=n+1,'tail_strictly_higher_valuation')
        ck(val(total,p)==2,'partial_log_nonzero')
        ck(residue(total,p,3)==p*p,'leading_log_residue')
    # Restrict H to Z/p^M Z via valuation shells. An isometry fixing zero
    # descends to each residue quotient and must be a permutation.
    for M in range(1,5):
        mod=p**M
        values=[]
        for r in range(mod):
            if not r:out=0
            else:out=(pow(1+p*p,val(F(r),p),mod)*r)%mod
            values.append(out)
        ck(len(set(values))==mod,'residue_quotient_permutation')
        for r in range(mod):
            ck(values[(p*r)%mod]==(p*(1+p*p)*values[r])%mod,'residue_conjugacy')
    # Fixed points of positive iterates reduce to a nonzero scalar coefficient.
    for n in range(1,31):
        for scalar in (F(p),F(p)*(1+p*p),F(1,p),F(1,p*(1+p*p))):
            ck(scalar**n!=1,'no_nonzero_periodic_points')
            ck(val(scalar**n,p)==n*val(scalar,p),'iterate_valuation')

root=Path(__file__).resolve().parent
result={'status':'PASS','assertions':sum(C.values()),'categories':dict(C),'sampled_primes':primes,'artifact_sha256':hashlib.sha256((root/'OBSTRUCTION.md').read_bytes()).hexdigest(),'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'Exact bounded diagnostics. The uniform all-prime theorem, continuity on all Q_p, Haar preservation and nonzero infinite logarithm are proved in the written artifact; no finite precision is used as their proof.'}
(root/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
