#!/usr/bin/env python3
"""Derive E6 data for h=p(p+q), R=(p+q)(-4Bp^2+Bpq+Cq^2)."""

from __future__ import annotations

import itertools
import sympy as sp

p, q, r, z = sp.symbols("p q r z")
B, C = sp.symbols("B C")
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


def contact_matrix(P_case, Q_case, R_case, first, second):
    tangent = tuple(
        sp.expand(s * first[index] + t * second[index])
        for index in range(3)
    )
    H4 = sp.Matrix([P_case, Q_case, 0])
    H3 = sp.Matrix([r * tangent[0], r * tangent[1], R_case])
    H2 = sp.Matrix([x5 * r**2, y5 * r**2, r * tangent[2]])
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
    e6r = sp.Poly(
        sp.expand(weighted.coeff_monomial(z**6)), r
    ).coeff_monomial(r)
    lifted = []
    for equation in coefficients(e6r, 5):
        poly = sp.Poly(equation, s, t)
        lifted.append(
            sp.expand(
                poly.coeff_monomial(s**2) * X
                + poly.coeff_monomial(s * t) * Y
                + poly.coeff_monomial(t**2) * Z
                + poly.coeff_monomial(1)
            )
        )
    return sp.Matrix(
        [
            [
                equation.coeff(variable)
                for variable in (X, Y, Z, x5, y5)
            ]
            for equation in lifted
        ]
    )


ell = p + q
h = p * ell
P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
R = ell * (-4 * B * p**2 + B * p * q + C * q**2)
alpha, beta, gamma = jac(Q, R), -jac(P, R), jac(P, Q)
print("gcd", sp.factor(sp.gcd(sp.gcd(alpha, beta), gamma)))

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
print(
    "E7 basis",
    [[sp.factor(value) for value in vector] for vector in M7.nullspace()],
)
for rows in itertools.combinations(range(8), 6):
    for cols in itertools.combinations(range(8), 6):
        minor = sp.factor(M7.extract(rows, cols).det())
        if minor:
            print("E7 decisive", rows, cols, minor)
            break
    else:
        continue
    break

tangents = []
for vector in M7.nullspace():
    substitution = dict(zip(unknowns, vector))
    tangents.append(
        (
            sp.factor(uform.subs(substitution)),
            sp.factor(vform.subs(substitution)),
            sp.factor(tform.subs(substitution)),
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
print("polynomial basis", N1, N2)

M = contact_matrix(P, Q, R, N1, N2)
print("contact generic rank", M.rank())
print(
    "contact generic kernel",
    [[sp.factor(value) for value in vector] for vector in M.nullspace()],
)
maximal = []
for omitted in range(6):
    rows = [index for index in range(6) if index != omitted]
    value = sp.factor(M.extract(rows, range(5)).det())
    maximal.append(value)
    print("contact omit", omitted, value)
print("contact maximal gcd", sp.factor(sp.gcd_list(maximal)))
for rank in (5, 4, 3):
    found = False
    for rows in itertools.combinations(range(6), rank):
        for cols in itertools.combinations(range(5), rank):
            minor = sp.factor(M.extract(rows, cols).det())
            if minor:
                print("first rank minor", rank, rows, cols, minor)
                found = True
                break
        if found:
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
print("constant generic rank", Mc.rank())
values = []
for omitted_pair in itertools.combinations(range(7), 2):
    rows = [index for index in range(7) if index not in omitted_pair]
    value = sp.factor(Mc.extract(rows, range(5)).det())
    if value:
        values.append(value)
        print("constant rows", rows, value)
print("constant maximal gcd", sp.factor(sp.gcd_list(values)))


def fresh_case(label, substitutions):
    R_case = sp.expand(R.subs(substitutions))
    alpha_case = jac(Q, R_case)
    beta_case = -jac(P, R_case)
    gcd_case = sp.factor(sp.gcd(sp.gcd(alpha_case, beta_case), gamma))
    M7_case = M7.subs(substitutions)
    basis_case = M7_case.nullspace()
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
    print(label, "gcd", gcd_case, "rank7", M7_case.rank(), "basis", forms)
    if M7_case.rank() == 6:
        found = False
        for rows in itertools.combinations(range(8), 6):
            for cols in itertools.combinations(range(8), 6):
                value = sp.factor(M7_case.extract(rows, cols).det())
                if value:
                    print(label, "E7 decisive", rows, cols, value)
                    found = True
                    break
            if found:
                break
    if len(forms) != 2:
        return
    contact_case = contact_matrix(P, Q, R_case, forms[0], forms[1])
    print(label, "contact rank", contact_case.rank())
    kernel_case = contact_case.nullspace()
    print(
        label,
        "contact kernel",
        [[sp.factor(value) for value in vector] for vector in kernel_case],
    )
    for vector in kernel_case:
        print(
            label,
            "Veronese",
            sp.factor(vector[1] ** 2 - vector[0] * vector[2]),
        )
    rank = contact_case.rank()
    found = False
    for rows in itertools.combinations(range(6), rank):
        for cols in itertools.combinations(range(5), rank):
            value = sp.factor(contact_case.extract(rows, cols).det())
            if value:
                print(label, "contact decisive", rows, cols, value)
                found = True
                break
        if found:
            break


fresh_case("C=0,B=1", {C: 0, B: 1})
fresh_case("C=5B,B=1", {C: 5, B: 1})
fresh_case("B=0,C=1", {B: 0, C: 1})
fresh_case("B=C=1", {B: 1, C: 1})
fresh_case("B=2,C=1", {B: 2, C: 1})
fresh_case("pivot B=-16C", {B: -16, C: 1})
fresh_case("contact 5B=4C", {B: 4, C: 5})
