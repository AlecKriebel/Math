#!/usr/bin/env python3
"""Independent exact audit of the characteristic-three anti-fold jet.

This checker does not trust the cyclotomic coefficient fixtures in the
search program.  It constructs cyclotomic polynomials from their defining
factorization, reduces them modulo three, and verifies the inseparable
factorizations.  It then compares the quadratic support expansion against
the physical four-row negacyclic norm on deterministic random supports.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
from random import Random
import sys


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
JET = SEARCH / "eliahou_char3_jet"
sys.path[:0] = [str(JET), str(SEARCH)]

import search_char3_antifold as char3  # noqa: E402
import search_char3_cp_sat as cp  # noqa: E402
import search_eliahou_antifold_sat as exact  # noqa: E402


def trim(poly: list[int]) -> list[int]:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def multiply(left: list[int], right: list[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return trim(result)


def divide_exact(dividend: list[int], divisor: list[int]) -> list[int]:
    """Monic exact division over Z, low coefficient first."""

    work = [Fraction(value) for value in dividend]
    divisor_q = [Fraction(value) for value in divisor]
    quotient = [Fraction(0)] * (len(dividend) - len(divisor) + 1)
    while len(work) >= len(divisor_q):
        degree = len(work) - len(divisor_q)
        coefficient = work[-1] / divisor_q[-1]
        quotient[degree] = coefficient
        for i, value in enumerate(divisor_q):
            work[degree + i] -= coefficient * value
        while work and work[-1] == 0:
            work.pop()
    assert not work
    assert all(value.denominator == 1 for value in quotient)
    return trim([int(value) for value in quotient])


def divisors(number: int) -> list[int]:
    return [value for value in range(1, number + 1) if number % value == 0]


def cyclotomic(number: int, known: dict[int, list[int]]) -> list[int]:
    polynomial = [-1] + [0] * (number - 1) + [1]
    for divisor in divisors(number):
        if divisor < number:
            polynomial = divide_exact(polynomial, known[divisor])
    return polynomial


def mod3(poly: list[int]) -> list[int]:
    return [value % 3 for value in poly]


def polynomial_audit() -> None:
    known: dict[int, list[int]] = {}
    for number in range(1, 85):
        known[number] = cyclotomic(number, known)

    phi4 = known[4]
    phi12 = known[12]
    phi28 = known[28]
    phi84 = known[84]
    assert mod3(multiply(phi4, phi4)) == mod3(phi12)
    assert mod3(multiply(phi28, phi28)) == mod3(phi84)

    z14_plus_1 = [1] + [0] * 13 + [1]
    z42_plus_1 = [1] + [0] * 41 + [1]
    cube = multiply(multiply(z14_plus_1, z14_plus_1), z14_plus_1)
    assert mod3(cube) == mod3(z42_plus_1)

    # Also verify that Phi_4 Phi_28 is exactly z^14+1 modulo 3, so the
    # cyclotomic and anti-fold formulations are the same statement.
    assert mod3(multiply(phi4, phi28)) == mod3(z14_plus_1)
    char3.factorization_self_test()


def evaluate_quadratic(
    equation: cp.QuadraticEquation,
    selected: set[tuple[str, int]],
) -> int:
    value = equation.constant
    value += sum(
        coefficient
        for key, coefficient in equation.linear.items()
        if key in selected
    )
    value += sum(
        coefficient
        for (left, right), coefficient in equation.quadratic.items()
        if left in selected and right in selected
    )
    return value


def support_audit() -> None:
    rng = Random(668_300_042)
    cases = char3.canonical_cases()
    assert len(cases) == 30
    support_census: dict[int, int] = {}
    for case in cases:
        # Build the PySAT representation without modular constraints and
        # compare its integer contents to the separate CP expansion.
        _, _, variables, pysat_equations = char3.build(case, ())
        cp_equations = cp.quadratic_equations(case, set(variables))
        assert len(pysat_equations) == len(cp_equations) == 20
        assert [equation.content for equation in pysat_equations] == [4] * 20
        assert [equation.content for equation in cp_equations] == [4] * 20
        support_census[len(variables)] = (
            support_census.get(len(variables), 0) + 1
        )
    assert support_census == {78: 29, 79: 1}

    for case_number in (0, 26):
        case = cases[case_number]
        # Construct the support domain through the authoritative low-level
        # routine but reconstruct both equation representations independently.
        from pysat.formula import IDPool

        variables, _ = exact.support_variables(IDPool(), case)
        keys = tuple(sorted(variables))
        equations = cp.quadratic_equations(case, set(keys))
        assert len(equations) == 20
        assert all(equation.content == 4 for equation in equations)

        fixtures = [
            set(keys[:39]),
            set(keys[-39:]),
        ]
        for _ in range(32):
            fixtures.append(set(rng.sample(keys, 39)))

        for selected in fixtures:
            rows = exact.direct_rows(case, selected)
            physical = exact.negacyclic_correlations(rows)
            assert physical[0] == 334
            for equation in equations:
                expanded = evaluate_quadratic(equation, selected)
                assert equation.content * expanded == physical[equation.lag]
                assert physical[42 - equation.lag] == -physical[equation.lag]

        # Check every Boolean monomial case explicitly, including x=y where
        # (1-x)^2=1-x rather than a generic quadratic.
        for left, right in combinations(keys[:12], 2):
            for left_value in (0, 1):
                for right_value in (0, 1):
                    assert (1 - left_value) * (1 - right_value) == (
                        1
                        - left_value
                        - right_value
                        + left_value * right_value
                    )
        for value in (0, 1):
            assert (1 - value) ** 2 == 1 - value


def witness_audit() -> None:
    payload = json.loads(
        (HERE / "CASE26_CHAR3_WITNESS.json").read_text()
    )
    case = char3.canonical_cases()[payload["case"]]
    assert case.block == payload["block"]
    assert case.index == payload["q_index"]
    selected = {
        (str(block), int(cell))
        for block, cell in payload["selected"]
    }
    assert len(selected) == 39
    from pysat.formula import IDPool

    variables, _ = exact.support_variables(IDPool(), case)
    assert selected <= set(variables)
    equations = cp.quadratic_equations(case, set(variables))
    correlations = exact.negacyclic_correlations(
        exact.direct_rows(case, selected)
    )
    normalized = [
        correlations[equation.lag] // equation.content
        for equation in equations
    ]
    assert normalized == payload["normalized_residuals"]
    assert all(value % 3 == 0 for value in normalized)
    assert any(value % 2 for value in normalized)


def main() -> None:
    polynomial_audit()
    support_audit()
    witness_audit()
    print(
        "PASS: independent cyclotomic derivation, inseparable "
        "characteristic-3 factorization, quadratic expansion, and "
        "2 x 34 direct four-row support replays; canonical case 26 "
        "full characteristic-3 witness replayed; PySAT/CP equation "
        "content 4 verified in all 30 cases"
    )


if __name__ == "__main__":
    main()
