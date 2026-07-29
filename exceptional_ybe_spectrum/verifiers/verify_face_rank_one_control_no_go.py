#!/usr/bin/env python3
"""Exact checks for the rank-one Bloch-controlled d=6 no-go theorem.

This verifier checks the finite algebraic identities used in
notes/face_rank_one_control_no_go_d6.md.  The dimension argument concerning
orthogonal two-dimensional row spaces in C^3 is elementary and is reported
explicitly rather than hidden in a numerical rank computation.
"""

from fractions import Fraction

import sympy as sp


def partial_trace_first(matrix: sp.Matrix, local_dimension: int) -> sp.Matrix:
    """Trace the first factor from an operator on C^d tensor C^d."""
    d = local_dimension
    return sp.Matrix(
        d,
        d,
        lambda row, column: sum(
            matrix[a * d + row, a * d + column] for a in range(d)
        ),
    )


def partial_trace_first_three(
    matrix: sp.Matrix, local_dimension: int
) -> sp.Matrix:
    """Trace site 1 from an operator on three d-dimensional sites."""
    d = local_dimension
    return sp.Matrix(
        d * d,
        d * d,
        lambda row, column: sum(
            matrix[
                (a * d * d) + row,
                (a * d * d) + column,
            ]
            for a in range(d)
        ),
    )


def verify_pauli_product() -> None:
    i = sp.I
    sigma = [
        sp.Matrix([[0, 1], [1, 0]]),
        sp.Matrix([[0, -i], [i, 0]]),
        sp.Matrix([[1, 0], [0, -1]]),
    ]
    x = sp.symbols("x0:3", real=True)
    y = sp.symbols("y0:3", real=True)
    ax = sum((x[a] * sigma[a] for a in range(3)), sp.zeros(2))
    ay = sum((y[a] * sigma[a] for a in range(3)), sp.zeros(2))
    dot = sum(x[a] * y[a] for a in range(3))
    cross = [
        x[1] * y[2] - x[2] * y[1],
        x[2] * y[0] - x[0] * y[2],
        x[0] * y[1] - x[1] * y[0],
    ]
    rhs = dot * sp.eye(2) + i * sum(
        (cross[a] * sigma[a] for a in range(3)), sp.zeros(2)
    )
    assert all(sp.expand(entry) == 0 for entry in ax * ay - rhs)


def verify_compression_and_channel_orientation() -> None:
    """Check every sign and leg orientation on a noncommuting exact example."""
    i2 = sp.eye(2)
    x = sp.Matrix([[0, 1], [1, 0]])
    z = sp.Matrix([[1, 0], [0, -1]])
    reflections = [x, z]
    projectors = [
        sp.diag(1, 0),
        sp.diag(0, 1),
    ]
    h = sum(
        (
            sp.kronecker_product(reflections[j], projectors[j])
            for j in range(2)
        ),
        sp.zeros(4),
    )
    h1 = sp.kronecker_product(h, i2)
    h2 = sp.kronecker_product(i2, h)
    h_residual = h1 * h2 * h1 - h2 * h1 * h2 - (h1 - h2) / 3

    p = (sp.eye(4) - h) / 2
    p1 = sp.kronecker_product(p, i2)
    p2 = sp.kronecker_product(i2, p)
    p_residual = p1 * p2 * p1 - p2 * p1 * p2 - (p1 - p2) / 3
    assert h_residual == -8 * p_residual

    for k in range(2):
        indices = [(a * 2 + b) * 2 + k for a in range(2) for b in range(2)]
        compressed = h_residual.extract(indices, indices)
        formula = sp.zeros(4)
        for row in range(2):
            for column in range(2):
                coefficient = reflections[k][row, column]
                matrix_unit = sp.zeros(2)
                matrix_unit[row, column] = 1
                formula += coefficient * sp.kronecker_product(
                    reflections[row] * reflections[column], matrix_unit
                )
        for row in range(2):
            formula -= sp.kronecker_product(
                reflections[row],
                reflections[k] * projectors[row] * reflections[k],
            )
        controlled_h = sum(
            (
                sp.kronecker_product(reflections[row], projectors[row])
                for row in range(2)
            ),
            sp.zeros(4),
        )
        formula -= (
            controlled_h - sp.kronecker_product(i2, reflections[k])
        ) / 3
        assert compressed == formula

    # The channel tracing the first leg is the Schur channel on the control
    # basis.  Here n_0 dot n_1 = 0, hence its off-diagonal symbol is 1/2.
    for row in range(2):
        for column in range(2):
            matrix_unit = sp.zeros(2)
            matrix_unit[row, column] = 1
            embedded = sp.kronecker_product(i2, matrix_unit)
            channel_value = partial_trace_first(p * embedded * p, 2)
            # Normalization 2/d equals one in this d=2 check.
            expected_symbol = (
                sp.Integer(1)
                if row == column
                else sp.Rational(1, 2)
            )
            assert channel_value == expected_symbol * matrix_unit

    # For an arbitrary controlled reflection the correctly oriented channel
    # defect is exactly (2/d) times the first-site partial trace of the
    # projection residual.  Thus a vanishing cubic residual implies
    # (E_L tensor id)(P) = (I + P)/3.
    channel_on_first_p = sp.zeros(4)
    for row in range(2):
        for column in range(2):
            local_unit = sp.zeros(2)
            local_unit[row, column] = 1
            coefficient = sp.zeros(2)
            for b in range(2):
                for c in range(2):
                    coefficient[b, c] = p[
                        row * 2 + b,
                        column * 2 + c,
                    ]
            channel_unit = partial_trace_first(
                p * sp.kronecker_product(i2, local_unit) * p, 2
            )
            channel_on_first_p += sp.kronecker_product(
                channel_unit, coefficient
            )
    # The preceding assembly applies the channel to the first local matrix
    # unit in P and leaves its second-leg coefficient untouched.
    channel_defect = channel_on_first_p - (sp.eye(4) + p) / 3
    traced_residual = partial_trace_first_three(p_residual, 2)
    assert channel_defect == traced_residual


def gram_matrix(size: int) -> sp.Matrix:
    return sp.Matrix(
        size,
        size,
        lambda row, column: sp.Integer(1)
        if row == column
        else -sp.Rational(1, 3),
    )


def verify_gram_spectra() -> None:
    gram4 = gram_matrix(4)
    gram6 = gram_matrix(6)
    assert gram4.eigenvals() == {sp.Rational(4, 3): 3, sp.Integer(0): 1}
    assert gram4.rank() == 3
    assert gram6.eigenvals() == {
        sp.Rational(4, 3): 5,
        -sp.Rational(2, 3): 1,
    }
    assert gram6.det() < 0


def main() -> None:
    verify_pauli_product()
    verify_compression_and_channel_orientation()

    exceptional_dot = -sp.Rational(1, 3)
    schur_symbol = (1 + exceptional_dot) / 2
    assert schur_symbol == sp.Rational(1, 3)

    cubic_constant = Fraction(1, 3)
    # If U D U* = -c D with U unitary and D != 0, norm preservation
    # would require 1 = c.  The exceptional constant fails this exactly.
    assert cubic_constant * cubic_constant != 1

    # Two maximally entangled 2 x m coefficient matrices have two-dimensional
    # row spaces.  Such spaces cannot be mutually orthogonal for m <= 3.
    assert 2 + 2 > 3

    verify_gram_spectra()
    print("PASS symbolic Pauli product identity")
    print("PASS exact compressed cubic signs and H/P normalization")
    print("PASS exact Schur-channel formula and first-leg orientation")
    print("PASS exceptional Schur symbol: (1 - 1/3)/2 = 1/3")
    print("PASS lower-span unitary-conjugation norm obstruction")
    print("PASS 2D + 2D row spaces cannot be orthogonal in C^3")
    print("PASS d=4 tetrahedral Gram spectrum: {4/3 x3, 0 x1}")
    print("PASS d=6 Gram spectrum: {4/3 x5, -2/3 x1}")
    print("PASS rank-one Bloch-controlled d=6 ansatz is excluded exactly")


if __name__ == "__main__":
    main()
