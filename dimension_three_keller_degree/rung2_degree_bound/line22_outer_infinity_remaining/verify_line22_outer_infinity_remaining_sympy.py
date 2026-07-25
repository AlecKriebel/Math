#!/usr/bin/env python3
"""Exact certificates for the remaining finite-companion outer-infinity chart."""

if not __debug__:
    raise RuntimeError("verification must not run with Python optimization")

from itertools import product

import sympy as sp


x, y, z = sp.symbols("x y z")
p, q = x**2, y * z
variables = (x, y, z)


def monomials(degree):
    return tuple(
        x**i * y**j * z ** (degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def form(prefix, degree):
    coefficients = sp.symbols(f"{prefix}0:{len(monomials(degree))}")
    return (
        sum(c * m for c, m in zip(coefficients, monomials(degree))),
        coefficients,
    )


def jacobian(vector):
    return vector.jacobian(variables)


def weighted_coefficient(linear, quadratic, cubic, quartic, degree):
    matrices = tuple(
        jacobian(vector) for vector in (linear, quadratic, cubic, quartic)
    )
    result = 0
    for choices in product(range(4), repeat=3):
        if sum(choices) != degree:
            continue
        result += sp.Matrix.vstack(
            *(matrices[choices[row]][row, :] for row in range(3))
        ).det()
    return sp.expand(result)


def coefficient(expression, monomial):
    return sp.Poly(sp.expand(expression), x, y, z).coeff_monomial(monomial)


def require_zero(expression, message):
    if sp.expand(expression) != 0:
        raise AssertionError(message)


def raw_e7_matrix(outer_parameter, companion_parameter):
    U, uc = form("rawu", 3)
    V, vc = form("rawv", 3)
    W, wc = form("raww", 2)
    H4 = sp.Matrix(
        [(p - outer_parameter * q) ** 2, q**2, 0]
    )
    H3 = sp.Matrix([U, V, x * (p - companion_parameter * q)])
    H2 = sp.Matrix([0, 0, W])
    E7 = weighted_coefficient(sp.zeros(3, 1), H2, H3, H4, 7)
    equations = [
        coefficient(E7, monomial) for monomial in monomials(7)
    ]
    matrix, right = sp.linear_eq_to_matrix(equations, uc + vc + wc)
    if right != sp.zeros(len(equations), 1):
        raise AssertionError("raw E7 is not homogeneous")
    return matrix


# The exact raw ranks on all finite-companion orbit strata.
t = sp.symbols("t")
if raw_e7_matrix(1, t).rank() != 18:
    raise AssertionError("generic raw E7 rank over C(t)")
generic_rows = (1, 2, 3, 5, 6, 7, 8, 9, 11, 13, 16, 17, 18, 19, 23, 25, 31, 32)
generic_columns = (1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 15, 16, 17, 18, 19, 23, 25)
generic_minor = sp.factor(
    raw_e7_matrix(1, t).extract(generic_rows, generic_columns).det()
)
require_zero(
    generic_minor
    + 782757789696 * t**4 * (t - 3) ** 4 * (2 * t - 3) ** 6,
    "generic exact rank minor",
)
rank_cases = {
    "generic representative": (1, 2, 18),
    "c=3a resonance": (1, 3, 14),
    "2c=3a resonance": (2, 3, 14),
    "c=0 noncritical triple": (1, 0, 16),
    "a=0 marked mixed": (0, 1, 18),
}
for label, (outer_parameter, companion_parameter, expected_rank) in rank_cases.items():
    rank = raw_e7_matrix(outer_parameter, companion_parameter).rank()
    if rank != expected_rank:
        raise AssertionError(f"{label}: raw rank {rank}, expected {expected_rank}")

minor_certificates = {
    "c=3a resonance": (
        (1, 2, 3, 5, 6, 7, 8, 9, 11, 13, 16, 17, 18, 19),
        (1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 15, 16, 19),
        -101559956668416,
        (1, 3),
    ),
    "2c=3a resonance": (
        (7, 8, 11, 13, 16, 17, 18, 19, 23, 25, 30, 31, 32, 33),
        (1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 15, 16, 19),
        -6499837226778624,
        (2, 3),
    ),
    "c=0 noncritical triple": (
        (1, 2, 3, 5, 6, 7, 8, 9, 11, 13, 16, 17, 18, 19, 23, 25),
        (1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 15, 16, 19, 23, 25),
        25999348907114496,
        (1, 0),
    ),
    "a=0 marked mixed": (
        generic_rows,
        generic_columns,
        -50096498540544,
        (0, 1),
    ),
}
for label, (rows, columns, expected_minor, parameters) in minor_certificates.items():
    actual_minor = raw_e7_matrix(*parameters).extract(rows, columns).det()
    require_zero(actual_minor - expected_minor, f"{label}: exact rank minor")


# Shared lower forms.
P2, aa = form("a", 2)
Q2, bb = form("b", 2)
ell = sp.symbols("l0:9")
linear_matrix = sp.Matrix(3, 3, ell)
L = linear_matrix * sp.Matrix([x, y, z])
A, B, w0, w1, w2, w3, w4, w5 = sp.symbols(
    "A B w0 w1 w2 w3 w4 w5"
)
r1, r2 = sp.symbols("r1 r2")


def determinant_after(*substitutions):
    result = linear_matrix.det()
    for substitution in substitutions:
        result = result.subs(substitution)
    return sp.factor(result)


# ---------------------------------------------------------------------------
# Generic a != 0 chart: normalize a=1 and put t=c/a.
# Here t(3-t)(3-2t) != 0.
# ---------------------------------------------------------------------------
Wg = w0 * p + w1 * x * y + w2 * x * z + w4 * q
Ug = (
    A * x * q
    + 2 * w1 * (x**2 * y - y**2 * z) / t
    + 2 * w2 * (x**2 * z - y * z**2) / t
)
Vg = B * x * q - 2 * w1 * y**2 * z / t - 2 * w2 * y * z**2 / t
Rg = x * (p - t * q)
H4g = sp.Matrix([(p - q) ** 2, q**2, 0])
H3g = sp.Matrix([Ug, Vg, Rg])
H2g = sp.Matrix([P2, Q2, Wg])
require_zero(
    weighted_coefficient(sp.zeros(3, 1), sp.Matrix([0, 0, Wg]), H3g, H4g, 7),
    "generic E7 parametrization",
)
E6g = weighted_coefficient(L, H2g, H3g, H4g, 6)
generic_e6 = {
    x**5 * y: -2 * (2 * t - 3) * (B * w1 + bb[1] * t) / t,
    x**5 * z: 2 * (2 * t - 3) * (B * w2 + bb[2] * t) / t,
    x**4 * y**2: -4 * (2 * t - 3) * (bb[3] * t**2 - w1**2) / t**2,
    x**4 * z**2: 4 * (2 * t - 3) * (bb[5] * t**2 - w2**2) / t**2,
    x**3 * y**2 * z: 2
    * (
        3 * A * w1
        + B * t * w1
        - 3 * B * w1
        + 3 * aa[1] * t
        + bb[1] * t**2
        - 3 * bb[1] * t
        - 4 * ell[7] * t
        - 4 * w1 * w4
    )
    / t,
    x**3 * y * z**2: -2
    * (
        3 * A * w2
        + B * t * w2
        - 3 * B * w2
        + 3 * aa[2] * t
        + bb[2] * t**2
        - 3 * bb[2] * t
        - 4 * ell[8] * t
        - 4 * w2 * w4
    )
    / t,
    x**2 * y**3 * z: 4
    * (3 * aa[3] * t + bb[3] * t**2 - 3 * bb[3] * t - w1**2)
    / t,
    x**2 * y * z**3: -4
    * (3 * aa[5] * t + bb[5] * t**2 - 3 * bb[5] * t - w2**2)
    / t,
    x * y**3 * z**2: -2
    * (
        A * t * w1
        - B * t * w1
        + aa[1] * t**2
        - bb[1] * t**2
        - 4 * ell[7] * t
        - 4 * w1 * w4
    )
    / t,
    x * y**2 * z**3: 2
    * (
        A * t * w2
        - B * t * w2
        + aa[2] * t**2
        - bb[2] * t**2
        - 4 * ell[8] * t
        - 4 * w2 * w4
    )
    / t,
    y**4 * z**2: -4 * t * (aa[3] - bb[3]),
    y**2 * z**4: 4 * t * (aa[5] - bb[5]),
}
require_zero(
    E6g - sum(value * monomial for monomial, value in generic_e6.items()),
    "complete generic E6 table",
)
generic_sub6 = {
    bb[1]: -B * w1 / t,
    bb[2]: -B * w2 / t,
    bb[3]: w1**2 / t**2,
    bb[5]: w2**2 / t**2,
    aa[1]: -A * w1 / t,
    aa[2]: -A * w2 / t,
    aa[3]: w1**2 / t**2,
    aa[5]: w2**2 / t**2,
    ell[7]: -w1 * w4 / t,
    ell[8]: -w2 * w4 / t,
}
require_zero(E6g.subs(generic_sub6), "generic E6 solve")
E5g = weighted_coefficient(L, H2g, H3g, H4g, 5).subs(generic_sub6)
generic_sub5 = {
    ell[1]: -aa[4] * w1 / t + 2 * w1**2 * w2 / t**3,
    ell[2]: -aa[4] * w2 / t + 2 * w1 * w2**2 / t**3,
    ell[4]: -bb[4] * w1 / t + 2 * w1**2 * w2 / t**3,
    ell[5]: -bb[4] * w2 / t + 2 * w1 * w2**2 / t**3,
}
require_zero(E5g.subs(generic_sub5), "generic E5 solve")
require_zero(
    determinant_after(generic_sub6, generic_sub5),
    "generic proportional-column exit",
)


# ---------------------------------------------------------------------------
# First resonance c=3a != 0: normalize (a,c)=(1,3).
# ---------------------------------------------------------------------------
W31 = w0 * p + w1 * x * y + w2 * x * z + w3 * y**2 + w4 * q + w5 * z**2
U31 = (
    A * x * q
    + (r1 + sp.Rational(4, 3) * w1) * x**2 * y
    + r1 * y**2 * z
    + (r2 + sp.Rational(4, 3) * w2) * x**2 * z
    + r2 * y * z**2
    + sp.Rational(4, 3) * w3 * x * y**2
    + sp.Rational(4, 3) * w5 * x * z**2
)
V31 = B * x * q + r1 * y**2 * z + r2 * y * z**2
R3 = x * (p - 3 * q)
H431 = sp.Matrix([(p - q) ** 2, q**2, 0])
H331 = sp.Matrix([U31, V31, R3])
H231 = sp.Matrix([P2, Q2, W31])
require_zero(
    weighted_coefficient(sp.zeros(3, 1), sp.Matrix([0, 0, W31]), H331, H431, 7),
    "first-resonance E7 parametrization",
)
E631 = weighted_coefficient(L, H231, H331, H431, 6)
require_zero(coefficient(E631, y**5 * z) + sp.Rational(16, 3) * w3**2, "first resonance w3 square")
require_zero(coefficient(E631, y * z**5) - sp.Rational(16, 3) * w5**2, "first resonance w5 square")
partial31 = {
    w3: 0,
    w5: 0,
    bb[1]: B * r1 / 2,
    bb[2]: B * r2 / 2,
    bb[3]: r1**2 / 4,
    bb[5]: r2**2 / 4,
    aa[3]: r1**2 / 4,
    aa[5]: r2**2 / 4,
}
require_zero(
    coefficient(E631.subs(partial31), x**2 * y**3 * z)
    + sp.Rational(2, 3) * (3 * r1 + 2 * w1) ** 2,
    "first resonance r1 square",
)
require_zero(
    coefficient(E631.subs(partial31), x**2 * y * z**3)
    - sp.Rational(2, 3) * (3 * r2 + 2 * w2) ** 2,
    "first resonance r2 square",
)
res31_sub6 = {
    w3: 0,
    w5: 0,
    r1: -sp.Rational(2, 3) * w1,
    r2: -sp.Rational(2, 3) * w2,
    bb[1]: -B * w1 / 3,
    bb[2]: -B * w2 / 3,
    bb[3]: w1**2 / 9,
    bb[5]: w2**2 / 9,
    aa[1]: -A * w1 / 3 + sp.Rational(4, 3) * ell[7] + sp.Rational(4, 9) * w1 * w4,
    aa[2]: -A * w2 / 3 + sp.Rational(4, 3) * ell[8] + sp.Rational(4, 9) * w2 * w4,
    aa[3]: w1**2 / 9,
    aa[5]: w2**2 / 9,
}
require_zero(E631.subs(res31_sub6), "complete first-resonance E6 solve")
E531 = weighted_coefficient(L, H231, H331, H431, 5).subs(res31_sub6)
s1, s2 = sp.symbols("s1 s2")
res31_sub5 = {
    ell[7]: (s1 - w1 * w4) / 3,
    ell[8]: (s2 - w2 * w4) / 3,
    ell[1]: -aa[4] * w1 / 3 + sp.Rational(2, 27) * w1**2 * w2 + (B - A) * s1 / 9,
    ell[2]: -aa[4] * w2 / 3 + sp.Rational(2, 27) * w1 * w2**2 + (B - A) * s2 / 9,
    ell[4]: -bb[4] * w1 / 3 + sp.Rational(2, 27) * w1**2 * w2,
    ell[5]: -bb[4] * w2 / 3 + sp.Rational(2, 27) * w1 * w2**2,
}
K31 = -3 * A + 6 * B + 8 * w0
residual531 = sp.factor(
    E531.subs(res31_sub5)
    - sp.Rational(2, 9) * x**2 * y * z * (s1 * y - s2 * z) * K31
)
if residual531 != 0:
    raise AssertionError(f"complete first-resonance E5 reduction: {residual531}")
E431special = (
    weighted_coefficient(L, H231, H331, H431, 4)
    .subs(res31_sub6)
    .subs(res31_sub5)
    .subs(A, 2 * B + sp.Rational(8, 3) * w0)
)
require_zero(
    coefficient(E431special, y**3 * z) + sp.Rational(8, 27) * s1**2,
    "first resonance exceptional s1 square",
)
require_zero(
    coefficient(E431special, y * z**3) - sp.Rational(8, 27) * s2**2,
    "first resonance exceptional s2 square",
)
require_zero(
    determinant_after(res31_sub6, res31_sub5, {s1: 0, s2: 0}),
    "first-resonance proportional-column exit",
)


# ---------------------------------------------------------------------------
# Second resonance 2c=3a != 0: normalize (a,c)=(2,3).
# ---------------------------------------------------------------------------
U32 = (
    A * x * q
    - 2 * r1 * x**2 * y
    + 4 * r1 * y**2 * z
    - 2 * r2 * x**2 * z
    + 4 * r2 * y * z**2
)
V32 = (
    B * x * q
    + (-r1 - sp.Rational(2, 3) * w1) * x**2 * y
    + r1 * y**2 * z
    + (-r2 - sp.Rational(2, 3) * w2) * x**2 * z
    + r2 * y * z**2
    - sp.Rational(2, 3) * w3 * x * y**2
    - sp.Rational(2, 3) * w5 * x * z**2
)
H432 = sp.Matrix([(p - 2 * q) ** 2, q**2, 0])
H332 = sp.Matrix([U32, V32, R3])
H232 = sp.Matrix([P2, Q2, W31])
require_zero(
    weighted_coefficient(sp.zeros(3, 1), sp.Matrix([0, 0, W31]), H332, H432, 7),
    "second-resonance E7 parametrization",
)
E632 = weighted_coefficient(L, H232, H332, H432, 6)
require_zero(coefficient(E632, x**2 * y**4) - sp.Rational(16, 3) * w3**2, "second resonance w3 square")
require_zero(coefficient(E632, x**2 * z**4) + sp.Rational(16, 3) * w5**2, "second resonance w5 square")
require_zero(
    coefficient(E632.subs({w3: 0, w5: 0}), x**4 * y**2)
    - sp.Rational(2, 3) * (3 * r1 + 2 * w1) ** 2,
    "second resonance r1 square",
)
require_zero(
    coefficient(E632.subs({w3: 0, w5: 0}), x**4 * z**2)
    + sp.Rational(2, 3) * (3 * r2 + 2 * w2) ** 2,
    "second resonance r2 square",
)
res32_sub6 = {
    w3: 0,
    w5: 0,
    r1: -sp.Rational(2, 3) * w1,
    r2: -sp.Rational(2, 3) * w2,
    aa[1]: -A * w1 / 3,
    aa[2]: -A * w2 / 3,
    aa[3]: sp.Rational(4, 9) * w1**2,
    aa[5]: sp.Rational(4, 9) * w2**2,
    bb[1]: -B * w1 / 3 - sp.Rational(2, 3) * ell[7] - sp.Rational(2, 9) * w1 * w4,
    bb[2]: -B * w2 / 3 - sp.Rational(2, 3) * ell[8] - sp.Rational(2, 9) * w2 * w4,
    bb[3]: w1**2 / 9,
    bb[5]: w2**2 / 9,
}
require_zero(E632.subs(res32_sub6), "complete second-resonance E6 solve")
E532 = weighted_coefficient(L, H232, H332, H432, 5).subs(res32_sub6)
res32_sub5 = {
    ell[7]: (s1 - w1 * w4) / 3,
    ell[8]: (s2 - w2 * w4) / 3,
    ell[1]: A * s1 / 9
    - sp.Rational(8, 9) * B * s1
    - sp.Rational(32, 27) * s1 * w0
    - sp.Rational(16, 27) * s1 * w4
    - aa[4] * w1 / 3
    + sp.Rational(8, 27) * w1**2 * w2,
    ell[2]: A * s2 / 9
    - sp.Rational(8, 9) * B * s2
    - sp.Rational(32, 27) * s2 * w0
    - sp.Rational(16, 27) * s2 * w4
    - aa[4] * w2 / 3
    + sp.Rational(8, 27) * w1 * w2**2,
    ell[4]: A * s1 / 18
    - B * s1 / 3
    - sp.Rational(8, 27) * s1 * w0
    - sp.Rational(4, 27) * s1 * w4
    - bb[4] * w1 / 3
    + sp.Rational(2, 27) * w1**2 * w2,
    ell[5]: A * s2 / 18
    - B * s2 / 3
    - sp.Rational(8, 27) * s2 * w0
    - sp.Rational(4, 27) * s2 * w4
    - bb[4] * w2 / 3
    + sp.Rational(2, 27) * w1 * w2**2,
}
K32 = -3 * A + 6 * B + 8 * w0 + 4 * w4
require_zero(
    E532.subs(res32_sub5)
    + sp.Rational(2, 9) * x**4 * (s1 * y - s2 * z) * K32,
    "complete second-resonance E5 reduction",
)
E432special = (
    weighted_coefficient(L, H232, H332, H432, 4)
    .subs(res32_sub6)
    .subs(res32_sub5)
    .subs(A, 2 * B + sp.Rational(8, 3) * w0 + sp.Rational(4, 3) * w4)
)
require_zero(
    coefficient(E432special, x**2 * y**2) - sp.Rational(8, 27) * s1**2,
    "second resonance exceptional s1 square",
)
require_zero(
    coefficient(E432special, x**2 * z**2) + sp.Rational(8, 27) * s2**2,
    "second resonance exceptional s2 square",
)
require_zero(
    determinant_after(res32_sub6, res32_sub5, {s1: 0, s2: 0}),
    "second-resonance proportional-column exit",
)


# ---------------------------------------------------------------------------
# Noncritical triple c=0,a!=0: normalize a=1.
# ---------------------------------------------------------------------------
W0 = w0 * p + w1 * x * y + w2 * x * z + w4 * q
U0 = (
    A * x * q
    + (-r1 + sp.Rational(4, 3) * w1) * x**2 * y
    + (r1 - sp.Rational(4, 3) * w1) * y**2 * z
    + (-r2 + sp.Rational(4, 3) * w2) * x**2 * z
    + (r2 - sp.Rational(4, 3) * w2) * y * z**2
)
V0 = B * x * q + r1 * y**2 * z + r2 * y * z**2
H30 = sp.Matrix([U0, V0, x**3])
H20 = sp.Matrix([P2, Q2, W0])
require_zero(
    weighted_coefficient(sp.zeros(3, 1), sp.Matrix([0, 0, W0]), H30, H4g, 7),
    "c=0 E7 parametrization",
)
E60 = weighted_coefficient(L, H20, H30, H4g, 6)
require_zero(coefficient(E60, y**4 * z**2) + sp.Rational(8, 3) * w1**2, "c=0 w1 square")
require_zero(coefficient(E60, y**2 * z**4) - sp.Rational(8, 3) * w2**2, "c=0 w2 square")
c0_sub6 = {
    w1: 0,
    w2: 0,
    bb[1]: B * r1 / 2,
    bb[2]: B * r2 / 2,
    bb[3]: r1**2 / 4,
    bb[5]: r2**2 / 4,
    aa[1]: A * r1 / 2,
    aa[2]: A * r2 / 2,
    aa[3]: r1**2 / 4,
    aa[5]: r2**2 / 4,
    ell[7]: r1 * w4 / 2,
    ell[8]: r2 * w4 / 2,
}
require_zero(E60.subs(c0_sub6), "complete c=0 E6 solve")
E50 = weighted_coefficient(L, H20, H30, H4g, 5).subs(c0_sub6)
c0_sub5 = {
    ell[1]: aa[4] * r1 / 2 - r1**2 * r2 / 4,
    ell[2]: aa[4] * r2 / 2 - r1 * r2**2 / 4,
    ell[4]: bb[4] * r1 / 2 - r1**2 * r2 / 4,
    ell[5]: bb[4] * r2 / 2 - r1 * r2**2 / 4,
}
require_zero(E50.subs(c0_sub5), "complete c=0 E5 solve")
require_zero(
    determinant_after(c0_sub6, c0_sub5),
    "c=0 proportional-column exit",
)


# ---------------------------------------------------------------------------
# Marked mixed a=0,c!=0: normalize c=1.
# ---------------------------------------------------------------------------
Wm = w0 * p + w1 * x * y + w2 * x * z + w4 * q
Um = A * x * q
Vm = B * x * q - 2 * w1 * y**2 * z - 2 * w2 * y * z**2
Rm = x * (p - q)
H4m = sp.Matrix([p**2, q**2, 0])
H3m = sp.Matrix([Um, Vm, Rm])
H2m = sp.Matrix([P2, Q2, Wm])
require_zero(
    weighted_coefficient(sp.zeros(3, 1), sp.Matrix([0, 0, Wm]), H3m, H4m, 7),
    "marked-mixed E7 parametrization",
)
E6m = weighted_coefficient(L, H2m, H3m, H4m, 6)
marked_sub6 = {
    bb[1]: -B * w1,
    bb[2]: -B * w2,
    bb[3]: w1**2,
    bb[5]: w2**2,
    aa[1]: -A * w1,
    aa[2]: -A * w2,
    aa[3]: 0,
    aa[5]: 0,
    ell[7]: -w1 * w4,
    ell[8]: -w2 * w4,
}
require_zero(E6m.subs(marked_sub6), "complete marked-mixed E6 solve")
E5m = weighted_coefficient(L, H2m, H3m, H4m, 5).subs(marked_sub6)
marked_sub5 = {
    ell[1]: -aa[4] * w1,
    ell[2]: -aa[4] * w2,
    ell[4]: -bb[4] * w1 + 2 * w1**2 * w2,
    ell[5]: -bb[4] * w2 + 2 * w1 * w2**2,
}
require_zero(E5m.subs(marked_sub5), "complete marked-mixed E5 solve")
require_zero(
    determinant_after(marked_sub6, marked_sub5),
    "marked-mixed proportional-column exit",
)


print("line-(2,2) remaining finite-companion outer-infinity SymPy checks passed")
