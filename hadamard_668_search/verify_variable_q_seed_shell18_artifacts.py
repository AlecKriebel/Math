#!/usr/bin/env python3
"""Verify the pinned layered exclusion certificate for seed shell 18.

The checker reconstructs the complete margin-plus-quad frontier, verifies
every artifact checksum and selection edge, independently checks all decoded
root witnesses with integer arithmetic, and confirms that every root survivor
is eliminated by a primitive-7 or primitive-14 compression identity.

As with the radius-16/17 artifact checker, this verifies the immutable result
chain but does not replay CP-SAT's infeasibility searches.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any

from variable_q_base import (
    LONG,
    SHORT,
    alternating_sum,
    base_quad_products,
    sign_sum,
)
from variable_q_compression import pad_to_period
from verify_variable_q_seed_quad_radius import MarginTarget, TargetCheck, check_radius
from verify_variable_q_seed_radius import SEED


BASE = Path(__file__).resolve().parent
RADIUS = 18
MINIMUM_DISTANCE = 18
ENERGY = 334


@dataclass(frozen=True)
class ArtifactSpec:
    filename: str
    sha256: str
    counts: tuple[tuple[str, int], ...]
    time_limit: float
    layers: tuple[tuple[str, Any], ...]

    @property
    def path(self) -> Path:
        return BASE / "output" / self.filename


ROOT_INITIAL = ArtifactSpec(
    "variable_q_seed_frontier_shell18_root_table_0p5s.json",
    "2a93ac19108cee6705743f21f8d60e5f0f17a7de2389539141a8a091ef2670ba",
    (("INFEASIBLE", 525), ("OPTIMAL", 7), ("UNKNOWN", 291)),
    0.5,
    (
        ("small_roots", True),
        ("small_root_encoding", "table"),
        ("compression_7", False),
        ("compression_7_alternating", False),
        ("full_correlations", False),
    ),
)
ROOT_TWO_SECONDS = ArtifactSpec(
    "variable_q_seed_frontier_shell18_root_unresolved_2s.json",
    "13956042c216c2a28815d2002599a6f0ebcd11921252cfd98ae6859b08156cc7",
    (("INFEASIBLE", 209), ("OPTIMAL", 11), ("UNKNOWN", 78)),
    2.0,
    ROOT_INITIAL.layers,
)
ROOT_FIVE_SECONDS = ArtifactSpec(
    "variable_q_seed_frontier_shell18_root_timeouts_5s.json",
    "db7aaa9127a81877c14d8da943736a1390be921c481ff81060481b72defc130e",
    (("INFEASIBLE", 37), ("OPTIMAL", 1), ("UNKNOWN", 40)),
    5.0,
    ROOT_INITIAL.layers,
)
ROOT_SYMMETRY = ArtifactSpec(
    "variable_q_seed_frontier_shell18_root_timeouts_symmetry_5s.json",
    "6b641bbf58f3adc7277522c624a7371c3105884dfbb2f0a16344312c0dc40085",
    (("INFEASIBLE", 2), ("UNKNOWN", 38)),
    5.0,
    ROOT_INITIAL.layers + (("exchangeable_quad_symmetry", True),),
)
ROOT_ORBIT = ArtifactSpec(
    "variable_q_seed_frontier_shell18_root_timeouts_orbit_5s.json",
    "6ebb2e43a254881923ace02801a93a62938fc9b1aecf586bcca6866f41024f82",
    (("INFEASIBLE", 32), ("UNKNOWN", 6)),
    5.0,
    ROOT_INITIAL.layers
    + (("quad_encoding", "orbit-counts"), ("exchangeable_quad_symmetry", True)),
)
ROOT_ORBIT_HARD = ArtifactSpec(
    "variable_q_seed_frontier_shell18_root_orbit_hard6_30s.json",
    "10342117cbcb70d39498fd77e7aa206f23fbc69560506e239491124f852f1808",
    (("INFEASIBLE", 6),),
    30.0,
    ROOT_ORBIT.layers,
)
WITNESSES_Z7 = ArtifactSpec(
    "variable_q_seed_frontier_shell18_root_witnesses_2s_z7_5s.json",
    "7730a740560337d1baf6716078d28e99e8f69fc0dea4dacb3775ef0a161a55db",
    (("INFEASIBLE", 9), ("UNKNOWN", 2)),
    5.0,
    (
        ("small_roots", True),
        ("small_root_encoding", "table"),
        ("compression_7", True),
        ("compression_7_alternating", False),
        ("full_correlations", False),
    ),
)
WITNESSES_Z14 = ArtifactSpec(
    "variable_q_seed_frontier_shell18_root_witnesses_z7_timeouts_z14_15s.json",
    "908b5571034ab2e1542e555281c7ea610903e5d41b5a06792e5986dcbca19f65",
    (("INFEASIBLE", 2),),
    15.0,
    (
        ("small_roots", True),
        ("small_root_encoding", "table"),
        ("quad_encoding", "bits"),
        ("compression_7", False),
        ("compression_7_alternating", True),
        ("full_correlations", False),
    ),
)
NEW_WITNESS_Z14 = ArtifactSpec(
    "variable_q_seed_frontier_shell18_new_root_witness_z14_30s.json",
    "a22c5f51abc466a8ce7cfa46cb44057a5ccedc2e3dc610b8503c3a6f0ae94c6e",
    (("INFEASIBLE", 1),),
    30.0,
    WITNESSES_Z14.layers,
)


def selected_frontier() -> tuple[TargetCheck, ...]:
    records = []
    for record in check_radius(RADIUS).targets:
        if record.quad_distance is None or record.quad_distance > RADIUS:
            continue
        first_possible = max(MINIMUM_DISTANCE, record.quad_distance)
        if (first_possible - record.margin_distance) % 2:
            first_possible += 1
        if first_possible <= RADIUS:
            records.append(record)
    return tuple(records)


def _target(value: Any) -> MarginTarget:
    result = tuple(tuple(int(entry) for entry in pair) for pair in value)
    if len(result) != 4 or any(len(pair) != 2 for pair in result):
        raise AssertionError("artifact target has the wrong shape")
    return result  # type: ignore[return-value]


def _key(result: dict[str, Any]) -> tuple[int, MarginTarget]:
    return int(result["shard"]), _target(result["target"])


def load_artifact(spec: ArtifactSpec) -> dict[str, Any]:
    raw = spec.path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != spec.sha256:
        raise AssertionError(
            f"checksum mismatch for {spec.filename}: expected {spec.sha256}, got {digest}"
        )
    payload = json.loads(raw)
    if payload.get("kind") != "variable-q-seed-frontier-filter":
        raise AssertionError(f"wrong artifact kind: {spec.filename}")
    if payload.get("radius") != RADIUS:
        raise AssertionError(f"wrong radius: {spec.filename}")
    if payload.get("minimum_distance") != MINIMUM_DISTANCE:
        raise AssertionError(f"wrong minimum distance: {spec.filename}")
    if payload.get("parity_skipped") != 276:
        raise AssertionError(f"wrong parity-skip count: {spec.filename}")
    if payload.get("workers") != 1 or payload.get("max_memory_mb") != 256:
        raise AssertionError(f"wrong resource metadata: {spec.filename}")
    if payload.get("time_limit_per_target") != spec.time_limit:
        raise AssertionError(f"wrong time limit: {spec.filename}")
    layers = payload.get("layers", {})
    for name, expected in spec.layers:
        if layers.get(name) != expected:
            raise AssertionError(f"wrong layer {name}: {spec.filename}")
    counts = Counter(result.get("status") for result in payload.get("results", ()))
    if counts != Counter(dict(spec.counts)):
        raise AssertionError(
            f"wrong status counts for {spec.filename}: {dict(counts)}"
        )
    return payload


def result_map(
    payload: dict[str, Any],
    expected_records: dict[tuple[int, MarginTarget], TargetCheck],
) -> dict[tuple[int, MarginTarget], dict[str, Any]]:
    observed = {}
    for result in payload.get("results", ()):
        key = _key(result)
        if key in observed:
            raise AssertionError(f"duplicate result: {key}")
        if key not in expected_records:
            raise AssertionError(f"unknown shell-18 target: {key}")
        record = expected_records[key]
        if result.get("margin_distance") != record.margin_distance:
            raise AssertionError(f"wrong margin distance: {key}")
        if result.get("quad_distance") != record.quad_distance:
            raise AssertionError(f"wrong quad distance: {key}")
        observed[key] = result
    if payload.get("frontier_size") != len(observed):
        raise AssertionError("frontier size does not match the unique results")
    return observed


def selected_keys(
    payload: dict[str, Any], mode: str
) -> set[tuple[int, MarginTarget]]:
    statuses = {
        "witnesses": {"FEASIBLE", "OPTIMAL"},
        "timeouts": {"UNKNOWN"},
        "unresolved": {"FEASIBLE", "OPTIMAL", "UNKNOWN"},
    }[mode]
    return {
        _key(result)
        for result in payload.get("results", ())
        if result.get("status") in statuses
    }


def verify_selection(
    child_spec: ArtifactSpec,
    child: dict[str, Any],
    child_results: dict[tuple[int, MarginTarget], dict[str, Any]],
    parent_spec: ArtifactSpec,
    parent: dict[str, Any],
    mode: str,
) -> None:
    if child.get("targets_from_mode") != mode:
        raise AssertionError(f"wrong selection mode: {child_spec.filename}")
    if child.get("targets_from_sha256") != parent_spec.sha256:
        raise AssertionError(f"wrong parent checksum: {child_spec.filename}")
    source = child.get("targets_from")
    if not source or Path(source).name != parent_spec.filename:
        raise AssertionError(f"wrong parent path: {child_spec.filename}")
    expected = selected_keys(parent, mode)
    if set(child_results) != expected:
        raise AssertionError(
            f"selection mismatch for {child_spec.filename}: "
            f"expected {len(expected)}, got {len(child_results)}"
        )


def _small_root_norms(
    sequences: tuple[tuple[int, ...], ...]
) -> tuple[int, int, int]:
    norms = []
    for modulus in (3, 4, 6):
        total = 0
        for sequence in sequences:
            padded = pad_to_period(sequence)
            residues = tuple(
                sum(padded[residue::modulus]) for residue in range(modulus)
            )
            if modulus == 3:
                first = residues[0] - residues[2]
                second = residues[1] - residues[2]
                total += first * first - first * second + second * second
            elif modulus == 4:
                first = residues[0] - residues[2]
                second = residues[1] - residues[3]
                total += first * first + second * second
            else:
                first = residues[0] - residues[2] - residues[3] + residues[5]
                second = residues[1] + residues[2] - residues[4] - residues[5]
                total += first * first + first * second + second * second
        norms.append(total)
    return tuple(norms)  # type: ignore[return-value]


def verify_root_witness(
    key: tuple[int, MarginTarget], result: dict[str, Any]
) -> None:
    stored = result.get("sequences", {})
    sequences = tuple(
        tuple(int(value) for value in stored.get(label, ())) for label in "abcd"
    )
    if tuple(map(len, sequences)) != (LONG, LONG, SHORT, SHORT):
        raise AssertionError(f"wrong witness lengths: {key}")
    if any(value not in (-1, 1) for sequence in sequences for value in sequence):
        raise AssertionError(f"non-sign witness value: {key}")
    margins = tuple(
        (sign_sum(sequence), alternating_sum(sequence)) for sequence in sequences
    )
    if margins != key[1]:
        raise AssertionError(f"witness margins changed: {key}")
    distance = sum(
        value != seed_value
        for sequence, seed in zip(sequences, SEED, strict=True)
        for value, seed_value in zip(sequence, seed, strict=True)
    )
    if distance != MINIMUM_DISTANCE or result.get("distance") != distance:
        raise AssertionError(f"wrong witness distance: {key}")
    long_products, short_products = base_quad_products(*sequences)
    if long_products != (-1,) + (1,) * 41:
        raise AssertionError(f"long quad parity failed: {key}")
    if short_products != (1,) * 41:
        raise AssertionError(f"short quad parity failed: {key}")
    if _small_root_norms(sequences) != (ENERGY, ENERGY, ENERGY):
        raise AssertionError(f"small-root identities failed: {key}")


def main() -> None:
    specs = (
        ROOT_INITIAL,
        ROOT_TWO_SECONDS,
        ROOT_FIVE_SECONDS,
        ROOT_SYMMETRY,
        ROOT_ORBIT,
        ROOT_ORBIT_HARD,
        WITNESSES_Z7,
        WITNESSES_Z14,
        NEW_WITNESS_Z14,
    )
    payloads = {spec: load_artifact(spec) for spec in specs}
    records = selected_frontier()
    expected_records = {(record.shard, record.target): record for record in records}
    if len(expected_records) != 823:
        raise AssertionError("reconstructed shell-18 frontier size changed")
    maps = {
        spec: result_map(payloads[spec], expected_records) for spec in specs
    }

    if set(maps[ROOT_INITIAL]) != set(expected_records):
        raise AssertionError("initial artifact does not cover the complete frontier")
    root_edges = (
        (ROOT_TWO_SECONDS, ROOT_INITIAL, "unresolved"),
        (ROOT_FIVE_SECONDS, ROOT_TWO_SECONDS, "timeouts"),
        (ROOT_SYMMETRY, ROOT_FIVE_SECONDS, "timeouts"),
        (ROOT_ORBIT, ROOT_SYMMETRY, "timeouts"),
        (ROOT_ORBIT_HARD, ROOT_ORBIT, "timeouts"),
    )
    for child_spec, parent_spec, mode in root_edges:
        verify_selection(
            child_spec,
            payloads[child_spec],
            maps[child_spec],
            parent_spec,
            payloads[parent_spec],
            mode,
        )

    root_state = dict(maps[ROOT_INITIAL])
    for spec, _parent, _mode in root_edges:
        root_state.update(maps[spec])
    root_counts = Counter(result["status"] for result in root_state.values())
    if root_counts != Counter({"INFEASIBLE": 811, "OPTIMAL": 12}):
        raise AssertionError(f"unexpected final root classification: {root_counts}")
    root_witnesses = {
        key: result
        for key, result in root_state.items()
        if result["status"] in ("FEASIBLE", "OPTIMAL")
    }
    for key, result in root_witnesses.items():
        verify_root_witness(key, result)

    verify_selection(
        WITNESSES_Z7,
        payloads[WITNESSES_Z7],
        maps[WITNESSES_Z7],
        ROOT_TWO_SECONDS,
        payloads[ROOT_TWO_SECONDS],
        "witnesses",
    )
    verify_selection(
        WITNESSES_Z14,
        payloads[WITNESSES_Z14],
        maps[WITNESSES_Z14],
        WITNESSES_Z7,
        payloads[WITNESSES_Z7],
        "timeouts",
    )
    verify_selection(
        NEW_WITNESS_Z14,
        payloads[NEW_WITNESS_Z14],
        maps[NEW_WITNESS_Z14],
        ROOT_FIVE_SECONDS,
        payloads[ROOT_FIVE_SECONDS],
        "witnesses",
    )
    eliminated = {
        key
        for spec in (WITNESSES_Z7, WITNESSES_Z14, NEW_WITNESS_Z14)
        for key, result in maps[spec].items()
        if result["status"] == "INFEASIBLE"
    }
    if eliminated != set(root_witnesses):
        raise AssertionError(
            f"stored compression statuses cover {len(eliminated)} of "
            f"{len(root_witnesses)} root survivors"
        )

    print("PASS: all 9 pinned shell-18 artifacts match their SHA-256 digests")
    print("PASS: the reconstructed 823-target root frontier is 811 infeasible + 12 witnessed")
    print("PASS: all 12 root witnesses pass independent integer verification")
    print(
        "PASS: stored primitive-7/14 INFEASIBLE statuses cover all 12 "
        "root-survivor targets"
    )
    print(
        "RESULT: artifact integrity and decoded witnesses verified; "
        "the 1,296 UNSAT claims are not replayed by this checker"
    )


if __name__ == "__main__":
    main()
