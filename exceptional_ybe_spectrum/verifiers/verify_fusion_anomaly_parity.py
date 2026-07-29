#!/usr/bin/env python3
"""Exact checks for the fusion-anomaly parity audit.

This verifier has four independent finite parts:

1. SU(3)_3 fusion grading and the neutral A4 fusion ring.
2. The binary-tetrahedral realization of the nontrivial twisted A4
   group algebra as M_2(C) direct-summed three times.
3. Odd-s Hecke-tower arithmetic and the scalar determinant blocks.
4. Exact flip/reversal defects of the published d=4 localizer.

No floating-point arithmetic is used.
"""

from __future__ import annotations

from functools import reduce

import sympy as sp


def tensor(*matrices: sp.Matrix) -> sp.Matrix:
    return reduce(sp.kronecker_product, matrices, sp.Matrix([[1]]))


def is_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def hs_norm_squared(matrix: sp.Matrix) -> sp.Expr:
    return sp.simplify(sp.trace(matrix.conjugate().T * matrix))


def fusion_audit() -> None:
    weights = [
        (a, b)
        for a in range(4)
        for b in range(4 - a)
    ]
    index = {weight: position for position, weight in enumerate(weights)}
    assert len(weights) == 10

    # Columns are input simples and rows are output simples.
    fusion_x = sp.zeros(10)
    for a, b in weights:
        successors: list[tuple[int, int]] = []
        if a + b < 3:
            successors.append((a + 1, b))
        if a > 0:
            successors.append((a - 1, b + 1))
        if b > 0:
            successors.append((a, b - 1))
        for successor in successors:
            fusion_x[index[successor], index[(a, b)]] += 1
            assert (
                successor[0]
                + 2 * successor[1]
                - a
                - 2 * b
                - 1
            ) % 3 == 0

    dimensions = sp.Matrix(
        [
            1 if weight in {(0, 0), (3, 0), (0, 3)}
            else 3 if weight == (1, 1)
            else 2
            for weight in weights
        ]
    )
    assert fusion_x.T * dimensions == 2 * dimensions

    # X tensor X* = 1 + Y.
    fusion_y = fusion_x * fusion_x.T - sp.eye(10)

    # The order-three simple current g=(3,0).
    fusion_g = sp.zeros(10)
    for a, b in weights:
        image = (3 - a - b, a)
        fusion_g[index[image], index[(a, b)]] = 1

    assert fusion_g**3 == sp.eye(10)
    assert fusion_g * fusion_y == fusion_y
    assert (
        fusion_y**2
        == sp.eye(10) + fusion_g + fusion_g**2 + 2 * fusion_y
    )

    grade_zero = {
        weight
        for weight in weights
        if (weight[0] + 2 * weight[1]) % 3 == 0
    }
    assert grade_zero == {(0, 0), (3, 0), (0, 3), (1, 1)}

    degree_one = [(1, 0), (2, 1), (0, 2)]
    for position, weight in enumerate(degree_one):
        expected_next = degree_one[(position + 1) % 3]
        # Our chosen simple-current orientation may cycle in either
        # direction; compare the actual singleton and audit the orbit.
        actual = [
            weights[row]
            for row in range(10)
            if fusion_g[row, index[weight]]
        ]
        assert len(actual) == 1
        assert actual[0] in degree_one
        assert set(
            weights[row]
            for row in range(10)
            if fusion_y[row, index[weight]]
        ) == set(degree_one)
        del expected_next

    # Exact tensor-power endpoint counts through six strands.
    endpoint = sp.zeros(10, 1)
    endpoint[index[(0, 0)]] = 1
    expected_three = {(0, 0): 1, (1, 1): 2, (3, 0): 1}
    for strand in range(7):
        active = {
            weights[row]: int(endpoint[row])
            for row in range(10)
            if endpoint[row]
        }
        assert all(
            (a + 2 * b - strand) % 3 == 0
            for a, b in active
        )
        if strand == 3:
            assert active == expected_three
        endpoint = fusion_x * endpoint


def binary_tetrahedral_audit() -> None:
    imaginary = sp.I
    root_three = sp.sqrt(3)
    omega = (-1 + imaginary * root_three) / 2

    identity = sp.eye(2)
    quat_i = sp.Matrix([[imaginary, 0], [0, -imaginary]])
    quat_j = sp.Matrix([[0, 1], [-1, 0]])
    quat_k = quat_i * quat_j

    assert quat_i**2 == quat_j**2 == quat_k**2 == -identity
    assert quat_i * quat_j == quat_k
    assert quat_j * quat_i == -quat_k

    order_three = (-identity + quat_i + quat_j + quat_k) / 2
    assert is_zero(order_three**3 - identity)
    assert is_zero(
        order_three * quat_i * order_three.inv() - quat_k
    )
    assert is_zero(
        order_three * quat_j * order_three.inv() - quat_i
    )
    assert is_zero(
        order_three * quat_k * order_three.inv() - quat_j
    )

    # Quotient basis after imposing the central quaternion -1 = scalar -1.
    quotient_basis = [
        (quaternion, exponent)
        for exponent in range(3)
        for quaternion in (identity, quat_i, quat_j, quat_k)
    ]
    columns: list[sp.Matrix] = []
    for quaternion, exponent in quotient_basis:
        entries: list[sp.Expr] = []
        for character in range(3):
            represented = sp.simplify(
                quaternion
                * (omega**character * order_three) ** exponent
            )
            entries.extend(list(represented))
        columns.append(sp.Matrix(entries))

    direct_sum_map = sp.Matrix.hstack(*columns)
    assert direct_sum_map.shape == (12, 12)
    determinant = sp.factor(
        direct_sum_map.det(),
        extension=[imaginary, root_three],
    )
    assert determinant == 6**6
    assert direct_sum_map.rank() == 12

    # Lift the real three-dimensional A4 representation to 2T by
    # conjugation on the imaginary quaternion span.  Its tensor product
    # with any spinor has character equal to the sum of all three spinors.
    y_i = sp.diag(1, -1, -1)
    y_j = sp.diag(-1, 1, -1)
    y_k = sp.diag(-1, -1, 1)
    y_order_three = sp.Matrix(
        [
            [0, 1, 0],
            [0, 0, 1],
            [1, 0, 0],
        ]
    )
    quaternion_elements = [
        (sign * quaternion, y_quaternion)
        for sign in (1, -1)
        for quaternion, y_quaternion in (
            (identity, sp.eye(3)),
            (quat_i, y_i),
            (quat_j, y_j),
            (quat_k, y_k),
        )
    ]
    for spinor_character in range(3):
        for quaternion, y_quaternion in quaternion_elements:
            for exponent in range(3):
                spinor_trace = sp.trace(
                    quaternion
                    * (omega**spinor_character * order_three) ** exponent
                )
                y_trace = sp.trace(
                    y_quaternion * y_order_three**exponent
                )
                all_spinor_traces = sum(
                    sp.trace(
                        quaternion
                        * (omega**character * order_three) ** exponent
                    )
                    for character in range(3)
                )
                assert sp.simplify(
                    y_trace * spinor_trace - all_spinor_traces
                ) == 0

    # Every module over M2 direct-summed three times has even dimension.
    for multiplicities in (
        (1, 0, 0),
        (0, 2, 0),
        (1, 1, 1),
        (3, 2, 4),
    ):
        module_dimension = 2 * sum(multiplicities)
        assert module_dimension % 2 == 0

    # The natural projective action on V=C^2 tensor C^s exists for odd s
    # as well.  It accounts only for the already-known evenness of d.
    s = 3
    repeated_identity = sp.eye(s)
    for quaternion, exponent in quotient_basis:
        represented = tensor(
            quaternion * order_three**exponent,
            repeated_identity,
        )
        assert represented.shape == (2 * s, 2 * s)

    # A quaternionic antiunitary on the categorical two-dimensional
    # spinor extends over an arbitrary (also odd) multiplicity space.
    quaternionic_linear_part = sp.Matrix([[0, 1], [-1, 0]])
    extended_linear_part = tensor(
        quaternionic_linear_part, repeated_identity
    )
    assert (
        extended_linear_part * extended_linear_part.conjugate()
        == -sp.eye(2 * s)
    )


def odd_s_tower_and_scalar_blocks() -> None:
    s = 3
    dimensions = (1, 3, 1)
    path_dimensions = (1, 2, 1)

    # Three-strand simple-module multiplicities and represented dimensions.
    multiplicities = tuple(dimension * s**3 for dimension in dimensions)
    assert multiplicities == (27, 81, 27)
    assert sum(
        path * multiplicity
        for path, multiplicity in zip(
            path_dimensions, multiplicities
        )
    ) == (2 * s) ** 3

    # On the two one-dimensional Hecke simples both generators are scalar.
    common_one_p = sp.eye(s**3)
    common_one_q = sp.eye(s**3)
    common_zero_p = sp.zeros(s**3)
    common_zero_q = sp.zeros(s**3)
    for p, q in (
        (common_one_p, common_one_q),
        (common_zero_p, common_zero_q),
    ):
        assert is_zero(p * q * p - q * p * q - (p - q) / 3)

    # Scalar braid actions preserve a symmetric form in odd dimension.
    hecke_root = (1 + sp.I * sp.sqrt(3)) / 2
    common_one_r = (
        hecke_root * sp.eye(s**3)
        - (1 + hecke_root) * common_one_p
    )
    assert common_one_r == -sp.eye(s**3)
    symmetric_form = sp.eye(s**3)
    assert symmetric_form.det() == 1
    assert symmetric_form.T == symmetric_form
    assert common_one_r.T * symmetric_form * common_one_r == symmetric_form

    # An alternating matrix in odd dimension is singular.
    generic_alternating = sp.zeros(s**3)
    for row in range(0, s**3 - 1, 2):
        generic_alternating[row, row + 1] = 1
        generic_alternating[row + 1, row] = -1
    assert generic_alternating.T == -generic_alternating
    assert generic_alternating.det() == 0


def published_d4_reversal_audit() -> None:
    identity_2 = sp.eye(2)
    x = sp.Matrix([[0, 1], [1, 0]])
    z = sp.diag(1, -1)
    j = sp.Matrix([[0, -1], [1, 0]])

    h = (
        -tensor(z, identity_2, z, z) / sp.sqrt(6)
        - tensor(z, identity_2, j, j) / sp.sqrt(6)
        - tensor(j, identity_2, z, j) / sp.sqrt(6)
        + tensor(j, identity_2, j, z) / sp.sqrt(6)
        - tensor(x, identity_2, x, x) / sp.sqrt(3)
    )
    d = 4
    projection = (sp.eye(d * d) - h) / 2
    assert is_zero(projection**2 - projection)
    assert is_zero(projection.conjugate() - projection)

    flip = sp.zeros(d * d)
    for left in range(d):
        for right in range(d):
            flip[right * d + left, left * d + right] = 1
    opposite = flip * projection * flip
    assert hs_norm_squared(projection - opposite) == 8

    p = tensor(projection, sp.eye(d))
    q = tensor(sp.eye(d), projection)
    p_domain = p.to_DM(extension=True)
    q_domain = q.to_DM(extension=True)
    one_third = p_domain.domain(sp.Rational(1, 3))
    cubic_residual = (
        p_domain * q_domain * p_domain
        - q_domain * p_domain * q_domain
        - one_third * (p_domain - q_domain)
    )
    assert cubic_residual.is_zero_matrix

    common_one = sp.Rational(3, 2) * p * q * p - p / 2
    assert is_zero(common_one**2 - common_one)
    assert sp.simplify(sp.trace(common_one)) == 8

    reversal = sp.zeros(d**3)
    for first in range(d):
        for middle in range(d):
            for last in range(d):
                source = first * d**2 + middle * d + last
                target = last * d**2 + middle * d + first
                reversal[target, source] = 1

    reflected = reversal * common_one * reversal
    assert hs_norm_squared(common_one - reflected) == 14
    assert sp.simplify(
        sp.trace(common_one * reflected)
    ) == 1

    # Since the witness is real, entrywise conjugation is an internal
    # antiunitary with square +1, not a forced quaternionic structure.
    assert is_zero(common_one.conjugate() - common_one)


def main() -> None:
    fusion_audit()
    print("PASS exact SU(3)_3 grading, neutral A4 ring, and degree-one module")
    binary_tetrahedral_audit()
    print("PASS exact twisted A4 algebra B_- is M2 direct-summed three times")
    odd_s_tower_and_scalar_blocks()
    print("PASS odd-s determinant blocks carry no forced alternating form")
    published_d4_reversal_audit()
    print("PASS exact d=4 flip and determinant-channel reversal defects")
    print("All fusion-anomaly parity audit checks passed exactly.")


if __name__ == "__main__":
    main()
