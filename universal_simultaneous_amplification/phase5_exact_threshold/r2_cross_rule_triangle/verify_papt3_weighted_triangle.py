#!/usr/bin/env python3
"""Exact symbolic replay of PAPT_3 for every weighted triangle."""

from __future__ import annotations

from collections import defaultdict
from itertools import permutations

import sympy as sp


R = sp.Integer(2)
a, b, c = sp.symbols("a b c", nonnegative=True)
VARIABLES = (a, b, c)


BD_TABLE = (
    ((8, 4, 0), 20, 80),
    ((8, 3, 1), 121, 484),
    ((8, 2, 2), 222, 888),
    ((7, 5, 0), 310, 700),
    ((7, 4, 1), 2123, 5067),
    ((7, 3, 2), 5097, 12593),
    ((6, 6, 0), 600, 1320),
    ((6, 5, 1), 6042, 13673),
    ((6, 4, 2), 20467, 47528),
    ((6, 3, 3), 30130, 70670),
    ((5, 5, 2), 31264, 71966),
    ((5, 4, 3), 66586, 155109),
    ((4, 4, 4), 96564, 225616),
)


DB_TABLE = (
    ((4, 2, 0), 16, 32),
    ((4, 1, 1), 40, 80),
    ((3, 3, 0), 56, 80),
    ((3, 2, 1), 223, 328),
    ((2, 2, 2), 456, 627),
)


CERTIFICATE = (
    ((0, 4, 12), 2880),
    ((0, 5, 11), 15040),
    ((0, 8, 8), 8720),
    ((1, 3, 12), 30384),
    ((1, 4, 11), 193060),
    ((1, 7, 8), 58546),
    ((1, 8, 7), 234046),
    ((2, 4, 10), 1235746),
    ((2, 5, 9), 41924),
    ((2, 7, 7), 1462847),
    ((2, 9, 5), 1310059),
    ((3, 4, 9), 2217205),
    ((3, 6, 7), 2475646),
    ((3, 7, 6), 686879),
    ((3, 8, 5), 11441942),
    ((3, 10, 3), 27000),
    ((4, 7, 5), 34933576),
    ((4, 8, 4), 1566204),
    ((4, 9, 3), 1169837),
    ((4, 10, 2), 136296),
    ((5, 5, 6), 2264809),
    ((5, 6, 5), 58710886),
    ((6, 8, 2), 89812),
    ((8, 8, 0), 960),
)


def monomial_symmetric(partition):
    answer = 0
    for exponent in set(permutations(partition)):
        answer += sp.prod(variable**power for variable, power in zip(VARIABLES, exponent))
    return answer


def table_polynomials(table):
    numerator = sum(
        numerator_coefficient * monomial_symmetric(partition)
        for partition, numerator_coefficient, _ in table
    )
    denominator = sum(
        denominator_coefficient * monomial_symmetric(partition)
        for partition, _, denominator_coefficient in table
    )
    return sp.expand(numerator), sp.expand(denominator)


def triangle_fixation(rule):
    weights = ((0, a, b), (a, 0, c), (b, c, 0))
    degrees = [sum(row) for row in weights]
    states = list(range(1, 7))
    index = {state: row for row, state in enumerate(states)}
    matrix = sp.eye(6)
    rhs = sp.zeros(6, 1)

    for state in states:
        mutant = [(state >> vertex) & 1 for vertex in range(3)]
        transitions = defaultdict(lambda: sp.Integer(0))
        if rule == "Bd":
            total_fitness = 3 + (R - 1) * sum(mutant)
            for parent in range(3):
                for target in range(3):
                    if parent == target:
                        continue
                    probability = (
                        (R if mutant[parent] else 1)
                        * weights[parent][target]
                        / (total_fitness * degrees[parent])
                    )
                    new_state = (
                        state | (1 << target)
                        if mutant[parent]
                        else state & ~(1 << target)
                    )
                    transitions[new_state] += probability
        elif rule == "dB":
            for target in range(3):
                denominator = sum(
                    weights[parent][target] * (R if mutant[parent] else 1)
                    for parent in range(3)
                )
                for parent in range(3):
                    if parent == target:
                        continue
                    probability = (
                        weights[parent][target]
                        * (R if mutant[parent] else 1)
                        / (3 * denominator)
                    )
                    new_state = (
                        state | (1 << target)
                        if mutant[parent]
                        else state & ~(1 << target)
                    )
                    transitions[new_state] += probability
        else:
            raise ValueError(rule)

        row = index[state]
        for target, probability in transitions.items():
            if target == 7:
                rhs[row] += probability
            elif target:
                matrix[row, index[target]] -= probability

    solution = next(iter(sp.linsolve((matrix, rhs))))
    return sp.cancel(sum(solution[index[1 << vertex]] for vertex in range(3)) / 3)


def exchange_atom(exponents):
    i, j, k = exponents
    return sp.expand(
        sum(
            x**i * y**j * z**k * (x - y) ** 2
            for x, y, z in permutations(VARIABLES)
        )
    )


def main():
    n_b, q_b = table_polynomials(BD_TABLE)
    n_d, q_d = table_polynomials(DB_TABLE)
    assert all(value > 0 for _, x, y in BD_TABLE for value in (x, y))
    assert all(value > 0 for _, x, y in DB_TABLE for value in (x, y))

    rho_bd = triangle_fixation("Bd")
    rho_db = triangle_fixation("dB")
    assert sp.cancel(rho_bd - 4 * n_b / (3 * q_b)) == 0
    assert sp.cancel(rho_db - 2 * n_d / (3 * q_d)) == 0
    complete = {a: 1, b: 1, c: 1}
    assert rho_bd.subs(complete) == sp.Rational(4, 7)
    assert rho_db.subs(complete) == sp.Rational(4, 9)

    primitive = sp.expand(2 * q_b * q_d - 7 * n_b * n_d)
    certificate = sp.expand(
        sum(coefficient * exchange_atom(exponents) for exponents, coefficient in CERTIFICATE)
    )
    assert all(coefficient > 0 for _, coefficient in CERTIFICATE)
    assert sp.Poly(primitive - certificate, *VARIABLES).is_zero

    gap = sp.cancel(sp.Rational(16, 63) - rho_bd * rho_db)
    assert sp.cancel(gap - 8 * primitive / (63 * q_b * q_d)) == 0

    rigidity_atom = exchange_atom((0, 8, 8))
    expected_rigidity = (
        c**8 * (a**8 + b**8) * (a - b) ** 2
        + b**8 * (a**8 + c**8) * (a - c) ** 2
        + a**8 * (b**8 + c**8) * (b - c) ** 2
    )
    assert sp.expand(rigidity_atom - expected_rigidity) == 0

    # Connected path boundary: c=0 and a,b>0.  The numerator is strict.
    path_numerator = sp.factor(primitive.subs(c, 0))
    assert path_numerator == 80 * a**6 * b**6 * (
        36 * a**6
        + 188 * a**5 * b
        + 133 * a**4 * b**2
        - 48 * a**3 * b**3
        + 133 * a**2 * b**4
        + 188 * a * b**5
        + 36 * b**6
    )
    # The only negative term is dominated by the two 133-terms by AM-GM.
    assert 2 * 133 > 48

    print("PASS: exact symbolic Bd and dB triangle fixation formulas")
    print("PASS: degree-18 PAPT numerator equals 24 positive exchange circuits")
    print("PASS: equality only at the equal positive triangle")
    print("PROVED: PAPT_3 for every connected weighted three-vertex graph")


if __name__ == "__main__":
    main()
