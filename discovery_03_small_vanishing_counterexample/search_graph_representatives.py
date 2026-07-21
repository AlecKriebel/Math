#!/usr/bin/env python3
"""Search cubic graph representatives with constant Jacobian.

Put p=xy, q=xz, r=p^2.  Each monomial of the normalized 3D Keller map has
several representatives of degree at most three in (x,y,z,p,q,r).  For each
of the 2,592 direct choices, this script checks the determinant of the natural
six-dimensional graph extension at deterministic finite-field samples.
Survivors are then certified symbolically over Q.
"""

from __future__ import annotations

from itertools import product
import random

import sympy as sp


x, y, z, p, q, r = sp.symbols("x y z p q r")
VARS = (x, y, z, p, q, r)


# Each entry is (output coordinate, alternatives).  Coefficients are included.
GROUPS = [
    (0, (-sp.Rational(3, 2) * x * p, -sp.Rational(3, 2) * x**2 * y)),
    (1, (3 * q, 3 * x * z)),
    (1, (12 * y * p, 12 * x * y**2)),
    (1, (6 * p * q, 6 * x * y * q, 6 * x * z * p)),
    (1, (9 * y * r, 9 * y * p**2)),
    (1, (3 * q * r, 3 * p**2 * q, 3 * x * z * r)),
    (2, (3 * z * p, 3 * y * q, 3 * x * y * z)),
    (2, (3 * z * r, 3 * z * p**2, 3 * y * p * q)),
    (2, (z * p * r, y * q * r)),
]

FIXED = [
    x - sp.Rational(1, 2) * x**2 * q,
    y,
    z + 4 * y**2 + 7 * y**2 * p + 3 * y**2 * r,
]


def det3(matrix, modulus):
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return (
        a * (e * i - f * h)
        - b * (d * i - f * g)
        + c * (d * h - e * g)
    ) % modulus


def rational_mod(value, modulus):
    value = sp.Rational(value)
    return int(value.p % modulus) * pow(int(value.q), -1, modulus) % modulus


def adapted_gradient(poly, sample, modulus):
    """Gradient in x,y,z with graph-error variables held fixed."""
    xx, yy, zz, aa, bb, cc = sample
    pp = (xx * yy + aa) % modulus
    qq = (xx * zz + bb) % modulus
    rr = (pp * pp + cc) % modulus
    values = dict(zip(VARS, (xx, yy, zz, pp, qq, rr)))
    chain = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (yy, xx, 0),
        (zz, 0, xx),
        (2 * pp * yy, 2 * pp * xx, 0),
    )
    result = [0, 0, 0]
    for variable_index, variable in enumerate(VARS):
        derivative = sp.Poly(sp.diff(poly, variable), *VARS)
        value = 0
        for monomial, coefficient in derivative.terms():
            term = rational_mod(coefficient, modulus)
            for v, exponent in zip(VARS, monomial):
                term = term * pow(values[v], exponent, modulus) % modulus
            value = (value + term) % modulus
        for j in range(3):
            result[j] = (result[j] + value * chain[variable_index][j]) % modulus
    return tuple(result)


def samples(modulus, count, seed):
    rng = random.Random(seed)
    return [tuple(rng.randrange(1, modulus) for _ in range(6)) for _ in range(count)]


def finite_field_survivors(modulus=1_000_003, sample_count=12, seed=20260721):
    test_points = samples(modulus, sample_count, seed)
    fixed_rows = [
        [[adapted_gradient(FIXED[row], point, modulus) for row in range(3)]][0]
        for point in test_points
    ]
    option_rows = []
    for coordinate, alternatives in GROUPS:
        option_rows.append(
            (
                coordinate,
                [
                    [adapted_gradient(term, point, modulus) for point in test_points]
                    for term in alternatives
                ],
            )
        )

    survivors = []
    choice_ranges = [range(len(alternatives)) for _, alternatives in GROUPS]
    for choice in product(*choice_ranges):
        valid = True
        for sample_index in range(sample_count):
            matrix = [list(row) for row in fixed_rows[sample_index]]
            for group_index, option_index in enumerate(choice):
                coordinate, alternatives = option_rows[group_index]
                contribution = alternatives[option_index][sample_index]
                for column in range(3):
                    matrix[coordinate][column] = (
                        matrix[coordinate][column] + contribution[column]
                    ) % modulus
            if det3(matrix, modulus) != 1:
                valid = False
                break
        if valid:
            survivors.append(choice)
    return survivors


def mapping(choice):
    first = FIXED[:]
    for group_index, option_index in enumerate(choice):
        coordinate, alternatives = GROUPS[group_index]
        first[coordinate] += alternatives[option_index]
    return [sp.expand(f) for f in first] + [p - x * y, q - x * z, r - p**2]


def certify(choice):
    candidate = mapping(choice)
    determinant = sp.factor(sp.Matrix(candidate).jacobian(VARS).det())
    return candidate, determinant


def main():
    total = 1
    for _, alternatives in GROUPS:
        total *= len(alternatives)
    print(f"Searching {total} direct cubic representatives")
    survivors = finite_field_survivors()
    print(f"finite-field survivors: {len(survivors)}")
    for choice in survivors:
        candidate, determinant = certify(choice)
        print("choice", choice, "det", determinant)
        if determinant == 1:
            print("CERTIFIED MAP")
            for component in candidate:
                print(sp.factor(component))


if __name__ == "__main__":
    main()
