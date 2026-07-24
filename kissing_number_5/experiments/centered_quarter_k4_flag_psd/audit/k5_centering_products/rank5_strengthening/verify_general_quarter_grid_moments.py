#!/usr/bin/env python3
"""Dependency-free exact verifier for general (not necessarily centered)
41-point quarter-grid H1/H2 moment congruences.
"""

from __future__ import annotations

from math import isqrt
from typing import Iterable, Mapping


COLORS = tuple(range(-4, 3))
PAIR_TOTAL = 820
TRIPLE_TOTAL = 41 * 40 * 39 // 6
B = {color: 5 * color * color - 16 for color in COLORS}


def invariants(
    counts: Mapping[int, int],
    unordered_h2_products: Iterable[int] | None = None,
) -> dict[str, int]:
    if set(counts) != set(COLORS):
        raise ValueError(f"pair colors must be exactly {COLORS}")
    if any(
        not isinstance(counts[color], int) or counts[color] < 0
        for color in COLORS
    ):
        raise ValueError("pair multiplicities must be nonnegative integers")
    if sum(counts.values()) != PAIR_TOTAL:
        raise ValueError("pair multiplicities must sum to 820")

    a_sum = sum(color * counts[color] for color in COLORS)
    q = sum(color * color * counts[color] for color in COLORS)
    s = sum(counts[color] * B[color] ** 2 for color in COLORS)
    x1 = 5 * q - 11_808
    x2 = 7 * s - 1_133_568

    if (q - a_sum) % 2:
        raise AssertionError("Q and A must agree modulo two")
    if (x1 - 5 * a_sum - 2) % 10:
        raise AssertionError("general H1 selector failed")
    if (s - 10 - 15 * a_sum) % 30:
        raise AssertionError("general H2 S selector failed")
    if (x2 - 105 * a_sum - 82) % 210:
        raise AssertionError("general H2 X2 selector failed")
    if (x2 - 21 * x1 + 1050 * a_sum - 40) % 2100:
        raise AssertionError("joint H1/H2 selector failed")

    result = {
        "A": a_sum,
        "Q": q,
        "S": s,
        "X1": x1,
        "X2": x2,
    }
    if unordered_h2_products is None:
        return result

    products = tuple(unordered_h2_products)
    if len(products) != TRIPLE_TOTAL:
        raise ValueError(f"need exactly {TRIPLE_TOTAL} unordered products")
    if any(not isinstance(value, int) for value in products):
        raise ValueError("triple products must be integers")
    if any(value % 5 != 4 for value in products):
        raise ValueError("every raw H2 triple product must be 4 modulo 5")
    r = 6 * sum(products)
    y2 = 49 * r - 36_288 * s + 4_933_287_936
    if r % 30:
        raise AssertionError("R must be divisible by 30")
    if y2 % 210 != 66:
        raise AssertionError("general H2 Y2 selector failed")
    if (y2 - 10 * x2 - 2) % 49:
        raise AssertionError("joint H2 X2/Y2 selector failed")
    result.update({"R": r, "Y2": y2})
    return result


def endpoint_counts() -> dict[int, int]:
    return dict(zip(COLORS, (12, 35, 199, 40, 279, 0, 255)))


def r11_control_counts() -> tuple[dict[int, int], ...]:
    return (
        dict(zip(COLORS, (11, 41, 186, 54, 272, 0, 256))),
        dict(zip(COLORS, (11, 41, 186, 55, 271, 0, 256))),
    )


def h1_y_branches(q: int) -> tuple[int, ...]:
    x1 = 5 * q - 11_808
    if x1 < 0:
        return ()
    bound = isqrt(9 * x1**3 // 2)
    # The integer square-root bound may be one too small only if the
    # division by two discarded one half; test the endpoints explicitly
    # through the exact inequality below.
    while 2 * (bound + 1) ** 2 <= 9 * x1**3:
        bound += 1
    return tuple(
        y1
        for y1 in range(-bound, bound + 1)
        if (y1 + 432 * x1 + 1_464_192) % 75 == 0
        and 9 * x1**3 - 2 * y1**2 >= 0
    )


def self_test() -> None:
    for color in COLORS:
        numerator = B[color]
        if (color * color - color) % 2:
            raise AssertionError("pointwise H1 parity failed")
        if (numerator * numerator - 16 - 15 * color) % 30:
            raise AssertionError("pointwise H2 affine congruence failed")
        if (
            numerator * numerator
            - 15 * color * color
            + 150 * color
            - 256
        ) % 300:
            raise AssertionError("pointwise H1/H2 joint congruence failed")

    result = invariants(endpoint_counts())
    expected = {
        "A": -81,
        "Q": 2363,
        "S": 162115,
        "X1": 7,
        "X2": 1237,
    }
    if result != expected:
        raise AssertionError((result, expected))

    r11_expected = (
        {"A": -81, "Q": 2367, "S": 162775, "X1": 27, "X2": 5857},
        {"A": -82, "Q": 2368, "S": 162640, "X1": 32, "X2": 4912},
    )
    for counts, expected_result in zip(r11_control_counts(), r11_expected):
        observed = invariants(counts)
        if observed != expected_result:
            raise AssertionError((observed, expected_result))

    branch_table = {
        2362: (-6,),
        2363: (9,),
        2364: (-51, 24),
        2365: (-111, -36, 39, 114),
        2366: (-171, -96, -21, 54, 129, 204),
        2367: (-231, -156, -81, -6, 69, 144, 219, 294),
        2368: (-366, -291, -216, -141, -66, 9, 84, 159, 234, 309, 384),
    }
    for q, expected_branches in branch_table.items():
        observed_branches = h1_y_branches(q)
        if observed_branches != expected_branches:
            raise AssertionError((q, observed_branches, expected_branches))

    triple_result = invariants(
        endpoint_counts(),
        [64] * TRIPLE_TOTAL,
    )
    if triple_result["Y2"] % 210 != 66:
        raise AssertionError("endpoint control Y2 residue failed")

    wrong_total = endpoint_counts()
    wrong_total[0] -= 1
    try:
        invariants(wrong_total)
    except ValueError:
        pass
    else:
        raise AssertionError("wrong pair total was not rejected")

    bad_product = [64] * TRIPLE_TOTAL
    bad_product[0] = 65
    try:
        invariants(endpoint_counts(), bad_product)
    except ValueError:
        pass
    else:
        raise AssertionError("bad raw triple product was not rejected")


def main() -> None:
    self_test()
    result = invariants(endpoint_counts())
    print(
        "PASS: general quarter-grid moment lattice; "
        f"r12 A={result['A']}, X1={result['X1']}, X2={result['X2']}"
    )


if __name__ == "__main__":
    main()
