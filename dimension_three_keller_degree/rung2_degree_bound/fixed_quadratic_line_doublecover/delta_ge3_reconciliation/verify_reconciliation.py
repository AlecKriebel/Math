#!/usr/bin/env python3
"""Dependency-free audit of the frozen delta>=3 atlas reconciliation."""

from __future__ import annotations

import json
from pathlib import Path
import sys


if not __debug__:
    print("FAIL: assertions are required; do not run with -O", file=sys.stderr)
    raise SystemExit(2)


HERE = Path(__file__).resolve().parent
PRIMARY = HERE.parent / "binary_locus" / "delta_ge3_universal" / "denominator.json"
AUDIT = HERE.parent / "audit_delta_ge3_denominator" / "DENOMINATOR.json"
MAPPING = HERE / "canonical_mapping.json"
BOUNDARIES = HERE / "BOUNDARY_CHARTS.json"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


primary = load(PRIMARY)
audit = load(AUDIT)
reconciliation = load(MAPPING)
boundaries = load(BOUNDARIES)

primary_delta3 = [entry["id"] for entry in primary["delta3"]]
primary_delta4 = [entry["id"] for entry in primary["delta4"]]
primary_power = [entry["id"] for entry in primary["power_fibre"]]
primary_ids = primary_delta3 + primary_delta4 + primary_power

audit_families = audit["families"]
audit_ids = [entry["id"] for entry in audit_families]
audit_delta3 = [
    entry["id"] for entry in audit_families
    if entry["coarse"] == "delta3_independent"
]
audit_delta4 = [
    entry["id"] for entry in audit_families
    if entry["coarse"] == "delta4_independent"
]
audit_power = [
    entry["id"] for entry in audit_families
    if entry["coarse"] == "dependent_power_fibre"
]

assert len(primary_delta3) == 17
assert len(primary_delta4) == 6
assert len(primary_power) == 1
assert len(primary_ids) == len(set(primary_ids)) == 24

assert len(audit_delta3) == 19
assert len(audit_delta4) == 6
assert len(audit_power) == 1
assert len(audit_ids) == len(set(audit_ids)) == 26

mapping = reconciliation["mapping"]
assert set(mapping) == set(primary_ids)
destinations = [target for targets in mapping.values() for target in targets]
assert len(destinations) == len(set(destinations)) == 26
assert set(destinations) == set(audit_ids)

splits = {source: targets for source, targets in mapping.items() if len(targets) > 1}
assert splits == {
    "D3-BS-P3": ["D3-BS-N2-Z", "D3-BS-N2-NZ"],
    "D3-BS-P2Q": ["D3-BS-N1-BR2", "D3-BS-N1-CONTACT"],
}
assert all(len(targets) == 1 for source, targets in mapping.items() if source not in splits)

by_id = {entry["id"]: entry for entry in audit_families}
primary_by_id = {
    entry["id"]: entry
    for entry in primary["delta3"] + primary["delta4"] + primary["power_fibre"]
}
assert all(by_id[target]["h_chart"] == "branch_square" for targets in splits.values() for target in targets)
assert {by_id[target]["normal_form"]["R"] for target in splits["D3-BS-P3"]} == {
    "p^2 q",
    "p^2(p+q)",
}
assert {by_id[target]["normal_form"]["R"] for target in splits["D3-BS-P2Q"]} == {
    "p q^2",
    "p(p^2+q^2)",
}

assert primary["counts"] == {
    "delta3": 17,
    "delta4": 6,
    "power_fibre": 1,
    "total_nonzero_delta_ge3_or_power": 24,
}
assert audit["counts"] == {
    "delta3_independent": 19,
    "delta4_independent": 6,
    "dependent_power_fibre": 1,
    "total": 26,
}

primary_moduli = {
    entry.get("modulus") for entry in primary["delta4"] if "modulus" in entry
}
audit_moduli = {
    entry["normal_form"]["condition"].split("kappa=")[-1]
    for entry in audit_families
    if entry["id"] in {"D4-SF-21C", "D4-SF-20CC", "D4-SF-11CC"}
}
assert primary_moduli == {"kappa=-16/5", "kappa=16/5", "kappa=16"}
assert audit_moduli == {"-16/5", "16/5", "16"}

assert audit_power == ["PF-BRANCH-FOURTH-THIRD"]
power_form = by_id[audit_power[0]]["normal_form"]
assert power_form["h"] == "p^2" and power_form["R"] == "p^3"

# The frozen primary atlas omitted two DN guards and the oriented reciprocal
# sheet at z=-1/5.  The canonical audit ledger must repair both defects.
assert primary_by_id["D3-DN-L3"]["exact_open"] == "A-B!=0; [A:B] modulo swap"
assert by_id["D3-DN-2"]["guards"] == [
    "u-v != 0",
    "2u+v != 0",
    "u+2v != 0",
]
assert "kappa not in {-16/5,16/5}" in primary_by_id["D3-SF-2C"]["exact_open"]
assert by_id["D3-SF-20C"]["parameter_space"].startswith("z in C^*")
assert any(
    pivot["condition"] == "z=-1/5 (kappa=-16/5)"
    for pivot in by_id["D3-SF-20C"]["retained_pivots"]
)
assert any(
    boundary["condition"] == "z=-5"
    and boundary["destination"] == "D4-SF-21C"
    for boundary in by_id["D3-SF-20C"]["exit_boundaries"]
)

# Every retained pivot and exit in the canonical ledger has a stable F1 ID.
charts = boundaries["charts"]
chart_ids = [entry["id"] for entry in charts]
assert len(chart_ids) == len(set(chart_ids)) == 36
retained = [entry for entry in charts if entry["kind"] == "retained_pivot"]
exits = [entry for entry in charts if entry["kind"] == "exit_arrow"]
assert len(retained) == 12
assert len(exits) == 24
assert boundaries["counts"] == {
    "retained_pivots": 12,
    "exit_arrows": 24,
    "total_boundary_ids": 36,
}

audit_retained_keys = {
    (family["id"], pivot["condition"])
    for family in audit_families
    for pivot in family["retained_pivots"]
}
registry_retained_keys = {(entry["source"], entry["condition"]) for entry in retained}
assert registry_retained_keys == audit_retained_keys

audit_exit_keys = {
    (family["id"], boundary["condition"], boundary["destination"])
    for family in audit_families
    for boundary in family["exit_boundaries"]
}
registry_exit_keys = {
    (entry["source"], entry["condition"], entry["destination"])
    for entry in exits
    if entry["id"] != "BX-PF-R0"
}
assert registry_exit_keys == audit_exit_keys
assert {
    (entry["source"], entry["condition"], entry["destination"])
    for entry in exits
    if entry["id"] == "BX-PF-R0"
} == {("PF-BRANCH-FOURTH-THIRD", "R=0", "L00")}

assert {entry["source"] for entry in charts} <= set(audit_ids)
assert {entry["destination"] for entry in charts} <= set(audit_ids) | {"L00"}

print("DELTA_GE3_RECONCILIATION_PASS_PRIMARY17_CANONICAL19_DELTA4_6_POWER_1")
