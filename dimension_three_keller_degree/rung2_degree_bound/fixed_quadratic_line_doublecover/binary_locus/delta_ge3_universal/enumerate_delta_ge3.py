#!/usr/bin/env python3
"""Exact low-memory enumeration of the delta>=3 top-incidence strata.

The input is
    P = h*p^2, Q = h*q^2, R = a*p^3+b*p^2*q+c*p*q^2+d*q^3.
For each of the four fixed-divisor orbit charts (splitting the last chart
at its doubled-root boundary), this script imposes divisibility of
alpha=J(Q,R) and beta=-J(P,R) by every degree-three/four divisor of
gamma=J(P,Q).  All conditions are linear in a,b,c,d.

This is an exploratory generator.  The release verifier contains pinned
normal forms and fail-closed mutations.
"""

from __future__ import annotations

from itertools import product
from itertools import combinations

import sympy as sp

p, q = sp.symbols("p q")
a, b, c, d = sp.symbols("a b c d")
s = sp.symbols("s")
coeffs = (a, b, c, d)
R0 = a * p**3 + b * p**2 * q + c * p * q**2 + d * q**3


def jac(f, g):
    return sp.expand(sp.diff(f, p) * sp.diff(g, q)
                     - sp.diff(f, q) * sp.diff(g, p))


def equations_at_root(poly, root, exponent):
    """Conditions for (p-root*q)^exponent to divide a binary form."""
    result = []
    for order in range(exponent):
        value = sp.expand(sp.diff(poly, p, order).subs(p, root * q))
        scalar = sp.cancel(value / q ** (5 - order))
        result.append(sp.factor(scalar))
    return result


def equations_at_infinity(poly, exponent):
    """Conditions for q^exponent to divide a binary quintic."""
    result = []
    for order in range(exponent):
        value = sp.expand(sp.diff(poly, q, order).subs(q, 0))
        scalar = sp.cancel(value / p ** (5 - order))
        result.append(sp.factor(scalar))
    return result


def order_at_root(poly, root):
    for exponent in range(6):
        value = sp.factor(
            sp.cancel(sp.diff(poly, p, exponent).subs(p, root * q))
        )
        if value != 0:
            return exponent
    return 6


def order_at_infinity(poly):
    for exponent in range(6):
        value = sp.factor(
            sp.cancel(sp.diff(poly, q, exponent).subs(q, 0))
        )
        if value != 0:
            return exponent
    return 6


def is_dependent(alpha, beta):
    avec = sp.Matrix([
        sp.Poly(alpha, p, q).coeff_monomial(p ** (5 - i) * q**i)
        for i in range(6)
    ])
    bvec = sp.Matrix([
        sp.Poly(beta, p, q).coeff_monomial(p ** (5 - i) * q**i)
        for i in range(6)
    ])
    return all(
        sp.expand(avec[i] * bvec[j] - avec[j] * bvec[i]) == 0
        for i in range(6)
        for j in range(i + 1, 6)
    )


def enumerate_chart(label, h, factors):
    P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
    alpha, beta, gamma = jac(Q, R0), -jac(P, R0), jac(P, Q)
    print(f"=== {label} ===")
    seen = set()
    for delta in (3, 4):
        for exponents in product(*(range(cap + 1) for _, _, cap in factors)):
            if sum(exponents) != delta:
                continue
            equations = []
            for (name, root, _), exponent in zip(factors, exponents):
                if root == "infinity":
                    equations.extend(equations_at_infinity(alpha, exponent))
                    equations.extend(equations_at_infinity(beta, exponent))
                else:
                    equations.extend(equations_at_root(alpha, root, exponent))
                    equations.extend(equations_at_root(beta, root, exponent))
            matrix, rhs = sp.linear_eq_to_matrix(equations, coeffs)
            assert rhs == sp.zeros(len(equations), 1)
            kernel = matrix.nullspace()
            if not kernel:
                continue
            key = tuple(tuple(sp.factor(x) for x in col) for col in kernel)
            # Different requested divisors can give the same higher-delta
            # kernel.  Print each kernel only after computing its true order.
            if key in seen:
                continue
            seen.add(key)
            parameters = sp.symbols(f"z0:{len(kernel)}")
            vector = sum(
                (parameter * column
                 for parameter, column in zip(parameters, kernel)),
                sp.zeros(4, 1),
            )
            sub = dict(zip(coeffs, vector))
            aa, bb = sp.expand(alpha.subs(sub)), sp.expand(beta.subs(sub))
            actual_orders = []
            for name, root, _ in factors:
                if root == "infinity":
                    actual_orders.append(order_at_infinity(aa))
                else:
                    actual_orders.append(order_at_root(aa, root))
                # alpha and beta must have the same gcd order after taking
                # the minimum; gamma caps are applied below.
                if root == "infinity":
                    actual_orders[-1] = min(
                        actual_orders[-1], order_at_infinity(bb)
                    )
                else:
                    actual_orders[-1] = min(
                        actual_orders[-1], order_at_root(bb, root)
                    )
            actual_orders = tuple(
                min(order, cap)
                for order, (_, _, cap) in zip(actual_orders, factors)
            )
            actual_delta = sum(actual_orders)
            dep = is_dependent(aa, bb)
            names = ",".join(
                f"{name}^{power}"
                for (name, _, _), power in zip(factors, actual_orders)
                if power
            )
            R = sp.factor(R0.subs(sub))
            print(
                f"requested delta={delta} -> actual={actual_delta}; "
                f"g={names}; dim={len(kernel)}; dependent={dep}; R={R}"
            )


enumerate_chart(
    "branch_square",
    p**2,
    (("p", 0, 5), ("q", "infinity", 1)),
)
enumerate_chart(
    "two_branch",
    p * q,
    (("p", 0, 3), ("q", "infinity", 3)),
)
enumerate_chart(
    "one_branch",
    p * (p + q),
    (("p", 0, 3), ("q", "infinity", 1), ("L", -1, 2)),
)
enumerate_chart(
    "doubled_nonbranch",
    (p + q) ** 2,
    (("p", 0, 1), ("q", "infinity", 1), ("L", -1, 4)),
)
L = p - s * q
M = s * p - q
enumerate_chart(
    "squarefree_interior",
    sp.expand(L * M),
    (("p", 0, 1), ("q", "infinity", 1),
     ("L", s, 2), ("M", 1 / s, 2)),
)


def interior_rank_drop(exponents):
    h = sp.expand(L * M)
    P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
    alpha, beta = jac(Q, R0), -jac(P, R0)
    factors = (
        ("p", 0, 1), ("q", "infinity", 1),
        ("L", s, 2), ("M", 1 / s, 2),
    )
    equations = []
    for (_, root, _), exponent in zip(factors, exponents):
        if root == "infinity":
            equations.extend(equations_at_infinity(alpha, exponent))
            equations.extend(equations_at_infinity(beta, exponent))
        else:
            equations.extend(equations_at_root(alpha, root, exponent))
            equations.extend(equations_at_root(beta, root, exponent))
    matrix, rhs = sp.linear_eq_to_matrix(equations, coeffs)
    assert rhs == sp.zeros(len(equations), 1)
    numerators = []
    for rows in combinations(range(matrix.rows), 4):
        value = sp.factor(matrix.extract(rows, range(4)).det())
        if value != 0:
            numerators.append(sp.factor(sp.together(value).as_numer_denom()[0]))
    common = numerators[0]
    for value in numerators[1:]:
        common = sp.gcd(common, value)
    print(
        "INTERIOR DELTA4 PATTERN",
        exponents,
        "generic rank",
        matrix.rank(),
        "rank-drop gcd",
        sp.factor(common),
    )
    return matrix, sp.factor(common)


for pattern in (
    (0, 0, 2, 2),
    (1, 0, 2, 1),
    (1, 1, 2, 0),
    (1, 1, 1, 1),
):
    interior_rank_drop(pattern)
