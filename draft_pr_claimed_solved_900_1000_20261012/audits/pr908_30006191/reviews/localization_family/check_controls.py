#!/usr/bin/env python3
"""Exact finite-dimensional controls for a fully analytic continuum audit.

These controls do not approximate the PDE and do not prove a continuum limit.
They independently exercise the Slater moment identity, sector factorization,
particle-number phase, and integer packing bounds using exact arithmetic.
"""
from fractions import Fraction as F
from itertools import combinations
from math import prod
from pathlib import Path
import json


def determinant(a):
    a = [list(row) for row in a]
    det = F(1)
    for i in range(len(a)):
        pivot = next((j for j in range(i, len(a)) if a[j][i]), None)
        if pivot is None:
            return F(0)
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            det *= -1
        p = a[i][i]
        det *= p
        a[i] = [x / p for x in a[i]]
        for j in range(i + 1, len(a)):
            c = a[j][i]
            a[j] = [x - c * y for x, y in zip(a[j], a[i])]
    return det


def fraction_string(x):
    return str(x.numerator) + "/" + str(x.denominator)


def run():
    dim = 7
    u = [[F(i == j) for j in range(dim)] for i in range(dim)]
    # Rational orthogonal row rotations, including inside/outside mixing.
    rotations = [
        (0, 3, F(3, 5), F(4, 5)),
        (1, 4, F(5, 13), F(12, 13)),
        (0, 1, F(8, 17), F(15, 17)),
        (2, 5, F(7, 25), F(24, 25)),
        (1, 2, F(20, 29), F(21, 29)),
        (3, 6, F(9, 41), F(40, 41)),
    ]
    for i, j, c, s in rotations:
        x, y = u[i][:], u[j][:]
        u[i] = [c * a - s * b for a, b in zip(x, y)]
        u[j] = [s * a + c * b for a, b in zip(x, y)]
    assert all(sum(u[k][i] * u[k][j] for k in range(dim)) == F(i == j)
               for i in range(dim) for j in range(dim))
    outside = {1, 3, 5}
    slater_cases = []
    for n in range(0, dim + 1):
        normalization = F(0)
        mean = F(0)
        second = F(0)
        for indices in combinations(range(dim), n):
            amplitude = determinant([[u[k][j] for j in range(n)] for k in indices])
            weight = amplitude * amplitude
            leaked = len(outside.intersection(indices))
            normalization += weight
            mean += leaked * weight
            second += leaked * leaked * weight
        cmat = [[sum(u[k][i] * u[k][j] for k in outside)
                 for j in range(n)] for i in range(n)]
        lam = sum(cmat[i][i] for i in range(n))
        trace_square = sum(cmat[i][j] * cmat[j][i]
                           for i in range(n) for j in range(n))
        asserted_second = lam * lam + lam - trace_square
        assert normalization == 1
        assert mean == lam
        assert second == asserted_second
        assert 0 <= second - mean * mean <= mean
        slater_cases.append({"n": n, "mean": fraction_string(mean),
                             "second_moment": fraction_string(second),
                             "variance": fraction_string(second - mean * mean),
                             "exact_match": True})

    sector_count = 0
    for sigma in (0, 1):
        for n in range(0, 151):
            for leaked in range(n + 1):
                localized = n - leaked
                actual = localized * (localized - sigma) - n * (n - sigma)
                factored = -leaked * (2 * n - sigma - leaked)
                assert actual == factored
                if n >= 1:
                    assert 0 <= 2 * n - sigma - leaked <= 2 * n
                    assert abs(actual) <= 2 * n * leaked
                sector_count += 1
    for sigma in (0, 1):
        for n in range(1, 10001):
            delta = (n + 1) * (n + 1 - sigma) - n * (n - sigma)
            assert delta == 2 * n + 1 - sigma
            assert delta >= 2 * n

    grid_cases = []
    for n in (1, 2, 7, 8, 9, 26, 27, 28, 63, 64, 65, 999, 1000, 1001, 1000000):
        # Exact integer cube ceiling, avoiding floating rounding at perfect cubes.
        low, high = 0, n
        while low < high:
            mid = (low + high) // 2
            if mid ** 3 < n:
                low = mid + 1
            else:
                high = mid
        m = low
        assert (m - 1) ** 3 < n <= m ** 3
        # m <= 2 n^(1/3), cubed without approximate arithmetic.
        assert m ** 3 <= 8 * n
        grid_cases.append({"N": n, "m": m, "capacity": m ** 3, "pass": True})

    exponents = {}
    for d in (1, 2, 3, 4, 5):
        first = -F(1, 2) + F(1, d)
        second = -F(1) + F(2, d)
        exponents[str(d)] = {"first": fraction_string(first),
                             "second": fraction_string(second),
                             "both_decay": first < 0 and second < 0}
    assert exponents["3"]["first"] == "-1/6"
    assert exponents["3"]["second"] == "-1/3"
    assert not exponents["1"]["both_decay"]
    assert not exponents["2"]["both_decay"]

    result = {
        "all_pass": True,
        "role": "Exact finite controls supplement but do not establish the continuum proof.",
        "slater_moment_cases": slater_cases,
        "sector_identity_cases": sector_count,
        "phase_difference_cases": 20000,
        "integer_grid_cases": grid_cases,
        "dimension_exponents": exponents,
        "continuum_claim_basis": "Universal analytic equations L1-L15 in INDEPENDENT_DERIVATION.md.",
    }
    destination = Path(__file__).resolve().parent / "CONTROL_RESULTS.json"
    destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"all_pass": True, "slater_cases": len(slater_cases),
                      "sector_cases": sector_count, "phase_cases": 20000,
                      "grid_cases": len(grid_cases)}, sort_keys=True))


if __name__ == "__main__":
    run()
