#!/usr/bin/env python3
"""Prove every weighted triangle is a dB suppressor for every `r>1`.

This is a symbolic derivation from the two six-state absorbing chains.  It
does not assume a fixation formula for the graph under test.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import permutations

import sympy as sp


r, a, b, c = sp.symbols("r a b c", positive=True)
WEIGHTS = ((0, a, b), (a, 0, c), (b, c, 0))
VARIABLES = (a, b, c)


def fixation(rule: str) -> sp.Expr:
    degree = [sum(row) for row in WEIGHTS]
    states = list(range(1, 7))
    index = {state: row for row, state in enumerate(states)}
    matrix = sp.eye(6)
    rhs = sp.zeros(6, 1)

    for state in states:
        mutant = [(state >> vertex) & 1 for vertex in range(3)]
        transition = defaultdict(lambda: sp.Integer(0))
        if rule == "Bd":
            total_fitness = 3 + (r - 1) * sum(mutant)
            for parent in range(3):
                for target in range(3):
                    if parent == target:
                        continue
                    probability = (
                        (r if mutant[parent] else 1)
                        * WEIGHTS[parent][target]
                        / (total_fitness * degree[parent])
                    )
                    new_state = (
                        state | (1 << target)
                        if mutant[parent]
                        else state & ~(1 << target)
                    )
                    transition[new_state] += probability
        elif rule == "dB":
            for target in range(3):
                denominator = sum(
                    WEIGHTS[parent][target] * (r if mutant[parent] else 1)
                    for parent in range(3)
                )
                for parent in range(3):
                    if parent == target:
                        continue
                    probability = (
                        WEIGHTS[parent][target]
                        * (r if mutant[parent] else 1)
                        / (3 * denominator)
                    )
                    new_state = (
                        state | (1 << target)
                        if mutant[parent]
                        else state & ~(1 << target)
                    )
                    transition[new_state] += probability
        else:
            raise ValueError(rule)

        row = index[state]
        for target, probability in transition.items():
            if target == 7:
                rhs[row] += probability
            elif target:
                matrix[row, index[target]] -= probability

    solution = next(iter(sp.linsolve((matrix, rhs))))
    return sp.factor(
        sp.cancel(sum(solution[index[1 << vertex]] for vertex in range(3)) / 3)
    )


def exchange_atom(exponents: tuple[int, int, int]) -> sp.Expr:
    i, j, k = exponents
    return sp.expand(
        sum(
            x**i * y**j * z**k * (x - y) ** 2
            for x, y, z in permutations(VARIABLES)
        )
    )


def main() -> None:
    rho_bd = fixation("Bd")
    rho_db = fixation("dB")
    complete_bd = (1 - 1 / r) / (1 - r ** -3)
    complete_db = sp.Rational(2, 3) * (1 - 1 / r) / (1 - r ** -2)

    db_gap = sp.factor(sp.cancel(rho_db - complete_db))
    numerator, denominator = sp.fraction(db_gap)
    factor_data = sp.factor_list(numerator)
    assert factor_data[0] == -1
    scalar_factors = [
        (factor, multiplicity)
        for factor, multiplicity in factor_data[1]
        if sp.Poly(factor, *VARIABLES).total_degree() == 0
    ]
    assert scalar_factors == [(r - 1, 1), (r, 1)]
    weight_factors = [
        factor
        for factor, multiplicity in factor_data[1]
        if sp.Poly(factor, *VARIABLES).total_degree() > 0
        for _ in range(multiplicity)
    ]
    assert len(weight_factors) == 1
    weight_factor = sp.expand(weight_factors[0])
    assert sp.Poly(weight_factor, *VARIABLES).total_degree() == 6
    assert all(
        coefficient > 0
        for _, coefficient in sp.Poly(sp.expand(denominator), *VARIABLES).terms()
    )

    polynomial_r = sp.Poly(weight_factor, r)
    coefficient_a = polynomial_r.coeff_monomial(r**4)
    coefficient_b = polynomial_r.coeff_monomial(r**3)
    coefficient_c = polynomial_r.coeff_monomial(r**2)
    assert polynomial_r.coeff_monomial(r) == coefficient_b
    assert polynomial_r.coeff_monomial(1) == coefficient_a

    atom_112 = exchange_atom((1, 1, 2))
    atom_121 = exchange_atom((1, 2, 1))
    atom_013 = exchange_atom((0, 1, 3))
    atom_220 = exchange_atom((2, 2, 0))
    atom_004 = exchange_atom((0, 0, 4))
    certificate_a = sp.Rational(3, 2) * atom_112
    certificate_m = (
        6 * atom_121 + sp.Rational(11, 2) * atom_112 + 2 * atom_013
    )
    certificate_h = (
        2 * atom_220 + 20 * atom_121 + 4 * atom_112 + 4 * atom_004
    )
    assert sp.expand(coefficient_a - certificate_a) == 0
    assert sp.expand(4 * coefficient_a + coefficient_b - certificate_m) == 0
    assert sp.expand(
        2 * coefficient_a + 2 * coefficient_b + coefficient_c - certificate_h
    ) == 0

    tau = r + 1 / r
    reconstructed = sp.cancel(
        r**2
        * (
            (tau - 2) ** 2 * certificate_a
            + (tau - 2) * certificate_m
            + certificate_h
        )
    )
    assert sp.expand(weight_factor - reconstructed) == 0
    assert sp.expand(weight_factor.subs({a: 1, b: 1, c: 1})) == 0

    print("PASS exact symbolic Bd and dB weighted-triangle chains")
    print("PASS dB gap denominator has strictly positive coefficients")
    print("PASS all-r dB numerator has a positive exchange-square certificate")
    print("PROVED every unequal positive weighted triangle is a strict dB suppressor")


if __name__ == "__main__":
    main()
