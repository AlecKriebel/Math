#!/usr/bin/env python3
"""Independent exact audit of the omitted outer-critical-at-infinity chart."""

from __future__ import annotations

from functools import reduce
from itertools import combinations

import sympy as sp


if not __debug__:
    raise SystemExit("ERROR: exact audit refuses Python optimized mode (-O)")

x, y, z = sp.symbols("x y z")
p = x**2
q = y * z
a, c = sp.symbols("a c")


def monomials(degree: int) -> tuple[sp.Expr, ...]:
    return tuple(
        x**i * y**j * z ** (degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def form(prefix: str, degree: int) -> tuple[sp.Expr, tuple[sp.Symbol, ...]]:
    coefficients = sp.symbols(f"{prefix}0:{len(monomials(degree))}")
    return (
        sum(
            coefficient * monomial
            for coefficient, monomial in zip(coefficients, monomials(degree))
        ),
        coefficients,
    )


def jacobian(first: sp.Expr, second: sp.Expr, third: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.Matrix([first, second, third]).jacobian((x, y, z)).det()
    )


def weight(monomial: sp.Expr) -> int:
    powers = monomial.as_powers_dict()
    return int(powers.get(z, 0) - powers.get(y, 0))


def polynomial_gcd(values: list[sp.Expr]) -> sp.Expr:
    nonzero = [sp.Poly(value, a, c) for value in values if value != 0]
    return sp.factor(reduce(sp.gcd, nonzero).as_expr())


def assert_associate(left: sp.Expr, right: sp.Expr) -> None:
    quotient = sp.cancel(left / right)
    assert quotient.is_Rational and quotient != 0, (left, right, quotient)


U, u = form("u", 3)
V, v = form("v", 3)
W, w = form("w", 2)
H41 = (p - a * q) ** 2
H42 = q**2
R = x * (p - c * q)
E7 = jacobian(H41, H42, W) + jacobian(H41, V, R) + jacobian(U, H42, R)

outputs = monomials(7)
inputs = monomials(3) + monomials(3) + monomials(2)
polynomial = sp.Poly(E7, x, y, z)
matrix, rhs = sp.linear_eq_to_matrix(
    [polynomial.coeff_monomial(monomial) for monomial in outputs],
    u + v + w,
)
assert rhs == sp.zeros(len(outputs), 1)

blocks: dict[int, sp.Matrix] = {}
for current_weight in range(-3, 4):
    rows = [
        index
        for index, monomial in enumerate(outputs)
        if weight(monomial) == current_weight
    ]
    columns = [
        index
        for index, monomial in enumerate(inputs)
        if weight(monomial) == current_weight
    ]
    blocks[current_weight] = matrix.extract(rows, columns)

assert [blocks[index].shape for index in range(-3, 4)] == [
    (3, 2),
    (3, 3),
    (4, 5),
    (4, 6),
    (4, 5),
    (3, 3),
    (3, 2),
]
assert blocks[0] == sp.zeros(4, 6)

for current_weight in (-2, 2):
    assert_associate(
        sp.factor(blocks[current_weight].det()),
        (3 * a - c) * (3 * a - 2 * c),
    )

for current_weight in (-1, 1):
    block = blocks[current_weight]
    minors = [
        block.extract(range(4), columns).det()
        for columns in combinations(range(5), 4)
    ]
    assert_associate(
        polynomial_gcd(minors),
        c * (3 * a - c) * (3 * a - 2 * c),
    )

assert matrix.rank() == 18

# Exact ranks on every orbit type in the finite-companion chart.  For a,c
# both nonzero the common stabilizer scaling leaves c/a invariant.
rank_cases = {
    "generic": ({a: 1, c: 2}, 18, [2, 3, 4, 0, 4, 3, 2]),
    "c=3a resonance": ({a: 1, c: 3}, 14, [2, 2, 3, 0, 3, 2, 2]),
    "c=3a/2 resonance": (
        {a: 2, c: 3},
        14,
        [2, 2, 3, 0, 3, 2, 2],
    ),
    "noncritical triple": ({a: 1, c: 0}, 16, [2, 3, 3, 0, 3, 3, 2]),
    "marked mixed": ({a: 0, c: 1}, 18, [2, 3, 4, 0, 4, 3, 2]),
    "marked triple": ({a: 0, c: 0}, 8, [1, 1, 2, 0, 2, 1, 1]),
}
for _, (substitution, expected_rank, expected_block_ranks) in rank_cases.items():
    assert matrix.subs(substitution).rank() == expected_rank
    assert [
        blocks[current_weight].subs(substitution).rank()
        for current_weight in range(-3, 4)
    ] == expected_block_ranks

# Exact witnesses show that every omitted orbit type is nonempty and survives
# the top E8/E7 identities (they are not asserted to extend to Keller maps).
leading_witnesses = {
    "generic finite mixed": ((p - q) ** 2, x * (p - 2 * q)),
    "c=3a resonance": ((p - q) ** 2, x * (p - 3 * q)),
    "c=3a/2 resonance": ((p - q) ** 2, x * (p - sp.Rational(3, 2) * q)),
    "noncritical triple": ((p - q) ** 2, x**3),
    "marked mixed": (p**2, x * (p - q)),
    "marked triple": (p**2, x**3),
    "noncritical companion infinity": ((p - q) ** 2, x * q),
    "marked companion infinity": (p**2, x * q),
}
for _, (first_quartic, third_cubic) in leading_witnesses.items():
    assert jacobian(first_quartic, q**2, third_cubic) == 0
    assert (
        jacobian(first_quartic, q**2, 0)
        + jacobian(first_quartic, 0, third_cubic)
        + jacobian(0, q**2, third_cubic)
        == 0
    )

print(
    "PASS: omitted outer-infinity chart, resonances, ranks, and leading "
    "witness reconstructed"
)
