#!/usr/bin/env python3
"""Derive E6 data for h=p(p+q), R=p(4Tp^2+3Tpq+Cq^2)."""

from __future__ import annotations

import itertools
import sympy as sp

p, q, r, z = sp.symbols("p q r z")
T, C = sp.symbols("T C")
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
R = p * (4 * T * p**2 + 3 * T * p * q + C * q**2)
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
basis = M7.nullspace()
print("basis", [[sp.factor(value) for value in K] for K in basis])
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
for vector in basis:
    substitution = dict(zip(unknowns, vector))
    tangents.append(
        (
            sp.factor(uform.subs(substitution)),
            sp.factor(vform.subs(substitution)),
            sp.factor(tform.subs(substitution)),
        )
    )
denominators = []
for tangent in tangents:
    for value in tangent:
        _, denominator = sp.fraction(value)
        denominators.append(denominator)
scale = sp.factor(sp.lcm(denominators))
print("basis denominator lcm", scale)
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
print("contact generic rank", M.rank())
print(
    "contact generic kernel",
    [[sp.factor(value) for value in vector] for vector in M.nullspace()],
)
for vector in M.nullspace():
    print(
        "contact Veronese obstruction",
        sp.factor(vector[1] ** 2 - vector[0] * vector[2]),
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
constant_maximal = []
for omitted_pair in itertools.combinations(range(7), 2):
    rows = [index for index in range(7) if index not in omitted_pair]
    value = sp.factor(Mc.extract(rows, range(5)).det())
    if value:
        constant_maximal.append(value)
        print("constant rows", rows, value)
print("constant maximal gcd", sp.factor(sp.gcd_list(constant_maximal)))
contact_specialized = M.subs({C: 7, T: -12})
print(
    "generic-basis contact-divisor kernel",
    [[sp.factor(value) for value in vector]
     for vector in contact_specialized.nullspace()],
)


def fresh_case(label, substitutions):
    P_case = sp.expand(P.subs(substitutions))
    Q_case = sp.expand(Q.subs(substitutions))
    R_case = sp.expand(R.subs(substitutions))
    alpha_case = jac(Q_case, R_case)
    beta_case = -jac(P_case, R_case)
    gamma_case = jac(P_case, Q_case)
    gcd_case = sp.factor(sp.gcd(sp.gcd(alpha_case, beta_case), gamma_case))
    matrix7 = sp.Matrix(
        [
            [equation.coeff(variable) for variable in unknowns]
            for equation in coefficients(
                alpha_case * uform
                + beta_case * vform
                + gamma_case * tform,
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
    print(label, "gcd", gcd_case, "rank7", matrix7.rank(), "basis", forms)
    if matrix7.rank() == 6:
        rank_minor_found = False
        for rows in itertools.combinations(range(8), 6):
            for cols in itertools.combinations(range(8), 6):
                rank_minor = sp.factor(matrix7.extract(rows, cols).det())
                if rank_minor:
                    print(label, "E7 decisive", rows, cols, rank_minor)
                    rank_minor_found = True
                    break
            if rank_minor_found:
                break
    if len(forms) != 2:
        return
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
                + z**3 * sp.Matrix([P_case, Q_case, 0]).jacobian(variables)
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
    print(label, "contact rank", matrix_case.rank())
    print(
        label,
        "contact kernel",
        [[sp.factor(value) for value in vector]
         for vector in matrix_case.nullspace()],
    )
    for vector in matrix_case.nullspace():
        print(
            label,
            "Veronese",
            sp.factor(vector[1] ** 2 - vector[0] * vector[2]),
        )
    decisive_found = False
    for omitted in range(6):
        rows = [index for index in range(6) if index != omitted]
        determinant_case = sp.factor(
            matrix_case.extract(rows, range(5)).det()
        )
        if determinant_case:
            print(label, "contact decisive", rows, determinant_case)
            decisive_found = True
            break
    if not decisive_found:
        for rows in itertools.combinations(range(6), 4):
            for cols in itertools.combinations(range(5), 4):
                determinant_case = sp.factor(
                    matrix_case.extract(rows, cols).det()
                )
                if determinant_case:
                    print(
                        label,
                        "contact rank4 decisive",
                        rows,
                        cols,
                        determinant_case,
                    )
                    decisive_found = True
                    break
            if decisive_found:
                break


fresh_case("C=0,T=1", {C: 0, T: 1})
fresh_case("C=-T,T=1", {C: -1, T: 1})
fresh_case("T=0,C=1", {T: 0, C: 1})
fresh_case("T=C=1", {T: 1, C: 1})
fresh_case("T=2,C=1", {T: 2, C: 1})
fresh_case("pivot 16C=9T", {C: 9, T: 16})
fresh_case("contact 12C=-7T", {C: 7, T: -12})
