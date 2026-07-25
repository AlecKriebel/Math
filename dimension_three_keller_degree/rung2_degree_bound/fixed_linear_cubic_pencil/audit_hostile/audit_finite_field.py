#!/usr/bin/python3
"""Dependency-free exact audit over a large prime field.

This is deliberately independent of the supplied SymPy and PARI/GP
implementations.  It reconstructs polynomial arithmetic, Jacobian
derivations, linear ranks, and weighted 3-by-3 determinants from scratch.
"""

from __future__ import annotations

from random import Random

PRIME = 1_000_003
Poly = dict[tuple[int, int, int], int]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def clean(poly: Poly) -> Poly:
    return {monomial: coefficient % PRIME for monomial, coefficient in poly.items()
            if coefficient % PRIME}


def add(first: Poly, second: Poly, scale: int = 1) -> Poly:
    result = dict(first)
    for monomial, coefficient in second.items():
        result[monomial] = (result.get(monomial, 0) + scale * coefficient) % PRIME
    return clean(result)


def mul(first: Poly, second: Poly) -> Poly:
    result: Poly = {}
    for left, left_coefficient in first.items():
        for right, right_coefficient in second.items():
            monomial = tuple(left[index] + right[index] for index in range(3))
            result[monomial] = (
                result.get(monomial, 0) + left_coefficient * right_coefficient
            ) % PRIME
    return clean(result)


def derivative(poly: Poly, variable: int) -> Poly:
    result: Poly = {}
    for monomial, coefficient in poly.items():
        exponent = monomial[variable]
        if exponent:
            target = list(monomial)
            target[variable] -= 1
            result[tuple(target)] = coefficient * exponent % PRIME
    return clean(result)


def jacobian(first: Poly, second: Poly, third: Poly) -> Poly:
    rows = [
        [derivative(form, variable) for variable in range(3)]
        for form in (first, second, third)
    ]
    positive = add(
        add(
            mul(rows[0][0], mul(rows[1][1], rows[2][2])),
            mul(rows[0][1], mul(rows[1][2], rows[2][0])),
        ),
        mul(rows[0][2], mul(rows[1][0], rows[2][1])),
    )
    negative = add(
        add(
            mul(rows[0][2], mul(rows[1][1], rows[2][0])),
            mul(rows[0][1], mul(rows[1][0], rows[2][2])),
        ),
        mul(rows[0][0], mul(rows[1][2], rows[2][1])),
    )
    return add(positive, negative, -1)


def homogeneous_monomials(degree: int) -> list[tuple[int, int, int]]:
    return [
        (i, j, degree - i - j)
        for i in range(degree + 1)
        for j in range(degree + 1 - i)
    ]


def form(coefficients: list[int], degree: int) -> Poly:
    monomials = homogeneous_monomials(degree)
    require(len(coefficients) == len(monomials), "coefficient-vector length")
    return clean(dict(zip(monomials, coefficients)))


def monomial(exponents: tuple[int, int, int], coefficient: int = 1) -> Poly:
    return clean({exponents: coefficient})


def matrix_rank(matrix: list[list[int]]) -> int:
    if not matrix:
        return 0
    work = [[entry % PRIME for entry in row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column], PRIME - 2, PRIME)
        work[pivot_row] = [entry * inverse % PRIME for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (work[row][index] - factor * work[pivot_row][index]) % PRIME
                for index in range(column_count)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def kernel_rank(first: Poly, second: Poly, degree: int) -> int:
    input_monomials = homogeneous_monomials(degree)
    output_monomials = homogeneous_monomials(degree + 5)
    columns = [
        jacobian(first, second, monomial(input_monomial))
        for input_monomial in input_monomials
    ]
    matrix = [
        [column.get(output_monomial, 0) for column in columns]
        for output_monomial in output_monomials
    ]
    return matrix_rank(matrix)


def restrict_to_z_zero(poly: Poly) -> list[int]:
    return [
        poly.get((i, 3 - i, 0), 0)
        for i in range(4)
    ]


def is_horizontal_for_z(p: Poly, q: Poly) -> bool:
    return matrix_rank([restrict_to_z_zero(p), restrict_to_z_zero(q)]) == 2


def scalar_mul(poly: Poly, coefficient: int) -> Poly:
    return clean({key: coefficient * value for key, value in poly.items()})


def random_cubic(random: Random) -> Poly:
    return form([random.randrange(PRIME) for _ in range(10)], 3)


def audit_random_horizontal_kernels() -> None:
    random = Random(0xC0B1C)
    h = monomial((0, 0, 1))
    checked = 0
    attempts = 0
    while checked < 64 and attempts < 512:
        attempts += 1
        p = random_cubic(random)
        q = random_cubic(random)
        if not is_horizontal_for_z(p, q):
            continue
        P = mul(h, p)
        Q = mul(h, q)
        require(kernel_rank(P, Q, 2) == 6, "random horizontal quadratic kernel")
        require(kernel_rank(P, Q, 3) == 10, "random horizontal cubic kernel")
        checked += 1
    require(checked == 64, "insufficient horizontal samples")


TauPoly = list[int]


def tau_add(first: TauPoly, second: TauPoly, scale: int = 1) -> TauPoly:
    length = max(len(first), len(second))
    result = [0] * length
    for index in range(length):
        result[index] = (
            (first[index] if index < len(first) else 0)
            + scale * (second[index] if index < len(second) else 0)
        ) % PRIME
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def tau_mul(first: TauPoly, second: TauPoly) -> TauPoly:
    result = [0] * (len(first) + len(second) - 1)
    for left_index, left in enumerate(first):
        for right_index, right in enumerate(second):
            result[left_index + right_index] = (
                result[left_index + right_index] + left * right
            ) % PRIME
    return result


def tau_det(matrix: list[list[TauPoly]]) -> TauPoly:
    positive = tau_add(
        tau_add(
            tau_mul(matrix[0][0], tau_mul(matrix[1][1], matrix[2][2])),
            tau_mul(matrix[0][1], tau_mul(matrix[1][2], matrix[2][0])),
        ),
        tau_mul(matrix[0][2], tau_mul(matrix[1][0], matrix[2][1])),
    )
    negative = tau_add(
        tau_add(
            tau_mul(matrix[0][2], tau_mul(matrix[1][1], matrix[2][0])),
            tau_mul(matrix[0][1], tau_mul(matrix[1][0], matrix[2][2])),
        ),
        tau_mul(matrix[0][0], tau_mul(matrix[1][2], matrix[2][1])),
    )
    return tau_add(positive, negative, -1)


def scalar_det(matrix: list[list[int]]) -> int:
    return (
        matrix[0][0] * matrix[1][1] * matrix[2][2]
        + matrix[0][1] * matrix[1][2] * matrix[2][0]
        + matrix[0][2] * matrix[1][0] * matrix[2][1]
        - matrix[0][2] * matrix[1][1] * matrix[2][0]
        - matrix[0][1] * matrix[1][0] * matrix[2][2]
        - matrix[0][0] * matrix[1][2] * matrix[2][1]
    ) % PRIME


def audit_weighted_polarizations() -> None:
    random = Random(0xE8E7)
    for _ in range(128):
        L = [[random.randrange(PRIME) for _ in range(3)] for _ in range(3)]
        A = [[random.randrange(PRIME) for _ in range(3)] for _ in range(3)]
        B = [[random.randrange(PRIME) for _ in range(3)] for _ in range(3)]
        C = [[random.randrange(PRIME) for _ in range(3)] for _ in range(2)]
        C.append([0, 0, 0])
        weighted = [
            [
                [L[row][column], A[row][column], B[row][column], C[row][column]]
                for column in range(3)
            ]
            for row in range(3)
        ]
        determinant = tau_det(weighted)
        coefficient_e8 = determinant[8] if len(determinant) > 8 else 0
        expected_e8 = scalar_det([C[0], C[1], B[2]])
        require(coefficient_e8 == expected_e8, "raw E8 polarization")

        B[2] = [0, 0, 0]
        weighted_after = [
            [
                [L[row][column], A[row][column], B[row][column], C[row][column]]
                for column in range(3)
            ]
            for row in range(3)
        ]
        determinant_after = tau_det(weighted_after)
        coefficient_e7 = determinant_after[7] if len(determinant_after) > 7 else 0
        expected_e7 = scalar_det([C[0], C[1], A[2]])
        require(coefficient_e7 == expected_e7, "raw E7 polarization")


def audit_vertical_witnesses() -> None:
    x = monomial((1, 0, 0))
    z = monomial((0, 0, 1))
    p_simple = monomial((2, 0, 1))
    q_fermat = add(monomial((3, 0, 0)), monomial((0, 3, 0)))
    P_simple = mul(z, p_simple)
    Q_simple = mul(z, q_fermat)
    G2 = mul(x, z)
    require(P_simple == mul(G2, G2), "simple vertical square identity")
    require(not jacobian(P_simple, Q_simple, G2), "simple vertical witness")

    p_triple = monomial((0, 0, 3))
    P_triple = mul(z, p_triple)
    Q_triple = mul(z, q_fermat)
    require(not jacobian(P_triple, Q_triple, monomial((0, 0, 3))),
            "triple vertical cubic witness")
    require(not jacobian(P_triple, Q_triple, monomial((0, 0, 2))),
            "triple vertical quadratic witness")


audit_random_horizontal_kernels()
audit_weighted_polarizations()
audit_vertical_witnesses()
print("AUDIT_HORIZONTAL_CUBIC_PENCIL_FF_PASS_8D1A77")
