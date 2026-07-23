#!/usr/bin/env python3
"""Check the algebraic 2-adic lifting formulation around Eliahou's seed.

This checker is intentionally dependency-free.  It proves finite identities
used in NOVEL_LIFTING_64.md; it does not search for, or claim to construct, an
exact Hadamard matrix.
"""

from __future__ import annotations

from math import comb
from random import Random
from typing import Iterable, Sequence

from seed import ELIAHOU_Q, ELIAHOU_S, N
from variable_q_base import base_correlations, special_to_base


LONG = 84
SHORT = 83
INDEPENDENT_LAGS = range(1, 83)
ALL_LAGS = range(1, 84)


def sign_bits(sequence: Sequence[int]) -> list[int]:
    return [int(value == -1) for value in sequence]


def active_edges(q_bits: Sequence[int], lag: int) -> tuple[tuple[int, int], ...]:
    """Edges retained by the half mask and equality of the two q bits."""

    if len(q_bits) != N or not 1 <= lag <= 83:
        raise ValueError("wrong q length or lag")
    edges: list[tuple[int, int]] = []
    for offset, length in ((0, LONG), (LONG, SHORT)):
        for local in range(length - lag):
            left = offset + local
            right = left + lag
            if q_bits[left] == q_bits[right]:
                edges.append((left, right))
    return tuple(edges)


def gate_correlations(
    s_bits: Sequence[int], q_bits: Sequence[int]
) -> tuple[int, ...]:
    """Return T_k, where base correlation R_k=2*T_k."""

    if len(s_bits) != N or len(q_bits) != N:
        raise ValueError("wrong bit-vector length")
    result = []
    for lag in ALL_LAGS:
        result.append(
            sum(
                1 if s_bits[left] == s_bits[right] else -1
                for left, right in active_edges(q_bits, lag)
            )
        )
    return tuple(result)


def q_from_skeleton(parameters: Sequence[int]) -> list[int]:
    """Build the 167 q bits from its 84 exact first-lift parameters."""

    if len(parameters) != 84 or any(value not in (0, 1) for value in parameters):
        raise ValueError("the q skeleton needs 84 bits")
    long_free = list(parameters[:42])
    short_free = list(parameters[42:])
    long_bits = (
        long_free
        + list(reversed(long_free[1:]))
        + [1 ^ long_free[0]]
    )
    short_bits = short_free + list(reversed(short_free[:-1]))
    assert len(long_bits) == LONG
    assert len(short_bits) == SHORT
    return long_bits + short_bits


def q_has_skeleton(q_bits: Sequence[int]) -> bool:
    if len(q_bits) != N:
        return False
    long_bits = q_bits[:LONG]
    short_bits = q_bits[LONG:]
    return (
        long_bits[0] != long_bits[-1]
        and all(long_bits[index] == long_bits[83 - index] for index in range(1, 42))
        and all(short_bits[index] == short_bits[82 - index] for index in range(41))
    )


def active_counts_are_even(q_bits: Sequence[int]) -> bool:
    return all(len(active_edges(q_bits, lag)) % 2 == 0 for lag in ALL_LAGS)


def gf2_rref(
    equations: Iterable[tuple[int, int]], variables: int
) -> tuple[tuple[int, int], ...]:
    """Canonical reduced rows `(mask,rhs)` over GF(2)."""

    rows = [[mask, rhs] for mask, rhs in equations if mask or rhs]
    pivot_row = 0
    for column in range(variables):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(rows))
                if (rows[row][0] >> column) & 1
            ),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        for row in range(len(rows)):
            if row != pivot_row and ((rows[row][0] >> column) & 1):
                rows[row][0] ^= rows[pivot_row][0]
                rows[row][1] ^= rows[pivot_row][1]
        pivot_row += 1
    if any(mask == 0 and rhs for mask, rhs in rows):
        return tuple(sorted((mask, rhs) for mask, rhs in rows))
    return tuple(
        sorted(
            ((mask, rhs) for mask, rhs in rows if mask),
            key=lambda row: (row[0] & -row[0]).bit_length(),
        )
    )


def q_active_parity_equations() -> tuple[tuple[int, int], ...]:
    """Linear equations saying every active-edge count is even."""

    equations = []
    for lag in ALL_LAGS:
        mask = 0
        total_edges = 0
        for offset, length in ((0, LONG), (LONG, SHORT)):
            for local in range(length - lag):
                left = offset + local
                right = left + lag
                # equality(q_l,q_r) = 1 + q_l + q_r over GF(2)
                total_edges += 1
                mask ^= (1 << left) ^ (1 << right)
        equations.append((mask, total_edges & 1))
    return tuple(equations)


def q_skeleton_equations() -> tuple[tuple[int, int], ...]:
    equations = [((1 << 0) | (1 << 83), 1)]
    equations.extend(
        (((1 << index) | (1 << (83 - index))), 0)
        for index in range(1, 42)
    )
    equations.extend(
        (((1 << (84 + index)) | (1 << (166 - index))), 0)
        for index in range(41)
    )
    return tuple(equations)


def cyclic_cross_mask(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    """Coefficients of L*R^*+R*L^* in F2[C_167]."""

    values = []
    for lag in range(N):
        value = 0
        for index in range(N):
            value ^= (
                left[index] & right[(index - lag) % N]
            ) ^ (
                right[index] & left[(index - lag) % N]
            )
        values.append(value)
    return tuple(values)


def mod4_lift_equations(
    q_bits: Sequence[int],
) -> tuple[tuple[int, int], ...]:
    """The linear-in-s conditions T_k == 0 (mod 4), k=1,...,82."""

    equations = []
    for lag in INDEPENDENT_LAGS:
        edges = active_edges(q_bits, lag)
        if len(edges) % 2:
            raise ValueError("q is not on the first lifting layer")
        mask = 0
        for left, right in edges:
            mask ^= (1 << left) ^ (1 << right)
        equations.append((mask, (len(edges) // 2) & 1))
    return tuple(equations)


def rank_of_masks(masks: Iterable[int]) -> int:
    basis: dict[int, int] = {}
    for value in masks:
        while value:
            pivot = value.bit_length() - 1
            if pivot in basis:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                break
    return len(basis)


def system_consistent(equations: Sequence[tuple[int, int]]) -> bool:
    coefficient_rank = rank_of_masks(mask for mask, _ in equations)
    augmented_rank = rank_of_masks(mask | (rhs << N) for mask, rhs in equations)
    return coefficient_rank == augmented_rank


def equation_holds(mask: int, rhs: int, bits: Sequence[int]) -> bool:
    value = 0
    while mask:
        low = mask & -mask
        value ^= bits[low.bit_length() - 1]
        mask ^= low
    return value == rhs


def split_42_cross(
    sequences: Sequence[Sequence[int]],
) -> tuple[dict[int, int], dict[int, int]]:
    """Return coefficients of W and K in W+z^42 K+z^-42 K^*."""

    within: dict[int, int] = {}
    cross: dict[int, int] = {}
    for sequence in sequences:
        lower = sequence[:42]
        upper = sequence[42:]
        for block in (lower, upper):
            for left in range(len(block)):
                for right in range(len(block)):
                    exponent = left - right
                    within[exponent] = (
                        within.get(exponent, 0) + block[left] * block[right]
                    )
        for upper_index, upper_value in enumerate(upper):
            for lower_index, lower_value in enumerate(lower):
                exponent = upper_index - lower_index
                cross[exponent] = (
                    cross.get(exponent, 0) + upper_value * lower_value
                )
    return within, cross


def folded_periodic_correlations(
    sequences: Sequence[Sequence[int]],
) -> tuple[int, ...]:
    folded = []
    for sequence in sequences[:2]:
        folded.append((sequence[0] + sequence[83], *sequence[1:83]))
    folded.extend(tuple(sequence) for sequence in sequences[2:])
    result = []
    for lag in range(83):
        result.append(
            sum(
                sequence[index] * sequence[(index + lag) % 83]
                for sequence in folded
                for index in range(83)
            )
        )
    return tuple(result)


def q_parameter_flips() -> tuple[tuple[int, ...], ...]:
    """Physical q positions toggled by each of the 84 skeleton parameters."""

    result = [(index, 83 - index) for index in range(42)]
    result.extend((84 + index, 166 - index) for index in range(41))
    result.append((125,))
    return tuple(result)


def layer_bits(values: Sequence[int], shifts: Sequence[int]) -> tuple[int, ...]:
    return tuple((value >> shift) & 1 for shift in shifts for value in values)


def tangent_certificate(
    seed_s: Sequence[int], seed_q: Sequence[int]
) -> tuple[tuple[int, ...], int, int]:
    """Ranks and augmented rank for the Boolean first-order lift at the seed."""

    base_values = gate_correlations(seed_s, seed_q)[:82]
    base_layers = layer_bits(base_values, (1, 2, 3, 4))
    parameter_flips = (
        tuple(("q", positions) for positions in q_parameter_flips())
        + tuple(("s", (index,)) for index in range(N))
    )
    columns: list[int] = []
    for which, positions in parameter_flips:
        changed_s = list(seed_s)
        changed_q = list(seed_q)
        target = changed_q if which == "q" else changed_s
        for position in positions:
            target[position] ^= 1
        changed_layers = layer_bits(
            gate_correlations(changed_s, changed_q)[:82],
            (1, 2, 3, 4),
        )
        column = 0
        for row, (before, after) in enumerate(
            zip(base_layers, changed_layers, strict=True)
        ):
            if before ^ after:
                column |= 1 << row
        columns.append(column)

    rows = []
    for row in range(4 * 82):
        mask = 0
        for column, values in enumerate(columns):
            if (values >> row) & 1:
                mask |= 1 << column
        rows.append(mask)

    cumulative_ranks = tuple(
        rank_of_masks(rows[:end]) for end in (82, 164, 246, 328)
    )
    target = base_layers[246:]
    coefficient_rows = rows[:]
    augmented_rows = [
        mask | ((0 if index < 246 else target[index - 246]) << 251)
        for index, mask in enumerate(rows)
    ]
    return (
        cumulative_ranks,
        rank_of_masks(coefficient_rows),
        rank_of_masks(augmented_rows),
    )


def verify() -> None:
    seed_s = sign_bits(ELIAHOU_S)
    seed_q = sign_bits(ELIAHOU_Q)

    # The active-edge parity equations row-reduce exactly to the reciprocal
    # q skeleton, proving both necessity and sufficiency for the first layer.
    parity_rref = gf2_rref(q_active_parity_equations(), N)
    skeleton_rref = gf2_rref(q_skeleton_equations(), N)
    assert parity_rref == skeleton_rref
    assert len(parity_rref) == 83
    assert q_has_skeleton(seed_q)
    assert active_counts_are_even(seed_q)

    rng = Random(668)
    for _ in range(12):
        q_bits = q_from_skeleton([rng.randrange(2) for _ in range(84)])
        assert q_has_skeleton(q_bits)
        assert active_counts_are_even(q_bits)

    # Group-ring form H Q^* + Q H^* = J+1.
    half_mask = [0] * LONG + [1] * SHORT
    assert cyclic_cross_mask(half_mask, seed_q) == (0,) + (1,) * 166

    # Exact gate identity and all Hensel digit identities.
    base = special_to_base(ELIAHOU_S, ELIAHOU_Q)
    base_values = base_correlations(*base)
    gate_values = gate_correlations(seed_s, seed_q)
    assert tuple(2 * value for value in gate_values) == base_values[1:]
    for lag, value in zip(ALL_LAGS, gate_values, strict=True):
        edges = active_edges(seed_q, lag)
        cut = sum(seed_s[left] ^ seed_s[right] for left, right in edges)
        assert value == len(edges) - 2 * cut
        if lag <= 82:
            assert len(edges) % 2 == 0
            for bit in range(7):
                assert (comb(cut, 1 << bit) & 1) == ((cut >> bit) & 1)
                assert (comb(len(edges), 1 << (bit + 1)) & 1) == (
                    (len(edges) >> (bit + 1)) & 1
                )

    equations = mod4_lift_equations(seed_q)
    assert rank_of_masks(mask for mask, _ in equations) == 82
    assert system_consistent(equations)
    assert all(equation_holds(mask, rhs, seed_s) for mask, rhs in equations)
    assert all(value % 16 == 0 for value in gate_values)
    expected_bad = {
        32: (26, 34, 42, 50, 58),
        64: (8, 16, 26, 30, 34, 42, 50, 54, 58),
        128: (8, 12, 16, 26, 30, 34, 38, 42, 46, 50, 54, 58),
        256: (4, 8, 12, 16, 26, 30, 34, 38, 42, 46, 50, 54, 58),
    }
    for modulus, expected in expected_bad.items():
        actual = tuple(
            lag
            for lag, value in zip(ALL_LAGS, gate_values, strict=True)
            if value % modulus
        )
        assert actual == expected

    # The first failed syndrome is the Frobenius square
    # (z^13(1+z^4+...+z^16))^2 over GF(2).
    syndrome = {
        lag
        for lag, value in zip(ALL_LAGS, gate_values, strict=True)
        if (value // 16) & 1
    }
    square_root_support = {13 + 4 * index for index in range(5)}
    frobenius_square = {2 * exponent for exponent in square_root_support}
    assert syndrome == frobenius_square

    # Integer one-sided defect factorization.
    p = {4 * index: (-1) ** index for index in range(5)}
    p_square: dict[int, int] = {}
    for left_exp, left_value in p.items():
        for right_exp, right_value in p.items():
            exponent = left_exp + right_exp
            p_square[exponent] = (
                p_square.get(exponent, 0) + left_value * right_value
            )
    predicted = {
        4: -8,
        8: 6,
        12: -4,
        16: 2,
    }
    for exponent, coefficient in p_square.items():
        predicted[26 + exponent] = predicted.get(26 + exponent, 0) - coefficient
    actual_defect = {
        lag: value // 16
        for lag, value in zip(ALL_LAGS, gate_values, strict=True)
        if value
    }
    assert predicted == actual_defect

    # The 42+42 causal split: high lags are precisely K_0,...,K_41.
    within, cross = split_42_cross(base)
    for lag in range(1, 84):
        predicted_value = within.get(lag, 0)
        predicted_value += cross.get(lag - 42, 0)
        assert predicted_value == base_values[lag]
    expected_high_cross = {0: -160, 4: 128, 8: -96, 12: 64, 16: -32}
    assert {
        exponent: value
        for exponent, value in cross.items()
        if exponent >= 0 and value
    } == expected_high_cross

    # Folding at z^83=1 gives PAF_k=R_k+R_(83-k).
    folded = folded_periodic_correlations(base)
    assert folded[0] == base_values[0] + 2 * (
        base[0][0] * base[0][83] + base[1][0] * base[1][83]
    )
    for lag in range(1, 83):
        assert folded[lag] == base_values[lag] + base_values[83 - lag]

    # Fixed-s row-sum obstruction: B(1)^2+D(1)^2 would have to equal 321.
    fixed_a_sum = sum(base[0])
    fixed_c_sum = sum(base[2])
    assert (fixed_a_sum, fixed_c_sum) == (-2, 3)
    remaining = 334 - fixed_a_sum**2 - fixed_c_sum**2
    assert remaining == 321 and remaining % 3 == 0 and remaining % 9 != 0

    # Strict alternation of q makes exactly three lag-82 edges active.
    alternating_q = [
        local & 1
        for length in (LONG, SHORT)
        for local in range(length)
    ]
    assert not q_has_skeleton(alternating_q)
    assert len(active_edges(alternating_q, 82)) == 3

    # Exact Boolean-Jacobian certificate at the published modular point.
    ranks, coefficient_rank, augmented_rank = tangent_certificate(seed_s, seed_q)
    assert ranks == (82, 163, 200, 200)
    assert coefficient_rank == 200
    assert augmented_rank == 201


if __name__ == "__main__":
    verify()
    print("PASS q first-lift skeleton: 84 parameters and group-ring identity")
    print("PASS s second lift: rank 82, leaving an 85-dimensional affine fiber")
    print("PASS finite Hensel ladder and five-lag Frobenius-square obstruction")
    print("PASS 42+42 causal split, folding identity, and tangent obstruction")
