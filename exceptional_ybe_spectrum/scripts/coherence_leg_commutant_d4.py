#!/usr/bin/env python3
"""Exact leg-commutant audit for the published d=4 exceptional solution.

This calculation is deliberately local.  It determines three finite-dimensional
algebras associated with the reflection H:

  C_L = {a in M_4 : [a tensor I_4, H] = 0},
  C_R = {a in M_4 : [I_4 tensor a, H] = 0},
  M_1 = {a in M_4 : R^*(a tensor I_4)R = I_4 tensor a}.

The first two are the one-site leg commutants.  The third is the first relative
commutant of the Yang--Baxter endomorphism in the notation of
Conti--Lechner.  All nullspaces are computed over exact algebraic expressions
by SymPy.
"""

from __future__ import annotations

import sympy as sp


def tensor(*matrices: sp.Matrix) -> sp.Matrix:
    result = sp.Matrix([[1]])
    for matrix in matrices:
        result = sp.kronecker_product(result, matrix)
    return result


I2 = sp.eye(2)
X = sp.Matrix([[0, 1], [1, 0]])
Z = sp.diag(1, -1)
J = sp.Matrix([[0, -1], [1, 0]])
I4 = sp.eye(4)

H = (
    -(
        tensor(Z, I2, Z, Z)
        + tensor(Z, I2, J, J)
        + tensor(J, I2, Z, J)
        - tensor(J, I2, J, Z)
    )
    / sp.sqrt(6)
    - tensor(X, I2, X, X) / sp.sqrt(3)
)

q = (1 + sp.I * sp.sqrt(3)) / 2
R = (q - 1) * sp.eye(16) / 2 + (q + 1) * H / 2


def matrix_nullspace(expression_builder) -> list[sp.Matrix]:
    variables = sp.symbols("x0:16")
    unknown = sp.Matrix(4, 4, variables)
    expression = expression_builder(unknown)
    coefficient_matrix, _ = sp.linear_eq_to_matrix(
        [sp.expand(entry) for entry in expression],
        variables,
    )
    return [
        sp.Matrix(4, 4, list(vector))
        for vector in coefficient_matrix.nullspace()
    ]


def center_dimension(basis: list[sp.Matrix]) -> int:
    coefficients = sp.symbols(f"c0:{len(basis)}")
    generic = sum(
        (coefficient * element for coefficient, element in zip(coefficients, basis)),
        sp.zeros(4),
    )
    equations = []
    for element in basis:
        equations.extend(list(generic * element - element * generic))
    coefficient_matrix, _ = sp.linear_eq_to_matrix(equations, coefficients)
    return len(coefficient_matrix.nullspace())


left_basis = matrix_nullspace(
    lambda a: tensor(a, I4) * H - H * tensor(a, I4)
)
right_basis = matrix_nullspace(
    lambda a: tensor(I4, a) * H - H * tensor(I4, a)
)
relative_basis = matrix_nullspace(
    lambda a: R.conjugate().T * tensor(a, I4) * R - tensor(I4, a)
)

assert H.conjugate().T == H
assert sp.simplify(H * H) == sp.eye(16)
assert len(left_basis) == 4
assert len(right_basis) == 4
assert center_dimension(left_basis) == 1
assert center_dimension(right_basis) == 4
assert len(relative_basis) == 1
assert relative_basis[0] == I4

# Tensor flip exchanges the two leg commutants.
flip = sp.zeros(16)
for i in range(4):
    for j in range(4):
        flip[4 * j + i, 4 * i + j] = 1
flipped_h = flip * H * flip
flipped_left_basis = matrix_nullspace(
    lambda a: tensor(a, I4) * flipped_h - flipped_h * tensor(a, I4)
)
flipped_right_basis = matrix_nullspace(
    lambda a: tensor(I4, a) * flipped_h - flipped_h * tensor(I4, a)
)
assert len(flipped_left_basis) == len(right_basis)
assert len(flipped_right_basis) == len(left_basis)
assert center_dimension(flipped_left_basis) == center_dimension(right_basis)
assert center_dimension(flipped_right_basis) == center_dimension(left_basis)

print("Exact leg-commutant audit for the published d=4 solution")
print(f"dim C_L = {len(left_basis)}")
print(f"dim Z(C_L) = {center_dimension(left_basis)}")
print("classification: C_L is isomorphic to M_2(C)")
print(f"dim C_R = {len(right_basis)}")
print(f"dim Z(C_R) = {center_dimension(right_basis)}")
print("classification: C_R is isomorphic to C^4 (a MASA in M_4)")
print(f"dim M_1 = {len(relative_basis)}")
print("classification: the Yang--Baxter endomorphism is irreducible at level 1")
print("[ok] tensor flip exchanges the left and right leg-algebra types")
