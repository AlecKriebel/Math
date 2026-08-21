#!/usr/bin/env python3
"""Numerically minimize the exact flat-kernel quartic.

Discovery only.  A negative direction printed here is not a result until
it is reconstructed over the rationals and checked by the exact verifier.
"""

from __future__ import annotations

import importlib.util
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
    term_data = []
    for exponent, coefficient in polynomial.terms():
        support = []
        for index, power in enumerate(exponent):
            support.extend([index] * power)
        assert len(support) == 4
        term_data.append((float(coefficient), tuple(support)))

    def value_gradient_on_sphere(raw):
        squared_norm = float(np.dot(raw, raw))
        if squared_norm < 1e-30:
            return 1e6, np.zeros_like(raw)
        inverse_norm = squared_norm**-0.5
        x = raw * inverse_norm
        value = 0.0
        gradient = np.zeros_like(x)
        for coefficient, support in term_data:
            product = coefficient
            for index in support:
                product *= x[index]
            value += product
            for position, index in enumerate(support):
                derivative = coefficient
                for other_position, other_index in enumerate(support):
                    if other_position != position:
                        derivative *= x[other_index]
                gradient[index] += derivative
        # Derivative through raw -> raw / ||raw||.
        gradient = inverse_norm * (gradient - 4.0 * value * x)
        return value, gradient

    starts = int(os.environ.get("N3_QUARTIC_STARTS", "100"))
    seed = int(os.environ.get("N3_QUARTIC_SEED", "370031"))
    rng = np.random.default_rng(seed)
    best = None
    for start in range(starts):
        initial = rng.normal(size=len(variables))
        result = minimize(
            value_gradient_on_sphere,
            initial,
            jac=True,
            method="L-BFGS-B",
            options={"maxiter": 3000, "ftol": 1e-14, "gtol": 1e-11},
        )
        x = result.x / np.linalg.norm(result.x)
        value, gradient = value_gradient_on_sphere(x)
        gradient_norm = np.linalg.norm(gradient)
        if best is None or value < best[0]:
            best = (value, gradient_norm, x.copy(), result.success)
            print(
                "start",
                start,
                "best",
                f"{value:.17g}",
                "tangent-gradient",
                f"{gradient_norm:.3g}",
                "success",
                result.success,
                flush=True,
            )
    assert best is not None
    value, gradient_norm, x, success = best
    print("minimum", repr(value))
    print("tangent-gradient", repr(gradient_norm))
    print("success", success)
    print("direction")
    for index, coordinate in enumerate(x):
        if abs(coordinate) > 1e-7:
            print(index, repr(float(coordinate)))


if __name__ == "__main__":
    main()
