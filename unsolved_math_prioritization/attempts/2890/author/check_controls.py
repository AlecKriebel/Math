#!/usr/bin/env python3
"""Exact finite diagnostics for PROOF.md; no topology/Floer computation.

Python 3 standard library only. No network, randomness, file writes, or external
source dependencies. Counts are diagnostics, not proof certificates.
"""
from itertools import product, permutations
from collections import Counter
import json

counts = Counter()

def check(name, proposition):
    counts[name] += 1
    if not proposition:
        raise AssertionError((name, counts[name]))

def bitdot(a,b):
    return (a & b).bit_count() % 2

def act(rows,x):
    return sum(bitdot(row,x) << i for i,row in enumerate(rows))

# The gluing-functional identity is valid for every endomorphism, not only
# involutions. For involutions, delta is fixed in characteristic two.
for d in range(1,4):
    size=1<<d
    for rows in product(range(size), repeat=d):
        involutive=all(act(rows,act(rows,1<<i))==(1<<i) for i in range(d))
        for x in range(size):
            fx=act(rows,x)
            delta=x^fx
            for functional in range(size):
                check('linear_difference_identity',
                      bitdot(functional,x)^bitdot(functional,fx)==bitdot(functional,delta))
            if involutive:
                check('involutive_difference_fixed',act(rows,delta)==delta)
    for delta in range(1,size):
        mu=next(m for m in range(size) if bitdot(m,delta)==1)
        for length in range(1,7):
            for bits in product((0,1), repeat=length):
                values=tuple(bitdot(mu if b else 0,delta) for b in bits)
                check('prescribed_nonzero_evaluations', values==bits)

# Order statistics preserve componentwise inequalities. Each tuple contains
# (minimal genus upper bound, representative genus, square).
data=[(lo,hi,q) for hi in range(3) for lo in range(hi+1) for q in range(-2,3)]
for rank in range(1,4):
    for rows in product(data, repeat=rank):
        low=sorted((2*a-q for a,b,q in rows),reverse=True)
        high=sorted((2*b-q for a,b,q in rows),reverse=True)
        for i in range(rank):
            check('adjunction_order_bound',low[i]<=high[i])
        check('exterior_max_bound',max(low)<=max(high))
# Do not add an unjustified lower bound or absolute value to 2g-q.
check('signed_adjunction_control',2*0-1 == -1)

# Complete small signed intersection arrays with algebraic matrix I.
for n in range(1,4):
    for neg in product(range(3), repeat=n*n):
        positive=[neg[i*n+j]+int(i==j) for i in range(n) for j in range(n)]
        geometric=sum(a+b for a,b in zip(positive,neg))
        complexity=geometric-n
        check('intersection_complexity_identity',complexity==2*sum(neg))
        check('intersection_complexity_parity',complexity>=0 and complexity%2==0)

# All small positive/negative ranks: stabilization adds a hyperbolic pair.
for p,q,n in product(range(17),range(17),range(17)):
    b2=p+q
    sig=p-q
    chi=2+b2  # simply connected closed oriented case
    check('stabilization_rank',p+n+q+n==b2+2*n)
    check('stabilization_signature',(p+n)-(q+n)==sig)
    check('stabilization_euler',2+p+n+q+n==chi+2*n)
    check('cork_yasui_hypothesis_failure',not (0-4*0>11*(n+1)+10))

# Quantifier-order and minimum-over-cobordisms negative controls.
for n in range(2,33):
    relation=[[i==j for j in range(n)] for i in range(n)]
    check('embedding_quantifier_negative_control',
          all(any(relation[i][j] for i in range(n)) for j in range(n))
          and not any(all(row) for row in relation))
    check('selected_cobordism_minimum_control',min([0,2*n])==0 and 2*n>n)
    # Neither singleton preservation law gives a preservation law for mixed
    # moves: moves 00->01 and 01->11 preserve different coordinates.
    check('mixed_moves_negative_control',(0,0)[0]==(0,1)[0]
          and (0,1)[1]==(1,1)[1] and (0,0)!=(1,1))

# The boundary compatibility a*g=h*b corresponds to h in A*g*B.
def compose(a,b):
    return tuple(a[b[i]] for i in range(len(a)))

def inverse(a):
    r=[0]*len(a)
    for i,j in enumerate(a):
        r[j]=i
    return tuple(r)

def generated(generators,n):
    identity=tuple(range(n))
    found={identity}
    frontier=[identity]
    while frontier:
        x=frontier.pop()
        for g in generators:
            y=compose(g,x)
            if y not in found:
                found.add(y);frontier.append(y)
    return frozenset(found)

for n in (3,4):
    group=tuple(permutations(range(n)))
    identity=tuple(range(n))
    swap=(1,0)+tuple(range(2,n))
    cycle=tuple(list(range(1,n))+[0])
    subgroups={generated([],n),generated([swap],n),generated([cycle],n),frozenset(group)}
    if n==4:
        subgroups.add(generated([(1,0,3,2),(2,3,0,1)],n))
        subgroups.add(generated([(1,0,2,3),(1,2,0,3)],n))
    subgroups=sorted(subgroups,key=lambda x:(len(x),sorted(x)))
    for A,B in product(subgroups,repeat=2):
        for g in group:
            orbit={compose(compose(a,g),b) for a in A for b in B}
            invg=inverse(g)
            for h in group:
                # a*g=h*b iff a=h*b*g^-1.
                compatible=any(compose(compose(h,b),invg) in A for b in B)
                check('double_coset_compatibility',(h in orbit)==compatible)
            check('double_coset_contains_representative',g in orbit)
    A=generated([swap],n)
    B=generated([],n)
    check('nonextension_not_effectiveness_model',swap not in B and swap in A)

result={
    'status':'PASS',
    'arithmetic':'exact integers, finite F2 arithmetic and permutations',
    'total_assertions':sum(counts.values()),
    'groups':dict(sorted(counts.items())),
    'scope':'Finite diagnostics only; does not construct corks, compute Floer maps, certify embeddings, or settle KP-4.14.'
}
print(json.dumps(result,indent=2,sort_keys=True))
