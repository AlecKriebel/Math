#!/usr/bin/env python3
"""Symbolic E3 descent on the punctured F=G overlap, normalized by k=1."""

from __future__ import annotations

import sys

import sympy as sp

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

p, q, r, weight = sp.symbols("p q r weight")
coords = (p, q, r)
h = (p + q) ** 2
P = sp.expand(h * p**2)
Q = sp.expand(h * q**2)
R = sp.expand(h * (p - 2 * q))

t1, t2, u3, v1, v2, v3 = sp.symbols("t1 t2 u3 v1 v2 v3")
a2, b1, b2, l2, l6, l7 = sp.symbols("a2 b1 b2 l2 l6 l7")
u0, u1, u2, v0 = sp.symbols("u0 u1 u2 v0")
a0, a1, b0 = sp.symbols("a0 a1 b0")
l0, l1, l3, l4 = sp.symbols("l0 l1 l3 l4")

t0 = t1 - t2
zed = 6 * v1 - 9 * v2 + 9 * v3
br0 = zed / 3
ell33 = t1 - 2 * t2 - sp.Rational(3, 2) * v1 + 3 * v2 - sp.Rational(9, 2) * v3
ar1 = sp.Rational(4, 3) * (t1 - t2) - sp.Rational(3, 2) * u3 + 2 * v2 - 3 * v3
ar0 = ar1 + 2 * br0 - 3 * v1 + 4 * v2 - 3 * v3
br1 = v1 - v2
vquadratic = v1**2 - 3 * v1 * v2 + 3 * v1 * v3 + 2 * v2**2 - 3 * v2 * v3
l5 = b1 - 2 * b2 - vquadratic / 2

U = (
    u0 * p**3 + u1 * p**2 * q + u2 * p * q**2 + u3 * q**3
    + 2 * r * p * (p + q)
)
V = (
    v0 * p**3 + v1 * p**2 * q + v2 * p * q**2 + v3 * q**3
    - 2 * r * q * (p + q)
)
T = t0 * p**2 + t1 * p * q + t2 * q**2 + 3 * r * (p + q)
A = (
    a0 * p**2 + a1 * p * q + a2 * q**2
    + r * (ar0 * p + ar1 * q) + r**2
)
B = (
    b0 * p**2 + b1 * p * q + b2 * q**2
    + r * (br0 * p + br1 * q) + r**2
)
linear = sp.Matrix(((l0, l1, l2), (l3, l4, l5), (l6, l7, ell33)))
H2 = sp.Matrix((A, B, T))
H3 = sp.Matrix((U, V, R))
H4 = sp.Matrix((P, Q, 0))
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


def coeffs(expression: sp.Expr, degree: int) -> sp.Matrix:
    polynomial = sp.Poly(sp.expand(expression), p, q, r)
    return sp.Matrix(
        [
            polynomial.coeff_monomial(p**i * q ** (degree-k-i) * r**k)
            for k in range(degree + 1)
            for i in range(degree-k, -1, -1)
        ]
    )


def solve_by_pivot(equations: sp.Matrix, variables: tuple[sp.Symbol, ...]):
    matrix = equations.jacobian(variables)
    constant = equations.subs({variable: 0 for variable in variables})
    assert equations == matrix * sp.Matrix(variables) + constant
    pivot_columns = matrix.rref()[1]
    assert len(pivot_columns) == len(variables)
    rows = next(
        rows
        for rows in sp.utilities.iterables.combinations(range(matrix.rows), len(variables))
        if matrix.extract(rows, range(len(variables))).det() != 0
    )
    pivot = matrix.extract(rows, range(len(variables)))
    solution = dict(
        zip(
            variables,
            tuple(-pivot.inv() * constant.extract(rows, (0,))),
        )
    )
    assert all(sp.cancel(value.subs(solution)) == 0 for value in equations)
    return solution, rows, sp.factor(pivot.det())


eq6 = coeffs(determinant.coeff_monomial(weight**6), 6)
sol6, rows6, det6 = solve_by_pivot(eq6, (u0, u1, u2, v0))
print("E6_PIVOT", rows6, det6)

eq5 = coeffs(determinant.coeff_monomial(weight**5).subs(sol6), 5)
sol5, rows5, det5 = solve_by_pivot(eq5, (a0, a1, b0))
print("E5_PIVOT", rows5, det5)

eq4 = coeffs(
    determinant.coeff_monomial(weight**4).subs(sol6).subs(sol5),
    4,
)
M4 = eq4.jacobian((l0, l3))
c4 = eq4.subs({l0: 0, l3: 0})
assert eq4 == M4 * sp.Matrix((l0, l3)) + c4
assert M4.rank() == 2
rows4 = next(
    rows
    for rows in sp.utilities.iterables.combinations(range(M4.rows), 2)
    if M4.extract(rows, (0, 1)).det() != 0
)
pivot4 = M4.extract(rows4, (0, 1))
sol4 = dict(zip((l0, l3), tuple(-pivot4.inv() * c4.extract(rows4, (0,)))))
residual4 = tuple(sp.cancel(value.subs(sol4)) for value in eq4)
assert all(value == 0 for value in residual4)
print("E4_PIVOT", rows4, sp.factor(pivot4.det()))

linear_done = sp.simplify(linear.subs(sol4))
det_linear = sp.factor(linear_done.det())
eq3 = coeffs(
    determinant.coeff_monomial(weight**3)
    .subs(sol6)
    .subs(sol5)
    .subs(sol4),
    3,
)
nonzero3 = tuple(sp.factor(value) for value in eq3[:4, 0])
assert all(value == 0 for value in eq3[4:, 0])
assert sp.expand(nonzero3[0] - nonzero3[1] + nonzero3[2] - nonzero3[3]) == 0
print("DET_LINEAR =", det_linear)
for index, value in enumerate(nonzero3):
    print("E3_BINARY", index, "=", value)

common = sp.factor(sp.gcd(nonzero3[0], nonzero3[1]))
assert common != 0
assert all(sp.rem(value, common) == 0 for value in nonzero3)
quotients3 = tuple(sp.cancel(value / common) for value in nonzero3)
assert sp.expand(
    quotients3[0] - quotients3[1] + quotients3[2] - quotients3[3]
) == 0

# If the common E3 factor vanishes, det(L) vanishes from the displayed
# factorization.  On its complement, the quotient equations solve
# triangularly for b1, a2, and l6; substituting those three equations
# kills the other quotient and the remaining determinant factor.
solution_b1 = sp.solve(quotients3[0], b1, dict=True)[0]
after_b1 = tuple(sp.cancel(value.subs(solution_b1)) for value in quotients3)
solution_a2 = sp.solve(after_b1[3], a2, dict=True)[0]
after_a2 = tuple(sp.cancel(value.subs(solution_a2)) for value in after_b1)
solution_l6 = sp.solve(after_a2[1], l6, dict=True)[0]
triangular_solution = {}
triangular_solution.update(solution_b1)
triangular_solution.update(solution_a2)
triangular_solution.update(solution_l6)
assert all(
    sp.cancel(value.subs(solution_l6)) == 0 for value in after_a2
)
determinant_quotient_remainder = sp.factor(
    sp.cancel((det_linear / common).subs(triangular_solution))
)
print("DET_QUOTIENT_AFTER_E3 =", determinant_quotient_remainder)
common_after_e3 = sp.factor(common.subs(triangular_solution))
print("COMMON_AFTER_E3 =", common_after_e3)
assert common_after_e3 == 0
print("E3_COMMON_FACTOR =", common)
print("E3_TRIANGULAR_PIVOTS =", (b1, a2, l6))
print("E3_FORCES_DET_LINEAR_ZERO")

print("D4_DN2C_OVERLAP_E3_SYMBOLIC_PASS")
