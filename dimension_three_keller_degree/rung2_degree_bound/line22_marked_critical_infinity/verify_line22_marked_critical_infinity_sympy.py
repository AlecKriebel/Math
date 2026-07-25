#!/usr/bin/env python3
"""Exact checks for the marked-critical infinity line-(2,2) orbit."""

if not __debug__:
    raise RuntimeError("verification must not run with Python optimization")

from itertools import product

import sympy as sp


x, y, z = sp.symbols("x y z")
variables = (x, y, z)
p = x**2
q = y * z


def monomials(degree):
    result = []
    for i in range(degree, -1, -1):
        for j in range(degree - i, -1, -1):
            result.append(x**i * y**j * z ** (degree - i - j))
    return tuple(result)


def form(prefix, degree):
    mons = monomials(degree)
    coefficients = sp.symbols(f"{prefix}0:{len(mons)}")
    return sum(c * m for c, m in zip(coefficients, mons)), coefficients


def jacobian(vector):
    return vector.jacobian(variables)


def weighted_coefficient(linear, quadratic, cubic, quartic, degree):
    matrices = tuple(
        jacobian(vector) for vector in (linear, quadratic, cubic, quartic)
    )
    result = 0
    for weights in product(range(4), repeat=3):
        if sum(weights) != degree:
            continue
        selected = sp.Matrix.vstack(
            *(matrices[weights[row]][row, :] for row in range(3))
        )
        result += selected.det()
    return sp.expand(result)


def coefficient(expression, monomial):
    return sp.Poly(sp.expand(expression), x, y, z).coeff_monomial(monomial)


def require_zero(expression, message):
    if sp.expand(expression) != 0:
        raise AssertionError(message)


delta = lambda expression: sp.expand(
    z * sp.diff(expression, z) - y * sp.diff(expression, y)
)
H4 = sp.Matrix([p**2, q**2, 0])

# Complete E7 identity and kernel.
Uraw, uraw = form("topu", 3)
Vraw, vraw = form("topv", 3)
Wraw, wraw = form("topw", 2)
H3raw = sp.Matrix([Uraw, Vraw, x**3])
H2raw = sp.Matrix([0, 0, Wraw])
zero_linear = sp.zeros(3, 1)
E7raw = weighted_coefficient(zero_linear, H2raw, H3raw, H4, 7)
require_zero(
    E7raw + 2 * x**2 * q * delta(3 * Uraw - 4 * x * Wraw),
    "raw E7 formula",
)

kernel_cubic, kernel_coefficients = form("kernel", 3)
kernel_equations = sp.Poly(delta(kernel_cubic), x, y, z).coeffs()
kernel_matrix, _ = sp.linear_eq_to_matrix(kernel_equations, kernel_coefficients)
if kernel_matrix.rank() != 8:
    raise AssertionError("delta cubic rank")
require_zero(delta(x**3), "x^3 invariant")
require_zero(delta(x * q), "xq invariant")

# Gauge-fixed E7 family and the complete E6 table.
A = sp.symbols("A")
w = sp.symbols("w0:6")
v = sp.symbols("v1 v2 v3 v4 v5 v6 v9")
W = sum(c * m for c, m in zip(w, monomials(2)))
U = sp.Rational(4, 3) * x * W + A * x * q
V = (
    v[0] * x**2 * y
    + v[1] * x**2 * z
    + v[2] * x * y**2
    + v[3] * x * y * z
    + v[4] * x * z**2
    + v[5] * y**3
    + v[6] * z**3
)
U2, u = form("u", 2)
V2, h = form("h", 2)
ell = sp.symbols("l0:9")
L = sp.Matrix(3, 3, ell) * sp.Matrix([x, y, z])
E6 = weighted_coefficient(L, sp.Matrix([U2, V2, W]), sp.Matrix([U, V, x**3]), H4, 6)

expected_e6 = {
    x**5 * y: -3 * A * v[0],
    x**5 * z: 3 * A * v[1],
    x**4 * y**2: -6 * A * v[2],
    x**4 * z**2: 6 * A * v[4],
    x**3 * y**3: -9 * A * v[5],
    x**3 * z**3: 9 * A * v[6],
    x**3 * y**2 * z: sp.Rational(2, 3)
    * (-12 * ell[7] + 9 * u[1] - 4 * w[0] * w[1]),
    x**3 * y * z**2: -sp.Rational(2, 3)
    * (-12 * ell[8] + 9 * u[2] - 4 * w[0] * w[2]),
    x**2 * y**3 * z: sp.Rational(4, 3)
    * (9 * u[3] - 4 * w[0] * w[3] - 2 * w[1] ** 2),
    x**2 * y * z**3: -sp.Rational(4, 3)
    * (9 * u[5] - 4 * w[0] * w[5] - 2 * w[2] ** 2),
    x * y**4 * z: -8 * w[1] * w[3],
    x * y**3 * z**2: -sp.Rational(2, 3)
    * (3 * A * w[1] + 4 * w[1] * w[4] + 4 * w[2] * w[3]),
    x * y**2 * z**3: sp.Rational(2, 3)
    * (3 * A * w[2] + 4 * w[1] * w[5] + 4 * w[2] * w[4]),
    x * y * z**4: 8 * w[2] * w[5],
    y**5 * z: -sp.Rational(16, 3) * w[3] ** 2,
    y**4 * z**2: -sp.Rational(4, 3) * w[3] * (3 * A + 4 * w[4]),
    y**2 * z**4: sp.Rational(4, 3) * w[5] * (3 * A + 4 * w[4]),
    y * z**5: sp.Rational(16, 3) * w[5] ** 2,
}
reconstructed_e6 = sum(value * monomial for monomial, value in expected_e6.items())
require_zero(E6 - reconstructed_e6, "complete E6 table")

C = sp.symbols("C")
B, w0, w1, w2, w4 = sp.symbols("B w0 w1 w2 w4")
u0, u4 = sp.symbols("u0 u4")
h2 = sp.symbols("b0:6")


def general_second_quadratic():
    return sum(c * m for c, m in zip(h2, monomials(2)))


def linear_vector():
    return sp.Matrix(3, 3, ell) * sp.Matrix([x, y, z])


# Case A != 0, C != 0 after the E6 products.
W1 = w0 * p + w4 * q
U21 = (
    u0 * p
    + sp.Rational(4, 3) * ell[7] * x * y
    + sp.Rational(4, 3) * ell[8] * x * z
    + u4 * q
)
H31 = sp.Matrix([C * x * q, B * x * q, x**3])
H21 = sp.Matrix([U21, general_second_quadratic(), W1])
E51 = weighted_coefficient(linear_vector(), H21, H31, H4, 5)
require_zero(coefficient(E51, y**3 * z**2) + 2 * C * ell[7], "case 1 l32")
require_zero(coefficient(E51, y**2 * z**3) - 2 * C * ell[8], "case 1 l33")
case1_zero = {ell[7]: 0, ell[8]: 0}
require_zero(coefficient(E51.subs(case1_zero), x**2 * y**2 * z) - 6 * ell[1], "case 1 l12")
require_zero(coefficient(E51.subs(case1_zero), x**2 * y * z**2) + 6 * ell[2], "case 1 l13")
require_zero(
    sp.Matrix(3, 3, ell).det().subs(
        {ell[1]: 0, ell[2]: 0, ell[7]: 0, ell[8]: 0}
    ),
    "case 1 determinant",
)

# Case A != 0, C = 0.
AA = sp.symbols("AA")
W2case = w0 * p + w1 * x * y + w2 * x * z - sp.Rational(3, 4) * AA * q
U3case = sp.Rational(4, 3) * x * W2case + AA * x * q
U22 = (
    u0 * p
    + (sp.Rational(4, 3) * ell[7] + sp.Rational(4, 9) * w0 * w1) * x * y
    + (sp.Rational(4, 3) * ell[8] + sp.Rational(4, 9) * w0 * w2) * x * z
    + sp.Rational(2, 9) * w1**2 * y**2
    + u4 * q
    + sp.Rational(2, 9) * w2**2 * z**2
)
E52 = weighted_coefficient(
    linear_vector(),
    sp.Matrix([U22, general_second_quadratic(), W2case]),
    sp.Matrix([U3case, B * x * q, x**3]),
    H4,
    5,
)
require_zero(coefficient(E52, y**4 * z) - sp.Rational(8, 9) * w1**3, "case 2 w1 cube")
require_zero(coefficient(E52, y * z**4) + sp.Rational(8, 9) * w2**3, "case 2 w2 cube")
case2_pre = {
    w1: 0,
    w2: 0,
    h2[1]: 0,
    h2[2]: 0,
    h2[3]: 0,
    h2[5]: 0,
    ell[1]: sp.Rational(4, 9) * w0 * ell[7],
    ell[2]: sp.Rational(4, 9) * w0 * ell[8],
}
E42 = weighted_coefficient(
    linear_vector(),
    sp.Matrix([U22, general_second_quadratic(), W2case]),
    sp.Matrix([U3case, B * x * q, x**3]),
    H4,
    4,
).subs(case2_pre)
require_zero(coefficient(E42, y**3 * z) + sp.Rational(8, 3) * ell[7] ** 2, "case 2 l32 square")
require_zero(coefficient(E42, y * z**3) - sp.Rational(8, 3) * ell[8] ** 2, "case 2 l33 square")

# Case A = 0, C != 0.
r1, r2, r3, r4, r5, r6, r9 = sp.symbols("r1 r2 r3 r4 r5 r6 r9")
V3case = (
    r1 * x**2 * y
    + r2 * x**2 * z
    + r3 * x * y**2
    + r4 * x * y * z
    + r5 * x * z**2
    + r6 * y**3
    + r9 * z**3
)
W3case = w0 * p + sp.Rational(3, 4) * C * q
U23 = U21
E53 = weighted_coefficient(
    linear_vector(),
    sp.Matrix([U23, general_second_quadratic(), W3case]),
    sp.Matrix([C * x * q, V3case, x**3]),
    H4,
    5,
)
require_zero(coefficient(E53, x * y**3 * z) - sp.Rational(3, 2) * C**2 * r3, "case 3 r3")
require_zero(coefficient(E53, x * y * z**3) + sp.Rational(3, 2) * C**2 * r5, "case 3 r5")
require_zero(coefficient(E53, y**4 * z) - sp.Rational(9, 4) * C**2 * r6, "case 3 r6")
require_zero(coefficient(E53, y * z**4) + sp.Rational(9, 4) * C**2 * r9, "case 3 r9")
require_zero(coefficient(E53, y**3 * z**2) + 2 * C * ell[7], "case 3 l32")
require_zero(coefficient(E53, y**2 * z**3) - 2 * C * ell[8], "case 3 l33")

case3_pre = {
    r3: 0,
    r5: 0,
    r6: 0,
    r9: 0,
    ell[7]: 0,
    ell[8]: 0,
    ell[1]: -C**2 * r1 / 8,
    ell[2]: -C**2 * r2 / 8,
    u4: -sp.Rational(2, 3) * C * w0,
}
E43 = weighted_coefficient(
    linear_vector(),
    sp.Matrix([U23, general_second_quadratic(), W3case]),
    sp.Matrix([C * x * q, V3case, x**3]),
    H4,
    4,
).subs(case3_pre)
case3_lower = {
    h2[1]: sp.Rational(2, 3) * r1 * w0,
    h2[2]: sp.Rational(2, 3) * r2 * w0,
    h2[3]: 0,
    h2[5]: 0,
}
require_zero(coefficient(E43, x * y**2 * z).subs(case3_lower), "case 3 h1")
require_zero(coefficient(E43, x * y * z**2).subs(case3_lower), "case 3 h2")
require_zero(coefficient(E43, y**3 * z).subs(case3_lower), "case 3 h3")
require_zero(coefficient(E43, y * z**3).subs(case3_lower), "case 3 h5")

E23 = weighted_coefficient(
    linear_vector(),
    sp.Matrix([U23, general_second_quadratic(), W3case]),
    sp.Matrix([C * x * q, V3case, x**3]),
    H4,
    2,
).subs(case3_pre).subs(case3_lower)
expected_e2 = -sp.Rational(3, 8) * C**2 * (r1 * ell[5] - r2 * ell[4])
require_zero(coefficient(E23, x**2) - expected_e2, "case 3 resonant E2")
det3 = sp.Matrix(3, 3, ell).det().subs(case3_pre)
require_zero(det3 - ell[6] * expected_e2 / 3, "case 3 determinant factor")

# Case A = C = 0.  The pre-shear E5 cubes kill w1,w2.
W4raw = w0 * p + w1 * x * y + w2 * x * z
U4raw = sp.Rational(4, 3) * x * W4raw
U24raw = (
    u0 * p
    + (sp.Rational(4, 3) * ell[7] + sp.Rational(4, 9) * w0 * w1) * x * y
    + (sp.Rational(4, 3) * ell[8] + sp.Rational(4, 9) * w0 * w2) * x * z
    + sp.Rational(2, 9) * w1**2 * y**2
    + u4 * q
    + sp.Rational(2, 9) * w2**2 * z**2
)
E54raw = weighted_coefficient(
    linear_vector(),
    sp.Matrix([U24raw, general_second_quadratic(), W4raw]),
    sp.Matrix([U4raw, V3case, x**3]),
    H4,
    5,
)
require_zero(coefficient(E54raw, y**4 * z) - sp.Rational(8, 9) * w1**3, "case 4 w1 cube")
require_zero(coefficient(E54raw, y * z**4) + sp.Rational(8, 9) * w2**3, "case 4 w2 cube")

# After the target shear removing (4/3)w0*x^3.
W4 = w0 * p
U24 = U21
E54 = weighted_coefficient(
    linear_vector(),
    sp.Matrix([U24, general_second_quadratic(), W4]),
    sp.Matrix([0, V3case, x**3]),
    H4,
    5,
)
case4_pre = {
    ell[1]: -sp.Rational(8, 9) * w0 * ell[7],
    ell[2]: -sp.Rational(8, 9) * w0 * ell[8],
}
require_zero(coefficient(E54, x**2 * y**2 * z).subs(case4_pre), "case 4 l12")
require_zero(coefficient(E54, x**2 * y * z**2).subs(case4_pre), "case 4 l13")
E44 = weighted_coefficient(
    linear_vector(),
    sp.Matrix([U24, general_second_quadratic(), W4]),
    sp.Matrix([0, V3case, x**3]),
    H4,
    4,
).subs(case4_pre)
require_zero(coefficient(E44, y**3 * z) + sp.Rational(8, 3) * ell[7] ** 2, "case 4 l32 square")
require_zero(coefficient(E44, y * z**3) - sp.Rational(8, 3) * ell[8] ** 2, "case 4 l33 square")

print("line-(2,2) marked-critical infinity SymPy checks passed")
