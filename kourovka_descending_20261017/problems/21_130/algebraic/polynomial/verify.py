#!/usr/bin/env python3
"""Exact integer checks for the cyclic adjacent-sum CN coefficient.

Uses only Python's standard library. No randomized choices or external data.
"""
from collections import defaultdict
from itertools import permutations
from math import factorial, prod
from time import perf_counter


def vandermonde(xs):
    return prod(xs[j] - xs[i] for i in range(len(xs)) for j in range(i + 1, len(xs)))


def coefficient_by_antisymmetrization(n):
    """C_n = (-1)^(n choose 2) Alt(V(Bx))/V(x), evaluated x=(0,...,n-1)."""
    total = 0
    nonzero = 0
    for p in permutations(range(n)):
        sums = [p[i] + p[(i + 1) % n] for i in range(n)]
        if len(set(sums)) < n:
            continue
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        total += (-1) ** inversions * vandermonde(sums)
        nonzero += 1
    numerator = (-1) ** (n * (n - 1) // 2) * total
    denominator = prod(factorial(i) for i in range(n))
    quotient, remainder = divmod(numerator, denominator)
    assert remainder == 0
    return quotient, nonzero


def coefficient_by_direct_expansion(n):
    """Independent multiplication of the 2*(n choose 2) linear factors.

    Truncate any exponent above n-1: later multiplication cannot reduce it.
    """
    zero = (0,) * n
    poly = {zero: 1}
    factors = []
    for i in range(n):
        for j in range(i + 1, n):
            factors.append({j: 1, i: -1})
    for i in range(n):
        for j in range(i + 1, n):
            factor = defaultdict(int)
            for k, coefficient in [(j, 1), ((j + 1) % n, 1), (i, -1), ((i + 1) % n, -1)]:
                factor[k] += coefficient
            factors.append({k: c for k, c in factor.items() if c})
    for factor in factors:
        updated = defaultdict(int)
        for exponent, coefficient in poly.items():
            for k, c in factor.items():
                if exponent[k] >= n - 1:
                    continue
                next_exponent = list(exponent)
                next_exponent[k] += 1
                updated[tuple(next_exponent)] += c * coefficient
        poly = {e: c for e, c in updated.items() if c}
    return poly.get((n - 1,) * n, 0)


def factor_integer(value):
    factors = {}
    p = 2
    while p * p <= value:
        while value % p == 0:
            factors[p] = factors.get(p, 0) + 1
            value //= p
        p += 1
    if value > 1:
        factors[value] = factors.get(value, 0) + 1
    return factors


def main():
    expected = {3: 6, 4: 0, 5: 980, 6: 0, 7: 2292864, 8: 0, 9: 87215071680}
    for n, expected_value in expected.items():
        start = perf_counter()
        value, nonzero = coefficient_by_antisymmetrization(n)
        assert value == expected_value, (n, value, expected_value)
        if n <= 7:
            direct = coefficient_by_direct_expansion(n)
            assert direct == value, (n, direct, value)
        print(f'n={n}: C_n={value}; factorization={factor_integer(value) if value else "zero"}; nonzero alternating terms={nonzero}; seconds={perf_counter()-start:.4f}')
    # Method obstruction only: the five-element example still has a rainbow cycle.
    order = (0, 1, 2, 3, 4)
    sums_mod_7 = tuple((order[i] + order[(i + 1) % 5]) % 7 for i in range(5))
    assert len(set(sums_mod_7)) == 5
    assert expected[5] % 7 == 0
    print('Characteristic-7 witness:', order, 'has distinct sums', sums_mod_7)


if __name__ == '__main__':
    main()
