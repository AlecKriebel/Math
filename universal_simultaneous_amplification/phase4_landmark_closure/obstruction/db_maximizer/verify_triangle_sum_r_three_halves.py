#!/usr/bin/env python3
"""Exact certificate for the Bd+dB sum on weighted triangles at r=3/2.

The program derives both fixation probabilities from the six transient
subset equations.  It then verifies a 24-term manifestly nonnegative
decomposition of the comparison numerator.  No declared fixation formula is
used for the graph under test.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import permutations

import sympy as sp


a, b, c = sp.symbols("a b c", nonnegative=True)
r = sp.Rational(3, 2)
variables = (a, b, c)


def fixation(rule: str) -> sp.Expr:
    weights = ((0, a, b), (a, 0, c), (b, c, 0))
    degrees = [sum(row) for row in weights]
    states = list(range(1, 7))
    index = {state: k for k, state in enumerate(states)}
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
                        * weights[parent][target]
                        / (total_fitness * degrees[parent])
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
                    weights[parent][target] * (r if mutant[parent] else 1)
                    for parent in range(3)
                )
                for parent in range(3):
                    if parent == target:
                        continue
                    probability = (
                        weights[parent][target]
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
        for new_state, probability in transition.items():
            if new_state == 7:
                rhs[row] += probability
            elif new_state:
                matrix[row, index[new_state]] -= probability

    solution = next(iter(sp.linsolve((matrix, rhs))))
    return sp.cancel(sum(solution[index[1 << vertex]] for vertex in range(3)) / 3)


# Each entry ((i,j,k), q) denotes
#
#   q * sum_{(x,y,z) in all six permutations of (a,b,c)}
#           x^i y^j z^k (x-y)^2.
#
# Every summand is nonnegative on the nonnegative orthant.
CERTIFICATE = (
    ((0, 8, 8), sp.Integer(67481600)),
    ((1, 3, 12), sp.Integer(140184000)),
    ((1, 5, 10), sp.Integer(520628044)),
    ((1, 8, 7), sp.Integer(174382692)),
    ((1, 9, 6), sp.Integer(611973264)),
    ((2, 4, 10), sp.Integer(9665987445)),
    ((2, 9, 5), sp.Integer(2376788555)),
    ((3, 6, 7), sp.Rational(35868109001, 2)),
    ((3, 7, 6), sp.Rational(67239003671, 2)),
    ((3, 10, 3), sp.Integer(167660064)),
    ((4, 6, 6), sp.Integer(114665750791)),
    ((4, 9, 3), sp.Integer(5432809764)),
    ((4, 10, 2), sp.Integer(709840800)),
    ((5, 5, 6), sp.Integer(64309259153)),
    ((5, 6, 5), sp.Integer(1066977984)),
    ((5, 7, 4), sp.Integer(23886041285)),
    ((5, 8, 3), sp.Integer(48104061036)),
    ((5, 9, 2), sp.Integer(1624816945)),
    ((6, 7, 3), sp.Rational(137709611177, 2)),
    ((6, 10, 0), sp.Integer(17127936)),
    ((7, 7, 2), sp.Rational(762688155, 2)),
    ((7, 8, 1), sp.Integer(5282864)),
    ((7, 9, 0), sp.Integer(86009472)),
    ((8, 8, 0), sp.Integer(53569504)),
)


def certificate_polynomial() -> sp.Expr:
    answer = 0
    for (i, j, k), coefficient in CERTIFICATE:
        assert coefficient > 0
        atom = sum(
            x**i * y**j * z**k * (x - y) ** 2
            for x, y, z in permutations(variables)
        )
        answer += coefficient * atom
    return sp.expand(answer)


def main() -> None:
    rho_bd = fixation("Bd")
    rho_db = fixation("dB")
    complete_bd = (1 - 1 / r) / (1 - r ** -3)
    complete_db = sp.Rational(2, 3) * (1 - 1 / r) / (1 - r ** -2)
    gap = sp.cancel(complete_bd + complete_db - rho_bd - rho_db)
    numerator, denominator = map(sp.expand, sp.fraction(gap))

    denominator_poly = sp.Poly(denominator, *variables)
    assert denominator_poly.total_degree() == 18
    assert len(denominator_poly.terms()) == 127
    assert all(coefficient > 0 for _, coefficient in denominator_poly.terms())

    numerator_poly = sp.Poly(numerator, *variables)
    assert numerator_poly.total_degree() == 18
    assert len(numerator_poly.terms()) == 127
    certificate = certificate_polynomial()
    assert sp.Poly(numerator - 2 * certificate, *variables).is_zero

    # The first atom alone is strictly positive when a,b,c>0 are not all
    # equal: it is abc-positive times a sum of squared pair differences.
    first_atom = sum(
        x**0 * y**8 * z**8 * (x - y) ** 2
        for x, y, z in permutations(variables)
    )
    expected_first = (
        c**8 * (a**8 + b**8) * (a - b) ** 2
        + b**8 * (a**8 + c**8) * (a - c) ** 2
        + a**8 * (b**8 + c**8) * (b - c) ** 2
    )
    assert sp.expand(first_atom - expected_first) == 0

    # An exact counterexample to transposition-averaging monotonicity.  The
    # path (a,b,c)=(5,0,1), averaged with its copy under 0<->1, becomes the
    # triangle (5,1/2,1/2).
    total = sp.cancel(rho_bd + rho_db)
    path_total = sp.cancel(total.subs({a: 5, b: 0, c: 1}))
    averaged_total = sp.cancel(
        total.subs({a: 5, b: sp.Rational(1, 2), c: sp.Rational(1, 2)})
    )
    assert path_total == sp.Rational(5864, 7371)
    assert averaged_total == sp.Rational(106603567, 135117445)
    assert path_total - averaged_total == sp.Rational(
        6553805123, 995950687095
    )

    print("PASS: exact six-state Bd and dB chains constructed")
    print("PASS: comparison denominator has 127 strictly positive coefficients")
    print("PASS: numerator equals twice the 24-atom nonnegative certificate")
    print("PASS: equality for positive weights occurs only at a=b=c")
    print("PASS: exact path example refutes transposition-averaging monotonicity")


if __name__ == "__main__":
    main()
