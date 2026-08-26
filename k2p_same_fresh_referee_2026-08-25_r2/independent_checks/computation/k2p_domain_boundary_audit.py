#!/usr/bin/env python3
"""Exact, submission-independent checks of the strict K2P D_plus inequalities."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from itertools import product


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def in_d_plus(s: Fraction, g: Fraction) -> bool:
    return 0 < s < 1 and 0 < g < 1 and g > 2 * s - 1


def probabilities(s: Fraction, g: Fraction):
    # Inverse Fourier transform for spectrum (1,s,g,s), character order
    # (0,C,G,T).  The equal nontrivial sector is C/T.
    return {
        "identity": (1 + 2 * s + g) / 4,
        "C": (1 - g) / 4,
        "G": (1 - 2 * s + g) / 4,
        "T": (1 - g) / 4,
    }


def main():
    denominators = (11, 37, 101, 1009)
    boundary = []
    for n in denominators:
        near_s_zero = (Fraction(1, n), Fraction(1, n + 1))
        near_g_zero = (Fraction(1, n), Fraction(1, n * n))
        near_g_one = (Fraction(n - 1, n), Fraction(n * n - 1, n * n))
        near_oblique = (Fraction(n - 1, n), Fraction(2 * n - 3, 2 * n))
        continuous = (
            Fraction(n - 1, n),
            Fraction((n - 1) ** 2, n * n) + Fraction(1, n**3),
        )
        for label, pair in (
            ("s_zero", near_s_zero),
            ("g_zero", near_g_zero),
            ("g_one", near_g_one),
            ("oblique", near_oblique),
            ("continuous", continuous),
        ):
            s, g = pair
            assert in_d_plus(s, g), (label, n, pair)
            probs = probabilities(s, g)
            assert sum(probs.values()) == 1
            assert all(value > 0 for value in probs.values())
            assert probs["C"] == probs["T"]
            if label == "continuous":
                assert s * s < g < 1
                assert g - (2 * s - 1) == (1 - s) ** 2 + Fraction(1, n**3)
            boundary.append(
                {
                    "family": label,
                    "n": n,
                    "s": str(s),
                    "g": str(g),
                    "oblique_gap": str(g - (2 * s - 1)),
                    "minimum_probability": str(min(probs.values())),
                }
            )

    grid = []
    for denominator in (7, 11):
        for i, j in product(range(1, denominator), repeat=2):
            s, g = Fraction(i, denominator), Fraction(j, denominator)
            strict_stochastic = all(value > 0 for value in probabilities(s, g).values())
            assert strict_stochastic == in_d_plus(s, g)
            if in_d_plus(s, g):
                grid.append((s, g))

    products_checked = 0
    for left, right in product(grid, repeat=2):
        s = left[0] * right[0]
        g = left[1] * right[1]
        assert in_d_plus(s, g), (left, right)
        products_checked += 1

    result = {
        "schema": "fresh-independent-k2p-domain-boundary-audit-v1",
        "status": "PASS",
        "spectrum": ["1", "s", "g", "s"],
        "equal_sector": ["C", "T"],
        "inverse_fourier_probabilities": {
            "identity": "(1+2s+g)/4",
            "C": "(1-g)/4",
            "G": "(1-2s+g)/4",
            "T": "(1-g)/4",
        },
        "strict_stochastic_iff_D_plus_grid_points": sum(
            (denominator - 1) ** 2 for denominator in (7, 11)
        ),
        "D_plus_grid_points": len(grid),
        "D_plus_product_pairs_checked": products_checked,
        "boundary_witnesses": boundary,
        "continuous_cone_implication": "g-s^2>0 and s^2-(2s-1)=(1-s)^2>0",
    }
    result["payload_sha256"] = hashlib.sha256(canonical(result)).hexdigest()
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
