#!/usr/bin/env python3
"""Exact Farkas refutation of a rank-dependent additive dB potential.

The proposed fitness-two ansatz is

    G(S) = 1 + |S|/n + sum_{v in S} a_{|S|,v},

with no correction at ranks zero and n, and with the singleton boundary
condition ``sum_v a_{1,v}=0``.  This script constructs a complete-support
17-vertex rational weighted graph, derives the scaled dB drift inequalities
directly from the update rule, and proves exact infeasibility by a positive
Farkas ray on 48 state orbits.

Every quotient row is independently reconstructed from the labelled graph.
The script then uses python-flint to solve the separate 196-state lumped dB
fixation system exactly.  The witness graph is dB-suppressing at fitness two;
it refutes only this potential ansatz, not the universal fixation inequality.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product

from flint import fmpq, fmpq_mat
from sympy import Rational
from sympy.polys.matrices import DomainMatrix


CLASS_SIZES = (2, 5, 10)
N_VERTICES = sum(CLASS_SIZES)
CLASS_WEIGHTS = (
    (20_000_000, 15, 5),
    (15, 9, 4_500),
    (5, 4_500, 150),
)

# The support discovered numerically is embedded here so that the exact
# certificate has no dependency on a solver output or a temporary file.
DUAL_SUPPORT = (
    (0, 0, 1), (0, 0, 10), (0, 1, 0), (0, 1, 1), (0, 2, 0),
    (0, 3, 0), (0, 3, 1), (0, 3, 2), (0, 3, 3), (0, 3, 8),
    (0, 3, 9), (0, 4, 3), (0, 4, 4), (0, 4, 6), (0, 4, 7),
    (0, 4, 8), (0, 4, 9), (0, 4, 10), (0, 5, 4), (0, 5, 5),
    (0, 5, 8), (0, 5, 9), (0, 5, 10), (1, 0, 0), (1, 5, 10),
    (2, 0, 0), (2, 0, 1), (2, 0, 2), (2, 0, 3), (2, 0, 4),
    (2, 0, 5), (2, 0, 6), (2, 0, 7), (2, 0, 8), (2, 0, 9),
    (2, 0, 10), (2, 1, 2), (2, 1, 10), (2, 2, 0), (2, 2, 10),
    (2, 3, 10), (2, 4, 0), (2, 4, 9), (2, 4, 10), (2, 5, 0),
    (2, 5, 1), (2, 5, 2), (2, 5, 9),
)


def orbit_states() -> list[tuple[int, int, int]]:
    """All transient state orbits under S_2 x S_5 x S_10."""

    return [
        state
        for state in product(*(range(size + 1) for size in CLASS_SIZES))
        if state not in ((0, 0, 0), CLASS_SIZES)
    ]


def variable_types() -> list[tuple[int, int]]:
    """The 48 invariant variables (rank, vertex class)."""

    return [
        (rank, vertex_class)
        for rank in range(1, N_VERTICES)
        for vertex_class in range(len(CLASS_SIZES))
    ]


def class_degrees() -> tuple[int, int, int]:
    degrees = []
    for vertex_class, size in enumerate(CLASS_SIZES):
        degree = (size - 1) * CLASS_WEIGHTS[vertex_class][vertex_class]
        degree += sum(
            CLASS_SIZES[other] * CLASS_WEIGHTS[vertex_class][other]
            for other in range(len(CLASS_SIZES))
            if other != vertex_class
        )
        degrees.append(degree)
    return tuple(degrees)  # type: ignore[return-value]


def orbit_rates(
    state: tuple[int, int, int],
) -> tuple[list[Q], list[Q], Q, Q]:
    """Return class gain/loss rates and their outside/inside sums.

    For a death in class c, ``gain[c]`` is the probability that a resident
    vacancy is filled by a mutant, while ``loss[c]`` is the probability that
    a mutant vacancy is filled by a resident.  Mutant fitness is two.
    """

    degrees = class_degrees()
    gain: list[Q] = []
    loss: list[Q] = []
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
            weighted_mutants_in = (
                weighted_mutants
                - CLASS_WEIGHTS[vertex_class][vertex_class]
            )
            x_in = Q(weighted_mutants_in, degrees[vertex_class])
            loss.append((1 - x_in) / (1 + x_in))
        else:
            loss.append(Q(0))

    gain_out = sum(
        ((size - count) * value
         for size, count, value in zip(CLASS_SIZES, state, gain)),
        Q(0),
    )
    loss_in = sum(
        ((count * value for count, value in zip(state, loss))),
        Q(0),
    )
    return gain, loss, gain_out, loss_in


def reduced_drift_row(
    state: tuple[int, int, int],
) -> tuple[list[Q], Q]:
    """Build the exact invariant drift row supplied by the update rule."""

    gain, loss, gain_out, loss_in = orbit_rates(state)
    rank = sum(state)
    constant = (
        -Q(N_VERTICES + rank - 1, N_VERTICES) * gain_out
        + Q(2 * (N_VERTICES + rank - 2), N_VERTICES) * loss_in
    )

    row = []
    for variable_rank, vertex_class in variable_types():
        count = state[vertex_class]
        if variable_rank == rank:
            value = -2 * (gain_out + loss_in) * count
        elif variable_rank == rank + 1:
            value = (
                count * gain_out
                + (CLASS_SIZES[vertex_class] - count) * gain[vertex_class]
            )
        elif variable_rank == rank - 1:
            value = 4 * count * (loss_in - loss[vertex_class])
        else:
            value = Q(0)
        row.append(value)
    return row, constant


def reduced_system() -> tuple[
    list[tuple[int, int, int]], list[list[Q]], list[Q], list[Q]
]:
    states = orbit_states()
    rows = []
    constants = []
    for state in states:
        row, constant = reduced_drift_row(state)
        rows.append(row)
        constants.append(constant)
    boundary = [
        Q(CLASS_SIZES[vertex_class]) if rank == 1 else Q(0)
        for rank, vertex_class in variable_types()
    ]
    return states, rows, constants, boundary


def labelled_graph() -> tuple[
    tuple[int, ...], list[list[Q]], list[tuple[int, ...]]
]:
    """Return class labels, the row-stochastic kernel, and class vertices."""

    labels = []
    vertices_by_class = []
    first = 0
    for vertex_class, size in enumerate(CLASS_SIZES):
        vertices = tuple(range(first, first + size))
        vertices_by_class.append(vertices)
        labels.extend([vertex_class] * size)
        first += size

    weights = [[Q(0) for _ in range(N_VERTICES)] for _ in range(N_VERTICES)]
    for source in range(N_VERTICES):
        for target in range(N_VERTICES):
            if source != target:
                weights[source][target] = Q(
                    CLASS_WEIGHTS[labels[source]][labels[target]]
                )
    replacement = []
    for source, row in enumerate(weights):
        degree = sum(row, Q(0))
        assert degree == class_degrees()[labels[source]]
        normalized = [weight / degree for weight in row]
        assert normalized[source] == 0
        assert sum(normalized, Q(0)) == 1
        replacement.append(normalized)
    return tuple(labels), replacement, vertices_by_class


def labelled_row_audit() -> None:
    """Reconstruct every one of the 196 quotient rows from 17 labels."""

    labels, replacement, vertices_by_class = labelled_graph()
    for state in orbit_states():
        selected = {
            vertex
            for vertex_class, count in enumerate(state)
            for vertex in vertices_by_class[vertex_class][:count]
        }
        rank = len(selected)
        x = [
            sum((replacement[v][u] for u in selected), Q(0))
            for v in range(N_VERTICES)
        ]
        gain = [2 * value / (1 + value) for value in x]
        loss = [(1 - value) / (1 + value) for value in x]
        gain_out = sum(
            (gain[v] for v in range(N_VERTICES) if v not in selected), Q(0)
        )
        loss_in = sum((loss[v] for v in selected), Q(0))
        labelled_constant = (
            -Q(N_VERTICES + rank - 1, N_VERTICES) * gain_out
            + Q(2 * (N_VERTICES + rank - 2), N_VERTICES) * loss_in
        )

        quotient_row, quotient_constant = reduced_drift_row(state)
        assert labelled_constant == quotient_constant
        aggregated = []
        for variable_rank, vertex_class in variable_types():
            value = Q(0)
            for vertex in vertices_by_class[vertex_class]:
                if variable_rank == rank and vertex in selected:
                    value += -2 * (gain_out + loss_in)
                elif variable_rank == rank + 1:
                    value += gain_out if vertex in selected else gain[vertex]
                elif variable_rank == rank - 1 and vertex in selected:
                    value += 4 * (loss_in - loss[vertex])
            aggregated.append(value)
        assert aggregated == quotient_row

        class_gain, class_loss, class_gain_out, class_loss_in = orbit_rates(state)
        assert class_gain_out == gain_out
        assert class_loss_in == loss_in
        for vertex_class, vertices in enumerate(vertices_by_class):
            outside = [v for v in vertices if v not in selected]
            inside = [v for v in vertices if v in selected]
            if outside:
                assert all(gain[v] == class_gain[vertex_class] for v in outside)
            if inside:
                assert all(loss[v] == class_loss[vertex_class] for v in inside)


def to_sympy(value: Q) -> Rational:
    return Rational(value.numerator, value.denominator)


def from_sympy(value: object) -> Q:
    numerator, denominator = value.as_numer_denom()  # type: ignore[attr-defined]
    return Q(int(numerator), int(denominator))


def exact_farkas_ray() -> tuple[list[Q], Q]:
    """Solve the 48-by-49 exact dual balance system and certify its sign."""

    states, rows, constants, boundary = reduced_system()
    state_index = {state: index for index, state in enumerate(states)}
    assert len(DUAL_SUPPORT) == len(variable_types()) == 48
    assert len(set(DUAL_SUPPORT)) == len(DUAL_SUPPORT)
    assert all(state in state_index for state in DUAL_SUPPORT)

    support_rows = [rows[state_index[state]] for state in DUAL_SUPPORT]
    balance = [
        [to_sympy(-support_rows[support_index][column])
         for support_index in range(len(DUAL_SUPPORT))]
        + [to_sympy(boundary[column])]
        for column in range(len(variable_types()))
    ]
    domain_matrix = DomainMatrix.from_list_sympy(48, 49, balance)
    assert domain_matrix.rank() == 48
    nullspace = domain_matrix.nullspace().to_Matrix()
    assert nullspace.shape == (1, 49)

    raw = [from_sympy(entry) for entry in nullspace.row(0)]
    assert raw[-1] != 0
    ray = [-entry / raw[-1] for entry in raw]
    y = ray[:-1]
    z = ray[-1]
    assert z == -1
    assert all(value > 0 for value in y)

    # Independently substitute into every exact dual equation.
    for column in range(len(variable_types())):
        balance_value = -sum(
            (support_rows[index][column] * y[index]
             for index in range(len(DUAL_SUPPORT))),
            Q(0),
        ) + boundary[column] * z
        assert balance_value == 0

    objective = sum(
        (constants[state_index[state]] * y[index]
         for index, state in enumerate(DUAL_SUPPORT)),
        Q(0),
    )
    assert objective < 0
    return y, objective


def rank_balance_audit(y: list[Q], objective: Q) -> tuple[Q, Q, Q]:
    """Check the telescoping rank conservation law behind the witness."""

    gain_mass = [Q(0) for _ in range(N_VERTICES + 1)]
    loss_mass = [Q(0) for _ in range(N_VERTICES + 1)]
    for state, weight in zip(DUAL_SUPPORT, y):
        _, _, gain_out, loss_in = orbit_rates(state)
        rank = sum(state)
        gain_mass[rank] += weight * gain_out
        loss_mass[rank] += weight * loss_in

    assert gain_mass[0] == 0
    assert loss_mass[N_VERTICES] == 0
    for rank in range(2, N_VERTICES):
        assert (
            gain_mass[rank - 1]
            - 2 * (gain_mass[rank] + loss_mass[rank])
            + 4 * loss_mass[rank + 1]
        ) == 0

    # The rank-one balance contains the boundary multiplier z=-1.
    assert (
        gain_mass[0]
        - 2 * (gain_mass[1] + loss_mass[1])
        + 4 * loss_mass[2]
    ) == -N_VERTICES

    endpoint_coefficient = (
        2 ** (N_VERTICES - 1) * (N_VERTICES + 1) - 2 * N_VERTICES
    )
    telescoped = (
        2 * (N_VERTICES - 1) * loss_mass[1]
        - endpoint_coefficient * gain_mass[N_VERTICES - 1]
    ) / N_VERTICES
    assert telescoped == objective

    endpoint_ratio = gain_mass[N_VERTICES - 1] / loss_mass[1]
    threshold = Q(2 * (N_VERTICES - 1), endpoint_coefficient)
    assert endpoint_ratio > threshold
    return loss_mass[1], gain_mass[N_VERTICES - 1], threshold


def to_fmpq(value: Q) -> fmpq:
    return fmpq(value.numerator, value.denominator)


def from_fmpq(value: fmpq) -> Q:
    return Q(int(value.numerator), int(value.denominator))


def exact_lumped_fixation() -> Q:
    """Solve the 196-state dB fixation equations exactly with FLINT."""

    states = orbit_states()
    state_index = {state: index for index, state in enumerate(states)}
    matrix = [[Q(0) for _ in states] for _ in states]
    right = [Q(0) for _ in states]

    for row_index, state in enumerate(states):
        gain, loss, _, _ = orbit_rates(state)
        total_change = Q(0)
        for vertex_class, size in enumerate(CLASS_SIZES):
            count = state[vertex_class]
            if count < size:
                probability = Q(size - count, N_VERTICES) * gain[vertex_class]
                total_change += probability
                target = list(state)
                target[vertex_class] += 1
                target_tuple = tuple(target)
                if target_tuple == CLASS_SIZES:
                    right[row_index] += probability
                else:
                    matrix[row_index][state_index[target_tuple]] -= probability
            if count > 0:
                probability = Q(count, N_VERTICES) * loss[vertex_class]
                total_change += probability
                target = list(state)
                target[vertex_class] -= 1
                target_tuple = tuple(target)
                if target_tuple != (0, 0, 0):
                    matrix[row_index][state_index[target_tuple]] -= probability
        assert 0 < total_change <= 1
        matrix[row_index][row_index] += total_change

    flint_matrix = fmpq_mat([[to_fmpq(value) for value in row] for row in matrix])
    flint_right = fmpq_mat([[to_fmpq(value)] for value in right])
    solution = flint_matrix.solve(flint_right)

    # Check the exact equations independently after conversion to Fraction.
    solution_q = [from_fmpq(solution[index, 0]) for index in range(len(states))]
    for row_index, row in enumerate(matrix):
        assert sum(
            (value * solution_q[column] for column, value in enumerate(row)),
            Q(0),
        ) == right[row_index]
    assert all(0 < value < 1 for value in solution_q)

    fixation = sum(
        (
            Q(CLASS_SIZES[vertex_class], N_VERTICES)
            * solution_q[state_index[tuple(
                1 if other == vertex_class else 0
                for other in range(len(CLASS_SIZES))
            )]]
            for vertex_class in range(len(CLASS_SIZES))
        ),
        Q(0),
    )
    assert 0 < fixation < 1
    return fixation


def exact_complete_baseline() -> Q:
    """Independently solve the one-dimensional K_17 dB chain at r=2."""

    transient_ranks = list(range(1, N_VERTICES))
    matrix = [[Q(0) for _ in transient_ranks] for _ in transient_ranks]
    right = [Q(0) for _ in transient_ranks]
    for row, rank in enumerate(transient_ranks):
        up = (
            Q(N_VERTICES - rank, N_VERTICES)
            * Q(2 * rank, N_VERTICES + rank - 1)
        )
        down = (
            Q(rank, N_VERTICES)
            * Q(N_VERTICES - rank, N_VERTICES + rank - 2)
        )
        matrix[row][row] += up + down
        if rank + 1 == N_VERTICES:
            right[row] += up
        else:
            matrix[row][row + 1] -= up
        if rank - 1 > 0:
            matrix[row][row - 1] -= down

    solution = fmpq_mat(
        [[to_fmpq(value) for value in row] for row in matrix]
    ).solve(fmpq_mat([[to_fmpq(value)] for value in right]))
    baseline = from_fmpq(solution[0, 0])
    assert baseline == Q(524_288, 1_114_095)
    return baseline


def decimal_string(value: Q, digits: int = 20) -> str:
    with localcontext() as context:
        context.prec = digits
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def rational_digest(value: Q) -> str:
    payload = f"{value.numerator}/{value.denominator}".encode()
    return sha256(payload).hexdigest()


def main() -> None:
    assert CLASS_WEIGHTS == tuple(zip(*CLASS_WEIGHTS))
    assert all(
        CLASS_WEIGHTS[i][j] > 0
        for i in range(len(CLASS_SIZES))
        for j in range(len(CLASS_SIZES))
    )
    assert class_degrees() == (20_000_125, 45_066, 23_860)
    assert len(orbit_states()) == 196

    labelled_row_audit()
    y, objective = exact_farkas_ray()
    rank_one_loss, rank_last_gain, endpoint_threshold = rank_balance_audit(
        y, objective
    )
    fixation = exact_lumped_fixation()
    baseline = exact_complete_baseline()
    ratio = fixation / baseline
    assert fixation < baseline

    print("rank-dependent additive Farkas verifier: PASS")
    print("graph: n=17, class sizes=(2,5,10), complete positive support")
    print("labelled-to-quotient drift rows checked: 196")
    print("dual balance: rank=48, nullity=1, normalization z=-1")
    print(f"strictly positive support weights: {len(y)}")
    print(f"dual objective: {decimal_string(objective)} < 0 (exact)")
    print(
        "dual objective digits/hash: "
        f"{len(str(abs(objective.numerator)))}/"
        f"{len(str(objective.denominator))}, {rational_digest(objective)}"
    )
    print(
        "rank endpoint masses R_1,A_16: "
        f"{decimal_string(rank_one_loss)}, {decimal_string(rank_last_gain)}"
    )
    print(
        "A_16/R_1 versus exact threshold: "
        f"{decimal_string(rank_last_gain / rank_one_loss)} > "
        f"{decimal_string(endpoint_threshold)}"
    )
    print(f"dB fixation at r=2: {decimal_string(fixation)}")
    print(f"K_17 baseline: {baseline}")
    print(f"normalized fixation ratio: {decimal_string(ratio)} < 1 (exact)")
    print(
        "fixation digits/hash: "
        f"{len(str(fixation.numerator))}/{len(str(fixation.denominator))}, "
        f"{rational_digest(fixation)}"
    )


if __name__ == "__main__":
    main()
