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
        "e21d3269904cdf3b4c1a3d18cdd2c8fa6ef2e88fcea1dc29669fee96beaa7dc1",
        "4fa0db41fade5fe0e746a5ac38fade342ef9df7cfa57bbf05c73473427629677",
    ),
    "analysis/FAMILY_COVERAGE_EQUIVALENCE_CERTIFICATE.json": (
        "k2p-pc-partial-family-coverage-equivalence-v1",
        "977e7adf8e930d3335aaa590b69f8d371f71a3b4381e9f4c25170f8b570fee57",
        "ce29b509fc71bc487f083fbeeadacd89df5a4f8403b7e50f177e611eeac7b1cd",
    ),
    "templates/DIRECT_CERTIFICATE_TEMPLATE_TABLE.json": (
        "k2p-direct-certificate-template-table-v1",
        "c5ce4176e0020cfc01b8d8351f02c87df6e87663b37d372669216ad5bd08be47",
        "b6c63c7818c54ac0bae1e4d3f64047cbcaa531f83ad0b16e6a4ec92f134f7698",
    ),
    "restoration/RESTORATION_ARCHETYPES.json": (
        "k2p-restoration-descriptive-archetypes-v1",
        "f0215c897773be25ae756e61f8ed2942705ce8f400163f80c32f204b60cea454",
        "03b30ed654228833b159e533eb419ca2efc2f64b01a58a88027b212aca5152b7",
    ),
    "restoration/RESTORATION_ARCHETYPE_VERIFICATION.json": (
        "k2p-restoration-archetype-verification-v1",
        "8f3134bd2cb2f01f6a91cfe90fe536cce5f209d4edaaa2e6d25b0c2c64de776c",
        "a9e44df19cc0ec3207d4de95b64c59fa975d752f48e73da337c6ed37fb3c8074",
    ),
    "probe/PROBE_WORD_COVERAGE.json": (
        "k2p-probe-word-theorem-coverage-v1",
        "d66b28240092a04112fde67d54527e3df3964d7eea64f7b75ed75f877435ec49",
        "c2e32b37d32eda11470afc7f747cb2bca5fa58c78fd92793f8fa94309f3d3660",
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
