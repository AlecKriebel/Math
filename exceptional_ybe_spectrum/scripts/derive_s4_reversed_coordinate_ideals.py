#!/usr/bin/env python3
"""Discover sparse exact coordinate certificates for reversed S4 branch.

The coefficient arithmetic is in Z[s]/(s^2-3)[i].  Every local
commutant generator is first multiplied by 24, after which all four
components are integral.
"""

from __future__ import annotations

import itertools
import math
import time

import numpy as np
import sympy as sp

from derive_s4_reversed_heterogeneous import build_exact_commutant


SCALE = 24


def exact_components(matrix):
    """Return (real_1, real_s, imag_1, imag_s) int64 components."""
    result = np.zeros((4, matrix.rows, matrix.cols), dtype=np.int64)
    square_root = sp.sqrt(3)
    for row in range(matrix.rows):
        for column in range(matrix.cols):
            entry = sp.expand(SCALE * matrix[row, column])
            for offset, part in (
                (0, sp.re(entry)),
                (2, sp.im(entry)),
            ):
                constant = sp.simplify(part.subs(square_root, 0))
                radical = sp.simplify((part - constant) / square_root)
                assert constant.is_Integer
                assert radical.is_Integer
                result[offset, row, column] = int(constant)
                result[offset + 1, row, column] = int(radical)
    return result


def quadratic_matmul(first, second):
    """Matrix product for pairs a+b*sqrt(3)."""
    return (
        first[0] @ second[0] + 3 * (first[1] @ second[1]),
        first[0] @ second[1] + first[1] @ second[0],
    )


def algebra_matmul(first, second):
    real_real = quadratic_matmul(first[:2], second[:2])
    imag_imag = quadratic_matmul(first[2:], second[2:])
    real_imag = quadratic_matmul(first[:2], second[2:])
    imag_real = quadratic_matmul(first[2:], second[:2])
    return np.stack(
        (
            real_real[0] - imag_imag[0],
            real_real[1] - imag_imag[1],
            real_imag[0] + imag_real[0],
            real_imag[1] + imag_real[1],
        )
    )


def branch_generators(signature):
    """Return fixed H part and Pauli triples for a half-rank branch."""
    data = build_exact_commutant()
    central = data["central"]
    paulis = data["paulis"]
    simple_one, simple_sign, rank_two, rank_three, rank_three_twisted = (
        signature
    )
    fixed = (
        (1 if simple_one else -1) * central[0]
        + (1 if simple_sign else -1) * central[1]
    )
    active = []
    for multiplicity_rank, projector, triple in zip(
        (rank_two, rank_three, rank_three_twisted),
        central[2:],
        paulis,
    ):
        if multiplicity_rank == 0:
            fixed -= projector
        elif multiplicity_rank == 2:
            fixed += projector
        else:
            assert multiplicity_rank == 1
            active.append(triple)
    return [fixed] + [matrix for triple in active for matrix in triple]


def residual_coefficients(signature):
    """Return polynomial coefficient matrices after substituting x_0=1."""
    local = [exact_components(matrix) for matrix in branch_generators(signature)]
    count = len(local)
    identity_six = np.eye(6, dtype=np.int64)
    left = [
        np.stack(
            tuple(np.kron(component, identity_six) for component in matrix)
        )
        for matrix in local
    ]
    right = [
        np.stack(
            tuple(np.kron(identity_six, component) for component in matrix)
        )
        for matrix in local
    ]
    left_right = [
        [algebra_matmul(left[i], right[j]) for j in range(count)]
        for i in range(count)
    ]
    right_left = [
        [algebra_matmul(right[i], left[j]) for j in range(count)]
        for i in range(count)
    ]

    variable_count = count - 1
    zero_exponent = (0,) * variable_count
    coefficients = {}
    for first, middle, last in itertools.product(range(count), repeat=3):
        exponent = [0] * variable_count
        for index in (first, middle, last):
            if index:
                exponent[index - 1] += 1
        exponent = tuple(exponent)
        forward = algebra_matmul(left_right[first][middle], left[last])
        backward = algebra_matmul(right_left[first][middle], right[last])
        contribution = forward - backward
        if exponent not in coefficients:
            coefficients[exponent] = contribution
        else:
            coefficients[exponent] += contribution

    # SCALE^3 D has linear contribution
    # -(SCALE^3/3)(H_1-H_2) = -(SCALE^2/3)(L-R).
    linear_factor = SCALE * SCALE // 3
    coefficients.setdefault(zero_exponent, np.zeros_like(left[0]))
    coefficients[zero_exponent] -= linear_factor * (left[0] - right[0])
    for index in range(1, count):
        exponent = [0] * variable_count
        exponent[index - 1] = 1
        exponent = tuple(exponent)
        coefficients.setdefault(exponent, np.zeros_like(left[0]))
        coefficients[exponent] -= linear_factor * (
            left[index] - right[index]
        )
    return coefficients


def sparse_polynomials(coefficients, limit=80):
    exponents = sorted(coefficients)
    stacked = np.stack(tuple(coefficients[exponent] for exponent in exponents))
    support = np.count_nonzero(stacked, axis=0)
    candidates = []
    for component, row, column in itertools.product(
        range(4), range(108), range(108)
    ):
        count = int(support[component, row, column])
        if count:
            candidates.append((count, component, row, column))
    candidates.sort()
    variables = sp.symbols(f"x0:{len(exponents[0])}", real=True)
    result = []
    seen = set()
    for count, component, row, column in candidates:
        values = [
            int(coefficients[exponent][component, row, column])
            for exponent in exponents
        ]
        divisor = 0
        for value in values:
            divisor = math.gcd(divisor, abs(value))
        values = [value // divisor for value in values]
        polynomial = sp.expand(
            sum(
                value
                * sp.prod(
                    variable**power
                    for variable, power in zip(variables, exponent)
                )
                for value, exponent in zip(values, exponents)
            )
        )
        canonical = str(polynomial)
        if canonical in seen or str(-polynomial) in seen:
            continue
        seen.add(canonical)
        result.append(
            {
                "support": count,
                "component": component,
                "row": row,
                "column": column,
                "divisor": divisor,
                "polynomial": polynomial,
            }
        )
        if len(result) >= limit:
            break
    return variables, result


BRANCHES = (
    (0, 0, 0, 1, 2),
    (0, 0, 0, 2, 1),
    (0, 1, 1, 0, 2),
    (0, 1, 1, 1, 1),
    (0, 1, 1, 2, 0),
)


def main():
    for branch in BRANCHES:
        started = time.monotonic()
        coefficients = residual_coefficients(branch)
        variables, sparse = sparse_polynomials(coefficients)
        print("branch:", branch)
        print("variables:", variables)
        print("elapsed:", time.monotonic() - started)
        for item in sparse[:30]:
            print(
                item["support"],
                (item["component"], item["row"], item["column"]),
                item["polynomial"],
            )
        print()


if __name__ == "__main__":
    main()
