#!/usr/bin/env python3
"""Exact verification of the mixed-derivation identities and obstruction."""

import sympy as sp


I = sp.I
sqrt = sp.sqrt


def hs_inner(left, right):
    return sp.simplify(sp.trace(left.conjugate().T * right))


def hs_norm_squared(matrix):
    return sp.simplify(hs_inner(matrix, matrix))


def matrix_unit(row, column):
    out = sp.zeros(3)
    out[row, column] = 1
    return out


eye = sp.eye(3)
E = {
    (row, column): matrix_unit(row, column)
    for row in range(3)
    for column in range(3)
}

# Hermitian Hilbert--Schmidt orthonormal basis of M_3.
basis = [
    eye / sqrt(3),
    sp.diag(1, -1, 0) / sqrt(2),
    sp.diag(1, 1, -2) / sqrt(6),
]
for row, column in ((0, 1), (0, 2), (1, 2)):
    basis.append((E[row, column] + E[column, row]) / sqrt(2))
    basis.append(I * (E[row, column] - E[column, row]) / sqrt(2))

assert len(basis) == 9
assert sp.Matrix(
    [[hs_inner(first, second) for second in basis] for first in basis]
) == sp.eye(9)


def kron3(first, second, third):
    return sp.kronecker_product(first, second, third)


def embed(local, site):
    factors = [eye, eye, eye]
    factors[site] = local
    return kron3(*factors)


def derivation(local, site, matrix):
    operator = embed(local, site)
    return sp.simplify(operator * matrix - matrix * operator)


Z = sp.diag(1, 0, -1) / sqrt(2)
X = (
    E[0, 1] + E[1, 0] + E[1, 2] + E[2, 1]
) / 2
S = eye / sqrt(3)
a = sqrt(2) / 3

components = [
    a * kron3(S, X, X),  # scalar at site 1
    a * kron3(X, S, Z),  # scalar at site 2
    a * kron3(Z, Z, S),  # scalar at site 3
]
D = sp.simplify(sum(components, sp.zeros(27)))

assert [hs_norm_squared(component) for component in components] == [
    sp.Rational(2, 9)
] * 3
assert hs_norm_squared(D) == sp.Rational(2, 3)

t = sp.symbols("t")
expected_characteristic = (
    t**7
    * (t**2 - sp.Rational(1, 18))
    * (t**2 - sp.Rational(1, 27)) ** 3
    * (t**2 - sqrt(6) * t / 18 - sp.Rational(1, 54)) ** 3
    * (t**2 + sqrt(6) * t / 18 - sp.Rational(1, 54)) ** 3
)
assert sp.simplify(D.charpoly(t).as_expr() - expected_characteristic) == 0

# Each local derivation is injective on the eight-dimensional traceless
# input space.
traceless_basis = basis[1:]
derivation_columns = []
for site in range(3):
    columns = [
        derivation(local, site, D).reshape(27 * 27, 1)
        for local in traceless_basis
    ]
    derivation_columns.append(sp.Matrix.hstack(*columns))
    assert derivation_columns[-1].rank() == 8

# First-Casimir norms and complete cross-site Gram blocks.
for site in range(3):
    first_norm = sum(
        hs_norm_squared(derivation(local, site, D))
        for local in basis
    )
    assert sp.simplify(first_norm) == sp.Rational(8, 3)

for first_site, second_site in ((0, 1), (0, 2), (1, 2)):
    cross_gram = sp.Matrix(
        [
            [
                hs_inner(
                    derivation(first, first_site, D),
                    derivation(second, second_site, D),
                )
                for second in basis
            ]
            for first in basis
        ]
    )
    assert cross_gram == sp.zeros(9)

# Mixed double-Casimir norms, sector isolation, and reconstruction.
pairs = ((0, 1, 2), (0, 2, 1), (1, 2, 0))
for first_site, second_site, missing_site in pairs:
    double_norm = 0
    reconstruction = sp.zeros(27)
    for first in basis:
        for second in basis:
            mixed = derivation(
                first,
                first_site,
                derivation(second, second_site, D),
            )
            double_norm += hs_norm_squared(mixed)
            reconstruction += derivation(
                first,
                first_site,
                derivation(
                    first,
                    first_site,
                    derivation(
                        second,
                        second_site,
                        derivation(second, second_site, D),
                    ),
                ),
            )
    assert sp.simplify(double_norm) == 8
    assert sp.simplify(reconstruction / 36 - components[missing_site]) == sp.zeros(27)

# Audit the operator-valued frame identity on every pair component.
def trace_replacement_two_site(matrix, site):
    """Unnormalized e_site on a 3 x 3 bipartite operator."""

    tensor = sp.MutableDenseNDimArray(matrix, (3, 3, 3, 3))
    if site == 0:
        reduced = sp.Matrix(
            3,
            3,
            lambda row, column: sum(
                tensor[value, row, value, column] for value in range(3)
            ),
        )
        return sp.kronecker_product(eye, reduced)
    reduced = sp.Matrix(
        3,
        3,
        lambda row, column: sum(
            tensor[row, value, column, value] for value in range(3)
        ),
    )
    return sp.kronecker_product(reduced, eye)


for left, right in ((Z, Z), (X, Z), (X, X)):
    pair_component = sp.kronecker_product(left, right)
    frame = sp.zeros(9)
    for first in basis:
        for second in basis:
            first_op = sp.kronecker_product(first, eye)
            second_op = sp.kronecker_product(eye, second)
            mixed = (
                first_op
                * (second_op * pair_component - pair_component * second_op)
                - (second_op * pair_component - pair_component * second_op)
                * first_op
            )
            frame += mixed * mixed.conjugate().T
    density = pair_component * pair_component.conjugate().T
    expected = (
        9 * density
        + 3 * trace_replacement_two_site(density, 0)
        + 3 * trace_replacement_two_site(density, 1)
        + trace_replacement_two_site(
            trace_replacement_two_site(density, 0),
            1,
        )
    )
    assert sp.simplify(frame - expected) == sp.zeros(9)

print("verified: D_* has exact sector masses 2/9,2/9,2/9")
print("verified: D_* has top-two singular mass 1/9")
print("verified: all three traceless derivation maps have rank eight")
print("verified: every cross-site first-derivation Gram block vanishes")
print("verified: each mixed double-Casimir norm is eight")
print("verified: mixed Casimir reconstruction recovers every pair component")
print("verified: the operator-valued double-frame identity holds exactly")
