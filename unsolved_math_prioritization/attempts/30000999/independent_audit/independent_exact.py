#!/usr/bin/env python3
"""Independent finite exact controls. These are not a proof of the theorem.

Uses no author-module imports. Python standard library only. The accompanying
AUDIT.md supplies the all-parameter analytic reasoning.
"""
from fractions import Fraction as Q
from math import comb, prod
import json

counts = {}
def check(label, condition):
    if not condition:
        raise AssertionError(label)
    counts[label] = counts.get(label, 0) + 1

def add(p, q):
    r = dict(p)
    for e, c in q.items():
        r[e] = r.get(e, Q(0)) + c
    return {e: c for e, c in r.items() if c}

def scale(p, a):
    return {e: a*c for e, c in p.items() if a*c}

def mul(p, q):
    r = {}
    for e, a in p.items():
        for f, b in q.items():
            g = tuple(x+y for x, y in zip(e, f))
            r[g] = r.get(g, Q(0)) + a*b
    return {e: c for e, c in r.items() if c}

def diff(p, j):
    r = {}
    for e, a in p.items():
        if e[j]:
            f = list(e)
            f[j] -= 1
            r[tuple(f)] = a*e[j]
    return r

def hpoly(k):
    return {(k-j, j): Q((-1)**(j//2)*comb(k, j))
            for j in range(0, k+1, 2)}

def evaluate(poly, x, y):
    return sum(c*x**e[0]*y**e[1] for e, c in poly.items())

def eigen_product(n, k):
    return (-1)**(k//2)*prod(Q(2*j+1, n-1+2*j) for j in range(k//2))

def moment_even(n, q):
    assert q >= 0 and q % 2 == 0
    return prod(Q(2*j, n+2*j-2) for j in range(1, q//2+1))

# A new polynomial control: exact Euclidean gradient norm identity plus Euler.
# Orthogonal projection then gives |grad_S H|^2 = k^2(r^(2k-2)-H^2).
for k in range(1, 41):
    h = hpoly(k)
    dx, dy = diff(h, 0), diff(h, 1)
    gradient_square = add(mul(dx, dx), mul(dy, dy))
    target = {(2*(k-1-j), 2*j): Q(k*k*comb(k-1, j))
              for j in range(k)}
    check('euclidean_gradient_norm_polynomial', gradient_square == target)
    euler = add(mul({(1, 0): Q(1)}, dx), mul({(0, 1): Q(1)}, dy))
    check('euler_homogeneous_identity', euler == scale(h, k))
    check('harmonic_all_degrees', not add(diff(dx, 0), diff(dy, 1)))

# Independent recurrence route to the eigenvalue: normalized Gegenbauer
# values at 0 and 1, rather than the author's equator-frame integration.
# (j+1) C_(j+1)(t)=2(j+alpha)t C_j(t)-(j+2alpha-1)C_(j-1)(t).
for n in range(3, 15):
    alpha = Q(n-2, 2)
    c0, c1 = [Q(1), Q(0)], [Q(1), 2*alpha]
    for j in range(1, 100):
        c0.append(-(j+2*alpha-1)*c0[-2]/(j+1))
        c1.append((2*(j+alpha)*c1[-1]-(j+2*alpha-1)*c1[-2])/(j+1))
    for k in range(2, 101, 2):
        check('gegenbauer_eigenvalue', c0[k]/c1[k] == eigen_product(n, k))
        check('eigenvalue_nonzero_bounded', 0 < abs(eigen_product(n, k)) < 1)
    for k in range(1, 100, 2):
        check('gegenbauer_odd_nullspace', c0[k] == 0)

# Exact integrated gradient-energy identity is a sensitive independent check
# of the beta parameter, Laplacian eigenvalue, and k versus m conventions.
for n in range(3, 15):
    for k in range(1, 51):
        integrated_gradient = k*k*(moment_even(n, 2*k-2)-moment_even(n, 2*k)/2)
        laplacian_energy = Q(k*(k+n-2), 2)*moment_even(n, 2*k)
        check('integrated_gradient_energy', integrated_gradient == laplacian_energy)

# Circle modes, independently by the shift theta -> theta+pi/2.
for k in range(2, 102, 2):
    check('circle_eigenvalue_modulus_one', eigen_product(2, k) == (-1)**(k//2))

# Direct expanded continuity equation with the reciprocal density retained.
# This catches a reversed flow, missing density Jacobian, or denominator sign.
for n in (3, 4, 8):
    points = [
        [Q(3, 5), Q(4, 5)] + [Q(0)]*(n-2),
        [Q(2, 3), Q(1, 3), Q(2, 3)] + [Q(0)]*(n-3),
        [Q(0), Q(0), Q(1)] + [Q(0)]*(n-3),
    ]
    for k in (2, 4, 6, 10, 20):
        h = hpoly(k)
        L = k*(k+n-2)
        lam = eigen_product(n, k)
        for x in points:
            assert sum(z*z for z in x) == 1
            H = evaluate(h, *x[:2])
            ambient = [evaluate(diff(h, 0), *x[:2]),
                       evaluate(diff(h, 1), *x[:2])] + [Q(0)]*(n-2)
            gs = [v-k*H*z for v, z in zip(ambient, x)]
            G2 = sum(v*v for v in gs)
            check('tangent_gradient', sum(v*z for v, z in zip(gs, x)) == 0)
            check('projected_gradient_square', G2 == k*k*((x[0]**2+x[1]**2)**(k-1)-H*H))
            for a in (Q(1, 10), Q(1, 2), Q(999, 1000)):
                b = a*lam
                for t in (Q(0), Q(1, 4), Q(1, 2), Q(1)):
                    eta = 1+t*b*H
                    check('strict_density_lower_bound', eta >= 1-a > 0)
                    grad_eta_dot_v = t*b*b*G2/(L*eta)
                    div_v = b*(-L*H/eta - t*b*G2/(eta*eta))/L
                    check('expanded_continuity_equation', b*H+grad_eta_dot_v+eta*div_v == 0)

# First fixed dimension has alpha=1/2, not zero: asymptotic exponent >0
# for noninteger rational p as well as integer p. This is algebra only.
for n in range(3, 15):
    for p in (Q(1), Q(5, 4), Q(3, 2), Q(2), Q(7, 2), Q(1000)):
        alpha = Q(n-2, 2)
        check('ratio_exponent_cancellation', -alpha-(-alpha-alpha/p) == alpha/p > 0)

print(json.dumps({
    'status': 'PASS',
    'arithmetic': 'exact fractions.Fraction and integer polynomial arithmetic',
    'author_imports': False,
    'counts': counts,
    'total_checks': sum(counts.values()),
    'limitations': [
        'Finite checks do not establish all dimensions, degrees, or Wasserstein orders.',
        'No numerical Wasserstein optimization is used.',
        'The smooth-flow argument and asymptotic limits are audited analytically in AUDIT.md.'
    ]
}, indent=2, sort_keys=True))
