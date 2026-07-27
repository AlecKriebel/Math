#!/usr/bin/env python3
"""Regenerate the compact machine-readable d=4 certificate.

This generator does not import the verifier.  It records the sparse monomial
data derived from the weighted-shift formulas in the manuscript.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

OUTPUT = Path(__file__).with_name("certificate.json")


def polar_phase_exponent(root_exponent: int) -> int:
    """Exponent e for (1+zeta^r)/|1+zeta^r|=zeta^e."""
    root_exponent %= 16
    if root_exponent == 8:
        raise ValueError("singular polar factor")
    if root_exponent < 8:
        return root_exponent // 2
    return (root_exponent // 2 + 8) % 16


def build_certificate() -> dict:
    order = [0, 1, 3, 2]
    equality_roots = [(4 * k + 2) % 16 for k in order]
    phase_rows = [
        [polar_phase_exponent((root_exponent + 4 * y) % 16) for root_exponent in equality_roots]
        for y in range(4)
    ]
    q_exponents = [0]
    for exponent in equality_roots[:-1]:
        q_exponents.append((q_exponents[-1] + exponent) % 16)
    probability_table = [
        ["1/32" if (a + b) % 2 == 0 else "3/32" for b in range(4)]
        for a in range(4)
    ]
    return {
        "schema": "cyclic-bell-randomness-counterexample/v2",
        "claim": {
            "dimension": 4,
            "augmented_bell_value": "2*csc(pi/8)+1",
            "target_settings": {"alice": 1, "bob": 4},
            "guessing_probability": "3/32",
            "uniform_benchmark": "1/16",
            "strict_gap": "1/32",
        },
        "field": {
            "name": "Q(zeta_16)",
            "generator": "zeta",
            "interpretation": "zeta=exp(pi*i/8)",
            "minimal_polynomial": "zeta^8+1",
        },
        "spaces": {"H_A": 4, "H_B": 4, "H_E": 1},
        "state": {"name": "Phi_4", "formula": "(1/2)*sum_{j=0}^3 |j,j>"},
        "weighted_shift_encoding": {
            "convention": "X|j>=|j+1 mod 4>; X*diag(zeta^e_j) has weight exponents e_j",
            "phase_order_kappa": order,
            "equality_phase_exponents_in_kappa_order": equality_roots,
            "A0_weight_exponents": [0, 0, 0, 0],
            "A1_weight_exponents": equality_roots,
            "V_y_weight_exponents": phase_rows,
            "B_y_weight_exponents": [[(-entry) % 16 for entry in row] for row in phase_rows],
            "B4_weight_exponents": [0, 0, 0, 0],
        },
        "fourier_certificate": {
            "q_exponents": q_exponents,
            "definition": "q_0=1; q_{j+1}=z_{kappa_j} q_j",
            "qhat_definition": "qhat_m=sum_j q_j*i^(m*j)",
            "qhat_squared_magnitudes": [2, 6, 2, 6],
        },
        "target_probability_table": probability_table,
        "checks_required": [
            "A0,A1,B0,...,B4 are unitary",
            "A0^4=A1^4=B0^4=...=B4^4=I",
            "A0+i^y*A1=V_y*H_y with H_y strictly positive",
            "the original Bell expression equals 2*csc(pi/8)+1 on Phi_4",
            "the projector calculation equals the displayed rational probability table",
            "the independent Fourier calculation has squared magnitudes 2,6,2,6",
            "both one-party marginals equal 1/4",
            "the optimal trivial-Eve guess is 3/32>1/16",
        ],
        "verifier": "verify_exact.py",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    args.output.write_text(json.dumps(build_certificate(), indent=2) + "\n")
    print(args.output)


if __name__ == "__main__":
    main()
