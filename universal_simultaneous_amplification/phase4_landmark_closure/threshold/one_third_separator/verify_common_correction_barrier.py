#!/usr/bin/env python3
"""Exact Farkas barrier to a pointwise common-correction proof.

For the one-third affine target, a tempting sufficient certificate is a
function ``h`` on transient mutant sets, zero at both absorbing states, with

    L_B (phi_B/rho_B(K_n) + 2h) <= 0,
    2 L_D (phi_D/rho_D(K_n) - h) <= 0.

The initial corrections cancel in ``e_B+2e_D``.  On the four-vertex star
with edge weights 1,10,100, however, the two systems are jointly infeasible
even when ``h`` is an arbitrary function on all fourteen transient sets.
This verifier gives an exact seven-atom rational Farkas certificate.

The graph itself satisfies the affine separator strictly.  Thus this file
closes only the pointwise common-potential architecture.
"""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve()
HOSTILE = HERE.parents[1] / "endpoint_hostile_exact"
sys.path.insert(0, str(HOSTILE))

import verify_balanced_poisson as poisson  # noqa: E402
from verify_endpoint_candidates import (  # noqa: E402
    complete_baseline,
    exact_fixation,
    graph,
)


def system():
    weights = graph(4, [(0, 1, 1), (0, 2, 10), (0, 3, 100)])
    n = 4
    full = (1 << n) - 1
    states = list(range(1, full))
    index = {state: column for column, state in enumerate(states)}
    rows = []
    rhs = []
    labels = []

    for rule, drift_weight, correction_weight in (
        ("Bd", sp.Integer(1), sp.Integer(2)),
        ("dB", sp.Integer(2), sp.Integer(-2)),
    ):
        phi = poisson.harmonics(n, rule)
        baseline = complete_baseline(n, rule)
        for state in states:
            row = [sp.Integer(0)] * len(states)
            normalized_drift = sp.cancel(
                drift_weight
                * poisson.harmonic_drift(weights, state, rule, phi)
                / baseline
            )
            for target, rate in poisson.changing_rates(weights, state, rule):
                if target not in (0, full):
                    row[index[target]] += correction_weight * rate
                row[index[state]] -= correction_weight * rate
            rows.append(list(map(sp.cancel, row)))
            rhs.append(sp.cancel(-normalized_drift))
            labels.append((rule, state))
    return weights, labels, sp.Matrix(rows), sp.Matrix(rhs)


def main():
    weights, labels, matrix, rhs = system()

    atoms = {
        ("Bd", 0b1000): sp.Rational(12191450440535, 45112766875736),
        ("Bd", 0b1001): sp.Rational(7430283174771, 22556383437868),
        ("Bd", 0b1011): sp.Rational(4193038067845, 473684052195228),
        ("Bd", 0b1101): sp.Rational(82921712801, 135338300627208),
        ("dB", 0b1001): sp.Rational(5653839339077, 38668085893488),
        ("dB", 0b1011): sp.Rational(270870259182787, 1894736208780912),
        ("dB", 0b1101): sp.Rational(6882502162483, 67669150313604),
    }
    dual = sp.Matrix([atoms.get(label, 0) for label in labels])
    assert all(value >= 0 for value in dual)
    assert sum(dual) == 1
    assert dual.T * matrix == sp.zeros(1, matrix.cols)
    defect = sp.cancel((dual.T * rhs)[0])
    assert defect == -sp.Rational(202911350726485, 1421052156585684) < 0

    # If matrix*h <= rhs held, multiplication by the nonnegative ``dual``
    # would give 0 <= defect, contradicting the certified strict sign.
    rho_b = exact_fixation(weights, "Bd")
    rho_d = exact_fixation(weights, "dB")
    x = sp.cancel(rho_b / complete_baseline(4, "Bd"))
    y = sp.cancel(rho_d / complete_baseline(4, "dB"))
    slack = sp.cancel(1 - (x + 2 * y) / 3)
    assert slack > 0

    print("PASS exact seven-atom Farkas certificate")
    print(f"dual defect = {defect}")
    print(f"actual one-third slack = {slack}")
    print("PASS graph obeys separator; only the common-correction route fails")


if __name__ == "__main__":
    main()
