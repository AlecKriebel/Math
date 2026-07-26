#!/usr/bin/env python3
"""Independent hostile reconstruction of the D4-DN-3 E6 contact theorem.

This file deliberately imports no code or data from the primary verifier.  It
rebuilds the weighted determinant from the frozen normal form, derives the
contact radical in an independently chosen syzygy basis, and checks the full
18-lower-variable consistency atlas.
"""

from __future__ import annotations

import sys

import sympy as sp

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)


p, q, r, w = sp.symbols("p q r w")
sqrt2 = sp.sqrt(2)
xyz = (p, q, r)


def jacobian_minor(f: sp.Expr, g: sp.Expr) -> sp.Expr:
    return sp.expand(sp.diff(f, p) * sp.diff(g, q) - sp.diff(f, q) * sp.diff(g, p))


def weighted_jacobian_determinant(
    degree4: tuple[sp.Expr, sp.Expr, sp.Expr],
    degree3: tuple[sp.Expr, sp.Expr, sp.Expr],
    degree2: tuple[sp.Expr, sp.Expr, sp.Expr],
    linear_part: sp.Matrix,
) -> sp.Poly:
    j4 = sp.Matrix(degree4).jacobian(xyz)
    j3 = sp.Matrix(degree3).jacobian(xyz)
    j2 = sp.Matrix(degree2).jacobian(xyz)
    return sp.Poly(sp.expand((linear_part + w * j2 + w**2 * j3 + w**3 * j4).det()), w)


def homogeneous_monomials(total_degree: int) -> tuple[sp.Expr, ...]:
    """SymPy lexicographic order, including monomials with zero coefficient."""
    result: list[sp.Expr] = []
    for p_degree in range(total_degree, -1, -1):
        remaining = total_degree - p_degree
        for q_degree in range(remaining, -1, -1):
            r_degree = remaining - q_degree
            result.append(p**p_degree * q**q_degree * r**r_degree)
    return tuple(result)


def unique_nonzero(expressions: list[sp.Expr]) -> list[sp.Expr]:
    result: list[sp.Expr] = []
    for expression in expressions:
        value = sp.factor(expression)
        if value == 0:
            continue
        if not any(sp.simplify(value - old) == 0 for old in result):
            result.append(value)
    return result


def constant_associate(left: sp.Expr, right: sp.Expr) -> bool:
    ratio = sp.cancel(left / right)
    return ratio != 0 and not ratio.free_symbols


# Frozen degree-four and degree-three normal form.
h = (p + q) ** 2
P = sp.expand(h * p**2)
Q = sp.expand(h * q**2)
R = sp.expand((p + q) ** 3)
alpha = jacobian_minor(Q, R)
beta = -jacobian_minor(P, R)
gamma = jacobian_minor(P, Q)
assert sp.factor(alpha) == -6 * q * (p + q) ** 4
assert sp.factor(beta) == -6 * p * (p + q) ** 4
assert sp.factor(gamma) == 8 * p * q * (p + q) ** 4


# Reconstruct all three r-blocks of the E7 syzygy directly.  Their nullities
# are 0, 2, and 4; no contact parameter is discarded.
u3, v3 = sp.symbols("u3 v3")
block0, _ = sp.linear_eq_to_matrix(
    sp.Poly(alpha * u3 + beta * v3, p, q).coeffs(),
    (u3, v3),
)
assert block0.shape == (6, 2)
assert block0.rank() == 2

u20, u21, v20, v21, t20 = sp.symbols("u20 u21 v20 v21 t20")
block2_variables = (u20, u21, v20, v21, t20)
block2, _ = sp.linear_eq_to_matrix(
    sp.Poly(
        alpha * (u20 * p + u21 * q)
        + beta * (v20 * p + v21 * q)
        + gamma * t20,
        p,
        q,
    ).coeffs(),
    block2_variables,
)
assert block2.rank() == 3
assert len(block2_variables) - block2.rank() == 2

u10, u11, u12, v10, v11, v12, t10, t11 = sp.symbols(
    "u10 u11 u12 v10 v11 v12 t10 t11"
)
block4_variables = (u10, u11, u12, v10, v11, v12, t10, t11)
block4, _ = sp.linear_eq_to_matrix(
    sp.Poly(
        alpha * (u10 * p**2 + u11 * p * q + u12 * q**2)
        + beta * (v10 * p**2 + v11 * p * q + v12 * q**2)
        + gamma * (t10 * p + t11 * q),
        p,
        q,
    ).coeffs(),
    block4_variables,
)
assert block4.rank() == 4
assert len(block4_variables) - block4.rank() == 4


# Independent syzygy coordinates.  The two r^2 basis vectors are
# (-p,q,0), (4p/3,0,1); the four r basis vectors are
# (-p^2,pq,0), (-pq,q^2,0), (4p^2/3,0,p), (4pq/3,0,q).
x0, x1, y0, y1, y2, y3 = sp.symbols("x0 x1 y0 y1 y2 y3")
U2 = sp.expand(-x0 * p + sp.Rational(4, 3) * x1 * p)
V2 = x0 * q
T2 = x1
U1 = sp.expand(
    -y0 * p**2
    - y1 * p * q
    + sp.Rational(4, 3) * y2 * p**2
    + sp.Rational(4, 3) * y3 * p * q
)
V1 = sp.expand(y0 * p * q + y1 * q**2)
T1 = y2 * p + y3 * q
assert sp.expand(alpha * U2 + beta * V2 + gamma * T2) == 0
assert sp.expand(alpha * U1 + beta * V1 + gamma * T1) == 0


# Keep the entire lower layer.  The 18 variables are six nonbinary
# coefficients of A,B; L_33; and all binary coefficients of U0,V0,T0.
binary3 = (p**3, p**2 * q, p * q**2, q**3)
binary2 = (p**2, p * q, q**2)
quadratic3 = (p**2, p * q, p * r, q**2, q * r, r**2)

u = sp.symbols("hu0:4")
v = sp.symbols("hv0:4")
t = sp.symbols("ht0:3")
aa = sp.symbols("ha0:6")
bb = sp.symbols("hb0:6")
ell = sp.symbols("hl0:9")

U0 = sum(coefficient * monomial for coefficient, monomial in zip(u, binary3))
V0 = sum(coefficient * monomial for coefficient, monomial in zip(v, binary3))
T0 = sum(coefficient * monomial for coefficient, monomial in zip(t, binary2))
A = sum(coefficient * monomial for coefficient, monomial in zip(aa, quadratic3))
B = sum(coefficient * monomial for coefficient, monomial in zip(bb, quadratic3))
L = sp.Matrix(3, 3, ell)

lower18 = (
    aa[2],
    aa[4],
    aa[5],
    bb[2],
    bb[4],
    bb[5],
    ell[8],
) + u + v + t
assert len(lower18) == 18
assert len(set(lower18)) == 18

determinant = weighted_jacobian_determinant(
    (P, Q, 0),
    (U0 + r * U1 + r**2 * U2, V0 + r * V1 + r**2 * V2, R),
    (A, B, T0 + r * T1 + r**2 * T2),
    L,
)
assert all(determinant.coeff_monomial(w**degree) == 0 for degree in (9, 8, 7))
E6 = sp.Poly(determinant.coeff_monomial(w**6), p, q, r)
monomials6 = homogeneous_monomials(6)
equations = [E6.coeff_monomial(monomial) for monomial in monomials6]
matrix, rhs = sp.linear_eq_to_matrix(equations, lower18)
assert matrix.shape == (28, 18)
assert rhs.shape == (28, 1)
assert all(any(matrix[row, column] != 0 for row in range(28)) for column in range(18))


# A constant pivot exists before any contact specialization.  Thus the
# subsequent necessary contact equations are obtained without dividing by a
# contact polynomial.
pivot_rows5 = (0, 1, 2, 3, 4)
pivot_columns5 = (0, 1, 2, 3, 5)
constant_pivot = sp.factor(
    matrix[list(pivot_rows5), list(pivot_columns5)].det()
)
assert constant_pivot == 31104

pivot_variables = tuple(lower18[index] for index in pivot_columns5)
pivot_solution_list = sp.solve(
    [equations[index] for index in pivot_rows5],
    pivot_variables,
    dict=True,
    simplify=False,
)
assert len(pivot_solution_list) == 1
pivot_solution = pivot_solution_list[0]
assert set(pivot_solution) == set(pivot_variables)
residuals = unique_nonzero(
    [sp.together(equation.subs(pivot_solution)) for equation in equations]
)

contact_variables = {x0, x1, y0, y1, y2, y3}
pure_contact = [
    residual for residual in residuals if residual.free_symbols <= contact_variables
]
first_x_certificate = sp.Rational(3, 2) * x0**2
second_x_certificate = (
    27 * x0**2 - 24 * x0 * x1 + 8 * x1**2
) / 6
assert any(constant_associate(item, first_x_certificate) for item in pure_contact)
assert any(constant_associate(item, second_x_certificate) for item in pure_contact)


# After the set-theoretically forced x0=x1=0, compute the remaining pure
# contact ideal and certify its radical without a numerical factorization.
y_variables = (y0, y1, y2, y3)
y_set = set(y_variables)
y_residuals = unique_nonzero(
    [
        residual.subs({x0: 0, x1: 0})
        for residual in residuals
        if residual.subs({x0: 0, x1: 0}).free_symbols <= y_set
    ]
)
assert len(y_residuals) == 4

delta = y2 - y3
contact_quadric = 9 * (y0 - y1) ** 2 + 24 * (y0 - y1) * y3 + 8 * y3**2
I_y = sp.groebner(y_residuals, *y_variables, order="grevlex", domain=sp.QQ)
J_y = sp.groebner((delta, contact_quadric), *y_variables, order="grevlex", domain=sp.QQ)
assert all(J_y.reduce(generator)[1] == 0 for generator in y_residuals)
assert I_y.reduce(delta**2)[1] == 0
assert I_y.reduce(contact_quadric**2)[1] == 0

# The lower-variable-free residuals vanish on the proposed radical.  The
# converse set-theoretic implications are furnished by the two x-certificates
# and the preceding y-nilpotence certificates.  Sufficiency (and hence exact
# projection, rather than just necessity) is checked by the atlas below.
candidate_radical = sp.groebner(
    (x0, x1, delta, contact_quadric),
    x0,
    x1,
    y0,
    y1,
    y2,
    y3,
    order="grevlex",
    domain=sp.QQ,
)
assert all(candidate_radical.reduce(residual)[1] == 0 for residual in pure_contact)

zeta = sp.symbols("zeta")
univariate_quadric = 9 * zeta**2 + 24 * zeta + 8
assert sp.degree(sp.gcd(univariate_quadric, sp.diff(univariate_quadric, zeta)), zeta) == 0

c_plus = (-4 + 2 * sqrt2) / 3
c_minus = (-4 - 2 * sqrt2) / 3
assert sp.expand(
    contact_quadric
    - 9
    * ((y0 - y1) - c_plus * y3)
    * ((y0 - y1) - c_minus * y3)
) == 0
assert sp.simplify(c_plus - c_minus) != 0


# Exact full-lower consistency atlas.  Each coefficient matrix and augmented
# matrix is rebuilt from the unspecialized 28-by-18 system.
s, k = sp.symbols("s k")
rows7 = (0, 1, 2, 3, 4, 6, 10)
columns7 = (0, 1, 2, 3, 5, 7, 8)
rows6 = (0, 1, 2, 3, 4, 6)
columns6 = (0, 1, 2, 3, 5, 7)

plane_data: dict[str, tuple[sp.Matrix, sp.Matrix, sp.Expr]] = {}
for label, root, expected_pivot in (
    ("plus", c_plus, 373248 * (7 - 5 * sqrt2) * k**2),
    ("minus", c_minus, 373248 * (7 + 5 * sqrt2) * k**2),
):
    specialization = {
        x0: 0,
        x1: 0,
        y0: s + root * k,
        y1: s,
        y2: k,
        y3: k,
    }
    plane_matrix = matrix.subs(specialization)
    plane_rhs = rhs.subs(specialization)
    safe_pivot = sp.factor(
        plane_matrix[list(rows7), list(columns7)].det(),
        extension=sqrt2,
    )
    assert sp.expand(safe_pivot - expected_pivot) == 0
    assert plane_matrix.rank() == 7
    assert plane_matrix.row_join(plane_rhs).rank() == 7
    plane_data[label] = (plane_matrix, plane_rhs, safe_pivot)


# The Galois-conjugate planes meet along k=0.  Recompute the two boundary
# charts from the original matrix rather than specializing a solved formula.
intersection_specialization = {
    x0: 0,
    x1: 0,
    y0: s,
    y1: s,
    y2: 0,
    y3: 0,
}
intersection_matrix = matrix.subs(intersection_specialization)
intersection_rhs = rhs.subs(intersection_specialization)
intersection_pivot = sp.factor(
    intersection_matrix[list(rows6), list(columns6)].det()
)
assert intersection_pivot == -279936 * s
assert intersection_matrix.rank() == 6
assert intersection_matrix.row_join(intersection_rhs).rank() == 6

origin_matrix = intersection_matrix.subs(s, 0)
origin_rhs = intersection_rhs.subs(s, 0)
origin_pivot = origin_matrix[list(pivot_rows5), list(pivot_columns5)].det()
assert origin_pivot == 31104
assert origin_matrix.rank() == 5
assert origin_matrix.row_join(origin_rhs).rank() == 5


# An earlier formula divided by this expression on the plus plane.  It is not
# a geometric boundary: the safe pivot is independent of s and remains
# nonzero at a concrete point of that line.
old_denominator = s + (-sp.Rational(10, 3) + 2 * sqrt2) * k
old_line_point = {s: sp.Rational(10, 3) - 2 * sqrt2, k: 1}
assert sp.simplify(old_denominator.subs(old_line_point)) == 0
plus_matrix, plus_rhs, plus_safe_pivot = plane_data["plus"]
assert sp.simplify(plus_safe_pivot.subs(old_line_point)) != 0
assert plus_matrix.subs(old_line_point).rank() == 7
assert plus_matrix.subs(old_line_point).row_join(
    plus_rhs.subs(old_line_point)
).rank() == 7


print("D4_DN3_HOSTILE_FULL_E6_CONTACT_ATLAS_PASS")
