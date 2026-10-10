#!/usr/bin/env python3
"""Portable exact arithmetic controls for PROOF.md, not a formal PDE proof."""
from fractions import Fraction as F
from itertools import product
import json

def check(condition,label):
    if not condition:raise RuntimeError(label)

counts={}
# Finite controls for the all-integer argument in Approach 1.
k=0
for a in [F(-1,2),F(-1,3),F(0),F(1,4),F(1,2)]:
    for extra in [F(0),F(1,10),F(1),F(3),F(10)]:
        b2=1-a*a+extra
        values=[]
        for m,n in product(range(-7,8),repeat=2):
            if m==n==0:continue
            val=b2*m*m+(n-a*m)**2
            check(val>=1,'dual-lattice bound')
            values.append(val);k+=1
        check(min(values)==1,'dual-lattice equality')
counts['dual_lattice_nonzero_modes']=k
# Exact variance/Schur-complement identity for arbitrary rational discrete models.
k=0
for weights in product([F(1,2),F(1),F(2)],repeat=3):
    total=sum(weights)
    for v in product([F(-1),F(0),F(1)],repeat=3):
        mean=sum(w*z for w,z in zip(weights,v))/total
        left=sum(w*(z-mean)**2 for w,z in zip(weights,v))
        right=sum(w*z*z for w,z in zip(weights,v))-sum(w*z for w,z in zip(weights,v))**2/total
        check(left==right,'weighted mean subtraction')
        check(sum(w*(z-mean) for w,z in zip(weights,v))==0,'weighted kernel orthogonality')
        if len(set(v))>1:check(left>0,'positive covariance')
        k+=1
counts['weighted_variance_cases']=k
# For cosine factors, F=b, Q=b(1+epsilon²/2), M=1+abs(epsilon).
k=0
for b in [F(1),F(3,2),F(2),F(7,2),F(4),F(6)]:
    for e in [F(-3,4),F(-1,2),F(-1,4),F(0),F(1,4),F(1,2),F(3,4)]:
        if 1+abs(e)>b:continue
        norm_sq_over_4pi2=b*(1+e*e/2)/(b*b)
        check(norm_sq_over_4pi2>=1/b,'cosine family lower bound')
        check((norm_sq_over_4pi2==1/b)==(e==0),'cosine equality')
        # Homothetic scaling cancels in Q/F².
        for s in [F(1,3),F(2),F(7,2)]:
            check((s*s*b*(1+e*e/2))/(s*b)**2==norm_sq_over_4pi2,'scaling')
        k+=1
counts['admissible_cosine_parameters']=k
# All 3 nonzero parity characters have an index-two kernel in Z².
k=0
for p,q in [(1,0),(0,1),(1,1)]:
    residues=[(m,n) for m,n in product(range(2),repeat=2) if (p*m+q*n)%2==0]
    check(len(residues)==2,'index-two spin kernel')
    # Canonical lattice bases of that kernel.
    u,v={(1,0):((2,0),(0,1)),(0,1):((1,0),(0,2)),(1,1):((1,1),(1,-1))}[(p,q)]
    check(abs(u[0]*v[1]-u[1]*v[0])==2,'cover determinant')
    check(all((p*z[0]+q*z[1])%2==0 for z in [u,v]),'cover kills character')
    k+=1
counts['nontrivial_spin_cover_characters']=k
# Deliberately reject three shortcuts, rather than assuming them.
f=[F(1),F(2),F(3)];v=[F(1),F(-1),F(0)]
check(sum(v)==0 and sum(x*y for x,y in zip(f,v))!=0,'unweighted mean countercontrol')
check(max(f)**2>sum(x*x for x in f)/len(f),'reversed L-infinity shortcut')
# Trivial-spin equator frequency must be even along both generators.
check(any(m%2 for m in (1,0)) and all(m%2==0 for m in (2,0)),'parity shortcut')
counts['rejected_shortcut_controls']=3
print(json.dumps({'status':'PASS','scope':'finite exact arithmetic controls; not formal analytic verification','counts':counts},indent=2,sort_keys=True))
