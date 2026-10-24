#!/usr/bin/env python3
"""Exact finite controls for Hydra cyclic covers; not virtual-specialness tests."""
from itertools import combinations
from math import comb, gcd, prod
from pathlib import Path
import json


def matrix(m, d):
    return [[comb(d, j-i) if 0 < j-i <= d else 0
             for j in range(m)] for i in range(m)]


def determinant(a):
    a = [list(row) for row in a]
    n = len(a)
    if not n:
        return 1
    sign, divisor = 1, 1
    for k in range(n-1):
        pivot = next((i for i in range(k, n) if a[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        pivot_value = a[k][k]
        for i in range(k+1, n):
            for j in range(k+1, n):
                value = a[i][j]*pivot_value-a[i][k]*a[k][j]
                assert value % divisor == 0
                a[i][j] = value // divisor
            a[i][k] = 0
        divisor = pivot_value
    return sign*a[-1][-1]


def smith_by_minors(a):
    m = len(a)
    divisors = [1]
    for size in range(1, m):
        common = 0
        for rows in combinations(range(m), size):
            for cols in combinations(range(m), size):
                common = gcd(common, abs(determinant(
                    [[a[i][j] for j in cols] for i in rows])))
        assert common and common % divisors[-1] == 0
        divisors.append(common)
    invariants = [divisors[i]//divisors[i-1]
                  for i in range(1, len(divisors))]
    assert all(b % a == 0 for a, b in zip(invariants, invariants[1:]))
    return invariants


def rank_mod(a, p):
    a = [[x % p for x in row] for row in a]
    rank = 0
    for col in range(len(a)):
        pivot = next((i for i in range(rank, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = pow(a[rank][col], -1, p)
        a[rank] = [(x*inv) % p for x in a[rank]]
        for i in range(len(a)):
            if i != rank:
                multiplier = a[i][col]
                a[i] = [(x-multiplier*y) % p
                        for x, y in zip(a[i], a[rank])]
        rank += 1
    return rank


def main():
    cases = []
    for m in range(1, 8):
        for d in range(1, 13):
            a = matrix(m, d)
            smith = smith_by_minors(a)
            assert prod(smith) == d**(m-1)
            maximal_nonzero = 0
            for rows in combinations(range(m), m-1):
                for cols in combinations(range(m), m-1):
                    value = determinant([[a[i][j] for j in cols] for i in rows])
                    maximal_nonzero += bool(value)
                    assert not value or abs(value) == d**(m-1)
            assert maximal_nonzero == 1
            cases.append(dict(rank=m, height_index=d, nonzero_smith=smith,
                              rational_betti=2, torsion_order=prod(smith)))
    prime_cases = []
    for m in range(1, 21):
        for p in (2, 3, 5, 7, 11):
            q = p
            while q < m:
                q *= p
            a = matrix(m, q)
            assert rank_mod(a, p) == 0
            prime_cases.append(dict(rank=m, prime=p, height_index=q,
                                    mod_p_betti=m+1,
                                    minimum_generator_number=m+1))
    assert smith_by_minors(matrix(3, 2)) == [1, 4]
    assert rank_mod(matrix(3, 2), 2) == 1
    for p in (2, 3, 5, 7):
        for m in range(1, min(p, 7)+1):
            assert smith_by_minors(matrix(m, p)) == [p]*(m-1)
    result = dict(scope="Finite exact matrix and Smith sanity checks only; general proofs in note",
                  integral_cases=cases, prime_power_cases=prime_cases,
                  boundary_m3_d2=dict(nonzero_smith=[1, 4], mod2_betti=3),
                  all_checks_passed=True)
    Path(__file__).with_name('height_cover_certificate.json').write_text(
        json.dumps(result, indent=2)+'\n')
    print(f"PASS: {len(cases)} exact Smith cases; {len(prime_cases)} prime-power covers.")


if __name__ == '__main__':
    main()
