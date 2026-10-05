#!/usr/bin/env python3
"""Exact finite regression controls, not a certificate for analytic claims."""
from fractions import Fraction as F
import json
from math import isqrt


def q(a=0, b=0):
    return (F(a), F(b))


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def neg(x):
    return (-x[0], -x[1])


def sub(x, y):
    return add(x, neg(y))


def mul(x, y):
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def inv(x):
    norm = x[0] ** 2 + x[1] ** 2
    if not norm:
        raise ZeroDivisionError
    return (x[0] / norm, -x[1] / norm)


def div(x, y):
    return mul(x, inv(y))


def mm(A, B):
    return tuple(tuple(add(mul(A[i][0], B[0][j]), mul(A[i][1], B[1][j]))
                       for j in range(2)) for i in range(2))


def det(A):
    return sub(mul(A[0][0], A[1][1]), mul(A[0][1], A[1][0]))


def compute():
    counts = {}
    def check(label, truth):
        if not truth:
            raise AssertionError(label)
        counts[label] = counts.get(label, 0) + 1
    zero, one = q(), q(1)
    identity = ((one, zero), (zero, one))
    lambdas = [q(1), q(-1), q(0, 1), q(0, -1), q(F(3, 5), F(4, 5)),
               q(F(5, 13), F(12, 13)), q(2), q(F(1, 2)), q(-2)]
    mus = [q(F(1, 2)), q(F(1, 8)), q(F(1, 32)), q(F(-1, 3)), q(0, F(1, 4))]
    points = [(q(1), q(2)), (q(F(1, 3), F(-1, 4)), q(F(2, 3), F(1, 5))),
              (q(-1, 1), q(F(1, 2), F(-1, 2)))]
    for lam in lambdas:
        for mu in mus:
            tau, delta = add(lam, mu), mul(lam, mu)
            def f(z, w):
                return (sub(add(mul(tau, z), mul(z, z)), mul(delta, w)), z)
            def finv(z, w):
                return (w, div(sub(add(mul(w, w), mul(tau, w)), z), delta))
            def jac(z):
                return ((add(tau, mul(q(2), z)), neg(delta)), (one, zero))
            check('fixed_origin', f(zero, zero) == (zero, zero))
            check('determinant_at_origin', det(jac(zero)) == delta)
            for e in (lam, mu):
                value = add(sub(mul(e, e), mul(tau, e)), delta)
                check('characteristic_root', value == zero)
            for start in points:
                check('inverse_identity', finv(*f(*start)) == start)
                z, w = start
                J, dn = identity, one
                for n in range(1, 6):
                    J = mm(jac(z), J)
                    dn = mul(dn, delta)
                    check('iterate_jacobian_determinant', det(J) == dn)
                    z, w = f(z, w)
    lam = q(F(3, 5), F(4, 5))
    check('irrational_neutral_algebra', mul(lam, q(lam[0], -lam[1])) == one)
    check('irrational_neutral_algebra', add(lam, inv(lam)) == q(F(6, 5)))
    check('irrational_neutral_algebra', F(6, 5).denominator != 1)
    # Scope guards: contracting determinant does not force eigenvalue 1.
    check('spectral_nonimplication', F(2) * F(1, 8) < 1 and F(2) > 1)
    check('spectral_nonimplication', lam != one and F(1, 2) < 1)
    for M in range(1, 21):
        seq = [0]
        while seq[-1] <= 500:
            seq.append(seq[-1] + 1 + (len(seq) - 1) % M)
        j = 0
        for n in range(501):
            while seq[j + 1] <= n:
                j += 1
            check('bounded_gap_decomposition', 0 <= n - seq[j] < M)
    # u(z)^2=(|z|+Re(z))/2; use integer coordinates with rational |z|.
    pythagorean = [(x, y) for x in range(-30, 31) for y in range(-30, 31)
                   if isqrt(x*x+y*y)**2 == x*x+y*y]
    for x, y in pythagorean:
        norm = isqrt(x*x+y*y)
        v2 = F(norm+x, 2)
        check('subharmonic_value_nonnegative', v2 >= 0)
        check('subharmonic_zero_ray', (v2 == 0) == (y == 0 and x <= 0))
        for d in range(2, 13):
            scaled = F(d*d*norm+d*d*x, 2)
            check('threshold_scaling_squared', scaled == d*d*v2)
    for d in range(2, 13):
        for k in range(1, 7):
            stable = F(1, d**k)
            rho = F(1, k)
            check('strict_wiman_threshold', (stable < F(1, d*d)) == (rho < F(1, 2)))
    return {'status': 'PASS', 'arithmetic': 'exact Gaussian rational and rational arithmetic',
            'counts': dict(sorted(counts.items())), 'assertions': sum(counts.values()),
            'family_parameter_pairs': len(lambdas)*len(mus),
            'pythagorean_inputs': len(pythagorean),
            'analytic_theorems_certified': False,
            'henon_counterexample_constructed': False}


if __name__ == '__main__':
    print(json.dumps(compute(), indent=2, sort_keys=True))
