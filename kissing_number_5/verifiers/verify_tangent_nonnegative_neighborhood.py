#!/usr/bin/env python3
"""Exact audit of the tangent nonnegative-neighborhood lemma."""

from __future__ import annotations

from fractions import Fraction as Q
import importlib.util
from pathlib import Path


ONE_SIDED_PATH = Path(__file__).with_name("verify_one_sided_tukey.py")
ONE_SIDED_SPEC = importlib.util.spec_from_file_location(
    "verify_one_sided_tukey_dependency", ONE_SIDED_PATH
)
assert ONE_SIDED_SPEC is not None and ONE_SIDED_SPEC.loader is not None
ONE_SIDED_MODULE = importlib.util.module_from_spec(ONE_SIDED_SPEC)
ONE_SIDED_SPEC.loader.exec_module(ONE_SIDED_MODULE)


def d_value(z: Q, w: Q) -> Q:
    return Q(1, 4) - z * z - w * w + 3 * z * w - 2 * z * z * w * w


def verify() -> dict[str, object]:
    # D is concave in w for every z in the relevant closed interval.
    # Its two endpoint polynomials have the factorizations in the proof.
    for numerator in range(101):
        z = Q(numerator, 200)
        assert -(1 + 2 * z * z) < 0
        assert d_value(z, Q(0)) == Q(1, 4) - z * z >= 0
        assert d_value(z, Q(1, 2)) == Q(3, 2) * z * (1 - z) >= 0

    # Exact values at every corner, including the two sharp mixed corners.
    assert d_value(Q(0), Q(0)) == Q(1, 4)
    assert d_value(Q(1, 2), Q(1, 2)) == Q(3, 8)
    assert d_value(Q(0), Q(1, 2)) == 0
    assert d_value(Q(1, 2), Q(0)) == 0

    imported = ONE_SIDED_MODULE.verify()
    assert imported["status"] == "PASS"
    assert imported["A_4_sqrt3_upper_bound"] == 33

    n = 41
    minimum_negative_degree = n - 34
    minimum_negative_edges = (n * minimum_negative_degree + 1) // 2
    assert minimum_negative_degree == 7
    assert minimum_negative_edges == 144

    hemisphere_n = 38
    hemisphere_minimum_degree = hemisphere_n - 34
    hemisphere_minimum_edges = (
        hemisphere_n * hemisphere_minimum_degree + 1
    ) // 2
    assert hemisphere_minimum_degree == 4
    assert hemisphere_minimum_edges == 76

    return {
        "status": "PASS",
        "projected_neighborhood_upper_bound": 33,
        "hypothetical_41_minimum_negative_degree": minimum_negative_degree,
        "hypothetical_41_minimum_negative_edges": minimum_negative_edges,
        "one_sided_38_minimum_negative_degree": hemisphere_minimum_degree,
        "one_sided_38_minimum_negative_edges": hemisphere_minimum_edges,
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
