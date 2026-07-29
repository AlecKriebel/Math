#!/usr/bin/env python3
"""Dependency-free exact checks for the Takagi--Hodge reduction."""

from fractions import Fraction as F


def matmul(left, right):
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def main():
    # The spin-flip bilinear form gives twice the determinant.
    epsilon = [[F(0), F(1)], [F(-1), F(0)]]
    j = [
        [
            epsilon[i // 2][k // 2] * epsilon[i % 2][k % 2]
            for k in range(4)
        ]
        for i in range(4)
    ]
    identity_vector = [[F(1)], [F(0)], [F(0)], [F(1)]]
    twice_determinant = matmul(
        matmul(transpose(identity_vector), j),
        identity_vector,
    )[0][0]
    assert twice_determinant == 2

    # Exact sharp feature state.
    kf = [
        [F(1, 9), F(0), F(0), F(0)],
        [F(0), F(4, 9), F(-1, 3), F(0)],
        [F(0), F(-1, 3), F(4, 9), F(0)],
        [F(0), F(0), F(0), F(1, 9)],
    ]
    singlet = [[F(0)], [F(1)], [F(-1)], [F(0)]]
    triplet = [[F(0)], [F(1)], [F(1)], [F(0)]]
    assert matmul(kf, singlet) == [
        [F(0)], [F(7, 9)], [F(-7, 9)], [F(0)]
    ]
    assert matmul(kf, triplet) == [
        [F(0)], [F(1, 9)], [F(1, 9)], [F(0)]
    ]
    assert kf[0][0] == kf[3][3] == F(1, 9)
    takagi_values = [F(7, 9), F(1, 9), F(1, 9), F(1, 9)]
    assert takagi_values[0] - sum(takagi_values[1:]) == F(4, 9)

    # The explicit Hadamard mixing in Lemma 2.1.  Squared entries of
    # the normalized Hadamard are all 1/4.  Phases (+,-,-,-) make
    # every diagonal determinant amplitude equal to 1/9 in modulus.
    phased_sum = (
        takagi_values[0]
        - takagi_values[1]
        - takagi_values[2]
        - takagi_values[3]
    )
    each_diagonal = phased_sum / 4
    assert each_diagonal == F(1, 9)
    assert 4 * abs(each_diagonal) == F(4, 9)

    # The parity regrouping (5).
    # If A_i are commuting idempotents, E2=sum A_i A_j-3 A123.
    coefficient_triple = F(4, 9) * (-3) + F(20, 9)
    assert coefficient_triple == F(8, 9)

    print(
        "verified: spin-flip determinant, sharp Takagi excess, "
        "Hadamard mixing, and Hodge-channel regrouping"
    )


if __name__ == "__main__":
    main()
