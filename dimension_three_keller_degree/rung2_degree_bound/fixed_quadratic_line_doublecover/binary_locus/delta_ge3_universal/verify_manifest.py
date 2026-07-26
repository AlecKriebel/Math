#!/usr/bin/env python3
"""Fail-closed structural audit of denominator.json.

This is dependency-free and intentionally does not duplicate any algebra.
It freezes the identifiers, chart denominator, counts, boundary targets,
and the convention for parameter endpoints and stabilizer jumps.
"""

from __future__ import annotations

import json
import os
import sys
from collections import Counter
from pathlib import Path

if not __debug__:
    print("FAIL: assertions are required", file=sys.stderr)
    raise SystemExit(2)

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / "denominator.json").read_text(encoding="utf-8"))

expected_counts = {
    "delta3": 17,
    "delta4": 6,
    "power_fibre": 1,
    "total_nonzero_delta_ge3_or_power": 24,
}
assert data["counts"] == expected_counts
assert data["normal_component_degree"] == 3
assert data["notation"]["R"] == "a*p^3+b*p^2*q+c*p*q^2+d*q^3"

expected_delta3_by_chart = {
    "branch_square": 2,
    "two_branch": 2,
    "one_branch": 6,
    "doubled_nonbranch": 3,
    "squarefree_interior": 4,
}
expected_delta4_by_chart = {
    "doubled_nonbranch": 3,
    "squarefree_interior": 3,
}
assert Counter(row["h_chart"] for row in data["delta3"]) == (
    expected_delta3_by_chart
)
assert Counter(row["h_chart"] for row in data["delta4"]) == (
    expected_delta4_by_chart
)

expected_ids = {
    "D3-BS-P3", "D3-BS-P2Q",
    "D3-TB-P3", "D3-TB-P2Q",
    "D3-OB-P3", "D3-OB-P2L", "D3-OB-PL2",
    "D3-OB-P2Q", "D3-OB-PQL", "D3-OB-QL2",
    "D3-DN-L3", "D3-DN-PL2", "D3-DN-PQL",
    "D3-SF-21", "D3-SF-2C", "D3-SF-11C", "D3-SF-1C2",
    "D4-DN-L4", "D4-DN-PL3", "D4-DN-PQL2",
    "D4-SF-21C", "D4-SF-2C2", "D4-SF-11C2",
    "PF-BS",
}
rows = data["delta3"] + data["delta4"] + data["power_fibre"]
ids = [row["id"] for row in rows]
assert len(ids) == len(set(ids)) == 24
assert set(ids) == expected_ids

for row in data["delta3"] + data["delta4"]:
    assert row["normal_form"]
    assert row["exact_open"]
    assert row["gcd_signature"]
for row in data["power_fibre"]:
    assert row["normal_form"]
    assert row["condition"]

allowed_targets = expected_ids | {"L00"}
seen_targets: set[str] = set()
for row in rows:
    for target in row.get("boundaries", {}).values():
        assert target in allowed_targets
        seen_targets.add(target)
assert {
    "PF-BS", "D4-DN-L4", "D4-DN-PL3", "D4-DN-PQL2",
    "D4-SF-21C", "D4-SF-2C2", "D4-SF-11C2", "L00",
} <= seen_targets

convention = data["counting_convention"]
assert convention[
    "exact_delta_parameter_endpoints_or_stabilizer_jumps_are_separate_families"
] is False
retained = convention["retained_exact_delta_specializations"]
assert {entry["family"] for entry in retained} == {
    "D3-BS-P3",
    "D3-BS-P2Q",
    "D3-DN-L3",
    "D3-DN-PL2",
    "D3-DN-PQL",
    "D3-SF-21, D3-SF-2C, D3-SF-11C, D3-SF-1C2",
}
assert any("kappa=0" in entry["locus"] for entry in retained)
boundary_charts = convention["retained_boundary_charts_not_added_to_the_count"]
assert len(boundary_charts) == 5
assert len(data["global_boundary_protocol"]) == 4

# This opt-in mutation makes the strict wrapper prove that the audit is live.
if os.environ.get("DELTA_GE3_MANIFEST_FAULT") == "drop-id":
    assert "D3-BS-P3" not in expected_ids, "injected manifest fault detected"

print("DELTA_GE3_MANIFEST_PASS_17_6_1")
