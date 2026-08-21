#!/usr/bin/env python3
"""Full E6/E5 equations on the branch-square delta=1 survivor.

Exploratory only: this retains every binary H3/H2 coefficient and every
linear coefficient.  It prints exact split equations and parameter ranks
without asserting a classification.
"""

from __future__ import annotations

import sympy as sp

p, q, r, z = sp.symbols("p q r z")
b, d, k = sp.symbols("b d k")
variables = (p, q, r)

u = sp.symbols("u0:4")
v = sp.symbols("v0:4")
t = sp.symbols("t0:3")
x = sp.symbols("x0:6")
y = sp.symbols("y0:6")
ell = sp.symbols("l0:9")


def binary(coefficients, degree):
    return sum(
        coefficients[index] * p ** (degree - index) * q**index
        for index in range(degree + 1)
    )


U0 = binary(u, 3)
V0 = binary(v, 3)
T0 = binary(t, 2)
A0 = binary(x[:3], 2)
A1 = x[3] * p + x[4] * q
A2 = x[5]
B0 = binary(y[:3], 2)
B1 = y[3] * p + y[4] * q
B2 = y[5]

H4 = sp.Matrix([p**4, p**2 * q**2, 0])
H3 = sp.Matrix(
    [U0 + 2 * k * r * p**2, V0 + k * r * q**2,
     b * p**2 * q + d * q**3]
)
H2 = sp.Matrix(
    [
        A0 + r * A1 + A2 * r**2,
        B0 + r * B1 + B2 * r**2,
        T0 + k * b * q * r,
    ]
)
L = sp.Matrix(3, 3, ell)

weighted = sp.Poly(
    sp.expand(
        (
            L
            + z * H2.jacobian(variables)
            + z**2 * H3.jacobian(variables)
            + z**3 * H4.jacobian(variables)
        ).det()
    ),
    z,
)
E6 = sp.Poly(sp.expand(weighted.coeff_monomial(z**6)), r)
E5 = sp.Poly(sp.expand(weighted.coeff_monomial(z**5)), r)
E4 = sp.Poly(sp.expand(weighted.coeff_monomial(z**4)), r)

print("E6 r-degree", E6.degree(r))
for power in range(E6.degree(r), -1, -1):
    part = sp.factor(E6.coeff_monomial(r**power))
    if part != 0:
        print("E6 r^", power, "=", part)

print("E5 r-degree", E5.degree(r))
for power in range(E5.degree(r), -1, -1):
    part = sp.factor(E5.coeff_monomial(r**power))
    if part != 0:
        print("E5 r^", power, "=", part)

e6_solution = {
    x[5]: k**2,
    y[5]: 0,
    u[2]: 0,
    t[1]: b * v[2],
    y[3]: sp.Rational(3, 2) * k * v[0],
    y[4]: k * v[1],
    x[3]: k * (sp.Rational(3, 2) * u[0] - v[2]),
    x[4]: k * u[1],
    ell[8]: k * t[0],
}
print("AFTER GENERIC E6 (b*d*k != 0)")
for power in range(E5.degree(r), -1, -1):
    part = sp.factor(
        sp.expand(E5.coeff_monomial(r**power).subs(e6_solution))
    )
    if part != 0:
        print("E5|E6 r^", power, "=", part)

e5_high_solution = {v[0]: 0, u[0]: 2 * v[2]}
print("AFTER E5 r^1")
print(
    sp.factor(
        sp.expand(
            E5.coeff_monomial(1).subs(e6_solution).subs(e5_high_solution)
        )
    )
)

e5_constant_solution = {
    x[1]: u[1] * v[2],
    y[1]: v[1] * v[2],
    ell[2]: k * (x[0] - v[2] ** 2),
    ell[5]: k * y[0],
    ell[6]: t[0] * v[2],
}
print("E4 AFTER FULL E5")
for power in range(E4.degree(r), -1, -1):
    part = sp.factor(
        sp.expand(
            E4.coeff_monomial(r**power)
            .subs(e6_solution)
            .subs(e5_high_solution)
            .subs(e5_constant_solution)
        )
    )
    if part != 0:
        print("E4|E5 r^", power, "=", part)

# Gauge-normalized E5-completed family (after scaling b=d=k=1).
omega, theta = sp.symbols("omega theta")
aa0, aa2, bb0, bb2, tau = sp.symbols("aa0 aa2 bb0 bb2 tau")
m0, m1, m3, m4, m7 = sp.symbols("m0 m1 m3 m4 m7")
H3_normal = sp.Matrix(
    [2 * r * p**2, r * q**2 + omega * q**3, p**2 * q + q**3]
)
H2_normal = sp.Matrix(
    [
        r**2 + aa0 * p**2 + aa2 * q**2,
        bb0 * p**2 + bb2 * q**2,
        q * r + tau * p**2 + theta * q**2,
    ]
)
L_normal = sp.Matrix(
    [[m0, m1, aa0], [m3, m4, bb0], [0, m7, tau]]
)
normal_weighted = sp.Poly(
    sp.expand(
        (
            L_normal
            + z * H2_normal.jacobian(variables)
            + z**2 * H3_normal.jacobian(variables)
            + z**3 * H4.jacobian(variables)
        ).det()
    ),
    z,
)
print("GAUGE-NORMAL E5-COMPLETED FAMILY")
for degree in range(8, -1, -1):
    coefficient = sp.factor(normal_weighted.coeff_monomial(z**degree))
    if coefficient != 0:
        print("E", degree, "=", coefficient)


def equation_matrix(expression, unknowns):
    equations = sp.Poly(sp.expand(expression), p, q, r).coeffs()
    matrix, _ = sp.linear_eq_to_matrix(equations, unknowns)
    return matrix


e6_unknowns = (x[5], y[5], x[3], x[4], y[3], y[4], ell[8])
M_e6 = equation_matrix(E6.as_expr(), e6_unknowns)
e5_after_e6 = sp.expand(E5.as_expr().subs(e6_solution))
M_e5_high = equation_matrix(
    sp.Poly(e5_after_e6, r).coeff_monomial(r), (u[0], v[0], v[2])
)
e5_low_after_high = sp.expand(
    sp.Poly(e5_after_e6, r).coeff_monomial(1).subs(e5_high_solution)
)
M_e5_low = equation_matrix(
    e5_low_after_high,
    (x[0], x[1], y[0], y[1], ell[2], ell[5], ell[6]),
)
print("RANK TABLE b,d,k")
for label, values in (
    ("open", {b: 1, d: 1, k: 1}),
    ("b=0", {b: 0, d: 1, k: 1}),
    ("d=0", {b: 1, d: 0, k: 1}),
    ("k=0", {b: 1, d: 1, k: 0}),
    ("R=0", {b: 0, d: 0, k: 1}),
):
    print(
        label,
        tuple(
            matrix.subs(values).rank()
            for matrix in (M_e6, M_e5_high, M_e5_low)
        ),
    )
