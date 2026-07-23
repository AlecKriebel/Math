#!/usr/bin/env python3
"""Check completeness and integrity of the recorded seed-frontier artifacts.

This standard-library checker reconstructs the margin-plus-quad frontiers and
checks that the pinned JSON files contain every selected target exactly once,
with compatible metadata and an ``INFEASIBLE`` status.  It verifies artifact
aggregation and checksums; it does not independently replay CP-SAT's search.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any

from verify_variable_q_seed_quad_radius import MarginTarget, TargetCheck, check_radius


BASE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class ArtifactSpec:
    path: Path
    radius: int
    minimum_distance: int
    sha256: str
    frontier_size: int


SPECS = (
    ArtifactSpec(
        BASE / "output/variable_q_seed_frontier_radius16_root_table.json",
        16,
        0,
        "4b38d392d9b48e9ee3d9466813863d4ab9ca59c513245469fa5afeb39ef39a0f",
        197,
    ),
    ArtifactSpec(
        BASE / "output/variable_q_seed_frontier_shell17_root_table.json",
        17,
        17,
        "a0c842a2bb01696874cb911ac8d2ba41d1fd5467323b1e9e58d833a24d51bf8e",
        276,
    ),
)


def selected_frontier(radius: int, minimum_distance: int) -> tuple[TargetCheck, ...]:
    records = []
    for record in check_radius(radius).targets:
        if record.quad_distance is None or record.quad_distance > radius:
            continue
        first_possible = max(minimum_distance, record.quad_distance)
        if (first_possible - record.margin_distance) % 2:
            first_possible += 1
        if first_possible <= radius:
            records.append(record)
    return tuple(records)


def _target(value: Any) -> MarginTarget:
    result = tuple(tuple(int(entry) for entry in pair) for pair in value)
    if len(result) != 4 or any(len(pair) != 2 for pair in result):
        raise AssertionError("artifact target has the wrong shape")
    return result  # type: ignore[return-value]


def verify_artifact(spec: ArtifactSpec) -> None:
    raw = spec.path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != spec.sha256:
        raise AssertionError(
            f"checksum mismatch for {spec.path}: expected {spec.sha256}, got {digest}"
        )
    payload = json.loads(raw)
    expected_records = selected_frontier(spec.radius, spec.minimum_distance)
    expected = {
        (record.shard, record.target): record for record in expected_records
    }
    if len(expected) != spec.frontier_size:
        raise AssertionError("reconstructed frontier size changed")
    if payload.get("kind") != "variable-q-seed-frontier-filter":
        raise AssertionError("wrong artifact kind")
    if payload.get("radius") != spec.radius:
        raise AssertionError("wrong artifact radius")
    if payload.get("minimum_distance", 0) != spec.minimum_distance:
        raise AssertionError("wrong artifact minimum distance")
    if payload.get("frontier_size") != spec.frontier_size:
        raise AssertionError("wrong recorded frontier size")
    layers = payload.get("layers", {})
    if (
        layers.get("small_roots") is not True
        or layers.get("small_root_encoding") != "table"
        or layers.get("compression_7") is not False
        or layers.get("compression_7_alternating") is not False
        or layers.get("full_correlations") is not False
    ):
        raise AssertionError("unexpected frontier proof layers")
    if payload.get("workers") != 1 or payload.get("max_memory_mb") != 256:
        raise AssertionError("unexpected resource metadata")

    observed = {}
    for result in payload.get("results", ()):
        key = (int(result["shard"]), _target(result["target"]))
        if key in observed:
            raise AssertionError(f"duplicate frontier result: {key}")
        if key not in expected:
            raise AssertionError(f"unexpected frontier result: {key}")
        record = expected[key]
        if result.get("margin_distance") != record.margin_distance:
            raise AssertionError("recorded margin distance changed")
        if result.get("quad_distance") != record.quad_distance:
            raise AssertionError("recorded quad distance changed")
        if result.get("status") != "INFEASIBLE":
            raise AssertionError(f"frontier result is not infeasible: {key}")
        observed[key] = result
    missing = set(expected) - set(observed)
    if missing:
        raise AssertionError(f"artifact omits {len(missing)} frontier targets")


def main() -> None:
    for spec in SPECS:
        verify_artifact(spec)
        print(
            f"PASS: {spec.path} contains all {spec.frontier_size} "
            "expected INFEASIBLE records"
        )
    print(
        "RESULT: recorded CP-SAT statuses cover the complete raw seed ball "
        "through radius 17; this checker does not replay their UNSAT proofs"
    )


if __name__ == "__main__":
    main()
