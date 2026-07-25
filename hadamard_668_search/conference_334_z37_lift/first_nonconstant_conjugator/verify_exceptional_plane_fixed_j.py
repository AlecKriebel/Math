#!/usr/bin/env python3
"""Close the exceptional first-nonconstant nondegenerate-plane pencil.

The symmetry-reduced diagonal function code for

    K=z*(P+S)+z^2*B

has one quotient-compatible parameter type:

    alpha=19, beta=20,
    S^2=alpha*P, B^2=beta*P, SB+BS=0.

This verifier restores the fixed matrix J in the z^18 trace term while
still allowing the N0 coefficients to vary arbitrarily.  The ordinary
function space F and z^18*F are in direct sum.  Hence each candidate
binary word has a uniquely determined z^18*F component.

For one coordinate put p=(P*1)_i, s=(S*1)_i, b=(B*1)_i.  The ten J
coefficients are

    1,p,s,b,p^2,p*s,b*p,s^2,b*s,-b^2.

An exhaustive 37^3 local census for each trace orientation proves that
none of the four exceptional binary words has the required component.
This is a safe local obstruction: all global projector and N0 relations
remain relaxed.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROMOTED = HERE.parent
P = 37


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


R = load_module(
    "rank_two_code_base",
    PROMOTED / "verify_rank_two_conjugation_obstruction.py",
)
Y = load_module("z37_yadic_base", HERE / "verify_z37_yadic_frontier.py")

WORDS = (
    "010011010000111011110111000010110010",  # weight 18
    "011101011100101111111101001110101110",  # weight 24
    "100010100011010000000010110001010001",  # weight 12
    "101100101111000100001000111101001101",  # weight 18
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def subtract(left, right):
    return [(first - second) % P for first, second in zip(left, right)]


def coefficient_functions(alpha: int, beta: int):
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
        subtract(
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
    multiply = R.polynomial_multiply
    add = R.polynomial_add
    a = subtract(multiply(x, hyperbolic_c), R.ONE)
    a_prime = subtract(multiply(x_inverse, hyperbolic_c), R.ONE)
    b = multiply(x, multiply(z, hyperbolic_s))
    b_prime = R.polynomial_scale(
        multiply(x_inverse, multiply(z, hyperbolic_s)), -1
    )
    c = multiply(x, multiply(z2, hyperbolic_s))
    c_prime = R.polynomial_scale(
        multiply(x_inverse, multiply(z2, hyperbolic_s)), -1
    )
    return [
        R.ONE,
        add(a, a_prime),
        add(b, b_prime),
        subtract(c_prime, c),
        multiply(a_prime, a),
        add(multiply(a_prime, b), multiply(b_prime, a)),
        subtract(multiply(c_prime, a), multiply(a_prime, c)),
        multiply(b_prime, b),
        subtract(multiply(c_prime, b), multiply(b_prime, c)),
        multiply(c_prime, c),
    ]


def main() -> None:
    # Independent concrete check of the ten factored J coefficients,
    # including the two signs involving the skew matrix.
    projector = [[0, 0, 0], [0, 1, 0], [0, 0, 1]]
    symmetric = [[0, 0, 0], [0, 2, 3], [0, 3, -2 % P]]
    skew = [[0, 0, 0], [0, 0, 4], [0, -4 % P, 0]]
    ones = [[1] * 3 for _ in range(3)]
    multiply_numeric = R.numeric_matrix_multiply
    coefficient_matrices = [
        ones,
        multiply_numeric(projector, ones),
        multiply_numeric(symmetric, ones),
        multiply_numeric(skew, ones),
        multiply_numeric(multiply_numeric(projector, ones), projector),
        multiply_numeric(multiply_numeric(projector, ones), symmetric),
        multiply_numeric(multiply_numeric(skew, ones), projector),
        multiply_numeric(multiply_numeric(symmetric, ones), symmetric),
        multiply_numeric(multiply_numeric(skew, ones), symmetric),
        multiply_numeric(multiply_numeric(skew, ones), skew),
    ]
    p_vector = [sum(row) % P for row in projector]
    s_vector = [sum(row) % P for row in symmetric]
    b_vector = [sum(row) % P for row in skew]
    for coordinate in range(3):
        p_value = p_vector[coordinate]
        s_value = s_vector[coordinate]
        b_value = b_vector[coordinate]
        expected = (
            1,
            p_value,
            s_value,
            b_value,
            p_value * p_value % P,
            p_value * s_value % P,
            b_value * p_value % P,
            s_value * s_value % P,
            b_value * s_value % P,
            -b_value * b_value % P,
        )
        require(
            tuple(matrix[coordinate][coordinate] % P
                  for matrix in coefficient_matrices)
            == expected,
            "factored J coefficient identity changed",
        )

    functions = coefficient_functions(19, 20)
    ordinary = [R.y_to_x_coefficients(value) for value in functions]
    half = [
        R.y_to_x_coefficients(
            R.polynomial_multiply(R.HALF_POWER, value)
        )
        for value in functions
    ]
    ordinary_basis, ordinary_pivots = R.reduced_row_basis(ordinary)
    half_basis, half_pivots = R.reduced_row_basis(half)
    combined = ordinary_basis + half_basis
    combined_matrix = [list(row) for row in zip(*combined)]
    require(len(ordinary_basis) == 7, "ordinary function rank changed")
    require(len(half_basis) == 7, "half function rank changed")
    require(
        Y.rank(combined_matrix) == 14,
        "F and z^18*F stopped being a direct sum",
    )

    target_half_components = []
    target_half_information = []
    for bits in WORDS:
        target = [0] + [18 + int(bit) for bit in bits]
        solution = Y.solve_linear(combined_matrix, target)
        require(solution is not None, "an exceptional word left F+hF")
        require(len(solution) == 14, "combined coordinate size changed")
        component = [0] * P
        for coefficient, row in zip(solution[7:], half_basis):
            for coordinate in range(P):
                component[coordinate] = (
                    component[coordinate] + coefficient * row[coordinate]
                ) % P
        target_half_components.append(component)
        target_half_information.append(
            tuple(component[pivot] for pivot in half_pivots)
        )

    require(len(set(target_half_information)) == 4,
            "exceptional half components collided")

    # At information coordinates, the actual J contribution is a quadratic
    # map of the completely relaxed local triple (p,s,b).
    generator_information = [
        tuple(row[pivot] for pivot in half_pivots)
        for row in half
    ]
    survivor_counts: dict[int, list[int]] = {}
    examples: dict[int, list[tuple[int, int, int] | None]] = {}
    for eta in (1, -1):
        counts = [0] * len(WORDS)
        witnesses: list[tuple[int, int, int] | None] = [None] * len(WORDS)
        for p_value in range(P):
            for s_value in range(P):
                for b_value in range(P):
                    coefficients = (
                        1,
                        p_value,
                        s_value,
                        b_value,
                        p_value * p_value % P,
                        p_value * s_value % P,
                        b_value * p_value % P,
                        s_value * s_value % P,
                        b_value * s_value % P,
                        -b_value * b_value % P,
                    )
                    information = tuple(
                        sum(
                            eta * coefficient * generator[index]
                            for coefficient, generator
                            in zip(coefficients, generator_information)
                        )
                        % P
                        for index in range(len(half_pivots))
                    )
                    for word_index, target in enumerate(
                        target_half_information
                    ):
                        if information == target:
                            counts[word_index] += 1
                            if witnesses[word_index] is None:
                                witnesses[word_index] = (
                                    p_value, s_value, b_value
                                )
        survivor_counts[eta] = counts
        examples[eta] = witnesses

    require(
        survivor_counts == {1: [0, 0, 0, 0], -1: [0, 0, 0, 0]},
        "an exceptional local J profile survived",
    )
    require(
        all(witness is None
            for orientation in examples.values()
            for witness in orientation),
        "a witness was recorded despite zero counts",
    )

    print("exceptional_parameter_alpha=19")
    print("exceptional_parameter_beta=20")
    print(f"ordinary_function_rank={len(ordinary_basis)}")
    print(f"half_function_rank={len(half_basis)}")
    print("combined_function_rank=14")
    print("local_triples_checked_per_orientation=50653")
    for bits, information in zip(WORDS, target_half_information):
        print(
            f"word_weight={bits.count('1')} "
            "required_half_information="
            + ",".join(map(str, information))
        )
    print("eta_plus_survivors=0,0,0,0")
    print("eta_minus_survivors=0,0,0,0")
    print("common_nondegenerate_plane_pencil=IMPOSSIBLE")
    print("certificate=PASS")


if __name__ == "__main__":
    main()
