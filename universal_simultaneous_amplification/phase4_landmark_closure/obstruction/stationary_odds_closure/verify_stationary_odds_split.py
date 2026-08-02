#!/usr/bin/env python3
"""Exact certificates for the stationary component-odds split at r=2.

The program uses only ``fractions.Fraction``.  It verifies the direct
stationary/resolvent identities, an exact directed counterexample to the
left split, and exact symmetric counterexamples to two tempting intermediate
resolvent bridges.  It does *not* claim that either split is proved for all
undirected weighted graphs.
"""

from __future__ import annotations

from fractions import Fraction as F


def solve(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    n = len(matrix)
    augmented = [matrix[row][:] + [rhs[row]] for row in range(n)]
    for column in range(n):
        pivot = next(row for row in range(column, n) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [entry / scale for entry in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            scale = augmented[row][column]
            if scale:
                augmented[row] = [
                    left - scale * right
                    for left, right in zip(augmented[row], augmented[column])
                ]
    return [augmented[row][-1] for row in range(n)]


def inverse(matrix: list[list[F]]) -> list[list[F]]:
    size = len(matrix)
    columns = [
        solve(matrix, [F(int(row == column)) for row in range(size)])
        for column in range(size)
    ]
    return [[columns[column][row] for column in range(size)] for row in range(size)]


def matvec(matrix: list[list[F]], vector: list[F]) -> list[F]:
    return [sum(entry * value for entry, value in zip(row, vector)) for row in matrix]


def rowmat(vector: list[F], matrix: list[list[F]]) -> list[F]:
    return [
        sum(vector[row] * matrix[row][column] for row in range(len(vector)))
        for column in range(len(vector))
    ]


def dot(left: list[F], right: list[F]) -> F:
    return sum(a * b for a, b in zip(left, right))


def transition(weights: list[list[int]]) -> list[list[F]]:
    return [[F(entry, sum(row)) for entry in row] for row in weights]


def h(value: F) -> F:
    return 2 * value / (1 + value)


def geometric_union_law(row: list[F]) -> dict[int, F]:
    """Law of the distinct sites in K geometric(1/2) row samples."""

    n = len(row)
    values = [F(0) for _ in range(1 << n)]
    for mask in range(1 << n):
        mass = sum((row[j] for j in range(n) if mask >> j & 1), F(0))
        values[mask] = mass / (2 - mass)
    for j in range(n):
        for mask in range(1 << n):
            if mask >> j & 1:
                values[mask] -= values[mask ^ (1 << j)]
    law = {mask: values[mask] for mask in range(1, 1 << n) if values[mask]}
    assert sum(law.values()) == 1
    assert all(probability > 0 for probability in law.values())
    return law


def batched_generator(P: list[list[F]]) -> tuple[list[list[F]], list[dict[int, F]]]:
    n = len(P)
    size = (1 << n) - 1
    laws = [geometric_union_law(row) for row in P]
    generator = [[F(0) for _ in range(size)] for _ in range(size)]
    for state in range(1, 1 << n):
        row = state - 1
        for vertex in range(n):
            if not (state >> vertex & 1):
                continue
            for offspring, probability in laws[vertex].items():
                new_state = (state & ~(1 << vertex)) | offspring
                if new_state != state:
                    generator[row][new_state - 1] += probability
        generator[row][row] = -sum(generator[row])
    return generator, laws


def stationary(generator: list[list[F]]) -> list[F]:
    size = len(generator)
    matrix = [
        [generator[column][row] for column in range(size)]
        for row in range(size)
    ]
    rhs = [F(0) for _ in range(size)]
    matrix[-1] = [F(1) for _ in range(size)]
    rhs[-1] = F(1)
    law = solve(matrix, rhs)
    assert sum(law) == 1
    assert all(mass >= 0 for mass in law)
    for column in range(size):
        assert sum(law[row] * generator[row][column] for row in range(size)) == 0
    return law


def marginals(pi: list[F], n: int) -> list[F]:
    return [
        sum(pi[state - 1] for state in range(1, 1 << n) if state >> vertex & 1)
        for vertex in range(n)
    ]


def post_target_law(
    pi: list[F], laws: list[dict[int, F]], target: int, n: int
) -> list[F]:
    outside = [vertex for vertex in range(n) if vertex != target]
    local = {vertex: position for position, vertex in enumerate(outside)}
    eta = [F(0) for _ in range(1 << (n - 1))]
    for state in range(1, 1 << n):
        if not (state >> target & 1):
            outputs = {state: F(1)}
        else:
            outputs: dict[int, F] = {}
            for offspring, probability in laws[target].items():
                output = (state & ~(1 << target)) | offspring
                outputs[output] = outputs.get(output, F(0)) + probability
        for output, probability in outputs.items():
            assert not (output >> target & 1)
            local_state = sum(
                1 << local[vertex]
                for vertex in outside
                if output >> vertex & 1
            )
            eta[local_state] += pi[state - 1] * probability
    assert sum(eta) == 1
    return eta


def stopped_operators(
    P: list[list[F]], laws: list[dict[int, F]], target: int
) -> tuple[list[F], list[F], list[list[F]], list[int]]:
    """Return u, g and the zero-count terminal kernel R0."""

    n = len(P)
    outside = [vertex for vertex in range(n) if vertex != target]
    local = {vertex: position for position, vertex in enumerate(outside)}
    size = 1 << (n - 1)
    zero_matrix = [
        [F(int(row == column)) for column in range(size)]
        for row in range(size)
    ]
    generator = [[F(0) for _ in range(size)] for _ in range(size)]
    reward = [F(0) for _ in range(size)]

    for state in range(size):
        active = [
            outside[position]
            for position in range(n - 1)
            if state >> position & 1
        ]
        zero_matrix[state][state] += len(active)
        for vertex in active:
            reward[state] += 2 * P[vertex][target]
            marginal: dict[int, F] = {}
            for offspring, probability in laws[vertex].items():
                outside_offspring = sum(
                    1 << local[j]
                    for j in outside
                    if offspring >> j & 1
                )
                new_state = (
                    state & ~(1 << local[vertex])
                ) | outside_offspring
                marginal[new_state] = marginal.get(new_state, F(0)) + probability
                if not (offspring >> target & 1):
                    zero_matrix[state][new_state] -= probability
            for new_state, probability in marginal.items():
                if new_state != state:
                    generator[state][new_state] += probability
        generator[state][state] = -sum(generator[state])

    zero_resolvent = inverse(zero_matrix)
    u = matvec(zero_resolvent, [F(1) for _ in range(size)])
    unmarked_matrix = [
        [F(int(row == column)) - generator[row][column] for column in range(size)]
        for row in range(size)
    ]
    g = solve(unmarked_matrix, reward)
    return u, g, zero_resolvent, outside


def direct_absent_law(pi: list[F], target: int, n: int, vacancy: F) -> list[F]:
    outside = [vertex for vertex in range(n) if vertex != target]
    law = [F(0) for _ in range(1 << (n - 1))]
    for local_state in range(1 << (n - 1)):
        full_state = sum(
            1 << outside[position]
            for position in range(n - 1)
            if local_state >> position & 1
        )
        if full_state:
            law[local_state] = pi[full_state - 1] / vacancy
    assert sum(law) == 1
    return law


def diagnostics(weights: list[list[int]], target: int) -> dict[str, F | list[F]]:
    P = transition(weights)
    n = len(P)
    generator, laws = batched_generator(P)
    pi = stationary(generator)
    p = marginals(pi, n)
    eta = post_target_law(pi, laws, target, n)
    u, g, zero_resolvent, outside = stopped_operators(P, laws, target)

    vacancy = 1 - p[target]
    raw_mean = 2 * sum(P[vertex][target] * p[vertex] for vertex in range(n))
    regenerated_q = dot(eta, u)
    regenerated_mean = dot(eta, g)
    assert regenerated_q == vacancy
    assert regenerated_mean == raw_mean

    pi_zero = direct_absent_law(pi, target, n, vacancy)
    zero_terminal = rowmat(eta, zero_resolvent)
    assert zero_terminal == [vacancy * mass for mass in pi_zero]

    fill_hazard = [
        sum(
            h(P[outside[position]][target])
            for position in range(n - 1)
            if state >> position & 1
        )
        for state in range(1 << (n - 1))
    ]
    odds = p[target] / vacancy
    assert dot(pi_zero, fill_hazard) == odds

    eta_ug = sum(mass * left * right for mass, left, right in zip(eta, u, g))
    split_a = vacancy + eta_ug - 1
    covariance = eta_ug - vacancy * raw_mean
    total = vacancy * (1 + raw_mean) - 1
    assert total == split_a - covariance

    zero_g = matvec(zero_resolvent, g)
    bridge_left = dot(eta, [left * right - z for left, right, z in zip(u, g, zero_g)])
    bridge_right = dot(eta, zero_g) - p[target]

    eta_zero_start = [mass * survival / vacancy for mass, survival in zip(eta, u)]
    assert sum(eta_zero_start) == 1
    middle = dot(eta_zero_start, g)
    assert split_a == vacancy * (middle - odds)
    assert covariance == vacancy * (middle - raw_mean)

    return {
        "split_a": split_a,
        "covariance": covariance,
        "total": total,
        "bridge_left": bridge_left,
        "bridge_right": bridge_right,
        "odds": odds,
        "middle": middle,
        "raw_mean": raw_mean,
        "eta": eta,
        "u": u,
        "g": g,
        "outside": outside,
    }


def symmetric_weights(edges: list[int]) -> list[list[int]]:
    assert len(edges) == 6
    weights = [[0 for _ in range(4)] for _ in range(4)]
    position = 0
    for left in range(4):
        for right in range(left + 1, 4):
            weights[left][right] = weights[right][left] = edges[position]
            position += 1
    return weights


def main() -> None:
    # A is false without the undirected/reversible-row restriction.
    directed = [
        [0, 150, 1, 600],
        [1, 0, 6000, 300],
        [1, 3000, 0, 6],
        [300, 25, 1, 0],
    ]
    directed_data = diagnostics(directed, target=3)
    assert directed_data["split_a"] < 0
    assert directed_data["covariance"] < 0
    assert directed_data["total"] > 0

    # On an admissible symmetric K4, the bridge eta(ug-R0g)>=0 fails.
    left_bridge_graph = symmetric_weights([40, 1, 60, 1, 1, 1000])
    left_data = diagnostics(left_bridge_graph, target=3)
    assert left_data["bridge_left"] < 0
    assert left_data["split_a"] > 0
    assert left_data["covariance"] < 0

    # The companion bridge eta R0 g >= p also fails on a symmetric K4.
    right_bridge_graph = symmetric_weights([2000, 1, 1, 100, 1, 300])
    right_data = diagnostics(right_bridge_graph, target=2)
    assert right_data["bridge_right"] < 0
    assert right_data["split_a"] > 0
    assert right_data["covariance"] < 0

    # eta need not even be pairwise associated.  For target 0, outside
    # coordinates 2 and 3 have a strict negative covariance.
    association_graph = symmetric_weights([1, 2, 1, 2, 2, 10])
    association_data = diagnostics(association_graph, target=0)
    eta = association_data["eta"]
    assert isinstance(eta, list)
    outside = association_data["outside"]
    assert outside == [1, 2, 3]
    p_two = sum(eta[state] for state in range(8) if state >> 1 & 1)
    p_three = sum(eta[state] for state in range(8) if state >> 2 & 1)
    p_both = sum(
        eta[state]
        for state in range(8)
        if state >> 1 & 1 and state >> 2 & 1
    )
    pair_covariance = p_both - p_two * p_three
    assert pair_covariance < 0

    # Nor are u and g globally ordered in opposite scalar directions.
    # Local states 3={1,2} and 4={3} move in the same strict direction.
    scalar_graph = symmetric_weights([1, 5, 100, 2, 5, 10])
    scalar_data = diagnostics(scalar_graph, target=0)
    scalar_u = scalar_data["u"]
    scalar_g = scalar_data["g"]
    assert isinstance(scalar_u, list) and isinstance(scalar_g, list)
    scalar_same_direction = (scalar_u[3] - scalar_u[4]) * (
        scalar_g[3] - scalar_g[4]
    )
    assert scalar_same_direction > 0

    print("PASS: exact stationary/resolvent identities")
    print("directed A counterexample:", directed_data["split_a"])
    print("directed full odds slack:", directed_data["total"])
    print("symmetric left-bridge counterexample:", left_data["bridge_left"])
    print("symmetric right-bridge counterexample:", right_data["bridge_right"])
    print("negative pair covariance in eta:", pair_covariance)
    print("same-direction scalar u/g product:", scalar_same_direction)
    print("left symmetric sandwich:", left_data["odds"], left_data["middle"], left_data["raw_mean"])
    print("right symmetric sandwich:", right_data["odds"], right_data["middle"], right_data["raw_mean"])


if __name__ == "__main__":
    main()
