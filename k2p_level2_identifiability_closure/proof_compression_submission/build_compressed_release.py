#!/usr/bin/env python3
"""Build the deterministic top-level PC-PARTIAL result and crosswalk.

This is a read-only consumer of the frozen theorem evidence.  It writes only
inside ``proof_compression_submission`` and refuses optimized Python.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent
RESULT = ROOT / "PROOF_COMPRESSION_RESULT.json"
CROSSWALK = ROOT / "THEOREM_TO_TEMPLATE_CROSSWALK.json"

EXPECTED_INPUTS = {
    "analysis/PROOF_COMPRESSION_BASELINE.json": (
        "k2p-proof-compression-baseline-v1",
        "5cf2d3ea03d6379608eda6fe71213c2fd17bb8aafdf0c558d9c5e4f508c97246",
        "cdb5936ad94305409460235db7067a9a295cde049419eaaf6e425c2b78c388de",
    ),
    "analysis/FAMILY_COVERAGE_EQUIVALENCE_CERTIFICATE.json": (
        "k2p-pc-partial-family-coverage-equivalence-v1",
        "d9772068ad9047e5878a864e616cca3bd8583afeca705a77ba63020c0a217465",
        "5bda1d38eaa3e732b31eebaca14866fce05d2c2012beeb74e6da0bfe6f1b8105",
    ),
    "templates/DIRECT_CERTIFICATE_TEMPLATE_TABLE.json": (
        "k2p-direct-certificate-template-table-v1",
        "202c53806954e0fcd5e49cb3ff2c678fed0dcd64a5904e88abca07b6332f3fd9",
        "26da1771d10798323cf50f8d861f5d45fc44028d81df18660e16c0335f0cb02d",
    ),
    "restoration/RESTORATION_ARCHETYPES.json": (
        "k2p-restoration-descriptive-archetypes-v1",
        "7afeb89d3d349204cf969d6d27cc9dbfe9bff34084e5c9c3e20ba6e85000a343",
        "127f3920c1a882e07c7d424eeb43d696067ffe0c068a820a34ee5394b49d0ba4",
    ),
    "restoration/RESTORATION_ARCHETYPE_VERIFICATION.json": (
        "k2p-restoration-archetype-verification-v1",
        "8a95857a9961c36c673b4eb5daafbf66dcf6fea198a7672aade6276a7b7bd2cc",
        "2c18ea9271fe260a404d7d239c81d7f5f79af8363cc324135325b33ab61a6c1e",
    ),
    "probe/PROBE_WORD_COVERAGE.json": (
        "k2p-probe-word-theorem-coverage-v1",
        "10fbb422c113bec30e7370ca2f2000531b09344a257c3531601c9cb802a8453c",
        "4a38372635ba617268cfc921baf3a7b397c9beb639dde31bf26b3d2dc7673414",
    ),
}

PROSE_INPUTS = (
    "analysis/PROOF_COMPRESSION_BASELINE.md",
    "analysis/FINITE_UNIVERSE_COMPLETENESS.md",
    "templates/DIRECT_CERTIFICATE_TEMPLATE_TABLE.md",
    "restoration/RESTORATION_ARCHETYPES.md",
    "probe/PROBE_WORD_THEOREM.md",
    "COMPRESSED_BOUNDED_THEOREM.md",
    "THEOREM_TO_TEMPLATE_CROSSWALK.md",
)


class BuildFailure(RuntimeError):
    pass


def need(condition: bool, code: str, detail: Any | None = None) -> None:
    if not condition:
        raise BuildFailure(code if detail is None else f"{code}:{detail}")


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


def sealed(payload: dict[str, Any]) -> dict[str, Any]:
    need("payload_sha256" not in payload, "PAYLOAD_ALREADY_SEALED")
    return {**payload, "payload_sha256": object_sha(payload)}


def load(relative: str) -> dict[str, Any]:
    path = ROOT / relative
    need(path.is_file() and not path.is_symlink(), "INPUT_MISSING_OR_SYMLINK", relative)
    value = json.loads(path.read_text(encoding="utf-8"))
    need(isinstance(value, dict), "INPUT_NOT_OBJECT", relative)
    observed = value.get("payload_sha256")
    payload = dict(value)
    payload.pop("payload_sha256", None)
    need(observed == object_sha(payload), "INPUT_SEAL", relative)
    schema, payload_sha, artifact_sha = EXPECTED_INPUTS[relative]
    need(value.get("schema") == schema, "INPUT_SCHEMA", relative)
    need(observed == payload_sha, "INPUT_PAYLOAD", relative)
    need(file_sha(path) == artifact_sha, "INPUT_FILE_SHA", relative)
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def build_crosswalk() -> dict[str, Any]:
    rows = [
        {
            "theorem_id": "CBT-1",
            "claim": "The corrected primitive completion grammar generates the complete directed raw four-port, five-port theta2, and three-port cycle universes exactly once as records.",
            "templates": ["primitive-core completion-count lemma", "ordered completion keys"],
            "exact_coverage": {"raw4": 405216, "theta2": 2946240, "cycle_base": 13440},
            "evidence": ["analysis/PROOF_COMPRESSION_BASELINE.json", "analysis/FAMILY_COVERAGE_EQUIVALENCE_CERTIFICATE.json"],
            "residue": "The frozen primitive-core theorem and directed record encodings remain load-bearing.",
            "status": "exact compressed theorem",
        },
        {
            "theorem_id": "CBT-2",
            "claim": "Every one of the 934 canonical four-port terminal classes is assigned to an exact terminal family.",
            "templates": ["R4Q-01--R4Q-08", "D36-01--D36-03", "F2/F3/F4 coupled family", "labelled mixed-graph isomorphism", "ordinary-triangle common germ"],
            "exact_coverage": {"terminal_classes": 934, "terminal_presentations": 1472, "quadratic_classes": 839, "direct36_records": 36, "hard_records": 4, "isomorphism_classes": 20, "triangle_classes": 35},
            "evidence": ["templates/DIRECT_CERTIFICATE_TEMPLATE_TABLE.json", "analysis/FAMILY_COVERAGE_EQUIVALENCE_CERTIFICATE.json"],
            "residue": "Twenty-seven direction-specific direct-36 polynomial bodies and all exact graph certificates remain explicit.",
            "status": "exact family compression with explicit transported bodies",
        },
        {
            "theorem_id": "CBT-3",
            "claim": "Every five-port theta2 and three-port cycle direct algebraic terminal is covered by its exact quadratic template family with direction retained.",
            "templates": ["T2Q-01--T2Q-04", "C3Q-01--C3Q-06", "whole-map T_i relation classes", "rank mechanisms"],
            "exact_coverage": {"theta2_quadratic_classes": 96, "cycle_quadratic_classes": 54, "rank_exception_representatives": 75},
            "evidence": ["templates/DIRECT_CERTIFICATE_TEMPLATE_TABLE.json", "analysis/PROOF_COMPRESSION_BASELINE.json"],
            "residue": "All 75 exceptional rank representatives and direction-sensitive whole-map T_i rows remain explicit.",
            "status": "exact family compression with explicit exceptional ledger",
        },
        {
            "theorem_id": "CBT-4",
            "claim": "The 997 restoration obligations form a terminating depth-two exact parent-child forest with no missing, duplicate, cyclic, or unresolved records.",
            "templates": ["displayed-quartet mismatch", "whole-map T_i zero/strict sign", "RSQ-01--RSQ-05", "transported F_(2,112) quartic", "restore remaining role"],
            "exact_coverage": {"canonical_parents": 997, "member_roots": 2540, "first_children": 36568, "second_children": 256, "forest_edges": 36824, "leaves": 36792, "unresolved": 0},
            "evidence": ["restoration/RESTORATION_ARCHETYPES.json", "restoration/RESTORATION_ARCHETYPE_VERIFICATION.json"],
            "residue": "The 297 archetypes are descriptive, not transport quotients; all 997 assignments, 2,540 roots, 36,824 edges, and 16 algebra transport classes remain load-bearing.",
            "status": "PC-PARTIAL descriptive compression; exact forest retained",
        },
        {
            "theorem_id": "CBT-5",
            "claim": "The one-/two-port premises imply coherent transport of arbitrary attachment words on every primitive support.",
            "templates": ["one-port segment lemma", "two-port order lemma", "arbitrary-word induction", "ordinary-triangle arrowhead transport"],
            "exact_coverage": {"anchors": 176, "one_port_rows": 29964, "two_port_rows": 544571, "exact_transports": 67741, "parent_restrictions": 4379, "unresolved": 0},
            "evidence": ["probe/PROBE_WORD_COVERAGE.json", "probe/PROBE_WORD_THEOREM.md"],
            "residue": "The uniform induction does not replace the finite separation and transport ledgers.",
            "status": "word theorem proved; finite premises PC-PARTIAL",
        },
        {
            "theorem_id": "CBT-6",
            "claim": "The bounded classification has zero unresolved mathematical records and leaves the frozen principal-domain K2P-SAME theorem unchanged.",
            "templates": ["CBT-1--CBT-5", "frozen release lock"],
            "exact_coverage": {"unresolved_mathematical_records": 0, "frozen_outcome": "K2P-SAME"},
            "evidence": ["analysis/PROOF_COMPRESSION_BASELINE.json", "analysis/FAMILY_COVERAGE_EQUIVALENCE_CERTIFICATE.json", "restoration/RESTORATION_ARCHETYPE_VERIFICATION.json", "probe/PROBE_WORD_COVERAGE.json"],
            "residue": "This package compresses the proof presentation only and does not supersede the frozen release evidence.",
            "status": "logical consequence of exact ledgers; compression verdict PC-PARTIAL",
        },
    ]
    return sealed(
        {
            "schema": "k2p-pc-partial-theorem-template-crosswalk-v1",
            "status": "PASS",
            "scope": "Bounded principal-D_plus proof-compression layer; direction and labelled transports are retained.",
            "rows": rows,
            "forbidden_inferences": [
                "source-target reversal",
                "ordinary triangle as polynomial symmetry",
                "rooted restriction oracle",
                "uncertified graph symmetry",
                "297 restoration fingerprints as exact transport quotients",
            ],
        }
    )


def artifact_binding(relative: str, payload: str | None = None) -> dict[str, Any]:
    path = ROOT / relative
    need(path.is_file() and not path.is_symlink(), "ARTIFACT_MISSING_OR_SYMLINK", relative)
    result: dict[str, Any] = {
        "path": relative,
        "sha256": file_sha(path),
        "bytes": path.stat().st_size,
    }
    if payload is not None:
        result["payload_sha256"] = payload
    return result


def build_result(inputs: dict[str, dict[str, Any]], crosswalk: dict[str, Any]) -> dict[str, Any]:
    baseline = inputs["analysis/PROOF_COMPRESSION_BASELINE.json"]
    coverage = inputs["analysis/FAMILY_COVERAGE_EQUIVALENCE_CERTIFICATE.json"]
    templates = inputs["templates/DIRECT_CERTIFICATE_TEMPLATE_TABLE.json"]
    restoration = inputs["restoration/RESTORATION_ARCHETYPES.json"]
    probe = inputs["probe/PROBE_WORD_COVERAGE.json"]
    machine_bindings = [
        artifact_binding(relative, value["payload_sha256"])
        for relative, value in sorted(inputs.items())
    ]
    machine_bindings.append(
        artifact_binding("THEOREM_TO_TEMPLATE_CROSSWALK.json", crosswalk["payload_sha256"])
    )
    prose_bindings = [artifact_binding(relative) for relative in PROSE_INPUTS]
    payload = {
        "schema": "k2p-principal-d-plus-proof-compression-result-v1",
        "status": "PC-PARTIAL",
        "frozen_theorem": {
            "outcome": "K2P-SAME",
            "promotion_ready": True,
            "release_lock_sha256": baseline["frozen_release"]["release_lock_sha256"],
            "release_lock_payload_sha256": baseline["frozen_release"]["release_lock_payload_sha256"],
            "transitively_locked_evidence_files": baseline["frozen_release"]["transitively_locked_evidence_files"],
            "modified_or_superseded": False,
        },
        "bounded_census": {
            "raw4_directions": baseline["finite_universes"]["raw4"]["rows"],
            "theta2_directions": baseline["finite_universes"]["theta2"]["rows"],
            "cycle_base_directions": baseline["finite_universes"]["cycle"]["base_rows"],
            "terminal_classes": templates["raw4"]["canonical_terminal_classes"],
            "restoration_parents": restoration["census"]["canonical_parents"],
            "restoration_edges": restoration["census"]["forest_edges"],
            "probe_two_port_rows": probe["two_port"]["raw_pairs"],
            "unresolved_mathematical_records": 0,
        },
        "proved_compressions": {
            "primitive_completion_formula": "exact",
            "direct_certificate_families": "exact with transported bodies and exceptions retained",
            "restoration_mechanism_table": "exact mechanism census",
            "restoration_archetypes": 297,
            "probe_word_induction": "proved from exact finite premises",
        },
        "irreducible_exact_ledgers": {
            "rank_exception_representatives": 75,
            "direct36_direction_specific_bodies": 27,
            "restoration": {
                "canonical_parent_assignments": 997,
                "member_root_presentations": 2540,
                "parent_child_edges": 36824,
                "algebra_transport_certificate_classes": 16,
            },
            "probe": {
                "anchors": 176,
                "one_port_rows": 29964,
                "two_port_rows": 544571,
                "exact_transports": 67741,
                "parent_restrictions": 4379,
            },
            "whole_map_Ti": {
                "raw4_rows": templates["structural_templates"]["full_map_Ti"]["raw4"]["rows"],
                "theta2_rows": templates["structural_templates"]["full_map_Ti"]["theta2"]["rows"],
                "cycle_rows": templates["structural_templates"]["full_map_Ti"]["cycle"]["rows"],
                "restoration_rows": templates["structural_templates"]["full_map_Ti"]["restoration"]["rows"],
            },
        },
        "compression_gaps": [
            "No exact cross-parent transport quotient reducing the 997 restoration assignments was proved.",
            "No smaller exact theorem replaced the finite probe separation and transport premises.",
            "The 75 exceptional rank representatives and all direction-sensitive T_i rows remain finite evidence.",
        ],
        "logical_boundaries": {
            "unresolved_mathematical_records": 0,
            "unresolved_compression_obligations": 3,
            "ordinary_triangle_is_graph_common_germ_not_polynomial_symmetry": True,
            "source_target_reversal_used": False,
            "uncertified_symmetry_used": False,
            "restoration_297_is_exact_transport_quotient": False,
        },
        "equivalence_payload_sha256": coverage["payload_sha256"],
        "artifact_bindings": {
            "machine_readable": machine_bindings,
            "prose": prose_bindings,
        },
    }
    return sealed(payload)


def main() -> int:
    need(__debug__ and sys.flags.optimize == 0, "OPTIMIZED_PYTHON_FORBIDDEN")
    inputs = {relative: load(relative) for relative in EXPECTED_INPUTS}
    crosswalk = build_crosswalk()
    write_json(CROSSWALK, crosswalk)
    result = build_result(inputs, crosswalk)
    write_json(RESULT, result)
    print(
        json.dumps(
            {
                "crosswalk_payload_sha256": crosswalk["payload_sha256"],
                "result_payload_sha256": result["payload_sha256"],
                "status": result["status"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BuildFailure as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}, sort_keys=True))
        raise SystemExit(1)
