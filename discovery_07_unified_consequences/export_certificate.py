#!/usr/bin/env python3
"""Export the compact unified every-order certificate as deterministic JSON."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from construction import (
    ROOT,
    WEIGHTS_14,
    d3_quartic_data,
    d6_direct_data,
    d6_homogeneous_data,
    symmetrized_potential,
)


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "output" / "unified_every_order.json"
D3_CERTIFICATE = ROOT / "discovery_03_small_vanishing_counterexample" / "output" / "potential_sparse.json"
D6_CERTIFICATE = ROOT / "discovery_06_unipotent_three_point" / "output" / "unipotent14_sparse.json"


def encode_rational(value) -> str:
    value = sp.Rational(value)
    return str(value.p) if value.q == 1 else f"{value.p}/{value.q}"


def encode_complex(value):
    real, imaginary = sp.expand_complex(value).as_real_imag()
    return [encode_rational(real), encode_rational(imaginary)]


def sparse(polynomial, variables):
    return [
        {"coefficient_qi": encode_complex(coefficient), "powers": list(monomial)}
        for monomial, coefficient in sp.Poly(polynomial, *variables).terms()
        if coefficient != 0
    ]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    direct = d6_direct_data()
    homogeneous = d6_homogeneous_data()
    quartic = d3_quartic_data()
    variables28, potential28 = symmetrized_potential(direct, "c", "d")
    variables30, potential30 = symmetrized_potential(homogeneous, "a", "b")

    payload = {
        "format": "unified-every-order-certificate-v1",
        "field": "Q(i)",
        "precursors": {
            "quartic44": {
                "path": "../discovery_03_small_vanishing_counterexample/output/potential_sparse.json",
                "sha256": sha256(D3_CERTIFICATE),
                "variables": 44,
                "degree": 4,
                "terms": 538,
            },
            "unipotent14": {
                "path": "../discovery_06_unipotent_three_point/output/unipotent14_sparse.json",
                "sha256": sha256(D6_CERTIFICATE),
                "variables": 14,
                "terms": 24,
            },
        },
        "unipotent14": {
            "weights": list(WEIGHTS_14),
            "fiber_groebner_variable_order": ["z", "y", "x"],
            "fiber_groebner_basis": [
                "-27*x^2+4*z+1",
                "3*x+2*y",
                "x^3-x",
            ],
            "homogeneous_jordan_type": [14, 1],
        },
        "inverse_series": {
            "equation": "tau+t*tau^3=t/2",
            "q_observable": "x+y+u11",
            "q_target14": [encode_rational(value) for value in direct.target],
            "q_coefficients": {
                "3k": "(-1)^k*binom(3k+1,k)/2^(2k+1)",
                "3k+1": "(-1)^(k+1)*3*binom(3k+1,k)/((3k+1)*2^(2k+1))",
                "3k+2": "(-1)^k*binom(3k+4,k+1)/2^(2k+3)",
            },
            "r_observable": "x+y+g3a",
            "r_target22": [encode_rational(value) for value in quartic.target],
            "r_coefficients": {
                "3k": "(-1)^k*binom(3k+1,k)/2^(2k+1)",
                "3k+1": "(-1)^(k+1)*3*binom(3k+1,k)/((3k+1)*2^(2k+1))",
                "3k+2": "(-1)^k*3*binom(3k+2,k)/2^(2k+2)",
            },
        },
        "companions": {
            "nonhomogeneous28": {
                "variables": [str(variable) for variable in variables28],
                "degree_min": 2,
                "degree_max": 8,
                "number_of_terms": 178,
                "terms": sparse(potential28, variables28),
            },
            "homogeneous30": {
                "variables": [str(variable) for variable in variables30],
                "degree": 8,
                "number_of_terms": 608,
                "inverse_target15": [encode_rational(value) for value in homogeneous.target],
                "terms": sparse(potential30, variables30),
            },
        },
    }
    serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(serialized, encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(HERE)}")
    print(f"sha256 {hashlib.sha256(serialized.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
