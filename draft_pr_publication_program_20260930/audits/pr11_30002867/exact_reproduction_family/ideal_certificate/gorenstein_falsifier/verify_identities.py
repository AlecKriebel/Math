#!/usr/bin/env python3
"""Exact, dependency-free checks of the explicit algebra certificate."""

from itertools import permutations, product
import json
from pathlib import Path


def add(*polynomials):
    result = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] = result.get(monomial, 0) + coefficient
    return {monomial: coefficient for monomial, coefficient in result.items()
            if coefficient}


def multiply(first, second):
    result = {}
    for left, left_coefficient in first.items():
        for right, right_coefficient in second.items():
            monomial = tuple(a + b for a, b in zip(left, right))
            result[monomial] = result.get(monomial, 0) + (
                left_coefficient * right_coefficient
            )
    return {monomial: coefficient for monomial, coefficient in result.items()
            if coefficient}


def negative(polynomial):
    return {monomial: -coefficient
            for monomial, coefficient in polynomial.items()}


zero = {}
x = {(1, 0, 0): 1}
y = {(0, 1, 0): 1}
z = {(0, 0, 1): 1}
x2 = multiply(x, x)
y2 = multiply(y, y)
xz = multiply(x, z)
yz = multiply(y, z)
e = add(multiply(z, z), negative(multiply(x, y)))

d1 = [x2, y2, xz, yz, e]
d2 = [
    [z, zero, zero, y, zero],
    [zero, z, zero, zero, x],
    [negative(x), zero, y, negative(z), zero],
    [zero, negative(y), negative(x), zero, negative(z)],
    [zero, zero, zero, x, y],
]
d3 = [negative(y2), x2, e, yz, negative(xz)]

for column in range(5):
    assert not add(*(multiply(d1[row], d2[row][column]) for row in range(5)))
for row in range(5):
    assert not add(*(multiply(d2[row][column], d3[column]) for column in range(5)))

# Basis is 1,x,y,z,q. This table has integer structure constants.
basis = [tuple(int(i == j) for i in range(5)) for j in range(5)]


def algebra_product(left, right):
    result = [0] * 5
    for i in range(5):
        for j in range(5):
            if i == 0:
                result[j] += left[i] * right[j]
            elif j == 0:
                result[i] += left[i] * right[j]
            elif (i, j) in ((1, 2), (2, 1), (3, 3)):
                result[4] += left[i] * right[j]
    return tuple(result)


for a, b, c in product(basis, repeat=3):
    assert algebra_product(algebra_product(a, b), c) == algebra_product(
        a, algebra_product(b, c)
    )
for a, b in product(basis, repeat=2):
    assert algebra_product(a, b) == algebra_product(b, a)

gram = [[algebra_product(a, b)[4] for b in basis] for a in basis]
determinant = 0
for permutation in permutations(range(5)):
    inversions = sum(permutation[i] > permutation[j]
                     for i in range(5) for j in range(i + 1, 5))
    term = (-1) ** inversions
    for row, column in enumerate(permutation):
        term *= gram[row][column]
    determinant += term
assert determinant == 1

# This identity is integral, so survives reduction in every characteristic.
q_hilbert = {(0,): 1, (1,): 3, (2,): 1}
s_denominator = {(0,): 1, (1,): -3, (2,): 3, (3,): -1}
assert multiply(q_hilbert, s_denominator) == {
    (0,): 1, (2,): -5, (3,): 5, (5,): -1
}

result = {
    "d1_times_d2_zero_over_Z": True,
    "d2_times_d3_zero_over_Z": True,
    "associativity_basis_triples_checked": 125,
    "commutativity_basis_pairs_checked": 25,
    "frobenius_pairing_determinant": determinant,
    "hilbert_numerator_identity_over_Z": True,
    "characteristic_restrictions": [],
    "proof_reference": "algebra_certificate.md",
}
output = Path(__file__).with_name("verification_result.json")
output.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
