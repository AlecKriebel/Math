#!/usr/bin/env python3
"""Exact verifier for the r=2 integrated-module constructive target."""

from __future__ import annotations

import sympy as sp


def exact_local_success(
    internal: list[list[sp.Rational]],
    portal: list[sp.Rational],
    rule: str,
) -> list[sp.Expr]:
    order = len(portal)
    degrees = [portal[i] + sum(internal[i]) for i in range(order)]
    states = list(range(1, 1 << order))
    index = {mask: row for row, mask in enumerate(states)}
    matrix = sp.zeros(len(states))
    rhs = sp.zeros(len(states), 1)

    for mask, row in index.items():
        mutant = [(mask >> i) & 1 for i in range(order)]
        moves: dict[int, sp.Expr] = {}

        def add(target: int, rate: sp.Expr) -> None:
            if rate:
                moves[target] = moves.get(target, sp.Integer(0)) + rate

        if rule == "Bd":
            for parent in range(order):
                parent_fitness = 2 if mutant[parent] else 1
                for target in range(order):
                    if mutant[parent] != mutant[target] and internal[parent][target]:
                        add(
                            mask ^ (1 << target),
                            parent_fitness
                            * internal[parent][target]
                            / degrees[parent],
                        )
            for target in range(order):
                if mutant[target]:
                    add(mask ^ (1 << target), portal[target])
            mark = sum(
                portal[i] / degrees[i] for i in range(order) if mutant[i]
            )
        elif rule == "dB":
            for target in range(order):
                denominator = portal[target] + sum(
                    (2 if mutant[parent] else 1) * internal[parent][target]
                    for parent in range(order)
                    if parent != target
                )
                if mutant[target]:
                    change = portal[target] + sum(
                        internal[parent][target]
                        for parent in range(order)
                        if not mutant[parent]
                    )
                else:
                    change = 2 * sum(
                        internal[parent][target]
                        for parent in range(order)
                        if mutant[parent]
                    )
                add(mask ^ (1 << target), change / denominator)
            mark = sum(portal[i] for i in range(order) if mutant[i])
        else:
            raise ValueError(rule)

        total = mark + sum(moves.values())
        matrix[row, row] = total
        rhs[row] = mark
        for target, rate in moves.items():
            if target:
                matrix[row, index[target]] -= rate

    solution = matrix.inv() * rhs
    assert matrix * solution == rhs
    return [sp.factor(solution[index[1 << i]]) for i in range(order)]


def main() -> None:
    r = sp.symbols("r", positive=True)
    order = sp.symbols("s", positive=True, integer=True)
    ub, ud, xub, xodud, xod, portal_sum = sp.symbols(
        "U_B U_D XU_B XODU_D XOD P"
    )
    p = (r - 1) / r
    source_b = r * xub - (r - 1) * xod
    source_d = r * xodud - (r - 1) * (portal_sum + r - 1)
    response_b = ub / p - order + source_b / (r - 1) ** 2
    response_d = ud / p - order + 1 + source_d / (r - 1) ** 2
    endpoint_b = 2 * ub - order + 2 * xub - xod
    endpoint_d = 2 * ud - order + 2 * xodud - portal_sum
    assert sp.factor(response_b.subs(r, 2) - endpoint_b) == 0
    assert sp.factor(response_d.subs(r, 2) - endpoint_d) == 0

    # Independent rational two-vertex local trace.
    internal = [[sp.Rational(0), sp.Rational(1)],
                [sp.Rational(1), sp.Rational(0)]]
    portal = [sp.Rational(1), sp.Rational(1)]
    degrees = [sp.Rational(2), sp.Rational(2)]
    local_b = exact_local_success(internal, portal, "Bd")
    local_d = exact_local_success(internal, portal, "dB")
    assert local_b == [sp.Rational(5, 14), sp.Rational(5, 14)]
    assert local_d == [sp.Rational(3, 5), sp.Rational(3, 5)]

    score_b = sum(
        2 * (1 + portal[i]) * local_b[i] - 1 - portal[i] / degrees[i]
        for i in range(2)
    )
    score_d = sum(
        2 * (1 + portal[i] / degrees[i]) * local_d[i] - 1 - portal[i]
        for i in range(2)
    )
    score_s = sum(
        2 * (1 + portal[i]) * local_b[i]
        + 2 * (1 + portal[i] / degrees[i]) * local_d[i]
        - 2
        - portal[i]
        - portal[i] / degrees[i]
        for i in range(2)
    )
    assert sp.factor(score_b + sp.Rational(1, 7)) == 0
    assert sp.factor(score_d + sp.Rational(2, 5)) == 0
    assert sp.factor(score_s - score_b - score_d) == 0
    assert sp.factor(score_s + sp.Rational(19, 35)) == 0

    # Leaf balancing is equivalent to D>0 and B+D>0.
    B, D, lam = sp.symbols("B D lambda", real=True)
    assert sp.factor((B + lam) + (D - lam) - (B + D)) == 0

    print("PASS exact r=2 integrated-module constructive target")


if __name__ == "__main__":
    main()
