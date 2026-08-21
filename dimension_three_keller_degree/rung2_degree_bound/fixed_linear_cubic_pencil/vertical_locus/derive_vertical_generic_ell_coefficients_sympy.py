#!/usr/bin/env python3
"""Derive the decisive E6 coefficients after the generic binary E5/E4 solve."""

from __future__ import annotations

import sympy as sp


x, y, z = sp.symbols("x y z")
s, u, v, w, k, c = sp.symbols("s u v w k c", nonzero=True)
r20, r11, r02, r10, r01 = sp.symbols("r20 r11 r02 r10 r01")
a = sp.symbols("a0:6")
b3, b4, b5 = sp.symbols("b3 b4 b5")
t4, t5, t6, t7, t8 = sp.symbols("t4 t5 t6 t7 t8")
l = sp.symbols("l0:9")

quadratics = (x**2, x * y, y**2, x * z, y * z, z**2)
A = sum(coefficient * monomial for coefficient, monomial in zip(a, quadratics))
B = (
    k * (a[0] * x**2 + a[1] * x * y + a[2] * y**2) / s
    + b3 * x * z
    + b4 * y * z
    + b5 * z**2
)
W = z * (u * x + v * y + w * z)
L = sp.Matrix(((l[0], l[1], l[2]), (l[3], l[4], l[5]), (0, 0, l[8])))

root_types = {
    "squarefree": x * y * (x - y),
    "double": x**2 * y,
}


def bracket(left: sp.Expr, right: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.diff(left, x) * sp.diff(right, y)
        - sp.diff(left, y) * sp.diff(right, x)
    )


def print_binary_pivot(label: str, q0: sp.Expr, ell0: sp.Expr) -> None:
    p = sp.symbols(f"{label}_p0:4")
    rr, tt = sp.symbols(f"{label}_rr {label}_tt")
    candidate = p[0] * x**3 + p[1] * x**2 * y + p[2] * x * y**2 + p[3] * y**3
    row = rr * x + tt * y
    equation = sp.Poly(
        sp.expand(ell0 * bracket(q0, candidate) - q0 * bracket(q0, row)),
        x,
        y,
    )
    matrix, _ = sp.linear_eq_to_matrix(equation.coeffs(), p + (rr, tt))
    minors = []
    for rows in __import__("itertools").combinations(range(matrix.rows), 5):
        for columns in __import__("itertools").combinations(range(matrix.cols), 5):
            minor = sp.factor(matrix.extract(rows, columns).det())
            if minor != 0:
                minors.append(minor)
            if minor != 0 and not minor.has(c):
                print(label, "binary pivot", rows, columns, minor)
                return
    gcd = sp.factor(sp.gcd_list(minors))
    print(label, "binary pivot NONE; gcd", gcd, "factors", sorted(set(map(str, minors))))


print_binary_pivot("squarefree_chart", root_types["squarefree"], x + c * y)
print_binary_pivot("squarefree_endpoint", root_types["squarefree"], y)
print_binary_pivot("double_generic", root_types["double"], x + y)

for label, q0 in root_types.items():
    q = (
        q0
        + z * (r20 * x**2 + r11 * x * y + r02 * y**2)
        + z**2 * (r10 * x + r01 * y)
    )
    V = (
        k * q0
        + z * (t4 * x**2 + t5 * x * y + t6 * y**2)
        + z**2 * (t7 * x + t8 * y)
    )
    H2 = sp.Matrix((A, B, W))
    H3 = sp.Matrix((sp.Rational(4, 3) * z * W + s * q, V, z**3))
    H4 = sp.Matrix((z**4, z * q, 0))
    determinant = sp.Poly(
        sp.expand(
            (L + H2.jacobian((x, y, z)) + H3.jacobian((x, y, z))
             + H4.jacobian((x, y, z))).det()
        ),
        x,
        y,
        z,
    )
    coefficients = {
        monomial: sp.factor(coefficient)
        for monomial, coefficient in determinant.terms()
        if sum(monomial) == 6 and monomial[2] == 1
    }
    print(label)
    for monomial, coefficient in coefficients.items():
        print(monomial, coefficient)
