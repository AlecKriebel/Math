#!/usr/bin/env python3
"""Independent consumer for the first PC-PARTIAL compression checkpoint.

This module deliberately does not import the producer helpers.  It verifies the
immutable release anchor, exact Cartesian finite universes, reversible direct
certificate templates, and direction-sensitive full-map/restoration evidence.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import itertools
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
TEMPLATES = HERE.parent / "templates"
STRICT_JSON_DIR = PROJECT / "work/final_theorem_release"
if str(STRICT_JSON_DIR) not in sys.path:
    sys.path.insert(0, str(STRICT_JSON_DIR))

from strict_json import (  # noqa: E402
    StrictJSONError,
    decode_json_document,
    iter_canonical_gzip_jsonl,
    load_canonical_gzip_json,
)

BASELINE = HERE / "PROOF_COMPRESSION_BASELINE.json"
BASELINE_MD = HERE / "PROOF_COMPRESSION_BASELINE.md"
UNIVERSE_MD = HERE / "FINITE_UNIVERSE_COMPLETENESS.md"
TABLE = TEMPLATES / "DIRECT_CERTIFICATE_TEMPLATE_TABLE.json"
TABLE_MD = TEMPLATES / "DIRECT_CERTIFICATE_TEMPLATE_TABLE.md"
OUTPUT = HERE / "FAMILY_COVERAGE_EQUIVALENCE_CERTIFICATE.json"

LOCK_REL = "work/final_theorem_release/RELEASE_LOCK.json"
LOCK_SHA = "ae48ec2e052db0aec8fca25482d75847fc34333cc91e9eaa7fc6b49e35c55914"
LOCK_PAYLOAD = "da68cd2d5e259ac7c121c80b6f6c5b5c29285ccdb4ceb831a69b54252fa72e54"
ATLAS_REL = "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
EXPECTED_PRIMITIVE_GRAMMAR_SHA256 = (
    "d5e7608f70a2243df605dee6e35d0ea6af74e4e47b42142e91ddfa4cbcbad09b"
)
RAW4_LEDGER = "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_ledger.jsonl.gz"
THETA2_LEDGER = "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_ledger.jsonl.gz"
CYCLE_BASE = "work/cycle_three_port_closure/promotion/cycle_base_authoritative.jsonl.gz"
CYCLE_FULL = "work/cycle_three_port_closure/promotion/cycle_full_authoritative.jsonl.gz"
RAW4_REGISTRY = "work/corrected_composite_ledgers/artifacts/raw4_terminal_certificate_registry.json.gz"
THETA2_DIRECT = "work/theta2_five_port_closure/artifacts/direct_proof_certificates.json.gz"
CYCLE_QUADRATICS = "work/cycle_three_port_closure/artifacts/quadratic_certificates.json"
RESTORATION = "work/restoration_sign_reclassification/corrected_restoration_forest.json"
DIRECT36 = "package/referee/k2p_offline_sweep_portable/proofs/four_port_direct_residual_closure_certificate.json"

EXPECTED_CORES = {
    "cycle": {
        "arcs": (("S", "X"), ("S", "X")),
        "retics": ("X",),
        "sinks": ("X",),
        "repairs": ((0,), (1,)),
    },
    "theta0": {
        "arcs": (("S", "U"), ("S", "V"), ("U", "X"), ("V", "X"), ("U", "V")),
        "retics": ("V", "X"),
        "sinks": ("X",),
        "repairs": ((2, 3), (3, 4)),
    },
    "theta1": {
        "arcs": (("S", "U"), ("S", "X"), ("V", "X"), ("U", "V"), ("U", "V")),
        "retics": ("V", "X"),
        "sinks": ("X",),
        "repairs": ((2, 3), (2, 4)),
    },
    "theta2": {
        "arcs": (("S", "U"), ("S", "V"), ("U", "X0"), ("V", "X0"), ("U", "X1"), ("V", "X1")),
        "retics": ("X0", "X1"),
        "sinks": ("X0", "X1"),
        "repairs": ((2, 3), (2, 5), (3, 4), (4, 5)),
    },
    "theta3": {
        "arcs": (("S", "U"), ("S", "X0"), ("V", "X0"), ("U", "X1"), ("V", "X1"), ("U", "V")),
        "retics": ("X0", "X1"),
        "sinks": ("X0", "X1"),
        "repairs": ((2,), (4,)),
    },
}


class VerificationFailure(RuntimeError):
    pass


def need(condition: bool, code: str, detail: Any | None = None) -> None:
    if not condition:
        raise VerificationFailure(code if detail is None else f"{code}:{detail}")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe(relative: str) -> Path:
    requested = Path(relative)
    need(not requested.is_absolute(), "ABSOLUTE_PATH", relative)
    need(".." not in requested.parts, "PATH_ESCAPE", relative)
    path = PROJECT / requested
    need(path.resolve().is_relative_to(PROJECT.resolve()), "PATH_ESCAPE", relative)
    need(path.is_file(), "FILE_MISSING", relative)
    return path


def read_json(path: Path) -> dict[str, Any]:
    try:
        return decode_json_document(
            path.read_bytes(), label=str(path), require_object=True
        )
    except (OSError, StrictJSONError) as error:
        raise VerificationFailure(
            f"JSON_STRICT_DECODE_FAIL:{path}:{error}"
        ) from error


def read_gzip_json(relative: str) -> dict[str, Any]:
    path = safe(relative)
    try:
        value = load_canonical_gzip_json(path, label=relative)
    except (OSError, StrictJSONError) as error:
        raise VerificationFailure(
            f"GZIP_JSON_STRICT_DECODE_FAIL:{relative}:{error}"
        ) from error
    need(isinstance(value, dict), "GZIP_JSON_NOT_OBJECT", relative)
    return value


def iter_jsonl(relative: str) -> Iterable[dict[str, Any]]:
    path = safe(relative)
    try:
        for line_number, value in enumerate(
            iter_canonical_gzip_jsonl(path, label=relative), 1
        ):
            need(isinstance(value, dict), "JSONL_NOT_OBJECT", f"{relative}:{line_number}")
            yield value
    except (OSError, StrictJSONError) as error:
        raise VerificationFailure(
            f"JSONL_STRICT_DECODE_FAIL:{relative}:{error}"
        ) from error


def verify_seal(value: dict[str, Any], code: str) -> None:
    observed = value.get("payload_sha256")
    need(isinstance(observed, str), f"{code}_SEAL_MISSING")
    payload = dict(value)
    del payload["payload_sha256"]
    need(object_sha(payload) == observed, f"{code}_SEAL_MISMATCH")


def verify_release_and_transitive_hashes() -> dict[str, str]:
    lock_path = safe(LOCK_REL)
    need(file_sha(lock_path) == LOCK_SHA, "IMMUTABLE_LOCK_FILE_SHA")
    lock = read_json(lock_path)
    verify_seal(lock, "LOCK")
    need(lock["payload_sha256"] == LOCK_PAYLOAD, "IMMUTABLE_LOCK_PAYLOAD")
    need(lock["schema"] == "k2p-principal-d-plus-final-theorem-release-lock-v1", "LOCK_SCHEMA")
    need(lock["candidate_outcome"] == "K2P-SAME", "LOCK_OUTCOME")
    need(lock["promotion_ready"] is True, "LOCK_NOT_READY")
    need(lock["blockers"] == [] and lock["missing_required_files"] == [], "LOCK_GAPS")
    locked: dict[str, str] = {}
    for relative, record in lock["files"].items():
        need(isinstance(record, dict) and isinstance(record.get("sha256"), str), "LOCK_RECORD")
        digest = record["sha256"]
        need(file_sha(safe(relative)) == digest, "OUTER_HASH", relative)
        locked[relative] = digest

    direct_root = PROJECT / "package/referee/k2p_offline_sweep_portable"
    for lock_name in ("DIRECT_CLOSURE_LOCK.json", "INPUT_LOCK.json"):
        nested = read_json(direct_root / lock_name)
        for name, digest in nested["files"].items():
            path = direct_root / name
            need(path.is_file() and file_sha(path) == digest, "DIRECT_NESTED_HASH", name)
            relative = str(path.relative_to(PROJECT))
            need(relative not in locked or locked[relative] == digest, "NESTED_HASH_CONFLICT")
            locked[relative] = digest

    for relative in (
        "work/rank_upper_certificates/MANIFEST.sha256",
        "work/cycle_three_port_closure/MANIFEST.sha256",
    ):
        manifest = safe(relative)
        for line in manifest.read_text(encoding="utf-8").splitlines():
            digest, name = line.split("  ", 1)
            path = manifest.parent / name
            need(path.is_file() and file_sha(path) == digest, "MANIFEST_HASH", path)
            item = str(path.relative_to(PROJECT))
            need(item not in locked or locked[item] == digest, "MANIFEST_HASH_CONFLICT")
            locked[item] = digest
    need(len(locked) == 407, "TRANSITIVE_FILE_COUNT", len(locked))
    return locked


def parse_cores() -> dict[str, Any]:
    tree = ast.parse(safe(ATLAS_REL).read_text(encoding="utf-8"), filename=ATLAS_REL)
    found: list[Any] = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "CORES" for target in node.targets
        ):
            found.append(ast.literal_eval(node.value))
    need(found == [EXPECTED_CORES], "PRIMITIVE_CORE_ENCODING")
    need(
        object_sha({"CORES": found[0]}) == EXPECTED_PRIMITIVE_GRAMMAR_SHA256,
        "PRIMITIVE_GRAMMAR_SEMANTIC_HASH",
    )
    return found[0]


def weak_compositions(total: int, bins: int):
    if bins == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in weak_compositions(total - first, bins - 1):
            yield (first,) + rest


def target_keys(k: int, incoming_selected: bool, cores: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    outgoing = k - int(incoming_selected)
    for core, spec in cores.items():
        repairs = ((None, ()),) if core == "cycle" else tuple(enumerate(spec["repairs"]))
        for mask in range(1 << len(spec["sinks"])):
            ordinary = outgoing - mask.bit_count()
            if ordinary < 0:
                continue
            for composition in weak_compositions(ordinary, len(spec["arcs"])):
                for repair_index, repair in repairs:
                    result.append(
                        {
                            "core": core,
                            "incoming_selected": incoming_selected,
                            "selected_sink_mask": mask,
                            "weak_composition": list(composition),
                            "repair_index": repair_index,
                            "repair_arc_indices": list(repair),
                        }
                    )
    need(len({canonical_bytes(row) for row in result}) == len(result), "TARGET_KEY_DUPLICATE")
    return result


def verify_formula(baseline: dict[str, Any]) -> dict[str, int]:
    cores = parse_cores()
    cases = {
        "three_port_selected_incoming": (3, True, 289),
        "three_port_marginalized_incoming": (3, False, 831),
        "four_port_selected_incoming": (4, True, 831),
        "four_port_marginalized_incoming": (4, False, 1983),
        "five_port_selected_incoming": (5, True, 1983),
        "five_port_marginalized_incoming": (5, False, 4155),
    }
    observed: dict[str, int] = {}
    frozen_cases = baseline["finite_universes"]["completion_formula_cases"]
    for label, (k, incoming, expected) in cases.items():
        keys = target_keys(k, incoming, cores)
        need(len(keys) == expected, "TARGET_KEY_COUNT", label)
        need(frozen_cases[label]["total"] == expected, "BASELINE_TARGET_COUNT", label)
        need(
            frozen_cases[label]["ordered_target_key_sha256"] == object_sha(keys),
            "TARGET_KEY_ORDERED_ROOT",
            label,
        )
        observed[label] = expected
    return observed


def verify_composite_cartesian(
    relative: str,
    *,
    schema: str,
    sources: int,
    targets: int,
    ports: int,
    expected_categories: dict[str, int],
    ti_direction: str,
) -> tuple[Counter[str], Counter[str]]:
    permutations = list(itertools.permutations(range(ports)))
    terminal_presentations: Counter[str] = Counter()
    categories: Counter[str] = Counter()
    rows_per_source = targets * len(permutations)
    row_count = 0
    for ordinal, row in enumerate(iter_jsonl(relative)):
        row_count += 1
        need(row["schema"] == schema, "COMPOSITE_SCHEMA", ordinal)
        need(row["raw_id"] == ordinal, "RAW_ID_ORDER", ordinal)
        source, remainder = divmod(ordinal, rows_per_source)
        target, permutation_index = divmod(remainder, len(permutations))
        need(source < sources, "SOURCE_INDEX_RANGE", ordinal)
        need(row["source_index"] == source, "SOURCE_CARTESIAN", ordinal)
        need(row["target_index"] == target, "TARGET_CARTESIAN", ordinal)
        need(row["permutation_index"] == permutation_index, "PERMUTATION_CARTESIAN", ordinal)
        need(tuple(row["port_permutation"]) == permutations[permutation_index], "PORT_PERMUTATION", ordinal)
        need("tree_sunlet" not in canonical_bytes(row).decode("utf-8").lower(), "ROOTED_ORACLE_FIELD", ordinal)
        category = row["corrected_category"]
        categories[category] += 1
        evidence = row["evidence_binding"]
        if category == "direct_terminal_presentation":
            terminal_presentations[evidence["terminal_class_id"]] += 1
        if category == "full_map_Ti_strict_sign":
            need(evidence["kind"] == "exact_whole_map_Ti_zero_sign_certificate", "TI_EVIDENCE_KIND")
            need(isinstance(evidence["chosen_T_orientation_label"], int), "TI_ORIENTATION")
            need(len(evidence["coordinate_triple"]) == 3, "TI_TRIPLE")
            if ti_direction == "source_sign_target_zero":
                need(row["exact_reason"] == "whole_map_source_strict_sign_target_zero", "RAW4_TI_REASON")
                need(evidence["target_identically_zero"] is True, "RAW4_TI_ZERO_SIDE")
                need(evidence["target_pullback_term_count"] == 0, "RAW4_TI_TARGET_TERMS")
                need(evidence["source_pullback_term_count"] > 0, "RAW4_TI_SOURCE_TERMS")
                need(evidence["source_strict_sign"] == "strictly_negative", "RAW4_TI_SIGN")
            else:
                need(row["exact_reason"] == "whole_map_source_zero_target_strict_sign", "THETA2_TI_REASON")
                need(evidence["source_identically_zero"] is True, "THETA2_TI_ZERO_SIDE")
                need(evidence["source_pullback_term_count"] == 0, "THETA2_TI_SOURCE_TERMS")
                need(evidence["target_pullback_term_count"] > 0, "THETA2_TI_TARGET_TERMS")
                need(evidence["target_strict_sign"] == "strictly_negative", "THETA2_TI_SIGN")
    need(row_count == sources * targets * math.factorial(ports), "COMPOSITE_ROW_COUNT", relative)
    need(categories == Counter(expected_categories), "COMPOSITE_CATEGORY_COUNTS", relative)
    return categories, terminal_presentations


def verify_cycle() -> dict[str, Any]:
    permutations = list(itertools.permutations(range(3)))
    base_counts: Counter[str] = Counter()
    for ordinal, row in enumerate(iter_jsonl(CYCLE_BASE)):
        need(row["raw_id"] == ordinal, "CYCLE_BASE_RAW_ID")
        source, rem = divmod(ordinal, 1120 * 6)
        target, permutation = divmod(rem, 6)
        need((row["source_index"], row["target_index"], row["permutation_index"]) == (source, target, permutation), "CYCLE_BASE_CARTESIAN")
        need(tuple(row["port_permutation"]) == permutations[permutation], "CYCLE_BASE_PERMUTATION")
        payload = {key: value for key, value in row.items() if key != "authoritative_row_sha256"}
        need(object_sha(payload) == row["authoritative_row_sha256"], "CYCLE_BASE_ROW_HASH")
        base_counts[row["terminal_kind"]] += 1
    need(sum(base_counts.values()) == 13440, "CYCLE_BASE_COUNT")
    need(base_counts == Counter({"fixed_full_restoration_obligation": 5964, "full_map_Ti_strict_sign": 7452, "labelled_isomorphism": 8, "ordinary_triangle_relation": 16}), "CYCLE_BASE_CENSUS")

    full_counts: Counter[str] = Counter()
    full_port_counts: Counter[int] = Counter()
    for ordinal, row in enumerate(iter_jsonl(CYCLE_FULL)):
        need(row["raw_id"] == ordinal, "CYCLE_FULL_RAW_ID")
        payload = {key: value for key, value in row.items() if key != "authoritative_row_sha256"}
        need(object_sha(payload) == row["authoritative_row_sha256"], "CYCLE_FULL_ROW_HASH")
        need(
            row["port_count"] == 3 + len(row["dummy_roles_in_label_order"]),
            "CYCLE_FULL_PORT_COUNT",
        )
        need(isinstance(row["fixed_full_transport_sha256"], str), "CYCLE_FULL_TRANSPORT")
        full_counts[row["terminal_kind"]] += 1
        full_port_counts[row["port_count"]] += 1
    need(sum(full_counts.values()) == 536364, "CYCLE_FULL_COUNT")
    need(full_counts == Counter({"displayed_quartet_strict_separator": 535920, "exact_directional_quadratic": 132, "full_map_Ti_strict_sign": 300, "labelled_isomorphism": 12}), "CYCLE_FULL_CENSUS")
    need(
        full_port_counts == Counter({4: 972, 5: 22752, 6: 167040, 7: 345600}),
        "CYCLE_FULL_PORT_CENSUS",
    )
    return {
        "base": dict(sorted(base_counts.items())),
        "full": dict(sorted(full_counts.items())),
        "full_port_counts": {str(key): value for key, value in sorted(full_port_counts.items())},
    }


BODY_FIELDS = ("coefficients", "coordinate_pairs", "degree", "weight")


def template_assignment_map(templates: list[dict[str, Any]]) -> dict[str, tuple[str, dict[str, Any], dict[str, Any]]]:
    result: dict[str, tuple[str, dict[str, Any], dict[str, Any]]] = {}
    for template in templates:
        need(object_sha(template["body"]) == template["body_sha256"], "TEMPLATE_BODY_HASH")
        for assignment in template["assignments"]:
            class_id = assignment["canonical_class"]
            need(class_id not in result, "DUPLICATE_TEMPLATE_ASSIGNMENT", class_id)
            result[class_id] = (template["template_id"], template["body"], assignment)
    return result


def reconstruct_certificate(body: dict[str, Any], assignment: dict[str, Any]) -> dict[str, Any]:
    certificate = {field: body[field] for field in BODY_FIELDS}
    certificate.update(assignment["certificate_residual"])
    need(object_sha(certificate) == assignment["frozen_certificate_sha256"], "RECONSTRUCTED_CERTIFICATE_HASH")
    return certificate


def verify_quadratic_templates(table: dict[str, Any], terminal_counts: Counter[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    raw4 = table["raw4"]
    raw4_map = template_assignment_map(raw4["quadratic_literal_templates"])
    registry = read_gzip_json(RAW4_REGISTRY)
    q_classes: set[str] = set()
    expected_family_rows: dict[str, dict[str, Any]] = {}
    class_to_template = {class_id: row[0] for class_id, row in raw4_map.items()}
    for record in registry["rows"]:
        class_id = f"source_{record['source_index']}:class_{record['class_id']:06d}"
        terminal = record["terminal_certificate"]
        expected_family_rows[class_id] = {
            "terminal_class_id": class_id,
            "terminal_kind": terminal["kind"],
            "presentation_count": terminal_counts[class_id],
            "direction": "source_to_target",
            "certificate_binding_sha256": record["certificate_binding_sha256"],
            "literal_template_id": class_to_template.get(class_id),
        }
        if terminal["kind"] != "exact_multihomogeneous_quadratic":
            continue
        q_classes.add(class_id)
        need(class_id in raw4_map, "RAW4_Q_TEMPLATE_MISSING", class_id)
        _, body, assignment = raw4_map[class_id]
        need(reconstruct_certificate(body, assignment) == terminal["certificate"], "RAW4_Q_NOT_REVERSIBLE", class_id)
        need(assignment["raw_presentation_count"] == terminal_counts[class_id], "RAW4_Q_PRESENTATIONS")
    need(q_classes == set(raw4_map) and len(q_classes) == 839, "RAW4_Q_COVERAGE")
    observed_family_rows = {row["terminal_class_id"]: row for row in raw4["family_assignments"]}
    need(observed_family_rows == expected_family_rows, "RAW4_TERMINAL_FAMILY_EQUIVALENCE")
    need(len(terminal_counts) == 934 and sum(terminal_counts.values()) == 1472, "RAW4_TERMINAL_PRESENTATIONS")
    counts["raw4_classes"] = len(q_classes)

    theta2_map = template_assignment_map(table["theta2"]["quadratic_literal_templates"])
    direct = read_gzip_json(THETA2_DIRECT)
    expected_theta2: set[str] = set()
    for certificate in direct["quadratic_certificates"].values():
        class_id = f"source_{certificate['source_index']}:class_{certificate['class_id']:06d}"
        expected_theta2.add(class_id)
        need(class_id in theta2_map, "THETA2_Q_TEMPLATE_MISSING", class_id)
        _, body, assignment = theta2_map[class_id]
        need(reconstruct_certificate(body, assignment) == certificate, "THETA2_Q_NOT_REVERSIBLE", class_id)
    need(expected_theta2 == set(theta2_map) and len(expected_theta2) == 96, "THETA2_Q_COVERAGE")
    counts["theta2_classes"] = len(expected_theta2)

    cycle_map = template_assignment_map(table["cycle"]["quadratic_literal_templates"])
    cycle = read_json(safe(CYCLE_QUADRATICS))
    need(set(cycle_map) == set(cycle["certificates"]), "CYCLE_Q_CLASS_SET")
    for class_id, certificate in cycle["certificates"].items():
        _, body, assignment = cycle_map[class_id]
        need(reconstruct_certificate(body, assignment) == certificate, "CYCLE_Q_NOT_REVERSIBLE", class_id)
        need(assignment["raw_presentation_count"] == cycle["raw_multiplicity"][class_id], "CYCLE_Q_PRESENTATIONS")
    counts["cycle_classes"] = len(cycle_map)

    restoration_map = template_assignment_map(table["restoration"]["quadratic_literal_templates"])
    forest = read_json(safe(RESTORATION))
    q_rows = [row for row in forest["first_coverage"] if row["proof"] == "exact_multihomogeneous_quadratic"]
    multiplicities = Counter(row["certificate_sha256"] for row in q_rows)
    need(set(restoration_map) == set(multiplicities), "RESTORATION_Q_CLASS_SET")
    for class_id, presentations in multiplicities.items():
        _, body, assignment = restoration_map[class_id]
        need(reconstruct_certificate(body, assignment) == forest["algebra_certificates"][class_id], "RESTORATION_Q_NOT_REVERSIBLE", class_id)
        need(assignment["raw_presentation_count"] == presentations, "RESTORATION_Q_PRESENTATIONS")
    counts["restoration_classes"] = len(restoration_map)
    return counts


def verify_direct36(table: dict[str, Any]) -> dict[str, int]:
    frozen = read_json(safe(DIRECT36))
    expected = {(row["source_index"], row["canonical_class_id"]): row for row in frozen["coverage"]}
    need(len(expected) == 36 and frozen["remaining_unproved_among_36"] == 0 and frozen["binding_gaps"] == [], "DIRECT36_FROZEN_COVERAGE")
    observed: dict[tuple[int, int], dict[str, Any]] = {}
    for template in table["direct36"]["literal_templates"]:
        need(object_sha(template["body"]) == template["body_sha256"], "DIRECT36_BODY_HASH")
        for assignment in template["covered_records"]:
            row = dict(template["body"])
            row.update(assignment["record_residual"])
            key = (assignment["source_index"], assignment["canonical_class_id"])
            need(key not in observed, "DIRECT36_DUPLICATE", key)
            need(object_sha(row) == assignment["frozen_record_sha256"], "DIRECT36_RECONSTRUCTED_HASH", key)
            observed[key] = row
    need(observed == expected, "DIRECT36_NOT_REVERSIBLE")
    need((1, 24) not in observed and (1, 38) not in observed, "DIRECT36_ZERO_ROW")
    families = Counter(row["family"] for row in observed.values())
    need(families == Counter({"theta0_quintic_port_orbit": 22, "lower_theta_quartic": 12, "theta3_cubic": 2}), "DIRECT36_FAMILIES")
    need(len(table["direct36"]["literal_templates"]) == 27, "DIRECT36_LITERAL_BODIES")
    return {"records": len(observed), "literal_bodies": 27, "proposition_families": 3}


def verify_restoration_direction() -> dict[str, Any]:
    forest = read_json(safe(RESTORATION))
    census = forest["census"]
    need(census["canonical_restoration_parents"] == 997, "RESTORATION_PARENTS")
    need(census["member_roots"] == 2540, "RESTORATION_ROOTS")
    need(census["forest_edges"] == 36824 and census["final_leaves"] == 36792, "RESTORATION_EDGE_LEAF_CENSUS")
    need(census["cycles"] == census["missing_children"] == census["unresolved"] == 0, "RESTORATION_GAPS")
    first = forest["first_coverage"]
    second = forest["second_coverage"]
    need(len(first) == 36568 and len(second) == 256, "RESTORATION_LAYER_COUNTS")
    source_transports = forest["first_source_transport_certificates"]
    target_transports = forest["first_target_transport_certificates"]
    continuation_indices: set[int] = set()
    roots: set[str] = set()
    orientation: Counter[tuple[str, str, int]] = Counter()
    for index, row in enumerate(first):
        roots.add(row["root_id"])
        payload = {key: value for key, value in row.items() if key != "row_sha256"}
        need(object_sha(payload) == row["row_sha256"], "RESTORATION_FIRST_ROW_HASH", index)
        need(row["source_parent_transport_id"] in source_transports, "RESTORATION_SOURCE_TRANSPORT")
        need(row["target_parent_transport_id"] in target_transports, "RESTORATION_TARGET_TRANSPORT")
        if row["status"] == "continuation":
            continuation_indices.add(index)
            need(
                row["proof"] == "restore_remaining_physical_role"
                and len(row["remaining_roles"]) == 1,
                "RESTORATION_CONTINUATION_ROLE",
            )
        else:
            # A separator may terminate before all dummy roles are restored; the
            # remaining-role list is retained as exact provenance, not a gap.
            need(
                row["status"] == "separated"
                and row["proof"] != "restore_remaining_physical_role",
                "RESTORATION_FIRST_TERMINAL",
            )
        if row["proof"] == "full_map_Ti_zero_strict_sign":
            certificate = row["certificate"]
            orientation[(certificate["zero_side"], certificate["signed_side"], certificate["orientation"])] += 1
            need(certificate["strict_sign"] == "negative", "RESTORATION_TI_SIGN")
            need(certificate[f"{certificate['zero_side']}_pullback_sha256"] != certificate["signed_pullback_sha256"], "RESTORATION_TI_SIDE_HASH")
    need(len(roots) == 2540 and len(continuation_indices) == 32, "RESTORATION_ROOT_CONTINUATION_COUNT")
    second_per_parent: Counter[int] = Counter()
    for index, row in enumerate(second):
        payload = {key: value for key, value in row.items() if key != "row_sha256"}
        need(object_sha(payload) == row["row_sha256"], "RESTORATION_SECOND_ROW_HASH", index)
        parent = row["parent_first_coverage_index"]
        need(parent in continuation_indices, "RESTORATION_WRONG_SECOND_PARENT")
        need(row["parent_first_row_sha256"] == first[parent]["row_sha256"], "RESTORATION_PARENT_HASH")
        need(row["root_id"] == first[parent]["root_id"], "RESTORATION_PARENT_ROOT")
        need(row["status"] == "separated" and row["remaining_roles"] == [], "RESTORATION_SECOND_TERMINAL")
        second_per_parent[parent] += 1
        if row["proof"] == "full_map_Ti_zero_strict_sign":
            certificate = row["certificate"]
            orientation[(certificate["zero_side"], certificate["signed_side"], certificate["orientation"])] += 1
            need(certificate["strict_sign"] == "negative", "RESTORATION_TI_SIGN")
    need(set(second_per_parent) == continuation_indices, "RESTORATION_MISSING_SECOND_PARENT")
    need(set(second_per_parent.values()) == {8}, "RESTORATION_SECOND_BRANCHING")
    expected = Counter({("target", "source", 1): 248, ("source", "target", 0): 240, ("target", "source", 2): 70, ("source", "target", 2): 56})
    need(orientation == expected, "RESTORATION_TI_ORIENTATION")
    return {
        "canonical_parents": 997,
        "member_roots": len(roots),
        "edges": len(first) + len(second),
        "leaves": census["final_leaves"],
        "continuation_parents": len(continuation_indices),
        "Ti_orientation_counts": [
            {"zero_side": key[0], "signed_side": key[1], "orientation": key[2], "rows": count}
            for key, count in sorted(orientation.items())
        ],
    }


def verify_input_bindings(value: dict[str, Any], code: str) -> None:
    for binding in value["input_bindings"]:
        if binding.get("binding_kind") == "CORES literal semantic fingerprint":
            need(binding["path"] == ATLAS_REL, f"{code}_GRAMMAR_PATH")
            need(
                binding["sha256"]
                == object_sha({"CORES": parse_cores()})
                == EXPECTED_PRIMITIVE_GRAMMAR_SHA256,
                f"{code}_GRAMMAR_HASH",
            )
            continue
        path = safe(binding["path"])
        need(path.stat().st_size == binding["bytes"], f"{code}_INPUT_BYTES", binding["path"])
        need(file_sha(path) == binding["sha256"], f"{code}_INPUT_HASH", binding["path"])


def build_certificate() -> dict[str, Any]:
    locked = verify_release_and_transitive_hashes()
    baseline = read_json(BASELINE)
    table = read_json(TABLE)
    verify_seal(baseline, "BASELINE")
    verify_seal(table, "TABLE")
    need(baseline["status"] == table["status"] == "PASS", "DERIVATION_STATUS")
    need(baseline["frozen_release"]["release_lock_sha256"] == LOCK_SHA, "BASELINE_LOCK_ANCHOR")
    need(baseline["frozen_release"]["release_lock_payload_sha256"] == LOCK_PAYLOAD, "BASELINE_LOCK_PAYLOAD")
    verify_input_bindings(baseline, "BASELINE")
    verify_input_bindings(table, "TABLE")
    for path, payload in ((BASELINE_MD, baseline["payload_sha256"]), (UNIVERSE_MD, baseline["payload_sha256"]), (TABLE_MD, table["payload_sha256"])):
        need(path.is_file() and payload in path.read_text(encoding="utf-8"), "MARKDOWN_PAYLOAD_BINDING", path)

    formula = verify_formula(baseline)
    raw4_categories, terminal_counts = verify_composite_cartesian(
        RAW4_LEDGER,
        schema="k2p-raw4-corrected-composite-row-v1",
        sources=6,
        targets=2814,
        ports=4,
        expected_categories={"displayed_quartet_exclusion": 360408, "full_map_Ti_strict_sign": 16974, "exact_rank_exclusion": 23822, "direct_terminal_presentation": 1472, "restoration_member_presentation": 2540},
        ti_direction="source_sign_target_zero",
    )
    theta2_categories, _ = verify_composite_cartesian(
        THETA2_LEDGER,
        schema="k2p-theta2-corrected-composite-row-v1",
        sources=4,
        targets=6138,
        ports=5,
        expected_categories={"displayed_quartet_exclusion": 2942592, "full_map_Ti_strict_sign": 2528, "exact_rank_exclusion": 800, "direct_quadratic_separator": 240, "labelled_isomorphism": 80},
        ti_direction="source_zero_target_sign",
    )
    cycle = verify_cycle()
    quadratics = verify_quadratic_templates(table, terminal_counts)
    direct36 = verify_direct36(table)
    restoration = verify_restoration_direction()

    payload = {
        "schema": "k2p-pc-partial-family-coverage-equivalence-v1",
        "status": "PASS",
        "scope": (
            "First PC-PARTIAL checkpoint: immutable baseline, primitive Cartesian "
            "universes, reversible direct quadratic/high-degree templates, and "
            "direction-sensitive restoration/Ti coverage. No triangle or uncertified "
            "symmetry quotient is used."
        ),
        "immutable_release": {
            "release_lock_sha256": LOCK_SHA,
            "release_lock_payload_sha256": LOCK_PAYLOAD,
            "transitive_evidence_files_verified": len(locked),
        },
        "derived_payloads": {
            "baseline": baseline["payload_sha256"],
            "direct_template_table": table["payload_sha256"],
        },
        "finite_formula_cases": formula,
        "raw4_categories": dict(sorted(raw4_categories.items())),
        "theta2_categories": dict(sorted(theta2_categories.items())),
        "cycle": cycle,
        "reversible_quadratic_classes": quadratics,
        "direct36": direct36,
        "restoration": restoration,
        "coverage_boundary": {
            "completion_records_not_unlabelled_graphs": True,
            "source_target_reversal_used": False,
            "ordinary_triangle_quotient_used": False,
            "uncertified_symmetry_used": False,
            "restoration_transport_reconstruction": (
                "The first checkpoint verifies exact row self-hashes, parent links, "
                "transport-registry membership, and mixed Ti direction. Exact labelled "
                "mixed-graph restriction replay remains frozen, hash-bound v3 evidence "
                "and is not claimed as newly compressed here."
            ),
        },
        "completion_percentage": {
            "requested_checkpoint": 100,
            "full_PC_PARTIAL_submission_program_best_guess": 42,
        },
    }
    result = dict(payload)
    result["payload_sha256"] = object_sha(payload)
    return result


def main() -> None:
    need(__debug__, "OPTIMIZED_PYTHON_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(not (args.write and args.check), "MODE_CONFLICT")
    value = build_certificate()
    if args.write:
        OUTPUT.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    else:
        need(OUTPUT.is_file(), "EQUIVALENCE_CERTIFICATE_MISSING")
        need(read_json(OUTPUT) == value, "EQUIVALENCE_CERTIFICATE_DRIFT")
    print(json.dumps({"status": "PASS", "payload_sha256": value["payload_sha256"], "mode": "write" if args.write else "check"}, sort_keys=True))


if __name__ == "__main__":
    main()
