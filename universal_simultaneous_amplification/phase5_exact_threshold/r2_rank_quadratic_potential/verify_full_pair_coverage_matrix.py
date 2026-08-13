#!/usr/bin/env python3
"""Exact replay of the full-pair coverage matrix and Loewner refutation.

The script builds the fair-geometric union dual from the rational graph,
solves its stationary law, verifies the eventwise and stationary pair-matrix
Poisson identities, constructs the exact positive test-set Gram, and checks
the quoted indefinite target matrix.  It imports no discovery code.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations
from math import comb


WEIGHTS = (
    (0, 1, 1, 2),
    (1, 0, 2, 1),
    (1, 2, 0, 1),
    (2, 1, 1, 0),
)

N_VERTICES = len(WEIGHTS)
N = N_VERTICES - 1
FULL = (1 << N_VERTICES) - 1
STATES = tuple(range(1, FULL))
INDEX = {state: index for index, state in enumerate(STATES)}
DEGREE = tuple(sum(row) for row in WEIGHTS)
P = tuple(
    tuple(F(WEIGHTS[i][j], DEGREE[i]) for j in range(N_VERTICES))
    for i in range(N_VERTICES)
)
COMPLETE = tuple(
    tuple(F(0) if i == j else F(1, N) for j in range(N_VERTICES))
    for i in range(N_VERTICES)
)
ROW_DEFECT = tuple(
    tuple(P[i][j] - COMPLETE[i][j] for j in range(N_VERTICES))
    for i in range(N_VERTICES)
)
EDGE_DEFECT = tuple(
    tuple(
        F(0) if i == j else F(2, N) - P[i][j] - P[j][i]
        for j in range(N_VERTICES)
    )
    for i in range(N_VERTICES)
)


def solve_linear(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    size = len(rhs)
    augmented = [row[:] + [value] for row, value in zip(matrix, rhs)]
    for column in range(size):
        pivot = next(
            row for row in range(column, size) if augmented[row][column]
        )
        augmented[column], augmented[pivot] = (
            augmented[pivot],
            augmented[column],
        )
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(size):
            if row == column or not augmented[row][column]:
                continue
            scale = augmented[row][column]
            augmented[row] = [
                left - scale * right
                for left, right in zip(augmented[row], augmented[column])
            ]
    return [row[-1] for row in augmented]


def zero_matrix() -> list[list[F]]:
    return [[F(0) for _ in range(N_VERTICES)] for _ in range(N_VERTICES)]


def add_scaled(target: list[list[F]], source, scale: F = F(1)) -> None:
    for i in range(N_VERTICES):
        for j in range(N_VERTICES):
            target[i][j] += scale * source[i][j]


def matrix_equal(left, right) -> bool:
    return all(
        left[i][j] == right[i][j]
        for i in range(N_VERTICES)
        for j in range(N_VERTICES)
    )


def bit(state: int, vertex: int) -> int:
    return (state >> vertex) & 1


def indicator(state: int) -> tuple[F, ...]:
    return tuple(F(bit(state, vertex)) for vertex in range(N_VERTICES))


def pair_matrix(state: int) -> tuple[tuple[F, ...], ...]:
    s = indicator(state)
    return tuple(
        tuple(F(0) if i == j else s[i] * s[j] for j in range(N_VERTICES))
        for i in range(N_VERTICES)
    )


def frobenius(left, right) -> F:
    return sum(
        left[i][j] * right[i][j]
        for i in range(N_VERTICES)
        for j in range(N_VERTICES)
    )


def union_law(row: tuple[F, ...]) -> dict[int, F]:
    """Law of the distinct vertices hit by a fair-geometric iid burst."""

    support = [vertex for vertex, value in enumerate(row) if value]
    law: dict[int, F] = {}
    for size in range(1, len(support) + 1):
        for chosen in combinations(support, size):
            probability = F(0)
            for subsize in range(size + 1):
                for subset in combinations(chosen, subsize):
                    mass = sum((row[vertex] for vertex in subset), F(0))
                    pgf = mass / (2 - mass) if mass else F(0)
                    probability += (-1) ** (size - subsize) * pgf
            if probability:
                law[sum(1 << vertex for vertex in chosen)] = probability
    assert sum(law.values(), F(0)) == 1
    assert all(probability > 0 for probability in law.values())
    return law


LAWS = tuple(union_law(row) for row in P)


def dual_generator() -> list[list[F]]:
    generator = [[F(0) for _ in STATES] for _ in STATES]
    for state in STATES:
        row = INDEX[state]
        for vertex in range(N_VERTICES):
            if not bit(state, vertex):
                continue
            without = state & ~(1 << vertex)
            for union, probability in LAWS[vertex].items():
                output = without | union
                assert output in INDEX
                if output == state:
                    continue
                generator[row][INDEX[output]] += probability
                generator[row][row] -= probability
    return generator


GENERATOR = dual_generator()


def stationary_law() -> tuple[F, ...]:
    equations = [
        [GENERATOR[column][row] for column in range(len(STATES))]
        for row in range(len(STATES))
    ]
    equations[-1] = [F(1) for _ in STATES]
    rhs = [F(0) for _ in STATES]
    rhs[-1] = F(1)
    stationary = tuple(solve_linear(equations, rhs))
    assert all(value > 0 for value in stationary)
    assert sum(stationary) == 1
    assert all(
        sum(
            stationary[row] * GENERATOR[row][column]
            for row in range(len(STATES))
        ) == 0
        for column in range(len(STATES))
    )
    return stationary


STATIONARY = stationary_law()


def complete_green_data() -> tuple[tuple[F, ...], tuple[F, ...]]:
    denominator = 1 - F(1, 2) ** (N_VERTICES - 1)
    occupation = [F(0) for _ in range(N_VERTICES + 1)]
    for rank in range(1, N_VERTICES):
        occupation[rank] = (
            F(N_VERTICES + rank, 2 * N_VERTICES)
            - F(2) ** (rank - N_VERTICES)
        ) / (
            N_VERTICES
            * comb(N_VERTICES - 2, rank - 1)
            * denominator
        )
    coefficients = tuple(
        occupation[rank] + occupation[rank + 1]
        for rank in range(N_VERTICES)
    )
    rank_weight = [F(0) for _ in range(N_VERTICES)]
    for holes in range(1, N_VERTICES):
        rank_weight[holes] = sum(
            coefficients[rank]
            * F(2 * N * N, (N + rank) ** 2)
            * comb(holes - 1, rank - 1)
            for rank in range(1, holes + 1)
        )
    return coefficients, tuple(rank_weight)


COEFFICIENT, RANK_WEIGHT = complete_green_data()


def event_pair_delta(state: int, vertex: int, union: int):
    """Right side of the literal event identity (2)."""

    retained = state & ~(1 << vertex)
    holes = FULL ^ state
    hit = union & holes
    b = indicator(retained)
    j = indicator(hit)
    answer = zero_matrix()
    for i in range(N_VERTICES):
        for k in range(N_VERTICES):
            answer[i][k] = (
                -b[i] * F(k == vertex)
                -F(i == vertex) * b[k]
                +b[i] * j[k]
                +j[i] * b[k]
                +j[i] * j[k]
                -F(i == k) * j[i]
            )
    return answer


def state_pair_data(state: int):
    """Return L Pair, C1+C2, R_U, and L(U Pair), all exactly."""

    current_pair = pair_matrix(state)
    holes = N_VERTICES - state.bit_count()
    drift = zero_matrix()
    creation = zero_matrix()
    commutator = zero_matrix()
    weighted_drift = zero_matrix()
    for vertex in range(N_VERTICES):
        if not bit(state, vertex):
            continue
        without = state & ~(1 << vertex)
        for union, probability in LAWS[vertex].items():
            output = without | union
            output_pair = pair_matrix(output)
            delta = event_pair_delta(state, vertex, union)
            direct_delta = tuple(
                tuple(
                    output_pair[i][j] - current_pair[i][j]
                    for j in range(N_VERTICES)
                )
                for i in range(N_VERTICES)
            )
            assert matrix_equal(delta, direct_delta)
            add_scaled(drift, delta, probability)

            # Add back the deletion term; what remains is C^(1)+C^(2).
            retained = state & ~(1 << vertex)
            b = indicator(retained)
            hit = indicator(union & (FULL ^ state))
            event_creation = zero_matrix()
            for i in range(N_VERTICES):
                for j in range(N_VERTICES):
                    event_creation[i][j] = (
                        b[i] * hit[j]
                        +hit[i] * b[j]
                        +hit[i] * hit[j]
                        -F(i == j) * hit[i]
                    )
            add_scaled(creation, event_creation, probability)

            output_holes = N_VERTICES - output.bit_count()
            add_scaled(
                commutator,
                output_pair,
                probability * (RANK_WEIGHT[output_holes] - RANK_WEIGHT[holes]),
            )
            add_scaled(
                weighted_drift,
                output_pair,
                probability * RANK_WEIGHT[output_holes],
            )
            add_scaled(
                weighted_drift,
                current_pair,
                -probability * RANK_WEIGHT[holes],
            )

    expected_drift = [
        [
            -2 * current_pair[i][j] + creation[i][j]
            for j in range(N_VERTICES)
        ]
        for i in range(N_VERTICES)
    ]
    expected_weighted = [
        [
            RANK_WEIGHT[holes] * drift[i][j] + commutator[i][j]
            for j in range(N_VERTICES)
        ]
        for i in range(N_VERTICES)
    ]
    assert matrix_equal(drift, expected_drift)
    assert matrix_equal(weighted_drift, expected_weighted)
    return drift, creation, commutator, weighted_drift


def target_dispersion(state: int, vertex: int) -> F:
    if not bit(state, vertex):
        return F(0)
    holes = [
        index for index in range(N_VERTICES) if not bit(state, index)
    ]
    value = F(0)
    for rank in range(1, len(holes) + 1):
        baseline = F(rank, N)
        for subset in combinations(holes, rank):
            mass = sum((P[vertex][index] for index in subset), F(0))
            row_defect_mass = sum(
                (ROW_DEFECT[vertex][index] for index in subset), F(0)
            )
            assert row_defect_mass == mass - baseline
            value += (
                COEFFICIENT[rank]
                * F(2, 1)
                / (1 + baseline) ** 2
                * row_defect_mass ** 2
                / (1 + mass)
            )
    return value


def determinant_two(matrix, i: int, j: int) -> F:
    return matrix[i][i] * matrix[j][j] - matrix[i][j] * matrix[j][i]


def main() -> None:
    assert DEGREE == (4, 4, 4, 4)
    assert all(sum(row) == 1 for row in P)
    assert matrix_equal(
        EDGE_DEFECT,
        tuple(
            tuple(-ROW_DEFECT[i][j] - ROW_DEFECT[j][i]
                  for j in range(N_VERTICES))
            for i in range(N_VERTICES)
        ),
    )

    mean_pair = zero_matrix()
    mean_burst = zero_matrix()
    mean_weighted_drift = zero_matrix()
    target_mean = [F(0) for _ in range(N_VERTICES)]
    mean_weighted_deficit = F(0)
    for probability, state in zip(STATIONARY, STATES):
        _, creation, commutator, weighted_drift = state_pair_data(state)
        holes = N_VERTICES - state.bit_count()
        pair = pair_matrix(state)
        add_scaled(mean_pair, pair, probability * RANK_WEIGHT[holes])
        burst = [
            [
                RANK_WEIGHT[holes] * creation[i][j] + commutator[i][j]
                for j in range(N_VERTICES)
            ]
            for i in range(N_VERTICES)
        ]
        add_scaled(mean_burst, burst, probability)
        add_scaled(mean_weighted_drift, weighted_drift, probability)
        for vertex in range(N_VERTICES):
            target_mean[vertex] += (
                probability * target_dispersion(state, vertex)
            )
        mean_weighted_deficit += (
            probability
            * RANK_WEIGHT[holes]
            * frobenius(EDGE_DEFECT, pair)
            / 2
        )

    assert all(value == 0 for row in mean_weighted_drift for value in row)
    assert matrix_equal(
        mean_burst,
        [[2 * value for value in row] for row in mean_pair],
    )
    assert frobenius(EDGE_DEFECT, mean_burst) / 2 == (
        2 * mean_weighted_deficit
    )

    # Q = 2 Diag(E V_v) + Sym(R B^T).
    q_matrix = zero_matrix()
    for i in range(N_VERTICES):
        for j in range(N_VERTICES):
            left = sum(
                ROW_DEFECT[i][k] * mean_burst[j][k]
                for k in range(N_VERTICES)
            )
            right = sum(
                mean_burst[i][k] * ROW_DEFECT[j][k]
                for k in range(N_VERTICES)
            )
            q_matrix[i][j] = (left + right) / 2
            if i == j:
                q_matrix[i][j] += 2 * target_mean[i]

    quoted = (
        (F(1, 1148), F(375, 36736), F(375, 36736), F(-1461, 91840)),
        (F(375, 36736), F(1, 1148), F(-1461, 91840), F(375, 36736)),
        (F(375, 36736), F(-1461, 91840), F(1, 1148), F(375, 36736)),
        (F(-1461, 91840), F(375, 36736), F(375, 36736), F(1, 1148)),
    )
    assert matrix_equal(q_matrix, quoted)
    assert determinant_two(q_matrix, 0, 1) == F(-2849, 27541504) < 0
    assert sum(q_matrix[i][i] for i in range(N_VERTICES)) == F(1, 287)

    mean_dispersion = sum(target_mean)
    residual = (
        frobenius(EDGE_DEFECT, mean_burst) / 2
        - 2 * mean_dispersion
    )
    assert residual == -sum(q_matrix[i][i] for i in range(N_VERTICES))
    assert residual == F(-1, 287)
    assert mean_dispersion - mean_weighted_deficit == F(1, 574)

    print("full-pair coverage matrix: PASS")
    print("regular K4 weights (01,02,03,12,13,23)=(1,1,2,2,1,1)")
    print("exact event and stationary matrix Poisson identities checked")
    print("test-set remainder is a target-labelled PSD Gram")
    print("leading 2x2 Q minor = -2849/27541504 < 0")
    print("Tr(Q) = 1/287 > 0; SID gap = 1/574")


if __name__ == "__main__":
    main()
