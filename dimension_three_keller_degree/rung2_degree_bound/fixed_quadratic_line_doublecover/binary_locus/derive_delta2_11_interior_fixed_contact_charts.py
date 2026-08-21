#!/usr/bin/env python3
"""Fresh internal charts for the squarefree fixed-root/contact leaf."""

from __future__ import annotations

import itertools
import sympy as sp

p, q, r, z = sp.symbols("p q r z")
w = sp.symbols("w")
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
H4 = sp.Matrix([P, Q, 0])
uu = sp.symbols("u0:3")
vv = sp.symbols("v0:3")
tt = sp.symbols("t0:2")
uform = uu[0] * p**2 + uu[1] * p * q + uu[2] * q**2
vform = vv[0] * p**2 + vv[1] * p * q + vv[2] * q**2
tform = tt[0] * p + tt[1] * q
unknowns = (*uu, *vv, *tt)


def analyze(label, A_case, T_case):
    R = sp.expand(
        L
        * (
            A_case * p**2
            + (1 - 3 * w**2) * T_case * p * q
            + 4 * w * T_case * q**2
        )
    )
    alpha, beta, gamma = jac(Q, R), -jac(P, R), jac(P, Q)
    M7 = sp.Matrix(
        [
            [equation.coeff(variable) for variable in unknowns]
            for equation in coefficients(
                alpha * uform + beta * vform + gamma * tform, 7
            )
        ]
    )
    basis = M7.nullspace()
    print(label, "gcd", sp.factor(sp.gcd(sp.gcd(alpha, beta), gamma)))
    print(label, "E7 rank", M7.rank())
    print(
        label,
        "E7 basis",
        [[sp.factor(value) for value in vector] for vector in basis],
    )
    for rows in itertools.combinations(range(8), 6):
        for cols in itertools.combinations(range(8), 6):
            value = sp.factor(M7.extract(rows, cols).det())
            if value:
                print(label, "E7 decisive", rows, cols, value)
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
    N1 = tuple(sp.factor(scale * value) for value in tangents[0])
    N2 = tuple(sp.factor(scale * value) for value in tangents[1])
    print(label, "basis scale", scale)
    print(label, "N1", N1)
    print(label, "N2", N2)
    N = tuple(
        sp.expand(c1 * N1[index] + c2 * N2[index])
        for index in range(3)
    )
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
    e6r = sp.Poly(
        sp.expand(weighted.coeff_monomial(z**6)), r
    ).coeff_monomial(r)
    lifted = []
    for equation in coefficients(e6r, 5):
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
    print(label, "contact rank", contact.rank())
    found = False
    for rows in itertools.combinations(range(6), 5):
        value = sp.factor(contact.extract(rows, range(5)).det())
        if value:
            print(label, "contact decisive", rows, value)
            found = True
            break
    if not found:
        for rows in itertools.combinations(range(6), 4):
            for cols in itertools.combinations(range(5), 4):
                value = sp.factor(contact.extract(rows, cols).det())
                if value:
                    print(label, "contact rank4 decisive", rows, cols, value)
                    found = True
                    break
            if found:
                break
        kernel = contact.nullspace()
        print(
            label,
            "contact kernel",
            [[sp.factor(value) for value in vector] for vector in kernel],
        )
        for vector in kernel:
            print(
                label,
                "Veronese",
                sp.factor(vector[1] ** 2 - vector[0] * vector[2]),
            )


S = 9 * w**4 - 6 * w**2 + 1
K = 7 * w**6 + 9 * w**4 - 3 * w**2 - 5
analyze("D=0", S, 16 * w)
analyze("H=0", -K, 4 * w * (3 * w**2 - 1))
