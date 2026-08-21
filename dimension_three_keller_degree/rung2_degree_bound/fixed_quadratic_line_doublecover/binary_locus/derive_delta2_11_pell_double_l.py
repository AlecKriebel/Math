#!/usr/bin/env python3
"""Derive E6 contact data for h=p(p+q), R=(p+q)^2(Ap+Bq)."""

from __future__ import annotations

import itertools
import sympy as sp

p, q, r, z = sp.symbols("p q r z")
A, B = sp.symbols("A B")
s, t, x5, y5 = sp.symbols("s t x5 y5")
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


ell = p + q
h = p * ell
P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
R = ell**2 * (A * p + B * q)
alpha, beta, gamma = jac(Q, R), -jac(P, R), jac(P, Q)
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
print("basis", [[sp.factor(value) for value in K] for K in basis])
tangents = []
for vector in basis:
    substitution = dict(zip(unknowns, vector))
    tangents.append(
        (
            sp.factor(uform.subs(substitution)),
            sp.factor(vform.subs(substitution)),
            sp.factor(tform.subs(substitution)),
        )
    )
scale = 5 * (A - B) ** 2
N1 = tuple(sp.factor(scale * value) for value in tangents[0])
N2 = tuple(sp.factor(scale * value) for value in tangents[1])
print("polynomial basis", N1, N2)
N = tuple(sp.expand(s * N1[i] + t * N2[i]) for i in range(3))
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
    [
        [
            equation.coeff(variable)
            for variable in (X, Y, Z, x5, y5)
        ]
        for equation in lifted
    ]
)
print("contact rank", M.rank())
print("contact kernel", [[sp.factor(v) for v in K] for K in M.nullspace()])
maximal = []
for omitted in range(6):
    rows = [index for index in range(6) if index != omitted]
    maximal.append(sp.factor(M.extract(rows, range(5)).det()))
print("contact maximal gcd", sp.factor(sp.gcd_list(maximal)))
for omitted, value in enumerate(maximal):
    print("contact omit", omitted, value)
rank = M.rank()
for rows in itertools.combinations(range(6), rank):
    found = False
    for cols in itertools.combinations(range(5), rank):
        minor = sp.factor(M.extract(rows, cols).det())
        if minor:
            print("decisive", rows, cols, minor)
            found = True
            break
    if found:
        break

a0, a1, b0, b1, l33 = sp.symbols("a0 a1 b0 b1 l33")
constant = (
    alpha * (a0 * p + a1 * q)
    + beta * (b0 * p + b1 * q)
    + gamma * l33
)
Mc = sp.Matrix(
    [
        [equation.coeff(variable) for variable in (a0, a1, b0, b1, l33)]
        for equation in coefficients(constant, 6)
    ]
)
print("constant rank", Mc.rank())
for rows in itertools.combinations(range(7), 5):
    determinant = sp.factor(Mc.extract(rows, range(5)).det())
    if determinant:
        print("constant decisive", rows, determinant)
        break

# Exceptional quartic in the normalized B=1 chart.
a = sp.symbols("a")
exceptional = 5 * a**4 + 40 * a**3 + 120 * a**2 + 592 * a + 701
Ma = sp.simplify(M.subs({A: a, B: 1}))
for rows in itertools.combinations(range(6), 4):
    submatrix = Ma.extract(rows, range(5))
    minors = sp.Matrix(
        [
            sp.factor(
                (-1) ** column
                * submatrix[
                    :,
                    [index for index in range(5) if index != column],
                ].det()
            )
            for column in range(5)
        ]
    )
    reduced = sp.Matrix(
        [
            sp.rem(sp.together(value), exceptional, domain=sp.QQ)
            for value in minors
        ]
    )
    if any(value != 0 for value in reduced):
        residual = [
            sp.factor(value)
            for value in Ma * reduced
        ]
        if all(
            sp.rem(sp.together(value), exceptional, domain=sp.QQ) == 0
            for value in residual
        ):
            obstruction = sp.factor(reduced[1] ** 2 - reduced[0] * reduced[2])
            obstruction_remainder = sp.factor(
                sp.rem(obstruction, exceptional, domain=sp.QQ)
            )
            print("exceptional rows", rows)
            print("exceptional kernel mod f", list(reduced))
            print("exceptional obstruction rem", obstruction_remainder)
            print(
                "exceptional resultant",
                sp.factor(sp.resultant(exceptional, obstruction_remainder, a)),
            )
            break


def fresh_case(label, R_case):
    alpha_case = jac(Q, R_case)
    beta_case = -jac(P, R_case)
    gamma_case = jac(P, Q)
    matrix7 = sp.Matrix(
        [
            [equation.coeff(variable) for variable in unknowns]
            for equation in coefficients(
                alpha_case * uform + beta_case * vform + gamma_case * tform,
                7,
            )
        ]
    )
    basis_case = matrix7.nullspace()
    forms = []
    for vector in basis_case:
        substitution = dict(zip(unknowns, vector))
        forms.append(
            (
                sp.factor(uform.subs(substitution)),
                sp.factor(vform.subs(substitution)),
                sp.factor(tform.subs(substitution)),
            )
        )
    N_case = tuple(
        sp.expand(s * forms[0][i] + t * forms[1][i])
        for i in range(3)
    )
    H3_case = sp.Matrix([r * N_case[0], r * N_case[1], R_case])
    H2_case = sp.Matrix([x5 * r**2, y5 * r**2, r * N_case[2]])
    determinant = sp.Poly(
        sp.expand(
            (
                z * H2_case.jacobian(variables)
                + z**2 * H3_case.jacobian(variables)
                + z**3 * H4.jacobian(variables)
            ).det()
        ),
        z,
    )
    e6r = sp.Poly(
        sp.expand(determinant.coeff_monomial(z**6)), r
    ).coeff_monomial(r)
    lifted_case = []
    for equation in coefficients(e6r, 5):
        poly = sp.Poly(equation, s, t)
        lifted_case.append(
            sp.expand(
                poly.coeff_monomial(s**2) * X
                + poly.coeff_monomial(s * t) * Y
                + poly.coeff_monomial(t**2) * Z
                + poly.coeff_monomial(1)
            )
        )
    matrix_case = sp.Matrix(
        [
            [
                equation.coeff(variable)
                for variable in (X, Y, Z, x5, y5)
            ]
            for equation in lifted_case
        ]
    )
    print(label, "basis", forms)
    print(label, "rank", matrix_case.rank())
    for omitted in range(6):
        rows = [index for index in range(6) if index != omitted]
        determinant = sp.factor(matrix_case.extract(rows, range(5)).det())
        if determinant:
            print(label, "decisive", rows, determinant)
            break


fresh_case("A=B=1", (p + q) ** 3)
