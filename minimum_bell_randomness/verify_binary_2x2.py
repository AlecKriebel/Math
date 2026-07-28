#!/usr/bin/env python3
"""Independent finite verification of the exact binary 2x2 construction.

The all-dimensional upper bound and Eve-decoupling statement are analytic.
This script independently checks:

* the formal coefficients in the SOS identity;
* the ideal two-qubit observables and their order-two relations;
* the exact target probabilities;
* numerical saturation of both the Bell operator and every SOS factor.

Only the Python standard library is used.
"""

from __future__ import annotations

from fractions import Fraction
import math


Scalar = tuple[Fraction, Fraction]
Matrix = list[list[complex]]
Vector = list[complex]


def scalar_add(left: Scalar, right: Scalar) -> Scalar:
    return left[0] + right[0], left[1] + right[1]


def scalar_mul(left: Scalar, right: Scalar) -> Scalar:
    # (a+b sqrt(3))(c+d sqrt(3))
    return (
        left[0] * right[0] + 3 * left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def add_coefficient(
    coefficients: dict[str, Scalar], word: str, value: Scalar
) -> None:
    coefficients[word] = scalar_add(
        coefficients.get(word, (Fraction(0), Fraction(0))),
        value,
    )


def expand_square(
    terms: list[tuple[str, Scalar]], prefactor: Scalar
) -> dict[str, Scalar]:
    """Expand one formal square using only A_x^2=B_y^2=I.

    Alice and Bob letters commute across wings. Bob letters are not commuted
    past one another, which exposes the cancellation of B0B1 and B1B0.
    """
    result: dict[str, Scalar] = {}
    for left_word, left_value in terms:
        for right_word, right_value in terms:
            value = scalar_mul(
                prefactor, scalar_mul(left_value, right_value)
            )
            if left_word == right_word:
                word = "I"
            elif left_word.startswith("A") and right_word.startswith("B"):
                word = left_word + right_word
            elif left_word.startswith("B") and right_word.startswith("A"):
                word = right_word + left_word
            else:
                word = left_word + right_word
            add_coefficient(result, word, value)
    return result


def verify_formal_sos() -> None:
    zero: Scalar = (Fraction(0), Fraction(0))
    one: Scalar = (Fraction(1), Fraction(0))
    sqrt3: Scalar = (Fraction(0), Fraction(1))
    inv_sqrt3: Scalar = (Fraction(0), Fraction(1, 3))

    first = expand_square(
        [
            ("A0", sqrt3),
            ("B0", (Fraction(-1), Fraction(0))),
            ("B1", (Fraction(2), Fraction(0))),
        ],
        scalar_mul((Fraction(1, 2), Fraction(0)), inv_sqrt3),
    )
    second = expand_square(
        [
            ("A1", sqrt3),
            ("B0", (Fraction(-1), Fraction(0))),
            ("B1", (Fraction(-1), Fraction(0))),
        ],
        inv_sqrt3,
    )
    combined = dict(first)
    for word, value in second.items():
        add_coefficient(combined, word, value)

    expected: dict[str, Scalar] = {
        "I": (Fraction(0), Fraction(3)),
        "A0B0": (Fraction(-1), Fraction(0)),
        "A0B1": (Fraction(2), Fraction(0)),
        "A1B0": (Fraction(-2), Fraction(0)),
        "A1B1": (Fraction(-2), Fraction(0)),
        "B0B1": zero,
        "B1B0": zero,
    }
    assert set(combined) == set(expected)
    assert combined == expected
    assert one != zero


def matrix_add(*matrices: Matrix) -> Matrix:
    return [
        [sum(matrix[j][k] for matrix in matrices) for k in range(len(matrices[0]))]
        for j in range(len(matrices[0]))
    ]


def matrix_scale(value: complex, matrix: Matrix) -> Matrix:
    return [[value * entry for entry in row] for row in matrix]


def matrix_mul(left: Matrix, right: Matrix) -> Matrix:
    return [
        [
            sum(left[j][r] * right[r][k] for r in range(len(right)))
            for k in range(len(right[0]))
        ]
        for j in range(len(left))
    ]


def kron(left: Matrix, right: Matrix) -> Matrix:
    return [
        [
            left[j // len(right)][k // len(right[0])]
            * right[j % len(right)][k % len(right[0])]
            for k in range(len(left[0]) * len(right[0]))
        ]
        for j in range(len(left) * len(right))
    ]


def apply(matrix: Matrix, vector: Vector) -> Vector:
    return [
        sum(matrix[j][k] * vector[k] for k in range(len(vector)))
        for j in range(len(matrix))
    ]


def inner(left: Vector, right: Vector) -> complex:
    return sum(left[j].conjugate() * right[j] for j in range(len(left)))


def norm(vector: Vector) -> float:
    return math.sqrt(max(0.0, inner(vector, vector).real))


def identity(dimension: int) -> Matrix:
    return [
        [complex(j == k) for k in range(dimension)]
        for j in range(dimension)
    ]


def matrix_error(left: Matrix, right: Matrix) -> float:
    return max(
        abs(left[j][k] - right[j][k])
        for j in range(len(left))
        for k in range(len(left[0]))
    )


def verify_ideal_strategy() -> None:
    identity2 = identity(2)
    x = [[0j, 1 + 0j], [1 + 0j, 0j]]
    z = [[1 + 0j, 0j], [0j, -1 + 0j]]
    a0 = z
    a1 = matrix_add(
        matrix_scale(-0.5, z),
        matrix_scale(math.sqrt(3) / 2, x),
    )
    b0 = x
    b1 = matrix_add(
        matrix_scale(-math.sqrt(3) / 2, z),
        matrix_scale(0.5, x),
    )
    observables = (a0, a1, b0, b1)
    for observable in observables:
        assert matrix_error(
            matrix_mul(observable, observable), identity2
        ) < 2e-15

    phi = [1 / math.sqrt(2), 0j, 0j, 1 / math.sqrt(2)]
    bell = matrix_add(
        kron(a0, b0),
        matrix_scale(-2, kron(a0, b1)),
        matrix_scale(2, kron(a1, b0)),
        matrix_scale(2, kron(a1, b1)),
    )
    score = inner(phi, apply(bell, phi)).real
    assert abs(score - 3 * math.sqrt(3)) < 2e-14

    first_factor = matrix_add(
        matrix_scale(math.sqrt(3), kron(a0, identity2)),
        matrix_scale(-1, kron(identity2, b0)),
        matrix_scale(2, kron(identity2, b1)),
    )
    second_factor = matrix_add(
        matrix_scale(math.sqrt(3), kron(a1, identity2)),
        matrix_scale(-1, kron(identity2, b0)),
        matrix_scale(-1, kron(identity2, b1)),
    )
    assert norm(apply(first_factor, phi)) < 2e-15
    assert norm(apply(second_factor, phi)) < 2e-15

    probabilities: list[float] = []
    for a in range(2):
        projector_a = matrix_scale(
            0.5,
            matrix_add(
                identity2,
                matrix_scale((-1) ** a, a0),
            ),
        )
        for b in range(2):
            projector_b = matrix_scale(
                0.5,
                matrix_add(
                    identity2,
                    matrix_scale((-1) ** b, b0),
                ),
            )
            projected = apply(kron(projector_a, projector_b), phi)
            probabilities.append(norm(projected) ** 2)
    assert max(abs(value - 0.25) for value in probabilities) < 2e-15
    assert abs(sum(probabilities) - 1) < 2e-15


def main() -> None:
    verify_formal_sos()
    verify_ideal_strategy()
    print("PASS: formal SOS coefficients verified exactly.")
    print("PASS: ideal 2x2 strategy attains 3*sqrt(3).")
    print("PASS: target probabilities are exactly 1/4 (numerical matrix check).")


if __name__ == "__main__":
    main()
