#!/usr/bin/env python3
"""Exact channel certificates for the exceptional d=4 witness.

The first half constructs the published sparse reflection and verifies the
two canonical one-site channels over Q(sqrt(2), sqrt(3)).  The second half
constructs a rational rank-half projection with scalar partial traces whose
canonical channels do *not* commute.  The latter is not a Yang--Baxter
solution; it is a guard against accidentally deriving channel commutation
from standardness alone.
"""

from __future__ import annotations

import sympy as sp


def tensor(*matrices: sp.Matrix) -> sp.Matrix:
    result = sp.Matrix([[1]])
    for matrix in matrices:
        result = sp.kronecker_product(result, matrix)
    return result


def partial_trace_second(matrix: sp.Matrix, d: int) -> sp.Matrix:
    return sp.Matrix(
        d,
        d,
        lambda i, k: sum(matrix[d * i + j, d * k + j] for j in range(d)),
    )


def partial_trace_first(matrix: sp.Matrix, d: int) -> sp.Matrix:
    return sp.Matrix(
        d,
        d,
        lambda j, ell: sum(
            matrix[d * i + j, d * i + ell] for i in range(d)
        ),
    )


def vectorize(matrix: sp.Matrix) -> sp.Matrix:
    """Row-major vectorization, used consistently for the superoperators."""
    return sp.Matrix(
        [matrix[i, j] for i in range(matrix.rows) for j in range(matrix.cols)]
    )


def channel_superoperator(
    projection: sp.Matrix, d: int, right: bool
) -> sp.Matrix:
    identity = sp.eye(d)
    columns: list[sp.Matrix] = []
    for i in range(d):
        for j in range(d):
            matrix_unit = sp.zeros(d)
            matrix_unit[i, j] = 1
            if right:
                insertion = tensor(matrix_unit, identity)
                image = sp.Rational(2, d) * partial_trace_second(
                    projection * insertion * projection, d
                )
            else:
                insertion = tensor(identity, matrix_unit)
                image = sp.Rational(2, d) * partial_trace_first(
                    projection * insertion * projection, d
                )
            columns.append(vectorize(image))
    return sp.Matrix.hstack(*columns)


def apply_to_second_leg(
    matrix: sp.Matrix, channel: sp.Matrix, d: int
) -> sp.Matrix:
    result = sp.zeros(d * d)
    for a in range(d):
        for c in range(d):
            block = sp.Matrix(
                d,
                d,
                lambda b, ell: matrix[d * a + b, d * c + ell],
            )
            image = sp.Matrix(d, d, list(channel * vectorize(block)))
            for b in range(d):
                for ell in range(d):
                    result[d * a + b, d * c + ell] = image[b, ell]
    return result


def apply_to_first_leg(
    matrix: sp.Matrix, channel: sp.Matrix, d: int
) -> sp.Matrix:
    result = sp.zeros(d * d)
    for b in range(d):
        for ell in range(d):
            block = sp.Matrix(
                d,
                d,
                lambda a, c: matrix[d * a + b, d * c + ell],
            )
            image = sp.Matrix(d, d, list(channel * vectorize(block)))
            for a in range(d):
                for c in range(d):
                    result[d * a + b, d * c + ell] = image[a, c]
    return result


def realignment(matrix: sp.Matrix, d: int) -> sp.Matrix:
    return sp.Matrix(
        d * d,
        d * d,
        lambda ac, bd: matrix[
            d * (ac // d) + bd // d,
            d * (ac % d) + bd % d,
        ],
    )


def is_zero_matrix(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def exact_sparse_witness() -> None:
    d = 4
    identity_2 = sp.eye(2)
    identity_4 = sp.eye(4)
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
    projection = (sp.eye(d * d) - h) / 2

    assert h.conjugate().T == h
    assert sp.simplify(h * h) == sp.eye(d * d)
    assert partial_trace_first(projection, d) == 2 * identity_4
    assert partial_trace_second(projection, d) == 2 * identity_4

    # Canonical simplification once keeps all subsequent exact matrix
    # operations in the small field Q(sqrt(2),sqrt(3)).
    channel_r = channel_superoperator(
        projection, d, right=True
    ).applyfunc(sp.simplify)
    channel_l = channel_superoperator(
        projection, d, right=False
    ).applyfunc(sp.simplify)
    super_identity = sp.eye(d * d)
    identity_vector = vectorize(identity_4)
    omega = identity_vector * identity_vector.T / d

    for channel in (channel_r, channel_l):
        assert is_zero_matrix(channel.conjugate().T - channel)
        assert is_zero_matrix(channel * identity_vector - identity_vector)
        assert sp.simplify(sp.trace(channel) - 8) == 0
        assert is_zero_matrix(
            (channel - super_identity) * (3 * channel - super_identity)
        )
        polynomial = channel.charpoly()
        characteristic = sp.factor(polynomial.as_expr())
        symbol = polynomial.gen
        expected = (symbol - 1) ** 4 * (
            symbol - sp.Rational(1, 3)
        ) ** 12
        assert sp.expand(characteristic - expected) == 0
        assert len((channel - super_identity).nullspace()) == 4

    assert is_zero_matrix(channel_r * channel_l - channel_l * channel_r)
    assert is_zero_matrix(
        (channel_r + channel_l - sp.Rational(4, 3) * super_identity)
        * (channel_r - sp.Rational(1, 3) * super_identity)
        * (channel_l - sp.Rational(1, 3) * super_identity)
        - sp.Rational(8, 27) * omega
    )
    assert is_zero_matrix(
        apply_to_second_leg(projection, channel_r, d)
        - (sp.eye(d * d) + projection) / 3
    )
    assert is_zero_matrix(
        apply_to_first_leg(projection, channel_l, d)
        - (sp.eye(d * d) + projection) / 3
    )
    intertwiner = realignment(projection, d).T
    identity_reshuffling = realignment(sp.eye(d * d), d).T
    affine_intertwiner_image = (
        identity_reshuffling + intertwiner
    ) / 3
    assert is_zero_matrix(
        channel_r * intertwiner - affine_intertwiner_image
    )
    assert is_zero_matrix(
        intertwiner * channel_l.T - affine_intertwiner_image
    )
    assert realignment(h, d).rank() == 3
    assert intertwiner.rank() == 4

    print("Published sparse d=4 witness")
    print("  spectrum(E_R) = spectrum(E_L) = {1^4, (1/3)^12}")
    print("  tr_super(E_R) = tr_super(E_L) = 8")
    print("  [E_L,E_R] = 0 exactly")
    print("  paired joint-channel polynomial holds exactly")
    print("  operator-Schmidt rank(H) = 3")
    print("  crossed reshuffling intertwiner has rank 4")


def exact_standard_non_ybe_guard() -> None:
    """A rational standard projection whose two channels do not commute."""
    d = 4
    identity = sp.eye(d)
    a = sp.diag(1, 1, -1, -1)
    rotation = sp.eye(d)
    rotation[0, 0] = sp.Rational(3, 5)
    rotation[0, 2] = -sp.Rational(4, 5)
    rotation[2, 0] = sp.Rational(4, 5)
    rotation[2, 2] = sp.Rational(3, 5)
    c = rotation * a * rotation.T
    blocks = (a, -a, c, -c)

    h = sp.zeros(d * d)
    for color, block in enumerate(blocks):
        color_projection = sp.zeros(d)
        color_projection[color, color] = 1
        h += tensor(color_projection, block)
    projection = (sp.eye(d * d) - h) / 2

    assert h.T == h
    assert h * h == sp.eye(d * d)
    assert sp.trace(h) == 0
    assert partial_trace_first(projection, d) == 2 * identity
    assert partial_trace_second(projection, d) == 2 * identity

    channel_r = channel_superoperator(projection, d, right=True)
    channel_l = channel_superoperator(projection, d, right=False)
    commutator = channel_r * channel_l - channel_l * channel_r
    commutator_squared = sp.trace(commutator.T * commutator)
    assert commutator_squared > 0
    moment_differences = [
        sp.factor(sp.trace(channel_r**power) - sp.trace(channel_l**power))
        for power in range(2, d * d + 1)
    ]
    first_distinguishing_moment = next(
        (
            (power, difference)
            for power, difference in enumerate(moment_differences, start=2)
            if difference != 0
        ),
        None,
    )
    identity_vector = vectorize(identity)
    omega = identity_vector * identity_vector.T / d
    super_identity = sp.eye(d * d)
    paired_residual = (
        (channel_r + channel_l - sp.Rational(4, 3) * super_identity)
        * (channel_r - sp.Rational(1, 3) * super_identity)
        * (channel_l - sp.Rational(1, 3) * super_identity)
        - sp.Rational(8, 27) * omega
    )
    paired_residual_squared = sp.factor(
        sp.trace(paired_residual.T * paired_residual)
    )
    assert paired_residual_squared > 0

    h_1 = tensor(h, identity)
    h_2 = tensor(identity, h)
    cubic_residual = (
        h_1 * h_2 * h_1
        - h_2 * h_1 * h_2
        - (h_1 - h_2) / 3
    )
    assert cubic_residual != sp.zeros(d**3)

    print("Rational standardness guard")
    print(f"  ||[E_L,E_R]||_F^2 = {commutator_squared}")
    if first_distinguishing_moment is None:
        print("  E_L and E_R have the same characteristic polynomial")
    else:
        power, difference = first_distinguishing_moment
        print(
            f"  tr_super(E_R^{power})-tr_super(E_L^{power}) = "
            f"{difference}"
        )
    print(
        "  paired-polynomial residual norm^2 = "
        f"{paired_residual_squared}"
    )
    print("  cubic residual is nonzero (this is not a YBE solution)")
    print("  standardness alone therefore does not imply channel commutation")


if __name__ == "__main__":
    exact_sparse_witness()
    exact_standard_non_ybe_guard()
    print("[ok] exact canonical-channel certificates passed")
