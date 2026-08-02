#!/usr/bin/env python3
"""Exact diagnostics for the open occupied-event rank reflection.

The script proves the finite combinatorial formulas by exhaustive rational
evaluation and checks the open inequalities only on the explicitly listed
graphs.  Its output labels the latter as diagnostics.
"""

from __future__ import annotations

import math
import pathlib
import sys

import sympy as sp

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from verify_exact_duals import (  # noqa: E402
    dual_generator,
    geometric_union_probabilities,
    stationary,
)


def transition(weights):
    n = len(weights)
    degrees = [sum(map(sp.sympify, row), sp.Integer(0)) for row in weights]
    return [
        [sp.sympify(weights[i][j]) / degrees[i] for j in range(n)]
        for i in range(n)
    ]


def event_kernel(weights, fitness):
    n = len(weights)
    full = (1 << n) - 1
    rows = transition(weights)
    laws = [geometric_union_probabilities(row, fitness) for row in rows]
    kernel = sp.zeros(full, full)
    for state in range(1, full + 1):
        size = state.bit_count()
        for target in range(n):
            if not ((state >> target) & 1):
                continue
            without = state & ~(1 << target)
            for union, probability in laws[target].items():
                kernel[state - 1, (without | union) - 1] += probability / size
    assert all(sum(kernel.row(i)) == 1 for i in range(full))
    return kernel, laws


def closed_conditional_coefficient(n, union_size, level, a):
    N = n - 1
    s = union_size
    prefactor = a ** (1 - s) * (1 + a) ** (s - 1)
    total = sp.Integer(0)
    for h_inside in range(s + 1):
        for h_outside in range(N - s + 1):
            output_size = s + h_outside
            if output_size != level:
                continue
            source_h = h_inside + h_outside
            new_outside = s - h_inside
            total += (
                sp.binomial(s, h_inside)
                * sp.binomial(N - s, h_outside)
                * (N - source_h)
                * a ** (1 - new_outside)
            )
    if s == N:
        formula = N * prefactor if level == N else sp.Integer(0)
    else:
        formula = prefactor * (
            (N + a * (N - s))
            * sp.binomial(N - s - 1, level - s)
            + s * sp.binomial(N - s - 1, level - s - 1)
        )
    assert sp.cancel(total - formula) == 0
    return sp.cancel(formula)


def subset_sum_coefficient(row, level):
    n = len(row) + 1
    N = n - 1
    ell = lambda x: x / (2 - x)
    total = sp.Integer(0)
    for j in range(1, level + 1):
        Ej = sp.Integer(0)
        for mask in range(1 << N):
            if mask.bit_count() != j:
                continue
            mass = sum(row[i] for i in range(N) if (mask >> i) & 1)
            Ej += ell(mass)
        total += (
            (-1) ** (level - j)
            * 2 ** (j - 1)
            * (2 * N - j)
            * sp.binomial(N - j, level - j)
            * Ej
        )
    return sp.cancel(total)


def check_graph(weights):
    n = len(weights)
    full = (1 << n) - 1
    fitness = sp.Integer(2)
    dual = dual_generator(weights, fitness, "dB")
    pi = stationary(dual)
    mean = sum(
        state.bit_count() * pi[state - 1] for state in range(1, full + 1)
    )
    nu = [
        sp.cancel(state.bit_count() * pi[state - 1] / mean)
        for state in range(1, full + 1)
    ]
    kernel, laws = event_kernel(weights, fitness)
    assert sp.Matrix([nu]).T == sp.Matrix(kernel.T) * sp.Matrix(nu)

    levels = [sp.Integer(0)] * (n + 1)
    for state, value in enumerate(nu, 1):
        levels[state.bit_count()] += value
    for k in range(n // 2 + 1, n):
        assert sp.cancel(levels[n - k] - levels[k]) >= 0
    for j in range(1, n):
        difference = sum(
            value
            * (
                sp.binomial(n - state.bit_count(), j)
                - sp.binomial(state.bit_count(), j)
            )
            for state, value in enumerate(nu, 1)
        )
        assert sp.cancel(difference) >= 0

    # The symmetric complete-reference event measure, followed by one event.
    reference = sp.Matrix(
        [[state.bit_count() * (n - state.bit_count()) for state in range(1, full + 1)]]
    )
    output = reference * kernel
    output_levels = [sp.Integer(0)] * (n + 1)
    for state in range(1, full + 1):
        output_levels[state.bit_count()] += output[state - 1]
    for k in range(n // 2 + 1, n):
        assert sp.cancel(output_levels[n - k] - output_levels[k]) >= 0

    # Verify (7)--(8) target by target.  Remove the target coordinate before
    # evaluating the one-row subset-sum formula.
    rows = transition(weights)
    for target in range(n):
        reduced_row = [rows[target][u] for u in range(n) if u != target]
        for level in range(1, n):
            direct = sum(
                probability
                * closed_conditional_coefficient(
                    n, union.bit_count(), level, sp.Integer(1)
                )
                for union, probability in laws[target].items()
            )
            formula = subset_sum_coefficient(reduced_row, level)
            assert sp.cancel(direct - formula) == 0


def main():
    # Formula (5) is a pure combinatorial identity; check a range of sizes and
    # exact fitness tilts independently of all graph calculations.
    identities = 0
    for n in range(3, 10):
        for a in (sp.Rational(1, 2), sp.Integer(1), sp.Integer(2)):
            for union_size in range(1, n):
                for level in range(1, n):
                    closed_conditional_coefficient(n, union_size, level, a)
                    identities += 1

    graphs = [
        [[0, 1, 0], [1, 0, 2], [0, 2, 0]],
        [[0, 1, 3], [1, 0, 2], [3, 2, 0]],
        [[0, 1, 3, 0], [1, 0, 2, 4], [3, 2, 0, 5], [0, 4, 5, 0]],
        [[0, 1, 0, 2], [1, 0, 3, 0], [0, 3, 0, 4], [2, 0, 4, 0]],
    ]
    for weights in graphs:
        check_graph(weights)

    print(f"PASS: {identities} exact conditional-rank formula checks")
    print(
        "PASS: OPEN stationary/one-step rank and factorial inequalities "
        f"on {len(graphs)} exact rational graphs at r=2"
    )


if __name__ == "__main__":
    main()
