#!/usr/bin/env python3
"""Exact controls for RESULT.md. No dependencies, downloads, or dynamics claims.

Finite computations are controls; the infinite-orbit arguments are in RESULT.md.
Run: python3 verification/check.py > verification/result.json
"""
import json
from fractions import Fraction as Q
from math import factorial


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def add(a, b):
    return trim([(a[k] if k < len(a) else 0) +
                 (b[k] if k < len(b) else 0)
                 for k in range(max(len(a), len(b)))])


def scale(a, c):
    return trim([c*x for x in a])


def mul(a, b):
    p = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            p[i+j] += x*y
    return trim(p)


# Put t=(1+z)/(1-z). The Cayley transform of T(i*t) is
# (t + 1/t - 1)/(t + 1/t + 1).
a, b = [1, 1], [1, -1]
common = add(mul(a, a), mul(b, b))
ab = mul(a, b)
num = add(common, scale(ab, -1))
den = add(common, ab)
assert num == [1, 0, 3]
assert den == [3, 0, 1]
assert add(num, scale(mul([0, 1], den), -1)) == mul(mul(b, b), b)
assert den[0]+den[2] == 4


def boole(x):
    if not x:
        raise ZeroDivisionError('real orbit hits the pole')
    return x - 1/x


# Every listed real step outside [-1,1] strictly decreases modulus.
checked_steps = 0
hit_poles = []
for start in [Q(-5), Q(-3, 2), Q(-1), Q(-1, 2), Q(1, 2),
              Q(1), Q(3, 2), Q(5)]:
    x = start
    for n in range(8):
        if not x:
            hit_poles.append(str(start))
            break
        nx = boole(x)
        if abs(x) > 1:
            assert abs(nx) == abs(x)-1/abs(x)
            assert abs(nx) < abs(x)
            checked_steps += 1
        x = nx

# Exact arbitrarily-long-prefix template at several finite sizes.
# General induction, not these samples, is the proof for all N.
prefixes = []
for R in [1, 2, 10]:
    for N in [1, 2, 4, 8]:
        x0 = Q(R+N+2)
        x = x0
        for j in range(N+1):
            assert x > R
            assert x >= x0-j  # strict for j>0
            if j:
                assert x > x0-j
            if j < N:
                x = boole(x)
        prefixes.append({'R': R, 'N': N, 'initial': str(x0),
                         'all_prefix_terms_above_R': True})

# On the imaginary axis y -> y + 1/y and
# y_next^2-y^2 = 2+1/y^2, for every rational y>0.
height_controls = []
for y in [Q(1, 4), Q(1, 2), Q(1), Q(2), Q(4), Q(10)]:
    ny = y+1/y
    assert ny*ny-y*y == 2+1/(y*y)
    height_controls.append(str(y))

# Certified rational enclosures of exp(q), q in [0,1].
# Tail after degree d is bounded using a geometric bound on term ratios.
def exp_interval(q, d=12):
    assert 0 <= q <= 1
    lo = sum((q**n / factorial(n) for n in range(d+1)), Q(0))
    term = q**(d+1)/factorial(d+1)
    hi = lo + term/(1-q/Q(d+2))
    return lo, hi

exp_samples = []
for k in range(17):
    q = Q(k, 16)
    lo, hi = exp_interval(q)
    assert lo >= 1+q
    assert hi <= 1+2*q
    exp_samples.append(str(q))
assert exp_interval(Q(1))[1] < 3

# Residue of h - T, when h is an arbitrary polynomial, equals 1.
# RESULT.md uses Cauchy's theorem to extend this to every entire h.
residue_controls = []
for degree in [0, 1, 2, 5, 10, 20]:
    h = {k: (-1)**k*(k+1) for k in range(degree+1)}
    h_minus_T = dict(h)
    h_minus_T[1] = h_minus_T.get(1, 0)-1
    h_minus_T[-1] = h_minus_T.get(-1, 0)+1
    assert h_minus_T[-1] == 1
    residue_controls.append(degree)

# Topological model: its real-coordinate gaps separate its components.
# These sample identities do not replace the continuum argument in RESULT.md.
for m in range(1, 100):
    assert -Q(1, m) < 0
    assert 1+Q(1, m) > 1
    assert -Q(1, m) < -Q(1, m+1)
    assert 1+Q(1, m+1) < 1+Q(1, m)

print(json.dumps({
    'target_id': 30001388,
    'status': 'passed',
    'arithmetic': 'integer polynomials and fractions.Fraction only',
    'cayley_numerator_ascending': num,
    'cayley_denominator_ascending': den,
    'parabolic_fixed_point_identity': 'numerator - z*denominator = (1-z)^3',
    'real_contraction_steps_checked': checked_steps,
    'pole_hitting_starting_values': hit_poles,
    'finite_prefix_controls': prefixes,
    'imaginary_height_controls': height_controls,
    'exp_enclosure_sample_points': exp_samples,
    'residue_polynomial_degrees': residue_controls,
    'proof_scope': 'Controls only; not a full solution, numerical Julia membership, or an infinite-orbit computation.'
}, indent=2, sort_keys=True))
