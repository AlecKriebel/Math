#!/usr/bin/env python3
"""Exact, independent one-dimensional falsification controls for PR15.

Uses integer sets only, no package installation and no source verifier.
Finite-hole certification comes from the proved endpoint criterion described
in REPORT.md, rather than a numerically chosen degree cutoff.
"""

from itertools import combinations
from math import gcd
from functools import reduce
import json
from pathlib import Path


def sumsets(a, degree):
    out = [{0}]
    for _ in range(degree):
        out.append({u + v for u in out[-1] for v in a})
    return out


def family_checks():
    out = []
    for m in range(4, 31):
        a = (0, 1, m - 1, m)
        layers = sumsets(a, m)
        hole_counts = []
        for k, layer in enumerate(layers):
            holes = set(range(k * m + 1)) - layer
            expected_count = k * (m - k - 2) if 1 <= k <= m - 3 else 0
            assert len(holes) == expected_count
            expected_layer = {
                j * (m - 1) + i
                for j in range(k + 1)
                for i in range(k + 1)
            }
            assert layer == expected_layer
            hole_counts.append(len(holes))
        h = max(k for k, count in enumerate(hole_counts) if count)
        assert h == m - 3
        out.append({"m": m, "highest_hole": h,
                    "reg_R_by_exact_cohomology_derivation": m - 2,
                    "reg_I_by_minimal_resolution_shift": m - 1,
                    "subtract_two_is_equality": h == (m - 1) - 2})
    return out


def interval_checks():
    totals = {"endpoint_subsets": 0, "intrinsic_gcd_one": 0,
              "finite_hole_configurations": 0,
              "finite_nonempty_hole_configurations": 0,
              "infinite_hole_witnesses": 0,
              "circuit_relations_checked": 0}
    max_by_volume = {}
    for v in range(1, 13):
        max_h = -1
        for mask in range(1 << (v - 1)):
            a = (0,) + tuple(i for i in range(1, v)
                             if mask & (1 << (i - 1))) + (v,)
            totals["endpoint_subsets"] += 1
            if reduce(gcd, a) != 1:
                continue
            totals["intrinsic_gcd_one"] += 1
            n, c = len(a), len(a) - 2
            assert c <= v - 1
            for left, middle, right in combinations(a, 3):
                delta = gcd(middle - left, right - middle)
                relation = ((right - middle) // delta,
                            -(right - left) // delta,
                            (middle - left) // delta)
                assert sum(relation) == 0
                assert left * relation[0] + middle * relation[1] + right * relation[2] == 0
                assert reduce(gcd, (abs(x) for x in relation)) == 1
                assert sum(x for x in relation if x > 0) <= v
                totals["circuit_relations_checked"] += 1
            finite = (1 in a and v - 1 in a)
            if not finite:
                totals["infinite_hole_witnesses"] += 1
                layers = sumsets(a, 5)
                for k in range(1, 6):
                    witness = 1 if 1 not in a else k * v - 1
                    assert witness not in layers[k]
                continue
            totals["finite_hole_configurations"] += 1
            layers = sumsets(a, max(v, 3))
            heights = []
            for k, layer in enumerate(layers):
                holes = set(range(k * v + 1)) - layer
                if holes:
                    heights.append(k)
                if k >= max(v - 2, 0):
                    assert not holes
            h = max(heights, default=-1)
            max_h = max(max_h, h)
            if heights:
                totals["finite_nonempty_hole_configurations"] += 1
                assert v >= 4  # stronger in dimension one than PR15's V >= 2
                assert n <= 2 * v * c
                assert h <= 2 * v * v * (v - 1) * (v - 1) - 2
                assert h <= v - 3
        max_by_volume[str(v)] = max_h
    return totals, max_by_volume


def controls():
    # Missing degree-one point 2 yields exactly C = k(-1) for A_4.
    a = (0, 1, 3, 4)
    layers = sumsets(a, 5)
    assert set(range(5)) - layers[1] == {2}
    assert all(set(range(4 * k + 1)) == layers[k] for k in range(2, 6))
    assert all(2 + u in layers[2] for u in a)
    assert 4 in layers[2]  # square of the missing monomial lies in R

    # A proper ambient index has no effect on intrinsic saturation.
    scaled = (0, 2, 6, 8)
    scaled_layers = sumsets(scaled, 5)
    for k in range(6):
        intrinsic = set(range(0, 8 * k + 1, 2))
        assert intrinsic - scaled_layers[k] == ({4} if k == 1 else set())
        if k:
            assert 1 not in scaled_layers[k]  # ambient hole in every degree

    # Height-one pyramid apex with an independent additional coordinate.
    pyramid = ((0, 0), (1, 0), (3, 0), (4, 0), (0, 1))
    points = {(0, 0)}
    for k in range(1, 9):
        points = {(x + a0, y + a1)
                  for x, y in points for a0, a1 in pyramid}
        assert (2, k - 1) not in points
        # It is in the cone in degree k: midpoint of (0,0) and (4,0)
        # at base degree 1 plus k-1 apex copies; it is in generated group.

    return {"A4_quotient": "one hole (2,1), annihilated by R_+",
            "proper_index": "scaled A4 has intrinsic V=4,h=1; ambient holes infinite",
            "free_pyramid": "(2,k-1,k) absent for k=1,...,8, with exact all-k proof in report",
            "V1_empty_holes": "free generated-group semigroup; theorem excludes nonempty case"}


if __name__ == "__main__":
    totals, maxima = interval_checks()
    result = {"arithmetic": "exact Python integers and finite sets",
              "scope": "one-dimensional controls, not a replacement for general proof",
              "totals": totals, "max_highest_hole_by_intrinsic_volume": maxima,
              "family": family_checks(), "controls": controls(), "passed": True}
    destination = Path(__file__).with_name("exact_checks.json")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"passed": True, "totals": totals,
                      "max_highest_hole_by_intrinsic_volume": maxima}, indent=2))
