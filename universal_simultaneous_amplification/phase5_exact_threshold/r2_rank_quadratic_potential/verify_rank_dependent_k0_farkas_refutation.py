#!/usr/bin/env python3
"""Exact refutation of the rank-dependent-``K_0`` certificate.

The potential space contains arbitrary rank constants, arbitrary
rank-labelled vertex coefficients, and one independent coefficient of
``s^T K_0 s`` on every nontrivial rank, where
``K_0=Pi-P^T Pi P``.  A nine-vertex, five-class integer-weighted graph has
a restricted optimum strictly above the complete ``K_9`` baseline.

The script rebuilds the dB quotient chain at r=2 from the update rule,
audits every quotient row against a separately labelled construction, and
checks matching rational primal and Farkas-dual solutions exactly.

This refutes only this compressed certificate.  It does not refute the
universal r=2 fixation bound or the larger rank-H plus rank-K0 certificate.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product

from flint import fmpq, fmpq_mat


CLASS_SIZES = (1, 1, 2, 2, 3)
N_VERTICES = sum(CLASS_SIZES)
CLASS_WEIGHTS = (
    (1_000_000, 300_000_000_000, 70_000_000_000, 400_000, 30_000_000),
    (300_000_000_000, 10, 400_000, 50_000_000_000, 5),
    (70_000_000_000, 400_000, 3_000_000, 1_100_000, 90_000_000_000),
    (400_000, 50_000_000_000, 1_100_000, 170_000_000_000, 50_000_000_000),
    (30_000_000, 5, 90_000_000_000, 50_000_000_000, 36_000_000_000),
)


DUAL_SUPPORT = (
    (0, 0, 0, 0, 1),
    (0, 0, 0, 0, 2),
    (0, 0, 0, 0, 3),
    (0, 0, 0, 1, 0),
    (0, 0, 0, 2, 0),
    (0, 0, 0, 2, 1),
    (0, 0, 0, 2, 2),
    (0, 0, 1, 0, 0),
    (0, 0, 1, 0, 1),
    (0, 0, 1, 0, 2),
    (0, 0, 1, 2, 1),
    (0, 0, 1, 2, 2),
    (0, 0, 1, 2, 3),
    (0, 0, 2, 0, 0),
    (0, 0, 2, 0, 1),
    (0, 0, 2, 0, 2),
    (0, 0, 2, 0, 3),
    (0, 0, 2, 2, 3),
    (0, 1, 0, 0, 0),
    (0, 1, 0, 2, 1),
    (0, 1, 2, 0, 0),
    (0, 1, 2, 2, 2),
    (0, 1, 2, 2, 3),
    (1, 0, 0, 0, 0),
    (1, 0, 1, 0, 0),
    (1, 0, 2, 0, 2),
    (1, 0, 2, 0, 3),
    (1, 0, 2, 2, 3),
    (1, 1, 0, 0, 0),
    (1, 1, 0, 2, 0),
    (1, 1, 0, 2, 1),
    (1, 1, 0, 2, 2),
    (1, 1, 0, 2, 3),
    (1, 1, 1, 0, 0),
    (1, 1, 1, 0, 1),
    (1, 1, 1, 2, 0),
    (1, 1, 1, 2, 1),
    (1, 1, 1, 2, 2),
    (1, 1, 1, 2, 3),
    (1, 1, 2, 0, 1),
    (1, 1, 2, 0, 2),
    (1, 1, 2, 0, 3),
    (1, 1, 2, 1, 3),
    (1, 1, 2, 2, 0),
    (1, 1, 2, 2, 1),
    (1, 1, 2, 2, 2),
)


def orbit_states() -> list[tuple[int, ...]]:
    return [
        state
        for state in product(*(range(size + 1) for size in CLASS_SIZES))
        if state not in ((0,) * len(CLASS_SIZES), CLASS_SIZES)
    ]


def class_degrees() -> tuple[int, ...]:
    return tuple(
        (CLASS_SIZES[a] - 1) * CLASS_WEIGHTS[a][a]
        + sum(
            CLASS_SIZES[b] * CLASS_WEIGHTS[a][b]
            for b in range(len(CLASS_SIZES))
            if b != a
        )
        for a in range(len(CLASS_SIZES))
    )


DEGREES = class_degrees()
TOTAL_DEGREE = sum(
    size * degree for size, degree in zip(CLASS_SIZES, DEGREES)
)
PI_PER_VERTEX = tuple(Q(degree, TOTAL_DEGREE) for degree in DEGREES)


def orbit_rates(state: tuple[int, ...]) -> tuple[list[Q], list[Q]]:
    """Per-vertex type-change rates, omitting the common death factor 1/n."""

    gain = []
    loss = []
    for a, size in enumerate(CLASS_SIZES):
        weighted_mutants = sum(
            CLASS_WEIGHTS[a][b] * state[b]
            for b in range(len(CLASS_SIZES))
        )
        if state[a] < size:
            x_out = Q(weighted_mutants, DEGREES[a])
            gain.append(2 * x_out / (1 + x_out))
        else:
            gain.append(Q(0))
        if state[a]:
            x_in = Q(
                weighted_mutants - CLASS_WEIGHTS[a][a], DEGREES[a]
            )
            loss.append((1 - x_in) / (1 + x_in))
        else:
            loss.append(Q(0))
    return gain, loss


def collision_feature(state: tuple[int, ...]) -> Q:
    """Evaluate ``s^T K_0 s=sum_v pi_v x_v(1-x_v)`` exactly."""

    value = Q(0)
    for a, size in enumerate(CLASS_SIZES):
        weighted_mutants = sum(
            CLASS_WEIGHTS[a][b] * state[b]
            for b in range(len(CLASS_SIZES))
        )
        mutant_count = state[a]
        if mutant_count:
            x_in = Q(
                weighted_mutants - CLASS_WEIGHTS[a][a], DEGREES[a]
            )
            value += (
                mutant_count
                * PI_PER_VERTEX[a]
                * x_in
                * (1 - x_in)
            )
        if mutant_count < size:
            x_out = Q(weighted_mutants, DEGREES[a])
            value += (
                (size - mutant_count)
                * PI_PER_VERTEX[a]
                * x_out
                * (1 - x_out)
            )
    return value


def feature_keys() -> list[tuple[object, ...]]:
    keys: list[tuple[object, ...]] = []
    for rank in range(1, N_VERTICES):
        keys.append((rank, "constant"))
        # Four class counts span all rank-slice one-mark functions because
        # the fifth is fixed by the rank.
        keys.extend((rank, vertex_class) for vertex_class in range(4))
        if 2 <= rank <= N_VERTICES - 2:
            keys.append((rank, "collision"))
    keys.append((N_VERTICES, "constant"))
    assert len(keys) == 47
    return keys


KEYS = feature_keys()


def features(state: tuple[int, ...]) -> list[Q]:
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
    list[tuple[int, ...]], list[list[Q]], list[Q], list[Q]
]:
    states = orbit_states()
    empty = (0,) * len(CLASS_SIZES)
    cache = {state: features(state) for state in states + [empty, CLASS_SIZES]}
    rows = []
    for state in states:
        gain, loss = orbit_rates(state)
        row = [Q(0) for _ in KEYS]
        total = Q(0)
        for a, size in enumerate(CLASS_SIZES):
            if state[a] < size:
                rate = (size - state[a]) * gain[a]
                target = list(state)
                target[a] += 1
                total += rate
                row = [
                    old + rate * (new - current)
                    for old, new, current in zip(
                        row, cache[tuple(target)], cache[state]
                    )
                ]
            if state[a]:
                rate = state[a] * loss[a]
                target = list(state)
                target[a] -= 1
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
    for a, size in enumerate(CLASS_SIZES):
        singleton = tuple(
            int(b == a) for b in range(len(CLASS_SIZES))
        )
        objective = [
            old + Q(size, N_VERTICES) * value
            for old, value in zip(objective, cache[singleton])
        ]
    return states, rows, objective, cache[CLASS_SIZES]


def labelled_row_audit(states: list[tuple[int, ...]], rows: list[list[Q]]) -> None:
    """Rebuild all transition rows from an explicitly labelled kernel."""

    labels = []
    vertices_by_class = []
    start = 0
    for a, size in enumerate(CLASS_SIZES):
        vertices = tuple(range(start, start + size))
        start += size
        vertices_by_class.append(vertices)
        labels.extend([a] * size)

    kernel = [[Q(0) for _ in range(N_VERTICES)] for _ in range(N_VERTICES)]
    for v in range(N_VERTICES):
        for i in range(N_VERTICES):
            if i != v:
                kernel[v][i] = Q(
                    CLASS_WEIGHTS[labels[v]][labels[i]], DEGREES[labels[v]]
                )
        assert sum(kernel[v], Q(0)) == 1

    empty = (0,) * len(CLASS_SIZES)
    cache = {state: features(state) for state in states + [empty, CLASS_SIZES]}
    for state, quotient_row in zip(states, rows):
        selected = {
            vertex
            for a, count in enumerate(state)
            for vertex in vertices_by_class[a][:count]
        }
        row = [Q(0) for _ in KEYS]
        total = Q(0)
        for v in range(N_VERTICES):
            x = sum((kernel[v][i] for i in selected), Q(0))
            if v in selected:
                rate = (1 - x) / (1 + x)
                target = list(state)
                target[labels[v]] -= 1
            else:
                rate = 2 * x / (1 + x)
                target = list(state)
                target[labels[v]] += 1
            total += rate
            row = [
                old + rate * (new - current)
                for old, new, current in zip(
                    row, cache[tuple(target)], cache[state]
                )
            ]
        assert [value / total for value in row] == quotient_row


def to_fmpq(value: Q) -> fmpq:
    return fmpq(value.numerator, value.denominator)


def from_fmpq(value: fmpq) -> Q:
    return Q(int(value.numerator), int(value.denominator))


def exact_primal_dual() -> tuple[list[Q], list[Q], Q]:
    states, rows, objective, boundary = exact_system()
    state_index = {state: j for j, state in enumerate(states)}
    support_rows = [rows[state_index[state]] for state in DUAL_SUPPORT]
    assert len(states) == 142 and len(DUAL_SUPPORT) == 46

    dual_matrix = fmpq_mat([
        [to_fmpq(row[column]) for row in support_rows]
        + [to_fmpq(-boundary[column])]
        for column in range(len(KEYS))
    ])
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


def decimal_string(value: Q, digits: int = 25) -> str:
    with localcontext() as context:
        context.prec = digits
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def digest(value: Q) -> str:
    return sha256(f"{value.numerator}/{value.denominator}".encode()).hexdigest()


def main() -> None:
    assert CLASS_WEIGHTS == tuple(zip(*CLASS_WEIGHTS))
    states, rows, _, _ = exact_system()
    labelled_row_audit(states, rows)
    y, coefficients, optimum = exact_primal_dual()
    baseline = Q(1024, 2295)
    gap = optimum - baseline
    assert gap > 0
    print("rank-dependent-K0 Farkas refutation: PASS")
    print("graph: n=9, class sizes=(1,1,2,2,3), complete positive support")
    print("exact labelled/quotient drift rows checked: 142")
    print(f"restricted function-space dimension: {len(coefficients)}")
    print(f"strictly positive dual support weights: {len(y)}")
    print(f"exact restricted optimum: {decimal_string(optimum)}")
    print(f"K_9 baseline: {baseline}")
    print(f"strict exact excess: {decimal_string(gap)} > 0")
    print(
        "excess digits/hash: "
        f"{len(str(abs(gap.numerator)))}/{len(str(gap.denominator))}, "
        f"{digest(gap)}"
    )


if __name__ == "__main__":
    main()
