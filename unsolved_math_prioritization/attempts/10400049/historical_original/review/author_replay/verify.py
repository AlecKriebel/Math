#!/usr/bin/env python3
"""Exact supporting controls; the all-invariant claim is the skein proof."""
from fractions import Fraction as F
from itertools import product,permutations
from math import comb
from collections import Counter
from pathlib import Path
from hashlib import sha256
import json
C=Counter()
def ck(t,g):
    assert t,g
    C[g]+=1

def choose(x,r):
    out=F(1)
    for i in range(r):out*=F(x-i,i+1)
    return out

def delta(values,r):return sum((-1)**(r-j)*comb(r,j)*values[j] for j in range(r+1))
def newton(values,t):return sum((choose(t,r)*delta(values,r) for r in range(len(values))),F(0))

for degree in range(13):
    values=[F(n**degree) for n in range(degree+1)]
    for t in [F(a,b) for b in (1,2,3) for a in range(-5,9)]:
        ck(newton(values,t)==t**degree,'Newton_monomial_identity')
    for n in range(8):
        ck(delta([(n+j)**degree for j in range(degree+2)],degree+1)==0,'finite_difference_vanishing')
# Exact exponent coefficients of the singular-braid resolution.
for r in range(13):
    terms={0:1}
    for _ in range(r):
        out=Counter()
        for e,a in terms.items():out[e+1]+=a;out[e-1]-=a
        terms=dict(out)
    for n in range(6):
        expanded={2*n+r+e:a for e,a in terms.items() if a}
        expected={2*n+2*j:(-1)**(r-j)*comb(r,j) for j in range(r+1)}
        ck(expanded==expected,'braid_full_twist_resolution')
        ck(all(e%2==0 for e in expanded),'two_component_permutation')

pairs=[(0,1),(0,2),(1,2)]
def G(v):return sum(x*x for x in v)
def transform(v,perm,sign):
    matrix=[[0]*3 for _ in range(3)]
    for (i,j),x in zip(pairs,v):matrix[i][j]=matrix[j][i]=x
    return tuple(sign[i]*sign[j]*matrix[perm[i]][perm[j]] for i,j in pairs)
for v in product((-1,0,1),repeat=3):
    g=G(v)
    ck((g*(4*g-1)==0)==all(x==0 for x in v),'actual_algebraically_split_zero_set')
    for perm in permutations(range(3)):
        for signs in product((-1,1),repeat=3):ck(G(transform(v,perm,signs))==g,'orientation_and_order_independence')
    moves=[(i,sign) for i in range(3) for sign in (-1,1)]
    for triple in product(moves,repeat=3):
        total=0
        for bits in product((0,1),repeat=3):
            resolved=list(v)
            for (i,sign),bit in zip(triple,bits):resolved[i]+=sign*bit
            total+=(-1)**(3-sum(bits))*G(resolved)
        ck(total==0,'third_skein_difference_g')

for a in range(-3,4):
    for b in range(-3,4):
        p=lambda n:F(a*n*n+b*n+1)
        q=lambda n:F(b*n*n*n+a)
        vp=[p(n) for n in range(3)];vq=[q(n) for n in range(4)]
        prod=[p(n)*q(n) for n in range(6)]
        for t in (F(-1,2),F(1,2),F(2,3),F(7,2)):
            ck(newton(prod,t)==newton(vp,t)*newton(vq,t),'restriction_multiplicativity')

half=F(1,2);chi_g=half**2
ck(chi_g==F(1,4),'half_twist_character')
ck(chi_g*(4*chi_g-1)==0,'ideal_generator_in_kernel')
for N in range(1,101):ck(chi_g**N!=0,'all_sampled_powers_outside_kernel')
for n in range(100):
    g=n*n
    ck((g*(4*g-1)==0)==(n==0),'torus_family_actual_zero_set')
    ck(F(g)!=chi_g,'character_not_actual_integer_value')
ck(newton([F(0),F(1),F(4)],half)==chi_g,'global_g_restriction')

p=Path(__file__).resolve().parent
r={'status':'PASS','assertions':sum(C.values()),'categories':dict(C),'artifact_sha256':sha256((p/'CANDIDATE.md').read_bytes()).hexdigest(),'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'Exact algebraic and resolution controls only. The arbitrary-order polynomial restriction, actual linking interpretation and full-algebra radical obstruction are established by the written proof, not by testing finitely many invariants.'}
(p/'verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
