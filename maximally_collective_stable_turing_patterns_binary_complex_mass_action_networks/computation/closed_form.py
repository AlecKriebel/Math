#!/usr/bin/env python3
"""Closed all-m formulas for the successful rational seed.

This module is discovery-side convenience code.  The independent verifier has
its own formulas and does not import this module.
"""
from __future__ import annotations
import sympy as sp


def L(m: int | sp.Expr, j: int | sp.Expr) -> sp.Expr:
    return sp.Integer(227) * m - 451 - 3 * j


def right_vector(m: int) -> sp.Matrix:
    if m < 3:
        raise ValueError("m must be at least 3")
    vals = [sp.Integer(1)]
    vals.extend(-sp.Rational(L(m, i), 96 * (m - 2)) for i in range(2, m))
    vals.extend([sp.Rational(-11, 16), sp.Rational(1, 40)])
    return sp.Matrix(vals)


def diffusion_entries(m: int) -> list[sp.Expr]:
    if m < 3:
        raise ValueError("m must be at least 3")
    return (
        [sp.Rational(257, 240), sp.Rational(m + 1, L(m, 2))]
        + [sp.Rational(3, L(m, i)) for i in range(3, m)]
        + [sp.Rational(43, 165), sp.Integer(21)]
    )


def diffusion_matrix(m: int) -> sp.Matrix:
    return sp.diag(*diffusion_entries(m))


def left_vector(m: int) -> sp.Matrix:
    if m < 3:
        raise ValueError("m must be at least 3")
    vals: list[sp.Expr] = [sp.Rational(-45880, 5123), sp.Rational(783160, 15369)]
    for i in range(3, m):
        vals.append(sp.Rational(59520160 * (m - 2), 5123 * (227 * m - 448 - 3 * i)))
    vals.extend([sp.Rational(219835, 10246), sp.Integer(1)])
    return sp.Matrix(vals)


def Hsum(m: int) -> sp.Expr:
    if m < 3:
        raise ValueError("m must be at least 3")
    return sp.Add(*(sp.Rational(1, L(m, j)) for j in range(2, m - 1)), evaluate=True)


def zero_mode(m: int) -> sp.Matrix:
    if m < 3:
        raise ValueError("m must be at least 3")
    w1 = sp.Rational(721600 * m - 1519799, 76800 * (8 * m - 17))
    w2 = sp.Rational(
        4800 * m**2 - 43001 * m + 68002,
        76800 * (m - 2) * (8 * m - 17),
    )
    vals = [w1, w2]
    vals.extend(w2 - sp.Rational(i - 2, 64 * (m - 2)) for i in range(3, m))
    vals.extend([
        sp.Rational(-121, 1024),
        sp.Rational(109402 * m - 229079, 38400 * (8 * m - 17)),
    ])
    return sp.Matrix(vals)


def Tfactor(m: int, i: int) -> sp.Expr:
    """The four-factor telescoping product T_i, valid already at i=2."""
    num = sp.prod(L(m, j) for j in range(i - 3, i + 1))
    den = sp.prod(L(m, j) for j in range(-1, 3))
    return sp.factor(num / den)


def second_harmonic_data(m: int) -> dict[str, sp.Expr | sp.Matrix]:
    if m < 3:
        raise ValueError("m must be at least 3")
    sigma = sp.Rational(1, 64 * (m - 2))
    s1 = sp.Rational(-14503, 9600)
    s2 = -sp.Rational(L(m, 2), 192 * (m - 2)) - sp.Rational(121, 512)
    sm = sp.Rational(47269, 19200)
    sz = sp.Rational(1101, 1600)
    P = Tfactor(m, m - 1)
    g2 = sp.Rational(231 * m - 453, L(m, 2))
    alpha = sp.factor(P / g2)
    U = sp.factor((L(m, m - 1) - P * L(m, 2)) / 9)
    beta = sp.factor(-alpha * s2 - sigma * U)
    M = sp.Matrix([
        [-sp.Rational(377, 60) + alpha, -2 * alpha - 1, 2],
        [1 - 2 * alpha, 4 * alpha - sp.Rational(997, 165), 2],
        [2, 2, -88],
    ])
    boundary_rhs = sp.Matrix([s1 + beta, sm - 2 * beta, sz])
    W1, Wm, Wz = [sp.factor(x) for x in M.inv() * boundary_rhs]
    W2 = sp.factor((-W1 + 2 * Wm - s2) / g2)
    vals = [W1, W2]
    vals.extend(
        sp.factor(Tfactor(m, i) * (W2 + sigma * L(m, 2) / 9) - sigma * L(m, i) / 9)
        for i in range(3, m)
    )
    vals.extend([Wm, Wz])
    return {
        "sigma": sigma,
        "s1": s1,
        "s2": s2,
        "sm": sm,
        "sz": sz,
        "P": P,
        "g2": g2,
        "alpha": alpha,
        "U": U,
        "beta": beta,
        "M": M,
        "boundary_rhs": boundary_rhs,
        "vector": sp.Matrix(vals),
        "detM": sp.factor(M.det()),
    }


def second_harmonic(m: int) -> sp.Matrix:
    return second_harmonic_data(m)["vector"]  # type: ignore[return-value]


def qpoly(m: sp.Expr) -> sp.Expr:
    return (
        sp.Integer(1910521667596003) * m**3
        - sp.Integer(11322779437089660) * m**2
        + sp.Integer(22368031913707929) * m
        - sp.Integer(14729097938020928)
    )


def ell_dot_r_formula(m: int | sp.Expr, H: sp.Expr) -> sp.Expr:
    return sp.factor(
        -(
            sp.Integer(892802400) * m**2
            - sp.Integer(3400424303) * m
            + sp.Integer(3217891606)
        ) / (sp.Integer(7377120) * (m - 2))
        + sp.Rational(1860005, 5123) * H
    )


def ell_dot_Dr_formula(m: int | sp.Expr, H: sp.Expr) -> sp.Expr:
    return sp.factor(
        -(
            sp.Integer(99148487) * m - sp.Integer(186549574)
        ) / (sp.Integer(7377120) * (m - 2))
        - sp.Rational(1860005, 5123) * H
    )


def cubic_numerator_formula(m: int | sp.Expr, H: sp.Expr) -> sp.Expr:
    A5 = (
        sp.Integer(86392373709756938206702324880) * m**5
        - sp.Integer(878316832027584429913234554493) * m**4
        + sp.Integer(3570576759617470240582317330966) * m**3
        - sp.Integer(7255203323904441261456947317999) * m**2
        + sp.Integer(7368642295819384535817788489606) * m
        - sp.Integer(2992572008943165191299483794816)
    )
    B4 = (
        sp.Integer(892292533383541579520) * m**4
        - sp.Integer(7159841249775619992477) * m**3
        + sp.Integer(21539344009097108736900) * m**2
        - sp.Integer(28792766432259158176231) * m
        + sp.Integer(14430205416389750108352)
    )
    R = A5 / (sp.Integer(566562816000) * (m - 2) * (8 * m - 17) * qpoly(m))
    C = -sp.Integer(372001) * B4 / (
        sp.Integer(78689280) * (8 * m - 17) * qpoly(m)
    )
    return sp.factor(R + C * H)


def eta_formula(m: int) -> sp.Expr:
    H = Hsum(m)
    return sp.factor(ell_dot_Dr_formula(m, H) / ell_dot_r_formula(m, H))


def cubic_formula(m: int) -> sp.Expr:
    H = Hsum(m)
    return sp.factor(cubic_numerator_formula(m, H) / ell_dot_r_formula(m, H))


def boundary_determinant_polynomial(m: sp.Expr) -> sp.Expr:
    return qpoly(m)


def cubic_lower_polynomial(m: sp.Expr) -> sp.Expr:
    return (
        sp.Integer(16961968965064836030215580229120) * m**6
        - sp.Integer(204060992591161140189804029423632) * m**5
        + sp.Integer(1022744662082541440031646436769769) * m**4
        - sp.Integer(2733435957152538936565966048042046) * m**3
        + sp.Integer(4108750818252419615808760310850899) * m**2
        - sp.Integer(3293419603698721148657010487662254) * m
        + sp.Integer(1099794747471284681949805627086720)
    )


def ell_r_upper_polynomial(m: sp.Expr) -> sp.Expr:
    return (
        sp.Integer(199987737600) * m**3
        - sp.Integer(1161670519072) * m**2
        + sp.Integer(2247388570579) * m
        - sp.Integer(1448032207870)
    )


def shifted_coefficients(poly: sp.Expr, degree: int | None = None) -> list[int]:
    u = sp.symbols("u")
    p = sp.Poly(sp.expand(poly.subs({sp.symbols("m"): u + 3}) if sp.symbols("m") in poly.free_symbols else poly), u)
    if degree is None:
        degree = p.degree()
    return [int(p.coeff_monomial(u**k)) for k in range(degree, -1, -1)]


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("m", type=int)
    args = parser.parse_args()
    m = args.m
    print("r =", right_vector(m).T)
    print("D =", diffusion_entries(m))
    print("ell =", left_vector(m).T)
    print("w0 =", zero_mode(m).T)
    print("w2 =", second_harmonic(m).T)
    print("eta =", eta_formula(m))
    print("c =", cubic_formula(m))
