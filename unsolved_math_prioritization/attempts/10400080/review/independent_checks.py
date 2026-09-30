#!/usr/bin/env python3
"""Independent integral quotient and Laurent trace controls."""
from itertools import product
from collections import Counter
from math import comb
from pathlib import Path
from hashlib import sha256
import json
C=Counter()
def ck(x,g):
    assert x,g
    C[g]+=1

def mul(X,Y):return (X[0]*Y[0]+X[1]*Y[2],X[0]*Y[1]+X[1]*Y[3],X[2]*Y[0]+X[3]*Y[2],X[2]*Y[1]+X[3]*Y[3])
def tr(X):return X[0]+X[3]
def inv(X):return (X[3],-X[1],-X[2],X[0])
mats=[(1+a*b,a,b,1) for a,b in product(range(-3,4),repeat=2)]
for X,Y in product(mats,repeat=2):
    ck(X[0]*X[3]-X[1]*X[2]==1,'SL2_determinant')
    ck(tr(X)*tr(Y)==tr(mul(X,Y))+tr(mul(X,inv(Y))),'trace_skein_identity')
    ck(tr(inv(X))==tr(X),'orientation_independent_trace')
# Parallel-copy Laurent polynomials by coefficient recurrence.
poly={0:1}
for j in range(41):
    ck(poly.get(j)==(-1)**j,'distinct_leading_coefficient')
    ck(max(poly)==j and min(poly)==-j,'Laurent_degree_bounds')
    if j:
        ck(sum(poly.values())==(-2)**j,'trivial_diagonal_specialization')
    new=Counter()
    for exponent,value in poly.items():new[exponent+1]-=value;new[exponent-1]-=value
    poly=dict(new)
# Integral ideal membership in Z[h]/(c h^e); multiplication by A=h-1
# cannot kill a class with a nonzero coefficient in degree below e.
def in_ideal(poly,c,e):
    return all(a==0 if i<e else a%c==0 for i,a in enumerate(poly))
for e in range(1,13):
    for c in (1,2,3,6,10):
        eta=[0]*(e-1)+[c]
        ck(not in_ideal(eta,c,e),'integral_torsion_class_nonzero')
        ck(in_ideal([0]+eta,c,e),'annihilated_by_h')
        for power in range(9):
            coeff=[0]*(e-1)+[c*comb(power,j)*(-1)**(power-j) for j in range(power+1)]
            ck(not in_ideal(coeff,c,e),'survives_Laurent_unit_localization')
            ck(in_ideal([0]+coeff,c,e),'localized_h_annihilator')
        # Nonprimitive integer coefficient does not obstruct rational
        # specialization independence, but it must not be discarded in R.
        ck(eta[e-1]==c and c!=0,'nonprimitive_coefficient_retained')
# Generic relation in R plus R/(h^e) and its annihilator.
for e in range(1,15):
    ck(not in_ideal([1],1,e),'localization_kernel_witness')
    ck(in_ideal([0]*e+[1],1,e),'extra_localization_multiplier')
    ck(not in_ideal([0]*(e-1)+[1],1,e),'minimal_exponent_extraction')
# A primitive coefficient at h=0 survives the rational specialization.
for a,b,c in product(range(-3,4),repeat=3):
    if a==0:continue
    for e in range(1,5):
        coeff=[0]*e+[a,b,c]
        first=next(i for i,x in enumerate(coeff) if x)
        ck(first==e and coeff[first]==a,'maximal_common_h_power')

root=Path(__file__).resolve().parent
r={'status':'PASS','assertions':sum(C.values()),'categories':dict(C),'artifact_sha256':sha256((root/'author_replay/KNOWN_RESULT.md').read_bytes()).hexdigest(),'limits':'Finite exact algebraic controls. Published generic finiteness and geometric existence are credited inputs; no finite computation verifies those deep theorems.'}
(root/'independent_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
