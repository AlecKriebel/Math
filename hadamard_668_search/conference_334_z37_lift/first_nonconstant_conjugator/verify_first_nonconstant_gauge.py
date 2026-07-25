#!/usr/bin/env python3
"""Verify the first genuinely nonconstant unitary-conjugator layer.

Put z=log(1+y).  Every near-identity unitary conjugator has a unique
logarithm

    K(z)=z*A0+z^2*A1+...

with A0 symmetric and A1 skew-symmetric.  This script verifies the exact
20+20 low-layer normal-form dimensions for the certified quotient and
excludes the pure rank-two first-higher family K=z^2*A1 by a safe diagonal
function over-code.

The over-code forgets N0, J, and coordinate coupling.  Consequently its
failure is an obstruction, while a survivor would not be a binary lift.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Callable, Sequence


HERE = Path(__file__).resolve().parent
PROMOTED = HERE.parent


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


Y = load_module("z37_yadic_base", HERE / "verify_z37_yadic_frontier.py")
R = load_module(
    "rank_two_code_base",
    PROMOTED / "verify_rank_two_conjugation_obstruction.py",
)

P = 37
require = R.require


def polynomial_subtract(left, right):
    return [(first - second) % P for first, second in zip(left, right)]


def commutator(left, right):
    return Y.add(
        Y.multiply(left, right),
        Y.scale(-1, Y.multiply(right, left)),
    )


def anticommutator(left, right):
    return Y.add(Y.multiply(left, right), Y.multiply(right, left))


def map_matrix(
    source_basis,
    operation: Callable,
    flatten: Callable,
):
    columns = [flatten(operation(source)) for source in source_basis]
    return [list(row) for row in zip(*columns)], columns


def independent_source_columns(columns: Sequence[Sequence[int]]) -> list[int]:
    chosen: list[list[int]] = []
    result: list[int] = []
    current_rank = 0
    for index, column in enumerate(columns):
        candidate = chosen + [list(column)]
        matrix = [list(row) for row in zip(*candidate)]
        new_rank = Y.rank(matrix)
        if new_rank > current_rank:
            chosen.append(list(column))
            result.append(index)
            current_rank = new_rank
    return result


def basis_labels(kind: str) -> list[tuple[int, int]]:
    return [
        (i, j)
        for i in range(9)
        for j in range(i if kind == "symmetric" else i + 1, 9)
    ]


def verify_low_layer_normal_form() -> dict[str, object]:
    (
        n0,
        _,
        _,
        _,
        _,
    ) = Y.verify_quotient_and_first_layer()
    symmetric = Y.symmetric_basis()
    skew = Y.skew_basis()

    sym_ad, sym_ad_columns = map_matrix(
        symmetric,
        lambda value: commutator(n0, value),
        Y.flatten_skew,
    )
    skew_ad, skew_ad_columns = map_matrix(
        skew,
        lambda value: commutator(n0, value),
        Y.flatten_symmetric,
    )
    require(Y.rank(sym_ad) == 20, "symmetric adjoint rank changed")
    require(Y.rank(skew_ad) == 20, "skew adjoint rank changed")

    first_tangent, _ = map_matrix(
        skew,
        lambda value: anticommutator(n0, value),
        Y.flatten_skew,
    )
    second_tangent, _ = map_matrix(
        symmetric,
        lambda value: anticommutator(n0, value),
        Y.flatten_symmetric,
    )
    require(Y.rank(first_tangent) == 16, "first tangent rank changed")
    require(Y.rank(second_tangent) == 24, "second tangent rank changed")

    # Every first-order skew solution {N0,X}=0 is [N0,A0].
    for source in symmetric:
        image = commutator(n0, source)
        require(
            anticommutator(n0, image) == Y.zero_matrix(),
            "a first commutator left the square-zero tangent",
        )
    require(
        len(skew) - Y.rank(first_tangent) == Y.rank(sym_ad) == 20,
        "first tangent and orbit dimensions disagree",
    )

    # At second order, [N0,A1] is exactly the trace-zero part of the
    # 21-dimensional symmetric homogeneous tangent.
    trace_row = [
        sum(source[i][i] for i in range(9)) % P
        for source in symmetric
    ]
    trace_zero_second_constraints = second_tangent + [trace_row]
    require(
        Y.rank(trace_zero_second_constraints) == 25,
        "trace did not cut the second tangent by one",
    )
    for source in skew:
        image = commutator(n0, source)
        require(
            anticommutator(n0, image) == Y.zero_matrix(),
            "a second commutator left the square-zero tangent",
        )
        require(
            sum(image[i][i] for i in range(9)) % P == 0,
            "a commutator acquired nonzero trace",
        )
    require(
        len(symmetric) - Y.rank(trace_zero_second_constraints)
        == Y.rank(skew_ad)
        == 20,
        "second trace-zero tangent and orbit dimensions disagree",
    )

    diagonal_map = [
        [commutator(n0, source)[i][i] for source in skew]
        for i in range(9)
    ]
    require(Y.rank(diagonal_map) == 8, "second diagonal freedom changed")
    require(
        all(sum(row) % P == 0 for row in zip(*diagonal_map)),
        "second diagonal image is not trace zero",
    )

    symmetric_complement = independent_source_columns(sym_ad_columns)
    skew_complement = independent_source_columns(skew_ad_columns)
    require(
        len(symmetric_complement) == len(skew_complement) == 20,
        "normal-form complement dimensions changed",
    )

    # The order-z^2 BCH gauge law.  If H=exp(z*C+z^2*D) is multiplied on
    # the left, then
    #
    #   A0 -> A0+C,
    #   A1 -> A1+D+1/2[C,A0].
    #
    # Symmetric C,A0 make the correction skew, as required.
    c = symmetric[1]
    a0 = symmetric[10]
    d = skew[2]
    a1 = skew[9]
    correction = Y.scale(pow(2, -1, P), commutator(c, a0))
    transformed_a1 = Y.add(Y.add(a1, d), correction)
    require(
        Y.transpose(transformed_a1)
        == Y.scale(-1, transformed_a1),
        "BCH second coefficient lost skew parity",
    )

    return {
        "symmetric_adjoint_rank": Y.rank(sym_ad),
        "symmetric_adjoint_kernel_dimension": len(symmetric) - Y.rank(sym_ad),
        "skew_adjoint_rank": Y.rank(skew_ad),
        "skew_adjoint_kernel_dimension": len(skew) - Y.rank(skew_ad),
        "first_tangent_dimension": len(skew) - Y.rank(first_tangent),
        "second_homogeneous_tangent_dimension": (
            len(symmetric) - Y.rank(second_tangent)
        ),
        "second_trace_zero_tangent_dimension": (
            len(symmetric) - Y.rank(trace_zero_second_constraints)
        ),
        "second_diagonal_freedom_rank": Y.rank(diagonal_map),
        "symmetric_normal_form_entries": [
            basis_labels("symmetric")[index]
            for index in symmetric_complement
        ],
        "skew_normal_form_entries": [
            basis_labels("skew")[index] for index in skew_complement
        ],
    }


def exponential_with_squared_parameter(
    matrix: Sequence[Sequence[int]], sign: int
):
    """Return exp(sign*z^2*matrix) with polynomial entries."""

    order = len(matrix)
    result = [
        [[0] * P for _ in range(order)]
        for _ in range(order)
    ]
    for i in range(order):
        result[i][i] = R.ONE[:]
    matrix_power = [
        [int(i == j) for j in range(order)]
        for i in range(order)
    ]
    signed = [
        [sign * entry % P for entry in row]
        for row in matrix
    ]
    z_squared = R.polynomial_multiply(R.LOGARITHM, R.LOGARITHM)
    parameter_power = R.ONE[:]
    factorial = 1
    for degree in range(1, P):
        matrix_power = R.numeric_matrix_multiply(matrix_power, signed)
        parameter_power = R.polynomial_multiply(
            parameter_power, z_squared
        )
        factorial = factorial * degree % P
        inverse_factorial = pow(factorial, -1, P)
        for i in range(order):
            for j in range(order):
                coefficient = (
                    matrix_power[i][j] * inverse_factorial
                ) % P
                if coefficient:
                    result[i][j] = R.polynomial_add(
                        result[i][j],
                        R.polynomial_scale(parameter_power, coefficient),
                    )
    return result


def pure_higher_diagonal_code(matrix: Sequence[Sequence[int]]):
    negative = exponential_with_squared_parameter(matrix, -1)
    positive = exponential_with_squared_parameter(matrix, 1)
    negative_entries = [entry for row in negative for entry in row]
    positive_entries = [entry for row in positive for entry in row]
    generators = []
    for left in negative_entries:
        for right in positive_entries:
            value = R.polynomial_multiply(left, right)
            generators.append(R.y_to_x_coefficients(value))
            generators.append(
                R.y_to_x_coefficients(
                    R.polynomial_multiply(R.HALF_POWER, value)
                )
            )
    return R.reduced_row_basis(generators)


def matrix_power(matrix, exponent: int):
    result = [
        [int(i == j) for j in range(len(matrix))]
        for i in range(len(matrix))
    ]
    for _ in range(exponent):
        result = R.numeric_matrix_multiply(result, matrix)
    return result


def matrix_rank(matrix) -> int:
    return Y.rank([list(row) for row in matrix])


def verify_pure_rank_two_higher_family() -> list[dict[str, object]]:
    representatives = [
        (
            "split_semisimple",
            [[0, 0, 0], [0, 1, 0], [0, 0, -1 % P]],
            "B^3=B",
        ),
        (
            "irreducible_semisimple",
            R.companion_matrix(0, 2),
            "B^3=-2B",
        ),
        (
            "J3_zero",
            [[0, 1, 0], [0, 0, 1], [0, 0, 0]],
            "B^3=0,B^2!=0",
        ),
        (
            "J2_plus_J2_zero",
            [
                [0, 1, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 1],
                [0, 0, 0, 0],
            ],
            "B^2=0",
        ),
    ]
    residue_word = tuple(
        int(R.quadratic_character(value) == 1)
        for value in range(1, P)
    )
    paley_pair = {
        residue_word,
        tuple(1 - bit for bit in residue_word),
    }
    records = []
    for name, matrix, identity in representatives:
        require(matrix_rank(matrix) == 2, f"{name} lost rank two")
        square = matrix_power(matrix, 2)
        cube = matrix_power(matrix, 3)
        if name == "split_semisimple":
            require(cube == matrix, "split cubic identity changed")
        elif name == "irreducible_semisimple":
            require(
                cube
                == [[(-2 * entry) % P for entry in row] for row in matrix],
                "irreducible cubic identity changed",
            )
        elif name == "J3_zero":
            require(
                any(entry for row in square for entry in row)
                and not any(entry for row in cube for entry in row),
                "J3 nilpotent identity changed",
            )
        else:
            require(
                not any(entry for row in square for entry in row),
                "J2+J2 square changed",
            )

        basis, pivots = pure_higher_diagonal_code(matrix)
        words = R.compatible_binary_words(basis, pivots)
        require(set(words) == paley_pair, f"{name} gained a binary word")
        records.append(
            {
                "type": name,
                "rational_identity": identity,
                "overcode_dimension": len(basis),
                "compatible_word_count": len(words),
                "compatible_weights": sorted({sum(word) for word in words}),
                "paley_pair_only": True,
            }
        )
    return records


def polynomial_matrix_multiply(left, right):
    rows = len(left)
    middle = len(right)
    columns = len(right[0])
    result = [
        [[0] * P for _ in range(columns)]
        for _ in range(rows)
    ]
    for i in range(rows):
        for k in range(middle):
            for j in range(columns):
                result[i][j] = R.polynomial_add(
                    result[i][j],
                    R.polynomial_multiply(left[i][k], right[k][j]),
                )
    return result


def constant_polynomial_matrix(matrix):
    return [
        [[entry % P] + [0] * (P - 1) for entry in row]
        for row in matrix
    ]


def polynomial_matrix_exponential(matrix, sign: int):
    order = len(matrix)
    identity = [
        [R.ONE[:] if i == j else R.ZERO[:] for j in range(order)]
        for i in range(order)
    ]
    signed = [
        [R.polynomial_scale(entry, sign) for entry in row]
        for row in matrix
    ]
    result = [[entry[:] for entry in row] for row in identity]
    power_matrix = identity
    factorial = 1
    for degree in range(1, P):
        power_matrix = polynomial_matrix_multiply(power_matrix, signed)
        factorial = factorial * degree % P
        inverse_factorial = pow(factorial, -1, P)
        for i in range(order):
            for j in range(order):
                result[i][j] = R.polynomial_add(
                    result[i][j],
                    R.polynomial_scale(
                        power_matrix[i][j], inverse_factorial
                    ),
                )
    return result


def verify_symmetric_diagonal_function_reduction() -> None:
    """Independently check all signs in the ten-function reduction."""

    order = 3
    identity = [
        [int(i == j) for j in range(order)]
        for i in range(order)
    ]
    projector = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ]
    symmetric_part = [
        [0, 0, 0],
        [0, 2, 3],
        [0, 3, -2 % P],
    ]
    skew_part = [
        [0, 0, 0],
        [0, 0, 4],
        [0, -4 % P, 0],
    ]
    test_matrix = [
        [1, 2, 3],
        [2, 4, 5],
        [3, 5, 6],
    ]
    alpha = (2 * 2 + 3 * 3) % P
    beta = (-4 * 4) % P

    z = R.LOGARITHM
    z2 = R.polynomial_multiply(z, z)
    z4 = R.polynomial_multiply(z2, z2)
    delta = R.polynomial_add(
        R.polynomial_scale(z2, alpha),
        R.polynomial_scale(z4, beta),
    )
    hyperbolic_c = R.ZERO[:]
    hyperbolic_s = R.ZERO[:]
    delta_power = R.ONE[:]
    even_factorial = 1
    for n in range(19):
        if n:
            even_factorial = (
                even_factorial * (2 * n - 1) * (2 * n)
            ) % P
        hyperbolic_c = R.polynomial_add(
            hyperbolic_c,
            R.polynomial_scale(
                delta_power, pow(even_factorial, -1, P)
            ),
        )
        if 2 * n + 1 < P:
            odd_factorial = even_factorial * (2 * n + 1) % P
            hyperbolic_s = R.polynomial_add(
                hyperbolic_s,
                R.polynomial_scale(
                    delta_power, pow(odd_factorial, -1, P)
                ),
            )
        delta_power = R.polynomial_multiply(delta_power, delta)
    require(
        polynomial_subtract(
            R.polynomial_multiply(hyperbolic_c, hyperbolic_c),
            R.polynomial_multiply(
                delta,
                R.polynomial_multiply(hyperbolic_s, hyperbolic_s),
            ),
        )
        == R.ONE,
        "hyperbolic identity changed",
    )

    x = [1, 1] + [0] * (P - 2)
    x_inverse = R.polynomial_power(x, P - 1)
    a = polynomial_subtract(
        R.polynomial_multiply(x, hyperbolic_c), R.ONE
    )
    a_prime = polynomial_subtract(
        R.polynomial_multiply(x_inverse, hyperbolic_c), R.ONE
    )
    b = R.polynomial_multiply(
        x, R.polynomial_multiply(z, hyperbolic_s)
    )
    b_prime = R.polynomial_scale(
        R.polynomial_multiply(
            x_inverse, R.polynomial_multiply(z, hyperbolic_s)
        ),
        -1,
    )
    c = R.polynomial_multiply(
        x, R.polynomial_multiply(z2, hyperbolic_s)
    )
    c_prime = R.polynomial_scale(
        R.polynomial_multiply(
            x_inverse, R.polynomial_multiply(z2, hyperbolic_s)
        ),
        -1,
    )

    def closed_exponential(ap, bp, cp):
        result = constant_polynomial_matrix(identity)
        for scalar, matrix in (
            (ap, projector),
            (bp, symmetric_part),
            (cp, skew_part),
        ):
            for i in range(order):
                for j in range(order):
                    if matrix[i][j]:
                        result[i][j] = R.polynomial_add(
                            result[i][j],
                            R.polynomial_scale(scalar, matrix[i][j]),
                        )
        return result

    closed_positive = closed_exponential(a, b, c)
    closed_negative = closed_exponential(a_prime, b_prime, c_prime)

    logarithm_matrix = [
        [
            R.polynomial_add(
                R.polynomial_scale(
                    z, (projector[i][j] + symmetric_part[i][j]) % P
                ),
                R.polynomial_scale(z2, skew_part[i][j]),
            )
            for j in range(order)
        ]
        for i in range(order)
    ]
    require(
        polynomial_matrix_exponential(logarithm_matrix, 1)
        == closed_positive,
        "closed positive exponential changed",
    )
    require(
        polynomial_matrix_exponential(logarithm_matrix, -1)
        == closed_negative,
        "closed negative exponential changed",
    )

    direct = polynomial_matrix_multiply(
        polynomial_matrix_multiply(
            closed_negative, constant_polynomial_matrix(test_matrix)
        ),
        closed_positive,
    )

    multiply_numeric = R.numeric_matrix_multiply
    coefficient_matrices = [
        test_matrix,
        multiply_numeric(projector, test_matrix),
        multiply_numeric(symmetric_part, test_matrix),
        multiply_numeric(skew_part, test_matrix),
        multiply_numeric(
            multiply_numeric(projector, test_matrix), projector
        ),
        multiply_numeric(
            multiply_numeric(projector, test_matrix), symmetric_part
        ),
        multiply_numeric(
            multiply_numeric(skew_part, test_matrix), projector
        ),
        multiply_numeric(
            multiply_numeric(symmetric_part, test_matrix), symmetric_part
        ),
        multiply_numeric(
            multiply_numeric(skew_part, test_matrix), symmetric_part
        ),
        multiply_numeric(
            multiply_numeric(skew_part, test_matrix), skew_part
        ),
    ]
    functions = [
        R.ONE,
        R.polynomial_add(a, a_prime),
        R.polynomial_add(b, b_prime),
        polynomial_subtract(c_prime, c),
        R.polynomial_multiply(a_prime, a),
        R.polynomial_add(
            R.polynomial_multiply(a_prime, b),
            R.polynomial_multiply(b_prime, a),
        ),
        polynomial_subtract(
            R.polynomial_multiply(c_prime, a),
            R.polynomial_multiply(a_prime, c),
        ),
        R.polynomial_multiply(b_prime, b),
        polynomial_subtract(
            R.polynomial_multiply(c_prime, b),
            R.polynomial_multiply(b_prime, c),
        ),
        R.polynomial_multiply(c_prime, c),
    ]
    predicted_diagonal = [R.ZERO[:] for _ in range(order)]
    for function, matrix in zip(functions, coefficient_matrices):
        for i in range(order):
            predicted_diagonal[i] = R.polynomial_add(
                predicted_diagonal[i],
                R.polynomial_scale(function, matrix[i][i]),
            )
    require(
        predicted_diagonal == [direct[i][i] for i in range(order)],
        "ten-function diagonal expansion changed",
    )


def main() -> None:
    low = verify_low_layer_normal_form()
    pure = verify_pure_rank_two_higher_family()
    verify_symmetric_diagonal_function_reduction()

    print("unitary_logarithm_parity=A0_symmetric,A1_skew")
    print(f"first_layer_effective_parameters={low['first_tangent_dimension']}")
    print(
        "second_layer_effective_parameters="
        f"{low['second_trace_zero_tangent_dimension']}"
    )
    print(
        "second_homogeneous_tangent_dimension="
        f"{low['second_homogeneous_tangent_dimension']}"
    )
    print(
        "second_diagonal_freedom_rank="
        f"{low['second_diagonal_freedom_rank']}"
    )
    print(
        "normal_form_parameter_count_through_z2="
        f"{low['first_tangent_dimension'] + low['second_trace_zero_tangent_dimension']}"
    )
    print(
        "symmetric_normal_form_entries="
        + ",".join(f"{i}:{j}" for i, j in low["symmetric_normal_form_entries"])
    )
    print(
        "skew_normal_form_entries="
        + ",".join(f"{i}:{j}" for i, j in low["skew_normal_form_entries"])
    )
    for record in pure:
        print(
            "pure_rank2_type="
            f"{record['type']} dimension={record['overcode_dimension']} "
            f"words={record['compatible_word_count']} "
            f"weights={record['compatible_weights']}"
        )
    print("pure_rank2_first_higher_family=IMPOSSIBLE")
    print("symmetric_ten_function_reduction=VERIFIED")
    print("certificate=PASS")


if __name__ == "__main__":
    main()
