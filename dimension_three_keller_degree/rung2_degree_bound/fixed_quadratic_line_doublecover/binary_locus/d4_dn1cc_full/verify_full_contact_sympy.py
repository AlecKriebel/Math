#!/usr/bin/env python3
"""Fail-closed exact verification for the full D4-DN-1CC contact locus.

The top data are

    h=(p+q)^2,
    P=h p^2, Q=h q^2,
    R=(p+q)(2p^2+pq+2q^2).

No ansatz is made for the r-dependent part of (U,V,T).  E7 is solved in
all r-powers.  The contact-only coefficients of E6 then force the full
six-parameter E7 contact space onto one affine line.  Finally, arbitrary
binary cubic/quadratic summands and a general linear part are restored:
the nonzero line chart is inconsistent already in E4, while the zero
boundary loses every nonlinear r-dependent coefficient.
"""

from __future__ import annotations

import itertools
import sys

import sympy as sp

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

p, q, r, weight = sp.symbols("p q r weight")
coords = (p, q, r)


def jac2(f, g):
    return sp.expand(sp.diff(f, p) * sp.diff(g, q) - sp.diff(f, q) * sp.diff(g, p))


def coefficient(poly, exponent):
    return sp.Poly(sp.expand(poly), p, q, r).coeff_monomial(
        p ** exponent[0] * q ** exponent[1] * r ** exponent[2]
    )


h = (p + q) ** 2
P = sp.expand(h * p**2)
Q = sp.expand(h * q**2)
R = sp.expand((p + q) * (2 * p**2 + p * q + 2 * q**2))
alpha = jac2(Q, R)
beta = -jac2(P, R)
gamma = jac2(P, Q)

assert sp.factor(alpha) == -6 * p * q * (p + q) ** 2 * (2 * p + 3 * q)
assert sp.factor(beta) == -6 * p * q * (p + q) ** 2 * (3 * p + 2 * q)
assert sp.factor(gamma) == 8 * p * q * (p + q) ** 4


def homogeneous_rows(poly, degree):
    pp = sp.Poly(sp.expand(poly), p, q)
    return [
        pp.coeff_monomial(p**i * q ** (degree - i))
        for i in range(degree, -1, -1)
    ]


# E7, r^2: the r^3 coefficients of U,V vanish.
u3, v3 = sp.symbols("u3 v3")
matrix3, rhs3 = sp.linear_eq_to_matrix(
    homogeneous_rows(alpha * u3 + beta * v3, 5), (u3, v3)
)
assert matrix3.rank() == 2
assert tuple(next(iter(sp.linsolve((matrix3, rhs3), (u3, v3))))) == (0, 0)

# E7, r^1: all r^2 coefficients, with free parameters d,z.
d, z = sp.symbols("d z")
U2 = (sp.Rational(8, 15) * z - d) * p + (
    sp.Rational(4, 9) * z - sp.Rational(2, 3) * d
) * q
V2 = (sp.Rational(4, 45) * z + sp.Rational(2, 3) * d) * p + d * q
T2 = z
u20, u21, v20, v21, t2 = sp.symbols("u20 u21 v20 v21 t2")
matrix2, rhs2 = sp.linear_eq_to_matrix(
    homogeneous_rows(
        alpha * (u20 * p + u21 * q)
        + beta * (v20 * p + v21 * q)
        + gamma * t2,
        6,
    ),
    (u20, u21, v20, v21, t2),
)
assert matrix2.rank() == 3
assert all(
    sp.expand(value) == 0
    for value in homogeneous_rows(alpha * U2 + beta * V2 + gamma * T2, 6)
)

# E7, r^0: all r-linear coefficients, with free parameters x,y,a,b.
x, y, a, b = sp.symbols("x y a b")
U1 = (
    sp.Rational(1, 45) * (24 * a + 4 * b - 45 * x + 30 * y) * p**2
    + sp.Rational(1, 27) * (12 * a + 16 * b - 18 * x - 15 * y) * p * q
    + sp.Rational(2, 9) * (2 * b - 3 * y) * q**2
)
V1 = (
    sp.Rational(2, 135) * (6 * a - 4 * b + 45 * x - 30 * y) * p**2
    + x * p * q
    + y * q**2
)
T1 = a * p + b * q
u10, u11, u12, v10, v11, v12, t10, t11 = sp.symbols(
    "u10 u11 u12 v10 v11 v12 t10 t11"
)
matrix1, rhs1 = sp.linear_eq_to_matrix(
    homogeneous_rows(
        alpha * (u10 * p**2 + u11 * p * q + u12 * q**2)
        + beta * (v10 * p**2 + v11 * p * q + v12 * q**2)
        + gamma * (t10 * p + t11 * q),
        7,
    ),
    (u10, u11, u12, v10, v11, v12, t10, t11),
)
assert matrix1.rank() == 4
assert all(
    sp.expand(value) == 0
    for value in homogeneous_rows(alpha * U1 + beta * V1 + gamma * T1, 7)
)

# The preceding three independent blocks give the complete E7 contact
# dimension 0+2+4=6.
assert (2 - matrix3.rank()) + (5 - matrix2.rank()) + (8 - matrix1.rank()) == 6


def weighted_determinant(U, V, T, A, B, linear):
    H2 = sp.Matrix([A, B, T])
    H3 = sp.Matrix([U, V, R])
    H4 = sp.Matrix([P, Q, 0])
    return sp.Poly(
        sp.expand(
            (
                linear
                + weight * H2.jacobian(coords)
                + weight**2 * H3.jacobian(coords)
                + weight**3 * H4.jacobian(coords)
            ).det()
        ),
        weight,
    )


# Contact-only E6.  The two extreme r^3 coefficients already force d=z=0.
contact_det = weighted_determinant(
    r * U1 + r**2 * U2,
    r * V1 + r**2 * V2,
    r * T1 + r**2 * T2,
    0,
    0,
    sp.zeros(3),
)
assert contact_det.coeff_monomial(weight**7) == 0
contact_e6 = contact_det.coeff_monomial(weight**6)
expected_r3 = {
    (0, 3, 3): sp.Rational(20, 27) * (3 * d - 2 * z) ** 2,
    (1, 2, 3): sp.Rational(2, 3) * (15 * d**2 - 16 * d * z + 8 * z**2),
    (2, 1, 3): sp.Rational(2, 45) * (225 * d**2 + 56 * z**2),
    (3, 0, 3): sp.Rational(4, 135) * (15 * d + 2 * z) ** 2,
}
for exponent, expected in expected_r3.items():
    assert sp.factor(coefficient(contact_e6, exponent) - expected) == 0
assert sp.solve(
    (3 * d - 2 * z, 15 * d + 2 * z), (d, z), dict=True
) == [{d: 0, z: 0}]

# Once d=z=0, E6 at r-degree one contains only the two r^2
# coefficients ar,br of A,B in addition to the contact parameters.
ar, br = sp.symbols("ar br")
line_test_det = weighted_determinant(
    r * U1,
    r * V1,
    r * T1,
    ar * r**2,
    br * r**2,
    sp.zeros(3),
)
line_e6 = sp.Poly(line_test_det.coeff_monomial(weight**6), p, q, r)
line_equations = [
    line_e6.coeff_monomial(p**i * q ** (5 - i) * r) for i in range(6)
]
assert sp.factor(line_equations[0] - sp.Rational(10, 27) * (-2 * b + 3 * y) ** 2) == 0
assert sp.factor(
    line_equations[5]
    - sp.Rational(2, 1215) * (6 * a - 4 * b + 45 * x - 30 * y) ** 2
) == 0

# On the two extreme equations, b=3y/2 and a=(12y-15x)/2.  Any three
# of the four remaining equations have the same augmented determinant.
extreme_substitution = {
    b: sp.Rational(3, 2) * y,
    a: (12 * y - 15 * x) / 2,
}
middle = [sp.factor(value.subs(extreme_substitution)) for value in line_equations[1:5]]
middle_matrix, middle_rhs = sp.linear_eq_to_matrix(middle, (ar, br))
assert middle_matrix.rank() == 2
for rows in itertools.combinations(range(4), 3):
    augmented_minor = sp.factor(
        middle_matrix.row_join(middle_rhs)[list(rows), :].det()
    )
    assert augmented_minor == 32400 * (x - y) ** 2

# Thus x=y, and the extreme equations give the unique affine line.  The
# converse is checked directly, including the forced r^2 terms in A,B.
k = sp.symbols("k")
contact_line = {
    d: 0,
    z: 0,
    a: -k,
    b: k,
    x: sp.Rational(2, 3) * k,
    y: sp.Rational(2, 3) * k,
}
assert sp.factor(U1.subs(contact_line) + sp.Rational(2, 3) * k * p * (p + q)) == 0
assert sp.factor(V1.subs(contact_line) - sp.Rational(2, 3) * k * q * (p + q)) == 0
assert sp.factor(T1.subs(contact_line) - k * (-p + q)) == 0
assert all(
    sp.factor(value.subs(contact_line).subs({ar: k**2 / 45, br: k**2 / 45})) == 0
    for value in line_equations
)

# Restore every binary cubic/quadratic coefficient and all nine entries of
# the linear part.  This is the lower-chart calculation, not a sparse ansatz.
mon3_binary = (p**3, p**2 * q, p * q**2, q**3)
mon2_binary = (p**2, p * q, q**2)
mon2 = (p**2, p * q, p * r, q**2, q * r, r**2)
uc = sp.symbols("uc0:4")
vc = sp.symbols("vc0:4")
tc = sp.symbols("tc0:3")
ac = sp.symbols("ac0:6")
bc = sp.symbols("bc0:6")
ell = sp.symbols("ell0:9")
U0 = sum(value * monomial for value, monomial in zip(uc, mon3_binary))
V0 = sum(value * monomial for value, monomial in zip(vc, mon3_binary))
T0 = sum(value * monomial for value, monomial in zip(tc, mon2_binary))
Afull = sum(value * monomial for value, monomial in zip(ac, mon2))
Bfull = sum(value * monomial for value, monomial in zip(bc, mon2))
L = sp.Matrix(3, 3, ell)


def solve_e6(k_value):
    Uline = U0 - sp.Rational(2, 3) * k_value * p * (p + q) * r
    Vline = V0 + sp.Rational(2, 3) * k_value * q * (p + q) * r
    Tline = T0 + k_value * (-p + q) * r
    determinant = weighted_determinant(Uline, Vline, Tline, Afull, Bfull, L)
    assert all(
        determinant.coeff_monomial(weight**degree) == 0 for degree in (9, 8, 7)
    )
    e6 = sp.Poly(determinant.coeff_monomial(weight**6), p, q, r)
    equations = e6.coeffs()
    variables = (
        ac[2],
        ac[4],
        ac[5],
        bc[2],
        bc[4],
        bc[5],
        ell[8],
    ) + uc + vc + tc
    matrix, rhs = sp.linear_eq_to_matrix(equations, variables)
    assert matrix.rank() == matrix.row_join(rhs).rank()
    solution = tuple(next(iter(sp.linsolve((matrix, rhs), variables))))
    substitution = dict(zip(variables, solution))
    assert all(sp.factor(value.subs(substitution)) == 0 for value in equations)
    return determinant, variables, matrix, substitution


# Nonzero pivot chart.  Work over Q(k), so every denominator involving k
# is legal only on this chart.  E4 is inconsistent before E5 is even needed.
nonzero_det, _, nonzero_matrix, nonzero_substitution = solve_e6(k)
assert nonzero_matrix.rank() == 6
nonzero_e4 = sp.Poly(
    sp.expand(
        nonzero_det.coeff_monomial(weight**4).subs(nonzero_substitution)
    ),
    p,
    q,
    r,
)
for monomial in (p * r**3, q * r**3):
    assert sp.factor(
        nonzero_e4.coeff_monomial(monomial)
        - sp.Rational(16, 135) * k**4
    ) == 0

# Pivot boundary k=0.  It is recomputed from scratch (no substitution into
# a formula containing 1/k).  E4 forces b_qr=L_33=0 and hence all six
# r-dependent nonlinear quadratic coefficients to vanish.
zero_det, _, zero_matrix, zero_substitution = solve_e6(sp.S.Zero)
assert zero_matrix.rank() == 5
zero_e4 = sp.Poly(
    sp.expand(zero_det.coeff_monomial(weight**4).subs(zero_substitution)),
    p,
    q,
    r,
)
assert sp.factor(
    zero_e4.coeff_monomial(p**3 * r)
    - sp.Rational(2, 135) * (15 * bc[4] + 2 * ell[8]) ** 2
) == 0
assert sp.factor(
    zero_e4.coeff_monomial(q**3 * r)
    - sp.Rational(10, 27) * (3 * bc[4] - 2 * ell[8]) ** 2
) == 0
boundary_zero = {bc[4]: 0, ell[8]: 0}
for variable in (ac[2], ac[4], ac[5], bc[2], bc[4], bc[5]):
    assert sp.factor(zero_substitution[variable].subs(boundary_zero)) == 0

print("D4_DN1CC_FULL_CONTACT_STRICT_PASS_ONE_LINE")
