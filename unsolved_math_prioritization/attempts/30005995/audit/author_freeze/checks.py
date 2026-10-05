#!/usr/bin/env python3
"""Exact finite checks supporting REPORT.md, not a verification of the full PDE conjecture.
Python standard library only. Deterministic output; no sources or datasets required.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import sys

counts = {}
def check(group, condition):
    counts[group] = counts.get(group, 0) + 1
    if not condition:
        raise AssertionError(group)

def G(x):
    p, q = x
    return p+q, q**3-p

def dot(x,y):
    return sum(a*b for a,b in zip(x,y))

def sub(x,y):
    return tuple(a-b for a,b in zip(x,y))

points = list(product([F(i,2) for i in range(-4,5)], repeat=2))
for x in points:
    for y in points:
        if x == y:
            continue
        p,q = x; r,s = y
        value = dot(sub(G(x),G(y)),sub(x,y))
        formula = (p-r)**2 + (q-s)**2*(q*q+q*s+s*s)
        check('monotonicity_identity', value == formula)
        check('strict_positivity_on_grid', value > 0)
        # Two-state normal-flux pairing cannot vanish.
        check('jump_flux_pairing', value != 0)

for q in [F(i,3) for i in range(-15,16)]:
    d=1+3*q*q
    A=((F(1),F(1)),(F(-1),3*q*q))
    inv=((3*q*q/d,-1/d),(1/d,1/d))
    for i,j in product(range(2),repeat=2):
        check('matrix_inverse',sum(A[i][k]*inv[k][j] for k in range(2)) == int(i==j))
    check('inverse_symmetric_offdiagonal', inv[0][1]+inv[1][0] == 0)
    check('inverse_degeneracy_location', (inv[0][0] == 0) == (q==0))
    check('inverse_other_eigenvalue_positive',inv[1][1]>0)

previous=F(0)
for n in range(1,65):
    t=F(1,2**n)
    x=(F(0),t); dg=G(x)
    plus=tuple(a+b for a,b in zip(x,dg)); minus=tuple(a-b for a,b in zip(x,dg))
    ratio=dot(minus,minus)/dot(plus,plus)
    formula=(2-2*t*t+t**4)/(2+2*t*t+t**4)
    check('minty_ratio_identity',ratio==formula)
    check('minty_strict_but_approaching_one',previous<ratio<1)
    check('minty_exact_deficit',1-ratio==4*t*t/(2+2*t*t+t**4))
    previous=ratio

for n in range(1,65):
    c=F(1,2**n); R=F(1,2**(3*n+4))
    check('spike_relative_radius',R<=c/64)
    check('spike_inside_unit_ball',c+R<1)
    for m in range(n+1,65):
        cm=F(1,2**m); Rm=F(1,2**(3*m+4))
        check('spike_disjoint_supports',c-cm>R+Rm)
    tail=R*R/(1-F(1,64))
    check('spike_exact_area_tail',tail==c**6/252)
    check('spike_density_at_dyadic_radius',tail/c**2<=F(16,63)*c**4)
    energy_coefficient=sum((F(1,2**k) for k in range(1,n+1)), F(0))
    check('spike_energy_partial_sum',energy_coefficient==1-F(1,2**n))

result={
    'problem_id':30005995,
    'verdict':'NO RESOLUTION',
    'approaches_completed':5,
    'assertions':sum(counts.values()),
    'groups':counts,
    'result':'PASS',
    'limits':[
        'Finite exact checks support algebra and explicit spike bounds only.',
        'Analytic propositions and the conditional blow-up theorem require mathematical review.',
        'Imported literature theorems are not formally verified by this script.',
        'No numerical check is a proof of the unrestricted PDE conjecture.'
    ]
}
print(json.dumps(result,indent=2,sort_keys=True))
