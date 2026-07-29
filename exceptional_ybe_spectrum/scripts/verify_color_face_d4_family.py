#!/usr/bin/env python3
"""Exact symbolic certificate for a color/face d=4 family.

This family was recognized after calibrating the color/face optimizer.  It is
not a d=6 witness.  Its purpose is to prove that the reduced ansatz and its
implementation contain exact exceptional solutions, rather than merely small
numerical residuals.

Let s,t be real with s^2+2t^2=1.  In the mixed color basis use the Hadamard
matrix on the second site's color and four 4-by-4 reflection blocks K_ab
defined below.  Every entry of H^2-I and of the cubic Yang--Baxter residual is
divisible by s^2+2t^2-1.
"""

from __future__ import annotations

import sympy as sp


def tensor(*matrices: sp.Matrix) -> sp.Matrix:
    result = sp.Matrix([[1]])
    for matrix in matrices:
        result = sp.kronecker_product(result, matrix)
    return result


def assemble_face_blocks(blocks: list[sp.Matrix]) -> sp.Matrix:
    h0 = sp.zeros(16)
    for index, (a, b) in enumerate(
        [(a, b) for a in range(2) for b in range(2)]
    ):
        indices = [
            (2 * a + r) * 4 + (2 * b + u)
            for r in range(2)
            for u in range(2)
        ]
        for i, row in enumerate(indices):
            for j, column in enumerate(indices):
                h0[row, column] = blocks[index][i, j]
    return h0


def assert_multiple_of_relation(
    matrix: sp.Matrix, relation: sp.Expr, s: sp.Symbol, t: sp.Symbol
) -> int:
    nonzero = 0
    for entry in matrix:
        entry = sp.expand(entry)
        if entry == 0:
            continue
        nonzero += 1
        quotient = sp.cancel(entry / relation)
        # A genuine polynomial quotient proves divisibility.  ``extension=True``
        # admits the algebraic coefficients sqrt(2), sqrt(3), and i.
        sp.Poly(quotient, s, t, extension=True)
        assert sp.expand(entry - relation * quotient) == 0
    return nonzero


I2 = sp.eye(2)
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
Z = sp.diag(1, -1)
F = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2)

s, t = sp.symbols("s t", real=True)
relation = s**2 + 2 * t**2 - 1

B0 = X
B1 = -Y
C0 = -t * X - t * Y - s * Z
C1 = -t * X - t * Y + s * Z

blocks = []
for a in range(2):
    for b in range(2):
        parity = (a + b) % 2
        sign = 1 if parity == 0 else -1
        b_operator = B0 if parity == 0 else B1
        c_operator = C0 if b == 0 else C1
        blocks.append(
            sign * tensor(Z, I2) / sp.sqrt(3)
            + sp.sqrt(sp.Rational(2, 3)) * tensor(b_operator, c_operator)
        )

h0 = assemble_face_blocks(blocks)
pair_change = tensor(sp.eye(4), F, I2)
H = sp.expand(pair_change * h0 * pair_change.conjugate().T)

assert H.conjugate().T == H
assert sp.trace(H) == 0
involution_nonzero = assert_multiple_of_relation(
    sp.expand(H * H - sp.eye(16)), relation, s, t
)

H1 = tensor(H, sp.eye(4))
H2 = tensor(sp.eye(4), H)
residual = sp.expand(H1 * H2 * H1 - H2 * H1 * H2 - (H1 - H2) / 3)
cubic_nonzero = assert_multiple_of_relation(residual, relation, s, t)

print("Exact color/face d=4 family")
print("constraint: s^2 + 2 t^2 = 1")
print(f"nonzero symbolic entries in H^2-I before constraint: {involution_nonzero}")
print(
    "nonzero symbolic entries in cubic residual before constraint: "
    f"{cubic_nonzero}"
)
print("[ok] every entry is divisible by s^2+2t^2-1")
print("[ok] H is Hermitian and traceless")
