#!/usr/bin/env python3
"""Hardened SymPy verifier for the exceptional d=4 witness.

All arithmetic is symbolic over Q(sqrt(2), sqrt(3), i).  Scientific checks
use explicit failures rather than Python ``assert`` statements so that
optimized Python cannot silently disable them.  The byte-for-byte originally
supplied attachment is retained as ``verify_supplied_original.py``.
"""
import sys

import mpmath
import sympy as sp


if sys.flags.optimize:
    raise RuntimeError("optimized Python is not permitted for scientific verification")
if (sp.__version__, mpmath.__version__) != ("1.14.0", "1.3.0"):
    raise RuntimeError("this verifier requires SymPy 1.14.0 and mpmath 1.3.0")


def require(condition, label):
    if not condition:
        raise AssertionError(label)


def partial_trace_right(matrix, left_dim, right_dim):
    return sp.Matrix(
        left_dim,
        left_dim,
        lambda row, col: sum(
            matrix[row * right_dim + k, col * right_dim + k]
            for k in range(right_dim)
        ),
    )


def partial_trace_left(matrix, left_dim, right_dim):
    return sp.Matrix(
        right_dim,
        right_dim,
        lambda row, col: sum(
            matrix[k * right_dim + row, k * right_dim + col]
            for k in range(left_dim)
        ),
    )


def qubit_permutation(output_sources):
    """Matrix sending |b_0...b_{n-1}> to |b_{p_0}...b_{p_{n-1}}>."""

    require(sorted(output_sources) == list(range(len(output_sources))),
            "invalid qubit permutation")
    dimension = 2 ** len(output_sources)
    out = sp.zeros(dimension)
    for input_index in range(dimension):
        bits = [
            (input_index >> (len(output_sources) - 1 - position)) & 1
            for position in range(len(output_sources))
        ]
        output_index = 0
        for source in output_sources:
            output_index = 2 * output_index + bits[source]
        out[output_index, input_index] = 1
    return out

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

# A deliberately asymmetric toy case certifies that the two partial-trace
# helpers use different tensor legs rather than accidentally duplicating one.
partial_trace_toy = sp.diag(1, 2, 3, 5)
require(
    partial_trace_right(partial_trace_toy, 2, 2) == sp.diag(3, 8),
    "right partial-trace convention failed on the asymmetric toy case",
)
require(
    partial_trace_left(partial_trace_toy, 2, 2) == sp.diag(4, 7),
    "left partial-trace convention failed on the asymmetric toy case",
)

require(H.T == H, "H is not symmetric")
require(sp.simplify(H * H - I16) == sp.zeros(16), "H^2 != I_16")
require(sp.trace(H) == 0, "Tr(H) != 0")

H1 = kron(H, I4)
H2 = kron(I4, H)
require(
    sp.simplify(H1 * H2 * H1 - H2 * H1 * H2 - (H1 - H2) / 3)
    == sp.zeros(64),
    "the 64-dimensional cubic reflection identity failed",
)

q = sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
expected_q = sp.cos(sp.pi / 3) + sp.I * sp.sin(sp.pi / 3)
require(sp.simplify(q - expected_q) == 0, "q is not exp(+i*pi/3)")
R = sp.simplify((q - 1) * I16 / 2 + (q + 1) * H / 2)
P = sp.simplify((I16 - H) / 2)

require(P.T == P, "P is not symmetric")
require(sp.simplify(P * P - P) == sp.zeros(16), "P^2 != P")
require(P.rank() == 8, "rank(P) != 8")
require(
    sp.simplify((R + I16) * (R - q * I16)) == sp.zeros(16),
    "the Hecke polynomial failed",
)
require(
    sp.simplify(R.conjugate().T * R - I16) == sp.zeros(16),
    "R is not unitary",
)
require(sp.trace(R) == 8 * (q - 1), "Tr(R) != 8(q - 1)")
require(partial_trace_right(P, 4, 4) == 2 * I4, "Tr_right(P) != 2 I_4")
require(partial_trace_left(P, 4, 4) == 2 * I4, "Tr_left(P) != 2 I_4")

R1 = kron(R, I4)
R2 = kron(I4, R)
require(
    sp.simplify(R1 * R2 * R1 - R2 * R1 * R2) == sp.zeros(64),
    "the 64-dimensional Yang--Baxter equation failed",
)

P1 = kron(P, I4)
P2 = kron(I4, P)
TL = sp.simplify(P1 * P2 * P1 - P1 / 3)
require(sp.simplify(sum(entry**2 for entry in TL) / 64) == sp.Rational(1, 18),
        "the d=3 Temperley--Lieb obstruction norm is not 1/18")
Q = I16 - P
Q1 = kron(Q, I4)
Q2 = kron(I4, Q)
CTL = sp.simplify(Q1 * Q2 * Q1 - Q1 / 3)
require(sp.simplify(sum(entry**2 for entry in CTL) / 64) == sp.Rational(1, 18),
        "the complementary d=3 obstruction norm is not 1/18")

KH = sp.simplify(
    -kron(Z, Z, Z) / sp.sqrt(6)
    -kron(Z, J, J) / sp.sqrt(6)
    -kron(J, J, Z) / sp.sqrt(6)
    +kron(J, Z, J) / sp.sqrt(6)
    -kron(X, X, X) / sp.sqrt(3)
)
sitewise_swap = qubit_permutation((1, 0, 3, 2))
require(
    sp.simplify(sitewise_swap * H * sitewise_swap.T - kron(I2, KH))
    == sp.zeros(16),
    "the printed H does not factor as I_2 tensor the printed K_H after swapping",
)
I8 = sp.eye(8)
K = sp.simplify((q - 1) * I8 / 2 + (q + 1) * KH / 2)
require(sp.simplify((K + I8) * (K - q * I8)) == sp.zeros(8),
        "the active Hecke polynomial failed")
require(sp.simplify(K.conjugate().T * K - I8) == sp.zeros(8),
        "the active operator is not unitary")
K1 = kron(K, I4)
K2 = kron(I4, K)
require(sp.simplify(K1 * K2 * K1 - K2 * K1 * K2) == sp.zeros(32),
        "the (3,2)-generalized Yang--Baxter equation failed")

print("All exact checks passed.")
print("base dimension = 4")
print("matrix size = 16 x 16")
print("rank of (-1)-spectral projection =", P.rank())
print("normalized spectral trace eta =", sp.Rational(P.rank(), 16))
print("q =", q)
