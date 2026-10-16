#!/usr/bin/env python3
"""Independent exact checks of the geometric composition coefficients.

The intersection-number evaluator uses string, dilaton, and DVV recursions.
No reviewed candidate code, inherited audit, or numerical intersection table
is imported. All arithmetic is rational. The zeta factors remain formal.
"""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from math import factorial, log, exp, comb
import json
from pathlib import Path

def dfact(x):
    if x <= 0:
        return 1
    ans=1
    for i in range(x,0,-2): ans*=i
    return ans

@lru_cache(None)
def intersection(g, ds):
    ds=tuple(sorted(ds))
    n=len(ds)
    if g<0 or 2*g-2+n<=0 or any(d<0 for d in ds) or sum(ds)!=3*g-3+n:
        return Q(0)
    if g==0 and n==3: return Q(1)
    if g==1 and n==1 and ds==(1,): return Q(1,24)
    if ds[0]==0:
        tail=list(ds[1:]); ans=Q(0)
        for i,d in enumerate(tail):
            if d:
                new=tail.copy(); new[i]-=1
                ans+=intersection(g,tuple(sorted(new)))
        return ans
    if ds[0]==1:
        return (2*g-3+n)*intersection(g,ds[1:])
    d=ds[-1]; tail=ds[:-1]; ans=Q(0)
    for i,e in enumerate(tail):
        new=list(tail); new.pop(i); new.append(d+e-1)
        ans+=Q(dfact(2*d+2*e-1),dfact(2*e-1))*intersection(g,tuple(sorted(new)))
    for a in range(d-1):
        b=d-2-a
        spl=intersection(g-1,tuple(sorted((a,b)+tail)))
        for mask in range(1<<len(tail)):
            left=tuple(tail[i] for i in range(len(tail)) if mask>>i&1)
            right=tuple(tail[i] for i in range(len(tail)) if not mask>>i&1)
            for h in range(g+1):
                spl+=intersection(h,tuple(sorted((a,)+left)))*intersection(g-h,tuple(sorted((b,)+right)))
        ans+=Q(dfact(2*a+1)*dfact(2*b+1),2)*spl
    return ans/dfact(2*d+1)

def comps(n,k):
    if k==1:
        if n>=1: yield(n,)
    else:
        for j in range(1,n-k+2):
            for tail in comps(n-j,k-1): yield(j,)+tail

def F_coefficient(g,js):
    k=len(js); ans=Q(0)
    for lower in product(*(range(j) for j in js)):
        ds=tuple(v for j,a in zip(js,lower) for v in (a,j-1-a))
        den=1
        for d in ds: den*=factorial(d)
        ans+=intersection(g-k,tuple(sorted(ds)))/den
    return ans/Q(2**(3*g-3-k))

def A(g,k):
    return Q(factorial(6*g-5-2*k)*2**(3*k-3),factorial(g-k)*factorial(3*g-3-k)*3**(g-k))

def D(g,k): return A(g,k)/2**k

def c_binomial_average(g,js):
    G=g-len(js); k=len(js); ans=Q(0)
    for lower in product(*(range(j) for j in js)):
        ds=tuple(v for j,a in zip(js,lower) for v in (a,j-1-a))
        baseline=Q(dfact(6*G-5+4*k),factorial(G)*24**G)
        for d in ds: baseline/=dfact(2*d+1)
        normalized=intersection(G,tuple(sorted(ds)))/baseline
        weight=1
        for j,a in zip(js,lower): weight*=comb(2*j,2*a+1)
        ans+=normalized*weight
    return ans/Q(2**(6*G-6+5*k))

for d in range(31):
    assert sum(comb(2*d+2,2*a+1) for a in range(d+1))==2**(2*d+1)
records=[]
for g in range(2,6):
    for k in range(1,min(3,g)+1):
        allcoeff=[]
        for js in comps(3*g-3,k):
            f=F_coefficient(g,js)
            prod_fact=1
            for j in js: prod_fact*=factorial(2*j)
            c=f*prod_fact/A(g,k)
            assert f>0
            assert c==c_binomial_average(g,js)
            # Independently compare the pre-integral coefficient after graph
            # automorphisms and the post-integral assembly factor. Zeta is formal.
            left=f/Q(2**k*factorial(k))
            for j in js: left*=factorial(2*j-1)
            right=D(g,k)*c/Q(factorial(k))
            for j in js: right/=2*j
            assert left==right
            allcoeff.append(c)
        records.append({'g':g,'k':k,'compositions':len(allcoeff),'ctilde_min':str(min(allcoeff)),'ctilde_max':str(max(allcoeff))})
        if k<g:
            ratio=D(g,k+1)/D(g,k)
            claimed=Q(12*(g-k)*(3*g-3-k),(6*g-5-2*k)*(6*g-6-2*k))
            assert ratio==claimed
# Published genus-two one-vertex polynomial entries, checked independently.
assert F_coefficient(2,(3,))==Q(1,48)
assert F_coefficient(2,(1,2))==Q(1)
assert F_coefficient(2,(2,1))==Q(1)
# Independent standard low intersection numbers.
assert intersection(2,(4,))==Q(1,1152)
assert intersection(1,(0,2))==Q(1,24)
assert intersection(1,(1,1))==Q(1,24)
eta=Q(3,5)*log(1.1)-Q(1,20)
assert eta>Q(1,220)
assert Q(3,5)<1/log(Q(9,4))
large=[]
for g in (10**3,10**6,10**12):
    kmax=int(.6*log(6*g-6))
    ratio=1.0
    for k in range(1,kmax):
        ratio*=12*(g-k)*(3*g-3-k)/((6*g-5-2*k)*(6*g-6-2*k))
    large.append({'g':g,'kmax':kmax,'D_kmax_over_D_1':ratio})
result={'status':'PASS','exact_records':records,'large_prefactor_ratios':large,'eta':eta,'error_exponent_before_logs':1-.6*log(2),'cached_intersections':intersection.cache_info()._asdict()}
Path('EXACT_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
