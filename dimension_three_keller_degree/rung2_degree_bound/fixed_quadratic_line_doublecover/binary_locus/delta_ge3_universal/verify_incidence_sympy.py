#!/usr/bin/env python3
"""Exact certificate for the universal binary delta>=3 denominator.

The computation is deliberately small.  Every incidence condition is a
linear divisibility condition in the four coefficients of a binary cubic.
The only parameterized rank calculation is univariate in the squarefree
fixed-divisor modulus s.
"""

from __future__ import annotations

import sys
from itertools import combinations, product

if not __debug__:
    print("FAIL: assertions are required", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp

p, q = sp.symbols("p q")
a, b, c, d = sp.symbols("a b c d")
A, B, C = sp.symbols("A B C")
s = sp.symbols("s")
coeffs = (a, b, c, d)
Rraw = a * p**3 + b * p**2 * q + c * p * q**2 + d * q**3


def jac(f, g):
    return sp.expand(sp.diff(f, p) * sp.diff(g, q)
                     - sp.diff(f, q) * sp.diff(g, p))


def equal(left, right):
    return sp.factor(sp.cancel(left - right)) == 0


def triple(h, R):
    P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
    return jac(Q, R), -jac(P, R), jac(P, Q)


def at_root(poly, root, order):
    return sp.factor(
        sp.cancel(sp.diff(poly, p, order).subs(p, root * q))
    )


def at_infinity(poly, order):
    return sp.factor(
        sp.cancel(sp.diff(poly, q, order).subs(q, 0))
    )


def root_order(polys, root, cap):
    for order in range(cap + 1):
        values = [at_root(poly, root, order) for poly in polys]
        if any(value != 0 for value in values):
            return order
    return cap


def infinity_order(polys, cap):
    for order in range(cap + 1):
        values = [at_infinity(poly, order) for poly in polys]
        if any(value != 0 for value in values):
            return order
    return cap


def signature(h, R, factors):
    polys = triple(h, R)
    output = []
    for _, root, cap in factors:
        if root == "infinity":
            output.append(infinity_order(polys, cap))
        else:
            output.append(root_order(polys, root, cap))
    return tuple(output)


def coefficient_vector(poly):
    value = sp.Poly(poly, p, q)
    return sp.Matrix([
        value.coeff_monomial(p ** (5 - i) * q**i)
        for i in range(6)
    ])


def dependent(h, R):
    alpha, beta, _ = triple(h, R)
    av, bv = coefficient_vector(alpha), coefficient_vector(beta)
    return all(
        sp.expand(av[i] * bv[j] - av[j] * bv[i]) == 0
        for i in range(6)
        for j in range(i + 1, 6)
    )


def divisibility_equations(poly, root, exponent):
    if root == "infinity":
        return [
            sp.factor(at_infinity(poly, order) / p ** (5 - order))
            for order in range(exponent)
        ]
    return [
        sp.factor(at_root(poly, root, order) / q ** (5 - order))
        for order in range(exponent)
    ]


def exact_pattern_set(h, factors, delta):
    alpha, beta, _ = triple(h, Rraw)
    output = set()
    for exponents in product(*(range(cap + 1) for _, _, cap in factors)):
        if sum(exponents) != delta:
            continue
        equations = []
        for (_, root, _), exponent in zip(factors, exponents):
            equations += divisibility_equations(alpha, root, exponent)
            equations += divisibility_equations(beta, root, exponent)
        matrix, rhs = sp.linear_eq_to_matrix(equations, coeffs)
        assert rhs == sp.zeros(len(equations), 1)
        kernel = matrix.nullspace()
        if not kernel:
            continue
        zs = sp.symbols(f"z0:{len(kernel)}")
        vector = sum(
            (z * column for z, column in zip(zs, kernel)),
            sp.zeros(4, 1),
        )
        R = sp.expand(Rraw.subs(dict(zip(coeffs, vector))))
        actual = signature(h, R, factors)
        if actual == exponents and not dependent(h, R):
            output.add(exponents)
    return output


BS = (("p", 0, 5), ("q", "infinity", 1))
TB = (("p", 0, 3), ("q", "infinity", 3))
OB = (("p", 0, 3), ("q", "infinity", 1), ("L", -1, 2))
DN = (("p", 0, 1), ("q", "infinity", 1), ("L", -1, 4))
Lint = p - s * q
Mint = s * p - q
SF = (
    ("p", 0, 1), ("q", "infinity", 1),
    ("L", s, 2), ("M", 1 / s, 2),
)

assert exact_pattern_set(p**2, BS, 3) == {(3, 0), (2, 1)}
assert exact_pattern_set(p**2, BS, 4) == set()
assert exact_pattern_set(p * q, TB, 3) == {
    (3, 0), (2, 1), (1, 2), (0, 3)
}
assert exact_pattern_set(p * q, TB, 4) == set()
assert exact_pattern_set(p * (p + q), OB, 3) == {
    (3, 0, 0), (2, 1, 0), (2, 0, 1),
    (1, 1, 1), (1, 0, 2), (0, 1, 2),
}
assert exact_pattern_set(p * (p + q), OB, 4) == set()
assert exact_pattern_set((p + q) ** 2, DN, 3) == {
    (0, 0, 3), (1, 0, 2), (0, 1, 2), (1, 1, 1)
}
assert exact_pattern_set((p + q) ** 2, DN, 4) == {
    (0, 0, 4), (1, 0, 3), (0, 1, 3), (1, 1, 2)
}
assert exact_pattern_set(sp.expand(Lint * Mint), SF, 3) == {
    (0, 0, 2, 1), (0, 0, 1, 2),
    (1, 0, 2, 0), (1, 0, 0, 2),
    (0, 1, 2, 0), (0, 1, 0, 2),
    (1, 0, 1, 1), (0, 1, 1, 1),
    (1, 1, 1, 0), (1, 1, 0, 1),
}
assert exact_pattern_set(sp.expand(Lint * Mint), SF, 4) == set()

print("PASS generic linear-divisibility enumeration")


def rank_drop_gcd(exponents):
    h = sp.expand(Lint * Mint)
    alpha, beta, _ = triple(h, Rraw)
    equations = []
    for (_, root, _), exponent in zip(SF, exponents):
        equations += divisibility_equations(alpha, root, exponent)
        equations += divisibility_equations(beta, root, exponent)
    matrix, rhs = sp.linear_eq_to_matrix(equations, coeffs)
    assert rhs == sp.zeros(len(equations), 1)
    minors = []
    for rows in combinations(range(matrix.rows), 4):
        value = sp.factor(matrix.extract(rows, range(4)).det())
        if value != 0:
            minors.append(sp.factor(sp.together(value).as_numer_denom()[0]))
    common = minors[0]
    for value in minors[1:]:
        common = sp.gcd(common, value)
    return sp.factor(common)


assert rank_drop_gcd((0, 0, 2, 2)) == 9 * (s - 1) ** 8 * (s + 1) ** 8
assert rank_drop_gcd((1, 0, 2, 1)) == (
    9 * (s - 1) ** 5 * (s + 1) ** 5 * (s**2 + 5)
)
assert rank_drop_gcd((1, 1, 2, 0)) == (
    9 * s**2 * (s - 1) ** 2 * (s + 1) ** 2
    * (5 * s**4 - 6 * s**2 + 5)
)
assert rank_drop_gcd((1, 1, 1, 1)) == (
    9 * (s - 1) ** 3 * (s + 1) ** 3
    * (s**2 - 4 * s + 1) * (s**2 + 4 * s + 1)
)

print("PASS saturation-safe squarefree delta-four rank loci")


def check(h, R, factors, expected, name):
    got = signature(h, sp.expand(R), factors)
    assert got == expected, f"{name}: {got} != {expected}"
    assert not dependent(h, sp.expand(R)), f"{name}: dependent alpha,beta"


L = p + q

# Branch-square and two-branch representatives.
check(p**2, p**2 * (A * p + B * q), BS, (3, 0), "D3-BS-P3")
check(p**2, p * (A * p**2 + C * q**2), BS, (2, 1), "D3-BS-P2Q")
check(p * q, p**3, TB, (3, 0), "D3-TB-P3")
check(p * q, p**2 * q, TB, (2, 1), "D3-TB-P2Q")

# One-branch representatives.
ob_forms = (
    (p**3, (3, 0, 0), "D3-OB-P3"),
    (p**2 * L, (2, 0, 1), "D3-OB-P2L"),
    (p * L**2, (1, 0, 2), "D3-OB-PL2"),
    (p**2 * (4 * p + 3 * q), (2, 1, 0), "D3-OB-P2Q"),
    (p * L * (4 * p - q), (1, 1, 1), "D3-OB-PQL"),
    (L**2 * (4 * p - 5 * q), (0, 1, 2), "D3-OB-QL2"),
)
for R, expected, name in ob_forms:
    check(p * L, R, OB, expected, name)

# Doubled-nonbranch representatives, including their exact boundaries.
R_dn_l3 = L**2 * (A * p + B * q)
R_dn_pl2 = L * (A * p**2 + sp.Rational(1, 2) * C * p * q + C * q**2)
R_dn_pql = A * (2 * p**3 + 3 * p**2 * q) + B * (
    3 * p * q**2 + 2 * q**3
)
check(L**2, R_dn_l3, DN, (0, 0, 3), "D3-DN-L3")
check(L**2, R_dn_pl2, DN, (1, 0, 2), "D3-DN-PL2")
check(L**2, R_dn_pql, DN, (1, 1, 1), "D3-DN-PQL")
assert signature(L**2, R_dn_l3.subs(B, A), DN) == (0, 0, 4)
assert signature(L**2, R_dn_pl2.subs(A, -C / 2), DN) == (1, 0, 3)
assert signature(L**2, R_dn_pl2.subs(A, C), DN) == (1, 1, 2)
assert signature(L**2, R_dn_pql.subs(B, A), DN) == (1, 1, 2)

dn_d4 = (
    (L**3, (0, 0, 4), "D4-DN-L4"),
    (L**2 * (p - 2 * q), (1, 0, 3), "D4-DN-PL3"),
    (L * (2 * p**2 + p * q + 2 * q**2), (1, 1, 2),
     "D4-DN-PQL2"),
)
for R, expected, name in dn_d4:
    check(L**2, R, DN, expected, name)

# Four generic squarefree delta-three families.
h_sf = sp.expand(Lint * Mint)
R_sf_21 = sp.expand(Lint**2 * Mint)
R_sf_2c = sp.expand(
    Lint**2 * ((3 * s**2 - 5) * p - 4 * s * q)
)
R_sf_11c = sp.expand(
    Lint * Mint * (4 * s * p + (s**2 + 1) * q)
)
R_sf_1c2 = sp.expand(
    Mint
    * (
        4 * p**2 * s**3 - 12 * p**2 * s
        - 3 * p * q * s**4 + 10 * p * q * s**2 - 3 * p * q
        - 12 * q**2 * s**3 + 4 * q**2 * s
    )
)
check(h_sf, R_sf_21, SF, (0, 0, 2, 1), "D3-SF-21")
check(h_sf, R_sf_2c, SF, (1, 0, 2, 0), "D3-SF-2C")
check(h_sf, R_sf_11c, SF, (0, 1, 1, 1), "D3-SF-11C")
check(h_sf, R_sf_1c2, SF, (1, 1, 0, 1), "D3-SF-1C2")

# Literal boundary factors; these are the saturation divisors declared in
# the machine-readable denominator.
alpha, beta, _ = triple(h_sf, R_sf_21)
assert equal(alpha.subs(p, 0) / q**5, -s**2 * (s**2 + 5))
assert equal(beta.subs(q, 0) / p**5, s * (5 * s**2 + 1))

alpha, beta, _ = triple(h_sf, R_sf_2c)
assert alpha.subs(p, 0) == beta.subs(p, 0) == 0
assert equal(
    beta.subs(q, 0) / p**5,
    3 * (5 * s**4 - 6 * s**2 + 5),
)
assert equal(
    sp.cancel(R_sf_2c / Lint**2).subs(q, s * p) / p,
    -(s**2 + 5),
)

alpha, beta, _ = triple(h_sf, R_sf_11c)
assert alpha.subs(q, 0) == beta.subs(q, 0) == 0
assert equal(
    alpha.subs(p, 0) / q**5,
    s * (s**2 - 4 * s + 1) * (s**2 + 4 * s + 1),
)
linear_11c = 4 * s * p + (s**2 + 1) * q
assert equal(linear_11c.subs(p, s * q) / q, 5 * s**2 + 1)
assert equal(linear_11c.subs(q, s * p) / p, s * (s**2 + 5))

alpha, beta, _ = triple(h_sf, R_sf_1c2)
assert alpha.subs(p, 0) == beta.subs(p, 0) == 0
assert alpha.subs(q, 0) == beta.subs(q, 0) == 0
quadratic_1c2 = sp.cancel(R_sf_1c2 / Mint)
assert equal(
    quadratic_1c2.subs(q, s * p) / p**2,
    -3 * s * (5 * s**4 - 6 * s**2 + 5),
)
assert equal(
    quadratic_1c2.subs(p, s * q) / q**2,
    s * (s**2 - 4 * s + 1) * (s**2 + 4 * s + 1),
)

print("PASS pinned delta-three normal forms and every internal divisor")


def zero_mod(value, modulus):
    numerator = sp.together(value).as_numer_denom()[0]
    return sp.rem(sp.Poly(numerator, s), sp.Poly(modulus, s)).as_expr() == 0


def order_mod(polys, root, cap, modulus):
    for order in range(cap + 1):
        values = []
        for poly in polys:
            if root == "infinity":
                value = at_infinity(poly, order)
            else:
                value = at_root(poly, root, order)
            values.append(zero_mod(value, modulus))
        if not all(values):
            return order
    return cap


def signature_mod(h, R, factors, modulus):
    polys = triple(h, R)
    return tuple(
        order_mod(polys, root, cap, modulus)
        for _, root, cap in factors
    )


special = (
    (
        s**2 + 5,
        R_sf_21,
        (1, 0, 2, 1),
        sp.Rational(-16, 5),
        "D4-SF-21C",
    ),
    (
        5 * s**4 - 6 * s**2 + 5,
        R_sf_2c,
        (1, 1, 2, 0),
        sp.Rational(16, 5),
        "D4-SF-2C2",
    ),
    (
        s**2 - 4 * s + 1,
        sp.expand(Lint * Mint * (p + q)),
        (1, 1, 1, 1),
        sp.Integer(16),
        "D4-SF-11C2",
    ),
)
for modulus, R, expected, kappa, name in special:
    got = signature_mod(h_sf, R, SF, modulus)
    assert got == expected, f"{name}: {got} != {expected}"
    assert zero_mod((s + 1 / s) ** 2 - kappa, modulus)

print("PASS three algebraic squarefree delta-four orbits and moduli")

# Fixed-divisor chart boundaries in the chosen symmetric normalization.
assert equal(R_sf_21.subs(s, 1), (p - q) ** 3)
assert equal(R_sf_2c.subs(s, 1), -2 * (p - q) ** 2 * (p + 2 * q))
assert equal(R_sf_11c.subs(s, 1), 2 * (p - q) ** 2 * (2 * p + q))
assert equal(
    R_sf_1c2.subs(s, 1),
    -4 * (p - q) * (2 * p**2 - p * q + 2 * q**2),
)
assert equal(R_sf_21.subs(s, 0), -p**2 * q)
assert equal(R_sf_2c.subs(s, 0), -5 * p**3)
assert equal(R_sf_11c.subs(s, 0), -p * q**2)
assert equal(R_sf_1c2.subs(s, 0), 3 * p * q**2)

assert dependent(p**2, p**3)
print("PASS fixed-divisor boundary arrows and unique power fibre")
print("DELTA_GE3_UNIVERSAL_SYMPY_PASS_17_6_1")
