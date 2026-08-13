#!/usr/bin/env python3
"""Exact rational replay for the root-to-diffuse adjoint reduction.

The replay independently constructs

* physical Bd and dB subset generators;
* their linear multitype branching generators;
* the maximal common-clock chain killed at its first nonlinear defect;
* complete-graph fixation probabilities.

All arithmetic is fractions.Fraction.  No numerical tolerance is used.
"""

from fractions import Fraction as F
from itertools import combinations, product


def solve(a, b):
    """Solve a nonsingular rational linear system by Gauss--Jordan."""
    n = len(b)
    m = [list(a[i]) + [b[i]] for i in range(n)]
    for col in range(n):
        pivot = next(row for row in range(col, n) if m[row][col])
        m[col], m[pivot] = m[pivot], m[col]
        scale = m[col][col]
        m[col] = [x / scale for x in m[col]]
        for row in range(n):
            if row == col or not m[row][col]:
                continue
            scale = m[row][col]
            m[row] = [m[row][j] - scale * m[col][j]
                      for j in range(n + 1)]
    return [m[i][-1] for i in range(n)]


def subsets(n, minimum=1, maximum=None):
    if maximum is None:
        maximum = n
    return [frozenset(c) for k in range(minimum, maximum + 1)
            for c in combinations(range(n), k)]


def stochastic_matrix(weights):
    degree = [sum(row) for row in weights]
    return [[weights[i][j] / degree[i] for j in range(len(weights))]
            for i in range(len(weights))]


def verify_adjoint_parametrization(weights, p):
    """Check D_alpha^-1 P D_alpha=P^T and (P alpha)/alpha=t."""
    n = len(p)
    degree = [sum(row) for row in weights]
    volume = sum(degree)
    pi = [degree[i] / volume for i in range(n)]
    alpha = [volume / (n * degree[i]) for i in range(n)]
    temperature = [sum(p[j][i] for j in range(n)) for i in range(n)]
    assert all(pi[i] * alpha[i] == F(1, n) for i in range(n))
    for i in range(n):
        assert sum(p[i][j] * alpha[j] for j in range(n)) / alpha[i] == temperature[i]
        for j in range(n):
            assert p[i][j] * alpha[j] / alpha[i] == p[j][i]


def physical_rates(p, r, rule, state):
    """Effective physical transition rates from a mutant subset."""
    n = len(p)
    state = frozenset(state)
    rates = {}
    if rule == "Bd":
        for j in range(n):
            if j not in state:
                rate = r * sum(p[i][j] for i in state)
                if rate:
                    rates[state | {j}] = rate
        for i in state:
            rate = sum(p[j][i] for j in range(n) if j not in state)
            if rate:
                rates[state - {i}] = rate
    elif rule == "dB":
        x = [sum(p[j][i] for i in state) for j in range(n)]
        for j in range(n):
            denominator = 1 + (r - 1) * x[j]
            if j not in state:
                rate = r * x[j] / denominator
                if rate:
                    rates[state | {j}] = rate
            else:
                rate = (1 - x[j]) / denominator
                if rate:
                    rates[state - {j}] = rate
    else:
        raise ValueError(rule)
    return rates


def branch_rates(p, r, rule, counts):
    """Transition rates of the independent-particle branching process."""
    n = len(p)
    temperature = [sum(p[j][i] for j in range(n)) for i in range(n)]
    rates = {}
    for i, number in enumerate(counts):
        if not number:
            continue
        death = temperature[i] if rule == "Bd" else F(1)
        child = p[i] if rule == "Bd" else [p[j][i] for j in range(n)]
        down = list(counts)
        down[i] -= 1
        down = tuple(down)
        rates[down] = rates.get(down, F(0)) + number * death
        for j in range(n):
            up = list(counts)
            up[j] += 1
            up = tuple(up)
            rates[up] = rates.get(up, F(0)) + number * r * child[j]
    return rates


def defect_rate(p, r, rule, state):
    n = len(p)
    state = frozenset(state)
    interaction = sum(p[i][j] for i in state for j in state)
    if rule == "Bd":
        return (r + 1) * interaction
    x = [sum(p[j][i] for i in state) for j in range(n)]
    occupied_loss = sum(r * x[i] / (1 + (r - 1) * x[i])
                        for i in state)
    resident_nonlinearity = sum(
        r * (r - 1) * x[j] * x[j] / (1 + (r - 1) * x[j])
        for j in range(n) if j not in state
    )
    return r * interaction + occupied_loss + resident_nonlinearity


def verify_rate_decomposition(p, r):
    """Check every displayed defect formula against transition differences."""
    n = len(p)
    temperature = [sum(p[j][i] for j in range(n)) for i in range(n)]
    for state in subsets(n, 1, n - 1):
        interaction = sum(p[i][j] for i in state for j in state)

        # Bd: resident additions are common.  The two unmatched families are
        # births onto occupied targets and suppressed branching deaths.
        collision = r * interaction
        suppressed_death = sum(
            temperature[i]
            - sum(p[j][i] for j in range(n) if j not in state)
            for i in state
        )
        assert suppressed_death == interaction
        assert collision + suppressed_death == defect_rate(p, r, "Bd", state)

        # dB: compare every physical state-changing rate with its branching
        # counterpart, then add births whose target is already occupied.
        x = [sum(p[j][i] for i in state) for j in range(n)]
        difference = r * sum(x[i] for i in state)
        physical = physical_rates(p, r, "dB", state)
        for j in range(n):
            if j not in state:
                branch = r * x[j]
                actual = physical.get(state | {j}, F(0))
                assert branch >= actual
                difference += branch - actual
            else:
                branch = F(1)
                actual = physical.get(state - {j}, F(0))
                assert branch >= actual
                difference += branch - actual
        assert difference == defect_rate(p, r, "dB", state)


def hit_probability(states, rate_function, boundary_size, initial_states):
    """Hit population boundary_size before zero in a finite CTMC."""
    index = {state: i for i, state in enumerate(states)}
    matrix = [[F(0) for _ in states] for _ in states]
    rhs = [F(0) for _ in states]
    for state, row in index.items():
        rates = rate_function(state)
        total = sum(rates.values())
        assert total > 0
        matrix[row][row] = total
        for target, rate in rates.items():
            size = len(target) if isinstance(target, frozenset) else sum(target)
            if size >= boundary_size:
                rhs[row] += rate
            elif size:
                matrix[row][index[target]] -= rate
    values = solve(matrix, rhs)
    return sum(weight * values[index[state]] for state, weight in initial_states)


def physical_hit(p, r, rule, boundary_size):
    n = len(p)
    states = subsets(n, 1, boundary_size - 1)
    initial = [(frozenset({i}), F(1, n)) for i in range(n)]
    return hit_probability(
        states,
        lambda state: physical_rates(p, r, rule, state),
        boundary_size,
        initial,
    )


def weak_compositions_below(n, boundary_size):
    return [counts for counts in product(range(boundary_size), repeat=n)
            if 1 <= sum(counts) < boundary_size]


def branching_hit(p, r, rule, boundary_size):
    n = len(p)
    states = weak_compositions_below(n, boundary_size)
    initial = []
    for i in range(n):
        counts = tuple(1 if j == i else 0 for j in range(n))
        initial.append((counts, F(1, n)))
    return hit_probability(
        states,
        lambda counts: branch_rates(p, r, rule, counts),
        boundary_size,
        initial,
    )


def coupling_defect_probability(p, r, rule, boundary_size):
    """Solve the killed common-clock Green system for chi_U(K)."""
    n = len(p)
    states = subsets(n, 1, boundary_size - 1)
    index = {state: i for i, state in enumerate(states)}
    matrix = [[F(0) for _ in states] for _ in states]
    defect = [F(0) for _ in states]
    for state, row in index.items():
        common = physical_rates(p, r, rule, state)
        delta = defect_rate(p, r, rule, state)
        total = sum(common.values()) + delta
        matrix[row][row] = total
        defect[row] = delta
        for target, rate in common.items():
            if 0 < len(target) < boundary_size:
                matrix[row][index[target]] -= rate
    green_defect = solve(matrix, defect)
    chi = sum(green_defect[index[frozenset({i})]] for i in range(n)) / n

    # Independent first-step reconstruction of the same absorbing committor.
    for state, row in index.items():
        common = physical_rates(p, r, rule, state)
        lhs = (sum(common.values()) + defect[row]) * green_defect[row]
        rhs = defect[row]
        for target, rate in common.items():
            if 0 < len(target) < boundary_size:
                rhs += rate * green_defect[index[target]]
        assert lhs == rhs
    return chi


def fixation_probability(p, r, rule):
    return physical_hit(p, r, rule, len(p))


def complete_baseline(n, r, rule):
    p0 = (r - 1) / r
    if rule == "Bd":
        return p0 / (1 - r ** (-n))
    return p0 * F(n - 1, n) / (1 - r ** (-(n - 1)))


def main():
    r = F(3, 2)

    # A genuinely nonregular undirected kernel checks every P-versus-P^T
    # orientation in the rates and in the reversible adjoint transform.
    nonregular_weights = [
        [F(0), F(1), F(2), F(1)],
        [F(1), F(0), F(3), F(1)],
        [F(2), F(3), F(0), F(4)],
        [F(1), F(1), F(4), F(0)],
    ]
    nonregular_p = stochastic_matrix(nonregular_weights)
    verify_adjoint_parametrization(nonregular_weights, nonregular_p)
    verify_rate_decomposition(nonregular_p, r)
    for rule in ("Bd", "dB"):
        physical = physical_hit(nonregular_p, r, rule, 3)
        branching = branching_hit(nonregular_p, r, rule, 3)
        chi = coupling_defect_probability(nonregular_p, r, rule, 3)
        assert abs(physical - branching) <= chi

    # A nonuniform but weighted-regular K4.  Opposite edges have equal
    # weights, so all degrees are six while the transition rows are not
    # uniform.  This tests orientations without using an isothermal matrix
    # entry-by-entry.
    weights = [
        [F(0), F(1), F(2), F(3)],
        [F(1), F(0), F(3), F(2)],
        [F(2), F(3), F(0), F(1)],
        [F(3), F(2), F(1), F(0)],
    ]
    p = stochastic_matrix(weights)
    assert all(sum(row) == 1 for row in p)
    assert all(sum(p[j][i] for j in range(4)) == 1 for i in range(4))

    verify_adjoint_parametrization(weights, p)
    verify_rate_decomposition(p, r)

    cutoff = 3
    for rule in ("Bd", "dB"):
        physical = physical_hit(p, r, rule, cutoff)
        branching = branching_hit(p, r, rule, cutoff)
        chi = coupling_defect_probability(p, r, rule, cutoff)
        assert abs(physical - branching) <= chi

        # Here the branching survival vector is constant p0 because P is
        # doubly stochastic.  This checks rho <= bar_u + theta + chi.
        p0 = (r - 1) / r
        theta = branching - p0
        rho = fixation_probability(p, r, rule)
        assert theta >= 0
        assert rho <= p0 + theta + chi

    # Independently reconstruct both complete-graph baselines from the full
    # subset chains at two orders.
    for n in (3, 4):
        complete_weights = [
            [F(0) if i == j else F(1) for j in range(n)]
            for i in range(n)
        ]
        complete_p = stochastic_matrix(complete_weights)
        for rule in ("Bd", "dB"):
            exact = fixation_probability(complete_p, r, rule)
            assert exact == complete_baseline(n, r, rule)

    # Exact elementary bounds used in the response inequality.
    a = r - 1
    p0 = a / r
    for n in range(8, 25):
        kappa_b = complete_baseline(n, r, "Bd")
        kappa_d = complete_baseline(n, r, "dB")
        assert (kappa_d - p0) + a * (kappa_b - p0) >= -2 * p0 / n
        for delta_b, delta_d in ((F(1, 100), F(1, 200)),
                                 (F(1, 200), F(1, 100))):
            epsilon = max(delta_b, delta_d)
            assert (kappa_d * delta_d + a * kappa_b * delta_b
                    >= a * p0 * epsilon / 2)

    print("PASS: exact reversible-adjoint orientation identities")
    print("PASS: exact physical/branching defect-rate decompositions")
    print("PASS: exact killed-Green coupling inequalities")
    print("PASS: exact Bd/dB complete-graph baselines")
    print("PASS: exact response-scale algebra used in (26)")


if __name__ == "__main__":
    main()
