#!/usr/bin/env python3
"""Targeted full-fitness quotient audit for the frozen seven-arm theta graph.

The quotient has 13,728 S_7-orbits (hub bits and counts of the eight arm
patterns).  This script is proof infrastructure, not a parameter search.  It
builds both update rules directly and solves the sparse first-step systems.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb

import numpy as np
import sympy as sp
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import bicgstab


SERIES_ORDER = 4
ZERO_SERIES = (F(0),) * (SERIES_ORDER + 1)
ONE_SERIES = (F(1),) + (F(0),) * SERIES_ORDER


def s_add(*values):
    return tuple(
        sum((value[k] for value in values), F(0))
        for k in range(SERIES_ORDER + 1)
    )


def s_neg(value):
    return tuple(-entry for entry in value)


def s_scale(value, scalar):
    return tuple(scalar * entry for entry in value)


def s_mul(left, right):
    return tuple(
        sum((left[i] * right[k - i] for i in range(k + 1)), F(0))
        for k in range(SERIES_ORDER + 1)
    )


def s_inv(value):
    if not value[0]:
        raise ZeroDivisionError(value)
    answer = [F(1, 1) / value[0]]
    for k in range(1, SERIES_ORDER + 1):
        answer.append(
            -sum(value[i] * answer[k - i] for i in range(1, k + 1))
            / value[0]
        )
    return tuple(answer)


def s_div(numerator, denominator):
    return s_mul(numerator, s_inv(denominator))


def s_linear(constant, slope):
    return (F(constant), F(slope)) + (F(0),) * (SERIES_ORDER - 1)


ARMS = 7
ORDER = 23
PATTERNS = tuple(product((0, 1), repeat=3))
PATTERN_INDEX = {pattern: index for index, pattern in enumerate(PATTERNS)}


def compositions(total: int, parts: int):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, parts - 1):
            yield (first,) + rest


COUNTS = tuple(compositions(ARMS, len(PATTERNS)))
STATES = tuple(
    (left_hub, right_hub, counts)
    for left_hub in (0, 1)
    for right_hub in (0, 1)
    for counts in COUNTS
)
EXTINCTION = (0, 0, (ARMS,) + (0,) * 7)
FIXATION = (1, 1, (0,) * 7 + (ARMS,))
TRANSIENT = tuple(state for state in STATES if state not in (EXTINCTION, FIXATION))
INDEX = {state: index for index, state in enumerate(TRANSIENT)}


def changed_counts(counts, old_pattern, new_pattern):
    result = list(counts)
    result[PATTERN_INDEX[old_pattern]] -= 1
    result[PATTERN_INDEX[new_pattern]] += 1
    return tuple(result)


@lru_cache(maxsize=None)
def neighbours(location: int):
    """Return (other kind, edge-weight label) for a vertex in one arm."""

    if location == 0:
        return (("left_hub", "x"), (1, "one"))
    if location == 1:
        return ((0, "one"), (2, "one"))
    return ((1, "one"), ("right_hub", "x"))


def add_change(row, target, probability):
    if probability:
        row[target] = row.get(target, probability * 0) + probability


def changes(state, fitness: float, x: float, rule: str):
    left_hub, right_hub, counts = state
    row = {}
    one = x * 0 + 1
    hub_degree = ARMS * x
    endpoint_degree = 1 + x
    middle_degree = 2 * one
    total_degree = 2 * hub_degree + 14 * endpoint_degree + 7 * middle_degree

    if rule == "Bd":
        mutant_count = left_hub + right_hub + sum(
            count * sum(pattern) for count, pattern in zip(counts, PATTERNS)
        )
        total_fitness = ORDER + (fitness - 1) * mutant_count

        # Hub births.  Each selects one of the seven endpoint targets.
        for side, hub_type in ((0, left_hub), (1, right_hub)):
            birth_probability = (fitness if hub_type else one) / total_fitness
            for pattern, count in zip(PATTERNS, counts):
                if not count:
                    continue
                position = 0 if side == 0 else 2
                if pattern[position] == hub_type:
                    continue
                new_pattern = list(pattern)
                new_pattern[position] = hub_type
                target = (
                    left_hub,
                    right_hub,
                    changed_counts(counts, pattern, tuple(new_pattern)),
                )
                add_change(row, target, birth_probability * count / ARMS)

        # Internal births, aggregated by arm pattern and source position.
        for pattern, count in zip(PATTERNS, counts):
            if not count:
                continue
            for source_position in range(3):
                source_type = pattern[source_position]
                birth_probability = (
                    count
                    * (fitness if source_type else one)
                    / total_fitness
                )
                source_degree = endpoint_degree if source_position in (0, 2) else middle_degree
                for target_kind, weight_label in neighbours(source_position):
                    weight = x if weight_label == "x" else one
                    if target_kind == "left_hub":
                        if left_hub != source_type:
                            add_change(
                                row,
                                (source_type, right_hub, counts),
                                birth_probability * weight / source_degree,
                            )
                    elif target_kind == "right_hub":
                        if right_hub != source_type:
                            add_change(
                                row,
                                (left_hub, source_type, counts),
                                birth_probability * weight / source_degree,
                            )
                    elif pattern[target_kind] != source_type:
                        new_pattern = list(pattern)
                        new_pattern[target_kind] = source_type
                        target = (
                            left_hub,
                            right_hub,
                            changed_counts(counts, pattern, tuple(new_pattern)),
                        )
                        add_change(
                            row,
                            target,
                            birth_probability * weight / source_degree,
                        )

    elif rule == "dB":
        # Hub deaths.  Its seven endpoint neighbours compete.
        for side, hub_type in ((0, left_hub), (1, right_hub)):
            position = 0 if side == 0 else 2
            mutants = sum(count * pattern[position] for count, pattern in zip(counts, PATTERNS))
            denominator = ARMS + (fitness - 1) * mutants
            opposite = 1 - hub_type
            opposite_count = mutants if opposite else ARMS - mutants
            if opposite_count:
                probability = one * (fitness if opposite else one) * opposite_count / (ORDER * denominator)
                target = (opposite, right_hub, counts) if side == 0 else (left_hub, opposite, counts)
                add_change(row, target, probability)

        # Internal deaths.  Neighbours compete locally.
        for pattern, count in zip(PATTERNS, counts):
            if not count:
                continue
            for target_position in range(3):
                target_type = pattern[target_position]
                competitor_types = []
                competitor_weights = []
                for source_kind, weight_label in neighbours(target_position):
                    weight = x if weight_label == "x" else one
                    if source_kind == "left_hub":
                        source_type = left_hub
                    elif source_kind == "right_hub":
                        source_type = right_hub
                    else:
                        source_type = pattern[source_kind]
                    competitor_types.append(source_type)
                    competitor_weights.append(weight)
                denominator = sum(
                    weight * (fitness if source_type else one)
                    for weight, source_type in zip(competitor_weights, competitor_types)
                )
                opposite = 1 - target_type
                numerator = sum(
                    weight * (fitness if source_type else one)
                    for weight, source_type in zip(competitor_weights, competitor_types)
                    if source_type == opposite
                )
                if numerator:
                    new_pattern = list(pattern)
                    new_pattern[target_position] = opposite
                    target = (
                        left_hub,
                        right_hub,
                        changed_counts(counts, pattern, tuple(new_pattern)),
                    )
                    add_change(row, target, one * count * numerator / (ORDER * denominator))
    else:
        raise ValueError(rule)
    return row


def changes_series(state, x: F, rule: str):
    """Type-changing rows over QQ[[epsilon]]/(epsilon^4), r=1+epsilon."""

    left_hub, right_hub, counts = state
    row = {}
    hub_degree = ARMS * x
    endpoint_degree = 1 + x
    middle_degree = F(2)

    def add(target, probability):
        if probability != ZERO_SERIES:
            row[target] = s_add(row.get(target, ZERO_SERIES), probability)

    if rule == "Bd":
        mutant_count = left_hub + right_hub + sum(
            count * sum(pattern) for count, pattern in zip(counts, PATTERNS)
        )
        inverse_total_fitness = s_inv(s_linear(ORDER, mutant_count))

        for side, hub_type in ((0, left_hub), (1, right_hub)):
            birth_probability = s_mul(
                s_linear(1, hub_type), inverse_total_fitness
            )
            for pattern, count in zip(PATTERNS, counts):
                if not count:
                    continue
                position = 0 if side == 0 else 2
                if pattern[position] == hub_type:
                    continue
                new_pattern = list(pattern)
                new_pattern[position] = hub_type
                target = (
                    left_hub,
                    right_hub,
                    changed_counts(counts, pattern, tuple(new_pattern)),
                )
                add(target, s_scale(birth_probability, F(count, ARMS)))

        for pattern, count in zip(PATTERNS, counts):
            if not count:
                continue
            for source_position in range(3):
                source_type = pattern[source_position]
                birth_probability = s_scale(
                    s_mul(
                        s_linear(1, source_type), inverse_total_fitness
                    ),
                    F(count),
                )
                source_degree = (
                    endpoint_degree
                    if source_position in (0, 2)
                    else middle_degree
                )
                for target_kind, weight_label in neighbours(source_position):
                    weight = x if weight_label == "x" else F(1)
                    factor = weight / source_degree
                    if target_kind == "left_hub":
                        if left_hub != source_type:
                            add(
                                (source_type, right_hub, counts),
                                s_scale(birth_probability, factor),
                            )
                    elif target_kind == "right_hub":
                        if right_hub != source_type:
                            add(
                                (left_hub, source_type, counts),
                                s_scale(birth_probability, factor),
                            )
                    elif pattern[target_kind] != source_type:
                        new_pattern = list(pattern)
                        new_pattern[target_kind] = source_type
                        add(
                            (
                                left_hub,
                                right_hub,
                                changed_counts(
                                    counts, pattern, tuple(new_pattern)
                                ),
                            ),
                            s_scale(birth_probability, factor),
                        )
    elif rule == "dB":
        for side, hub_type in ((0, left_hub), (1, right_hub)):
            position = 0 if side == 0 else 2
            mutants = sum(
                count * pattern[position]
                for count, pattern in zip(counts, PATTERNS)
            )
            inverse_denominator = s_inv(s_linear(ARMS, mutants))
            opposite = 1 - hub_type
            opposite_count = mutants if opposite else ARMS - mutants
            if opposite_count:
                probability = s_scale(
                    s_mul(s_linear(1, opposite), inverse_denominator),
                    F(opposite_count, ORDER),
                )
                target = (
                    (opposite, right_hub, counts)
                    if side == 0
                    else (left_hub, opposite, counts)
                )
                add(target, probability)

        for pattern, count in zip(PATTERNS, counts):
            if not count:
                continue
            for target_position in range(3):
                target_type = pattern[target_position]
                competitors = []
                for source_kind, weight_label in neighbours(target_position):
                    weight = x if weight_label == "x" else F(1)
                    if source_kind == "left_hub":
                        source_type = left_hub
                    elif source_kind == "right_hub":
                        source_type = right_hub
                    else:
                        source_type = pattern[source_kind]
                    competitors.append((weight, source_type))
                denominator = ZERO_SERIES
                numerator = ZERO_SERIES
                opposite = 1 - target_type
                for weight, source_type in competitors:
                    term = s_scale(s_linear(1, source_type), weight)
                    denominator = s_add(denominator, term)
                    if source_type == opposite:
                        numerator = s_add(numerator, term)
                if numerator != ZERO_SERIES:
                    new_pattern = list(pattern)
                    new_pattern[target_position] = opposite
                    add(
                        (
                            left_hub,
                            right_hub,
                            changed_counts(counts, pattern, tuple(new_pattern)),
                        ),
                        s_scale(s_div(numerator, denominator), F(count, ORDER)),
                    )
    else:
        raise ValueError(rule)
    return row


def solve(fitness: float, x: float, rule: str, return_atoms: bool = False):
    rows = []
    columns = []
    data = []
    rhs = np.zeros(len(TRANSIENT))
    for state, row_index in INDEX.items():
        row = changes(state, fitness, x, rule)
        exit_probability = sum(row.values())
        if not exit_probability:
            raise RuntimeError((rule, state, "zero type-changing probability"))
        rows.append(row_index)
        columns.append(row_index)
        data.append(exit_probability)
        for target, probability in row.items():
            if target == FIXATION:
                rhs[row_index] += probability
            elif target != EXTINCTION:
                rows.append(row_index)
                columns.append(INDEX[target])
                data.append(-probability)
    matrix = csr_matrix((data, (rows, columns)), shape=(len(TRANSIENT), len(TRANSIENT)))
    diagonal = matrix.diagonal()
    scaled = matrix.multiply((1 / diagonal)[:, None]).tocsr()
    scaled_rhs = rhs / diagonal
    solution, info = bicgstab(
        scaled,
        scaled_rhs,
        rtol=2e-12,
        atol=1e-14,
        maxiter=200_000,
    )
    if info != 0:
        raise RuntimeError((rule, "bicgstab", info))
    residual = np.max(np.abs(matrix @ solution - rhs))

    # Uniform placement: two hubs plus 21 internal vertices.
    hub_left = solution[INDEX[(1, 0, (ARMS,) + (0,) * 7)]]
    hub_right = solution[INDEX[(0, 1, (ARMS,) + (0,) * 7)]]
    internal_sum = 0.0
    zero = (0, 0, 0)
    for position in range(3):
        pattern = list(zero)
        pattern[position] = 1
        counts = [0] * 8
        counts[PATTERN_INDEX[zero]] = ARMS - 1
        counts[PATTERN_INDEX[tuple(pattern)]] = 1
        internal_sum += ARMS * solution[INDEX[(0, 0, tuple(counts))]]
    fixation = (hub_left + hub_right + internal_sum) / ORDER
    if return_atoms:
        atoms = {
            "hub": (hub_left + hub_right) / 2,
        }
        zero = (0, 0, 0)
        for position in range(3):
            pattern = list(zero)
            pattern[position] = 1
            counts = [0] * 8
            counts[PATTERN_INDEX[zero]] = ARMS - 1
            counts[PATTERN_INDEX[tuple(pattern)]] = 1
            atoms[f"position_{position}"] = solution[
                INDEX[(0, 0, tuple(counts))]
            ]
        return fixation, residual, atoms
    return fixation, residual


def solve_series(x: F, rule: str):
    """Exact fixation Taylor series through epsilon^3 at r=1."""

    matrices = [([], [], []) for _ in range(SERIES_ORDER + 1)]
    rhs = [[F(0) for _ in TRANSIENT] for _ in range(SERIES_ORDER + 1)]
    for state, row_index in INDEX.items():
        row = changes_series(state, x, rule)
        exit_probability = s_add(*row.values())
        for order in range(SERIES_ORDER + 1):
            matrices[order][0].append(row_index)
            matrices[order][1].append(row_index)
            matrices[order][2].append(float(exit_probability[order]))
        for target, probability in row.items():
            if target == FIXATION:
                for order in range(SERIES_ORDER + 1):
                    rhs[order][row_index] += probability[order]
            elif target != EXTINCTION:
                column = INDEX[target]
                for order in range(SERIES_ORDER + 1):
                    matrices[order][0].append(row_index)
                    matrices[order][1].append(column)
                    matrices[order][2].append(-float(probability[order]))
    sparse = [
        csr_matrix(
            (values, (rows, columns)),
            shape=(len(TRANSIENT), len(TRANSIENT)),
        )
        for rows, columns, values in matrices
    ]
    A0 = sparse[0]
    diagonal = A0.diagonal()
    scaled_A0 = A0.multiply((1 / diagonal)[:, None]).tocsr()

    coefficients = []
    residuals = []
    for order in range(SERIES_ORDER + 1):
        forcing = np.array([float(value) for value in rhs[order]])
        for k in range(1, order + 1):
            forcing -= sparse[k] @ coefficients[order - k]
        solution, info = bicgstab(
            scaled_A0,
            forcing / diagonal,
            rtol=5e-13,
            atol=2e-14,
            maxiter=300_000,
        )
        if info != 0:
            raise RuntimeError((rule, "series bicgstab", order, info))
        coefficients.append(solution)
        residuals.append(np.max(np.abs(A0 @ solution - forcing)))

    def average(vector):
        hub_left = vector[INDEX[(1, 0, (ARMS,) + (0,) * 7)]]
        hub_right = vector[INDEX[(0, 1, (ARMS,) + (0,) * 7)]]
        internal_sum = 0.0
        zero = (0, 0, 0)
        for position in range(3):
            pattern = list(zero)
            pattern[position] = 1
            counts = [0] * 8
            counts[PATTERN_INDEX[zero]] = ARMS - 1
            counts[PATTERN_INDEX[tuple(pattern)]] = 1
            internal_sum += ARMS * vector[INDEX[(0, 0, tuple(counts))]]
        return (hub_left + hub_right + internal_sum) / ORDER

    return np.array([average(vector) for vector in coefficients]), residuals


def baseline_series(order: int, rule: str):
    """Complete-graph Taylor coefficients through epsilon^3."""

    epsilon = sp.symbols("epsilon")
    if rule == "Bd":
        expression = (1 - 1 / (1 + epsilon)) / (
            1 - (1 + epsilon) ** (-order)
        )
    else:
        expression = sp.Rational(order - 1, order) * (
            1 - 1 / (1 + epsilon)
        ) / (
            1 - (1 + epsilon) ** (1 - order)
        )
    polynomial = sp.Poly(
        sp.series(expression, epsilon, 0, SERIES_ORDER).removeO(), epsilon
    )
    return np.array(
        [float(polynomial.coeff_monomial(epsilon**k)) for k in range(SERIES_ORDER)]
    )


def series_divide(numerator, denominator):
    result = []
    for order in range(len(numerator)):
        value = numerator[order]
        for k in range(1, order + 1):
            value -= denominator[k] * result[order - k]
        result.append(value / denominator[0])
    return np.array(result)


def baseline(order: int, fitness: float, rule: str):
    if rule == "Bd":
        return (1 - 1 / fitness) / (1 - fitness ** (-order))
    return ((order - 1) / order) * (1 - 1 / fitness) / (1 - fitness ** (1 - order))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--r", type=float, default=1.01)
    parser.add_argument("--x", type=float, default=103 / 500)
    parser.add_argument("--series", action="store_true")
    args = parser.parse_args()
    assert len(STATES) == 13728
    assert len(TRANSIENT) == 13726
    print(f"states={len(STATES)} transient={len(TRANSIENT)}")
    for rule in ("Bd", "dB"):
        if args.series:
            rational_x = F(str(args.x))
            fixation_coefficients, series_residuals = solve_series(
                rational_x, rule
            )
            reference_coefficients = baseline_series(ORDER, rule)
            normalized = series_divide(
                fixation_coefficients[:SERIES_ORDER], reference_coefficients
            )
            print(
                f"{rule} Taylor rho coefficients={fixation_coefficients.tolist()}"
            )
            print(
                f"{rule} Taylor normalized-gap coefficients="
                f"{(normalized - np.array([1.0, 0.0, 0.0, 0.0])).tolist()} "
                f"residuals={[float(value) for value in series_residuals]}"
            )
        fixation, residual = solve(args.r, args.x, rule)
        reference = baseline(ORDER, args.r, rule)
        gap = fixation / reference - 1
        print(
            f"{rule}: rho={fixation:.16g} ref={reference:.16g} "
            f"normalized_gap={gap:+.12g} residual={residual:.3e}"
        )


if __name__ == "__main__":
    main()
