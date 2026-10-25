#!/usr/bin/env python3
"""Exact verifier for a 16x16 exceptional Hecke-type unitary YBE matrix.

All arithmetic is symbolic over Q(sqrt(2), sqrt(3), i).
"""
import sympy as sp

I2 = sp.eye(2)
X = sp.Matrix([[0, 1], [1, 0]])
Z = sp.Matrix([[1, 0], [0, -1]])
J = sp.Matrix([[0, -1], [1, 0]])

kron = sp.kronecker_product

# The base space is V = C^2 \otimes C^2, so H acts on V \otimes V.
H = (
    -kron(Z, I2, Z, Z) / sp.sqrt(6)
    -kron(Z, I2, J, J) / sp.sqrt(6)
    -kron(J, I2, Z, J) / sp.sqrt(6)
    +kron(J, I2, J, Z) / sp.sqrt(6)
    -kron(X, I2, X, X) / sp.sqrt(3)
)
H = sp.simplify(H)

I4 = sp.eye(4)
I16 = sp.eye(16)
I64 = sp.eye(64)

assert H.T == H
assert sp.simplify(H * H - I16) == sp.zeros(16)
assert sp.trace(H) == 0

H1 = kron(H, I4)
H2 = kron(I4, H)
assert sp.simplify(H1 * H2 * H1 - H2 * H1 * H2 - (H1 - H2) / 3) == sp.zeros(64)

q = sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
R = sp.simplify((q - 1) * I16 / 2 + (q + 1) * H / 2)
P = sp.simplify((I16 - H) / 2)

assert P.T == P
assert sp.simplify(P * P - P) == sp.zeros(16)
assert P.rank() == 8
assert sp.simplify((R + I16) * (R - q * I16)) == sp.zeros(16)
assert sp.simplify(R.conjugate().T * R - I16) == sp.zeros(16)
assert sp.trace(R) == 8 * (q - 1)

R1 = kron(R, I4)
R2 = kron(I4, R)
assert sp.simplify(R1 * R2 * R1 - R2 * R1 * R2) == sp.zeros(64)

print("All exact checks passed.")
print("base dimension = 4")
print("matrix size = 16 x 16")
print("rank of (-1)-spectral projection =", P.rank())
print("normalized spectral trace eta =", sp.Rational(P.rank(), 16))
print("q =", q)
