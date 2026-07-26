#!/usr/bin/env python3
"""Independent exact exclusion of the six released CH/CS endpoint slices.

Five slices force det(L)=0 at E5.  RO-smooth/H has a genuine invertible
through-E5 family; two E4 coefficients then force det(L)=0.  The script
retains an explicit sharp through-E5 witness as a regression.
"""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: assertions are required; do not run with -O", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp

x, y, z, weight = sp.symbols("x y z weight")
xyz = (x, y, z)
A, B, C, D, T, S = sp.symbols("A B C D T S")
a = sp.symbols("a0:6")
b = sp.symbols("b0:6")
ell = sp.symbols("l0:9")
lower = a + b + ell
L = sp.Matrix(3, 3, ell)

mon2 = tuple(
    x**i * y**j * z ** (2 - i - j)
    for i in range(2, -1, -1)
    for j in range(2 - i, -1, -1)
)


def exponents(degree: int) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        (i, j, degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def coefficient(polynomial: sp.Expr, exponent: tuple[int, int, int]) -> sp.Expr:
    poly = sp.Poly(sp.expand(polynomial), x, y, z)
    i, j, k = exponent
    return sp.factor(poly.coeff_monomial(x**i * y**j * z**k))


def coefficients(polynomial: sp.Expr, degree: int) -> list[sp.Expr]:
    return [coefficient(polynomial, exponent) for exponent in exponents(degree)]


def exact_zero(value: sp.Expr) -> bool:
    return sp.expand(value) == 0


def assert_equal(actual: sp.Expr, expected: sp.Expr) -> None:
    assert exact_zero(actual - expected)


def weighted_determinant(
    h: sp.Expr,
    U: sp.Expr,
    V: sp.Expr,
    R: sp.Expr,
    W: sp.Expr,
) -> sp.Poly:
    H2 = sp.Matrix(
        [
            sum(c * m for c, m in zip(a, mon2)),
            sum(c * m for c, m in zip(b, mon2)),
            W,
        ]
    )
    H3 = sp.Matrix([U, V, R])
    H4 = sp.Matrix([h**2, h * x**2, 0])
    determinant = sp.Poly(
        sp.expand(
            (
                L
                + weight * H2.jacobian(xyz)
                + weight**2 * H3.jacobian(xyz)
                + weight**3 * H4.jacobian(xyz)
            ).det()
        ),
        weight,
    )
    assert all(determinant.coeff_monomial(weight**degree) == 0 for degree in (9, 8, 7))
    return determinant


def solve_e6(
    determinant: sp.Poly,
    pivot_rows: tuple[int, ...],
    pivot_columns: tuple[int, ...],
    expected_minor: sp.Expr,
) -> dict[sp.Symbol, sp.Expr]:
    matrix, rhs = sp.linear_eq_to_matrix(
        coefficients(determinant.coeff_monomial(weight**6), 6), lower
    )
    pivot = matrix.extract(pivot_rows, pivot_columns)
    assert pivot.det() == expected_minor
    free_columns = tuple(index for index in range(len(lower)) if index not in pivot_columns)
    solution = pivot.inv() * (
        rhs.extract(pivot_rows, [0])
        - matrix.extract(pivot_rows, free_columns)
        * sp.Matrix([lower[index] for index in free_columns])
    )
    substitution = {
        lower[index]: sp.factor(value)
        for index, value in zip(pivot_columns, solution)
    }
    assert all(
        exact_zero(value.subs(substitution))
        for value in matrix * sp.Matrix(lower) - rhs
    )
    return substitution


RT_H_ROWS = (7, 8, 11, 13, 17, 18, 23, 25)
RT_H_COLUMNS = (1, 2, 3, 5, 7, 8, 9, 11)
RT_S_ROWS = (1, 2, 3, 5, 7, 8, 11, 13, 17, 18)
RT_S_COLUMNS = (1, 2, 3, 5, 7, 8, 9, 11, 19, 20)
RO_H_ROWS = (2, 4, 5, 7, 8, 9, 11, 13)
RO_H_COLUMNS = (1, 2, 4, 5, 7, 8, 10, 11)
RO_S_ROWS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 11)
RO_S_COLUMNS = (1, 2, 4, 5, 7, 8, 10, 11, 19, 20)


# ---------------------------------------------------------------------------
# The two CS slices in the rank-two pencil.
# ---------------------------------------------------------------------------

for h, smooth in ((y * z, False), (x**2 + y * z, True)):
    determinant = weighted_determinant(
        h,
        A * x * y * z,
        B * x * y * z,
        x**3,
        T * y * z,
    )
    substitution6 = solve_e6(
        determinant, RT_S_ROWS, RT_S_COLUMNS, -26873856
    )
    E5 = sp.expand(determinant.coeff_monomial(weight**5).subs(substitution6))
    assert exact_zero(coefficient(E5, (2, 2, 1)) + 6 * ell[4])
    assert exact_zero(coefficient(E5, (2, 1, 2)) - 6 * ell[5])
    after_middle_zero = {ell[4]: 0, ell[5]: 0}
    expected_x4y = 3 * (ell[1] - 2 * ell[4]) if smooth else 3 * ell[1]
    expected_x4z = -3 * (ell[2] - 2 * ell[5]) if smooth else -3 * ell[2]
    assert exact_zero(coefficient(E5, (4, 1, 0)) - expected_x4y)
    assert exact_zero(coefficient(E5, (4, 0, 1)) - expected_x4z)
    forced5 = {ell[1]: 0, ell[2]: 0, ell[4]: 0, ell[5]: 0}
    assert exact_zero(L.det().subs(substitution6).subs(forced5))


# ---------------------------------------------------------------------------
# The two CH slices in the rank-two pencil.
# ---------------------------------------------------------------------------

for h in (y * z, x**2 + y * z):
    U = A * x**3 - 2 * C * y * h - 2 * D * z * h
    V = B * x**3 + C * x**2 * y + D * x**2 * z
    R = x * h
    W = T * x**2

    # E6 radical component A=0.  E5 immediately forces C=D=0.
    determinant_a0 = weighted_determinant(h, U.subs(A, 0), V, R, W)
    substitution6_a0 = solve_e6(
        determinant_a0, RT_H_ROWS, RT_H_COLUMNS, 256
    )
    E5_a0 = sp.expand(
        determinant_a0.coeff_monomial(weight**5).subs(substitution6_a0)
    )
    assert coefficient(E5_a0, (2, 3, 0)) == -12 * C**3
    assert coefficient(E5_a0, (2, 0, 3)) == 12 * D**3

    # E6 radical component C=D=0.  Four E5 equations make rows one and
    # three proportional in columns two and three, independently of A.
    determinant_cd0 = weighted_determinant(
        h, U.subs({C: 0, D: 0}), V.subs({C: 0, D: 0}), R, W
    )
    substitution6_cd0 = solve_e6(
        determinant_cd0, RT_H_ROWS, RT_H_COLUMNS, 256
    )
    E5_cd0 = sp.expand(
        determinant_cd0.coeff_monomial(weight**5).subs(substitution6_cd0)
    )
    common_factor = 6 * B - 8 * T
    assert coefficient(E5_cd0, (0, 3, 2)) == -2 * ell[4]
    assert coefficient(E5_cd0, (0, 2, 3)) == 2 * ell[5]
    assert exact_zero(
        coefficient(E5_cd0, (2, 2, 1))
        .subs({ell[4]: 0, ell[1]: common_factor * ell[7]})
    )
    assert exact_zero(
        coefficient(E5_cd0, (2, 1, 2))
        .subs({ell[5]: 0, ell[2]: common_factor * ell[8]})
    )
    forced5 = {
        ell[1]: common_factor * ell[7],
        ell[2]: common_factor * ell[8],
        ell[4]: 0,
        ell[5]: 0,
    }
    assert exact_zero(L.det().subs(substitution6_cd0).subs(forced5))


# ---------------------------------------------------------------------------
# RO-smooth/CS.
# ---------------------------------------------------------------------------

h_ro = y**2 + x * z
determinant_ro_s = weighted_determinant(
    h_ro,
    2 * A * z * h_ro,
    A * x**2 * z + B * x * h_ro + sp.Rational(2, 3) * C * y * h_ro,
    x**3,
    C * x * y + S * h_ro,
)
substitution6_ro_s = solve_e6(
    determinant_ro_s, RO_S_ROWS, RO_S_COLUMNS, 1934917632
)
E5_ro_s = sp.expand(
    determinant_ro_s.coeff_monomial(weight**5).subs(substitution6_ro_s)
)
assert_equal(coefficient(E5_ro_s, (2, 0, 3)), -sp.Rational(2, 9) * C**3)
E5_ro_s_c0 = sp.expand(E5_ro_s.subs(C, 0))
assert_equal(coefficient(E5_ro_s_c0, (5, 0, 0)), 3 * ell[1])
assert_equal(coefficient(E5_ro_s_c0, (4, 1, 0)), 6 * (A * a[3] - ell[2]))
assert_equal(coefficient(E5_ro_s_c0, (4, 0, 1)), -6 * ell[4])
assert_equal(coefficient(E5_ro_s_c0, (3, 1, 1)), -12 * (A * b[3] - ell[5]))
forced_ro_s = {
    C: 0,
    ell[1]: 0,
    ell[2]: A * a[3],
    ell[4]: 0,
    ell[5]: A * b[3],
}
assert exact_zero(L.det().subs(substitution6_ro_s).subs(forced_ro_s))


# ---------------------------------------------------------------------------
# RO-smooth/CH.  This is the only endpoint surviving E5 with det(L) != 0.
# ---------------------------------------------------------------------------

U_ro_h = A * x**3 - 2 * C * y * h_ro - 2 * D * z * h_ro + 2 * T * z * h_ro
V_ro_h = B * x**3 + C * x**2 * y + (D + T) * x**2 * z
R_ro_h = x * h_ro
W_ro_h = T * x * z

# On the E6 component A=0, E5 forces C=0.  The three displayed
# consequences form a division-free case argument over a field.
determinant_ro_h_a0 = weighted_determinant(
    h_ro, U_ro_h.subs(A, 0), V_ro_h, R_ro_h, W_ro_h
)
substitution6_ro_h_a0 = solve_e6(
    determinant_ro_h_a0, RO_H_ROWS, RO_H_COLUMNS, 3072
)
E5_ro_h_a0 = sp.expand(
    determinant_ro_h_a0.coeff_monomial(weight**5).subs(substitution6_ro_h_a0)
)
q = a[0] - 9 * B**2
assert_equal(coefficient(E5_ro_h_a0, (5, 0, 0)), 2 * C * q)
assert_equal(
    coefficient(E5_ro_h_a0, (4, 1, 0)), -4 * (D * q + 6 * B * C**2)
)
assert exact_zero(
    coefficient(E5_ro_h_a0, (3, 2, 0))
    - coefficient(E5_ro_h_a0, (4, 0, 1))
    - 12 * C * (6 * B * D - C**2)
)

# After C=0, three D-chain equations force D=0.
E5_ro_h_c0 = sp.expand(E5_ro_h_a0.subs(C, 0))
assert_equal(
    coefficient(E5_ro_h_c0, (0, 5, 0)), 4 * ((D - T) * b[3] + ell[5])
)
assert_equal(
    coefficient(E5_ro_h_c0, (1, 3, 1)),
    8 * ((D - T) * b[3] - 2 * D * ell[8] + ell[5]),
)
assert_equal(
    coefficient(E5_ro_h_c0, (2, 1, 2)),
    4 * (6 * D**3 + (D - T) * b[3] - 4 * D * ell[8] + ell[5]),
)

# On the E6 component C=D=0, solve E6 and record the complete E5
# relations relevant to det(L).
determinant_ro_h_cd0 = weighted_determinant(
    h_ro,
    U_ro_h.subs({C: 0, D: 0}),
    V_ro_h.subs({C: 0, D: 0}),
    R_ro_h,
    W_ro_h,
)
substitution6_ro_h_cd0 = solve_e6(
    determinant_ro_h_cd0, RO_H_ROWS, RO_H_COLUMNS, 3072
)
E5_ro_h_cd0 = sp.expand(
    determinant_ro_h_cd0.coeff_monomial(weight**5).subs(substitution6_ro_h_cd0)
)
assert_equal(coefficient(E5_ro_h_cd0, (5, 0, 0)), 3 * A * ell[7])
assert_equal(coefficient(E5_ro_h_cd0, (4, 1, 0)), -6 * A * ell[8])
assert_equal(
    coefficient(E5_ro_h_cd0, (4, 0, 1)), 6 * B * ell[7] - ell[1]
)
assert_equal(
    coefficient(E5_ro_h_cd0, (3, 1, 1)),
    -2 * (6 * B * ell[8] + T * a[3] - ell[2]),
)
assert_equal(coefficient(E5_ro_h_cd0, (3, 0, 2)), -2 * ell[4])
assert_equal(
    coefficient(E5_ro_h_cd0, (2, 1, 2)), -4 * (T * b[3] - ell[5])
)

forced_ro_h_e5 = {
    ell[1]: 6 * B * ell[7],
    ell[2]: 6 * B * ell[8] + T * a[3],
    ell[4]: 0,
    ell[5]: T * b[3],
}
det_after_ro_h_e5 = sp.factor(
    L.det().subs(substitution6_ro_h_cd0).subs(forced_ro_h_e5)
)
assert_equal(
    det_after_ro_h_e5,
    T
    * ell[7]
    * (6 * B * b[3] * ell[6] + a[3] * ell[3] - b[3] * ell[0]),
)

# If A != 0 then E5 forces l7=0.  The only invertible possibility has
# A=0.  On that subbranch, two E4 coefficients kill l8 and then l7.
E4_ro_h = sp.expand(
    determinant_ro_h_cd0.coeff_monomial(weight**4)
    .subs(substitution6_ro_h_cd0)
    .subs(forced_ro_h_e5)
    .subs(A, 0)
)
assert_equal(coefficient(E4_ro_h, (1, 1, 2)), -8 * ell[8] ** 2)
assert_equal(
    coefficient(E4_ro_h, (2, 1, 1)),
    -4 * (2 * b[0] * ell[8] - 2 * ell[6] * ell[8] - ell[7] ** 2),
)
assert exact_zero(det_after_ro_h_e5.subs(ell[7], 0))

# Sharpness witness: invertible and satisfies E9,...,E5, but not E4.
sharp_h2 = sp.Matrix([z**2, 2 * x * y + x * z + y**2, x * z])
sharp_h3 = sp.Matrix([2 * z * h_ro, x**2 * z, x * h_ro])
sharp_h4 = sp.Matrix([h_ro**2, h_ro * x**2, 0])
sharp_L = sp.Matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
sharp_det = sp.Poly(
    sp.expand(
        (
            sharp_L
            + weight * sharp_h2.jacobian(xyz)
            + weight**2 * sharp_h3.jacobian(xyz)
            + weight**3 * sharp_h4.jacobian(xyz)
        ).det()
    ),
    weight,
)
assert sharp_L.det() == -1
assert all(sharp_det.coeff_monomial(weight**degree) == 0 for degree in (9, 8, 7, 6, 5))
assert sp.factor(sharp_det.coeff_monomial(weight**4)) == 4 * x * y * h_ro

print("SIX_ENDPOINTS_E5_E4_SYMPY_PASS_0A77C2")
print("five endpoint slices die at E5; RO-smooth/H has a sharp E5 survivor and dies at E4")
