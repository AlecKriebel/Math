#!/usr/bin/env python3
"""Derive E6 contact ranks for h=p^2 with the q-branch contact."""

from __future__ import annotations

import itertools
import sympy as sp

p, q, r, z = sp.symbols("p q r z")
A, C, D = sp.symbols("A C D")
s, t, x5, y5 = sp.symbols("s t x5 y5")
X, Y, Z = sp.symbols("X Y Z")
variables = (p, q, r)


def coefficients(value, degree):
    poly = sp.Poly(sp.expand(value), p, q)
    return [
        poly.coeff_monomial(p ** (degree - index) * q**index)
        for index in range(degree + 1)
    ]


def contact_matrix(P, Q, R, N1, N2):
    N = tuple(
        sp.expand(s * N1[index] + t * N2[index])
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


P, Q = p**4, p**2 * q**2
R = A * p**3 + C * p * q**2 + D * q**3
Lambda = 27 * A * D**2 + 4 * C**3
N1 = (
    36 * D**2 * p**2,
    4 * C**2 * p**2 - 6 * C * D * p * q + 18 * D**2 * q**2,
    Lambda * p,
)
N2 = (
    -24 * C * D * p**2,
    18 * A * D * p**2 + 4 * C**2 * p * q - 12 * C * D * q**2,
    Lambda * q,
)
M = contact_matrix(P, Q, R, N1, N2)
print("generic rank", M.rank())
maximal = []
for omitted in range(6):
    rows = [index for index in range(6) if index != omitted]
    maximal.append(sp.factor(M.extract(rows, range(5)).det()))
print("maximal gcd", sp.factor(sp.gcd_list(maximal)))
for omitted, value in enumerate(maximal):
    print("omit", omitted, sp.factor(value))

# Fresh E7 basis at Lambda=0.  Normalize D=1 using the available
# diagonal/source and third-target scalings, then A=-4*C^3/27.
A_special = -4 * C**3 / 27
R_special = sp.expand(R.subs({A: A_special, D: 1}))
alpha = (
    sp.diff(Q, p) * sp.diff(R_special, q)
    - sp.diff(Q, q) * sp.diff(R_special, p)
)
beta = -(
    sp.diff(P, p) * sp.diff(R_special, q)
    - sp.diff(P, q) * sp.diff(R_special, p)
)
gamma = sp.diff(P, p) * sp.diff(Q, q) - sp.diff(P, q) * sp.diff(Q, p)
uu = sp.symbols("u0:3")
vv = sp.symbols("v0:3")
tt = sp.symbols("t0:2")
uform = uu[0] * p**2 + uu[1] * p * q + uu[2] * q**2
vform = vv[0] * p**2 + vv[1] * p * q + vv[2] * q**2
tform = tt[0] * p + tt[1] * q
unknowns = (*uu, *vv, *tt)
eq7 = coefficients(alpha * uform + beta * vform + gamma * tform, 7)
M7 = sp.Matrix(
    [[sp.expand(equation).coeff(variable) for variable in unknowns]
     for equation in eq7]
)
print("Lambda=0 E7 rank", M7.rank())
kernel7 = M7.nullspace()
print(
    "Lambda=0 tangent vectors",
    [[sp.factor(value) for value in vector] for vector in kernel7],
)
if len(kernel7) == 2:
    tangents = []
    for vector in kernel7:
        substitution = dict(zip(unknowns, vector))
        tangents.append(
            (
                sp.factor(uform.subs(substitution)),
                sp.factor(vform.subs(substitution)),
                sp.factor(tform.subs(substitution)),
            )
        )
    M_special = contact_matrix(P, Q, R_special, *tangents)
    print("Lambda=0 contact rank", M_special.rank())
    maximal_special = []
    for omitted in range(6):
        rows = [index for index in range(6) if index != omitted]
        maximal_special.append(
            sp.factor(M_special.extract(rows, range(5)).det())
        )
    print("Lambda=0 maximal gcd", sp.factor(sp.gcd_list(maximal_special)))
    for omitted, value in enumerate(maximal_special):
        print("Lambda=0 omit", omitted, value)


def fresh_contact(label, R_case, substitutions=()):
    alpha_case = (
        sp.diff(Q, p) * sp.diff(R_case, q)
        - sp.diff(Q, q) * sp.diff(R_case, p)
    )
    beta_case = -(
        sp.diff(P, p) * sp.diff(R_case, q)
        - sp.diff(P, q) * sp.diff(R_case, p)
    )
    gamma_case = (
        sp.diff(P, p) * sp.diff(Q, q)
        - sp.diff(P, q) * sp.diff(Q, p)
    )
    eq7_case = coefficients(
        alpha_case * uform + beta_case * vform + gamma_case * tform,
        7,
    )
    matrix7 = sp.Matrix(
        [
            [
                sp.expand(equation).coeff(variable)
                for variable in unknowns
            ]
            for equation in eq7_case
        ]
    )
    print(label, "E7 rank", matrix7.rank())
    basis = matrix7.nullspace()
    print(
        label,
        "tangent vectors",
        [[sp.factor(value) for value in vector] for vector in basis],
    )
    tangent_forms = []
    for vector in basis:
        substitution = dict(zip(unknowns, vector))
        tangent_forms.append(
            (
                sp.factor(uform.subs(substitution)),
                sp.factor(vform.subs(substitution)),
                sp.factor(tform.subs(substitution)),
            )
        )
    matrix_contact = contact_matrix(P, Q, R_case, *tangent_forms)
    print(label, "contact rank", matrix_contact.rank())
    contact_kernel = matrix_contact.nullspace()
    print(
        label,
        "contact kernel",
        [
            [sp.factor(value) for value in vector]
            for vector in contact_kernel
        ],
    )
    if len(contact_kernel) == 1:
        vector = contact_kernel[0]
        print(
            label,
            "obstruction",
            sp.factor(vector[1] ** 2 - vector[0] * vector[2]),
        )
    elif len(contact_kernel) == 2:
        lam, mu = sp.symbols("lam mu")
        vector = lam * contact_kernel[0] + mu * contact_kernel[1]
        print(
            label,
            "kernel-conic",
            sp.factor(vector[1] ** 2 - vector[0] * vector[2]),
        )
    rank = matrix_contact.rank()
    for rows in itertools.combinations(range(6), rank):
        found = False
        for columns in itertools.combinations(range(5), rank):
            minor = sp.factor(
                matrix_contact.extract(rows, columns).det()
            )
            if minor:
                print(label, "decisive", rows, columns, minor)
                found = True
                break
        if found:
            break
    maximal_case = []
    for omitted in range(6):
        rows = [index for index in range(6) if index != omitted]
        maximal_case.append(
            sp.factor(matrix_contact.extract(rows, range(5)).det())
        )
    print(label, "maximal gcd", sp.factor(sp.gcd_list(maximal_case)))
    print(label, "maximal", maximal_case)


fresh_contact("C=0,A generic,D=1", A * p**3 + q**3)
fresh_contact("C=0,A=0,D=1", q**3)
fresh_contact("C=0,A,D generic", A * p**3 + D * q**3)
fresh_contact("C=0,A=0,D generic", D * q**3)

# General-D replay of Lambda=0, avoiding normalization in the final
# certificate.
A_lambda_general = -4 * C**3 / (27 * D**2)
fresh_contact(
    "Lambda=0 general D",
    sp.expand(R.subs(A, A_lambda_general)),
)
