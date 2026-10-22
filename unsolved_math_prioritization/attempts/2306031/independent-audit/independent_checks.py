#!/usr/bin/env python3
"""Independent finite controls of frozen Function Theory 6.31 partial results.
Requires Python 3.10+ and mpmath. Reads no author code. Emits JSON to stdout.
These checks are supplementary; they are not proofs of limiting statements.
"""
import json
from fractions import Fraction as Q
import mpmath as mp


def convolution(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for j, x in enumerate(a):
        for k, y in enumerate(b):
            c[j+k] += x*y
    return c


def run():
    polynomial_count = 0
    # Clear denominators in equation (18), so all angles including the
    # removable q=1 point are covered by an exact polynomial identity.
    for n in range(1, 513):
        numerator = [n] + [2*(n-j) for j in range(1, n)]
        left = convolution(numerator, [1, -2, 1])
        right = [0] * (n+2)
        right[0] += n
        right[2] -= n
        right[1] -= 2
        right[n+1] += 2
        assert left == right
        assert sum(numerator) == n*n
        polynomial_count += 1

    fejer_coefficient_count = 0
    # Independent Laurent multiplication of |1+q+...+q^(n-1)|^2.
    for n in range(1, 129):
        product = {}
        for j in range(n):
            for k in range(n):
                product[j-k] = product.get(j-k, 0) + 1
        for ell in range(1-n, n):
            assert product[ell] == n-abs(ell)
            fejer_coefficient_count += 1

    rational_family_count = 0
    # Rational-radius substitution and exact endpoint cancellation.
    for c in (Q(1, 7), Q(1, 2), Q(6, 7), Q(1)):
        for s in (Q(1,2), Q(1,3), Q(1,10), Q(1,100), Q(1,10000)):
            r = 1-s
            f = c*r/s**2 + (1-c)*r/s
            assert s*s*f == c+(1-2*c)*s-(1-c)*s*s
            p = c*(1+r)/s+(1-c)
            assert p > 0
            if c == Q(1,2):
                assert f == (1/s**2-1)/2
                assert s*s*f-c == -s*s/2
            rational_family_count += 1
        for n in range(1, 257):
            a_n = c*n+(1-c)
            assert a_n/n-c == (1-c)/n
            rational_family_count += 1

    mp.mp.dps = 120
    tol = mp.mpf('1e-60')
    kernel_points = 0
    max_closed_error = mp.mpf(0)
    max_fejer_error = mp.mpf(0)
    ns = (1, 2, 7, 31, 128, 1024)
    for n in ns:
        positive = [mp.pi, mp.pi-mp.mpf('1e-24'),
                    mp.mpf('0.7'), mp.mpf('0.01'),
                    mp.mpf('1e-6'), mp.mpf('1e-12'), mp.mpf('1e-24'),
                    mp.mpf(1)/(10*n), mp.mpf(1)/n]
        if mp.mpf(10)/n <= mp.pi:
            positive.append(mp.mpf(10)/n)
        for theta in positive + [-x for x in positive]:
            q = mp.exp(-1j*theta)
            power = mp.mpc(1)
            triangular = mp.mpc(0)
            geometric = mp.mpc(1)
            for j in range(1, n):
                power *= q
                triangular += (n-j)*power
                geometric += power
            K = mp.mpf(1)/n + 2*triangular/n**2
            closed = (1+q)/(n*(1-q))-2*q*(1-q**n)/(n**2*(1-q)**2)
            fejer = abs(geometric)**2/n**2
            e1 = abs(K-closed)
            e2 = abs(mp.re(K)-fejer)
            max_closed_error = max(max_closed_error, e1)
            max_fejer_error = max(max_fejer_error, e2)
            assert e1 < tol
            assert e2 < tol
            assert abs(K) <= min(1, 3*mp.pi/(n*abs(theta)))+tol
            assert -tol <= mp.re(K) <= min(1, mp.pi**2/(n*n*theta*theta))+tol
            kernel_points += 1

    lower_bound_points = 0
    minimum_ratio = mp.inf
    for s in [mp.mpf('0.249'), mp.mpf('0.1'), mp.mpf('0.01'),
              mp.mpf('1e-6'), mp.mpf('1e-12'), mp.mpf('1e-24')]:
        for theta_fraction in (mp.mpf(-1), mp.mpf('-0.5'), mp.mpf(0), mp.mpf('0.5'), mp.mpf(1)):
            theta = s*theta_fraction
            q = mp.exp(-1j*theta)
            for v in (mp.mpf(1), mp.mpf('1.25'), mp.mpf('1.5'), mp.mpf('1.75'), mp.mpf(2)):
                t = 1-v*s
                real_kernel = (1-t*t)/abs(1-q*t)**2
                assert real_kernel >= 1/(5*s)-tol
                integrand = real_kernel/(1-t)**2
                ratio = integrand * 20*s**3
                assert ratio >= 1-tol
                minimum_ratio = min(minimum_ratio, ratio)
                lower_bound_points += 1

    return {
        'status': 'passed',
        'exact_polynomial_kernel_identities': polynomial_count,
        'exact_fejer_laurent_coefficients': fejer_coefficient_count,
        'exact_rational_family_checks': rational_family_count,
        'high_precision_kernel_points': kernel_points,
        'high_precision_local_lower_bound_points': lower_bound_points,
        'high_precision_digits': mp.mp.dps,
        'minimum_nonzero_theta': '1e-24',
        'maximum_kernel_n': max(ns),
        'maximum_closed_form_error': mp.nstr(max_closed_error, 12),
        'maximum_fejer_error': mp.nstr(max_fejer_error, 12),
        'minimum_lower_bound_ratio': mp.nstr(minimum_ratio, 12),
        'mpmath_version': mp.__version__,
        'scope': 'Finite deterministic exact and high-precision controls; no asymptotic, formal-proof, novelty, or literature-completeness certification.'
    }


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
