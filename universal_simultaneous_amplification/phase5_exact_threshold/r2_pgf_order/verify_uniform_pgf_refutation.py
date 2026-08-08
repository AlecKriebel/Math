#!/usr/bin/env python3
"""Independent exact refutation of the uniform-baseline marked PGF order.

The verifier constructs the one-sample marked chain directly from its
definition and solves its invariant law over QQ with python-flint.  It does
not import the geometric-union dual or the phase-4 discovery implementation.
"""

from __future__ import annotations

from itertools import combinations

from flint import fmpq, fmpq_mat
from math import comb


def weight_matrix(n: int, edge_weights: tuple[int, ...]):
    assert len(edge_weights) == n * (n - 1) // 2
    weights = [[0 for _ in range(n)] for _ in range(n)]
    for (u, v), weight in zip(combinations(range(n), 2), edge_weights):
        weights[u][v] = weights[v][u] = weight
    return weights


def marked_chain(weights):
    n = len(weights)
    degrees = [sum(row) for row in weights]
    states = [
        (cache, target)
        for target in range(n)
        for cache in range(1 << n)
        if not cache >> target & 1
    ]
    index = {state: position for position, state in enumerate(states)}
    transition = fmpq_mat(len(states), len(states))
    for source, (cache, target) in enumerate(states):
        for sample in range(n):
            if not weights[target][sample]:
                continue
            probability = fmpq(weights[target][sample], degrees[target])
            active = cache | 1 << sample
            transition[source, index[active, target]] += probability / 2
            rank = active.bit_count()
            for new_target in range(n):
                if active >> new_target & 1:
                    destination = (active & ~(1 << new_target), new_target)
                    transition[source, index[destination]] += probability / (2 * rank)
        assert sum(transition[source, j] for j in range(len(states))) == 1
    return states, transition


def stationary_law(transition):
    size = transition.nrows()
    system = transition.transpose() - fmpq_mat(size, size, [
        int(i == j) for i in range(size) for j in range(size)
    ])
    rhs = fmpq_mat(size, 1)
    for j in range(size):
        system[size - 1, j] = 1
    rhs[size - 1, 0] = 1
    law = system.solve(rhs)
    assert transition.transpose() * law == law
    assert sum(law[i, 0] for i in range(size)) == 1
    assert all(law[i, 0] > 0 for i in range(size))
    return law


def stationary_rank_law(n, edge_weights):
    states, transition = marked_chain(weight_matrix(n, edge_weights))
    law = stationary_law(transition)
    eta = [fmpq(0) for _ in range(n)]
    for i, (cache, _) in enumerate(states):
        eta[cache.bit_count()] += law[i, 0]
    assert sum(eta) == 1
    assert sum(((-1) ** k) * eta[k] for k in range(n)) == 0
    return eta


def factor_quotient(eta):
    """Return Q with F_mu-F_K=(1-t^2)Q, checking exact division."""
    n = len(eta)
    delta = [eta[k] - fmpq(comb(n - 1, k), 2 ** (n - 1)) for k in range(n)]
    quotient = [fmpq(0) for _ in range(n - 2)]
    for k in range(n - 2):
        quotient[k] = delta[k] + (quotient[k - 2] if k >= 2 else 0)
    assert delta[n - 2] == -quotient[n - 4]
    assert delta[n - 1] == -quotient[n - 3]
    return delta, quotient


def derivative_polynomial(quotient):
    """Coefficients of A=E[t^(K-1)(N x-K)] from D=(1-t^2)Q."""
    N = len(quotient) + 1
    answer = [fmpq(0) for _ in quotient]
    for j in range(len(answer)):
        answer[j] += N * quotient[j]
        if j >= 1:
            answer[j] += (j + 1 - N) * quotient[j - 1]
        if j + 1 < len(quotient):
            answer[j] -= (j + 1) * quotient[j + 1]
    return answer


def active_law_from_marked(eta):
    q = [fmpq(0) for _ in range(len(eta) + 1)]
    for k in range(len(eta)):
        q[k + 1] = 2 * eta[k] - q[k]
    assert q[-1] == 0
    assert all(value >= 0 for value in q)
    assert sum(q) == 1
    return q


def main():
    # Lexicographic edge order (01,02,...,45).  This is the frozen reversible
    # six-vertex rank-tail witness, used here for a different exact sign.
    edges = (1, 3, 3, 1000, 30, 1000, 300, 3, 1, 10, 1, 30, 1, 300, 30)
    eta = stationary_rank_law(6, edges)
    gap_at_zero = eta[0] - fmpq(1, 32)
    assert gap_at_zero < 0

    # The weakest integrated psi target nevertheless has the required sign.
    psi = [
        2 * sum(fmpq((-1) ** (ell - 1 - j), ell) for ell in range(j + 1, 6))
        for j in range(6)
    ]
    inverse_mean = sum(eta[j] * psi[j] for j in range(6))
    complete_inverse_mean = fmpq(31, 80)
    collision_gap = inverse_mean - complete_inverse_mean
    assert collision_gap > 0

    # Polynomial division by 1-t^2 is exact because normalization and
    # stationary parity force roots at +1 and -1.
    _, quotient = factor_quotient(eta)
    assert quotient[0] < 0
    assert all(value > 0 for value in quotient[1:])
    integrated_gap = 2 * sum(
        quotient[k] * fmpq(1, (k + 1) * (k + 2)) for k in range(4)
    )
    assert integrated_gap == collision_gap
    active = active_law_from_marked(eta)
    complete_active = [fmpq(0)] + [
        fmpq(comb(4, k - 1), 16) for k in range(1, 6)
    ] + [fmpq(0)]
    for j, coefficient in enumerate(quotient):
        assert 2 * coefficient == (
            sum(active[1:j + 2]) - sum(complete_active[1:j + 2])
        )

    derivative_coefficients = derivative_polynomial(quotient)
    unweighted_derivative = sum(
        coefficient / (j + 1)
        for j, coefficient in enumerate(derivative_coefficients)
    )
    mean = 1 / inverse_mean
    singleton_mass = active[1] * mean
    assert unweighted_derivative == (5 + singleton_mass - 2 * mean) / (2 * mean)
    assert unweighted_derivative > 0

    # Independently freeze the supplied failure of the pointwise derivative
    # shortcut.  This graph actually obeys the full PGF order (all Q
    # coefficients are positive), but A(1/100)<0.
    derivative_edges = (7, 7, 7, 31, 2, 31, 1, 1, 31, 7)
    derivative_eta = stationary_rank_law(5, derivative_edges)
    _, derivative_q = factor_quotient(derivative_eta)
    assert all(value > 0 for value in derivative_q)
    derivative_a = derivative_polynomial(derivative_q)
    derivative_value = sum(
        coefficient * fmpq(1, 100) ** k
        for k, coefficient in enumerate(derivative_a)
    )
    assert derivative_value < 0

    # A six-vertex weighted path exactly refutes the stronger claim that all
    # nonconstant coefficients of A are nonnegative.  Path order is
    # 1-0-2-4-5-3 with consecutive weights (30,4,64,1,1860).
    path_edges = (30, 4, 0, 0, 0, 0, 0, 0, 0, 0, 64, 0, 0, 1860, 1)
    path_eta = stationary_rank_law(6, path_edges)
    _, path_q_polynomial = factor_quotient(path_eta)
    path_a = derivative_polynomial(path_q_polynomial)
    assert path_a[0] > 0 and path_a[1] < 0
    assert path_a[2] > 0 and path_a[3] > 0
    # Despite the failed coefficient sign, A itself is positive on [0,1]:
    # the only negative monomial is dominated already by the constant term.
    assert path_a[0] + path_a[1] > 0

    path_active = active_law_from_marked(path_eta)
    assert (5 - 2) * path_active[2] < 2 * path_active[3]

    print("PASS: direct 192-state QQ marked-chain solve")
    print("PASS: stationary parity and exact (1-t^2) factorization")
    print(f"PGF gap at t=0 = {gap_at_zero}")
    print(f"decimal PGF gap = {float(gap_at_zero):.15g} < 0")
    print(f"integrated collision gap = {collision_gap}")
    print(f"decimal collision gap = {float(collision_gap):.15g} > 0")
    print(f"derivative shortcut at t=1/100 = {derivative_value} < 0")
    print(f"path likelihood-ratio coefficient at rank two = {path_a[1]} < 0")
    print("EXACTLY REFUTED: uniform-baseline stationary PGF order")


if __name__ == "__main__":
    main()
