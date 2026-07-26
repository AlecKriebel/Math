#!/usr/bin/env python3
"""Low-complexity punctured-intersection representative through E3.

This is a direct determinant calculation, independent of the general
elimination formulas.  It chooses k=1 and a sparse point on the overlap
of the two E5 linear branches, then solves E6, E5, and E4 by exact
coefficient matrices.  Finally it evaluates E3.
"""

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

# Sparse free coefficients.  The q^3 coefficient of U0 and the last
# three coefficients of V0 have been set to zero.
u0, u1, u2, v0 = sp.symbols("u0 u1 u2 v0")
a0, a1, b0 = sp.symbols("a0 a1 b0")
l0, l1, l3, l4 = sp.symbols("l0 l1 l3 l4")

U0 = u0 * p**3 + u1 * p**2 * q + u2 * p * q**2
V0 = v0 * p**3
U = U0 + 2 * r * p * (p + q)
V = V0 - 2 * r * q * (p + q)
T = p**2 + p * q + 3 * r * (p + q)

# On the F=G overlap with the above sparse choice:
# ar0=ar1=4/3, br0=br1=0, ar2=br2=2, and L33=1.
A = a0 * p**2 + a1 * p * q + sp.Rational(4, 3) * r * (p + q) + r**2
B = b0 * p**2 + r**2
linear = sp.Matrix(
    (
        (l0, l1, 0),
        (l3, l4, 0),
        (0, 0, 1),
    )
)

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


def coefficient_vector(expression: sp.Expr, degree: int) -> sp.Matrix:
    polynomial = sp.Poly(sp.expand(expression), p, q, r)
    return sp.Matrix(
        [
            polynomial.coeff_monomial(p**i * q ** (degree - k - i) * r**k)
            for k in range(degree + 1)
            for i in range(degree - k, -1, -1)
        ]
    )


def exact_linear_solve(
    equations: sp.Matrix,
    variables: tuple[sp.Symbol, ...],
    expected_rank: int,
) -> dict[sp.Symbol, sp.Expr]:
    matrix = equations.jacobian(variables)
    constant = equations.subs({variable: 0 for variable in variables})
    assert equations == matrix * sp.Matrix(variables) + constant
    assert matrix.rank() == expected_rank
    assert matrix.row_join(-constant).rank() == expected_rank
    solution_set = sp.linsolve((matrix, -constant), variables)
    solution_tuple = tuple(next(iter(solution_set)))
    assert len(solution_tuple) == len(variables)
    return dict(zip(variables, solution_tuple))


E6 = determinant.coeff_monomial(weight**6)
equations6 = coefficient_vector(E6, 6)
solution6 = exact_linear_solve(equations6, (u0, u1, u2, v0), 4)
assert all(
    sp.factor(value.subs(solution6)) == 0 for value in equations6
)
print("E6_SOLUTION", solution6)

E5 = determinant.coeff_monomial(weight**5)
equations5 = coefficient_vector(E5.subs(solution6), 5)
solution5 = exact_linear_solve(equations5, (a0, a1, b0), 3)
assert all(
    sp.factor(value.subs(solution5)) == 0 for value in equations5
)
print("E5_SOLUTION", solution5)

E4 = determinant.coeff_monomial(weight**4)
equations4 = coefficient_vector(E4.subs(solution6).subs(solution5), 4)
matrix4 = equations4.jacobian((l0, l1, l3, l4))
constant4 = equations4.subs({l0: 0, l1: 0, l3: 0, l4: 0})
assert equations4 == matrix4 * sp.Matrix((l0, l1, l3, l4)) + constant4
print("E4_RANKS", matrix4.rank(), matrix4.row_join(-constant4).rank())
solution_set4 = sp.linsolve(
    (matrix4, -constant4),
    (l0, l1, l3, l4),
)
print("E4_SOLUTION_SET", solution_set4)
solution4 = dict(zip((l0, l1, l3, l4), tuple(next(iter(solution_set4)))))
assert all(
    sp.factor(value.subs(solution4)) == 0 for value in equations4
)

linear_done = sp.simplify(linear.subs(solution4))
det_linear = sp.factor(linear_done.det())
print("LINEAR_PART", linear_done)
print("DET_LINEAR", det_linear)

E3done = sp.Poly(
    sp.expand(
        determinant.coeff_monomial(weight**3)
        .subs(solution6)
        .subs(solution5)
        .subs(solution4)
    ),
    p,
    q,
    r,
)
nonzero_e3 = [
    (monomial, coefficient)
    for monomial, coefficient in E3done.terms()
    if coefficient != 0
]
print("E3_NONZERO_TERMS", nonzero_e3)

print("D4_DN2C_LOW_REPRESENTATIVE_PASS")
