#!/usr/bin/env python3
"""Independent exact checks for hostile endpoint candidates.

This file does not import the floating search.  It constructs the effective
flip chain over exact rationals from the update definitions, checks every row,
and solves the absorbing equations.  It also proves a symbolic separator for
the closest non-complete order-four support found by the optimizer.

Finite checks are diagnostics, not a universal theorem.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import product

import sympy as sp


R = sp.Rational(3, 2)


def complete_baseline(n: int, rule: str) -> sp.Rational:
    if rule == "Bd":
        return sp.Rational(3 ** (n - 1), 3**n - 2**n)
    return sp.Rational(
        (n - 1) * 3 ** (n - 2), n * (3 ** (n - 1) - 2 ** (n - 1))
    )


def exact_fixation(weights, rule: str):
    """Exact uniform-singleton fixation after analytic self-loop deletion."""
    weights = tuple(tuple(map(sp.Rational, row)) for row in weights)
    n = len(weights)
    full = (1 << n) - 1
    degree = tuple(sum(row, sp.Integer(0)) for row in weights)
    assert all(value > 0 for value in degree)
    matrix = sp.eye(full - 1)
    rhs = sp.zeros(full - 1, 1)

    for state in range(1, full):
        row = state - 1
        changes = defaultdict(lambda: sp.Integer(0))
        for target in range(n):
            target_mutant = bool(state & (1 << target))
            if rule == "Bd":
                mutant = sum(
                    (
                        weights[parent][target] / degree[parent]
                        if state & (1 << parent)
                        else 0
                    )
                    for parent in range(n)
                )
                resident = sum(
                    (
                        weights[parent][target] / degree[parent]
                        if not state & (1 << parent)
                        else 0
                    )
                    for parent in range(n)
                )
                rate = resident if target_mutant else R * mutant
            elif rule == "dB":
                mutant = sum(
                    weights[parent][target]
                    for parent in range(n)
                    if state & (1 << parent)
                )
                resident = degree[target] - mutant
                denominator = R * mutant + resident
                assert denominator > 0
                rate = resident / denominator if target_mutant else R * mutant / denominator
            else:
                raise ValueError(rule)
            if rate:
                changes[state ^ (1 << target)] += sp.cancel(rate)

        total = sp.cancel(sum(changes.values(), sp.Integer(0)))
        assert total > 0
        row_sum = sp.Integer(0)
        for target, rate in changes.items():
            probability = sp.cancel(rate / total)
            assert probability > 0
            row_sum += probability
            if target == full:
                rhs[row] += probability
            elif target:
                matrix[row, target - 1] -= probability
        assert sp.cancel(row_sum - 1) == 0

    solution = tuple(next(iter(sp.linsolve((matrix, rhs)))))
    assert matrix * sp.Matrix(solution) == rhs
    density = sp.cancel(
        sum(solution[(1 << vertex) - 1] for vertex in range(n)) / n
    )
    return density


def graph(n: int, edge_weights):
    weights = [[sp.Integer(0) for _ in range(n)] for _ in range(n)]
    for i, j, value in edge_weights:
        weights[i][j] = weights[j][i] = sp.Rational(value)
    return tuple(map(tuple, weights))


def hostile_corpus():
    yield "K4", graph(4, [(i, j, 1) for i in range(4) for j in range(i + 1, 4)])
    yield "weighted-star", graph(4, [(0, 1, 1), (0, 2, 10), (0, 3, 100)])
    yield "separated-path", graph(4, [(0, 1, 1), (1, 2, 6), (2, 3, 36)])
    yield "rationalized-nearest-five-edge", graph(
        4,
        [(0, 1, 1), (0, 2, sp.Rational(11, 70)), (0, 3, 1), (1, 2, 1), (2, 3, 1)],
    )
    yield "extreme-complete", graph(
        4,
        [
            (0, 1, 1),
            (0, 2, 10),
            (0, 3, 100),
            (1, 2, 1000),
            (1, 3, 10000),
            (2, 3, 100000),
        ],
    )
    yield "weakly-completed-star", graph(
        5,
        [(0, i, 1000) for i in range(1, 5)]
        + [(i, j, 1) for i in range(1, 5) for j in range(i + 1, 5)],
    )
    yield "irregular-core-periphery", graph(
        5,
        [(0, 1, 100), (0, 2, 100), (1, 2, 100),
         (0, 3, 1), (1, 3, 3), (2, 3, 7),
         (0, 4, sp.Rational(1, 100)), (1, 4, 2), (2, 4, 11), (3, 4, sp.Rational(1, 10))],
    )
    # Exact dB-amplifying three-blade windmill.  It is a particularly hostile
    # endpoint point because the dB ratio is genuinely above one; its Bd loss
    # must carry the separator.
    windmill_edges = []
    for (left, right), outer, internal in zip(
        ((1, 2), (3, 4), (5, 6)), (100, 10, 1), (600, 1200, 1800)
    ):
        windmill_edges.extend(
            ((left, right, internal), (0, left, outer), (0, right, outer))
        )
    yield "exact-dB-amplifying-windmill", graph(7, windmill_edges)
    # Rational reconstruction of an apparent enormous Pareto violation from
    # an ill-conditioned double solve.  Exact arithmetic shows that it is a
    # strong suppressor under both rules.
    yield "resolved-separated-star-artifact", graph(
        7,
        [
            (0, 1, 480000000),
            (0, 2, 370000),
            (0, 3, 2),
            (0, 4, 37000000000000),
            (0, 5, 133000000000000000),
            (0, 6, 1),
        ],
    )
    yield "affine-lower-multiplier-witness", graph(
        7,
        [
            (0, 1, 642311627470),
            (0, 2, 641177352713),
            (1, 2, 2172410361743),
            (0, 3, 5),
            (0, 4, 1665053),
            (3, 4, 4231492313836),
            (0, 5, 79),
            (0, 6, 71),
            (5, 6, 5921340201086),
        ],
    )


def exact_uniform_star_lumped(n: int, rule: str):
    """Exact two-count chain for the unit-weight star on ``n`` vertices."""
    m = n - 1
    states = tuple(
        (center, leaves)
        for center in (0, 1)
        for leaves in range(m + 1)
        if (center, leaves) not in ((0, 0), (1, m))
    )
    index = {state: row for row, state in enumerate(states)}
    matrix = sp.eye(len(states))
    rhs = sp.zeros(len(states), 1)
    for state, row in index.items():
        center, leaves = state
        changes = []
        if rule == "Bd":
            if center and leaves < m:
                changes.append(((center, leaves + 1), R * (m - leaves) / m))
            if not center and leaves:
                changes.extend(
                    (((center, leaves - 1), sp.Rational(leaves, m)),
                     ((1, leaves), R * leaves))
                )
            if center and leaves < m:
                changes.append(((0, leaves), m - leaves))
        elif rule == "dB":
            if center and leaves < m:
                changes.extend(
                    (((center, leaves + 1), m - leaves),
                     ((0, leaves), sp.Rational(m - leaves, 1) / (R * leaves + m - leaves)))
                )
            if not center and leaves:
                changes.extend(
                    (((center, leaves - 1), leaves),
                     ((1, leaves), R * leaves / (R * leaves + m - leaves)))
                )
        else:
            raise ValueError(rule)
        total = sp.cancel(sum(rate for _, rate in changes))
        assert total > 0
        for target, rate in changes:
            probability = sp.cancel(rate / total)
            if target == (1, m):
                rhs[row] += probability
            elif target != (0, 0):
                matrix[row, index[target]] -= probability
    solution = tuple(next(iter(sp.linsolve((matrix, rhs)))))
    assert matrix * sp.Matrix(solution) == rhs
    return sp.cancel(
        (solution[index[(1, 0)]] + m * solution[index[(0, 1)]]) / n
    )


def symbolic_one_chord_certificate():
    """Exact two-orbit chain for K_{2,2} plus one weight-a chord.

    Classes A and B each have two vertices.  Every A--B edge has weight one,
    the A chord has weight a, and the B chord is absent.  The optimizer's
    closest proper-support product point lies in this family.
    """
    a = sp.symbols("a", nonnegative=True)
    states = tuple(
        (i, j)
        for i, j in product(range(3), repeat=2)
        if (i, j) not in ((0, 0), (2, 2))
    )
    index = {state: row for row, state in enumerate(states)}
    d_a = a + 2
    d_b = sp.Integer(2)

    def changes(state, rule):
        i, j = state
        answer = []
        if rule == "Bd":
            if i < 2:
                answer.append(((i + 1, j), (2 - i) * R * (i * a / d_a + j / d_b)))
            if i > 0:
                answer.append(((i - 1, j), i * ((2 - i) * a / d_a + (2 - j) / d_b)))
            if j < 2:
                answer.append(((i, j + 1), (2 - j) * R * i / d_a))
            if j > 0:
                answer.append(((i, j - 1), j * (2 - i) / d_a))
        else:
            if i < 2:
                mutant = i * a + j
                resident = d_a - mutant
                if mutant:
                    answer.append(((i + 1, j), (2 - i) * R * mutant / (R * mutant + resident)))
            if i > 0:
                mutant = (i - 1) * a + j
                resident = (2 - i) * a + (2 - j)
                if resident:
                    answer.append(((i - 1, j), i * resident / (R * mutant + resident)))
            if j < 2 and i:
                mutant = i
                resident = 2 - i
                answer.append(((i, j + 1), (2 - j) * R * mutant / (R * mutant + resident)))
            if j > 0 and i < 2:
                mutant = i
                resident = 2 - i
                answer.append(((i, j - 1), j * resident / (R * mutant + resident)))
        return [(target, sp.cancel(rate)) for target, rate in answer if rate != 0]

    def solve(rule):
        matrix = sp.eye(len(states))
        rhs = sp.zeros(len(states), 1)
        for state, row in index.items():
            outgoing = changes(state, rule)
            total = sp.factor(sum(rate for _, rate in outgoing))
            assert total != 0
            for target, rate in outgoing:
                probability = sp.cancel(rate / total)
                if target == (2, 2):
                    rhs[row] += probability
                elif target != (0, 0):
                    matrix[row, index[target]] -= probability
        solution = matrix.inv() * rhs
        return sp.factor((solution[index[(1, 0)]] + solution[index[(0, 1)]]) / 2)

    bd = solve("Bd")
    db = solve("dB")
    expected_bd = sp.factor(
        27
        * (66*a**5 + 1333*a**4 + 8629*a**3 + 23300*a**2 + 26300*a + 10000)
        / (5 * (972*a**5 + 17469*a**4 + 110011*a**3 + 299900*a**2 + 341900*a + 130000))
    )
    expected_db = sp.factor(
        (450*a**4 + 6110*a**3 + 27602*a**2 + 48219*a + 28512)
        / (4 * (450*a**4 + 5075*a**3 + 20362*a**2 + 33953*a + 20196))
    )
    assert sp.cancel(bd - expected_bd) == 0
    assert sp.cancel(db - expected_db) == 0

    x = sp.cancel(bd / complete_baseline(4, "Bd"))
    y = sp.cancel(db / complete_baseline(4, "dB"))
    arithmetic_numerator, arithmetic_denominator = map(
        sp.expand, sp.fraction(sp.cancel(2 - x - y))
    )
    product_numerator, product_denominator = map(
        sp.expand, sp.fraction(sp.cancel(1 - x * y))
    )
    db_loss_numerator, db_loss_denominator = map(
        sp.expand, sp.fraction(sp.cancel(1 - y))
    )
    for polynomial in (
        arithmetic_numerator,
        product_numerator,
        db_loss_numerator,
        arithmetic_denominator,
        product_denominator,
        db_loss_denominator,
    ):
        coefficients = sp.Poly(polynomial, a).all_coeffs()
        assert coefficients and all(coefficient > 0 for coefficient in coefficients)
    return bd, db, arithmetic_numerator, product_numerator


def main():
    bd_symbolic, db_symbolic, arithmetic_certificate, product_certificate = (
        symbolic_one_chord_certificate()
    )
    print("PASS: exact one-chord lumped Bd/dB chains")
    print("PASS: one-chord dB, normalized-arithmetic, and product gaps have positive coefficients")
    print(f"symbolic Bd = {bd_symbolic}")
    print(f"symbolic dB = {db_symbolic}")
    print(f"arithmetic numerator = {arithmetic_certificate}")
    print(f"product numerator = {product_certificate}")

    count = 0
    affine_lower = None
    for label, weights in hostile_corpus():
        n = len(weights)
        bd = exact_fixation(weights, "Bd")
        db = exact_fixation(weights, "dB")
        x = sp.cancel(bd / complete_baseline(n, "Bd"))
        y = sp.cancel(db / complete_baseline(n, "dB"))
        product_ratio = sp.cancel(x * y)
        minimum_ratio = min(x, y)
        arithmetic_ratio = sp.cancel((x + y) / 2)
        assert product_ratio <= 1, (label, product_ratio)
        assert minimum_ratio <= 1, (label, minimum_ratio)
        assert arithmetic_ratio <= 1, (label, arithmetic_ratio)
        if label == "K4":
            assert x == y == 1
        else:
            assert product_ratio < 1 and minimum_ratio < 1 and arithmetic_ratio < 1
        if label == "exact-dB-amplifying-windmill":
            assert y > 1 and x < 1
        if label == "affine-lower-multiplier-witness":
            affine_lower = sp.cancel((y - 1) / (y - x))
            assert y > 1 > x
            assert affine_lower > sp.Rational(177, 2000)
            assert sp.cancel(
                sp.Rational(177, 2000) * x
                + sp.Rational(1823, 2000) * y
            ) > 1
        print(
            f"PASS {label}: x~{sp.N(x, 10)}, y~{sp.N(y, 10)}, "
            f"P~{sp.N(product_ratio, 10)}, M~{sp.N(minimum_ratio, 10)}, "
            f"A~{sp.N(arithmetic_ratio, 10)}"
        )
        count += 1
    print(f"PASS: {count} exact hostile rational endpoint graphs")

    # A fixed graph-independent affine separator would have the form
    # lambda*x+(1-lambda)*y <= 1.  The exact dB witness above rules out small
    # lambda.  The unit star on ten vertices rules out large lambda.
    assert affine_lower is not None
    full_star = graph(4, [(0, 1, 1), (0, 2, 1), (0, 3, 1)])
    for rule in ("Bd", "dB"):
        assert exact_uniform_star_lumped(4, rule) == exact_fixation(full_star, rule)
    star_x = sp.cancel(
        exact_uniform_star_lumped(10, "Bd") / complete_baseline(10, "Bd")
    )
    star_y = sp.cancel(
        exact_uniform_star_lumped(10, "dB") / complete_baseline(10, "dB")
    )
    affine_upper = sp.cancel((1 - star_y) / (star_x - star_y))
    assert star_x > 1 > star_y
    assert affine_upper < sp.Rational(7, 12)
    assert sp.cancel(sp.Rational(7, 12) * star_x + sp.Rational(5, 12) * star_y) > 1
    print(
        "PASS: exact affine-multiplier witnesses force "
        f"lambda > 177/2000 and lambda < 7/12 "
        f"(actual witness crossings ~{sp.N(affine_lower, 12)} and "
        f"~{sp.N(affine_upper, 12)})"
    )


if __name__ == "__main__":
    main()
