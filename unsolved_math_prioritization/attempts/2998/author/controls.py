#!/usr/bin/env python3
"""Exact finite sanity checks, not a proof of branched-cover realizability."""
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path


def partitions(n, least=1):
    if n == 0:
        yield ()
    for k in range(least, n + 1):
        for tail in partitions(n - k, k):
            yield (k,) + tail


def defect(cycles):
    return sum(k - 1 for k in cycles)


def weight(cycles):
    return sum((Q(k * k - 1, 3 * k) for k in cycles), Q(0))


def invariants(chis, es, profiles):
    assert len(chis) == len(es) == len(profiles)
    d = sum(profiles[0])
    assert all(sum(p) == d for p in profiles)
    return (2 * d - sum(defect(p) * c for c, p in zip(chis, profiles)),
            -sum((e * weight(p) for e, p in zip(es, profiles)), Q(0)))


def main():
    counts = {"partition_profiles": 0, "euler_inequalities": 0,
              "same_sign_pairs": 0, "two_nonorientable_euler_bounds": 0,
              "degree_growth_bounds": 0}
    # All partitions of d <= 18: no floating point and no random sampling.
    for d in range(1, 19):
        for p in partitions(d):
            r = defect(p)
            a = weight(p)
            counts["partition_profiles"] += 1
            assert r == d - len(p)
            assert 0 <= r <= d - 1
            assert (a == 0) == (r == 0)
            assert Q(r, 3) <= a <= Q(r, 2)
            # The equality on the right is characteristic of indices <= 2.
            assert (a == Q(r, 2)) == all(k <= 2 for k in p)
    # The Euler bound is tested for all defect vectors and Euler tuples
    # in this finite box. Every such vector is an arithmetic relaxation.
    for d in range(2, 10):
        for chis in product(range(-2, 3), repeat=3):
            pos = sum(max(c, 0) for c in chis)
            for rs in product(range(1, d), repeat=3):
                chi = 2 * d - sum(r * c for r, c in zip(rs, chis))
                assert chi >= (2 - pos) * d + pos
                counts["euler_inequalities"] += 1
    # Signature cannot cancel if all nonzero normal Euler numbers share a sign.
    for d in range(2, 10):
        ps = [p for p in partitions(d) if defect(p)]
        for p, q in product(ps, repeat=2):
            for es in [(2, 2), (-2, -2), (0, 2), (0, -2)]:
                sig = -(es[0] * weight(p) + es[1] * weight(q))
                assert sig != 0
                counts["same_sign_pairs"] += 1
        # Any two closed nonorientable components have chi_i <= 1.
        for x, y in product(range(-4, 2), repeat=2):
            for p, q in product(ps, repeat=2):
                chi, _ = invariants((x, y), (2, -2), (p, q))
                assert chi >= 2
                counts["two_nonorientable_euler_bounds"] += 1
    # Controls distinguishing simple branching from index-two-only branching.
    assert defect((2, 1, 1)) == 1
    assert defect((2, 2)) == 2
    assert weight((2, 1, 1)) == Q(1, 2)
    assert weight((2, 2)) == Q(1)
    # Numerical normalization: chi(S)=1, e(S)=-2, degree two.
    assert invariants((1,), (-2,), ((2,),)) == (3, 1)
    # Double cover branched over an unknotted 2-sphere.
    assert invariants((2,), (0,), ((2,),)) == (2, 0)
    # A double of annulus plus two discs is torus plus two spheres.
    assert (0 + 2 + 2) == 2 * (0 + 1 + 1)
    assert invariants((0, 2, 2), (0, 0, 0), ((2,),) * 3)[1] == 0
    # This profile passes chi and sigma requirements but is NOT asserted
    # to come from any actual surface complement or cover.
    relaxed = invariants((1, 1, 2), (2, -2, 0), ((2, 1), (2, 1), (3,)))
    assert relaxed == (0, 0)
    # The general lower bound gives d >= ceil(1 + 2g/(P-2)).
    for pos in range(3, 13):
        for genus in range(1, 101):
            threshold = Q(1) + Q(2 * genus, pos - 2)
            for d in range(1, 30):
                if 2 - 2 * genus >= (2 - pos) * d + pos:
                    assert d >= threshold
                counts["degree_growth_bounds"] += 1
    report = {
        "status": "PASS", "arithmetic": "exact integer and Fraction",
        "counts": counts,
        "negative_controls": {
            "simple_vs_index_two": "defects 1 versus 2",
            "orientation_sensitive_cp2": "chi=3, signature=1 for e=-2",
            "orientable_double": "signature=0",
            "three_component_relaxation": "chi=0, signature=0 at degree 3; not a realization"
        },
        "limitations": "No enumeration of complement representations, no certification of a manifold, and no universal existence or nonexistence proof."
    }
    target = Path(__file__).with_name("CONTROL_RESULTS.json")
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
