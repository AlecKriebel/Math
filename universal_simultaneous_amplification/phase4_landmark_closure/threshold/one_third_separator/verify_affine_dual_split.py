#!/usr/bin/env python3
"""Independent exact verifier for the affine L--C--D split and obstruction."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve()
THRESHOLD = HERE.parents[1]
HOSTILE = THRESHOLD / "endpoint_hostile_exact"
OBSTRUCTION = THRESHOLD.parent / "obstruction"
sys.path.insert(0, str(HOSTILE))
sys.path.insert(0, str(OBSTRUCTION))

from verify_endpoint_candidates import (  # noqa: E402
    complete_baseline,
    exact_fixation,
    graph,
)
import verify_exact_duals as duals  # noqa: E402


R = sp.Rational(3, 2)
A = R - 1


def transition_kernel(weights):
    degrees = [sum(row, sp.Integer(0)) for row in weights]
    return [
        [sp.cancel(weights[i][j] / degrees[i]) for j in range(len(weights))]
        for i in range(len(weights))
    ]


def exact_link_fixation(q):
    """Uniform-singleton fixation for labelled arrow rates q[parent][target]."""
    n = len(q)
    full = (1 << n) - 1
    matrix = sp.eye(full - 1)
    rhs = sp.zeros(full - 1, 1)
    for state in range(1, full):
        changes = defaultdict(lambda: sp.Integer(0))
        for target in range(n):
            target_mutant = bool(state & (1 << target))
            rate = sum(
                q[parent][target]
                for parent in range(n)
                if bool(state & (1 << parent)) != target_mutant
            )
            if not target_mutant:
                rate *= R
            if rate:
                changes[state ^ (1 << target)] += sp.cancel(rate)
        total = sp.cancel(sum(changes.values(), sp.Integer(0)))
        assert total > 0
        for target, rate in changes.items():
            probability = sp.cancel(rate / total)
            if target == full:
                rhs[state - 1] += probability
            elif target:
                matrix[state - 1, target - 1] -= probability
    solution = tuple(next(iter(sp.linsolve((matrix, rhs)))))
    assert matrix * sp.Matrix(solution) == rhs
    return sp.cancel(
        sum(solution[(1 << vertex) - 1] for vertex in range(n)) / n
    )


def poisson_solution(generator, mean, mu):
    count = generator.rows
    cardinality = sp.Matrix([(state + 1).bit_count() for state in range(count)])
    original_rhs = cardinality - mean * sp.ones(count, 1)
    matrix = -generator.copy()
    rhs = original_rhs.copy()
    matrix[-1, :] = mu.T
    rhs[-1] = 0
    answer = matrix.inv() * rhs
    assert sp.cancel((mu.T * answer)[0]) == 0
    assert -generator * answer == original_rhs
    return answer


def verify_poisson_identity():
    # A small asymmetric graph checks (7)--(8) independently of the
    # absorption-chain implementation used for the order-six obstruction.
    weights = graph(3, [(0, 2, 1), (1, 2, 17)])
    n = len(weights)
    l_generator = duals.dual_generator(weights, R, "Bd")
    c_generator = duals.reversed_arrow_generator(weights, R)
    pi_l = sp.Matrix(duals.stationary(l_generator))
    pi_c = sp.Matrix(duals.stationary(c_generator))
    cardinality = sp.Matrix(
        [(state + 1).bit_count() for state in range((1 << n) - 1)]
    )
    m_l = sp.cancel((pi_l.T * cardinality)[0])
    m_c = sp.cancel((pi_c.T * cardinality)[0])
    normalization = (1 + A) ** n - 1
    mu = sp.Matrix(
        [A ** (state + 1).bit_count() / normalization for state in range((1 << n) - 1)]
    )
    b = sp.cancel(n * A * (1 + A) ** (n - 1) / normalization)
    chi_l = poisson_solution(l_generator, m_l, mu)
    chi_c = poisson_solution(c_generator, m_c, mu)

    p = transition_kernel(weights)
    temperature_defect = [
        sp.cancel(1 - sum(p[j][i] for j in range(n))) for i in range(n)
    ]
    potential = sp.Matrix(
        [
            R
            * sum(
                temperature_defect[i]
                for i in range(n)
                if ((state + 1) >> i) & 1
            )
            for state in range((1 << n) - 1)
        ]
    )
    psi = chi_c - A * chi_l
    pairing = sp.cancel(sum(mu[i] * potential[i] * psi[i] for i in range(len(mu))))
    gap = sp.cancel(R * b - A * m_l - m_c)
    assert pairing == gap

    degree = [sum(row, sp.Integer(0)) for row in weights]
    marginal = [
        sp.cancel(
            sum(
                mu[state - 1] * psi[state - 1]
                for state in range(1, 1 << n)
                if (state >> i) & 1
            )
        )
        for i in range(n)
    ]
    dirichlet = sp.cancel(
        R
        * sum(
            weights[i][j]
            * (1 / degree[i] - 1 / degree[j])
            * (marginal[i] - marginal[j])
            for i in range(n)
            for j in range(i + 1, n)
        )
    )
    assert dirichlet == gap


def verify_orientation_obstruction():
    weights = graph(
        6,
        [
            (0, 1, 1),
            (1, 2, 6_000_000_000),
            (2, 3, 4_000_000),
            (3, 4, 5_000_000_000),
            (4, 5, 20_000),
            (5, 0, 7_000_000_000),
        ],
    )
    p = transition_kernel(weights)
    rho_l = exact_link_fixation(p)
    rho_c = exact_link_fixation([list(column) for column in zip(*p)])
    rho_d = exact_fixation(weights, "dB")
    baseline_b = complete_baseline(6, "Bd")
    baseline_d = complete_baseline(6, "dB")
    x = sp.cancel(rho_l / baseline_b)
    z = sp.cancel(rho_c / baseline_b)
    y = sp.cancel(rho_d / baseline_d)
    orientation = sp.cancel((x + 2 * z) / 3 - 1)
    batching = sp.cancel(y - z)
    target = sp.cancel((x + 2 * y) / 3 - 1)
    assert orientation > 0
    assert batching < 0
    assert target < 0
    assert target == sp.cancel(orientation + sp.Rational(2, 3) * batching)
    print(f"x~{sp.N(x, 20)}")
    print(f"z~{sp.N(z, 20)}")
    print(f"y~{sp.N(y, 20)}")
    print(f"orientation_excess~{sp.N(orientation, 20)}")
    print(f"batching_difference~{sp.N(batching, 20)}")
    print(f"one_third_excess~{sp.N(target, 20)}")
    print(
        "orientation_certificate_digits="
        f"{len(str(sp.numer(orientation)))}/{len(str(sp.denom(orientation)))}"
    )


def main():
    verify_poisson_identity()
    verify_orientation_obstruction()
    print("PASS exact affine dual split")
    print("PASS exact Poisson--Dirichlet orientation identity")
    print("PASS exact order-six refutation of separate orientation sign")
    print("PASS actual one-third separator survives by batching cancellation")


if __name__ == "__main__":
    main()
