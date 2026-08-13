#!/usr/bin/env python3
"""Exact symbolic audit of the integrated marked-semigroup P3 theorem.

This script verifies identities over QQ(p).  It proves the formulas used in
INTEGRATED_MARKED_SEMIGROUP.md; it does not assert the open all-graph signs.
"""

from __future__ import annotations

import sympy as sp


def stationary_row(kernel_or_generator, stochastic):
    """Return the normalized invariant row over a symbolic fraction field."""

    size = kernel_or_generator.rows
    if stochastic:
        system = kernel_or_generator.T - sp.eye(size)
    else:
        system = kernel_or_generator.T
    rhs = sp.zeros(size, 1)
    system = system.copy()
    system[size - 1, :] = sp.ones(1, size)
    rhs[size - 1] = 1
    column = system.inv() * rhs
    row = column.T
    assert all(sp.cancel(value) >= 0 for value in row.subs(PARAMETER, sp.Rational(1, 3)))
    return row.applyfunc(sp.factor)


def build_left(request):
    """Fitness-two L generator on the seven nonempty subsets."""

    n = request.rows
    full = (1 << n) - 1
    generator = sp.zeros(full)
    for state in range(1, full + 1):
        row = state - 1
        for target in range(n):
            if not (state >> target) & 1:
                continue
            for source in range(n):
                rate = request[source, target]
                neutral = (state & ~(1 << target)) | (1 << source)
                selective = state | (1 << source)
                if neutral != state:
                    generator[row, neutral - 1] += rate
                if selective != state:
                    generator[row, selective - 1] += rate
    for row in range(full):
        generator[row, row] = -sum(
            generator[row, column] for column in range(full) if column != row
        )
        assert sp.factor(sum(generator[row, column] for column in range(full))) == 0
    return generator


def build_marked(request):
    """Return X states, A_P, R, M=A_P R, and K=R A_P."""

    n = request.rows
    full = (1 << n) - 1
    marked = tuple(
        (cache, target)
        for cache in range(1 << n)
        for target in range(n)
        if not (cache >> target) & 1
    )
    active = tuple(
        (cache, target)
        for cache in range(1, 1 << n)
        for target in range(n)
        if not (cache >> target) & 1
    )
    marked_index = {state: index for index, state in enumerate(marked)}
    active_index = {state: index for index, state in enumerate(active)}
    sample = sp.zeros(len(marked), len(active))
    refresh = sp.zeros(len(active), len(marked))

    for row, (cache, target) in enumerate(marked):
        for source in range(n):
            probability = request[target, source]
            if probability == 0:
                continue
            output = cache | (1 << source)
            sample[row, active_index[output, target]] += probability

    for row, (active_cache, target) in enumerate(active):
        refresh[row, marked_index[active_cache, target]] += sp.Rational(1, 2)
        reciprocal = sp.Rational(1, 2 * active_cache.bit_count())
        for new_target in range(n):
            if (active_cache >> new_target) & 1:
                output = active_cache & ~(1 << new_target)
                refresh[row, marked_index[output, new_target]] += reciprocal

    assert sample * sp.ones(len(active), 1) == sp.ones(len(marked), 1)
    assert refresh * sp.ones(len(marked), 1) == sp.ones(len(active), 1)
    return marked, active, sample, refresh, sample * refresh, refresh * sample


def marked_psi(n, rank):
    return sp.factor(
        2
        * sum(
            sp.Rational((-1) ** (active_rank - 1 - rank), active_rank)
            for active_rank in range(rank + 1, n)
        )
    )


PARAMETER = sp.symbols("p", positive=True)


def main():
    p = PARAMETER
    u = sp.symbols("u", nonnegative=True)
    request = sp.Matrix(
        (
            (0, 1, 0),
            (p, 0, 1 - p),
            (0, 1, 0),
        )
    )
    left = build_left(request)
    pi_l = stationary_row(left, stochastic=False)
    ranks = sp.Matrix([state.bit_count() for state in range(1, 8)])
    mean_l_p = sp.factor((pi_l * ranks)[0])

    marked, active, sample, refresh, marked_kernel, active_kernel = build_marked(
        request
    )
    psi = sp.Matrix([marked_psi(3, cache.bit_count()) for cache, _ in marked])
    harmonic = sp.Matrix([sp.Rational(1, cache.bit_count()) for cache, _ in active])
    assert refresh * psi == harmonic

    full = 7
    q_l = sp.Matrix(
        [[pi_l[(full ^ cache) - 1] / mean_l_p for cache, _ in marked]]
    ).applyfunc(sp.factor)
    assert sp.factor((q_l * sp.ones(len(marked), 1))[0]) == 1
    nu_l = (q_l * sample).applyfunc(sp.factor)

    # The active initial-law formula (14).
    for column, (cache, target) in enumerate(active):
        occupied = full ^ cache
        expected = (
            sum(request[target, source] for source in range(3) if (cache >> source) & 1)
            * pi_l[occupied - 1]
            + sum(
                request[target, source] * pi_l[(occupied | (1 << source)) - 1]
                for source in range(3)
                if (cache >> source) & 1
            )
        ) / mean_l_p
        assert sp.factor(nu_l[column] - expected) == 0

    a1_p = sp.factor((q_l * marked_kernel * psi)[0])
    a2_p = sp.factor((q_l * marked_kernel**2 * psi)[0])
    assert sp.factor(a1_p - (nu_l * harmonic)[0]) == 0
    assert sp.factor(a2_p - (nu_l * active_kernel * harmonic)[0]) == 0

    nu_d = stationary_row(active_kernel, stochastic=True)
    inverse_mean_d = sp.factor((nu_d * harmonic)[0])
    # Replace p^2-p by -u to expose symmetry under exchanging the leaves.
    relation = p**2 - p + u

    def reduce_to_u(expression):
        numerator, denominator = sp.fraction(sp.cancel(expression))
        numerator = sp.rem(numerator, relation, p)
        denominator = sp.rem(denominator, relation, p)
        return sp.factor(numerator / denominator)

    mean_l = sp.factor(reduce_to_u(mean_l_p))
    a1 = sp.factor(reduce_to_u(a1_p))
    a2 = sp.factor(reduce_to_u(a2_p))
    inverse_mean = sp.factor(reduce_to_u(inverse_mean_d))
    assert sp.factor(
        mean_l - (4 * u**2 + 46 * u + 4) / (4 * u**2 + 19 * u + 4)
    ) == 0
    assert sp.factor(
        a1 - (-20 * u**2 + 217 * u + 10) / (10 * (2 * u**2 + 23 * u + 2))
    ) == 0
    assert sp.factor(
        a2 - 3 * (-7 * u**2 + 29 * u + 2) / (4 * (2 * u**2 + 23 * u + 2))
    ) == 0
    assert sp.factor(inverse_mean - (u + 2) / (3 * u + 2)) == 0

    midpoint = sp.factor((a1 + a2) / 2)
    stationary_gap = sp.factor(inverse_mean - midpoint)
    floor = sp.factor(sp.Rational(7, 16) * mean_l)
    floor_gap = sp.factor(midpoint - floor)
    assert sp.factor(
        stationary_gap
        - (5 * u + 1) * (103 * u**2 - 268 * u + 60)
        / (40 * (3 * u + 2) * (2 * u**2 + 23 * u + 2))
    ) == 0
    polynomial = 20 + 402 * u - 888 * u**2 - 833 * u**3 - 240 * u**4
    assert sp.factor(
        floor_gap
        - 3 * polynomial
        / (40 * (2 * u**2 + 23 * u + 2) * (4 * u**2 + 19 * u + 4))
    ) == 0

    # The abstract two-step current (11) is checked directly over QQ(p).
    centered = harmonic - inverse_mean_d * sp.ones(len(active), 1)
    poisson_system = sp.eye(len(active)) - active_kernel
    poisson_system = poisson_system.copy()
    poisson_system[len(active) - 1, :] = sp.ones(1, len(active))
    poisson_rhs = centered.copy()
    poisson_rhs[len(active) - 1] = 0
    green = poisson_system.inv() * poisson_rhs
    current = sp.factor(
        (nu_l * (active_kernel**2 - sp.eye(len(active))) * green)[0] / 2
    )
    assert sp.factor(current - (inverse_mean_d - (a1_p + a2_p) / 2)) == 0

    # Exact unweighted-path obstruction to stationary >= midpoint.
    assert a1.subs(u, sp.Rational(1, 4)) == sp.Rational(4, 5)
    assert a2.subs(u, sp.Rational(1, 4)) == sp.Rational(47, 56)
    assert midpoint.subs(u, sp.Rational(1, 4)) == sp.Rational(459, 560)
    assert inverse_mean.subs(u, sp.Rational(1, 4)) == sp.Rational(9, 11)
    assert stationary_gap.subs(u, sp.Rational(1, 4)) == sp.Rational(-9, 6160)

    # Direct combined PAPT_3 formula and elementary sign certificates.
    combined_gap = sp.factor(inverse_mean - floor)
    combined_numerator = 36 - 28 * u - 295 * u**2 - 10 * u**3
    assert sp.factor(
        combined_gap
        - combined_numerator / (8 * (3 * u + 2) * (4 * u**2 + 19 * u + 4))
    ) == 0
    assert sp.Rational(402) - sp.Rational(4445, 16) == sp.Rational(1987, 16)
    assert sp.Rational(819, 32) < 36

    print("PASS: exact integrated marked-semigroup recurrence over QQ(p)")
    print("EXACTLY REFUTED: stationary >= midpoint on unweighted P3")
    print("PASS: weighted-P3 midpoint lower bound over QQ(u)")
    print("PROVED HERE: PAPT_3 for every weighted three-vertex path")
    print("OPEN: the combined integrated current sign for general graphs")


if __name__ == "__main__":
    main()
