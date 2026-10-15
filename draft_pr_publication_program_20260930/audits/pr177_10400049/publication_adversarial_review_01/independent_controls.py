#!/usr/bin/env python3
"""Reviewer-authored exact finite diagnostics; universal proof is in the assessment."""
from fractions import Fraction as F
from itertools import product
from math import comb
from collections import Counter
import random,json
rng=random.Random(17710400049);counts=Counter()
def check(cat,b):
    if not b:raise RuntimeError('independent scientific gate: '+cat)
    counts[cat]+=1
# Boolean functions of degree d represented by monomial-support coefficient maps.
def poly(r,d):
    out={}
    for bits in product((0,1),repeat=r):
        support=frozenset(i for i,b in enumerate(bits) if b)
        if len(support)<=d:
            c=rng.randint(-3,3)
            if c:out[support]=F(c)
    return out
def mul(p,q):
    a=Counter()
    for u,c in p.items():
        for v,d in q.items():a[u|v]+=c*d
    return {u:c for u,c in a.items() if c}
def evalp(p,bits):return sum(c for u,c in p.items() if all(bits[i] for i in u))
for d,e in product(range(4),repeat=2):
    r=d+e+1
    for _ in range(8):
        p=poly(r,d);q=poly(r,e);pq=mul(p,q)
        check('product_support_degree',all(len(u)<=d+e for u in pq))
        difference=F(0)
        for bits in product((0,1),repeat=r):
            v=evalp(p,bits)*evalp(q,bits)
            check('pointwise_product_matches_cube_polynomial',v==evalp(pq,bits))
            difference+=(-1)**(r-sum(bits))*v
        check('product_high_difference',difference==0)
# g and f: varying component count, signed moves, repeated pair and self-crossing moves.
for m in [2,3,4,7,12]:
    pairs=[(i,j) for i in range(m) for j in range(i+1,m)]
    for _ in range(30):
        base=[rng.randint(-4,4) for _ in pairs]
        signs=[rng.choice([-1,1]) for _ in range(m)]
        g=sum(x*x for x in base)
        check('orientation_symmetry',sum((signs[i]*signs[j]*x)**2 for (i,j),x in zip(pairs,base))==g)
        check('actual_integer_zero_set',(g*(4*g-1)==0)==all(x==0 for x in base))
        for r,is_f in [(3,False),(5,True)]:
            moves=[(rng.choice([None]+list(range(len(pairs)))),rng.choice([-1,1])) for _ in range(r)]
            difference=0
            for bits in product((0,1),repeat=r):
                v=base[:]
                for b,(i,s) in zip(bits,moves):
                    if i is not None:v[i]+=b*s
                gg=sum(x*x for x in v);value=gg*(4*gg-1) if is_f else gg
                difference+=(-1)**(r-sum(bits))*value
            check('f_fifth_difference' if is_f else 'g_third_difference',difference==0)
# Direct even-exponent resolution, including negative bases.
for n,r in product(range(-12,13),range(11)):
    got=Counter()
    for bits in product((0,1),repeat=r):
        exponent=2*n+sum(1+(1 if b else -1) for b in bits)
        got[exponent]+=(-1)**(r-sum(bits))
        check('even_component_permutation',exponent%2==0)
        check('resolved_linking_integer',F(exponent,2)==n+sum(bits))
    expected={2*n+2*j:(-1)**(r-j)*comb(r,j) for j in range(r+1)}
    check('singular_cube_binomial_expansion',dict(got)==expected)
# Exact nonzero all-positive-power formula, finitely sampled to much higher order.
for N in range(1,201):
    t=F(1,2);g=t*t
    check('nonzero_character_on_powers',g**N==F(1,4**N)!=0)
    check('generator_kernel',g*(4*g-1)==0)
print(json.dumps({'status':'PASS','categories':dict(counts),'checks':sum(counts.values()),'seed':17710400049,'scope':'Finite reviewer diagnostics only; arbitrary-order/full-algebra proof checked separately.'},indent=2))
