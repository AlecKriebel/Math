#!/usr/bin/env python3
"""Exact replay for the cross-rule orbital-midpoint refutation."""

from __future__ import annotations

import sympy as sp


def matrix_from_edges(a, b, c):
    """Triangle edge order (01,02,12)."""
    a, b, c = map(sp.sympify, (a, b, c))
    return [[0, a, b], [a, 0, c], [b, c, 0]]


def conjugate(weights, permutation):
    n = len(weights)
    return [
        [weights[permutation[i]][permutation[j]] for j in range(n)]
        for i in range(n)
    ]


def midpoint(left, right):
    n = len(left)
    return [
        [sp.factor((left[i][j] + right[i][j]) / 2) for j in range(n)]
        for i in range(n)
    ]


def killed_system(weights, rule):
    """Row-normalized flip chain, with empty/full boundary removed."""
    weights = [[sp.sympify(value) for value in row] for row in weights]
    n = len(weights)
    full = (1 << n) - 1
    states = list(range(1, full))
    index = {state: row for row, state in enumerate(states)}
    size = len(states)
    killed = sp.zeros(size)
    boundary = sp.zeros(size, 1)
    degrees = [sum(row) for row in weights]

    for state, row in index.items():
        raw = []
        for target in range(n):
            target_mutant = bool(state & (1 << target))
            if rule == "dB":
                mutant_mass = sum(
                    weights[source][target]
                    for source in range(n)
                    if state & (1 << source)
                )
                resident_mass = degrees[target] - mutant_mass
                denominator = 2 * mutant_mass + resident_mass
                rate = (
                    resident_mass / denominator
                    if target_mutant
                    else 2 * mutant_mass / denominator
                )
            elif rule == "Bd":
                rate = sum(
                    weights[source][target] / degrees[source]
                    for source in range(n)
                    if bool(state & (1 << source)) != target_mutant
                )
                if not target_mutant:
                    rate *= 2
            else:
                raise ValueError(rule)
            if rate:
                raw.append((state ^ (1 << target), sp.factor(rate)))

        total = sp.factor(sum(rate for _, rate in raw))
        killed[row, row] = 1
        for target_state, rate in raw:
            probability = sp.factor(rate / total)
            if target_state == full:
                boundary[row] += probability
            elif target_state:
                killed[row, index[target_state]] -= probability

    return states, killed, boundary


def start_vector(states, n):
    index = {state: row for row, state in enumerate(states)}
    alpha = sp.zeros(len(states), 1)
    for vertex in range(n):
        alpha[index[1 << vertex]] = sp.Rational(1, n)
    return alpha


def fixation(weights, rule):
    states, killed, boundary = killed_system(weights, rule)
    alpha = start_vector(states, len(weights))
    committor = killed.inv() * boundary
    return sp.factor((alpha.T * committor)[0])


def swapped_mask(state, permutation):
    answer = 0
    for vertex, image in enumerate(permutation):
        if state & (1 << vertex):
            answer |= 1 << image
    return answer


def permutation_matrix(states, permutation):
    index = {state: row for row, state in enumerate(states)}
    operator = sp.zeros(len(states))
    for state, row in index.items():
        operator[row, index[swapped_mask(state, permutation)]] = 1
    return operator


def sector_parts(endpoint, center, permutation, rule):
    states, killed, boundary = killed_system(endpoint, rule)
    _, killed_zero, boundary_zero = killed_system(center, rule)
    alpha = start_vector(states, len(endpoint))
    operator = permutation_matrix(states, permutation)

    conjugate_endpoint = conjugate(endpoint, permutation)
    _, killed_conjugate, boundary_conjugate = killed_system(
        conjugate_endpoint, rule
    )
    assert operator * killed * operator == killed_conjugate
    assert operator * boundary == boundary_conjugate
    assert operator * alpha == alpha

    committor = killed.inv() * boundary
    committor_zero = killed_zero.inv() * boundary_zero
    even_committor = (committor + operator * committor) / 2
    odd_committor = (committor - operator * committor) / 2
    even_killed = (killed + operator * killed * operator) / 2
    odd_killed = (killed - operator * killed * operator) / 2
    even_boundary = (boundary + operator * boundary) / 2
    odd_boundary = (boundary - operator * boundary) / 2

    assert even_killed * even_committor + odd_killed * odd_committor == even_boundary
    assert even_killed * odd_committor + odd_killed * even_committor == odd_boundary

    occupation = killed_zero.T.inv() * alpha
    vectors = (
        boundary_zero - even_boundary,
        (even_killed - killed_zero) * even_committor,
        odd_killed * odd_committor,
    )
    parts = tuple(sp.factor((occupation.T * vector)[0]) for vector in vectors)
    rho = sp.factor((alpha.T * committor)[0])
    rho_zero = sp.factor((alpha.T * committor_zero)[0])
    assert sp.factor(sum(parts) - (rho_zero - rho)) == 0
    return rho, rho_zero, parts


def symbolic_path_orbit():
    parameter = sp.symbols("s", real=True)
    weights = matrix_from_edges((1 - parameter) / 2, 3, (1 + parameter) / 2)
    bd = fixation(weights, "Bd")
    db = fixation(weights, "dB")

    expected_bd = (
        5 * parameter**12
        - 1814 * parameter**10
        + 231015 * parameter**8
        - 12910628 * parameter**6
        + 297441683 * parameter**4
        - 1684883718 * parameter**2
        + 2755428417
    ) / (
        3
        * (
            5 * parameter**12
            - 1514 * parameter**10
            + 172980 * parameter**8
            - 9062048 * parameter**6
            + 201258113 * parameter**4
            - 1092844158 * parameter**2
            + 1718304462
        )
    )
    expected_db = 2 * (
        6 * parameter**6
        - 721 * parameter**4
        + 16160 * parameter**2
        - 62677
    ) / (
        3
        * (
            4 * parameter**6
            - 623 * parameter**4
            + 24082 * parameter**2
            - 104103
        )
    )
    assert sp.factor(bd - expected_bd) == 0
    assert sp.factor(db - expected_db) == 0

    product = sp.factor(bd * db)
    curvature = sp.factor(sp.diff(sp.log(product), parameter, 2).subs(parameter, 0))
    assert curvature == -sp.Rational(273956014655842, 69260545804505391)
    assert sp.factor(product.subs(parameter, 0) - product.subs(parameter, 1)) == (
        -sp.Rational(94973014, 82395955215)
    )
    return curvature


def main():
    permutation = (2, 1, 0)
    endpoint = matrix_from_edges(0, 3, 1)
    center = midpoint(endpoint, conjugate(endpoint, permutation))

    bd, bd_zero, bd_parts = sector_parts(endpoint, center, permutation, "Bd")
    db, db_zero, db_parts = sector_parts(endpoint, center, permutation, "dB")
    assert bd == sp.Rational(817, 1479)
    assert bd_zero == sp.Rational(4397, 8226)
    assert db == sp.Rational(41, 105)
    assert db_zero == sp.Rational(466, 1161)

    assert bd_parts == (
        sp.Rational(4358, 143955),
        -sp.Rational(2851883, 89060160),
        -sp.Rational(3488083, 216288960),
    )
    assert db_parts == (
        -sp.Rational(8531, 4346784),
        sp.Rational(689653, 24766560),
        -sp.Rational(14773, 986076),
    )

    average_db = (db_zero + db) / 2
    average_bd = (bd_zero + bd) / 2
    combined = tuple(
        sp.factor(average_db * bd_part + average_bd * db_part)
        for bd_part, db_part in zip(bd_parts, db_parts)
    )
    assert combined == (
        sp.Rational(471596086168619, 43188663885494400),
        sp.Rational(13253289226241, 5398582985686800),
        -sp.Rational(368843888887, 25390161014400),
    )
    product_gap = sp.factor(bd_zero * db_zero - bd * db)
    assert product_gap == -sp.Rational(94973014, 82395955215)
    assert sp.factor(sum(combined) - product_gap) == 0

    positive_endpoint = matrix_from_edges(1, 10, 2)
    positive_center = midpoint(
        positive_endpoint, conjugate(positive_endpoint, permutation)
    )
    positive_values = tuple(
        fixation(weights, rule)
        for weights in (positive_endpoint, positive_center)
        for rule in ("Bd", "dB")
    )
    assert positive_values == (
        sp.Rational(8410983, 15863798),
        sp.Rational(488666, 1233045),
        sp.Rational(571, 1080),
        sp.Rational(271, 682),
    )
    positive_gap = sp.factor(
        positive_values[2] * positive_values[3]
        - positive_values[0] * positive_values[1]
    )
    assert positive_gap == -sp.Rational(531647447363, 14553217942853040)

    curvature = symbolic_path_orbit()
    print("PASS: exact cross-rule orbital midpoint refutation")
    print("path product gap:", product_gap)
    print("positive-triangle product gap:", positive_gap)
    print("combined (source, even, odd):", combined)
    print("midpoint log-product curvature:", curvature)


if __name__ == "__main__":
    main()
