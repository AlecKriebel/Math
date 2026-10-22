#!/usr/bin/env python3
"""Exact checks for the explicitly partial bounds in proof.md; Python stdlib only."""
from fractions import Fraction as Q
from math import comb, factorial
import json

DEGREE = 200
BAND = 100


def integer_rows(degree):
    """Return A[n][k] = k! [t^k] F_n, for 0 <= n,k <= degree."""
    rows = [[-1] + [0] * degree]
    for n in range(1, degree + 1):
        previous = rows[-1]
        exponential = [1] + [0] * degree
        for k in range(n, degree + 1):
            exponential[k] = sum(
                comb(k - 1, j - 1) * j * previous[j - 1]
                * exponential[k - j]
                for j in range(n, k + 1)
            )
        exponential[0] = 0
        rows.append(exponential)
    return rows


def multiply(a, b, degree):
    c = [Q(0)] * (degree + 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b[:degree + 1 - i]):
                if y:
                    c[i + j] += x * y
    return c


def direct_rows(degree):
    """Independent ordinary-series expansion by powers and rational arithmetic."""
    rows = [[Q(-1)] + [Q(0)] * degree]
    for _ in range(degree):
        g = [Q(0)] + rows[-1][:-1]
        power = [Q(1)] + [Q(0)] * degree
        result = [Q(0)] * (degree + 1)
        for m in range(1, degree + 1):
            power = multiply(power, g, degree)
            for k in range(degree + 1):
                result[k] += power[k] / factorial(m)
        rows.append(result)
    return rows


def stirling_second(n, k):
    s = [[0] * (n + 1) for _ in range(n + 1)]
    s[0][0] = 1
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            s[i][j] = j * s[i - 1][j] + s[i - 1][j - 1]
    return s[n][k]


def main():
    facts = [factorial(k) for k in range(DEGREE + 1)]
    rows = integer_rows(DEGREE)
    maximum_nonleading = (Q(0), 0, 0)
    for n in range(1, DEGREE + 1):
        assert all(x == 0 for x in rows[n][:n])
        assert rows[n][n] == -facts[n]
        for k, a in enumerate(rows[n]):
            assert abs(a) <= facts[k], (n, k)
            if k > n and Q(abs(a), facts[k]) > maximum_nonleading[0]:
                maximum_nonleading = (Q(abs(a), facts[k]), n, k)
    assert maximum_nonleading == (Q(2663, 4480), 6, 13)
    assert rows[6][13] == -Q(2663, 4480) * facts[13]

    independent_degree = 24
    independent = direct_rows(independent_degree)
    for n in range(independent_degree + 1):
        for k in range(independent_degree + 1):
            assert independent[n][k] == Q(rows[n][k], facts[k])

    # Finite part of the diagonal-band proof. Stabilization extends n > 100.
    for n in range(1, BAND + 1):
        for j in range(BAND + 1):
            assert abs(rows[n][n + j]) <= facts[n + j]
    for j in range(BAND + 1):
        for n in range(max(1, j), DEGREE - j):
            assert Q(rows[n][n + j], facts[n + j]) == Q(
                rows[n + 1][n + 1 + j], facts[n + 1 + j])

    # Rational inequalities used to dominate exponentials, all explained in proof.md.
    assert Q(8, 3) + Q(5, 96) == Q(87, 32) < Q(11, 4)
    assert Q(11, 4) * Q(10, 9) < Q(31, 10)
    assert Q(11, 4)**2 * Q(100, 69) < 11
    assert Q(11, 10)**128 > 3**11
    assert Q(87, 32) * Q(20, 17) < Q(16, 5)
    assert Q(11, 4) < Q(5, 3)**2
    assert Q(11, 4)**2 * Q(5, 3) * Q(100, 97) < 13
    assert Q(21, 20)**136 > 3**6

    r = Q(21, 20)
    q = Q(21, 23)
    polynomial = sum(Q(abs(rows[3][k]), facts[k]) * r**k
                     for k in range(DEGREE + 1))
    tail = Q(11, 4)**14 * q**(DEGREE + 1) / (1 - q)
    assert polynomial + tail < Q(4621, 1000) < 5
    assert Q(4620, 1000) < polynomial + tail

    # Failed majorants are checked so they cannot be mistaken for proofs.
    # Positive-start recurrence at (n,k)=(3,6), computed directly.
    positive = [Q(1)] + [Q(0)] * 6
    for _ in range(3):
        g = [Q(0)] + positive[:-1]
        p = [Q(1)] + [Q(0)] * 6
        positive = [Q(0)] * 7
        for m in range(1, 7):
            p = multiply(p, g, 6)
            for k in range(7):
                positive[k] += p[k] / factorial(m)
    assert positive[6] == Q(25, 24) > 1
    tree_summand = Q(stirling_second(6, 3) * stirling_second(9, 6)
                     * stirling_second(12, 9), factorial(12))
    assert tree_summand == Q(2835, 256) > 1

    result = {
        "status": "partial; universal problem unresolved",
        "integer_arithmetic": "exact",
        "finite_rectangle": {"n": [1, DEGREE], "k": [0, DEGREE],
                             "pairs_checked": DEGREE * (DEGREE + 1),
                             "all_moduli_at_most_one": True},
        "independent_crosscheck": {"method": "rational exponential powers",
                                    "n": [0, independent_degree],
                                    "k": [0, independent_degree]},
        "proved_extension": {
            "all_iterates_degrees": [0, DEGREE],
            "all_iterates_diagonal_offsets": [0, BAND],
            "all_degrees_iterates": [1, 4]},
        "largest_nonleading_modulus_in_rectangle": {
            "value": str(maximum_nonleading[0]), "n": 6, "k": 13,
            "coefficient": "-2663/4480"},
        "third_iterate_weighted_norm_upper_bound_interval": ["4620/1000", "4621/1000"],
        "cauchy_tail_cutoffs": {"n_le_3": 128, "n_eq_4": 136},
        "positive_majorant_failure": {"n": 3, "k": 6, "value": "25/24"},
        "tree_termwise_bound_failure": {"layers": [3, 6, 9, 12],
                                         "value": str(tree_summand)},
        "unresolved_region": "n >= 5, k >= 201, k - n >= 101"
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
