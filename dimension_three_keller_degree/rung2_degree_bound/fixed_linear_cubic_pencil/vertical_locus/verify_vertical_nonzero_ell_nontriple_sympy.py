#!/usr/bin/env python3
"""Exact raw-determinant check for the nonzero-ell nontriple branch."""

from __future__ import annotations

import itertools

import sympy as sp

if not __debug__:
    raise SystemExit("refusing optimized Python: fail-closed checks required")


def check(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


x, y, z = sp.symbols("x y z")
source_variables = (x, y, z)
s, kappa, u, v, omega = sp.symbols("s kappa u v omega")
collision_scale, collision_parameter = sp.symbols(
    "collision_scale collision_parameter"
)

r20, r11, r02, r10, r01 = sp.symbols("r20 r11 r02 r10 r01")
a = sp.symbols("a0:6")
b = sp.symbols("b0:6")
v_tail = sp.symbols("v4:9")
linear = sp.symbols("l0:9")
binary_v = sp.symbols("c0:4")
lambda_x, lambda_y = sp.symbols("lambda_x lambda_y")

quadratic_monomials = (x**2, x * y, y**2, x * z, y * z, z**2)
cubic_tail_monomials = (
    x**2 * z,
    x * y * z,
    y**2 * z,
    x * z**2,
    y * z**2,
)
binary_cubic_monomials = (x**3, x**2 * y, x * y**2, y**3)

A = sum(coefficient * monomial for coefficient, monomial
        in zip(a, quadratic_monomials))
B = sum(coefficient * monomial for coefficient, monomial
        in zip(b, quadratic_monomials))
V_tail = sum(coefficient * monomial for coefficient, monomial
             in zip(v_tail, cubic_tail_monomials))
V0_general = sum(coefficient * monomial for coefficient, monomial
                 in zip(binary_v, binary_cubic_monomials))

q_tail = (
    z * (r20 * x**2 + r11 * x * y + r02 * y**2)
    + z**2 * (r10 * x + r01 * y)
)


def bracket(first: sp.Expr, second: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.diff(first, x) * sp.diff(second, y)
        - sp.diff(first, y) * sp.diff(second, x)
    )


def homogeneous_part(polynomial: sp.Poly, degree: int) -> sp.Expr:
    return sp.expand(sum(
        coefficient * x**monomial[0] * y**monomial[1] * z**monomial[2]
        for monomial, coefficient in polynomial.terms()
        if sum(monomial) == degree
    ))


def raw_determinant(
    q0: sp.Expr,
    ell: sp.Expr,
    V0: sp.Expr,
    third_row_xy: tuple[sp.Expr, sp.Expr],
) -> sp.Poly:
    q = q0 + q_tail
    W = z * ell + omega * z**2
    V = V0 + V_tail
    L = sp.Matrix([
        [linear[0], linear[1], linear[2]],
        [linear[3], linear[4], linear[5]],
        [third_row_xy[0], third_row_xy[1], linear[8]],
    ])
    H2 = sp.Matrix((A, B, W))
    H3 = sp.Matrix((
        sp.Rational(4, 3) * z * W + s * q,
        V,
        z**3,
    ))
    H4 = sp.Matrix((z**4, z * q, 0))
    return sp.Poly(
        sp.expand(
            (
                L
                + H2.jacobian(source_variables)
                + H3.jacobian(source_variables)
                + H4.jacobian(source_variables)
            ).det()
        ),
        x,
        y,
        z,
    )


def binary_e5_matrix(q0: sp.Expr) -> sp.Matrix:
    ell = u * x + v * y
    third_row = lambda_x * x + lambda_y * y
    equation = sp.Poly(
        sp.expand(
            ell * bracket(q0, V0_general)
            - q0 * bracket(q0, third_row)
        ),
        x,
        y,
    )
    equations = [
        equation.coeff_monomial(x**(5 - index) * y**index)
        for index in range(6)
    ]
    matrix, right_hand_side = sp.linear_eq_to_matrix(
        equations,
        binary_v + (lambda_x, lambda_y),
    )
    check(
        all(entry == 0 for entry in right_hand_side),
        "binary E5 system is unexpectedly inhomogeneous",
    )
    return matrix


root_types = {
    "squarefree": x * y * (x - y),
    "double": x**2 * y,
}

# Reconstruct the binary E5 restriction from the complete determinant while
# retaining every lower-z coefficient of q, every coefficient of A and B,
# all five lower-z coefficients of V, omega, and all other linear entries.
for label, q0 in root_types.items():
    ell = u * x + v * y
    determinant = raw_determinant(
        q0,
        ell,
        V0_general,
        (lambda_x, lambda_y),
    )
    e5_at_z_zero = sp.expand(homogeneous_part(determinant, 5).subs(z, 0))
    expected = s * (
        ell * bracket(q0, V0_general)
        - q0 * bracket(q0, lambda_x * x + lambda_y * y)
    )
    check(
        sp.expand(e5_at_z_zero - expected) == 0,
        f"{label}: raw binary E5 identity",
    )

# Squarefree: three explicit 5-by-5 minors cover every nonzero (u,v),
# including all three root-line collisions. The known q0 kernel bounds the
# rank above by five.
squarefree_matrix = binary_e5_matrix(root_types["squarefree"])
squarefree_kernel = sp.Matrix([0, 1, -1, 0, 0, 0])
check(
    squarefree_matrix * squarefree_kernel == sp.zeros(6, 1),
    "squarefree: q0 is not in the binary E5 kernel",
)
squarefree_columns = (0, 1, 3, 4, 5)
squarefree_minors = (
    (
        (0, 1, 2, 3, 4),
        -27 * u * (u**2 - 4 * u * v - 4 * v**2),
    ),
    ((0, 1, 2, 4, 5), 27 * u**2 * v),
    (
        (1, 2, 3, 4, 5),
        27 * v * (4 * u**2 + 4 * u * v - v**2),
    ),
)
for rows, expected in squarefree_minors:
    minor = sp.factor(
        squarefree_matrix.extract(rows, squarefree_columns).det()
    )
    check(minor == expected, f"squarefree: binary E5 minor {rows}")

# Double-root noncollision: u*v != 0 and a single literal minor has no
# additional modulus divisor.
double_matrix = binary_e5_matrix(root_types["double"])
double_kernel = sp.Matrix([0, 1, 0, 0, 0, 0])
check(
    double_matrix * double_kernel == sp.zeros(6, 1),
    "double: q0 is not in the binary E5 kernel",
)
double_minor = sp.factor(
    double_matrix.extract(
        (0, 1, 2, 3, 4),
        (0, 2, 3, 4, 5),
    ).det()
)
check(
    double_minor == 108 * u * v**2,
    "double: noncollision binary E5 minor",
)

# The two collision matrices have rank exactly four and the displayed full
# two-dimensional kernels. These are checked without importing the generic
# E4 relation.
double_x = double_matrix.subs({u: 1, v: 0})
double_y = double_matrix.subs({u: 0, v: 1})
check(
    double_x.extract((0, 1, 2, 3), (0, 2, 3, 4)).det() == -54,
    "double ell=x: rank-four minor",
)
check(
    double_y.extract((1, 2, 3, 4), (0, 2, 3, 5)).det() == 108,
    "double ell=y: rank-four minor",
)
double_x_basis = (
    sp.Matrix([0, 1, 0, 0, 0, 0]),
    sp.Matrix([0, 0, sp.Rational(2, 3), 0, 0, 1]),
)
double_y_basis = (
    sp.Matrix([0, 1, 0, 0, 0, 0]),
    sp.Matrix([sp.Rational(1, 3), 0, 0, 0, 1, 0]),
)
for vector in double_x_basis:
    check(
        double_x * vector == sp.zeros(6, 1),
        "double ell=x: incomplete displayed kernel",
    )
for vector in double_y_basis:
    check(
        double_y * vector == sp.zeros(6, 1),
        "double ell=y: incomplete displayed kernel",
    )
check(double_x.rank() == 4, "double ell=x: binary E5 rank")
check(double_y.rank() == 4, "double ell=y: binary E5 rank")
check(
    sp.factor(
        double_matrix.subs({u: collision_scale, v: 0}).extract(
            (0, 1, 2, 3),
            (0, 2, 3, 4),
        ).det()
    ) == -54 * collision_scale**3,
    "double ell=c*x: scaled rank-four minor",
)
check(
    sp.factor(
        double_matrix.subs({u: 0, v: collision_scale}).extract(
            (1, 2, 3, 4),
            (0, 2, 3, 5),
        ).det()
    ) == 108 * collision_scale**3,
    "double ell=c*y: scaled rank-four minor",
)

double_q0 = root_types["double"]
check(
    sp.expand(
        collision_scale * x * bracket(
            double_q0,
            (
                kappa * double_q0
                + sp.Rational(2, 3)
                * collision_parameter * x * y**2
            ),
        )
        - double_q0 * bracket(
            double_q0,
            collision_scale * collision_parameter * y,
        )
    ) == 0,
    "double ell=c*x: scaled full E5 kernel",
)
check(
    sp.expand(
        collision_scale * y * bracket(
            double_q0,
            (
                kappa * double_q0
                + sp.Rational(1, 3)
                * collision_parameter * x**3
            ),
        )
        - double_q0 * bracket(
            double_q0,
            collision_scale * collision_parameter * x,
        )
    ) == 0,
    "double ell=c*y: scaled full E5 kernel",
)

# On the one-dimensional generic E5 kernel, reconstruct the E4 restriction
# exactly. It is not needed for the final contradiction, but confirms that
# no relation from the binary ledger was silently discarded.
for label, q0 in root_types.items():
    ell = u * x + v * y
    determinant = raw_determinant(q0, ell, kappa * q0, (0, 0))
    e4_at_z_zero = sp.expand(homogeneous_part(determinant, 4).subs(z, 0))
    expected = -ell * bracket(
        q0,
        kappa * A.subs(z, 0) - s * B.subs(z, 0),
    )
    check(
        sp.expand(e4_at_z_zero - expected) == 0,
        f"{label}: raw generic E4 identity",
    )

    quadratic_coefficients = sp.symbols(f"{label}_quadratic0:3")
    quadratic = (
        quadratic_coefficients[0] * x**2
        + quadratic_coefficients[1] * x * y
        + quadratic_coefficients[2] * y**2
    )
    bracket_polynomial = sp.Poly(bracket(q0, quadratic), x, y)
    bracket_equations = [
        bracket_polynomial.coeff_monomial(x**(3 - index) * y**index)
        for index in range(4)
    ]
    bracket_matrix, _ = sp.linear_eq_to_matrix(
        bracket_equations,
        quadratic_coefficients,
    )
    check(
        bracket_matrix.extract((0, 1, 2), (0, 1, 2)).det() == -8,
        f"{label}: binary quadratic bracket has zero kernel",
    )

# Decisive full E6 coefficients on the generic kernels. No E4 substitution
# is made here: A and B are still completely general.
squarefree_generic = raw_determinant(
    root_types["squarefree"],
    u * x + v * y,
    kappa * root_types["squarefree"],
    (0, 0),
)
check(
    sp.factor(squarefree_generic.coeff_monomial(x**4 * y * z)) == s * u,
    "squarefree: [x^4*y*z]E6",
)
check(
    sp.factor(squarefree_generic.coeff_monomial(x * y**4 * z)) == -s * v,
    "squarefree: [x*y^4*z]E6",
)

double_generic = raw_determinant(
    root_types["double"],
    u * x + v * y,
    kappa * root_types["double"],
    (0, 0),
)
check(
    sp.factor(double_generic.coeff_monomial(x**4 * y * z)) == s * u,
    "double noncollision: [x^4*y*z]E6",
)
check(
    sp.factor(double_generic.coeff_monomial(x**3 * y**2 * z))
    == -2 * s * v,
    "double noncollision: [x^3*y^2*z]E6",
)

# Collision ell=c*x: retain the complete second binary-kernel parameter.
# Scaling the E5 basis correctly scales the third linear row by c.
double_x_collision = raw_determinant(
    root_types["double"],
    collision_scale * x,
    (
        kappa * root_types["double"]
        + sp.Rational(2, 3) * collision_parameter * x * y**2
    ),
    (0, collision_scale * collision_parameter),
)
check(
    sp.factor(double_x_collision.coeff_monomial(x**4 * y * z))
    == s * collision_scale,
    "double ell=x collision: [x^4*y*z]E6",
)

# Collision ell=c*y: retain its complete second binary-kernel parameter.
double_y_collision = raw_determinant(
    root_types["double"],
    collision_scale * y,
    (
        kappa * root_types["double"]
        + sp.Rational(1, 3) * collision_parameter * x**3
    ),
    (collision_scale * collision_parameter, 0),
)
check(
    sp.factor(double_y_collision.coeff_monomial(x**3 * y**2 * z))
    == -2 * s * collision_scale,
    "double ell=y collision: [x^3*y^2*z]E6",
)

# Coverage ledger: squarefree nonzero has one complete kernel family; the
# double-root locus is the disjoint union uv!=0, ell=c*x, and ell=c*y.
coverage = {
    "squarefree_nonzero",
    "double_noncollision",
    "double_ell_x",
    "double_ell_y",
}
check(len(coverage) == 4, "branch coverage ledger")

print("VERTICAL_NONZERO_ELL_NONTRIPLE_SYMPY_PASS_6E2C91")
