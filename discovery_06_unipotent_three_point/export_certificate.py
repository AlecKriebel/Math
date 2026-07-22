#!/usr/bin/env python3
"""Export the Discovery 06 map as deterministic sparse JSON."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from construction import build_construction, evaluate, map_T


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "output" / "unipotent14_sparse.json"


def encode_number(value):
    value = sp.Rational(value)
    return str(value.p) if value.q == 1 else f"{value.p}/{value.q}"


def sparse(polynomial, variables):
    return [
        {"coefficient": encode_number(coefficient), "powers": list(monomial)}
        for monomial, coefficient in sp.Poly(polynomial, *variables).terms()
        if coefficient != 0
    ]


def main() -> None:
    data = build_construction()
    images = [
        evaluate(map_T(data), data.variables, point)
        for point in data.collision_points
    ]
    assert images[0] == images[1] == images[2]
    payload = {
        "format": "unipotent14-sparse-certificate-v1",
        "field": "Q",
        "variables": [str(variable) for variable in data.variables],
        "xi_variables": [str(variable) for variable in data.xi_variables],
        "chain_lengths": [2, 4, 5],
        "g": [sparse(component, data.variables) for component in data.g],
        "A": sparse(data.A, data.xi_variables + data.variables),
        "b_variable_indices": [0, 1, 3],
        "source_homogeneous_parts": [
            [sparse(component, data.base_variables) for component in part]
            for part in data.homogeneous_parts
        ],
        "collision_points": [
            [encode_number(coordinate) for coordinate in point]
            for point in data.collision_points
        ],
        "common_image": [encode_number(coordinate) for coordinate in images[0]],
        "sic_target": ["1/2", "0", "1"] + ["0"] * 11,
        "sic_coefficient_formula": {
            "3k": "(-1)^k*binom(3k+1,k)/2^(2k+1)",
            "3k+1": "(-1)^(k+1)*3*binom(3k+1,k)/((3k+1)*2^(2k+1))",
            "3k+2": "(-1)^k*binom(3k+4,k+1)/2^(2k+3)",
        },
    }
    serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(serialized, encoding="utf-8")
    digest = hashlib.sha256(serialized.encode()).hexdigest()
    print(f"wrote {OUTPUT.relative_to(HERE)}")
    print(f"sha256 {digest}")


if __name__ == "__main__":
    main()
