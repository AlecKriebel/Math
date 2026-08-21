#!/usr/bin/env python3
"""Full E6/E5 equations on the interior eta=0 delta=1 survivor."""

from __future__ import annotations

import sympy as sp

p, q, r, z = sp.symbols("p q r z")
a, c, k = sp.symbols("a c k")
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

H4 = sp.Matrix(
    [(p**2 + q**2) * p**2, (p**2 + q**2) * q**2, 0]
)
H3 = sp.Matrix(
    [
        U0 + k * r * p**2,
        V0 + k * r * (p**2 + 2 * q**2),
        a * p**3 + c * p * q**2,
    ]
)
H2 = sp.Matrix(
    [
        A0 + r * A1 + A2 * r**2,
        B0 + r * B1 + B2 * r**2,
        T0 + k * c * p * r,
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

E6_expression = sp.expand(weighted.coeff_monomial(z**6))
E5_expression = sp.expand(weighted.coeff_monomial(z**5))
E4_expression = sp.expand(weighted.coeff_monomial(z**4))

for degree in (6, 5, 4):
    coefficient = sp.Poly(
        sp.expand(weighted.coeff_monomial(z**degree)), r
    )
    print("E", degree, "r-degree", coefficient.degree())
    for power in range(coefficient.degree(), -1, -1):
        part = sp.factor(coefficient.coeff_monomial(r**power))
        if part != 0:
            print("E", degree, "r^", power, "=", part)

E6_after_high = sp.expand(E6_expression.subs({x[5]: 0, y[5]: k**2}))
E6_constant = sp.Poly(E6_after_high, r).coeff_monomial(1)
equations_e6_constant = sp.Poly(E6_constant, p, q).coeffs()
solution_e6_constant = sp.solve(
    equations_e6_constant,
    (x[3], x[4], y[3], y[4], ell[8]),
    dict=True,
)
print("E6 CONSTANT SOLUTIONS", solution_e6_constant)
M6, rhs6 = sp.linear_eq_to_matrix(
    equations_e6_constant, (x[3], x[4], y[3], y[4], ell[8])
)
print("M6 rank", M6.rank())
left6 = M6.T.nullspace()
print("M6 compatibility", [sp.factor((vector.T * rhs6)[0]) for vector in left6])
row_pivots = M6.T.rref()[1]
print("M6 independent rows", row_pivots)
selected_solution = sp.solve(
    [equations_e6_constant[index] for index in row_pivots],
    (x[3], x[4], y[3], y[4], ell[8]),
    dict=True,
)[0]
print("M6 selected solution", selected_solution)
print(
    "M6 residual",
    [
        sp.factor(equation.subs(selected_solution))
        for equation in equations_e6_constant
    ],
)

e6_solution = {
    x[5]: 0,
    y[5]: k**2,
    v[1]: u[1],
    t[1]: c * u[1],
    x[3]: k * u[2],
    x[4]: sp.Rational(3, 2) * k * u[3],
    y[3]: k * v[2],
    y[4]: k * (sp.Rational(3, 2) * v[3] - u[1]),
    ell[8]: k * t[2],
}
E5_after_e6 = sp.Poly(sp.expand(E5_expression.subs(e6_solution)), r)
print("E5 AFTER GENERIC E6")
for power in range(E5_after_e6.degree(), -1, -1):
    value = sp.factor(E5_after_e6.coeff_monomial(r**power))
    if value != 0:
        print("E5|E6 r^", power, "=", value)

e5_high_solution = {u[3]: 0, v[3]: 2 * u[1]}
print(
    "E5 CONSTANT AFTER HIGH",
    sp.factor(
        E5_after_e6.coeff_monomial(1).subs(e5_high_solution)
    ),
)
E5_constant_after_high = sp.expand(
    E5_after_e6.coeff_monomial(1).subs(e5_high_solution)
)
equations_e5_constant = sp.Poly(E5_constant_after_high, p, q).coeffs()
M5, rhs5 = sp.linear_eq_to_matrix(
    equations_e5_constant,
    (x[1], x[2], y[1], y[2], ell[2], ell[5], ell[7]),
)
print("M5 rank", M5.rank())
print("M5 left compatibility", [
    sp.factor((vector.T * rhs5)[0]) for vector in M5.T.nullspace()
])
print(
    "M5 solution",
    sp.solve(
        equations_e5_constant,
        (x[1], x[2], y[1], y[2], ell[2], ell[5], ell[7]),
        dict=True,
    ),
)

e5_constant_solution = {
    x[1]: u[1] * u[2],
    y[1]: u[1] * v[2],
    x[2]: ell[2] / k,
    y[2]: u[1] ** 2 + ell[5] / k,
    ell[7]: t[2] * u[1],
}
E4_after_e5 = sp.Poly(
    sp.factor(
        E4_expression
        .subs(e6_solution)
        .subs(e5_high_solution)
        .subs(e5_constant_solution)
    ),
    r,
)
print("E4 AFTER FULL E5")
for power in range(E4_after_e5.degree(), -1, -1):
    value = sp.factor(E4_after_e5.coeff_monomial(r**power))
    if value != 0:
        print("E4|E5 r^", power, "=", value)
