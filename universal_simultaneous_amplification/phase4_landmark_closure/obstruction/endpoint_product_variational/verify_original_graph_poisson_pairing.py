#!/usr/bin/env python3
"""Exact verifier for the original-graph Poisson-pairing reduction.

For Q_s=M+sK, let chi_s be the centered Poisson solution

    -Q_s chi_s = |A|-m(s).

At r=3/2 the centered orientation deficit is exactly

    2m(0)-m(s)-m(-s)
      = (3s/2) sum_{i<j} w_ij (d_i^-1-d_j^-1)
          (zeta_i-zeta_j),

where zeta_i=<1_{i in A},chi_-s-chi_s>_mu.  The universal sign of this
original n-vertex Dirichlet pairing remains open.  This program verifies the
identity over exact rationals, preserves an exact counterexample to
edge-by-edge positivity, and performs a deterministic finite hostile screen.
"""

from __future__ import annotations

from fractions import Fraction as F
import random

from verify_root_marked_tree_transform import generators, solve, stationary


FITNESS = F(3, 2)
SELECTIVE_RATE = FITNESS - 1


def interpolate(left: list[list[F]], reverse: list[list[F]], s: F):
    size = len(left)
    return [
        [
            (left[i][j] + reverse[i][j]) / 2
            + s * (left[i][j] - reverse[i][j]) / 2
            for j in range(size)
        ]
        for i in range(size)
    ]


def mat_vec(matrix: list[list[F]], vector: list[F]) -> list[F]:
    return [
        sum((matrix[i][j] * vector[j] for j in range(len(vector))), F(0))
        for i in range(len(matrix))
    ]


def poisson_solution(
    generator: list[list[F]], law: list[F], mu: list[F], rank: list[F]
) -> tuple[list[F], F]:
    """Solve -Q chi=k-E_pi(k), with the gauge <chi>_mu=0."""
    size = len(generator)
    mean = sum((law[i] * rank[i] for i in range(size)), F(0))
    right = [value - mean for value in rank]
    system = [[-generator[i][j] for j in range(size)] for i in range(size)]
    system[-1] = mu[:]
    right[-1] = F(0)
    potential = solve(system, right)
    assert sum((mu[i] * potential[i] for i in range(size)), F(0)) == 0
    assert mat_vec(
        [[-value for value in row] for row in generator], potential
    ) == [value - mean for value in rank]
    return potential, mean


def poisson_pairing(
    weights: tuple[tuple[int, ...], ...], s: F
) -> tuple[F, list[tuple[int, int, F]], list[F]]:
    """Return the exact deficit, edge terms, and marginal response."""
    left, reverse = generators(weights)
    plus = interpolate(left, reverse, s)
    minus = interpolate(left, reverse, -s)
    plus_law = stationary(plus)
    minus_law = stationary(minus)
    n = len(weights)
    size = (1 << n) - 1
    rank = [F(state.bit_count()) for state in range(1, size + 1)]
    mu = [SELECTIVE_RATE ** state.bit_count() for state in range(1, size + 1)]
    normalizer = sum(mu, F(0))
    mu = [value / normalizer for value in mu]
    midpoint_mean = sum((mu[i] * rank[i] for i in range(size)), F(0))
    plus_potential, plus_mean = poisson_solution(plus, plus_law, mu, rank)
    minus_potential, minus_mean = poisson_solution(minus, minus_law, mu, rank)
    difference = [
        minus_potential[i] - plus_potential[i] for i in range(size)
    ]
    marginal = [
        sum(
            (
                mu[state - 1] * difference[state - 1]
                for state in range(1, size + 1)
                if (state >> vertex) & 1
            ),
            F(0),
        )
        for vertex in range(n)
    ]
    degree = [sum(row) for row in weights]
    edge_terms = []
    for first in range(n):
        for second in range(first + 1, n):
            if not weights[first][second]:
                continue
            term = (
                weights[first][second]
                * (F(1, degree[first]) - F(1, degree[second]))
                * (marginal[first] - marginal[second])
            )
            edge_terms.append((first, second, term))
    deficit = 2 * midpoint_mean - plus_mean - minus_mean
    pairing = s * FITNESS * sum((term for _, _, term in edge_terms), F(0))
    assert deficit == pairing

    # Check the equivalent divergence form q dot zeta independently.
    q = [
        F(1)
        - sum(
            (F(weights[other][vertex], degree[other]) for other in range(n)),
            F(0),
        )
        for vertex in range(n)
    ]
    assert sum(q, F(0)) == 0
    divergence_pairing = s * FITNESS * sum(
        (q[i] * marginal[i] for i in range(n)), F(0)
    )
    assert deficit == divergence_pairing
    return deficit, edge_terms, marginal


def atomic_triangle_check() -> None:
    """Verify the three-state block that supplies the original currents."""
    a = SELECTIVE_RATE
    midpoint = (
        (-(1 + a), 1, a),
        (1, -(1 + a), a),
        (1, 1, -2),
    )
    defect = (
        (1 + a, -1, -a),
        (1, -(1 + a), a),
        (1, -1, 0),
    )
    rank = [F(1), F(1), F(2)]
    defect_rank = mat_vec([list(row) for row in defect], rank)
    assert defect_rank == [-a, a, F(0)]
    # The midpoint block is a scaled projection: T^2=-(a+2)T.
    midpoint_square = [
        [
            sum((midpoint[i][k] * midpoint[k][j] for k in range(3)), F(0))
            for j in range(3)
        ]
        for i in range(3)
    ]
    assert midpoint_square == [
        [-(a + 2) * midpoint[i][j] for j in range(3)] for i in range(3)
    ]


def random_connected_graph(rng: random.Random, n: int):
    weights = [[0] * n for _ in range(n)]
    order = list(range(n))
    rng.shuffle(order)
    choices = [1, 2, 7, 100, 10_000, 1_000_000]
    for position in range(1, n):
        first = order[position]
        second = order[rng.randrange(position)]
        value = rng.choice(choices)
        weights[first][second] = weights[second][first] = value
    density = rng.random()
    for first in range(n):
        for second in range(first + 1, n):
            if not weights[first][second] and rng.random() < density:
                value = rng.choice(choices)
                weights[first][second] = weights[second][first] = value
    return tuple(tuple(row) for row in weights)


def main() -> None:
    atomic_triangle_check()
    print("PASS: exact original-edge three-state midpoint/current blocks")

    # On this weighted path the global pairing is positive, but its heavy
    # edge contributes negatively.  Therefore the new n-vertex inequality
    # still requires cancellation between original edges.
    weighted_path = (
        (0, 0, 1),
        (0, 0, 17),
        (1, 17, 0),
    )
    path_deficit, path_terms, _ = poisson_pairing(weighted_path, F(1))
    term_by_edge = {(first, second): term for first, second, term in path_terms}
    assert term_by_edge[(0, 2)] > 0
    assert term_by_edge[(1, 2)] < 0
    assert sum(term_by_edge.values(), F(0)) > 0
    assert path_deficit > 0
    # Independent cross-check against the electrical transfer verifier's
    # exact chord at s=2/3 (with the opposite sign convention there).
    transfer_deficit, _, _ = poisson_pairing(weighted_path, F(2, 3))
    assert transfer_deficit == F(
        189475553746489491137376, 1108033745563239785565715
    )
    print("PASS: exact endpoint Poisson-pairing identity on weighted P3")
    print("PASS: exact agreement with the electrical transfer scalar")
    print("PASS: exact negative individual-edge contribution on weighted P3")
    print("weighted-P3 endpoint deficit:", path_deficit)

    hostile_cases = (
        (
            "statewise-curvature K4",
            (
                (0, 1, 1, 1),
                (1, 0, 0, 0),
                (1, 0, 0, 3),
                (1, 0, 3, 0),
            ),
            F(1),
        ),
        (
            "all-root-mark witness",
            (
                (0, 1000, 1, 0, 10),
                (1000, 0, 0, 1000, 10000),
                (1, 0, 0, 1, 1000),
                (0, 1000, 1, 0, 1),
                (10, 10000, 1000, 1, 0),
            ),
            F(1),
        ),
        (
            "rank-tail witness",
            (
                (0, 2, 227000, 0, 0),
                (2, 0, 536000, 5, 85),
                (227000, 536000, 0, 941000, 650000),
                (0, 5, 941000, 0, 1),
                (0, 85, 650000, 1, 0),
            ),
            F(1, 5),
        ),
    )
    for name, weights, interpolation_value in hostile_cases:
        deficit, _, _ = poisson_pairing(weights, interpolation_value)
        assert deficit > 0
        print(f"PASS: exact Poisson pairing on {name}")

    # Deterministic exact hostile screen.  This is finite evidence only.
    rng = random.Random(731_991)
    trials = 24
    interpolation_values = (F(1, 5), F(1, 2), F(1))
    for trial in range(trials):
        n = 3 + trial % 3
        weights = random_connected_graph(rng, n)
        s = interpolation_values[trial % len(interpolation_values)]
        deficit, _, _ = poisson_pairing(weights, s)
        assert deficit >= 0
        if (trial + 1) % 8 == 0:
            print(f"PASS: {trial + 1}/{trials} exact Poisson-pairing screens")
    print("STATUS: original-graph Dirichlet sign remains OPEN universally")


if __name__ == "__main__":
    main()
