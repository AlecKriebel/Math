#!/usr/bin/env python3
"""Exact checks for proofs/d5_saturation.md.

The universal step in the manuscript is a short symbolic inequality.  This
verifier checks its polynomial identity exactly, as well as all finite claims
about the D5 roots.  It uses only Python's standard library.
"""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import combinations, product
from typing import Iterable


Vector = tuple[int, int, int, int, int]


def dot(x: Iterable[int], y: Iterable[int]) -> int:
    return sum(a * b for a, b in zip(x, y))


def d5_roots() -> tuple[Vector, ...]:
    """Return the 40 unnormalized roots +/-e_i +/-e_j."""
    roots: list[Vector] = []
    for i, j in combinations(range(5), 2):
        for sign_i, sign_j in product((-1, 1), repeat=2):
            coordinates = [0] * 5
            coordinates[i] = sign_i
            coordinates[j] = sign_j
            roots.append(tuple(coordinates))  # type: ignore[arg-type]
    return tuple(roots)


def verify_root_configuration() -> dict[str, object]:
    """Check cardinality, norms, and the exact distinct-pair bound."""
    roots = d5_roots()
    assert len(roots) == 40
    assert len(set(roots)) == 40
    assert all(dot(root, root) == 2 for root in roots)

    distinct_inner_products = [
        dot(roots[i], roots[j])
        for i, j in combinations(range(len(roots)), 2)
    ]
    assert set(distinct_inner_products) == {-2, -1, 0, 1}
    assert max(distinct_inner_products) == 1

    # Dividing both roots by sqrt(2) divides their inner product by 2.
    normalized_max = Fraction(max(distinct_inner_products), 2)
    assert normalized_max == Fraction(1, 2)

    return {
        "root_count": len(roots),
        "unnormalized_norm_squared": 2,
        "unnormalized_distinct_inner_products": sorted(
            set(distinct_inner_products)
        ),
        "normalized_max_distinct_inner_product": str(normalized_max),
    }


def verify_universal_inequality_identity() -> dict[str, object]:
    """Check the coefficient identity used for a >= b >= 0.

    Coefficients are stored in the order (a^2, ab, b^2).
    """
    five_fourths_square = (
        Fraction(5, 4),
        Fraction(5, 2),
        Fraction(5, 4),
    )
    a_squared_plus_four_b_squared = (
        Fraction(1),
        Fraction(0),
        Fraction(4),
    )
    difference = tuple(
        left - right
        for left, right in zip(
            five_fourths_square,
            a_squared_plus_four_b_squared,
        )
    )

    # (a-b)(a+11b)/4 = (a^2 + 10ab - 11b^2)/4.
    factored = (
        Fraction(1, 4),
        Fraction(10, 4),
        Fraction(-11, 4),
    )
    assert difference == factored

    return {
        "coefficient_order": ["a^2", "ab", "b^2"],
        "difference_coefficients": [str(value) for value in difference],
        "factorization": "(a-b)(a+11b)/4",
        "sign_condition": "nonnegative when a >= b >= 0",
    }


def verify_sharp_constant() -> dict[str, object]:
    """Check the all-equal witness and the strict gap above 1/2."""
    roots = d5_roots()

    # For y=(1,1,1,1,1)/sqrt(5) and x=root/sqrt(2),
    # <x,y> = sum(root coordinates)/sqrt(10).
    numerators = [sum(root) for root in roots]
    max_numerator = max(numerators)
    assert max_numerator == 2

    lower_bound_squared = Fraction(max_numerator**2, 10)
    kissing_threshold_squared = Fraction(1, 4)
    strict_squared_gap = lower_bound_squared - kissing_threshold_squared
    assert lower_bound_squared == Fraction(2, 5)
    assert strict_squared_gap == Fraction(3, 20)
    assert strict_squared_gap > 0

    return {
        "sharp_witness": "(1,1,1,1,1)/sqrt(5)",
        "saturation_lower_bound_squared": str(lower_bound_squared),
        "kissing_threshold_squared": str(kissing_threshold_squared),
        "strict_squared_gap": str(strict_squared_gap),
    }


def main() -> None:
    report = {
        "claim": "fixed D5 is saturated against adding one point",
        "arithmetic": "exact integers and fractions",
        "root_configuration": verify_root_configuration(),
        "universal_identity": verify_universal_inequality_identity(),
        "sharp_constant": verify_sharp_constant(),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
