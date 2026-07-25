#!/usr/bin/env python3
"""Dependency-free hostile reconstruction over a large finite field.

This is intentionally independent of both supplied CAS implementations.
It checks the E8 polarization/orientation, cubic-normal kernels in all
three rows, a mixed horizontal/vertical fixed-divisor degeneration, and
the finite/infinite horizontal-valuation ledger.
"""

from __future__ import annotations

if not __debug__:
    raise RuntimeError("audit requires assertions; do not use -O")

from collections.abc import Iterable


MODULUS = 1_000_003
Exponent = tuple[int, int, int]
Polynomial = dict[Exponent, int]


def normalize(polynomial: Polynomial) -> Polynomial:
    return {
        exponent: coefficient % MODULUS
        for exponent, coefficient in polynomial.items()
        if coefficient % MODULUS
    }


def add(left: Polynomial, right: Polynomial, scale: int = 1) -> Polynomial:
    answer = dict(left)
    for exponent, coefficient in right.items():
        answer[exponent] = (
            answer.get(exponent, 0) + scale * coefficient
        ) % MODULUS
    return normalize(answer)


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for first, first_coefficient in left.items():
        for second, second_coefficient in right.items():
            exponent = tuple(first[index] + second[index] for index in range(3))
            answer[exponent] = (
                answer.get(exponent, 0)
                + first_coefficient * second_coefficient
            ) % MODULUS
    return normalize(answer)


def power(polynomial: Polynomial, exponent: int) -> Polynomial:
    answer: Polynomial = {(0, 0, 0): 1}
    base = polynomial
    current = exponent
    while current:
        if current & 1:
            answer = multiply(answer, base)
        base = multiply(base, base)
        current //= 2
    return answer


def derivative(polynomial: Polynomial, variable: int) -> Polynomial:
    answer: Polynomial = {}
    for exponent, coefficient in polynomial.items():
        if exponent[variable] == 0:
            continue
        new_exponent = list(exponent)
        new_exponent[variable] -= 1
        answer[tuple(new_exponent)] = (
            coefficient * exponent[variable]
        ) % MODULUS
    return normalize(answer)


def determinant3(rows: tuple[tuple[Polynomial, ...], ...]) -> Polynomial:
    a, b, c = rows
    return add(
        add(
            multiply(a[0], add(multiply(b[1], c[2]), multiply(b[2], c[1]), -1)),
            multiply(a[1], add(multiply(b[0], c[2]), multiply(b[2], c[0]), -1)),
            -1,
        ),
        multiply(a[2], add(multiply(b[0], c[1]), multiply(b[1], c[0]), -1)),
    )


def jacobian(first: Polynomial, second: Polynomial, third: Polynomial) -> Polynomial:
    rows = tuple(
        tuple(derivative(polynomial, variable) for variable in range(3))
        for polynomial in (first, second, third)
    )
    return determinant3(rows)


def monomial(exponent: Exponent, coefficient: int = 1) -> Polynomial:
    return {exponent: coefficient % MODULUS}


X = monomial((1, 0, 0))
Y = monomial((0, 1, 0))
Z = monomial((0, 0, 1))


def homogeneous_monomials(degree: int) -> tuple[Exponent, ...]:
    return tuple(
        (i, j, degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def rank_mod(matrix: list[list[int]]) -> int:
    if not matrix:
        return 0
    work = [[entry % MODULUS for entry in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, rows) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], MODULUS - 2, MODULUS)
        work[rank] = [(entry * inverse) % MODULUS for entry in work[rank]]
        for row in range(rows):
            if row == rank or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (work[row][index] - factor * work[rank][index]) % MODULUS
                for index in range(columns)
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def cubic_kernel_rank(h: Polynomial, p: Polynomial, q: Polynomial) -> int:
    first = multiply(h, p)
    second = multiply(h, q)
    input_monomials = homogeneous_monomials(3)
    output_monomials = homogeneous_monomials(8)
    columns = [
        jacobian(first, second, monomial(exponent))
        for exponent in input_monomials
    ]
    matrix = [
        [column.get(exponent, 0) for column in columns]
        for exponent in output_monomials
    ]
    return rank_mod(matrix)


def v_coordinate(polynomial: Polynomial, variable: int) -> int:
    assert polynomial
    return min(exponent[variable] for exponent in polynomial)


def polynomial_sum(terms: Iterable[Polynomial]) -> Polynomial:
    answer: Polynomial = {}
    for term in terms:
        answer = add(answer, term)
    return answer


def check_cubic_kernels_and_valuations() -> None:
    x2, y2, z2 = power(X, 2), power(Y, 2), power(Z, 2)
    x3, y3, z3 = power(X, 3), power(Y, 3), power(Z, 3)

    samples = (
        (
            "(e,a)=(1,3)",
            Z,
            add(x3, multiply(Y, z2)),
            add(y3, multiply(X, z2)),
        ),
        (
            "(e,a)=(2,2)",
            z2,
            add(x2, multiply(Y, Z)),
            add(y2, multiply(X, Z)),
        ),
        (
            "(e,a)=(3,1)",
            add(x3, multiply(Y, z2)),
            X,
            Y,
        ),
        (
            "mixed shared-factor degeneration",
            multiply(Y, Z),
            multiply(X, Z),
            add(x2, y2),
        ),
    )
    for label, h, p, q in samples:
        actual = cubic_kernel_rank(h, p, q)
        assert actual == 10, (label, actual)

    # In the mixed degeneration, z divides h and p, while the selected
    # horizontal component y divides neither p nor any q-lambda*p.
    h = multiply(Y, Z)
    p = multiply(X, Z)
    q = add(x2, y2)
    assert v_coordinate(p, 1) == 0
    for scalar in (0, 2, 5, MODULUS - 3):
        assert v_coordinate(add(q, p, -scalar), 1) == 0
    first = multiply(h, p)
    assert v_coordinate(first, 1) == 1

    # A finite-zero/pole ledger and a separate infinity factor.
    finite_numerator = multiply(
        power(add(q, p, -2), 2),
        add(q, p, 3),
    )
    finite_denominator = power(add(q, p, -5), 3)
    infinity_numerator = power(q, 2)
    infinity_denominator = multiply(p, add(q, p, -1))
    assert v_coordinate(finite_numerator, 1) == 0
    assert v_coordinate(finite_denominator, 1) == 0
    assert v_coordinate(infinity_numerator, 1) == 0
    assert v_coordinate(infinity_denominator, 1) == 0

    # The advertised vertical sharpness witness remains an exact kernel.
    vertical_h = z2
    vertical_p = z2
    vertical_q = add(x2, y2)
    assert jacobian(
        multiply(vertical_h, vertical_p),
        multiply(vertical_h, vertical_q),
        z3,
    ) == {}


def up_add(left: list[int], right: list[int], scale: int = 1) -> list[int]:
    size = max(len(left), len(right))
    return [
        (
            (left[index] if index < len(left) else 0)
            + scale * (right[index] if index < len(right) else 0)
        ) % MODULUS
        for index in range(size)
    ]


def up_multiply(left: list[int], right: list[int]) -> list[int]:
    answer = [0] * (len(left) + len(right) - 1)
    for i, first in enumerate(left):
        for j, second in enumerate(right):
            answer[i + j] = (answer[i + j] + first * second) % MODULUS
    return answer


def numeric_det(rows: list[list[int]]) -> int:
    return (
        rows[0][0] * (rows[1][1] * rows[2][2] - rows[1][2] * rows[2][1])
        - rows[0][1] * (rows[1][0] * rows[2][2] - rows[1][2] * rows[2][0])
        + rows[0][2] * (rows[1][0] * rows[2][1] - rows[1][1] * rows[2][0])
    ) % MODULUS


def check_eight_orientation() -> None:
    state = 22022026

    def next_value() -> int:
        nonlocal state
        state = (48271 * state) % 2_147_483_647
        return state % MODULUS

    for _ in range(128):
        linear = [[next_value() for _ in range(3)] for _ in range(3)]
        quadratic = [[next_value() for _ in range(3)] for _ in range(3)]
        cubic = [[next_value() for _ in range(3)] for _ in range(3)]
        leading = [
            [next_value() for _ in range(3)],
            [next_value() for _ in range(3)],
            [0, 0, 0],
        ]
        entries = [
            [
                [
                    linear[row][column],
                    quadratic[row][column],
                    cubic[row][column],
                    leading[row][column],
                ]
                for column in range(3)
            ]
            for row in range(3)
        ]
        determinant = up_add(
            up_add(
                up_multiply(
                    entries[0][0],
                    up_add(
                        up_multiply(entries[1][1], entries[2][2]),
                        up_multiply(entries[1][2], entries[2][1]),
                        -1,
                    ),
                ),
                up_multiply(
                    entries[0][1],
                    up_add(
                        up_multiply(entries[1][0], entries[2][2]),
                        up_multiply(entries[1][2], entries[2][0]),
                        -1,
                    ),
                ),
                -1,
            ),
            up_multiply(
                entries[0][2],
                up_add(
                    up_multiply(entries[1][0], entries[2][1]),
                    up_multiply(entries[1][1], entries[2][0]),
                    -1,
                ),
            ),
        )
        coefficient = determinant[8] if len(determinant) > 8 else 0
        expected = numeric_det([leading[0], leading[1], cubic[2]])
        assert coefficient == expected


if __name__ == "__main__":
    check_eight_orientation()
    check_cubic_kernels_and_valuations()
    print(
        "PASS: dependency-free E8 orientation, horizontal kernels, "
        "shared-factor degeneration, and valuation ledger"
    )
