#!/usr/bin/env python3
"""Standard-library exact replay of the odd-sector affine Hodge identity."""

from __future__ import annotations

from fractions import Fraction


Exponent = tuple[int, ...]
Polynomial = dict[Exponent, Fraction]
VARIABLES = 8
ZERO_EXPONENT = (0,) * VARIABLES


def clean(poly: Polynomial) -> Polynomial:
    return {monomial: coefficient
            for monomial, coefficient in poly.items() if coefficient}


def constant(value: int | Fraction) -> Polynomial:
    coefficient = Fraction(value)
    return {} if not coefficient else {ZERO_EXPONENT: coefficient}


def variable(index: int) -> Polynomial:
    exponent = [0] * VARIABLES
    exponent[index] = 1
    return {tuple(exponent): Fraction(1)}


def add(*polynomials: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for poly in polynomials:
        for monomial, coefficient in poly.items():
            result[monomial] = result.get(monomial, Fraction(0)) + coefficient
    return clean(result)


def scale(value: int | Fraction, poly: Polynomial) -> Polynomial:
    coefficient = Fraction(value)
    return clean({monomial: coefficient * entry
                  for monomial, entry in poly.items()})


def subtract(left: Polynomial, right: Polynomial) -> Polynomial:
    return add(left, scale(-1, right))


def multiply(*polynomials: Polynomial) -> Polynomial:
    result = constant(1)
    for poly in polynomials:
        product: Polynomial = {}
        for left, left_coefficient in result.items():
            for right, right_coefficient in poly.items():
                monomial = tuple(a + b for a, b in zip(left, right))
                product[monomial] = (
                    product.get(monomial, Fraction(0))
                    + left_coefficient * right_coefficient
                )
        result = clean(product)
    return result


def power(poly: Polynomial, exponent: int) -> Polynomial:
    result = constant(1)
    for _ in range(exponent):
        result = multiply(result, poly)
    return result


def substitute(poly: Polynomial, replacements: list[Polynomial]) -> Polynomial:
    result: Polynomial = {}
    for monomial, coefficient in poly.items():
        term = constant(coefficient)
        for index, exponent in enumerate(monomial):
            if exponent:
                term = multiply(term, power(replacements[index], exponent))
        result = add(result, term)
    return result


Y = [variable(index) for index in range(4)]
Z = [variable(index + 4) for index in range(4)]
i, j, k, l = 0, 1, 2, 3

# Coefficient of 2(m_i-m_j)-m_ik-m_il.
K = add(
    scale(2, multiply(Z[i], Y[j], Y[k], Y[l])),
    scale(-2, multiply(Y[i], Z[j], Y[k], Y[l])),
    scale(-1, multiply(Z[i], Y[j], Z[k], Y[l])),
    scale(-1, multiply(Z[i], Y[j], Y[k], Z[l])),
)

# A<->B and C<->D both interchange Y and Z.
swap_yz = Z + Y
K_minus = scale(Fraction(1, 2), subtract(K, substitute(K, swap_yz)))
certificate = scale(
    Fraction(-1, 2),
    multiply(
        subtract(multiply(Y[i], Z[j]), multiply(Y[j], Z[i])),
        add(
            scale(2, multiply(Y[k], Y[l])),
            scale(-1, multiply(Y[k], Z[l])),
            scale(-1, multiply(Y[l], Z[k])),
            scale(2, multiply(Z[k], Z[l])),
        ),
    ),
)
assert K_minus == certificate

# B<->C sends (Y,Z) to (Y-Z,-Z) by the two-dimensional epsilon identity.
swap_bc = [subtract(Y[r], Z[r]) for r in range(4)] + [
    scale(-1, Z[r]) for r in range(4)
]
assert add(substitute(K_minus, swap_yz), K_minus) == {}
assert add(substitute(K_minus, swap_bc), K_minus) == {}


# Replay the Walsh calculation as exact coefficient vectors in the eight
# independent moments m_T, with m_(complement T)=-m_T.
Vector = tuple[Fraction, ...]


def vector_add(*vectors: Vector) -> Vector:
    return tuple(sum(entries, Fraction(0)) for entries in zip(*vectors))


def vector_scale(value: int | Fraction, vector: Vector) -> Vector:
    coefficient = Fraction(value)
    return tuple(coefficient * entry for entry in vector)


def moment(mask: int) -> Vector:
    complement = 15 ^ mask
    representative = mask if mask < complement else complement
    sign = 1 if mask < complement else -1
    return tuple(Fraction(sign if index == representative else 0)
                 for index in range(8))


def parity(mask: int) -> int:
    return mask.bit_count() & 1


def q(mask: int) -> Vector:
    return vector_scale(
        Fraction(1, 16),
        vector_add(*[
            vector_scale(-1 if parity(mask & subset) else 1, moment(subset))
            for subset in range(16)
        ]),
    )


site_i, site_j, site_k, site_l = 1, 2, 4, 8
walsh_difference = vector_add(
    vector_scale(3, q(15 ^ site_i)),
    vector_scale(-1, q(site_i)),
    vector_scale(-3, q(15 ^ site_j)),
    q(site_j),
)
moment_certificate = vector_scale(
    Fraction(1, 2),
    vector_add(
        vector_scale(2, moment(site_i)),
        vector_scale(-2, moment(site_j)),
        vector_scale(-1, moment(site_i | site_k)),
        vector_scale(-1, moment(site_i | site_l)),
    ),
)
assert walsh_difference == moment_certificate

# Lemma 2.1 makes the right side below zero, so 3q_(bar i)-q_i is
# independent of the singleton i.  Replay all three displayed relations,
# taking site 8 as the reference and the other two sites as k,l.
for singleton in (1, 2, 4):
    other_sites = [site for site in (1, 2, 4, 8)
                   if site not in (singleton, 8)]
    walsh_relation = vector_add(
        vector_scale(3, q(15 ^ singleton)),
        vector_scale(-1, q(singleton)),
        vector_scale(-3, q(7)),
        q(8),
    )
    lemma_relation = vector_scale(
        Fraction(1, 2),
        vector_add(
            vector_scale(2, moment(singleton)),
            vector_scale(-2, moment(8)),
            vector_scale(-1, moment(singleton | other_sites[0])),
            vector_scale(-1, moment(singleton | other_sites[1])),
        ),
    )
    assert walsh_relation == lemma_relation

print("balanced Hodge affine identity: exact standard-library checks passed")
