#!/usr/bin/env python3
"""Exact verifier for the odd-leg-projection divisibility theorem.

This uses three logically separate checks:

1. an arbitrary balanced controlled projection (not a YBE solution) checks
   first- and second-control compression orientations;
2. the published exact d=4 solution checks the common-sector count on actual
   rank-one leg-commutant projections;
3. an exact Schmidt-rank-three Hermitian reflection checks that Chen--Yu
   pre/post local equivalence cannot be replaced silently by a leg-commutant
   MASA.
"""

from __future__ import annotations

import sympy as sp


def tensor(*matrices: sp.Matrix) -> sp.Matrix:
    result = sp.Matrix([[1]])
    for matrix in matrices:
        result = sp.kronecker_product(result, matrix)
    return result


def is_zero_matrix(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def tensor_flip(d: int) -> sp.Matrix:
    flip = sp.zeros(d * d)
    for a in range(d):
        for b in range(d):
            flip[b * d + a, a * d + b] = 1
    return flip


def partial_trace_second(matrix: sp.Matrix, d: int) -> sp.Matrix:
    return sp.Matrix(
        d,
        d,
        lambda a, c: sum(
            matrix[a * d + b, c * d + b] for b in range(d)
        ),
    )


def partial_trace_first(matrix: sp.Matrix, d: int) -> sp.Matrix:
    return sp.Matrix(
        d,
        d,
        lambda b, e: sum(
            matrix[a * d + b, a * d + e] for a in range(d)
        ),
    )


def projection_residual(p: sp.Matrix, d: int) -> sp.Matrix:
    p12 = tensor(p, sp.eye(d))
    p23 = tensor(sp.eye(d), p)
    return (
        p12 * p23 * p12
        - p23 * p12 * p23
        - sp.Rational(1, 3) * (p12 - p23)
    )


def h_residual(h: sp.Matrix, d: int) -> sp.Matrix:
    h12 = tensor(h, sp.eye(d))
    h23 = tensor(sp.eye(d), h)
    return (
        h12 * h23 * h12
        - h23 * h12 * h23
        - sp.Rational(1, 3) * (h12 - h23)
    )


def compress_site(
    matrix: sp.Matrix, d: int, site: int, value: int
) -> sp.Matrix:
    """Compress a three-site matrix at one fixed computational basis vector."""
    if site == 0:
        indices = [
            (value * d + b) * d + c
            for b in range(d)
            for c in range(d)
        ]
    elif site == 2:
        indices = [
            (a * d + b) * d + value
            for a in range(d)
            for b in range(d)
        ]
    else:
        raise ValueError("only spectator sites 0 and 2 are used")
    return matrix.extract(indices, indices)


def balanced_control_orientation_check() -> None:
    """Check compression formulas before imposing a zero YBE residual."""
    d = 4
    i4 = sp.eye(d)
    p0 = sp.diag(1, 1, 0, 0)
    v1 = sp.Matrix([1, 0, 1, 0]) / sp.sqrt(2)
    v2 = sp.Matrix([0, 1, 0, 1]) / sp.sqrt(2)
    p1 = v1 * v1.T + v2 * v2.T
    blocks = [p0, p1, i4 - p0, i4 - p1]
    control_units = []
    for x in range(d):
        ex = sp.zeros(d)
        ex[x, x] = 1
        control_units.append(ex)

    p = sum(
        (
            tensor(control_units[x], blocks[x])
            for x in range(d)
        ),
        sp.zeros(d * d),
    )
    assert p == p.T
    assert p * p == p
    assert sp.trace(p) == d * d // 2
    assert partial_trace_second(p, d) == d * sp.eye(d) / 2
    assert partial_trace_first(p, d) == d * sp.eye(d) / 2

    residual = projection_residual(p, d)
    assert residual != sp.zeros(d**3)
    c = sp.Rational(1, 3)

    for x, px in enumerate(blocks):
        a = tensor(px, i4)
        expected = a * p * a - p * a * p - c * (a - p)
        assert compress_site(residual, d, 0, x) == expected
        assert sp.trace(a * p) == sp.Rational(d * d, 4)

    flip = tensor_flip(d)
    p_flipped = flip * p * flip
    residual_flipped = projection_residual(p_flipped, d)
    for x, px in enumerate(blocks):
        b = tensor(i4, px)
        expected = (
            p_flipped * b * p_flipped
            - b * p_flipped * b
            - c * (p_flipped - b)
        )
        assert compress_site(residual_flipped, d, 2, x) == expected


def abstract_arithmetic_check() -> None:
    d_symbol, common = sp.symbols("D common", integer=True, positive=True)
    c = sp.Rational(1, 3)
    trace_overlap = c * d_symbol / 2 + (1 - c) * common
    solution = sp.solve(
        sp.Eq(trace_overlap, d_symbol / 4), common
    )
    assert solution == [d_symbol / 8]

    # The rank-one consequence 8 | d^2 is exactly 4 | d.
    for d in range(1, 101):
        assert ((d * d) % 8 == 0) == (d % 4 == 0)

    # In the first unresolved dimension, 8 | r d^2 iff r is even.
    for rank in range(1, 7):
        assert ((rank * 6 * 6) % 8 == 0) == (rank % 2 == 0)


def controlled_d4_leg_sector_check() -> None:
    """Apply the count to an exact controlled V_4 conference witness."""
    d = 4
    i4 = sp.eye(d)
    conference = sp.Matrix(
        [
            [0, 1, 1, 1],
            [-1, 0, -1, 1],
            [-1, 1, 0, -1],
            [-1, -1, 1, 0],
        ]
    )
    assert conference.T == -conference
    assert conference * conference == -3 * i4
    small_h = sp.I * conference / sp.sqrt(3)

    def left_regular(element: int) -> sp.Matrix:
        result = sp.zeros(d)
        for basis in range(d):
            result[element ^ basis, basis] = 1
        return result

    blocks = []
    for element in range(d):
        left = left_regular(element)
        blocks.append(left * small_h * left.T)
    h = sp.diag(*blocks)
    p = (sp.eye(d * d) - h) / 2
    assert h.H == h
    assert h * h == sp.eye(d * d)
    assert partial_trace_first(h, d) == sp.zeros(d)
    assert partial_trace_second(h, d) == sp.zeros(d)
    assert projection_residual(p, d) == sp.zeros(d**3)

    p12 = tensor(p, i4)
    p23 = tensor(i4, p)
    c = sp.Rational(1, 3)
    for value in range(d):
        a = compress_site(p12, d, 0, value)
        b = compress_site(p23, d, 0, value)
        assert a * a == a
        assert b * b == b
        assert sp.trace(a) == sp.trace(b) == 8
        assert sp.trace(a * b) == 4
        assert a * b * a - b * a * b == c * (a - b)

        common_one = (a * b * a - c * a) / (1 - c)
        assert common_one * common_one == common_one
        assert sp.trace(common_one) == 2

        ac = sp.eye(16) - a
        bc = sp.eye(16) - b
        common_zero = (ac * bc * ac - c * ac) / (1 - c)
        assert common_zero * common_zero == common_zero
        assert sp.trace(common_zero) == 2


def operator_schmidt_rank(matrix: sp.Matrix, d: int) -> int:
    realigned = sp.Matrix(
        d * d,
        d * d,
        lambda row, column: matrix[
            (row // d) * d + (column // d),
            (row % d) * d + (column % d),
        ],
    )
    return realigned.rank()


def linear_commutant_dimension(
    matrix: sp.Matrix, d: int, left: bool
) -> int:
    variables = sp.symbols(f"c0:{d*d}")
    unknown = sp.Matrix(d, d, variables)
    embedded = (
        tensor(unknown, sp.eye(d))
        if left
        else tensor(sp.eye(d), unknown)
    )
    equations = list(embedded * matrix - matrix * embedded)
    coefficient_matrix, _ = sp.linear_eq_to_matrix(equations, variables)
    return len(coefficient_matrix.nullspace())


def schmidt_rank_three_counter_audit() -> None:
    i2 = sp.eye(2)
    x = sp.Matrix([[0, 1], [1, 0]])
    z = sp.diag(1, -1)
    a_terms = [tensor(x, i2), tensor(z, i2), tensor(i2, z)]
    b_terms = [tensor(z, i2), tensor(z, z), tensor(x, i2)]
    h = sum(
        (
            tensor(a_term, b_term)
            for a_term, b_term in zip(a_terms, b_terms)
        ),
        sp.zeros(16),
    ) / sp.sqrt(3)

    assert h.H == h
    assert sp.simplify(h * h) == sp.eye(16)
    assert sp.trace(h) == 0
    assert partial_trace_first(h, 4) == sp.zeros(4)
    assert partial_trace_second(h, 4) == sp.zeros(4)
    assert operator_schmidt_rank(h, 4) == 3

    common_nontrivial = tensor(i2, z)
    assert tensor(common_nontrivial, sp.eye(4)) * h == (
        h * tensor(common_nontrivial, sp.eye(4))
    )
    assert tensor(sp.eye(4), common_nontrivial) * h == (
        h * tensor(sp.eye(4), common_nontrivial)
    )
    assert linear_commutant_dimension(h, 4, left=True) == 2
    assert linear_commutant_dimension(h, 4, left=False) == 2
    minimal = (sp.eye(4) + common_nontrivial) / 2
    assert minimal * minimal == minimal
    assert sp.trace(minimal) == 2

    residual = h_residual(h, 4)
    assert residual != sp.zeros(64)
    norm_squared = sp.simplify(sp.trace(residual.H * residual))
    assert norm_squared == sp.Rational(512, 3)


def main() -> None:
    balanced_control_orientation_check()
    abstract_arithmetic_check()
    controlled_d4_leg_sector_check()
    schmidt_rank_three_counter_audit()
    print("PASS both controlled-leg compression orientations")
    print("PASS overlap D/4 and common-one/common-zero arithmetic D/8")
    print("PASS 8 | d^2 iff 4 | d for rank-one control")
    print("PASS d=6 requires every leg-commutant projection rank to be even")
    print("PASS four exact rank-one sectors of a V4 conference d=4 witness")
    print("PASS each d=4 restricted common-one/common-zero rank equals 2")
    print("PASS exact OSR-3 local-equivalence/commutant counter-audit")
    print("PASS OSR-3 counterexample cubic residual norm^2 = 512/3")


if __name__ == "__main__":
    main()
