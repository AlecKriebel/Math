#!/usr/bin/env python3
"""Fail-closed bridge from the frozen exact-delta-four atlas to six proofs."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "FAMILIES.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


with MANIFEST.open(encoding="utf-8") as stream:
    manifest = json.load(stream)

require(
    manifest["theorem_scope"]
    == "fixed-quadratic line-double-cover binary locus, exact gcd degree delta=4",
    "theorem scope changed",
)
require(
    manifest["frozen_source"]
    == "../../audit_delta_ge3_denominator/DENOMINATOR.json",
    "canonical denominator path changed",
)
families = list(manifest["families"])
if os.environ.get("EXACT_DELTA4_MANIFEST_FAULT") == "drop-family":
    families.pop()
    print("injected exact-delta-four manifest fault detected")

require(manifest["family_count"] == 6, "declared family count is not six")
require(len(families) == 6, "manifest does not contain six families")

frozen_path = (HERE / manifest["frozen_source"]).resolve()
canonical_path = (
    HERE / "../../audit_delta_ge3_denominator/DENOMINATOR.json"
).resolve()
require(frozen_path == canonical_path, "source is not the canonical denominator")
with frozen_path.open(encoding="utf-8") as stream:
    frozen = json.load(stream)

require(frozen["schema_version"] == 1, "wrong canonical schema")
require(frozen["status"] == "PASS", "canonical denominator is not PASS")
require(
    frozen["scope"] == "binary (h,R), exact delta>=3 incidence denominator only",
    "canonical denominator scope changed",
)
require(
    frozen["counts"]
    == {
        "delta3_independent": 19,
        "delta4_independent": 6,
        "dependent_power_fibre": 1,
        "total": 26,
    },
    "canonical denominator counts changed",
)
expected_ids = [
    row["id"]
    for row in frozen["families"]
    if row["coarse"] == "delta4_independent"
]
actual_ids = [row["atlas_id"] for row in families]
require(len(expected_ids) == len(set(expected_ids)) == 6, "frozen atlas is not six")
require(len(actual_ids) == len(set(actual_ids)) == 6, "bridge IDs are not unique")
require(actual_ids == expected_ids, "bridge order or membership differs from frozen atlas")

labels = [row["certificate_label"] for row in families]
markers = [row["terminal_marker"] for row in families]
require(len(labels) == len(set(labels)) == 6, "certificate labels are not unique")
require(len(markers) == len(set(markers)) == 6, "terminal markers are not unique")

required_keys = {
    "atlas_id",
    "certificate_label",
    "certificate_dir",
    "terminal_marker",
}
expected_certificate_map = {
    "D4-SF-21C": (
        "../d4_sf_21c_exclusion",
        "D4_SF_21C_FULL_STRICT_PASS",
    ),
    "D4-SF-20CC": (
        "../d4_sf_20cc_exclusion",
        "D4_SF_20CC_FULL_STRICT_PASS",
    ),
    "D4-SF-11CC": (
        "../d4_sf_11cc_exclusion",
        "D4_SF_11CC_FULL_STRICT_PASS",
    ),
    "D4-DN-3": (
        "../d4_dn3_full_descent",
        "D4_DN3_FULL_FAMILY_EXCLUSION_STRICT_PASS",
    ),
    "D4-DN-2C": (
        "../d4_dn2c_full_descent",
        "D4_DN2C_FULL_DESCENT_STRICT_PASS",
    ),
    "D4-DN-1CC": (
        "../d4_dn1cc_full",
        "D4_DN1CC_FAIL_CLOSED_STRICT_PASS",
    ),
}
for row in families:
    require(set(row) == required_keys, f"unexpected bridge fields for {row!r}")
    certificate_dir = (HERE / row["certificate_dir"]).resolve()
    require(certificate_dir.is_dir(), f"missing certificate directory: {certificate_dir}")
    require(
        (certificate_dir / "NOTE.md").is_file(),
        f"missing family note: {certificate_dir}",
    )
    require(
        (certificate_dir / "verify_strict.sh").is_file(),
        f"missing strict family wrapper: {certificate_dir}",
    )
    require(
        row["terminal_marker"].startswith("D4_"),
        f"non-family marker: {row['terminal_marker']}",
    )
    require(
        row["certificate_label"] == row["atlas_id"],
        f"canonical ID and certificate label differ: {row!r}",
    )
    require(
        (row["certificate_dir"], row["terminal_marker"])
        == expected_certificate_map[row["atlas_id"]],
        f"wrong certificate binding: {row!r}",
    )

if "--emit-plan" in sys.argv:
    for row in families:
        print(f"{row['certificate_dir']}|{row['terminal_marker']}")
else:
    print("EXACT_DELTA4_MANIFEST_PASS_6_OF_6_CANONICAL_19_6_1")
