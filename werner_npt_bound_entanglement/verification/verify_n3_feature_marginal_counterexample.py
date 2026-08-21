#!/usr/bin/env python3
"""Exact counterexample to a proposed feature-state marginal inequality.

All arithmetic is in Q(omega), omega^2+omega+1=0.  The graph-state
amplitudes are stored without their common normalization 1/sqrt(27);
two-replica matrix elements are divided by 27^2 at the end.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import product


QutritString = tuple[int, int, int]
Cyclotomic = tuple[F, F]  # a+b*omega

STRINGS = list(product(range(3), repeat=3))


def add(first: Cyclotomic, second: Cyclotomic) -> Cyclotomic:
    return first[0] + second[0], first[1] + second[1]


def scale(value: Cyclotomic, scalar: F) -> Cyclotomic:
    return scalar * value[0], scalar * value[1]


def residue_sum(counts) -> Cyclotomic:
    """n0+n1*omega+n2*omega^2 in the basis (1,omega)."""

    return F(counts[0] - counts[2]), F(counts[1] - counts[2])


def phase(label: QutritString, string: QutritString) -> int:
    """Graph phase for the sole edge (site 1,site 2) of weight 2."""

    return (
        2 * string[1] * string[2]
        + sum(label[index] * string[index] for index in range(3))
    ) % 3


def swap_matrix_element(left, right, subset) -> Cyclotomic:
    """<g_left0 g_left1|F_subset|g_right0 g_right1>."""

    counts = [0, 0, 0]
    for first in STRINGS:
        for second in STRINGS:
            swapped_first = tuple(
                second[index] if index in subset else first[index]
                for index in range(3)
            )
            swapped_second = tuple(
                first[index] if index in subset else second[index]
                for index in range(3)
            )
            exponent = (
                -phase(left[0], first)
                -phase(left[1], second)
                +phase(right[0], swapped_first)
                +phase(right[1], swapped_second)
            ) % 3
            counts[exponent] += 1
    return scale(residue_sum(counts), F(1, 729))


# S=(4/9)E_2+(20/9)E_3, expanded in the commuting local swaps.
SWAP_COEFFICIENTS = {
    (): F(4, 9),
    (0,): F(-1, 3),
    (1,): F(-1, 3),
    (2,): F(-1, 3),
    (0, 1): F(2, 9),
    (0, 2): F(2, 9),
    (1, 2): F(2, 9),
    (0, 1, 2): F(-1, 9),
}


def feature_entry(left, right) -> Cyclotomic:
    answer = (F(0), F(0))
    for subset, coefficient in SWAP_COEFFICIENTS.items():
        answer = add(
            answer,
            scale(swap_matrix_element(left, right, subset), coefficient),
        )
    return answer


def main():
    # Graph labels are ordered as in the note:
    # U=(g_220,g_011), V=(g_020,g_022).
    u = ((2, 2, 0), (0, 1, 1))
    v = ((0, 2, 0), (0, 2, 2))
    logical = [(row, column) for row in range(2) for column in range(2)]
    matrix = []
    for first_row, first_column in logical:
        row = []
        for second_row, second_column in logical:
            row.append(
                feature_entry(
                    (u[first_row], v[first_column]),
                    (u[second_row], v[second_column]),
                )
            )
        matrix.append(row)

    expected_diagonal = (F(4, 9), F(2, 9), F(1, 27), F(1, 27))
    assert matrix == [
        [
            (expected_diagonal[row], F(0)) if row == column
            else (F(0), F(0))
            for column in range(4)
        ]
        for row in range(4)
    ]

    lambda_max = F(4, 9)
    partial_trace_second = (F(2, 3), F(2, 27))
    lambda_min_marginal = min(partial_trace_second)
    proposed_right_side = F(2, 9) + lambda_min_marginal
    assert proposed_right_side == F(8, 27)
    assert lambda_max - proposed_right_side == F(4, 27) > 0

    print(
        "verified exact feature-marginal counterexample:",
        "K_f=diag(4/9,2/9,1/27,1/27),",
        "lambda_max-(2/9+lambda_min Tr_2 K_f)=4/27",
    )


if __name__ == "__main__":
    main()
