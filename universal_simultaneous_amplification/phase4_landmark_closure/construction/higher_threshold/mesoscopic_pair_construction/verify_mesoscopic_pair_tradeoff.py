#!/usr/bin/env python3
"""Exact symbolic verifier for MESOSCOPIC_PAIR_BURST_NO_GO.md.

The script checks only finite symbolic components.  The stopped-chain
convergence in Section 6 is an analytic rare-event argument, not a symbolic
identity.
"""

import sympy as sp


def main() -> None:
    r, m, x, h, b = sp.symbols("r m x h b", positive=True)

    beta_b = r**2 / (r + 1)
    c_b = 2 * r * (r + 1)
    h_b = (r**3 - 1) / (r * (r**2 + 2 * m * (r + 1)))
    h_d = m * (r**3 - 1) / (r**2 + m * r**3)

    # Jensen rearrangements: equality for the homogeneous ratio x_i=m.
    s_child_b = c_b * h * m / (1 + c_b * h * m)
    eq_b = sp.factor(
        h - beta_b * s_child_b / (2 * m + beta_b * s_child_b)
    )
    assert sp.factor((eq_b / h).subs(h, h_b)) == 0

    a_d = r**2 * h
    s_child_d = a_d / (m + a_d)
    eq_d = sp.factor(h - r * m * s_child_d / (1 + r * m * s_child_d))
    assert sp.factor((eq_d / h).subs(h, h_d)) == 0

    # Homogeneous extinction formulas reconstructed from the burst equations.
    q_b_hom = sp.factor(1 / (1 + c_b * m * h_b))
    q_d_hom = sp.factor(m / (m + r**2 * h_d))
    assert sp.factor(
        q_b_hom
        - (2 * m * (r + 1) + r**2)
        / (r**2 * (1 + 2 * r * m * (r + 1)))
    ) == 0
    assert sp.factor(
        q_d_hom - (1 + r * m) / (r * (m + r**2))
    ) == 0

    K = sp.factor(c_b * h_b)
    A = sp.factor(r**2 * h_d)
    L = sp.factor(K * A)
    L_expected = (
        2
        * r**2
        * m
        * (r + 1)
        * (r**3 - 1) ** 2
        / ((r**2 + 2 * m * (r + 1)) * (r**2 + m * r**3))
    )
    assert sp.factor(L - L_expected) == 0

    surv_b = K * x / (1 + K * x)
    surv_d = A / (x + A)
    assert sp.factor(
        surv_b
        + surv_d
        - 1
        - x * (L - 1) / ((1 + K * x) * (x + A))
    ) == 0

    f = L * (1 - b) / (b + L * (1 - b))
    assert sp.factor(
        sp.diff(f, b, 2)
        - 2 * L * (1 - L) / (L + (1 - L) * b) ** 3
    ) == 0

    # Maximization of L(m): its derivative has the advertised unique sign
    # change at m^2=r/(2(r+1)).
    dL_num = sp.factor(sp.together(sp.diff(L, m))).as_numer_denom()[0]
    dL_expected = (
        -2
        * r
        * (r + 1)
        * (r - 1) ** 2
        * (r**2 + r + 1) ** 2
        * (2 * m**2 * (r + 1) - r)
    )
    assert sp.factor(dL_num - dL_expected) == 0

    m_star = sp.sqrt(r / (2 * (r + 1)))
    L_max = sp.factor(L.subs(m, m_star))
    L_max_expected = (
        2
        * (r + 1)
        * (r**3 - 1) ** 2
        / (r ** sp.Rational(3, 2) + sp.sqrt(2 * (r + 1))) ** 2
    )
    assert sp.simplify(L_max - L_max_expected) == 0

    B0 = 1 - r**-2
    D0 = 2 * (r - 1) / r
    assert sp.factor(B0 + D0 - 1) == (2 * r**2 - 2 * r - 1) / r**2
    assert sp.factor(f.subs(b, B0) - L / (r**2 - 1 + L)) == 0

    L_req = 2 * (r - 1) ** 2 * (r + 1) / (2 - r)
    # f_L(B0)=D0 exactly at L=L_req.
    assert sp.factor(
        (L / (r**2 - 1 + L) - D0).subs(L, L_req)
    ) == 0

    # Derivative certificate for the radical inequality L_max<L_req.
    g = (
        r ** sp.Rational(3, 2)
        + sp.sqrt(2 * (r + 1))
        - (r**2 + r + 1) * sp.sqrt(2 - r)
    )
    g_prime_expected = (
        sp.Rational(3, 2) * sp.sqrt(r)
        + 1 / sp.sqrt(2 * (r + 1))
        + (5 * r**2 - 5 * r - 3) / (2 * sp.sqrt(2 - r))
    )
    assert sp.simplify(sp.diff(g, r) - g_prime_expected) == 0
    last = (5 * r**2 - 5 * r - 3) / (2 * sp.sqrt(2 - r))
    assert sp.simplify(
        sp.diff(last, r)
        - (-15 * r**2 + 45 * r - 23) / (4 * (2 - r) ** sp.Rational(3, 2))
    ) == 0
    assert sp.simplify(g.subs(r, 1)) == 0
    assert sp.simplify(g_prime_expected.subs(r, 1) - sp.Rational(1, 2)) == 0

    # Exact threshold root.
    r0 = (1 + sp.sqrt(3)) / 2
    assert sp.simplify(2 * r0**2 - 2 * r0 - 1) == 0

    # Generic two-state protected-module template, equations (37)--(46).
    CB, CD = sp.symbols("C_B C_D", positive=True)
    betaB, betaD = sp.symbols("beta_B beta_D", positive=True)
    ellB, ellD = sp.symbols("ell_B ell_D", positive=True)
    RB = CB * betaB / ellB
    RD = CD * betaD / ellD
    HB_generic = (betaB * CB - ellB) / (CB * (ellB * m + betaB))
    HD_generic = m * (betaD * CD - ellD) / (CD * (ellD + betaD * m))
    Kg = sp.factor(CB * HB_generic)
    Ag = sp.factor(CD * HD_generic)
    ug, vg = betaB / ellB, betaD / ellD
    assert sp.factor(Kg - (RB - 1) / (m + ug)) == 0
    assert sp.factor(Ag - m * (RD - 1) / (1 + vg * m)) == 0
    Lg = sp.factor(Kg * Ag)
    mg = sp.sqrt(ug / vg)
    Lg_max = sp.simplify(Lg.subs(m, mg))
    Lg_expected = (RB - 1) * (RD - 1) / (1 + sp.sqrt(ug * vg)) ** 2
    assert sp.simplify(Lg_max - Lg_expected) == 0

    pair_subs = {
        CB: 2 * r * (r + 1),
        betaB: r**2 / (r + 1),
        ellB: 2,
        CD: r**2,
        betaD: r,
        ellD: 1,
    }
    assert sp.factor(RB.subs(pair_subs) - r**3) == 0
    assert sp.factor(RD.subs(pair_subs) - r**3) == 0
    assert sp.simplify(Lg_expected.subs(pair_subs) - L_max_expected) == 0

    print("PASS: Bd and dB burst fixed-point identities")
    print("PASS: homogeneous Jensen envelopes")
    print("PASS: constant-odds-product curvature identity")
    print("PASS: exact maximizer and L_max formula")
    print("PASS: radical derivative certificate and threshold")
    print("PASS: generic two-state protected-module extension")


if __name__ == "__main__":
    main()
