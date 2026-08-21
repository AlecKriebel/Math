#!/usr/bin/env python3
"""Exact top-identity exploration on the v9=0 power-fibre branch."""

from __future__ import annotations

import sympy as sp


p, q, r, tau = sp.symbols("p q r tau")
variables = (p, q, r)


def binary_form(prefix: str, degree: int):
    coefficients = sp.symbols(f"{prefix}0:{degree + 1}")
    return (
        sum(
            coefficients[index] * p ** (degree - index) * q**index
            for index in range(degree + 1)
        ),
        coefficients,
    )


U0, u = binary_form("u", 3)
T0, c = binary_form("c", 2)
A0, x = binary_form("x", 2)
B0, y = binary_form("y", 2)
tp, tq, tt = sp.symbols("tp tq tt")
ap, aq, aa = sp.symbols("ap aq aa")
bp, bq, bb = sp.symbols("bp bq bb")

T = T0 + r * (tp * p + tq * q) + tt * r**2
U = (
    U0
    + sp.Rational(4, 3) * r * p * (tp * p + tq * q)
    + sp.Rational(4, 3) * tt * p * r**2
)
v = sp.symbols("v0:10")
monomials3 = (
    p**3,
    p**2 * q,
    p * q**2,
    q**3,
    p**2 * r,
    p * q * r,
    q**2 * r,
    p * r**2,
    q * r**2,
    r**3,
)
V = sum(coefficient * monomial for coefficient, monomial in zip(v, monomials3))
A = A0 + r * (ap * p + aq * q) + aa * r**2
B = B0 + r * (bp * p + bq * q) + bb * r**2

H4 = sp.Matrix((p**4, p**2 * q**2, 0))
H3 = sp.Matrix((U, V, p**3))
H2 = sp.Matrix((A, B, T))
l = sp.symbols("l11 l12 l13 l21 l22 l23 l31 l32 l33")
L = sp.Matrix(3, 3, l)
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
    degree: sp.Poly(sp.expand(weighted.coeff_monomial(tau**degree)), p, q, r)
    for degree in (7, 6, 5, 4, 3, 2, 1)
}
assert E[7].is_zero

base = {v[9]: 0, tt: 0}
orbits = {
    "ell_zero": {v[7]: 0, v[8]: 0},
    "ell_p": {v[7]: 1, v[8]: 0},
    "ell_q": {v[7]: 0, v[8]: 1},
    "ell_p_plus_q": {v[7]: 1, v[8]: 1},
}

def print_top_identities() -> None:
    print("PASS full determinant and E7 parameterization")
    for label, orbit in orbits.items():
        substitutions = {**base, **orbit}
        print(f"\n[{label}]")
        for degree in (6, 5):
            polynomial_in_r = sp.Poly(E[degree].as_expr(), r)
            for r_power in range(polynomial_in_r.degree(), -1, -1):
                coefficient = sp.factor(
                    polynomial_in_r.coeff_monomial(r**r_power).subs(substitutions)
                )
                if coefficient != 0:
                    print(f"E{degree}[r^{r_power}] = {coefficient}")


if __name__ == "__main__":
    print_top_identities()
