#!/usr/bin/env python3
"""Exact audit of the fixed-colour row-mixture and unicycle reductions.

The identities are general; the triangle calculations are exact hostile
checks showing that neither individual row locations nor individual
spanning unicycles have the desired sign.
"""

from __future__ import annotations

from itertools import combinations
from math import comb

import sympy as sp

from verify_complete_ray_critical_transfer import complete_data


def bernstein_controls(polynomial, variable, degree):
    poly = sp.Poly(sp.expand(polynomial), variable)
    power = [poly.coeff_monomial(variable**j) for j in range(degree + 1)]
    return [
        sp.factor(sum(
            power[j] * sp.binomial(k, j) / sp.binomial(degree, j)
            for j in range(k + 1)
        ))
        for k in range(degree + 1)
    ]


def triangle_data():
    weights = (
        (0, 1, 10),
        (1, 0, 3),
        (10, 3, 0),
    )
    P = [
        [sp.Rational(weights[i][j], sum(weights[i])) for j in range(3)]
        for i in range(3)
    ]
    return complete_data(P)


def tree_controls(states, K0, K):
    alpha = sp.symbols("alpha")
    mixed = K0 + alpha * (K - K0)
    laplacian = sp.eye(len(states)) - mixed
    points = list(range(len(states)))
    root_polynomials = []
    for root in range(len(states)):
        values = []
        rows = [i for i in range(len(states)) if i != root]
        for value in points:
            minor = laplacian.extract(rows, rows).subs(alpha, value)
            values.append(minor.det(method="domain-ge"))
        root_polynomials.append(sp.interpolate(list(zip(points, values)), alpha))
    degree = len(states) - 1
    controls = [
        sp.Matrix([bernstein_controls(poly, alpha, degree)[j]
                   for poly in root_polynomials]).T
        for j in range(degree + 1)
    ]
    return controls


def root_recurrence_audit(states, K0, K, q):
    controls = tree_controls(states, K0, K)
    d = len(states) - 1
    zero = sp.zeros(1, len(states))
    for j in range(d + 2):
        current = controls[j] if j <= d else zero
        previous = controls[j - 1] if j else zero
        assert (
            (d + 1 - j) * current * (sp.eye(len(states)) - K0)
            + j * previous * (sp.eye(len(states)) - K)
        ) == zero

    one = sp.ones(len(states), 1)
    nu0 = sp.Matrix([[
        sp.Rational(B.bit_count(), 3 * 2 * 2) for B, _ in states
    ]])
    h = (sp.eye(len(states)) - K0 + one * nu0).inv() * q
    delta_h = (K - K0) * h
    numerators = [sp.factor((control * q)[0]) for control in controls]
    for j in range(1, d + 2):
        previous = controls[j - 1]
        right = numerators[j - 1]
        if j <= d:
            right += sp.Rational(d + 1 - j, j) * numerators[j]
        assert sp.factor((previous * delta_h)[0] - right) == 0
    print("PASS: exact fixed-colour root-vector recurrence")
    return controls, h, delta_h


def row_mixture_audit(states, K0, K, nu0, q, controls, h, delta_h):
    size = len(states)
    identity = sp.eye(size)

    # Verify the all-order identity on every singleton location and on
    # representative higher-cardinality row sets.
    row_sets = [(i,) for i in range(size)]
    row_sets += [
        (0, 1), (0, 3, 6), (0, 2, 3, 5),
        (0, 1, 2, 3, 5, 6), tuple(range(size)),
    ]
    for row_set in row_sets:
        C = set(row_set)
        KC = K0.copy()
        for x in C:
            KC[x, :] = K[x, :]
        lhs = sp.factor((identity - KC + q * nu0).det(method="domain-ge"))

        rhs = 0
        for x in C:
            KD = K0.copy()
            for y in C - {x}:
                KD[y, :] = K[y, :]
            rows = [i for i in range(size) if i != x]
            tau = (identity - KD).extract(rows, rows).det(method="domain-ge")
            rhs += tau * delta_h[x]
        assert sp.factor(lhs - rhs) == 0

    singleton = 0  # state (2,0) in the canonical ordering
    assert states[singleton] == (2, 0)
    KC = K0.copy()
    KC[singleton, :] = K[singleton, :]
    value = sp.factor((identity - KC + q * nu0).det(method="domain-ge"))
    assert delta_h[singleton] == -sp.Rational(9, 44)
    assert value == -sp.Rational(891, 524288)

    # Row multilinearity and degree elevation, checked at every level by
    # enumerating the 512 row choices of this nine-state chain.
    level_sums = [sp.Integer(0) for _ in range(size + 1)]
    for mask in range(1 << size):
        KC = K0.copy()
        for x in range(size):
            if mask >> x & 1:
                KC[x, :] = K[x, :]
        level_sums[mask.bit_count()] += (
            identity - KC + q * nu0
        ).det(method="domain-ge")

    n_controls = [sp.factor((control * q)[0]) for control in controls]
    for j in range(size + 1):
        elevated = sp.Integer(0)
        if j <= size - 1:
            elevated += sp.Rational(size - j, size) * n_controls[j]
        if j:
            elevated += sp.Rational(j, size) * n_controls[j - 1]
        assert sp.factor(level_sums[j] / comb(size, j) - elevated) == 0
    print("PASS: exact row-mixture identity and degree elevation")
    print("PASS (EXACT REFUTATION): a singleton row-location determinant is negative")


def elementary(values, degree):
    if degree < 0:
        return sp.Integer(0)
    answer = [sp.Integer(1)] + [sp.Integer(0)] * degree
    for value in values:
        for j in range(degree, 0, -1):
            answer[j] += value * answer[j - 1]
    return answer[degree]


def unicycle_audit(states, K0, K, h):
    index = {state: i for i, state in enumerate(states)}
    cycle_states = [
        (2, 0), (6, 0), (4, 1), (5, 1),
        (4, 0), (2, 2), (3, 2),
    ]
    cycle = [index[state] for state in cycle_states]
    edges = list(zip(cycle, cycle[1:] + cycle[:1]))
    edges += [
        (index[(1, 1)], index[(2, 0)]),
        (index[(1, 2)], index[(2, 0)]),
    ]
    assert len(edges) == len(states)

    ratios = [sp.factor(K[a, b] / K0[a, b]) for a, b in edges]
    increments = [sp.factor(h[a] - h[b]) for a, b in edges]
    expected_ratios = [
        sp.Rational(20, 11), sp.Rational(3, 2), sp.Rational(1, 2),
        sp.Rational(20, 11), sp.Rational(6, 13), sp.Rational(20, 13),
        sp.Rational(2, 11), sp.Rational(2, 11), sp.Rational(2, 11),
    ]
    assert ratios == expected_ratios
    assert increments == [1, -1, 1, -1, 0, 1, -1, 0, 0]

    # The second line of the fixed-skeleton formula (16).
    packet = -sum(
        increments[e] * ratios[e]
        * elementary(ratios[:e] + ratios[e + 1:], 1)
        for e in range(len(cycle))
    )
    assert sp.factor(packet) == -sp.Rational(4804, 1859)

    # Independent direct colour-subset expansion of the first line.
    direct = 0
    for actual in combinations(range(len(edges)), 2):
        actual = set(actual)
        direct += (
            sp.prod(ratios[e] for e in actual)
            * sum(increments[e] for e in range(len(cycle)) if e not in actual)
        )
    assert sp.factor(direct - packet) == 0
    print("PASS: exact spanning-unicycle circulation identity")
    print("PASS (EXACT REFUTATION): one level-two unicycle packet is negative")


def simple_directed_cycles(kernel):
    """Enumerate nontrivial directed cycles once, with their minimum first."""
    size = kernel.rows
    answer = []
    for start in range(size):
        path = [start]
        seen = {start}

        def extend(source):
            for target in range(size):
                if source == target or not kernel[source, target]:
                    continue
                if target == start:
                    if len(path) >= 2:
                        answer.append(tuple(path))
                    continue
                # The unique minimum-vertex convention removes rotations.
                if target <= start or target in seen:
                    continue
                seen.add(target)
                path.append(target)
                extend(target)
                path.pop()
                seen.remove(target)

        extend(start)
    return answer


def cycle_attachment_audit(states, K0, K, nu0, q, h):
    """Check the all-attachment cycle formula and its smallest obstruction."""
    size = len(states)
    alpha = sp.symbols("alpha")
    Kalpha = K0 + alpha * (K - K0)
    Lalpha = sp.eye(size) - Kalpha
    index = {state: i for i, state in enumerate(states)}
    cycle = [index[state] for state in ((2, 0), (6, 0), (3, 2))]
    outside = [i for i in range(size) if i not in cycle]
    edges = list(zip(cycle, cycle[1:] + cycle[:1]))
    packet = sum(
        K0[u, v] * (h[u] - h[v])
        * sp.prod(
            Kalpha[x, y]
            for position, (x, y) in enumerate(edges)
            if position != distinguished
        )
        for distinguished, (u, v) in enumerate(edges)
    )
    contribution = sp.factor(
        Lalpha.extract(outside, outside).det(method="domain-ge") * packet
    )
    expected = sp.factor(
        -sp.Rational(9, 139375149056) * alpha * (7 * alpha + 13)
        * (2709 * alpha**4 - 9824 * alpha**3 - 60233 * alpha**2
           - 355368 * alpha + 646932)
    )
    assert contribution == expected
    controls = bernstein_controls(contribution, alpha, size - 1)
    assert controls == [
        0,
        -sp.Rational(783, 11534336),
        -sp.Rational(97821, 721616896),
        -sp.Rational(119626803, 600385257472),
        -sp.Rational(310593141, 1219532554240),
        -sp.Rational(331189569, 1115001192448),
        -sp.Rational(626218821, 1951252086784),
        -sp.Rational(22336947, 69687574528),
        -sp.Rational(1261215, 4355473408),
    ]

    # Independently sum every simple cycle and all its attachment forests at
    # two rational interpolation points.  This is the all-minors identity,
    # checked without expanding individual functional unicycles.
    cycles = simple_directed_cycles(K0)
    assert len(cycles) == 362
    one = sp.ones(size, 1)
    for value in (sp.Rational(1, 3), sp.Rational(2, 3)):
        mixed = K0 + value * (K - K0)
        laplacian = sp.eye(size) - mixed
        total = 0
        for directed_cycle in cycles:
            complement = [i for i in range(size) if i not in directed_cycle]
            forest = (
                laplacian.extract(complement, complement).det(method="domain-ge")
                if complement else sp.Integer(1)
            )
            cycle_edges = list(zip(
                directed_cycle,
                directed_cycle[1:] + directed_cycle[:1],
            ))
            circulation = sum(
                K0[u, v] * (h[u] - h[v])
                * sp.prod(
                    mixed[x, y]
                    for position, (x, y) in enumerate(cycle_edges)
                    if position != distinguished
                )
                for distinguished, (u, v) in enumerate(cycle_edges)
            )
            total += forest * circulation
        determinant = (
            sp.eye(size) - mixed + q * nu0
        ).det(method="domain-ge")
        assert sp.factor(total - determinant) == 0
    print("PASS: exact cycle-plus-all-attachments mixed-minor identity")
    print("PASS (EXACT REFUTATION): one all-attachment cycle packet is negative")


def main():
    states, K0, K, nu0, _, q = triangle_data()
    controls, h, delta_h = root_recurrence_audit(states, K0, K, q)
    row_mixture_audit(states, K0, K, nu0, q, controls, h, delta_h)
    unicycle_audit(states, K0, K, h)
    cycle_attachment_audit(states, K0, K, nu0, q, h)
    print("OPEN: the all-location, all-unicycle fixed-colour sign")


if __name__ == "__main__":
    main()
