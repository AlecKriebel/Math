#!/usr/bin/env python3
"""Exact SymPy checks for the nonbinary fixed-linear line triple-cover row."""

if not __debug__:
    raise RuntimeError("verification must not run with Python optimization")

import sympy as sp


def require_zero(expr, message):
    if sp.expand(expr) != 0:
        raise AssertionError(message)


p, q, r, t, s, z = sp.symbols("p q r t s z")
a = sp.symbols("a0:4")
b = sp.symbols("b0:4")

A = sum(a[i] * p ** (3 - i) * q**i for i in range(4))
B = sum(b[i] * p ** (3 - i) * q**i for i in range(4))
P = r * A
Q = r * B
variables = (p, q, r)

gradP = sp.Matrix([sp.diff(P, variable) for variable in variables])
gradQ = sp.Matrix([sp.diff(Q, variable) for variable in variables])
D = gradP.cross(gradQ)

at = sum(a[i] * t**i for i in range(4))
bt = sum(b[i] * t**i for i in range(4))
w = sp.expand(at * sp.diff(bt, t) - sp.diff(at, t) * bt)
dehom_D = D.subs({p: 1, q: t, r: s}, simultaneous=True)
expected_D = s * w * sp.Matrix([-1, -t, 3 * s])
for entry in dehom_D - expected_D:
    require_zero(entry, "dehomogenized cross-product formula failed")


def homogeneous_form(degree, prefix):
    coefficients = []
    expression = 0
    for i in range(degree + 1):
        for j in range(degree + 1 - i):
            k = degree - i - j
            coefficient = sp.symbols(f"{prefix}_{i}_{j}_{k}")
            coefficients.append((coefficient, k))
            expression += coefficient * p**i * q**j * r**k
    return sp.expand(expression), coefficients


for degree in (2, 3):
    G, coefficient_data = homogeneous_form(degree, f"g{degree}")
    g = G.subs({p: 1, q: t, r: s}, simultaneous=True)
    lhs = D.dot(sp.Matrix([sp.diff(G, variable) for variable in variables]))
    lhs = lhs.subs({p: 1, q: t, r: s}, simultaneous=True)
    rhs = s * w * (4 * s * sp.diff(g, s) - degree * g)
    require_zero(lhs - rhs, f"degree-{degree} derivation formula failed")

    eigen_expression = sp.expand(4 * s * sp.diff(g, s) - degree * g)
    expected_eigen_expression = sum(
        (4 * r_power - degree)
        * coefficient
        * sp.diff(g, coefficient)
        for coefficient, r_power in coefficient_data
    )
    require_zero(
        eigen_expression - expected_eigen_expression,
        f"degree-{degree} eigenvalue table failed",
    )
    if any(4 * r_power - degree == 0 for _, r_power in coefficient_data):
        raise AssertionError(f"degree-{degree} unexpectedly has a zero eigenvalue")

# Reconstruct the two top determinant coefficients from independent matrix
# entries.  The third row of C is zero.  At z^8 only the 3+3+2
# polarization survives; after its third row is killed, z^7 is exactly the
# 3+3+1 polarization.
l = sp.symbols("l0:9")
h2 = sp.symbols("h20:29")
h3 = sp.symbols("h30:39")
c = sp.symbols("c0:6")
L = sp.Matrix(3, 3, l)
J2 = sp.Matrix(3, 3, h2)
J3 = sp.Matrix(3, 3, h3)
C = sp.Matrix([[c[0], c[1], c[2]], [c[3], c[4], c[5]], [0, 0, 0]])

weighted = sp.Poly((L + z * J2 + z**2 * J3 + z**3 * C).det(), z)
E8 = sp.expand(weighted.coeff_monomial(z**8))
expected_E8 = sp.Matrix(
    [
        [c[0], c[1], c[2]],
        [c[3], c[4], c[5]],
        [h3[6], h3[7], h3[8]],
    ]
).det()
require_zero(E8 - expected_E8, "degree-eight polarization failed")

zero_third_H3 = {h3[6]: 0, h3[7]: 0, h3[8]: 0}
E7 = sp.expand(weighted.coeff_monomial(z**7).subs(zero_third_H3))
expected_E7 = sp.Matrix(
    [
        [c[0], c[1], c[2]],
        [c[3], c[4], c[5]],
        [h2[6], h2[7], h2[8]],
    ]
).det()
require_zero(E7 - expected_E7, "degree-seven polarization failed")

print("nonbinary fixed-linear line triple-cover SymPy checks passed")
