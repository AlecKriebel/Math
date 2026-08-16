#!/usr/bin/env python3
"""Independent exact reconstruction for the all-spectrum stable family.

This verifier layer intentionally does not import anything from ``computation``.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
import sympy as sp


@dataclass(frozen=True)
class Reaction:
    label: str
    y: tuple[int, ...]
    yp: tuple[int, ...]


def reactions(m: int) -> list[Reaction]:
    if m < 3:
        raise ValueError("m >= 3 required")
    n = m + 1

    def v(items: dict[int, int] | None = None) -> tuple[int, ...]:
        out = [0] * n
        if items:
            for i, value in items.items():
                out[i] = value
        return tuple(out)

    out = [Reaction("R0", v(), v({0: 1}))]
    for i in range(2, m - 1):
        out.append(Reaction(f"R{i}", v({0: 1, i - 1: 1}), v({0: 1, i: 1})))
    out += [
        Reaction("Ra", v({0: 1, m - 2: 1}), v({m - 1: 2})),
        Reaction("Rb", v({m - 1: 2}), v({1: 1})),
        Reaction("R+", v({m: 2}), v({0: 1, m - 1: 1})),
        Reaction("R-", v({0: 1, m - 1: 1}), v({m: 2})),
    ]
    if len(out) != m + 2:
        raise AssertionError("wrong reaction count")
    return out


def gamma_y(m: int) -> tuple[sp.Matrix, sp.Matrix]:
    rs = reactions(m)
    Y = sp.Matrix.hstack(*(sp.Matrix(r.y) for r in rs))
    Yp = sp.Matrix.hstack(*(sp.Matrix(r.yp) for r in rs))
    return Yp - Y, Y


def conservation(m: int) -> sp.Matrix:
    return sp.Matrix([0] + [4] * (m - 2) + [2, 1])


def flux(m: int, a: sp.Expr, b: sp.Expr) -> sp.Matrix:
    return sp.Matrix([a] * m + [b, b])


def A_matrix(m: int, a: sp.Expr = sp.Integer(1), b: sp.Expr = sp.Integer(1)) -> sp.Matrix:
    G, Y = gamma_y(m)
    return sp.simplify(G * sp.diag(*list(flux(m, a, b))) * Y.T)


def B_map(m: int, u: sp.Matrix, w: sp.Matrix) -> sp.Matrix:
    G, Y = gamma_y(m)
    weights = flux(m, sp.Integer(1), sp.Integer(1))
    ans = sp.zeros(m + 1, 1)
    for r in range(Y.cols):
        val = sp.Integer(0)
        for i in range(m + 1):
            yi = int(Y[i, r])
            val += yi * (yi - 1) * u[i] * w[i]
            for j in range(i + 1, m + 1):
                yj = int(Y[j, r])
                val += yi * yj * (u[i] * w[j] + u[j] * w[i])
        ans += weights[r] * val * G[:, r]
    return sp.simplify(ans)


def Lval(m: int | sp.Expr, j: int | sp.Expr) -> sp.Expr:
    return sp.Integer(227) * m - 451 - 3 * j


def r_seed(m: int) -> sp.Matrix:
    return sp.Matrix(
        [1]
        + [-sp.Rational(Lval(m, i), 96 * (m - 2)) for i in range(2, m)]
        + [sp.Rational(-11, 16), sp.Rational(1, 40)]
    )


def d_seed(m: int) -> list[sp.Expr]:
    return (
        [sp.Rational(257, 240), sp.Rational(m + 1, Lval(m, 2))]
        + [sp.Rational(3, Lval(m, i)) for i in range(3, m)]
        + [sp.Rational(43, 165), 21]
    )


def D_seed(m: int) -> sp.Matrix:
    return sp.diag(*d_seed(m))


def ell_seed(m: int) -> sp.Matrix:
    return sp.Matrix(
        [sp.Rational(-45880, 5123), sp.Rational(783160, 15369)]
        + [
            sp.Rational(59520160 * (m - 2), 5123 * (227 * m - 448 - 3 * i))
            for i in range(3, m)
        ]
        + [sp.Rational(219835, 10246), 1]
    )


def Hsum(m: int) -> sp.Expr:
    return sp.Add(*(sp.Rational(1, Lval(m, j)) for j in range(2, m - 1)), evaluate=True)


def w0_formula(m: int) -> sp.Matrix:
    v1 = sp.Rational(721600 * m - 1519799, 76800 * (8 * m - 17))
    v2 = sp.Rational(4800 * m**2 - 43001 * m + 68002,
                     76800 * (m - 2) * (8 * m - 17))
    return sp.Matrix(
        [v1, v2]
        + [v2 - sp.Rational(i - 2, 64 * (m - 2)) for i in range(3, m)]
        + [sp.Rational(-121, 1024),
           sp.Rational(109402 * m - 229079, 38400 * (8 * m - 17))]
    )


def Tfactor(m: int, i: int) -> sp.Expr:
    num = sp.prod(Lval(m, j) for j in range(i - 3, i + 1))
    den = sp.prod(Lval(m, j) for j in range(-1, 3))
    return sp.factor(num / den)


def w2_formula(m: int) -> tuple[sp.Matrix, sp.Expr]:
    sig = sp.Rational(1, 64 * (m - 2))
    s1 = sp.Rational(-14503, 9600)
    s2 = -sp.Rational(Lval(m, 2), 192 * (m - 2)) - sp.Rational(121, 512)
    sm = sp.Rational(47269, 19200)
    sz = sp.Rational(1101, 1600)
    P = Tfactor(m, m - 1)
    g2 = sp.Rational(231 * m - 453, Lval(m, 2))
    alpha = sp.factor(P / g2)
    U = sp.factor((Lval(m, m - 1) - P * Lval(m, 2)) / 9)
    beta = sp.factor(-alpha * s2 - sig * U)
    M = sp.Matrix([
        [-sp.Rational(377, 60) + alpha, -2 * alpha - 1, 2],
        [1 - 2 * alpha, 4 * alpha - sp.Rational(997, 165), 2],
        [2, 2, -88],
    ])
    W1, Wm, Wz = [sp.factor(x) for x in M.inv() * sp.Matrix([s1 + beta, sm - 2 * beta, sz])]
    W2 = sp.factor((-W1 + 2 * Wm - s2) / g2)
    vec = [W1, W2]
    vec += [
        sp.factor(Tfactor(m, i) * (W2 + sig * Lval(m, 2) / 9) - sig * Lval(m, i) / 9)
        for i in range(3, m)
    ]
    vec += [Wm, Wz]
    return sp.Matrix(vec), sp.factor(M.det())


def qpoly(m: int | sp.Expr) -> sp.Expr:
    return (
        sp.Integer(1910521667596003) * m**3
        - sp.Integer(11322779437089660) * m**2
        + sp.Integer(22368031913707929) * m
        - sp.Integer(14729097938020928)
    )


def ell_r_formula(m: int | sp.Expr, H: sp.Expr) -> sp.Expr:
    return sp.factor(
        -(sp.Integer(892802400) * m**2 - sp.Integer(3400424303) * m + sp.Integer(3217891606))
        / (sp.Integer(7377120) * (m - 2))
        + sp.Rational(1860005, 5123) * H
    )


def ell_Dr_formula(m: int | sp.Expr, H: sp.Expr) -> sp.Expr:
    return sp.factor(
        -(sp.Integer(99148487) * m - sp.Integer(186549574))
        / (sp.Integer(7377120) * (m - 2))
        - sp.Rational(1860005, 5123) * H
    )


def cubic_num_formula(m: int | sp.Expr, H: sp.Expr) -> sp.Expr:
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
    return sp.factor(
        A5 / (sp.Integer(566562816000) * (m - 2) * (8 * m - 17) * qpoly(m))
        - sp.Integer(372001) * B4 * H
        / (sp.Integer(78689280) * (8 * m - 17) * qpoly(m))
    )


def cubic_lower_poly(m: int | sp.Expr) -> sp.Expr:
    return (
        sp.Integer(16961968965064836030215580229120) * m**6
        - sp.Integer(204060992591161140189804029423632) * m**5
        + sp.Integer(1022744662082541440031646436769769) * m**4
        - sp.Integer(2733435957152538936565966048042046) * m**3
        + sp.Integer(4108750818252419615808760310850899) * m**2
        - sp.Integer(3293419603698721148657010487662254) * m
        + sp.Integer(1099794747471284681949805627086720)
    )


def ell_r_bound_poly(m: int | sp.Expr) -> sp.Expr:
    return (
        sp.Integer(199987737600) * m**3
        - sp.Integer(1161670519072) * m**2
        + sp.Integer(2247388570579) * m
        - sp.Integer(1448032207870)
    )


def shifted_coeffs(expr: sp.Expr, symbol: sp.Symbol) -> list[sp.Integer]:
    u = sp.symbols("u")
    p = sp.Poly(sp.expand(expr.subs(symbol, u + 3)), u)
    return [p.coeff_monomial(u**k) for k in range(p.degree(), -1, -1)]


def characteristic_product(m: int, lam: sp.Expr, t: sp.Expr) -> sp.Expr:
    ds = d_seed(m)
    g1 = lam + 2 + t * ds[0]
    gm = lam + 5 + t * ds[m - 1]
    gz = lam + 4 + t * ds[m]
    Q = sp.prod(lam + 1 + t * ds[i - 1] for i in range(2, m))
    F = g1 * gm * gz - 4 * g1 - 4 * gm + gz
    G = gz * (4 * g1 + gm) - 36
    return sp.factor(Q * F - G)


def hurwitz_determinants(coeffs: Iterable[sp.Expr]) -> list[sp.Expr]:
    """Hurwitz determinants for a monic polynomial coefficients [1,a1,...,an]."""
    cs = list(coeffs)
    n = len(cs) - 1
    a = [sp.Integer(1)] + cs[1:]
    out = []
    for k in range(1, n + 1):
        H = sp.zeros(k)
        for i in range(k):
            for j in range(k):
                idx = 2 * (i + 1) - (j + 1)
                H[i, j] = a[idx] if 0 <= idx <= n else 0
        out.append(sp.factor(H.det()))
    return out
