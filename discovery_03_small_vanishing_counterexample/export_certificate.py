#!/usr/bin/env python3
"""Export the 44-variable quartic and collision as exact sparse JSON."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

from construction import meng_potential, quartic_potential, symmetric_collision_points


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"


def encode_number(value):
    real, imag = sp.expand(value).as_real_imag()
    return {"real": str(real), "imag": str(imag)}


def main():
    meng_variables, meng_polynomial, meng_points = meng_potential()
    meng_sparse_polynomial = sp.Poly(
        meng_polynomial, *meng_variables, extension=sp.I
    )
    variables, potential = quartic_potential(expand=True)
    polynomial = sp.Poly(potential, *variables, extension=sp.I)
    points = symmetric_collision_points(2)

    sparse = {
        "field": "Q(i)",
        "variables": [str(variable) for variable in variables],
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
        "variables": sparse["variables"],
        "points": [[encode_number(value) for value in point] for point in points],
    }
    meng_sparse = {
        "field": "Q(i)",
        "variables": [str(variable) for variable in meng_variables],
        "degree": 8,
        "number_of_terms": len(meng_sparse_polynomial.terms()),
        "terms": [
            {
                "powers": [
                    [index, exponent]
                    for index, exponent in enumerate(monomial)
                    if exponent
                ],
                "coefficient": encode_number(coefficient),
            }
            for monomial, coefficient in meng_sparse_polynomial.terms()
        ],
    }
    meng_collision = {
        "map": "gradient(S)",
        "variables": meng_sparse["variables"],
        "points": [
            [encode_number(value) for value in point] for point in meng_points
        ],
    }

    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "potential_sparse.json").write_text(
        json.dumps(sparse, indent=2) + "\n", encoding="utf-8"
    )
    (OUTPUT / "collision.json").write_text(
        json.dumps(collision, indent=2) + "\n", encoding="utf-8"
    )
    (OUTPUT / "symmetric_potential_sparse.json").write_text(
        json.dumps(meng_sparse, indent=2) + "\n", encoding="utf-8"
    )
    (OUTPUT / "symmetric_collision.json").write_text(
        json.dumps(meng_collision, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote {OUTPUT / 'potential_sparse.json'} ({len(polynomial.terms())} terms)")
    print(f"Wrote {OUTPUT / 'collision.json'}")
    print(
        f"Wrote {OUTPUT / 'symmetric_potential_sparse.json'} "
        f"({len(meng_sparse_polynomial.terms())} terms)"
    )
    print(f"Wrote {OUTPUT / 'symmetric_collision.json'}")


if __name__ == "__main__":
    main()
