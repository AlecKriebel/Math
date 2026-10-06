#!/usr/bin/env python3
"""Exact finite/symbolic consistency checks, not a general-conjecture proof."""
import sys
if not (sys.flags.isolated and sys.flags.no_site):
    sys.stderr.write("ISOLATED STARTUP REQUIRED: use python -I -S -B (optionally -O)\n")
    sys.exit(2)

from collections import Counter
from fractions import Fraction as F
import hashlib
import json


def need(condition, message):
    if not condition:
        raise ValueError(message)


def weight_formula(k, j):
    if abs(j) > k:
        return 0
    return (k - abs(j)) // 2 + 1


# Sparse Laurent polynomials in a,x,u,r over Q, for exact identities.
N = 4
ZERO = {}
ONE = {(0, 0, 0, 0): F(1)}


def mono(coefficient=1, powers=(0, 0, 0, 0)):
    return {tuple(powers): F(coefficient)} if coefficient else {}


def add(*terms):
    out = {}
    for p in terms:
        for e, c in p.items():
            out[e] = out.get(e, F(0)) + c
    return {e: c for e, c in out.items() if c}


def neg(p):
    return {e: -c for e, c in p.items()}


def mul(p, q):
    out = {}
    for e, c in p.items():
        for f, d in q.items():
            ef = tuple(e[j] + f[j] for j in range(N))
            out[ef] = out.get(ef, F(0)) + c*d
    return {e: c for e, c in out.items() if c}


def scale(p, c):
    return mul(mono(c), p)


def matrix_mul(A, B):
    return [[add(*(mul(A[i][h], B[h][j]) for h in range(2)))
             for j in range(2)] for i in range(2)]


def main():
    weights_checked = 0
    monomials_counted = 0
    max_by_k = []
    for k in range(65):
        counts = Counter()
        for a in range(k+1):
            for d in range(k-a+1):
                b = k-a-d
                need(b >= 0, 'nonnegative exponent')
                counts[d-a] += 1
                monomials_counted += 1
        for j in range(-k-2, k+3):
            need(counts[j] == weight_formula(k, j), 'weight formula')
            weights_checked += 1
        need(sum(counts.values()) == (k+1)*(k+2)//2, 'dimension formula')
        need(max(counts.values()) == k//2+1, 'maximal multiplicity')
        max_by_k.append(max(counts.values()))
    need(max_by_k[1] == 1 and all(v >= 2 for v in max_by_k[2:]),
         'single level versus tensor powers')
    need(weight_formula(2, 0) == 2, 'explicit degree-two collision')
    need((-1, 0, 1) == tuple(sorted(d-a for a,b,d in [(1,0,0),(0,1,0),(0,0,1)])),
         'degree-one distinct weights')

    level_samples = 0
    for c in [F(-9,10), F(-3,4), F(-1,2), F(0), F(1,2), F(3,4), F(9,10)]:
        low = max(F(0), -c)
        high = (1-c)/2
        need(high-low == (1-abs(c))/2 and high>low, 'interval width')
        seen = set()
        for j in range(1, 20):
            s = low + (high-low)*F(j,20)
            p0, p1, p2 = s+c, 1-2*s-c, s
            need(min(p0,p1,p2)>0, 'positive coordinates')
            need(p0+p1+p2 == 1, 'unit normalization')
            need(p0-p2 == c, 'moment level')
            need(p2 not in seen, 'orbit-distinguishing invariant')
            seen.add(p2)
            level_samples += 1
    need([F(1),F(0),F(0)][0]-[F(1),F(0),F(0)][2] == 1, 'top endpoint')
    need([F(0),F(0),F(1)][0]-[F(0),F(0),F(1)][2] == -1, 'bottom endpoint')

    a = mono(powers=(1,0,0,0))
    x = mono(powers=(0,1,0,0))
    u = mono(powers=(0,0,1,0))
    invu = mono(powers=(0,0,-1,0))
    r = mono(powers=(0,0,0,1))
    invr = mono(powers=(0,0,0,-1))
    a2, x2 = mul(a,a), mul(x,x)
    C = add(a2,x2)
    b = neg(mul(C,invu))
    X = [[x,b],[u,neg(x)]]
    square = matrix_mul(X,X)
    need(square == [[neg(a2), ZERO],[ZERO, neg(a2)]], 'elliptic matrix identity')
    det = add(mul(x,neg(x)),neg(mul(b,u)))
    need(det == a2, 'constant determinant')
    y = scale(add(u,neg(mul(C,invu))), F(1,2))
    z = scale(add(u,mul(C,invu)), F(1,2))
    need(add(mul(z,z),neg(x2),neg(mul(y,y))) == a2, 'hyperboloid identity')
    D, Di = [[r,ZERO],[ZERO,invr]], [[invr,ZERO],[ZERO,r]]
    conjugate = matrix_mul(matrix_mul(D,X),Di)
    need(conjugate == [[x,mul(mul(r,r),b)],
                      [mul(mul(invr,invr),u),neg(x)]], 'diagonal action')

    transitivity_cases = 0
    for aa in [F(1,2), F(1), F(2)]:
        for xx in [F(-3),F(-1,2),F(0),F(2,3),F(3)]:
            CC=aa*aa+xx*xx
            for u1 in [F(1,3),F(1),F(3)]:
                for u2 in [F(1,4),F(2),F(5)]:
                    r2=u1/u2
                    need(r2>0 and (-CC/u1)*r2 == -CC/u2 and u1/r2 == u2,
                         'positive diagonal transitivity')
                    transitivity_cases += 1
    central_cases = 0
    for t in [F(-2),F(0),F(1,2),F(3)]:
        characters = {(j,t) for j in [-1,0,1]}
        need(len(characters)==3, 'distinct product characters')
        central_cases += 1
    return {
        'schema':1,
        'classification':'exact consistency checks; not a proof of the original conjecture',
        'tensor_degrees_checked':[0,64],
        'weight_values_checked':weights_checked,
        'monomials_counted':monomials_counted,
        'rational_level_samples':level_samples,
        'laurent_polynomial_identities':4,
        'rational_transitivity_cases':transitivity_cases,
        'central_character_samples':central_cases,
        'degree_one_weights':[-1,0,1],
        'degree_two_zero_weight_multiplicity':2,
        'all_checks_passed':True,
        'finite_evidence_limit':'All-parameter claims and cardinality are proved in prose, not inferred from the samples.'
    }


if __name__ == '__main__':
    print(json.dumps(main(), sort_keys=True, indent=2))
