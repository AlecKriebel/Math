#!/usr/bin/env python3
"""Exact refutation of the combined rank-``H,K_0`` certificate.

The potential space contains arbitrary rank constants, arbitrary
rank-labelled vertex coefficients, and independent coefficients of both
stationary internal conductance and ``s^T K_0 s`` on every rank.  A
twelve-vertex, five-class integer-weighted graph has restricted optimum
strictly above the complete ``K_12`` baseline.

The script reconstructs the dB quotient chain at r=2 from the update rule,
audits every quotient row against a separately labelled construction, and
checks matching rational primal and Farkas-dual solutions exactly.
It also reconstructs the exact Green occupation and proves that the best
static rankwise covariance tangent fails even though the full endpoint
residual is strictly positive.

This refutes only this compressed certificate.  It does not refute the
universal r=2 fixation bound or the full rank-pair certificate.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import sys

from flint import fmpq, fmpq_mat


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


CLASS_SIZES = (1, 1, 2, 3, 5)
N_VERTICES = sum(CLASS_SIZES)
CLASS_WEIGHTS = (
    (1_000, 5_000_000_000, 10_000, 30, 3),
    (5_000_000_000, 2_500, 350, 44, 1_200),
    (10_000, 350, 26_000, 4_800, 80_000_000),
    (30, 44, 4_800, 6_000_000, 30_000_000),
    (3, 1_200, 80_000_000, 30_000_000, 10_000_000),
)


DUAL_SUPPORT = (
    (0, 0, 0, 0, 1),
    (0, 0, 0, 0, 2),
    (0, 0, 0, 1, 0),
    (0, 0, 0, 1, 1),
    (0, 0, 0, 1, 5),
    (0, 0, 1, 0, 0),
    (0, 0, 1, 0, 1),
    (0, 0, 1, 0, 2),
    (0, 0, 1, 0, 3),
    (0, 0, 1, 1, 1),
    (0, 0, 1, 1, 2),
    (0, 0, 1, 1, 3),
    (0, 0, 1, 2, 2),
    (0, 0, 1, 2, 3),
    (0, 0, 1, 2, 4),
    (0, 0, 1, 3, 3),
    (0, 0, 1, 3, 4),
    (0, 0, 1, 3, 5),
    (0, 0, 2, 0, 0),
    (0, 0, 2, 0, 1),
    (0, 0, 2, 0, 2),
    (0, 0, 2, 0, 3),
    (0, 0, 2, 0, 4),
    (0, 0, 2, 1, 3),
    (0, 0, 2, 1, 4),
    (0, 0, 2, 2, 4),
    (0, 0, 2, 2, 5),
    (0, 0, 2, 3, 4),
    (0, 0, 2, 3, 5),
    (0, 1, 0, 0, 0),
    (0, 1, 0, 0, 1),
    (0, 1, 0, 0, 3),
    (0, 1, 0, 0, 5),
    (0, 1, 0, 2, 5),
    (0, 1, 1, 0, 1),
    (0, 1, 1, 1, 2),
    (0, 1, 1, 2, 3),
    (0, 1, 1, 3, 4),
    (0, 1, 2, 2, 5),
    (0, 1, 2, 3, 5),
    (1, 0, 0, 0, 0),
    (1, 0, 0, 0, 1),
    (1, 0, 0, 0, 3),
    (1, 0, 0, 0, 5),
    (1, 0, 0, 2, 5),
    (1, 0, 1, 0, 1),
    (1, 0, 1, 1, 2),
    (1, 0, 1, 2, 3),
    (1, 0, 1, 3, 4),
    (1, 0, 2, 2, 5),
    (1, 0, 2, 3, 5),
    (1, 1, 0, 0, 0),
    (1, 1, 0, 1, 0),
    (1, 1, 0, 1, 1),
    (1, 1, 0, 1, 5),
    (1, 1, 0, 2, 0),
    (1, 1, 0, 2, 1),
    (1, 1, 0, 3, 0),
    (1, 1, 0, 3, 1),
    (1, 1, 0, 3, 2),
    (1, 1, 0, 3, 3),
    (1, 1, 0, 3, 4),
    (1, 1, 0, 3, 5),
    (1, 1, 1, 0, 0),
    (1, 1, 1, 2, 5),
    (1, 1, 1, 3, 3),
    (1, 1, 1, 3, 4),
    (1, 1, 1, 3, 5),
    (1, 1, 2, 2, 5),
    (1, 1, 2, 3, 0),
    (1, 1, 2, 3, 1),
    (1, 1, 2, 3, 3),
    (1, 1, 2, 3, 4),
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


def internal_feature(state: tuple[int, ...]) -> Q:
    """Stationary internal conductance ``E_1``."""

    value = sum(
        Q(CLASS_WEIGHTS[a][a] * state[a] * (state[a] - 1), 2)
        for a in range(len(CLASS_SIZES))
    )
    value += sum(
        Q(CLASS_WEIGHTS[a][b] * state[a] * state[b])
        for a in range(len(CLASS_SIZES))
        for b in range(a + 1, len(CLASS_SIZES))
    )
    return value / TOTAL_DEGREE


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
        keys.extend((rank, vertex_class) for vertex_class in range(4))
        if 2 <= rank <= N_VERTICES - 2:
            keys.extend(((rank, "internal"), (rank, "collision")))
    keys.append((N_VERTICES, "constant"))
    assert len(keys) == 74
    return keys


KEYS = feature_keys()


def features(state: tuple[int, ...]) -> list[Q]:
    rank = sum(state)
    return [
        Q(0)
        if key[0] != rank
        else Q(1)
        if key[1] == "constant"
        else internal_feature(state)
        if key[1] == "internal"
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
        singleton = tuple(int(b == a) for b in range(len(CLASS_SIZES)))
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
    assert len(states) == 286 and len(DUAL_SUPPORT) == 73

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


def exact_fixation() -> Q:
    """Solve the independent 286-state quotient harmonic system exactly."""

    states = orbit_states()
    state_index = {state: j for j, state in enumerate(states)}
    dimension = len(states)
    rows = [[Q(0) for _ in range(dimension)] for _ in range(dimension)]
    rhs = [Q(0) for _ in range(dimension)]
    empty = (0,) * len(CLASS_SIZES)

    for state in states:
        row_index = state_index[state]
        gain, loss = orbit_rates(state)
        events = []
        total = Q(0)
        for a, size in enumerate(CLASS_SIZES):
            if state[a] < size:
                rate = (size - state[a]) * gain[a]
                target = list(state)
                target[a] += 1
                events.append((tuple(target), rate))
                total += rate
            if state[a]:
                rate = state[a] * loss[a]
                target = list(state)
                target[a] -= 1
                events.append((tuple(target), rate))
                total += rate
        rows[row_index][row_index] = total
        for target, rate in events:
            if target == CLASS_SIZES:
                rhs[row_index] += rate
            elif target != empty:
                rows[row_index][state_index[target]] -= rate

    matrix = fmpq_mat([
        [to_fmpq(value) for value in row] for row in rows
    ])
    vector = fmpq_mat([[to_fmpq(value)] for value in rhs])
    solution = matrix.solve(vector)

    fixation = Q(0)
    for a, size in enumerate(CLASS_SIZES):
        singleton = tuple(int(b == a) for b in range(len(CLASS_SIZES)))
        fixation += Q(size, N_VERTICES) * from_fmpq(
            solution[state_index[singleton], 0]
        )
    return fixation


def exact_green_schur_audit() -> tuple[Q, Q]:
    """Separate the static covariance bound from the true endpoint target.

    The first return value is the strongest lower-bound residual obtainable
    by optimizing the rankwise tangent

        D_k >= 2 theta_k C_k - theta_k^2 V_k,

    namely ``sum_k C_k^2/V_k + W - (2-kappa)C``.  The second is the true
    residual ``D+W-(2-kappa)C``.  All Green occupations and moments are
    reconstructed over the rationals from the update rule.
    """

    states = orbit_states()
    state_index = {state: j for j, state in enumerate(states)}
    dimension = len(states)
    rows = [[Q(0) for _ in range(dimension)] for _ in range(dimension)]
    source = [Q(0) for _ in range(dimension)]
    empty = (0,) * len(CLASS_SIZES)

    for state in states:
        row_index = state_index[state]
        if sum(state) == 1:
            mutant_class = next(a for a, count in enumerate(state) if count)
            source[row_index] = Q(CLASS_SIZES[mutant_class], N_VERTICES)
        gain, loss = orbit_rates(state)
        total = Q(0)
        for a, size in enumerate(CLASS_SIZES):
            if state[a] < size:
                rate = (size - state[a]) * gain[a]
                target = list(state)
                target[a] += 1
                target = tuple(target)
                total += rate
                if target != CLASS_SIZES:
                    rows[row_index][state_index[target]] -= rate
            if state[a]:
                rate = state[a] * loss[a]
                target = list(state)
                target[a] -= 1
                target = tuple(target)
                total += rate
                if target != empty:
                    rows[row_index][state_index[target]] -= rate
        rows[row_index][row_index] += total

    matrix = fmpq_mat([
        [to_fmpq(value) for value in row] for row in rows
    ])
    vector = fmpq_mat([[to_fmpq(value)] for value in source])
    green = matrix.transpose().solve(vector)
    occupation = [from_fmpq(green[j, 0]) for j in range(dimension)]
    assert all(value > 0 for value in occupation)

    variance = [Q(0) for _ in range(N_VERTICES + 1)]
    cut = [Q(0) for _ in range(N_VERTICES + 1)]
    prediction_error = [Q(0) for _ in range(N_VERTICES + 1)]
    nonlinear = [Q(0) for _ in range(N_VERTICES + 1)]

    for state, weight in zip(states, occupation):
        rank = sum(state)
        mutant_mass = sum(
            PI_PER_VERTEX[a] * state[a] for a in range(len(CLASS_SIZES))
        )
        state_cut = Q(0)
        state_collision = Q(0)
        state_nonlinear = Q(0)
        for a, size in enumerate(CLASS_SIZES):
            weighted_mutants = sum(
                CLASS_WEIGHTS[a][b] * state[b]
                for b in range(len(CLASS_SIZES))
            )
            if state[a]:
                x = Q(
                    weighted_mutants - CLASS_WEIGHTS[a][a], DEGREES[a]
                )
                count = state[a]
                state_cut += count * PI_PER_VERTEX[a] * (1 - x)
                state_collision += count * PI_PER_VERTEX[a] * x * (1 - x)
                state_nonlinear += (
                    count * PI_PER_VERTEX[a] * x * x * (1 - x) / (1 + x)
                )
            if state[a] < size:
                x = Q(weighted_mutants, DEGREES[a])
                count = size - state[a]
                state_collision += count * PI_PER_VERTEX[a] * x * (1 - x)
                state_nonlinear += (
                    count * PI_PER_VERTEX[a] * x * x * (1 - x) / (1 + x)
                )

        variance[rank] += weight * mutant_mass * (1 - mutant_mass)
        cut[rank] += weight * state_cut
        prediction_error[rank] += weight * (
            2 * state_cut - state_collision
        )
        nonlinear[rank] += weight * state_nonlinear

    for rank in range(1, N_VERTICES):
        assert variance[rank] > 0
        assert (
            variance[rank] * prediction_error[rank] - cut[rank] ** 2
            >= 0
        )

    kappa = Q(
        2 * ((N_VERTICES - 3) * 2 ** N_VERTICES + 4),
        (3 * N_VERTICES - 7) * 2 ** N_VERTICES + 8,
    )
    target_coefficient = 2 - kappa
    schur_residual = sum(
        cut[rank] ** 2 / variance[rank]
        for rank in range(1, N_VERTICES)
    ) + sum(nonlinear) - target_coefficient * sum(cut)
    target_residual = (
        sum(prediction_error)
        + sum(nonlinear)
        - target_coefficient * sum(cut)
    )
    return schur_residual, target_residual


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
    baseline = Q(2_816, 6_141)
    gap = optimum - baseline
    assert gap > 0
    fixation = exact_fixation()
    fixation_margin = baseline - fixation
    assert fixation_margin > 0
    schur_residual, target_residual = exact_green_schur_audit()
    assert schur_residual < 0 < target_residual
    print("combined rank-H,K0 Farkas refutation: PASS")
    print("graph: n=12, class sizes=(1,1,2,3,5), complete positive support")
    print("exact labelled/quotient drift rows checked: 286")
    print(f"restricted function-space dimension: {len(coefficients)}")
    print(f"strictly positive dual support weights: {len(y)}")
    print(f"exact restricted optimum: {decimal_string(optimum)}")
    print(f"K_12 baseline: {baseline}")
    print(f"strict exact excess: {decimal_string(gap)} > 0")
    print(
        "excess digits/hash: "
        f"{len(str(abs(gap.numerator)))}/{len(str(gap.denominator))}, "
        f"{digest(gap)}"
    )
    print(f"exact true fixation: {decimal_string(fixation)}")
    print(
        "true suppression margin: "
        f"{decimal_string(fixation_margin)} > 0, {digest(fixation_margin)}"
    )
    print(
        "optimized rankwise covariance residual: "
        f"{decimal_string(schur_residual)} < 0, {digest(schur_residual)}"
    )
    print(
        "exact full target residual: "
        f"{decimal_string(target_residual)} > 0, {digest(target_residual)}"
    )


if __name__ == "__main__":
    main()
