#!/usr/bin/env python3
"""Discovery helper for a compact exact S4-equivariant no-go certificate."""

from __future__ import annotations

import itertools
import math
import pathlib
import sys

import numpy as np
import sympy as sp


sys.path.insert(
    0, str(pathlib.Path(__file__).resolve().parents[1] / "verifiers")
)
from verify_s4_equivariant_noncentral_no_go import build_exact_paulis


def main():
    _, _, _, paulis = build_exact_paulis()
    integer_paulis = []
    for matrix in paulis[0] + paulis[1]:
        numerical = np.array(matrix.tolist(), dtype=complex) * 12
        assert np.max(
            np.abs(numerical.real - np.rint(numerical.real))
        ) < 1e-10
        assert np.max(
            np.abs(numerical.imag - np.rint(numerical.imag))
        ) < 1e-10
        integer_paulis.append(
            np.rint(numerical.real)
            + 1j * np.rint(numerical.imag)
        )

    identity = np.eye(6)
    left = [
        np.kron(matrix, identity) for matrix in integer_paulis
    ]
    right = [
        np.kron(identity, matrix) for matrix in integer_paulis
    ]
    cubic_monomials = list(
        itertools.combinations_with_replacement(range(6), 3)
    )
    cubic_coefficients = {
        monomial: np.zeros((72, 72), dtype=complex)
        for monomial in cubic_monomials
    }
    for first, middle, last in itertools.product(range(6), repeat=3):
        cubic_coefficients[tuple(sorted((first, middle, last)))] += (
            left[first] @ right[middle] @ left[last]
            - right[first] @ left[middle] @ right[last]
        )
    linear_coefficients = [
        -48 * (left[index] - right[index]) for index in range(6)
    ]

    variables = sp.symbols("x y z u v w")
    unique = {}
    for row in range(72):
        for column in range(72):
            for part in ("real", "imaginary"):
                coefficients = []
                for monomial in cubic_monomials:
                    value = cubic_coefficients[monomial][row, column]
                    coefficients.append(
                        int(round(value.real if part == "real" else value.imag))
                    )
                for matrix in linear_coefficients:
                    value = matrix[row, column]
                    coefficients.append(
                        int(round(value.real if part == "real" else value.imag))
                    )
                if not any(coefficients):
                    continue
                divisor = 0
                for coefficient in coefficients:
                    divisor = math.gcd(divisor, abs(coefficient))
                coefficients = [
                    coefficient // divisor for coefficient in coefficients
                ]
                if next(
                    coefficient
                    for coefficient in coefficients
                    if coefficient
                ) < 0:
                    coefficients = [
                        -coefficient for coefficient in coefficients
                    ]
                key = tuple(coefficients)
                if key in unique:
                    continue
                unique[key] = (row, column, part, divisor)

    ranked = sorted(
        unique.items(),
        key=lambda item: (
            sum(coefficient != 0 for coefficient in item[0]),
            sum(abs(coefficient) for coefficient in item[0]),
        ),
    )

    def polynomial(coefficients):
        return sum(
            coefficient
            * variables[first]
            * variables[middle]
            * variables[last]
            for coefficient, (first, middle, last) in zip(
                coefficients, cubic_monomials
            )
        ) + sum(
            coefficients[len(cubic_monomials) + index]
            * variables[index]
            for index in range(6)
        )

    spheres = [
        variables[0] ** 2
        + variables[1] ** 2
        + variables[2] ** 2
        - 1,
        variables[3] ** 2
        + variables[4] ** 2
        + variables[5] ** 2
        - 1,
    ]
    print("unique residual coordinate polynomials:", len(ranked))
    certificate = list(range(20)) + [154, 160, 323]
    for index in certificate:
        coefficients, location = ranked[index]
        print(
            index,
            location,
            sp.factor(polynomial(coefficients)),
        )
    basis = sp.groebner(
        spheres
        + [
            polynomial(ranked[index][0])
            for index in certificate
        ],
        *variables,
        order="grevlex",
        domain=sp.QQ,
    )
    assert len(basis.polys) == 1
    assert basis.polys[0].as_expr() == 1
    print("selected 23-coordinate ideal: <1>")


if __name__ == "__main__":
    main()
