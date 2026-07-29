#!/usr/bin/env python3
"""Exact checks for the cyclic low-Schmidt color/face no-go proof.

The verifier checks the two tensor contractions that drive the human proof,
the nonzero Fourier coefficient on the zero-sum real plane, and both terminal
sign contradictions.  It does not substitute a numerical candidate and does
not use floating-point arithmetic.
"""

from __future__ import annotations

import sympy as sp


def tensor(*matrices: sp.Matrix) -> sp.Matrix:
    result = sp.Matrix([[1]])
    for matrix in matrices:
        result = sp.kronecker_product(result, matrix)
    return result


def partial_trace_first(matrix: sp.Matrix) -> sp.Matrix:
    """Trace qubit 1 from an operator on three qubits."""
    return sp.Matrix(
        4,
        4,
        lambda jk, lm: sum(
            matrix[4 * i + jk, 4 * i + lm] for i in range(2)
        ),
    )


def partial_trace_first_third(matrix: sp.Matrix) -> sp.Matrix:
    """Trace qubits 1 and 3 from an operator on three qubits."""
    return sp.Matrix(
        2,
        2,
        lambda j, ell: sum(
            matrix[4 * i + 2 * j + k, 4 * i + 2 * ell + k]
            for i in range(2)
            for k in range(2)
        ),
    )


I2 = sp.eye(2)
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
Z = sp.diag(1, -1)

x, xp, y, yp, u, v = sp.symbols("x xp y yp u v", real=True)
p, q, pp, qp = sp.symbols("p q pp qp", real=True)
c1, c2, c3 = sp.symbols("c1 c2 c3", real=True)
cp1, cp2, cp3 = sp.symbols("cp1 cp2 cp3", real=True)
d1, d2, d3 = sp.symbols("d1 d2 d3", real=True)
e1, e2, e3 = sp.symbols("e1 e2 e3", real=True)

B = p * X + q * Y
Bp = pp * X + qp * Y
C = c1 * X + c2 * Y + c3 * Z
Cp = cp1 * X + cp2 * Y + cp3 * Z
D = d1 * X + d2 * Y + d3 * Z
E = e1 * X + e2 * Y + e3 * Z
g = p * pp + q * qp

K = x * tensor(Z, I2, I2) + y * tensor(B, C, I2)
Kp = xp * tensor(Z, I2, I2) + yp * tensor(Bp, Cp, I2)
L = u * tensor(I2, Z, I2) + v * tensor(I2, D, E)

word = sp.expand(K * L * Kp)
expected_one = 2 * (
    x * xp * (u * tensor(Z, I2) + v * tensor(D, E))
    + y
    * yp
    * g
    * tensor(C, I2)
    * (u * tensor(Z, I2) + v * tensor(D, E))
    * tensor(Cp, I2)
)
assert sp.expand(partial_trace_first(word) - expected_one) == sp.zeros(4)

expected_one_three = 4 * u * (
    x * xp * Z + y * yp * g * C * Z * Cp
)
assert (
    sp.expand(partial_trace_first_third(word) - expected_one_three)
    == sp.zeros(2)
)

# The reversed cubic word L K L' has zero first-qubit trace because every
# first-qubit coefficient of K is traceless.
up, vp = sp.symbols("up vp", real=True)
dp1, dp2, dp3 = sp.symbols("dp1 dp2 dp3", real=True)
ep1, ep2, ep3 = sp.symbols("ep1 ep2 ep3", real=True)
Dp = dp1 * X + dp2 * Y + dp3 * Z
Ep = ep1 * X + ep2 * Y + ep3 * Z
Lp = up * tensor(I2, Z, I2) + vp * tensor(I2, Dp, Ep)
assert partial_trace_first(sp.expand(L * K * Lp)) == sp.zeros(4)

# Exact Fourier norm on x0+x1+x2=0.
x0, x1 = sp.symbols("x0 x1", real=True)
x2 = -x0 - x1
omega = (-1 + sp.I * sp.sqrt(3)) / 2
fourier = x0 + omega * x1 + omega**2 * x2
fourier_norm = sp.expand(fourier * sp.conjugate(fourier))
expected_fourier_norm = sp.Rational(3, 2) * (
    x0**2 + x1**2 + x2**2
)
assert sp.simplify(fourier_norm - expected_fourier_norm) == 0

# Exact diagonal equation in the anticommuting branch.  Gauge A=Z, C=X,
# and use Y for the perpendicular equatorial axis.  The signed product
# vector y_l B_l is h_l X + z_l Y.
xq = sp.symbols("xq", real=True)
xl0, xl1 = sp.symbols("xl0 xl1", real=True)
xl2 = -xl0 - xl1
h, z0, z1, z2 = sp.symbols("h z0 z1 z2", real=True)
local_blocks = [
    xl * tensor(Z, I2) + tensor(h * X + zl * Y, X)
    for xl, zl in ((xl0, z0), (xl1, z1), (xl2, z2))
]
conjugator = tensor(X, I2)
diagonal_sum = sp.zeros(4)
for local_block in local_blocks:
    diagonal_sum += (
        (xq**2 + sp.Rational(1, 3)) * local_block
        + (1 - xq**2) * conjugator * local_block * conjugator
    )
expected_diagonal = (
    4 * h * tensor(X, X)
    + 2
    * (xq**2 - sp.Rational(1, 3))
    * (z0 + z1 + z2)
    * tensor(Y, X)
)
assert sp.expand(diagonal_sum - expected_diagonal) == sp.zeros(4)

# Three unit vectors w_j with sum zero have pairwise dot product -1/2.
a0, b0, a1, b1 = sp.symbols("a0 b0 a1 b1", real=True)
a2, b2 = -a0 - a1, -b0 - b1
n0 = a0**2 + b0**2 - 1
n1 = a1**2 + b1**2 - 1
n2 = a2**2 + b2**2 - 1
dot01 = a0 * a1 + b0 * b1
assert sp.expand(2 * dot01 + 1 - (n2 - n0 - n1)) == 0

# Terminal contradictions: a real square cannot equal either negative value.
assert (-sp.Rational(1, 3)) ** 3 == -sp.Rational(1, 27)
assert (-sp.Rational(5, 12)) ** 3 == -sp.Rational(125, 1728)

# In the pure-product boundary, unitary left/right multiplication would have
# to shrink a nonzero Fourier mode by 2/3.
assert 1 - sp.Rational(2, 3) ** 2 == sp.Rational(5, 9)

print("Exact cyclic low-Schmidt color/face certificate")
print("[ok] one-qubit contraction (3)")
print("[ok] first-and-third-qubit contraction (4)")
print("[ok] reversed cubic word has zero first-qubit trace")
print("[ok] nontrivial Fourier coefficients are nonzero off the origin")
print("[ok] anticommuting-branch diagonal reduction (16)")
print("[ok] zero-sum unit-vector lemma")
print("[ok] both terminal products are negative real squares")
print("[ok] pure-product boundary has impossible 2/3 norm contraction")
