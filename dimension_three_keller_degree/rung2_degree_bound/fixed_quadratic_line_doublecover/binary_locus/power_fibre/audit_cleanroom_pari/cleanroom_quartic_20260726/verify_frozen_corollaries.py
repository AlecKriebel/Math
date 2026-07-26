#!/usr/bin/env python3
"""Check only the cube-component corollaries against the frozen denominator."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
DENOMINATOR = HERE.parents[3] / "audit_delta_ge3_denominator" / "DENOMINATOR.json"
raw = DENOMINATOR.read_bytes()
data = json.loads(raw)
families = {entry["id"]: entry for entry in data["families"]}


def normal(family_id):
    return families[family_id]["normal_form"]


assert normal("PF-BRANCH-FOURTH-THIRD") == {"h": "p^2", "R": "p^3"}
assert normal("D4-DN-3") == {"h": "L^2", "R": "L^3"}
assert normal("D3-BB-30") == {"h": "pq", "R": "p^3"}
assert normal("D3-OB-300") == {"h": "p(p+q)", "R": "p^3"}

sf20c = families["D3-SF-20C"]
assert sf20c["normal_form"]["R"] == "X^2((5-3z)p+4rq)"
cube_pivots = [
    pivot
    for pivot in sf20c["retained_pivots"]
    if "R=X^3" in pivot["destination"]
]
assert cube_pivots == [
    {
        "condition": "z=3 (kappa=16/3)",
        "destination": "same family with residual line X, so R=X^3",
    }
]

print("DENOMINATOR_SHA256=" + hashlib.sha256(raw).hexdigest())
print("POWER_FIBRE_FROZEN_COROLLARIES_PASS")
