#!/usr/bin/env python3
"""Exact certificates for the batching interpolation and current identity."""

from __future__ import annotations

import sympy as sp


R = sp.Rational(3, 2)
A = R - 1


def popcount(state: int) -> int:
    return bin(state).count("1")


def verify_local_interpolation() -> None:
    x, s = sp.symbols("x s")
    r_s = 1 + s / 2
    beta = (R - r_s) / r_s
    geometric_mutant = r_s * x / (1 + (r_s - 1) * x)
    replacement_birth = geometric_mutant
    retention_birth = beta * geometric_mutant
    replacement_death = (1 - x) / (1 + (r_s - 1) * x)
    assert sp.cancel(
        replacement_birth + retention_birth
        - R * x / (1 + s * x / 2)
    ) == 0
    assert sp.cancel(
        replacement_death - (1 - x) / (1 + s * x / 2)
    ) == 0
    inclusion_rate = sp.cancel((1 + beta) * geometric_mutant)
    assert sp.cancel(inclusion_rate - R * x / (1 + s * x / 2)) == 0
    assert sp.cancel(sp.diff(inclusion_rate, s)) == sp.cancel(
        -R * x**2 / (2 * (1 + s * x / 2) ** 2)
    )


def verify_complete_curve() -> None:
    s = sp.symbols("s")
    for n in range(2, 11):
        product = sp.Integer(1)
        for ell in range(1, n):
            up = R * ell * (n - ell) / (n - 1 + s * ell / 2)
            down = ell * (n - ell) / (n - 1 + s * (ell - 1) / 2)
            product = sp.cancel(product * down / up)
            expected = (sp.Rational(2, 3) ** ell) * (
                1 + s * sp.Rational(ell, 2 * (n - 1))
            )
            assert sp.cancel(product - expected) == 0

        a_n = sum(sp.Rational(2, 3) ** ell for ell in range(1, n))
        b_n = sum(
            ell * sp.Rational(2, 3) ** ell for ell in range(1, n)
        ) / (2 * (n - 1))
        rho = sp.cancel(1 / (1 + a_n + s * b_n))
        ratio = sp.cancel(rho.subs(s, 1) / rho.subs(s, 0))
        expected_ratio = sp.cancel(
            sp.Rational(n - 1, n)
            * (1 - sp.Rational(2, 3) ** n)
            / (1 - sp.Rational(2, 3) ** (n - 1))
        )
        assert ratio == expected_ratio
        assert sp.cancel(
            sp.diff(sp.log(rho), s) + b_n / (1 + a_n + s * b_n)
        ) == 0


def triangle_system(s: sp.Rational):
    weights = [[0, 1, 1], [1, 0, 100], [1, 100, 0]]
    n = 3
    full = (1 << n) - 1
    states = list(range(1, full))
    index = {state: row for row, state in enumerate(states)}
    p = [
        [sp.Rational(value, sum(row)) for value in row]
        for row in weights
    ]
    matrix = sp.zeros(len(states))
    matrix_prime = sp.zeros(len(states))
    rhs = sp.zeros(len(states), 1)
    rhs_prime = sp.zeros(len(states), 1)
    edge_rates = {}
    for state in states:
        row = index[state]
        for target in range(n):
            x = sum(
                p[target][source]
                for source in range(n)
                if (state >> source) & 1
            )
            denominator = 1 + s * x / 2
            if (state >> target) & 1:
                base = 1 - x
                new_state = state & ~(1 << target)
            else:
                base = R * x
                new_state = state | (1 << target)
            rate = sp.cancel(base / denominator)
            rate_prime = sp.cancel(-base * x / (2 * denominator**2))
            edge_rates[state, target] = (rate, new_state, x)
            matrix[row, row] += rate
            matrix_prime[row, row] += rate_prime
            if new_state == full:
                rhs[row] += rate
                rhs_prime[row] += rate_prime
            elif new_state:
                matrix[row, index[new_state]] -= rate
                matrix_prime[row, index[new_state]] -= rate_prime
    return p, states, index, matrix, matrix_prime, rhs, rhs_prime, edge_rates


def verify_occupation_current() -> None:
    s = sp.Integer(0)
    (
        p,
        states,
        index,
        matrix,
        matrix_prime,
        rhs,
        rhs_prime,
        edge_rates,
    ) = triangle_system(s)
    n = 3
    full = 7
    values_vector = matrix.inv() * rhs
    derivative_vector = matrix.inv() * (
        rhs_prime - matrix_prime * values_vector
    )
    values = [sp.Integer(0)] + list(values_vector) + [sp.Integer(1)]
    alpha = sp.zeros(1, len(states))
    for vertex in range(n):
        alpha[0, index[1 << vertex]] = sp.Rational(1, n)
    occupation = alpha * matrix.inv()
    rho = sp.cancel(
        sum(values[1 << vertex] for vertex in range(n)) / n
    )
    rho_prime = sp.cancel(
        sum(
            derivative_vector[index[1 << vertex]]
            for vertex in range(n)
        )
        / n
    )

    def nu(state: int) -> sp.Expr:
        if state in (0, full):
            return sp.Integer(0)
        return occupation[0, index[state]]

    currents = {}
    weighted_current = 0
    level_current = {1: sp.Integer(0), 2: sp.Integer(0)}
    for lower in range(full):
        for target in range(n):
            if (lower >> target) & 1:
                continue
            upper = lower | (1 << target)
            x = sum(
                p[target][source]
                for source in range(n)
                if (lower >> source) & 1
            )
            denominator = 1 + s * x / 2
            upward = sp.cancel(R * x / denominator)
            downward = sp.cancel((1 - x) / denominator)
            current = sp.cancel(
                nu(lower) * upward - nu(upper) * downward
            )
            currents[lower, target] = current
            delta_h = values[upper] - values[lower]
            theta = sp.cancel((x / 2) / denominator)
            weighted_current += theta * current * delta_h
            if popcount(lower) in level_current:
                level_current[popcount(lower)] += current

    assert currents[0b001, 1] == -sp.Rational(4317, 186944)
    assert all(sp.cancel(value - rho) == 0 for value in level_current.values())
    assert sp.cancel(rho_prime / rho + weighted_current / rho) == 0

    # The proposed derivative ceiling survives this exact heterogeneous test.
    a_n = sp.Rational(2, 3) + sp.Rational(4, 9)
    b_n = (
        sp.Rational(2, 3) + 2 * sp.Rational(4, 9)
    ) / 4
    complete_derivative = -b_n / (1 + a_n)
    assert sp.cancel(rho_prime / rho - complete_derivative) < 0

    verify_overlap_decomposition(p, rho_prime)


def verify_overlap_decomposition(
    p: list[list[sp.Rational]], forward_rho_prime: sp.Expr
) -> None:
    """Check the exact C2/C3 Poisson-curvature identity on the triangle."""
    n = len(p)
    full = (1 << n) - 1
    generator = sp.zeros(full, full)
    for state in range(1, full + 1):
        row = state - 1
        for target in range(n):
            if not ((state >> target) & 1):
                continue
            for source in range(n):
                probability = p[target][source]
                neutral = (state & ~(1 << target)) | (1 << source)
                selective = state | (1 << source)
                if neutral != state:
                    generator[row, neutral - 1] += probability
                if selective != state:
                    generator[row, selective - 1] += (R - 1) * probability
        generator[row, row] = -sum(generator.row(row))

    stationary_matrix = generator.T.copy()
    stationary_matrix[-1, :] = sp.ones(1, full)
    stationary_rhs = sp.zeros(full, 1)
    stationary_rhs[-1] = 1
    invariant = stationary_matrix.inv() * stationary_rhs
    sizes = sp.Matrix([popcount(state) for state in range(1, full + 1)])
    mean = sp.cancel((invariant.T * sizes)[0])

    poisson_matrix = generator.copy()
    poisson_rhs = sp.ones(full, 1) * mean - sizes
    poisson_matrix[-1, :] = sp.zeros(1, full)
    poisson_matrix[-1, -1] = 1
    poisson_rhs[-1] = 0
    potential = poisson_matrix.inv() * poisson_rhs
    assert generator * potential == sp.ones(full, 1) * mean - sizes

    def value(state: int) -> sp.Expr:
        return potential[state - 1]

    def curvature(base: int, first: int, second: int) -> sp.Expr:
        return sp.cancel(
            value(base | (1 << first))
            + value(base | (1 << second))
            - value(base | (1 << first) | (1 << second))
            - value(base)
        )

    c_two = 0
    c_three = 0
    for state in range(1, full + 1):
        mass = invariant[state - 1]
        for target in range(n):
            if not ((state >> target) & 1):
                continue
            for first in range(n):
                for second in range(n):
                    sample_mass = p[target][first] * p[target][second]
                    if not sample_mass:
                        continue
                    swapped = (state & ~(1 << target)) | (1 << first)
                    c_two += mass * sample_mass * curvature(
                        swapped, target, second
                    )
                    c_three += mass * sample_mass * curvature(
                        state, first, second
                    )
    c_two = sp.cancel(c_two)
    c_three = sp.cancel(c_three)
    assert c_two >= 0
    assert c_three >= 0
    assert sp.cancel(
        n * forward_rho_prime - (R - 1) * (c_two - R * c_three)
    ) == 0


def main() -> None:
    verify_local_interpolation()
    verify_complete_curve()
    verify_occupation_current()
    print("PASS exact additive interpolation and collision derivative")
    print("PASS exact complete-graph curve for n=2,...,10")
    print("PASS exact occupation-current and rank-cut identities")
    print("PASS exact negative internal current -4317/186944")
    print("PASS exact Poisson-curvature C2/C3 decomposition")


if __name__ == "__main__":
    main()
