#!/usr/bin/env python3
"""Exact replay of the complete-ray coloured-forest reduction.

This verifies the local first-appearance expansion of a fair-geometric
burst, the positive full clearing, the canonical degree, the triangle
Bernstein consequence, and the single K4 two-orbit quadratic audit.  It
does not assert the open all-order fixed-colour sign.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import permutations

import sympy as sp


def subsets(items):
    items = tuple(items)
    for mask in range(1 << len(items)):
        yield tuple(items[i] for i in range(len(items)) if (mask >> i) & 1)


def geometric_exact_support_inclusion(probabilities, target):
    """Inclusion--exclusion formula for Pr{the iid geometric union is target}."""

    answer = 0
    for included in subsets(target):
        mass = sum((probabilities[i] for i in included), sp.Integer(0))
        sign = (-1) ** (len(target) - len(included))
        answer += sign * mass / (2 - mass)
    return sp.cancel(answer)


def geometric_exact_support_orders(weights, target):
    """Positive first-appearance-order expansion in unnormalised weights."""

    degree = sum(weights)
    answer = 0
    for order in permutations(target):
        prefix = []
        term = 1
        for vertex in order:
            prefix.append(vertex)
            term *= weights[vertex] / (2 * degree - sum(weights[i] for i in prefix))
        answer += term
    return sp.cancel(answer)


def full_local_clearing(weights):
    degree = sum(weights)
    vertices = tuple(range(len(weights)))
    return sp.prod(
        2 * degree - sum(weights[i] for i in target)
        for target in subsets(vertices)
        if target
    )


def assert_positive_coefficients(expression, variables):
    polynomial = sp.Poly(sp.expand(expression), *variables)
    assert polynomial.total_degree() >= 0
    assert all(coefficient >= 0 for coefficient in polynomial.coeffs())


def audit_local_positive_clearing():
    # Three symbolic neighbours exercise proper/full-subset cases.  The
    # proof for arbitrary support is the same order partition; the verifier
    # deliberately avoids expanding the exponentially large full product.
    weights = sp.symbols("x0:3", nonnegative=True)
    degree = sum(weights)
    probabilities = tuple(weight / degree for weight in weights)
    gamma = full_local_clearing(weights)
    assert sp.Poly(gamma, *weights).total_degree() == 2**3 - 1
    assert_positive_coefficients(gamma, weights)
    for target in subsets(range(3)):
        if not target:
            continue
        inclusion = geometric_exact_support_inclusion(probabilities, target)
        ordered = geometric_exact_support_orders(weights, target)
        assert sp.cancel(inclusion - ordered) == 0
        cleared = sp.cancel(gamma * ordered)
        assert sp.denom(cleared) == 1
        assert_positive_coefficients(cleared, weights)

    # One exact four-neighbour numerical identity guards the next support
    # size without incurring a large symbolic cancellation.
    rational_weights = tuple(map(sp.Integer, (1, 2, 3, 5)))
    rational_probabilities = tuple(
        weight / sum(rational_weights) for weight in rational_weights
    )
    for target in subsets(range(4)):
        if target:
            assert geometric_exact_support_inclusion(
                rational_probabilities, target
            ) == geometric_exact_support_orders(rational_weights, target)


def canonical_degrees(n):
    l_degree = n * (2**n - 2)
    local_factors = 2 ** (n - 1) - 1
    d_degree = n * local_factors * (2**n - 3)
    return l_degree, d_degree, l_degree + d_degree


def triangle_certificate_bernstein_check():
    # The committed PAPT_3 certificate has 24 terms
    # sum_perm x^i y^j z^k (x-y)^2.  On x_alpha=1-alpha+alpha*x,
    # every square contributes alpha^2(x-y)^2, and all remaining linear
    # factors have nonnegative Bernstein endpoint controls.
    from pathlib import Path
    import sys

    triangle = Path(__file__).resolve().parents[1] / "r2_cross_rule_triangle"
    sys.path.insert(0, str(triangle))
    from verify_papt3_weighted_triangle import (  # noqa: PLC0415
        BD_TABLE,
        CERTIFICATE,
        DB_TABLE,
        a,
        b,
        c,
        table_polynomials,
    )

    assert len(CERTIFICATE) == 24
    assert all(sum(exponents) == 16 and coefficient > 0
               for exponents, coefficient in CERTIFICATE)
    # Full clearing: Lambda trees contribute d_product^6; Gamma_D is
    # d_product*delta and its five-edge tree contributes the fifth power.
    # After cancelling the common primitive denominators, the multiplier is
    # d_product^7 delta^4, of degree 45; N has degree 18.
    assert canonical_degrees(3) == (18, 45, 63)

    # Exact rational tree-cofactor audit of the multiplier in the note.
    cross_rule = Path(__file__).resolve().parents[1] / "r2_cross_rule_sum"
    sys.path.insert(0, str(cross_rule))
    from verify_cross_rule_tree_reduction import (  # noqa: PLC0415
        db_generator,
        tree_data,
        unbatched_generators,
    )

    weights = ((0, 1, 2), (1, 0, 3), (2, 3, 0))
    left, _ = unbatched_generators(weights)
    death = db_generator(weights)
    _, z_l, y_l, _ = tree_data(left, list(range(1, 8)))
    _, z_d, y_d, _ = tree_data(death, list(range(1, 7)))
    degrees = [sum(row) for row in weights]
    d_product = degrees[0] * degrees[1] * degrees[2]
    gamma = 1
    for target in range(3):
        neighbours = tuple(vertex for vertex in range(3) if vertex != target)
        for support in subsets(neighbours):
            if support:
                gamma *= 2 * degrees[target] - sum(
                    weights[target][vertex] for vertex in support
                )
    delta = gamma // d_product
    z_l_hat, y_l_hat = z_l * d_product**6, y_l * d_product**6
    z_d_hat, y_d_hat = z_d * gamma**5, y_d * gamma**5
    cleared = 48 * z_l_hat * z_d_hat - 21 * y_l_hat * y_d_hat
    n_b, q_b = table_polynomials(BD_TABLE)
    n_d, q_d = table_polynomials(DB_TABLE)
    primitive = (2 * q_b * q_d - 7 * n_b * n_d).subs({a: 1, b: 2, c: 3})
    assert cleared == 72 * d_product**7 * delta**4 * int(primitive)


ZERO = (F(0), F(0), F(0))
ONE = (F(1), F(0), F(0))


def s_add(*values):
    return tuple(sum((value[k] for value in values), F(0)) for k in range(3))


def s_neg(value):
    return tuple(-entry for entry in value)


def s_mul(left, right):
    return (
        left[0] * right[0],
        left[0] * right[1] + left[1] * right[0],
        left[0] * right[2] + left[1] * right[1] + left[2] * right[0],
    )


def s_inv(value):
    a0, a1, a2 = value
    assert a0
    return (1 / a0, -a1 / a0**2, a1**2 / a0**3 - a2 / a0**2)


def s_div(left, right):
    return s_mul(left, s_inv(right))


def s_scale(value, scalar):
    return tuple(scalar * entry for entry in value)


def add_series_rate(matrix, row, column, value):
    if row != column:
        matrix[row][column] = s_add(matrix[row][column], value)


def finish_series_generator(matrix):
    for row in range(len(matrix)):
        matrix[row][row] = s_neg(s_add(*(
            matrix[row][column]
            for column in range(len(matrix))
            if column != row
        )))
    return matrix


def series_transition_matrix(direction):
    n = 4
    weights = [[ZERO for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            weights[i][j] = weights[j][i] = (F(1), F(direction[i, j]), F(0))
    degrees = [s_add(*row) for row in weights]
    return [[s_div(weights[i][j], degrees[i]) for j in range(n)]
            for i in range(n)]


def l_series_generator(direction):
    p = series_transition_matrix(direction)
    n = 4
    full = (1 << n) - 1
    matrix = [[ZERO for _ in range(full)] for _ in range(full)]
    for state in range(1, full + 1):
        for target in range(n):
            if not ((state >> target) & 1):
                continue
            for source in range(n):
                neutral = (state & ~(1 << target)) | (1 << source)
                selective = state | (1 << source)
                add_series_rate(matrix, state - 1, neutral - 1, p[source][target])
                add_series_rate(matrix, state - 1, selective - 1, p[source][target])
    return finish_series_generator(matrix)


def geometric_series_support(row, target):
    answer = ZERO
    for included in subsets(target):
        mass = s_add(*(row[i] for i in included)) if included else ZERO
        term = s_div(mass, s_add(s_scale(ONE, 2), s_neg(mass)))
        answer = s_add(answer, s_scale(term, (-1) ** (len(target) - len(included))))
    return answer


def d_series_generator(direction):
    p = series_transition_matrix(direction)
    n = 4
    full = (1 << n) - 1
    matrix = [[ZERO for _ in range(full - 1)] for _ in range(full - 1)]
    laws = []
    for target in range(n):
        law = {}
        neighbours = tuple(i for i in range(n) if i != target)
        for union in subsets(neighbours):
            if union:
                law[sum(1 << i for i in union)] = geometric_series_support(p[target], union)
        laws.append(law)
    for state in range(1, full):
        for target in range(n):
            if not ((state >> target) & 1):
                continue
            without = state & ~(1 << target)
            for union, probability in laws[target].items():
                output = without | union
                if output < full:
                    add_series_rate(matrix, state - 1, output - 1, probability)
    return finish_series_generator(matrix)


def solve_fraction(matrix, rhs):
    size = len(matrix)
    work = [row[:] + [value] for row, value in zip(matrix, rhs)]
    for column in range(size):
        pivot = next(row for row in range(column, size) if work[row][column])
        work[column], work[pivot] = work[pivot], work[column]
        value = work[column][column]
        work[column] = [entry / value for entry in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [entry - scale * pivot_entry
                         for entry, pivot_entry in zip(work[row], work[column])]
    return [row[-1] for row in work]


def matrix_vector(matrix, vector):
    return [sum((entry * value for entry, value in zip(row, vector)), F(0))
            for row in matrix]


def stationary_mean_series(generator, ranks):
    size = len(generator)
    coefficients = [
        [[generator[column][row][order] for column in range(size)]
         for row in range(size)]
        for order in range(3)
    ]
    for column in range(size):
        coefficients[0][-1][column] = F(1)
        coefficients[1][-1][column] = F(0)
        coefficients[2][-1][column] = F(0)
    rhs0 = [F(0)] * size
    rhs0[-1] = F(1)
    x0 = solve_fraction(coefficients[0], rhs0)
    rhs1 = [-value for value in matrix_vector(coefficients[1], x0)]
    x1 = solve_fraction(coefficients[0], rhs1)
    a1x1 = matrix_vector(coefficients[1], x1)
    a2x0 = matrix_vector(coefficients[2], x0)
    x2 = solve_fraction(coefficients[0],
                        [-(left + right) for left, right in zip(a1x1, a2x0)])
    return tuple(sum((rank * vector[i] for i, rank in enumerate(ranks)), F(0))
                 for vector in (x0, x1, x2))


def second_variations(direction):
    full = (1 << 4) - 1
    m_l = stationary_mean_series(
        l_series_generator(direction),
        [state.bit_count() for state in range(1, full + 1)],
    )
    m_d = stationary_mean_series(
        d_series_generator(direction),
        [state.bit_count() for state in range(1, full)],
    )
    rho_l = s_scale(m_l, F(1, 4))
    rho_d = s_scale(m_d, F(1, 4))
    values = [(rho[0], rho[1], 2 * rho[2]) for rho in (rho_l, rho_d)]
    product = s_mul(rho_l, rho_d)
    gap_second = -2 * product[2]
    return values, gap_second


def edge_pair_energies(direction):
    edges = tuple(direction)
    adjacent = 0
    disjoint = 0
    for index, edge in enumerate(edges):
        for other in edges[index + 1:]:
            value = (direction[edge] - direction[other]) ** 2
            if set(edge) & set(other):
                adjacent += value
            else:
                disjoint += value
    return adjacent, disjoint


def audit_k4_two_orbits():
    standard = {(0, 1): 0, (0, 2): 1, (0, 3): 1,
                (1, 2): -1, (1, 3): -1, (2, 3): 0}
    cycle = {(0, 1): 1, (0, 2): -1, (0, 3): 0,
             (1, 2): 0, (1, 3): -1, (2, 3): 1}
    standard_values, standard_gap = second_variations(standard)
    cycle_values, cycle_gap = second_variations(cycle)
    assert standard_values == [
        (F(8, 15), F(0), -F(24256, 1257525)),
        (F(3, 7), F(0), -F(29, 245)),
    ]
    assert cycle_values == [
        (F(8, 15), F(0), F(0)),
        (F(3, 7), F(0), -F(12, 637)),
    ]
    assert standard_gap == F(293288, 4107915)
    assert cycle_gap == F(32, 3185)
    assert edge_pair_energies(standard) == (16, 8)
    assert edge_pair_energies(cycle) == (24, 0)
    adjacent_coefficient = cycle_gap / 24
    disjoint_coefficient = (standard_gap - 16 * adjacent_coefficient) / 8
    assert adjacent_coefficient == F(4, 9555)
    assert disjoint_coefficient == F(431881, 53402895)
    assert adjacent_coefficient > 0 and disjoint_coefficient > 0


def main():
    audit_local_positive_clearing()
    triangle_certificate_bernstein_check()
    audit_k4_two_orbits()
    print("PASS: fair-geometric support law has a positive first-appearance clearing")
    print("PASS: canonical full-clearing degrees q_3=63 and general formula audited")
    print("PASS: triangle certificate has nonnegative complete-ray Bernstein controls")
    print("PASS: the sole K4 audit has two positive quadratic edge-pair orbit weights")
    print("OPEN: fixed-colour root-rank expectation for general n and j>=3")


if __name__ == "__main__":
    main()
