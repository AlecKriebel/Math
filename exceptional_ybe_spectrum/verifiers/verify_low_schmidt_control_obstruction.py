#!/usr/bin/env python3
"""Exact replay for the low-operator-Schmidt obstruction.

The human proof is in ``notes/low_schmidt_control_obstruction.md``.  This
program independently checks the tensor orientations that are easiest to
get wrong in that proof:

1. arbitrary four-unitary local equivalence to a controlled gate can be
   rewritten, after one *sitewise conjugacy*, as
       sum_i E_i K tensor V_i;
2. for a fixed-point-free twisted-control involution
       H = sum_x |bar(x)><x| tensor U_x,
   the off-diagonal coefficient of the shifted cubic is exactly
       -H (U_x tensor I) H - c (U_x tensor I);
3. a balanced, standard, Schmidt-rank-three d=6 involution of that
   fixed-point-free form exists but has nonzero exceptional residual;
4. both exact d=4 Schmidt-rank-three calibration orbits satisfy the cubic
   and have a genuine rank-one projection in one leg commutant.

All calculations use SymPy exact arithmetic.
"""

from __future__ import annotations

import itertools

import sympy as sp


def kron(*matrices: sp.MatrixBase) -> sp.Matrix:
    out = sp.Matrix([[1]])
    for matrix in matrices:
        out = sp.kronecker_product(out, matrix)
    return sp.Matrix(out)


def sparse_kron(*matrices: sp.MatrixBase) -> sp.SparseMatrix:
    return sp.SparseMatrix(kron(*matrices))


def is_zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def partial_trace_second(matrix: sp.MatrixBase, d: int) -> sp.Matrix:
    return sp.Matrix(
        d,
        d,
        lambda a, c: sum(
            matrix[d * a + b, d * c + b] for b in range(d)
        ),
    )


def partial_trace_first(matrix: sp.MatrixBase, d: int) -> sp.Matrix:
    return sp.Matrix(
        d,
        d,
        lambda b, e: sum(
            matrix[d * a + b, d * a + e] for a in range(d)
        ),
    )


def realignment(matrix: sp.MatrixBase, d: int) -> sp.Matrix:
    """Rows are first-site matrix indices, columns second-site indices."""

    return sp.Matrix(
        d * d,
        d * d,
        lambda row, column: matrix[
            d * (row // d) + column // d,
            d * (row % d) + column % d,
        ],
    )


def residual(matrix: sp.MatrixBase, d: int) -> sp.Matrix:
    h1 = kron(matrix, sp.eye(d))
    h2 = kron(sp.eye(d), matrix)
    return sp.simplify(
        h1 * h2 * h1
        - h2 * h1 * h2
        - sp.Rational(1, 3) * (h1 - h2)
    )


def squared_norm(matrix: sp.MatrixBase) -> sp.Expr:
    return sp.simplify(
        sum(sp.conjugate(entry) * entry for entry in matrix)
    )


I2 = sp.eye(2)
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
Z = sp.diag(1, -1)
J = -sp.I * Y


def check_four_unitary_normalization() -> None:
    """Replay the precise allowed map from local equivalence to H'=DK."""

    # Deliberately use four distinct exact unitaries.
    q = X
    r = Z
    s = sp.diag(1, sp.I)
    t = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2)
    controls = [sp.diag(1, 0), sp.diag(0, 1)]
    targets = [X, Z]
    controlled = sum(
        (kron(controls[i], targets[i]) for i in range(2)),
        sp.zeros(4),
    )
    original = kron(q, s) * controlled * kron(r, t)

    # This is a sitewise conjugacy, unlike the four-unitary equivalence.
    transformed = kron(q.H, q.H) * original * kron(q, q)
    k_matrix = r * q
    new_targets = [q.H * s * target * t * q for target in targets]
    normal_form = sum(
        (
            kron(controls[i] * k_matrix, new_targets[i])
            for i in range(2)
        ),
        sp.zeros(4),
    )
    assert is_zero(transformed - normal_form)
    assert all(is_zero(v.H * v - I2) for v in new_targets)


def check_fixed_point_free_coefficient_identity() -> None:
    """Exact d=6 orientation test for the all-bipartite graph branch."""

    d = 6
    identity_3 = sp.eye(3)
    target_unitaries = [
        kron(X, identity_3),
        kron(Y, identity_3),
        kron(Z, identity_3),
    ]

    pair_flips: list[sp.SparseMatrix] = []
    for pair in range(3):
        flip = sp.MutableSparseMatrix(d, d, {})
        flip[2 * pair, 2 * pair + 1] = 1
        flip[2 * pair + 1, 2 * pair] = 1
        pair_flips.append(sp.SparseMatrix(flip))

    h = sp.MutableSparseMatrix(d * d, d * d, {})
    for pair in range(3):
        h += sparse_kron(pair_flips[pair], target_unitaries[pair])
    h = sp.SparseMatrix(h)

    assert is_zero(h.H - h)
    assert is_zero(h * h - sp.eye(d * d))
    assert sp.trace(h) == 0
    assert is_zero(partial_trace_first(h, d))
    assert is_zero(partial_trace_second(h, d))
    assert realignment(h, d).rank() == 3

    h1 = sparse_kron(h, sp.eye(d))
    h2 = sparse_kron(sp.eye(d), h)
    aba = h1 * h2 * h1
    bab = h2 * h1 * h2

    def first_leg_block(
        matrix: sp.MatrixBase, row: int, column: int
    ) -> sp.SparseMatrix:
        block_size = d * d
        return sp.SparseMatrix(
            matrix[
                row * block_size : (row + 1) * block_size,
                column * block_size : (column + 1) * block_size,
            ]
        )

    for x in range(d):
        bar_x = x ^ 1
        u_x = target_unitaries[x // 2]
        insertion = sparse_kron(u_x, sp.eye(d))

        # These four assertions independently fix every tensor orientation
        # in the coefficient extraction used in the proof.
        assert first_leg_block(aba, bar_x, x).nnz() == 0
        assert is_zero(
            first_leg_block(bab, bar_x, x) - h * insertion * h
        )
        assert is_zero(first_leg_block(h1, bar_x, x) - insertion)
        assert first_leg_block(h2, bar_x, x).nnz() == 0

        extracted_residual = first_leg_block(
            h1 * h2 * h1
            - h2 * h1 * h2
            - sp.Rational(1, 3) * (h1 - h2),
            bar_x,
            x,
        )
        expected = -h * insertion * h - sp.Rational(1, 3) * insertion
        assert is_zero(extracted_residual - expected)

        # The first summand is unitary, whereas the proposed right side of
        # the cubic would have norm 1/3.
        assert is_zero((h * insertion * h).H * (h * insertion * h) - sp.eye(36))

    cubic_residual = sp.SparseMatrix(
        h1 * h2 * h1
        - h2 * h1 * h2
        - sp.Rational(1, 3) * (h1 - h2)
    )
    assert squared_norm(cubic_residual) == 512


def check_mixed_component_stress_test() -> None:
    """A nonbipartite block works without cross-target commutation."""

    omega = (-1 + sp.sqrt(3) * sp.I) / 2
    w_loop = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    w_edge = sp.diag(1, omega, omega**2)
    assert not is_zero(w_loop * w_edge - w_edge * w_loop)

    e0 = sp.diag(1, 0, 0)
    s12 = sp.zeros(3)
    s12[1, 2] = 1
    h = (
        kron(e0, w_loop)
        + kron(s12, w_edge)
        + kron(s12.H, w_edge.H)
    )
    assert is_zero(h.H - h)
    assert is_zero(h * h - sp.eye(9))
    assert realignment(h, 3).rank() == 3

    # e0 is the spectral rank-one projection supplied by the loop
    # component.  It commutes on the control leg even though its target
    # unitary does not commute with the target of the other component.
    assert is_zero(kron(e0, sp.eye(3)) * h - h * kron(e0, sp.eye(3)))


def published_witness() -> tuple[sp.Matrix, list[sp.Matrix], list[sp.Matrix]]:
    a_coefficients = [kron(X, I2), kron(Y, I2), kron(Z, I2)]
    b_coefficients = [
        -kron(X, X) / sp.sqrt(3),
        (kron(Z, Y) - kron(Y, Z)) / sp.sqrt(6),
        (kron(Y, Y) - kron(Z, Z)) / sp.sqrt(6),
    ]
    h = sum(
        (
            kron(a_coefficients[i], b_coefficients[i])
            for i in range(3)
        ),
        sp.zeros(16),
    )

    original_five_word = (
        -kron(Z, I2, Z, Z) / sp.sqrt(6)
        - kron(Z, I2, J, J) / sp.sqrt(6)
        - kron(J, I2, Z, J) / sp.sqrt(6)
        + kron(J, I2, J, Z) / sp.sqrt(6)
        - kron(X, I2, X, X) / sp.sqrt(3)
    )
    assert is_zero(h - original_five_word)
    return h, a_coefficients, b_coefficients


def assemble_color_face(s_value: sp.Expr, t_value: sp.Expr) -> sp.Matrix:
    """Independent reconstruction of the C15 face-block representative."""

    hadamard = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2)
    b_operators = (X, -Y)
    c_operators = (
        -t_value * X - t_value * Y - s_value * Z,
        -t_value * X - t_value * Y + s_value * Z,
    )
    blocks: list[sp.Matrix] = []
    for first_color in range(2):
        for second_color in range(2):
            parity = (first_color + second_color) % 2
            sign = 1 if parity == 0 else -1
            blocks.append(
                sign * kron(Z, I2) / sp.sqrt(3)
                + sp.sqrt(sp.Rational(2, 3))
                * kron(b_operators[parity], c_operators[second_color])
            )

    matrix = sp.zeros(16)
    for block, (first_color, second_color) in zip(
        blocks, itertools.product(range(2), repeat=2)
    ):
        indices = [
            (2 * first_color + first_internal) * 4
            + (2 * second_color + second_internal)
            for first_internal in range(2)
            for second_internal in range(2)
        ]
        for row_in_block, row in enumerate(indices):
            for column_in_block, column in enumerate(indices):
                matrix[row, column] = block[row_in_block, column_in_block]

    change = kron(sp.eye(4), hadamard, I2)
    return sp.expand(change * matrix * change.H)


def color_face_representative() -> tuple[
    sp.Matrix, list[sp.Matrix], list[sp.Matrix]
]:
    u_plus = (X + Y) / sp.sqrt(2)
    u_minus = (X - Y) / sp.sqrt(2)
    # This is the a=0,b=1 point, equivalently s=1,t=0, on the C15 circle.
    a_coefficients = [
        kron(I2, u_minus),
        kron(Z, u_plus),
        kron(Z, Z),
    ]
    b_coefficients = [
        -kron(X, Z) / sp.sqrt(3),
        -kron(I2, Z) / sp.sqrt(3),
        kron(X, I2) / sp.sqrt(3),
    ]
    h = sum(
        (
            kron(a_coefficients[i], b_coefficients[i])
            for i in range(3)
        ),
        sp.zeros(16),
    )
    assert is_zero(h - assemble_color_face(sp.Integer(1), sp.Integer(0)))
    return h, a_coefficients, b_coefficients


def check_rank_three_calibration(
    name: str,
    h: sp.Matrix,
    a_coefficients: list[sp.Matrix],
    b_coefficients: list[sp.Matrix],
    rank_one: sp.Matrix,
) -> None:
    d = 4
    assert is_zero(h.H - h)
    assert is_zero(h * h - sp.eye(16))
    assert sp.trace(h) == 0
    assert is_zero(partial_trace_first(h, d))
    assert is_zero(partial_trace_second(h, d))
    assert is_zero(residual(h, d))

    reshuffled = realignment(h, d)
    gram = sp.simplify(reshuffled * reshuffled.H)
    assert reshuffled.rank() == 3
    assert is_zero(gram * gram - sp.Rational(16, 3) * gram)

    # The right coefficients form a four-dimensional MASA.  This is not
    # confused with the published left commutant I_2 tensor M_2, whose
    # minimal projections have rank two.
    assert all(
        is_zero(b_coefficients[i] * b_coefficients[j]
                - b_coefficients[j] * b_coefficients[i])
        for i in range(3)
        for j in range(3)
    )
    algebra_columns = [
        sp.Matrix(sp.eye(4)).reshape(16, 1),
        *[sp.Matrix(b).reshape(16, 1) for b in b_coefficients],
    ]
    assert sp.Matrix.hstack(*algebra_columns).rank() == 4
    assert rank_one.rank() == 1
    assert is_zero(rank_one * rank_one - rank_one)
    assert is_zero(rank_one.H - rank_one)
    assert all(
        is_zero(rank_one * b - b * rank_one) for b in b_coefficients
    )
    assert is_zero(kron(sp.eye(4), rank_one) * h - h * kron(sp.eye(4), rank_one))

    # Tensor reversal checks the opposite control orientation and preserves
    # both the cubic and operator-Schmidt rank.
    flip = sp.zeros(16)
    for i in range(4):
        for j in range(4):
            flip[4 * j + i, 4 * i + j] = 1
    opposite = flip * h * flip
    assert realignment(opposite, d).rank() == 3
    assert is_zero(residual(opposite, d))
    assert is_zero(kron(rank_one, sp.eye(4)) * opposite
                   - opposite * kron(rank_one, sp.eye(4)))

    print(f"PASS {name}: exact d=4 cubic, Schmidt rank 3, right-leg MASA")


def main() -> None:
    check_four_unitary_normalization()
    print("PASS four-unitary equivalence -> valid sitewise twisted-control form")

    check_mixed_component_stress_test()
    print("PASS mixed nonbipartite/bipartite graph: true control-leg rank-one symmetry")

    check_fixed_point_free_coefficient_identity()
    print("PASS fixed-point-free coefficient orientation; d=6 residual norm^2 = 512")

    h_published, a_published, b_published = published_witness()
    phi_plus = sp.Matrix([1, 0, 0, 1]) / sp.sqrt(2)
    p_phi_plus = phi_plus * phi_plus.H
    check_rank_three_calibration(
        "published five-Pauli witness",
        h_published,
        a_published,
        b_published,
        p_phi_plus,
    )

    h_color, a_color, b_color = color_face_representative()
    plus = sp.Matrix([1, 1]) / sp.sqrt(2)
    zero = sp.Matrix([1, 0])
    color_vector = kron(plus, zero)
    p_color = color_vector * color_vector.H
    check_rank_three_calibration(
        "C15 color/face representative",
        h_color,
        a_color,
        b_color,
        p_color,
    )

    print("PASS exact low-operator-Schmidt obstruction certificate")


if __name__ == "__main__":
    main()
