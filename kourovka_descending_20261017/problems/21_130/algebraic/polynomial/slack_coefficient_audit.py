#!/usr/bin/env python3
"""Independent finite-difference certificates for the reduced cycle polynomial.

This does not expand any polynomial or import slack_probe.  For x^t of
total degree deg Q, the coefficient is a weighted grid evaluation divided
by product(t_i!).  Nonzero Vandermonde evaluations reduce that grid to
permutations of 0,...,n-1.
"""
from itertools import permutations
from math import comb, factorial, gcd, prod
from functools import reduce


def q_value(p):
    n = len(p)
    sums = [p[i] + p[(i + 1) % n] for i in range(n)]
    vertices = prod(p[j] - p[i] for i in range(n) for j in range(i + 1, n))
    colors = prod(sums[j] - sums[i]
                  for i in range(n) for j in range(i + 1, n)
                  if j - i not in (1, n - 1))
    return vertices * colors


def coefficient_by_finite_differences(t):
    n = len(t)
    assert n > 2 and all(0 <= k < n for k in t)
    assert sum(t) == n * (n - 2)
    numerator = 0
    for p in permutations(range(n)):
        if any(a > k for a, k in zip(p, t)):
            continue
        weight = prod((-1) ** (k - a) * comb(k, a) for a, k in zip(p, t))
        numerator += weight * q_value(p)
    denominator = prod(factorial(k) for k in t)
    quotient, remainder = divmod(numerator, denominator)
    assert remainder == 0
    return quotient


WITNESSES = {
    3: [((0, 1, 2), 1)],
    4: [((0, 2, 3, 3), 4)],
    5: [((1, 3, 3, 4, 4), 14), ((0, 4, 3, 4, 4), -24)],
    6: [((2, 3, 5, 5, 4, 5), 182),
        ((2, 4, 5, 5, 3, 5), -476),
        ((0, 4, 5, 5, 5, 5), -520)],
    7: [((1, 5, 6, 5, 6, 6, 6), -1454),
        ((4, 4, 5, 5, 5, 6, 6), 1570)],
    8: [((4, 6, 5, 7, 7, 6, 6, 7), -108696),
        ((3, 4, 6, 7, 7, 7, 7, 7), -2270792)],
    9: [((0, 7, 8, 8, 8, 8, 8, 8, 8), -137176976),
        ((1, 7, 8, 7, 8, 8, 8, 8, 8), -1261141910)],
}


if __name__ == '__main__':
    for n, witnesses in WITNESSES.items():
        computed = [coefficient_by_finite_differences(t) for t, _ in witnesses]
        assert computed == [value for _, value in witnesses], (n, computed)
        witness_gcd = reduce(gcd, map(abs, computed), 0)
        print(f'n={n}: exact coefficients={computed}; witness gcd={witness_gcd}')
