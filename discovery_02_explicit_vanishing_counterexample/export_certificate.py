#!/usr/bin/env python3
"""Export the expanded quartic and collision as machine-readable JSON."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

from construction import degree_reduction, quartic_potential, symmetric_collision_points


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"


def encode_number(value):
    value = sp.expand(value)
    real, imag = value.as_real_imag()
    return {"real": str(real), "imag": str(imag)}


def main():
    reduction = degree_reduction()
    variables, potential = quartic_potential(reduction, expand=True)
    polynomial = sp.Poly(potential, *variables, extension=sp.I)
    points = symmetric_collision_points(reduction, 2)

    sparse = {
        "field": "Q(i)",
        "variables": [str(v) for v in variables],
        "degree": 4,
        "number_of_terms": len(polynomial.terms()),
        "terms": [
            {
                "powers": [
                    [index, exponent]
                    for index, exponent in enumerate(monomial)
                    if exponent
                ],
                "coefficient": encode_number(coefficient),
            }
            for monomial, coefficient in polynomial.terms()
        ],
    }
    collision = {
        "map": "Z - gradient(P)",
        "variables": [str(v) for v in variables],
        "points": [[encode_number(value) for value in point] for point in points],
    }

    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "potential_sparse.json").write_text(
        json.dumps(sparse, indent=2) + "\n", encoding="utf-8"
    )
    (OUTPUT / "collision.json").write_text(
        json.dumps(collision, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote {OUTPUT / 'potential_sparse.json'}")
    print(f"Wrote {OUTPUT / 'collision.json'}")


if __name__ == "__main__":
    main()
