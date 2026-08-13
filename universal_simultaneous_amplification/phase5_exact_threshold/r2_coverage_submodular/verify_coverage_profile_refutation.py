#!/usr/bin/env python3
"""Exact certificate for the six-vertex degree-profile refutation.

The script independently builds the 22-state equitable count chain over
fractions, solves it, checks the quoted fixation value, and verifies the
rational enclosure of the transcendental profile value.
"""

from fractions import Fraction as Q
from itertools import combinations, product
from math import comb


def solve(matrix, rhs):
    n = len(rhs)
    aug = [list(matrix[i]) + [rhs[i]] for i in range(n)]
    for col in range(n):
        pivot = next(row for row in range(col, n) if aug[row][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        value = aug[col][col]
        aug[col] = [entry / value for entry in aug[col]]
        for row in range(n):
            if row == col or not aug[row][col]:
                continue
            value = aug[row][col]
            aug[row] = [
                aug[row][j] - value * aug[col][j]
                for j in range(n + 1)
            ]
    return [aug[i][-1] for i in range(n)]


def main():
    size_a, size_b = 3, 2
    weight_aa, weight_ah = 5, 2
    weight_bb, weight_bh = 73, 1

    degree_a = 2 * weight_aa + weight_ah
    degree_b = weight_bb + weight_bh
    degree_h = size_a * weight_ah + size_b * weight_bh
    assert (degree_a, degree_b, degree_h) == (12, 74, 8)

    states = [
        state
        for state in product(range(4), range(3), range(2))
        if state not in ((0, 0, 0), (3, 2, 1))
    ]
    assert len(states) == 22
    index = {state: position for position, state in enumerate(states)}
    matrix = [[Q(0) for _ in states] for _ in states]
    rhs = [Q(0) for _ in states]

    def add(source, target, rate):
        row = index[source]
        matrix[row][row] += rate
        if target == (3, 2, 1):
            rhs[row] += rate
        elif target != (0, 0, 0):
            matrix[row][index[target]] -= rate

    for state in states:
        a, b, hub = state

        if a < size_a:
            mass = Q(weight_aa * a + weight_ah * hub, degree_a)
            add(state, (a + 1, b, hub), (size_a - a) * 2 * mass / (1 + mass))
        if a:
            mass = Q(weight_aa * (a - 1) + weight_ah * hub, degree_a)
            add(state, (a - 1, b, hub), a * (1 - mass) / (1 + mass))

        if b < size_b:
            mass = Q(weight_bb * b + weight_bh * hub, degree_b)
            add(state, (a, b + 1, hub), (size_b - b) * 2 * mass / (1 + mass))
        if b:
            mass = Q(weight_bb * (b - 1) + weight_bh * hub, degree_b)
            add(state, (a, b - 1, hub), b * (1 - mass) / (1 + mass))

        mass = Q(weight_ah * a + weight_bh * b, degree_h)
        if hub:
            add(state, (a, b, 0), (1 - mass) / (1 + mass))
        else:
            add(state, (a, b, 1), 2 * mass / (1 + mass))

    harmonic = solve(matrix, rhs)
    rho = (
        3 * harmonic[index[(1, 0, 0)]]
        + 2 * harmonic[index[(0, 1, 0)]]
        + harmonic[index[(0, 0, 1)]]
    ) / 6
    quoted = Q(
        3068195756606417046102333640985779252,
        8357819445634194964176471307640845009,
    )
    assert rho == quoted
    for row_number, row in enumerate(matrix):
        assert sum(entry * x for entry, x in zip(row, harmonic)) \
            == rhs[row_number]

    # The reversible masses are (1/16)^3, (37/96)^2, 1/24.
    total_degree = 3 * degree_a + 2 * degree_b + degree_h
    assert total_degree == 192
    assert Q(degree_a, total_degree) == Q(1, 16)
    assert Q(degree_b, total_degree) == Q(37, 96)
    assert Q(degree_h, total_degree) == Q(1, 24)

    # If alpha=2^(1/16) and u>alpha, replacing alpha by u in the
    # negative-power profile expression gives a strict rational upper bound.
    u = Q(10443, 10000)
    assert u**16 > 2
    profile_upper = Q(32, 31) * (
        1
        - Q(1, 6)
        * (
            3 * Q(17, 16) * u**-6
            + 2 * Q(133, 96) * u**-37
            + Q(25, 24) * u**-4
        )
    )
    assert rho - profile_upper > Q(42, 10000)
    assert rho < Q(80, 189)  # The actual complete K_6 baseline.

    print("PASS: exact 22-state fixation solve")
    print("PASS: reversible degree profile (1/16)^3,(37/96)^2,1/24")
    print("PASS: rational enclosure proves rho > profile RHS by > 0.0042")
    print("PASS: witness remains below K_6; only the profile envelope is refuted")


def verify_test_set_collapse():
    """Check (35)--(36) independently on rational graph/set atoms."""
    weights = [
        [0, 3, 0, 2, 1],
        [3, 0, 5, 0, 4],
        [0, 5, 0, 7, 0],
        [2, 0, 7, 0, 6],
        [1, 4, 0, 6, 0],
    ]
    n = len(weights)
    degrees = [sum(row) for row in weights]
    transition = [
        [Q(weights[v][u], degrees[v]) for u in range(n)]
        for v in range(n)
    ]
    for mask in range(1, (1 << n) - 1):
        occupied = [v for v in range(n) if (mask >> v) & 1]
        holes = [v for v in range(n) if not ((mask >> v) & 1)]
        size, hole_count = len(occupied), len(holes)
        internal = sum(
            transition[v][u] for v in occupied for u in occupied
        )
        deficit = Q(size * (size - 1), n - 1) - internal
        edge_deficit = sum(
            Q(2, n - 1)
            - weights[u][v] * (Q(1, degrees[u]) + Q(1, degrees[v]))
            for u, v in combinations(occupied, 2)
        )
        assert deficit == edge_deficit
        for k in range(hole_count + 1):
            centered = sum(
                sum(transition[v][u] for u in subset) - Q(k, n - 1)
                for v in occupied
                for subset in combinations(holes, k)
            )
            expected = Q(k * comb(hole_count, k), hole_count) * deficit
            assert centered == expected
    print("PASS: exact test-set first moment collapses to internal-edge deficit")


if __name__ == "__main__":
    main()
    verify_test_set_collapse()
