#!/usr/bin/env python3
"""Build the specialization-safe full-lower E6 linear system for D4-DN-2C.

The six contact parameters are coordinates in the explicit E7 nullspace.
The 18 lower variables are exactly

  * 4 binary coefficients each in U_0 and V_0,
  * 3 binary coefficients in T_0,
  * 3 coefficients each in A_r-integrating and B_r-integrating quadratics,
  * the (3,3) entry of the linear part.

E6 is affine-linear in these 18 variables.  This script constructs its
coefficient matrix without solving at a generic point and prints its
r-degree block structure and all lower-variable-free equations.
"""

from __future__ import annotations

import collections
import sys

import sympy as sp

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

p, q, r, weight = sp.symbols("p q r weight")
coords = (p, q, r)


def jac2(f: sp.Expr, g: sp.Expr) -> sp.Expr:
    return sp.expand(sp.diff(f, p) * sp.diff(g, q) - sp.diff(f, q) * sp.diff(g, p))


def homogeneous_exponents(degree: int) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        (i, j, degree - i - j)
        for k in range(degree, -1, -1)
        for i in range(degree - k, degree - k + 1)
        for j in range(k, k + 1)
    )


# More transparent order: increasing r-degree, decreasing p-degree.
EXPONENTS = tuple(
    (i, 6 - k - i, k)
    for k in range(7)
    for i in range(6 - k, -1, -1)
)
assert len(EXPONENTS) == 28

h = (p + q) ** 2
P = sp.expand(h * p**2)
Q = sp.expand(h * q**2)
R = sp.expand(h * (p - 2 * q))
alpha = sp.factor(jac2(Q, R))
beta = sp.factor(-jac2(P, R))
gamma = sp.factor(jac2(P, Q))

# E7 kernel coordinates.  The first two span the r^2 coefficients in
# U,V,T; the final four span the r-linear coefficients.
a, b, c, d, e, f = sp.symbols("a b c d e f")
U2 = sp.expand(a * (p + 2 * q) + 4 * b * (p + q))
V2 = a * q
T2 = 3 * b
U1 = sp.expand(
    c * (p**2 + 2 * p * q)
    + d * (p * q + 2 * q**2)
    + 4 * e * p * (p + q)
    + 4 * f * q * (p + q)
)
V1 = sp.expand(c * p * q + d * q**2)
T1 = 3 * e * p + 3 * f * q

assert sp.expand(alpha * U2 + beta * V2 + gamma * T2) == 0
assert sp.expand(alpha * U1 + beta * V1 + gamma * T1) == 0

uc = sp.symbols("uc0:4")
vc = sp.symbols("vc0:4")
tc = sp.symbols("tc0:3")
ar = sp.symbols("ar0:3")
br = sp.symbols("br0:3")
ell33 = sp.symbols("ell33")
LOWER = uc + vc + tc + ar + br + (ell33,)
assert len(LOWER) == 18

binary3 = (p**3, p**2 * q, p * q**2, q**3)
binary2 = (p**2, p * q, q**2)
U0 = sum(value * monomial for value, monomial in zip(uc, binary3))
V0 = sum(value * monomial for value, monomial in zip(vc, binary3))
T0 = sum(value * monomial for value, monomial in zip(tc, binary2))

# A and B are chosen so their derivatives in r are
# ar0*p+ar1*q+ar2*r and br0*p+br1*q+br2*r.  This avoids harmless factors 2.
A = r * (ar[0] * p + ar[1] * q) + sp.Rational(1, 2) * ar[2] * r**2
B = r * (br[0] * p + br[1] * q) + sp.Rational(1, 2) * br[2] * r**2

U = U0 + r * U1 + r**2 * U2
V = V0 + r * V1 + r**2 * V2
T = T0 + r * T1 + r**2 * T2
H2 = sp.Matrix((A, B, T))
H3 = sp.Matrix((U, V, R))
H4 = sp.Matrix((P, Q, 0))
linear = sp.zeros(3)
linear[2, 2] = ell33

determinant = sp.Poly(
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
assert sp.expand(determinant.coeff_monomial(weight**7)) == 0
E6 = sp.Poly(sp.expand(determinant.coeff_monomial(weight**6)), p, q, r)

equations = sp.Matrix(
    [
        E6.coeff_monomial(p**i * q**j * r**k)
        for i, j, k in EXPONENTS
    ]
)
constant = equations.subs({value: 0 for value in LOWER})
matrix = equations.jacobian(LOWER)

affine_defect = sp.simplify(equations - matrix * sp.Matrix(LOWER) - constant)
if affine_defect != sp.zeros(28, 1):
    for row, value in enumerate(affine_defect):
        if value != 0:
            print("NONAFFINE", EXPONENTS[row], sp.factor(value))
assert affine_defect == sp.zeros(28, 1)
assert all(
    sp.diff(equation, left, right) == 0
    for equation in equations
    for index, left in enumerate(LOWER)
    for right in LOWER[index:]
)

row_by_exponent = {
    exponent: index for index, exponent in enumerate(EXPONENTS)
}
assert sp.factor(constant[row_by_exponent[(3, 0, 3)]] + 6 * a**2) == 0
assert sp.factor(
    constant[row_by_exponent[(2, 1, 3)]] - 48 * b * (a + b)
) == 0
# Over a characteristic-zero field the first identity gives a=0; the
# second then gives b=0.  Every coefficient of r-degree at least two
# vanishes after this forced substitution.
assert all(
    sp.factor(constant[index].subs({a: 0, b: 0})) == 0
    for index, exponent in enumerate(EXPONENTS)
    if exponent[2] >= 2
)

print("contact parameters:", (a, b, c, d, e, f))
print("lower variables:", LOWER)
print("full matrix shape:", matrix.shape)
for rdegree in range(7):
    rows = [index for index, exponent in enumerate(EXPONENTS) if exponent[2] == rdegree]
    block = matrix[rows, :]
    zero_rows = [rows[j] for j in range(len(rows)) if block.row(j) == sp.zeros(1, 18)]
    print(
        f"rdeg={rdegree}: rows={len(rows)}, "
        f"generic-rank={block.rank()}, zero-lower-rows={len(zero_rows)}"
    )
    for row in zero_rows:
        value = sp.factor(constant[row])
        if value != 0:
            print("  exponent", EXPONENTS[row], "constant =", value)

contact_boundary = {a: 0, b: 0}
survivor_matrix = sp.simplify(matrix.subs(contact_boundary))
survivor_constant = sp.simplify(constant.subs(contact_boundary))
active_rows = [
    index
    for index, exponent in enumerate(EXPONENTS)
    if exponent[2] in (0, 1)
]
survivor_system = survivor_matrix[active_rows, :]
survivor_rhs = -survivor_constant[active_rows, :]
active_columns = [
    column
    for column in range(18)
    if survivor_system[:, column] != sp.zeros(len(active_rows), 1)
]
print("a=b=0 active lower variables:", tuple(LOWER[column] for column in active_columns))
print(
    "a=b=0 system shape/rank:",
    survivor_system.shape,
    survivor_system.rank(),
    "augmented generic rank:",
    survivor_system.row_join(survivor_rhs).rank(),
)
for rdegree in (0, 1):
    rows = [
        active_rows.index(index)
        for index, exponent in enumerate(EXPONENTS)
        if exponent[2] == rdegree
    ]
    columns = [
        column
        for column in active_columns
        if survivor_system[rows, column] != sp.zeros(len(rows), 1)
    ]
    print(
        f"a=b=0 rdeg={rdegree} active columns:",
        tuple(LOWER[column] for column in columns),
    )

# Persist exact sparse matrix data in a deterministic plain-text format.
with open("E6_MATRIX.txt", "w", encoding="utf-8") as stream:
    stream.write("CONTACT " + " ".join(map(str, (a, b, c, d, e, f))) + "\n")
    stream.write("LOWER " + " ".join(map(str, LOWER)) + "\n")
    for row, exponent in enumerate(EXPONENTS):
        stream.write(f"ROW {exponent[0]} {exponent[1]} {exponent[2]}\n")
        stream.write("  CONST " + str(sp.factor(constant[row])) + "\n")
        for column, variable in enumerate(LOWER):
            value = sp.factor(matrix[row, column])
            if value != 0:
                stream.write(f"  {variable} {value}\n")

print("D4_DN2C_FULL_LOWER_E6_MATRIX_PASS")
