#!/usr/bin/env python3
"""Exact E5 exclusion of the two DN2C contact-plane interiors."""

from __future__ import annotations

import sys

import sympy as sp

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

import derive_e6_projection as base

p, q, r, weight = base.p, base.q, base.r, base.weight
a, b, c, d, e, f = base.a, base.b, base.c, base.d, base.e, base.f
s = sp.sqrt(-2)

plus_plane = {
    a: 0,
    b: 0,
    d: -2 * f,
    c: -sp.Rational(1, 3) * ((4 + 2 * s) * e + (2 - 2 * s) * f),
}

# Solve the constant-rank E6 r^1 block for ar2,br2.
rows1 = [
    index for index, exponent in enumerate(base.EXPONENTS) if exponent[2] == 1
]
columns1 = [base.LOWER.index(base.ar[2]), base.LOWER.index(base.br[2])]
A1 = base.matrix[rows1, columns1].subs({a: 0, b: 0})
b1 = -base.constant[rows1, :].subs({a: 0, b: 0})
pivot = A1.extract((0, 1), (0, 1))
assert pivot.det() == 36
solution_vector = pivot.inv() * b1.extract((0, 1), (0,))
solution = {
    base.ar[2]: sp.factor(solution_vector[0].subs(plus_plane), extension=s),
    base.br[2]: sp.factor(solution_vector[1].subs(plus_plane), extension=s),
}
assert all(
    sp.factor(value.subs(plus_plane).subs(solution), extension=s) == 0
    for value in A1 * sp.Matrix((base.ar[2], base.br[2])) - b1
)

# Restore every E5-only coefficient before extracting the selected terms.
ab = sp.symbols("ab0:3")
bb = sp.symbols("bb0:3")
binary2 = (p**2, p * q, q**2)
Afull = base.A + sum(value * monomial for value, monomial in zip(ab, binary2))
Bfull = base.B + sum(value * monomial for value, monomial in zip(bb, binary2))
ell = sp.symbols("ell0:8")
linear = sp.Matrix(
    (
        (ell[0], ell[1], ell[2]),
        (ell[3], ell[4], ell[5]),
        (ell[6], ell[7], base.ell33),
    )
)
H2 = sp.Matrix((Afull, Bfull, base.T))
H3 = sp.Matrix((base.U, base.V, base.R))
H4 = sp.Matrix((base.P, base.Q, 0))
determinant = sp.Poly(
    sp.expand(
        (
            linear
            + weight * H2.jacobian(base.coords)
            + weight**2 * H3.jacobian(base.coords)
            + weight**3 * H4.jacobian(base.coords)
        ).det()
    ),
    weight,
)
E5 = sp.Poly(
    sp.expand(
        determinant.coeff_monomial(weight**5)
        .subs(plus_plane)
        .subs(solution)
    ),
    p,
    q,
    r,
)
selected_exponents = ((3, 0, 2), (2, 1, 2), (1, 2, 2))
selected = tuple(
    sp.factor(
        E5.coeff_monomial(p**i * q**j * r**k) / (e - f),
        extension=s,
    )
    for i, j, k in selected_exponents
)
all_lower = (
    set(base.LOWER)
    | set(ab)
    | set(bb)
    | set(ell)
)
assert all(not (value.free_symbols & all_lower) for value in selected)
quadratic_monomials = (e**2, e * f, f**2)
coefficient_matrix = sp.Matrix(
    [
        [
            sp.Poly(value, e, f, extension=s).coeff_monomial(monomial)
            for monomial in quadratic_monomials
        ]
        for value in selected
    ]
)
det_selected = sp.factor(coefficient_matrix.det(), extension=s)
print("RAW_SELECTED_E5_MATRIX_DET", det_selected)
assert sp.expand(det_selected + 768 * (-22 + s)) == 0
assert det_selected != 0

# Therefore, on e-f != 0, E5=0 forces e^2=ef=f^2=0, impossible.
# Conjugation s -> -s gives the identical exclusion of the minus plane.
print("SELECTED_E5_MATRIX_DET", det_selected)
print("D4_DN2C_PLANE_INTERIORS_E5_PASS")
