#!/usr/bin/env python3
"""Independent finite-difference check of the rare-satellite coefficients."""

from __future__ import annotations

import numpy as np

from search_branching_derivative import coefficients
from search_branching_satellites import survival


def check() -> None:
    fitness = 1.55
    delta = 0.37
    outer = np.array((0.2, 0.05, 0.11))
    center_degree = 2.3
    baseline = 1.0 - 1.0 / fitness
    expected = coefficients(fitness, delta, outer, center_degree)
    epsilon = 3.0e-6
    for rule in ("Bd", "dB"):
        finite = survival(
            fitness,
            delta,
            outer,
            center_degree,
            epsilon,
            rule,
        )[0]
        quotient = (finite - baseline) / epsilon
        error = abs(quotient - expected[rule][0])
        if error > 4.0e-6:
            raise AssertionError((rule, quotient, expected[rule][0], error))
        print(
            f"PASS {rule} derivative finite_difference={quotient:.12g} "
            f"formula={expected[rule][0]:.12g} error={error:.3g}"
        )


if __name__ == "__main__":
    check()
