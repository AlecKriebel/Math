#!/usr/bin/env python3
"""Independent exact reconstruction of the marked-critical infinity proof."""

from __future__ import annotations

from itertools import product

import sympy as sp


if not __debug__:
    raise SystemExit("ERROR: hostile audit refuses optimized Python mode")

x, y, z = sp.symbols("x y z")
xyz = (x, y, z)
p = x**2
q = y * z


def monomials(degree: int) -> tuple[sp.Expr, ...]:
    return tuple(
        x**i * y**j * z ** (degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def form(prefix: str, degree: int) -> tuple[sp.Expr, tuple[sp.Symbol, ...]]:
    coefficients = sp.symbols(f"{prefix}0:{len(monomials(degree))}")
    return (
        sum(
            coefficient_value * monomial
            for coefficient_value, monomial in zip(
                coefficients, monomials(degree)
            )
        ),
        coefficients,
    )


def jacobian_determinant(
    first: sp.Expr, second: sp.Expr, third: sp.Expr
) -> sp.Expr:
    return sp.expand(
        sp.Matrix([first, second, third]).jacobian(xyz).det()
    )


def weighted(
    linear: sp.Matrix,
    quadratic: sp.Matrix,
    cubic: sp.Matrix,
    quartic: sp.Matrix,
    weight: int,
) -> sp.Expr:
    jacobians = tuple(
        vector.jacobian(xyz)
        for vector in (linear, quadratic, cubic, quartic)
    )
    result = 0
    for row_weights in product(range(4), repeat=3):
        if sum(row_weights) != weight:
            continue
        result += sp.Matrix.vstack(
            *(
                jacobians[row_weights[row]][row, :]
                for row in range(3)
            )
        ).det()
    return sp.expand(result)


def coefficient(expression: sp.Expr, monomial: sp.Expr) -> sp.Expr:
    return sp.Poly(sp.expand(expression), x, y, z).coeff_monomial(monomial)


def coefficient_vector(expression: sp.Expr, degree: int) -> sp.Matrix:
    polynomial = sp.Poly(sp.expand(expression), x, y, z)
    return sp.Matrix(
        [
            polynomial.coeff_monomial(monomial)
            for monomial in monomials(degree)
        ]
    )


def coefficient_map(expression: sp.Expr, degree: int) -> dict[sp.Expr, sp.Expr]:
    polynomial = sp.Poly(sp.expand(expression), x, y, z)
    return {
        monomial: sp.factor(polynomial.coeff_monomial(monomial))
        for monomial in monomials(degree)
        if polynomial.coeff_monomial(monomial) != 0
    }


def assert_maps_equal(
    actual: dict[sp.Expr, sp.Expr], expected: dict[sp.Expr, sp.Expr]
) -> None:
    assert set(actual) == set(expected), (set(actual), set(expected))
    for monomial, expected_value in expected.items():
        assert sp.expand(actual[monomial] - expected_value) == 0, (
            monomial,
            actual[monomial],
            expected_value,
        )


delta = lambda expression: sp.expand(
    z * sp.diff(expression, z) - y * sp.diff(expression, y)
)
H4 = sp.Matrix([p**2, q**2, 0])
zero_linear = sp.zeros(3, 1)

# ---------------------------------------------------------------------------
# 1. Complete E7 kernel before and after all four affine gauges.

Uraw, uraw = form("raw_u", 3)
Vraw, vraw = form("raw_v", 3)
Wraw, wraw = form("raw_w", 2)
E7raw = weighted(
    zero_linear,
    sp.Matrix([0, 0, Wraw]),
    sp.Matrix([Uraw, Vraw, x**3]),
    H4,
    7,
)
assert sp.expand(
    E7raw + 2 * x**2 * q * delta(3 * Uraw - 4 * x * Wraw)
) == 0

raw_equations = [
    coefficient(E7raw, monomial) for monomial in monomials(7)
]
raw_matrix, raw_rhs = sp.linear_eq_to_matrix(
    raw_equations, uraw + vraw + wraw
)
assert raw_rhs == sp.zeros(len(monomials(7)), 1)
assert raw_matrix.rank() == 8

A = sp.symbols("A")
w = sp.symbols("w0:6")
v = sp.symbols("v1 v2 v3 v4 v5 v6 v9")
W = sum(value * monomial for value, monomial in zip(w, monomials(2)))
V = (
    v[0] * x**2 * y
    + v[1] * x**2 * z
    + v[2] * x * y**2
    + v[3] * x * q
    + v[4] * x * z**2
    + v[5] * y**3
    + v[6] * z**3
)
U = sp.Rational(4, 3) * x * W + A * x * q

u_shear, v_shear, translate_y, translate_z = sp.symbols(
    "u_shear v_shear translate_y translate_z"
)
raw_U_family = U + u_shear * x**3
raw_V_family = (
    V
    + v_shear * x**3
    + translate_y * sp.diff(q**2, y)
    + translate_z * sp.diff(q**2, z)
)
raw_W_family = W
family_parameters = (
    A,
    *w,
    *v,
    u_shear,
    v_shear,
    translate_y,
    translate_z,
)
assert len(family_parameters) == 18
family_vector = sp.Matrix.vstack(
    coefficient_vector(raw_U_family, 3),
    coefficient_vector(raw_V_family, 3),
    coefficient_vector(raw_W_family, 2),
)
family_matrix = family_vector.jacobian(family_parameters)
assert family_matrix.rank() == 18
assert raw_matrix * family_matrix == sp.zeros(36, 18)
assert raw_matrix.rank() + family_matrix.rank() == 26

print("  PASS E7 raw rank 8, nullity 18, and complete four-gauge quotient")

# ---------------------------------------------------------------------------
# 2. Target shears: record their exact effects on every homogeneous layer.

U2_general, u = form("u", 2)
V2_general, h = form("h", 2)
ell = sp.symbols("ell0:9")
L = sp.Matrix(3, 3, ell) * sp.Matrix([x, y, z])
H2_general = sp.Matrix([U2_general, V2_general, W])
H3_general = sp.Matrix([U, V, x**3])
shear_parameter = sp.symbols("shear_parameter")
T1 = sp.eye(3)
T1[0, 2] = shear_parameter
T2 = sp.eye(3)
T2[1, 2] = shear_parameter
assert T1.det() == 1 and T2.det() == 1
assert sp.expand((T1 * H3_general)[0] - (U + shear_parameter * x**3)) == 0
assert sp.expand((T1 * H2_general)[0] - (U2_general + shear_parameter * W)) == 0
assert sp.expand((T1 * L)[0] - (L[0] + shear_parameter * L[2])) == 0
assert sp.expand((T2 * H3_general)[1] - (V + shear_parameter * x**3)) == 0
assert sp.expand((T2 * H2_general)[1] - (V2_general + shear_parameter * W)) == 0
assert sp.expand((T2 * L)[1] - (L[1] + shear_parameter * L[2])) == 0
assert sp.expand(
    sp.Matrix(3, 3, ell).det()
    - (T1 * sp.Matrix(3, 3, ell)).det()
) == 0
assert sp.expand(
    sp.Matrix(3, 3, ell).det()
    - (T2 * sp.Matrix(3, 3, ell)).det()
) == 0

print("  PASS target-shear effects on H3, H2, L0, and det(L0)")

# ---------------------------------------------------------------------------
# 3. Complete raw E6 table, radical, product split, and converse.

E6 = weighted(
    L,
    H2_general,
    H3_general,
    H4,
    6,
)
expected_E6 = {
    x**5 * y: -3 * A * v[0],
    x**5 * z: 3 * A * v[1],
    x**4 * y**2: -6 * A * v[2],
    x**4 * z**2: 6 * A * v[4],
    x**3 * y**3: -9 * A * v[5],
    x**3 * z**3: 9 * A * v[6],
    x**3 * y**2 * z: sp.Rational(2, 3)
    * (-12 * ell[7] + 9 * u[1] - 4 * w[0] * w[1]),
    x**3 * y * z**2: -sp.Rational(2, 3)
    * (-12 * ell[8] + 9 * u[2] - 4 * w[0] * w[2]),
    x**2 * y**3 * z: sp.Rational(4, 3)
    * (9 * u[3] - 4 * w[0] * w[3] - 2 * w[1] ** 2),
    x**2 * y * z**3: -sp.Rational(4, 3)
    * (9 * u[5] - 4 * w[0] * w[5] - 2 * w[2] ** 2),
    x * y**4 * z: -8 * w[1] * w[3],
    x * y**3 * z**2: -sp.Rational(2, 3)
    * (3 * A * w[1] + 4 * w[1] * w[4] + 4 * w[2] * w[3]),
    x * y**2 * z**3: sp.Rational(2, 3)
    * (3 * A * w[2] + 4 * w[1] * w[5] + 4 * w[2] * w[4]),
    x * y * z**4: 8 * w[2] * w[5],
    y**5 * z: -sp.Rational(16, 3) * w[3] ** 2,
    y**4 * z**2: -sp.Rational(4, 3)
    * w[3]
    * (3 * A + 4 * w[4]),
    y**2 * z**4: sp.Rational(4, 3)
    * w[5]
    * (3 * A + 4 * w[4]),
    y * z**5: sp.Rational(16, 3) * w[5] ** 2,
}
assert_maps_equal(coefficient_map(E6, 6), expected_E6)

lower_unknowns = u + h + ell
E6_matrix, _ = sp.linear_eq_to_matrix(
    list(expected_E6.values()), lower_unknowns
)
assert E6_matrix.rank() == 4
assert E6_matrix.extract(
    (6, 7, 8, 9), (1, 2, 3, 5)
).det() != 0

C = sp.symbols("C")
e6_solution = {
    w[3]: 0,
    w[5]: 0,
    u[1]: sp.Rational(4, 3) * ell[7]
    + sp.Rational(4, 9) * w[0] * w[1],
    u[2]: sp.Rational(4, 3) * ell[8]
    + sp.Rational(4, 9) * w[0] * w[2],
    u[3]: sp.Rational(2, 9) * w[1] ** 2,
    u[5]: sp.Rational(2, 9) * w[2] ** 2,
    w[4]: sp.Rational(3, 4) * (C - A),
}
reduced_E6 = coefficient_map(E6.subs(e6_solution), 6)
expected_reduced_E6 = {
    x**5 * y: -3 * A * v[0],
    x**5 * z: 3 * A * v[1],
    x**4 * y**2: -6 * A * v[2],
    x**4 * z**2: 6 * A * v[4],
    x**3 * y**3: -9 * A * v[5],
    x**3 * z**3: 9 * A * v[6],
    x * y**3 * z**2: -2 * C * w[1],
    x * y**2 * z**3: 2 * C * w[2],
}
assert_maps_equal(reduced_E6, expected_reduced_E6)

print("  PASS E6 rank 4, square radical, product split, and full converse")

# Common lower notation for the four branches, already after removal of the
# first cubic's x^3 term when the branch is written in canonical form.
B, w0, w1, w2, w4, u0, u4 = sp.symbols(
    "B w0 w1 w2 w4 u0 u4"
)
b = sp.symbols("b0:6")
V2 = sum(value * monomial for value, monomial in zip(b, monomials(2)))
L = sp.Matrix(3, 3, ell) * sp.Matrix([x, y, z])


def invariant_U2() -> sp.Expr:
    return (
        u0 * p
        + sp.Rational(4, 3) * ell[7] * x * y
        + sp.Rational(4, 3) * ell[8] * x * z
        + u4 * q
    )


def determinant_after(substitutions: dict[sp.Symbol, sp.Expr]) -> sp.Expr:
    return sp.expand(sp.Matrix(3, 3, ell).det().subs(substitutions))


# ---------------------------------------------------------------------------
# 4. A != 0, C != 0.

H3_case1 = sp.Matrix([C * x * q, B * x * q, x**3])
H2_case1 = sp.Matrix([invariant_U2(), V2, w0 * p + w4 * q])
assert weighted(L, H2_case1, H3_case1, H4, 6) == 0
E5_case1 = weighted(L, H2_case1, H3_case1, H4, 5)
assert coefficient(E5_case1, y**3 * z**2) == -2 * C * ell[7]
assert coefficient(E5_case1, y**2 * z**3) == 2 * C * ell[8]
case1_reduced = E5_case1.subs({ell[7]: 0, ell[8]: 0})
assert coefficient(case1_reduced, x**2 * y**2 * z) == 6 * ell[1]
assert coefficient(case1_reduced, x**2 * y * z**2) == -6 * ell[2]
assert determinant_after(
    {ell[1]: 0, ell[2]: 0, ell[7]: 0, ell[8]: 0}
) == 0

print("  PASS case A!=0, C!=0")

# ---------------------------------------------------------------------------
# 5. A != 0, C = 0, including the complete E5 solve.

AA = sp.symbols("AA")
W_case2 = w0 * p + w1 * x * y + w2 * x * z - sp.Rational(3, 4) * AA * q
U3_case2 = sp.Rational(4, 3) * x * W_case2 + AA * x * q
U2_case2 = (
    u0 * p
    + (
        sp.Rational(4, 3) * ell[7]
        + sp.Rational(4, 9) * w0 * w1
    )
    * x
    * y
    + (
        sp.Rational(4, 3) * ell[8]
        + sp.Rational(4, 9) * w0 * w2
    )
    * x
    * z
    + sp.Rational(2, 9) * w1**2 * y**2
    + u4 * q
    + sp.Rational(2, 9) * w2**2 * z**2
)
H3_case2 = sp.Matrix([U3_case2, B * x * q, x**3])
H2_case2 = sp.Matrix([U2_case2, V2, W_case2])
assert weighted(L, H2_case2, H3_case2, H4, 6) == 0
E5_case2 = weighted(L, H2_case2, H3_case2, H4, 5)
assert coefficient(E5_case2, y**4 * z) == sp.Rational(8, 9) * w1**3
assert coefficient(E5_case2, y * z**4) == -sp.Rational(8, 9) * w2**3
case2_after_cubes = coefficient_map(
    E5_case2.subs({w1: 0, w2: 0}), 5
)
assert_maps_equal(
    case2_after_cubes,
    {
        x**4 * y: -3 * AA * b[1],
        x**4 * z: 3 * AA * b[2],
        x**3 * y**2: -6 * AA * b[3],
        x**3 * z**2: 6 * AA * b[5],
        x**2 * y**2 * z: sp.Rational(2, 3)
        * (9 * ell[1] - 4 * w0 * ell[7]),
        x**2 * y * z**2: -sp.Rational(2, 3)
        * (9 * ell[2] - 4 * w0 * ell[8]),
    },
)
case2_E5_solution = {
    w1: 0,
    w2: 0,
    b[1]: 0,
    b[2]: 0,
    b[3]: 0,
    b[5]: 0,
    ell[1]: sp.Rational(4, 9) * w0 * ell[7],
    ell[2]: sp.Rational(4, 9) * w0 * ell[8],
}
E4_case2 = weighted(L, H2_case2, H3_case2, H4, 4).subs(
    case2_E5_solution
)
assert coefficient(E4_case2, y**3 * z) == -sp.Rational(8, 3) * ell[7] ** 2
assert coefficient(E4_case2, y * z**3) == sp.Rational(8, 3) * ell[8] ** 2
assert determinant_after(
    {
        ell[7]: 0,
        ell[8]: 0,
        ell[1]: 0,
        ell[2]: 0,
    }
) == 0

print("  PASS case A!=0, C=0, including zero values of B,w0,u4")

# ---------------------------------------------------------------------------
# 6. A = 0, C != 0, including both K leaves and the extra E4 products.

r = sp.symbols("r1 r2 r3 r4 r5 r6 r9")
V3_case3 = (
    r[0] * x**2 * y
    + r[1] * x**2 * z
    + r[2] * x * y**2
    + r[3] * x * q
    + r[4] * x * z**2
    + r[5] * y**3
    + r[6] * z**3
)
W_case3 = w0 * p + sp.Rational(3, 4) * C * q
H3_case3 = sp.Matrix([C * x * q, V3_case3, x**3])
H2_case3 = sp.Matrix([invariant_U2(), V2, W_case3])
assert weighted(L, H2_case3, H3_case3, H4, 6) == 0
E5_case3 = weighted(L, H2_case3, H3_case3, H4, 5)
case3_high = {
    r[2]: 0,
    r[4]: 0,
    r[5]: 0,
    r[6]: 0,
    ell[7]: 0,
    ell[8]: 0,
}
assert coefficient(E5_case3, x * y**3 * z) == sp.Rational(3, 2) * C**2 * r[2]
assert coefficient(E5_case3, x * y * z**3) == -sp.Rational(3, 2) * C**2 * r[4]
assert coefficient(E5_case3, y**4 * z) == sp.Rational(9, 4) * C**2 * r[5]
assert coefficient(E5_case3, y * z**4) == -sp.Rational(9, 4) * C**2 * r[6]
assert coefficient(E5_case3, y**3 * z**2) == -2 * C * ell[7]
assert coefficient(E5_case3, y**2 * z**3) == 2 * C * ell[8]

case3_remaining = coefficient_map(E5_case3.subs(case3_high), 5)
K = 2 * C * w0 + 3 * u4
assert_maps_equal(
    case3_remaining,
    {
        x**4 * y: -K * r[0],
        x**4 * z: K * r[1],
        x**2 * y**2 * z: sp.Rational(3, 4)
        * (C**2 * r[0] + 8 * ell[1]),
        x**2 * y * z**2: -sp.Rational(3, 4)
        * (C**2 * r[1] + 8 * ell[2]),
    },
)

# K != 0 forces r1=r2=0, then the first/third column pairs vanish.
assert determinant_after(
    {
        **case3_high,
        r[0]: 0,
        r[1]: 0,
        ell[1]: 0,
        ell[2]: 0,
    }
) == 0

# K=0 leaves r1,r2, fixes the first-row entries, and then E4 fixes four
# second-quadratic coefficients.  Two additional products are retained.
case3_resonant = {
    **case3_high,
    u4: -sp.Rational(2, 3) * C * w0,
    ell[1]: -C**2 * r[0] / 8,
    ell[2]: -C**2 * r[1] / 8,
}
E4_case3 = weighted(L, H2_case3, H3_case3, H4, 4).subs(
    case3_resonant
)
Q = 9 * C * r[3] + 24 * ell[6] - 36 * u0 - 32 * w0**2
assert_maps_equal(
    coefficient_map(E4_case3, 4),
    {
        x**3 * y: -C * r[0] * Q / 24,
        x**3 * z: C * r[1] * Q / 24,
        x * y**2 * z: sp.Rational(1, 4)
        * C**2
        * (3 * b[1] - 2 * r[0] * w0),
        x * y * z**2: sp.Rational(1, 4)
        * C**2
        * (-3 * b[2] + 2 * r[1] * w0),
        y**3 * z: sp.Rational(3, 2) * C**2 * b[3],
        y * z**3: -sp.Rational(3, 2) * C**2 * b[5],
    },
)
case3_E4_solution = {
    b[1]: sp.Rational(2, 3) * r[0] * w0,
    b[2]: sp.Rational(2, 3) * r[1] * w0,
    b[3]: 0,
    b[5]: 0,
}
E2_case3 = weighted(L, H2_case3, H3_case3, H4, 2).subs(
    case3_resonant
).subs(case3_E4_solution)
expected_x2 = -sp.Rational(3, 8) * C**2 * (
    r[0] * ell[5] - r[1] * ell[4]
)
assert sp.expand(coefficient(E2_case3, x**2) - expected_x2) == 0
det_case3 = determinant_after(case3_resonant)
assert sp.expand(det_case3 - ell[6] * expected_x2 / 3) == 0

print(
    "  PASS case A=0, C!=0, both K leaves, E4 products, and E2 determinant"
)

# ---------------------------------------------------------------------------
# 7. A = C = 0, including pre/post-shear coordinates and u4=0.

W_case4_raw = w0 * p + w1 * x * y + w2 * x * z
U3_case4_raw = sp.Rational(4, 3) * x * W_case4_raw
U2_case4_raw = (
    u0 * p
    + (
        sp.Rational(4, 3) * ell[7]
        + sp.Rational(4, 9) * w0 * w1
    )
    * x
    * y
    + (
        sp.Rational(4, 3) * ell[8]
        + sp.Rational(4, 9) * w0 * w2
    )
    * x
    * z
    + sp.Rational(2, 9) * w1**2 * y**2
    + u4 * q
    + sp.Rational(2, 9) * w2**2 * z**2
)
H3_case4_raw = sp.Matrix([U3_case4_raw, V3_case3, x**3])
H2_case4_raw = sp.Matrix([U2_case4_raw, V2, W_case4_raw])
assert weighted(L, H2_case4_raw, H3_case4_raw, H4, 6) == 0
E5_case4_raw = weighted(L, H2_case4_raw, H3_case4_raw, H4, 5)
assert coefficient(E5_case4_raw, y**4 * z) == sp.Rational(8, 9) * w1**3
assert coefficient(E5_case4_raw, y * z**4) == -sp.Rational(8, 9) * w2**3

# Apply the actual target shear lambda=-4w0/3.  It removes U3's x^3 term,
# shifts U2 only in its free p coefficient, and shifts row 1 by the same
# multiple of row 3.  Relabel the resulting free coefficients.
lambda_case4 = -sp.Rational(4, 3) * w0
T_case4 = sp.eye(3)
T_case4[0, 2] = lambda_case4
raw_after_cubes_H3 = H3_case4_raw.subs({w1: 0, w2: 0})
raw_after_cubes_H2 = H2_case4_raw.subs({w1: 0, w2: 0})
assert sp.expand((T_case4 * raw_after_cubes_H3)[0]) == 0
assert sp.expand(
    (T_case4 * raw_after_cubes_H2)[0]
    - (
        (u0 - sp.Rational(4, 3) * w0**2) * p
        + sp.Rational(4, 3) * ell[7] * x * y
        + sp.Rational(4, 3) * ell[8] * x * z
        + u4 * q
    )
) == 0
assert sp.expand(
    (T_case4 * L)[0]
    - (L[0] - sp.Rational(4, 3) * w0 * L[2])
) == 0

# Canonical post-shear variables.
H3_case4 = sp.Matrix([0, V3_case3, x**3])
H2_case4 = sp.Matrix([invariant_U2(), V2, w0 * p])
assert weighted(L, H2_case4, H3_case4, H4, 6) == 0
E5_case4 = weighted(L, H2_case4, H3_case4, H4, 5)
case4_E5_expected = {
    x**4 * y: -3 * r[0] * u4,
    x**4 * z: 3 * r[1] * u4,
    x**3 * y**2: -6 * r[2] * u4,
    x**3 * z**2: 6 * r[4] * u4,
    x**2 * y**3: -9 * r[5] * u4,
    x**2 * y**2 * z: sp.Rational(2, 3)
    * (9 * ell[1] + 8 * w0 * ell[7]),
    x**2 * y * z**2: -sp.Rational(2, 3)
    * (9 * ell[2] + 8 * w0 * ell[8]),
    x**2 * z**3: 9 * r[6] * u4,
}
assert_maps_equal(coefficient_map(E5_case4, 5), case4_E5_expected)
case4_relations = {
    ell[1]: -sp.Rational(8, 9) * w0 * ell[7],
    ell[2]: -sp.Rational(8, 9) * w0 * ell[8],
}
E4_case4 = weighted(L, H2_case4, H3_case4, H4, 4).subs(
    case4_relations
)
assert coefficient(E4_case4, y**3 * z) == -sp.Rational(8, 3) * ell[7] ** 2
assert coefficient(E4_case4, y * z**3) == sp.Rational(8, 3) * ell[8] ** 2
assert determinant_after(
    {
        ell[7]: 0,
        ell[8]: 0,
        ell[1]: 0,
        ell[2]: 0,
    }
) == 0

print("  PASS case A=C=0, exact shear, and all u4/V specializations")
print("PASS: hostile exact reconstruction of marked-critical infinity orbit")
