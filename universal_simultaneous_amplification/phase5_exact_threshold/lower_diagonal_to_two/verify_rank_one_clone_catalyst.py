#!/usr/bin/env python3
"""Exact verifier for the diffuse rank-one clone catalyst obstruction."""

from __future__ import annotations

import sympy as sp


def main() -> None:
    # Atomic finite-clone rate limits for two symbolic types and general r.
    m = sp.symbols("m", positive=True, integer=True)
    r = sp.symbols("r", positive=True)
    p1, p2, a1, a2 = sp.symbols("p1 p2 a1 a2", positive=True)
    abar = p1 * a1 + p2 * a2

    # A type-1 Bd parent targets type 2; its incoming resident temperature is
    # summed over every possible parent, with its own vertex omitted.
    target_12 = (m * p2 * a2) / (m * abar - a1)
    assert sp.limit(target_12, m, sp.oo) == p2 * a2 / abar
    temperature_1 = a1 * (
        m * p1 / (m * abar - a1)
        + m * p2 / (m * abar - a2)
        - 1 / (m * abar - a1)
    )
    temperature_limit = sp.factor(sp.limit(temperature_1, m, sp.oo))
    assert temperature_limit == a1 * (p1 + p2) / abar
    assert sp.factor(temperature_limit.subs(p2, 1 - p1) - a1 / abar.subs(p2, 1 - p1)) == 0

    # A single type-1 dB mutant creates type-2 children.  The mutant fitness
    # correction is retained in the exact finite denominator.
    db_birth_12 = m * p2 * r * a1 / (m * abar - a2 + (r - 1) * a1)
    assert sp.factor(
        sp.limit(db_birth_12, m, sp.oo) - r * p2 * a1 / abar
    ) == 0

    # General-r scalar equations.  On any probability space, the Bd
    # self-consistency residual forces beta=(r-1)/r exactly.
    x, M, S = sp.symbols("x M S", positive=True)
    b = r * M / (x + r * M)
    s = r * x * S / (1 + r * x * S)
    bd_integrand = r * x / (x + r * M)
    assert sp.factor(1 - b - bd_integrand / r) == 0

    # At the complete-graph dB candidate S=(r-1)/r, the integrand is the
    # strictly concave function r*x/(1+(r-1)*x); its curvature is negative.
    f = r * x / (1 + (r - 1) * x)
    expected_curvature = -2 * r * (r - 1) / (x * (r - 1) + 1) ** 3
    assert sp.factor(sp.diff(f, x, 2) - expected_curvature) == 0

    # Exact nonconstant profile x=(1/2,3/2), each with probability 1/2.
    xs = [sp.Rational(1, 2), sp.Rational(3, 2)]
    bd_eq = sp.factor(sum((r * value) / (value + r * M) for value in xs) / 2 - 1)
    beta = sp.factor(sum((r * M) / (value + r * M) for value in xs) / 2)
    assert sp.factor(beta - (r - 1) / r + bd_eq / r) == 0

    # The dB residual at S=p is strictly negative for this nonconstant
    # profile; because the residual decreases in S, its positive root is <p.
    p = (r - 1) / r
    db_eq = sp.factor(sum((r * value) / (1 + r * value * S) for value in xs) / 2 - 1)
    db_at_p = sp.factor(db_eq.subs(S, p))
    expected_db_at_p = -(r - 1) / ((r + 1) * (3 * r - 1))
    assert sp.factor(db_at_p - expected_db_at_p) == 0
    expected_db_derivative = -r**2 * (9 * S**2 * r**2 + 24 * S * r + 20) / (
        (S * r + 2) ** 2 * (3 * S * r + 2) ** 2
    )
    assert sp.factor(sp.diff(db_eq, S) - expected_db_derivative) == 0

    # At r=2, independently check the pointwise odds factorization and solve
    # both sample scalar systems exactly.
    b2 = sp.factor(b.subs(r, 2))
    s2 = sp.factor(s.subs(r, 2))
    assert sp.factor((b2 / (1 - b2)) * (s2 / (1 - s2)) - 4 * M * S) == 0
    assert sp.factor(
        1 - b2 - s2 - x * (1 - 4 * M * S) / ((x + 2 * M) * (1 + 2 * x * S))
    ) == 0

    equation_M = sp.factor(bd_eq.subs(r, 2))
    equation_S = sp.factor(db_eq.subs(r, 2))
    M_star = sp.sqrt(3) / 4
    S_star = (-1 + sp.sqrt(13)) / 6
    assert sp.factor(equation_M.subs(M, M_star)) == 0
    assert sp.factor(equation_S.subs(S, S_star)) == 0
    beta_star = sp.factor(beta.subs({r: 2, M: M_star}))
    assert sp.simplify(beta_star - sp.Rational(1, 2)) == 0
    assert sp.simplify(sp.Rational(1, 2) - S_star) > 0
    assert sp.simplify(1 - 4 * M_star * S_star) > 0
    for value in xs:
        total = sp.factor(
            b2.subs({x: value, M: M_star})
            + s2.subs({x: value, S: S_star})
        )
        assert sp.simplify(1 - total) > 0

    print("PASS exact all-r diffuse rank-one clone catalyst obstruction")


if __name__ == "__main__":
    main()
