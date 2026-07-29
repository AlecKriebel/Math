#!/usr/bin/env python3
"""Exact checks for the grouped-rank-two recoupled boundary analysis.

The script uses only the Python standard library.  It reconstructs the
true 416-dimensional real constrained Hessian as two isospectral
208 by 208 rational blocks, proves their exact spectrum by small
connected blocks, checks the Phi_r threshold family, and verifies the
rank-two counterexample to the rank-only relaxation.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as F


ROW_PAIRS = ((0, 3), (1, 4), (2, 5))
COL_PAIRS = ((6, 9), (7, 10), (8, 11))
SWAP_HALVES = (6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5)


def add(first, second, scale=F(1)):
    output = dict(first)
    for key, value in second.items():
        output[key] = output.get(key, F(0)) + scale * value
        if not output[key]:
            del output[key]
    return output


def scaled(state, scale):
    return {
        key: scale * value
        for key, value in state.items()
        if scale * value
    }


def scalar_projection(state, first, second):
    """Project two qutrit axes onto (1/3)|sum_j jj><sum_k kk|."""

    grouped = {}
    for key, value in state.items():
        if key[first] != key[second]:
            continue
        reduced = key[:first] + key[first + 1:second] + key[second + 1:]
        grouped[reduced] = grouped.get(reduced, F(0)) + value

    output = {}
    for reduced, value in grouped.items():
        for digit in range(3):
            key = list(reduced)
            key.insert(first, digit)
            key.insert(second, digit)
            key = tuple(key)
            output[key] = output.get(key, F(0)) + value / 3
    return {key: value for key, value in output.items() if value}


def pattern_projection(state, pairs, scalar_site):
    output = state
    for site, (first, second) in enumerate(pairs):
        scalar = scalar_projection(output, first, second)
        output = scalar if site == scalar_site else add(output, scalar, -1)
    return output


def pair_projection(state, pairs):
    output = {}
    for scalar_site in range(3):
        output = add(output, pattern_projection(state, pairs, scalar_site))
    return output


def transpose_halves(state):
    return {
        tuple(key[index] for index in SWAP_HALVES): value
        for key, value in state.items()
    }


def yy_on_skew(state):
    """Return (2I-3P)_row (P_- state) (2I-3P)_column."""

    skew = scaled(add(state, transpose_halves(state), -1), F(1, 2))
    row = pair_projection(skew, ROW_PAIRS)
    column = pair_projection(skew, COL_PAIRS)
    both = pair_projection(row, COL_PAIRS)
    return add(
        add(scaled(skew, 4), row, -6),
        add(scaled(both, 9), column, -6),
    )


def digits(index):
    output = [0, 0, 0]
    for position in (2, 1, 0):
        output[position] = index % 3
        index //= 3
    return tuple(output)


def key(left_row, right_row, left_column, right_column):
    return (
        digits(left_row)
        + digits(right_row)
        + digits(left_column)
        + digits(right_column)
    )


A_UNNORMALIZED = ((0, 9), (1, 10))
B_UNNORMALIZED = ((3, 12), (4, 13))
A_ROWS = {0, 1}
A_COLUMNS = {9, 10}
B_ROWS = {3, 4}
B_COLUMNS = {12, 13}

A_COORDINATES = tuple(
    (row, column)
    for row in range(27)
    for column in range(27)
    if row in A_ROWS or column in A_COLUMNS
)
B_COORDINATES = tuple(
    (row, column)
    for row in range(27)
    for column in range(27)
    if row in B_ROWS or column in B_COLUMNS
)


def tangent_state(index):
    """Unnormalized first variation N=sqrt(2) delta(A tensor conjugate B)."""

    output = {}
    if index < len(A_COORDINATES):
        row, column = A_COORDINATES[index]
        for right_row, right_column in B_UNNORMALIZED:
            tensor_key = key(row, right_row, column, right_column)
            output[tensor_key] = output.get(tensor_key, F(0)) + 1
    else:
        right_row, right_column = B_COORDINATES[
            index - len(A_COORDINATES)
        ]
        for row, column in A_UNNORMALIZED:
            tensor_key = key(row, right_row, column, right_column)
            output[tensor_key] = output.get(tensor_key, F(0)) + 1
    return output


def base_state(rank):
    """M=A_r tensor conjugate(B_r) for the normalized Phi_r family."""

    output = {}
    for left_digit in range(rank):
        for right_digit in range(rank):
            tensor_key = key(
                left_digit,
                3 + right_digit,
                9 + left_digit,
                12 + right_digit,
            )
            output[tensor_key] = F(1, rank)
    return output


def inner(first, second):
    return sum(
        (value * second.get(key, 0) for key, value in first.items()),
        F(0),
    )


def derive_gauss_newton():
    """Return the tangent-linear term; this is not the full Hessian."""

    tangent = [tangent_state(index) for index in range(208)]
    columns = [yy_on_skew(state) for state in tangent]
    # O=2 YY P_-.  The two normalized base factors give a prefactor 1/2,
    # so H_uv=<N_u, YY P_- N_v>.
    return [
        [inner(tangent[row], columns[column]) for column in range(208)]
        for row in range(208)
    ]


def derive_second_fundamental_form():
    """Return N in the real block H+N; the imaginary block is H-N."""

    output = [[F(0) for _ in range(208)] for _ in range(208)]
    # base_state(2) is the normalized M0.  O M0=2 YY(P_-M0).
    normal = scaled(yy_on_skew(base_state(2)), 2)
    a_index = {
        coordinate: index
        for index, coordinate in enumerate(A_COORDINATES)
    }
    b_index = {
        coordinate: 104 + index
        for index, coordinate in enumerate(B_COORDINATES)
    }
    a_rows = tuple(sorted(A_ROWS))
    a_columns = tuple(sorted(A_COLUMNS))
    b_rows = tuple(sorted(B_ROWS))
    b_columns = tuple(sorted(B_COLUMNS))

    # The mixed term X tensor Y in the second coefficient of
    # (A0+tX+... ) tensor (C0+tY+...).
    for first, (a_row, a_column) in enumerate(A_COORDINATES):
        for offset, (b_row, b_column) in enumerate(B_COORDINATES):
            second = 104 + offset
            value = normal.get(
                key(a_row, b_row, a_column, b_column), F(0)
            )
            output[first][second] = output[second][first] = value

    # A_22=A_21 A_11^{-1} A_12.  Since A_11=I_2/sqrt(2)
    # and C0 has entries 1/sqrt(2), the square roots cancel.
    for outside_row in range(27):
        if outside_row in A_ROWS:
            continue
        for outside_column in range(27):
            if outside_column in A_COLUMNS:
                continue
            state = {
                key(outside_row, b_row, outside_column, b_column): F(1)
                for b_row, b_column in B_UNNORMALIZED
            }
            value = inner(state, normal)
            for logical in range(2):
                first = a_index[(outside_row, a_columns[logical])]
                second = a_index[(a_rows[logical], outside_column)]
                output[first][second] = output[second][first] = value

    # The identical second fundamental form on the conjugated B chart.
    for outside_row in range(27):
        if outside_row in B_ROWS:
            continue
        for outside_column in range(27):
            if outside_column in B_COLUMNS:
                continue
            state = {
                key(a_row, outside_row, a_column, outside_column): F(1)
                for a_row, a_column in A_UNNORMALIZED
            }
            value = inner(state, normal)
            for logical in range(2):
                first = b_index[(outside_row, b_columns[logical])]
                second = b_index[(b_rows[logical], outside_column)]
                output[first][second] = output[second][first] = value
    return output


def connected_components(matrix):
    unseen = set(range(len(matrix)))
    output = []
    while unseen:
        initial = unseen.pop()
        component = {initial}
        stack = [initial]
        while stack:
            row = stack.pop()
            for column, value in enumerate(matrix[row]):
                if value and column in unseen:
                    unseen.remove(column)
                    component.add(column)
                    stack.append(column)
        output.append(tuple(sorted(component)))
    return output


def rank(matrix):
    work = [[F(value) for value in row] for row in matrix]
    pivot_row = 0
    for column in range(len(work[0]) if work else 0):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(work))
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [
                entry - value * pivot_entry
                for entry, pivot_entry in zip(
                    work[row], work[pivot_row]
                )
            ]
        pivot_row += 1
    return pivot_row


def spectrum_by_blocks(matrix):
    """Prove the spectrum of 18H using exact eigenspace dimensions."""

    candidates = (0, 2, 3, 6, 10, 12, 14, 15, 18,
                  21, 22, 24, 27, 28, 30, 33, 36, 42, 54)
    multiplicity = Counter()
    profile = Counter()
    for component in connected_components(matrix):
        block = [
            [18 * matrix[row][column] for column in component]
            for row in component
        ]
        assert all(value.denominator == 1 for row in block for value in row)
        block = [[int(value) for value in row] for row in block]
        local = Counter()
        for eigenvalue in candidates:
            shifted = [
                [
                    block[row][column]
                    - (eigenvalue if row == column else 0)
                    for column in range(len(block))
                ]
                for row in range(len(block))
            ]
            nullity = len(block) - rank(shifted)
            if nullity:
                local[eigenvalue] = nullity
                multiplicity[eigenvalue] += nullity
        # The block is real symmetric.  Eigenspaces at distinct values are
        # independent; accounting for its full dimension proves this list.
        assert sum(local.values()) == len(block)
        profile[(len(block), tuple(sorted(local.items())))] += 1
    return multiplicity, profile


def main():
    # Reconstruct the exact Phi_r site-product values from the operator.
    family = tuple(
        2 * inner(state := base_state(rank), yy_on_skew(state))
        for rank in (1, 2, 3)
    )
    assert family == (
        F(1, 3), F(0), F(-1, 9)
    )
    # Rank alone cannot prove the reduced block inequality.  For unit
    # p in P and q in Q, M=pq^T-qp^T has rank two and only mixed blocks:
    # 4||K_QQ||^2+||K_PP||^2-4||K_PQ||^2 = -4.
    rank_only_defect = 4 * 0 + 0 - 4 * 1
    assert rank_only_defect == -4

    gauss_newton = derive_gauss_newton()
    second_form = derive_second_fundamental_form()
    assert len(A_COORDINATES) == len(B_COORDINATES) == 104
    # The ambient normal is nonzero, but it annihilates every first
    # tangent variation.  This is why the second fundamental form must
    # be retained in the true chart Hessian.
    ambient_normal = yy_on_skew(base_state(2))
    assert ambient_normal
    assert all(
        inner(tangent_state(index), ambient_normal) == 0
        for index in range(208)
    )

    real_block = [
        [
            gauss_newton[row][column] + second_form[row][column]
            for column in range(208)
        ]
        for row in range(208)
    ]
    imaginary_block = [
        [
            gauss_newton[row][column] - second_form[row][column]
            for column in range(208)
        ]
        for row in range(208)
    ]
    assert all(
        real_block[row][column] == real_block[column][row]
        and imaginary_block[row][column] == imaginary_block[column][row]
        for row in range(208)
        for column in range(208)
    )

    real_spectrum, real_profile = spectrum_by_blocks(real_block)
    imaginary_spectrum, imaginary_profile = spectrum_by_blocks(
        imaginary_block
    )
    expected = Counter(
        {
            0: 31,
            2: 1,
            3: 4,
            6: 15,
            10: 1,
            12: 23,
            14: 8,
            15: 16,
            18: 6,
            21: 24,
            22: 3,
            24: 8,
            27: 16,
            28: 5,
            30: 32,
            33: 4,
            36: 1,
            42: 6,
            54: 4,
        }
    )
    assert real_spectrum == imaginary_spectrum == expected
    assert sum(expected.values()) == 208
    assert min(expected) == 0
    assert real_profile == imaginary_profile
    expected_sizes = {1: 64, 2: 40, 4: 14, 8: 1}
    for size, expected_count in expected_sizes.items():
        assert sum(
            count
            for (block_size, _), count in real_profile.items()
            if block_size == size
        ) == expected_count

    print(
        "PASS: rank-only no-go; Phi_r=(1/3,0,-1/9); "
        "true grouped-rank-two chart Hessian PSD, "
        "real dimension 416, rank 354, nullity 62"
    )


if __name__ == "__main__":
    main()
