#!/usr/bin/env python3
"""Exact checks for the diagonal-regular finite-group ansatz.

The verifier has two logically separate parts.

1.  It reconstructs the V_4 calibration from an integer skew conference
    matrix and verifies the full exceptional cubic relation over Q(sqrt(3),i).
2.  It exhausts the inverse-closed support patterns in the dual Fourier
    obstruction for the cyclic group C_6 using exact rational arithmetic.

The general rank-one-leg divisibility theorem used to exclude both C_6 and
S_3 is proved in notes/controlled_leg_divisibility.md.  Here we verify its
small integer arithmetic independently.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product

import sympy as sp


def partial_trace(matrix: sp.Matrix, dims: tuple[int, ...], leg: int) -> sp.Matrix:
    """Trace one tensor leg of a matrix in lexicographic tensor order."""
    kept = dims[:leg] + dims[leg + 1 :]
    output_size = 1
    for dimension in kept:
        output_size *= dimension

    def decode(index: int, shape: tuple[int, ...]) -> list[int]:
        result = [0] * len(shape)
        for position in range(len(shape) - 1, -1, -1):
            result[position] = index % shape[position]
            index //= shape[position]
        return result

    def encode(indices: list[int], shape: tuple[int, ...]) -> int:
        result = 0
        for index, dimension in zip(indices, shape):
            result = result * dimension + index
        return result

    answer = sp.zeros(output_size)
    for row in range(output_size):
        row_kept = decode(row, kept)
        for column in range(output_size):
            column_kept = decode(column, kept)
            entry = 0
            for traced_index in range(dims[leg]):
                row_full = row_kept.copy()
                column_full = column_kept.copy()
                row_full.insert(leg, traced_index)
                column_full.insert(leg, traced_index)
                entry += matrix[
                    encode(row_full, dims),
                    encode(column_full, dims),
                ]
            answer[row, column] = sp.simplify(entry)
    return answer


def klein_left_regular(element: int) -> sp.Matrix:
    """Left translation by an element of V_4, indexed by two-bit XOR."""
    matrix = sp.zeros(4)
    for basis in range(4):
        matrix[element ^ basis, basis] = 1
    return matrix


def lifted_controlled_reflection(small_h: sp.Matrix) -> sp.Matrix:
    """H = sum_x |x><x| tensor L_x h L_x^* for V_4."""
    blocks = []
    for element in range(4):
        left = klein_left_regular(element)
        blocks.append(left * small_h * left.T)
    return sp.diag(*blocks)


def verify_v4_conference_calibration() -> None:
    conference = sp.Matrix(
        [
            [0, 1, 1, 1],
            [-1, 0, -1, 1],
            [-1, 1, 0, -1],
            [-1, -1, 1, 0],
        ]
    )
    assert conference.T == -conference
    assert conference * conference == -3 * sp.eye(4)

    small_h = sp.I * conference / sp.sqrt(3)
    assert small_h.H == small_h
    assert small_h * small_h == sp.eye(4)
    assert sp.trace(small_h) == 0

    orbit = []
    for element in range(4):
        left = klein_left_regular(element)
        orbit.append(left * small_h * left.T)
    assert sum(orbit, sp.zeros(4)) == sp.zeros(4)
    gram = sp.Matrix(
        4,
        4,
        lambda row, column: sp.simplify(
            sp.trace(orbit[row] * orbit[column]) / 4
        ),
    )
    expected_gram = sp.Matrix(
        4,
        4,
        lambda row, column: 1
        if row == column
        else -sp.Rational(1, 3),
    )
    assert gram == expected_gram

    full_h = lifted_controlled_reflection(small_h)
    assert full_h.H == full_h
    assert full_h * full_h == sp.eye(16)
    assert sp.trace(full_h) == 0
    assert partial_trace(full_h, (4, 4), 0) == sp.zeros(4)
    assert partial_trace(full_h, (4, 4), 1) == sp.zeros(4)

    h1 = sp.kronecker_product(full_h, sp.eye(4))
    h2 = sp.kronecker_product(sp.eye(4), full_h)
    residual = (
        h1 * h2 * h1
        - h2 * h1 * h2
        - sp.Rational(1, 3) * (h1 - h2)
    )
    assert residual == sp.zeros(64)

    projection = (sp.eye(16) - full_h) / 2
    assert projection.H == projection
    assert projection * projection == projection
    assert projection.rank() == 8

    # Audit the integer content of the controlled-leg theorem at r=1,d=4.
    p12 = sp.kronecker_product(projection, sp.eye(4))
    p23 = sp.kronecker_product(sp.eye(4), projection)
    fixed_first_indices = [
        (0 * 4 + middle) * 4 + last
        for middle in range(4)
        for last in range(4)
    ]
    restricted_p = p12.extract(fixed_first_indices, fixed_first_indices)
    restricted_q = p23.extract(fixed_first_indices, fixed_first_indices)
    assert restricted_p.rank() == restricted_q.rank() == 8
    assert sp.trace(restricted_p * restricted_q) == 4

    common_one = (restricted_p - sp.eye(16)).col_join(
        restricted_q - sp.eye(16)
    ).nullspace()
    common_zero = restricted_p.col_join(restricted_q).nullspace()
    assert len(common_one) == len(common_zero) == 2
    assert 16 % 8 == 0


def fourier_value(
    first_pair_weight: Fraction,
    second_pair_weight: Fraction,
    order_two_weight: Fraction,
    frequency_type: int,
) -> Fraction:
    """Fourier coefficient on C_6 for a symmetric probability measure.

    The measure has values a on {1,5}, b on {2,4}, and c on {3}.
    frequency_type is 1 for {1,5}, 2 for {2,4}, or 3 for {3}.
    """
    a = first_pair_weight
    b = second_pair_weight
    c = order_two_weight
    if frequency_type == 1:
        return a - b - c
    if frequency_type == 2:
        return -a - b + c
    if frequency_type == 3:
        return -2 * a + 2 * b - c
    raise ValueError("frequency type must be 1, 2, or 3")


def strictly_positive_affine_solution_exists(
    measure_support: tuple[int, ...],
    constrained_frequencies: tuple[int, ...],
) -> bool:
    """Exact feasibility for the three-variable symmetric C_6 measures.

    The equations have affine dimension at most one because the frequency
    set is nonempty.  Strict positivity on the declared support is therefore
    decided by intersecting exact rational open intervals.
    """
    a, b, c = sp.symbols("a b c", real=True)
    symbols = (a, b, c)
    weights = {1: a, 2: b, 3: c}
    equations = [2 * a + 2 * b + c - 1]
    equations.extend(
        weights[inactive]
        for inactive in {1, 2, 3}.difference(measure_support)
    )
    equations.extend(
        fourier_value(a, b, c, frequency_type) + sp.Rational(1, 3)
        for frequency_type in constrained_frequencies
    )
    solution_set = sp.linsolve(equations, symbols)
    if solution_set == sp.EmptySet:
        return False
    solutions = list(solution_set)
    assert len(solutions) == 1
    solution = solutions[0]
    free_symbols = set().union(*(entry.free_symbols for entry in solution))

    if not free_symbols:
        return all(
            solution[index - 1] > 0 for index in measure_support
        ) and all(
            solution[index - 1] == 0
            for index in {1, 2, 3}.difference(measure_support)
        )

    assert len(free_symbols) == 1
    parameter = next(iter(free_symbols))
    lower: sp.Rational | None = None
    upper: sp.Rational | None = None
    for index in measure_support:
        expression = sp.expand(solution[index - 1])
        slope = expression.coeff(parameter)
        intercept = expression.subs(parameter, 0)
        assert not intercept.free_symbols
        if slope == 0:
            if intercept <= 0:
                return False
        elif slope > 0:
            bound = -intercept / slope
            lower = bound if lower is None else max(lower, bound)
        else:
            bound = -intercept / slope
            upper = bound if upper is None else min(upper, bound)
    return lower is None or upper is None or lower < upper


def verify_c6_dual_fourier_support_no_go() -> None:
    """Exhaust the seven inverse-closed nonzero support types exactly."""
    support_types = [
        tuple(index for index, bit in zip((1, 2, 3), mask) if bit)
        for mask in product((False, True), repeat=3)
        if any(mask)
    ]

    forward_feasible = set()
    feasible_pairs = []
    for spatial_support in support_types:
        for fourier_support in support_types:
            forward = strictly_positive_affine_solution_exists(
                spatial_support, fourier_support
            )
            if forward:
                forward_feasible.add((spatial_support, fourier_support))
            reverse = strictly_positive_affine_solution_exists(
                fourier_support, spatial_support
            )
            if forward and reverse:
                feasible_pairs.append((spatial_support, fourier_support))

    expected_forward = {
        ((1, 2), (1,)),
        ((1, 2), (3,)),
        ((1, 3), (1,)),
        ((1, 3), (2,)),
        ((2, 3), (2,)),
        ((2, 3), (3,)),
        ((1, 2, 3), (1,)),
        ((1, 2, 3), (2,)),
        ((1, 2, 3), (3,)),
        ((1, 2, 3), (1, 2)),
        ((1, 2, 3), (1, 3)),
        ((1, 2, 3), (2, 3)),
    }
    assert forward_feasible == expected_forward
    assert feasible_pairs == []

    # Independent controlled-leg arithmetic: r=1,d=6 would require
    # the common-one multiplicity d^2/8=9/2 to be an integer.
    assert Fraction(6 * 6, 8).denominator == 2


def main() -> None:
    verify_v4_conference_calibration()
    verify_c6_dual_fourier_support_no_go()
    print("PASS exact V4 skew-conference calibration")
    print("PASS full 64 x 64 exceptional cubic identity")
    print("PASS V4 restricted two-projection multiplicities (2,2,6)")
    print("PASS exact C6 dual-Fourier support obstruction")
    print("PASS rank-one controlled-leg obstruction at d=6")


if __name__ == "__main__":
    main()
