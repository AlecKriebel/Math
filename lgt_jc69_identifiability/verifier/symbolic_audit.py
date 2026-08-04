#!/usr/bin/env python3
"""Exact symbolic audits for the LGT-JC69 derivation.

This script is intentionally separate from the interval root verifier.  It
checks normalization, topology masses, direct history-by-history Fourier
integration, the auxiliary fourteen-history compact map, and the corrected CTMC compact map.
"""
from __future__ import annotations

import sympy as s

L, MU, t1, t2 = s.symbols("lambda mu t1 t2", positive=True)
u, v = s.symbols("u v", positive=True)


def H(rate, T):
    return (1 - s.exp(-rate * T)) / rate


def TRI(a, b, T):
    # Integral over 0<u<v<T of exp(-a*u-b*v) du dv.
    return (H(b, T) - H(a + b, T)) / a


def RECT(a, b, T1, T2):
    # Integral over 0<u<T1<v<T2.
    return H(a, T1) * (s.exp(-b * T1) - s.exp(-b * T2)) / b


def fourier_rates(topology, coordinate, g1, g2):
    if coordinate == "A":
        factors = [(g1 if topology == 1 else g2, 2 * MU)]
    elif coordinate == "B":
        factors = [(g1 if topology == 2 else g2, 2 * MU)]
    elif coordinate == "C":
        factors = [(g1, MU), (g2, 2 * MU)]
    else:
        raise ValueError(coordinate)

    ct1 = ct2 = ru = rv = s.Integer(0)
    for var, rate in factors:
        if var == "t1":
            ct1 += rate
        elif var == "t2":
            ct2 += rate
        elif var == "u":
            ru += rate
        elif var == "v":
            rv += rate
        else:
            raise ValueError(var)
    return ct1, ct2, ru, rv


def term(top, coord, coef, *, d_t1=0, d_t2=0, d_u=0, d_v=0,
         g1=None, g2=None, domain="point"):
    ct1, ct2, ru, rv = fourier_rates(top, coord, g1, g2)
    pref = coef * s.exp(-(d_t1 + ct1) * t1 - (d_t2 + ct2) * t2)
    a, b = d_u + ru, d_v + rv
    if domain == "point":
        assert a == 0 and b == 0
        return pref
    if domain == "u0t1":
        assert b == 0
        return pref * H(a, t1)
    if domain == "v_t1_t2":
        assert a == 0
        return pref * (s.exp(-b * t1) - s.exp(-b * t2)) / b
    if domain == "tri":
        return pref * TRI(a, b, t1)
    if domain == "rect":
        return pref * RECT(a, b, t1, t2)
    raise ValueError(domain)


def table_history_sum(coord):
    z = s.Integer(0)
    z += term(1, coord, 1, d_t1=L, d_t2=2 * L, g1="t1", g2="t2")
    for _ in range(2):
        z += term(1, coord, L / 2, d_t2=2 * L, d_u=L,
                  g1="u", g2="t2", domain="u0t1")
    for top in (2, 3):
        z += term(top, coord, L / 2, d_t1=2 * L, d_u=L,
                  g1="u", g2="t1", domain="u0t1")
        z += term(top, coord, L / 2, d_t2=2 * L, d_u=L,
                  g1="u", g2="t2", domain="u0t1")
    for top in (1, 2, 3):
        z += term(top, coord, 2 * L**2, d_u=L, d_v=2 * L,
                  g1="u", g2="v", domain="tri")
    z += term(1, coord, 2 * L**2, d_u=L, d_v=2 * L,
              g1="u", g2="v", domain="rect")
    for top in (2, 3):
        z += term(top, coord, L**2, d_u=L, d_v=2 * L,
                  g1="u", g2="v", domain="rect")
    z += term(1, coord, 2 * L, d_t1=L, d_v=2 * L,
              g1="t1", g2="v", domain="v_t1_t2")
    return s.factor(z)


def corrected_history_sum(coord):
    z = s.Integer(0)
    # No first transfer below t1.
    z += term(1, coord, 2 * L, d_t1=L, d_v=2 * L,
              g1="t1", g2="v", domain="v_t1_t2")
    z += term(1, coord, 1, d_t1=L, d_t2=2 * L,
              g1="t1", g2="t2")

    # A second-lineage absorption below t1.  Movement events have already been
    # summed by the three-state empty-branch CTMC.
    for top in (1, 2, 3):
        z += term(top, coord, L**2, d_u=2 * L, d_v=L,
                  g1="u", g2="v", domain="tri")

    # Survive to t1.  Each weight is base + rho-base, where
    # base=lambda*exp[-lambda(t1+2u)] and
    # rho-base=lambda*exp[-(5/2)lambda*t1-(1/2)lambda*u].
    coeffs = {
        1: ((s.Rational(1, 3), -s.Rational(1, 3)),
            (s.Rational(2, 3), s.Rational(1, 3))),
        2: ((s.Rational(1, 3), s.Rational(1, 6)),
            (s.Rational(2, 3), -s.Rational(1, 6))),
        3: ((s.Rational(1, 3), s.Rational(1, 6)),
            (s.Rational(2, 3), -s.Rational(1, 6))),
    }
    for top in (1, 2, 3):
        (tb, tr), (cb, cr) = coeffs[top]
        z += term(top, coord, tb * L, d_t1=L, d_u=2 * L,
                  g1="u", g2="t1", domain="u0t1")
        z += term(top, coord, tr * L, d_t1=s.Rational(5, 2) * L,
                  d_u=s.Rational(1, 2) * L,
                  g1="u", g2="t1", domain="u0t1")

        z += term(top, coord, cb * 2 * L**2, d_t1=-L, d_u=2 * L, d_v=2 * L,
                  g1="u", g2="v", domain="rect")
        z += term(top, coord, cr * 2 * L**2, d_t1=s.Rational(1, 2) * L,
                  d_u=s.Rational(1, 2) * L, d_v=2 * L,
                  g1="u", g2="v", domain="rect")

        z += term(top, coord, cb * L, d_t1=-L, d_t2=2 * L, d_u=2 * L,
                  g1="u", g2="t2", domain="u0t1")
        z += term(top, coord, cr * L, d_t1=s.Rational(1, 2) * L,
                  d_t2=2 * L, d_u=s.Rational(1, 2) * L,
                  g1="u", g2="t2", domain="u0t1")
    return s.factor(z)


def main():
    # Site-pattern/Fourier linear equivalence.
    p0, p12, p13, pD = s.symbols("p0 p12 p13 pD")
    A = (4 * (p0 + p12) - 1) / 3
    B = (4 * (p0 + p13) - 1) / 3
    C = (16 * p0 - 1 - 3 * A - 6 * B) / 6
    inv = [
        (1 + 3 * A + 6 * B + 6 * C) / 16,
        3 * (1 + 3 * A - 2 * B - 2 * C) / 16,
        3 * (1 - A + 2 * B - 2 * C) / 16,
        3 * (1 - A - 2 * B + 2 * C) / 8,
    ]
    normalization = s.Eq(pD, 1 - p0 - p12 - 2 * p13)
    assert all(s.simplify(expr.subs(pD, normalization.rhs) - target) == 0
               for expr, target in zip(inv, (p0, p12, p13, normalization.rhs)))
    print("PASS Fourier/site-pattern transform and inverse")

    # Auxiliary fourteen-history table: exact normalization and topology frequencies.
    m0 = s.exp(-L * (t1 + 2 * t2))
    m1_T1 = 2 * s.integrate((L / 2) * s.exp(-L * (2 * t2 + u)), (u, 0, t1))
    m1_da = 2 * s.integrate((L / 2) * s.exp(-L * (2 * t1 + u)), (u, 0, t1))
    m1_db = 2 * s.integrate((L / 2) * s.exp(-L * (2 * t2 + u)), (u, 0, t1))
    m2_below = 3 * s.integrate(s.integrate(2 * L**2 * s.exp(-L * (u + 2 * v)),
                                           (u, 0, v)), (v, 0, t1))
    m2_cross = s.integrate(s.integrate(4 * L**2 * s.exp(-L * (u + 2 * v)),
                                       (u, 0, t1)), (v, t1, t2))
    m_above = s.integrate(2 * L * s.exp(-L * (t1 + 2 * v)), (v, t1, t2))
    assert s.simplify(m0 + m1_T1 + m1_da + m1_db + m2_below + m2_cross + m_above - 1) == 0
    print("PASS auxiliary fourteen-history table sums to one (internal normalization only)")

    # Direct integration of every auxiliary-table history gives exactly the auxiliary table map.
    a = L + MU
    table_formula = [
        L * (3 * L + MU) / (a * (3 * L + 2 * MU))
        + MU / a * (s.exp(-2 * a * t1) + (1 - s.exp(-L * t1)) * s.exp(-2 * a * t2))
        + L * MU / (a * (3 * L + 2 * MU)) * s.exp(-(3 * L + 2 * MU) * t1),
        L * (3 * L + MU) / (a * (3 * L + 2 * MU))
        + MU / (2 * a) * (s.exp(-2 * a * t1) + (3 - s.exp(-L * t1)) * s.exp(-2 * a * t2))
        - MU * (L + 2 * MU) / (2 * a * (3 * L + 2 * MU)) * s.exp(-(3 * L + 2 * MU) * t1),
        (L**2 + L * MU * s.exp(-2 * a * t1) + 2 * L * MU * s.exp(-2 * a * t2)
         + MU * (MU - L) * s.exp(-a * (t1 + 2 * t2))) / a**2,
    ]
    for coord, formula in zip(("A", "B", "C"), table_formula):
        assert s.simplify(table_history_sum(coord) - formula) == 0
    print("PASS every auxiliary-table history integrates to the supplied compact map")

    # Correct CTMC-integrated history map in original parameters.
    rho = (L + MU * s.exp(-2 * (L + MU) * (t2 - t1))) / (L + MU)
    E = s.exp(-2 * MU * t1)
    Lap = E * rho
    HH = lambda r: (1 - s.exp(-r * t1)) / r
    JJ = lambda aa, bb: (HH(bb) - HH(aa + bb)) / aa
    N_A = s.exp(-(3 * L + 2 * MU) * t1)
    N_B = N_A * rho
    N_C = s.exp(-(3 * L + 3 * MU) * t1) * rho
    S_AB = L**2 * (JJ(2 * L + 2 * MU, L) + 2 * JJ(2 * L, L + 2 * MU))
    S_C = 3 * L**2 * JJ(2 * L + MU, L + 2 * MU)
    I0 = L * s.exp(-L * t1) * HH(2 * L)
    Ich = L * s.exp(-L * t1) * HH(2 * L + 2 * MU)
    Irho = 2 * s.exp(-s.Rational(5, 2) * L * t1) * (1 - s.exp(-s.Rational(1, 2) * L * t1))
    Imu = L * s.exp(-L * t1) * HH(2 * L + MU)
    corrected_formula = [
        N_A + S_AB + Ich + (2 * E + 4 * Lap) * I0 / 3 + (E - Lap) * Irho / 3,
        N_B + S_AB + Ich + (2 * E + 4 * Lap) * I0 / 3 - (E - Lap) * Irho / 6,
        N_C + S_C + (E + 2 * Lap) * Imu,
    ]
    for coord, formula in zip(("A", "B", "C"), corrected_formula):
        assert s.simplify(corrected_history_sum(coord) - formula) == 0
    print("PASS CTMC-corrected histories integrate to the corrected original map")

    # Correct cube simplification.
    q, x, y = s.symbols("q x y", positive=True)
    R = q + (1 - q) * y**2
    hd = lambda c: (1 - x**c) / c
    jd = lambda aa, bb: (hd(bb) - hd(aa + bb)) / aa
    S = q**2 * (jd(2, q) + 2 * jd(2 * q, 2 - q))
    SC = 3 * q**2 * jd(1 + q, 2 - q)
    Ec = x**(2 * (1 - q))
    I0c = s.Rational(1, 2) * x**q * (1 - x**(2 * q))
    Ichc = s.Rational(1, 2) * q * x**q * (1 - x**2)
    Irc = 2 * x**(s.Rational(5, 2) * q) * (1 - x**(q / 2))
    Imc = q * x**q * (1 - x**(1 + q)) / (1 + q)
    Ac = x**(q + 2) + S + Ichc + 2 * Ec * (1 + 2 * R) * I0c / 3 + Ec * (1 - R) * Irc / 3
    Bc = x**(q + 2) * R + S + Ichc + 2 * Ec * (1 + 2 * R) * I0c / 3 - Ec * (1 - R) * Irc / 6
    Cc = x**3 * R + SC + Ec * (1 + 2 * R) * Imc
    X, Z = x**(2 - q), x**3
    Dsimple = (1 - R) * x**(2 + q / 2)
    Msimple = q * (1 - X) / (2 - q) + (1 + 2 * R) * X / 3
    Csimple = (q**2 * ((q - 2) * Z + 3 * X - (q + 1)) / ((q - 2) * (q + 1))
               + R * Z + q * (1 + 2 * R) * (X - Z) / (1 + q))
    assert s.simplify(Ac - Bc - Dsimple) == 0
    assert s.simplify((Ac + 2 * Bc) / 3 - Msimple) == 0
    assert s.simplify(Cc - Csimple) == 0
    print("PASS corrected cube map and A-B factorization")
    print("ALL SYMBOLIC AUDITS PASSED")


if __name__ == "__main__":
    main()
