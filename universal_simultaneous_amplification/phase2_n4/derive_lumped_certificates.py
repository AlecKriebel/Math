#!/usr/bin/env python3
"""Exact dB derivations for the symmetric 1+3 and 2+2 weighted K4 families.

No project solver is imported here.  The quotient chains are constructed
directly from the death--birth definition and solved over rational-function
fields.  The script then verifies explicit global sign certificates.
"""

from __future__ import annotations

from typing import Sequence, Tuple

import sympy as sp


r = sp.symbols("r", positive=True)
x, y = sp.symbols("x y", positive=True)
g = sp.symbols("g", positive=True)
d, t = sp.symbols("d t", nonnegative=True)


def build_lumped_system(
    p: int,
    q: int,
    alpha: sp.Expr,
    beta: sp.Expr,
    gamma: sp.Expr,
) -> Tuple[sp.Matrix, sp.Matrix, Tuple[Tuple[int, int], ...]]:
    """Build the exact two-class dB state-change equations.

    Class A has size ``p`` and internal edge weight ``alpha``; class B has
    size ``q`` and internal edge weight ``beta``; every cross edge has weight
    ``gamma``.  State ``(i,j)`` records the mutant counts in A and B.
    """

    n = p + q
    states = tuple(
        (i, j)
        for i in range(p + 1)
        for j in range(q + 1)
        if (i, j) not in ((0, 0), (p, q))
    )
    index = {state: location for location, state in enumerate(states)}
    matrix = sp.zeros(len(states), len(states))
    rhs = sp.zeros(len(states), 1)

    for i, j in states:
        moves = []
        if i < p:
            mutant_mass = i * alpha + j * gamma
            resident_mass = (p - i - 1) * alpha + (q - j) * gamma
            if mutant_mass != 0:
                probability = sp.Rational(p - i, n) * (
                    r * mutant_mass / (r * mutant_mass + resident_mass)
                )
                moves.append(((i + 1, j), sp.cancel(probability)))
        if i > 0:
            mutant_mass = (i - 1) * alpha + j * gamma
            resident_mass = (p - i) * alpha + (q - j) * gamma
            if resident_mass != 0:
                probability = sp.Rational(i, n) * (
                    resident_mass / (r * mutant_mass + resident_mass)
                )
                moves.append(((i - 1, j), sp.cancel(probability)))
        if j < q:
            mutant_mass = j * beta + i * gamma
            resident_mass = (q - j - 1) * beta + (p - i) * gamma
            if mutant_mass != 0:
                probability = sp.Rational(q - j, n) * (
                    r * mutant_mass / (r * mutant_mass + resident_mass)
                )
                moves.append(((i, j + 1), sp.cancel(probability)))
        if j > 0:
            mutant_mass = (j - 1) * beta + i * gamma
            resident_mass = (q - j) * beta + (p - i) * gamma
            if resident_mass != 0:
                probability = sp.Rational(j, n) * (
                    resident_mass / (r * mutant_mass + resident_mass)
                )
                moves.append(((i, j - 1), sp.cancel(probability)))

        row = index[(i, j)]
        matrix[row, row] = sum(probability for _, probability in moves)
        for target, probability in moves:
            if target == (p, q):
                rhs[row, 0] += probability
            elif target != (0, 0):
                matrix[row, index[target]] -= probability

    return matrix, rhs, states


def solve_average(
    p: int,
    q: int,
    alpha: sp.Expr,
    beta: sp.Expr,
    gamma: sp.Expr,
):
    matrix, rhs, states = build_lumped_system(p, q, alpha, beta, gamma)
    index = {state: location for location, state in enumerate(states)}
    solution = tuple(next(iter(sp.linsolve((matrix, rhs)))))
    average = sp.cancel(
        (p * solution[index[(1, 0)]] + q * solution[index[(0, 1)]]) / (p + q)
    )
    return average, matrix, states


def baseline_k4() -> sp.Expr:
    return sp.cancel(3 * r**2 / (4 * (r**2 + r + 1)))


def positive_integer_coefficients(expression: sp.Expr, *variables: sp.Symbol) -> bool:
    polynomial = sp.Poly(sp.expand(expression), *variables)
    return all(coefficient.is_positive is True for _, coefficient in polynomial.terms())


def certificate_13():
    F = sp.expand(
        2 * r**4 * x**2
        + 2 * r**4 * x
        + 11 * r**3 * x**2
        + 14 * r**3 * x
        + 3 * r**3
        + 21 * r**2 * x**2
        + 29 * r**2 * x
        + 12 * r**2
        + 16 * r * x**2
        + 22 * r * x
        + 8 * r
        + 4 * x**2
        + 5 * x
        + 1
    )
    P = sp.expand(
        8 * x**2 * (x + 1) * (r**6 + 1)
        + (6 * x**4 + 36 * x**3 + 46 * x**2 + 16 * x) * (r**5 + r)
        + (27 * x**4 + 73 * x**3 + 85 * x**2 + 59 * x + 12)
        * (r**4 + r**2)
        + (42 * x**4 + 90 * x**3 + 106 * x**2 + 66 * x + 24) * r**3
    )
    difference = sp.cancel(
        -3 * r**2 * (r - 1) * (x - 1) ** 2 * F
        / (4 * (r**2 + r + 1) * P)
    )
    return F, P, difference


def certificate_22_coefficients():
    R0 = sp.expand(
        (2 * g**2 + 2 * g) * t**4
        + (g**3 + 10 * g**2 + 21 * g + 6) * t**3
        + (3 * g**3 + 26 * g**2 + 61 * g + 38) * t**2
        + (4 * g**3 + 32 * g**2 + 80 * g + 64) * t
        + 2 * g**3
        + 16 * g**2
        + 40 * g
        + 32
    )
    C0 = sp.expand(2 * t * (g - 1) ** 2 * (g + 1) * (t + 1) * R0)
    C1 = sp.expand(
        2 * (g**4 + 4 * g**3 - 2 * g**2 + 4 * g + 1) * t**6
        + (11 * g**4 + 108 * g**3 + 76 * g**2 + 60 * g + 17) * t**5
        + 2 * (40 * g**4 + 288 * g**3 + 393 * g**2 + 176 * g + 19) * t**4
        + (16 * g**5 + 331 * g**4 + 1704 * g**3 + 2766 * g**2 + 1360 * g + 39)
        * t**3
        + 2 * (28 * g**5 + 337 * g**4 + 1426 * g**3 + 2399 * g**2 + 1378 * g + 12)
        * t**2
        + 2 * (g + 2) * (32 * g**4 + 263 * g**3 + 722 * g**2 + 661 * g + 2)
        * t
        + 24 * g * (g + 2) * (g + 4) * (g**2 + 4 * g + 5)
    )
    C2 = sp.expand(
        2 * (g**2 + 1) * t**6
        + 3 * (9 * g**2 + 26 * g + 5) * t**5
        + 2 * (18 * g**3 + 120 * g**2 + 321 * g + 44) * t**4
        + 2 * (2 * g**4 + 105 * g**3 + 525 * g**2 + 1071 * g + 170) * t**3
        + (14 * g**4 + 474 * g**3 + 2201 * g**2 + 3648 * g + 689) * t**2
        + 2 * (8 * g**4 + 240 * g**3 + 1080 * g**2 + 1587 * g + 331) * t
        + 6 * (g**4 + 30 * g**3 + 133 * g**2 + 186 * g + 40)
    )
    C3 = sp.expand(
        13 * t**5
        + (6 * g**2 + 48 * g + 107) * t**4
        + (35 * g**2 + 312 * g + 357) * t**3
        + (79 * g**2 + 744 * g + 608) * t**2
        + (80 * g**2 + 768 * g + 529) * t
        + 6 * (5 * g**2 + 48 * g + 31)
    )
    C4 = sp.expand(6 * t**4 + 39 * t**3 + 93 * t**2 + 96 * t + 36)
    return R0, (C0, C1, C2, C3, C4)


def main() -> None:
    # 1+3: the singleton class has no internal edge; beta=x, cross weight=1.
    rho13, _, _ = solve_average(1, 3, 0, x, 1)
    difference13 = sp.cancel(rho13 - baseline_k4())
    F13, P13, claimed13 = certificate_13()
    assert sp.cancel(difference13 - claimed13) == 0
    assert positive_integer_coefficients(F13, r, x)
    assert positive_integer_coefficients(P13, r, x)

    # 2+2: internal weights x,y and cross weight 1.
    rho22, matrix22, _ = solve_average(2, 2, x, y, 1)
    difference22 = sp.cancel(rho22 - baseline_k4())
    numerator22, denominator22 = sp.fraction(difference22)
    H22 = sp.cancel(-numerator22 / (r**2 * (r - 1)))
    assert sp.denom(H22) == 1

    # Symmetrize in x,y, then use xy=g^2 and x+y=2g+d.
    symmetric, remainder, mapping = sp.symmetrize(sp.expand(H22), [x, y], formal=True)
    assert remainder == 0
    s1_symbol, s2_symbol = mapping[0][0], mapping[1][0]
    transformed = sp.expand(
        symmetric.subs({s1_symbol: 2 * g + d, s2_symbol: g**2, r: 1 + t})
    )
    R0, coefficients = certificate_22_coefficients()
    claimed_transformed = sp.expand(sum(coefficients[k] * d**k for k in range(5)))
    assert sp.expand(transformed - claimed_transformed) == 0

    # Machine-check every elementary coefficient-positivity assertion.
    assert positive_integer_coefficients(R0, g, t)
    C0, C1, C2, C3, C4 = coefficients
    leading_C1 = sp.Poly(C1, t).nth(6)
    assert sp.expand(
        leading_C1 - 2 * ((g**2 - 1) ** 2 + 4 * g * (g**2 + 1))
    ) == 0
    for power in range(6):
        assert positive_integer_coefficients(sp.Poly(C1, t).nth(power), g)
    for coefficient in (C2, C3, C4):
        assert positive_integer_coefficients(coefficient, g, t)

    # The reduced denominator is manifestly positive as a polynomial.
    P22 = sp.cancel(denominator22 / (4 * (r**2 + r + 1)))
    assert sp.denom(P22) == 1
    assert positive_integer_coefficients(P22, r, x, y)

    # Independent denominator identity: P22 is the numerator of det(M22).
    determinant = sp.cancel(matrix22.det(method="domain-ge"))
    det_numerator, det_denominator = sp.fraction(determinant)
    local_product = (
        (2 * r + x)
        * (2 * r + y)
        * (r * x + 2)
        * (r * y + 2)
        * (r + x + 1)
        * (r + y + 1)
        * (r * x + r + 1)
        * (r * y + r + 1)
    )
    assert sp.expand(det_numerator - P22) == 0
    assert sp.expand(det_denominator - 128 * local_product) == 0

    print("[EXACTLY DERIVED] 1+3 and 2+2 orbit chains solved over rational functions")
    print("[PROVED] 1+3 is strictly dB-suppressing for x!=1 and every r>1")
    print("[CERTIFIED IDENTITY] H22(g,d,t)=sum_{k=0}^4 C_k(g,t)d^k")
    print("[CERTIFIED POSITIVITY] C0>=0, C1..C4>0 for g>0,t>0")
    print("[PROVED] 2+2 is strictly dB-suppressing off x=y=1 for every r>1")
    print("[CERTIFIED POSITIVITY] both reduced denominators are positive")


if __name__ == "__main__":
    main()
