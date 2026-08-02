#!/usr/bin/env python3
"""Independent exact checks for the r=2 Green--collision reduction.

Only the Python standard library is used.  Every Markov-chain solve is over
fractions.Fraction; no floating-point value is used in an assertion.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations
from math import comb


def popcount(state):
    return bin(state).count("1")


def solve(matrix, rhs):
    """Solve a square rational system by Gauss--Jordan elimination."""
    n = len(rhs)
    aug = [list(matrix[i]) + [rhs[i]] for i in range(n)]
    for col in range(n):
        pivot = next(row for row in range(col, n) if aug[row][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        for row in range(n):
            if row == col or not aug[row][col]:
                continue
            scale = aug[row][col]
            aug[row] = [
                aug[row][j] - scale * aug[col][j] for j in range(n + 1)
            ]
    return [aug[i][-1] for i in range(n)]


def h(x):
    return 2 * x / (1 + x)


def transition(weights):
    degrees = [sum(row) for row in weights]
    assert all(degree > 0 for degree in degrees)
    return [
        [F(weights[v][u], degrees[v]) for u in range(len(weights))]
        for v in range(len(weights))
    ]


def geometric_union_law(row):
    """Law of the distinct union of Geom(1/2) row samples."""
    support = [u for u, value in enumerate(row) if value]
    law = {}
    for size in range(1, len(support) + 1):
        for chosen in combinations(support, size):
            probability = F(0)
            for subsize in range(size + 1):
                for subset in combinations(chosen, subsize):
                    mass = sum((row[u] for u in subset), F(0))
                    pgf = mass / (2 - mass) if mass else F(0)
                    probability += (-1) ** (size - subsize) * pgf
            if probability:
                mask = sum(1 << u for u in chosen)
                law[mask] = probability
    assert sum(law.values(), F(0)) == 1
    assert all(value > 0 for value in law.values())
    return law


def stationary_dual(P):
    n = len(P)
    full = (1 << n) - 1
    laws = [geometric_union_law(P[v]) for v in range(n)]
    Q = [[F(0) for _ in range(full)] for _ in range(full)]
    for state in range(1, full + 1):
        source = state - 1
        for target in range(n):
            if not ((state >> target) & 1):
                continue
            without = state & ~(1 << target)
            for union, probability in laws[target].items():
                output = without | union
                if output == state:
                    continue
                Q[source][output - 1] += probability
                Q[source][source] -= probability
    equations = [[Q[col][row] for col in range(full)] for row in range(full)]
    equations[-1] = [F(1)] * full
    rhs = [F(0)] * full
    rhs[-1] = F(1)
    pi = solve(equations, rhs)
    assert all(value >= 0 for value in pi)
    assert sum(pi, F(0)) == 1
    for col in range(full):
        assert sum(pi[row] * Q[row][col] for row in range(full)) == 0
    return pi


def proper_dual_generator(P):
    """Exact dual generator restricted to its closed proper-set class."""
    n = len(P)
    full = (1 << n) - 1
    states = list(range(1, full))
    index = {state: pos for pos, state in enumerate(states)}
    laws = [geometric_union_law(P[v]) for v in range(n)]
    Q = [[F(0) for _ in states] for _ in states]
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
                Q[source][index[output]] += probability
                Q[source][source] -= probability
    return states, Q


def forward_fixation(P):
    n = len(P)
    full = (1 << n) - 1
    states = list(range(1, full))
    index = {state: pos for pos, state in enumerate(states)}
    matrix = [[F(0) for _ in states] for _ in states]
    rhs = [F(0) for _ in states]
    for state in states:
        row = index[state]
        for target in range(n):
            mass = sum(
                (P[target][u] for u in range(n) if (state >> u) & 1),
                F(0),
            )
            mutant_probability = h(mass)
            if (state >> target) & 1:
                rate = 1 - mutant_probability
                output = state & ~(1 << target)
            else:
                rate = mutant_probability
                output = state | (1 << target)
            if not rate:
                continue
            matrix[row][row] += rate
            if output == full:
                rhs[row] += rate
            elif output:
                matrix[row][index[output]] -= rate
    transient = solve(matrix, rhs)
    fixation = [F(0)] * (full + 1)
    fixation[full] = F(1)
    for state, value in zip(states, transient):
        fixation[state] = value
    assert all(F(0) <= value <= F(1) for value in fixation)
    return fixation


def complete_data(n):
    denominator = 1 - F(1, 2) ** (n - 1)
    phi = [
        (1 - F(n + k, n * 2**k)) / denominator for k in range(n + 1)
    ]
    assert phi[0] == 0 and phi[n] == 1
    rho = phi[1]
    assert rho == F((n - 1) * 2 ** (n - 2), n * (2 ** (n - 1) - 1))
    mu = [F(0)] * (n + 1)
    for k in range(1, n):
        mu[k] = (
            F(n + k, 2 * n) - F(2) ** (k - n)
        ) / (n * comb(n - 2, k - 1) * denominator)
        assert mu[k] > 0
    coefficients = [mu[k] + mu[k + 1] for k in range(n)]
    return phi, rho, mu, coefficients


def pair_bound_data(weights, source, hole):
    """Return the exact proposed stationary pair-bound data.

    The proposed upper bound is

        Pr(source in A, hole not in A)
        <= (1 + P[source][hole]) p_source (1-p_hole).

    Its margin is returned as right side minus left side.
    """
    n = len(weights)
    full = (1 << n) - 1
    P = transition(weights)
    pi = stationary_dual(P)
    marginals = [
        sum(
            pi[state - 1]
            for state in range(1, full + 1)
            if (state >> vertex) & 1
        )
        for vertex in range(n)
    ]
    crossing = sum(
        pi[state - 1]
        for state in range(1, full + 1)
        if (state >> source) & 1 and not ((state >> hole) & 1)
    )
    proposed_upper = (
        (1 + P[source][hole])
        * marginals[source]
        * (1 - marginals[hole])
    )
    component_slacks = [
        2 * sum(P[v][i] * marginals[v] for v in range(n))
        - marginals[i] / (1 - marginals[i])
        for i in range(n)
    ]
    return (
        P[source][hole],
        marginals,
        crossing,
        proposed_upper,
        proposed_upper - crossing,
        component_slacks,
    )


def check_pair_bound_counterexamples():
    """Certify that both the nonedge and positive-edge pair bounds fail."""
    # The unweighted path 0--1--2--3 violates the proposed P_03=0 case.
    path = [
        [0, 1, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [0, 0, 1, 0],
    ]
    path_data = pair_bound_data(path, 0, 3)
    assert path_data[0] == 0
    assert path_data[1] == [F(2, 7), F(33, 70), F(33, 70), F(2, 7)]
    assert path_data[2] == F(16, 77)
    assert path_data[3] == F(10, 49)
    assert path_data[4] == F(-2, 539)
    assert all(slack > 0 for slack in path_data[5])

    # A positive regular K4 counterexample.  Edges 02 and 13 have weight 18;
    # every other edge has weight 1.  The weak edge 01 has P_01=1/20.
    weighted_complete = [
        [0, 1, 18, 1],
        [1, 0, 1, 18],
        [18, 1, 0, 1],
        [1, 18, 1, 0],
    ]
    weighted_data = pair_bound_data(weighted_complete, 0, 1)
    assert weighted_data[0] == F(1, 20)
    assert weighted_data[1] == [F(827, 2026)] * 4
    assert weighted_data[2] == F(1029, 4052)
    assert weighted_data[3] == F(20823033, 82093520)
    assert weighted_data[4] == F(-24507, 82093520)
    assert weighted_data[5] == [F(153822, 1214587)] * 4

    print(
        "PASS: pair bound is false on P4 and on a positive regular K4; "
        "the summed component-odds target is not refuted"
    )


def evaluate(weights, expected):
    n = len(weights)
    N = n - 1
    full = (1 << n) - 1
    P = transition(weights)
    pi = stationary_dual(P)
    forward = forward_fixation(P)

    # Independent Boolean-coverage recovery of every forward committor.
    covered = [F(0)] * (full + 1)
    for initial in range(1, full + 1):
        covered[initial] = sum(
            pi[dual - 1] for dual in range(1, full + 1) if dual & initial
        )
    assert covered == forward

    mean = sum(F(popcount(state)) * pi[state - 1] for state in range(1, full + 1))
    rho = mean / n
    assert rho == sum(forward[1 << v] for v in range(n)) / n

    D = [F(0)] * n
    W = [F(0)] * n
    for k in range(n):
        for state in range(full + 1):
            if popcount(state) != k:
                continue
            for target in range(n):
                if (state >> target) & 1:
                    continue
                output = state | (1 << target)
                delta = forward[output] - forward[state]
                assert delta >= 0
                mass = sum(
                    (P[target][u] for u in range(n) if (state >> u) & 1),
                    F(0),
                )
                D[k] += delta
                W[k] += h(mass) * delta

    # Coverage formulas (5)--(6), checked independently of the edge sums.
    for k in range(n):
        d_coverage = F(0)
        w_coverage = F(0)
        for dual in range(1, full + 1):
            probability = pi[dual - 1]
            size = popcount(dual)
            holes = [u for u in range(n) if not ((dual >> u) & 1)]
            d_coverage += probability * size * comb(len(holes), k)
            for target in range(n):
                if not ((dual >> target) & 1):
                    continue
                for subset in combinations(holes, k):
                    mass = sum((P[target][u] for u in subset), F(0))
                    w_coverage += probability * h(mass)
        assert d_coverage == D[k]
        assert w_coverage == W[k]

    for k in range(1, n):
        assert W[k] + W[k - 1] == D[k - 1]

    _, rho_complete, mu, coefficients = complete_data(n)
    residuals = [
        W[k] - F(2 * k, N + k) * D[k] for k in range(n)
    ]
    assert residuals[0] == residuals[-1] == 0
    green_gap = sum(
        coefficients[k] * residuals[k] for k in range(n)
    )
    assert green_gap == rho - rho_complete

    U = [F(0)] * n
    for holes in range(1, n):
        U[holes] = sum(
            coefficients[k]
            * F(2 * N * N, (N + k) ** 2)
            * comb(holes - 1, k - 1)
            for k in range(1, holes + 1)
        )

    linear = F(0)
    dispersion = F(0)
    dispersion_by_state = {}
    surplus_by_state = {}
    for dual in range(1, full + 1):
        probability = pi[dual - 1]
        size = popcount(dual)
        holes = [u for u in range(n) if not ((dual >> u) & 1)]
        hole_count = len(holes)
        if not holes:
            continue
        cut = sum(
            (
                P[target][u]
                for target in range(n)
                if (dual >> target) & 1
                for u in holes
            ),
            F(0),
        )
        surplus = cut - F(size * hole_count, N)
        surplus_by_state[dual] = surplus
        linear += probability * U[hole_count] * surplus
        conditional_dispersion = F(0)
        for k in range(1, hole_count + 1):
            baseline = F(k, N)
            factor = coefficients[k] * F(2, 1) / (1 + baseline) ** 2
            for target in range(n):
                if not ((dual >> target) & 1):
                    continue
                for subset in combinations(holes, k):
                    mass = sum((P[target][u] for u in subset), F(0))
                    conditional_dispersion += (
                        factor
                        * (mass - baseline) ** 2
                        / (1 + mass)
                    )
        dispersion_by_state[dual] = conditional_dispersion
        dispersion += probability * conditional_dispersion
    assert dispersion >= 0
    assert rho - rho_complete == linear - dispersion

    # Levelwise reference centering of the internal-pair/cut surplus, and
    # the all-holes-atom quadratic lower bound (25)--(27).
    for size in range(1, n):
        level_sum = F(0)
        for dual in range(1, full):
            if popcount(dual) != size:
                continue
            holes = [u for u in range(n) if not ((dual >> u) & 1)]
            cut = sum(
                (
                    P[target][u]
                    for target in range(n)
                    if (dual >> target) & 1
                    for u in holes
                ),
                F(0),
            )
            level_sum += cut - F(size * len(holes), N)
        assert level_sum == 0

    quadratic_lower = F(0)
    expected_surplus = F(0)
    singleton_dispersion = F(0)
    second_moment = F(0)
    for dual in range(1, full):
        probability = pi[dual - 1]
        size = popcount(dual)
        second_moment += probability * size**2
        holes = [u for u in range(n) if not ((dual >> u) & 1)]
        hole_count = len(holes)
        cut = sum(
            (
                P[target][u]
                for target in range(n)
                if (dual >> target) & 1
                for u in holes
            ),
            F(0),
        )
        surplus = cut - F(size * hole_count, N)
        expected_surplus += probability * surplus
        singleton_dispersion += probability * sum(
            (
                (P[target][u] - F(1, N)) ** 2 / (1 + P[target][u])
                for target in range(n)
                if (dual >> target) & 1
                for u in holes
            ),
            F(0),
        )
        quadratic_lower += (
            probability
            * coefficients[hole_count]
            * surplus**2
            / (size * (1 + F(hole_count, N)) ** 2)
        )
    assert dispersion >= quadratic_lower
    assert expected_surplus - singleton_dispersion == F(n, N * N) * (
        second_moment - F(n, 2) * mean
    )

    # Complete Poisson/Dirichlet representation (28)--(30).
    proper_states, actual_dual = proper_dual_generator(P)
    complete_P = [
        [F(0) if v == u else F(1, N) for u in range(n)]
        for v in range(n)
    ]
    complete_states, complete_dual = proper_dual_generator(complete_P)
    assert proper_states == complete_states
    forcing = [
        U[n - popcount(state)] * surplus_by_state[state]
        for state in proper_states
    ]
    poisson_matrix = [row[:] for row in complete_dual]
    poisson_rhs = forcing[:]
    poisson_matrix[-1] = [F(0)] * len(proper_states)
    poisson_matrix[-1][0] = F(1)
    poisson_rhs[-1] = F(0)
    psi = solve(poisson_matrix, poisson_rhs)
    for row in range(len(proper_states) - 1):
        assert sum(complete_dual[row][col] * psi[col] for col in range(len(psi))) == forcing[row]
    dirichlet = []
    for row in range(len(proper_states)):
        value = sum(
            (complete_dual[row][col] - actual_dual[row][col]) * psi[col]
            for col in range(len(psi))
        )
        dirichlet.append(value)
    assert sum(
        pi[state - 1] * dirichlet[row]
        for row, state in enumerate(proper_states)
    ) == linear
    for state, value in expected.get("dirichlet_residuals", {}).items():
        row = proper_states.index(state)
        assert dispersion_by_state[state] - dirichlet[row] == value

    # Exact factorial hit hierarchy (23) and row-local bounds (26).
    B_expectation = [F(0)] * n
    rhs_expectation = [F(0)] * n
    for dual in range(1, full + 1):
        probability = pi[dual - 1]
        size = popcount(dual)
        holes = [u for u in range(n) if not ((dual >> u) & 1)]
        B = [F(0)] * n
        for j in range(1, n):
            for target in range(n):
                if not ((dual >> target) & 1):
                    continue
                for subset in combinations(holes, j):
                    mass = sum((P[target][u] for u in subset), F(0))
                    B[j] += h(mass)
            if j <= len(holes):
                lower = F(j + 1, 2 * j) * comb(len(holes) - 1, j - 1) * B[1]
                upper = comb(len(holes) - 1, j - 1) * B[1]
                assert lower <= B[j] <= upper
            B_expectation[j] += probability * B[j]
            rhs_expectation[j] += probability * size * comb(len(holes), j - 1)
    for j in range(1, n):
        assert B_expectation[j] + B_expectation[j - 1] == rhs_expectation[j]

    assert rho == expected["rho"]
    assert rho_complete == expected["rho_complete"]
    assert residuals[1 : n - 1] == expected["residuals"]
    assert linear == expected["linear"]
    assert dispersion == expected["dispersion"]
    assert rho - rho_complete == expected["gap"]
    print(
        f"PASS n={n}: rho={rho}, gap={rho-rho_complete}, "
        f"L={linear}, V={dispersion}"
    )


def main():
    evaluate(
        [[0, 1, 0], [1, 0, 2], [0, 2, 0]],
        {
            "rho": F(2, 5),
            "rho_complete": F(4, 9),
            "residuals": [F(-2, 15)],
            "linear": F(2, 135),
            "dispersion": F(8, 135),
            "gap": F(-2, 45),
            "dirichlet_residuals": {3: F(-16, 4455)},
        },
    )
    evaluate(
        [[0, 1, 1, 2], [1, 0, 2, 1], [1, 2, 0, 1], [2, 1, 1, 0]],
        {
            "rho": F(35, 82),
            "rho_complete": F(3, 7),
            "residuals": [F(-1, 82), F(1, 205)],
            "linear": F(207, 22960),
            "dispersion": F(247, 22960),
            "gap": F(-1, 574),
        },
    )
    check_pair_bound_counterexamples()
    print("PASS: all exact Green, collision, and counterexample checks")


if __name__ == "__main__":
    main()
