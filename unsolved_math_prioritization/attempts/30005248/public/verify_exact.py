#!/usr/bin/env python3
"""Small exact-arithmetic checks for the accompanying elementary arguments.

No numerical result establishes an asymptotic theorem. Uses only the Python
standard library; no network, random sampling, or exhaustive model search.
"""
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import json

counts = {}

def check(name, assertion):
    assert assertion, name
    counts[name] = counts.get(name, 0) + 1

def bern_probs(n,p):
    return [F(comb(n,k))*p**k*(1-p)**(n-k) for k in range(n+1)]

# Paired-sign mixture second moment, independently summed over both sign vectors.
for S in (2,4,6,8):
    d=S//2
    signs=list(product((-1,1),repeat=d))
    for n in range(1,9):
        for a in (F(1,8),F(1,4),F(1,2),F(3,4)):
            by_overlap=sum(F(comb(d,j),2**d)*(1+2*a*a*F(d-2*j,S))**n
                           for j in range(d+1))-1
            brute=sum((1+2*a*a*F(sum(x*y for x,y in zip(z,w)),S))**n
                      for z in signs for w in signs)/len(signs)**2-1
            check('mixture_overlap_equals_double_sum',by_overlap==brute)
            check('mixture_chi_square_nonnegative',by_overlap>=0)
            t=F(n*n,S)*a**4
            if t<1:
                # Analytic chain: chi^2 <= exp(t)-1 <= t/(1-t).
                check('mixture_geometric_upper_bound',by_overlap<=t/(1-t))
            if t<=F(1,16):
                check('mixture_small_signal_bound',by_overlap<=F(1,15))

# Exact risk of the point-mass reference estimator.
for n in range(1,13):
    for j in range(17):
        p=F(j,16)
        risk=sum(prob*(2*(1-F(k,n))-2*(1-p))**2
                 for k,prob in enumerate(bern_probs(n,p)))
        check('point_reference_variance_identity',risk==4*p*(1-p)/n)
        check('point_reference_risk_upper',risk<=F(1,n))

# Pythagorean parametrization keeps Bernoulli square roots rational.
params=[]
for u in (F(0),F(1,16),F(1,8),F(1,6),F(1,4),F(1,3)):
    root_p=2*u/(1+u*u)
    root_1mp=(1-u*u)/(1+u*u)
    params.append((root_p**2,root_p,root_1mp))
for (p,rp,rq),(q,sp,sq) in product(params,repeat=2):
    if not 0<=p<q<=F(1,2):
        continue
    delta=q-p
    affinity=rp*sp+rq*sq
    h2=1-affinity
    rationalized=delta**2/(sp+rp)**2+delta**2/(sq+rq)**2
    check('hellinger_rationalization',2*h2==rationalized)
    check('hellinger_lower',h2>=delta**2/(8*q))
    check('hellinger_upper',h2<=delta**2/q)
    for n in range(1,13):
        b0,b1=bern_probs(n,p),bern_probs(n,q)
        total_error=sum(min(x,y) for x,y in zip(b0,b1))
        tv=sum(abs(x-y) for x,y in zip(b0,b1))/2
        check('endpoint_optimal_error',total_error==1-tv)
        check('endpoint_affinity_upper',total_error<=affinity**n)
        check('endpoint_tv_affinity_bound',tv**2<=1-affinity**(2*n))
        check('endpoint_tv_linear_bound',tv**2<=2*n*h2)

# Deterministic grid reconstruction bound underlying the expectation argument.
for K in range(1,9):
    delta=F(1,K)
    for z in range(4*K+1):
        target=F(z,4*K)
        for bits in product((0,1),repeat=K):
            errors=0
            for j,bit in enumerate(bits):
                if target<=j*delta:
                    errors+=bit
                elif target>=(j+1)*delta:
                    errors+=1-bit
            estimate=delta*sum(bits)
            check('grid_reconstruction_bound',abs(estimate-target)<=2*delta+delta*errors)

result={'status':'PASS','arithmetic':'fractions.Fraction; exact rational arithmetic',
        'checks':counts,'total_assertions':sum(counts.values()),
        'limitations':'Checks finite identities and bounds only, not asymptotic rates, citations, novelty, or full problem resolution.'}
Path(__file__).with_name('verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
