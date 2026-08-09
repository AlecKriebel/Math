#!/usr/bin/env python3
"""Exact refutation of the single-global-conductance r=2 certificate.

The tested fixation-potential space consists of arbitrary rank constants,
arbitrary rank-labelled vertex coefficients, and one global coefficient of
the reversible internal conductance.  The graph is the complete-support
17-vertex, three-class integer-weighted graph from the additive Farkas
audit.  Within-class symmetrization reduces the system exactly to 196 state
orbits and 50 independent function columns.

The script constructs the drift rows directly from the dB rule over
``Fraction`` arithmetic.  A 49-state exact dual ray proves that the least
uniform-singleton boundary value in this function space is strictly larger
than the complete-graph fixation probability.  An exact matching primal
potential is also reconstructed and every one of its 196 inequalities is
checked.  This refutes only this restricted certificate, not the universal
fitness-two fixation inequality.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product

from flint import fmpq, fmpq_mat


CLASS_SIZES = (2, 5, 10)
N_VERTICES = sum(CLASS_SIZES)
CLASS_WEIGHTS = (
    (20_000_000, 15, 5),
    (15, 9, 4_500),
    (5, 4_500, 150),
)

# The positive support selected by the floating discovery LP.  Everything
# after this declaration is exact and does not import that LP.
DUAL_SUPPORT = (
    (0, 0, 1),
    (0, 1, 0),
    (0, 1, 1),
    (0, 2, 0),
    (0, 2, 1),
    (0, 3, 0),
    (0, 3, 1),
    (0, 3, 2),
    (0, 3, 5),
    (0, 3, 6),
    (0, 3, 7),
    (0, 3, 8),
    (0, 3, 9),
    (0, 4, 2),
    (0, 4, 3),
    (0, 4, 4),
    (0, 4, 5),
    (0, 4, 6),
    (0, 4, 7),
    (0, 4, 8),
    (0, 4, 9),
    (0, 4, 10),
    (0, 5, 8),
    (0, 5, 9),
    (0, 5, 10),
    (1, 0, 0),
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
    (2, 1, 8),
    (2, 1, 9),
    (2, 2, 0),
    (2, 3, 0),
    (2, 3, 8),
    (2, 3, 9),
    (2, 3, 10),
    (2, 4, 0),
    (2, 4, 7),
    (2, 4, 9),
    (2, 4, 10),
    (2, 5, 0),
    (2, 5, 9),
)


def orbit_states() -> list[tuple[int, int, int]]:
    return [
        state
        for state in product(*(range(size + 1) for size in CLASS_SIZES))
        if state not in ((0, 0, 0), CLASS_SIZES)
    ]


def class_degrees() -> tuple[int, int, int]:
    answer = []
    for vertex_class, size in enumerate(CLASS_SIZES):
        degree = (size - 1) * CLASS_WEIGHTS[vertex_class][vertex_class]
        degree += sum(
            CLASS_SIZES[other] * CLASS_WEIGHTS[vertex_class][other]
            for other in range(len(CLASS_SIZES))
            if other != vertex_class
        )
        answer.append(degree)
    return tuple(answer)  # type: ignore[return-value]


def orbit_rates(
    state: tuple[int, int, int],
) -> tuple[list[Q], list[Q]]:
    """Return per-vertex gain/loss rates for each class."""

    gain: list[Q] = []
    loss: list[Q] = []
    degrees = class_degrees()
    for vertex_class, size in enumerate(CLASS_SIZES):
        weighted_mutants = sum(
            CLASS_WEIGHTS[vertex_class][other] * state[other]
            for other in range(len(CLASS_SIZES))
        )
        if state[vertex_class] < size:
            x_out = Q(weighted_mutants, degrees[vertex_class])
            gain.append(2 * x_out / (1 + x_out))
        else:
            gain.append(Q(0))
        if state[vertex_class] > 0:
            x_in = Q(
                weighted_mutants
                - CLASS_WEIGHTS[vertex_class][vertex_class],
                degrees[vertex_class],
            )
            loss.append((1 - x_in) / (1 + x_in))
        else:
            loss.append(Q(0))
    return gain, loss


def feature_keys() -> list[tuple[object, ...]]:
    """A nonredundant basis of the invariant restricted potential space."""

    keys: list[tuple[object, ...]] = []
    for rank in range(1, N_VERTICES):
        # On a fixed rank, s_3=rank-s_1-s_2.  Thus a constant plus the first
        # two class counts spans every invariant rank-labelled linear field.
        keys.extend(((rank, "constant"), (rank, 0), (rank, 1)))
    # The full slice has one state, so only its constant is needed.
    keys.append((N_VERTICES, "constant"))
    # One coefficient shared by internal conductance on every rank.
    keys.append(("internal",))
    assert len(keys) == 50
    return keys


KEYS = feature_keys()


def internal_feature(state: tuple[int, int, int]) -> Q:
    """Internal edge weight; scaling is immaterial for a free coefficient."""

    value = sum(
        Q(CLASS_WEIGHTS[a][a] * state[a] * (state[a] - 1), 2)
        for a in range(len(CLASS_SIZES))
    )
    value += sum(
        Q(CLASS_WEIGHTS[a][b] * state[a] * state[b])
        for a in range(len(CLASS_SIZES))
        for b in range(a + 1, len(CLASS_SIZES))
    )
    # This keeps the exact matrices smaller.  It spans precisely the same
    # one-dimensional column as stationary internal conductance.
    return value / 20_000_000


def features(state: tuple[int, int, int]) -> list[Q]:
    rank = sum(state)
    values = []
    for key in KEYS:
        if key == ("internal",):
            values.append(internal_feature(state))
        elif key[0] != rank:
            values.append(Q(0))
        elif key[1] == "constant":
            values.append(Q(1))
        else:
            values.append(Q(state[int(key[1])]))
    return values


def exact_system() -> tuple[
    list[tuple[int, int, int]], list[list[Q]], list[Q], list[Q]
]:
    """Return normalized drift rows, singleton objective, and full boundary."""

    states = orbit_states()
    empty = (0, 0, 0)
    all_states = states + [empty, CLASS_SIZES]
    feature_cache = {state: features(state) for state in all_states}
    drift_rows = []
    for state in states:
        gain, loss = orbit_rates(state)
        row = [Q(0) for _ in KEYS]
        total_rate = Q(0)
        for vertex_class, size in enumerate(CLASS_SIZES):
            count = state[vertex_class]
            if count < size:
                rate = (size - count) * gain[vertex_class]
                target = list(state)
                target[vertex_class] += 1
                target_tuple = tuple(target)
                total_rate += rate
                row = [
                    old + rate * (new - current)
                    for old, new, current in zip(
                        row, feature_cache[target_tuple], feature_cache[state]
                    )
                ]
            if count > 0:
                rate = count * loss[vertex_class]
                target = list(state)
                target[vertex_class] -= 1
                target_tuple = tuple(target)
                total_rate += rate
                row = [
                    old + rate * (new - current)
                    for old, new, current in zip(
                        row, feature_cache[target_tuple], feature_cache[state]
                    )
                ]
        assert total_rate > 0
        drift_rows.append([value / total_rate for value in row])

    objective = [Q(0) for _ in KEYS]
    for vertex_class, size in enumerate(CLASS_SIZES):
        singleton = tuple(
            1 if other == vertex_class else 0
            for other in range(len(CLASS_SIZES))
        )
        objective = [
            old + Q(size, N_VERTICES) * value
            for old, value in zip(objective, feature_cache[singleton])
        ]
    return states, drift_rows, objective, feature_cache[CLASS_SIZES]


def labelled_row_audit(
    states: list[tuple[int, int, int]], drift_rows: list[list[Q]]
) -> None:
    """Rebuild all quotient drifts from the labelled 17-vertex graph."""

    labels = []
    vertices_by_class = []
    start = 0
    for vertex_class, size in enumerate(CLASS_SIZES):
        vertices = tuple(range(start, start + size))
        start += size
        vertices_by_class.append(vertices)
        labels.extend([vertex_class] * size)
    degrees = class_degrees()
    replacement = [[Q(0) for _ in range(N_VERTICES)] for _ in range(N_VERTICES)]
    for v in range(N_VERTICES):
        for i in range(N_VERTICES):
            if i != v:
                replacement[v][i] = Q(
                    CLASS_WEIGHTS[labels[v]][labels[i]], degrees[labels[v]]
                )
        assert sum(replacement[v], Q(0)) == 1

    feature_cache = {
        state: features(state)
        for state in states + [(0, 0, 0), CLASS_SIZES]
    }
    for state, quotient_row in zip(states, drift_rows):
        selected = {
            vertex
            for vertex_class, count in enumerate(state)
            for vertex in vertices_by_class[vertex_class][:count]
        }
        row = [Q(0) for _ in KEYS]
        total_rate = Q(0)
        for vertex in range(N_VERTICES):
            x = sum(
                (replacement[vertex][i] for i in selected),
                Q(0),
            )
            if vertex in selected:
                rate = (1 - x) / (1 + x)
                target = list(state)
                target[labels[vertex]] -= 1
            else:
                rate = 2 * x / (1 + x)
                target = list(state)
                target[labels[vertex]] += 1
            if rate:
                target_tuple = tuple(target)
                total_rate += rate
                row = [
                    old + rate * (new - current)
                    for old, new, current in zip(
                        row, feature_cache[target_tuple], feature_cache[state]
                    )
                ]
        assert [value / total_rate for value in row] == quotient_row


def to_fmpq(value: Q) -> fmpq:
    return fmpq(value.numerator, value.denominator)


def from_fmpq(value: fmpq) -> Q:
    return Q(int(value.numerator), int(value.denominator))


def exact_primal_dual() -> tuple[list[Q], list[Q], Q]:
    states, drift_rows, objective, boundary = exact_system()
    state_index = {state: index for index, state in enumerate(states)}
    assert len(states) == 196
    assert len(DUAL_SUPPORT) == 49
    assert len(set(DUAL_SUPPORT)) == len(DUAL_SUPPORT)
    assert all(state in state_index for state in DUAL_SUPPORT)
    support_rows = [drift_rows[state_index[state]] for state in DUAL_SUPPORT]

    # Dual stationarity is
    #     objective + D^T y - z boundary = 0,
    # with y>=0.  There are 50 equations for the 49 support weights and z.
    dual_matrix = fmpq_mat(
        [
            [to_fmpq(row[column]) for row in support_rows]
            + [to_fmpq(-boundary[column])]
            for column in range(len(KEYS))
        ]
    )
    dual_rhs = fmpq_mat([[to_fmpq(-value)] for value in objective])
    dual_solution = dual_matrix.solve(dual_rhs)
    y = [from_fmpq(dual_solution[index, 0]) for index in range(len(DUAL_SUPPORT))]
    z = from_fmpq(dual_solution[len(DUAL_SUPPORT), 0])
    assert all(value > 0 for value in y)

    # Independent exact substitution in every dual column.
    for column in range(len(KEYS)):
        residual = objective[column]
        residual += sum(
            (support_rows[index][column] * y[index]
             for index in range(len(DUAL_SUPPORT))),
            Q(0),
        )
        residual -= z * boundary[column]
        assert residual == 0

    # The complementary primal has equality at every supported drift row.
    primal_matrix = fmpq_mat(
        [[to_fmpq(value) for value in row] for row in support_rows]
        + [[to_fmpq(value) for value in boundary]]
    )
    primal_rhs = fmpq_mat(
        [[fmpq(0)] for _ in DUAL_SUPPORT] + [[fmpq(1)]]
    )
    primal_solution = primal_matrix.solve(primal_rhs)
    coefficients = [
        from_fmpq(primal_solution[index, 0]) for index in range(len(KEYS))
    ]
    assert sum(a * b for a, b in zip(boundary, coefficients)) == 1
    primal_objective = sum(a * b for a, b in zip(objective, coefficients))
    assert primal_objective == z

    # Check all 196 inequalities, not only the active support.
    drift_values = [
        sum(a * b for a, b in zip(row, coefficients))
        for row in drift_rows
    ]
    assert all(value <= 0 for value in drift_values)
    assert all(drift_values[state_index[state]] == 0 for state in DUAL_SUPPORT)

    # The maximum principle predicts nonnegativity; verify it directly as an
    # additional independent check of the reconstructed optimum.
    values = [
        sum(a * b for a, b in zip(features(state), coefficients))
        for state in states
    ]
    assert all(value >= 0 for value in values)
    return y, coefficients, z


def decimal_string(value: Q, digits: int = 22) -> str:
    with localcontext() as context:
        context.prec = digits
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def rational_digest(value: Q) -> str:
    return sha256(f"{value.numerator}/{value.denominator}".encode()).hexdigest()


def main() -> None:
    assert CLASS_WEIGHTS == tuple(zip(*CLASS_WEIGHTS))
    assert class_degrees() == (20_000_125, 45_066, 23_860)
    states, drift_rows, _, _ = exact_system()
    labelled_row_audit(states, drift_rows)
    y, coefficients, optimum = exact_primal_dual()
    baseline = Q(524_288, 1_114_095)
    gap = optimum - baseline
    assert gap > 0

    print("single-global-conductance Farkas refutation: PASS")
    print("graph: n=17, class sizes=(2,5,10), complete positive support")
    print("exact labelled/quotient drift rows checked: 196")
    print(f"restricted function-space dimension: {len(coefficients)}")
    print(f"strictly positive dual support weights: {len(y)}")
    print(f"exact restricted optimum: {decimal_string(optimum)}")
    print(f"K_17 baseline: {baseline}")
    print(f"strict exact excess: {decimal_string(gap)} > 0")
    print(
        "excess digits/hash: "
        f"{len(str(abs(gap.numerator)))}/{len(str(gap.denominator))}, "
        f"{rational_digest(gap)}"
    )


if __name__ == "__main__":
    main()
