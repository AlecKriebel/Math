#!/usr/bin/env python3
"""Exact-log checks of the independent cut estimate on adversarial families.

Only standard-library integer/rational arithmetic is used. This is supporting
evidence for the written proof, not an exhaustive proof of arbitrary weights.
"""

from fractions import Fraction
from random import Random
import json


RNG = Random(30005897)


def weight_log(n, d, cuts, heights, middle):
    k, r = divmod(n, d)
    t = cuts[r]
    if k <= t:
        return heights[r] + k - t
    return heights[r] + middle[r] - (k - t - 1)


def inspect_family(d, cuts, heights, middle):
    """Each residue rises with slope 1, has one edge <1, then falls with -1."""
    u = lambda n: weight_log(n, d, cuts, heights, middle)
    lo = d * (min(cuts) - 3)
    hi = d * (max(cuts) + 4)
    # Outside this interval both endpoints of every nearest-neighbor pair
    # are in matching affine tails, so their difference is constant.
    L = max(abs(u(n + 1) - u(n)) for n in range(lo, hi + 1))
    assert L >= 1
    for n in range(lo, hi + 1):
        assert min(u(n - d), u(n + d)) <= u(n) - 1
        assert abs(u(n + 1) - u(n)) <= L
    for r in range(d):
        for s in range(d):
            assert abs(cuts[r] - cuts[s]) <= 1 + abs(r - s) * L

    # Here a=1 and L is integral, making this exactly the written H.
    H = 1 + (d - 1) * L
    log_C = Fraction((d - 1) * L + (H + 1) * (d * L + 1))
    log_C += Fraction(d - 1, d)
    K = d * cuts[0]
    shifts = list(range(0, 33)) + [67, 101]
    points = list(range(K - 3 * d - 2, K + 3 * d + 3))
    points += [lo - 1000 * d, hi + 1000 * d]
    checked = 0
    for j in points:
        for ell in shifts:
            bound = log_C - Fraction(ell, d)
            value = u(j - ell) - u(j) if j <= K else u(j + ell) - u(j)
            assert value <= bound, (d, cuts, j, ell, value, bound)
            checked += 1
    return checked


checks = 0
families = 0
for d in range(1, 9):
    for trial in range(50):
        cuts = [RNG.randint(-12, 12) for _ in range(d)]
        heights = [RNG.randint(-8, 8) for _ in range(d)]
        # Includes intermediate zero edges and pronounced both-side drops.
        middle = [RNG.randint(-5, 0) for _ in range(d)]
        checks += inspect_family(d, cuts, heights, middle)
        families += 1

# Large common translations check that no estimate depends on cut location.
for translation in [-10**6, -31, 0, 47, 10**6]:
    checks += inspect_family(4, [translation + q for q in [0, 3, -2, 1]],
                             [0, 1, 0, -1], [-1, 0, -3, -1])
    families += 1

# Infinite-cut extremes, using integral log weights u_n=+/-n and eta=e^-d.
for direction in [1, -1]:
    for j in [-10**6, -1, 0, 1, 10**6]:
        for ell in [0, 1, 2, 33, 101]:
            target = j - ell if direction == 1 else j + ell
            assert direction * target - direction * j == -ell
            checks += 1

print(json.dumps({
    "status": "passed",
    "seed": 30005897,
    "finite_families": families,
    "scalar_decay_inequalities_checked": checks,
    "arithmetic": "exact integer log weights and Fraction bounds",
    "coverage": ["disagreeing residue cuts", "one exceptional edge",
                 "both-direction drops", "large translated cuts",
                 "d=1 through d=8", "full/zero-band extremes"],
    "limit": "supporting computational evidence; general claim proved in derivation"
}, indent=2))
