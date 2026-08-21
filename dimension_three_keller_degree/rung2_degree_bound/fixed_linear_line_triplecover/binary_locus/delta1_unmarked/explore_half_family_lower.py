#!/usr/bin/env python3
"""Full lower determinant on the exact-delta1 a3=1/2 contact family."""

from __future__ import annotations

import sympy as sp


p, q, r, tau, z = sp.symbols("p q r tau z")
variables = (p, q, r)


def binary_form(prefix: str, degree: int):
    coeffs = sp.symbols(f"{prefix}0:{degree + 1}")
    value = sum(
        coeffs[index] * p ** (degree - index) * q**index
        for index in range(degree + 1)
    )
    return value, coeffs


A3 = p * q**2 + sp.Rational(1, 2) * q**3
B3 = p**3 + p**2 * q - sp.Rational(1, 8) * q**3
R = (
    p**3
    + sp.Rational(3, 4) * p**2 * q
    + (4 * z + sp.Rational(1, 8)) * p * q**2
    + z * q**3
)
P, Q = p * A3, p * B3

direction = lambda f: sp.diff(f, q) - sp.Rational(1, 4) * sp.diff(f, p)
Nu, Nv, Nt = [sp.cancel(direction(form) / q) for form in (P, Q, R)]

U0, u = binary_form("u", 3)
V0, v = binary_form("v", 3)
T0, t = binary_form("t", 2)
A0, x = binary_form("x", 2)
B0, y = binary_form("y", 2)

x3, x4, x5, y3, y4, y5 = sp.symbols("x3 x4 x5 y3 y4 y5")
U = U0 + r * Nu
V = V0 + r * Nv
T = T0 + r * Nt
A = A0 + r * (x3 * p + x4 * q) + x5 * r**2
B = B0 + r * (y3 * p + y4 * q) + y5 * r**2

H4 = sp.Matrix((P, Q, 0))
H3 = sp.Matrix((U, V, R))
H2 = sp.Matrix((A, B, T))
l = sp.symbols("l11 l12 l13 l21 l22 l23 l31 l32 l33")
L = sp.Matrix(3, 3, l)
weighted = sp.Poly(
    sp.expand(
        (
            L
            + tau * H2.jacobian(variables)
            + tau**2 * H3.jacobian(variables)
            + tau**3 * H4.jacobian(variables)
        ).det()
    ),
    tau,
)
E = {
    degree: sp.Poly(
        sp.expand(weighted.coeff_monomial(tau**degree)), p, q, r
    )
    for degree in (8, 7, 6, 5, 4, 3, 2, 1)
}
assert E[8].is_zero and E[7].is_zero


def equations(poly: sp.Poly):
    return [coefficient for _, coefficient in poly.terms()]


def main() -> None:
    unknowns = (x5, y5, x3, x4, y3, y4, l[8])
    matrix, rhs = sp.linear_eq_to_matrix(equations(E[6]), unknowns)
    print("E6 shape", matrix.shape, "rank", matrix.rank())
    left_kernel = matrix.T.nullspace()
    print("E6 compatibility count", len(left_kernel))
    compatibility = []
    for index, vector in enumerate(left_kernel):
        value = sp.factor((vector.T * rhs)[0])
        compatibility.append(value)
        print("E6 compatibility", index, value)
    t0_solution = sp.solve(compatibility[0], t[0], dict=True)[0][t[0]]
    print("E6 t0 =", sp.factor(t0_solution))
    for index, value in enumerate(compatibility[1:], start=1):
        reduced = sp.factor(value.subs({t[0]: t0_solution}))
        if reduced != 0:
            print("E6 residual compatibility", index, reduced)
    _, independent_rows = matrix.T.rref()
    square = matrix.extract(independent_rows, range(len(unknowns)))
    square_rhs = rhs.extract(independent_rows, [0])
    solution = [sp.factor(value) for value in square.inv() * square_rhs]
    print("E6 independent rows", independent_rows)
    for variable, value in zip(unknowns, solution):
        print(variable, "=", value)
    gauge = {
        u[0]: 0,
        v[0]: 0,
        t[0]: 0,
        t[2]: 0,
        v[1]: -sp.Rational(3, 8) * u[1],
        t[1]: (64 * z - 1) * u[1] / 16,
    }
    print("E6 gauge u0=v0=t0=t2=0")
    for variable, value in zip(unknowns, solution):
        print(variable, "=", sp.factor(value.subs(gauge)))


if __name__ == "__main__":
    main()
