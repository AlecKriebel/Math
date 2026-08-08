#!/usr/bin/env python3
"""Exact subset-chain audit of the universal portal-clone expansion.

The generic three-vertex calculation keeps every symmetric internal tangent
and every portal tangent symbolic.  Additional exact rational checks exercise
orders four and five.  The analytic all-order coefficient extraction is in
SECOND_ORDER_CLONE_OBSTRUCTION.md.
"""

from __future__ import annotations

import sympy as sp


def killed_chain_coefficients(
    rule: str, internal: list[list[sp.Expr]], portal_tangent: list[sp.Expr], r: sp.Expr
) -> tuple[list[int], sp.Matrix, sp.Matrix, sp.Matrix]:
    n = len(portal_tangent)
    epsilon = sp.symbols("epsilon")
    states = list(range(1, 1 << n))
    index = {mask: row for row, mask in enumerate(states)}
    matrix = sp.zeros(len(states))
    rhs = sp.zeros(len(states), 1)
    portal = [1 + epsilon * portal_tangent[i] for i in range(n)]
    degree = [
        portal[i] + epsilon * sum(internal[i][j] for j in range(n))
        for i in range(n)
    ]

    for mask, row in index.items():
        mutant = [(mask >> i) & 1 for i in range(n)]
        changes: dict[int, sp.Expr] = {}
        if rule == "Bd":
            for parent in range(n):
                fitness = r if mutant[parent] else 1
                for target in range(n):
                    if internal[parent][target] and mutant[parent] != mutant[target]:
                        next_mask = mask ^ (1 << target)
                        changes[next_mask] = changes.get(next_mask, 0) + (
                            fitness
                            * epsilon
                            * internal[parent][target]
                            / degree[parent]
                        )
            for target in range(n):
                if mutant[target]:
                    next_mask = mask ^ (1 << target)
                    changes[next_mask] = changes.get(next_mask, 0) + portal[target]
            mark = (r - 1) * sum(
                (portal[i] / degree[i] for i in range(n) if mutant[i]),
                sp.Integer(0),
            )
        elif rule == "dB":
            fitness = [r if value else 1 for value in mutant]
            for target in range(n):
                denominator = portal[target] + epsilon * sum(
                    internal[target][parent] * fitness[parent] for parent in range(n)
                )
                if mutant[target]:
                    recovery = portal[target] + epsilon * sum(
                        (
                            internal[target][parent]
                            for parent in range(n)
                            if not mutant[parent]
                        ),
                        sp.Integer(0),
                    )
                    next_mask = mask ^ (1 << target)
                    changes[next_mask] = changes.get(next_mask, 0) + recovery / denominator
                else:
                    invasion = r * epsilon * sum(
                        (
                            internal[target][parent]
                            for parent in range(n)
                            if mutant[parent]
                        ),
                        sp.Integer(0),
                    )
                    next_mask = mask ^ (1 << target)
                    changes[next_mask] = changes.get(next_mask, 0) + invasion / denominator
            mark = (r - 1) * sum(
                (portal[i] for i in range(n) if mutant[i]), sp.Integer(0)
            )
        else:
            raise ValueError(rule)

        matrix[row, row] = mark + sum(changes.values())
        rhs[row] = mark
        for target, rate in changes.items():
            if target:
                matrix[row, index[target]] -= rate

    matrices = [
        matrix.subs(epsilon, 0),
        matrix.diff(epsilon).subs(epsilon, 0),
        matrix.diff(epsilon, 2).subs(epsilon, 0) / 2,
    ]
    vectors = [
        rhs.subs(epsilon, 0),
        rhs.diff(epsilon).subs(epsilon, 0),
        rhs.diff(epsilon, 2).subs(epsilon, 0) / 2,
    ]
    u0 = matrices[0].inv() * vectors[0]
    u1 = matrices[0].inv() * (vectors[1] - matrices[1] * u0)
    u2 = matrices[0].inv() * (
        vectors[2] - matrices[1] * u1 - matrices[2] * u0
    )
    return states, u0, u1, u2


def expected_singleton_coefficients(
    rule: str,
    vertex: int,
    internal: list[list[sp.Expr]],
    portal_tangent: list[sp.Expr],
    r: sp.Expr,
) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    n = len(portal_tangent)
    alpha = [sum(internal[i][j] for j in range(n)) for i in range(n)]
    c = [portal_tangent[i] + alpha[i] for i in range(n)]
    p = (r - 1) / r
    if rule == "Bd":
        first = -(r - 1) * c[vertex] / r**2
        second = (r - 1) / r**3 * (
            c[vertex] ** 2
            + (r - 1)
            * sum(internal[vertex][j] * c[j] for j in range(n))
        )
    elif rule == "dB":
        first = (r - 1) * c[vertex] / r**2
        second = -(r - 1) ** 2 / r**3 * (
            c[vertex] ** 2
            + sum(internal[vertex][j] * c[j] for j in range(n))
            + (r - 1) * sum(internal[vertex][j] ** 2 for j in range(n))
        )
    else:
        raise ValueError(rule)
    return p, sp.factor(first), sp.factor(second)


def audit_instance(
    internal: list[list[sp.Expr]], portal_tangent: list[sp.Expr], r: sp.Expr
) -> None:
    n = len(portal_tangent)
    alpha = [sum(internal[i][j] for j in range(n)) for i in range(n)]
    c = [portal_tangent[i] + alpha[i] for i in range(n)]
    edge_square = sum(
        internal[i][j] ** 2 for i in range(n) for j in range(i + 1, n)
    )
    responses: dict[str, tuple[sp.Expr, sp.Expr]] = {}

    for rule in ("Bd", "dB"):
        states, u0, u1, u2 = killed_chain_coefficients(
            rule, internal, portal_tangent, r
        )
        index = {mask: row for row, mask in enumerate(states)}
        singleton_rows = [index[1 << i] for i in range(n)]
        for mask, row in index.items():
            mutant = [i for i in range(n) if (mask >> i) & 1]
            base = sum(c[i] for i in mutant)
            if rule == "Bd":
                expected_first = -(r - 1) * base / r ** (len(mutant) + 1)
            else:
                internal_mutant = sum(
                    internal[i][j]
                    for position, i in enumerate(mutant)
                    for j in mutant[position + 1 :]
                )
                expected_first = (r - 1) * (
                    base + (r - 1) * internal_mutant
                ) / r ** (len(mutant) + 1)
            assert sp.factor(u1[row] - expected_first) == 0
        for vertex, row in enumerate(singleton_rows):
            expected = expected_singleton_coefficients(
                rule, vertex, internal, portal_tangent, r
            )
            assert sp.factor(u0[row] - expected[0]) == 0
            assert sp.factor(u1[row] - expected[1]) == 0
            assert sp.factor(u2[row] - expected[2]) == 0

        U1 = sp.factor(sum(u1[row] for row in singleton_rows))
        U2 = sp.factor(sum(u2[row] for row in singleton_rows))
        if rule == "Bd":
            first = sp.factor(
                r**2 * U1 / (r - 1) ** 2 + sum(c) / (r - 1)
            )
            second = sp.factor(
                r**2 * U2 / (r - 1) ** 2
                + r
                * sum(portal_tangent[i] * u1[singleton_rows[i]] for i in range(n))
                / (r - 1) ** 2
                - sum(alpha[i] * c[i] for i in range(n)) / (r - 1)
            )
        else:
            first = sp.factor(
                r**2 * U1 / (r - 1) ** 2 - sum(c) / (r - 1)
            )
            second = sp.factor(
                r**2 * U2 / (r - 1) ** 2
                - r
                * sum(alpha[i] * u1[singleton_rows[i]] for i in range(n))
                / (r - 1) ** 2
                + sum(alpha[i] * c[i] for i in range(n)) / (r - 1)
            )
        responses[rule] = (first, second)

    expected_db = -(
        sum(value**2 for value in c) + 2 * (r - 1) * edge_square
    ) / r
    assert responses["Bd"] == (0, 0)
    assert responses["dB"][0] == 0
    assert sp.factor(responses["dB"][1] - expected_db) == 0


def main() -> None:
    r = sp.symbols("r", positive=True)
    a, b, c, x, y, z = sp.symbols("a b c x y z", real=True)
    generic_three = [[0, a, b], [a, 0, c], [b, c, 0]]
    audit_instance(generic_three, [x, y, z], r)

    audit_instance(
        [
            [0, sp.Rational(1, 3), 0, sp.Rational(2, 5)],
            [sp.Rational(1, 3), 0, sp.Rational(4, 7), 0],
            [0, sp.Rational(4, 7), 0, sp.Rational(3, 8)],
            [sp.Rational(2, 5), 0, sp.Rational(3, 8), 0],
        ],
        [sp.Rational(2, 3), -sp.Rational(1, 5), sp.Rational(5, 11), -sp.Rational(3, 7)],
        sp.Rational(7, 4),
    )

    audit_instance(
        [
            [0, 1, 0, 0, sp.Rational(1, 2)],
            [1, 0, sp.Rational(2, 3), 0, 0],
            [0, sp.Rational(2, 3), 0, sp.Rational(3, 5), 0],
            [0, 0, sp.Rational(3, 5), 0, sp.Rational(4, 7)],
            [sp.Rational(1, 2), 0, 0, sp.Rational(4, 7), 0],
        ],
        [1, -sp.Rational(1, 2), sp.Rational(1, 3), -sp.Rational(1, 4), sp.Rational(1, 5)],
        sp.Rational(2),
    )

    print("PASS: generic labelled order-three subset chain matches the all-order expansion")
    print("PASS: independent exact order-four and order-five instances")
    print("PASS: Bd epsilon^2 coefficient vanishes; dB quadratic is negative definite")


if __name__ == "__main__":
    main()
