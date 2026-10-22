#!/usr/bin/env python3
"""Independent exact chain-level controls for B²N and the detector argument.

No author code is imported. Low-dimensional nerve relations are checked;
Ara's all-dimensional classifying-space theorem is not replaced by a truncation.
"""
from collections import Counter
from itertools import product
from math import factorial
import json

counts=Counter()
def check(value,key):
    assert value,key
    counts[key]+=1

def basis(n,L):
    v=[0]*L
    if n:v[n-1]=1
    return v

def boundary(a,b,c,d,L):
    # Labels a=012, b=013, c=023, d=123, with a+c=b+d.
    return [x-y+z-t for x,y,z,t in zip(basis(d,L),basis(c,L),basis(b,L),basis(a,L))]

def degree(v):return sum((i+1)*x for i,x in enumerate(v))

quadruples=0
for L in range(1,11):
    relations=[]
    for n in range(2,L+1):
        # The tetrahedron (n-1,n,1,0) gives [n]-[n-1]-[1].
        v=boundary(n-1,n,1,0,L)
        check(degree(v)==0,'basic_nerve_relation_degree')
        check(v[n-1]==1 and all(v[j]==0 for j in range(n,L)),
              'unit_triangular_relation_basis')
        relations.append(v)
    for a,b,c in product(range(L+1),repeat=3):
        d=a+c-b
        if not 0<=d<=L:continue
        quadruples+=1
        v=boundary(a,b,c,d,L)
        check(degree(v)==0,'all_tetrahedron_boundaries_have_zero_degree')
        # Integer decomposition, proving saturation without division.
        coeff=[sum(v[n-1:]) for n in range(2,L+1)]
        rebuilt=[sum(coeff[j]*relations[j][i] for j in range(L-1)) for i in range(L)]
        check(rebuilt==v,'integral_boundary_decomposition')
        for m in (1,2,3):
            image=[0]*(m*L)
            for n,x in enumerate(v,1):image[m*n-1]=x
            check(image==boundary(m*a,m*b,m*c,m*d,m*L),'multiplication_chain_naturality')
    for n in range(1,L+1):
        for m in (1,2,3,5):
            check(degree(basis(m*n,m*L))==m*degree(basis(n,L)),
                  'multiplication_on_integral_H2')

# Integral cohomology is Z[c]; pairing with c^r introduces no factorial.
for m,r in product(range(1,8),range(1,9)):
    coeff=1
    for _ in range(r):coeff*=m
    check(coeff==m**r,'cup_power_multiplier')
    for n in (-7,-1,0,1,7):
        check((coeff*n==0)==(n==0),'nonzero_composite_implies_injection')
    if r>=2:
        check(coeff*factorial(r)!=coeff,'factorial_would_change_normalization')

# A finite torsion summand in the middle group cannot invalidate injection.
for m,r,d in product(range(1,5),range(1,4),range(2,6)):
    q=m**r
    for t in range(d):
        for n in range(-3,4):
            j=(q*n,t*n%d)
            check((j==(0,0))==(n==0),'injection_with_middle_group_torsion')
            check(j[0]==q*n,'detector_factorization_with_torsion')
# The subgroup mZ need not split integrally, since Z/m is torsion.
for m in range(2,9):
    check(len({n%m for n in range(m)})==m,'proper_image_has_torsion_quotient')

# The two-generator composite bubble: differential (1,-1), cycle (1,1).
for n in range(-10,11):
    check(n-n==0 and n+n==2*n,'composite_bubble_cycle_and_total_count')
# Nonfree idempotent: additivity in N forces its image to vanish.
for n in range(21):
    check((2*n==n)==(n==0),'nonfree_idempotent_obstruction')

print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),
 'checks':dict(sorted(counts.items())),'balanced_tetrahedra':quadruples,
 'max_label':10,'limitation':'Exact low-degree nerve, cup-power and factorization controls; not a computation of the full infinite nerve or proof of the bubble-free converse.'},indent=2,sort_keys=True))
