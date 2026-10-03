#!/usr/bin/env python3
"""Independent finite arithmetic audit; no gauge-theory or realization claims.

This file does not import, execute, or read the author's verifier. The test ranges
are held fixed to make its coverage directly comparable with the frozen packet.
The two kernel descriptions are published inputs, not proved by this program.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
from math import gcd
import json

counts = Counter()
def require(label, value):
    assert value, label
    counts[label] += 1

def original_order(k, r):
    if k == 0 or k == 4:
        return 1
    if k == 1 or k == 2:
        return gcd(r, 2)
    return gcd(r, 24) if r % 2 == 0 else gcd(r - 3, 24) // 2

def primary_order(k, r):
    if k == 0 or k == 4:
        return 1
    if k == 1 or k == 2:
        return 1 + (r % 2 == 0)
    # Primary components from Bauer Proposition 6.1; exponent zero is trivial.
    exponent_2 = {0:3, 1:0, 2:1, 3:2, 4:2, 5:0, 6:1, 7:1}[r % 8]
    return (2 ** exponent_2) * (3 if r % 3 == 0 else 1)

for r, k in product(range(2, 50), range(5)):
    bp = 2*r-k-1
    if bp > 1:
        require('published_kernel_formula_crosscheck', original_order(k,r) == primary_order(k,r))
        if k in (1,2) and original_order(k,r) != 1:
            require('witness_congruence', not r % 2)
            require('witness_congruence', (bp+k+1) % 4 == 0)

for bp,bm,r in product(range(2,19),range(20),range(-4,13)):
    # Characteristic-square index congruence is an arithmetic input only.
    signature = bp-bm
    characteristic_square = signature+8*r
    euler = 2+bp+bm
    expected = Fraction(characteristic_square - 2*euler - 3*signature, 4)
    require('index_identity', 4*expected == 8*r-4-4*bp)
    require('index_parity', expected.denominator == 1 and (expected+bp+1) % 2 == 0)

for m in range(1,9):
    # Sum Euler characteristics, then subtract two for each neck.
    euler = sum([24]*m)-2*(m-1)
    signature = sum([-16]*m)
    require('connected_sum_recurrence', euler == 22*m+2 and signature == -16*m)
    require('connected_sum_recurrence', (euler-2, signature) == (3*m+19*m,3*m-19*m))
    require('connected_sum_spin_dimension', (-2*euler-3*signature) == 4*(m-1))

Q = (1,-1,-1)
C = (0,1,1)
def pairing(v,w):
    return sum(q*x*y for q,x,y in zip(Q,v,w))
def reflect(v):
    p = pairing(v,C)
    return tuple(x+p*y for x,y in zip(v,C))
for v in product(range(-5,6),repeat=3):
    rv = reflect(v)
    difference = tuple(y-x for x,y in zip(v,rv))
    require('sphere_reflection', reflect(rv) == v)
    require('sphere_reflection', pairing(v,v) == pairing(rv,rv))
    require('sphere_reflection', pairing(difference,difference) == -2*pairing(v,C)**2)

# RP^3 has no rational H1 or H2; the removed disk bundles each have
# Euler characteristic two and one negative direction.
euler = 24+24-2-2
signature = -16-16-(-1)-(-1)
b2 = euler-2
require('minus_two_gluing_arithmetic', (euler,signature,0,(b2+signature)//2,(b2-signature)//2) == (44,-30,0,6,36))

for n in range(2,33):
    bp,bm = 4*n-2,20*n-2
    euler,signature = 2+bp+bm,bp-bm
    require('fkm_family_indices', (euler,signature) == (24*n-2,-16*n))
    require('fkm_family_indices', -signature == 8*(2*n))
    require('fkm_family_indices', -2*euler-3*signature == 4)
    require('fkm_family_target_order', primary_order(1,2*n) == 2)

small = {}
for m in range(1,129):
    degrees = []
    for q in range(1,65):
        euler,signature = Fraction(22*m+2,q),Fraction(-16*m,q)
        positive = (euler+signature-2)/2
        negative = (euler-signature-2)/2
        integral = all(t == int(t) for t in [euler,signature,positive,negative])
        # The only possible prime is two: q divides 16 and 3m+1.
        divides = (16 % q == 0 and (3*m+1) % q == 0)
        require('quotient_degree_equivalence', integral == divides)
        if integral:
            degrees.append(q)
            require('quotient_betti_nonnegative', min(positive,negative) >= 0)
    if m <= 8:
        small[str(m)] = degrees
for m,expected in [(2,[1]),(3,[1,2]),(4,[1])]:
    require('quotient_small_cases', small[str(m)] == expected)

print(json.dumps({'result':'PASS','total_assertions':sum(counts.values()),'assertions_by_family':dict(sorted(counts.items())), 'small_quotient_degrees':small, 'scope':'Independent finite arithmetic reimplementation only. Published stable-cohomotopy formulas are inputs; no invariant, manifold, or irreducibility computation.'},indent=2,sort_keys=True))
