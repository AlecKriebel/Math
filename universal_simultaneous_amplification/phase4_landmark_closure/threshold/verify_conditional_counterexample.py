#!/usr/bin/env python3
"""Exact from-definitions counterexample to a proposed conditional inequality.

The proposed implication was

    a_dB(r) > p  ==>  r (a_Bd(r)-p) <= a_Bd(1/r),
    p = 1 - 1/r.

The unit-weight three-vertex path violates it on a nonempty exact interval.
This script constructs both subset chains rather than importing a fixation
formula.
"""

from __future__ import annotations

from collections import defaultdict

import sympy as sp


r = sp.symbols("r", positive=True)


def fixation_average(rule: str) -> sp.Expr:
    weights = (
        (sp.Integer(0), sp.Integer(1), sp.Integer(0)),
        (sp.Integer(1), sp.Integer(0), sp.Integer(1)),
        (sp.Integer(0), sp.Integer(1), sp.Integer(0)),
    )
    degree = [sum(row) for row in weights]
    states = list(range(1, 7))
    index = {mask: position for position, mask in enumerate(states)}
    matrix = sp.eye(6)
    rhs = sp.zeros(6, 1)

    for mask in states:
        changes: dict[int, sp.Expr] = defaultdict(lambda: sp.Integer(0))
        if rule == "Bd":
            total = sum(r if mask >> vertex & 1 else 1 for vertex in range(3))
            for parent in range(3):
                parent_fitness = r if mask >> parent & 1 else 1
                for target in range(3):
                    if not weights[parent][target]:
                        continue
                    probability = (
                        parent_fitness
                        / total
                        * weights[parent][target]
                        / degree[parent]
                    )
                    if mask >> parent & 1:
                        new_mask = mask | (1 << target)
                    else:
                        new_mask = mask & ~(1 << target)
                    changes[new_mask] += probability
        elif rule == "dB":
            for target in range(3):
                denominator = sum(
                    weights[parent][target]
                    * (r if mask >> parent & 1 else 1)
                    for parent in range(3)
                )
                for parent in range(3):
                    if not weights[parent][target]:
                        continue
                    probability = (
                        sp.Rational(1, 3)
                        * weights[parent][target]
                        * (r if mask >> parent & 1 else 1)
                        / denominator
                    )
                    if mask >> parent & 1:
                        new_mask = mask | (1 << target)
                    else:
                        new_mask = mask & ~(1 << target)
                    changes[new_mask] += probability
        else:
            raise ValueError(rule)

        row = index[mask]
        for new_mask, probability in changes.items():
            if new_mask == 7:
                rhs[row] += probability
            elif new_mask:
                matrix[row, index[new_mask]] -= probability

    values = matrix.inv() * rhs
    return sp.factor(sum(values[index[1 << vertex]] for vertex in range(3)) / 3)


def assert_zero(expression: sp.Expr) -> None:
    assert sp.cancel(expression) == 0, sp.factor(expression)


def main() -> None:
    a_bd = fixation_average("Bd")
    a_db = fixation_average("dB")
    declared_bd = r**2 * (2 * r + 3) / ((r + 2) * (2 * r**2 + r + 2))
    declared_db = (5 * r + 1) / (9 * (r + 1))
    assert_zero(a_bd - declared_bd)
    assert_zero(a_db - declared_db)

    p = 1 - 1 / r
    reverse_bd = sp.factor(a_bd.subs(r, 1 / r))
    conditional_excess = sp.factor(a_db - p)
    proposed_margin = sp.factor(reverse_bd - r * (a_bd - p))

    assert_zero(
        reverse_bd - (3 * r + 2) / ((2 * r + 1) * (2 * r**2 + r + 2))
    )
    assert_zero(
        conditional_excess + (4 * r**2 - r - 9) / (9 * r * (r + 1))
    )
    assert_zero(
        proposed_margin
        + 2 * r**2 * (r - 1) / ((r + 2) * (2 * r + 1) * (2 * r**2 + r + 2))
    )

    # The premise holds for 1<r<(1+sqrt(145))/8, while the proposed margin
    # is strictly negative for every r>1.
    cutoff = (1 + sp.sqrt(145)) / 8
    assert sp.N(cutoff, 30) > sp.Rational(3, 2)

    at = {r: sp.Rational(3, 2)}
    exact = {
        "p": sp.factor(p.subs(at)),
        "a_Bd(r)": sp.factor(a_bd.subs(at)),
        "a_Bd(1/r)": sp.factor(reverse_bd.subs(at)),
        "a_dB(r)": sp.factor(a_db.subs(at)),
        "premise excess": sp.factor(conditional_excess.subs(at)),
        "proposed margin": sp.factor(proposed_margin.subs(at)),
    }
    expected = {
        "p": sp.Rational(1, 3),
        "a_Bd(r)": sp.Rational(27, 56),
        "a_Bd(1/r)": sp.Rational(13, 64),
        "a_dB(r)": sp.Rational(17, 45),
        "premise excess": sp.Rational(2, 45),
        "proposed margin": -sp.Rational(9, 448),
    }
    assert exact == expected, (exact, expected)
    for label, value in exact.items():
        print(f"{label}: {value}")
    print(f"premise interval endpoint: {cutoff}")
    print("PASS: exact P3 counterexample")


if __name__ == "__main__":
    main()
