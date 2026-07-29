#!/usr/bin/env python3
"""Exact checks for the high-principal-overlap scalar reduction.

The mathematical proof is in
notes/agent_n3_high_principal_overlap_scalar.md.  This checker audits
the normalizations and the sharp biseparable point using rational
arithmetic only.
"""

from fractions import Fraction


def epsilon(i: int, j: int, k: int) -> int:
    if len({i, j, k}) < 3:
        return 0
    word = (i, j, k)
    inversions = sum(
        word[a] > word[b] for a in range(3) for b in range(a + 1, 3)
    )
    return -1 if inversions % 2 else 1


def hodge_matrix(label: int) -> list[list[Fraction]]:
    # Store sqrt(2) A_label, whose entries are integral.  Products of
    # three matrices therefore acquire the common squared factor 1/8.
    return [
        [Fraction(epsilon(label, row, column)) for column in range(3)]
        for row in range(3)
    ]


def kron(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    return [
        [
            left[i // len(right)][j // len(right[0])]
            * right[i % len(right)][j % len(right[0])]
            for j in range(len(left[0]) * len(right[0]))
        ]
        for i in range(len(left) * len(right))
    ]


def transpose(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(row) for row in zip(*matrix)]


def multiply(
    left: list[list[Fraction]], right: list[list[Fraction]]
) -> list[list[Fraction]]:
    return [
        [
            sum(
                (left[i][k] * right[k][j] for k in range(len(right))),
                Fraction(0),
            )
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def add(
    left: list[list[Fraction]], right: list[list[Fraction]]
) -> list[list[Fraction]]:
    return [
        [left[i][j] + right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def scale(
    value: Fraction, matrix: list[list[Fraction]]
) -> list[list[Fraction]]:
    return [[value * entry for entry in row] for row in matrix]


def main() -> None:
    hodge = [hodge_matrix(label) for label in range(3)]

    # t = Phi_AB tensor |0>_C.  Its three nonzero coefficients are
    # 1/sqrt(3).  Work with sqrt(3)*2^(3/2) D_t, which is the integral
    # matrix sum below.  Therefore D_t^*D_t is the displayed Gram
    # divided by 24.
    integer_d = [[Fraction(0) for _ in range(27)] for _ in range(27)]
    for label in range(3):
        term = kron(kron(hodge[label], hodge[label]), hodge[0])
        integer_d = add(integer_d, term)
    gram = multiply(transpose(integer_d), integer_d)

    # The exact top eigenvalue is 4/24=1/6.  Check directly on
    # x=Phi_AB tensor |2> and check D_t t=0 after clearing square roots.
    t = [Fraction(0) for _ in range(27)]
    x = [Fraction(0) for _ in range(27)]
    for label in range(3):
        t[9 * label + 3 * label] = Fraction(1)
        x[9 * label + 3 * label + 2] = Fraction(1)

    def quadratic(vector: list[Fraction]) -> Fraction:
        return sum(
            (
                vector[i] * gram[i][j] * vector[j]
                for i in range(27)
                for j in range(27)
            ),
            Fraction(0),
        )

    assert quadratic(t) == 0
    # Both t and x have squared norm 3.  The actual normalized energy is
    # quadratic(x)/(24*3).
    assert quadratic(x) == 12
    assert quadratic(x) / Fraction(72) == Fraction(1, 6)

    # Audit the scalar margin algebra:
    # 4/9 - (8/9)(4-gamma)/6 = 4(gamma-1)/27.
    for gamma in (Fraction(0), Fraction(1), Fraction(3, 2), Fraction(2)):
        left = Fraction(4, 9) - Fraction(8, 9) * (4 - gamma) / 6
        right = Fraction(4, 27) * (gamma - 1)
        assert left == right

    print(
        "verified exact Hodge normalization, D_t t=0, sharp 1/6 "
        "biseparable energy, and the principal-overlap margin"
    )


if __name__ == "__main__":
    main()

