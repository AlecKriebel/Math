#!/usr/bin/env python3
"""Numerically search affine graph-constraint corrections, then certify exactly.

The numerical stage is only a candidate generator.  A reported success must
survive rational reconstruction and a full symbolic Jacobian determinant over
Q before it has any mathematical status.
"""

from __future__ import annotations

from fractions import Fraction
import random

import numpy as np
from scipy.optimize import least_squares
import sympy as sp


x, y, z, p, q, r = sp.symbols("x y z p q r")
VARS = (x, y, z, p, q, r)

BASE = [
    x - sp.Rational(3, 2) * x * p - sp.Rational(1, 2) * x**2 * q,
    y + 3 * q + 12 * y * p + 6 * p * q + 9 * y * r + 3 * q * r,
    z + 4 * y**2 + 3 * z * p + 7 * y**2 * p + 3 * z * r
    + 3 * y**2 * r + z * p * r,
]

CONSTRAINTS = (p - x * y, q - x * z, r - p**2)
LINEAR_BASIS = (x, y, z, p, q, r)


def symbolic_base_jacobian():
    a, b, c = sp.symbols("a b c")
    substitutions = {p: x * y + a, q: x * z + b}
    substitutions[r] = (x * y + a) ** 2 + c
    # Differentiate after substitution: a,b,c are the fixed graph-error outputs.
    lifted = [sp.expand(f.subs(substitutions, simultaneous=True)) for f in BASE]
    jacobian = sp.Matrix(lifted).jacobian((x, y, z))
    return (a, b, c), jacobian


ERRORS, BASE_JACOBIAN = symbolic_base_jacobian()
BASE_FUNCTION = sp.lambdify((x, y, z, *ERRORS), BASE_JACOBIAN, "numpy")


def make_samples(count, seed):
    rng = random.Random(seed)
    rows = []
    while len(rows) < count:
        row = [rng.uniform(-1.25, 1.25) for _ in range(6)]
        if max(abs(value) for value in row[3:]) > 0.2:
            rows.append(row)
    return np.asarray(rows, dtype=float)


def base_matrices(samples):
    matrices = []
    for row in samples:
        matrix = np.asarray(BASE_FUNCTION(*row), dtype=float)
        matrices.append(matrix)
    return np.asarray(matrices)


def feature_tensor(samples):
    """Return features[sample,constraint,basis,derivative-coordinate]."""
    result = np.zeros((len(samples), 3, 6, 3), dtype=float)
    for sample_index, (xx, yy, zz, aa, bb, cc) in enumerate(samples):
        pp = xx * yy + aa
        errors = (aa, bb, cc)
        gradients = np.asarray(
            [
                (1, 0, 0),
                (0, 1, 0),
                (0, 0, 1),
                (yy, xx, 0),
                (zz, 0, xx),
                (2 * pp * yy, 2 * pp * xx, 0),
            ],
            dtype=float,
        )
        for constraint_index, error in enumerate(errors):
            result[sample_index, constraint_index, :, :] = error * gradients
    return result


def residual_function(samples):
    bases = base_matrices(samples)
    features = feature_tensor(samples)

    def residual(vector):
        parameters = vector.reshape(3, 3, 6)
        corrections = np.einsum("ijb,sjbk->sik", parameters, features)
        determinants = np.linalg.det(bases + corrections)
        return determinants - 1.0

    return residual


def rationalize(vector, max_denominator=512, tolerance=2e-7):
    rationals = []
    for value in vector:
        candidate = Fraction(float(value)).limit_denominator(max_denominator)
        if abs(float(candidate) - value) > tolerance:
            return None
        rationals.append(sp.Rational(candidate.numerator, candidate.denominator))
    return rationals


def exact_candidate(rationals):
    parameters = np.asarray(rationals, dtype=object).reshape(3, 3, 6)
    first = BASE[:]
    for output in range(3):
        correction = 0
        for constraint in range(3):
            linear_form = sum(
                parameters[output, constraint, basis] * LINEAR_BASIS[basis]
                for basis in range(6)
            )
            correction += CONSTRAINTS[constraint] * linear_form
        first[output] = sp.expand(first[output] + correction)
    candidate = first + list(CONSTRAINTS)
    determinant = sp.factor(sp.Matrix(candidate).jacobian(VARS).det())
    return candidate, determinant


def main():
    training = make_samples(180, 6102026)
    holdout = make_samples(80, 6112026)
    training_residual = residual_function(training)
    holdout_residual = residual_function(holdout)
    rng = np.random.default_rng(20260721)

    for attempt in range(16):
        start = np.zeros(54) if attempt == 0 else rng.normal(0, 0.35, 54)
        solution = least_squares(
            training_residual,
            start,
            method="trf",
            max_nfev=4000,
            ftol=1e-13,
            xtol=1e-13,
            gtol=1e-13,
            verbose=0,
        )
        train_error = float(np.max(np.abs(training_residual(solution.x))))
        holdout_error = float(np.max(np.abs(holdout_residual(solution.x))))
        print(
            f"attempt={attempt:02d} cost={solution.cost:.3e} "
            f"train={train_error:.3e} holdout={holdout_error:.3e} "
            f"norm={np.linalg.norm(solution.x):.3e}"
        )
        if max(train_error, holdout_error) > 1e-8:
            continue
        rationals = rationalize(solution.x)
        if rationals is None:
            print("  numerical identity found, but no small rational reconstruction")
            continue
        candidate, determinant = exact_candidate(rationals)
        print("  exact determinant:", determinant)
        if determinant == 1:
            print("CERTIFIED SIX-DIMENSIONAL CUBIC KELLER MAP")
            for component in candidate:
                print(sp.factor(component))
            return

    print("No exactly certified affine-correction solution found.")


if __name__ == "__main__":
    main()
