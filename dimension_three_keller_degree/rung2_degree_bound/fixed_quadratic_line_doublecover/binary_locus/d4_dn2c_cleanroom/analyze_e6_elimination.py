#!/usr/bin/env python3
"""Determinantal elimination and rank-stratum analysis for D4-DN-2C E6.

This script starts from the exact coefficient matrix constructed in
``derive_e6_projection.py``.  It treats consistency as a rank equality;
no denominator is divided out without recording its boundary.
"""

from __future__ import annotations

import itertools
import sys

import sympy as sp

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

import derive_e6_projection as base

a, b, c, d, e, f = base.a, base.b, base.c, base.d, base.e, base.f
contact = (c, d, e, f)
boundary = {a: 0, b: 0}
matrix = base.matrix.subs(boundary)
constant = base.constant.subs(boundary)


def unique_primitive(polynomials: list[sp.Expr]) -> tuple[sp.Expr, ...]:
    """Normalize nonzero polynomials over QQ up to multiplication by units."""
    normalized: dict[str, sp.Expr] = {}
    for polynomial in polynomials:
        value = sp.Poly(sp.expand(polynomial), *contact, domain=sp.QQ)
        if value.is_zero:
            continue
        _, primitive = value.primitive()
        expression = primitive.as_expr()
        leading = sp.Poly(expression, *contact).LC()
        if leading < 0:
            expression = -expression
        normalized[sp.srepr(expression)] = sp.factor(expression)
    return tuple(normalized.values())


rows1 = [
    index for index, exponent in enumerate(base.EXPONENTS) if exponent[2] == 1
]
columns1 = [base.LOWER.index(base.ar[2]), base.LOWER.index(base.br[2])]
A1 = matrix[rows1, columns1]
b1 = -constant[rows1, :]
Aug1 = A1.row_join(b1)

assert A1.rank() == 2
nonzero_2minor = next(
    sp.factor(A1.extract(rows, (0, 1)).det())
    for rows in itertools.combinations(range(6), 2)
    if A1.extract(rows, (0, 1)).det() != 0
)
assert nonzero_2minor.is_number and nonzero_2minor != 0
r1_pivot_rows = next(
    rows
    for rows in itertools.combinations(range(6), 2)
    if sp.factor(A1.extract(rows, (0, 1)).det()) == nonzero_2minor
)

minors1 = unique_primitive(
    [
        Aug1.extract(rows, (0, 1, 2)).det()
        for rows in itertools.combinations(range(6), 3)
    ]
)
print("R1 constant rank-2 pivot:", nonzero_2minor)
print("R1 nonzero normalized augmented minors:", len(minors1))
for value in minors1:
    print("  ", sp.factor(value))

groebner1 = sp.groebner(minors1, c, d, e, f, order="grevlex")
print("R1 Groebner basis:")
for value in groebner1.polys:
    print("  ", sp.factor(value.as_expr()))

with open("E6_R1_IDEAL.txt", "w", encoding="utf-8") as stream:
    stream.write("constant_rank 2\n")
    stream.write("constant_pivot " + str(nonzero_2minor) + "\n")
    stream.write("augmented_minors\n")
    for value in minors1:
        stream.write(str(sp.factor(value)) + "\n")
    stream.write("groebner_grevlex\n")
    for value in groebner1.polys:
        stream.write(str(sp.factor(value.as_expr())) + "\n")

# The radical over C is the union of two planes.  Work over
# K=QQ(sqrt(-2)); Galois conjugation exchanges them.
s = sp.sqrt(-2)
H = sp.factor(
    (
        3 * c**2
        + 8 * c * e
        + 4 * c * f
        + 8 * e**2
        + 4 * f**2
    )
)
assert sp.factor(groebner1.polys[1].as_expr()) == (d + 2 * f) ** 2
assert sp.factor(
    groebner1.polys[0].as_expr().subs(d, -2 * f) - H
) == 0
Lplus = 3 * c + (4 + 2 * s) * e + (2 - 2 * s) * f
Lminus = 3 * c + (4 - 2 * s) * e + (2 + 2 * s) * f
assert sp.expand(Lplus * Lminus - 3 * H) == 0
plane_plus = {
    d: -2 * f,
    c: -sp.Rational(1, 3) * ((4 + 2 * s) * e + (2 - 2 * s) * f),
}

# r^0 quotient.  First remove the fixed three-dimensional image of the
# A_r,B_r,ell33 columns by a constant left-nullspace matrix N.
rows0 = [
    index for index, exponent in enumerate(base.EXPONENTS) if exponent[2] == 0
]
A0 = matrix[rows0, :]
b0 = -constant[rows0, :]
fixed_variables = (base.ar[0], base.ar[1], base.br[0], base.br[1], base.ell33)
fixed_columns = [base.LOWER.index(value) for value in fixed_variables]
W = A0[:, fixed_columns]
assert W.rank() == 3
w_pivot = next(
    (rows, columns, sp.factor(W.extract(rows, columns).det()))
    for rows in itertools.combinations(range(7), 3)
    for columns in itertools.combinations(range(5), 3)
    if W.extract(rows, columns).det() != 0
)
left_kernel = W.T.nullspace()
assert len(left_kernel) == 4
N = sp.Matrix.vstack(*(vector.T for vector in left_kernel))
assert N.shape == (4, 7)
assert N * W == sp.zeros(4, 5)
assert N.rank() == 4

binary_variables = base.uc + base.vc + base.tc
binary_columns = [base.LOWER.index(value) for value in binary_variables]
B = sp.simplify(N * A0[:, binary_columns])
y = sp.simplify(N * b0)
assert B.shape == (4, 11)
assert y.shape == (4, 1)
assert B.rank() == 3

Bplus = sp.simplify(B.subs(plane_plus))
yplus = sp.simplify(y.subs(plane_plus))
print("R0 quotient matrix shape/rank on plus plane:", Bplus.shape, Bplus.rank())
assert Bplus.rank() in (2, 3)
A0plus = sp.simplify(A0.subs(plane_plus))
b0plus = sp.simplify(b0.subs(plane_plus))
assert A0plus.rank() == 5
assert A0plus.row_join(b0plus).rank() == 5
assert A1.row_join(b1.subs(plane_plus)).rank() == 2

# The gcd of all nonzero maximal minors detects any common rank-drop divisor.
quotient_rank = Bplus.rank()
maximal_minors_raw: list[sp.Expr] = []
for row_choice in itertools.combinations(range(4), quotient_rank):
    for column_choice in itertools.combinations(range(11), quotient_rank):
        value = sp.Poly(
            sp.expand(Bplus.extract(row_choice, column_choice).det()),
            e,
            f,
            extension=s,
        )
        if not value.is_zero:
            maximal_minors_raw.append(value.as_expr())

# Compress the many minors to a vector-space basis before ideal operations.
maximal_monomials = tuple(
    e ** (quotient_rank - index) * f**index
    for index in range(quotient_rank + 1)
)
maximal_coefficients = sp.Matrix(
    [
        [
            sp.Poly(value, e, f, extension=s).coeff_monomial(monomial)
            for monomial in maximal_monomials
        ]
        for value in maximal_minors_raw
    ]
)
maximal_rref, maximal_pivots = maximal_coefficients.T.rref()
maximal_basis_indices = maximal_pivots
maximal_minors = [
    maximal_minors_raw[index] for index in maximal_basis_indices
]
gcd_poly = sp.Poly(maximal_minors[0], e, f, extension=s)
for value in maximal_minors[1:]:
    gcd_poly = gcd_poly.gcd(sp.Poly(value, e, f, extension=s))
gcd_maximal = gcd_poly.monic().as_expr()
print("R0 quotient nonzero maximal minors:", len(maximal_minors_raw))
print("R0 quotient maximal-minor span rank:", maximal_coefficients.rank())
print("R0 quotient gcd of maximal minors:", gcd_maximal)
plus_pivot = next(
    (
        rows,
        columns,
        sp.Poly(
            sp.expand(Bplus.extract(rows, columns).det()),
            e,
            f,
            extension=s,
        ).as_expr(),
    )
    for rows in itertools.combinations(range(4), 2)
    for columns in itertools.combinations(range(11), 2)
    if Bplus.extract(rows, columns).det() != 0
)
plus_pivot_expected = 108 * (s - 1) * (e - f) ** 2
assert sp.expand(plus_pivot[2] - plus_pivot_expected) == 0
assert sp.rem(
    sp.Poly(plus_pivot[2], e, f, extension=s),
    sp.Poly((e - f) ** 2, e, f, extension=s),
).is_zero

# Exact ideal of all maximal minors in K[e,f].  A Groebner basis provides
# the radical-support certificate for the rank-drop boundary.
groebner_rankdrop = sp.groebner(
    maximal_minors, e, f, extension=s, order="grevlex"
)
print("R0 rank-drop Groebner basis:")
for value in groebner_rankdrop.polys:
    print("  ", sp.factor(value.as_expr(), extension=s))

# Generic consistency equations are the (rank+1)-minors of [B|y] containing
# the last column.  Their ideal is then reduced modulo the plane equations.
Aug0plus = Bplus.row_join(yplus)
compat_raw = [
    Aug0plus.extract(rows, columns + (11,)).det()
    for rows in itertools.combinations(range(4), quotient_rank + 1)
    for columns in itertools.combinations(range(11), quotient_rank)
]
compatibility: list[sp.Expr] = []
for value in compat_raw:
    polynomial = sp.Poly(sp.expand(value), e, f, extension=s)
    if polynomial.is_zero:
        continue
    compatibility.append(polynomial.as_expr())
compatibility_degree = quotient_rank + 2
compatibility_monomials = tuple(
    e ** (compatibility_degree - index) * f**index
    for index in range(compatibility_degree + 1)
)
compatibility_coefficients = sp.Matrix(
    [
        [
            sp.Poly(value, e, f, extension=s).coeff_monomial(monomial)
            for monomial in compatibility_monomials
        ]
        for value in compatibility
    ]
)
_, compatibility_pivots = compatibility_coefficients.T.rref()
compatibility = [compatibility[index] for index in compatibility_pivots]
print("R0 nonzero normalized generic compatibility minors:", len(compatibility))
for value in compatibility:
    print("  ", value)
if compatibility:
    groebner_compat = sp.groebner(
        compatibility, e, f, extension=s, order="grevlex"
    )
    print("R0 generic compatibility Groebner basis:")
    for value in groebner_compat.polys:
        print("  ", sp.factor(value.as_expr(), extension=s))
else:
    assert all(
        sp.Poly(sp.expand(value), e, f, extension=s).is_zero
        for value in compat_raw
    )

# Boundary of both conjugate planes: e=f=k, hence c=d=-2k.
# The quotient rank falls to one for k != 0, and a 2x2 augmented minor
# is a nonzero scalar times k^3.  Thus only the origin survives.
k = sp.symbols("k")
line_substitution = {e: k, f: k}
Bline = sp.simplify(Bplus.subs(line_substitution))
yline = sp.simplify(yplus.subs(line_substitution))
assert Bline.rank() == 1
A0line = sp.simplify(A0plus.subs(line_substitution))
b0line = sp.simplify(b0plus.subs(line_substitution))
assert A0line.rank() == 4
assert A0line.row_join(b0line).rank() == 4
line_pivot = next(
    (row, column, sp.factor(Bline[row, column]))
    for row in range(4)
    for column in range(11)
    if Bline[row, column] != 0
)
Augline = Bline.row_join(yline)
line_augmented_minors = [
    sp.factor(Augline.extract(rows, (column, 11)).det())
    for rows in itertools.combinations(range(4), 2)
    for column in range(11)
]
assert all(value == 0 for value in line_augmented_minors)
assert Bline.subs(k, 0) == sp.zeros(4, 11)
assert yline.subs(k, 0) == sp.zeros(4, 1)
assert A0line.subs(k, 0).rank() == 3
assert A0line.subs(k, 0).row_join(b0line.subs(k, 0)).rank() == 3

print(
    "R1 pivot rows/exponents/value:",
    r1_pivot_rows,
    tuple(base.EXPONENTS[rows1[index]] for index in r1_pivot_rows),
    nonzero_2minor,
)
print("R0 fixed-image pivot rows/columns/value:", w_pivot)
print("R0 plus-interior quotient pivot:", plus_pivot)
print("R0 intersection-line rank-1 pivot:", line_pivot)
print("R0 intersection-line augmented 2x2 minors: all zero")

with open("E6_R0_PLUS_ATLAS.txt", "w", encoding="utf-8") as stream:
    stream.write("field QQ(s), s^2=-2\n")
    stream.write("plane d=-2*f, 3*c+(4+2*s)*e+(2-2*s)*f=0\n")
    stream.write("fixed_image_rank 3\n")
    stream.write("fixed_image_pivot " + repr(w_pivot) + "\n")
    stream.write("quotient_generic_rank 3\n")
    stream.write("plus_plane_quotient_rank 2\n")
    stream.write("plus_plane_pivot " + repr(plus_pivot) + "\n")
    stream.write("rankdrop_gcd " + str(gcd_maximal) + "\n")
    stream.write("rankdrop_groebner\n")
    for value in groebner_rankdrop.polys:
        stream.write(str(sp.factor(value.as_expr(), extension=s)) + "\n")
    stream.write("compatibility_minors\n")
    for value in compatibility:
        stream.write(str(sp.factor(value, extension=s)) + "\n")
    if compatibility:
        stream.write("compatibility_groebner\n")
        for value in groebner_compat.polys:
            stream.write(str(sp.factor(value.as_expr(), extension=s)) + "\n")
    else:
        stream.write("compatibility_groebner ZERO_IDEAL\n")
    stream.write("intersection e=f=k, c=d=-2*k\n")
    stream.write("intersection_quotient_rank 1_for_k_nonzero\n")
    stream.write("intersection_pivot " + repr(line_pivot) + "\n")
    stream.write("intersection_augmented_2minors ZERO_IDEAL\n")
    stream.write("origin_quotient_rank 0_rhs_zero\n")

print("D4_DN2C_E6_DETERMINANTAL_ELIMINATION_PASS")
