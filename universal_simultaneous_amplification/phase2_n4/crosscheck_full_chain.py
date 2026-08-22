#!/usr/bin/env python3
"""Independent full-subset-state checks for the Phase-2 n=4 certificates."""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp


class CertificateFailure(RuntimeError):
    """Raised when an explicit certificate check fails."""


def require(condition, detail="certificate check failed"):
    """Raise a failure that remains active under optimized Python."""
    if not condition:
        raise CertificateFailure(str(detail))


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from derive_lumped_certificates import (  # noqa: E402
    baseline_k4,
    r,
    solve_average,
    x,
    y,
)
from src.exact_markov import (  # noqa: E402
    average_single_mutant_fixation,
    check_lumping,
    transition_matrix,
)


def weights_13(satellite_weight: sp.Expr):
    return tuple(
        tuple(
            0
            if i == j
            else (1 if i == 0 or j == 0 else satellite_weight)
            for j in range(4)
        )
        for i in range(4)
    )


def weights_22(internal_a: sp.Expr, internal_b: sp.Expr):
    return (
        (0, internal_a, 1, 1),
        (internal_a, 0, 1, 1),
        (1, 1, 0, internal_b),
        (1, 1, internal_b, 0),
    )


def orbit_cells(p: int, q: int):
    cells = []
    first_mask = (1 << p) - 1
    second_mask = ((1 << q) - 1) << p
    for i in range(p + 1):
        for j in range(q + 1):
            cells.append(
                tuple(
                    mask
                    for mask in range(1 << (p + q))
                    if (mask & first_mask).bit_count() == i
                    and (mask & second_mask).bit_count() == j
                )
            )
    return cells


def solve_quotient_average(quotient, p: int, q: int):
    all_states = [(i, j) for i in range(p + 1) for j in range(q + 1)]
    cell_index = {state: location for location, state in enumerate(all_states)}
    transient = [state for state in all_states if state not in ((0, 0), (p, q))]
    index = {state: location for location, state in enumerate(transient)}
    matrix = sp.zeros(len(transient), len(transient))
    rhs = sp.zeros(len(transient), 1)
    for state in transient:
        row = index[state]
        matrix[row, row] = 1
        source = cell_index[state]
        for target in transient:
            matrix[row, index[target]] -= quotient[source][cell_index[target]]
        rhs[row, 0] = quotient[source][cell_index[(p, q)]]
    solution = tuple(next(iter(sp.linsolve((matrix, rhs)))))
    return sp.cancel(
        (p * solution[index[(1, 0)]] + q * solution[index[(0, 1)]]) / (p + q)
    )


def main() -> None:
    # Symbolic strong-lumpability and quotient-solve checks.
    cases = (
        (1, 3, weights_13(x), solve_average(1, 3, 0, x, 1)[0]),
        (2, 2, weights_22(x, y), solve_average(2, 2, x, y, 1)[0]),
    )
    for p, q, weights, manual_rho in cases:
        rows = transition_matrix(weights, "dB", r)
        require(all(sp.cancel(sum(row.values()) - 1) == 0 for row in rows))
        quotient = check_lumping(rows, orbit_cells(p, q))
        quotient_rho = solve_quotient_average(quotient, p, q)
        require(sp.cancel(quotient_rho - manual_rho) == 0)

    # Full 14-transient-state solves at exact rational weight specializations.
    specializations = (
        (weights_13(sp.Rational(5, 2)), solve_average(1, 3, 0, sp.Rational(5, 2), 1)[0]),
        (weights_13(sp.Rational(2, 5)), solve_average(1, 3, 0, sp.Rational(2, 5), 1)[0]),
        (weights_22(sp.Rational(2), sp.Rational(3)), solve_average(2, 2, 2, 3, 1)[0]),
        (
            weights_22(sp.Rational(1, 3), sp.Rational(7, 2)),
            solve_average(2, 2, sp.Rational(1, 3), sp.Rational(7, 2), 1)[0],
        ),
    )
    for weights, expected in specializations:
        actual = average_single_mutant_fixation(weights, "dB", r)
        require(sp.cancel(actual - expected) == 0)
        difference = sp.cancel(actual - baseline_k4())
        numerator, denominator = sp.fraction(difference)
        # Exact Sturm-free specialization certificate after r=1+z: the reduced
        # numerator is negative and denominator positive coefficientwise.
        z = sp.symbols("z", positive=True)
        signed_numerator = sp.Poly(sp.expand(-numerator.subs(r, 1 + z)), z)
        positive_denominator = sp.Poly(sp.expand(denominator.subs(r, 1 + z)), z)
        require(all(coefficient >= 0 for coefficient in signed_numerator.all_coeffs()))
        require(any(coefficient > 0 for coefficient in signed_numerator.all_coeffs()))
        require(all(coefficient > 0 for coefficient in positive_denominator.all_coeffs()))

    print("[INDEPENDENTLY VERIFIED] full transition rows are exactly stochastic")
    print("[INDEPENDENTLY VERIFIED] both count partitions are strongly lumpable symbolically")
    print("[INDEPENDENTLY VERIFIED] quotient solutions match both manual orbit chains")
    print("[INDEPENDENTLY VERIFIED] four full 14-state rational-weight solves match exactly")
    print("[EXACTLY CERTIFIED] specialized differences are negative for every r>1")


if __name__ == "__main__":
    main()
