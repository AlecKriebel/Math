#!/usr/bin/env python3
"""Deterministic bookkeeping support, not evidence for the continuous theorem.

Tests fixed-cell geometry, positive and negative coefficients, and all
anchored variation menus through M=7. The proof is in
restriction_independent.md; these finite tests are not its substitute.
"""
from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import combinations, product
import json
import random

getcontext().prec = 70
h, q, rho = Fraction(1, 8), Fraction(1, 16), Fraction(3, 16)

def dec(x):
    if isinstance(x, Fraction):
        return Decimal(x.numerator) / Decimal(x.denominator)
    return Decimal(x)

def overlap(a, b):
    return -h-min(a,b), h-max(a,b)

def coeff(k, a, b):
    lo, hi = overlap(a,b)
    return abs(dec(k+hi)).ln()-abs(dec(k+lo)).ln()

def variation(values, r=3):
    out = 0.0
    for size in range(1, len(values)):
        for menu in combinations(range(1, len(values)), size):
            nodes = (0,)+menu
            value = sum(abs(values[b]-values[a])**r
                        for a,b in zip(nodes, nodes[1:]))**(1/r)
            out = max(out, value)
    return out

phases = [Fraction(0), -q+Fraction(1, 2**16),
          q-Fraction(1, 2**16), -q/2, q/2]
ks = list(range(-32,0))+list(range(1,33))+[-10**6,10**6]
checks = 0
max_normalized_error = Decimal(0)
for a,b in product(phases, repeat=2):
    lo,hi = overlap(a,b)
    ell = hi-lo
    assert h <= ell <= 2*h
    assert -rho <= lo < hi <= rho
    for k,l in product(range(-3,4),repeat=2):
        left = max(k-h-a,l-h-b)
        right = min(k+h-a,l+h-b)
        assert (left < right) == (k == l)
        checks += 1
    for k in ks:
        K = coeff(k,a,b)
        assert K*dec(k)>0
        err = abs(K-dec(ell)/dec(k))
        normalized = err*dec(k*k)/dec(ell)
        assert normalized <= Decimal(3)/Decimal(13)
        assert abs(K+coeff(-k,-a,-b)) < Decimal('1e-60')
        max_normalized_error = max(max_normalized_error,normalized)
        checks += 3
        for N in range(5):
            # All nonzero windows have constant sign. Exact radial extrema.
            radial_lo = k+lo if k>0 else -k-hi
            radial_hi = k+hi if k>0 else -k-lo
            included = radial_lo > Fraction(1,2) and radial_hi < N+Fraction(1,2)
            excluded = radial_hi < Fraction(1,2) or radial_lo > N+Fraction(1,2)
            assert included == (0<abs(k)<=N)
            assert included or excluded
            checks += 1
    for N in range(5):
        assert max(abs(lo),abs(hi)) < Fraction(1,2)
        checks += 1

rng = random.Random(20261006)
M = 7
for trial in range(30):
    a,b = rng.choice(phases),rng.choice(phases)
    lo,hi = overlap(a,b)
    ell = float(hi-lo)
    pk = {k: complex(rng.uniform(-2,2),rng.uniform(-2,2))
          for k in range(-M,M+1) if k}
    d,e,c = [0j],[0j],[0j]
    total_error = 0.0
    bound = 0.0
    for n in range(1,M+1):
        di,ei,ci = 0j,0j,0j
        for k in (-n,n):
            K = float(coeff(k,a,b))
            delta = K-ell/k
            di += pk[k]/k
            ei += delta*pk[k]
            ci += K*pk[k]
            total_error += abs(delta*pk[k])
            bound += (3/13)*ell*abs(pk[k])/(k*k)
        d.append(d[-1]+di)
        e.append(e[-1]+ei)
        c.append(c[-1]+ci)
        assert abs(c[-1]-ell*d[-1]-e[-1]) < 1e-12
        checks += 1
    assert variation(e) <= total_error+1e-12
    assert total_error <= bound+1e-12
    assert ell*variation(d) <= variation(c)+variation(e)+1e-12
    checks += 3

print(json.dumps({
    'status': 'PASS',
    'purpose': 'finite kernel/geometry/variation bookkeeping only',
    'decimal_precision': getcontext().prec,
    'phase_pairs': len(phases)**2,
    'checks': checks,
    'largest_sampled_k_squared_relative_error': str(max_normalized_error),
    'proved_upper_bound_for_that_quantity': '3/13',
    'random_seed': 20261006,
    'all_anchored_partition_menus_through_M': M,
    'random_complex_increment_trials': 30,
}, indent=2))
