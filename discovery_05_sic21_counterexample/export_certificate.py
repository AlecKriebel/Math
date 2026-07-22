#!/usr/bin/env python3
"""Export the explicit SIC(21) witness as deterministic sparse JSON."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from construction import build_construction, evaluate, image_map


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "output" / "sic21_sparse.json"


def encode_number(value):
    value = sp.Rational(value)
    return str(value.p) if value.q == 1 else f"{value.p}/{value.q}"


def sparse(polynomial, variables):
    return [
        {"coefficient": encode_number(coefficient), "powers": list(monomial)}
        for monomial, coefficient in sp.Poly(polynomial, *variables).terms()
    ]


def main():
    data = build_construction()
    mapping = image_map(data)
    images = [evaluate(mapping, data.z_variables, point) for point in data.collision_points]
    assert images[0] == images[1] == images[2]

    payload = {
        "format": "sic21-sparse-certificate-v1",
        "field": "Q",
        "z_variables": [str(variable) for variable in data.z_variables],
        "xi_variables": [str(variable) for variable in data.xi_variables],
        "g": [sparse(component, data.z_variables) for component in data.g],
        "A": sparse(data.A, data.xi_variables + data.z_variables),
        "b_variable_index": 0,
        "collision_points": [
            [encode_number(coordinate) for coordinate in point]
            for point in data.collision_points
        ],
        "common_image": [encode_number(coordinate) for coordinate in images[0]],
    }
    serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(serialized, encoding="utf-8")
    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    print(f"wrote {OUTPUT.relative_to(HERE)}")
    print(f"sha256 {digest}")


if __name__ == "__main__":
    main()

