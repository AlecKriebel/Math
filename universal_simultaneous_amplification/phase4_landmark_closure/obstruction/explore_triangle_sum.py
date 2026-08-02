#!/usr/bin/env python3
"""Symbolic discovery calculation for the finite-sum conjecture on n=3."""

from __future__ import annotations

from collections import defaultdict

import sympy as sp


r = sp.symbols("r", positive=True)
a, b, c = sp.symbols("a b c", positive=True)


def singleton_fixation(rule: str) -> list[sp.Expr]:
    weights = ((0, a, b), (a, 0, c), (b, c, 0))
    degree = [sum(row) for row in weights]
    states = list(range(1, 7))
    index = {state: position for position, state in enumerate(states)}
    matrix = sp.eye(6)
    rhs = sp.zeros(6, 1)
    for state in states:
        mutant = [(state >> i) & 1 for i in range(3)]
        transitions: dict[int, sp.Expr] = defaultdict(lambda: sp.Integer(0))
        if rule == "Bd":
            total = 3 + (r - 1) * sum(mutant)
            for parent in range(3):
                for target in range(3):
                    if weights[parent][target] == 0:
                        continue
                    probability = (
                        (r if mutant[parent] else 1)
                        / total
                        * weights[parent][target]
                        / degree[parent]
                    )
                    new = (
                        state | (1 << target)
                        if mutant[parent]
                        else state & ~(1 << target)
                    )
                    transitions[new] += probability
        else:
            for target in range(3):
                denominator = sum(
                    weights[parent][target] * (r if mutant[parent] else 1)
                    for parent in range(3)
                )
                for parent in range(3):
                    if weights[parent][target] == 0:
                        continue
                    probability = (
                        sp.Rational(1, 3)
                        * weights[parent][target]
                        * (r if mutant[parent] else 1)
                        / denominator
                    )
                    new = (
                        state | (1 << target)
                        if mutant[parent]
                        else state & ~(1 << target)
                    )
                    transitions[new] += probability
        row = index[state]
        for new, probability in transitions.items():
            if new == 7:
                rhs[row] += probability
            elif new:
                matrix[row, index[new]] -= probability
    solution = list(next(iter(sp.linsolve((matrix, rhs)))))
    return [sp.factor(solution[index[1 << i]]) for i in range(3)]


def main() -> None:
    bd = sp.factor(sum(singleton_fixation("Bd")) / 3)
    db = sp.factor(sum(singleton_fixation("dB")) / 3)
    complete_bd = (1 - 1 / r) / (1 - r ** -3)
    complete_db = sp.Rational(2, 3) * (1 - 1 / r) / (1 - r ** -2)
    gap = sp.factor(complete_bd + complete_db - bd - db)
    print("gap factor:", gap)
    numerator, denominator = sp.together(gap).as_numer_denom()
    print("numerator factor:", sp.factor(numerator))
    print("denominator factor:", sp.factor(denominator))


if __name__ == "__main__":
    main()
