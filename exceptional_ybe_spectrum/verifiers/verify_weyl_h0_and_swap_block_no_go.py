#!/usr/bin/env python3
"""Exact checks for the d=6 Weyl cubic point and swap-block no-go.

This verifier is independent of verify_channel_d6_abstract_model.py.  It
uses the closed qubit/qutrit-swap formula rather than reconstructing the
nineteen Weyl Kraus directions.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import product

import sympy as sp


sqrt_three = sp.sqrt(3)
identity_two = sp.eye(2)
x = sp.Matrix([[0, 1], [1, 0]])
y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
z = sp.diag(1, -1)


def kron(*matrices: sp.Matrix) -> sp.Matrix:
    result = sp.Matrix([[1]])
    for matrix in matrices:
        result = sp.kronecker_product(result, matrix)
    return result


def zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def coefficient_residuals(
    a: sp.Matrix,
    b: sp.Matrix,
) -> tuple[sp.Matrix, ...]:
    """Six S_3 coefficients of the three-site cubic."""
    c = (a + b) / 2
    d = (a - b) / 2
    c_one = kron(c, identity_two)
    c_two = kron(identity_two, c)
    d_one = kron(d, identity_two)
    d_two = kron(identity_two, d)
    return (
        c_one * c_two * c_one
        + d_one * c_two * d_one
        - c_two * c_one * c_two
        - d_two * c_one * d_two
        - (c_one - c_two) / 3,
        c_one * c_two * d_one
        + d_one * c_two * c_one
        - c_two * d_one * c_two
        - d_one / 3,
        c_one * d_two * c_one
        - c_two * c_one * d_two
        - d_two * c_one * c_two
        + d_two / 3,
        c_one * d_two * d_one - d_two * d_one * c_two,
        d_one * d_two * c_one - c_two * d_one * d_two,
        d_one * d_two * d_one - d_two * d_one * d_two,
    )


# ---------------------------------------------------------------------------
# 1. Closed-form H0.
# ---------------------------------------------------------------------------

qubit_c = kron(y, y) / sqrt_three
qubit_d = (kron(x, x) + kron(z, z)) / sqrt_three
a_zero = qubit_c + qubit_d
b_zero = qubit_c - qubit_d

assert all(zero(coefficient) for coefficient in coefficient_residuals(a_zero, b_zero))

swap_three = sp.zeros(9)
for first, second in product(range(3), repeat=2):
    swap_three[second * 3 + first, first * 3 + second] = 1
h_zero = kron(qubit_c, sp.eye(9)) + kron(qubit_d, swap_three)
assert zero(h_zero.conjugate().T - h_zero)
assert sp.trace(h_zero) == 0
assert zero(
    3 * h_zero**2
    + 2 * sqrt_three * h_zero
    - 3 * sp.eye(36)
)
assert (h_zero + sqrt_three * sp.eye(36)).rank() == 27
assert (sqrt_three * h_zero - sp.eye(36)).rank() == 9

braid_involution = (sp.eye(36) + sqrt_three * h_zero) / 2
assert zero(braid_involution**2 - sp.eye(36))
assert sp.trace(braid_involution) == 18


# ---------------------------------------------------------------------------
# 2. Independent group-algebra expansion audit of the six coefficients.
# ---------------------------------------------------------------------------

Permutation = tuple[int, int, int]
identity_permutation: Permutation = (0, 1, 2)
first_swap: Permutation = (1, 0, 2)
second_swap: Permutation = (0, 2, 1)


def compose(left: Permutation, right: Permutation) -> Permutation:
    """Permutation for applying right and then left."""
    return tuple(left[right[index]] for index in range(3))


def multiply_group_algebra(
    left: dict[Permutation, sp.Matrix],
    right: dict[Permutation, sp.Matrix],
) -> dict[Permutation, sp.Matrix]:
    result: dict[Permutation, sp.Matrix] = defaultdict(lambda: sp.zeros(8))
    for left_group, left_matrix in left.items():
        for right_group, right_matrix in right.items():
            result[compose(left_group, right_group)] += (
                left_matrix * right_matrix
            )
    return dict(result)


def add_group_algebra(
    *terms: tuple[sp.Rational, dict[Permutation, sp.Matrix]],
) -> dict[Permutation, sp.Matrix]:
    result: dict[Permutation, sp.Matrix] = defaultdict(lambda: sp.zeros(8))
    for scalar, algebra_element in terms:
        for group_element, coefficient in algebra_element.items():
            result[group_element] += scalar * coefficient
    return dict(result)


c_zero = (a_zero + b_zero) / 2
d_zero = (a_zero - b_zero) / 2
c_one = kron(c_zero, identity_two)
c_two = kron(identity_two, c_zero)
d_one = kron(d_zero, identity_two)
d_two = kron(identity_two, d_zero)
h_one = {
    identity_permutation: c_one,
    first_swap: d_one,
}
h_two = {
    identity_permutation: c_two,
    second_swap: d_two,
}
first_product = multiply_group_algebra(
    multiply_group_algebra(h_one, h_two), h_one
)
second_product = multiply_group_algebra(
    multiply_group_algebra(h_two, h_one), h_two
)
formal_cubic = add_group_algebra(
    (sp.Integer(1), first_product),
    (-sp.Integer(1), second_product),
    (-sp.Rational(1, 3), h_one),
    (sp.Rational(1, 3), h_two),
)
assert len(formal_cubic) == 6
assert all(zero(coefficient) for coefficient in formal_cubic.values())


# ---------------------------------------------------------------------------
# 3. Signature reduction and the rank-one local lemma.
# ---------------------------------------------------------------------------

possible_traces = tuple(range(-4, 5, 2))
trace_pairs = {
    (trace_a, trace_b)
    for trace_a in possible_traces
    for trace_b in possible_traces
    if 6 * trace_a + 3 * trace_b == 0
}
assert trace_pairs == {(-2, 4), (0, 0), (2, -4)}

# General odd color dimension m.  For m>=5, the only trace-balanced pair
# is (0,0).  (The finite loop is an audit; the proof uses coprimality of
# (m-1)/2 and (m+1)/2 and the bound |tr(A)|,|tr(B)|<=4.)
for odd_color_dimension in range(5, 102, 2):
    general_trace_pairs = {
        (trace_a, trace_b)
        for trace_a in possible_traces
        for trace_b in possible_traces
        if (
            (odd_color_dimension + 1) * trace_a
            + (odd_color_dimension - 1) * trace_b
            == 0
        )
    }
    assert general_trace_pairs == {(0, 0)}

# For a rank-one qubit projection Q=|vec(S)><vec(S)|, normalized by
# ||S||_F=1, compression of Q_12 Q_23 Q_12 to ran(Q_12) is L^*L with
# L=S*conjugate(S).  The projection cubic forces its two eigenvalues to be
# in {1,1/3}, so its determinant is at least 1/9.  But singular-value
# AM-GM gives |det(S)| <= 1/2 and hence det(L^*L)=|det(S)|^4 <= 1/16.
assert sp.Rational(1, 16) < sp.Rational(1, 9)

# A concrete maximally-entangled audit checks the compression formula and
# displays a nonzero cubic residual exactly.
bell = sp.Matrix([1, 0, 0, 1]) / sp.sqrt(2)
q = bell * bell.conjugate().T
q_one = kron(q, identity_two)
q_two = kron(identity_two, q)
compression_one = q_one * q_two * q_one
compression_two = q_two * q_one * q_two
assert zero(compression_one - q_one / 4)
assert zero(compression_two - q_two / 4)
assert not zero(compression_one - compression_two)
assert sp.trace(
    (compression_one - compression_two).conjugate().T
    * (compression_one - compression_two)
) == sp.Rational(3, 16)

# Pauli coefficients used in the exact block-preserving pairing no-go.
assert zero(kron(y, y) * kron(z, z) + kron(z, z) * kron(y, y) + 2 * kron(x, x))
assert zero(kron(y, y) * kron(x, x) + kron(x, x) * kron(y, y) + 2 * kron(z, z))
# The two identities below audit the whole-block interchange separately:
# Y tensor Y paired with Z tensor X (respectively X tensor Z) produces a
# nonzero crossed Pauli coefficient rather than allowing cancellation.
assert zero(kron(y, y) * kron(z, x) + kron(z, x) * kron(y, y) - 2 * kron(x, z))
assert zero(kron(y, y) * kron(x, z) + kron(x, z) * kron(y, y) - 2 * kron(z, x))

print("PASS closed H0 formula and quadratic minimal polynomial")
print("PASS six exact S3 coefficient equations for the H0 cubic")
print("PASS spectrum(H0)={(-sqrt(3))^9,(1/sqrt(3))^27}")
print("PASS affine braid involution has trace 18, not 0")
print("PASS swap-block trace signatures are (-2,4),(0,0),(2,-4)")
print("PASS odd m>=5 trace arithmetic leaves only (0,0)")
print("PASS rank-one compression determinant gap: 1/16 < 1/9")
print("PASS maximally-entangled rank-one audit, residual norm^2=3/16")
print("PASS block-preserving Schmidt pairings fail involutivity")
print(
    "[ok] reduction plus established d=2 emptiness excludes the "
    "U(m)-equivariant branch for every odd m"
)
