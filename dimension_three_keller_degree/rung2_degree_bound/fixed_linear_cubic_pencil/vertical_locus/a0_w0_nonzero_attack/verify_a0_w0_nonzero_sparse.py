#!/usr/bin/env python3
"""Dependency-free exact audit of the a=0, W_0 != 0 E6 exclusion.

The arithmetic engine is pinned by hash.  This checker constructs the raw
determinant and the exterior E6 separately, compares both with the compact
factorization, and checks the decisive coefficient and ideal identities.
It does not import the accompanying SymPy verifier.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import importlib.util
import os
from pathlib import Path
import sys


if not __debug__:
    raise SystemExit("FAIL: optimized Python disables fail-closed assertions")


def fail(message):
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def check(condition, message):
    if not condition:
        fail(message)


KERNEL = (
    Path(__file__).resolve().parent.parent
    / "audit_vertical_triple_yz2_gamma0_ell0"
    / "verify_vertical_triple_yz2_sparse.py"
)
check(KERNEL.is_file(), "sparse arithmetic kernel missing")
check(
    hashlib.sha256(KERNEL.read_bytes()).hexdigest()
    == "9ad87c003bc0ce00e86b8c863b53af356aeec900d487c93999981908e28528e9",
    "sparse arithmetic kernel hash mismatch",
)
spec = importlib.util.spec_from_file_location("a0_w0_sparse_kernel", KERNEL)
check(spec is not None and spec.loader is not None, "cannot load sparse kernel")
sp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sp)


def jac(first, second, third):
    return sp.det3(sp.jacobian((first, second, third)))


def bracket(first, second):
    return sp.sub(
        sp.mul(sp.derivative(first, "x"), sp.derivative(second, "y")),
        sp.mul(sp.derivative(first, "y"), sp.derivative(second, "x")),
    )


def source_degree_part(poly, degree):
    answer = {}
    for exponent, coefficient in poly.items():
        if sum(exponent[position] for position in sp.SOURCE) == degree:
            answer[exponent] = coefficient
    return sp.clean(answer)


def source_coefficient(poly, monomial):
    answer = {}
    for exponent, coefficient in poly.items():
        if tuple(exponent[position] for position in sp.SOURCE) != monomial:
            continue
        reduced = list(exponent)
        for position in sp.SOURCE:
            reduced[position] = 0
        reduced = tuple(reduced)
        answer[reduced] = answer.get(reduced, Fraction(0)) + coefficient
    return sp.clean(answer)


def eq(left, right, message):
    check(sp.sub(left, right) == {}, message)


X, Y, Z = sp.X, sp.Y, sp.Z
kappa = sp.variable("kappa")
gamma = sp.variable("k")
alpha = sp.variable("alpha")
beta = sp.variable("c")
chi = sp.variable("t")
delta = sp.variable("r10")
epsilon = sp.variable("r01")
phi = sp.variable("g0")
u = sp.variable("u")
v = sp.variable("v")
omega = sp.variable("w")

a20 = sp.variable("a0")
a11 = sp.variable("a1")
a02 = sp.variable("a2")
a10 = sp.variable("a3")
a01 = sp.variable("a4")
a00 = sp.variable("a5")
l31 = sp.variable("l6")
l32 = sp.variable("l7")
l33 = sp.variable("l8")

q = sp.add(
    sp.mul(kappa, sp.power(X, 3)),
    sp.mul(
        Z,
        sp.add(
            sp.mul(alpha, sp.power(X, 2)),
            sp.mul(beta, sp.mul(X, Y)),
            sp.mul(chi, sp.power(Y, 2)),
        ),
    ),
    sp.mul(
        sp.power(Z, 2),
        sp.add(sp.mul(delta, X), sp.mul(epsilon, Y)),
    ),
    sp.mul(phi, sp.power(Z, 3)),
)
W = sp.add(
    sp.mul(gamma, sp.power(X, 2)),
    sp.mul(Z, sp.add(sp.mul(u, X), sp.mul(v, Y))),
    sp.mul(omega, sp.power(Z, 2)),
)
L3 = sp.add(sp.mul(l31, X), sp.mul(l32, Y), sp.mul(l33, Z))

mutation = os.environ.get("A0_W0_SPARSE_MUTATION", "")
u_factor = Fraction(5, 3) if mutation == "wrong_U" else Fraction(4, 3)

h2 = (sp.A, sp.B_GENERAL, W)
h3 = (sp.scale(sp.mul(Z, W), u_factor), sp.V_GENERAL, sp.power(Z, 3))
h4 = (sp.power(Z, 4), sp.mul(Z, q), {})
raw = sp.determinant_of_jets(sp.linear_matrix(), h2, h3, h4)
raw_e8 = source_degree_part(raw, 8)
raw_e7 = source_degree_part(raw, 7)
raw_e6 = source_degree_part(raw, 6)
check(raw_e8 == {}, "E8 did not vanish")
check(raw_e7 == {}, "E7 did not vanish")

exterior_e6 = sp.add(
    jac(h4[0], h4[1], L3),
    jac(h3[0], h4[1], W),
    jac(h4[0], h3[1], W),
    jac(sp.A, h4[1], h3[2]),
    jac(h3[0], h3[1], h3[2]),
    jac(h4[0], sp.B_GENERAL, h3[2]),
)
eq(raw_e6, exterior_e6, "raw and exterior E6 differ")

first_bracket = bracket(W, q) if mutation == "flip_bracket" else bracket(q, W)
Phi = sp.add(
    sp.scale(sp.mul(W, first_bracket), 4),
    sp.scale(sp.mul(sp.power(Z, 2), bracket(sp.A, q)), 9),
    sp.scale(sp.mul(sp.power(Z, 3), bracket(q, L3)), 12),
)
eq(
    sp.scale(raw_e6, 3),
    sp.mul(Z, Phi),
    "3 E6 != z Phi",
)


def product(*factors):
    answer = sp.constant(1)
    for factor in factors:
        answer = sp.mul(answer, factor)
    return answer


expected = {
    (3, 1, 1): sp.scale(product(chi, sp.power(gamma, 2)), -16),
    (4, 0, 1): sp.scale(
        sp.mul(
            gamma,
            sp.add(
                sp.scale(product(beta, gamma), -2),
                sp.scale(product(kappa, v), 3),
            ),
        ),
        4,
    ),
    (2, 1, 2): sp.scale(
        sp.add(
            sp.scale(product(a02, kappa), 27),
            sp.scale(product(beta, gamma, v), 2),
            sp.scale(product(chi, gamma, u), 12),
            sp.scale(product(kappa, sp.power(v, 2)), -6),
        ),
        -2,
    ),
    (0, 2, 3): sp.scale(
        sp.add(
            sp.scale(product(a02, beta), 9),
            sp.scale(product(a11, chi), -9),
            sp.scale(product(beta, sp.power(v, 2)), -2),
            sp.scale(product(chi, u, v), 4),
        ),
        -2,
    ),
    (3, 0, 2): sp.add(
        sp.scale(product(a11, kappa), -27),
        sp.scale(product(alpha, gamma, v), 8),
        sp.scale(product(beta, gamma, u), -12),
        sp.scale(product(epsilon, sp.power(gamma, 2)), -8),
        sp.scale(product(kappa, u, v), 12),
    ),
    (0, 1, 4): sp.add(
        sp.scale(product(a01, beta), -9),
        sp.scale(product(a02, delta), -18),
        sp.scale(product(a10, chi), 18),
        sp.scale(product(a11, epsilon), 9),
        sp.scale(product(beta, l32), 12),
        sp.scale(product(beta, v, omega), 4),
        sp.scale(product(chi, l31), -24),
        sp.scale(product(chi, u, omega), -8),
        sp.scale(product(delta, sp.power(v, 2)), 4),
        sp.scale(product(epsilon, u, v), -4),
    ),
}
for monomial, value in expected.items():
    eq(source_coefficient(Phi, monomial), value, f"wrong Phi coefficient {monomial}")

# Check the exact ideal combinations used after chi=0.
r = sp.add(sp.scale(product(beta, gamma), 2), sp.scale(product(kappa, v), -3))
f = sp.add(
    sp.scale(product(kappa, a02), 27),
    sp.scale(product(beta, gamma, v), 2),
    sp.scale(product(kappa, sp.power(v, 2)), -6),
)
g = sp.add(sp.scale(a02, 9), sp.neg(sp.power(v, 2)))
h = sp.add(
    sp.scale(product(a02, beta), 9),
    sp.scale(product(beta, sp.power(v, 2)), -2),
)
eq(
    sp.sub(sp.sub(f, sp.mul(v, r)), sp.scale(sp.mul(kappa, g), 3)),
    {},
    "first ideal identity failed",
)
eq(
    sp.add(sp.sub(h, sp.mul(beta, g)), product(beta, sp.power(v, 2))),
    {},
    "second ideal identity failed",
)
j = sp.add(
    sp.scale(product(kappa, a11), 27),
    sp.scale(product(sp.power(gamma, 2), epsilon), 8),
)
k = sp.scale(product(a11, epsilon), 9)
eq(
    sp.add(
        sp.mul(epsilon, j),
        sp.scale(sp.mul(kappa, k), -3),
        sp.scale(product(sp.power(gamma, 2), sp.power(epsilon, 2)), -8),
    ),
    {},
    "epsilon ideal identity failed",
)

# The exact nonminimal boundary witness survives E8 through E4.  Its complete
# determinant is checked here, including the nonzero lower residual.
identity_matrix = [
    [sp.constant(1), {}, {}],
    [{}, sp.constant(1), {}],
    [{}, {}, sp.constant(1)],
]
boundary_q = sp.power(X, 3)
boundary_w = sp.power(X, 2)
boundary_raw = sp.determinant_of_jets(
    identity_matrix,
    ({}, {}, boundary_w),
    (
        sp.scale(sp.mul(Z, boundary_w), Fraction(4, 3)),
        {},
        sp.power(Z, 3),
    ),
    (sp.power(Z, 4), sp.mul(Z, boundary_q), {}),
)
boundary_expected = sp.add(
    sp.constant(1),
    sp.scale(sp.mul(X, Z), Fraction(8, 3)),
    sp.scale(sp.power(Z, 2), 3),
    sp.scale(sp.power(X, 3), Fraction(-8, 3)),
)
eq(boundary_raw, boundary_expected, "wrong nonminimal boundary determinant")

print("PASS: A0_W0_NONZERO_SPARSE_E6_D91C47")
