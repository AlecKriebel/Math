#!/usr/bin/env python3
"""Independent exact checks for the finite-critical F=0 resonance chart.

This implementation uses direct determinant expansion in a bookkeeping
variable.  It does not import either supplied verifier.
"""

from __future__ import annotations

from itertools import product

import sympy as sp


if not __debug__:
    raise SystemExit("ERROR: exact audit refuses Python optimized mode (-O)")

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
            coefficient * monomial
            for coefficient, monomial in zip(coefficients, monomials(degree))
        ),
        coefficients,
    )


def coefficients(form_value: sp.Expr, degree: int) -> list[sp.Expr]:
    polynomial = sp.Poly(sp.expand(form_value), x, y, z)
    return [
        polynomial.coeff_monomial(monomial)
        for monomial in monomials(degree)
    ]


def coefficient(form_value: sp.Expr, i: int, j: int, k: int) -> sp.Expr:
    return sp.Poly(sp.expand(form_value), x, y, z).coeff_monomial(
        x**i * y**j * z**k
    )


def jacobian(first: sp.Expr, second: sp.Expr, third: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.Matrix([first, second, third]).jacobian(xyz).det()
    )


def weighted_coefficient(
    linear: sp.Matrix,
    quadratic: sp.Matrix,
    cubic: sp.Matrix,
    quartic: sp.Matrix,
    degree_weight: int,
) -> sp.Expr:
    """Expand by row degrees, independently of the supplied helper."""

    jacobians = tuple(
        vector.jacobian(xyz)
        for vector in (linear, quadratic, cubic, quartic)
    )
    answer = 0
    for row_degrees in product(range(4), repeat=3):
        if sum(row_degrees) != degree_weight:
            continue
        answer += sp.Matrix.vstack(
            *(
                jacobians[row_degrees[row]][row, :]
                for row in range(3)
            )
        ).det()
    return sp.expand(answer)


def coefficient_vector(
    value: sp.Expr, degree: int
) -> sp.Matrix:
    polynomial = sp.Poly(sp.expand(value), x, y, z)
    return sp.Matrix(
        [
            polynomial.coeff_monomial(monomial)
            for monomial in monomials(degree)
        ]
    )


def assert_associate(left: sp.Expr, right: sp.Expr) -> None:
    quotient = sp.cancel(left / right)
    assert quotient.is_Rational and quotient != 0, (left, right, quotient)


t = sp.symbols("t")
c = 3 * t / (2 * t + 1)
D = (t - 1) * (2 * t + 1)
H4 = sp.Matrix([(p - t * q) ** 2, (p - q) ** 2, 0])
R = x * (p - c * q)

# Endpoint accounting is polynomial and precedes every division.
endpoint_c = sp.symbols("endpoint_c")
Fchart = 3 * t - endpoint_c * (2 * t + 1)
assert Fchart.subs(t, -sp.Rational(1, 2)) == -sp.Rational(3, 2)
assert Fchart.subs(t, 0) == -endpoint_c
assert (t - 1).subs(t, 1) == 0


def raw_e7_matrix() -> tuple[
    sp.Expr,
    sp.Matrix,
    sp.Expr,
    sp.Expr,
    tuple[sp.Symbol, ...],
    tuple[sp.Symbol, ...],
    tuple[sp.Symbol, ...],
]:
    U, u = form("raw_u", 3)
    V, v = form("raw_v", 3)
    W, w = form("raw_w", 2)
    E7 = (
        jacobian(H4[0], H4[1], W)
        + jacobian(H4[0], V, R)
        + jacobian(U, H4[1], R)
    )
    matrix, rhs = sp.linear_eq_to_matrix(
        coefficients(E7, 7), u + v + w
    )
    assert rhs == sp.zeros(len(monomials(7)), 1)
    return E7, matrix, U, V, u, v, w


E7_raw, raw_matrix, raw_U, raw_V, raw_u, raw_v, raw_w = raw_e7_matrix()
raw_unknowns = raw_u + raw_v + raw_w

# Select a rank-14 minor using exact t=2 pivoting, then retain its symbolic
# determinant as a specialization-safe certificate.
raw_at_two = raw_matrix.subs(t, 2)
raw_pivot_columns = raw_at_two.rref()[1]
assert len(raw_pivot_columns) == 14
raw_pivot_rows = (
    raw_at_two[:, raw_pivot_columns].T.rref()[1]
)
assert len(raw_pivot_rows) == 14
raw_minor = sp.factor(
    raw_matrix.extract(raw_pivot_rows, raw_pivot_columns).det()
)
assert_associate(
    raw_minor,
    t**6 * (t - 1) ** 6 / (2 * t + 1) ** 14,
)

# The displayed generic gauge plus the two target shears and two source
# translations supplies twelve independent raw kernel directions.  Together
# with the preceding minor, this proves rank=14 and proves the converse.
A, B = sp.symbols("A B")
w0, wr, ws, wm, wq, wn = sp.symbols("w0 wr ws wm wq wn")
W_gauge = w0 * p + wr * x * y + ws * x * z + wm * y**2 + wq * q + wn * z**2
U_gauge = (
    A * x * q
    - sp.Rational(4, 3) * D * (wm * x * y**2 + wn * x * z**2)
    - 4 * t * D * (wr * y**2 * z + ws * y * z**2)
    / (3 * (2 * t - 1))
)
V_gauge = (
    B * x * q
    + 4
    * D
    * (
        wr * (x**2 * y - y**2 * z)
        + ws * (x**2 * z - y * z**2)
    )
    / (3 * t * (2 * t - 1))
)
assert sp.cancel(
    jacobian(H4[0], H4[1], W_gauge)
    + jacobian(H4[0], V_gauge, R)
    + jacobian(U_gauge, H4[1], R)
) == 0

shear_u, shear_v, translate_y, translate_z = sp.symbols(
    "shear_u shear_v translate_y translate_z"
)
U_raw_family = (
    U_gauge
    + shear_u * x**3
    + translate_y * sp.diff(H4[0], y)
    + translate_z * sp.diff(H4[0], z)
)
V_raw_family = (
    V_gauge
    + shear_v * x**3
    + translate_y * sp.diff(H4[1], y)
    + translate_z * sp.diff(H4[1], z)
)
W_raw_family = (
    W_gauge
    + translate_y * sp.diff(R, y)
    + translate_z * sp.diff(R, z)
)
raw_parameters = (
    A,
    B,
    w0,
    wr,
    ws,
    wm,
    wq,
    wn,
    shear_u,
    shear_v,
    translate_y,
    translate_z,
)
raw_family_vector = sp.Matrix.vstack(
    coefficient_vector(U_raw_family, 3),
    coefficient_vector(V_raw_family, 3),
    coefficient_vector(W_raw_family, 2),
)
raw_family_matrix = raw_family_vector.jacobian(raw_parameters)
assert sp.simplify(raw_matrix * raw_family_matrix) == sp.zeros(36, 12)
family_at_two = raw_family_matrix.subs(t, 2)
family_pivot_rows = family_at_two.T.rref()[1]
assert len(family_pivot_rows) == 12
family_minor = sp.factor(
    raw_family_matrix.extract(family_pivot_rows, range(12)).det()
)
assert_associate(
    family_minor,
    t**4 * (t - 1) ** 4 * (2 * t + 1) ** 4 / (2 * t - 1) ** 2,
)

# The alternate t=1/2 gauge is an independent complete kernel at the only
# point where the preceding translation section degenerates.
half_substitution = {t: sp.Rational(1, 2)}
half_R = R.subs(half_substitution)
half_H4 = H4.subs(half_substitution)
half_U = A * x * q + sp.Rational(4, 3) * (
    wr * x**2 * y
    + ws * x**2 * z
    + wm * x * y**2
    + wn * x * z**2
)
half_V = B * x * q
assert (
    jacobian(half_H4[0], half_H4[1], W_gauge)
    + jacobian(half_H4[0], half_V, half_R)
    + jacobian(half_U, half_H4[1], half_R)
    == 0
)
half_family_vector = sp.Matrix.vstack(
    coefficient_vector(
        half_U
        + shear_u * x**3
        + translate_y * sp.diff(half_H4[0], y)
        + translate_z * sp.diff(half_H4[0], z),
        3,
    ),
    coefficient_vector(
        half_V
        + shear_v * x**3
        + translate_y * sp.diff(half_H4[1], y)
        + translate_z * sp.diff(half_H4[1], z),
        3,
    ),
    coefficient_vector(
        W_gauge
        + translate_y * sp.diff(half_R, y)
        + translate_z * sp.diff(half_R, z),
        2,
    ),
)
half_family_matrix = half_family_vector.jacobian(raw_parameters)
assert raw_matrix.subs(half_substitution) * half_family_matrix == sp.zeros(
    36, 12
)
assert half_family_matrix.rank() == 12
assert raw_matrix.subs(half_substitution).rank() == 14

print("  PASS raw E7 rank 14 and complete generic/half kernels")


# Direct E6 square obstructions, with all lower coefficients retained.
U2, u2 = form("square_u", 2)
V2, v2 = form("square_v", 2)
ell = sp.symbols("square_ell0:9")
L = sp.Matrix(3, 3, ell) * sp.Matrix([x, y, z])
E6 = weighted_coefficient(
    L,
    sp.Matrix([U2, V2, W_gauge]),
    sp.Matrix([U_gauge, V_gauge, R]),
    H4,
    6,
)
assert sp.factor(coefficient(E6, 2, 4, 0)) == -sp.Rational(16, 3) * D * wm**2
assert sp.factor(coefficient(E6, 2, 0, 4)) == sp.Rational(16, 3) * D * wn**2
E6_reduced = sp.expand(E6.subs({wm: 0, wn: 0}))
square_factor = (
    sp.Rational(8, 3)
    * t
    * (t - 1) ** 2
    * (2 * t + 1)
    / (2 * t - 1) ** 2
)
Cy = (
    t**2 * coefficient(E6_reduced, 4, 2, 0)
    + t * coefficient(E6_reduced, 2, 3, 1)
    + coefficient(E6_reduced, 0, 4, 2)
)
Cz = (
    t**2 * coefficient(E6_reduced, 4, 0, 2)
    + t * coefficient(E6_reduced, 2, 1, 3)
    + coefficient(E6_reduced, 0, 2, 4)
)
assert sp.factor(Cy) == -square_factor * wr**2
assert sp.factor(Cz) == square_factor * ws**2

half_E6 = weighted_coefficient(
    L,
    sp.Matrix([U2, V2, W_gauge]),
    sp.Matrix([half_U, half_V, half_R]),
    half_H4,
    6,
)
assert coefficient(half_E6, 2, 4, 0) == sp.Rational(16, 3) * wm**2
assert coefficient(half_E6, 2, 0, 4) == -sp.Rational(16, 3) * wn**2
half_reduced = sp.expand(half_E6.subs({wm: 0, wn: 0}))
half_Cy = (
    sp.Rational(1, 4) * coefficient(half_reduced, 4, 2, 0)
    + sp.Rational(1, 2) * coefficient(half_reduced, 2, 3, 1)
    + coefficient(half_reduced, 0, 4, 2)
)
half_Cz = (
    sp.Rational(1, 4) * coefficient(half_reduced, 4, 0, 2)
    + sp.Rational(1, 2) * coefficient(half_reduced, 2, 1, 3)
    + coefficient(half_reduced, 0, 2, 4)
)
assert half_Cy == -sp.Rational(2, 3) * wr**2
assert half_Cz == sp.Rational(2, 3) * ws**2

print("  PASS direct generic/half E6 square obstructions")


# Once the four modes vanish, reconstruct the entire E6 solution and the
# common E5 column-kernel without dividing by a lower coefficient.
Ai, Bi, wi0, wiq = sp.symbols("Ai Bi wi0 wiq")
H3_invariant = sp.Matrix([Ai * x * q, Bi * x * q, R])
H2_invariant = sp.Matrix([U2, V2, wi0 * p + wiq * q])
E6_invariant = weighted_coefficient(
    L, H2_invariant, H3_invariant, H4, 6
)
K = -sp.Rational(4, 3) * D
solution = {
    u2[1]: K * ell[7],
    u2[2]: K * ell[8],
    u2[3]: 0,
    u2[5]: 0,
    v2[1]: 0,
    v2[2]: 0,
    v2[3]: 0,
    v2[5]: 0,
}
assert sp.expand(E6_invariant.subs(solution)) == 0

pivot_variables = (
    u2[1],
    u2[2],
    u2[3],
    u2[5],
    v2[1],
    v2[2],
    v2[3],
    v2[5],
)
E6_pivot_matrix = sp.Matrix(
    [
        [sp.diff(equation, variable) for variable in pivot_variables]
        for equation in coefficients(E6_invariant, 6)
    ]
)
pivot_rows = E6_pivot_matrix.subs(t, 2).T.rref()[1]
assert len(pivot_rows) == 8
E6_minor = sp.factor(
    E6_pivot_matrix.extract(pivot_rows, range(8)).det()
)
assert_associate(
    E6_minor,
    t**4 * (t - 1) ** 4 / (2 * t + 1) ** 8,
)

E5 = weighted_coefficient(
    L,
    H2_invariant.subs(solution),
    H3_invariant,
    H4,
    5,
).subs(solution)
E5_polynomial = sp.Poly(E5, x, y, z)
y_equations = [
    E5_polynomial.coeff_monomial(monomial)
    for monomial in (x**4 * y, x**2 * y**2 * z, y**3 * z**2)
]
z_equations = [
    E5_polynomial.coeff_monomial(monomial)
    for monomial in (x**4 * z, x**2 * y * z**2, y**2 * z**3)
]
My, rhs_y = sp.linear_eq_to_matrix(
    y_equations, (ell[1], ell[4], ell[7])
)
Mz, rhs_z = sp.linear_eq_to_matrix(
    z_equations, (ell[2], ell[5], ell[8])
)
assert rhs_y == sp.zeros(3, 1)
assert rhs_z == sp.zeros(3, 1)
assert sp.simplify(My + Mz) == sp.zeros(3)
assert (
    sp.factor(My.extract((0, 1), (0, 1)).det())
    == -36 * t * (t - 1) / (2 * t + 1) ** 2
)

print("  PASS complete lower E6 converse and common E5 column-kernel")
print("PASS: independent exact finite-critical F/G chart audit")
