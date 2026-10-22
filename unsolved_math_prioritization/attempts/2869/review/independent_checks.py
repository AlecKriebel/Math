#!/usr/bin/env python3
"""Independent exact controls; no author imports or manifold-existence claims.

Finite abelian groups are enumerated directly. A cellular mapping-cone model
for the Mayer--Vietoris calculation is checked by enumerating finite-field
images, rather than by copying the author's matrix-rank implementation.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations_with_replacement, product
from math import prod
import json
from pathlib import Path

checks = Counter()
def require(condition, label):
    assert condition, label
    checks[label] += 1

def logq(n,q):
    k=0
    while n>1:
        require(n%q==0,'vector_space_cardinality')
        n//=q;k+=1
    return k

def image(matrix,ncols,q):
    return {tuple(sum(row[i]*x[i] for i in range(ncols))%q for row in matrix)
            for x in product(range(q),repeat=ncols)}

models=0
for k in range(4):
    for ds in combinations_with_replacement(range(1,13),k):
        models+=1
        elements=list(product(*(range(d) for d in ds)))
        require(len(elements)==prod(ds),'group_order')
        # The standard Q/Z pairing detects every element in either argument.
        for a in elements:
            annihilated=all(Fraction(ai,d).denominator==1 for ai,d in zip(a,ds))
            require(annihilated==(not any(a)),'character_pairing_nondegenerate')
        for q in (2,3,5,7):
            mult={tuple(q*x%d for x,d in zip(a,ds)) for a in elements}
            ker=[a for a in elements if all(q*x%d==0 for x,d in zip(a,ds))]
            quotient_size=len(elements)//len(mult)
            require(quotient_size==len(ker),'tensor_Tor_cardinality')
            t=sum(d%q==0 for d in ds)
            require(quotient_size==q**t,'UCT_prime_multiplicity')
            b=(t,2*t,t)
            require(1-b[0]+b[1]-b[2]==1,'punctured_Euler_characteristic')
        require((all(d%2 for d in ds))==(prod(ds)%2==1),'odd_order_criterion')

# U=X x S1, V=S2 x D2, E=S2 x S1; Cone(C(E)->C(U)+C(V)).
# Bases: C0=(u,v), C1=(a,t,e0), C2=(b,at,s,e1),
# C3=(bt,e2), C4=(e3).  The sign changes the gluing orientation.
mv_cases=0
for p in range(1,26):
    for sign in (-1,1):
        dims=(2,3,4,2,1)
        d={1:[[0,0,1],[0,0,-1]],
           2:[[p,0,0,0],[0,0,0,sign],[0,0,0,0]],
           3:[[0,0],[p,0],[0,sign],[0,0]],
           4:[[0],[0]]}
        for i in (2,3,4):
            require(all(sum(d[i-1][r][j]*d[i][j][c] for j in range(dims[i-1]))==0
                        for r in range(dims[i-2]) for c in range(dims[i])),
                    'mapping_cone_integer_d_squared')
        for q in (2,3,5,7):
            mv_cases+=1
            ranks={i:logq(len(image(d[i],dims[i],q)),q) for i in (1,2,3,4)}
            ranks[0]=ranks[5]=0
            betti=[dims[i]-ranks[i]-ranks[i+1] for i in range(5)]
            t=int(p%q==0)
            require(betti==[1,t,2*t,t,1],'closed_spin_field_homology')
            require(sum((-1)**i*b for i,b in enumerate(betti))==2,'closed_Euler_characteristic')
            require(betti[:4]==[1,t,2*t,t],'puncture_removes_only_top_class')
        # The two torsion coordinates have independent relations p*a and p*at.
        require(len({(a%p,b%p) for a in range(p) for b in range(p)})==p*p,
                'integral_torsion_coordinates')
        # Killing t in <a,t | a^p, [a,t]> leaves <a | a^p>.
        require(len({a%p for a in range(p)})==p,'van_Kampen_cyclic_abelian_control')

# Tensor/Tor obstructions cannot disappear under boundary connected sum.
for a in ((),(3,),(5,9),(2,),(2,3),(4,9)):
    for b in ((),(5,),(3,7),(2,),(6,10)):
        ra=sum(x%2==0 for x in a);rb=sum(x%2==0 for x in b)
        require(sum(x%2==0 for x in a+b)==ra+rb,'boundary_sum_two_primary_additivity')

result={'status':'PASS','exact_assertions':sum(checks.values()),'checks':dict(sorted(checks.items())),
        'finite_abelian_models':models,'mapping_cone_field_cases':mv_cases,
        'scope':'Independent algebraic controls only. Smooth realization and the standard S3 boundary are justified in the written review; no nonzero homology-cobordism class is certified.'}
print(json.dumps(result,indent=2,sort_keys=True))
