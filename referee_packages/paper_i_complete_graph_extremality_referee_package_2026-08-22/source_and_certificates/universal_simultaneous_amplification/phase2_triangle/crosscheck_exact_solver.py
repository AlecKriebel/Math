#!/usr/bin/env python3
"""Cross-check the triangle certificate against the project subset-state solver.

Unlike ``derive_certificate.py``, the reference implementation constructs all
eight subset-state transition rows literally from the dB rule.  This script
compares all six transient fixation probabilities, not only their average.
"""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from derive_certificate import (  # noqa: E402
    build_six_state_system,
    formula_difference,
    r,
    x,
    y,
)
from src.exact_markov import (  # noqa: E402
    average_single_mutant_fixation,
    complete_baseline,
    fixation_vector,
    transition_matrix,
)


def main() -> None:
    weights = ((0, 1, x), (1, 0, y), (x, y, 0))

    # Independent subset-state transition rows are exact and stochastic.
    rows = transition_matrix(weights, "dB", r)
    assert len(rows) == 8
    assert all(sp.cancel(sum(row.values()) - 1) == 0 for row in rows)

    reference = fixation_vector(weights, "dB", r)
    matrix, rhs = build_six_state_system(weights)
    manual = matrix.inv(method="DM") * rhs
    full = 0b111
    for vertex in range(3):
        singleton_mask = 1 << vertex
        doubleton_mask = full ^ singleton_mask
        assert sp.cancel(reference[singleton_mask] - manual[vertex, 0]) == 0
        assert sp.cancel(reference[doubleton_mask] - manual[3 + vertex, 0]) == 0

    rho_reference = average_single_mutant_fixation(weights, "dB", r)
    baseline_reference = complete_baseline(3, "dB", r)
    assert sp.cancel(baseline_reference - 2 * r / (3 * (r + 1))) == 0
    assert sp.cancel(rho_reference - baseline_reference - formula_difference(1, x, y)) == 0

    # Additional exact specializations exercise cancellation and signs without
    # floating point.  Uniform weights tie; every listed nonuniform case is strict.
    fitness_values = (sp.Rational(11, 10), sp.Rational(2), sp.Rational(17, 3))
    weight_values = (
        (sp.Rational(1), sp.Rational(1)),
        (sp.Rational(1, 2), sp.Rational(3)),
        (sp.Rational(2), sp.Rational(5, 3)),
        (sp.Rational(7, 4), sp.Rational(7, 4)),
    )
    for edge_x, edge_y in weight_values:
        for fitness in fitness_values:
            exact_value = sp.cancel(
                formula_difference(1, edge_x, edge_y).subs(r, fitness)
            )
            if edge_x == edge_y == 1:
                assert exact_value == 0
            else:
                assert exact_value < 0

    print("[INDEPENDENTLY VERIFIED] all eight subset-state transition rows sum exactly to one")
    print("[INDEPENDENTLY VERIFIED] all six transient fixation values match the manual system")
    print("[INDEPENDENTLY VERIFIED] the symbolic averaged difference matches the certificate")
    print("[EXACTLY CHECKED] rational specializations have the classified signs")


if __name__ == "__main__":
    main()
