#!/usr/bin/env python3
"""Exact certificate for the color/face-circle amplification cut theorem.

The human proof is in
``notes/no_codimension_two_cut_color_face_family.md``.  This verifier:

1. independently rebuilds the C15 color/face matrix and extracts its
   uniform three-term form;
2. checks the Clifford and tetrahedral-pencil identities modulo
   a^2+b^2-1;
3. verifies the six low-rank lines and absence of rank-one pencil
   elements by exact integer linear algebra;
4. checks the active-commutant argument; and
5. checks the exact sitewise rotation of the whole family; and
6. separates this orbit from the published five-Pauli witness by a
   fourth flip-moment invariant.
"""

from __future__ import annotations

import itertools

import sympy as sp


I2 = sp.eye(2)
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
Z = sp.diag(1, -1)
U_PLUS = (X + Y) / sp.sqrt(2)
U_MINUS = (X - Y) / sp.sqrt(2)


def kron(*matrices: sp.Matrix) -> sp.Matrix:
    result = sp.ones(1, 1)
    for matrix in matrices:
        result = sp.kronecker_product(result, matrix)
    return result


def zero_mod(matrix: sp.Matrix, relations: list[sp.Expr]) -> bool:
    """Reduce polynomial entries by the supplied monic relations."""

    variables = sorted(
        set().union(*(relation.free_symbols for relation in relations)),
        key=lambda symbol: symbol.name,
    )
    for entry in matrix:
        numerator = sp.together(sp.expand(entry)).as_numer_denom()[0]
        remainder = sp.reduced(
            numerator,
            relations,
            *variables,
            extension=True,
        )[1]
        if sp.expand(remainder) != 0:
            return False
    return True


def assemble_color_face(s: sp.Expr, t: sp.Expr) -> sp.Matrix:
    """Rebuild the C15 family from its four face blocks."""

    hadamard = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2)
    b_operators = (X, -Y)
    c_operators = (
        -t * X - t * Y - s * Z,
        -t * X - t * Y + s * Z,
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
        blocks,
        itertools.product(range(2), repeat=2),
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


def coefficients(a: sp.Expr, b: sp.Expr) -> tuple[list[sp.Matrix], list[sp.Matrix]]:
    a_ops = [
        kron(I2, U_MINUS),
        kron(Z, U_PLUS),
        kron(Z, Z),
    ]
    b_hats = [
        -(a * kron(I2, U_PLUS) + b * kron(X, Z)),
        -(b * kron(I2, Z) + a * kron(X, U_PLUS)),
        kron(X, I2),
    ]
    return a_ops, [operator / sp.sqrt(3) for operator in b_hats]


def check_extraction() -> None:
    s, t = sp.symbols("s t", real=True)
    a = sp.sqrt(2) * t
    b = s
    h_blocks = assemble_color_face(s, t)
    a_ops, b_ops = coefficients(a, b)
    h_three_term = sum(
        (kron(left, right) for left, right in zip(a_ops, b_ops)),
        sp.zeros(16),
    )
    assert h_blocks == sp.expand(h_three_term)


def check_clifford_and_pencil() -> tuple[int, int]:
    a, b = sp.symbols("a b", real=True)
    relation = a**2 + b**2 - 1
    a_ops, b_ops = coefficients(a, b)
    identity = sp.eye(4)

    for index, left in enumerate(a_ops):
        assert left.H == left
        assert sp.simplify(left * left - identity) == sp.zeros(4)
        for other in a_ops[index + 1 :]:
            assert sp.simplify(left * other + other * left) == sp.zeros(4)

    b_hats = [sp.sqrt(3) * operator for operator in b_ops]
    for operator in b_hats:
        assert operator.H == operator
        assert zero_mod(operator * operator - identity, [relation])
    for first, second in itertools.combinations(b_hats, 2):
        assert sp.simplify(first * second - second * first) == sp.zeros(4)
    assert zero_mod(b_hats[0] * b_hats[1] * b_hats[2] - identity, [relation])

    # The joint projectors have trace one, hence rank one, on the circle.
    for first_sign, second_sign in itertools.product((1, -1), repeat=2):
        projector = (
            (identity + first_sign * b_hats[0])
            * (identity + second_sign * b_hats[1])
            / 4
        )
        assert zero_mod(projector * projector - projector, [relation])
        assert zero_mod(projector.H - projector, [relation])
        assert sp.simplify(sp.trace(projector) - 1) == 0

    vertices = [
        sp.Matrix((1, 1, 1)),
        sp.Matrix((1, -1, -1)),
        sp.Matrix((-1, 1, -1)),
        sp.Matrix((-1, -1, 1)),
    ]
    lines: set[tuple[int, int, int]] = set()
    for first, second in itertools.combinations(vertices, 2):
        direction = first.cross(second)
        entries = [int(entry) for entry in direction]
        divisor = sp.gcd_list([abs(entry) for entry in entries if entry])
        entries = [entry // divisor for entry in entries]
        first_nonzero = next(entry for entry in entries if entry)
        if first_nonzero < 0:
            entries = [-entry for entry in entries]
        lines.add(tuple(entries))
    expected_lines = {
        (0, 1, 1),
        (0, 1, -1),
        (1, 0, 1),
        (1, 0, -1),
        (1, 1, 0),
        (1, -1, 0),
    }
    assert lines == expected_lines

    # Vanishing of three eigenvalue forms forces the zero pencil.
    triple_determinants = {
        abs(int(sp.Matrix.hstack(*triple).T.det()))
        for triple in itertools.combinations(vertices, 3)
    }
    assert triple_determinants == {4}
    return len(lines), next(iter(triple_determinants))


def check_active_commutant() -> int:
    a, b = sp.symbols("a b", real=True)
    relation = a**2 + b**2 - 1
    a_ops, b_ops = coefficients(a, b)
    c_operator = kron(X, U_MINUS)
    identity = sp.eye(4)

    assert c_operator.H == c_operator
    assert sp.simplify(c_operator * c_operator - identity) == sp.zeros(4)
    for left in a_ops:
        assert sp.simplify(c_operator * left - left * c_operator) == sp.zeros(4)
    assert sp.simplify(sp.sqrt(3) * b_ops[2] - a_ops[0] * c_operator) == sp.zeros(4)
    assert sp.simplify(c_operator * b_ops[0] + b_ops[0] * c_operator) == sp.zeros(4)
    assert zero_mod(b_ops[0] * b_ops[0] - identity / 3, [relation])

    # Independently close the algebra at three representative points.
    def algebra_dimension(generators: list[sp.Matrix]) -> int:
        basis = [sp.eye(4)]
        rank = 1
        frontier = [sp.eye(4)]
        while frontier:
            current = frontier.pop()
            for generator in generators:
                candidate = sp.simplify(current * generator)
                columns = [
                    sp.Matrix(matrix).reshape(16, 1)
                    for matrix in basis + [candidate]
                ]
                new_rank = sp.Matrix.hstack(*columns).rank()
                if new_rank > rank:
                    basis.append(candidate)
                    frontier.append(candidate)
                    rank = new_rank
        return rank

    dimensions = []
    for point in ((0, 1), (1, 0), (sp.sqrt(2) / 2, sp.sqrt(2) / 2)):
        substitutions = {a: point[0], b: point[1]}
        generators = [
            operator.subs(substitutions) for operator in a_ops + b_ops
        ]
        dimensions.append(algebra_dimension(generators))
    assert dimensions == [16, 16, 16]
    return dimensions[0]


def check_sitewise_orbit() -> None:
    a, b, c, d = sp.symbols("a b c d", real=True)
    half_angle_relation = c**2 + d**2 - 1
    a_ops, b_ops = coefficients(a, b)
    c_operator = kron(X, U_MINUS)
    unitary = c * sp.eye(4) + sp.I * d * c_operator
    unitary_adjoint = unitary.H
    cosine = c**2 - d**2
    sine = 2 * c * d
    a_rotated = a * cosine + b * sine
    b_rotated = -a * sine + b * cosine
    _, rotated_b_ops = coefficients(a_rotated, b_rotated)

    assert zero_mod(unitary * unitary_adjoint - sp.eye(4), [half_angle_relation])
    for left in a_ops:
        assert zero_mod(
            unitary * left * unitary_adjoint - left,
            [half_angle_relation],
        )
    for original, rotated in zip(b_ops, rotated_b_ops):
        assert zero_mod(
            unitary * original * unitary_adjoint - rotated,
            [half_angle_relation],
        )


def check_published_orbit_separation() -> tuple[sp.Expr, sp.Expr]:
    """Compare the sitewise-conjugacy invariant Tr((H F)^4)."""

    flip = sp.zeros(16)
    for first in range(4):
        for second in range(4):
            flip[second * 4 + first, first * 4 + second] = 1

    j_matrix = -sp.I * Y
    published = (
        -kron(Z, I2, Z, Z) / sp.sqrt(6)
        - kron(Z, I2, j_matrix, j_matrix) / sp.sqrt(6)
        - kron(j_matrix, I2, Z, j_matrix) / sp.sqrt(6)
        + kron(j_matrix, I2, j_matrix, Z) / sp.sqrt(6)
        - kron(X, I2, X, X) / sp.sqrt(3)
    )
    color_face = assemble_color_face(sp.Integer(1), sp.Integer(0))
    published_flip = sp.simplify(published * flip)
    color_flip = sp.simplify(color_face * flip)

    assert sp.simplify(published_flip**4 - sp.eye(16)) == sp.zeros(16)
    published_moment = sp.simplify(sp.trace(published_flip**4))
    color_moment = sp.simplify(sp.trace(color_flip**4))
    assert published_moment == 16
    assert color_moment == -sp.Rational(16, 3)
    return published_moment, color_moment


def main() -> None:
    check_extraction()
    line_count, triple_determinant = check_clifford_and_pencil()
    algebra_dimension = check_active_commutant()
    check_sitewise_orbit()
    published_moment, color_moment = check_published_orbit_separation()
    print("exact color/face amplification-cut certificate passed")
    print("three-term coefficient extraction: exact")
    print(f"tetrahedral low-rank lines: {line_count}")
    print(f"absolute determinant of every three vertex rows: {triple_determinant}")
    print(f"active generated algebra dimension: {algebra_dimension}")
    print("sitewise unitary orbit: exact")
    print(
        "fourth flip moments (published, color/face): "
        f"({published_moment}, {color_moment})"
    )
    print("human theorem: no rank-(4m-2) square cut for every m >= 2")


if __name__ == "__main__":
    main()
