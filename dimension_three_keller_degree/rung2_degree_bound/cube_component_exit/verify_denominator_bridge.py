#!/usr/bin/env python3
"""Machine-check the exact five-target bridge into the frozen denominator."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutation", choices=("scope",))
    args = parser.parse_args()

    here = Path(__file__).resolve().parent
    bridge = json.loads((here / "BRIDGE.json").read_text())
    denominator_path = (
        here.parent
        / "fixed_quadratic_line_doublecover"
        / "audit_delta_ge3_denominator"
        / "DENOMINATOR.json"
    )
    raw = denominator_path.read_bytes()
    denominator = json.loads(raw)
    families = {entry["id"]: entry for entry in denominator["families"]}

    assert len(families) == bridge["denominator_family_count"] == 26
    assert hashlib.sha256(raw).hexdigest() == bridge["denominator_sha256"]
    assert "target-linear combination" in bridge["interpretation"]

    expected_whole = {
        "PF-BRANCH-FOURTH-THIRD": ({"h": "p^2", "R": "p^3"}, "newly_excluded"),
        "D3-BB-30": ({"h": "pq", "R": "p^3"}, "newly_excluded"),
        "D3-OB-300": ({"h": "p(p+q)", "R": "p^3"}, "newly_excluded"),
        "D4-DN-3": ({"h": "L^2", "R": "L^3"}, "already_excluded"),
    }
    claims = {
        item["id"]: (item["normal_form"], item["status"])
        for item in bridge["whole_family_points"]
    }
    if args.mutation == "scope":
        claims["D3-SF-20C"] = (families["D3-SF-20C"]["normal_form"], "newly_excluded")
    assert claims == expected_whole
    for family_id, (normal_form, _) in expected_whole.items():
        assert families[family_id]["normal_form"] == normal_form

    # These are exactly the whole-family normal forms whose R field is a
    # displayed cube of one linear symbol.
    displayed_whole_cubes = {
        family_id
        for family_id, entry in families.items()
        if entry["normal_form"].get("R") in {"p^3", "L^3"}
    }
    assert displayed_whole_cubes == set(expected_whole)

    pivot_claims = bridge["retained_pivot_only"]
    assert len(pivot_claims) == 1
    pivot_claim = pivot_claims[0]
    assert pivot_claim["id"] == "D3-SF-20C"
    sf20c = families["D3-SF-20C"]
    assert sf20c["normal_form"]["R"] == "X^2((5-3z)p+4rq)"
    cube_pivots = [
        (family_id, pivot["condition"], pivot["destination"])
        for family_id, entry in families.items()
        for pivot in entry.get("retained_pivots", [])
        if "R=X^3" in pivot["destination"]
    ]
    assert cube_pivots == [
        (
            "D3-SF-20C",
            "z=3 (kappa=16/3)",
            "same family with residual line X, so R=X^3",
        )
    ]
    assert pivot_claim["condition"] == cube_pivots[0][1]
    assert pivot_claim["cube_identity"] == "R=X^3"
    assert "z=1/3" in pivot_claim["warning"]

    print("DENOMINATOR_SHA256=" + hashlib.sha256(raw).hexdigest())
    print("CUBE_COMPONENT_DENOMINATOR_BRIDGE_PASS")


if __name__ == "__main__":
    main()
