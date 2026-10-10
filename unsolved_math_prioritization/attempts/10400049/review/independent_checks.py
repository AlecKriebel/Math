#!/usr/bin/env python3
"""Independent finite resolution and character diagnostics; exact rationals only."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from math import comb,factorial
from pathlib import Path
from hashlib import sha256
import json
C=Counter()
def ck(cat,cond):
    assert cond,cat
    C[cat]+=1
def choose(x,r):
    a=F(1)
    for i in range(r):a*=F(x-i,i+1)
    return a
# Resolve r disjoint two-crossing full-twist blocks individually.
# The second crossing in each block is the selected singular crossing.
for n in range(4):
    for r in range(1,8):
        powers=[0]*(r+1)
        for bits in product((0,1),repeat=r):
            crossings=[1]*(2*n)
            for bit in bits:crossings += [1,1 if bit else -1]
            labels=[0,1];signed_intercomponent=0
            for sign in crossings:
                ck('two_strand_intercomponent_crossing',labels[0]!=labels[1])
                signed_intercomponent+=sign
                labels.reverse()
            ck('closure_component_labels',labels==[0,1])
            lk=F(signed_intercomponent,2)
            ck('full_twist_linking_normalization',lk==n+sum(bits))
            coefficient=(-1)**(r-sum(bits))
            for d in range(r+1):powers[d]+=coefficient*lk**d
        for d in range(r):ck('singular_resolution_degree_vanishing',powers[d]==0)
        ck('leading_finite_difference',powers[r]==factorial(r))

# Binomial-basis multiplication is checked through its independent combinatorial
# linearization coefficients, rather than interpolation of monomials.
for r in range(9):
    for s in range(9):
        for x in (F(-5,3),F(-1,2),F(0),F(1,2),F(7,4),F(11,3)):
            val=sum(comb(k,r)*comb(r,r+s-k)*choose(x,k) for k in range(max(r,s),r+s+1))
            ck('binomial_basis_product',val==choose(x,r)*choose(x,s))
# Newton coefficients from recursively differenced integer sequences.
for coeff in product((-2,0,3),repeat=4):
    def p(x):return sum(F(a)*choose(x,i) for i,a in enumerate(coeff))
    vals=[p(F(n)) for n in range(4)]
    got=[];row=vals
    while row:
        got.append(row[0]);row=[b-a for a,b in zip(row,row[1:])]
    ck('Newton_basis_reconstruction',got==list(map(F,coeff)))
    ck('half_character_from_values',sum(choose(F(1,2),i)*v for i,v in enumerate(got))==p(F(1,2)))

# Four-component linking matrix, self-crossing moves included.
pairs=[(i,j) for i in range(4) for j in range(i+1,4)]
moves=[None]+list(range(6))
for seed in range(7):
    base=[((seed+2)*(i+1))%5-2 for i in range(6)]
    for triple in product(moves,repeat=3):
        value=0
        for bits in product((0,1),repeat=3):
            cur=list(base)
            for index,bit in zip(triple,bits):
                if index is not None:cur[index]+=bit
            value+=(-1)**(3-sum(bits))*sum(x*x for x in cur)
        ck('four_component_third_skein_difference',value==0)
    g=sum(x*x for x in base)
    for signs in product((-1,1),repeat=4):
        transformed=[signs[i]*signs[j]*base[k] for k,(i,j) in enumerate(pairs)]
        ck('component_orientation_independence',sum(x*x for x in transformed)==g)
    ck('actual_link_zero_set',(g*(4*g-1)==0)==all(x==0 for x in base))
for values in product(range(-2,3),repeat=3):
    g=sum(v*v for v in values)
    ck('nonempty_actual_zero_set',(g*(4*g-1)==0)==(g==0))
ck('unlink_zero_set',0*(4*0-1)==0)

# Exact division by 4t^4-t^2: every t^(2N) has nonzero quadratic remainder.
def rem(poly):
    p=list(map(F,poly))
    while p and p[-1]==0:p.pop()
    while len(p)>=5:
        shift=len(p)-5;lead=p[-1]/4
        p[shift+4]-=4*lead;p[shift+2]+=lead
        while p and p[-1]==0:p.pop()
    return p
for N in range(1,61):
    p=[F(0)]*(2*N)+[F(1)]
    remainder=rem(p)
    ck('full_algebra_restriction_radical_diagnostic',remainder==[0,0,F(1,4**(N-1))])
    ck('nonzero_character_on_every_tested_power',sum(c*F(1,2)**i for i,c in enumerate(remainder))==F(1,4)**N!=0)
half=F(1,2);g=half*half
ck('ideal_killed_by_character',g==F(1,4) and g*(4*g-1)==0)
for n in range(-20,21):
    ck('character_not_actual_link_value',F(n*n)!=g)
root=Path(__file__).resolve().parent
out={'verdict':'PASS','assertions':sum(C.values()),'categories':dict(C),
 'artifact_sha256':sha256((root/'author_replay/CANDIDATE.md').read_bytes()).hexdigest(),
 'scope':'Finite exact diagnostics. The character on every finite-type invariant is proved by the singular-link difference argument and polynomial uniqueness.'}
(root/'independent_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

