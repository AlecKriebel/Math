#!/usr/bin/env python3
"""Fail-closed gate verifier for the candidate principal-D+ K2P theorem.

The current expected outcome is a verified refusal to promote K2P-SAME.  This
script validates all locally cited hashes, optionally replays available exact
layers, and independently enforces the raw-universe and restoration ledgers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any


ASSEMBLY = Path(__file__).resolve().parent
PROJECT = ASSEMBLY.parents[1]
CONFIG_SCHEMA = "k2p-principal-d-plus-theorem-gates-v1"
INVENTORY_SCHEMA = "k2p-theorem-evidence-inventory-v1"
RAW_SCHEMA = "k2p-raw-universe-ledger-status-v1"
RESTORATION_SCHEMA = "k2p-restoration-ledger-status-v1"
PROMOTABLE_EVIDENCE = frozenset(("exact_replayable", "hash_bound_replayable"))
REQUIRED_GATE_IDS = frozenset((
    "principal_domain_rooting",
    "three_port_geometry",
    "decorated_tree_of_blobs",
    "physical_bridge_fibre",
    "paired_marginal_open_image",
    "raw_universe_ledger",
    "direct_four_port_overlay",
    "five_port_theta2_local",
    "restoration_forest",
    "coherent_probes",
    "finite_semialgebraic_selection",
    "simultaneous_physical_gluing",
    "genericity",
    "reconstruction",
))


def fail(code: str, detail: Any = None) -> "None":
    raise SystemExit(code if detail is None else f"{code}: {detail}")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail("THEOREM_GATE_DUPLICATE_JSON_KEY", key)
        result[key] = value
    return result


def load_json(path: Path, code: str) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle, object_pairs_hook=unique_object)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(code, f"{path}: {exc}")
    if not isinstance(value, dict):
        fail(code, f"top-level value is not an object: {path}")
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        fail("THEOREM_EVIDENCE_READ_FAIL", f"{path}: {exc}")
    return digest.hexdigest()


def safe_project_file(relative: str) -> Path:
    pure = PurePosixPath(relative)
    if (
        not relative or pure.is_absolute() or ".." in pure.parts or "." in pure.parts
        or "\\" in relative or pure.as_posix() != relative
    ):
        fail("THEOREM_EVIDENCE_UNSAFE_PATH", relative)
    path = PROJECT.joinpath(*pure.parts)
    try:
        mode = path.lstat().st_mode
        path.resolve().relative_to(PROJECT.resolve())
    except (OSError, ValueError) as exc:
        fail("THEOREM_EVIDENCE_PATH_FAIL", f"{relative}: {exc}")
    if not stat.S_ISREG(mode):
        fail("THEOREM_EVIDENCE_NOT_REGULAR", relative)
    return path


def validate_hash_entry(entry: dict[str, Any], label: str) -> None:
    if not isinstance(entry, dict) or set(entry) < {"path", "sha256"}:
        fail("THEOREM_EVIDENCE_ENTRY_FAIL", label)
    relative, expected = entry.get("path"), entry.get("sha256")
    if not isinstance(relative, str) or not isinstance(expected, str):
        fail("THEOREM_EVIDENCE_ENTRY_TYPE_FAIL", label)
    if len(expected) != 64 or any(character not in "0123456789abcdef" for character in expected):
        fail("THEOREM_EVIDENCE_HASH_FORMAT_FAIL", label)
    observed = sha256_file(safe_project_file(relative))
    if observed != expected:
        fail("THEOREM_EVIDENCE_HASH_MISMATCH", relative)


def validate_inventory(inventory: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if inventory.get("schema") != INVENTORY_SCHEMA:
        fail("THEOREM_INVENTORY_SCHEMA_FAIL")
    archives = inventory.get("archive_sources")
    layers = inventory.get("layers")
    if not isinstance(archives, list) or not isinstance(layers, list):
        fail("THEOREM_INVENTORY_SHAPE_FAIL")
    for index, entry in enumerate(archives):
        validate_hash_entry(entry, f"archive_sources[{index}]")
    layer_by_id: dict[str, dict[str, Any]] = {}
    for index, layer in enumerate(layers):
        if not isinstance(layer, dict) or not isinstance(layer.get("id"), str):
            fail("THEOREM_LAYER_SHAPE_FAIL", index)
        layer_id = layer["id"]
        if layer_id in layer_by_id:
            fail("THEOREM_LAYER_DUPLICATE_ID", layer_id)
        evidence = layer.get("local_evidence")
        if not isinstance(evidence, list):
            fail("THEOREM_LAYER_EVIDENCE_SHAPE_FAIL", layer_id)
        for evidence_index, entry in enumerate(evidence):
            validate_hash_entry(entry, f"{layer_id}.local_evidence[{evidence_index}]")
        eligible = layer.get("evidence_level") in PROMOTABLE_EVIDENCE
        if bool(layer.get("promotion_eligible")) != eligible:
            fail("THEOREM_LAYER_ELIGIBILITY_INCONSISTENT", layer_id)
        if eligible and not evidence:
            fail("THEOREM_LAYER_ELIGIBLE_WITHOUT_EVIDENCE", layer_id)
        layer_by_id[layer_id] = layer
    return layer_by_id


def raw_ledger_blockers(raw: dict[str, Any]) -> list[str]:
    if raw.get("schema") != RAW_SCHEMA:
        fail("RAW_LEDGER_SCHEMA_FAIL")
    blockers: list[str] = []
    if raw.get("complete") is not True:
        blockers.append("RAW_LEDGER_INCOMPLETE")
    if raw.get("gap_count") != 0:
        blockers.append(f"RAW_LEDGER_GAPS={raw.get('gap_count')}")
    for field in (
        "graph_derived", "partition_identity_verified",
        "raw_to_canonical_map_bound", "valid_dimension_upper_bounds_certified",
    ):
        if raw.get(field) is not True:
            blockers.append(f"RAW_LEDGER_{field.upper()}_FALSE")
    scopes = raw.get("scopes")
    if not isinstance(scopes, dict) or set(scopes) != {"four_port", "five_port_theta2"}:
        blockers.append("RAW_LEDGER_SCOPE_SET_FAIL")
    else:
        for scope_name in ("four_port", "five_port_theta2"):
            row = scopes[scope_name]
            if not isinstance(row, dict):
                blockers.append(f"RAW_LEDGER_{scope_name.upper()}_SHAPE_FAIL")
                continue
            expected = row.get("expected_presentations")
            accounted = row.get("accounted_presentations")
            if not isinstance(expected, int) or expected <= 0 or accounted != expected:
                blockers.append(f"RAW_LEDGER_{scope_name.upper()}_PARTITION_FAIL")
    return blockers


def restoration_ledger_blockers(restoration: dict[str, Any]) -> list[str]:
    if restoration.get("schema") != RESTORATION_SCHEMA:
        fail("RESTORATION_LEDGER_SCHEMA_FAIL")
    blockers: list[str] = []
    exact_values = {
        "expected_parent_count": 997,
        "expected_child_requests": 2962,
        "child_records_bound": 2962,
        "closed_child_requests": 2962,
        "unresolved_child_requests": 0,
        "incoherent_survivors": 0,
        "gap_count": 0,
    }
    if restoration.get("complete") is not True:
        blockers.append("RESTORATION_LEDGER_INCOMPLETE")
    for field, expected in exact_values.items():
        if restoration.get(field) != expected:
            blockers.append(
                f"RESTORATION_LEDGER_{field.upper()}={restoration.get(field)}"
            )
    for field in (
        "all_child_records_hash_bound", "all_implications_replayed",
        "coherent_probe_deck_verified",
    ):
        if restoration.get(field) is not True:
            blockers.append(f"RESTORATION_LEDGER_{field.upper()}_FALSE")
    return blockers


def gate_blockers(
    config: dict[str, Any],
    layer_by_id: dict[str, dict[str, Any]],
) -> tuple[list[str], dict[str, list[str]]]:
    if config.get("schema") != CONFIG_SCHEMA:
        fail("THEOREM_GATE_CONFIG_SCHEMA_FAIL")
    if config.get("candidate_outcome") != "K2P-SAME":
        fail("THEOREM_GATE_OUTCOME_FAIL")
    gates = config.get("gates")
    required = config.get("required_gate_ids")
    if not isinstance(gates, list) or not isinstance(required, list):
        fail("THEOREM_GATE_CONFIG_SHAPE_FAIL")
    if set(required) != REQUIRED_GATE_IDS or len(required) != len(REQUIRED_GATE_IDS):
        fail("THEOREM_GATE_REQUIRED_ID_SET_FAIL")
    gate_by_id: dict[str, dict[str, Any]] = {}
    for gate in gates:
        if not isinstance(gate, dict) or not isinstance(gate.get("id"), str):
            fail("THEOREM_GATE_ROW_SHAPE_FAIL")
        gate_id = gate["id"]
        if gate_id in gate_by_id:
            fail("THEOREM_GATE_DUPLICATE_ID", gate_id)
        gate_by_id[gate_id] = gate
    if set(gate_by_id) != REQUIRED_GATE_IDS:
        fail("THEOREM_GATE_ROW_ID_SET_FAIL", sorted(set(gate_by_id) ^ REQUIRED_GATE_IDS))

    details: dict[str, list[str]] = {}
    blockers: list[str] = []
    for gate_id in sorted(REQUIRED_GATE_IDS):
        gate = gate_by_id[gate_id]
        reasons: list[str] = []
        references = gate.get("evidence_refs")
        if not isinstance(references, list) or any(not isinstance(item, str) for item in references):
            fail("THEOREM_GATE_EVIDENCE_REFS_FAIL", gate_id)
        for reference in references:
            layer = layer_by_id.get(reference)
            if layer is None:
                fail("THEOREM_GATE_UNKNOWN_EVIDENCE_REF", f"{gate_id}: {reference}")
            if not layer.get("promotion_eligible"):
                reasons.append(f"EVIDENCE_NOT_PROMOTION_ELIGIBLE:{reference}")
        if not references:
            reasons.append("NO_BOUND_EVIDENCE")
        if gate.get("promotion_ready") is not True:
            reasons.append("PROMOTION_READY_FALSE")
        if gate.get("independent_replay") is not True:
            reasons.append("INDEPENDENT_REPLAY_FALSE")
        if gate.get("evidence_status") not in PROMOTABLE_EVIDENCE:
            reasons.append(f"EVIDENCE_STATUS:{gate.get('evidence_status')}")
        if reasons:
            details[gate_id] = reasons
            blockers.extend(f"GATE:{gate_id}:{reason}" for reason in reasons)
    return blockers, details


def child_environment() -> dict[str, str]:
    environment = dict(os.environ)
    environment.pop("PYTHONOPTIMIZE", None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment.setdefault("PYTHONHASHSEED", "0")
    return environment


def run_available_replays(
    layers: dict[str, dict[str, Any]], timeout_seconds: float
) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    for layer_id in sorted(layers):
        replay = layers[layer_id].get("replay")
        if replay is None:
            continue
        if not isinstance(replay, dict) or not isinstance(replay.get("command"), list):
            fail("THEOREM_REPLAY_SPEC_FAIL", layer_id)
        command = [
            sys.executable if item == "{python}" else item
            for item in replay["command"]
        ]
        try:
            completed = subprocess.run(
                command,
                cwd=PROJECT,
                env=child_environment(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired:
            fail("THEOREM_REPLAY_TIMEOUT", layer_id)
        if completed.returncode != 0:
            output = (completed.stdout + completed.stderr).decode(errors="replace")
            fail("THEOREM_REPLAY_FAIL", f"{layer_id}: {output[-4000:]}")
        if completed.stderr:
            fail(
                "THEOREM_REPLAY_STDERR",
                f"{layer_id}: {completed.stderr.decode(errors='replace')[-4000:]}",
            )
        if "stdout_golden" in replay:
            golden = safe_project_file(replay["stdout_golden"]).read_bytes()
            if completed.stdout != golden:
                fail("THEOREM_REPLAY_STDOUT_MISMATCH", layer_id)
        if "terminal_line" in replay:
            lines = completed.stdout.splitlines()
            terminal = replay["terminal_line"].encode()
            if terminal not in lines:
                fail("THEOREM_REPLAY_TERMINAL_MISSING", layer_id)
        results.append({
            "layer": layer_id,
            "stdout_sha256": hashlib.sha256(completed.stdout).hexdigest(),
        })
        print(f"THEOREM_LAYER_REPLAY_PASS layer={layer_id}")
    return results


def main() -> None:
    if not __debug__:
        fail("THEOREM_GATE_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ASSEMBLY / "THEOREM_GATES.json")
    parser.add_argument("--inventory", type=Path, default=ASSEMBLY / "EVIDENCE_INVENTORY.json")
    parser.add_argument("--raw-ledger", type=Path, default=ASSEMBLY / "raw_universe_ledger.status.json")
    parser.add_argument("--restoration-ledger", type=Path, default=ASSEMBLY / "restoration_ledger.status.json")
    parser.add_argument("--replay-available", action="store_true")
    parser.add_argument("--require-promotable", action="store_true")
    parser.add_argument("--timeout-seconds", type=float, default=180.0)
    args = parser.parse_args()
    if args.timeout_seconds <= 0:
        fail("THEOREM_REPLAY_TIMEOUT_INVALID")

    inventory = load_json(args.inventory.resolve(), "THEOREM_INVENTORY_JSON_FAIL")
    config = load_json(args.config.resolve(), "THEOREM_GATE_CONFIG_JSON_FAIL")
    raw = load_json(args.raw_ledger.resolve(), "RAW_LEDGER_JSON_FAIL")
    restoration = load_json(args.restoration_ledger.resolve(), "RESTORATION_LEDGER_JSON_FAIL")
    layers = validate_inventory(inventory)
    blockers, gate_details = gate_blockers(config, layers)
    raw_reasons = raw_ledger_blockers(raw)
    restoration_reasons = restoration_ledger_blockers(restoration)
    blockers.extend(raw_reasons)
    blockers.extend(restoration_reasons)
    promotable = not blockers
    expected_status = "PROMOTABLE" if promotable else "NOT_PROMOTABLE"
    if config.get("status") != expected_status:
        fail(
            "THEOREM_GATE_CONFIG_STATUS_MISMATCH",
            {"declared": config.get("status"), "computed": expected_status},
        )

    replay_results: list[dict[str, str]] = []
    if args.replay_available:
        replay_results = run_available_replays(layers, args.timeout_seconds)
    report = {
        "candidate_outcome": "K2P-SAME",
        "gate_blocker_count": len(blockers),
        "gate_details": gate_details,
        "promotable": promotable,
        "raw_ledger_blockers": raw_reasons,
        "replay_results": replay_results,
        "restoration_ledger_blockers": restoration_reasons,
        "schema": "k2p-principal-d-plus-theorem-gate-report-v1",
    }
    if promotable:
        print("K2P_SAME_PROMOTION_GATES_PASS")
        print(json.dumps(report, indent=2, sort_keys=True))
        return
    print("K2P_SAME_NOT_PROMOTABLE")
    print(json.dumps(report, indent=2, sort_keys=True))
    if args.require_promotable:
        fail("K2P_SAME_PROMOTION_REFUSED", f"blockers={len(blockers)}")


if __name__ == "__main__":
    main()
