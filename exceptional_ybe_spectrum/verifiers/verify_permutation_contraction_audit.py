#!/usr/bin/env python3
"""Exact checks for the permutation-contraction audit.

There are three logically separate checks.

1.  The published d=4 reflection calibrates the middle partial-trace
    identity exactly over Q(sqrt(2),sqrt(3)).
2.  A standard d=6 Hermitian involution is invisible to all 48 scalar
    tests obtained by partially transposing the six three-site permutation
    operators, although its cubic residual is nonzero with squared
    Hilbert--Schmidt norm 192.
3.  The positivity and marginal data forced on the middle contraction have
    a scalar d=6 model, so those data alone carry no four-divisibility.

No floating-point arithmetic is used.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations

import numpy as np
import sympy as sp


def tensor_sympy(*matrices: sp.Matrix) -> sp.Matrix:
    result = sp.Matrix([[1]])
    for matrix in matrices:
        result = sp.kronecker_product(result, matrix)
    return result


def partial_trace_middle_sympy(matrix: sp.Matrix, d: int) -> sp.Matrix:
    """Trace site 2 of an operator on V_1 tensor V_2 tensor V_3."""
    return sp.Matrix(
        d * d,
        d * d,
        lambda ac, ik: sum(
            matrix[
                (d * (ac // d) + b) * d + ac % d,
                (d * (ik // d) + b) * d + ik % d,
            ]
            for b in range(d)
        ),
    )


def partial_trace_two_site_numpy(matrix: np.ndarray, d: int, site: int) -> np.ndarray:
    tensor = matrix.reshape(d, d, d, d)
    if site == 0:
        return np.einsum("abad->bd", tensor)
    if site == 1:
        return np.einsum("abcb->ac", tensor)
    raise ValueError("site must be 0 or 1")


def partial_trace_three_site_numpy(
    matrix: np.ndarray, d: int, site: int
) -> np.ndarray:
    tensor = matrix.reshape(d, d, d, d, d, d)
    labels = list("abcdef")
    labels[3 + site] = labels[site]
    output = "".join(
        labels[index]
        for index in range(6)
        if index not in (site, 3 + site)
    )
    return np.einsum("".join(labels) + "->" + output, tensor).reshape(
        d * d, d * d
    )


def permutation_matrix(d: int, permutation: tuple[int, int, int]) -> np.ndarray:
    """The site permutation |i_0 i_1 i_2> -> |i_p0 i_p1 i_p2>."""
    result = np.zeros((d**3, d**3), dtype=np.int64)
    for indices in np.ndindex(d, d, d):
        source = np.ravel_multi_index(indices, (d, d, d))
        target_indices = tuple(indices[permutation[position]] for position in range(3))
        target = np.ravel_multi_index(target_indices, (d, d, d))
        result[target, source] = 1
    return result


def partial_transpose_sites(
    matrix: np.ndarray, d: int, mask: int
) -> np.ndarray:
    tensor = matrix.reshape((d,) * 6)
    axes = list(range(6))
    for site in range(3):
        if (mask >> site) & 1:
            axes[site], axes[3 + site] = axes[3 + site], axes[site]
    return tensor.transpose(axes).reshape(d**3, d**3)


def check_published_d4() -> None:
    d = 4
    i2 = sp.eye(2)
    x = sp.Matrix([[0, 1], [1, 0]])
    z = sp.diag(1, -1)
    j = sp.Matrix([[0, -1], [1, 0]])

    h = (
        -tensor_sympy(z, i2, z, z) / sp.sqrt(6)
        - tensor_sympy(z, i2, j, j) / sp.sqrt(6)
        - tensor_sympy(j, i2, z, j) / sp.sqrt(6)
        + tensor_sympy(j, i2, j, z) / sp.sqrt(6)
        - tensor_sympy(x, i2, x, x) / sp.sqrt(3)
    )
    identity_16 = sp.eye(d * d)
    identity_64 = sp.eye(d**3)
    projection = (identity_16 - h) / 2
    p = tensor_sympy(projection, sp.eye(d))
    q = tensor_sympy(sp.eye(d), projection)
    h1 = tensor_sympy(h, sp.eye(d))
    h2 = tensor_sympy(sp.eye(d), h)

    assert h.conjugate().T == h
    assert sp.simplify(h * h) == identity_16
    assert sp.simplify(
        h1 * h2 * h1 - h2 * h1 * h2 - (h1 - h2) / 3
    ) == sp.zeros(d**3)

    middle_left = partial_trace_middle_sympy(p * q * p, d)
    middle_right = partial_trace_middle_sympy(q * p * q, d)
    assert sp.simplify(middle_left - middle_right) == sp.zeros(d * d)
    # This scalar value is a calibration of the published sparse witness,
    # not a claimed universal identity.
    assert sp.simplify(middle_left) == identity_16

    reflection_middle_left = partial_trace_middle_sympy(h1 * h2 * h1, d)
    reflection_middle_right = partial_trace_middle_sympy(h2 * h1 * h2, d)
    assert reflection_middle_left == sp.zeros(d * d)
    assert reflection_middle_right == sp.zeros(d * d)

    print("Published d=4 calibration")
    print("  exact cubic residual: zero")
    print("  Tr_2(P_12 P_23 P_12) = Tr_2(P_23 P_12 P_23) = I_16")
    print("  both middle contractions in reflection form vanish")


def check_d6_brauer_shadow_countermodel() -> None:
    d = 6
    z2 = np.diag(np.array([1, -1], dtype=np.int64))
    x2 = np.array([[0, 1], [1, 0]], dtype=np.int64)
    identity_3 = np.eye(3, dtype=np.int64)
    identity_6 = np.eye(d, dtype=np.int64)
    a = np.kron(z2, identity_3)
    b = np.kron(x2, identity_3)
    h = np.kron(a, b)
    identity_36 = np.eye(d * d, dtype=np.int64)

    assert np.array_equal(a @ a, identity_6)
    assert np.array_equal(b @ b, identity_6)
    assert np.array_equal(a @ b, -(b @ a))
    assert np.array_equal(h.T, h)
    assert np.array_equal(h @ h, identity_36)
    assert int(np.trace(h)) == 0
    assert np.count_nonzero(np.diag(a) == 1) == 3
    assert np.count_nonzero(np.diag(a) == -1) == 3
    # A and B each have three eigenvalues of either sign, hence
    # H=A tensor B has eighteen eigenvalues of either sign.
    positive_multiplicity = 3 * 3 + 3 * 3
    negative_multiplicity = 3 * 3 + 3 * 3
    assert positive_multiplicity == negative_multiplicity == 18
    assert np.array_equal(
        partial_trace_two_site_numpy(h, d, 0), np.zeros((d, d), dtype=np.int64)
    )
    assert np.array_equal(
        partial_trace_two_site_numpy(h, d, 1), np.zeros((d, d), dtype=np.int64)
    )

    h1 = np.kron(h, identity_6)
    h2 = np.kron(identity_6, h)
    # Anticommutation gives
    # H_1 H_2 H_1 - H_2 H_1 H_2 = H_1-H_2.
    # Three times the target residual is therefore 2(H_1-H_2).
    residual_numerator = 2 * (h1 - h2)
    residual_norm_numerator_squared = int(
        np.vdot(residual_numerator, residual_numerator)
    )
    assert residual_norm_numerator_squared == 9 * 192

    zero_36 = np.zeros((d * d, d * d), dtype=np.int64)
    assert np.array_equal(
        partial_trace_three_site_numpy(residual_numerator, d, 1), zero_36
    )
    assert np.array_equal(
        partial_trace_three_site_numpy(residual_numerator, d, 2), 2 * d * h
    )
    assert np.array_equal(
        partial_trace_three_site_numpy(residual_numerator, d, 0), -2 * d * h
    )

    tested = 0
    for permutation in permutations(range(3)):
        permutation_operator = permutation_matrix(d, permutation)
        for mask in range(8):
            test_operator = partial_transpose_sites(
                permutation_operator, d, mask
            )
            assert int(np.vdot(test_operator, h1)) == 0
            assert int(np.vdot(test_operator, h2)) == 0
            pairing_numerator = int(
                np.vdot(test_operator, residual_numerator)
            )
            assert pairing_numerator == 0
            tested += 1
    assert tested == 48

    print("Exact d=6 scalar-shadow countermodel")
    print("  H=(Z tensor I_3) tensor (X tensor I_3)")
    print("  H=H*, H^2=I, Tr_1(H)=Tr_2(H)=0, signature=(18,18)")
    print("  cubic residual squared Hilbert--Schmidt norm = 192")
    print("  middle partial trace of the residual = 0")
    print("  all 48 partially-transposed permutation pairings = 0")


def check_d6_middle_marginal_model() -> None:
    d = 6
    # M=(d/4)I and K=(3/2)M-(d/4)I satisfy every scalar,
    # positivity, bound, and marginal condition forced in the note.
    m_scalar = Fraction(d, 4)
    k_scalar = Fraction(3, 2) * m_scalar - Fraction(d, 4)
    assert m_scalar == Fraction(3, 2)
    assert k_scalar == Fraction(3, 4)
    assert Fraction(d, 6) <= m_scalar <= Fraction(d, 2)
    assert Fraction(0) <= k_scalar <= Fraction(d, 2)
    assert d * d * m_scalar == Fraction(d**3, 4)
    assert d * m_scalar == Fraction(d**2, 4)
    assert d * d * k_scalar == Fraction(d**3, 8)
    assert d * k_scalar == Fraction(d**2, 8)

    print("Exact d=6 middle-marginal limitation model")
    print("  M=(3/2) I_36 and K=(3/4) I_36")
    print("  all forced traces, scalar marginals, positivity, and bounds hold")


if __name__ == "__main__":
    check_published_d4()
    check_d6_brauer_shadow_countermodel()
    check_d6_middle_marginal_model()
    print("PASS")
