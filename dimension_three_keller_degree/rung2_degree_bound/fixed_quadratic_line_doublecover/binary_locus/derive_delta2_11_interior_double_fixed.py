#!/usr/bin/env python3
"""Derive E6 data for h=(p-wq)(wp-q), R=(p-wq)^2(Ap+Bq)."""

from __future__ import annotations

import itertools
import sympy as sp

p, q, r, z = sp.symbols("p q r z")
w, A, B = sp.symbols("w A B")
c1, c2, x5, y5 = sp.symbols("c1 c2 x5 y5")
X, Y, Z = sp.symbols("X Y Z")
variables = (p, q, r)


def jac(first, second):
    return sp.expand(
        sp.diff(first, p) * sp.diff(second, q)
        - sp.diff(first, q) * sp.diff(second, p)
    )


def coefficients(value, degree):
    poly = sp.Poly(sp.expand(value), p, q)
    return [
        poly.coeff_monomial(p ** (degree - index) * q**index)
        for index in range(degree + 1)
    ]


L = p - w * q
Mfixed = w * p - q
h = sp.expand(L * Mfixed)
P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
R = sp.expand(L**2 * (A * p + B * q))
alpha, beta, gamma = jac(Q, R), -jac(P, R), jac(P, Q)
g = sp.factor(sp.gcd(sp.gcd(alpha, beta), gamma))
print("gcd", g)

uu = sp.symbols("u0:3")
vv = sp.symbols("v0:3")
tt = sp.symbols("t0:2")
uform = uu[0] * p**2 + uu[1] * p * q + uu[2] * q**2
vform = vv[0] * p**2 + vv[1] * p * q + vv[2] * q**2
tform = tt[0] * p + tt[1] * q
unknowns = (*uu, *vv, *tt)
M7 = sp.Matrix(
    [
        [equation.coeff(variable) for variable in unknowns]
        for equation in coefficients(
            alpha * uform + beta * vform + gamma * tform, 7
        )
    ]
)
print("E7 rank", M7.rank())
basis = M7.nullspace()
print(
    "E7 basis",
    [[sp.factor(value) for value in vector] for vector in basis],
)
for rows in itertools.combinations(range(8), 6):
    for cols in itertools.combinations(range(8), 6):
        value = sp.factor(M7.extract(rows, cols).det())
        if value:
            print("E7 decisive", rows, cols, value)
            break
    else:
        continue
    break

tangents = []
for vector in basis:
    substitution = dict(zip(unknowns, vector))
    tangents.append(
        tuple(
            sp.factor(form.subs(substitution))
            for form in (uform, vform, tform)
        )
    )
denominators = [
    sp.fraction(value)[1]
    for tangent in tangents
    for value in tangent
]
scale = sp.factor(sp.lcm(denominators))
print("basis denominator lcm", scale)
N1 = tuple(sp.factor(scale * value) for value in tangents[0])
N2 = tuple(sp.factor(scale * value) for value in tangents[1])
print("polynomial basis N1", N1)
print("polynomial basis N2", N2)

N = tuple(
    sp.expand(c1 * N1[index] + c2 * N2[index])
    for index in range(3)
)
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
lifted = []
for equation in coefficients(E6r, 5):
    poly = sp.Poly(equation, c1, c2)
    lifted.append(
        sp.expand(
            poly.coeff_monomial(c1**2) * X
            + poly.coeff_monomial(c1 * c2) * Y
            + poly.coeff_monomial(c2**2) * Z
            + poly.coeff_monomial(1)
        )
    )
contact = sp.Matrix(
    [
        [
            equation.coeff(variable)
            for variable in (X, Y, Z, x5, y5)
        ]
        for equation in lifted
    ]
)
print("contact generic rank", contact.rank())
maximal = []
for omitted in range(6):
    rows = [index for index in range(6) if index != omitted]
    value = sp.factor(contact.extract(rows, range(5)).det())
    maximal.append(value)
    print("contact omit", omitted, value)
print("contact maximal gcd", sp.factor(sp.gcd_list(maximal)))

# Saturate the residual rank-drop ideal on two projective coefficient
# charts.  The common factor comes from orbit/evaluation pivots; the
# exact-open product also removes deeper fixed-root and branch-contact
# incidences.
left_contact = 5 * A * w**2 - 3 * A - 4 * B * w
right_contact = 4 * A * w + 3 * B * w**2 - 5 * B
common_contact = (w - 1) ** 3 * (w + 1) ** 3 * (A * w + B) ** 6
reduced_maximal = [
    sp.cancel(value / common_contact) for value in maximal
]
inv = sp.symbols("inv")
for label, normalization, coefficient in (
    ("B=1", {B: 1}, A),
    ("A=1", {A: 1}, B),
):
    residual_chart = [
        sp.Poly(sp.expand(value.subs(normalization)), coefficient, w).as_expr()
        for value in reduced_maximal
    ]
    open_chart = sp.expand(
        (
            w
            * (w - 1)
            * (w + 1)
            * (A + B * w)
            * (A * w + B)
            * left_contact
            * right_contact
        ).subs(normalization)
    )
    print("starting saturation", label)
    basis_chart = sp.groebner(
        residual_chart + [inv * open_chart - 1],
        inv,
        coefficient,
        w,
        order="grevlex",
    )
    print(
        "saturation",
        label,
        [sp.factor(poly.as_expr()) for poly in basis_chart.polys],
    )

a0, a1, b0, b1, l33 = sp.symbols("a0 a1 b0 b1 l33")
constant = (
    alpha * (a0 * p + a1 * q)
    + beta * (b0 * p + b1 * q)
    + gamma * l33
)
constant_matrix = sp.Matrix(
    [
        [equation.coeff(variable) for variable in (a0, a1, b0, b1, l33)]
        for equation in coefficients(constant, 6)
    ]
)
print("constant generic rank", constant_matrix.rank())
constant_maximal = []
for omitted_pair in itertools.combinations(range(7), 2):
    rows = [index for index in range(7) if index not in omitted_pair]
    value = sp.factor(constant_matrix.extract(rows, range(5)).det())
    if value:
        constant_maximal.append(value)
        print("constant rows", rows, value)
print("constant maximal gcd", sp.factor(sp.gcd_list(constant_maximal)))
