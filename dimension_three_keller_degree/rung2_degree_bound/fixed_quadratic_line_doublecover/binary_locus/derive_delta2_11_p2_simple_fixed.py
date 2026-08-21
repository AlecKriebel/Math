#!/usr/bin/env python3
"""Derive the E6 contact divisor on h=p^2 with one simple fixed root."""

from __future__ import annotations

import itertools
import sympy as sp

p, q, r, z = sp.symbols("p q r z")
A, B, C = sp.symbols("A B C")
s, t, x5, y5 = sp.symbols("s t x5 y5")
X, Y, Z = sp.symbols("X Y Z")
variables = (p, q, r)


def coefficients(value, degree):
    poly = sp.Poly(sp.expand(value), p, q)
    return [
        poly.coeff_monomial(p ** (degree - index) * q**index)
        for index in range(degree + 1)
    ]


Delta = 4 * A * C - B**2
h = p**2
P, Q = p**4, p**2 * q**2
R = p * (A * p**2 + B * p * q + C * q**2)

# Polynomial Hilbert--Burch basis on Delta != 0.  It is 3*Delta times
# the rational basis returned by the E7 coefficient matrix.
N1 = (
    16 * C * p**2,
    -2 * q * (3 * B * p - 2 * C * q),
    3 * Delta * p,
)
N2 = (
    -8 * B * p**2,
    2 * q * (6 * A * p - B * q),
    3 * Delta * q,
)
N = tuple(sp.expand(s * N1[index] + t * N2[index]) for index in range(3))

H4 = sp.Matrix([P, Q, 0])
H3 = sp.Matrix([r * N[0], r * N[1], R])
H2 = sp.Matrix([x5 * r**2, y5 * r**2, r * N[2]])
weighted = sp.Poly(
    sp.expand(
        (
            z * H2.jacobian(variables)
            + z**2 * H3.jacobian(variables)
            + z**3 * H4.jacobian(variables)
        ).det()
    ),
    z,
)
assert sp.expand(weighted.coeff_monomial(z**7)) == 0
E6r = sp.Poly(
    sp.expand(weighted.coeff_monomial(z**6)), r
).coeff_monomial(r)
equations = coefficients(E6r, 5)
lifted = []
for equation in equations:
    poly = sp.Poly(equation, s, t)
    lifted.append(
        sp.expand(
            poly.coeff_monomial(s**2) * X
            + poly.coeff_monomial(s * t) * Y
            + poly.coeff_monomial(t**2) * Z
            + poly.coeff_monomial(1)
        )
    )
M = sp.Matrix(
    [[equation.coeff(variable) for variable in (X, Y, Z, x5, y5)]
     for equation in lifted]
)
print("shape", M.shape, "rank", M.rank())
kernel = M.nullspace()
print("kernel", [[sp.factor(value) for value in vector] for vector in kernel])

for rows in itertools.combinations(range(6), 4):
    submatrix = M.extract(rows, range(5))
    minors = [
        sp.factor((-1) ** column * submatrix[:, [j for j in range(5) if j != column]].det())
        for column in range(5)
    ]
    if any(minors):
        common = sp.factor(sp.gcd_list(minors))
        primitive = [sp.factor(value / common) for value in minors]
        residual = [sp.factor(value) for value in M * sp.Matrix(primitive)]
        if all(value == 0 for value in residual):
            obstruction = sp.factor(primitive[1] ** 2 - primitive[0] * primitive[2])
            print("rows", rows)
            print("common", common)
            print("signed minors", minors)
            print("primitive kernel", primitive)
            print("obstruction", obstruction)
            break

# Delta=0 remains exact delta=2 when B*C != 0 and requires a separate
# tangent chart.  Substitute A=B^2/(4C), clear C denominators, and ask
# the E7 block for a fresh basis.
A_delta = B**2 / (4 * C)
alpha = sp.diff(Q, p) * sp.diff(R, q) - sp.diff(Q, q) * sp.diff(R, p)
beta = -(sp.diff(P, p) * sp.diff(R, q) - sp.diff(P, q) * sp.diff(R, p))
gamma = sp.diff(P, p) * sp.diff(Q, q) - sp.diff(P, q) * sp.diff(Q, p)
uu = sp.symbols("u0:3")
vv = sp.symbols("v0:3")
tt = sp.symbols("t0:2")
uform = uu[0] * p**2 + uu[1] * p * q + uu[2] * q**2
vform = vv[0] * p**2 + vv[1] * p * q + vv[2] * q**2
tform = tt[0] * p + tt[1] * q
unknowns = (*uu, *vv, *tt)
e7_delta = coefficients(
    sp.together(
        (alpha * uform + beta * vform + gamma * tform).subs(A, A_delta)
    ) * C,
    7,
)
M_delta = sp.Matrix(
    [[sp.expand(equation).coeff(variable) for variable in unknowns]
     for equation in e7_delta]
)
print("Delta=0 E7 rank", M_delta.rank())
print(
    "Delta=0 tangents",
    [
        [sp.factor(value) for value in vector]
        for vector in M_delta.nullspace()
    ],
)

N1_delta = (8 * C * p**2, -3 * B * p * q + 2 * C * q**2, 0)
N2_delta = (0, 2 * p * q, B * p + 2 * C * q)
N_delta = tuple(
    sp.expand(s * N1_delta[index] + t * N2_delta[index])
    for index in range(3)
)
R_delta = sp.expand(R.subs(A, A_delta))
H3_delta = sp.Matrix([r * N_delta[0], r * N_delta[1], R_delta])
H2_delta = sp.Matrix([x5 * r**2, y5 * r**2, r * N_delta[2]])
weighted_delta = sp.Poly(
    sp.expand(
        (
            z * H2_delta.jacobian(variables)
            + z**2 * H3_delta.jacobian(variables)
            + z**3 * H4.jacobian(variables)
        ).det()
    ),
    z,
)
assert sp.expand(weighted_delta.coeff_monomial(z**7)) == 0
E6r_delta = sp.Poly(
    sp.expand(weighted_delta.coeff_monomial(z**6)), r
).coeff_monomial(r)
equations_delta = coefficients(E6r_delta, 5)
lifted_delta = []
for equation in equations_delta:
    poly = sp.Poly(equation, s, t)
    lifted_delta.append(
        sp.expand(
            poly.coeff_monomial(s**2) * X
            + poly.coeff_monomial(s * t) * Y
            + poly.coeff_monomial(t**2) * Z
            + poly.coeff_monomial(1)
        )
    )
M_contact_delta = sp.Matrix(
    [
        [
            equation.coeff(variable)
            for variable in (X, Y, Z, x5, y5)
        ]
        for equation in lifted_delta
    ]
)
print("Delta=0 contact rank", M_contact_delta.rank())
for rows in itertools.combinations(range(6), 4):
    submatrix = M_contact_delta.extract(rows, range(5))
    minors = [
        sp.factor(
            (-1) ** column
            * submatrix[:, [j for j in range(5) if j != column]].det()
        )
        for column in range(5)
    ]
    if any(minors):
        common = sp.factor(sp.gcd_list(minors))
        primitive = [sp.factor(value / common) for value in minors]
        residual = [
            sp.factor(value)
            for value in M_contact_delta * sp.Matrix(primitive)
        ]
        if all(value == 0 for value in residual):
            obstruction = sp.factor(
                primitive[1] ** 2 - primitive[0] * primitive[2]
            )
            print("Delta=0 rows", rows)
            print("Delta=0 common", common)
            print("Delta=0 signed minors", minors)
            print("Delta=0 primitive kernel", primitive)
            print("Delta=0 obstruction", obstruction)
            break
        break
