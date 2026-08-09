#!/usr/bin/env python3
"""Exact rank-dependent-``K_0`` certificate on the n=17 witness.

Here ``K_0=Pi-P^T Pi P`` is the reversible two-request covariance matrix.
The potential space contains rank constants, arbitrary rank-labelled vertex
terms, and one scalar coefficient of ``s^T K_0 s`` on every rank.  A rational
primal/dual pair proves that this space also repairs the exact single-global-
conductance witness.  This finite certificate is not a universal theorem.
"""

from __future__ import annotations

from fractions import Fraction as Q

from flint import fmpq, fmpq_mat

from verify_global_conductance_farkas_refutation import (
    CLASS_SIZES,
    CLASS_WEIGHTS,
    N_VERTICES,
    class_degrees,
    orbit_rates,
    orbit_states,
)
from verify_rank_dependent_conductance_witness import (
    decimal_string,
    from_fmpq,
    to_fmpq,
)


DUAL_SUPPORT = (
    (0, 0, 1), (0, 0, 2), (0, 1, 0), (0, 1, 1), (0, 1, 2),
    (0, 1, 3), (0, 2, 0), (0, 2, 1), (0, 2, 2), (0, 2, 3),
    (0, 2, 4), (0, 2, 5), (0, 2, 6), (0, 3, 3), (0, 3, 4),
    (0, 3, 5), (0, 3, 6), (0, 3, 7), (0, 3, 8), (0, 3, 9),
    (0, 4, 5), (0, 4, 6), (0, 4, 7), (0, 4, 8), (0, 4, 9),
    (0, 4, 10), (0, 5, 0), (0, 5, 8), (0, 5, 9), (0, 5, 10),
    (1, 0, 0), (1, 5, 10), (2, 0, 0), (2, 0, 1), (2, 0, 2),
    (2, 0, 3), (2, 0, 4), (2, 0, 5), (2, 0, 6), (2, 0, 7),
    (2, 0, 8), (2, 0, 9), (2, 0, 10), (2, 1, 0), (2, 1, 1),
    (2, 1, 2), (2, 1, 3), (2, 1, 4), (2, 1, 5), (2, 1, 6),
    (2, 1, 7), (2, 1, 8), (2, 1, 9), (2, 1, 10), (2, 2, 10),
    (2, 3, 8), (2, 3, 9), (2, 3, 10), (2, 4, 9), (2, 4, 10),
    (2, 5, 8), (2, 5, 9),
)


DEGREES = class_degrees()
TOTAL_DEGREE = sum(
    size * degree for size, degree in zip(CLASS_SIZES, DEGREES)
)
PI_PER_VERTEX = tuple(Q(degree, TOTAL_DEGREE) for degree in DEGREES)


def collision_feature(state: tuple[int, int, int]) -> Q:
    """Evaluate ``s^T(Pi-P^T Pi P)s=sum_v pi_v x_v(1-x_v)``."""

    value = Q(0)
    for vertex_class, size in enumerate(CLASS_SIZES):
        weighted_mutants = sum(
            CLASS_WEIGHTS[vertex_class][other] * state[other]
            for other in range(len(CLASS_SIZES))
        )
        mutant_count = state[vertex_class]
        if mutant_count:
            x_in = Q(
                weighted_mutants - CLASS_WEIGHTS[vertex_class][vertex_class],
                DEGREES[vertex_class],
            )
            value += (
                mutant_count * PI_PER_VERTEX[vertex_class]
                * x_in * (1 - x_in)
            )
        if mutant_count < size:
            x_out = Q(weighted_mutants, DEGREES[vertex_class])
            value += (
                (size - mutant_count) * PI_PER_VERTEX[vertex_class]
                * x_out * (1 - x_out)
            )
    return value


def feature_keys() -> list[tuple[object, ...]]:
    keys: list[tuple[object, ...]] = []
    for rank in range(1, N_VERTICES):
        keys.extend(((rank, "constant"), (rank, 0), (rank, 1)))
        if 2 <= rank <= N_VERTICES - 2:
            keys.append((rank, "collision"))
    keys.append((N_VERTICES, "constant"))
    assert len(keys) == 63
    return keys


KEYS = feature_keys()


def features(state: tuple[int, int, int]) -> list[Q]:
    rank = sum(state)
    return [
        Q(0)
        if key[0] != rank
        else Q(1)
        if key[1] == "constant"
        else collision_feature(state)
        if key[1] == "collision"
        else Q(state[int(key[1])])
        for key in KEYS
    ]


def exact_system() -> tuple[
    list[tuple[int, int, int]], list[list[Q]], list[Q], list[Q]
]:
    states = orbit_states()
    empty = (0, 0, 0)
    full = CLASS_SIZES
    cache = {state: features(state) for state in states + [empty, full]}
    rows = []
    for state in states:
        gain, loss = orbit_rates(state)
        row = [Q(0) for _ in KEYS]
        total = Q(0)
        for vertex_class, size in enumerate(CLASS_SIZES):
            count = state[vertex_class]
            if count < size:
                rate = (size - count) * gain[vertex_class]
                target = list(state)
                target[vertex_class] += 1
                total += rate
                row = [
                    old + rate * (new - current)
                    for old, new, current in zip(
                        row, cache[tuple(target)], cache[state]
                    )
                ]
            if count > 0:
                rate = count * loss[vertex_class]
                target = list(state)
                target[vertex_class] -= 1
                total += rate
                row = [
                    old + rate * (new - current)
                    for old, new, current in zip(
                        row, cache[tuple(target)], cache[state]
                    )
                ]
        assert total > 0
        rows.append([value / total for value in row])

    objective = [Q(0) for _ in KEYS]
    for vertex_class, size in enumerate(CLASS_SIZES):
        singleton = tuple(
            int(other == vertex_class) for other in range(len(CLASS_SIZES))
        )
        objective = [
            old + Q(size, N_VERTICES) * value
            for old, value in zip(objective, cache[singleton])
        ]
    return states, rows, objective, cache[full]


def exact_primal_dual() -> tuple[list[Q], list[Q], Q]:
    states, rows, objective, boundary = exact_system()
    index = {state: j for j, state in enumerate(states)}
    support_rows = [rows[index[state]] for state in DUAL_SUPPORT]
    assert len(states) == 196 and len(DUAL_SUPPORT) == 62

    dual_matrix = fmpq_mat(
        [
            [to_fmpq(row[column]) for row in support_rows]
            + [to_fmpq(-boundary[column])]
            for column in range(len(KEYS))
        ]
    )
    dual_rhs = fmpq_mat([[-to_fmpq(value)] for value in objective])
    dual_solution = dual_matrix.solve(dual_rhs)
    y = [from_fmpq(dual_solution[j, 0]) for j in range(len(DUAL_SUPPORT))]
    z = from_fmpq(dual_solution[len(DUAL_SUPPORT), 0])
    assert all(value > 0 for value in y)

    primal_matrix = fmpq_mat(
        [[to_fmpq(value) for value in row] for row in support_rows]
        + [[to_fmpq(value) for value in boundary]]
    )
    primal_rhs = fmpq_mat([[fmpq(0)] for _ in support_rows] + [[fmpq(1)]])
    primal_solution = primal_matrix.solve(primal_rhs)
    coefficients = [
        from_fmpq(primal_solution[j, 0]) for j in range(len(KEYS))
    ]

    for column in range(len(KEYS)):
        assert (
            objective[column]
            + sum(y[j] * support_rows[j][column] for j in range(len(y)))
            - z * boundary[column]
            == 0
        )
    assert sum(a * b for a, b in zip(boundary, coefficients)) == 1
    assert sum(a * b for a, b in zip(objective, coefficients)) == z
    drifts = [sum(a * b for a, b in zip(row, coefficients)) for row in rows]
    assert all(value <= 0 for value in drifts)
    assert all(drifts[index[state]] == 0 for state in DUAL_SUPPORT)
    values = [
        sum(a * b for a, b in zip(features(state), coefficients))
        for state in states
    ]
    assert all(value >= 0 for value in values)
    return y, coefficients, z


def main() -> None:
    y, coefficients, optimum = exact_primal_dual()
    baseline = Q(524_288, 1_114_095)
    gap = baseline - optimum
    assert gap > 0
    print("rank-dependent-K0 n=17 certificate: PASS")
    print("exact quotient drift rows checked: 196")
    print(f"restricted function-space dimension: {len(coefficients)}")
    print(f"strictly positive dual support weights: {len(y)}")
    print(f"exact restricted optimum: {decimal_string(optimum)}")
    print(f"K_17 baseline: {baseline}")
    print(f"strict exact margin below baseline: {decimal_string(gap)} > 0")


if __name__ == "__main__":
    main()
