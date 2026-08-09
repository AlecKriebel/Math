#!/usr/bin/env python3
"""Exact replay for the singular period-two catalyst obstruction."""

from fractions import Fraction

import sympy as sp


def symbolic_two_cycle() -> None:
    a = sp.symbols("a", positive=True)
    bi = sp.Rational(3, 2) / (a + 2)
    bj = 3 * a / (2 * (2 * a + 1))
    si, sj = bj, bi

    # Temperatures are a and 1/a.  Check both survival systems exactly.
    assert sp.factor(a * bi - 2 * (1 - bi) * bj) == 0
    assert sp.factor(bj / a - 2 * (1 - bj) * bi) == 0
    assert sp.factor(si - 2 * (1 - si) * a * sj) == 0
    assert sp.factor(sj - 2 * (1 - sj) * si / a) == 0
    assert sp.factor((1 - bi) * (1 - bj) - sp.Rational(1, 4)) == 0

    pi = 1 / (1 + a)
    pj = a / (1 + a)
    beta = sp.factor(pi * bi + pj * bj)
    sigma = sp.factor(pi * si + pj * sj)
    gain = sp.factor(beta - sp.Rational(1, 2))
    loss = sp.factor(sp.Rational(1, 2) - sigma)

    assert sp.factor(
        beta - 3 * (a**2 + a + 1) / (2 * (a + 2) * (2 * a + 1))
    ) == 0
    assert sp.factor(sigma - 9 * a / (2 * (a + 2) * (2 * a + 1))) == 0
    assert sp.factor(
        gain - (a - 1) ** 2 / (2 * (a + 2) * (2 * a + 1))
    ) == 0
    assert sp.factor(loss - 2 * gain) == 0


def exact_growing_involution() -> None:
    # One fixed point and four arbitrarily imbalanced two-cycles.  The
    # calculation uses only Fractions, independently of the symbolic path.
    raw = [1, 2, 3, 5, 11, 17, 29, 47, 83]
    total = sum(raw)
    masses = [Fraction(value, total) for value in raw]
    cycles = [(0,), (1, 2), (3, 4), (5, 6), (7, 8)]

    beta = Fraction(0)
    sigma = Fraction(0)
    for orbit in cycles:
        if len(orbit) == 1:
            weight = masses[orbit[0]]
            beta += weight * Fraction(1, 2)
            sigma += weight * Fraction(1, 2)
            continue
        i, j = orbit
        a = masses[j] / masses[i]
        bi = Fraction(3, 2) / (a + 2)
        bj = 3 * a / (2 * (2 * a + 1))
        beta += masses[i] * bi + masses[j] * bj
        sigma += masses[i] * bj + masses[j] * bi

    assert Fraction(1, 2) - sigma == 2 * (beta - Fraction(1, 2))
    assert beta > Fraction(1, 2)
    assert sigma < Fraction(1, 2)


def adjoint_atomic_rates() -> None:
    # For a two-cycle with masses p_i,p_j, P swaps the types.  Construct the
    # p-adjoint directly and check its row sums.
    pi, pj = sp.symbols("p_i p_j", positive=True)
    P = sp.Matrix([[0, 1], [1, 0]])
    Dp = sp.diag(pi, pj)
    adjoint = Dp.inv() * P.T * Dp
    temperature = sp.simplify(adjoint * sp.ones(2, 1))
    assert adjoint == sp.Matrix([[0, pj / pi], [pi / pj, 0]])
    assert temperature == sp.Matrix([pj / pi, pi / pj])


def main() -> None:
    adjoint_atomic_rates()
    symbolic_two_cycle()
    exact_growing_involution()
    print("PASS exact singular period-two catalyst obstruction")


if __name__ == "__main__":
    main()
