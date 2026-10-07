#!/usr/bin/env python3
"""Separately implemented finite arithmetic controls; no limiting claims."""
from fractions import Fraction as F
import json


def check(condition, label):
    if not condition:
        raise RuntimeError(label)


def main():
    limit = 500
    prime = [True]*(limit+1)
    prime[:2] = [False, False]
    primes = []
    for p in range(2, limit+1):
        if prime[p]:
            primes.append(p)
            for multiple in range(p*p, limit+1, p):
                prime[multiple] = False
    mobius = [1]*(limit+1)
    mobius[0] = 0
    for p in primes:
        for multiple in range(p, limit+1, p):
            mobius[multiple] *= -1
        for multiple in range(p*p, limit+1, p*p):
            mobius[multiple] = 0
    mertens = [0]*(limit+1)
    for n in range(1, limit+1):
        mertens[n] = mertens[n-1]+mobius[n]
    counts = {}
    counts['independent_sieve_divisor_and_summatory_identities'] = 0
    for n in range(1, limit+1):
        check(sum(mobius[d] for d in range(1, n+1) if n % d == 0) == int(n == 1), 'divisor inversion')
        check(sum(mertens[n//d] for d in range(1, n+1)) == 1, 'summatory inversion')
        counts['independent_sieve_divisor_and_summatory_identities'] += 1
    counts['floor_endpoint_and_damped_identities'] = 0
    for denominator in range(1, 12):
        for numerator in range(1, 81):
            t = F(numerator, denominator)
            cutoff = int(t)
            check(sum(mobius[n]*(t//n) for n in range(1, cutoff+1)) == int(t >= 1), 'rational floor inversion')
            for N in (1, 2, 3, 5, 13):
                for exponent in (1, 2):
                    coefficient = [F(0)]+[F(mobius[n], n**exponent) for n in range(1, N+1)]
                    value = -sum(coefficient[n]*(t/n-t//n) for n in range(1, N+1))
                    A = sum(coefficient[n]/n for n in range(1, N+1))
                    check(value == sum(coefficient[n]*(t//n) for n in range(1, N+1))-t*A, 'damping sign')
                    if t < 1:
                        check(value == -t*A, 'below-one coefficient')
            counts['floor_endpoint_and_damped_identities'] += 1
    counts['escaping_mass_three_exact_moments'] = 0
    for k in range(1, 51):
        N = k**4
        measure = F(1, 2*N)
        for amplitude_power, expected in ((k**2, F(1, 2*k**2)),
                                           (k**3, F(1, 2*k)),
                                           (k**4, F(1, 2))):
            check(amplitude_power*measure == expected, 'escaping mass')
            counts['escaping_mass_three_exact_moments'] += 1
    # Integrals of exp(-a*u), u >= 0, are 1/a. For negative shifts
    # z=exp(s) in (0,1); for positive shifts z=exp(-s).
    counts['two_exponential_pairings'] = 0
    for den in range(2, 31):
        for num in range(1, den):
            z = F(num, den)
            positive_shift = z*(F(1, 2)-F(3, 2)*F(1, 3))
            negative_shift = z*F(1, 2)-F(3, 2)*z*z*F(1, 3)
            check(positive_shift == 0, 'unilateral pairing')
            check(negative_shift == (z-z*z)/2 > 0, 'bilateral pairing')
            counts['two_exponential_pairings'] += 1
    check(F(1)/(1+F(1, 2)) == F(2, 3), 'target pairing')
    check(F(1, 2)*F(1, 2)-F(3, 2)*F(1, 4)*F(1, 3) == F(1, 8), 'negative log-two shift')
    check(F(1, 2)-3*F(1, 3)+F(9, 4)*F(1, 4) == F(1, 16), 'kernel square norm')
    # A genuine below-one nonzero annihilator: t^2 on (0,1/2),
    # -t^2/3 on (1/2,1). All a>=1 give pairing C/a=0.
    C = F(1, 8)-F(1, 3)*F(3, 8)
    for numerator in range(1, 101):
        a = F(1)+F(numerator, 17)
        check(C/a == 0, 'legitimate nonseparating annihilator')
    counts['nonseparating_below_one_annihilator'] = 100
    counts['kernel_constants'] = 3
    return {'schema': 'nyman-independent-finite-math-v1', 'status': 'PASS',
            'counts': counts, 'total_groups': sum(counts.values()),
            'limits': 'Independent exact finite checks only. Analytic propositions require the audit reasoning; infinite bounds, closure and RH are not computationally certified.'}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
