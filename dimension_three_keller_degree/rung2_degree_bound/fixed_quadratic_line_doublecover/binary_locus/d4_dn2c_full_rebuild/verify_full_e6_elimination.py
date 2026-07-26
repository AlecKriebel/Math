#!/usr/bin/env python3
"""Exact E7 kernel and full-lower E6 atlas for D4-DN-2C.

Fixed binary top data:

    h = (p+q)^2,
    P = h p^2,
    Q = h q^2,
    R = h (p-2q).

The calculation retains every one of the 18 lower coefficients which occurs
in E6.  It derives the projected contact scheme, its geometric radical, and
a four-chart specialization-safe atlas (the two plane interiors, their
punctured intersection line, and the origin).
"""

from __future__ import annotations

import sys

import sympy as sp

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

p, q, r, weight = sp.symbols("p q r weight")
source = (p, q, r)


def jacobian_bracket(f, g):
    """Binary Jacobian bracket in p,q."""
    return sp.expand(
        sp.diff(f, p) * sp.diff(g, q) - sp.diff(f, q) * sp.diff(g, p)
    )


def weighted_determinant(P, Q, R, U, V, T, A, B, linear):
    """det(L+w JH2+w^2 JH3+w^3 JH4)."""
    H2 = sp.Matrix((A, B, T))
    H3 = sp.Matrix((U, V, R))
    H4 = sp.Matrix((P, Q, 0))
    return sp.Poly(
        sp.expand(
            (
                linear
                + weight * H2.jacobian(source)
                + weight**2 * H3.jacobian(source)
                + weight**3 * H4.jacobian(source)
            ).det()
        ),
        weight,
    )


def verify_localized_chart(
    equations,
    variables,
    substitution,
    rows,
    columns,
    expected_pivot,
):
    """Solve on a displayed nonzero pivot and verify every residual exactly."""
    specialized = tuple(sp.expand(item.subs(substitution)) for item in equations)
    matrix, rhs = sp.linear_eq_to_matrix(specialized, variables)
    pivot = sp.factor(
        matrix.extract(rows, columns).det(), extension=sp.sqrt(-2)
    )
    assert sp.expand(pivot - expected_pivot) == 0, (pivot, expected_pivot)

    free_columns = tuple(
        index for index in range(len(variables)) if index not in columns
    )
    pivot_matrix = matrix.extract(rows, columns)
    free_matrix = matrix.extract(rows, free_columns)
    free_vector = sp.Matrix([variables[index] for index in free_columns])
    selected_rhs = rhs.extract(rows, (0,))
    pivot_values = pivot_matrix.inv() * (
        selected_rhs - free_matrix * free_vector
    )
    solved = {
        variables[column]: sp.cancel(pivot_values[index])
        for index, column in enumerate(columns)
    }
    assert all(sp.cancel(item.subs(solved)) == 0 for item in specialized)
    return pivot, solved


# ---------------------------------------------------------------------------
# Fixed top forms and complete E7 kernel
# ---------------------------------------------------------------------------

h = (p + q) ** 2
P = sp.expand(h * p**2)
Q = sp.expand(h * q**2)
R = sp.expand(h * (p - 2 * q))

alpha = jacobian_bracket(Q, R)
beta = -jacobian_bracket(P, R)
gamma = jacobian_bracket(P, Q)
contact_common_factor = sp.gcd(sp.gcd(alpha, beta), gamma)
assert sp.factor(contact_common_factor - 2 * p * (p + q) ** 3) == 0
reduced_alpha = sp.factor(alpha / contact_common_factor)
reduced_beta = sp.factor(beta / contact_common_factor)
reduced_gamma = sp.factor(gamma / contact_common_factor)
assert all(
    sp.expand(actual - expected) == 0
    for actual, expected in zip(
        (reduced_alpha, reduced_beta, reduced_gamma),
        (-3 * q, 3 * (p + 2 * q), 4 * q * (p + q)),
    )
)

# Check the E7 identity directly with a completely generic U,V,T.
ternary3 = (
    p**3,
    p**2 * q,
    p**2 * r,
    p * q**2,
    p * q * r,
    p * r**2,
    q**3,
    q**2 * r,
    q * r**2,
    r**3,
)
ternary2 = (p**2, p * q, p * r, q**2, q * r, r**2)
e7u = sp.symbols("e7u0:10")
e7v = sp.symbols("e7v0:10")
e7t = sp.symbols("e7t0:6")
generic_U = sum(value * monomial for value, monomial in zip(e7u, ternary3))
generic_V = sum(value * monomial for value, monomial in zip(e7v, ternary3))
generic_T = sum(value * monomial for value, monomial in zip(e7t, ternary2))
generic_e7 = weighted_determinant(
    P,
    Q,
    R,
    generic_U,
    generic_V,
    generic_T,
    0,
    0,
    sp.zeros(3),
).coeff_monomial(weight**7)
assert sp.expand(
    generic_e7
    - alpha * sp.diff(generic_U, r)
    - beta * sp.diff(generic_V, r)
    - gamma * sp.diff(generic_T, r)
) == 0

# Split by r-degree after differentiating.  The three blocks have ranks
# 2,3,4 and hence nullities 0,2,4.
u30, v30 = sp.symbols("u30 v30")
block2 = sp.Poly(
    reduced_alpha * u30 + reduced_beta * v30, p, q
)
block2_matrix, _ = sp.linear_eq_to_matrix(block2.coeffs(), (u30, v30))
assert block2_matrix.rank() == 2

u20, u21, v20, v21, t20 = sp.symbols("u20 u21 v20 v21 t20")
raw_U2 = u20 * p + u21 * q
raw_V2 = v20 * p + v21 * q
block1 = sp.Poly(
    reduced_alpha * raw_U2
    + reduced_beta * raw_V2
    + reduced_gamma * t20,
    p,
    q,
)
block1_variables = (u20, u21, v20, v21, t20)
block1_matrix, _ = sp.linear_eq_to_matrix(
    block1.coeffs(), block1_variables
)
assert block1_matrix.rank() == 3

u10, u11, u12, v10, v11, v12, t10, t11 = sp.symbols(
    "u10 u11 u12 v10 v11 v12 t10 t11"
)
raw_U1 = u10 * p**2 + u11 * p * q + u12 * q**2
raw_V1 = v10 * p**2 + v11 * p * q + v12 * q**2
raw_T1 = t10 * p + t11 * q
block0 = sp.Poly(
    reduced_alpha * raw_U1
    + reduced_beta * raw_V1
    + reduced_gamma * raw_T1,
    p,
    q,
)
block0_variables = (u10, u11, u12, v10, v11, v12, t10, t11)
block0_matrix, _ = sp.linear_eq_to_matrix(
    block0.coeffs(), block0_variables
)
assert block0_matrix.rank() == 4

# Six coordinates for the r-dependent kernel.  The eleven binary terms
# U0,V0,T0 are free because their r-derivatives vanish.
d, z, x, y, a, b = sp.symbols("d z x y a b")
U2 = (d + sp.Rational(4, 3) * z) * p + (
    2 * d + sp.Rational(4, 3) * z
) * q
V2 = d * q
T2 = z
U1 = (x + sp.Rational(4, 3) * a) * p**2 + (
    y + 2 * x + sp.Rational(4, 3) * (a + b)
) * p * q + (2 * y + sp.Rational(4, 3) * b) * q**2
V1 = x * p * q + y * q**2
T1 = a * p + b * q
assert sp.expand(
    reduced_alpha * U2 + reduced_beta * V2 + reduced_gamma * T2
) == 0
assert sp.expand(
    reduced_alpha * U1 + reduced_beta * V1 + reduced_gamma * T1
) == 0
assert block1_matrix.nullspace() and len(block1_matrix.nullspace()) == 2
assert block0_matrix.nullspace() and len(block0_matrix.nullspace()) == 4

# ---------------------------------------------------------------------------
# E6 projection with every lower coefficient retained
# ---------------------------------------------------------------------------

binary3 = (p**3, p**2 * q, p * q**2, q**3)
binary2 = (p**2, p * q, q**2)
uc = sp.symbols("uc0:4")
vc = sp.symbols("vc0:4")
tc = sp.symbols("tc0:3")
ac = sp.symbols("ac0:6")
bc = sp.symbols("bc0:6")
ell = sp.symbols("ell0:9")
U0 = sum(value * monomial for value, monomial in zip(uc, binary3))
V0 = sum(value * monomial for value, monomial in zip(vc, binary3))
T0 = sum(value * monomial for value, monomial in zip(tc, binary2))
A = sum(value * monomial for value, monomial in zip(ac, ternary2))
B = sum(value * monomial for value, monomial in zip(bc, ternary2))
linear = sp.Matrix(3, 3, ell)

lower18 = (
    ac[2],
    ac[4],
    ac[5],
    bc[2],
    bc[4],
    bc[5],
    ell[8],
) + uc + vc + tc
assert len(lower18) == 18

full_determinant = weighted_determinant(
    P,
    Q,
    R,
    U0 + r * U1 + r**2 * U2,
    V0 + r * V1 + r**2 * V2,
    T0 + r * T1 + r**2 * T2,
    A,
    B,
    linear,
)
assert all(
    full_determinant.coeff_monomial(weight**degree) == 0
    for degree in (9, 8, 7)
)
full_e6 = sp.Poly(
    full_determinant.coeff_monomial(weight**6), p, q, r
)

# The lower-variable-free r^3 equations force d=z=0 set-theoretically.
expected_r3 = {
    (3, 0, 3): -6 * d**2,
    (2, 1, 3): sp.Rational(16, 3) * z * (3 * d + z),
    (1, 2, 3): sp.Rational(2, 3)
    * (3 * d + 4 * z)
    * (9 * d + 4 * z),
    (0, 3, 3): sp.Rational(4, 3) * (3 * d + 2 * z) ** 2,
}
for monomial, expected in expected_r3.items():
    assert sp.factor(
        full_e6.coeff_monomial(p**monomial[0] * q**monomial[1] * r**3)
        - expected
    ) == 0

e6_dz0 = sp.Poly(full_e6.as_expr().subs({d: 0, z: 0}), p, q, r)
expected_monomials = (
    (6, 0, 0),
    (5, 1, 0),
    (5, 0, 1),
    (4, 2, 0),
    (4, 1, 1),
    (3, 3, 0),
    (3, 2, 1),
    (2, 4, 0),
    (2, 3, 1),
    (1, 5, 0),
    (1, 4, 1),
    (0, 6, 0),
    (0, 5, 1),
)
assert tuple(e6_dz0.monoms()) == expected_monomials

# Only A[r^2]=ac5 and B[r^2]=bc5 occur in the r^1 equations.  Eliminate
# them exactly and identify the projected scheme.
line_equations = tuple(
    e6_dz0.coeff_monomial(p**index * q ** (5 - index) * r)
    for index in range(6)
)
assert (
    set().union(*(item.free_symbols for item in line_equations))
    & set(lower18)
) == {ac[5], bc[5]}
line_groebner = sp.groebner(
    line_equations,
    ac[5],
    bc[5],
    a,
    b,
    x,
    y,
    order="lex",
    domain=sp.QQ,
)
elimination_generators = tuple(
    polynomial.as_expr()
    for polynomial in line_groebner.polys
    if not (
        polynomial.as_expr().free_symbols & {ac[5], bc[5]}
    )
)
contact_linear = 2 * b + 3 * y
contact_quadratic = (
    8 * a**2
    - 16 * a * b
    + 24 * a * x
    - 24 * a * y
    - 24 * b * x
    + 27 * x**2
    - 54 * x * y
    + 9 * y**2
)
actual_elimination_ideal = sp.groebner(
    elimination_generators, a, b, x, y, order="lex", domain=sp.QQ
)
expected_elimination_ideal = sp.groebner(
    (contact_quadratic, contact_linear**2),
    a,
    b,
    x,
    y,
    order="lex",
    domain=sp.QQ,
)
assert actual_elimination_ideal == expected_elimination_ideal

# Its set-theoretic radical is (contact_linear,contact_quadratic).  After
# contact_linear=0 the rank-two quadratic splits into two distinct planes
# over eta=sqrt(-2).
eta = sp.sqrt(-2)
quadratic_on_hyperplane = sp.factor(
    contact_quadratic.subs(b, -sp.Rational(3, 2) * y)
)
expected_quadratic_on_hyperplane = (
    8 * a**2 + 24 * a * x + 27 * x**2 - 18 * x * y + 9 * y**2
)
assert quadratic_on_hyperplane == expected_quadratic_on_hyperplane
plane_plus_equation = (
    9 * x + (4 + 2 * eta) * a + (-3 + 3 * eta) * y
)
plane_minus_equation = (
    9 * x + (4 - 2 * eta) * a + (-3 - 3 * eta) * y
)
assert sp.expand(
    plane_plus_equation * plane_minus_equation
    - 3 * quadratic_on_hyperplane
) == 0
assert sp.expand(plane_plus_equation - plane_minus_equation) != 0

# Form the full 13-by-18 E6 system.  Every displayed lower variable really
# occurs; none is silently specialized.
e6_equations = tuple(e6_dz0.coeffs())
full_matrix, full_rhs = sp.linear_eq_to_matrix(e6_equations, lower18)
assert full_matrix.shape == (13, 18)
assert all(any(full_matrix[:, index]) for index in range(18))

# ---------------------------------------------------------------------------
# Frozen specialization-safe geometric atlas
# ---------------------------------------------------------------------------

k, s = sp.symbols("k s")
plane_plus = {
    a: k,
    b: -sp.Rational(3, 2) * s,
    y: s,
    x: (-(4 + 2 * eta) * k + (3 - 3 * eta) * s) / 9,
}
plane_minus = {
    a: k,
    b: -sp.Rational(3, 2) * s,
    y: s,
    x: (-(4 - 2 * eta) * k + (3 + 3 * eta) * s) / 9,
}
assert sp.expand(contact_linear.subs(plane_plus)) == 0
assert sp.expand(contact_quadratic.subs(plane_plus)) == 0
assert sp.expand(contact_linear.subs(plane_minus)) == 0
assert sp.expand(contact_quadratic.subs(plane_minus)) == 0
assert sp.expand(
    plane_minus_equation.subs(plane_plus)
    + 2 * eta * (2 * k + 3 * s)
) == 0
assert sp.expand(
    plane_plus_equation.subs(plane_minus)
    - 2 * eta * (2 * k + 3 * s)
) == 0

rows7 = (0, 1, 2, 3, 4, 5, 7)
cols7 = (0, 1, 2, 3, 5, 7, 8)
pivot_plus, _ = verify_localized_chart(
    e6_equations,
    lower18,
    plane_plus,
    rows7,
    cols7,
    93312 * (eta - 1) * (2 * k + 3 * s) ** 2,
)
pivot_minus, _ = verify_localized_chart(
    e6_equations,
    lower18,
    plane_minus,
    rows7,
    cols7,
    93312 * (-eta - 1) * (2 * k + 3 * s) ** 2,
)

# The two planes meet on a line.  Recompute there, without specializing a
# plane-interior solve whose pivot has vanished.
intersection_line = {
    a: k,
    b: k,
    x: -sp.Rational(2, 3) * k,
    y: -sp.Rational(2, 3) * k,
}
rows6 = (0, 1, 2, 3, 4, 5)
cols6 = (0, 1, 2, 3, 5, 7)
pivot_intersection, _ = verify_localized_chart(
    e6_equations,
    lower18,
    intersection_line,
    rows6,
    cols6,
    186624 * k,
)

# Finally recompute at the origin.  This constant pivot makes the last chart
# specialization-safe with no hidden denominator.
origin = {a: 0, b: 0, x: 0, y: 0}
rows5 = (0, 1, 2, 3, 4)
cols5 = (0, 1, 2, 3, 5)
pivot_origin, _ = verify_localized_chart(
    e6_equations,
    lower18,
    origin,
    rows5,
    cols5,
    sp.Integer(31104),
)

print(
    "D4_DN2C_E7_KERNEL_PASS_RANKS_2_3_4 "
    "FREE_BINARY_11_CONTACT_6"
)
print(
    "D4_DN2C_CONTACT_RADICAL_PASS_TWO_PLANES_OVER_Q_SQRT_MINUS_2"
)
print(
    "D4_DN2C_FULL_E6_ATLAS_PASS "
    "PLANE_RANK7_INTERSECTION_RANK6_ORIGIN_RANK5 ALL_18_LOWER"
)
