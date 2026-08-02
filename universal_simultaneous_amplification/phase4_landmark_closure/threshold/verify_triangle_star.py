#!/usr/bin/env python3
"""Exact certificate for the singular-triangle / clique-star construction.

The program derives the four-state (equivalently six-subset) internal chains
directly from the Bd and dB definitions.  It then checks the closed forms used
in the asymptotic proof and the two rare-migration rate ratios.  No sampled
fixation probabilities enter any assertion.
"""

from __future__ import annotations

from collections import defaultdict

import sympy as sp


r, delta = sp.symbols("r delta", positive=True)


def singleton_fixations(rule: str) -> list[sp.Expr]:
    """Solve the full subset chain of the weighted triangle exactly."""
    weights = (
        (sp.Integer(0), delta, sp.Integer(1)),
        (delta, sp.Integer(0), delta),
        (sp.Integer(1), delta, sp.Integer(0)),
    )
    degree = [sum(row) for row in weights]
    transient = list(range(1, 7))
    index = {mask: i for i, mask in enumerate(transient)}
    matrix = sp.eye(len(transient))
    rhs = sp.zeros(len(transient), 1)

    for mask in transient:
        transitions: dict[int, sp.Expr] = defaultdict(lambda: sp.Integer(0))
        if rule == "Bd":
            total_fitness = sum(r if mask >> u & 1 else 1 for u in range(3))
            for parent in range(3):
                parent_fitness = r if mask >> parent & 1 else 1
                for target in range(3):
                    if not weights[parent][target]:
                        continue
                    probability = (
                        parent_fitness
                        / total_fitness
                        * weights[parent][target]
                        / degree[parent]
                    )
                    if mask >> parent & 1:
                        new_mask = mask | (1 << target)
                    else:
                        new_mask = mask & ~(1 << target)
                    transitions[new_mask] += probability
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
                    transitions[new_mask] += probability
        else:
            raise ValueError(rule)

        row = index[mask]
        for new_mask, probability in transitions.items():
            if new_mask == 7:
                rhs[row] += probability
            elif new_mask:
                matrix[row, index[new_mask]] -= probability

    solution = matrix.inv() * rhs
    return [sp.factor(solution[index[1 << vertex]]) for vertex in range(3)]


def assert_zero(expression: sp.Expr) -> None:
    assert sp.cancel(expression) == 0, sp.factor(expression)


def main() -> None:
    bd = singleton_fixations("Bd")
    db = singleton_fixations("dB")

    bd_denominator = (
        4 * delta**3 * r**4
        + 12 * delta**3 * r**3
        + 13 * delta**3 * r**2
        + 12 * delta**3 * r
        + 4 * delta**3
        + 16 * delta**2 * r**4
        + 52 * delta**2 * r**3
        + 83 * delta**2 * r**2
        + 52 * delta**2 * r
        + 16 * delta**2
        + 12 * delta * r**4
        + 24 * delta * r**3
        + 15 * delta * r**2
        + 24 * delta * r
        + 12 * delta
        + 9 * r**2
    )
    bd_average_declared = r**2 * (
        4 * delta**3 * r**2
        + 8 * delta**3 * r
        + 3 * delta**3
        + 16 * delta**2 * r**2
        + 36 * delta**2 * r
        + 21 * delta**2
        + 12 * delta * r**2
        + 12 * delta * r
        + 5 * delta
        + 3
    ) / bd_denominator

    db_denominator = 3 * (r + 1) * (
        6 * delta**2 * r
        + 3 * delta * r**2
        + delta * r
        + 3 * delta
        + 2 * r
    )
    db_average_declared = 2 * r * (
        5 * delta**2 * r
        + delta**2
        + 3 * delta * r**2
        + 3 * delta * r
        + delta
        + r
        + 1
    ) / db_denominator
    db_j_declared = r * (
        8 * delta**2 * r
        + delta**2
        + 5 * delta * r**2
        + 7 * delta * r
        + 3 * delta
        + r**2
        + 3 * r
        + 2
    ) / (
        (delta + 1)
        * (r + 1)
        * (
            6 * delta**2 * r
            + 3 * delta * r**2
            + delta * r
            + 3 * delta
            + 2 * r
        )
    )

    bd_average = sp.factor(sum(bd) / 3)
    db_average = sp.factor(sum(db) / 3)
    degrees = (delta + 1, 2 * delta, delta + 1)
    db_j = sp.factor(sum(value / degree for value, degree in zip(db, degrees)))

    assert_zero(bd[0] - bd[2])
    assert_zero(db[0] - db[2])
    assert_zero(bd_average - bd_average_declared)
    assert_zero(db_average - db_average_declared)
    assert_zero(db_j - db_j_declared)

    assert sp.limit(bd[0], delta, 0, dir="+") == 0
    assert sp.limit(bd[1], delta, 0, dir="+") == 1
    assert sp.limit(db[0], delta, 0, dir="+") == sp.Rational(1, 2)
    assert sp.limit(db[1], delta, 0, dir="+") == 0
    assert sp.limit(bd_average, delta, 0, dir="+") == sp.Rational(1, 3)
    assert sp.limit(db_average, delta, 0, dir="+") == sp.Rational(1, 3)
    assert sp.factor(sp.limit(db_j, delta, 0, dir="+") - (r + 2) / 2) == 0

    db_j_reverse = sp.factor(db_j.subs(r, 1 / r))
    assert sp.factor(
        sp.limit(db_j_reverse, delta, 0, dir="+") - (2 * r + 1) / (2 * r)
    ) == 0
    effective_db_ratio = sp.factor(
        sp.limit(r**2 * db_j / db_j_reverse, delta, 0, dir="+")
    )
    assert effective_db_ratio == r**3 * (r + 2) / (2 * r + 1)

    inverse_degree_sum = sp.factor(sum(1 / degree for degree in degrees))
    assert_zero(inverse_degree_sum - (5 * delta + 1) / (2 * delta * (delta + 1)))
    assert sp.limit(2 * delta * inverse_degree_sum, delta, 0, dir="+") == 1

    # Macro-chain identity.  A resident center with one mutant leaf has
    # favorable center-conversion rate A and adverse leaf-loss rate D.  Once
    # the center is mutant, each resident leaf is converted at rate B and the
    # center reverts at rate C.  The favorable direct-sweep probability is
    # A/(A+D) * (B/(B+C))**(M-1).
    A, B, C, D, M = sp.symbols("A B C D M", positive=True)
    first_step = sp.factor(A / (A + D))
    one_sweep_step = sp.factor(B / (B + C))
    assert_zero(first_step - 1 / (1 + D / A))
    assert_zero(one_sweep_step - 1 / (1 + C / B))

    # Exact threshold algebra when A/D=x and the leaf establishment tends 1/3.
    x = sp.symbols("x", positive=True)
    threshold_difference = sp.factor(sp.Rational(1, 3) * x / (x + 1) - (r - 1) / r)
    assert_zero(
        threshold_difference
        - ((3 - 2 * r) * x - 3 * (r - 1)) / (3 * r * (x + 1))
    )

    print("PASS: exact triangle chains, singular limits, and macro identities")


if __name__ == "__main__":
    main()
