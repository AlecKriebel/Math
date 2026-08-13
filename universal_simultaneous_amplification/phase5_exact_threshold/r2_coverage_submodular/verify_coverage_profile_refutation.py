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


def dual_data(weights):
    """Build the exact proper-set dual generator and stationary law."""
    n = len(weights)
    degrees = [sum(row) for row in weights]
    transition = [
        [Q(weights[v][u], degrees[v]) for u in range(n)]
        for v in range(n)
    ]

    def union_law(row):
        support = [u for u, value in enumerate(row) if value]
        law = {}
        for size in range(1, len(support) + 1):
            for chosen in combinations(support, size):
                probability = Q(0)
                for subsize in range(size + 1):
                    for subset in combinations(chosen, subsize):
                        mass = sum((row[u] for u in subset), Q(0))
                        pgf = mass / (2 - mass) if mass else Q(0)
                        probability += (-1) ** (size - subsize) * pgf
                if probability:
                    mask = sum(1 << u for u in chosen)
                    law[mask] = probability
        assert sum(law.values(), Q(0)) == 1
        assert all(value > 0 for value in law.values())
        return law

    full = (1 << n) - 1
    states = list(range(1, full))
    index = {state: position for position, state in enumerate(states)}
    laws = [union_law(row) for row in transition]
    generator = [[Q(0) for _ in states] for _ in states]
    for state in states:
        source = index[state]
        for target in range(n):
            if not ((state >> target) & 1):
                continue
            without = state & ~(1 << target)
            for union, probability in laws[target].items():
                output = without | union
                assert 0 < output < full
                if output == state:
                    continue
                generator[source][index[output]] += probability
                generator[source][source] -= probability

    equations = [
        [generator[column][row] for column in range(len(states))]
        for row in range(len(states))
    ]
    equations[-1] = [Q(1) for _ in states]
    rhs = [Q(0) for _ in states]
    rhs[-1] = Q(1)
    stationary = solve(equations, rhs)
    assert all(value > 0 for value in stationary)
    for column in range(len(states)):
        assert sum(
            stationary[row] * generator[row][column]
            for row in range(len(states))
        ) == 0
    return transition, states, generator, stationary, laws


def complete_green_weights(n):
    """Return the exact c_k and U_h from (10) and (38)."""
    denominator = 1 - Q(1, 2) ** (n - 1)
    mu = [Q(0) for _ in range(n + 1)]
    for k in range(1, n):
        mu[k] = (
            Q(n + k, 2 * n) - Q(2) ** (k - n)
        ) / (n * comb(n - 2, k - 1) * denominator)
    coefficients = [mu[k] + mu[k + 1] for k in range(n)]
    N = n - 1
    weights = [Q(0) for _ in range(n)]
    for holes in range(1, n):
        weights[holes] = sum(
            coefficients[k]
            * Q(2 * N * N, (N + k) ** 2)
            * comb(holes - 1, k - 1)
            for k in range(1, holes + 1)
        )
    return coefficients, weights


def verify_stationary_deficit_generator(weights, expected):
    """Check (42)--(58), including the nonreversible-flow obstruction."""
    P, states, generator, stationary, laws = dual_data(weights)
    n, N = len(P), len(P) - 1
    index = {state: position for position, state in enumerate(states)}
    coefficients, rank_weight = complete_green_weights(n)

    edge = [
        [Q(0) if i == j else Q(2, N) - P[i][j] - P[j][i]
         for j in range(n)]
        for i in range(n)
    ]

    def deficit(state):
        occupied = [v for v in range(n) if (state >> v) & 1]
        return sum(edge[i][j] for i, j in combinations(occupied, 2))

    def dispersion(state):
        occupied = [v for v in range(n) if (state >> v) & 1]
        holes = [v for v in range(n) if not ((state >> v) & 1)]
        value = Q(0)
        for v in occupied:
            for k in range(1, len(holes) + 1):
                baseline = Q(k, N)
                for subset in combinations(holes, k):
                    mass = sum((P[v][u] for u in subset), Q(0))
                    value += (
                        coefficients[k]
                        * Q(2)
                        / (1 + baseline) ** 2
                        * (mass - baseline) ** 2
                        / (1 + mass)
                    )
        return value

    # Check the event-level deletion/creation law, its averaged b-coefficients,
    # and both product-generator identities on every state.
    for state in states:
        occupied = [v for v in range(n) if (state >> v) & 1]
        holes = [v for v in range(n) if not ((state >> v) & 1)]
        z_value = deficit(state)
        creation_one = Q(0)
        creation_two = Q(0)
        commutator = Q(0)
        direct_lz = Q(0)
        direct_luz = Q(0)
        holes_count = len(holes)
        for v in occupied:
            without = state & ~(1 << v)
            retained = [x for x in occupied if x != v]
            for union, probability in laws[v].items():
                output = without | union
                hit = [i for i in holes if (union >> i) & 1]
                event_delta = (
                    -sum((edge[v][x] for x in retained), Q(0))
                    + sum(
                        (edge[i][x] for i in hit for x in retained), Q(0)
                    )
                    + sum(edge[i][j] for i, j in combinations(hit, 2))
                )
                assert event_delta == deficit(output) - z_value
                direct_lz += probability * event_delta
                output_holes = n - output.bit_count()
                direct_luz += probability * (
                    rank_weight[output_holes] * deficit(output)
                    - rank_weight[holes_count] * z_value
                )
                commutator += probability * (
                    rank_weight[output_holes] - rank_weight[holes_count]
                ) * deficit(output)
            for i in holes:
                hit_one = 2 * P[v][i] / (1 + P[v][i])
                creation_one += hit_one * sum(
                    (edge[i][x] for x in retained), Q(0)
                )
            for i, j in combinations(holes, 2):
                hit_two = (
                    2 * P[v][i] / (1 + P[v][i])
                    + 2 * P[v][j] / (1 + P[v][j])
                    - 2 * (P[v][i] + P[v][j])
                    / (1 + P[v][i] + P[v][j])
                )
                assert hit_two == (
                    Q(2) * P[v][i] * P[v][j]
                    * (2 + P[v][i] + P[v][j])
                    / (
                        (1 + P[v][i])
                        * (1 + P[v][j])
                        * (1 + P[v][i] + P[v][j])
                    )
                )
                creation_two += hit_two * edge[i][j]
        assert direct_lz == -2 * z_value + creation_one + creation_two
        assert direct_luz == rank_weight[holes_count] * direct_lz + commutator

    # Integrated generator and weighted-renewal checks.
    mean_uz = mean_v = mean_u_lz = mean_commutator = Q(0)
    for row, state in enumerate(states):
        probability = stationary[row]
        holes_count = n - state.bit_count()
        z_value = deficit(state)
        lz = sum(
            generator[row][column] * deficit(output)
            for column, output in enumerate(states)
        )
        luz = sum(
            generator[row][column]
            * rank_weight[n - output.bit_count()]
            * deficit(output)
            for column, output in enumerate(states)
        )
        mean_uz += probability * rank_weight[holes_count] * z_value
        mean_v += probability * dispersion(state)
        mean_u_lz += probability * rank_weight[holes_count] * lz
        mean_commutator += probability * (
            luz - rank_weight[holes_count] * lz
        )
    assert mean_u_lz + mean_commutator == 0

    # Exact stationary-flow split.  The set chain need not be reversible.
    symmetric_current = Q(0)
    circulation_current = Q(0)
    nonreversible_edges = 0
    for row, state in enumerate(states):
        for column in range(row + 1, len(states)):
            output = states[column]
            forward = stationary[row] * generator[row][column]
            backward = stationary[column] * generator[column][row]
            if forward != backward:
                nonreversible_edges += 1
            symmetric_flow = (forward + backward) / 2
            circulation = forward - backward
            delta_weight = (
                rank_weight[n - output.bit_count()]
                - rank_weight[n - state.bit_count()]
            )
            delta_deficit = deficit(output) - deficit(state)
            symmetric_current += (
                symmetric_flow * delta_weight * delta_deficit
            )
            circulation_current += (
                circulation
                * (
                    rank_weight[n - state.bit_count()]
                    + rank_weight[n - output.bit_count()]
                )
                * delta_deficit
                / 2
            )
    assert nonreversible_edges > 0
    assert mean_u_lz == -symmetric_current + circulation_current
    assert (
        symmetric_current,
        circulation_current,
        mean_u_lz,
        mean_v - mean_uz,
    ) == expected
    return symmetric_current


def verify_stationary_generator_and_circulation():
    path_current = verify_stationary_deficit_generator(
        [[0, 1, 0], [1, 0, 2], [0, 2, 0]],
        (Q(-13, 5400), Q(41, 5400), Q(1, 100), Q(2, 45)),
    )
    regular_current = verify_stationary_deficit_generator(
        [
            [0, 1, 1, 2],
            [1, 0, 2, 1],
            [1, 2, 0, 1],
            [2, 1, 1, 0],
        ],
        (Q(43, 34440), Q(97, 57400), Q(19, 43050), Q(1, 574)),
    )
    assert path_current < 0 < regular_current
    print("PASS: exact LZ and L(UZ) burst identities")
    print("PASS: dual circulation is nonzero and mixed Dirichlet sign changes")


if __name__ == "__main__":
    main()
    verify_test_set_collapse()
    verify_stationary_generator_and_circulation()
