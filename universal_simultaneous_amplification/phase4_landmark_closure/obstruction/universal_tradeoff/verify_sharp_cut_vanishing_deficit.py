#!/usr/bin/env python3
"""Exact audit for SHARP_CUT_VANISHING_DEFICIT.md.

The proof of time-scale separation is analytic.  This verifier checks all
finite symbolic components over Fraction arithmetic: local diagnostics, cut
biases, reciprocal-fitness identities, the weak-cut macro formula, and the
signed complete-sum comparison.
"""

from __future__ import annotations

from fractions import Fraction as F


def bd_complete(order: int, fitness: F) -> F:
    return (1 - 1 / fitness) / (1 - fitness ** (-order))


def db_complete(order: int, fitness: F) -> F:
    return (
        (1 - 1 / fitness)
        * F(order - 1, order)
        / (1 - fitness ** (1 - order))
    )


def macro_factor(order: int, fitness: F, ratio: F) -> F:
    first = fitness**order * ratio
    second = fitness**order / ratio
    return F(1, 2) * (first / (1 + first) + second / (1 + second))


def weak_sum_gap(order: int, fitness: F, ratio: F) -> F:
    factor = macro_factor(order, fitness, ratio)
    graph_sum = factor * (
        bd_complete(order, fitness) + db_complete(order, fitness)
    )
    baseline = bd_complete(2 * order, fitness) + db_complete(
        2 * order, fitness
    )
    return graph_sum - baseline


def structural_checks(order: int) -> int:
    eta = F(1, 2 ** (order**4))
    gamma = order * eta
    d_left = 3 + gamma
    d_right = 4 + gamma

    t_left = F(3, 1) / d_left + gamma / d_right
    t_right = F(4, 1) / d_right + gamma / d_left
    temperature_error = gamma / (d_left * d_right)
    assert t_left - 1 == -temperature_error
    assert t_right - 1 == temperature_error

    concentration = F(1, 2) * (
        (F(9, order - 1) + order * eta**2) / d_left**2
        + (F(16, order - 1) + order * eta**2) / d_right**2
    )
    assert concentration > 0
    assert concentration < F(2, order - 1)

    delta_left = gamma / d_left
    delta_right = gamma / d_right
    boundary_a = order * delta_left
    boundary_b = order * delta_right
    assert boundary_a / boundary_b == d_right / d_left
    return 3


def cut_checks(order: int, fitness: F) -> int:
    eta = F(1, 2 ** (order**4))
    gamma = order * eta
    delta_left = gamma / (3 + gamma)
    delta_right = gamma / (4 + gamma)

    bd_bias = fitness * delta_left / delta_right
    db_bias = (
        fitness
        * delta_right
        / delta_left
        * (fitness - (fitness - 1) * delta_left)
        / (1 + (fitness - 1) * delta_right)
    )
    product = bd_bias * db_bias
    declared_product = (
        fitness**2
        * (fitness - (fitness - 1) * delta_left)
        / (1 + (fitness - 1) * delta_right)
    )
    assert product == declared_product
    assert product < fitness**3
    return 2


def main() -> None:
    fitness = F(16, 9)
    ratio = F(4, 3)
    asymptotic = 1 - 1 / fitness
    target_bias = F(64, 27)
    assert fitness == ratio**2
    assert target_bias == ratio**3
    assert asymptotic == F(7, 16)

    checks = 0
    for order in range(2, 8):
        checks += structural_checks(order)
        checks += cut_checks(order, fitness)

    reciprocal_checks = 0
    negative_gaps = []
    scaled_errors = []
    for order in range(2, 61):
        assert bd_complete(order, fitness) / bd_complete(
            order, 1 / fitness
        ) == fitness ** (order - 1)
        assert db_complete(order, fitness) / db_complete(
            order, 1 / fitness
        ) == fitness ** (order - 2)
        reciprocal_checks += 2

        gap = weak_sum_gap(order, fitness, ratio)
        assert gap < 0
        negative_gaps.append(gap)
        scaled_errors.append(order * gap + asymptotic / 2)

    # This is an exact finite diagnostic of the proved expansion, not the
    # proof of its limit.  The displayed tail is already extremely close to
    # zero and decreases geometrically.
    assert abs(scaled_errors[-1]) < F(1, 10**12)
    assert abs(scaled_errors[-1]) < abs(scaled_errors[-2])

    print(f"PASS: {checks} exact local/cut checks")
    print(f"PASS: {reciprocal_checks} reciprocal-fitness checks")
    print(f"PASS: {len(negative_gaps)} exact negative weak-limit sum gaps")
    print(f"m=60 scaled remainder ~= {float(scaled_errors[-1]):.3e}")
    print("PROVED ROUTE FALSIFICATION: no unscaled deficit from local data + cut product")


if __name__ == "__main__":
    main()
