#!/usr/bin/env python3
"""Exact algebra controls for MODULAR_OBSTRUCTION.md.

This is not a numerical certificate for Rouché's theorem. The convergence and
zero-count argument is given analytically in the companion document.
Requires SymPy. No network calls or output-file changes.
"""

import sympy as s


tau, z, q = s.symbols("tau z q")
a, b, c, d = s.symbols("a b c d", real=True)
i = s.I


def check_zero(expr, description):
    assert s.simplify(expr) == 0, description
    print("PASS:", description)


def C(t):
    return (t - i) / (t + i)


def invC(x):
    return i * (1 + x) / (1 - x)


check_zero(C(invC(z)) - z, "Cayley inverse")
check_zero(s.diff(C(tau), tau) - 2 * i / (tau + i) ** 2,
           "Cayley derivative has sign +2i")
check_zero(invC(-z) + 1 / invC(z), "Cayley involution for h(-z)=1-h(z)")

matrices = {
    "cusp value 0": (1, 0, 0, 1),
    "cusp value 1": (0, -1, 1, 0),
    "cusp value infinity": (1, 0, 1, 1),
}
for name, (aa, bb, cc, dd) in matrices.items():
    assert aa * dd - bb * cc == 1
    M = (aa * tau + bb) / (cc * tau + dd)
    denominator = (aa + i * cc) * tau + (bb + i * dd)
    psi = C(M)
    check_zero(s.diff(psi, tau) - 2 * i / denominator ** 2,
               name + ": full disk derivative chain factor")
    assert s.simplify(aa + i * cc) != 0

# General matrix: differentiating the displayed fractional-linear expression
# produces its determinant times 2i. Dividing out the determinant checks the
# identity before the constraint ad-bc=1 is imposed.
psi_general = ((a - i * c) * tau + (b - i * d)) / (
    (a + i * c) * tau + (b + i * d)
)
check_zero(
    s.diff(psi_general, tau)
    - 2 * i * (a * d - b * c) / ((a + i * c) * tau + b + i * d) ** 2,
    "general Möbius derivative with explicit determinant",
)

# DLMF 23.17.4 gives these initial terms. d/dtau = pi*i*q*d/dq.
lambda_q = 16 * q - 128 * q ** 2 + 704 * q ** 3
lambda_prime = s.expand(s.pi * i * q * s.diff(lambda_q, q))
check_zero(lambda_prime - s.pi * i * (16 * q - 256 * q ** 2 + 2112 * q ** 3),
           "initial q-series derivative coefficients")
check_zero((tau + i) ** 2 / (2 * i) * (16 * s.pi * i * q)
           - 8 * s.pi * (tau + i) ** 2 * q,
           "leading scalar 8*pi for h prime")

# Check the general coefficient K from the rational-composition expansion.
m, A = s.symbols("m A", nonzero=True)
lhs_leading = ((a + i * c) * tau + b + i * d) ** 2 / (2 * i) * (m * s.pi * i * A)
beta = (b + i * d) / (a + i * c)
K = m * s.pi * A * (a + i * c) ** 2 / 2
check_zero(lhs_leading - K * (tau + beta) ** 2,
           "general coefficient K and shift beta")

q_bound = s.Rational(1, 16)
center_lower_bound = 1 - 8 * q_bound * (1 + q_bound ** 2) / (1 - q_bound ** 2) ** 2
check_zero(center_lower_bound - s.Rational(32129, 65025),
           "exact positive lower bound for q*L'(q)/L(q) at the center")
assert center_lower_bound > 0
assert sum(s.Rational(3) ** k / s.factorial(k) for k in range(5)) > 16
print("PASS: elementary bound exp(3)>16 from its first five series terms")

print("All exact algebra checks passed. Analytic justification remains in the note.")
