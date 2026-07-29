#!/usr/bin/env python3
"""Discovery-only reconstruction of the S4 squared-residual polynomial.

This helper uses high-precision floating evaluation followed by rational
recognition.  It was used to investigate a possible SOS certificate but
is not an exact verifier and is not evidence for the no-go theorem.
"""

from __future__ import annotations

from fractions import Fraction
import itertools
import pathlib
import sys

import numpy as np
import sympy as sp


sys.path.insert(
    0, str(pathlib.Path(__file__).resolve().parents[1] / "verifiers")
)
from verify_s4_equivariant_noncentral_no_go import build_exact_paulis


def main():
    metric, _, _, paulis = build_exact_paulis()
    integer_paulis = []
    for matrix in paulis[0] + paulis[1]:
        numerical = np.array(matrix.tolist(), dtype=complex) * 12
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
    coefficients = []
    for monomial in cubic_monomials:
        coefficient = np.zeros((72, 72), dtype=complex)
        for ordered in set(itertools.permutations(monomial)):
            first, middle, last = ordered
            coefficient += (
                left[first] @ right[middle] @ left[last]
                - right[first] @ left[middle] @ right[last]
            )
        coefficients.append(coefficient)
    coefficients.extend(
        -48 * (left[index] - right[index]) for index in range(6)
    )

    # Recover the two local metrics directly from their known Gram forms.
    metric_a = np.array([[2, 1], [1, 2]], dtype=float)
    metric_b = np.array(
        [[2, 1, 1], [1, 2, 1], [1, 1, 2]], dtype=float
    )
    metric_five = np.kron(
        np.kron(np.kron(np.kron(metric_a, metric_b), metric_a), metric_b),
        metric_a,
    )
    cholesky = np.linalg.cholesky(metric_five).T
    cholesky_inverse = np.linalg.inv(cholesky)
    flattened = np.array(
        [
            (cholesky @ matrix @ cholesky_inverse).reshape(-1)
            for matrix in coefficients
        ]
    )
    gram = np.real(flattened.conjugate() @ flattened.T)

    variables = sp.symbols("x y z u v w")
    monomial_exponents = []
    for monomial in cubic_monomials:
        exponents = [0] * 6
        for index in monomial:
            exponents[index] += 1
        monomial_exponents.append(tuple(exponents))
    monomial_exponents.extend(
        tuple(1 if index == position else 0 for index in range(6))
        for position in range(6)
    )

    objective_coefficients = {}
    scale = 1728**2
    for first, exponent_first in enumerate(monomial_exponents):
        for second, exponent_second in enumerate(monomial_exponents):
            value = gram[first, second] / scale
            if abs(value) < 1e-9:
                continue
            rational = Fraction(float(value)).limit_denominator(100000)
            assert abs(float(rational) - value) < 1e-8
            exponent = tuple(
                exponent_first[index] + exponent_second[index]
                for index in range(6)
            )
            objective_coefficients[exponent] = (
                objective_coefficients.get(exponent, Fraction(0))
                + rational
            )

    objective = sum(
        sp.Rational(coefficient.numerator, coefficient.denominator)
        * sp.prod(
            variables[index] ** exponent[index]
            for index in range(6)
        )
        for exponent, coefficient in objective_coefficients.items()
        if coefficient
    )
    objective = sp.factor(objective)
    print("objective terms:", len(sp.Poly(objective, variables).terms()))
    print("objective:")
    print(objective)
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
    basis = sp.groebner(
        spheres, *variables, order="lex", domain=sp.QQ
    )
    remainder = basis.reduce(sp.expand(objective - 64))[1]
    print("remainder of objective - 64:")
    print(sp.factor(remainder))


if __name__ == "__main__":
    main()
