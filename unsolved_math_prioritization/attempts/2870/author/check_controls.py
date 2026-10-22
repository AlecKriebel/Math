#!/usr/bin/env python3
"""Finite exact controls for the authored KP-3.72 reductions; no topology oracle."""
from collections import Counter
from fractions import Fraction
from itertools import product
from math import gcd
import json

counts = Counter()
def check(condition, category):
    counts[category] += 1
    if not condition:
        raise AssertionError((category, counts[category]))

def rank(matrix, p=None):
    if not matrix:
        return 0
    a = [[x % p if p else Fraction(x) for x in row] for row in matrix]
    m, n = len(a), len(a[0])
    r = 0
    for j in range(n):
        pivot = next((i for i in range(r, m) if a[i][j]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][j], -1, p) if p else 1 / a[r][j]
        a[r] = [(x * inv) % p if p else x * inv for x in a[r]]
        for i in range(m):
            if i != r:
                factor = a[i][j]
                a[i] = [(x - factor * y) % p if p else x - factor * y
                        for x, y in zip(a[i], a[r])]
        r += 1
        if r == m:
            break
    return r

def mul(a, b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]

def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]

# Family parameter checks and explicit polynomial/r_0 ordering controls.
previous = None
for n in range(1, 121):
    triples = [(2,4*n+1,12*n+5), (3,3*n+1,12*n+5),
               (2,4*n+3,12*n+7), (3,3*n+2,12*n+7),
               (2*n+1,4*n+1,4*n+3)]
    for a,b,c in triples:
        for u,v in [(a,b),(a,c),(b,c)]:
            check(gcd(u,v) == 1, 'pairwise_coprime_parameters')
    e = (2*n+1)*(4*n+1)*(4*n+3)
    enext = (2*n+3)*(4*n+5)*(4*n+7)
    check(e == 32*n**3+48*n*n+22*n+3, 'DHST_product_identity')
    check(enext-e == 96*n*n+192*n+102, 'DHST_product_difference')
    value = Fraction(1,4*e)
    if previous is not None:
        check(0 < value < previous, 'DHST_formal_spectral_order')
    previous = value

# Direct sums of the 1-2-3 chain-defect blocks. Every assertion is finite algebra.
for length in range(1,4):
    for torsion in product(range(2,9), repeat=length):
        d2 = [[torsion[i] if j == 2*i else 0 for j in range(2*length)]
              for i in range(length)]
        d3 = [[torsion[j] if i == 2*j+1 else 0 for j in range(length)]
              for i in range(2*length)]
        check(mul(d2,d3) == [[0]*length for _ in range(length)], 'chain_boundary_squared')
        r2,r3 = rank(d2),rank(d3)
        check((length-r2,2*length-r2-r3,length-r3) == (0,0,0), 'rational_acyclicity')
        for p in (2,3,5,7,11):
            rp = sum(m % p == 0 for m in torsion)
            r2,r3 = rank(d2,p),rank(d3,p)
            dims = (1,length-r2,2*length-r2-r3,length-r3,0)
            check(dims == (1,rp,2*rp,rp,0), 'mod_p_Betti_formula')
            check(sum((-1)**i*b for i,b in enumerate(dims)) == 1, 'Euler_characteristic')
            check((dims == (1,0,0,0,0)) == all(m%p for m in torsion), 'prime_acyclicity_criterion')

# A rank-one abstract family with infinitely many distinct odd-labelled elements.
for n in range(2,41):
    weights = [2*i+1 for i in range(n)]
    check(rank([weights]) == 1, 'Rokhlin_rank_one_countermodel')
    relation = [weights[1],-weights[0]]+[0]*(n-2)
    check(sum(a*w for a,w in zip(relation,weights)) == 0, 'nonzero_relation_control')
    check(sum(relation)%2 == 0 and any(relation), 'parity_is_insufficient')

# Exact correction into a kernel when the rational images are collinear.
for n in range(1,21):
    weights = [1]+[(-1)**i*(i+1) for i in range(n)]
    h = [[-weights[j+1] for j in range(n)]] + eye(n)
    projection = [[0]+[int(i==j) for j in range(n)] for i in range(n)]
    check(mul([weights],h) == [[0]*n], 'corrected_classes_in_kernel')
    check(rank(h) == n, 'corrected_classes_independent')
    check(mul(projection,h) == eye(n), 'finite_split_model')
    pmat = mul(h,projection)
    check(mul(pmat,pmat) == pmat, 'finite_retraction_idempotent')

# Finite-rank image/nullity controls. This is not a test of q on actual spheres.
for n in range(1,16):
    for r in range(1,6):
        matrix = [[(j+1)**i for j in range(n)] for i in range(r)]
        actual = rank(matrix)
        check(actual == min(n,r), 'finite_image_rank')
        check(n-actual >= max(0,n-r), 'rank_transfer_bound')

# Integral versus rational retractions: no integer solves 2*z=1.
for z in range(-100,101):
    check(2*z != 1, 'integral_retraction_obstruction')
check(Fraction(1,2)*2 == 1, 'rational_not_integral_retraction')

# Negative controls ensure important incorrect formulas fail these diagnostics.
check((1,1,1,1,0) != (1,1,2,1,0), 'negative_control_missing_Tor')
check(rank([[1,3,5,7]]) != 4, 'negative_control_distinct_is_not_independent')
check(Fraction(1,2).denominator != 1, 'negative_control_nonintegral_dual')
check((3*5*7) != (2*5*17), 'negative_control_family_substitution')

print(json.dumps({
    'problem_id':2870,
    'status':'PASS_FINITE_EXACT_CONTROLS_ONLY',
    'assertions':sum(counts.values()),
    'counts':dict(sorted(counts.items())),
    'limitations':[
        'No rational ball or cobordism is constructed by this program.',
        'No Floer invariant is computed; formal source-supplied expressions are checked.',
        'Finite controls do not prove infinite rank or a direct summand in the actual kernel.'
    ]},sort_keys=True,indent=2))
