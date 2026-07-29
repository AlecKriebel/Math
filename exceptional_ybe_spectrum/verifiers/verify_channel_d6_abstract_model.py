#!/usr/bin/env python3
"""Exact d=6 model of all currently isolated channel constraints.

This is intentionally not a projection or a Yang--Baxter witness.  It is a
Weyl-diagonal countermodel showing that even the stronger universal
constraint

    F = 2 E - id  is completely positive

does not turn the channel spectra into a divisibility-by-four obstruction.
The verifier constructs F twice: as a random-unitary Weyl channel and from
an orthonormal family of traceless Hermitian Kraus operators in exactly the
normalization forced by an operator-Schmidt decomposition of H.
"""

from __future__ import annotations

from collections import Counter
from itertools import product

import sympy as sp


d = 6
group = tuple(product(range(2), range(2), range(3), range(3)))
zero = (0, 0, 0, 0)
root_three = (-1 + sp.I * sp.sqrt(3)) / 2


def inverse(element: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    x, y, u, v = element
    return ((-x) % 2, (-y) % 2, (-u) % 3, (-v) % 3)


def character(
    spectral_label: tuple[int, int, int, int],
    group_element: tuple[int, int, int, int],
) -> sp.Expr:
    """Conjugation character for qubit-qutrit Weyl operators."""
    a, b, c, e = spectral_label
    x, y, u, v = group_element
    qubit_phase = -1 if (y * a - b * x) % 2 else 1
    qutrit_phase = root_three ** ((v * c - e * u) % 3)
    return sp.expand_complex(qubit_phase * qutrit_phase)


positive_spectral_set = {
    label
    for label in group
    if (
        label[:2] == (0, 0)
        and label[2:] != (0, 0)
    )
    or (
        label[:2] == (1, 1)
        and label[2:] != (0, 0)
    )
}
assert len(positive_spectral_set) == 16


def target_eigenvalue(label: tuple[int, int, int, int]) -> sp.Rational:
    if label == zero:
        return sp.Integer(1)
    if label in positive_spectral_set:
        return sp.Rational(1, 3)
    return -sp.Rational(1, 3)


# Exact inverse Fourier transform of the desired Weyl spectrum.
probability: dict[tuple[int, int, int, int], sp.Rational] = {}
for element in group:
    inverse_fourier = sum(
        target_eigenvalue(label) * sp.conjugate(character(label, element))
        for label in group
    ) / len(group)
    inverse_fourier = sp.simplify(sp.expand_complex(inverse_fourier))
    assert inverse_fourier.is_Rational
    probability[element] = sp.Rational(inverse_fourier)

assert sum(probability.values()) == 1
assert all(weight >= 0 for weight in probability.values())
assert Counter(probability.values()) == Counter(
    {
        sp.Integer(0): 17,
        sp.Rational(1, 27): 18,
        sp.Rational(1, 3): 1,
    }
)
assert probability[zero] == 0
assert all(probability[element] == probability[inverse(element)] for element in group)

# Independent forward Fourier check.
for label in group:
    recovered = sp.simplify(
        sum(
            probability[element] * character(label, element)
            for element in group
        )
    )
    assert recovered == target_eigenvalue(label)


def matrix_power(matrix: sp.Matrix, exponent: int) -> sp.Matrix:
    return matrix**exponent


x_two = sp.Matrix([[0, 1], [1, 0]])
z_two = sp.diag(1, -1)
x_three = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
z_three = sp.diag(1, root_three, root_three**2)


def weyl(element: tuple[int, int, int, int]) -> sp.Matrix:
    x, y, u, v = element
    return sp.kronecker_product(
        matrix_power(x_two, x) * matrix_power(z_two, y),
        matrix_power(x_three, u) * matrix_power(z_three, v),
    )


def vectorize(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [matrix[row, column] for row in range(d) for column in range(d)]
    )


def partial_trace_second(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        d,
        d,
        lambda first, third: sum(
            matrix[d * first + second, d * third + second]
            for second in range(d)
        ),
    )


def partial_trace_first(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        d,
        d,
        lambda second, fourth: sum(
            matrix[d * first + second, d * first + fourth]
            for first in range(d)
        ),
    )


def is_zero_matrix(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(sp.expand_complex(entry)) == 0 for entry in matrix)


def superoperator_from_kraus(
    kraus_operators: list[sp.Matrix],
) -> sp.Matrix:
    columns: list[sp.Matrix] = []
    for row in range(d):
        for column in range(d):
            matrix_unit = sp.zeros(d)
            matrix_unit[row, column] = 1
            image = sum(
                (
                    operator
                    * matrix_unit
                    * operator.conjugate().T
                    for operator in kraus_operators
                ),
                sp.zeros(d),
            )
            columns.append(vectorize(image))
    return sp.Matrix.hstack(*columns).applyfunc(sp.simplify)


# Random-unitary Kraus representation.  The identity Weyl has zero weight,
# so every nonzero Kraus operator is traceless.
random_unitary_kraus = [
    sp.sqrt(weight) * weyl(element)
    for element, weight in probability.items()
    if weight > 0
]
assert len(random_unitary_kraus) == 19
assert all(sp.simplify(sp.trace(operator)) == 0 for operator in random_unitary_kraus)
f_random_unitary = superoperator_from_kraus(random_unitary_kraus)


# Pair inverse Weyls to obtain an orthonormal traceless Hermitian family.
# Each entry is (A_alpha, sigma_alpha^2), normalized so
# F(X) = d^{-1} sum sigma_alpha^2 A_alpha X A_alpha.
hermitian_schmidt_data: list[tuple[sp.Matrix, sp.Rational]] = []
visited: set[tuple[int, int, int, int]] = set()
for element in group:
    weight = probability[element]
    if weight == 0 or element in visited:
        continue
    partner = inverse(element)
    operator = weyl(element)
    if partner == element:
        if is_zero_matrix(operator.conjugate().T - operator):
            hermitian = operator / sp.sqrt(d)
        else:
            assert is_zero_matrix(operator.conjugate().T + operator)
            hermitian = sp.I * operator / sp.sqrt(d)
        hermitian_schmidt_data.append((hermitian, d**2 * weight))
        visited.add(element)
        continue

    assert probability[partner] == weight
    hermitian_plus = (
        operator + operator.conjugate().T
    ) / sp.sqrt(2 * d)
    hermitian_minus = (
        operator - operator.conjugate().T
    ) / (sp.I * sp.sqrt(2 * d))
    hermitian_schmidt_data.extend(
        (
            (hermitian_plus, d**2 * weight),
            (hermitian_minus, d**2 * weight),
        )
    )
    visited.add(element)
    visited.add(partner)

assert len(hermitian_schmidt_data) == 19
assert sum(sigma_squared for _, sigma_squared in hermitian_schmidt_data) == d**2
for index, (operator, _) in enumerate(hermitian_schmidt_data):
    assert is_zero_matrix(operator.conjugate().T - operator)
    assert sp.simplify(sp.trace(operator)) == 0
    for second_index, (second_operator, _) in enumerate(hermitian_schmidt_data):
        inner_product = sp.simplify(
            sp.trace(operator.conjugate().T * second_operator)
        )
        assert inner_product == (1 if index == second_index else 0)

hermitian_kraus = [
    sp.sqrt(sigma_squared / d) * operator
    for operator, sigma_squared in hermitian_schmidt_data
]
f_hermitian = superoperator_from_kraus(hermitian_kraus)
assert is_zero_matrix(f_hermitian - f_random_unitary)
f_channel = f_hermitian

# The identity pairing of the two Schmidt legs is already highly
# structured.  It satisfies the exceptional cubic exactly, but its two
# eigenvalue multiplicities are 9 and 27 rather than 18 and 18.
h_zero = sum(
    (
        sp.sqrt(sigma_squared) * sp.kronecker_product(operator, operator)
        for operator, sigma_squared in hermitian_schmidt_data
    ),
    sp.zeros(d * d),
).applyfunc(sp.simplify)
assert is_zero_matrix(h_zero.conjugate().T - h_zero)
assert sp.trace(h_zero) == 0
assert partial_trace_first(h_zero) == sp.zeros(d)
assert partial_trace_second(h_zero) == sp.zeros(d)

# Closed form after regrouping the two qubits before the two qutrits:
# H_0 = (YY tensor I_9 + (XX+ZZ) tensor F_3)/sqrt(3).
y_two = sp.I * x_two * z_two
flip_three = sp.zeros(9)
for first in range(3):
    for second in range(3):
        flip_three[3 * first + second, 3 * second + first] = 1
site_regrouping = sp.zeros(d * d)
for qubit_one in range(2):
    for qutrit_one in range(3):
        for qubit_two in range(2):
            for qutrit_two in range(3):
                old_index = (
                    (3 * qubit_one + qutrit_one) * d
                    + 3 * qubit_two
                    + qutrit_two
                )
                new_index = (
                    (2 * qubit_one + qubit_two) * 9
                    + 3 * qutrit_one
                    + qutrit_two
                )
                site_regrouping[new_index, old_index] = 1
h_zero_closed = (
    sp.kronecker_product(y_two, y_two, sp.eye(9))
    + sp.kronecker_product(x_two, x_two, flip_three)
    + sp.kronecker_product(z_two, z_two, flip_three)
) / sp.sqrt(3)
assert is_zero_matrix(
    site_regrouping * h_zero * site_regrouping.T - h_zero_closed
)
assert is_zero_matrix(
    3 * h_zero**2
    + 2 * sp.sqrt(3) * h_zero
    - 3 * sp.eye(d * d)
)
assert (h_zero + sp.sqrt(3) * sp.eye(d * d)).rank() == 27
assert (sp.sqrt(3) * h_zero - sp.eye(d * d)).rank() == 9
h_zero_1 = sp.kronecker_product(h_zero, sp.eye(d))
h_zero_2 = sp.kronecker_product(sp.eye(d), h_zero)
assert is_zero_matrix(
    h_zero_1 * h_zero_2 * h_zero_1
    - h_zero_2 * h_zero_1 * h_zero_2
    - (h_zero_1 - h_zero_2) / 3
)

# The unique affine transform that maps the two eigenvalues of H_0 to
# {-1,+1} is an involutive braid operator, but its trace is 18.
unbalanced_involution = (
    sp.eye(d * d) + sp.sqrt(3) * h_zero
) / 2
assert is_zero_matrix(
    unbalanced_involution**2 - sp.eye(d * d)
)
assert sp.trace(unbalanced_involution) == 18
unbalanced_1 = sp.kronecker_product(unbalanced_involution, sp.eye(d))
unbalanced_2 = sp.kronecker_product(sp.eye(d), unbalanced_involution)
assert is_zero_matrix(
    unbalanced_1 * unbalanced_2 * unbalanced_1
    - unbalanced_2 * unbalanced_1 * unbalanced_2
)

# The Weyl basis is an exact eigenbasis with the prescribed spectrum.
for label in group:
    eigenoperator = weyl(label)
    image = sp.Matrix(
        d,
        d,
        list(f_channel * vectorize(eigenoperator)),
    )
    assert all(
        sp.simplify(entry) == 0
        for entry in image - target_eigenvalue(label) * eigenoperator
    )

identity_superoperator = sp.eye(d * d)
identity_matrix = sp.eye(d)
identity_vector = vectorize(identity_matrix)
omega = identity_vector * identity_vector.T / d
channel = (identity_superoperator + f_channel) / 2
reduced_channel = (identity_superoperator + 3 * f_channel) / 4
channel_probability = {
    element: probability[element] / 2
    + (sp.Rational(1, 2) if element == zero else 0)
    for element in group
}
reduced_probability = {
    element: 3 * probability[element] / 4
    + (sp.Rational(1, 4) if element == zero else 0)
    for element in group
}

assert f_channel.conjugate().T == f_channel
assert f_channel * identity_vector == identity_vector
assert sp.trace(f_channel) == 0
assert sum(channel_probability.values()) == 1
assert all(weight >= 0 for weight in channel_probability.values())
assert sum(reduced_probability.values()) == 1
assert all(weight >= 0 for weight in reduced_probability.values())
assert sp.trace(channel) == sp.Rational(d * d, 2)
assert sp.trace(reduced_channel) == sp.Rational(d * d, 4)
assert len((channel - identity_superoperator).nullspace()) == 1
assert len((3 * channel - 2 * identity_superoperator).nullspace()) == 16
assert len((3 * channel - identity_superoperator).nullspace()) == 19
for operator, _ in hermitian_schmidt_data:
    assert is_zero_matrix(
        sp.Matrix(d, d, list(channel * vectorize(operator)))
        - operator / 3
    )

# U=(id+3F)/4 is also CP: it is the convex combination
# (1/4) id + (3/4) F of random-unitary channels.
assert reduced_channel == (3 * channel - identity_superoperator) / 2

# Set E_L=E_R=E.  This enforces all observed joint identities.
paired_polynomial = (
    (2 * channel - sp.Rational(4, 3) * identity_superoperator)
    * (channel - sp.Rational(1, 3) * identity_superoperator) ** 2
)
assert paired_polynomial == sp.Rational(8, 27) * omega

print("Exact Weyl-diagonal d=6 canonical-channel countermodel")
print("  probabilities = {0^17, (1/27)^18, (1/3)^1}")
print("  spectrum(F) = {1^1, (1/3)^16, (-1/3)^19}")
print("  F=2E-id is CP, bistochastic, HS-self-adjoint, tr_super(F)=0")
print("  F has 19 traceless random-unitary Weyl Kraus operators")
print("  F also has 19 orthonormal traceless Hermitian Kraus directions")
print("  those 19 Hermitian Kraus directions span the 1/3-eigenspace of E")
print("  identity Schmidt pairing H_0 satisfies the cubic exactly")
print("  regrouped H_0=(YY tensor I_9 +(XX+ZZ) tensor F_3)/sqrt(3)")
print("  minpoly(H_0) = 3x^2+2sqrt(3)x-3")
print("  spectrum(H_0) = {(-sqrt(3))^9, (1/sqrt(3))^27}")
print("  (I+sqrt(3)H_0)/2 is a braid involution of trace 18, not 0")
print("  spectrum(E) = {1^1, (2/3)^16, (1/3)^19}")
print("  spectrum(U) = {1^1, (1/2)^16, 0^19}; U=(3E-id)/2 is CP")
print("  E_L=E_R, hence exact commutation and isospectrality")
print("  (E_L+E_R-4/3)(E_L-1/3)(E_R-1/3)=(8/27)Omega")
print("[ok] strengthened channel constraints still permit d=6")
print("[warning] this is not a projection and not a Yang--Baxter witness")
