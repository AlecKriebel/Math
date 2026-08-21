#!/usr/bin/env python3
"""Fail-closed binding to the frozen 26-family denominator."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("assertions must remain enabled")


EXPECTED_SHA256 = "440df4694f98b1b361a09e136afb4365c3aa302c5532e5291f4b76a2a068c65a"
HERE = Path(__file__).resolve().parent
DENOMINATOR = (
    HERE.parent.parent.parent
    / "audit_delta_ge3_denominator"
    / "DENOMINATOR.json"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


raw = DENOMINATOR.read_bytes()
require(hashlib.sha256(raw).hexdigest() == EXPECTED_SHA256, "frozen SHA drift")
data = json.loads(raw)

require(data["status"] == "PASS", "frozen denominator is not PASS")
require(
    data["counts"]
    == {
        "delta3_independent": 19,
        "delta4_independent": 6,
        "dependent_power_fibre": 1,
        "total": 26,
    },
    "frozen family counts drifted",
)
require(len(data["families"]) == 26, "literal family count is not 26")

families = {family["id"]: family for family in data["families"]}
require(len(families) == 26, "family IDs are not unique")

whole_new = {
    "PF-BRANCH-FOURTH-THIRD": {"h": "p^2", "R": "p^3"},
    "D3-BB-30": {"h": "pq", "R": "p^3"},
    "D3-OB-300": {"h": "p(p+q)", "R": "p^3"},
}
already_closed = {"D4-DN-3": {"h": "L^2", "R": "L^3"}}

for family_id, normal_form in {**whole_new, **already_closed}.items():
    require(family_id in families, f"missing frozen ID {family_id}")
    require(
        families[family_id]["normal_form"] == normal_form,
        f"normal form drift for {family_id}",
    )

require(len(whole_new) == 3, "new whole-family exclusion count is not three")
require(len(already_closed) == 1, "redundant whole-family count is not one")

sf20c = families["D3-SF-20C"]
pivots = {pivot["condition"]: pivot["destination"] for pivot in sf20c["retained_pivots"]}
require(
    pivots["z=3 (kappa=16/3)"]
    == "same family with residual line X, so R=X^3",
    "z=3 pivot identity drifted",
)
require(
    "z=1/3 (kappa=16/3)" in pivots,
    "reciprocal z=1/3 sheet disappeared",
)

# Independently distinguish the two reciprocal sheets.  With
# X=p-rq and R=X^2((5-3z)p+4rq):
#   z=3   -> the residual line is -4X;
#   z=1/3 -> it is 4(p+rq), whose determinant with X is 2r != 0.
residual_z3 = (-4, 4)  # coefficient of p, and coefficient multiplying r*q
x_line = (1, -1)
require(
    residual_z3[0] * x_line[1] - residual_z3[1] * x_line[0] == 0,
    "z=3 residual is not proportional to X",
)
residual_zthird = (4, 4)
require(
    residual_zthird[0] * x_line[1]
    - residual_zthird[1] * x_line[0]
    != 0,
    "z=1/3 was incorrectly collapsed to the cube pivot",
)

print(f"PASS frozen denominator SHA {EXPECTED_SHA256}")
print("PASS frozen count remains 19+6+1=26")
print("PASS newly excluded whole families: PF-BRANCH-FOURTH-THIRD, D3-BB-30, D3-OB-300")
print("PASS D4-DN-3 is bound separately as an already-closed redundant consequence")
print("PASS only z=3, not z=1/3 or all of D3-SF-20C, is the new cube pivot")
print("ALL FROZEN BRIDGE CHECKS PASSED")

