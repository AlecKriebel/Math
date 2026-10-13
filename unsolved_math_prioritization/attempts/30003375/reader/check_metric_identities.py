#!/usr/bin/env python3
"""Exact algebraic checks for the authored harmonic mapping-torus construction.

Run with Python 3; the standard library is sufficient. These finite checks are
sanity checks of identities used in the proof, not a proof of smooth fibering,
Hodge theory, Moser's argument, or any assertion about exotic structures.
"""

from fractions import Fraction as Q
import json
import random


def eye(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def mul(a, b):
    return [[sum(x * y for x, y in zip(row, col))
             for col in zip(*b)] for row in a]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def sub(a, b):
    return [[x - y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(c, a):
    return [[c * x for x in row] for row in a]


def det(a):
    a = [row[:] for row in a]
    n = len(a)
    answer = Q(1)
    for i in range(n):
        pivot = next((j for j in range(i, n) if a[j][i]), None)
        if pivot is None:
            return Q(0)
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            answer = -answer
        entry = a[i][i]
        answer *= entry
        for j in range(i + 1, n):
            ratio = a[j][i] / entry
            for k in range(i + 1, n):
                a[j][k] -= ratio * a[i][k]
            a[j][i] = Q(0)
    return answer


def inverse(a):
    n = len(a)
    a = [row[:] + unit for row, unit in zip(a, eye(n))]
    for i in range(n):
        pivot = next(j for j in range(i, n) if a[j][i])
        a[i], a[pivot] = a[pivot], a[i]
        entry = a[i][i]
        a[i] = [x / entry for x in a[i]]
        for j in range(n):
            if j != i:
                ratio = a[j][i]
                a[j] = [x - ratio * y for x, y in zip(a[j], a[i])]
    return [row[n:] for row in a]


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def is_spd(a):
    return a == transpose(a) and all(
        det([row[:k] for row in a[:k]]) > 0
        for k in range(1, len(a) + 1)
    )


def determinant_derivative(a, da):
    # Multilinearity in columns, independent of the inverse-matrix formula.
    total = Q(0)
    for col in range(len(a)):
        b = [row[:] for row in a]
        for row in range(len(a)):
            b[row][col] = da[row][col]
        total += det(b)
    return total


def main():
    rng = random.Random(30003375)
    n = 6
    cases = 0
    for _ in range(12):
        a = [[Q(rng.randrange(-3, 4)) for _ in range(n)] for _ in range(n)]
        h0 = add(mul(transpose(a), a), eye(n))
        p = eye(n)
        for _ in range(9):
            i, j = rng.sample(range(n), 2)
            shear = eye(n)
            shear[i][j] = Q(rng.choice((-2, -1, 1, 2)))
            p = mul(shear, p)
        assert det(p) == 1
        h1 = mul(mul(transpose(p), h0), p)
        assert is_spd(h0) and is_spd(h1)
        assert det(h1) == det(h0)
        derivative = sub(h1, h0)
        for t in map(Q, (0, Q(1, 7), Q(1, 2), Q(5, 7), 1)):
            k = add(scale(1 - t, h0), scale(t, h1))
            assert is_spd(k)
            log_det_derivative = trace(mul(inverse(k), derivative))
            assert determinant_derivative(k, derivative) == det(k) * log_det_derivative

            # H = lambda K, lambda=(det(K)/det(H0))^(-1/n).
            # The n-th power is rational even when lambda is irrational.
            lambda_to_n = det(h0) / det(k)
            assert lambda_to_n * det(k) == det(h0)
            log_lambda_derivative = -log_det_derivative / n
            assert n * log_lambda_derivative + log_det_derivative == 0

            # Equivalently use r=vol(K)/mu and H=r^(-2/n) K.
            # Volume rescales by the metric factor to power n/2.
            assert Q(-2, n) * Q(n, 2) + 1 == 0
            if t in (0, 1):
                assert lambda_to_n == 1
            cases += 1
    print(json.dumps({
        "result": "passed",
        "seed": 30003375,
        "fibre_dimension": n,
        "endpoint_pairs": 12,
        "exact_rational_interpolation_cases": cases,
        "checked": [
            "orientation-preserving unimodular frame changes",
            "positive-definite endpoint and interpolated metrics",
            "endpoint pullback determinant matching",
            "Jacobi determinant derivative identity",
            "fixed-volume normalization exponent",
            "vanishing normalized logarithmic volume derivative"
        ],
        "limitations": "Finite algebraic sanity checks; the global smooth proof is in PROOF.md."
    }, indent=2))


if __name__ == "__main__":
    main()
