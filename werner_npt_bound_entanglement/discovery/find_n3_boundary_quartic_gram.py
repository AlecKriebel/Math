#!/usr/bin/env python3
"""Search for a low-rank SOS Gram matrix for the flat-kernel quartic.

This is a discovery calculation.  It uses the exact polynomial but solves
the Gram equations numerically.  A successful output must be rationally
reconstructed and checked independently before it becomes a certificate.
"""

from __future__ import annotations

from collections import defaultdict
import importlib.util
import itertools
import os
from pathlib import Path

import numpy as np
from scipy.optimize import minimize


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "search_n3_boundary_quartic_sos.py"
SPEC = importlib.util.spec_from_file_location("quartic_source", SOURCE)
quartic_source = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(quartic_source)


def main() -> None:
    variables, polynomial = quartic_source.build_quartic()
    dimension = len(variables)
    coefficients = dict(polynomial.terms())

    active = []
    for index in range(dimension):
        exponent = [0] * dimension
        exponent[index] = 4
        if coefficients.get(tuple(exponent), 0):
            active.append(index)

    # If x_i^4=0 in an SOS, the x_i^2 Gram row vanishes.  Likewise, for
    # a cross monomial x_i x_j with at least one passive endpoint, a zero
    # x_i^2 x_j^2 coefficient forces that row to vanish.  These exact
    # zero-diagonal eliminations sharply reduce the numerical search.
    monomials = [(index, index) for index in active]
    active_set = set(active)
    for first, second in itertools.combinations(range(dimension), 2):
        exponent = [0] * dimension
        exponent[first] = exponent[second] = 2
        coefficient = coefficients.get(tuple(exponent), 0)
        if coefficient or (
            first in active_set and second in active_set
        ):
            monomials.append((first, second))
    monomials.sort()
    count = len(monomials)
    print("active squares", active)
    print("Gram monomials", count, flush=True)

    group_number = {}
    groups = []
    upper_first = []
    upper_second = []
    upper_group = []
    for first in range(count):
        for second in range(first, count):
            exponent = [0] * dimension
            for index in monomials[first]:
                exponent[index] += 1
            for index in monomials[second]:
                exponent[index] += 1
            exponent = tuple(exponent)
            if exponent not in group_number:
                group_number[exponent] = len(groups)
                groups.append(exponent)
            upper_first.append(first)
            upper_second.append(second)
            upper_group.append(group_number[exponent])

    upper_first = np.asarray(upper_first, dtype=np.int32)
    upper_second = np.asarray(upper_second, dtype=np.int32)
    upper_group = np.asarray(upper_group, dtype=np.int32)
    weights = np.where(upper_first == upper_second, 1.0, 2.0)
    target = np.zeros(len(groups))
    for group, exponent in enumerate(groups):
        target[group] = float(coefficients.get(exponent, 0))
    print("coefficient groups", len(groups), flush=True)

    rank = int(os.environ.get("N3_QUARTIC_GRAM_RANK", "12"))
    starts = int(os.environ.get("N3_QUARTIC_GRAM_STARTS", "4"))
    seed = int(os.environ.get("N3_QUARTIC_GRAM_SEED", "943031"))
    rng = np.random.default_rng(seed)

    def objective_gradient(flat):
        factor = flat.reshape(rank, count)
        gram = factor.T @ factor
        values = weights * gram[upper_first, upper_second]
        residual = (
            np.bincount(
                upper_group, weights=values, minlength=len(groups)
            )
            - target
        )
        objective = 0.5 * float(np.dot(residual, residual))
        derivative = np.zeros((count, count))
        entries = residual[upper_group]
        derivative[upper_first, upper_second] = entries
        derivative[upper_second, upper_first] = entries
        gradient = 2.0 * factor @ derivative
        return objective, gradient.ravel()

    best = None
    for start in range(starts):
        initial = rng.normal(scale=0.02, size=(rank, count))
        # Seed the six forced unit-norm active-square columns.
        for position, monomial in enumerate(monomials):
            if monomial[0] == monomial[1]:
                active_position = active.index(monomial[0])
                initial[active_position % rank, position] += 1.0
        result = minimize(
            objective_gradient,
            initial.ravel(),
            method="L-BFGS-B",
            jac=True,
            options={
                "maxiter": int(
                    os.environ.get("N3_QUARTIC_GRAM_MAXITER", "1500")
                ),
                "ftol": 1e-30,
                "gtol": 1e-11,
                "maxcor": 20,
            },
        )
        value, gradient = objective_gradient(result.x)
        gradient_norm = float(np.linalg.norm(gradient))
        print(
            "start",
            start,
            "residual-square/2",
            f"{value:.16g}",
            "gradient",
            f"{gradient_norm:.4g}",
            "iterations",
            result.nit,
            flush=True,
        )
        if best is None or value < best[0]:
            best = (value, gradient_norm, result.x.copy())

    assert best is not None
    value, gradient_norm, flat = best
    factor = flat.reshape(rank, count)
    print("best residual-square/2", repr(value))
    print("best gradient", repr(gradient_norm))
    np.savez_compressed(
        os.environ.get(
            "N3_QUARTIC_GRAM_OUTPUT", "/tmp/n3_boundary_quartic_gram.npz"
        ),
        factor=factor,
        monomials=np.asarray(monomials, dtype=np.int16),
        residual_square_over_two=value,
    )


if __name__ == "__main__":
    main()
