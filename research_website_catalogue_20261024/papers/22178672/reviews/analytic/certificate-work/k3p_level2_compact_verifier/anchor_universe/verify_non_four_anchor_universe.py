#!/usr/bin/env python3
"""Independent no-atlas verification of the non-four anchor universe.

The producer artifact is opened only after a fresh derivation from the literal
grammar in :mod:`independent_non_four_core`.  Neither this verifier nor its
core imports the producer, the submitted atlas, a frozen theta/cycle artifact,
or the 176-anchor contract.

The cross-implementation comparison covers every one of the 133 semantic row
bodies and keys, both directed-graph hashes in every row, the public census,
the ordered-key digest, and the raw/restoration cardinalities.  The producer's
stream hashes for *non-equality category labels* are schema-checked but are not
cross-compared: this verifier deliberately finds equalities directly through
incidence-graph isomorphisms instead of reproducing the producer's topology
category partition.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

from independent_non_four_core import (
    IndependentUniverseError,
    canonical_bytes,
    digest,
    enumerate_non_four_anchor_universe,
)


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
DEFAULT_ARTIFACT = HERE / "artifacts/NON_FOUR_ANCHOR_UNIVERSE.json"
DEFAULT_REPORT = HERE / "INDEPENDENT_NON_FOUR_VERIFICATION.json"
EXPECTED_SCHEMA = "k3p-model-independent-non-four-anchor-universe-v1"
REPORT_SCHEMA = "k3p-independent-non-four-anchor-universe-verification-v1"
HEX64 = re.compile(r"[0-9a-f]{64}\Z")


class VerificationFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationFailure(message)


def sha_file(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def portable_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(PROJECT.resolve()))
    except ValueError:
        return resolved.name


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise VerificationFailure(f"artifact read:{path}:{exc}") from exc
    require(isinstance(value, dict), "artifact top level is not an object")
    return value


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    content = json.dumps(value, sort_keys=True, indent=2) + "\n"
    with temporary.open("w") as handle:
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def verify_cleanroom_import_boundary() -> dict[str, Any]:
    """Statically enforce the small allowed import surface of the core."""

    core_path = HERE / "independent_non_four_core.py"
    source = core_path.read_text()
    tree = ast.parse(source, filename=str(core_path))
    imported_roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            require(node.module is not None, "relative import in independent core")
            imported_roots.add(node.module.split(".")[0])

    allowed = {
        "__future__",
        "ast",
        "collections",
        "dataclasses",
        "hashlib",
        "itertools",
        "json",
        "typing",
        "networkx",
    }
    require(imported_roots <= allowed, f"core import boundary:{sorted(imported_roots - allowed)}")

    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    require(
        not (called_names & {"open", "exec", "eval", "compile", "__import__"}),
        f"core dynamic/file premise:{sorted(called_names & {'open', 'exec', 'eval', 'compile', '__import__'})}",
    )
    return {
        "core_sha256": sha_file(core_path),
        "allowed_import_roots": sorted(imported_roots),
        "core_file_reads": 0,
        "producer_or_atlas_imports": 0,
    }


ROW_FIELDS = {
    "anchor_key",
    "origin",
    "port_count",
    "relation",
    "source_graph_sha256",
    "target_graph_sha256",
    "structural_locator",
}
BODY_FIELDS = ROW_FIELDS - {"anchor_key"}


def validate_anchor_rows(rows: Any, label: str) -> dict[str, dict[str, Any]]:
    require(isinstance(rows, list), f"{label}:anchors is not a list")
    by_key: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(rows):
        require(isinstance(row, dict), f"{label}:row object:{index}")
        require(set(row) == ROW_FIELDS, f"{label}:row fields:{index}:{sorted(row)}")
        key = row["anchor_key"]
        require(isinstance(key, str) and HEX64.fullmatch(key) is not None, f"{label}:key:{index}")
        require(key not in by_key, f"{label}:duplicate key:{key}")
        require(
            isinstance(row["source_graph_sha256"], str)
            and HEX64.fullmatch(row["source_graph_sha256"]) is not None,
            f"{label}:source graph hash:{key}",
        )
        require(
            isinstance(row["target_graph_sha256"], str)
            and HEX64.fullmatch(row["target_graph_sha256"]) is not None,
            f"{label}:target graph hash:{key}",
        )
        require(row["relation"] in {"isomorphic", "triangle"}, f"{label}:relation:{key}")
        require(isinstance(row["structural_locator"], dict), f"{label}:locator:{key}")
        body = {field: row[field] for field in BODY_FIELDS}
        require(digest(body) == key, f"{label}:semantic key mismatch:{key}")
        by_key[key] = row
    return by_key


def validate_stream_record(value: Any, expected_rows: int, label: str) -> None:
    require(isinstance(value, dict), f"{label}:stream object")
    require(set(value) == {"rows", "sha256"}, f"{label}:stream fields")
    require(value["rows"] == expected_rows, f"{label}:rows:{value['rows']}")
    require(
        isinstance(value["sha256"], str) and HEX64.fullmatch(value["sha256"]) is not None,
        f"{label}:sha256",
    )


def sum_count_object(value: Any, label: str) -> int:
    require(isinstance(value, dict), f"{label}:count object")
    require(
        all(isinstance(key, str) and isinstance(count, int) and count >= 0 for key, count in value.items()),
        f"{label}:count entries",
    )
    return sum(value.values())


def validate_producer_stage_schema(
    artifact: dict[str, Any], derived: dict[str, Any]
) -> dict[str, Any]:
    """Validate producer-only category ledgers without adopting their labels."""

    primitive = artifact.get("primitive_counts")
    require(isinstance(primitive, dict), "primitive_counts")
    cycle = primitive.get("cycle")
    theta = primitive.get("theta2")
    tree = primitive.get("tree")
    require(isinstance(cycle, dict) and isinstance(theta, dict) and isinstance(tree, dict), "primitive sections")

    expected_primitive = derived["primitive_counts"]
    require(cycle.get("sources") == expected_primitive["cycle_sources"], "cycle sources")
    require(cycle.get("targets") == expected_primitive["cycle_targets"], "cycle targets")
    require(cycle.get("selected_incoming_targets") == 289, "cycle selected targets")
    require(cycle.get("marginalized_incoming_targets") == 831, "cycle marginalized targets")
    require(cycle.get("permutations") == expected_primitive["cycle_port_permutations"], "cycle permutations")
    require(theta.get("sources") == expected_primitive["theta2_sources"], "theta2 sources")
    require(theta.get("selected_incoming_targets") == expected_primitive["theta2_selected_incoming_targets"], "theta2 selected targets")
    require(theta.get("marginalized_incoming_targets") == expected_primitive["theta2_marginalized_incoming_targets"], "theta2 marginalized targets")
    require(theta.get("targets") == expected_primitive["theta2_targets"], "theta2 targets")
    require(theta.get("permutations") == expected_primitive["theta2_port_permutations"], "theta2 permutations")
    require(tree == {"sources": 1, "physical_anchors": 1}, "tree primitive counts")

    stage = artifact.get("stage_counts")
    require(isinstance(stage, dict), "stage_counts")
    expected_stage = {
        "cycle_base_presentations": derived["stage_counts"]["cycle_base_raw_presentations"],
        "cycle_restoration_presentations": derived["stage_counts"]["cycle_full_restoration_children"],
        "theta2_base_presentations": derived["stage_counts"]["theta2_base_raw_presentations"],
        "theta2_six_port_children": derived["stage_counts"]["theta2_six_port_children"],
        "theta2_seven_port_children": derived["stage_counts"]["theta2_seven_port_children"],
    }
    require(stage == expected_stage, f"stage count mismatch:{stage}")

    require(cycle.get("base_raw") == expected_stage["cycle_base_presentations"], "cycle base raw binding")
    require(cycle.get("restoration_raw") == expected_stage["cycle_restoration_presentations"], "cycle restoration raw binding")
    require(sum_count_object(cycle.get("base_counts"), "cycle base counts") == cycle["base_raw"], "cycle base partition")
    require(sum_count_object(cycle.get("restoration_counts"), "cycle restoration counts") == cycle["restoration_raw"], "cycle restoration partition")
    require(cycle["base_counts"].get("isomorphic") == 8, "cycle base isomorphic")
    require(cycle["base_counts"].get("triangle") == 16, "cycle base triangle")
    require(cycle["restoration_counts"].get("isomorphic") == 12, "cycle restored isomorphic")
    require(
        cycle.get("dummy_root_multiplicity")
        == derived["diagnostics"]["cycle"]["root_multiplicity_by_dummy_count"],
        "cycle root multiplicity",
    )
    validate_stream_record(cycle.get("base_enumeration"), cycle["base_raw"], "cycle base enumeration")
    validate_stream_record(cycle.get("restoration_enumeration"), cycle["restoration_raw"], "cycle restoration enumeration")

    require(theta.get("base_raw") == expected_stage["theta2_base_presentations"], "theta2 base raw binding")
    require(theta.get("raw_per_source") * theta.get("sources") == theta["base_raw"], "theta2 raw/source binding")
    require(sum_count_object(theta.get("base_counts"), "theta2 base counts") == theta["base_raw"], "theta2 base partition")
    require(theta["base_counts"].get("isomorphic") == derived["stage_counts"]["theta2_base_exact_equalities"], "theta2 base equality count")
    require(theta["base_counts"].get("incoming_boundary_mismatch") == derived["stage_counts"]["theta2_incoming_boundary_mismatches"], "theta2 incoming boundary mismatch")
    # The producer reports only dummy roots (one and two); the independent
    # diagnostic also includes the 24 zero-dummy physical rows.
    expected_dummy_roots = {
        key: value
        for key, value in derived["diagnostics"]["theta2"]["base_dummy_multiplicity"].items()
        if key != "0"
    }
    require(theta.get("dummy_root_multiplicity") == expected_dummy_roots, "theta2 dummy roots")
    require(theta.get("first_layer_role_requests") == derived["stage_counts"]["theta2_first_layer_role_requests"], "theta2 role requests")
    require(theta.get("six_port_children") == expected_stage["theta2_six_port_children"], "theta2 six-port children")
    require(theta.get("seven_port_children") == expected_stage["theta2_seven_port_children"], "theta2 seven-port children")
    require(sum_count_object(theta.get("six_port_counts"), "theta2 six counts") == theta["six_port_children"], "theta2 six partition")
    require(sum_count_object(theta.get("seven_port_counts"), "theta2 seven counts") == theta["seven_port_children"], "theta2 seven partition")
    require(theta["six_port_counts"].get("isomorphic") == derived["stage_counts"]["theta2_six_port_exact_equalities"], "theta2 six equalities")
    require(theta["seven_port_counts"].get("isomorphic") == derived["stage_counts"]["theta2_seven_port_exact_equalities"], "theta2 seven equalities")
    require(theta.get("six_port_isomorphic_continuations") == derived["stage_counts"]["theta2_six_port_continuations"], "theta2 continuations")
    validate_stream_record(theta.get("base_enumeration"), theta["base_raw"], "theta2 base enumeration")
    validate_stream_record(theta.get("six_port_enumeration"), theta["six_port_children"], "theta2 six enumeration")
    validate_stream_record(theta.get("seven_port_enumeration"), theta["seven_port_children"], "theta2 seven enumeration")
    return {
        "raw_and_restoration_cardinalities_compared": expected_stage,
        "producer_category_stream_hashes_schema_checked": 5,
        "producer_category_stream_hashes_cross_compared": 0,
    }


def verify_artifact(artifact_path: Path) -> dict[str, Any]:
    boundary = verify_cleanroom_import_boundary()

    # Complete the independent derivation before opening the regression
    # artifact.  The artifact therefore cannot seed the enumeration.
    derived = enumerate_non_four_anchor_universe()
    artifact = load_json(artifact_path)

    require(artifact.get("schema") == EXPECTED_SCHEMA, "artifact schema")
    require(artifact.get("status") == "PASS", "artifact status")
    require(isinstance(artifact.get("claim_boundary"), dict), "claim boundary")
    forbidden = artifact["claim_boundary"].get("forbidden_and_unused")
    require(isinstance(forbidden, list) and len(forbidden) >= 6, "forbidden premise declaration")

    payload = {
        key: value
        for key, value in artifact.items()
        if key not in {"payload_sha256", "operational"}
    }
    require(artifact.get("payload_sha256") == digest(payload), "artifact payload hash")

    derived_by_key = validate_anchor_rows(derived["anchors"], "independent")
    artifact_by_key = validate_anchor_rows(artifact.get("anchors"), "producer")
    require(set(derived_by_key) == set(artifact_by_key), "133-row semantic-key set")
    for key in sorted(derived_by_key):
        require(
            derived_by_key[key] == artifact_by_key[key],
            f"semantic row/graph hash mismatch:{key}",
        )

    public_census = {
        key: derived["census"][key]
        for key in ("total", "by_origin", "by_relation", "by_port_count")
    }
    require(artifact.get("census") == public_census, "public anchor census")
    require(
        artifact.get("ordered_anchor_key_sha256")
        == derived["ordered_anchor_key_sha256"],
        "ordered anchor-key digest",
    )
    require(
        derived["ordered_anchor_key_sha256"]
        == digest(sorted(artifact_by_key)),
        "ordered anchor-key digest reconstruction",
    )
    stage_check = validate_producer_stage_schema(artifact, derived)

    theta_diagnostics = derived["diagnostics"]["theta2"]
    root_movement = theta_diagnostics["marginalized_root_movement_mapping"]
    require(
        theta_diagnostics["incoming_boundary_mismatches"] == 176,
        "marginalized incoming parent count",
    )
    require(
        theta_diagnostics["marginalized_incoming_dummy_multiplicity"]
        == {"1": 56, "2": 88, "3": 32},
        "marginalized incoming dummy multiplicity",
    )
    require(
        theta_diagnostics["marginalized_incoming_full_isomorphic_paths_by_depth"]
        == {"1": 56, "2": 176, "3": 192},
        "marginalized incoming terminal paths",
    )
    require(root_movement["mapped"] == 424, "root-movement mapped count")
    require(root_movement["unmatched"] == 0, "root-movement unmatched count")
    require(
        root_movement["mapped_by_seed_origin"]
        == {
            "theta2_physical_k5": 56,
            "theta2_physical_k6": 176,
            "theta2_physical_k7": 192,
        },
        "root-movement seed-origin counts",
    )
    require(
        root_movement["terminal_paths_with_every_prefix_checked"] == 424,
        "root-movement prefix-covered paths",
    )
    require(
        root_movement["prefix_exact_equality_checks"] == 984,
        "root-movement prefix equality checks",
    )
    require(
        len(root_movement["mapping_rows"]) == 424
        and digest(root_movement["mapping_rows"])
        == root_movement["mapping_rows_sha256"],
        "root-movement mapping-row digest",
    )

    report = {
        "schema": REPORT_SCHEMA,
        "status": "PASS",
        "artifact": {
            "path": portable_path(artifact_path),
            "sha256": sha_file(artifact_path),
            "schema": artifact["schema"],
            "payload_sha256": artifact["payload_sha256"],
        },
        "independence_boundary": {
            **boundary,
            "derivation_completed_before_artifact_read": True,
            "contract_reads": 0,
            "frozen_theta_or_cycle_artifact_reads": 0,
            "submitted_atlas_imports": 0,
            "producer_imports": 0,
            "method": (
                "direct exact incidence-isomorphism permutation enumeration; "
                "producer topology-category partitions are not reused"
            ),
            "producer_only_non_equality_stream_digests": (
                "schema and declared row counts checked; digest values intentionally "
                "outside the cross-implementation comparison"
            ),
        },
        "comparisons": {
            "semantic_rows": len(derived_by_key),
            "semantic_key_set_equal": True,
            "every_row_body_equal": True,
            "every_source_graph_hash_equal": True,
            "every_target_graph_hash_equal": True,
            "census_equal": True,
            "ordered_anchor_key_sha256": derived["ordered_anchor_key_sha256"],
            **stage_check,
        },
        "independent_census": public_census,
        "independent_stage_counts": derived["stage_counts"],
        "marginalized_incoming_root_movement_certificate": {
            "scope": (
                "All fully physical graph-isomorphic restoration paths from "
                "the 176 theta2 parents whose distinguished target incoming "
                "boundary was marginalized."
            ),
            "incoming_boundary_mismatch_parents": theta_diagnostics[
                "incoming_boundary_mismatches"
            ],
            "dummy_multiplicity": theta_diagnostics[
                "marginalized_incoming_dummy_multiplicity"
            ],
            "terminal_paths_by_restoration_depth": theta_diagnostics[
                "marginalized_incoming_full_isomorphic_paths_by_depth"
            ],
            **root_movement,
        },
    }
    report["payload_sha256"] = digest(
        {
            key: value
            for key, value in report.items()
            if key not in {"payload_sha256", "operational"}
        }
    )
    return report


def main(argv: list[str] | None = None) -> int:
    if not __debug__:
        raise VerificationFailure("optimized mode forbidden")
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path, default=DEFAULT_ARTIFACT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args(argv)
    report = verify_artifact(args.artifact.resolve())
    atomic_json(args.report.resolve(), report)
    print(
        "K3P_INDEPENDENT_NON_FOUR_ANCHOR_UNIVERSE_PASS "
        f"anchors={report['comparisons']['semantic_rows']} "
        f"key_root={report['comparisons']['ordered_anchor_key_sha256']}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (IndependentUniverseError, VerificationFailure) as exc:
        print(f"K3P_INDEPENDENT_NON_FOUR_ANCHOR_UNIVERSE_FAIL {exc}")
        raise SystemExit(1) from exc
