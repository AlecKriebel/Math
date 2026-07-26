#!/usr/bin/env python3
"""Independent fail-closed scope binding for the cube-component corollaries."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("assertions must remain enabled")


HERE = Path(__file__).resolve().parent
BRIDGE = HERE.parent / "BRIDGE.json"
DENOMINATOR = (
    HERE.parent.parent
    / "fixed_quadratic_line_doublecover"
    / "audit_delta_ge3_denominator"
    / "DENOMINATOR.json"
)
EXPECTED_SHA = "440df4694f98b1b361a09e136afb4365c3aa302c5532e5291f4b76a2a068c65a"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


raw = DENOMINATOR.read_bytes()
require(hashlib.sha256(raw).hexdigest() == EXPECTED_SHA, "denominator SHA drift")
denominator = json.loads(raw)
require(denominator["counts"]["total"] == 26, "frozen count drift")
families = {family["id"]: family for family in denominator["families"]}
require(len(families) == 26, "frozen IDs are not unique")

bridge = json.loads(BRIDGE.read_text())
require(bridge["denominator_family_count"] == 26, "bridge count drift")
require(bridge["denominator_sha256"] == EXPECTED_SHA, "bridge SHA drift")

expected_whole = {
    "PF-BRANCH-FOURTH-THIRD": ({"h": "p^2", "R": "p^3"}, "newly_excluded"),
    "D3-BB-30": ({"h": "pq", "R": "p^3"}, "newly_excluded"),
    "D3-OB-300": ({"h": "p(p+q)", "R": "p^3"}, "newly_excluded"),
    "D4-DN-3": ({"h": "L^2", "R": "L^3"}, "already_excluded"),
}
actual_whole = {entry["id"]: entry for entry in bridge["whole_family_points"]}
require(set(actual_whole) == set(expected_whole), "whole-family bridge IDs drifted")
for family_id, (normal_form, status) in expected_whole.items():
    require(families[family_id]["normal_form"] == normal_form, f"{family_id} frozen drift")
    require(actual_whole[family_id]["normal_form"] == normal_form, f"{family_id} bridge drift")
    require(actual_whole[family_id]["status"] == status, f"{family_id} status drift")

require(
    sum(entry["status"] == "newly_excluded" for entry in actual_whole.values()) == 3,
    "new whole-family count is not three",
)

pivots = bridge["retained_pivot_only"]
require(len(pivots) == 1, "cube bridge contains more than one retained pivot")
require(
    pivots[0]
    == {
        "id": "D3-SF-20C",
        "condition": "z=3 (kappa=16/3)",
        "cube_identity": "R=X^3",
        "status": "newly_excluded_pivot_only",
        "warning": "does not exclude the generic family or the reciprocal z=1/3 sheet",
    },
    "retained pivot scope drifted",
)

sf20c = families["D3-SF-20C"]
conditions = {entry["condition"] for entry in sf20c["retained_pivots"]}
require("z=3 (kappa=16/3)" in conditions, "z=3 pivot missing")
require("z=1/3 (kappa=16/3)" in conditions, "reciprocal sheet missing")

# X=(1,-r).  At z=3 the residual line is (-4,4r)=-4X; at
# z=1/3 it is (4,4r), whose determinant with X is 8r !=0.
require((-4) * (-1) - 4 * 1 == 0, "z=3 is not the cube pivot")
require(4 * (-1) - 4 * 1 != 0, "z=1/3 was incorrectly made a cube pivot")

print("PASS independent frozen SHA/count binding")
print("PASS exactly three new whole families and one redundant D4-DN-3 point")
print("PASS exactly the z=3 pivot, not all D3-SF-20C or z=1/3")
print("CUBE_COMPONENT_HOSTILE_SCOPE_PASS")
