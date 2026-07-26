#!/usr/bin/env python3
"""Exact coefficient-matrix derivation of the D4-DN-2C E7 kernel.

This is deliberately a block-matrix calculation.  It does not call a
generic polynomial-system solver.  The three blocks are the coefficients
of r^2, r^1, and r^0 in

    J(Q,R) U_r - J(P,R) V_r + J(P,Q) T_r.
"""

from __future__ import annotations

import sys

import sympy as sp

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

p, q = sp.symbols("p q")


def jac(f: sp.Expr, g: sp.Expr) -> sp.Expr:
    return sp.expand(sp.diff(f, p) * sp.diff(g, q) - sp.diff(f, q) * sp.diff(g, p))


def binary_coefficients(f: sp.Expr, degree: int) -> list[sp.Expr]:
    polynomial = sp.Poly(sp.expand(f), p, q)
    return [
        polynomial.coeff_monomial(p ** (degree - j) * q**j)
        for j in range(degree + 1)
    ]


def exact_kernel(matrix: sp.Matrix) -> tuple[sp.Matrix, ...]:
    """Return a denominator-cleared primitive nullspace basis."""
    answer: list[sp.Matrix] = []
    for vector in matrix.nullspace():
        denominators = [sp.denom(value) for value in vector]
        scale = sp.ilcm(*[int(value) for value in denominators])
        integral = [sp.expand(scale * value) for value in vector]
        nonzero = [int(value) for value in integral if value != 0]
        content = abs(sp.igcd(*nonzero))
        integral = [sp.Integer(value // content) for value in integral]
        first = next(value for value in integral if value != 0)
        if first < 0:
            integral = [-value for value in integral]
        answer.append(sp.Matrix(integral))
    return tuple(answer)


h = (p + q) ** 2
P = sp.expand(h * p**2)
Q = sp.expand(h * q**2)
R = sp.expand(h * (p - 2 * q))

alpha = sp.factor(jac(Q, R))
beta = sp.factor(-jac(P, R))
gamma = sp.factor(jac(P, Q))

assert alpha == -6 * p * q * (p + q) ** 3
assert beta == 6 * p * (p + q) ** 3 * (p + 2 * q)
assert gamma == 8 * p * q * (p + q) ** 4

print("alpha =", alpha)
print("beta  =", beta)
print("gamma =", gamma)
print("gcd   =", sp.factor(sp.gcd(alpha, sp.gcd(beta, gamma))))

# r^2 block: (U,V) have constant r^3 coefficients.
u3, v3 = sp.symbols("u3 v3")
vars_r2 = (u3, v3)
M_r2, zero_r2 = sp.linear_eq_to_matrix(
    binary_coefficients(alpha * u3 + beta * v3, 5), vars_r2
)
assert zero_r2 == sp.zeros(6, 1)

# r^1 block: U_2,V_2 are binary linear, T_2 is constant.
u20, u21, v20, v21, t2 = sp.symbols("u20 u21 v20 v21 t2")
vars_r1 = (u20, u21, v20, v21, t2)
M_r1, zero_r1 = sp.linear_eq_to_matrix(
    binary_coefficients(
        alpha * (u20 * p + u21 * q)
        + beta * (v20 * p + v21 * q)
        + gamma * t2,
        6,
    ),
    vars_r1,
)
assert zero_r1 == sp.zeros(7, 1)

# r^0 block: U_1,V_1 are binary quadratics, T_1 is binary linear.
u10, u11, u12, v10, v11, v12, t10, t11 = sp.symbols(
    "u10 u11 u12 v10 v11 v12 t10 t11"
)
vars_r0 = (u10, u11, u12, v10, v11, v12, t10, t11)
M_r0, zero_r0 = sp.linear_eq_to_matrix(
    binary_coefficients(
        alpha * (u10 * p**2 + u11 * p * q + u12 * q**2)
        + beta * (v10 * p**2 + v11 * p * q + v12 * q**2)
        + gamma * (t10 * p + t11 * q),
        7,
    ),
    vars_r0,
)
assert zero_r0 == sp.zeros(8, 1)

for label, matrix, variables in (
    ("r2", M_r2, vars_r2),
    ("r1", M_r1, vars_r1),
    ("r0", M_r0, vars_r0),
):
    kernel = exact_kernel(matrix)
    assert matrix.rank() + len(kernel) == len(variables)
    assert all(matrix * vector == sp.zeros(matrix.rows, 1) for vector in kernel)
    print(f"{label}: shape={matrix.shape}, rank={matrix.rank()}, nullity={len(kernel)}")
    print("  variables:", variables)
    for index, vector in enumerate(kernel):
        print(f"  K{index} =", tuple(vector))

assert M_r2.rank() == 2
assert M_r1.rank() == 3
assert M_r0.rank() == 4
assert (2 - M_r2.rank()) + (5 - M_r1.rank()) + (8 - M_r0.rank()) == 6

print("D4_DN2C_E7_MATRIX_KERNEL_PASS")
