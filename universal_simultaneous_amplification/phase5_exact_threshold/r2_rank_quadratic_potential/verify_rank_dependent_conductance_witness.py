#!/usr/bin/env python3
"""Exact rank-dependent-conductance certificate on the n=17 witness.

The single-global-conductance potential fails on this graph.  This verifier
shows that allowing an independent internal-conductance coefficient on every
rank repairs that exact witness: it constructs matching rational primal and
dual solutions in the 196-state class quotient, checks every drift inequality,
and proves that the restricted optimum is strictly below the K_17 baseline.

This is a finite exact certificate, not a universal theorem.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction as Q

from flint import fmpq, fmpq_mat

from verify_global_conductance_farkas_refutation import (
    CLASS_SIZES,
    N_VERTICES,
    internal_feature,
    orbit_rates,
    orbit_states,
)


# The strictly positive dual support discovered in floating arithmetic.
# All calculations after this declaration are exact.
DUAL_SUPPORT = (
    (0, 0, 1),
    (0, 0, 2),
    (0, 1, 0),
    (0, 1, 1),
    (0, 1, 2),
    (0, 2, 1),
    (0, 2, 2),
    (0, 2, 3),
    (0, 3, 1),
    (0, 3, 2),
    (0, 3, 3),
    (0, 3, 4),
    (0, 3, 5),
    (0, 3, 6),
    (0, 3, 7),
    (0, 3, 8),
    (0, 3, 9),
    (0, 4, 6),
    (0, 4, 7),
    (0, 4, 8),
    (0, 4, 9),
    (0, 4, 10),
    (0, 5, 8),
    (0, 5, 9),
    (0, 5, 10),
    (1, 0, 0),
    (1, 0, 6),
    (1, 0, 7),
    (1, 0, 8),
    (1, 0, 9),
    (1, 1, 0),
    (1, 1, 10),
    (1, 2, 0),
    (1, 2, 10),
    (1, 3, 10),
    (1, 4, 10),
    (1, 5, 10),
    (2, 0, 0),
    (2, 0, 1),
    (2, 0, 2),
    (2, 0, 3),
    (2, 0, 4),
    (2, 0, 5),
    (2, 0, 6),
    (2, 0, 7),
    (2, 0, 8),
    (2, 0, 9),
    (2, 0, 10),
    (2, 1, 1),
    (2, 1, 2),
    (2, 1, 3),
    (2, 1, 4),
    (2, 1, 10),
    (2, 2, 4),
    (2, 2, 5),
    (2, 2, 6),
    (2, 2, 7),
    (2, 2, 10),
    (2, 3, 10),
    (2, 4, 9),
    (2, 4, 10),
    (2, 5, 9),
)


def feature_keys() -> list[tuple[object, ...]]:
    """A nonredundant basis for the invariant rank-conductance space."""

    keys: list[tuple[object, ...]] = []
    for rank in range(1, N_VERTICES):
        keys.extend(((rank, "constant"), (rank, 0), (rank, 1)))
        # Rank one has no internal edge.  At rank n-1, internal edge weight
        # is an affine function of the missing vertex and is already in the
        # rank-labelled constant/vertex span.  Thus ranks 2,...,n-2 contain
        # every independent conductance column.
        if 2 <= rank <= N_VERTICES - 2:
            keys.append((rank, "internal"))
    keys.append((N_VERTICES, "constant"))
    assert len(keys) == 63
    return keys


KEYS = feature_keys()


def features(state: tuple[int, int, int]) -> list[Q]:
    rank = sum(state)
    values = []
    for key in KEYS:
        if key[0] != rank:
            values.append(Q(0))
        elif key[1] == "constant":
            values.append(Q(1))
        elif key[1] == "internal":
            values.append(internal_feature(state))
        else:
            values.append(Q(state[int(key[1])]))
    return values


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


def to_fmpq(value: Q) -> fmpq:
    return fmpq(value.numerator, value.denominator)


def from_fmpq(value: fmpq) -> Q:
    return Q(int(value.numerator), int(value.denominator))


def exact_primal_dual() -> tuple[list[Q], list[Q], Q]:
    states, rows, objective, boundary = exact_system()
    state_index = {state: index for index, state in enumerate(states)}
    assert len(states) == 196
    assert len(DUAL_SUPPORT) == 62
    support_rows = [rows[state_index[state]] for state in DUAL_SUPPORT]

    # objective + D^T y - z boundary = 0.
    dual_matrix = fmpq_mat(
        [
            [to_fmpq(row[column]) for row in support_rows]
            + [to_fmpq(-boundary[column])]
            for column in range(len(KEYS))
        ]
    )
    dual_rhs = fmpq_mat([[-to_fmpq(value)] for value in objective])
    dual_solution = dual_matrix.solve(dual_rhs)
    y = [from_fmpq(dual_solution[index, 0]) for index in range(len(DUAL_SUPPORT))]
    z = from_fmpq(dual_solution[len(DUAL_SUPPORT), 0])
    assert all(value > 0 for value in y)

    for column in range(len(KEYS)):
        assert (
            objective[column]
            + sum(
                y[index] * support_rows[index][column]
                for index in range(len(DUAL_SUPPORT))
            )
            - z * boundary[column]
            == 0
        )

    # Complementary primal: equality on the positive dual support and unit
    # value at the full state.
    primal_matrix = fmpq_mat(
        [[to_fmpq(value) for value in row] for row in support_rows]
        + [[to_fmpq(value) for value in boundary]]
    )
    primal_rhs = fmpq_mat([[fmpq(0)] for _ in support_rows] + [[fmpq(1)]])
    primal_solution = primal_matrix.solve(primal_rhs)
    coefficients = [
        from_fmpq(primal_solution[index, 0]) for index in range(len(KEYS))
    ]
    assert sum(a * b for a, b in zip(boundary, coefficients)) == 1
    assert sum(a * b for a, b in zip(objective, coefficients)) == z

    drift_values = [
        sum(a * b for a, b in zip(row, coefficients)) for row in rows
    ]
    assert all(value <= 0 for value in drift_values)
    assert all(drift_values[state_index[state]] == 0 for state in DUAL_SUPPORT)

    values = [
        sum(a * b for a, b in zip(features(state), coefficients))
        for state in states
    ]
    assert all(value >= 0 for value in values)
    return y, coefficients, z


def decimal_string(value: Q, digits: int = 24) -> str:
    with localcontext() as context:
        context.prec = digits
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def main() -> None:
    y, coefficients, optimum = exact_primal_dual()
    baseline = Q(524_288, 1_114_095)
    gap = baseline - optimum
    assert gap > 0
    print("rank-dependent-conductance n=17 certificate: PASS")
    print("exact quotient drift rows checked: 196")
    print(f"restricted function-space dimension: {len(coefficients)}")
    print(f"strictly positive dual support weights: {len(y)}")
    print(f"exact restricted optimum: {decimal_string(optimum)}")
    print(f"K_17 baseline: {baseline}")
    print(f"strict exact margin below baseline: {decimal_string(gap)} > 0")


if __name__ == "__main__":
    main()
