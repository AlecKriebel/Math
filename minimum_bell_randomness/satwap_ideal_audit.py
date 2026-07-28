#!/usr/bin/env python3
"""First-principles audit of the standard two-setting Fourier-phase strategy.

This program does not optimize a Bell score.  It computes the four ideal
joint probability tables on |Phi_d>.  The source convention

    theta = (1/4, 3/4), zeta = (1/2, 1)

gives offsets zeta_y-theta_x equal to

    ((1/4, 3/4), (-1/4, 1/4)).

This is equivalent to the common alpha=(0,1/2),
beta=(1/4,-1/4) presentation by input/output relabeling.  The script checks
the closed formula, tests whether any input pair is uniform, and checks the
cross table produced by perfectly anchoring a third Bob measurement to one
Alice basis.  Only the Python standard library is used.
"""

from __future__ import annotations

import cmath
import math


def geometric_probability(d: int, delta: float, a: int, b: int) -> float:
    """Direct Born probability from the finite geometric amplitude."""
    omega = cmath.exp(2j * math.pi / d)
    amplitude = sum(
        omega ** (-j * (a - b + delta)) for j in range(d)
    ) / (d * math.sqrt(d))
    return abs(amplitude) ** 2


def closed_probability(d: int, delta: float, a: int, b: int) -> float:
    """Closed Dirichlet-kernel formula for the same probability."""
    numerator = math.sin(math.pi * delta) ** 2
    denominator = (
        d**3 * math.sin(math.pi * (a - b + delta) / d) ** 2
    )
    return numerator / denominator


def table(d: int, delta: float) -> list[list[float]]:
    return [
        [closed_probability(d, delta, a, b) for b in range(d)]
        for a in range(d)
    ]


def max_abs_difference(
    left: list[list[float]], right: list[list[float]]
) -> float:
    return max(
        abs(left[a][b] - right[a][b])
        for a in range(len(left))
        for b in range(len(left))
    )


def audit_dimension(d: int) -> tuple[float, float, float, float]:
    deltas = ((0.25, 0.75), (-0.25, 0.25))
    tables: dict[tuple[int, int], list[list[float]]] = {}
    formula_error = 0.0
    marginal_error = 0.0

    for x in range(2):
        for y in range(2):
            delta = deltas[x][y]
            current = table(d, delta)
            tables[x, y] = current
            for a in range(d):
                for b in range(d):
                    formula_error = max(
                        formula_error,
                        abs(
                            current[a][b]
                            - geometric_probability(d, delta, a, b)
                        ),
                    )
            for a in range(d):
                marginal_error = max(
                    marginal_error,
                    abs(sum(current[a]) - 1 / d),
                )
            for b in range(d):
                marginal_error = max(
                    marginal_error,
                    abs(sum(current[a][b] for a in range(d)) - 1 / d),
                )

    # Input-pair equivalences by transpose and cyclic output relabeling.
    transpose_00 = [
        [tables[0, 0][b][a] for b in range(d)] for a in range(d)
    ]
    assert max_abs_difference(tables[1, 0], transpose_00) < 2e-12
    shifted_transpose_00 = [
        [transpose_00[a][(b - 1) % d] for b in range(d)]
        for a in range(d)
    ]
    assert (
        max_abs_difference(tables[0, 1], shifted_transpose_00)
        < 2e-12
    )
    assert max_abs_difference(tables[1, 1], tables[0, 0]) < 2e-12

    predicted_max = 1 / (
        2 * d**3 * math.sin(math.pi / (4 * d)) ** 2
    )
    predicted_min = 1 / (
        2 * d**3 * math.cos(math.pi / (4 * d)) ** 2
    )
    observed = [entry for current in tables.values() for row in current for entry in row]
    assert abs(max(observed) - predicted_max) < 2e-12
    assert abs(min(observed) - predicted_min) < 2e-12
    assert predicted_max > 1 / d**2
    assert formula_error < 2e-12
    assert marginal_error < 2e-12

    # If a third Bob measurement is perfectly matched to either Alice basis,
    # its cross table with the other Alice basis has a half-step offset.
    cross = [
        [
            1
            / (
                d**3
                * math.sin(math.pi * (a - b + 0.5) / d) ** 2
            )
            for b in range(d)
        ]
        for a in range(d)
    ]
    cross_max = 1 / (
        d**3 * math.sin(math.pi / (2 * d)) ** 2
    )
    assert abs(max(entry for row in cross for entry in row) - cross_max) < 2e-12
    for a in range(d):
        assert abs(sum(cross[a]) - 1 / d) < 2e-12
    if d == 2:
        assert max(
            abs(entry - 1 / d**2) for row in cross for entry in row
        ) < 2e-12
    else:
        assert cross_max > 1 / d**2

    return (
        predicted_max,
        predicted_min,
        -math.log2(predicted_max),
        cross_max,
    )


def main() -> None:
    for d in range(2, 11):
        p_max, p_min, entropy, cross_max = audit_dimension(d)
        print(
            f"PASS d={d}: "
            f"p_max={p_max:.12f}, "
            f"p_min={p_min:.12f}, "
            f"H_min={entropy:.12f}, "
            f"cross_max={cross_max:.12f}"
        )
    print("PASS: no ideal input pair is uniform for d=2,...,10")
    print("PASS: naive third-setting cross pair is uniform only for d=2")


if __name__ == "__main__":
    main()
