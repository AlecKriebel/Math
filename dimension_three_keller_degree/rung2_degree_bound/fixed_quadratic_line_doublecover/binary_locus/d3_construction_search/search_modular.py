#!/usr/bin/env python3
"""Deterministic modular reconnaissance beyond the exact sparse certificates.

For each displayed E7 tangent, all eleven binary coefficients in

    U_0,V_0 in k[p,q]_3,  T_0 in k[p,q]_2

are sampled.  For every sample, the first two quadratic components A,B
remain completely arbitrary and the linear part L remains arbitrary.
E6 and E5 are solved exactly over F_p.  The resulting affine spaces are
sampled at E4,...,E1, always checking det(L) != 0.

Failure to find a point is reconnaissance only, not an obstruction.
"""

from __future__ import annotations

import argparse
from itertools import product
import json
import random
import sys

import sympy as sp


if not __debug__:
    print("FAIL: assertions must remain enabled", file=sys.stderr)
    raise SystemExit(2)


p, q, r, z = sp.symbols("p q r z")
coords = (p, q, r)
mon2 = (p**2, p * q, p * r, q**2, q * r, r**2)
mon2_binary = (p**2, p * q, q**2)
mon3_binary = (p**3, p**2 * q, p * q**2, q**3)


def coefficients(poly, degree):
    pp = sp.Poly(sp.expand(poly), p, q, r)
    return tuple(
        pp.coeff_monomial(p**i * q**j * r ** (degree - i - j))
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def weighted_determinant(h, R, U, V, T, A, B, L):
    H2 = sp.Matrix((A, B, T))
    H3 = sp.Matrix((U, V, R))
    H4 = sp.Matrix((sp.expand(h * p**2), sp.expand(h * q**2), 0))
    return sp.Poly(
        sp.expand(
            (
                L
                + z * H2.jacobian(coords)
                + z**2 * H3.jacobian(coords)
                + z**3 * H4.jacobian(coords)
            ).det()
        ),
        z,
    )


def linear_system_mod(equations, variables, prime):
    matrix = []
    rhs = []
    for equation in equations:
        polynomial = sp.Poly(sp.expand(equation), *variables, modulus=prime)
        if polynomial.is_zero:
            continue
        if polynomial.total_degree() > 1:
            raise AssertionError("E6/E5 ceased to be affine-linear")
        constant = int(polynomial.coeff_monomial((0,) * len(variables))) % prime
        row = []
        for index in range(len(variables)):
            exponent = [0] * len(variables)
            exponent[index] = 1
            row.append(int(polynomial.coeff_monomial(tuple(exponent))) % prime)
        matrix.append(row)
        rhs.append((-constant) % prime)
    return matrix, rhs


def affine_solve_mod(matrix, rhs, prime, variable_count):
    augmented = [
        [entry % prime for entry in row] + [value % prime]
        for row, value in zip(matrix, rhs)
    ]
    pivot_columns = []
    pivot_row = 0
    for column in range(variable_count):
        selected = next(
            (
                row
                for row in range(pivot_row, len(augmented))
                if augmented[row][column] % prime
            ),
            None,
        )
        if selected is None:
            continue
        augmented[pivot_row], augmented[selected] = (
            augmented[selected],
            augmented[pivot_row],
        )
        inverse = pow(augmented[pivot_row][column] % prime, -1, prime)
        augmented[pivot_row] = [
            value * inverse % prime for value in augmented[pivot_row]
        ]
        for row in range(len(augmented)):
            if row == pivot_row:
                continue
            multiplier = augmented[row][column] % prime
            if multiplier:
                augmented[row] = [
                    (left - multiplier * right) % prime
                    for left, right in zip(augmented[row], augmented[pivot_row])
                ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(augmented):
            break

    for row in augmented:
        if all(value % prime == 0 for value in row[:-1]) and row[-1] % prime:
            return None

    free_columns = [
        column for column in range(variable_count) if column not in pivot_columns
    ]
    particular = [0] * variable_count
    for row, column in enumerate(pivot_columns):
        particular[column] = augmented[row][-1] % prime
    basis = []
    for free in free_columns:
        vector = [0] * variable_count
        vector[free] = 1
        for row, column in enumerate(pivot_columns):
            vector[column] = -augmented[row][free] % prime
        basis.append(vector)
    return particular, basis, len(pivot_columns)


def polynomial_mod(expression, variables, prime):
    return sp.Poly(sp.expand(expression), *variables, modulus=prime)


def evaluate_poly(polynomial, values, prime):
    total = 0
    for exponents, coefficient in polynomial.terms():
        term = int(coefficient) % prime
        for value, exponent in zip(values, exponents):
            if exponent:
                term = term * pow(value, exponent, prime) % prime
        total = (total + term) % prime
    return total


def parameter_points(prime, dimension, maximum, seed):
    total = prime**dimension
    if total <= maximum:
        yield from product(range(prime), repeat=dimension)
        return
    zero = (0,) * dimension
    yield zero
    emitted = {zero}
    for index in range(dimension):
        for value in range(1, prime):
            point = tuple(value if j == index else 0 for j in range(dimension))
            if point not in emitted:
                emitted.add(point)
                yield point
                if len(emitted) >= maximum:
                    return
    rng = random.Random(seed)
    while len(emitted) < maximum:
        point = tuple(rng.randrange(prime) for _ in range(dimension))
        if point not in emitted:
            emitted.add(point)
            yield point


def tangent_cases(prime):
    cases = {
        "BS-zero": (p**2, p**2 * q, 0, 0, 0),
        "BS-y0": (p**2, p**2 * q, -2 * p**2 * r, q**2 * r, 0),
        "BS-y1": (p**2, p**2 * q, 0, 2 * p * q * r, p * r),
        "BS-mixed": (
            p**2,
            p**2 * q,
            2 * p**2 * r,
            (q**2 + 2 * p * q) * r,
            (p + q) * r,
        ),
        "BB-zero": (p * q, p**2 * q, 0, 0, 0),
    }
    inverse_five = pow(5, -1, prime)
    roots = [
        value
        for value in range(prime)
        if (3 * value * value - 8 * value + 12) % prime == 0
    ]
    for index, y0 in enumerate(roots):
        u_coefficient = (-y0 + 8) * inverse_five % prime
        cases[f"BB-conjugate-{index}"] = (
            p * q,
            p**2 * q,
            u_coefficient * p**2 * r,
            y0 * q**2 * r,
            p * r,
        )
    return cases


def analyze_case(label, case, prime, trials, samples, seed):
    h, R, U_nonbinary, V_nonbinary, T_nonbinary = case
    avars = sp.symbols("a0:6")
    bvars = sp.symbols("b0:6")
    lvars = sp.symbols("l0:9")
    lower = avars + bvars + lvars
    A = sum(value * monomial for value, monomial in zip(avars, mon2))
    B = sum(value * monomial for value, monomial in zip(bvars, mon2))
    L = sp.Matrix(3, 3, lvars)

    rng = random.Random(seed)
    binary_samples = [(0,) * 11]
    while len(binary_samples) < trials:
        point = tuple(rng.randrange(prime) for _ in range(11))
        if point not in binary_samples:
            binary_samples.append(point)

    summary = {
        "binary_trials": len(binary_samples),
        "e6e5_consistent": 0,
        "e6e5_invertible_affine": 0,
        "free_points_tested": 0,
        "full_modular_hits": 0,
        "first_hit": None,
    }

    for trial_index, binary in enumerate(binary_samples):
        U0 = sum(value * monomial for value, monomial in zip(binary[:4], mon3_binary))
        V0 = sum(value * monomial for value, monomial in zip(binary[4:8], mon3_binary))
        T0 = sum(value * monomial for value, monomial in zip(binary[8:], mon2_binary))
        determinant = weighted_determinant(
            h,
            R,
            U_nonbinary + U0,
            V_nonbinary + V0,
            T_nonbinary + T0,
            A,
            B,
            L,
        )
        for degree in (9, 8, 7):
            require_top = coefficients(determinant.coeff_monomial(z**degree), degree)
            if any(int(value) % prime for value in require_top):
                raise AssertionError(f"{label}: E{degree} not zero modulo {prime}")

        top_equations = []
        for degree in (6, 5):
            top_equations.extend(
                coefficients(determinant.coeff_monomial(z**degree), degree)
            )
        matrix, rhs = linear_system_mod(top_equations, lower, prime)
        affine = affine_solve_mod(matrix, rhs, prime, len(lower))
        if affine is None:
            continue
        summary["e6e5_consistent"] += 1
        particular, basis, rank = affine
        free_symbols = sp.symbols(f"t0:{len(basis)}")
        lower_expressions = [
            particular[index]
            + sum(
                basis_column[index] * parameter
                for basis_column, parameter in zip(basis, free_symbols)
            )
            for index in range(len(lower))
        ]
        substitution = dict(zip(lower, lower_expressions))
        determinant_polynomial = polynomial_mod(
            L.det().subs(substitution), free_symbols, prime
        )
        if determinant_polynomial.is_zero:
            continue
        summary["e6e5_invertible_affine"] += 1
        lower_polynomials = []
        for degree in (4, 3, 2, 1):
            lower_polynomials.extend(
                polynomial_mod(value.subs(substitution), free_symbols, prime)
                for value in coefficients(
                    determinant.coeff_monomial(z**degree), degree
                )
                if sp.expand(value.subs(substitution)) != 0
            )

        for free_values in parameter_points(
            prime,
            len(basis),
            samples,
            seed + 1009 * trial_index,
        ):
            summary["free_points_tested"] += 1
            if any(
                evaluate_poly(polynomial, free_values, prime)
                for polynomial in lower_polynomials
            ):
                continue
            determinant_value = evaluate_poly(
                determinant_polynomial, free_values, prime
            )
            if determinant_value == 0:
                continue
            lower_values = [
                (
                    particular[index]
                    + sum(
                        basis_column[index] * value
                        for basis_column, value in zip(basis, free_values)
                    )
                )
                % prime
                for index in range(len(lower))
            ]
            summary["full_modular_hits"] += 1
            if summary["first_hit"] is None:
                summary["first_hit"] = {
                    "prime": prime,
                    "binary": binary,
                    "lower": lower_values,
                    "detL": determinant_value,
                    "e6e5_rank": rank,
                    "free_dimension": len(basis),
                }
            break
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--primes", nargs="+", type=int, default=(23, 29))
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--samples", type=int, default=512)
    parser.add_argument("--seed", type=int, default=20260726)
    args = parser.parse_args()
    if args.trials < 1 or args.samples < 1:
        raise SystemExit("trials and samples must be positive")

    report = {
        "schema": "d3-construction-modular-recon-v1",
        "seed": args.seed,
        "trials_per_case": args.trials,
        "free_samples_per_affine_space": args.samples,
        "warning": "absence of a modular hit is reconnaissance, not an obstruction",
        "results": {},
    }
    for prime_index, prime in enumerate(args.primes):
        if prime in (2, 3, 5, 7):
            raise SystemExit("use good primes other than 2, 3, 5, and 7")
        for case_index, (label, case) in enumerate(tangent_cases(prime).items()):
            result = analyze_case(
                label,
                case,
                prime,
                args.trials,
                args.samples,
                args.seed + 100000 * prime_index + 1000 * case_index,
            )
            report["results"][f"F{prime}:{label}"] = result
    if (
        tuple(args.primes) == (23, 29)
        and args.trials == 3
        and args.samples == 512
        and args.seed == 20260726
    ):
        expected_by_label = {
            "BB-conjugate-0": (0, 0, 0),
            "BB-conjugate-1": (0, 0, 0),
            "BB-zero": (3, 1, 512),
            "BS-mixed": (0, 0, 0),
            "BS-y0": (0, 0, 0),
            "BS-y1": (1, 1, 512),
            "BS-zero": (3, 1, 512),
        }
        for prime in (23, 29):
            for label, (
                expected_consistent,
                expected_invertible,
                expected_tested,
            ) in expected_by_label.items():
                result = report["results"][f"F{prime}:{label}"]
                if (
                    result["binary_trials"],
                    result["e6e5_consistent"],
                    result["e6e5_invertible_affine"],
                    result["free_points_tested"],
                    result["full_modular_hits"],
                    result["first_hit"],
                ) != (
                    3,
                    expected_consistent,
                    expected_invertible,
                    expected_tested,
                    0,
                    None,
                ):
                    raise AssertionError(
                        f"frozen modular summary drifted at F{prime}:{label}"
                    )
        print("D3_CONSTRUCTION_MODULAR_FROZEN_COUNTS_PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    print("D3_CONSTRUCTION_MODULAR_RECON_PASS")


if __name__ == "__main__":
    main()
