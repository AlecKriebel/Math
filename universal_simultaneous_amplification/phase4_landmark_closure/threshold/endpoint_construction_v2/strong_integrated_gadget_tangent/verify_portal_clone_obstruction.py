#!/usr/bin/env python3
"""Exact certificate for the portal-clone equality/suppression class."""

from __future__ import annotations

import numpy as np
import sympy as sp

from integrated_gadget import tangent_coefficients


def main() -> None:
    r, x = sp.symbols("r x", positive=True)
    p = (r - 1) / r

    u_b = (r - 1) / (r - 1 + x)
    b_term = sp.factor(
        u_b / p - 1 + (r * x * u_b - (r - 1)) / (r - 1) ** 2
    )
    assert b_term == 0

    u_d = (r - 1) * x / (1 + (r - 1) * x)
    d_term = sp.factor(
        u_d / p - 1 + (r * u_d - (r - 1) * x) / (r - 1) ** 2
    )
    expected_d = -(x - 1) ** 2 / (1 + (r - 1) * x)
    assert sp.factor(d_term - expected_d) == 0

    # Independent numerical replay of the all-order sum for a nonuniform
    # rational portal vector at each requested hostile fitness.
    portal = np.array([0.2, 1.0, 3.0, 7.0])
    internal = np.zeros((len(portal), len(portal)))
    for fitness in (1.51, 1.55, 2.0):
        result = tangent_coefficients(internal, portal, fitness)
        expected = -sum(
            (value - 1.0) ** 2 / (1.0 + (fitness - 1.0) * value)
            for value in portal
        )
        assert abs(result.Bd) < 2e-13
        assert abs(result.dB - expected) < 2e-13

    print("portal-clone identity: Bd=0, dB=-sum (x_i-1)^2/(1+(r-1)x_i)")
    print("PASS exact strong integrated portal-clone obstruction")


if __name__ == "__main__":
    main()
