#!/usr/bin/env python3
"""Full lower-jet exploration of the b1=0 unmarked-double endpoint."""

from __future__ import annotations

import sympy as sp


p, q, r, tau = sp.symbols("p q r tau")
d, m, n, rho = sp.symbols("d m n rho")
variables = (p, q, r)


def binary_form(prefix: str, degree: int):
    coefficients = sp.symbols(f"{prefix}0:{degree + 1}")
    value = sum(
        coefficients[index] * p ** (degree - index) * q**index
        for index in range(degree + 1)
    )
    return value, coefficients


P = p * q**3
Q = p**4
R = d * p**3 + q**3
U0, u = binary_form("u", 3)
V0, v = binary_form("v", 3)
T0, w = binary_form("w", 2)
A0, aa = binary_form("aa", 2)
B0, bb = binary_form("bb", 2)
xp, xq, yp, yq, xrr, yrr = sp.symbols("xp xq yp yq xrr yrr")
linear = sp.symbols("ell0:9")

f0 = m * p + n * q
U = U0 + 3 * p * f0 * r + sp.Rational(3, 2) * p * rho * r**2
V = V0
T = T0 + 3 * f0 * r + sp.Rational(3, 2) * rho * r**2
A = A0 + r * (xp * p + xq * q) + xrr * r**2
B = B0 + r * (yp * p + yq * q) + yrr * r**2

H4 = sp.Matrix((P, Q, 0))
H3 = sp.Matrix((U, V, R))
H2 = sp.Matrix((A, B, T))
L = sp.Matrix(3, 3, linear)
weighted = sp.Poly(
    sp.expand(
        (
            L
            + tau * H2.jacobian(variables)
            + tau**2 * H3.jacobian(variables)
            + tau**3 * H4.jacobian(variables)
        ).det()
    ),
    tau,
)
E = {
    degree: sp.Poly(
        sp.expand(weighted.coeff_monomial(tau**degree)), p, q, r
    )
    for degree in range(1, 9)
}
assert E[8].is_zero and E[7].is_zero


def equations(polynomial: sp.Poly):
    return [coefficient for _, coefficient in polynomial.terms()]


def main() -> None:
    print("E6 terms", len(E[6].terms()))
    for monomial, coefficient in E[6].terms():
        print(monomial, sp.factor(coefficient))

    rho_solution = {
        v[1]: 0,
        v[2]: 0,
        u[1]: w[1],
        u[2]: w[2],
        yp: 3 * m * v[3],
        yq: 3 * n * v[3],
        yrr: sp.Rational(3, 2) * rho * v[3],
        xp: linear[8] + 3 * m * u[3],
        xq: 3 * n * u[3],
        xrr: sp.Rational(3, 2) * rho * u[3],
    }
    assert all(
        sp.expand(value.subs(rho_solution)) == 0
        for value in equations(E[6])
    )
    e5_rho = sp.Poly(
        sp.expand(E[5].as_expr().subs(rho_solution)), p, q, r
    )
    print("E5 rho terms", len(e5_rho.terms()))
    for monomial, coefficient in e5_rho.terms():
        if monomial[2] > 0:
            print("rho", monomial, sp.factor(coefficient))
    e5_rho_solution = {
        bb[1]: v[3] * w[1],
        bb[2]: v[3] * w[2],
        aa[2]: u[3] * w[2],
        aa[1]: linear[7] + u[3] * w[1],
    }
    e5_rho = sp.Poly(
        sp.expand(e5_rho.as_expr().subs(e5_rho_solution)), p, q, r
    )
    print("E5 rho residual")
    for monomial, coefficient in e5_rho.terms():
        print(monomial, sp.factor(coefficient))
    column_solution = {
        linear[5]: linear[8] * v[3],
        linear[2]: linear[8] * u[3],
    }
    rho_all = {**rho_solution, **e5_rho_solution, **column_solution}
    e4_rho = sp.Poly(
        sp.expand(E[4].as_expr().subs(rho_all)), p, q, r
    )
    print("E4 rho r-positive")
    for monomial, coefficient in e4_rho.terms():
        if monomial[2] > 0:
            print(monomial, sp.factor(coefficient))

    # rho=0, m=0,n=1 chart.
    n_chart = {
        rho: 0,
        m: 0,
        n: 1,
        v[1]: 0,
        u[1]: w[1],
        yp: 2 * v[2],
        yq: 3 * v[3],
        xp: linear[8] + 2 * u[2] - 2 * w[2],
        xq: 3 * u[3],
        xrr: 0,
        yrr: 0,
    }
    assert all(
        sp.expand(value.subs(n_chart)) == 0
        for value in equations(E[6])
    )
    e5_n = sp.Poly(sp.expand(E[5].as_expr().subs(n_chart)), p, q, r)
    print("E5 n-chart r-positive")
    for monomial, coefficient in e5_n.terms():
        if monomial[2] > 0:
            print(monomial, sp.factor(coefficient))
    n_e5_solution = {v[2]: 0, u[2]: w[2]}
    e5_n_residual = sp.Poly(
        sp.expand(e5_n.as_expr().subs(n_e5_solution)), p, q, r
    )
    print("E5 n-chart residual")
    for monomial, coefficient in e5_n_residual.terms():
        print(monomial, sp.factor(coefficient))
    n_e5_pivots = (aa[1], aa[2], bb[1], bb[2])
    n_e5_lower_solution = sp.solve(
        equations(e5_n_residual), n_e5_pivots, dict=True
    )[0]
    print("n E5 solution", {
        key: sp.factor(value)
        for key, value in n_e5_lower_solution.items()
    })
    e4_n = sp.Poly(
        sp.expand(
            E[4]
            .as_expr()
            .subs(n_chart)
            .subs(n_e5_solution)
            .subs(n_e5_lower_solution)
        ),
        p,
        q,
        r,
    )
    print("E4 n-chart before column-three equations")
    for monomial, coefficient in e4_n.terms():
        print(monomial, sp.factor(coefficient))
    n_column_three = {
        linear[5]: linear[8] * v[3],
        linear[2]: linear[8] * u[3],
    }
    e4_n_columns = sp.Poly(
        sp.expand(e4_n.as_expr().subs(n_column_three)), p, q, r
    )
    print("E4 n-chart after column-three equations")
    for monomial, coefficient in e4_n_columns.terms():
        print(monomial, sp.factor(coefficient))

    # rho=0,m=1,n=t chart.
    tt = sp.symbols("tt")
    m_chart = {
        rho: 0,
        m: 1,
        n: tt,
        v[2]: -tt * v[1] / 2,
        u[1]: w[1] - sp.Rational(3, 4) * d * v[1],
        u[2]: w[2] + sp.Rational(3, 8) * d * tt * v[1],
        yp: 3 * v[3] - tt**2 * v[1],
        yq: 3 * tt * v[3],
        xp: (
            linear[8]
            + 3 * u[3]
            + sp.Rational(3, 4) * d * tt**2 * v[1]
        ),
        xq: 3 * tt * u[3] - v[1] / 4,
        xrr: 0,
        yrr: 0,
    }
    assert all(
        sp.expand(value.subs(m_chart)) == 0
        for value in equations(E[6])
    )
    e5_m = sp.Poly(sp.expand(E[5].as_expr().subs(m_chart)), p, q, r)
    print("E5 m-chart r-positive")
    for monomial, coefficient in e5_m.terms():
        if monomial[2] > 0:
            print(monomial, sp.factor(coefficient))
    m_e5_solution = {v[1]: 0}
    e5_m_residual = sp.Poly(
        sp.expand(e5_m.as_expr().subs(m_e5_solution)), p, q, r
    )
    print("E5 m-chart residual")
    for monomial, coefficient in e5_m_residual.terms():
        print(monomial, sp.factor(coefficient))
    m_column_three = {
        linear[5]: linear[8] * v[3],
        linear[2]: linear[8] * u[3],
    }
    e5_m_columns = sp.Poly(
        sp.expand(e5_m_residual.as_expr().subs(m_column_three)),
        p,
        q,
        r,
    )
    m_e5_pivots = (aa[1], aa[2], bb[1], bb[2])
    m_e5_lower_solution = sp.solve(
        equations(e5_m_columns), m_e5_pivots, dict=True
    )[0]
    print("m E5 solution", {
        key: sp.factor(value)
        for key, value in m_e5_lower_solution.items()
    })
    e4_m = sp.Poly(
        sp.expand(
            E[4]
            .as_expr()
            .subs(m_chart)
            .subs(m_e5_solution)
            .subs(m_column_three)
            .subs(m_e5_lower_solution)
        ),
        p,
        q,
        r,
    )
    print("E4 m-chart")
    for monomial, coefficient in e4_m.terms():
        print(monomial, sp.factor(coefficient))

    e4_zero_rho = sp.Poly(
        sp.expand(E[4].as_expr().subs(rho_all).subs(rho, 0)),
        p,
        q,
        r,
    )
    print("E4 rho=0 residual")
    for monomial, coefficient in e4_zero_rho.terms():
        print(monomial, sp.factor(coefficient))


if __name__ == "__main__":
    main()
