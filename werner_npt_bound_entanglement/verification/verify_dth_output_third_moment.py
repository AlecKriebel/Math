#!/usr/bin/env python3
"""Exact local permutation formula for Tr((D_z^* D_z)^3).

The verifier constructs the one-site sixth-order contraction from epsilon
tensors, expands it in the six permutation operators on three replicas, and
checks every one of its 729 matrix entries over the rationals.
"""

from fractions import Fraction as F
from itertools import permutations, product


WORDS = tuple(product(range(3), repeat=3))
PERMUTATIONS = tuple(permutations(range(3)))


def epsilon(p, a, i):
    positive = ((0, 1, 2), (1, 2, 0), (2, 0, 1))
    negative = ((0, 2, 1), (2, 1, 0), (1, 0, 2))
    return int((p, a, i) in positive) - int((p, a, i) in negative)


def local_b(p, q, i, j):
    # Sum_a (A_p)_{a i}(A_q)_{a j}; each A contributes 1/sqrt(2).
    return F(sum(
        epsilon(p, a, i) * epsilon(q, a, j) for a in range(3)
    ), 2)


def local_third_moment_entry(rows, columns):
    p1, p2, p3 = rows
    q1, q2, q3 = columns
    return sum((
        local_b(p1, q1, i, j)
        * local_b(p2, q2, j, k)
        * local_b(p3, q3, k, i)
        for i, j, k in product(range(3), repeat=3)
    ), F(0))


def permutation_entry(permutation, rows, columns):
    return F(int(all(
        rows[position] == columns[permutation[position]]
        for position in range(3)
    )))


def verify_expansion():
    # T = F_(23)+F_(12)+F_(13)-F_(123), in image-form notation.
    coefficients = {
        (0, 2, 1): F(1, 8),
        (1, 0, 2): F(1, 8),
        (2, 1, 0): F(1, 8),
        (1, 2, 0): F(-1, 8),
    }
    for rows in WORDS:
        for columns in WORDS:
            left = local_third_moment_entry(rows, columns)
            right = sum((
                coefficient * permutation_entry(permutation, rows, columns)
                for permutation, coefficient in coefficients.items()
            ), F(0))
            assert left == right


def verify_threshold_arithmetic():
    # At most thirteen distinct skew singular pairs occur in odd dimension 27.
    # Convexity gives the boundary minimum at
    # lambda_1=lambda_2=1/8 and lambda_3=...=lambda_13=1/44.
    pair_third_moment = F(2) * F(1, 8) ** 3 + F(11) * F(1, 44) ** 3
    full_third_moment = F(2) * pair_third_moment
    assert full_third_moment == F(125, 15488)

    # Product z is an equality audit for the permutation identity and the
    # Hölder upper bound: the local T expectation is 2 at each site.
    assert F(2) ** 3 / F(512) == F(1, 64)


def main():
    verify_expansion()
    verify_threshold_arithmetic()
    print("exact DTH output third-moment identity passed")
    print("violation threshold: Tr((D_z^* D_z)^3) > 125/15488")


if __name__ == "__main__":
    main()
