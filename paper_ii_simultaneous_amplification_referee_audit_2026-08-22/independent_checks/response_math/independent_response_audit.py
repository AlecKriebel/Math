#!/usr/bin/env python3
"""Independent exact audit of the response/optimization calculations.

This file deliberately re-derives the displayed formulas from the component
limits rather than importing or calling the authors' certificate programs.
"""

from __future__ import annotations

import sympy as sp


r, s, lam, eta = sp.symbols("r s lam eta", positive=True)
p = (r - 1) / r


def variation_count(sequence: list[sp.Expr], x: sp.Rational) -> int:
    signs: list[int] = []
    for term in sequence:
        value = sp.sign(term.subs(r, x))
        if value == 0:
            continue
        assert value in (-1, 1)
        signs.append(int(value))
    return sum(a != b for a, b in zip(signs, signs[1:]))


def main() -> None:
    # Complete-graph baselines from birth/death count-chain odds.  The dB
    # products telescope even though the one-step odds are not constant.
    for n_value in range(2, 13):
        for r_value in (sp.Rational(3, 2), sp.Rational(2), sp.Rational(7, 3)):
            bd_products = [sp.Integer(1)]
            db_products = [sp.Integer(1)]
            db_product = sp.Integer(1)
            for k in range(1, n_value):
                bd_products.append(r_value ** (-k))
                db_odds = (
                    n_value - 1 + (r_value - 1) * k
                ) / (
                    r_value
                    * (n_value - 1 + (r_value - 1) * (k - 1))
                )
                db_product *= db_odds
                expected_product = r_value ** (-k) * (
                    n_value - 1 + (r_value - 1) * k
                ) / (n_value - 1)
                assert sp.factor(db_product - expected_product) == 0
                db_products.append(db_product)
            rho_bd_chain = sp.cancel(1 / sum(bd_products))
            rho_db_chain = sp.cancel(1 / sum(db_products))
            rho_bd_formula = (1 - 1 / r_value) / (1 - r_value ** (-n_value))
            rho_db_formula = (
                sp.Rational(n_value - 1, n_value)
                * (1 - 1 / r_value)
                / (1 - r_value ** (-(n_value - 1)))
            )
            assert sp.factor(rho_bd_chain - rho_bd_formula) == 0
            assert sp.factor(rho_db_chain - rho_db_formula) == 0

    # Gate ratios from the four limiting component rates.  These are the
    # leading limits of the manuscript's A and D columns.
    A_bd = 2 * s * (r - 1)
    D_bd = 2 / (r + 1)
    A_db = 2 * (r - 1)
    D_db = s / r
    Z_bd = sp.cancel(A_bd / D_bd)
    Z_db = sp.cancel(A_db / D_db)
    assert sp.factor(Z_bd - s * (r**2 - 1)) == 0
    assert sp.factor(Z_db - 2 * r * (r - 1) / s) == 0

    pair_bd = r / (r + 1) * Z_bd / (1 + Z_bd)
    pair_db = sp.Rational(1, 2) * Z_db / (1 + Z_db)

    # Reconstruct the full normalized traces at first order.  C is scaled to
    # one, m/C=lam*eta, q/C=eta.  The center numerators are p+lam*eta for Bd
    # and p for dB; the common vertex-count denominator is 1+(lam+2)*eta.
    trace_bd_over_p = (p + lam * eta + 2 * eta * pair_bd) / (
        p * (1 + (lam + 2) * eta)
    )
    trace_db_over_p = (p + 2 * eta * pair_db) / (
        p * (1 + (lam + 2) * eta)
    )
    B_from_trace = sp.factor(sp.diff(trace_bd_over_p, eta).subs(eta, 0))
    D_from_trace = sp.factor(sp.diff(trace_db_over_p, eta).subs(eta, 0))

    B = 2 * (s - 1) / (1 + s * (r**2 - 1)) + lam / (r - 1)
    D = 2 * (r * (2 - r) - s) / (s + 2 * r * (r - 1)) - lam
    assert sp.factor(B_from_trace - B) == 0
    assert sp.factor(D_from_trace - D) == 0

    pair_response_bd = sp.factor(2 * (pair_bd / p - 1))
    pair_response_db = sp.factor(2 * (pair_db / p - 1))
    assert sp.factor(
        pair_response_bd - 2 * (s - 1) / (1 + s * (r**2 - 1))
    ) == 0
    assert sp.factor(
        pair_response_db
        - 2 * (r * (2 - r) - s) / (s + 2 * r * (r - 1))
    ) == 0
    # The remaining terms are exactly the pendant displacements:
    # lam*(1/p-1)=lam/(r-1) for Bd, and -lam for dB.
    assert sp.factor(lam * (1 / p - 1) - lam / (r - 1)) == 0

    L = 2 * (1 - s) * (r - 1) / (1 + s * (r**2 - 1))
    U = 2 * (r * (2 - r) - s) / (s + 2 * r * (r - 1))
    assert sp.factor(B - (lam - L) / (r - 1)) == 0
    assert sp.factor(D - (U - lam)) == 0

    F = (r - 1) * s**2 + (r**3 - 4 * r**2 + 3 * r + 1) * s + r * (
        2 * r - 3
    )
    gap_num, gap_den = sp.cancel(U - L).as_numer_denom()
    assert sp.factor(gap_num + 2 * r * F) == 0
    assert sp.factor(
        gap_den
        - (1 + s * (r**2 - 1)) * (s + 2 * r * (r - 1))
    ) == 0

    sigma_min = sp.factor(-sp.diff(F, s).subs(s, 0) / (2 * (r - 1)))
    expected_sigma = (-r**3 + 4 * r**2 - 3 * r - 1) / (2 * (r - 1))
    assert sp.factor(sigma_min - expected_sigma) == 0

    P = r**6 - 8 * r**5 + 22 * r**4 - 30 * r**3 + 21 * r**2 - 6 * r + 1
    min_F = sp.factor(F.subs(s, sigma_min))
    assert sp.factor(min_F + P / (4 * (r - 1))) == 0
    assert sp.factor(sp.discriminant(F, s) - P) == 0

    dL = sp.factor(sp.diff(L, r))
    dU = sp.factor(sp.diff(U, r))
    expected_dL = 2 * (s - 1) * (s * (r - 1) ** 2 - 1) / (
        1 + s * (r**2 - 1)
    ) ** 2
    expected_dU = 4 * r * (s - r) / (s + 2 * r * (r - 1)) ** 2
    assert sp.factor(dL - expected_dL) == 0
    assert sp.factor(dU - expected_dU) == 0

    # Independent Sturm variation counts at exact rational endpoints.
    sturm = sp.sturm(P, r)
    V1 = variation_count(sturm, sp.Rational(1))
    V15 = variation_count(sturm, sp.Rational(3, 2))
    V151 = variation_count(sturm, sp.Rational(151, 100))
    assert V1 - V15 == 0
    assert V15 - V151 == 1
    assert P.subs(r, sp.Rational(3, 2)) == sp.Rational(1, 64)
    assert P.subs(r, sp.Rational(151, 100)) == -sp.Rational(
        39866792399, 10**12
    )

    isolating_intervals = sp.intervals(P, eps=sp.Rational(1, 10**16))
    desired = [
        interval
        for interval, multiplicity in isolating_intervals
        if multiplicity == 1
        and interval[0] > sp.Rational(3, 2)
        and interval[1] < sp.Rational(151, 100)
    ]
    assert len(desired) == 1
    R = sp.CRootOf(sp.Poly(P, r), 0)
    assert sp.Rational(3, 2) < R < sp.Rational(151, 100)
    sigma_star = sigma_min.subs(r, R)
    lambda_star = L.subs({r: R, s: sigma_star})
    assert sigma_star > 0 and sigma_star < 1 and lambda_star > 0
    # Tangency: F and its sigma derivative vanish at the algebraic point.
    assert sp.simplify(F.subs({r: R, s: sigma_star})) == 0
    assert sp.simplify(sp.diff(F, s).subs({r: R, s: sigma_star})) == 0

    # Rational-edge specialization.
    sr = sp.Rational(19, 137)
    lr = sp.Rational(20, 27)
    Bq = sp.factor(B.subs({s: sr, lam: lr}))
    Dq = sp.factor(D.subs({s: sr, lam: lr}))
    assert Bq.subs(r, sp.Rational(3, 2)) == sp.Rational(232, 17361)
    assert Dq.subs(r, sp.Rational(3, 2)) == sp.Rational(65, 12123)
    Q = 6439 * r**2 - 10138 * r + 703
    Rq = (sp.Integer(5069) + 12 * sp.sqrt(147001)) / 6439
    assert sp.simplify(Q.subs(r, Rq)) == 0
    assert sp.factor(
        Dq + 2 * Q / (27 * (274 * r**2 - 274 * r + 19))
    ) == 0
    assert sp.Rational(3, 2) < Rq < sp.Rational(151, 100)
    assert sp.simplify(Bq.subs(r, Rq)) > 0
    assert sp.simplify(F.subs({r: Rq, s: sr})) < 0

    print("gate ratios:", Z_bd, Z_db)
    print("complete-graph count-chain baselines: exact checks n=2,...,12 PASS")
    print("response functions:", B, D)
    print("gap numerator/denominator:", sp.factor(gap_num), sp.factor(gap_den))
    print("Sturm variations at 1, 3/2, 151/100:", V1, V15, V151)
    print("all real isolating intervals for P:", isolating_intervals)
    print("R_hyb, sigma_*, lambda_*:", sp.N(R, 20), sp.N(sigma_star, 20), sp.N(lambda_star, 20))
    print("rational margins at 3/2:", Bq.subs(r, sp.Rational(3, 2)), Dq.subs(r, sp.Rational(3, 2)))
    print("R_Q:", sp.N(Rq, 20))
    print("Bd response at R_Q (exact):", sp.radsimp(Bq.subs(r, Rq)))
    print("Bd response at R_Q (decimal):", sp.N(Bq.subs(r, Rq), 20))
    print("F_{R_Q}(19/137) (exact):", sp.radsimp(F.subs({r: Rq, s: sr})))
    print("PASS independent response/optimization audit")


if __name__ == "__main__":
    main()
