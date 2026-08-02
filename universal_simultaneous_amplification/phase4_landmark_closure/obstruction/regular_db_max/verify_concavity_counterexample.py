#!/usr/bin/env python3
"""Exact counterexample to global concavity on the regular-kernel polytope.

This does *not* counterexample complete-graph maximization: all three graphs
are suppressors.  It closes only the tempting permutation-averaging route.
"""

from __future__ import annotations

import sympy as sp


N = 7
FULL = (1 << N) - 1
EPSILON = sp.Rational(1, 200000)
LAMBDA = sp.Rational(1, 2000)


def half(value: int) -> sp.Rational:
    return sp.Rational(value, 2)


E = [
    [0, 0, 0, 0, half(1), 0, half(1)],
    [0, 0, 0, half(1), 0, half(1), 0],
    [0, 0, 0, 0, half(1), half(1), 0],
    [0, half(1), 0, 0, 0, 0, half(1)],
    [half(1), 0, half(1), 0, 0, 0, 0],
    [0, half(1), half(1), 0, 0, 0, 0],
    [half(1), 0, 0, half(1), 0, 0, 0],
]

F = [
    [0, 1, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, half(1), 0, 0, half(1)],
    [0, 0, half(1), 0, 0, 0, half(1)],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, half(1), half(1), 0, 0, 0],
]

K = [
    [sp.Integer(0) if i == j else sp.Rational(1, N - 1) for j in range(N)]
    for i in range(N)
]


def convex_combination(left, right, coefficient):
    return [
        [
            sp.cancel(coefficient * left[i][j] + (1 - coefficient) * right[i][j])
            for j in range(N)
        ]
        for i in range(N)
    ]


def fixation(weights) -> sp.Rational:
    """Build and solve all 126 labelled dB equations over QQ."""
    states = list(range(1, FULL))
    index = {state: row for row, state in enumerate(states)}
    matrix = sp.eye(len(states))
    rhs = sp.zeros(len(states), 1)
    for state, row in index.items():
        changes = []
        for target in range(N):
            mutant_mass = sum(
                weights[target][source]
                for source in range(N)
                if (state >> source) & 1
            )
            resident_mass = 1 - mutant_mass
            denominator = 2 * mutant_mass + resident_mass
            assert denominator > 0
            if (state >> target) & 1:
                rate = resident_mass / denominator
                new_state = state & ~(1 << target)
            else:
                rate = 2 * mutant_mass / denominator
                new_state = state | (1 << target)
            if rate:
                changes.append((new_state, sp.cancel(rate)))
        changing_mass = sum(rate for _, rate in changes)
        assert changing_mass > 0
        for new_state, rate in changes:
            probability = sp.cancel(rate / changing_mass)
            if new_state == FULL:
                rhs[row] += probability
            elif new_state:
                matrix[row, index[new_state]] -= probability

    matrix_domain = matrix.to_DM()
    rhs_domain = rhs.to_DM()
    numerator, denominator = matrix_domain.solve_den(rhs_domain, method="rref")
    # Keep the residual check in the exact polynomial-domain representation.
    # Multiplying the converted dense SymPy matrices is far more expensive
    # because it repeatedly canonicalizes several-thousand-bit rationals.
    assert matrix_domain * numerator == rhs_domain * denominator
    solution = numerator.to_Matrix() / denominator
    return sp.cancel(
        sum(solution[index[1 << vertex]] for vertex in range(N)) / N
    )


def main() -> None:
    first = convex_combination(E, K, 1 - EPSILON)
    second = convex_combination(F, K, 1 - EPSILON)
    midpoint = convex_combination(first, second, LAMBDA)

    for weights in (first, second, midpoint):
        assert all(weights[i][i] == 0 for i in range(N))
        assert all(weights[i][j] == weights[j][i] for i in range(N) for j in range(N))
        assert all(sum(weights[i]) == 1 for i in range(N))
        # The K_7 completion makes every off-diagonal entry strictly positive.
        assert all(weights[i][j] > 0 for i in range(N) for j in range(N) if i != j)

    rho_first = fixation(first)
    rho_second = fixation(second)
    rho_midpoint = fixation(midpoint)
    slack = sp.cancel(
        rho_midpoint
        - LAMBDA * rho_first
        - (1 - LAMBDA) * rho_second
    )
    complete = sp.Rational(64, 147)
    assert rho_first < complete
    assert rho_second < complete
    assert rho_midpoint < complete
    assert slack < 0

    numerator, denominator = sp.fraction(slack)
    print("PASS: three exact 126-state labelled dB solves")
    print("PASS: P, Q and lambda P+(1-lambda)Q are positive regular kernels")
    print(f"rho(P,2) = {sp.N(rho_first, 18)}")
    print(f"rho(Q,2) = {sp.N(rho_second, 18)}")
    print(f"rho(mixture,2) = {sp.N(rho_midpoint, 18)}")
    print(f"negative Jensen slack = {sp.N(slack, 18)}")
    print(f"exact Jensen slack = {slack}")
    print("EXACT CLAIM: rho(mixture) < lambda*rho(P)+(1-lambda)*rho(Q)")
    print("EXACT CLAIM: rho(P), rho(Q), rho(mixture) < rho(K_7,2)=64/147")
    print(
        "exact slack height: "
        f"numerator_bits={abs(int(numerator)).bit_length()} "
        f"denominator_bits={int(denominator).bit_length()}"
    )


if __name__ == "__main__":
    main()
