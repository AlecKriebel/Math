"""Independent finite arithmetic checks; these do not certify universal theorems."""
if globals().get('_AUDIT_VERIFIED') != 'height-counts-30002439-independent-v1':
    raise SystemExit('Use the independent external bootstrap')
import sys
if not sys.flags.isolated or not sys.flags.no_site:
    raise SystemExit('Requires python -I -S')
import itertools
import json
import math
from fractions import Fraction

def need(ok, label):
    if not ok:
        raise RuntimeError(label)

def canonical(v):
    scale = 0
    for a in v:
        scale = math.gcd(scale, a)
    need(scale != 0, 'zero vector')
    if next(a for a in v if a) < 0:
        scale = -scale
    return tuple(a // scale for a in v)

def H(v):
    return max(abs(a) for a in canonical(v))

def mono(v, d):
    # Multiplication over multisets is independent of the author's compositions.
    return tuple(math.prod(v[i] for i in inds)
                 for inds in itertools.combinations_with_replacement(range(len(v)), d))

checks = {}
ct = 0
for r in (2, 3, 4):
    for v in itertools.product(range(-3, 4), repeat=r):
        if not any(v):
            continue
        for mask in range(1, 2**r):
            w = tuple(a for i, a in enumerate(v) if mask & (1 << i))
            if any(w):
                need(H(w) <= H(v), 'height under coordinate subset')
                ct += 1
checks['coordinate_subset_cases'] = ct
need(H((6, 10, 15)) == 15 and H((6, 10)) == 5, 'subset must be re-primitivized')
need(H((1, 1)) == 1 and H((101, 1)) == 101, 'arbitrary coordinate changes need not lower height')
checks['primitivity_and_bad_linear_change_examples'] = 2
ct = 0
for r in (2, 3, 4):
    points = {canonical(v) for v in itertools.product(range(-2, 3), repeat=r) if any(v)}
    for d in range(1, 7):
        for p in points:
            v = mono(p, d)
            need(len(v) == math.comb(r+d-1, d), 'symmetric power dimension')
            need(math.gcd(*v) == 1, 'pure-power primitivity')
            need(H(v) == H(p)**d, 'Veronese height')
            ct += 1
checks['multiset_veronese_cases'] = ct
ct = 0
for r in (2, 3):
    points = {canonical(v) for v in itertools.product(range(-3, 4), repeat=r) if any(v)}
    for d in range(1, 5):
        image = {canonical(mono(p, d)) for p in points}
        need(len(image) == len(points), 'finite Veronese injectivity')
        for B in (Fraction(1), Fraction(3, 2), Fraction(2), Fraction(7, 2), Fraction(8), Fraction(27), Fraction(81)):
            need(sum(H(q) <= B for q in image) == sum(H(p)**d <= B for p in points), 'threshold equality')
            ct += 1
checks['fractional_threshold_cases'] = ct
ct = 0
for n in range(1, 6):
    for d in range(1, 7):
        for T in (1, 2, 3, 17, 1009, 10**9):
            p = (T, 1) + (0,)*(n-1)
            q = (p[0]-T*p[1], p[1]) + p[2:]
            need(H(p) == T and H(mono(q, d)) == 1, 'large shear')
            ct += 1
checks['large_shear_cases'] = ct
ct = 0
for d in range(2, 201):
    for e in range(1, 31):
        delta = d*e
        need(delta >= d and delta != 1 and Fraction(2, delta) <= Fraction(2, d), 'curve-degree arithmetic')
        ct += 1
    need(Fraction(3, 2*d)+Fraction(2, d) == Fraction(7, 2*d), 'covering sum')
    need(Fraction(7, 2*d)-Fraction(3, d) == Fraction(1, 2*d), 'fixed surface gap')
checks['curve_degree_cases'] = ct
need(Fraction(43, 28)-Fraction(3, 2) == Fraction(1, 28), 'quartic gap')
checks['quadratic_surface_gap'] = '1/28'
ct = 0
for n in range(2, 51):
    for d in range(2, 51):
        need(d**n >= 4 and d*n > n+1, 'dimension-growth insufficient')
        ct += 1
checks['dimension_growth_cases'] = ct
ct = 0
for T in range(1, 151):
    # Mobius inversion independently counts coprime positive ordered pairs.
    mu = [0, 1] + [1]*(T-1)
    primes = []
    for p in range(2, T+1):
        if all(p % q for q in primes if q*q <= p):
            primes.append(p)
            for k in range(p, T+1, p):
                mu[k] *= -1
            for k in range(p*p, T+1, p*p):
                mu[k] = 0
    coprime = sum(mu[k]*(T//k)**2 for k in range(1, T+1))
    need(4*coprime >= T*T, 'Mobius coprime lower bound')
    ct += 1
checks['mobius_sharpness_cases'] = ct
print(json.dumps({'problem_id':30002439,'result':'PASS','checks':checks,'scope':'Independent finite corroboration; partial results only; no general solution or novelty certified'},sort_keys=True,indent=2))
