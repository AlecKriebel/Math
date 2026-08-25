#!/usr/bin/env python3
"""Shared fail-closed logic for the principal-D+ theorem release."""

from __future__ import annotations

import ast
import gzip
import hashlib
import importlib
import importlib.metadata
import json
import os
import re
import stat
import sys
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
LOCK_SCHEMA = "k2p-principal-d-plus-final-theorem-release-lock-v1"
EXPECTED_OUTCOME = "K2P-SAME"
CORRECTED_LOCATOR_SCHEMA = "k2p-corrected-finite-universe-locator-v1"
CORRECTED_RELEASE_SCHEMA = "k2p-corrected-finite-universe-release-v2"
RAW_FOUR_TOTAL = 405_216
REVOKED_RAW_FOUR_ROWS = 16_974
THETA2_TOTAL = 2_946_240
RAW4_COMPOSITE_CATEGORY_COUNTS = {
    "displayed_quartet_exclusion": 360_408,
    "full_map_Ti_strict_sign": 16_974,
    "exact_rank_exclusion": 23_822,
    "direct_terminal_presentation": 1_472,
    "restoration_member_presentation": 2_540,
}
RAW4_TERMINAL_CLASS_MULTIPLICITIES = {
    "1": 680,
    "2": 150,
    "4": 71,
    "5": 14,
    "6": 7,
    "8": 12,
}
RAW4_RESTORATION_PARENT_MULTIPLICITIES = {
    "1": 424,
    "2": 112,
    "4": 449,
    "8": 12,
}
THETA2_COMPOSITE_CATEGORY_COUNTS = {
    "displayed_quartet_exclusion": 2_942_592,
    "full_map_Ti_strict_sign": 2_528,
    "exact_rank_exclusion": 800,
    "direct_quadratic_separator": 240,
    "labelled_isomorphism": 80,
}
CYCLE_BASE_CATEGORY_COUNTS = {
    "fixed_full_restoration_obligation": 5_964,
    "full_map_Ti_strict_sign": 7_452,
    "labelled_isomorphism": 8,
    "ordinary_triangle_relation": 16,
}
CYCLE_FULL_CATEGORY_COUNTS = {
    "displayed_quartet_strict_separator": 535_920,
    "exact_directional_quadratic": 132,
    "full_map_Ti_strict_sign": 300,
    "labelled_isomorphism": 12,
}
CYCLE_BASE_TOTAL = 13_440
CYCLE_FULL_TOTAL = 536_364
PROBE_INPUT_ANCHORS = 176
PROBE_INPUT_SITES_PER_SIDE = 2_206
PROBE_INPUT_FIRST_PAIRS = 29_964
PROBE_ONE_PORT_COUNTS = {
    "displayed_quartet_mismatch": 27_758,
    "full_map_Ti_strict_sign": 99,
    "isomorphic": 1_915,
    "triangle": 192,
}
PROBE_TWO_PORT_COUNTS = {
    "displayed_quartet_mismatch": 511_266,
    "full_map_Ti_strict_sign": 576,
    "isomorphic": 30_969,
    "triangle": 1_760,
}
PROBE_ONE_PORT_EQUALITIES = 2_107
PROBE_TWO_PORT_PAIRS = 544_571
PROBE_TWO_PORT_EQUALITIES = 32_729
PROBE_TOTAL_PAIRS = PROBE_INPUT_FIRST_PAIRS + PROBE_TWO_PORT_PAIRS
PROBE_TOTAL_EQUALITIES = PROBE_ONE_PORT_EQUALITIES + PROBE_TWO_PORT_EQUALITIES
PROBE_AGGREGATE_COUNTS = {
    key: PROBE_ONE_PORT_COUNTS[key] + PROBE_TWO_PORT_COUNTS[key]
    for key in PROBE_ONE_PORT_COUNTS
}
PROBE_TRANSPORT_RECORDS = 67_741
PROBE_RESTRICTION_RECORDS = 4_379
PROBE_QUARTET_CERTIFICATES = 638
PROBE_TI_RELATION_CERTIFICATES = 156
PROBE_TI_STRICT_POLYNOMIALS = 118
RESTORATION_V3_FIRST_CHILDREN = 36_568
RESTORATION_V3_SECOND_CHILDREN = 256
RESTORATION_V3_FOREST_EDGES = 36_824
RESTORATION_V3_FINAL_LEAVES = 36_792
RESTORATION_V3_FIRST_PROOF_COUNTS = {
    "displayed_quartet_mismatch": 35_758,
    "exact_multihomogeneous_quadratic": 148,
    "full_map_Ti_zero_strict_sign": 606,
    "inherited_exact_F_2_112_quartic": 24,
    "restore_remaining_physical_role": 32,
}
RESTORATION_V3_SECOND_PROOF_COUNTS = {
    "displayed_quartet_mismatch": 248,
    "full_map_Ti_zero_strict_sign": 8,
}
COMPOSITE_SERIALIZATION = {
    "format": "gzip-jsonl-canonical-v1",
    "gzip_mtime": 0,
    "json_key_order": "lexicographic",
    "json_separators": [",", ":"],
    "line_ending": "LF",
    "final_newline": True,
    "row_order": "raw_id_ascending",
}
PROMOTION_MANUSCRIPT_FILES = {
    "work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md": "bff0a4e6ddfa123aff0f560795d3f90dc6d60a6da768690f1f8e39db0fddcc9f",
    "work/global_theorem_closure/promotion_manuscript/QUANTIFIER_AUDIT.md": "425a041bc3e4cc7bd4f74c952455623ff26f430d9c4ceb006edcac9e8c3765d8",
    "work/global_theorem_closure/promotion_manuscript/PROBE_PROMOTION_PLACEHOLDER.json": "79a9949f5a5598a83c7e2bfc60d669dfe4b8b7d3417d8d8673e2fc4c634efaaa",
    "work/global_theorem_closure/promotion_manuscript/verify_promotion_gate.py": "464bf0823283e93175e350fefcb5fce3fd2bce2cd137dfe833b4722e24943ccd",
}
PROMOTION_GUARD_CENSUS = {
    "frozen_inputs_verified": 23,
    "probe_artifacts_verified": 3,
    "probe_ledgers_verified": 6,
    "required_pass_gates": 10,
    "required_zero_gates": 8,
    "status": "PASS",
}
PROMOTION_GUARD_STDOUT_SHA256 = (
    "8ee70df32de5e6f6282e3e1902c8e5b339a92058e6f571862d2ba6ee2d5afd7c"
)
RUNTIME_EVIDENCE_SHA256 = {
    "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py":
        "37e9b7910f7723c146a87ae2f60dfb62529b1a3e4866ccd72d65dc4efda923ad",
    "package/referee/k2p_offline_sweep_portable/verify_package.py":
        "bc2dc5714b0928beda31e96eb15954715133ee4a8ab7ba106b7c5a1b62ba83cc",
}
REVOKED_RESTORATION_RUNTIME_SHA256 = {
    "work/restoration_forest/five_port_certificate.json":
        "dc3a3f68c1d8c347ac196de1cd802fd6cd4895a5e007c87c79431a89bd191fb9",
    "work/restoration_forest/replay_report.json":
        "6e0f82449cea5b783e5c0df6a589f2be46f611d7679d547effde1c43f466487b",
    "work/restoration_forest/RESTORATION_CLOSURE.md":
        "efd9d1d78d54289e511ce07113a1abbdf77dd8589734c0800ee0ff401b5f7a25",
}
REVOKED_RESTORATION_RUNTIME_ARTIFACTS = {
    "work/restoration_forest/RESTORATION_CLOSURE.md": {
        "classification": "REVOKED_LEGACY_RESTORATION_NARRATIVE",
        "authoritative_replacements": [
            "work/restoration_sign_reclassification/corrected_restoration_forest.json",
            "work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md",
        ],
    },
    "work/restoration_forest/five_port_certificate.json": {
        "classification": "REVOKED_LEGACY_RESTORATION_RUNTIME_INPUT",
        "authoritative_replacements": [
            "work/restoration_sign_reclassification/corrected_restoration_forest.json",
        ],
    },
    "work/restoration_forest/replay_report.json": {
        "classification": "REVOKED_LEGACY_RESTORATION_REPLAY",
        "authoritative_replacements": [
            "work/restoration_sign_reclassification/corrected_restoration_replay_certificate.json",
            "work/restoration_sign_reclassification/corrected_restoration_forest.json",
        ],
    },
}
HISTORICAL_ARTIFACT_REGISTRY = (
    "work/final_theorem_release/HISTORICAL_ARTIFACT_REGISTRY.json"
)
HISTORICAL_PROOF_ARTIFACTS = {
    "work/adversarial_proof_review/PROBE_AUDIT.md": {
        "sha256": "8c8c19f1c17e85e709994f4ec2582046c49ea1b496691699677f7a0becbd5d25",
        "classification": "REVOKED_INTERMEDIATE_PROBE_AUDIT",
        "authoritative_replacements": [
            "work/probe_coherence_corrected/probe_coherence_certificate.json",
            "work/global_proof_adversary/probe_full_audit/independent_probe_graph_audit_certificate.json",
            "work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md",
        ],
    },
    "work/adversarial_proof_review/TOPOLOGY_DIRECTIONAL_THEOREM.md": {
        "sha256": "abe1a9e089d7324d9509ebbe32f6b7217045ccb7c0d3044afc7db1d02604e7d7",
        "classification": "REVOKED_ROOTED_TOPOLOGY_ORACLE_NARRATIVE",
        "authoritative_replacements": [
            "work/final_theorem_release/corrected_universe_certificate.json",
            "work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md",
        ],
    },
    "work/theorem_assembly/THEOREM_STATEMENTS_DRAFT.md": {
        "sha256": "706090fb6370a0310bcd39f58544eabf75f6bdadf2a4dc707f24cb19bbc95814",
        "classification": "SUPERSEDED_CANDIDATE_THEOREM_DRAFT",
        "authoritative_replacements": [
            "work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md",
            "work/global_theorem_closure/promotion_manuscript/QUANTIFIER_AUDIT.md",
        ],
    },
    "work/audit_unified_closure/AUDIT_REPORT.md": {
        "sha256": "0386e8dbc35228f110efcd467186dd04f8a10d0279848ff19f6ebd90887d8bc8",
        "classification": "HISTORICAL_REPAIRED_GAP_DIRECT36_AUDIT",
        "authoritative_replacements": [
            "package/referee/k2p_offline_sweep_portable/proofs/four_port_direct_residual_closure_certificate.json",
            "work/final_theorem_release/corrected_universe_certificate.json",
            "work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md",
        ],
    },
    "work/global_proof_adversary/probe_full_audit/AUDIT_REPORT.md": {
        "sha256": "9ec50c3573ef0be2b421730cf95258c8927dde165cdd4138a3a596fcfb08f69a",
        "classification": "HISTORICAL_REPAIRED_GAP_PROBE_REPORT",
        "authoritative_replacements": [
            "work/global_proof_adversary/probe_full_audit/independent_probe_graph_audit_certificate.json",
            "work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md",
        ],
    },
}


class ReleaseFailure(RuntimeError):
    """A release qualification condition failed."""


def require(condition: bool, code: str, detail: object | None = None) -> None:
    if not condition:
        if detail is None:
            raise ReleaseFailure(code)
        raise ReleaseFailure(f"{code}:{detail}")


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha_object(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_runtime_environment() -> dict[str, str]:
    """Fail before qualification if the pinned referee runtime is absent."""

    require(sys.version_info >= (3, 10), "PYTHON_VERSION_TOO_OLD")
    expected = {"networkx": "3.5", "sympy": "1.14.0"}
    observed: dict[str, str] = {}
    for distribution, wanted in expected.items():
        try:
            importlib.import_module(distribution)
            actual = importlib.metadata.version(distribution)
        except (ImportError, importlib.metadata.PackageNotFoundError) as error:
            raise ReleaseFailure(
                f"RUNTIME_DEPENDENCY_MISSING:{distribution}:{error}"
            ) from error
        require(
            actual == wanted,
            "RUNTIME_DEPENDENCY_VERSION_FAIL",
            f"{distribution}:{actual}!={wanted}",
        )
        observed[distribution] = actual
    return {
        "python": ".".join(str(item) for item in sys.version_info[:3]),
        **observed,
    }


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "DUPLICATE_JSON_KEY", key)
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            result = json.load(handle, object_pairs_hook=unique_object)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ReleaseFailure(f"JSON_READ_FAIL:{path}:{error}") from error
    require(isinstance(result, dict), "JSON_TOP_LEVEL_NOT_OBJECT", path)
    return result


def safe_relative(relative: str) -> PurePosixPath:
    pure = PurePosixPath(relative)
    require(bool(relative), "EMPTY_RELATIVE_PATH")
    require(not pure.is_absolute(), "ABSOLUTE_PATH_FORBIDDEN", relative)
    require(".." not in pure.parts and "." not in pure.parts, "UNSAFE_PATH", relative)
    require("\\" not in relative and pure.as_posix() == relative, "NON_POSIX_PATH", relative)
    return pure


def project_file(relative: str, project: Path = PROJECT) -> Path:
    pure = safe_relative(relative)
    path = project.joinpath(*pure.parts)
    try:
        metadata = path.lstat()
        path.resolve().relative_to(project.resolve())
    except (OSError, ValueError) as error:
        raise ReleaseFailure(f"PROJECT_FILE_FAIL:{relative}:{error}") from error
    require(stat.S_ISREG(metadata.st_mode), "PROJECT_FILE_NOT_REGULAR", relative)
    return path


def verify_payload_hash(
    value: dict[str, Any], field: str = "payload_sha256"
) -> str:
    expected = value.get(field)
    require(
        isinstance(expected, str)
        and len(expected) == 64
        and all(character in "0123456789abcdef" for character in expected),
        "PAYLOAD_HASH_FORMAT_FAIL",
        field,
    )
    body = {key: item for key, item in value.items() if key != field}
    require(sha_object(body) == expected, "PAYLOAD_HASH_MISMATCH", field)
    return expected


def parse_sha256_manifest(path: Path, base: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for ordinal, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        require(match is not None, "MANIFEST_LINE_FAIL", f"{path}:{ordinal}")
        digest, relative = match.groups()
        if relative.startswith("./"):
            relative = relative[2:]
        pure = safe_relative(relative)
        require(relative not in result, "MANIFEST_DUPLICATE_PATH", relative)
        target = base.joinpath(*pure.parts)
        require(target.is_file(), "MANIFEST_FILE_MISSING", target)
        require(sha_file(target) == digest, "MANIFEST_FILE_HASH_MISMATCH", target)
        result[relative] = digest
    require(bool(result), "EMPTY_MANIFEST", path)
    return result


def fixed_evidence_files() -> dict[str, str]:
    """Files directly committed by the outer lock.

    Complete subpackages are recursively committed by their nested manifests;
    the outer lock includes those manifests and all cross-layer summaries.
    """

    return {
        # Submission-wide licensing and release boundary.
        "LICENSES.md": "submission_metadata",
        # Harness and independent three-port replacement.
        "work/final_theorem_release/no_assert_triangle_sunlet.py": "harness",
        "work/final_theorem_release/triangle_sunlet_certificate.json": "three_port",
        "work/final_theorem_release/release_common.py": "harness",
        "work/final_theorem_release/build_release_lock.py": "harness",
        "work/final_theorem_release/verify_final_theorem_release.py": "harness",
        "work/final_theorem_release/run_release_mutations.py": "harness",
        "work/final_theorem_release/verify_full_map_reseal.py": "corrected_finite_universe:full_map_reseal",
        "work/final_theorem_release/full_map_reseal_audit.json": "corrected_finite_universe:full_map_reseal",
        "work/final_theorem_release/verify_composite_reseal_diff.py": "corrected_finite_universe:composite_reseal",
        "work/final_theorem_release/composite_reseal_diff_audit.json": "corrected_finite_universe:composite_reseal",
        "work/final_theorem_release/README.md": "harness",
        "work/final_theorem_release/RESEARCH_LOG.md": "harness",
        "work/final_theorem_release/CORRECTED_FINITE_UNIVERSE_CONTRACT.md": "harness",
        "work/final_theorem_release/requirements.txt": "runtime_environment",
        HISTORICAL_ARTIFACT_REGISTRY: "historical_artifact_registry",
        "work/final_theorem_release/corrected_finite_universe_locator.json": "corrected_finite_universe",
        # Runtime evidence is a separate partition from theorem authority and
        # from narrative provenance.  Its bytes are also checked against the
        # frozen constants in validate_runtime_evidence().
        **{
            relative: "runtime_evidence"
            for relative in RUNTIME_EVIDENCE_SHA256
        },
        **{
            relative: "historical_revoked_runtime_provenance"
            for relative in REVOKED_RESTORATION_RUNTIME_SHA256
        },
        # Proof-like narrative retained solely for provenance.  The registry
        # gives each file an explicit status and authoritative replacement.
        **{
            relative: "historical_proof_provenance"
            for relative in HISTORICAL_PROOF_ARTIFACTS
        },
        # Domain/rooting and three-port frozen source.
        "work/domain_rooting_closure/verify_domain_rooting.py": "domain_rooting",
        "work/domain_rooting_closure/domain_rooting_certificate.json": "domain_rooting",
        "work/domain_rooting_closure/PROOF.md": "domain_rooting",
        "package/original/checkpoint_2/continuation_2/verify_triangle_and_sunlet.py": "three_port",
        "package/original/checkpoint_2/continuation_2/K2P_TRIANGLE_GERM_EXACT.md": "three_port",
        "package/original/checkpoint_2/continuation_2/K2P_TREE_SUNLET_SIGN_CERTIFICATE.md": "three_port",
        # Pointwise decorated tree of blobs.
        "work/quartet_separation_closure/QUARTET_SEMANTICS_SPEC.json": "quartet_tree_of_blobs",
        "work/quartet_separation_closure/verify_quartet_logic.py": "quartet_tree_of_blobs",
        "work/quartet_separation_closure/quartet_logic_certificate.json": "quartet_tree_of_blobs",
        "work/quartet_separation_closure/test_quartet_semantics_mutations.py": "quartet_tree_of_blobs",
        "work/quartet_separation_closure/quartet_semantics_mutation_certificate.json": "quartet_tree_of_blobs",
        "work/quartet_separation_closure/verify_quartet_terminal_bindings.py": "quartet_terminal_bindings",
        "work/quartet_separation_closure/quartet_terminal_binding_certificate.json": "quartet_terminal_bindings",
        "work/quartet_separation_closure/test_quartet_terminal_binding_mutations.py": "quartet_terminal_bindings",
        "work/quartet_separation_closure/quartet_terminal_binding_mutation_certificate.json": "quartet_terminal_bindings",
        "work/quartet_separation_closure/PROOF.md": "quartet_tree_of_blobs",
        "work/adversarial_proof_review/topology_direction_certificate.json": "quartet_tree_of_blobs",
        "work/adversarial_proof_review/verify_topology_direction.py": "quartet_tree_of_blobs",
        # Exhaustive orbit/canonicalizer comparison and graph-derived paired
        # edge/inheritance transports.  These close the strict ordinary-
        # triangle and parent-order semantics used by the finite ledgers.
        "work/canonicalizer_completeness/canonicalizer_audit.py": "canonicalizer_completeness",
        "work/canonicalizer_completeness/verify_canonicalizer_completeness.py": "canonicalizer_completeness",
        "work/canonicalizer_completeness/test_canonicalizer_mutations.py": "canonicalizer_completeness",
        "work/canonicalizer_completeness/canonicalizer_completeness_certificate.json": "canonicalizer_completeness",
        "work/canonicalizer_completeness/canonicalizer_completeness_mutation_certificate.json": "canonicalizer_completeness",
        "work/canonicalizer_completeness/PROOF.md": "canonicalizer_completeness",
        "work/canonicalizer_completeness/README.md": "canonicalizer_completeness",
        "work/canonicalizer_completeness/inheritance_transport/build_parameter_transport_certificate.py": "parameter_transport",
        "work/canonicalizer_completeness/inheritance_transport/verify_parameter_transport_certificate.py": "parameter_transport",
        "work/canonicalizer_completeness/inheritance_transport/run_parameter_transport_mutations.py": "parameter_transport",
        "work/canonicalizer_completeness/inheritance_transport/parameter_transport_certificate.json": "parameter_transport",
        "work/canonicalizer_completeness/inheritance_transport/parameter_transport_mutation_report.json": "parameter_transport",
        "work/canonicalizer_completeness/inheritance_transport/probe_relation_parameter_transports.jsonl.gz": "parameter_transport",
        "work/canonicalizer_completeness/inheritance_transport/probe_restriction_parameter_transports.jsonl.gz": "parameter_transport",
        "work/canonicalizer_completeness/inheritance_transport/restoration_restriction_parameter_transports.jsonl.gz": "parameter_transport",
        "work/canonicalizer_completeness/inheritance_transport/README.md": "parameter_transport",
        "work/canonicalizer_completeness/inheritance_transport/RESEARCH_LOG.md": "parameter_transport",
        # Bridge, marginal, gluing, and analytic adversarial audit.
        "work/bridge_marginal_closure/verify_bridge_marginal.py": "bridge_marginal_gluing",
        "work/bridge_marginal_closure/certificate.json": "bridge_marginal_gluing",
        "work/bridge_marginal_closure/PROOF.md": "bridge_marginal_gluing",
        "work/adversarial_proof_review/verify_adversarial.py": "bridge_marginal_gluing",
        "work/adversarial_proof_review/audit_certificate.json": "bridge_marginal_gluing",
        "work/adversarial_proof_review/test_mutations.py": "bridge_marginal_gluing",
        "work/adversarial_proof_review/mutation_certificate.json": "bridge_marginal_gluing",
        "work/adversarial_proof_review/PHYSICAL_LOCAL_PRODUCT_REPAIR.md": "bridge_marginal_gluing",
        "work/adversarial_proof_review/unconditional_lift_counterexample.json": "bridge_marginal_gluing",
        "work/global_proof_adversary/AUDIT.md": "global_analytic_audit",
        "work/global_proof_adversary/verify_component_scales.py": "global_analytic_audit",
        "work/global_proof_adversary/component_scale_certificate.json": "global_analytic_audit",
        # Complete raw four-port ledger and rank upper package.
        "work/raw_ledger_audit/verify_raw_ledger.py": "four_port_raw_rank",
        "work/raw_ledger_audit/generate_raw_ledger.py": "four_port_raw_rank",
        "work/raw_ledger_audit/ledger_common.py": "four_port_raw_rank",
        "work/raw_ledger_audit/rank_upper_binding.py": "four_port_raw_rank",
        "work/raw_ledger_audit/test_mutations.py": "four_port_raw_rank",
        "work/raw_ledger_audit/artifacts/raw_ledger_summary.json": "four_port_raw_rank",
        "work/raw_ledger_audit/artifacts/raw_directional_ledger.jsonl.gz": "four_port_raw_rank",
        "work/raw_ledger_audit/artifacts/rank_lower_certificates.json.gz": "four_port_raw_rank",
        "work/raw_ledger_audit/artifacts/rank_upper_binding.json.gz": "four_port_raw_rank",
        "work/raw_ledger_audit/artifacts/retained_class_partition.json.gz": "four_port_raw_rank",
        "work/raw_ledger_audit/artifacts/raw_ledger_mutation_report.json": "four_port_raw_rank",
        "work/rank_upper_certificates/MANIFEST.sha256": "four_port_raw_rank",
        "work/rank_upper_certificates/manifest.json": "four_port_raw_rank",
        "work/rank_upper_certificates/rank_upper_coverage.json": "four_port_raw_rank",
        "work/rank_upper_certificates/rank_upper_replay.json": "four_port_raw_rank",
        "work/rank_upper_certificates/mutation_report.json": "four_port_raw_rank",
        # Current direct-36 referee release.
        "package/referee/k2p_offline_sweep_portable/DIRECT_CLOSURE_LOCK.json": "four_port_direct36",
        "package/referee/k2p_offline_sweep_portable/verify_direct_closure_release.py": "four_port_direct36",
        "package/referee/k2p_offline_sweep_portable/test_direct_closure_release_mutations.py": "four_port_direct36",
        "package/referee/k2p_offline_sweep_portable/proofs/four_port_direct_residual_closure_certificate.json": "four_port_direct36",
        # The legacy 997-parent forest is revoked.  Its corrected replacement
        # is discovered through the signed locator rather than assumed here.
        # Historical theta2 raw/restoration inputs.  A corrected composite
        # discovered through the locator is the only promotion partition.
        "work/theta2_five_port_closure/verify_theta2_ledger.py": "theta2_legacy_provenance",
        "work/theta2_five_port_closure/generate_theta2_ledger.py": "theta2_legacy_provenance",
        "work/theta2_five_port_closure/restoration_closure.py": "theta2_legacy_provenance",
        "work/theta2_five_port_closure/theta2_common.py": "theta2_legacy_provenance",
        "work/theta2_five_port_closure/syzygy_upper.py": "theta2_legacy_provenance",
        "work/theta2_five_port_closure/test_mutations.py": "theta2_legacy_provenance",
        "work/theta2_five_port_closure/PROOF.md": "theta2_legacy_provenance",
        "work/theta2_five_port_closure/artifacts/theta2_five_port_summary.json": "theta2_legacy_provenance",
        "work/theta2_five_port_closure/artifacts/raw_directional_ledger.jsonl.gz": "theta2_legacy_provenance",
        "work/theta2_five_port_closure/artifacts/exact_rank_certificates.json.gz": "theta2_legacy_provenance",
        "work/theta2_five_port_closure/artifacts/direct_proof_certificates.json.gz": "theta2_legacy_provenance",
        "work/theta2_five_port_closure/artifacts/class_partition.json.gz": "theta2_legacy_provenance",
        "work/theta2_five_port_closure/artifacts/fixed_full_restoration_closure.json.gz": "theta2_legacy_provenance",
        "work/theta2_five_port_closure/artifacts/mutation_report.json": "theta2_legacy_provenance",
        # Historical cycle inputs; corrected cycle truth is dynamic.
        "work/cycle_three_port_closure/MANIFEST.sha256": "cycle_three_port_legacy_provenance",
        "work/cycle_three_port_closure/artifacts/cycle_three_port_summary.json": "cycle_three_port_legacy_provenance",
        "work/cycle_three_port_closure/verify_cycle_closure.py": "cycle_three_port_legacy_provenance",
        "work/cycle_three_port_closure/test_mutations.py": "cycle_three_port_legacy_provenance",
        "work/cycle_three_port_closure/mutation_certificate.json": "cycle_three_port_legacy_provenance",
        # Corrected probe and cross-family truth packages are path-configurable
        # signed locator artifacts, not fixed historical paths.
        # Weak-class sharpness, primary and independent.
        "work/weak_sharpness_closure/verify_weak_sharpness.py": "weak_sharpness",
        "work/weak_sharpness_closure/weak_sharpness_certificate.json": "weak_sharpness",
        "work/weak_sharpness_closure/PROOF.md": "weak_sharpness",
        "work/weak_sharpness_audit/audit_weak_sharpness.py": "weak_sharpness",
        "work/weak_sharpness_audit/audit_certificate.json": "weak_sharpness",
        "work/weak_sharpness_audit/test_mutations.py": "weak_sharpness",
        "work/weak_sharpness_audit/mutation_report.json": "weak_sharpness",
        "work/weak_sharpness_audit/PROOF_AUDIT.md": "weak_sharpness",
        # The promoted manuscript package is authoritative.  The earlier
        # GLOBAL_PROOF draft remains provenance only and is not a theorem gate.
        **{
            relative: "theorem_promotion"
            for relative in PROMOTION_MANUSCRIPT_FILES
        },
        "work/global_theorem_closure/GLOBAL_PROOF.md": "theorem_historical_provenance",
        "work/global_theorem_closure/README.md": "theorem_historical_provenance",
        "work/global_theorem_closure/RESEARCH_LOG.md": "theorem_historical_provenance",
    }


def corrected_locator(project: Path = PROJECT) -> dict[str, Any]:
    path = project / "work/final_theorem_release/corrected_finite_universe_locator.json"
    locator = load_json(path)
    verify_payload_hash(locator)
    require(locator.get("schema") == CORRECTED_LOCATOR_SCHEMA, "CORRECTED_LOCATOR_SCHEMA_FAIL")
    require(
        locator.get("contract_schema") == CORRECTED_RELEASE_SCHEMA,
        "CORRECTED_LOCATOR_CONTRACT_SCHEMA_FAIL",
    )
    require(locator.get("status") in {"BLOCKED", "FROZEN"}, "CORRECTED_LOCATOR_STATUS_FAIL")
    artifacts = locator.get("artifacts")
    require(isinstance(artifacts, dict), "CORRECTED_LOCATOR_ARTIFACTS_FAIL")
    seen_paths: set[str] = set()
    for role, row in artifacts.items():
        require(isinstance(role, str) and role, "CORRECTED_LOCATOR_ROLE_FAIL")
        require(isinstance(row, dict), "CORRECTED_LOCATOR_ARTIFACT_ROW_FAIL", role)
        relative = row.get("path")
        digest = row.get("sha256")
        require(isinstance(relative, str), "CORRECTED_LOCATOR_PATH_FAIL", role)
        safe_relative(relative)
        require(relative not in seen_paths, "CORRECTED_LOCATOR_PATH_DUPLICATE", relative)
        seen_paths.add(relative)
        require(
            isinstance(digest, str)
            and len(digest) == 64
            and all(character in "0123456789abcdef" for character in digest),
            "CORRECTED_LOCATOR_SHA256_FAIL",
            role,
        )
    required_roles = locator.get("required_frozen_roles")
    require(
        isinstance(required_roles, list)
        and required_roles
        and all(isinstance(role, str) and role for role in required_roles)
        and len(set(required_roles)) == len(required_roles),
        "CORRECTED_LOCATOR_REQUIRED_ROLES_FAIL",
    )
    family_status = locator.get("family_status")
    require(
        isinstance(family_status, dict)
        and set(family_status) == {"raw4", "theta2", "restoration", "cycle", "probe"}
        and all(status in {"PASS", "BLOCKED"} for status in family_status.values()),
        "CORRECTED_LOCATOR_FAMILY_STATUS_FAIL",
    )
    if locator["status"] == "FROZEN":
        require(set(required_roles) <= set(artifacts), "CORRECTED_LOCATOR_FROZEN_ROLE_MISSING")
        require(set(family_status.values()) == {"PASS"}, "CORRECTED_LOCATOR_FROZEN_FAMILY_BLOCKED")
    return locator


def declared_corrected_locator_blockers(project: Path = PROJECT) -> list[str]:
    """Expose signed producer blockers even if a moving artifact fails first."""

    locator = corrected_locator(project)
    if locator["status"] == "FROZEN":
        return []
    blockers = locator.get("blockers")
    require(
        isinstance(blockers, list)
        and blockers
        and all(isinstance(item, str) and item for item in blockers),
        "CORRECTED_LOCATOR_BLOCKERS_FAIL",
    )
    return ["CORRECTED_FINITE_UNIVERSE_NOT_FROZEN", *blockers]


def required_evidence_files(project: Path = PROJECT) -> dict[str, str]:
    """Return the fixed release surface plus signed, dynamically located inputs."""

    result = fixed_evidence_files()
    locator = corrected_locator(project)
    for role, row in locator["artifacts"].items():
        relative = row["path"]
        require(relative not in result, "CORRECTED_LOCATOR_COLLIDES_WITH_FIXED_FILE", relative)
        result[relative] = f"corrected_finite_universe:{role}"
    return result


def build_file_ledger(project: Path = PROJECT) -> tuple[dict[str, dict[str, object]], list[str]]:
    files: dict[str, dict[str, object]] = {}
    missing: list[str] = []
    for relative, layer in sorted(required_evidence_files(project).items()):
        try:
            path = project_file(relative, project)
        except ReleaseFailure:
            missing.append(relative)
            continue
        files[relative] = {
            "layer": layer,
            "sha256": sha_file(path),
            "bytes": path.stat().st_size,
        }
    return files, missing


def validate_locked_files(
    lock: dict[str, Any], project: Path = PROJECT
) -> dict[str, dict[str, object]]:
    files = lock.get("files")
    require(isinstance(files, dict), "LOCK_FILES_SHAPE_FAIL")
    evidence = required_evidence_files(project)
    expected_paths = set(evidence)
    missing = lock.get("missing_required_files")
    require(isinstance(missing, list), "LOCK_MISSING_LIST_SHAPE_FAIL")
    require(
        set(files) | set(missing) == expected_paths,
        "LOCK_REQUIRED_FILE_SET_FAIL",
        sorted(expected_paths ^ (set(files) | set(missing))),
    )
    require(not (set(files) & set(missing)), "LOCK_FILE_MISSING_OVERLAP")
    for relative in missing:
        pure = safe_relative(relative)
        require(
            not project.joinpath(*pure.parts).exists(),
            "LOCK_MISSING_FILE_NOW_PRESENT_REBUILD_REQUIRED",
            relative,
        )
    for relative, metadata in files.items():
        require(isinstance(metadata, dict), "LOCK_FILE_METADATA_FAIL", relative)
        require(
            metadata.get("layer") == evidence[relative],
            "LOCK_FILE_LAYER_FAIL",
            relative,
        )
        path = project_file(relative, project)
        require(sha_file(path) == metadata.get("sha256"), "LOCK_FILE_HASH_FAIL", relative)
        require(path.stat().st_size == metadata.get("bytes"), "LOCK_FILE_SIZE_FAIL", relative)
    return files


def validate_nested_manifests(project: Path = PROJECT) -> dict[str, object]:
    rank_root = project / "work/rank_upper_certificates"
    rank_rows = parse_sha256_manifest(rank_root / "MANIFEST.sha256", rank_root)
    rank_manifest = load_json(rank_root / "manifest.json")
    require(rank_manifest.get("schema") == "k2p-rank-upper-manifest-v1", "RANK_MANIFEST_SCHEMA")
    manifest_rows = {
        row["path"]: row["sha256"] for row in rank_manifest.get("files", [])
    }
    require(manifest_rows == rank_rows, "RANK_MANIFEST_CROSS_FORMAT_FAIL")
    require(rank_manifest.get("file_count") == len(rank_rows) == 95, "RANK_MANIFEST_COUNT_FAIL")
    aggregate = hashlib.sha256(
        b"".join(
            f"{digest}  {relative}\n".encode()
            for relative, digest in sorted(rank_rows.items())
        )
    ).hexdigest()
    require(aggregate == rank_manifest.get("aggregate_sha256"), "RANK_MANIFEST_AGGREGATE_FAIL")

    cycle_root = project / "work/cycle_three_port_closure"
    cycle_rows = parse_sha256_manifest(cycle_root / "MANIFEST.sha256", cycle_root)
    require(len(cycle_rows) == 17, "CYCLE_MANIFEST_COUNT_FAIL")

    direct_root = project / "package/referee/k2p_offline_sweep_portable"
    direct = load_json(direct_root / "DIRECT_CLOSURE_LOCK.json")
    require(
        direct.get("schema") == "k2p-four-port-direct-closure-lock-v1",
        "DIRECT_NESTED_LOCK_SCHEMA_FAIL",
    )
    direct_files = direct.get("files")
    require(isinstance(direct_files, dict), "DIRECT_NESTED_LOCK_FILES_FAIL")
    require(
        direct.get("file_count") == len(direct_files) == 60,
        "DIRECT_NESTED_LOCK_COUNT_FAIL",
    )
    direct_total = 0
    for relative, digest in direct_files.items():
        path = direct_root.joinpath(*safe_relative(relative).parts)
        require(path.is_file(), "DIRECT_NESTED_FILE_MISSING", relative)
        require(sha_file(path) == digest, "DIRECT_NESTED_FILE_HASH_FAIL", relative)
        direct_total += path.stat().st_size
    require(direct_total == direct.get("total_bytes"), "DIRECT_NESTED_TOTAL_BYTES_FAIL")

    # The direct-release verifier follows its byte-locked INPUT_LOCK at run
    # time.  Validate that second-level dependency partition here so a clean
    # referee copy never relies on an uncommitted descriptor, rank table, or
    # executable merely because INPUT_LOCK.json itself was committed.
    direct_input = load_json(direct_root / "INPUT_LOCK.json")
    require(
        direct_input.get("schema") == "k2p-offline-four-port-input-lock-v1",
        "DIRECT_INPUT_LOCK_SCHEMA_FAIL",
    )
    require(
        direct_input.get("expected_source_class_counts")
        == [536, 747, 276, 276, 64, 32],
        "DIRECT_INPUT_LOCK_CLASS_CENSUS_FAIL",
    )
    require(
        direct_input.get("expected_source_ranks") == [13, 14, 14, 14, 15, 16],
        "DIRECT_INPUT_LOCK_RANK_CENSUS_FAIL",
    )
    direct_input_files = direct_input.get("files")
    require(
        isinstance(direct_input_files, dict) and len(direct_input_files) == 15,
        "DIRECT_INPUT_LOCK_FILES_FAIL",
    )
    for relative, digest in direct_input_files.items():
        require(is_sha256(digest), "DIRECT_INPUT_LOCK_SHA256_FAIL", relative)
        path = direct_root.joinpath(*safe_relative(relative).parts)
        require(path.is_file(), "DIRECT_INPUT_LOCK_FILE_MISSING", relative)
        require(
            sha_file(path) == digest,
            "DIRECT_INPUT_LOCK_FILE_HASH_FAIL",
            relative,
        )
    require(
        direct_input.get("compiler_sha256")
        == direct_input_files.get("atlas/k2p_atlas_core.py"),
        "DIRECT_INPUT_LOCK_COMPILER_BINDING_FAIL",
    )
    return {
        "rank_manifest_files": len(rank_rows),
        "cycle_manifest_files": len(cycle_rows),
        "direct_nested_files": len(direct_files),
        "direct_input_lock_files": len(direct_input_files),
    }


def validate_probe_transport_restrictions(probe: dict[str, Any]) -> dict[str, int]:
    """Independently check literal parent-map restriction on every survivor."""

    def transport_map(row: dict[str, Any]) -> dict[str, str]:
        transport = row.get("transport")
        require(isinstance(transport, dict), "PROBE_TRANSPORT_SHAPE_FAIL")
        mapping = transport.get("vertex_map")
        require(isinstance(mapping, list), "PROBE_VERTEX_MAP_SHAPE_FAIL")
        result: dict[str, str] = {}
        target_seen: set[str] = set()
        for pair in mapping:
            require(
                isinstance(pair, list)
                and len(pair) == 2
                and all(isinstance(item, str) for item in pair),
                "PROBE_VERTEX_MAP_PAIR_FAIL",
            )
            source, target = pair
            require(source not in result, "PROBE_VERTEX_MAP_SOURCE_DUPLICATE", source)
            require(target not in target_seen, "PROBE_VERTEX_MAP_TARGET_DUPLICATE", target)
            result[source] = target
            target_seen.add(target)
        require(
            sha_object(transport) == row.get("transport_sha256"),
            "PROBE_TRANSPORT_HASH_FAIL",
            row.get("relation_id", row.get("anchor_id")),
        )
        return result

    anchors = probe.get("anchors", {}).get("records")
    one_rows = probe.get("one_port", {}).get("survivors")
    two_rows = probe.get("two_port", {}).get("survivors")
    require(isinstance(anchors, list), "PROBE_ANCHOR_ROWS_FAIL")
    require(isinstance(one_rows, list), "PROBE_ONE_ROWS_FAIL")
    require(isinstance(two_rows, list), "PROBE_TWO_ROWS_FAIL")
    anchor_by_id = {row["anchor_id"]: row for row in anchors}
    require(len(anchor_by_id) == len(anchors), "PROBE_ANCHOR_ID_DUPLICATE")
    one_by_id: dict[str, dict[str, Any]] = {}

    def check_child(row: dict[str, Any], parent: dict[str, Any], label: str) -> None:
        require(
            row.get("transport_restriction") == "exact_on_all_parent_mixed_vertices",
            "PROBE_RESTRICTION_MARKER_FAIL",
            label,
        )
        require(
            row.get("parent_transport_sha256") == parent.get("transport_sha256"),
            "PROBE_PARENT_TRANSPORT_HASH_FAIL",
            label,
        )
        parent_map = transport_map(parent)
        child_map = transport_map(row)
        require(
            all(child_map.get(source) == target for source, target in parent_map.items()),
            "PROBE_LITERAL_TRANSPORT_RESTRICTION_FAIL",
            label,
        )
        require(
            row.get("global_triangle") == parent.get("global_triangle"),
            "PROBE_GLOBAL_TRIANGLE_DRIFT",
            label,
        )

    for row in one_rows:
        relation_id = row.get("relation_id")
        require(isinstance(relation_id, str), "PROBE_ONE_ID_FAIL")
        parent = anchor_by_id.get(row.get("parent_id"))
        require(parent is not None, "PROBE_ONE_PARENT_FAIL", relation_id)
        check_child(row, parent, relation_id)
        require(relation_id not in one_by_id, "PROBE_ONE_ID_DUPLICATE", relation_id)
        one_by_id[relation_id] = row
    for row in two_rows:
        relation_id = row.get("relation_id")
        require(isinstance(relation_id, str), "PROBE_TWO_ID_FAIL")
        parent = one_by_id.get(row.get("parent_id"))
        require(parent is not None, "PROBE_TWO_PARENT_FAIL", relation_id)
        check_child(row, parent, relation_id)
        require(
            row.get("grandparent_id") == parent.get("parent_id"),
            "PROBE_GRANDPARENT_FAIL",
            relation_id,
        )
    return {
        "anchors": len(anchors),
        "one_port_survivors": len(one_rows),
        "two_port_survivors": len(two_rows),
    }


def is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def locator_artifacts(
    locator: dict[str, Any], project: Path = PROJECT
) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for role, row in locator["artifacts"].items():
        path = project_file(row["path"], project)
        require(sha_file(path) == row["sha256"], "CORRECTED_LOCATOR_ARTIFACT_DRIFT", role)
        result[role] = path
    return result


def json_lines(path: Path) -> Iterable[dict[str, Any]]:
    opener = gzip.open if path.suffix == ".gz" else open
    try:
        with opener(path, "rt", encoding="utf-8") as handle:
            for ordinal, line in enumerate(handle, 1):
                require(bool(line.strip()), "CORRECTED_LEDGER_BLANK_LINE", f"{path}:{ordinal}")
                try:
                    row = json.loads(line, object_pairs_hook=unique_object)
                except (UnicodeError, json.JSONDecodeError) as error:
                    raise ReleaseFailure(
                        f"CORRECTED_LEDGER_JSON_FAIL:{path}:{ordinal}:{error}"
                    ) from error
                require(isinstance(row, dict), "CORRECTED_LEDGER_ROW_SHAPE_FAIL", ordinal)
                yield row
    except OSError as error:
        raise ReleaseFailure(f"CORRECTED_LEDGER_READ_FAIL:{path}:{error}") from error


def legacy_raw_four_flags(project: Path = PROJECT) -> tuple[bytearray, bytearray]:
    """Independently recover the quartet and revoked-row ID sets."""

    quartet = bytearray(RAW_FOUR_TOTAL)
    revoked = bytearray(RAW_FOUR_TOTAL)
    path = project / "work/raw_ledger_audit/artifacts/raw_directional_ledger.jsonl.gz"
    count = 0
    for ordinal, row in enumerate(json_lines(path)):
        raw_id = row.get("raw_id")
        require(raw_id == ordinal, "LEGACY_RAW4_ID_ORDER_FAIL", ordinal)
        require(0 <= raw_id < RAW_FOUR_TOTAL, "LEGACY_RAW4_ID_RANGE_FAIL", raw_id)
        reason = row.get("topology_exclusion_reason")
        if reason == "quartet":
            quartet[raw_id] = 1
        elif reason == "tree_sunlet":
            revoked[raw_id] = 1
        count += 1
    require(count == RAW_FOUR_TOTAL, "LEGACY_RAW4_CENSUS_FAIL", count)
    require(sum(revoked) == REVOKED_RAW_FOUR_ROWS, "LEGACY_REVOKED_CENSUS_FAIL", sum(revoked))
    require(not any(left and right for left, right in zip(quartet, revoked)), "LEGACY_TOPOLOGY_SET_OVERLAP")
    return quartet, revoked


def validate_raw4_full_map_truth(path: Path) -> dict[str, Any]:
    full_map = load_json(path)
    verify_payload_hash(full_map)
    require(
        full_map.get("schema") == "k2p-raw4-tree-sunlet-full-map-truth-v1",
        "RAW4_FULL_MAP_TRUTH_SCHEMA_FAIL",
    )
    require(full_map.get("status") == "PASS", "RAW4_FULL_MAP_TRUTH_NOT_PASS")
    for field in (
        "claimed_rows",
        "full_map_strict_source_sign_rows",
        "full_map_target_zero_rows",
    ):
        require(
            full_map.get(field) == REVOKED_RAW_FOUR_ROWS,
            "RAW4_FULL_MAP_TRUTH_CENSUS_FAIL",
            field,
        )
    require(
        full_map.get("canonical_polynomial_relation_classes") == 8,
        "RAW4_FULL_MAP_CLASS_CENSUS_FAIL",
    )
    require(
        full_map.get("exact_full_graph_relation_census")
        == {"none": REVOKED_RAW_FOUR_ROWS},
        "RAW4_FULL_MAP_EXACT_RELATION_FAIL",
    )
    for field in ("false_iso_or_triangle_conflicts", "incoherent", "unresolved"):
        require(full_map.get(field) == 0, "RAW4_FULL_MAP_ZERO_GATE_FAIL", field)
    row_hashes = full_map.get("ordered_truth_row_hashes")
    require(
        isinstance(row_hashes, list)
        and len(row_hashes) == REVOKED_RAW_FOUR_ROWS
        and all(is_sha256(item) for item in row_hashes),
        "RAW4_FULL_MAP_ROW_HASH_LEDGER_FAIL",
    )
    require(
        sha_object(row_hashes) == full_map.get("ordered_truth_row_hash_root"),
        "RAW4_FULL_MAP_ROW_HASH_ROOT_FAIL",
    )
    require(
        "replacement claim is the exact full-map strict-sign separator"
        in full_map.get("claim_boundary", ""),
        "RAW4_FULL_MAP_CLAIM_BOUNDARY_FAIL",
    )
    return full_map


def load_gzip_json(path: Path) -> dict[str, Any]:
    try:
        with gzip.open(path, "rt", encoding="utf-8") as handle:
            value = json.load(handle, object_pairs_hook=unique_object)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ReleaseFailure(f"GZIP_JSON_READ_FAIL:{path}:{error}") from error
    require(isinstance(value, dict), "GZIP_JSON_TOP_LEVEL_FAIL", path)
    return value


def derived_restoration_class_census(project: Path = PROJECT) -> dict[str, Any]:
    path = project / "work/raw_ledger_audit/artifacts/retained_class_partition.json.gz"
    payload = load_gzip_json(path)
    require(
        payload.get("schema") == "k2p-four-port-raw-directional-ledger-v1",
        "CORRECTED_CLASS_SOURCE_SCHEMA_FAIL",
    )
    classes = payload.get("classes")
    require(isinstance(classes, list), "CORRECTED_CLASS_SOURCE_ROWS_FAIL")
    terminals = [row for row in classes if row.get("ledger_category") == "retained_terminal"]
    parents = [row for row in classes if row.get("ledger_category") == "restoration_obligation"]
    terminal_identifiers = [
        f"source_{row.get('source_index')}:class_{row.get('canonical_class_id'):06d}"
        for row in terminals
        if isinstance(row.get("source_index"), int)
        and isinstance(row.get("canonical_class_id"), int)
    ]
    require(
        len(terminal_identifiers) == len(terminals)
        and len(set(terminal_identifiers)) == len(terminal_identifiers),
        "CORRECTED_CLASS_SOURCE_TERMINAL_IDS_FAIL",
    )
    identifiers = [row.get("restoration_obligation_id") for row in parents]
    require(
        all(isinstance(item, str) and item for item in identifiers)
        and len(set(identifiers)) == len(identifiers),
        "CORRECTED_CLASS_SOURCE_PARENT_IDS_FAIL",
    )
    require(
        all(row.get("status_before_direct_overlay") == "restoration_parent" for row in parents),
        "CORRECTED_CLASS_SOURCE_PARENT_STATUS_FAIL",
    )
    terminal_multiplicities = {
        str(key): value
        for key, value in sorted(
            Counter(row.get("raw_presentation_count") for row in terminals).items()
        )
    }
    parent_multiplicities = {
        str(key): value
        for key, value in sorted(
            Counter(row.get("raw_presentation_count") for row in parents).items()
        )
    }
    require(
        terminal_multiplicities == RAW4_TERMINAL_CLASS_MULTIPLICITIES,
        "CORRECTED_CLASS_SOURCE_TERMINAL_MULTIPLICITY_FAIL",
    )
    require(
        parent_multiplicities == RAW4_RESTORATION_PARENT_MULTIPLICITIES,
        "CORRECTED_CLASS_SOURCE_PARENT_MULTIPLICITY_FAIL",
    )
    require(
        sum(int(size) * count for size, count in terminal_multiplicities.items())
        == RAW4_COMPOSITE_CATEGORY_COUNTS["direct_terminal_presentation"],
        "CORRECTED_CLASS_SOURCE_TERMINAL_PRESENTATION_CENSUS_FAIL",
    )
    require(
        sum(int(size) * count for size, count in parent_multiplicities.items())
        == RAW4_COMPOSITE_CATEGORY_COUNTS["restoration_member_presentation"],
        "CORRECTED_CLASS_SOURCE_PARENT_PRESENTATION_CENSUS_FAIL",
    )
    return {
        "parent_count": len(parents),
        "parent_ids_sha256": sha_object(sorted(identifiers)),
        "parent_multiplicity_histogram": parent_multiplicities,
        "terminal_class_count": len(terminals),
        "terminal_class_ids_sha256": sha_object(sorted(terminal_identifiers)),
        "terminal_multiplicity_histogram": terminal_multiplicities,
        "class_ledger_sha256": sha_file(path),
    }


def validate_raw4_corrected_overlay(
    paths: dict[str, Path], full_map: dict[str, Any], project: Path = PROJECT
) -> dict[str, Any]:
    required_roles = {
        "corrected_overlay",
        "corrected_overlay_builder",
        "corrected_overlay_verifier",
        "corrected_overlay_replay",
        "corrected_overlay_mutation_runner",
        "corrected_overlay_mutation_report",
    }
    require(required_roles <= set(paths), "RAW4_CORRECTED_OVERLAY_ROLE_MISSING", sorted(required_roles - set(paths)))
    overlay_path = paths["corrected_overlay"]
    overlay = load_json(overlay_path)
    verify_payload_hash(overlay)
    require(
        overlay.get("schema") == "k2p-raw4-corrected-terminal-overlay-v2",
        "RAW4_CORRECTED_OVERLAY_SCHEMA_FAIL",
    )
    require(overlay.get("status") == "PASS", "RAW4_CORRECTED_OVERLAY_NOT_PASS")
    for field in ("historical_rows_selected", "corrected_rows", "raw_id_unique"):
        require(
            overlay.get(field) == REVOKED_RAW_FOUR_ROWS,
            "RAW4_CORRECTED_OVERLAY_CENSUS_FAIL",
            field,
        )
    require(
        overlay.get("corrected_category_census") == {"exact_exclusion": REVOKED_RAW_FOUR_ROWS},
        "RAW4_CORRECTED_CATEGORY_CENSUS_FAIL",
    )
    require(
        overlay.get("corrected_reason_census")
        == {"full_map_Ti_strict_sign": REVOKED_RAW_FOUR_ROWS},
        "RAW4_CORRECTED_REASON_CENSUS_FAIL",
    )
    require(
        overlay.get("exact_full_graph_relation_census") == {"none": REVOKED_RAW_FOUR_ROWS},
        "RAW4_CORRECTED_GRAPH_RELATION_CENSUS_FAIL",
    )
    require(
        overlay.get("canonical_polynomial_relation_classes") == 8,
        "RAW4_CORRECTED_POLYNOMIAL_CLASS_CENSUS_FAIL",
    )
    coverage = overlay.get("coverage")
    hashes = overlay.get("coverage_row_hashes")
    require(
        isinstance(coverage, list)
        and isinstance(hashes, list)
        and len(coverage) == len(hashes) == REVOKED_RAW_FOUR_ROWS,
        "RAW4_CORRECTED_COVERAGE_SHAPE_FAIL",
    )
    require([sha_object(row) for row in coverage] == hashes, "RAW4_CORRECTED_ROW_HASH_FAIL")
    require(sha_object(hashes) == overlay.get("coverage_hash_root"), "RAW4_CORRECTED_HASH_ROOT_FAIL")
    raw_ids = [row.get("raw_id") for row in coverage]
    require(
        all(isinstance(raw_id, int) for raw_id in raw_ids)
        and raw_ids == sorted(set(raw_ids)),
        "RAW4_CORRECTED_RAW_ID_ORDER_OR_DUPLICATE_FAIL",
    )
    _, revoked = legacy_raw_four_flags(project)
    require(raw_ids == [raw_id for raw_id, flag in enumerate(revoked) if flag], "RAW4_CORRECTED_RAW_ID_COVERAGE_FAIL")
    for ordinal, row in enumerate(coverage):
        require(row.get("corrected_category") == "exact_exclusion", "RAW4_CORRECTED_ROW_CATEGORY_FAIL", ordinal)
        require(row.get("corrected_reason") == "full_map_Ti_strict_sign", "RAW4_CORRECTED_ROW_REASON_FAIL", ordinal)
        require(row.get("historical_reason") == "tree_sunlet_REVOKED", "RAW4_CORRECTED_ROW_HISTORY_MARKER_FAIL", ordinal)
        require(row.get("exact_full_graph_relation") == "none", "RAW4_CORRECTED_ROW_GRAPH_RELATION_FAIL", ordinal)
        require(is_sha256(row.get("source_pullback_sha256")), "RAW4_CORRECTED_SOURCE_DIGEST_FAIL", ordinal)
        require(is_sha256(row.get("target_pullback_sha256")), "RAW4_CORRECTED_TARGET_DIGEST_FAIL", ordinal)

    inputs = overlay.get("inputs")
    require(isinstance(inputs, dict), "RAW4_CORRECTED_INPUTS_FAIL")
    expected_inputs = {
        "adversarial_full_map_certificate_sha256": sha_file(paths["raw4_full_map_truth_certificate"]),
        "atlas_sha256": sha_file(
            project
            / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
        ),
        "historical_raw_ledger_sha256": sha_file(
            project / "work/raw_ledger_audit/artifacts/raw_directional_ledger.jsonl.gz"
        ),
        "historical_raw_summary_sha256": sha_file(
            project / "work/raw_ledger_audit/artifacts/raw_ledger_summary.json"
        ),
        "provisional_independent_partition_sha256": sha_file(
            paths["preliminary_reclassification"]
        ),
    }
    require(inputs == expected_inputs, "RAW4_CORRECTED_INPUT_BINDING_FAIL")
    require(
        overlay.get("cross_replay")
        == {
            "adversarial_payload_sha256": full_map["payload_sha256"],
            "agreement_polynomial_relation_classes": 8,
            "agreement_rows": REVOKED_RAW_FOUR_ROWS,
        },
        "RAW4_CORRECTED_CROSS_REPLAY_FAIL",
    )

    classes = derived_restoration_class_census(project)
    parent_effect = overlay.get("parent_census_effect")
    require(isinstance(parent_effect, dict), "RAW4_CORRECTED_PARENT_EFFECT_FAIL")
    require(parent_effect.get("new_restoration_parent_classes_from_corrected_family") == 0, "RAW4_CORRECTED_NEW_PARENT_FAIL")
    require(parent_effect.get("historical_restoration_parent_classes") == classes["parent_count"], "RAW4_CORRECTED_HISTORICAL_PARENT_FAIL")
    require(parent_effect.get("corrected_total_restoration_parent_classes") == classes["parent_count"], "RAW4_CORRECTED_TOTAL_PARENT_FAIL")

    replay = load_json(paths["corrected_overlay_replay"])
    verify_payload_hash(replay)
    require(replay.get("schema") == "k2p-raw4-corrected-independent-replay-v1", "RAW4_CORRECTED_REPLAY_SCHEMA_FAIL")
    require(replay.get("status") == "PASS", "RAW4_CORRECTED_REPLAY_NOT_PASS")
    require(replay.get("certificate_sha256") == sha_file(overlay_path), "RAW4_CORRECTED_REPLAY_FILE_BINDING_FAIL")
    require(replay.get("certificate_payload_sha256") == overlay["payload_sha256"], "RAW4_CORRECTED_REPLAY_PAYLOAD_BINDING_FAIL")
    for field in ("raw_rows_replayed", "strict_source_negative_rows", "target_zero_rows"):
        require(replay.get(field) == REVOKED_RAW_FOUR_ROWS, "RAW4_CORRECTED_REPLAY_CENSUS_FAIL", field)
    require(replay.get("sign_classes_replayed") == 8, "RAW4_CORRECTED_REPLAY_SIGN_CLASS_FAIL")
    require(replay.get("corrected_restoration_parent_classes") == classes["parent_count"], "RAW4_CORRECTED_REPLAY_PARENT_FAIL")
    for field in ("false_graph_terminal_conflicts", "unresolved"):
        require(replay.get(field) == 0, "RAW4_CORRECTED_REPLAY_ZERO_GATE_FAIL", field)

    mutations = load_json(paths["corrected_overlay_mutation_report"])
    verify_payload_hash(mutations)
    require(mutations.get("schema") == "k2p-raw4-corrected-mutations-v1", "RAW4_CORRECTED_MUTATION_SCHEMA_FAIL")
    require(mutations.get("status") == "PASS", "RAW4_CORRECTED_MUTATIONS_NOT_PASS")
    require(mutations.get("source_certificate_sha256") == sha_file(overlay_path), "RAW4_CORRECTED_MUTATION_BINDING_FAIL")
    results = mutations.get("results")
    require(isinstance(results, list) and mutations.get("mutation_count") == len(results), "RAW4_CORRECTED_MUTATION_CENSUS_FAIL")
    require(mutations.get("survived") == 0 and all(row.get("rejected") is True for row in results), "RAW4_CORRECTED_MUTATION_SURVIVOR")
    required_mutations = {
        "omitted_raw_record",
        "reassigned_raw_record",
        "wrong_port_transport",
        "reassigned_polynomial_certificate",
        "mutated_Bernstein_coefficient",
        "reversed_sign_conclusion",
        "reassigned_descriptor_class",
        "python_optimized_mode",
    }
    observed_mutations = {row.get("mutation") for row in results}
    require(required_mutations <= observed_mutations, "RAW4_CORRECTED_MUTATION_COVERAGE_FAIL", sorted(required_mutations - observed_mutations))
    return {
        "overlay_payload_sha256": overlay["payload_sha256"],
        "overlay_file_sha256": sha_file(overlay_path),
        "corrected_rows": REVOKED_RAW_FOUR_ROWS,
        "corrected_reason": "full_map_Ti_strict_sign",
        "polynomial_classes": 8,
        "new_restoration_parents": 0,
        "derived_parent_count": classes["parent_count"],
        "class_ledger_sha256": classes["class_ledger_sha256"],
        "independent_replay_payload_sha256": replay["payload_sha256"],
        "mutation_payload_sha256": mutations["payload_sha256"],
        "mutation_count": len(results),
    }


def validate_dynamic_family_record(name: str, row: object) -> dict[str, Any]:
    require(isinstance(row, dict), "CORRECTED_FAMILY_RECORD_FAIL", name)
    input_count = row.get("input_count")
    require(isinstance(input_count, int) and input_count >= 0, "CORRECTED_FAMILY_INPUT_COUNT_FAIL", name)
    require(row.get("distinct_input_ids") == input_count, "CORRECTED_FAMILY_DISTINCT_INPUT_FAIL", name)
    for field in (
        "duplicate_input_ids",
        "missing_input_ids",
        "unresolved",
        "forbidden_rooted_reason_count",
        "forbidden_rooted_field_count",
        "false_topology_oracle_count",
        "false_graph_terminal_conflicts",
    ):
        require(row.get(field) == 0, "CORRECTED_FAMILY_ZERO_GATE_FAIL", f"{name}:{field}")
    require(row.get("rows_with_exact_reason") == input_count, "CORRECTED_FAMILY_REASON_COVERAGE_FAIL", name)
    require(row.get("rows_with_exact_evidence") == input_count, "CORRECTED_FAMILY_EVIDENCE_COVERAGE_FAIL", name)
    categories = row.get("output_category_counts")
    require(
        isinstance(categories, dict)
        and all(isinstance(key, str) and key for key in categories)
        and all(isinstance(value, int) and value >= 0 for value in categories.values())
        and sum(categories.values()) == input_count,
        "CORRECTED_FAMILY_OUTPUT_PARTITION_FAIL",
        name,
    )
    require(is_sha256(row.get("input_id_hash_root")), "CORRECTED_FAMILY_INPUT_ROOT_FAIL", name)
    require(is_sha256(row.get("output_id_hash_root")), "CORRECTED_FAMILY_OUTPUT_ROOT_FAIL", name)
    children = row.get("generated_children")
    child_count = 0
    child_id_hash_root = None
    child_edge_hash_root = None
    child_transport_hash_root = None
    if children is not None:
        require(isinstance(children, dict), "CORRECTED_FAMILY_CHILD_RECORD_FAIL", name)
        child_count = children.get("count")
        require(isinstance(child_count, int) and child_count >= 0, "CORRECTED_FAMILY_CHILD_COUNT_FAIL", name)
        require(children.get("distinct_ids") == child_count, "CORRECTED_FAMILY_CHILD_DISTINCT_FAIL", name)
        for field in ("duplicate_ids", "missing_parent_links", "multiple_parent_links", "unresolved"):
            require(children.get(field) == 0, "CORRECTED_FAMILY_CHILD_ZERO_GATE_FAIL", f"{name}:{field}")
        for field in (
            "id_hash_root",
            "parent_child_edge_hash_root",
            "transport_restriction_hash_root",
        ):
            require(is_sha256(children.get(field)), "CORRECTED_FAMILY_CHILD_ROOT_FAIL", f"{name}:{field}")
        child_id_hash_root = children["id_hash_root"]
        child_edge_hash_root = children["parent_child_edge_hash_root"]
        child_transport_hash_root = children["transport_restriction_hash_root"]
    return {
        "input_count": input_count,
        "output_category_counts": categories,
        "generated_child_count": child_count,
        "generated_child_id_hash_root": child_id_hash_root,
        "generated_child_edge_hash_root": child_edge_hash_root,
        "generated_child_transport_hash_root": child_transport_hash_root,
        "input_id_hash_root": row["input_id_hash_root"],
        "output_id_hash_root": row["output_id_hash_root"],
    }


def validate_composite_primitive_summary(
    family: str,
    paths: dict[str, Path],
    total: int,
    expected_categories: dict[str, int],
) -> dict[str, Any]:
    """Validate one authoritative corrected primitive ledger package.

    Historical raw ledgers and overlays are inputs to these packages, never
    promotion partitions.  The independently regenerated canonical byte stream
    is the promotion object.
    """

    require(family in {"raw4", "theta2"}, "COMPOSITE_FAMILY_FAIL", family)
    roles = {
        "generator": "corrected_composite_generator",
        "ledger": f"{family}_corrected_composite_ledger",
        "summary": f"{family}_corrected_composite_summary",
        "verifier": "corrected_composite_independent_verifier",
        "replay": f"{family}_corrected_composite_replay",
        "mutation": f"{family}_corrected_composite_mutation_report",
    }
    require(
        set(roles.values()) <= set(paths),
        "COMPOSITE_ROLE_MISSING",
        f"{family}:{sorted(set(roles.values()) - set(paths))}",
    )
    located = {name: paths[role] for name, role in roles.items()}
    summary = load_json(located["summary"])
    verify_payload_hash(summary)
    require(
        summary.get("schema") == f"k2p-{family}-corrected-composite-summary-v1",
        "COMPOSITE_SUMMARY_SCHEMA_FAIL",
        family,
    )
    require(summary.get("status") == "PASS", "COMPOSITE_SUMMARY_NOT_PASS", family)
    require(summary.get("row_schema") == f"k2p-{family}-corrected-composite-row-v1", "COMPOSITE_ROW_SCHEMA_FAIL", family)
    require(summary.get("total_rows") == total, "COMPOSITE_TOTAL_FAIL", family)
    require(summary.get("distinct_raw_ids") == total, "COMPOSITE_DISTINCT_ID_FAIL", family)
    require(summary.get("raw_id_min") == 0, "COMPOSITE_MIN_ID_FAIL", family)
    require(summary.get("raw_id_max") == total - 1, "COMPOSITE_MAX_ID_FAIL", family)
    for field in (
        "duplicate_raw_ids",
        "missing_raw_ids",
        "missing_evidence_bindings",
        "multiple_evidence_bindings",
        "unresolved",
        "forbidden_rooted_field_count",
        "forbidden_rooted_reason_count",
    ):
        require(summary.get(field) == 0, "COMPOSITE_ZERO_GATE_FAIL", f"{family}:{field}")
    require(
        summary.get("category_counts") == expected_categories,
        "COMPOSITE_CATEGORY_CENSUS_FAIL",
        family,
    )
    require(sum(expected_categories.values()) == total, "COMPOSITE_EXPECTED_CENSUS_INTERNAL_FAIL", family)
    require(
        summary.get("serialization") == COMPOSITE_SERIALIZATION,
        "COMPOSITE_SERIALIZATION_FAIL",
        family,
    )
    require(summary.get("ledger_sha256") == sha_file(located["ledger"]), "COMPOSITE_LEDGER_BINDING_FAIL", family)
    require(summary.get("generator_sha256") == sha_file(located["generator"]), "COMPOSITE_GENERATOR_BINDING_FAIL", family)
    require(summary.get("verifier_sha256") == sha_file(located["verifier"]), "COMPOSITE_VERIFIER_BINDING_FAIL", family)
    require(summary.get("gzip_compresslevel") == 6, "COMPOSITE_GZIP_LEVEL_FAIL", family)
    require(
        summary.get("raw_id_hash_root_algorithm")
        == "sha256(concat(binary_sha256(canonical_raw_id_json)))",
        "COMPOSITE_RAW_ID_ROOT_ALGORITHM_FAIL",
        family,
    )
    require(
        summary.get("row_hash_root_algorithm")
        == "sha256(concat(binary_sha256(canonical_row_json)))",
        "COMPOSITE_ROW_ROOT_ALGORITHM_FAIL",
        family,
    )
    require(
        isinstance(summary.get("uncompressed_bytes"), int)
        and summary["uncompressed_bytes"] > 0,
        "COMPOSITE_UNCOMPRESSED_SIZE_FAIL",
        family,
    )
    for field in (
        "uncompressed_stream_sha256",
        "ordered_row_hash_root",
        "ordered_raw_id_hash_root",
    ):
        require(is_sha256(summary.get(field)), "COMPOSITE_HASH_ROOT_FAIL", f"{family}:{field}")
    inputs = summary.get("input_artifact_sha256")
    require(
        isinstance(inputs, dict)
        and inputs
        and all(isinstance(key, str) and key for key in inputs)
        and all(is_sha256(value) for value in inputs.values()),
        "COMPOSITE_INPUT_BINDINGS_FAIL",
        family,
    )
    if family == "raw4":
        required_input_names = {
            "atlas",
            "class_partition",
            "historical_raw_ledger_provenance",
            "rank_lower",
            "rank_upper",
            "restoration_forest",
            "terminal_registry",
            "whole_map_adversarial_truth",
            "whole_map_overlay",
        }
        require(set(inputs) == required_input_names, "RAW4_COMPOSITE_INPUT_SET_FAIL", sorted(set(inputs) ^ required_input_names))
        require(inputs["restoration_forest"] == sha_file(paths["restoration_v3_forest_certificate"]), "RAW4_COMPOSITE_RESTORATION_INPUT_FAIL")
        require(inputs["terminal_registry"] == sha_file(paths["raw4_terminal_certificate_registry"]), "RAW4_COMPOSITE_TERMINAL_REGISTRY_INPUT_FAIL")
        require(inputs["whole_map_adversarial_truth"] == sha_file(paths["raw4_full_map_truth_certificate"]), "RAW4_COMPOSITE_TRUTH_INPUT_FAIL")
        require(inputs["whole_map_overlay"] == sha_file(paths["corrected_overlay"]), "RAW4_COMPOSITE_OVERLAY_INPUT_FAIL")
    else:
        required_input_names = {
            "atlas",
            "direct_certificates",
            "historical_raw_ledger_provenance",
            "rank_certificates",
            "restoration_closure",
            "whole_map_adversarial_truth",
        }
        require(set(inputs) == required_input_names, "THETA2_COMPOSITE_INPUT_SET_FAIL", sorted(set(inputs) ^ required_input_names))
        require(inputs["whole_map_adversarial_truth"] == sha_file(paths["theta2_full_map_truth_certificate"]), "THETA2_COMPOSITE_TRUTH_INPUT_FAIL")
    require(summary.get("rows_with_source_target_permutation") == total, "COMPOSITE_PRESENTATION_COVERAGE_FAIL", family)
    require(summary.get("rows_with_evidence_binding") == total, "COMPOSITE_EVIDENCE_COVERAGE_FAIL", family)

    quartet_rows = expected_categories["displayed_quartet_exclusion"]
    full_map_rows = expected_categories["full_map_Ti_strict_sign"]
    rank_rows = expected_categories["exact_rank_exclusion"]
    require(summary.get("quartet_witness_rows") == quartet_rows, "COMPOSITE_QUARTET_BINDING_FAIL", family)
    full_map = summary.get("full_map_Ti_coverage")
    require(isinstance(full_map, dict), "COMPOSITE_FULL_MAP_RECORD_FAIL", family)
    for field in (
        "rows",
        "whole_map_pullbacks_replayed",
        "exact_graph_relation_none_rows",
        "coefficient_certificate_rows",
    ):
        require(full_map.get(field) == full_map_rows, "COMPOSITE_FULL_MAP_COVERAGE_FAIL", f"{family}:{field}")
    require(full_map.get("unresolved") == 0, "COMPOSITE_FULL_MAP_UNRESOLVED", family)
    if family == "raw4":
        require(full_map.get("source_strict_sign_rows") == full_map_rows, "RAW4_COMPOSITE_FULL_MAP_SOURCE_SIGN_FAIL")
        require(full_map.get("target_zero_rows") == full_map_rows, "RAW4_COMPOSITE_FULL_MAP_TARGET_ZERO_FAIL")
    else:
        require(full_map.get("source_zero_rows") == full_map_rows, "THETA2_COMPOSITE_FULL_MAP_SOURCE_ZERO_FAIL")
        require(full_map.get("target_strict_sign_rows") == full_map_rows, "THETA2_COMPOSITE_FULL_MAP_TARGET_SIGN_FAIL")
    rank = summary.get("rank_certificate_coverage")
    require(isinstance(rank, dict), "COMPOSITE_RANK_RECORD_FAIL", family)
    for field in ("rows", "exact_lower_rows", "symbolic_upper_rows", "matched_lower_upper_rows"):
        require(rank.get(field) == rank_rows, "COMPOSITE_RANK_COVERAGE_FAIL", f"{family}:{field}")
    require(rank.get("unresolved") == 0, "COMPOSITE_RANK_UNRESOLVED", family)

    result: dict[str, Any] = {
        "total_rows": total,
        "category_counts": expected_categories,
        "ledger_sha256": summary["ledger_sha256"],
        "ordered_row_hash_root": summary["ordered_row_hash_root"],
        "ordered_raw_id_hash_root": summary["ordered_raw_id_hash_root"],
        "summary_payload_sha256": summary["payload_sha256"],
    }
    if family == "raw4":
        classes = derived_restoration_class_census(PROJECT)
        terminal_registry = load_gzip_json(paths["raw4_terminal_certificate_registry"])
        verify_payload_hash(terminal_registry)
        require(
            terminal_registry.get("schema")
            == "k2p-raw4-terminal-certificate-registry-v1",
            "RAW4_TERMINAL_REGISTRY_SCHEMA_FAIL",
        )
        require(terminal_registry.get("status") == "PASS", "RAW4_TERMINAL_REGISTRY_NOT_PASS")
        registry_rows = terminal_registry.get("rows")
        require(
            isinstance(registry_rows, list)
            and len(registry_rows)
            == terminal_registry.get("terminal_class_count")
            == classes["terminal_class_count"],
            "RAW4_TERMINAL_REGISTRY_CENSUS_FAIL",
        )
        registry_ids: list[str] = []
        registry_kinds: Counter[str] = Counter()
        for ordinal, row in enumerate(registry_rows):
            require(isinstance(row, dict), "RAW4_TERMINAL_REGISTRY_ROW_FAIL", ordinal)
            source_index = row.get("source_index")
            class_id = row.get("class_id")
            identifier = row.get("class_identifier")
            require(
                isinstance(source_index, int)
                and isinstance(class_id, int)
                and identifier == f"source_{source_index}:class_{class_id:06d}",
                "RAW4_TERMINAL_REGISTRY_ID_FAIL",
                ordinal,
            )
            registry_ids.append(identifier)
            for field in (
                "descriptor_sha256",
                "manifest_record_sha256",
                "semantic_record_sha256",
                "certificate_binding_sha256",
            ):
                require(is_sha256(row.get(field)), "RAW4_TERMINAL_REGISTRY_HASH_FAIL", f"{ordinal}:{field}")
            terminal_certificate = row.get("terminal_certificate")
            require(isinstance(terminal_certificate, dict), "RAW4_TERMINAL_REGISTRY_CERTIFICATE_FAIL", ordinal)
            kind = terminal_certificate.get("kind")
            require(
                kind
                in {
                    "exact_multihomogeneous_quadratic",
                    "exact_direct_polynomial_separator",
                    "ordinary_triangle_quotient",
                    "exact_mixed_graph_isomorphism",
                    "direct_hard_case_F2_F3_F4",
                },
                "RAW4_TERMINAL_REGISTRY_KIND_FAIL",
                ordinal,
            )
            registry_kinds[kind] += 1
        require(len(set(registry_ids)) == len(registry_ids), "RAW4_TERMINAL_REGISTRY_DUPLICATE_ID")
        require(sha_object(sorted(registry_ids)) == terminal_registry.get("class_id_hash_root"), "RAW4_TERMINAL_REGISTRY_ID_ROOT_FAIL")
        require(terminal_registry.get("class_id_hash_root") == classes["terminal_class_ids_sha256"], "RAW4_TERMINAL_REGISTRY_CLASS_LEDGER_BINDING_FAIL")
        require(
            registry_kinds
            == {
                "exact_multihomogeneous_quadratic": 839,
                "exact_direct_polynomial_separator": 36,
                "ordinary_triangle_quotient": 35,
                "exact_mixed_graph_isomorphism": 20,
                "direct_hard_case_F2_F3_F4": 4,
            },
            "RAW4_TERMINAL_REGISTRY_KIND_CENSUS_FAIL",
        )
        direct_rows = expected_categories["direct_terminal_presentation"]
        restoration_rows = expected_categories["restoration_member_presentation"]
        terminal = summary.get("terminal_class_bindings")
        require(isinstance(terminal, dict), "RAW4_COMPOSITE_TERMINAL_CLASS_BINDING_FAIL")
        require(terminal.get("presentation_rows") == direct_rows, "RAW4_COMPOSITE_TERMINAL_PRESENTATION_FAIL")
        require(terminal.get("rows_with_terminal_certificate") == direct_rows, "RAW4_COMPOSITE_TERMINAL_CERTIFICATE_COVERAGE_FAIL")
        require(terminal.get("distinct_class_count") == classes["terminal_class_count"], "RAW4_COMPOSITE_TERMINAL_CLASS_COUNT_FAIL")
        require(terminal.get("class_multiplicity_histogram") == classes["terminal_multiplicity_histogram"], "RAW4_COMPOSITE_TERMINAL_MULTIPLICITY_FAIL")
        require(terminal.get("class_id_hash_root") == classes["terminal_class_ids_sha256"], "RAW4_COMPOSITE_TERMINAL_CLASS_ROOT_FAIL")
        require(terminal.get("class_id_hash_root") == terminal_registry.get("class_id_hash_root"), "RAW4_COMPOSITE_TERMINAL_REGISTRY_ROOT_FAIL")
        require(is_sha256(terminal.get("presentation_membership_hash_root")), "RAW4_COMPOSITE_TERMINAL_MEMBERSHIP_ROOT_FAIL")
        for field in ("missing_class_links", "multiple_class_links", "unresolved"):
            require(terminal.get(field) == 0, "RAW4_COMPOSITE_TERMINAL_ZERO_GATE_FAIL", field)
        restoration = summary.get("restoration_member_bindings")
        require(isinstance(restoration, dict), "RAW4_COMPOSITE_RESTORATION_BINDING_FAIL")
        for field in ("presentation_rows", "rows_with_exactly_one_parent", "rows_with_transport_binding"):
            require(restoration.get(field) == restoration_rows, "RAW4_COMPOSITE_RESTORATION_COVERAGE_FAIL", field)
        parent_count = restoration.get("distinct_parent_count")
        require(parent_count == classes["parent_count"], "RAW4_COMPOSITE_PARENT_COUNT_FAIL")
        require(restoration.get("parent_multiplicity_histogram") == classes["parent_multiplicity_histogram"], "RAW4_COMPOSITE_PARENT_MULTIPLICITY_FAIL")
        for field in ("missing_parent_links", "multiple_parent_links", "unresolved"):
            require(restoration.get(field) == 0, "RAW4_COMPOSITE_RESTORATION_ZERO_GATE_FAIL", field)
        require(restoration.get("parent_id_hash_root") == classes["parent_ids_sha256"], "RAW4_COMPOSITE_PARENT_ROOT_FAIL")
        require(is_sha256(restoration.get("presentation_membership_hash_root")), "RAW4_COMPOSITE_PARENT_MEMBERSHIP_ROOT_FAIL")
        result["terminal_class_count"] = classes["terminal_class_count"]
        result["terminal_registry_payload_sha256"] = terminal_registry["payload_sha256"]
        result["terminal_class_multiplicity_histogram"] = classes["terminal_multiplicity_histogram"]
        result["restoration_parent_count"] = parent_count
        result["restoration_parent_multiplicity_histogram"] = classes["parent_multiplicity_histogram"]
        result["restoration_parent_id_hash_root"] = restoration["parent_id_hash_root"]
        result["restoration_member_presentation_count"] = restoration_rows
        result["restoration_member_membership_hash_root"] = restoration["presentation_membership_hash_root"]
    else:
        direct_rows = (
            expected_categories["direct_quadratic_separator"]
            + expected_categories["labelled_isomorphism"]
        )
        require(summary.get("direct_certificate_rows") == direct_rows, "THETA2_COMPOSITE_DIRECT_BINDING_FAIL")
        descendants = summary.get("restoration_descendants")
        require(isinstance(descendants, dict), "THETA2_COMPOSITE_DESCENDANT_RECORD_FAIL")
        roots = descendants.get("root_count")
        children = descendants.get("generated_child_count")
        require(isinstance(roots, int) and roots > 0, "THETA2_COMPOSITE_DESCENDANT_ROOT_COUNT_FAIL")
        require(isinstance(children, int) and children > 0, "THETA2_COMPOSITE_DESCENDANT_CHILD_COUNT_FAIL")
        require(descendants.get("covered_root_count") == roots, "THETA2_COMPOSITE_DESCENDANT_ROOT_COVERAGE_FAIL")
        require(descendants.get("distinct_child_ids") == children, "THETA2_COMPOSITE_DESCENDANT_DISTINCT_FAIL")
        require(descendants.get("children_with_exactly_one_parent") == children, "THETA2_COMPOSITE_DESCENDANT_PARENT_COVERAGE_FAIL")
        edge_count = descendants.get("edge_count")
        require(edge_count == children, "THETA2_COMPOSITE_DESCENDANT_EDGE_COUNT_FAIL")
        require(descendants.get("transport_restrictions_replayed") == edge_count, "THETA2_COMPOSITE_DESCENDANT_TRANSPORT_FAIL")
        for field in (
            "duplicate_child_ids",
            "missing_parent_links",
            "multiple_parent_links",
            "missing_continuation_layers",
            "cycles",
            "unresolved",
        ):
            require(descendants.get(field) == 0, "THETA2_COMPOSITE_DESCENDANT_ZERO_GATE_FAIL", field)
        leaves = descendants.get("leaf_category_counts")
        require(
            isinstance(leaves, dict)
            and set(leaves) <= {"displayed_quartet_exclusion", "labelled_isomorphism"}
            and all(isinstance(value, int) and value >= 0 for value in leaves.values())
            and sum(leaves.values()) == descendants.get("leaf_count"),
            "THETA2_COMPOSITE_DESCENDANT_LEAF_PARTITION_FAIL",
        )
        for field in (
            "child_id_hash_root",
            "parent_child_edge_hash_root",
            "transport_restriction_hash_root",
        ):
            require(is_sha256(descendants.get(field)), "THETA2_COMPOSITE_DESCENDANT_ROOT_FAIL", field)
        result["restoration_descendant_roots"] = roots
        result["restoration_descendant_children"] = children
        result["restoration_descendant_edges"] = edge_count
        result["restoration_descendant_child_id_hash_root"] = descendants["child_id_hash_root"]
        result["restoration_descendant_edge_hash_root"] = descendants["parent_child_edge_hash_root"]
        result["restoration_descendant_transport_hash_root"] = descendants["transport_restriction_hash_root"]

    replay = load_json(located["replay"])
    verify_payload_hash(replay)
    require(
        replay.get("schema") == f"k2p-{family}-corrected-composite-independent-replay-v1",
        "COMPOSITE_REPLAY_SCHEMA_FAIL",
        family,
    )
    require(replay.get("status") == "PASS", "COMPOSITE_REPLAY_NOT_PASS", family)
    require(replay.get("summary_sha256") == sha_file(located["summary"]), "COMPOSITE_REPLAY_SUMMARY_BINDING_FAIL", family)
    require(replay.get("source_ledger_sha256") == sha_file(located["ledger"]), "COMPOSITE_REPLAY_SOURCE_BINDING_FAIL", family)
    require(replay.get("regenerated_ledger_sha256") == sha_file(located["ledger"]), "COMPOSITE_REPLAY_BYTE_MISMATCH", family)
    require(replay.get("total_rows") == total, "COMPOSITE_REPLAY_TOTAL_FAIL", family)
    require(replay.get("distinct_raw_ids") == total, "COMPOSITE_REPLAY_DISTINCT_FAIL", family)
    require(replay.get("category_counts") == expected_categories, "COMPOSITE_REPLAY_CATEGORY_FAIL", family)
    require(replay.get("ordered_row_hash_root") == summary["ordered_row_hash_root"], "COMPOSITE_REPLAY_ROW_ROOT_FAIL", family)
    for field in (
        "primitive_graph_generation_replayed",
        "source_target_permutations_replayed",
        "classification_evidence_replayed",
        "canonical_serialization_replayed",
    ):
        require(replay.get(field) is True, "COMPOSITE_REPLAY_LAYER_FAIL", f"{family}:{field}")
    for field in (
        "duplicate_raw_ids",
        "missing_raw_ids",
        "unresolved",
        "forbidden_rooted_field_count",
        "forbidden_rooted_reason_count",
        "source_tree_drift",
    ):
        require(replay.get(field) == 0, "COMPOSITE_REPLAY_ZERO_GATE_FAIL", f"{family}:{field}")

    mutations = load_json(located["mutation"])
    verify_payload_hash(mutations)
    require(
        mutations.get("schema") == f"k2p-{family}-corrected-composite-mutations-v1",
        "COMPOSITE_MUTATION_SCHEMA_FAIL",
        family,
    )
    require(mutations.get("status") == "PASS", "COMPOSITE_MUTATIONS_NOT_PASS", family)
    require(mutations.get("summary_sha256") == sha_file(located["summary"]), "COMPOSITE_MUTATION_SUMMARY_BINDING_FAIL", family)
    require(mutations.get("source_ledger_sha256") == sha_file(located["ledger"]), "COMPOSITE_MUTATION_LEDGER_BINDING_FAIL", family)
    require(mutations.get("source_tree_drift") == 0, "COMPOSITE_MUTATION_SOURCE_DRIFT", family)
    require(mutations.get("temporary_copies_only") is True, "COMPOSITE_MUTATION_TEMP_COPY_FAIL", family)
    require(mutations.get("survivors") == 0, "COMPOSITE_MUTATION_SURVIVOR", family)
    mutation_rows = mutations.get("tests")
    require(
        isinstance(mutation_rows, list)
        and len(mutation_rows) == mutations.get("test_count")
        and all(isinstance(row, dict) and row.get("rejected") is True for row in mutation_rows),
        "COMPOSITE_MUTATION_ROW_CENSUS_FAIL",
        family,
    )
    tests = {
        row.get("name") if isinstance(row, dict) else row
        for row in mutations.get("tests", [])
    }
    required_tests = {
        "omitted_raw_row",
        "duplicate_raw_id",
        "wrong_port_permutation",
        "reassigned_category",
        "reassigned_evidence_binding",
        "false_rank_exclusion",
        "rooted_restriction_reintroduction",
        "python_optimized_mode",
        "source_tree_write",
    }
    if family == "raw4":
        required_tests.update({
            "wrong_restoration_parent",
            "broken_transport",
            "reassigned_cubic_certificate",
            "reassigned_quartic_certificate",
            "reassigned_quintic_certificate",
        })
    else:
        required_tests.update({
            "missing_restoration_child",
            "broken_transport",
            "reassigned_quadratic_certificate",
        })
    require(required_tests <= tests, "COMPOSITE_MUTATION_COVERAGE_FAIL", f"{family}:{sorted(required_tests - tests)}")
    require(mutations.get("survivors") == 0, "COMPOSITE_MUTATION_SURVIVOR", family)
    require(mutations.get("source_tree_drift") == 0, "COMPOSITE_MUTATION_SOURCE_DRIFT", family)
    result["independent_replay_payload_sha256"] = replay["payload_sha256"]
    result["mutation_payload_sha256"] = mutations["payload_sha256"]
    return result


def validate_corrected_composite_release_package(
    paths: dict[str, Path],
    raw4: dict[str, Any],
    theta2: dict[str, Any],
) -> dict[str, Any]:
    """Bind the frozen package manifest and its contract-snapshot replay."""

    required = {
        "corrected_composite_generator",
        "corrected_composite_support",
        "corrected_composite_independent_verifier",
        "corrected_composite_mutation_runner",
        "raw4_terminal_registry_builder",
        "raw4_terminal_certificate_registry",
        "raw4_corrected_composite_ledger",
        "raw4_corrected_composite_summary",
        "raw4_corrected_composite_replay",
        "raw4_corrected_composite_mutation_report",
        "theta2_corrected_composite_ledger",
        "theta2_corrected_composite_summary",
        "theta2_corrected_composite_replay",
        "theta2_corrected_composite_mutation_report",
        "corrected_composite_release_contract_validator",
        "corrected_composite_release_contract_replay",
        "corrected_composite_readme",
        "corrected_composite_research_log",
        "corrected_composite_sha256sums",
    }
    require(required <= set(paths), "COMPOSITE_RELEASE_ROLE_MISSING", sorted(required - set(paths)))
    report = load_json(paths["corrected_composite_release_contract_replay"])
    verify_payload_hash(report)
    require(
        report.get("schema")
        == "k2p-corrected-composites-release-contract-replay-v1",
        "COMPOSITE_RELEASE_REPLAY_SCHEMA_FAIL",
    )
    require(report.get("status") == "PASS", "COMPOSITE_RELEASE_REPLAY_NOT_PASS")
    require(report.get("unresolved") == 0, "COMPOSITE_RELEASE_REPLAY_UNRESOLVED")
    require(
        report.get("validator_sha256")
        == sha_file(paths["corrected_composite_release_contract_validator"]),
        "COMPOSITE_RELEASE_VALIDATOR_BINDING_FAIL",
    )
    require(
        is_sha256(report.get("release_common_sha256")),
        "COMPOSITE_RELEASE_CONTRACT_SNAPSHOT_HASH_FAIL",
    )
    for family, live in (("raw4", raw4), ("theta2", theta2)):
        frozen = report.get(family)
        require(isinstance(frozen, dict), "COMPOSITE_RELEASE_FAMILY_RECORD_FAIL", family)
        for field, value in frozen.items():
            require(live.get(field) == value, "COMPOSITE_RELEASE_LIVE_CONTRACT_DRIFT", f"{family}:{field}")

    manifest_path = paths["corrected_composite_sha256sums"]
    package_root = paths["corrected_composite_readme"].parent
    manifest_entries: dict[str, str] = {}
    for line_number, line in enumerate(
        manifest_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        pieces = line.split("  ", 1)
        require(len(pieces) == 2, "COMPOSITE_RELEASE_MANIFEST_LINE_FAIL", line_number)
        digest, relative = pieces
        require(is_sha256(digest), "COMPOSITE_RELEASE_MANIFEST_HASH_FAIL", line_number)
        safe_relative(relative)
        require(relative not in manifest_entries, "COMPOSITE_RELEASE_MANIFEST_DUPLICATE", relative)
        manifest_entries[relative] = digest
    manifest_roles = required - {"corrected_composite_sha256sums"}
    expected_relatives = {
        paths[role].relative_to(package_root).as_posix()
        for role in manifest_roles
    }
    require(set(manifest_entries) == expected_relatives, "COMPOSITE_RELEASE_MANIFEST_FILE_SET_FAIL")
    for relative, digest in manifest_entries.items():
        require(sha_file(package_root / relative) == digest, "COMPOSITE_RELEASE_MANIFEST_FILE_HASH_FAIL", relative)
    return {
        "status": "PASS",
        "payload_sha256": report["payload_sha256"],
        "contract_snapshot_release_common_sha256": report["release_common_sha256"],
        "validator_sha256": report["validator_sha256"],
        "manifest_sha256": sha_file(manifest_path),
        "manifest_entries": len(manifest_entries),
    }


def validate_cycle_promotion_package(paths: dict[str, Path]) -> dict[str, Any]:
    """Validate the clean authoritative cycle base/full promotion package."""

    required = {
        "cycle_promotion_builder",
        "cycle_promotion_certificate",
        "cycle_base_authoritative_ledger",
        "cycle_full_authoritative_ledger",
        "cycle_promotion_verifier",
        "cycle_promotion_replay",
        "cycle_whole_map_auditor",
        "cycle_whole_map_truth_certificate",
        "cycle_whole_map_independent_verifier",
        "cycle_whole_map_replay",
        "cycle_mutation_runner",
        "cycle_mutation_report",
    }
    require(required <= set(paths), "CYCLE_PROMOTION_ROLE_MISSING", sorted(required - set(paths)))
    summary_path = paths["cycle_promotion_certificate"]
    summary = load_json(summary_path)
    verify_payload_hash(summary)
    require(summary.get("schema") == "k2p-cycle-three-port-authoritative-promotion-v1", "CYCLE_PROMOTION_SCHEMA_FAIL")
    require(summary.get("status") == "PASS", "CYCLE_PROMOTION_NOT_PASS")
    for field in ("unresolved", "incoherent", "legacy_rooted_reason_or_type_fields"):
        require(summary.get(field) == 0, "CYCLE_PROMOTION_ZERO_GATE_FAIL", field)
    base = summary.get("base")
    full = summary.get("full")
    require(isinstance(base, dict) and isinstance(full, dict), "CYCLE_PROMOTION_PARTITION_RECORD_FAIL")
    require(base.get("rows") == CYCLE_BASE_TOTAL, "CYCLE_PROMOTION_BASE_TOTAL_FAIL")
    require(base.get("terminal_census") == CYCLE_BASE_CATEGORY_COUNTS, "CYCLE_PROMOTION_BASE_CENSUS_FAIL")
    require(full.get("rows") == CYCLE_FULL_TOTAL, "CYCLE_PROMOTION_FULL_TOTAL_FAIL")
    require(full.get("terminal_census") == CYCLE_FULL_CATEGORY_COUNTS, "CYCLE_PROMOTION_FULL_CENSUS_FAIL")
    require(full.get("unresolved") == 0, "CYCLE_PROMOTION_FULL_UNRESOLVED")
    for record, label in ((base, "base"), (full, "full")):
        require(is_sha256(record.get("ordered_authoritative_row_hash_root")), "CYCLE_PROMOTION_ROW_ROOT_FAIL", label)
    restoration = summary.get("fixed_full_restoration")
    require(isinstance(restoration, dict), "CYCLE_PROMOTION_RESTORATION_RECORD_FAIL")
    require(restoration.get("roots") == CYCLE_BASE_CATEGORY_COUNTS["fixed_full_restoration_obligation"], "CYCLE_PROMOTION_ROOT_CENSUS_FAIL")
    require(restoration.get("children") == CYCLE_FULL_TOTAL, "CYCLE_PROMOTION_CHILD_CENSUS_FAIL")
    require(restoration.get("roots_with_zero_children") == 0, "CYCLE_PROMOTION_EMPTY_ROOT")
    require(is_sha256(restoration.get("ordered_child_transport_hash_root")), "CYCLE_PROMOTION_TRANSPORT_ROOT_FAIL")
    outputs = summary.get("outputs")
    require(isinstance(outputs, dict), "CYCLE_PROMOTION_OUTPUT_BINDING_FAIL")
    expected_outputs = {
        "cycle_base_authoritative.jsonl.gz": (
            CYCLE_BASE_TOTAL,
            sha_file(paths["cycle_base_authoritative_ledger"]),
        ),
        "cycle_full_authoritative.jsonl.gz": (
            CYCLE_FULL_TOTAL,
            sha_file(paths["cycle_full_authoritative_ledger"]),
        ),
    }
    for name, (rows, digest) in expected_outputs.items():
        require(outputs.get(name) == {"rows": rows, "sha256": digest}, "CYCLE_PROMOTION_OUTPUT_FAIL", name)

    truth_path = paths["cycle_whole_map_truth_certificate"]
    truth = load_json(truth_path)
    verify_payload_hash(truth)
    require(truth.get("schema") == "k2p-cycle-tree-sunlet-whole-map-truth-v1", "CYCLE_TRUTH_SCHEMA_FAIL")
    require(truth.get("status") == "PASS", "CYCLE_TRUTH_NOT_PASS")
    for field in ("false_topology_oracle_count", "incoherent", "unresolved"):
        require(truth.get(field) == 0, "CYCLE_TRUTH_ZERO_GATE_FAIL", field)
    require(truth.get("reopened_obligations") == [], "CYCLE_TRUTH_REOPENED_OBLIGATION")
    require(truth.get("revoked_legacy_witness_count") == 24, "CYCLE_TRUTH_REPAIR_CENSUS_FAIL")
    repairs = truth.get("revoked_legacy_witness_repairs")
    require(isinstance(repairs, list) and len(repairs) == 24, "CYCLE_TRUTH_REPAIR_ROWS_FAIL")
    require(len(truth.get("sign_certificates", {})) == 92, "CYCLE_TRUTH_SIGN_CLASS_FAIL")
    require(len(truth.get("coordinate_invariant_certificates", {})) == 12, "CYCLE_TRUTH_INVARIANT_CENSUS_FAIL")
    truth_families = truth.get("families")
    truth_expected = {
        "cycle_base": (7_452, 1, {"source": 7_452}),
        "cycle_full_equal_topology": (300, 91, {"target": 300}),
    }
    require(isinstance(truth_families, dict) and set(truth_families) == set(truth_expected), "CYCLE_TRUTH_FAMILY_SET_FAIL")
    for name, (rows, classes, sides) in truth_expected.items():
        row = truth_families[name]
        require(row.get("input_rows") == rows, "CYCLE_TRUTH_INPUT_CENSUS_FAIL", name)
        require(row.get("direct_full_map_zero_sign_rows") == rows, "CYCLE_TRUTH_CERTIFIED_CENSUS_FAIL", name)
        require(row.get("exact_full_graph_relation_census") == {"none": rows}, "CYCLE_TRUTH_RELATION_FAIL", name)
        require(row.get("false_iso_or_triangle_conflicts") == 0, "CYCLE_TRUTH_GRAPH_CONFLICT", name)
        require(row.get("reopened_obligations") == 0, "CYCLE_TRUTH_FAMILY_REOPENED", name)
        require(row.get("polynomial_relation_classes") == classes, "CYCLE_TRUTH_CLASS_CENSUS_FAIL", name)
        require(row.get("signed_side_census") == sides, "CYCLE_TRUTH_SIGNED_SIDE_FAIL", name)
        hashes = row.get("ordered_truth_row_hashes")
        require(isinstance(hashes, list) and len(hashes) == rows and all(is_sha256(item) for item in hashes), "CYCLE_TRUTH_ROW_HASHES_FAIL", name)
        require(sha_object(hashes) == row.get("ordered_truth_row_hash_root"), "CYCLE_TRUTH_ROW_ROOT_FAIL", name)
    inputs = summary.get("inputs")
    require(isinstance(inputs, dict), "CYCLE_PROMOTION_INPUTS_FAIL")
    require(inputs.get("whole_map_truth_file_sha256") == sha_file(truth_path), "CYCLE_PROMOTION_TRUTH_FILE_BINDING_FAIL")
    require(inputs.get("whole_map_truth_payload_sha256") == truth["payload_sha256"], "CYCLE_PROMOTION_TRUTH_PAYLOAD_BINDING_FAIL")

    truth_replay = load_json(paths["cycle_whole_map_replay"])
    verify_payload_hash(truth_replay)
    require(truth_replay.get("schema") == "k2p-cycle-whole-map-independent-replay-v1", "CYCLE_TRUTH_REPLAY_SCHEMA_FAIL")
    require(truth_replay.get("status") == "PASS", "CYCLE_TRUTH_REPLAY_NOT_PASS")
    require(truth_replay.get("source_certificate_sha256") == sha_file(truth_path), "CYCLE_TRUTH_REPLAY_FILE_BINDING_FAIL")
    require(truth_replay.get("source_certificate_payload_sha256") == truth["payload_sha256"], "CYCLE_TRUTH_REPLAY_PAYLOAD_BINDING_FAIL")
    require(truth_replay.get("base_rows_replayed") == 7_452, "CYCLE_TRUTH_REPLAY_BASE_FAIL")
    require(truth_replay.get("full_rows_replayed") == 300, "CYCLE_TRUTH_REPLAY_FULL_FAIL")
    require(truth_replay.get("legacy_witness_repairs_replayed") == 24, "CYCLE_TRUTH_REPLAY_REPAIRS_FAIL")
    require(truth_replay.get("sign_polynomials_replayed") == 92, "CYCLE_TRUTH_REPLAY_SIGNS_FAIL")
    require(truth_replay.get("bridge_multihomogeneous_invariants_replayed") == 12, "CYCLE_TRUTH_REPLAY_INVARIANTS_FAIL")
    for field in ("unresolved", "incoherent"):
        require(truth_replay.get(field) == 0, "CYCLE_TRUTH_REPLAY_ZERO_GATE_FAIL", field)

    promotion_replay = load_json(paths["cycle_promotion_replay"])
    verify_payload_hash(promotion_replay)
    require(
        promotion_replay.get("schema")
        == "k2p-cycle-authoritative-promotion-independent-verification-v1",
        "CYCLE_PROMOTION_REPLAY_SCHEMA_FAIL",
    )
    require(promotion_replay.get("status") == "PASS", "CYCLE_PROMOTION_REPLAY_NOT_PASS")
    require(promotion_replay.get("promotion_certificate_sha256") == sha_file(summary_path), "CYCLE_PROMOTION_REPLAY_FILE_BINDING_FAIL")
    require(promotion_replay.get("promotion_payload_sha256") == summary["payload_sha256"], "CYCLE_PROMOTION_REPLAY_PAYLOAD_BINDING_FAIL")
    require(promotion_replay.get("base_rows") == CYCLE_BASE_TOTAL, "CYCLE_PROMOTION_REPLAY_BASE_FAIL")
    require(promotion_replay.get("restoration_roots") == restoration["roots"], "CYCLE_PROMOTION_REPLAY_ROOTS_FAIL")
    require(promotion_replay.get("full_children") == CYCLE_FULL_TOTAL, "CYCLE_PROMOTION_REPLAY_CHILDREN_FAIL")
    for field in ("legacy_rooted_fields_or_reasons", "unresolved", "incoherent"):
        require(promotion_replay.get(field) == 0, "CYCLE_PROMOTION_REPLAY_ZERO_GATE_FAIL", field)

    mutations = load_json(paths["cycle_mutation_report"])
    verify_payload_hash(mutations)
    require(mutations.get("schema") == "k2p-cycle-authoritative-promotion-mutations-v1", "CYCLE_MUTATION_SCHEMA_FAIL")
    require(mutations.get("status") == "PASS", "CYCLE_MUTATIONS_NOT_PASS")
    require(mutations.get("source_promotion_certificate_sha256") == sha_file(summary_path), "CYCLE_MUTATION_PROMOTION_BINDING_FAIL")
    require(mutations.get("source_truth_certificate_sha256") == sha_file(truth_path), "CYCLE_MUTATION_TRUTH_BINDING_FAIL")
    results = mutations.get("results")
    require(isinstance(results, list) and len(results) == mutations.get("mutation_count") == 12, "CYCLE_MUTATION_CENSUS_FAIL")
    require(mutations.get("survived") == 0 and all(row.get("rejected") is True for row in results), "CYCLE_MUTATION_SURVIVOR")
    required_mutations = {
        "omitted_base_raw_record",
        "omitted_dummy_role",
        "wrong_source_placement",
        "quadratic_certificate_reassigned",
        "broken_fixed_full_transport",
        "reassigned_full_map_truth_row",
        "legacy_rooted_reason_reintroduction",
        "legacy_single_triple_reintroduction",
        "omitted_truth_row_hash",
        "sign_polynomial_reassigned",
        "broken_bridge_multihomogeneity",
        "python_optimized_mode",
    }
    require({row.get("mutation") for row in results} == required_mutations, "CYCLE_MUTATION_COVERAGE_FAIL")
    return {
        "status": "PASS",
        "promotion_payload_sha256": summary["payload_sha256"],
        "whole_map_truth_payload_sha256": truth["payload_sha256"],
        "whole_map_replay_payload_sha256": truth_replay["payload_sha256"],
        "promotion_replay_payload_sha256": promotion_replay["payload_sha256"],
        "mutation_payload_sha256": mutations["payload_sha256"],
        "base_rows": CYCLE_BASE_TOTAL,
        "base_category_counts": CYCLE_BASE_CATEGORY_COUNTS,
        "base_row_hash_root": base["ordered_authoritative_row_hash_root"],
        "restoration_roots": restoration["roots"],
        "full_children": CYCLE_FULL_TOTAL,
        "full_category_counts": CYCLE_FULL_CATEGORY_COUNTS,
        "full_row_hash_root": full["ordered_authoritative_row_hash_root"],
        "child_transport_hash_root": restoration["ordered_child_transport_hash_root"],
    }


def validate_probe_input_package(paths: dict[str, Path]) -> dict[str, Any]:
    """Validate probe-input v2 without treating it as probe closure."""

    required = {
        "probe_input_builder",
        "probe_input_contract",
        "probe_input_primary_verifier",
        "probe_input_structural_verifier",
        "probe_input_replay",
        "probe_input_mutation_runner",
        "probe_input_mutation_report",
        "probe_input_contract_document",
        "cycle_promotion_certificate",
    }
    require(required <= set(paths), "PROBE_INPUT_ROLE_MISSING", sorted(required - set(paths)))
    contract_path = paths["probe_input_contract"]
    contract = load_json(contract_path)
    verify_payload_hash(contract)
    require(contract.get("schema") == "k2p-root-invariant-probe-input-contract-v2", "PROBE_INPUT_SCHEMA_FAIL")
    require(contract.get("status") == "PASS", "PROBE_INPUT_NOT_PASS")
    require(contract.get("unresolved_anchor_inputs") == 0, "PROBE_INPUT_UNRESOLVED")
    require(contract.get("incoherent_site_transports") == 0, "PROBE_INPUT_INCOHERENT")
    require(
        "does not classify the ensuing one-/two-port cross-products"
        in contract.get("claim_boundary", ""),
        "PROBE_INPUT_CLAIM_BOUNDARY_FAIL",
    )
    census = contract.get("anchor_census")
    require(isinstance(census, dict), "PROBE_INPUT_ANCHOR_CENSUS_FAIL")
    require(census.get("physical_equality_anchor_records") == PROBE_INPUT_ANCHORS, "PROBE_INPUT_ANCHOR_COUNT_FAIL")
    require(census.get("unique_anchor_record_ids") == PROBE_INPUT_ANCHORS, "PROBE_INPUT_UNIQUE_ANCHOR_FAIL")
    expected_relations = {"isomorphic": 143, "triangle": 33}
    expected_ports = {"3": 25, "4": 38, "5": 41, "6": 40, "7": 32}
    expected_origins = {
        "cycle_physical_k3": 24,
        "cycle_restored_physical_k4": 12,
        "four_port_direct_physical": 26,
        "four_port_restored_physical_k5": 17,
        "theta2_physical_k5": 24,
        "theta2_physical_k6": 40,
        "theta2_physical_k7": 32,
        "tree_physical_k3": 1,
    }
    require(census.get("by_relation") == expected_relations, "PROBE_INPUT_RELATION_CENSUS_FAIL")
    require(census.get("by_port_count") == expected_ports, "PROBE_INPUT_PORT_CENSUS_FAIL")
    require(census.get("by_origin") == expected_origins, "PROBE_INPUT_ORIGIN_CENSUS_FAIL")
    candidates = contract.get("candidate_census")
    require(isinstance(candidates, dict), "PROBE_INPUT_CANDIDATE_CENSUS_FAIL")
    require(candidates.get("source_sites") == PROBE_INPUT_SITES_PER_SIDE, "PROBE_INPUT_SOURCE_SITE_CENSUS_FAIL")
    require(candidates.get("target_sites") == PROBE_INPUT_SITES_PER_SIDE, "PROBE_INPUT_TARGET_SITE_CENSUS_FAIL")
    require(candidates.get("first_probe_source_target_pairs") == PROBE_INPUT_FIRST_PAIRS, "PROBE_INPUT_PAIR_CENSUS_FAIL")
    require(candidates.get("per_graph_formula") == "site_count = 2*k + 3*r - 3", "PROBE_INPUT_SITE_FORMULA_FAIL")
    for field in (
        "all_suppressed_semi_directed_edges_included",
        "artificial_root_two_halves_quotiented",
        "pendant_arm_edges_included",
        "reticulation_incoming_edges_included",
    ):
        require(candidates.get(field) is True, "PROBE_INPUT_SITE_COMPLETENESS_FAIL", field)
    anchors = contract.get("anchors")
    hashes = contract.get("ordered_anchor_row_hashes")
    require(isinstance(anchors, list) and isinstance(hashes, list) and len(anchors) == len(hashes) == PROBE_INPUT_ANCHORS, "PROBE_INPUT_ANCHOR_ROWS_FAIL")
    anchor_ids: list[str] = []
    observed_hashes: list[str] = []
    for ordinal, row in enumerate(anchors):
        require(isinstance(row, dict), "PROBE_INPUT_ANCHOR_ROW_FAIL", ordinal)
        anchor_id = row.get("anchor_id")
        require(isinstance(anchor_id, str) and anchor_id, "PROBE_INPUT_ANCHOR_ID_FAIL", ordinal)
        anchor_ids.append(anchor_id)
        digest = row.get("anchor_row_sha256")
        require(is_sha256(digest), "PROBE_INPUT_ANCHOR_ROW_DIGEST_FAIL", ordinal)
        require(
            sha_object({key: value for key, value in row.items() if key != "anchor_row_sha256"})
            == digest,
            "PROBE_INPUT_ANCHOR_ROW_HASH_FAIL",
            ordinal,
        )
        observed_hashes.append(digest)
        labels = row.get("labels")
        require(isinstance(labels, list), "PROBE_INPUT_LABELS_FAIL", ordinal)
        for side in ("source_candidate_profile", "target_candidate_profile"):
            profile = row.get(side)
            require(isinstance(profile, dict), "PROBE_INPUT_PROFILE_FAIL", f"{ordinal}:{side}")
            k = profile.get("port_count")
            reticulations = profile.get("reticulation_count")
            require(
                isinstance(k, int)
                and k >= 3
                and isinstance(reticulations, int)
                and reticulations >= 0,
                "PROBE_INPUT_ROW_PROFILE_COUNT_FAIL",
                f"{ordinal}:{side}",
            )
            require(profile.get("site_count") == 2 * k + 3 * reticulations - 3, "PROBE_INPUT_ROW_SITE_FORMULA_FAIL", f"{ordinal}:{side}")
            require(profile.get("all_mixed_edge_sites_included") is True, "PROBE_INPUT_ROW_SITE_COVERAGE_FAIL", f"{ordinal}:{side}")
    require(len(set(anchor_ids)) == PROBE_INPUT_ANCHORS, "PROBE_INPUT_DUPLICATE_ANCHOR_ID")
    require(observed_hashes == hashes, "PROBE_INPUT_ORDERED_ROW_HASHES_FAIL")
    require(sha_object(hashes) == contract.get("ordered_anchor_hash_root"), "PROBE_INPUT_ORDERED_ROOT_FAIL")
    movement = contract.get("root_movement_contract")
    require(isinstance(movement, dict), "PROBE_INPUT_ROOT_MOVEMENT_RECORD_FAIL")
    require(movement.get("every_anchor_half_equivalences_certified") == 2 * PROBE_INPUT_ANCHORS, "PROBE_INPUT_ROOT_HALF_CENSUS_FAIL")
    require(movement.get("labelled_boundary_transport_compatible") is True, "PROBE_INPUT_ROOT_TRANSPORT_FAIL")
    require(movement.get("parent_transport_maps_every_source_site_bijectively_to_a_target_site") is True, "PROBE_INPUT_PARENT_SITE_BIJECTION_FAIL")
    inputs = contract.get("inputs")
    require(isinstance(inputs, dict), "PROBE_INPUT_INPUT_BINDINGS_FAIL")
    require(inputs.get("cycle_promotion_certificate_sha256") == sha_file(paths["cycle_promotion_certificate"]), "PROBE_INPUT_CYCLE_PROMOTION_BINDING_FAIL")

    replay = load_json(paths["probe_input_replay"])
    verify_payload_hash(replay)
    require(replay.get("schema") == "k2p-probe-input-independent-replay-v1", "PROBE_INPUT_REPLAY_SCHEMA_FAIL")
    require(replay.get("status") == "PASS", "PROBE_INPUT_REPLAY_NOT_PASS")
    require(replay.get("contract_sha256") == sha_file(contract_path), "PROBE_INPUT_REPLAY_FILE_BINDING_FAIL")
    require(replay.get("contract_payload_sha256") == contract["payload_sha256"], "PROBE_INPUT_REPLAY_PAYLOAD_BINDING_FAIL")
    require(replay.get("anchors_reconstructed") == PROBE_INPUT_ANCHORS, "PROBE_INPUT_REPLAY_ANCHOR_FAIL")
    require(replay.get("exact_relations_replayed") == PROBE_INPUT_ANCHORS, "PROBE_INPUT_REPLAY_RELATION_FAIL")
    require(replay.get("source_sites_reenumerated") == PROBE_INPUT_SITES_PER_SIDE, "PROBE_INPUT_REPLAY_SOURCE_SITES_FAIL")
    require(replay.get("target_sites_reenumerated") == PROBE_INPUT_SITES_PER_SIDE, "PROBE_INPUT_REPLAY_TARGET_SITES_FAIL")
    require(replay.get("first_probe_source_target_pairs") == PROBE_INPUT_FIRST_PAIRS, "PROBE_INPUT_REPLAY_PAIRS_FAIL")
    require(replay.get("root_half_equivalences_replayed") == 2 * PROBE_INPUT_ANCHORS, "PROBE_INPUT_REPLAY_ROOT_HALF_FAIL")
    require(replay.get("origin_census") == expected_origins, "PROBE_INPUT_REPLAY_ORIGIN_FAIL")
    require(replay.get("port_census") == expected_ports, "PROBE_INPUT_REPLAY_PORT_FAIL")
    require(replay.get("relation_census") == expected_relations, "PROBE_INPUT_REPLAY_RELATION_CENSUS_FAIL")
    for field in ("missing_anchors", "extra_anchors", "unresolved"):
        require(replay.get(field) == 0, "PROBE_INPUT_REPLAY_ZERO_GATE_FAIL", field)

    mutations = load_json(paths["probe_input_mutation_report"])
    verify_payload_hash(mutations)
    require(mutations.get("schema") == "k2p-probe-input-mutation-certificate-v1", "PROBE_INPUT_MUTATION_SCHEMA_FAIL")
    require(mutations.get("status") == "PASS", "PROBE_INPUT_MUTATIONS_NOT_PASS")
    require(mutations.get("contract_sha256") == sha_file(contract_path), "PROBE_INPUT_MUTATION_FILE_BINDING_FAIL")
    require(mutations.get("contract_payload_sha256") == contract["payload_sha256"], "PROBE_INPUT_MUTATION_PAYLOAD_BINDING_FAIL")
    require(mutations.get("adversarial_mutations") == mutations.get("mutations_rejected") == 20, "PROBE_INPUT_MUTATION_CENSUS_FAIL")
    require(mutations.get("mutation_survivors") == 0, "PROBE_INPUT_MUTATION_SURVIVOR")
    require(mutations.get("optimized_mode_pass") is True, "PROBE_INPUT_OPTIMIZED_POSITIVE_GATE_FAIL")
    results = mutations.get("results")
    require(isinstance(results, list) and len(results) == 21, "PROBE_INPUT_MUTATION_ROWS_FAIL")
    negative = [row for row in results if row.get("mutation") != "optimized_mode_original_contract"]
    positive = [row for row in results if row.get("mutation") == "optimized_mode_original_contract"]
    require(len(negative) == 20 and all(row.get("rejected") is True for row in negative), "PROBE_INPUT_MUTATION_NEGATIVE_GATE_FAIL")
    require(len(positive) == 1 and positive[0].get("passed") is True and positive[0].get("returncode") == 0, "PROBE_INPUT_MUTATION_OPTIMIZED_GATE_FAIL")
    required_mutations = {
        "omitted_anchor_record",
        "old_172_anchor_count_reintroduction",
        "duplicate_replacing_new_triangle_anchor",
        "raw67161_locator_reassignment",
        "collapse_two_k7_path_ids_sharing_topology_id",
        "omitted_pendant_arm",
        "omitted_reticulation_incoming",
        "dropped_root_suppressed_segment",
        "split_artificial_root_halves",
        "wrong_root_half_equivalence",
        "wrong_site_transport",
        "corrupt_anchor_parent_transport",
        "wrong_site_formula",
        "topology_first_classifier_reintroduction",
        "triple_type_gate_reintroduction",
        "forbidden_rooted_restriction_removed",
        "raw4424_false_tree_sunlet_reintroduction",
        "generic_rooted_restriction_reintroduction",
        "ordered_row_hash_omission",
        "upstream_input_binding_corruption",
        "optimized_mode_original_contract",
    }
    require({row.get("mutation") for row in results} == required_mutations, "PROBE_INPUT_MUTATION_COVERAGE_FAIL")
    return {
        "status": "PASS_INPUT_ONLY",
        "claim_boundary": "FULL_PROBE_CLASSIFICATION_NOT_CLAIMED",
        "contract_payload_sha256": contract["payload_sha256"],
        "replay_payload_sha256": replay["payload_sha256"],
        "mutation_payload_sha256": mutations["payload_sha256"],
        "anchors": PROBE_INPUT_ANCHORS,
        "anchor_row_hash_root": contract["ordered_anchor_hash_root"],
        "source_sites": PROBE_INPUT_SITES_PER_SIDE,
        "target_sites": PROBE_INPUT_SITES_PER_SIDE,
        "first_probe_pairs": PROBE_INPUT_FIRST_PAIRS,
        "relation_census": expected_relations,
    }


def validate_corrected_probe_package(
    paths: dict[str, Path], probe_input: dict[str, Any]
) -> dict[str, Any]:
    """Validate the frozen corrected one-/two-port producer package.

    Operational runtimes are deliberately outside producer logical payloads;
    all mathematical fields and every located byte remain hash-bound.
    """

    required = {
        "probe_builder",
        "probe_certificate",
        "probe_primary_verifier",
        "probe_independent_verifier",
        "probe_replay_report",
        "probe_mutation_runner",
        "probe_mutation_report",
        "probe_one_port_ledger",
        "probe_two_port_parent_inventory",
        "probe_two_port_ledger",
        "probe_exact_transport_ledger",
        "probe_parent_restriction_ledger",
        "probe_separation_registry",
        "probe_site_partition_verifier",
        "probe_site_partition_report",
        "probe_proof_document",
        "probe_readme",
        "probe_research_log",
        "probe_manifest",
        "probe_adversarial_auditor",
        "probe_adversarial_certificate",
        "probe_adversarial_mutation_report",
        "probe_adversarial_anchor_replay",
        "probe_adversarial_upstream_replay",
    }
    require(required <= set(paths), "CORRECTED_PROBE_ROLE_MISSING", sorted(required - set(paths)))

    def verify_logical_payload(value: dict[str, Any], code: str) -> None:
        claimed = value.get("payload_sha256")
        require(is_sha256(claimed), f"{code}_PAYLOAD_FORMAT_FAIL")
        body = {
            key: item
            for key, item in value.items()
            if key not in {"payload_sha256", "operational"}
        }
        require(sha_object(body) == claimed, f"{code}_PAYLOAD_HASH_FAIL")

    certificate_path = paths["probe_certificate"]
    certificate = load_json(certificate_path)
    verify_logical_payload(certificate, "CORRECTED_PROBE")
    require(
        certificate.get("schema") == "k2p-corrected-coherent-probe-closure-v1",
        "CORRECTED_PROBE_SCHEMA_FAIL",
    )
    require(certificate.get("status") == "PASS", "CORRECTED_PROBE_NOT_PASS")
    require(
        certificate.get("forbidden_rooted_triple_oracle_used") is False,
        "CORRECTED_PROBE_ROOTED_ORACLE_USED",
    )
    require(
        certificate.get("classifier_order")
        == [
            "exact_labelled_isomorphism_or_ordinary_triangle",
            "displayed_quartet_mismatch",
            "direct_original_full_map_Ti_zero_versus_Bernstein_strict_sign",
            "unresolved_fatal",
        ],
        "CORRECTED_PROBE_CLASSIFIER_ORDER_FAIL",
    )
    claim_boundary = certificate.get("claim_boundary", "")
    require(
        isinstance(claim_boundary, str)
        and "No rooted triple restriction is consulted" in claim_boundary,
        "CORRECTED_PROBE_CLAIM_BOUNDARY_FAIL",
    )

    inputs = certificate.get("inputs")
    require(isinstance(inputs, dict), "CORRECTED_PROBE_INPUT_RECORD_FAIL")
    input_paths = {
        "atlas_sha256": PROJECT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py",
        "probe_input_contract_sha256": paths["probe_input_contract"],
        "probe_input_independent_replay_sha256": paths["probe_input_replay"],
        "probe_input_mutations_sha256": paths["probe_input_mutation_report"],
        "corrected_restoration_sha256": paths["restoration_v3_forest_certificate"],
        "raw4_ledger_sha256": PROJECT / "work/raw_ledger_audit/artifacts/raw_directional_ledger.jsonl.gz",
        "theta2_fixed_full_closure_sha256": PROJECT / "work/theta2_five_port_closure/artifacts/fixed_full_restoration_closure.json.gz",
        "cycle_physical_anchors_sha256": PROJECT / "work/cycle_three_port_closure/artifacts/physical_anchors.json",
        "cycle_promotion_sha256": paths["cycle_promotion_certificate"],
    }
    require(set(input_paths) <= set(inputs), "CORRECTED_PROBE_INPUT_SET_FAIL")
    for field, path in input_paths.items():
        require(path.is_file(), "CORRECTED_PROBE_INPUT_FILE_MISSING", field)
        require(inputs.get(field) == sha_file(path), "CORRECTED_PROBE_INPUT_BINDING_FAIL", field)
    require(
        inputs.get("probe_input_contract_payload_sha256")
        == probe_input["contract_payload_sha256"],
        "CORRECTED_PROBE_INPUT_PAYLOAD_BINDING_FAIL",
    )

    anchors = certificate.get("anchor_inventory")
    require(isinstance(anchors, dict) and anchors.get("status") == "PASS", "CORRECTED_PROBE_ANCHOR_RECORD_FAIL")
    require(anchors.get("anchors") == PROBE_INPUT_ANCHORS, "CORRECTED_PROBE_ANCHOR_COUNT_FAIL")
    require(anchors.get("canonical_anchor_classes") == 39, "CORRECTED_PROBE_ANCHOR_CLASS_COUNT_FAIL")
    require(anchors.get("source_sites") == PROBE_INPUT_SITES_PER_SIDE, "CORRECTED_PROBE_SOURCE_SITE_COUNT_FAIL")
    require(anchors.get("target_sites") == PROBE_INPUT_SITES_PER_SIDE, "CORRECTED_PROBE_TARGET_SITE_COUNT_FAIL")
    require(anchors.get("first_pairs") == PROBE_INPUT_FIRST_PAIRS, "CORRECTED_PROBE_FIRST_PAIR_COUNT_FAIL")
    require(anchors.get("relation_counts") == {"isomorphic": 143, "triangle": 33}, "CORRECTED_PROBE_ANCHOR_RELATION_COUNT_FAIL")
    public_anchors = anchors.get("public_anchors")
    require(isinstance(public_anchors, list) and len(public_anchors) == PROBE_INPUT_ANCHORS, "CORRECTED_PROBE_ANCHOR_ROWS_FAIL")
    anchor_ids = [row.get("anchor_id") for row in public_anchors if isinstance(row, dict)]
    require(len(anchor_ids) == len(set(anchor_ids)) == PROBE_INPUT_ANCHORS, "CORRECTED_PROBE_ANCHOR_ID_FAIL")
    require(
        sha_object([sha_object(row) for row in public_anchors])
        == anchors.get("ordered_public_anchor_hash_root"),
        "CORRECTED_PROBE_ANCHOR_ROOT_FAIL",
    )
    class_coverage = anchors.get("canonical_class_coverage")
    require(isinstance(class_coverage, dict) and len(class_coverage) == 39, "CORRECTED_PROBE_ANCHOR_CLASS_COVERAGE_FAIL")
    covered_anchor_ids = [anchor_id for rows in class_coverage.values() for anchor_id in rows]
    require(sorted(covered_anchor_ids) == sorted(anchor_ids), "CORRECTED_PROBE_ANCHOR_CLASS_PARTITION_FAIL")

    ordered_algorithm = (
        "root_0=sha256(canonical([])); "
        "root_n=sha256(canonical({previous:root_(n-1),row_sha256:h_n}))"
    )

    def validate_stage(
        stage: str,
        expected_pairs: int,
        expected_counts: dict[str, int],
        expected_equalities: int,
        ledger_role: str,
    ) -> dict[str, Any]:
        row = certificate.get(stage)
        require(isinstance(row, dict), "CORRECTED_PROBE_STAGE_RECORD_FAIL", stage)
        require(row.get("raw_pairs") == expected_pairs, "CORRECTED_PROBE_STAGE_PAIR_COUNT_FAIL", stage)
        require(row.get("counts") == expected_counts, "CORRECTED_PROBE_STAGE_CATEGORY_COUNT_FAIL", stage)
        require(sum(expected_counts.values()) == expected_pairs, "CORRECTED_PROBE_STAGE_INTERNAL_CENSUS_FAIL", stage)
        require(row.get("equality_survivors") == expected_equalities, "CORRECTED_PROBE_STAGE_EQUALITY_COUNT_FAIL", stage)
        require(row.get("unresolved") == 0 and row.get("unresolved_examples") == [], "CORRECTED_PROBE_STAGE_UNRESOLVED", stage)
        require(row.get("ledger_sha256") == sha_file(paths[ledger_role]), "CORRECTED_PROBE_STAGE_LEDGER_BINDING_FAIL", stage)
        ordered = row.get("ordered_ledger")
        require(isinstance(ordered, dict), "CORRECTED_PROBE_STAGE_ORDERED_RECORD_FAIL", stage)
        require(ordered.get("algorithm") == ordered_algorithm, "CORRECTED_PROBE_STAGE_ORDER_ALGORITHM_FAIL", stage)
        require(ordered.get("rows") == expected_pairs, "CORRECTED_PROBE_STAGE_ORDER_ROW_COUNT_FAIL", stage)
        require(is_sha256(ordered.get("ordered_hash_root")), "CORRECTED_PROBE_STAGE_ORDER_ROOT_FAIL", stage)
        return {
            "raw_pairs": expected_pairs,
            "counts": expected_counts,
            "equality_survivors": expected_equalities,
            "ledger_sha256": row["ledger_sha256"],
            "ordered_row_hash_root": ordered["ordered_hash_root"],
        }

    one = validate_stage(
        "one_port",
        PROBE_INPUT_FIRST_PAIRS,
        PROBE_ONE_PORT_COUNTS,
        PROBE_ONE_PORT_EQUALITIES,
        "probe_one_port_ledger",
    )
    require(certificate["one_port"].get("canonical_equality_relation_classes") == 469, "CORRECTED_PROBE_ONE_CLASS_COUNT_FAIL")
    two = validate_stage(
        "two_port",
        PROBE_TWO_PORT_PAIRS,
        PROBE_TWO_PORT_COUNTS,
        PROBE_TWO_PORT_EQUALITIES,
        "probe_two_port_ledger",
    )
    two_record = certificate["two_port"]
    require(two_record.get("parents") == PROBE_ONE_PORT_EQUALITIES, "CORRECTED_PROBE_TWO_PARENT_COUNT_FAIL")
    require(two_record.get("parent_inventory_sha256") == sha_file(paths["probe_two_port_parent_inventory"]), "CORRECTED_PROBE_TWO_PARENT_LEDGER_BINDING_FAIL")
    parent_ordered = two_record.get("ordered_parent_inventory")
    require(isinstance(parent_ordered, dict), "CORRECTED_PROBE_TWO_PARENT_ORDER_RECORD_FAIL")
    require(parent_ordered.get("algorithm") == ordered_algorithm, "CORRECTED_PROBE_TWO_PARENT_ORDER_ALGORITHM_FAIL")
    require(parent_ordered.get("rows") == PROBE_ONE_PORT_EQUALITIES, "CORRECTED_PROBE_TWO_PARENT_ORDER_COUNT_FAIL")
    require(is_sha256(parent_ordered.get("ordered_hash_root")), "CORRECTED_PROBE_TWO_PARENT_ORDER_ROOT_FAIL")
    require(
        two_record.get("reverse_order_parent_relation_counts")
        == {"isomorphic": 30_969, "triangle": 1_760},
        "CORRECTED_PROBE_REVERSE_ORDER_CENSUS_FAIL",
    )

    registries = certificate.get("registries")
    require(isinstance(registries, dict), "CORRECTED_PROBE_REGISTRY_RECORD_FAIL")
    registry_contract = {
        "exact_transports": (
            "probe_exact_transport_ledger",
            "exact_transport_ledger.jsonl.gz",
            PROBE_TRANSPORT_RECORDS,
        ),
        "parent_restrictions": (
            "probe_parent_restriction_ledger",
            "parent_restriction_ledger.jsonl.gz",
            PROBE_RESTRICTION_RECORDS,
        ),
    }
    registry_summaries: dict[str, dict[str, Any]] = {}
    for name, (role, filename, count) in registry_contract.items():
        row = registries.get(name)
        require(isinstance(row, dict), "CORRECTED_PROBE_STREAM_REGISTRY_FAIL", name)
        require(row.get("path") == filename, "CORRECTED_PROBE_STREAM_REGISTRY_PATH_FAIL", name)
        require(row.get("sha256") == sha_file(paths[role]), "CORRECTED_PROBE_STREAM_REGISTRY_BINDING_FAIL", name)
        require(row.get("unique_records") == count, "CORRECTED_PROBE_STREAM_REGISTRY_UNIQUE_FAIL", name)
        ordered = row.get("ordered_records")
        require(isinstance(ordered, dict), "CORRECTED_PROBE_STREAM_REGISTRY_ORDER_FAIL", name)
        require(ordered.get("algorithm") == ordered_algorithm, "CORRECTED_PROBE_STREAM_REGISTRY_ALGORITHM_FAIL", name)
        require(ordered.get("rows") == count, "CORRECTED_PROBE_STREAM_REGISTRY_COUNT_FAIL", name)
        require(is_sha256(ordered.get("ordered_hash_root")), "CORRECTED_PROBE_STREAM_REGISTRY_ROOT_FAIL", name)
        registry_summaries[name] = {
            "count": count,
            "file_sha256": row["sha256"],
            "ordered_hash_root": ordered["ordered_hash_root"],
        }

    separation = registries.get("separation")
    require(isinstance(separation, dict), "CORRECTED_PROBE_SEPARATION_RECORD_FAIL")
    require(separation.get("path") == "separation_proof_registry.json.gz", "CORRECTED_PROBE_SEPARATION_PATH_FAIL")
    require(separation.get("sha256") == sha_file(paths["probe_separation_registry"]), "CORRECTED_PROBE_SEPARATION_FILE_BINDING_FAIL")
    proof = load_gzip_json(paths["probe_separation_registry"])
    verify_payload_hash(proof)
    require(proof.get("schema") == "k2p-corrected-probe-separation-registries-v1", "CORRECTED_PROBE_SEPARATION_SCHEMA_FAIL")
    require(proof.get("payload_sha256") == separation.get("payload_sha256"), "CORRECTED_PROBE_SEPARATION_PAYLOAD_BINDING_FAIL")
    quartet = proof.get("separation_proof_registry")
    ti = proof.get("full_map_Ti_registry")
    require(isinstance(quartet, dict) and len(quartet) == separation.get("topological_proofs") == PROBE_QUARTET_CERTIFICATES, "CORRECTED_PROBE_QUARTET_CERTIFICATE_COUNT_FAIL")
    require(isinstance(ti, dict) and ti.get("forbidden_rooted_triple_oracle_used") is False, "CORRECTED_PROBE_TI_REGISTRY_FAIL")
    require(len(ti.get("certificates", {})) == separation.get("full_map_Ti_relation_certificates") == PROBE_TI_RELATION_CERTIFICATES, "CORRECTED_PROBE_TI_CERTIFICATE_COUNT_FAIL")
    require(len(ti.get("strict_polynomial_registry", {})) == separation.get("full_map_Ti_strict_polynomials") == PROBE_TI_STRICT_POLYNOMIALS, "CORRECTED_PROBE_TI_POLYNOMIAL_COUNT_FAIL")
    for proof_id, row in quartet.items():
        require(proof_id == f"Q:{sha_object(row)}", "CORRECTED_PROBE_QUARTET_SELF_HASH_FAIL", proof_id)
        require(row.get("source_displayed_splits") != row.get("target_displayed_splits"), "CORRECTED_PROBE_QUARTET_NOT_SEPARATOR", proof_id)

    assembly = certificate.get("assembly_theorem")
    require(isinstance(assembly, dict), "CORRECTED_PROBE_ASSEMBLY_RECORD_FAIL")
    require(assembly.get("unresolved") == assembly.get("incoherent") == 0, "CORRECTED_PROBE_ASSEMBLY_ZERO_GATE_FAIL")
    require(
        assembly.get("all_primitive_physical_anchor_types")
        == ["ordinary_tree", "cycle", "theta0", "theta1", "theta2", "theta3"],
        "CORRECTED_PROBE_PRIMITIVE_SCOPE_FAIL",
    )
    bridge = assembly.get("bridge_torus_compatibility")
    require(isinstance(bridge, dict) and bridge.get("every_Ti_certificate_boundary_multihomogeneous") is True, "CORRECTED_PROBE_BRIDGE_TORUS_FAIL")
    segment = assembly.get("one_port_segment_gate")
    require(isinstance(segment, dict) and segment.get("raw_pairs") == PROBE_INPUT_FIRST_PAIRS and segment.get("equality_parents_retained") == PROBE_ONE_PORT_EQUALITIES and segment.get("every_non_equality_has_exact_separator") is True, "CORRECTED_PROBE_SEGMENT_GATE_FAIL")
    order = assembly.get("two_port_order_gate")
    require(isinstance(order, dict) and order.get("raw_pairs_above_equality_parents_only") == PROBE_TWO_PORT_PAIRS and order.get("reversed_marginals_checked") == PROBE_TWO_PORT_EQUALITIES and order.get("reversed_marginals_missing") == 0 and order.get("every_equality_has_reversed_one_port_marginal") is True, "CORRECTED_PROBE_ORDER_GATE_FAIL")
    triangle = assembly.get("one_global_triangle_gate")
    require(isinstance(triangle, dict) and triangle.get("new_triangle_created_above_isomorphic_parent") == 0 and triangle.get("two_port_equalities_inheriting_triangle") == 1_760 and triangle.get("every_triangle_transport_uses_the_same_parent_triangle_edges_and_common_reticulation") is True, "CORRECTED_PROBE_GLOBAL_TRIANGLE_GATE_FAIL")
    site_scope = assembly.get("root_movement_and_site_completeness")
    require(isinstance(site_scope, dict), "CORRECTED_PROBE_SITE_SCOPE_FAIL")
    for field in (
        "all_suppressed_mixed_edges",
        "artificial_root_halves_quotiented_by_exact_isomorphism",
        "pendant_arms",
        "reticulation_incoming_edges",
        "root_suppressed_segment",
    ):
        require(site_scope.get(field) is True, "CORRECTED_PROBE_SITE_SCOPE_FIELD_FAIL", field)
    require(site_scope.get("input_contract_payload_sha256") == probe_input["contract_payload_sha256"], "CORRECTED_PROBE_SITE_INPUT_BINDING_FAIL")

    site_partition = load_json(paths["probe_site_partition_report"])
    verify_logical_payload(site_partition, "CORRECTED_PROBE_SITE_PARTITION")
    require(site_partition.get("schema") == "k2p-probe-site-transport-partition-verification-v1", "CORRECTED_PROBE_SITE_PARTITION_SCHEMA_FAIL")
    require(site_partition.get("status") == "PASS" and site_partition.get("unresolved") == 0, "CORRECTED_PROBE_SITE_PARTITION_NOT_PASS")
    partition_inputs = site_partition.get("inputs")
    require(isinstance(partition_inputs, dict), "CORRECTED_PROBE_SITE_PARTITION_INPUT_FAIL")
    expected_partition_inputs = {
        "probe_input_contract_sha256": sha_file(paths["probe_input_contract"]),
        "one_port_ledger_sha256": sha_file(paths["probe_one_port_ledger"]),
        "two_port_ledger_sha256": sha_file(paths["probe_two_port_ledger"]),
        "transport_ledger_sha256": sha_file(paths["probe_exact_transport_ledger"]),
    }
    require(partition_inputs == expected_partition_inputs, "CORRECTED_PROBE_SITE_PARTITION_BINDING_FAIL")
    require(
        site_partition.get("one_port")
        == {
            "site_transport_partition": {"compatible": 2_206, "incompatible": 27_758},
            "compatible_statuses": {
                "full_map_Ti_strict_sign": 99,
                "isomorphic": 1_915,
                "triangle": 192,
            },
            "incompatible_statuses": {"displayed_quartet_mismatch": 27_758},
        },
        "CORRECTED_PROBE_ONE_SITE_PARTITION_FAIL",
    )
    require(
        site_partition.get("two_port")
        == {
            "site_transport_partition": {"compatible": 33_305, "incompatible": 511_266},
            "compatible_statuses": {
                "full_map_Ti_strict_sign": 576,
                "isomorphic": 30_969,
                "triangle": 1_760,
            },
            "incompatible_statuses": {"displayed_quartet_mismatch": 511_266},
        },
        "CORRECTED_PROBE_TWO_SITE_PARTITION_FAIL",
    )

    package_root = paths["probe_certificate"].parent
    manifest = parse_sha256_manifest(paths["probe_manifest"], package_root)
    manifest_roles = {
        "probe_coherence_certificate.json": "probe_certificate",
        "one_port_ledger.jsonl.gz": "probe_one_port_ledger",
        "two_port_parent_inventory.jsonl.gz": "probe_two_port_parent_inventory",
        "two_port_ledger.jsonl.gz": "probe_two_port_ledger",
        "exact_transport_ledger.jsonl.gz": "probe_exact_transport_ledger",
        "parent_restriction_ledger.jsonl.gz": "probe_parent_restriction_ledger",
        "separation_proof_registry.json.gz": "probe_separation_registry",
        "probe_coherence_independent_verification.json": "probe_replay_report",
        "site_transport_partition_verification.json": "probe_site_partition_report",
        "probe_coherence_mutation_certificate.json": "probe_mutation_report",
        "build_probe_coherence_corrected.py": "probe_builder",
        "verify_probe_coherence_corrected.py": "probe_independent_verifier",
        "verify_site_transport_partition.py": "probe_site_partition_verifier",
        "run_probe_coherence_mutations.py": "probe_mutation_runner",
        "reseal_probe_certificate.py": "probe_primary_verifier",
        "PROOF.md": "probe_proof_document",
        "README.md": "probe_readme",
        "RESEARCH_LOG.md": "probe_research_log",
    }
    require(set(manifest) == set(manifest_roles), "CORRECTED_PROBE_MANIFEST_FILE_SET_FAIL", sorted(set(manifest) ^ set(manifest_roles)))
    for filename, role in manifest_roles.items():
        require(manifest[filename] == sha_file(paths[role]), "CORRECTED_PROBE_MANIFEST_ROLE_BINDING_FAIL", role)

    replay = load_json(paths["probe_replay_report"])
    verify_logical_payload(replay, "CORRECTED_PROBE_REPLAY")
    require(replay.get("schema") == "k2p-corrected-probe-independent-verification-v1", "CORRECTED_PROBE_REPLAY_SCHEMA_FAIL")
    require(replay.get("status") == "PASS", "CORRECTED_PROBE_REPLAY_NOT_PASS")
    require(replay.get("source_certificate_sha256") == sha_file(certificate_path), "CORRECTED_PROBE_REPLAY_FILE_BINDING_FAIL")
    require(replay.get("source_payload_sha256") == certificate["payload_sha256"], "CORRECTED_PROBE_REPLAY_PAYLOAD_BINDING_FAIL")
    expected_replay = {
        "anchors": PROBE_INPUT_ANCHORS,
        "one_port_counts": PROBE_ONE_PORT_COUNTS,
        "two_port_parents": PROBE_ONE_PORT_EQUALITIES,
        "two_port_counts": PROBE_TWO_PORT_COUNTS,
        "reverse_order_counts": {"isomorphic": 30_969, "triangle": 1_760},
        "transport_records": PROBE_TRANSPORT_RECORDS,
        "restriction_records": PROBE_RESTRICTION_RECORDS,
        "quartet_certificates": PROBE_QUARTET_CERTIFICATES,
        "T_i_relation_certificates": PROBE_TI_RELATION_CERTIFICATES,
        "T_i_strict_polynomials_replayed": PROBE_TI_STRICT_POLYNOMIALS,
        "unresolved": 0,
        "incoherent": 0,
    }
    for field, expected in expected_replay.items():
        require(replay.get(field) == expected, "CORRECTED_PROBE_REPLAY_CENSUS_FAIL", field)

    mutations = load_json(paths["probe_mutation_report"])
    verify_logical_payload(mutations, "CORRECTED_PROBE_MUTATIONS")
    require(mutations.get("schema") == "k2p-corrected-probe-mutations-v1", "CORRECTED_PROBE_MUTATION_SCHEMA_FAIL")
    require(mutations.get("status") == "PASS", "CORRECTED_PROBE_MUTATIONS_NOT_PASS")
    require(mutations.get("source_certificate_sha256") == sha_file(certificate_path), "CORRECTED_PROBE_MUTATION_CERTIFICATE_BINDING_FAIL")
    require(mutations.get("source_verifier_sha256") == sha_file(paths["probe_independent_verifier"]), "CORRECTED_PROBE_MUTATION_VERIFIER_BINDING_FAIL")
    cases = mutations.get("cases")
    require(isinstance(cases, list) and len(cases) == mutations.get("mutations_attempted") == mutations.get("mutations_rejected") == 15, "CORRECTED_PROBE_MUTATION_CENSUS_FAIL")
    require(all(row.get("rejected") is True and row.get("returncode") != 0 for row in cases), "CORRECTED_PROBE_MUTATION_SURVIVOR")
    required_mutations = {
        "omitted_anchor",
        "swapped_classifier_precedence",
        "omitted_one_port_probe",
        "wrong_one_port_parent",
        "reassigned_Ti_certificate",
        "omitted_two_port_parent",
        "missing_root_suppressed_site",
        "omitted_two_port_probe",
        "wrong_two_port_parent",
        "reversed_order_class",
        "inconsistent_global_triangle",
        "broken_exact_transport",
        "omitted_parent_restriction",
        "altered_Bernstein_certificate",
        "optimized_mode",
    }
    require({row.get("mutation") for row in cases} == required_mutations, "CORRECTED_PROBE_MUTATION_COVERAGE_FAIL")
    hash_seed = mutations.get("nondefault_hash_seed_replay")
    require(isinstance(hash_seed, dict) and hash_seed.get("PYTHONHASHSEED") == 12_345 and hash_seed.get("status") == "PASS" and hash_seed.get("returncode") == 0, "CORRECTED_PROBE_HASH_SEED_REPLAY_FAIL")

    anchor_replay = load_json(paths["probe_adversarial_anchor_replay"])
    verify_payload_hash(anchor_replay)
    require(anchor_replay.get("schema") == "k2p-probe-input-independent-replay-v1" and anchor_replay.get("status") == "PASS", "CORRECTED_PROBE_ADVERSARIAL_ANCHOR_REPLAY_FAIL")
    require(anchor_replay.get("anchors_reconstructed") == PROBE_INPUT_ANCHORS and anchor_replay.get("source_sites_reenumerated") == PROBE_INPUT_SITES_PER_SIDE and anchor_replay.get("target_sites_reenumerated") == PROBE_INPUT_SITES_PER_SIDE and anchor_replay.get("first_probe_source_target_pairs") == PROBE_INPUT_FIRST_PAIRS, "CORRECTED_PROBE_ADVERSARIAL_ANCHOR_CENSUS_FAIL")
    for field in ("missing_anchors", "extra_anchors", "unresolved"):
        require(anchor_replay.get(field) == 0, "CORRECTED_PROBE_ADVERSARIAL_ANCHOR_ZERO_GATE_FAIL", field)

    adversarial_upstream = load_json(paths["probe_adversarial_upstream_replay"])
    verify_logical_payload(adversarial_upstream, "CORRECTED_PROBE_ADVERSARIAL_UPSTREAM")
    require(adversarial_upstream.get("schema") == replay.get("schema") and adversarial_upstream.get("status") == "PASS", "CORRECTED_PROBE_ADVERSARIAL_UPSTREAM_SCHEMA_FAIL")
    require(adversarial_upstream.get("payload_sha256") == replay["payload_sha256"], "CORRECTED_PROBE_ADVERSARIAL_UPSTREAM_PAYLOAD_FAIL")

    adversarial_mutations = load_json(paths["probe_adversarial_mutation_report"])
    verify_payload_hash(adversarial_mutations)
    require(adversarial_mutations.get("schema") == "k2p-corrected-probe-independent-mutations-v1" and adversarial_mutations.get("status") == "PASS", "CORRECTED_PROBE_ADVERSARIAL_MUTATION_SCHEMA_FAIL")
    require(adversarial_mutations.get("mutations_rejected") == 12 and adversarial_mutations.get("mutations_survived") == 0, "CORRECTED_PROBE_ADVERSARIAL_MUTATION_CENSUS_FAIL")
    adversarial_cases = adversarial_mutations.get("mutations")
    require(isinstance(adversarial_cases, list) and len(adversarial_cases) == 12 and all(row.get("result") == "REJECTED" for row in adversarial_cases), "CORRECTED_PROBE_ADVERSARIAL_MUTATION_ROWS_FAIL")
    required_adversarial_mutations = {
        "omitted_raw_record",
        "wrong_parent",
        "wrong_site",
        "wrong_reverse_transport",
        "broken_global_triangle",
        "reassigned_quartet_certificate",
        "reassigned_Ti_certificate",
        "wrong_parent_restriction",
        "broken_exact_transport",
        "old_rooted_cache_field",
        "classifier_status_reassignment",
        "child_graph_hash_mutation",
    }
    require({row.get("mutation") for row in adversarial_cases} == required_adversarial_mutations, "CORRECTED_PROBE_ADVERSARIAL_MUTATION_COVERAGE_FAIL")

    adversarial = load_json(paths["probe_adversarial_certificate"])
    verify_logical_payload(adversarial, "CORRECTED_PROBE_ADVERSARIAL")
    require(adversarial.get("schema") == "k2p-corrected-probe-independent-primitive-graph-audit-v1" and adversarial.get("status") == "PASS", "CORRECTED_PROBE_ADVERSARIAL_SCHEMA_FAIL")
    require(adversarial.get("source_file_sha256") == sha_file(certificate_path) and adversarial.get("source_payload_sha256") == certificate["payload_sha256"], "CORRECTED_PROBE_ADVERSARIAL_SOURCE_BINDING_FAIL")
    expected_primary_files = {
        filename: manifest[filename]
        for filename in (
            "probe_coherence_certificate.json",
            "one_port_ledger.jsonl.gz",
            "two_port_parent_inventory.jsonl.gz",
            "two_port_ledger.jsonl.gz",
            "exact_transport_ledger.jsonl.gz",
            "parent_restriction_ledger.jsonl.gz",
            "separation_proof_registry.json.gz",
        )
    }
    require(adversarial.get("primary_file_sha256") == expected_primary_files, "CORRECTED_PROBE_ADVERSARIAL_PRIMARY_FILE_BINDING_FAIL")
    require(adversarial.get("primitive_anchor_replay") == {"anchors": 176, "canonical_graph_pair_transport_classes": 39, "source_sites": 2_206, "target_sites": 2_206, "independent_replay_payload_sha256": anchor_replay["payload_sha256"]}, "CORRECTED_PROBE_ADVERSARIAL_ANCHOR_SUMMARY_FAIL")
    require(adversarial.get("one_port") == {"raw_pairs": 29_964, "compatible_site_pairs": 2_206, "incompatible_site_pairs": 27_758, "counts": PROBE_ONE_PORT_COUNTS, "equality_relation_classes": 469}, "CORRECTED_PROBE_ADVERSARIAL_ONE_FAIL")
    require(adversarial.get("two_port") == {"parents": 2_107, "raw_pairs": 544_571, "compatible_site_pairs": 33_305, "incompatible_site_pairs": 511_266, "counts": PROBE_TWO_PORT_COUNTS, "reverse_marginals": 32_729, "reverse_relation_counts": {"isomorphic": 30_969, "triangle": 1_760}}, "CORRECTED_PROBE_ADVERSARIAL_TWO_FAIL")
    witnesses = adversarial.get("exact_witnesses")
    require(witnesses == {"transport_records_applied_to_reconstructed_graphs": 67_741, "parent_restrictions_reconstructed": 4_379, "quartet_certificates_applied": 638, "T_i_relation_certificates_applied": 156, "T_i_strict_polynomials_Bernstein_replayed": 118, "new_global_triangles": 0, "unresolved": 0, "incoherent": 0}, "CORRECTED_PROBE_ADVERSARIAL_WITNESS_FAIL")
    classifier = adversarial.get("classifier_partition")
    require(isinstance(classifier, dict) and classifier.get("relation_first") is True and classifier.get("quartet_second") is True and classifier.get("direct_full_map_Ti_third") is True and classifier.get("forbidden_rooted_oracle_fields") == 0, "CORRECTED_PROBE_ADVERSARIAL_CLASSIFIER_FAIL")
    require(adversarial.get("auxiliary_independent_site_partition") == {"file_sha256": sha_file(paths["probe_site_partition_report"]), "payload_sha256": site_partition["payload_sha256"]}, "CORRECTED_PROBE_ADVERSARIAL_SITE_PARTITION_FAIL")
    require(adversarial.get("mutations") == {"report_sha256": sha_file(paths["probe_adversarial_mutation_report"]), "payload_sha256": adversarial_mutations["payload_sha256"], "rejected": 12, "survived": 0}, "CORRECTED_PROBE_ADVERSARIAL_MUTATION_BINDING_FAIL")

    return {
        "status": "PASS",
        "certificate_file_sha256": sha_file(certificate_path),
        "certificate_payload_sha256": certificate["payload_sha256"],
        "independent_replay_payload_sha256": replay["payload_sha256"],
        "mutation_payload_sha256": mutations["payload_sha256"],
        "anchors": PROBE_INPUT_ANCHORS,
        "producer_anchor_row_hash_root": anchors["ordered_public_anchor_hash_root"],
        "one_port": one,
        "two_port": two,
        "total_raw_pairs": PROBE_TOTAL_PAIRS,
        "aggregate_counts": PROBE_AGGREGATE_COUNTS,
        "total_equality_relations": PROBE_TOTAL_EQUALITIES,
        "two_port_parent_inventory_sha256": two_record["parent_inventory_sha256"],
        "two_port_parent_inventory_hash_root": parent_ordered["ordered_hash_root"],
        "transport_registry": registry_summaries["exact_transports"],
        "restriction_registry": registry_summaries["parent_restrictions"],
        "separation_registry_file_sha256": separation["sha256"],
        "separation_registry_payload_sha256": separation["payload_sha256"],
        "site_partition_payload_sha256": site_partition["payload_sha256"],
        "manifest_file_sha256": sha_file(paths["probe_manifest"]),
        "adversarial_file_sha256": sha_file(paths["probe_adversarial_certificate"]),
        "adversarial_payload_sha256": adversarial["payload_sha256"],
        "adversarial_mutation_payload_sha256": adversarial_mutations["payload_sha256"],
        **derive_probe_composite_roots(paths),
    }


def derive_probe_composite_roots(paths: dict[str, Path]) -> dict[str, Any]:
    """Stream-derive aggregate row and equality-edge roots for both stages."""

    equality_ids: list[str] = []
    edge_hashes: list[str] = []
    transport_hashes: list[str] = []
    stage_equalities = {"one_port": 0, "two_port": 0}

    def consume(path: Path, stage: str) -> None:
        try:
            with gzip.open(path, "rt", encoding="utf-8") as handle:
                for ordinal, line in enumerate(handle):
                    row = json.loads(line, object_pairs_hook=unique_object)
                    require(isinstance(row, dict), "PROBE_COMPOSITE_ROW_FAIL", f"{stage}:{ordinal}")
                    if row.get("status") not in {"isomorphic", "triangle"}:
                        continue
                    if stage == "one_port":
                        parent_id = row.get("parent_anchor_id")
                        child_id = (
                            f"P1:{parent_id}:{row.get('source_site_index')}:"
                            f"{row.get('target_site_index')}"
                        )
                        site_record = {
                            "source_site_id": row.get("source_site_id"),
                            "target_site_id": row.get("target_site_id"),
                        }
                        reverse = None
                    else:
                        parent_id = row.get("one_port_parent_id")
                        child_id = (
                            f"P2:{parent_id}:{row.get('second_source_site_index')}:"
                            f"{row.get('second_target_site_index')}"
                        )
                        site_record = {
                            "source_site_id": row.get("second_source_site_id"),
                            "target_site_id": row.get("second_target_site_id"),
                        }
                        reverse = row.get("reverse_order_certificate")
                    require(
                        isinstance(parent_id, str)
                        and parent_id
                        and isinstance(row.get("transport_id"), str),
                        "PROBE_COMPOSITE_EQUALITY_RECORD_FAIL",
                        f"{stage}:{ordinal}",
                    )
                    equality_ids.append(child_id)
                    edge_hashes.append(
                        sha_object(
                            {
                                "child_id": child_id,
                                "parent_id": parent_id,
                                "stage": stage,
                            }
                        )
                    )
                    transport_hashes.append(
                        sha_object(
                            {
                                "child_id": child_id,
                                "child_transport_id": row.get("transport_id"),
                                "global_triangle_sha256": row.get("global_triangle_sha256"),
                                "parent_id": parent_id,
                                "parent_transport_id": row.get("parent_transport_id"),
                                "reverse_order_certificate": reverse,
                                "source_parent_restriction_id": row.get("source_parent_restriction_id"),
                                "stage": stage,
                                "target_parent_restriction_id": row.get("target_parent_restriction_id"),
                                **site_record,
                            }
                        )
                    )
                    stage_equalities[stage] += 1
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise ReleaseFailure(f"PROBE_COMPOSITE_STREAM_FAIL:{stage}:{error}") from error

    consume(paths["probe_one_port_ledger"], "one_port")
    consume(paths["probe_two_port_ledger"], "two_port")
    require(stage_equalities["one_port"] == PROBE_ONE_PORT_EQUALITIES, "PROBE_COMPOSITE_ONE_EQUALITY_FAIL")
    require(stage_equalities["two_port"] == PROBE_TWO_PORT_EQUALITIES, "PROBE_COMPOSITE_TWO_EQUALITY_FAIL")
    require(len(equality_ids) == len(set(equality_ids)) == PROBE_TOTAL_EQUALITIES, "PROBE_COMPOSITE_EQUALITY_ID_FAIL")
    return {
        "aggregate_raw_id_hash_root": sha_object(
            {
                "one_port_ordered_row_hash_root": load_json(paths["probe_certificate"])["one_port"]["ordered_ledger"]["ordered_hash_root"],
                "two_port_ordered_row_hash_root": load_json(paths["probe_certificate"])["two_port"]["ordered_ledger"]["ordered_hash_root"],
            }
        ),
        "equality_relation_id_hash_root": sha_object(
            [sha_object(identifier) for identifier in equality_ids]
        ),
        "equality_parent_child_edge_hash_root": sha_object(edge_hashes),
        "equality_transport_restriction_hash_root": sha_object(transport_hashes),
    }


def validate_restoration_v3_package(paths: dict[str, Path]) -> dict[str, Any]:
    """Validate the clean, corrected two-level physical restoration forest."""

    required = {
        "restoration_v3_generator",
        "restoration_v3_builder",
        "restoration_v3_forest_certificate",
        "restoration_v3_historical_crosswalk",
        "restoration_v3_independent_verifier",
        "restoration_v3_replay",
        "restoration_v3_mutation_runner",
        "restoration_v3_mutation_report",
    }
    require(required <= set(paths), "RESTORATION_V3_ROLE_MISSING", sorted(required - set(paths)))
    certificate_path = paths["restoration_v3_forest_certificate"]
    crosswalk_path = paths["restoration_v3_historical_crosswalk"]
    certificate = load_json(certificate_path)
    verify_payload_hash(certificate)
    require(certificate.get("schema") == "k2p-corrected-restoration-forest-v3", "RESTORATION_V3_SCHEMA_FAIL")
    require(certificate.get("status") == "PASS", "RESTORATION_V3_NOT_PASS")
    clean_serialized = canonical_bytes(certificate)
    for retired in (
        b"tree_sunlet",
        b"strict_tree_sunlet_sign",
        b"historical_proof_REVOKED_if_sign",
        b"historical_row_sha256",
        b"rooted",
    ):
        require(retired not in clean_serialized, "RESTORATION_V3_RETIRED_FIELD_IN_CLEAN_PROJECTION", retired.decode())

    census = certificate.get("census")
    require(isinstance(census, dict), "RESTORATION_V3_CENSUS_FAIL")
    expected_scalars = {
        "canonical_restoration_parents": 997,
        "member_roots": 2_540,
        "first_children": RESTORATION_V3_FIRST_CHILDREN,
        "first_children_exact_relation_none": RESTORATION_V3_FIRST_CHILDREN,
        "first_parent_transport_edges": RESTORATION_V3_FIRST_CHILDREN,
        "second_children": RESTORATION_V3_SECOND_CHILDREN,
        "second_parent_transport_edges": RESTORATION_V3_SECOND_CHILDREN,
        "forest_edges": RESTORATION_V3_FOREST_EDGES,
        "continuation_parents": 32,
        "final_leaves": RESTORATION_V3_FINAL_LEAVES,
        "max_depth": 2,
        "first_source_parent_transport_classes": 42,
        "first_target_parent_transport_classes": 4_986,
        "sign_polynomial_classes": 113,
        "algebra_certificate_classes": 16,
        "exact_graph_relation_none_residuals": 818,
        "missing_children": 0,
        "cycles": 0,
        "unresolved": 0,
    }
    for field, expected in expected_scalars.items():
        require(census.get(field) == expected, "RESTORATION_V3_CENSUS_FIELD_FAIL", field)
    require(census.get("first_proof_counts") == RESTORATION_V3_FIRST_PROOF_COUNTS, "RESTORATION_V3_FIRST_PROOF_CENSUS_FAIL")
    require(census.get("second_proof_counts") == RESTORATION_V3_SECOND_PROOF_COUNTS, "RESTORATION_V3_SECOND_PROOF_CENSUS_FAIL")
    require(census.get("first_status_counts") == {"continuation": 32, "separated": 36_536}, "RESTORATION_V3_FIRST_STATUS_CENSUS_FAIL")

    first = certificate.get("first_coverage")
    second = certificate.get("second_coverage")
    first_hashes = certificate.get("first_row_hashes")
    second_hashes = certificate.get("second_row_hashes")
    require(
        isinstance(first, list)
        and isinstance(first_hashes, list)
        and len(first) == len(first_hashes) == RESTORATION_V3_FIRST_CHILDREN,
        "RESTORATION_V3_FIRST_ROWS_FAIL",
    )
    require(
        isinstance(second, list)
        and isinstance(second_hashes, list)
        and len(second) == len(second_hashes) == RESTORATION_V3_SECOND_CHILDREN,
        "RESTORATION_V3_SECOND_ROWS_FAIL",
    )
    observed_first_hashes: list[str] = []
    member_root_ids: list[str] = []
    seen_member_roots: set[str] = set()
    continuation_indices: set[int] = set()
    for ordinal, row in enumerate(first):
        require(isinstance(row, dict), "RESTORATION_V3_FIRST_ROW_FAIL", ordinal)
        require(row.get("ordinal") == ordinal, "RESTORATION_V3_FIRST_ORDINAL_FAIL", ordinal)
        public = dict(row)
        digest = public.pop("row_sha256", None)
        require(is_sha256(digest) and sha_object(public) == digest, "RESTORATION_V3_FIRST_ROW_HASH_FAIL", ordinal)
        observed_first_hashes.append(digest)
        root_id = row.get("root_id")
        require(isinstance(root_id, str) and re.fullmatch(r"s\d+:c\d+:t\d+:p\d+", root_id) is not None, "RESTORATION_V3_MEMBER_ROOT_ID_FAIL", ordinal)
        if root_id not in seen_member_roots:
            seen_member_roots.add(root_id)
            member_root_ids.append(root_id)
        status = row.get("status")
        proof = row.get("proof")
        remaining = row.get("remaining_roles")
        require(isinstance(remaining, list), "RESTORATION_V3_FIRST_REMAINING_ROLES_FAIL", ordinal)
        if status == "continuation":
            require(proof == "restore_remaining_physical_role" and len(remaining) == 1, "RESTORATION_V3_CONTINUATION_ROW_FAIL", ordinal)
            continuation_indices.add(ordinal)
        else:
            require(status == "separated", "RESTORATION_V3_FIRST_LEAF_FAIL", ordinal)
    require(observed_first_hashes == first_hashes, "RESTORATION_V3_FIRST_HASH_LEDGER_FAIL")
    require(sha_object(first_hashes) == certificate.get("first_hash_root"), "RESTORATION_V3_FIRST_HASH_ROOT_FAIL")
    require(len(continuation_indices) == 32, "RESTORATION_V3_CONTINUATION_CENSUS_FAIL")
    require(len(member_root_ids) == 2_540, "RESTORATION_V3_MEMBER_ROOT_CENSUS_FAIL")

    observed_second_hashes: list[str] = []
    parent_use: Counter[int] = Counter()
    for ordinal, row in enumerate(second):
        require(isinstance(row, dict), "RESTORATION_V3_SECOND_ROW_FAIL", ordinal)
        public = dict(row)
        digest = public.pop("row_sha256", None)
        require(is_sha256(digest) and sha_object(public) == digest, "RESTORATION_V3_SECOND_ROW_HASH_FAIL", ordinal)
        observed_second_hashes.append(digest)
        parent_index = row.get("parent_first_coverage_index")
        require(parent_index in continuation_indices, "RESTORATION_V3_SECOND_PARENT_FAIL", ordinal)
        require(row.get("parent_first_row_sha256") == first_hashes[parent_index], "RESTORATION_V3_SECOND_PARENT_HASH_FAIL", ordinal)
        require(row.get("status") == "separated" and row.get("remaining_roles") == [], "RESTORATION_V3_SECOND_LEAF_FAIL", ordinal)
        require(row.get("root_id") == first[parent_index].get("root_id"), "RESTORATION_V3_SECOND_MEMBER_ROOT_FAIL", ordinal)
        parent_use[parent_index] += 1
    require(observed_second_hashes == second_hashes, "RESTORATION_V3_SECOND_HASH_LEDGER_FAIL")
    require(sha_object(second_hashes) == certificate.get("second_hash_root"), "RESTORATION_V3_SECOND_HASH_ROOT_FAIL")
    require(set(parent_use) == continuation_indices and set(parent_use.values()) == {8}, "RESTORATION_V3_TERMINATING_FOREST_FAIL")
    require(len(set(first_hashes + second_hashes)) == RESTORATION_V3_FOREST_EDGES, "RESTORATION_V3_CHILD_ID_UNIQUENESS_FAIL")

    source_transports = certificate.get("first_source_transport_certificates")
    target_transports = certificate.get("first_target_transport_certificates")
    require(isinstance(source_transports, dict) and len(source_transports) == 42, "RESTORATION_V3_SOURCE_TRANSPORT_REGISTRY_FAIL")
    require(isinstance(target_transports, dict) and len(target_transports) == 4_986, "RESTORATION_V3_TARGET_TRANSPORT_REGISTRY_FAIL")
    for registry, label in ((source_transports, "source"), (target_transports, "target")):
        for transport_id, record in registry.items():
            require(sha_object(record) == transport_id, "RESTORATION_V3_TRANSPORT_RECORD_HASH_FAIL", label)
            require(
                record.get("parent_mixed_graph_sha256") == record.get("restricted_child_mixed_graph_sha256"),
                "RESTORATION_V3_TRANSPORT_RESTRICTION_FAIL",
                label,
            )
    require({row.get("source_parent_transport_id") for row in first} == set(source_transports), "RESTORATION_V3_SOURCE_TRANSPORT_COVERAGE_FAIL")
    require({row.get("target_parent_transport_id") for row in first} == set(target_transports), "RESTORATION_V3_TARGET_TRANSPORT_COVERAGE_FAIL")

    quartet_records = certificate.get("quartet_certificates")
    algebra_records = certificate.get("algebra_certificates")
    sign_records = certificate.get("sign_certificates")
    require(isinstance(quartet_records, dict) and len(quartet_records) == 92, "RESTORATION_V3_QUARTET_REGISTRY_FAIL")
    require(isinstance(algebra_records, dict) and len(algebra_records) == 16, "RESTORATION_V3_ALGEBRA_REGISTRY_FAIL")
    require(isinstance(sign_records, dict) and len(sign_records) == 113, "RESTORATION_V3_SIGN_REGISTRY_FAIL")
    require(all(sha_object(record) == key for key, record in quartet_records.items()), "RESTORATION_V3_QUARTET_RECORD_HASH_FAIL")
    require(all(sha_object(record) == key for key, record in algebra_records.items()), "RESTORATION_V3_ALGEBRA_RECORD_HASH_FAIL")
    require(
        all(record.get("normalized_negative_pullback_sha256") == key and record.get("strict_sign") == "negative" for key, record in sign_records.items()),
        "RESTORATION_V3_SIGN_RECORD_BINDING_FAIL",
    )
    referenced_quartets: set[str] = set()
    referenced_algebra: set[str] = set()
    referenced_signs: set[str] = set()
    for ordinal, row in enumerate(first + second):
        proof = row.get("proof")
        if proof == "displayed_quartet_mismatch":
            digest = row.get("certificate_sha256")
            require(digest in quartet_records, "RESTORATION_V3_QUARTET_REFERENCE_FAIL", ordinal)
            referenced_quartets.add(digest)
        elif proof in {"exact_multihomogeneous_quadratic", "inherited_exact_F_2_112_quartic"}:
            digest = row.get("certificate_sha256")
            require(digest in algebra_records, "RESTORATION_V3_ALGEBRA_REFERENCE_FAIL", ordinal)
            referenced_algebra.add(digest)
        elif proof == "full_map_Ti_zero_strict_sign":
            record = row.get("certificate")
            require(isinstance(record, dict), "RESTORATION_V3_SIGN_PRESENTATION_FAIL", ordinal)
            digest = record.get("normalized_negative_pullback_sha256")
            require(
                digest in sign_records
                and record.get("strict_sign") == "negative"
                and {record.get("zero_side"), record.get("signed_side")} == {"source", "target"},
                "RESTORATION_V3_SIGN_REFERENCE_FAIL",
                ordinal,
            )
            referenced_signs.add(digest)
        elif proof == "restore_remaining_physical_role":
            record = row.get("certificate")
            require(
                row in first
                and isinstance(record, dict)
                and record.get("all_asymmetric_Ti_search") == "none"
                and record.get("expected_source_insertion_children") == 8
                and record.get("next_restored_role") == row.get("remaining_roles", [None])[0],
                "RESTORATION_V3_CONTINUATION_CERTIFICATE_FAIL",
                ordinal,
            )
        else:
            raise ReleaseFailure(f"RESTORATION_V3_UNKNOWN_PROOF:{proof}")
    require(referenced_quartets == set(quartet_records), "RESTORATION_V3_QUARTET_REFERENCE_COVERAGE_FAIL")
    require(referenced_algebra == set(algebra_records), "RESTORATION_V3_ALGEBRA_REFERENCE_COVERAGE_FAIL")
    require(referenced_signs == set(sign_records), "RESTORATION_V3_SIGN_REFERENCE_COVERAGE_FAIL")

    crosswalk = load_json(crosswalk_path)
    verify_payload_hash(crosswalk)
    require(crosswalk.get("schema") == "k2p-corrected-restoration-historical-crosswalk-v1", "RESTORATION_V3_CROSSWALK_SCHEMA_FAIL")
    require(crosswalk.get("status") == "PASS", "RESTORATION_V3_CROSSWALK_NOT_PASS")
    inputs = certificate.get("inputs")
    require(isinstance(inputs, dict), "RESTORATION_V3_INPUT_BINDING_FAIL")
    require(inputs.get("restoration_generator_sha256") == sha_file(paths["restoration_v3_generator"]), "RESTORATION_V3_GENERATOR_BINDING_FAIL")
    require(inputs.get("provenance_crosswalk_sha256") == sha_file(crosswalk_path), "RESTORATION_V3_CROSSWALK_FILE_BINDING_FAIL")
    require(inputs.get("provenance_crosswalk_payload_sha256") == crosswalk["payload_sha256"], "RESTORATION_V3_CROSSWALK_PAYLOAD_BINDING_FAIL")
    require(crosswalk.get("clean_first_row_hashes") == first_hashes, "RESTORATION_V3_CROSSWALK_FIRST_HASHES_FAIL")
    require(crosswalk.get("clean_second_row_hashes") == second_hashes, "RESTORATION_V3_CROSSWALK_SECOND_HASHES_FAIL")
    require(crosswalk.get("clean_first_hash_root") == certificate.get("first_hash_root"), "RESTORATION_V3_CROSSWALK_FIRST_ROOT_FAIL")
    require(crosswalk.get("clean_second_hash_root") == certificate.get("second_hash_root"), "RESTORATION_V3_CROSSWALK_SECOND_ROOT_FAIL")
    require(crosswalk.get("scope_contract") == certificate.get("scope_contract"), "RESTORATION_V3_SCOPE_CROSSWALK_FAIL")
    scope = certificate.get("scope_contract")
    require(
        isinstance(scope, dict)
        and scope.get("member_presentations") == 54
        and scope.get("canonical_classes") == 35
        and scope.get("forest_intersection") == 0
        and scope.get("critical_triangle_raw_ids") == [67_161, 67_167, 67_401, 67_407]
        and is_sha256(scope.get("ordered_record_sha256")),
        "RESTORATION_V3_OMITTED_TERMINAL_SCOPE_FAIL",
    )
    crosswalk_first = crosswalk.get("first_coverage")
    crosswalk_second = crosswalk.get("second_coverage")
    require(isinstance(crosswalk_first, list) and len(crosswalk_first) == RESTORATION_V3_FIRST_CHILDREN, "RESTORATION_V3_CROSSWALK_FIRST_ROWS_FAIL")
    require(isinstance(crosswalk_second, list) and len(crosswalk_second) == RESTORATION_V3_SECOND_CHILDREN, "RESTORATION_V3_CROSSWALK_SECOND_ROWS_FAIL")
    for ordinal, (historical, clean) in enumerate(zip(crosswalk_first, first)):
        require(historical.get("clean_row_sha256") == clean["row_sha256"], "RESTORATION_V3_CROSSWALK_FIRST_LINK_FAIL", ordinal)
    for ordinal, (historical, clean) in enumerate(zip(crosswalk_second, second)):
        require(historical.get("clean_row_sha256") == clean["row_sha256"], "RESTORATION_V3_CROSSWALK_SECOND_LINK_FAIL", ordinal)

    replay = load_json(paths["restoration_v3_replay"])
    verify_payload_hash(replay)
    require(replay.get("schema") == "k2p-corrected-restoration-independent-replay-v3", "RESTORATION_V3_REPLAY_SCHEMA_FAIL")
    require(replay.get("status") == "PASS", "RESTORATION_V3_REPLAY_NOT_PASS")
    require(replay.get("source_certificate_sha256") == sha_file(certificate_path), "RESTORATION_V3_REPLAY_FILE_BINDING_FAIL")
    require(replay.get("source_certificate_payload_sha256") == certificate["payload_sha256"], "RESTORATION_V3_REPLAY_PAYLOAD_BINDING_FAIL")
    require(replay.get("source_crosswalk_sha256") == sha_file(crosswalk_path), "RESTORATION_V3_REPLAY_CROSSWALK_FILE_FAIL")
    require(replay.get("source_crosswalk_payload_sha256") == crosswalk["payload_sha256"], "RESTORATION_V3_REPLAY_CROSSWALK_PAYLOAD_FAIL")
    expected_replay = {
        "canonical_parents": 997,
        "member_roots": 2_540,
        "provenance_first_rows_rehashed": RESTORATION_V3_FIRST_CHILDREN,
        "continuation_parents": 32,
        "second_children_replayed": RESTORATION_V3_SECOND_CHILDREN,
        "first_parent_transport_edges_replayed": RESTORATION_V3_FIRST_CHILDREN,
        "first_exact_relation_none_replayed": RESTORATION_V3_FIRST_CHILDREN,
        "second_parent_transport_edges_replayed": RESTORATION_V3_SECOND_CHILDREN,
        "first_source_parent_transports_replayed": 42,
        "first_target_parent_transports_replayed": 4_986,
        "omitted_terminal_member_scope_replayed": 54,
        "final_leaves": RESTORATION_V3_FINAL_LEAVES,
        "sign_classes_replayed": 113,
        "algebra_classes_replayed": 16,
        "unresolved": 0,
        "missing_children": 0,
        "cycles": 0,
    }
    for field, expected in expected_replay.items():
        require(replay.get(field) == expected, "RESTORATION_V3_REPLAY_CENSUS_FAIL", field)

    mutations = load_json(paths["restoration_v3_mutation_report"])
    verify_payload_hash(mutations)
    require(mutations.get("schema") == "k2p-corrected-restoration-mutations-v1", "RESTORATION_V3_MUTATION_SCHEMA_FAIL")
    require(mutations.get("status") == "PASS", "RESTORATION_V3_MUTATIONS_NOT_PASS")
    require(mutations.get("source_certificate_sha256") == sha_file(certificate_path), "RESTORATION_V3_MUTATION_CERTIFICATE_BINDING_FAIL")
    require(mutations.get("source_crosswalk_sha256") == sha_file(crosswalk_path), "RESTORATION_V3_MUTATION_CROSSWALK_BINDING_FAIL")
    require(mutations.get("verifier_sha256") == sha_file(paths["restoration_v3_independent_verifier"]), "RESTORATION_V3_MUTATION_VERIFIER_BINDING_FAIL")
    cases = mutations.get("cases")
    require(isinstance(cases, list) and len(cases) == mutations.get("mutations_attempted") == mutations.get("mutations_rejected") == 13, "RESTORATION_V3_MUTATION_CENSUS_FAIL")
    require(all(row.get("rejected") is True and row.get("returncode") != 0 for row in cases), "RESTORATION_V3_MUTATION_SURVIVOR")
    required_mutations = {
        "omitted_clean_first_edge",
        "omitted_provenance_raw_record",
        "wrong_first_parent_transport",
        "broken_target_transport_payload",
        "reassigned_quartet_certificate",
        "reassigned_Ti_presentation",
        "altered_Bernstein_coefficient",
        "invalid_D_plus_parameter_witness",
        "reassigned_F_2_112_quartic",
        "omitted_second_child",
        "wrong_second_parent",
        "nonforest_depth_cycle_attempt",
        "optimized_mode",
    }
    require({row.get("mutation") for row in cases} == required_mutations, "RESTORATION_V3_MUTATION_COVERAGE_FAIL")

    canonical_parent_ids: list[str] = []
    seen_parent_ids: set[str] = set()
    class_membership_records: list[dict[str, str]] = []
    for member_root_id in member_root_ids:
        match = re.fullmatch(r"s(\d+):c(\d+):t\d+:p\d+", member_root_id)
        require(match is not None, "RESTORATION_V3_MEMBER_ROOT_PARSE_FAIL", member_root_id)
        parent_id = f"source_{int(match.group(1))}:class_{int(match.group(2)):06d}"
        if parent_id not in seen_parent_ids:
            seen_parent_ids.add(parent_id)
            canonical_parent_ids.append(parent_id)
        class_membership_records.append({"canonical_parent_id": parent_id, "member_root_id": member_root_id})
    require(len(canonical_parent_ids) == 997, "RESTORATION_V3_CANONICAL_PARENT_DERIVATION_FAIL")
    classes = derived_restoration_class_census(PROJECT)
    canonical_parent_id_hash_root = sha_object(sorted(canonical_parent_ids))
    require(canonical_parent_id_hash_root == classes["parent_ids_sha256"], "RESTORATION_V3_CLASS_LEDGER_PARENT_BINDING_FAIL")

    edge_hashes: list[str] = []
    transport_hashes: list[str] = []
    for ordinal, row in enumerate(first):
        edge_hashes.append(sha_object({"child_id": row["row_sha256"], "depth": 1, "parent_id": row["root_id"]}))
        transport_hashes.append(sha_object({
            "child_id": row["row_sha256"],
            "depth": 1,
            "source_parent_transport_id": row["source_parent_transport_id"],
            "target_parent_transport_id": row["target_parent_transport_id"],
        }))
    for ordinal, row in enumerate(second):
        edge_hashes.append(sha_object({"child_id": row["row_sha256"], "depth": 2, "parent_id": row["parent_first_row_sha256"]}))
        transport_hashes.append(sha_object({
            "child_id": row["row_sha256"],
            "depth": 2,
            "source_parent_mixed_graph_sha256": row["source_parent_mixed_graph_sha256"],
            "target_parent_mixed_graph_sha256": row["target_parent_mixed_graph_sha256"],
        }))
    leaf_hashes = [row["row_sha256"] for row in first if row["status"] == "separated"] + second_hashes
    return {
        "status": "PASS",
        "forest_payload_sha256": certificate["payload_sha256"],
        "crosswalk_payload_sha256": crosswalk["payload_sha256"],
        "replay_payload_sha256": replay["payload_sha256"],
        "mutation_payload_sha256": mutations["payload_sha256"],
        "canonical_parent_count": 997,
        "canonical_parent_id_hash_root": canonical_parent_id_hash_root,
        "member_root_count": 2_540,
        "member_root_id_hash_root": sha_object(member_root_ids),
        "class_membership_edge_hash_root": sha_object([sha_object(row) for row in class_membership_records]),
        "first_child_count": RESTORATION_V3_FIRST_CHILDREN,
        "first_child_hash_root": certificate["first_hash_root"],
        "second_child_count": RESTORATION_V3_SECOND_CHILDREN,
        "second_child_hash_root": certificate["second_hash_root"],
        "generated_child_count": RESTORATION_V3_FOREST_EDGES,
        "generated_child_id_hash_root": sha_object(first_hashes + second_hashes),
        "parent_child_edge_hash_root": sha_object(edge_hashes),
        "transport_restriction_hash_root": sha_object(transport_hashes),
        "continuation_parent_count": 32,
        "leaf_count": RESTORATION_V3_FINAL_LEAVES,
        "leaf_id_hash_root": sha_object(leaf_hashes),
        "leaf_category_counts": {"exact_separator": RESTORATION_V3_FINAL_LEAVES},
        "omitted_terminal_member_scope": 54,
        "omitted_terminal_class_scope": 35,
    }


def validate_frozen_corrected_universe(
    locator: dict[str, Any],
    paths: dict[str, Path],
    raw4_overlay_summary: dict[str, Any],
    theta2_truth_summary: dict[str, Any],
    raw4_composite: dict[str, Any],
    theta2_composite: dict[str, Any],
    composite_release: dict[str, Any],
    restoration_summary: dict[str, Any],
    cycle_summary: dict[str, Any],
    probe_input_summary: dict[str, Any],
    probe_producer_summary: dict[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    required_roles = set(locator["required_frozen_roles"])
    require(required_roles <= set(paths), "CORRECTED_FROZEN_ROLE_MISSING", sorted(required_roles - set(paths)))
    certificate = load_json(paths["corrected_universe_certificate"])
    verify_payload_hash(certificate)
    require(certificate.get("schema") == CORRECTED_RELEASE_SCHEMA, "CORRECTED_RELEASE_SCHEMA_FAIL")
    require(certificate.get("status") == "PASS", "CORRECTED_RELEASE_NOT_PASS")
    downstream_roles = {
        "corrected_universe_certificate",
        "corrected_universe_replay_report",
        "corrected_universe_mutation_report",
    }
    expected_bindings = {
        role: locator["artifacts"][role]["sha256"]
        for role in sorted(required_roles - downstream_roles)
    }
    require(certificate.get("artifact_sha256") == expected_bindings, "CORRECTED_RELEASE_ARTIFACT_BINDING_FAIL")
    families = certificate.get("families")
    required_families = {"raw4", "theta2", "restoration", "cycle", "probe"}
    require(isinstance(families, dict) and set(families) == required_families, "CORRECTED_RELEASE_FAMILY_SET_FAIL")
    family_summaries = {
        name: validate_dynamic_family_record(name, families[name])
        for name in sorted(required_families)
    }
    require(
        family_summaries["raw4"]["input_count"] == RAW_FOUR_TOTAL,
        "CORRECTED_RELEASE_RAW4_CROSS_BINDING_FAIL",
    )
    require(
        family_summaries["raw4"]["output_category_counts"]
        == RAW4_COMPOSITE_CATEGORY_COUNTS,
        "CORRECTED_RELEASE_RAW4_CATEGORY_BINDING_FAIL",
    )
    require(
        family_summaries["raw4"]["input_id_hash_root"]
        == raw4_composite["ordered_raw_id_hash_root"],
        "CORRECTED_RELEASE_RAW4_ID_ROOT_BINDING_FAIL",
    )
    require(
        family_summaries["raw4"]["output_id_hash_root"]
        == raw4_composite["ordered_row_hash_root"],
        "CORRECTED_RELEASE_RAW4_ROW_ROOT_BINDING_FAIL",
    )
    require(
        family_summaries["raw4"]["generated_child_count"] == 0,
        "CORRECTED_RELEASE_RAW4_CHILD_LEDGER_MISPLACED",
    )
    require(
        raw4_composite["category_counts"]["full_map_Ti_strict_sign"]
        == raw4_overlay_summary["corrected_rows"],
        "CORRECTED_RELEASE_RAW4_OVERLAY_CROSS_BINDING_FAIL",
    )
    require(
        family_summaries["theta2"]["input_count"] == THETA2_TOTAL,
        "CORRECTED_RELEASE_THETA2_CROSS_BINDING_FAIL",
    )
    require(
        family_summaries["theta2"]["output_category_counts"]
        == THETA2_COMPOSITE_CATEGORY_COUNTS,
        "CORRECTED_RELEASE_THETA2_CATEGORY_BINDING_FAIL",
    )
    require(
        family_summaries["theta2"]["input_id_hash_root"]
        == theta2_composite["ordered_raw_id_hash_root"],
        "CORRECTED_RELEASE_THETA2_ID_ROOT_BINDING_FAIL",
    )
    require(
        family_summaries["theta2"]["output_id_hash_root"]
        == theta2_composite["ordered_row_hash_root"],
        "CORRECTED_RELEASE_THETA2_ROW_ROOT_BINDING_FAIL",
    )
    require(
        family_summaries["theta2"]["generated_child_count"]
        == theta2_composite["restoration_descendant_children"],
        "CORRECTED_RELEASE_THETA2_CHILD_CROSS_BINDING_FAIL",
    )
    require(
        family_summaries["theta2"]["generated_child_id_hash_root"]
        == theta2_composite["restoration_descendant_child_id_hash_root"],
        "CORRECTED_RELEASE_THETA2_CHILD_ROOT_CROSS_BINDING_FAIL",
    )
    require(
        family_summaries["theta2"]["generated_child_edge_hash_root"]
        == theta2_composite["restoration_descendant_edge_hash_root"],
        "CORRECTED_RELEASE_THETA2_EDGE_ROOT_CROSS_BINDING_FAIL",
    )
    require(
        family_summaries["theta2"]["generated_child_transport_hash_root"]
        == theta2_composite["restoration_descendant_transport_hash_root"],
        "CORRECTED_RELEASE_THETA2_TRANSPORT_ROOT_CROSS_BINDING_FAIL",
    )
    require(
        theta2_composite["category_counts"]["full_map_Ti_strict_sign"]
        == theta2_truth_summary["rows"],
        "CORRECTED_RELEASE_THETA2_TRUTH_CROSS_BINDING_FAIL",
    )
    require(
        family_summaries["cycle"]["input_count"] == cycle_summary["base_rows"],
        "CORRECTED_RELEASE_CYCLE_INPUT_CROSS_BINDING_FAIL",
    )
    require(
        family_summaries["cycle"]["output_category_counts"]
        == cycle_summary["base_category_counts"],
        "CORRECTED_RELEASE_CYCLE_CATEGORY_CROSS_BINDING_FAIL",
    )
    require(
        family_summaries["cycle"]["input_id_hash_root"]
        == cycle_summary["base_row_hash_root"],
        "CORRECTED_RELEASE_CYCLE_INPUT_ROOT_FAIL",
    )
    require(
        family_summaries["cycle"]["output_id_hash_root"]
        == cycle_summary["base_row_hash_root"],
        "CORRECTED_RELEASE_CYCLE_OUTPUT_ROOT_FAIL",
    )
    require(
        family_summaries["cycle"]["generated_child_count"]
        == cycle_summary["full_children"],
        "CORRECTED_RELEASE_CYCLE_CHILD_COUNT_FAIL",
    )
    require(
        family_summaries["cycle"]["generated_child_id_hash_root"]
        == cycle_summary["full_row_hash_root"],
        "CORRECTED_RELEASE_CYCLE_CHILD_ROOT_FAIL",
    )
    require(
        family_summaries["cycle"]["generated_child_edge_hash_root"]
        == cycle_summary["child_transport_hash_root"],
        "CORRECTED_RELEASE_CYCLE_EDGE_ROOT_FAIL",
    )
    require(
        family_summaries["cycle"]["generated_child_transport_hash_root"]
        == cycle_summary["child_transport_hash_root"],
        "CORRECTED_RELEASE_CYCLE_TRANSPORT_ROOT_FAIL",
    )
    require(
        family_summaries["restoration"]["input_count"]
        == restoration_summary["member_root_count"],
        "CORRECTED_RELEASE_RESTORATION_INPUT_COUNT_FAIL",
    )
    require(
        family_summaries["restoration"]["input_id_hash_root"]
        == restoration_summary["member_root_id_hash_root"],
        "CORRECTED_RELEASE_RESTORATION_INPUT_ROOT_FAIL",
    )
    require(
        family_summaries["restoration"]["output_id_hash_root"]
        == restoration_summary["member_root_id_hash_root"],
        "CORRECTED_RELEASE_RESTORATION_OUTPUT_ROOT_FAIL",
    )
    require(
        family_summaries["restoration"]["generated_child_count"]
        == restoration_summary["generated_child_count"],
        "CORRECTED_RELEASE_RESTORATION_CHILD_COUNT_FAIL",
    )
    require(
        family_summaries["restoration"]["generated_child_id_hash_root"]
        == restoration_summary["generated_child_id_hash_root"],
        "CORRECTED_RELEASE_RESTORATION_CHILD_ROOT_FAIL",
    )
    require(
        family_summaries["restoration"]["generated_child_edge_hash_root"]
        == restoration_summary["parent_child_edge_hash_root"],
        "CORRECTED_RELEASE_RESTORATION_EDGE_ROOT_FAIL",
    )
    require(
        family_summaries["restoration"]["generated_child_transport_hash_root"]
        == restoration_summary["transport_restriction_hash_root"],
        "CORRECTED_RELEASE_RESTORATION_TRANSPORT_ROOT_FAIL",
    )

    forest = certificate.get("restoration_forest")
    require(isinstance(forest, dict), "CORRECTED_RELEASE_FOREST_RECORD_FAIL")
    class_parents = forest.get("class_parent_count")
    require(isinstance(class_parents, int) and class_parents >= 0, "CORRECTED_RELEASE_FOREST_PARENT_COUNT_FAIL")
    require(
        class_parents == raw4_composite["restoration_parent_count"],
        "CORRECTED_RELEASE_FOREST_COMPOSITE_PARENT_COUNT_FAIL",
    )
    require(
        class_parents == restoration_summary["canonical_parent_count"],
        "CORRECTED_RELEASE_FOREST_V3_PARENT_COUNT_FAIL",
    )
    require(
        forest.get("class_parent_id_hash_root")
        == raw4_composite["restoration_parent_id_hash_root"],
        "CORRECTED_RELEASE_FOREST_COMPOSITE_PARENT_ROOT_FAIL",
    )
    require(
        forest.get("class_parent_id_hash_root")
        == restoration_summary["canonical_parent_id_hash_root"],
        "CORRECTED_RELEASE_FOREST_V3_PARENT_ROOT_FAIL",
    )
    require(forest.get("canonical_root_count") == class_parents, "CORRECTED_RELEASE_FOREST_CANONICAL_ROOT_COUNT_FAIL")
    require(forest.get("covered_canonical_root_count") == class_parents, "CORRECTED_RELEASE_FOREST_CANONICAL_ROOT_COVERAGE_FAIL")
    member_roots = raw4_composite["restoration_member_presentation_count"]
    require(forest.get("member_root_count") == member_roots, "CORRECTED_RELEASE_FOREST_MEMBER_ROOT_COUNT_FAIL")
    require(forest.get("covered_member_root_count") == member_roots, "CORRECTED_RELEASE_FOREST_MEMBER_ROOT_COVERAGE_FAIL")
    require(
        forest.get("raw_presentation_membership_hash_root")
        == raw4_composite["restoration_member_membership_hash_root"],
        "CORRECTED_RELEASE_FOREST_RAW_MEMBERSHIP_ROOT_FAIL",
    )
    require(member_roots == restoration_summary["member_root_count"], "CORRECTED_RELEASE_FOREST_V3_MEMBER_COUNT_FAIL")
    require(
        forest.get("member_root_id_hash_root")
        == restoration_summary["member_root_id_hash_root"],
        "CORRECTED_RELEASE_FOREST_V3_MEMBER_ROOT_FAIL",
    )
    require(forest.get("class_membership_edge_count") == member_roots, "CORRECTED_RELEASE_FOREST_CLASS_MEMBERSHIP_EDGE_COUNT_FAIL")
    require(
        forest.get("class_membership_edge_hash_root")
        == restoration_summary["class_membership_edge_hash_root"],
        "CORRECTED_RELEASE_FOREST_V3_CLASS_MEMBERSHIP_EDGE_ROOT_FAIL",
    )
    generated_children = family_summaries["restoration"]["generated_child_count"]
    require(forest.get("generated_child_count") == generated_children, "CORRECTED_RELEASE_FOREST_CHILD_COUNT_FAIL")
    require(forest.get("covered_child_count") == generated_children, "CORRECTED_RELEASE_FOREST_CHILD_COVERAGE_FAIL")
    require(
        forest.get("generated_child_id_hash_root")
        == family_summaries["restoration"]["generated_child_id_hash_root"],
        "CORRECTED_RELEASE_FOREST_CHILD_ROOT_FAIL",
    )
    require(
        forest.get("parent_child_edge_hash_root")
        == family_summaries["restoration"]["generated_child_edge_hash_root"],
        "CORRECTED_RELEASE_FOREST_EDGE_ROOT_FAIL",
    )
    require(
        forest.get("transport_restriction_hash_root")
        == family_summaries["restoration"]["generated_child_transport_hash_root"],
        "CORRECTED_RELEASE_FOREST_TRANSPORT_ROOT_FAIL",
    )
    for field in (
        "missing_canonical_roots",
        "missing_member_roots",
        "multiple_class_memberships",
        "missing_children",
        "cycles",
        "unresolved",
        "incoherent_transports",
    ):
        require(forest.get(field) == 0, "CORRECTED_RELEASE_FOREST_ZERO_GATE_FAIL", field)
    edge_count = forest.get("edge_count")
    require(edge_count == generated_children, "CORRECTED_RELEASE_FOREST_EDGE_COUNT_FAIL")
    require(forest.get("transport_restrictions_replayed") == edge_count, "CORRECTED_RELEASE_FOREST_TRANSPORT_COVERAGE_FAIL")
    require(
        forest.get("first_child_count") == restoration_summary["first_child_count"]
        and forest.get("first_child_hash_root") == restoration_summary["first_child_hash_root"]
        and forest.get("second_child_count") == restoration_summary["second_child_count"]
        and forest.get("second_child_hash_root") == restoration_summary["second_child_hash_root"],
        "CORRECTED_RELEASE_FOREST_V3_LEVEL_BINDING_FAIL",
    )
    leaf_counts = forest.get("leaf_category_counts")
    require(
        isinstance(leaf_counts, dict)
        and set(leaf_counts) <= {"exact_separator", "labelled_isomorphism", "ordinary_triangle"}
        and all(isinstance(value, int) and value >= 0 for value in leaf_counts.values())
        and sum(leaf_counts.values()) == forest.get("leaf_count"),
        "CORRECTED_RELEASE_FOREST_LEAF_PARTITION_FAIL",
    )
    require(
        forest.get("leaf_count") == restoration_summary["leaf_count"]
        and forest.get("leaf_id_hash_root") == restoration_summary["leaf_id_hash_root"]
        and leaf_counts == restoration_summary["leaf_category_counts"],
        "CORRECTED_RELEASE_FOREST_V3_LEAF_BINDING_FAIL",
    )
    require(
        forest.get("omitted_terminal_member_scope")
        == restoration_summary["omitted_terminal_member_scope"]
        and forest.get("omitted_terminal_class_scope")
        == restoration_summary["omitted_terminal_class_scope"],
        "CORRECTED_RELEASE_FOREST_V3_OMITTED_SCOPE_FAIL",
    )

    probe = certificate.get("probe_coherence")
    require(isinstance(probe, dict), "CORRECTED_RELEASE_PROBE_RECORD_FAIL")
    require(
        probe.get("producer_certificate_sha256")
        == probe_producer_summary["certificate_file_sha256"],
        "CORRECTED_RELEASE_PROBE_PRODUCER_FILE_FAIL",
    )
    require(
        probe.get("producer_payload_sha256")
        == probe_producer_summary["certificate_payload_sha256"],
        "CORRECTED_RELEASE_PROBE_PRODUCER_PAYLOAD_FAIL",
    )
    require(
        probe.get("producer_manifest_sha256")
        == probe_producer_summary["manifest_file_sha256"],
        "CORRECTED_RELEASE_PROBE_MANIFEST_FAIL",
    )
    require(
        probe.get("adversarial_audit_file_sha256")
        == probe_producer_summary["adversarial_file_sha256"],
        "CORRECTED_RELEASE_PROBE_ADVERSARIAL_FILE_FAIL",
    )
    require(
        probe.get("adversarial_audit_payload_sha256")
        == probe_producer_summary["adversarial_payload_sha256"],
        "CORRECTED_RELEASE_PROBE_ADVERSARIAL_PAYLOAD_FAIL",
    )
    require(
        probe.get("adversarial_mutation_payload_sha256")
        == probe_producer_summary["adversarial_mutation_payload_sha256"],
        "CORRECTED_RELEASE_PROBE_ADVERSARIAL_MUTATION_FAIL",
    )
    derived_anchors = probe.get("derived_anchor_count")
    require(isinstance(derived_anchors, int) and derived_anchors >= 0, "CORRECTED_RELEASE_PROBE_ANCHOR_COUNT_FAIL")
    require(probe.get("anchor_count") == derived_anchors, "CORRECTED_RELEASE_PROBE_ANCHOR_COVERAGE_FAIL")
    require(derived_anchors == probe_input_summary["anchors"], "CORRECTED_RELEASE_PROBE_INPUT_ANCHOR_COUNT_FAIL")
    require(
        probe.get("input_anchor_row_hash_root")
        == probe_input_summary["anchor_row_hash_root"],
        "CORRECTED_RELEASE_PROBE_INPUT_ANCHOR_ROOT_FAIL",
    )
    require(
        probe.get("producer_anchor_row_hash_root")
        == probe_producer_summary["producer_anchor_row_hash_root"],
        "CORRECTED_RELEASE_PROBE_PRODUCER_ANCHOR_ROOT_FAIL",
    )
    require(
        probe.get("input_contract_payload_sha256")
        == probe_input_summary["contract_payload_sha256"],
        "CORRECTED_RELEASE_PROBE_INPUT_PAYLOAD_FAIL",
    )
    one_probe = probe.get("one_port")
    require(isinstance(one_probe, dict), "CORRECTED_RELEASE_PROBE_ONE_RECORD_FAIL")
    require(one_probe.get("raw_pair_count") == probe_input_summary["first_probe_pairs"] == PROBE_INPUT_FIRST_PAIRS, "CORRECTED_RELEASE_PROBE_ONE_PAIR_CENSUS_FAIL")
    require(one_probe.get("category_counts") == PROBE_ONE_PORT_COUNTS, "CORRECTED_RELEASE_PROBE_ONE_CATEGORY_FAIL")
    require(one_probe.get("equality_survivor_count") == PROBE_ONE_PORT_EQUALITIES, "CORRECTED_RELEASE_PROBE_ONE_EQUALITY_FAIL")
    require(one_probe.get("ledger_sha256") == probe_producer_summary["one_port"]["ledger_sha256"], "CORRECTED_RELEASE_PROBE_ONE_LEDGER_FAIL")
    require(one_probe.get("ordered_row_hash_root") == probe_producer_summary["one_port"]["ordered_row_hash_root"], "CORRECTED_RELEASE_PROBE_ONE_ROOT_FAIL")

    two_probe = probe.get("two_port")
    require(isinstance(two_probe, dict), "CORRECTED_RELEASE_PROBE_TWO_RECORD_FAIL")
    require(two_probe.get("parent_count") == PROBE_ONE_PORT_EQUALITIES, "CORRECTED_RELEASE_PROBE_TWO_PARENT_COUNT_FAIL")
    require(two_probe.get("parent_inventory_sha256") == probe_producer_summary["two_port_parent_inventory_sha256"], "CORRECTED_RELEASE_PROBE_TWO_PARENT_FILE_FAIL")
    require(two_probe.get("parent_inventory_hash_root") == probe_producer_summary["two_port_parent_inventory_hash_root"], "CORRECTED_RELEASE_PROBE_TWO_PARENT_ROOT_FAIL")
    require(two_probe.get("raw_pair_count") == PROBE_TWO_PORT_PAIRS, "CORRECTED_RELEASE_PROBE_TWO_PAIR_CENSUS_FAIL")
    require(two_probe.get("category_counts") == PROBE_TWO_PORT_COUNTS, "CORRECTED_RELEASE_PROBE_TWO_CATEGORY_FAIL")
    require(two_probe.get("equality_survivor_count") == PROBE_TWO_PORT_EQUALITIES, "CORRECTED_RELEASE_PROBE_TWO_EQUALITY_FAIL")
    require(two_probe.get("ledger_sha256") == probe_producer_summary["two_port"]["ledger_sha256"], "CORRECTED_RELEASE_PROBE_TWO_LEDGER_FAIL")
    require(two_probe.get("ordered_row_hash_root") == probe_producer_summary["two_port"]["ordered_row_hash_root"], "CORRECTED_RELEASE_PROBE_TWO_ROOT_FAIL")
    require(two_probe.get("reversed_marginals_checked") == PROBE_TWO_PORT_EQUALITIES and two_probe.get("reversed_marginals_missing") == 0, "CORRECTED_RELEASE_PROBE_REVERSE_COVERAGE_FAIL")

    require(family_summaries["probe"]["input_count"] == PROBE_TOTAL_PAIRS, "CORRECTED_RELEASE_PROBE_FAMILY_INPUT_COUNT_FAIL")
    require(family_summaries["probe"]["output_category_counts"] == PROBE_AGGREGATE_COUNTS, "CORRECTED_RELEASE_PROBE_FAMILY_CATEGORY_FAIL")
    require(probe.get("total_raw_pair_count") == PROBE_TOTAL_PAIRS, "CORRECTED_RELEASE_PROBE_TOTAL_PAIR_COUNT_FAIL")
    require(probe.get("aggregate_category_counts") == PROBE_AGGREGATE_COUNTS, "CORRECTED_RELEASE_PROBE_AGGREGATE_CATEGORY_FAIL")
    require(probe.get("aggregate_raw_id_hash_root") == family_summaries["probe"]["input_id_hash_root"], "CORRECTED_RELEASE_PROBE_AGGREGATE_INPUT_ROOT_FAIL")
    require(probe.get("aggregate_row_hash_root") == family_summaries["probe"]["output_id_hash_root"], "CORRECTED_RELEASE_PROBE_AGGREGATE_OUTPUT_ROOT_FAIL")
    require(probe.get("aggregate_raw_id_hash_root") == probe_producer_summary["aggregate_raw_id_hash_root"], "CORRECTED_RELEASE_PROBE_PRODUCER_AGGREGATE_ROOT_FAIL")
    derived_survivors = probe.get("derived_equality_relation_count")
    require(derived_survivors == PROBE_TOTAL_EQUALITIES, "CORRECTED_RELEASE_PROBE_EQUALITY_COUNT_FAIL")
    require(probe.get("equality_relation_count") == derived_survivors, "CORRECTED_RELEASE_PROBE_EQUALITY_COVERAGE_FAIL")
    require(
        derived_survivors == family_summaries["probe"]["generated_child_count"],
        "CORRECTED_RELEASE_PROBE_FAMILY_SURVIVOR_COUNT_FAIL",
    )
    require(
        probe.get("equality_relation_id_hash_root")
        == family_summaries["probe"]["generated_child_id_hash_root"],
        "CORRECTED_RELEASE_PROBE_SURVIVOR_ROOT_FAIL",
    )
    require(probe.get("equality_relation_id_hash_root") == probe_producer_summary["equality_relation_id_hash_root"], "CORRECTED_RELEASE_PROBE_PRODUCER_EQUALITY_ROOT_FAIL")
    for name, producer_key in (
        ("exact_transport_registry", "transport_registry"),
        ("parent_restriction_registry", "restriction_registry"),
    ):
        row = probe.get(name)
        expected = probe_producer_summary[producer_key]
        require(isinstance(row, dict), "CORRECTED_RELEASE_PROBE_REGISTRY_RECORD_FAIL", name)
        require(row.get("count") == expected["count"], "CORRECTED_RELEASE_PROBE_REGISTRY_COUNT_FAIL", name)
        require(row.get("file_sha256") == expected["file_sha256"], "CORRECTED_RELEASE_PROBE_REGISTRY_FILE_FAIL", name)
        require(row.get("ordered_hash_root") == expected["ordered_hash_root"], "CORRECTED_RELEASE_PROBE_REGISTRY_ROOT_FAIL", name)
    require(probe.get("separation_registry_file_sha256") == probe_producer_summary["separation_registry_file_sha256"], "CORRECTED_RELEASE_PROBE_SEPARATION_FILE_FAIL")
    require(probe.get("separation_registry_payload_sha256") == probe_producer_summary["separation_registry_payload_sha256"], "CORRECTED_RELEASE_PROBE_SEPARATION_PAYLOAD_FAIL")
    require(probe.get("site_partition_payload_sha256") == probe_producer_summary["site_partition_payload_sha256"], "CORRECTED_RELEASE_PROBE_SITE_PARTITION_PAYLOAD_FAIL")
    require(
        probe.get("all_restrictions_from_one_fixed_full_containment") is True,
        "CORRECTED_RELEASE_PROBE_FIXED_CONTAINMENT_FAIL",
    )
    require(
        probe.get("fixed_full_containment_audit_payload_sha256")
        == probe_producer_summary["adversarial_payload_sha256"],
        "CORRECTED_RELEASE_PROBE_FIXED_CONTAINMENT_AUDIT_FAIL",
    )
    for field in (
        "missing_anchors",
        "missing_equality_relations",
        "multiple_parent_links",
        "unresolved",
        "incoherent",
        "broken_transports",
        "rooted_reason_count",
        "mixed_isomorphic_deck_failures",
    ):
        require(probe.get(field) == 0, "CORRECTED_RELEASE_PROBE_ZERO_GATE_FAIL", field)
    probe_edges = probe.get("edge_count")
    require(probe_edges == derived_survivors, "CORRECTED_RELEASE_PROBE_EDGE_COUNT_FAIL")
    require(probe.get("transport_restrictions_replayed") == probe_edges, "CORRECTED_RELEASE_PROBE_TRANSPORT_COVERAGE_FAIL")
    require(probe.get("root_movement_or_internal_core_arc_restrictions_replayed") == probe_edges, "CORRECTED_RELEASE_PROBE_ROOT_MOVEMENT_COVERAGE_FAIL")
    require(
        probe.get("parent_child_edge_hash_root")
        == family_summaries["probe"]["generated_child_edge_hash_root"],
        "CORRECTED_RELEASE_PROBE_EDGE_ROOT_FAIL",
    )
    require(probe.get("parent_child_edge_hash_root") == probe_producer_summary["equality_parent_child_edge_hash_root"], "CORRECTED_RELEASE_PROBE_PRODUCER_EDGE_ROOT_FAIL")
    require(
        probe.get("transport_restriction_hash_root")
        == family_summaries["probe"]["generated_child_transport_hash_root"],
        "CORRECTED_RELEASE_PROBE_TRANSPORT_ROOT_FAIL",
    )
    require(probe.get("transport_restriction_hash_root") == probe_producer_summary["equality_transport_restriction_hash_root"], "CORRECTED_RELEASE_PROBE_PRODUCER_TRANSPORT_ROOT_FAIL")

    replay = load_json(paths["corrected_universe_replay_report"])
    verify_payload_hash(replay)
    require(
        replay.get("schema") == "k2p-corrected-finite-universe-independent-replay-v2",
        "CORRECTED_RELEASE_REPLAY_SCHEMA_FAIL",
    )
    require(replay.get("status") == "PASS", "CORRECTED_RELEASE_REPLAY_NOT_PASS")
    for field in (
        "raw_generation_replayed",
        "terminal_classification_replayed",
        "generated_children_replayed",
        "restoration_coverage_replayed",
        "cycle_coverage_replayed",
        "probe_coverage_replayed",
        "probe_one_port_cartesian_replayed",
        "probe_two_port_parent_inventory_replayed",
        "probe_two_port_cartesian_replayed",
        "probe_reverse_order_replayed",
        "probe_full_map_algebra_replayed",
        "probe_fixed_containment_replayed",
        "transport_coherence_replayed",
    ):
        require(replay.get(field) is True, "CORRECTED_RELEASE_REPLAY_LAYER_MISSING", field)
    for field in ("unresolved", "rooted_reason_count", "source_tree_drift"):
        require(replay.get(field) == 0, "CORRECTED_RELEASE_REPLAY_ZERO_GATE_FAIL", field)

    mutations = load_json(paths["corrected_universe_mutation_report"])
    verify_payload_hash(mutations)
    require(
        mutations.get("schema") == "k2p-corrected-finite-universe-mutations-v2",
        "CORRECTED_RELEASE_MUTATION_SCHEMA_FAIL",
    )
    require(mutations.get("status") == "PASS", "CORRECTED_RELEASE_MUTATIONS_NOT_PASS")
    require(mutations.get("survivors") == 0, "CORRECTED_RELEASE_MUTATION_SURVIVOR")
    tests = {
        row.get("name") if isinstance(row, dict) else row
        for row in mutations.get("tests", [])
    }
    required_tests = {
        "omitted_raw_row",
        "false_rank_exclusion",
        "missing_child",
        "wrong_parent",
        "broken_transport",
        "reassigned_quadratic_certificate",
        "reassigned_cubic_certificate",
        "reassigned_quartic_certificate",
        "reassigned_quintic_certificate",
        "raw4424_false_tree_sunlet_reintroduction",
        "rooted_restriction_reintroduction",
        "omitted_probe_one_port_row",
        "omitted_probe_two_port_parent",
        "omitted_probe_two_port_row",
        "wrong_probe_parent",
        "broken_probe_transport",
        "broken_probe_restriction",
        "reassigned_probe_Ti_certificate",
        "reversed_probe_order_class",
        "inconsistent_probe_global_triangle",
        "source_tree_write",
        "optimized_mode",
    }
    require(required_tests <= tests, "CORRECTED_RELEASE_MUTATION_COVERAGE_FAIL", sorted(required_tests - tests))
    return (
        {
            "status": "PASS",
            "locator_payload_sha256": locator["payload_sha256"],
            "release_payload_sha256": certificate["payload_sha256"],
            "families": family_summaries,
            "raw4_composite": raw4_composite,
            "theta2_composite": theta2_composite,
            "composite_release": composite_release,
            "restoration_v3": restoration_summary,
            "cycle_promotion": cycle_summary,
            "probe_input": probe_input_summary,
            "probe_producer": probe_producer_summary,
            "restoration_parent_count": class_parents,
            "restoration_member_root_count": member_roots,
            "restoration_generated_child_count": generated_children,
            "forest_edge_count": edge_count,
            "probe_anchor_count": derived_anchors,
            "probe_equality_relation_count": derived_survivors,
            "probe_edge_count": probe_edges,
            "independent_replay_payload_sha256": replay["payload_sha256"],
            "mutation_payload_sha256": mutations["payload_sha256"],
        },
        [],
    )


def validate_corrected_finite_universe(
    project: Path = PROJECT,
    *,
    family_inputs_only: bool = False,
) -> tuple[dict[str, Any], list[str]]:
    """Validate the dynamic replacement for every revoked four-port census."""

    locator = corrected_locator(project)
    paths = locator_artifacts(locator, project)
    cycle_summary = validate_cycle_promotion_package(paths)
    probe_input_summary = validate_probe_input_package(paths)
    probe_producer_summary = validate_corrected_probe_package(paths, probe_input_summary)
    restoration_summary = validate_restoration_v3_package(paths)
    require(locator["family_status"].get("cycle") == "PASS", "CORRECTED_LOCATOR_CYCLE_STATUS_FAIL")
    require(locator["family_status"].get("restoration") == "PASS", "CORRECTED_LOCATOR_RESTORATION_STATUS_FAIL")
    require(locator["family_status"].get("raw4") == "PASS", "CORRECTED_LOCATOR_RAW4_STATUS_FAIL")
    require(locator["family_status"].get("theta2") == "PASS", "CORRECTED_LOCATOR_THETA2_STATUS_FAIL")
    if locator["status"] == "BLOCKED" or family_inputs_only:
        require(locator["family_status"].get("probe") == "PASS", "CORRECTED_LOCATOR_PROBE_STATUS_FAIL")
    full_map_path = paths.get("raw4_full_map_truth_certificate")
    require(full_map_path is not None, "RAW4_FULL_MAP_TRUTH_ARTIFACT_MISSING")
    full_map = validate_raw4_full_map_truth(full_map_path)
    theta2_summary = validate_theta2_full_map_truth(project)
    overlay_summary = validate_raw4_corrected_overlay(paths, full_map, project)
    raw4_composite = validate_composite_primitive_summary(
        "raw4", paths, RAW_FOUR_TOTAL, RAW4_COMPOSITE_CATEGORY_COUNTS
    )
    theta2_composite = validate_composite_primitive_summary(
        "theta2", paths, THETA2_TOTAL, THETA2_COMPOSITE_CATEGORY_COUNTS
    )
    composite_release = validate_corrected_composite_release_package(
        paths, raw4_composite, theta2_composite
    )
    require(
        raw4_composite["category_counts"]["full_map_Ti_strict_sign"]
        == overlay_summary["corrected_rows"],
        "CORRECTED_BLOCKED_RAW4_OVERLAY_CROSS_BINDING_FAIL",
    )
    require(
        theta2_composite["category_counts"]["full_map_Ti_strict_sign"]
        == theta2_summary["rows"],
        "CORRECTED_BLOCKED_THETA2_TRUTH_CROSS_BINDING_FAIL",
    )
    require(
        raw4_composite["restoration_parent_count"]
        == restoration_summary["canonical_parent_count"]
        and raw4_composite["restoration_parent_id_hash_root"]
        == restoration_summary["canonical_parent_id_hash_root"]
        and raw4_composite["restoration_member_presentation_count"]
        == restoration_summary["member_root_count"],
        "CORRECTED_BLOCKED_RESTORATION_COMPOSITE_CROSS_BINDING_FAIL",
    )
    if locator["status"] == "BLOCKED" or family_inputs_only:
        preliminary = paths.get("preliminary_reclassification")
        require(preliminary is not None, "CORRECTED_PRELIMINARY_ARTIFACT_MISSING")
        payload = load_json(preliminary)
        verify_payload_hash(payload)
        require(
            payload.get("schema") == "k2p-raw4-revoked-sign-reclassification-v1",
            "CORRECTED_PRELIMINARY_SCHEMA_FAIL",
        )
        require(payload.get("raw_rows") == REVOKED_RAW_FOUR_ROWS, "CORRECTED_PRELIMINARY_CENSUS_FAIL")
        counts = payload.get("raw_category_counts")
        require(isinstance(counts, dict) and sum(counts.values()) == REVOKED_RAW_FOUR_ROWS, "CORRECTED_PRELIMINARY_PARTITION_FAIL")
        require(payload.get("status") != "PASS", "BLOCKED_LOCATOR_POINTS_TO_PROMOTED_PRELIMINARY")
        if locator["status"] == "BLOCKED":
            blockers = locator.get("blockers")
            require(
                isinstance(blockers, list)
                and blockers
                and all(isinstance(item, str) and item for item in blockers),
                "CORRECTED_LOCATOR_BLOCKERS_FAIL",
            )
        else:
            require(
                family_inputs_only and locator["status"] == "FROZEN",
                "CORRECTED_FAMILY_INPUT_MODE_STATUS_FAIL",
            )
            blockers = [
                "UNIFIED_CROSS_FAMILY_CERTIFICATE_REPLAY_MUTATIONS_PENDING"
            ]
        return (
            {
                "status": "ALL_FIVE_FAMILIES_PASS_UNIFIED_CROSS_FAMILY_PENDING",
                "locator_payload_sha256": locator["payload_sha256"],
                "preliminary_payload_sha256": payload["payload_sha256"],
                "superseded_preliminary_counts": counts,
                "superseded_preliminary_split": True,
                "full_map_truth_payload_sha256": full_map["payload_sha256"],
                "full_map_truth_rows": REVOKED_RAW_FOUR_ROWS,
                "full_map_polynomial_classes": 8,
                "theta2_full_map_truth": theta2_summary,
                "raw4_composite": raw4_composite,
                "theta2_composite": theta2_composite,
                "composite_release": composite_release,
                "cycle_promotion": cycle_summary,
                "probe_input": probe_input_summary,
                "probe_producer": probe_producer_summary,
                "restoration_v3": restoration_summary,
                **overlay_summary,
                "parent_count_promotion_status": "RESTORATION_V3_AND_RAW4_COMPOSITE_CROSS_BOUND",
            },
            ["CORRECTED_FINITE_UNIVERSE_NOT_FROZEN", *blockers],
        )

    return validate_frozen_corrected_universe(
        locator,
        paths,
        overlay_summary,
        theta2_summary,
        raw4_composite,
        theta2_composite,
        composite_release,
        restoration_summary,
        cycle_summary,
        probe_input_summary,
        probe_producer_summary,
    )


def validate_tree_sunlet_truth(project: Path = PROJECT) -> dict[str, Any]:
    path = project / "work/adversarial_proof_review/tree_sunlet_truth_certificate.json"
    require(path.is_file(), "TREE_SUNLET_TRUTH_CERTIFICATE_MISSING")
    certificate = load_json(path)
    verify_payload_hash(certificate)
    require(certificate.get("status") == "PASS", "TREE_SUNLET_TRUTH_NOT_PASS")
    require(
        certificate.get("false_topology_oracle_count") == 0,
        "TREE_SUNLET_FALSE_ORACLE_ROWS_REMAIN",
    )
    require(certificate.get("exact_iso_conflicts") == 0, "TREE_SUNLET_ISO_CONFLICTS_REMAIN")
    require(
        certificate.get("exact_triangle_conflicts") == 0,
        "TREE_SUNLET_TRIANGLE_CONFLICTS_REMAIN",
    )
    require(certificate.get("unresolved") == 0, "TREE_SUNLET_UNRESOLVED_REMAIN")
    families = certificate.get("families")
    require(isinstance(families, dict), "TREE_SUNLET_FAMILY_LEDGER_MISSING")
    required = {
        "raw4",
        "theta2",
        "restoration",
        "cycle",
        "probe",
    }
    require(required <= set(families), "TREE_SUNLET_FAMILY_SET_FAIL", sorted(required - set(families)))
    for family in sorted(required):
        row = families.get(family)
        require(isinstance(row, dict), "TREE_SUNLET_FAMILY_MISSING", family)
        expected_presentations = row.get("input_presentations")
        require(
            isinstance(expected_presentations, int) and expected_presentations >= 0,
            "TREE_SUNLET_INPUT_CENSUS_FAIL",
            family,
        )
        if family == "raw4":
            require(
                expected_presentations == REVOKED_RAW_FOUR_ROWS,
                "TREE_SUNLET_RAW4_INPUT_CENSUS_FAIL",
            )
        require(row.get("fully_replayed") is True, "TREE_SUNLET_FAMILY_NOT_REPLAYED", family)
        require(
            row.get("full_map_pullback_replayed") is True,
            "TREE_SUNLET_FULL_MAP_NOT_REPLAYED",
            family,
        )
        require(
            row.get("reclassified_presentations") == expected_presentations,
            "TREE_SUNLET_RECLASSIFICATION_COVERAGE_FAIL",
            family,
        )
        require(
            isinstance(row.get("output_category_counts"), dict)
            and all(
                isinstance(value, int) and value >= 0
                for value in row["output_category_counts"].values()
            )
            and sum(row["output_category_counts"].values()) == expected_presentations,
            "TREE_SUNLET_OUTPUT_PARTITION_FAIL",
            family,
        )
        require(
            row.get("rooted_reason_count") == 0,
            "TREE_SUNLET_ROOTED_REASON_REINTRODUCED",
            family,
        )
        require(row.get("exact_iso_conflicts") == 0, "TREE_SUNLET_FAMILY_ISO_CONFLICT", family)
        require(
            row.get("exact_triangle_conflicts") == 0,
            "TREE_SUNLET_FAMILY_TRIANGLE_CONFLICT",
            family,
        )
    mutation_path = project / "work/adversarial_proof_review/tree_sunlet_truth_mutation_certificate.json"
    require(mutation_path.is_file(), "TREE_SUNLET_TRUTH_MUTATIONS_MISSING")
    mutations = load_json(mutation_path)
    verify_payload_hash(mutations)
    require(mutations.get("status") == "PASS", "TREE_SUNLET_TRUTH_MUTATIONS_NOT_PASS")
    require(mutations.get("survivors") == 0, "TREE_SUNLET_TRUTH_MUTATION_SURVIVOR")
    return {
        "payload_sha256": certificate["payload_sha256"],
        "family_count": len(families),
        "false_topology_oracle_count": 0,
    }


def validate_theta2_full_map_truth(project: Path = PROJECT) -> dict[str, Any]:
    path = (
        project
        / "work/adversarial_proof_review/theta2_tree_sunlet_full_map_certificate.json"
    )
    certificate = load_json(path)
    verify_payload_hash(certificate)
    require(
        certificate.get("schema") == "k2p-theta2-tree-sunlet-full-map-truth-v1",
        "THETA2_FULL_MAP_TRUTH_SCHEMA_FAIL",
    )
    require(certificate.get("status") == "PASS", "THETA2_FULL_MAP_TRUTH_NOT_PASS")
    for field in (
        "claimed_rows",
        "full_map_source_zero_rows",
        "full_map_strict_target_sign_rows",
    ):
        require(certificate.get(field) == 2528, "THETA2_FULL_MAP_TRUTH_CENSUS_FAIL", field)
    require(
        certificate.get("canonical_polynomial_relation_classes") == 85,
        "THETA2_FULL_MAP_TRUTH_CLASS_CENSUS_FAIL",
    )
    require(
        certificate.get("exact_full_graph_relation_census") == {"none": 2528},
        "THETA2_FULL_MAP_EXACT_RELATION_FAIL",
    )
    for field in ("false_iso_or_triangle_conflicts", "incoherent", "unresolved"):
        require(certificate.get(field) == 0, "THETA2_FULL_MAP_ZERO_GATE_FAIL", field)
    row_hashes = certificate.get("ordered_truth_row_hashes")
    require(
        isinstance(row_hashes, list)
        and len(row_hashes) == 2528
        and all(is_sha256(item) for item in row_hashes),
        "THETA2_FULL_MAP_ROW_HASH_LEDGER_FAIL",
    )
    require(
        sha_object(row_hashes) == certificate.get("ordered_truth_row_hash_root"),
        "THETA2_FULL_MAP_ROW_HASH_ROOT_FAIL",
    )
    require(
        "proof is the direct full five-port Fourier-map zero/sign identity"
        in certificate.get("claim_boundary", ""),
        "THETA2_FULL_MAP_CLAIM_BOUNDARY_FAIL",
    )
    replay_path = (
        project
        / "work/theta2_sign_reclassification/theta2_independent_replay_certificate.json"
    )
    replay = load_json(replay_path)
    verify_payload_hash(replay)
    require(
        replay.get("schema") == "k2p-theta2-full-map-independent-replay-v1",
        "THETA2_FULL_MAP_REPLAY_SCHEMA_FAIL",
    )
    require(replay.get("status") == "PASS", "THETA2_FULL_MAP_REPLAY_NOT_PASS")
    require(replay.get("source_certificate_sha256") == sha_file(path), "THETA2_FULL_MAP_REPLAY_FILE_BINDING_FAIL")
    require(replay.get("source_certificate_payload_sha256") == certificate["payload_sha256"], "THETA2_FULL_MAP_REPLAY_PAYLOAD_BINDING_FAIL")
    for field in (
        "raw_rows_replayed",
        "exact_graph_relation_none_rows",
        "source_zero_rows",
        "strict_target_negative_rows",
    ):
        require(replay.get(field) == 2528, "THETA2_FULL_MAP_REPLAY_CENSUS_FAIL", field)
    require(replay.get("sign_classes_replayed") == 85, "THETA2_FULL_MAP_REPLAY_CLASS_FAIL")
    require(replay.get("unresolved") == 0, "THETA2_FULL_MAP_REPLAY_UNRESOLVED")

    mutation_path = project / "work/theta2_sign_reclassification/theta2_mutation_certificate.json"
    mutations = load_json(mutation_path)
    verify_payload_hash(mutations)
    require(
        mutations.get("schema") == "k2p-theta2-full-map-mutations-v1",
        "THETA2_FULL_MAP_MUTATION_SCHEMA_FAIL",
    )
    require(mutations.get("status") == "PASS", "THETA2_FULL_MAP_MUTATIONS_NOT_PASS")
    require(mutations.get("source_certificate_sha256") == sha_file(path), "THETA2_FULL_MAP_MUTATION_BINDING_FAIL")
    results = mutations.get("results")
    require(isinstance(results, list) and mutations.get("mutation_count") == len(results), "THETA2_FULL_MAP_MUTATION_CENSUS_FAIL")
    require(mutations.get("survived") == 0 and all(row.get("rejected") is True for row in results), "THETA2_FULL_MAP_MUTATION_SURVIVOR")
    required_mutations = {
        "omitted_truth_row",
        "reassigned_truth_row",
        "missing_target_presentation",
        "wrong_target_orientation",
        "mutated_Bernstein_coefficient",
        "reassigned_relation_multiplicity",
        "wrong_source_zero_count",
        "wrong_graph_relation_count",
        "python_optimized_mode",
    }
    observed_mutations = {row.get("mutation") for row in results}
    require(required_mutations <= observed_mutations, "THETA2_FULL_MAP_MUTATION_COVERAGE_FAIL", sorted(required_mutations - observed_mutations))
    return {
        "payload_sha256": certificate["payload_sha256"],
        "rows": 2528,
        "polynomial_classes": 85,
        "certificate_kind": "full_map_Ti_strict_sign",
        "independent_replay_payload_sha256": replay["payload_sha256"],
        "mutation_payload_sha256": mutations["payload_sha256"],
        "mutation_count": len(results),
    }


def validate_runtime_evidence(project: Path = PROJECT) -> dict[str, Any]:
    """Separate current runtime bytes from quarantined legacy inputs."""

    for relative, expected in RUNTIME_EVIDENCE_SHA256.items():
        require(
            sha_file(project_file(relative, project)) == expected,
            "RUNTIME_EVIDENCE_FILE_DRIFT",
            relative,
        )
    for relative, expected in REVOKED_RESTORATION_RUNTIME_SHA256.items():
        require(
            sha_file(project_file(relative, project)) == expected,
            "REVOKED_RUNTIME_PROVENANCE_FILE_DRIFT",
            relative,
        )

    locator = corrected_locator(project)
    corrected_forest = locator["artifacts"].get(
        "restoration_v3_forest_certificate"
    )
    corrected_replay = locator["artifacts"].get("restoration_v3_replay")
    require(
        corrected_forest
        == {
            "path": "work/restoration_sign_reclassification/corrected_restoration_forest.json",
            "sha256": "43bd2be5e7626a954fc4fa4cf45e8d0e6483c947ddc9cba80f2b1a13351bc3a8",
        },
        "REVOKED_RUNTIME_CORRECTED_FOREST_REPLACEMENT_FAIL",
    )
    require(
        corrected_replay
        == {
            "path": "work/restoration_sign_reclassification/corrected_restoration_replay_certificate.json",
            "sha256": "24fa2e61f60610a8b24c4107ec7f866278f0cc671ca203d7aaa40a37bea291dd",
        },
        "REVOKED_RUNTIME_CORRECTED_REPLAY_REPLACEMENT_FAIL",
    )
    locator_paths = {row["path"] for row in locator["artifacts"].values()}
    require(
        not (set(REVOKED_RESTORATION_RUNTIME_SHA256) & locator_paths),
        "REVOKED_RUNTIME_PRESENT_IN_PROMOTION_LOCATOR",
    )
    manuscript = (
        project
        / "work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md"
    ).read_text(encoding="utf-8")
    require(
        not any(relative in manuscript for relative in REVOKED_RESTORATION_RUNTIME_SHA256),
        "REVOKED_RUNTIME_CITED_AS_THEOREM_AUTHORITY",
    )
    return {
        "runtime_evidence": {
            "status": "BOUND",
            "file_count": len(RUNTIME_EVIDENCE_SHA256),
            "ordered_file_hash_root": sha_object(RUNTIME_EVIDENCE_SHA256),
        },
        "historical_revoked_runtime_provenance": {
            "status": "QUARANTINED_NOT_PROMOTION_EVIDENCE",
            "file_count": len(REVOKED_RESTORATION_RUNTIME_SHA256),
            "promotion_eligible_files": 0,
            "ordered_file_hash_root": sha_object(
                REVOKED_RESTORATION_RUNTIME_SHA256
            ),
            "authoritative_forest_sha256": corrected_forest["sha256"],
            "authoritative_replay_sha256": corrected_replay["sha256"],
        },
    }


def validate_historical_artifact_registry(
    project: Path = PROJECT,
    registry_override: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Require every reviewed proof-like historical file to be quarantined."""

    registry = (
        registry_override
        if registry_override is not None
        else load_json(project / HISTORICAL_ARTIFACT_REGISTRY)
    )
    require(isinstance(registry, dict), "HISTORICAL_REGISTRY_SHAPE_FAIL")
    verify_payload_hash(registry)
    require(
        registry.get("schema") == "k2p-historical-proof-artifact-registry-v1",
        "HISTORICAL_REGISTRY_SCHEMA_FAIL",
    )
    require(registry.get("status") == "PASS", "HISTORICAL_REGISTRY_NOT_PASS")
    require(
        registry.get("authoritative_theorem_path")
        == "work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md",
        "HISTORICAL_REGISTRY_THEOREM_AUTHORITY_FAIL",
    )
    partitions = registry.get("release_partitions")
    require(
        isinstance(partitions, dict)
        and set(partitions)
        == {
            "authoritative_proof_inputs",
            "bound_historical_provenance",
            "bound_runtime_evidence",
        }
        and all(isinstance(value, str) and value for value in partitions.values()),
        "HISTORICAL_REGISTRY_RELEASE_PARTITIONS_FAIL",
    )

    expected: dict[str, dict[str, Any]] = {
        path: dict(row) for path, row in HISTORICAL_PROOF_ARTIFACTS.items()
    }
    for path, row in REVOKED_RESTORATION_RUNTIME_ARTIFACTS.items():
        expected[path] = {
            "sha256": REVOKED_RESTORATION_RUNTIME_SHA256[path],
            **row,
        }
    artifacts = registry.get("artifacts")
    require(
        isinstance(artifacts, list) and len(artifacts) == len(expected) == 8,
        "HISTORICAL_REGISTRY_ARTIFACT_CENSUS_FAIL",
    )
    observed_paths = [row.get("path") for row in artifacts if isinstance(row, dict)]
    require(
        observed_paths == sorted(expected),
        "HISTORICAL_REGISTRY_PATH_ORDER_OR_COVERAGE_FAIL",
    )

    locator_paths = {
        row["path"] for row in corrected_locator(project)["artifacts"].values()
    }
    replacement_allowlist = locator_paths | set(PROMOTION_MANUSCRIPT_FILES) | {
        "package/referee/k2p_offline_sweep_portable/proofs/four_port_direct_residual_closure_certificate.json"
    }
    for row in artifacts:
        path = row["path"]
        specification = expected[path]
        require(
            row.get("sha256") == specification["sha256"]
            and sha_file(project_file(path, project)) == specification["sha256"],
            "HISTORICAL_REGISTRY_FILE_BINDING_FAIL",
            path,
        )
        require(
            row.get("classification") == specification["classification"],
            "HISTORICAL_REGISTRY_CLASSIFICATION_FAIL",
            path,
        )
        require(
            row.get("promotion_authority") is False,
            "HISTORICAL_REGISTRY_PROMOTION_AUTHORITY_FAIL",
            path,
        )
        require(
            isinstance(row.get("reason"), str) and len(row["reason"]) >= 40,
            "HISTORICAL_REGISTRY_REASON_FAIL",
            path,
        )
        replacements = row.get("authoritative_replacements")
        require(
            replacements == specification["authoritative_replacements"],
            "HISTORICAL_REGISTRY_REPLACEMENT_FAIL",
            path,
        )
        require(
            all(
                replacement in replacement_allowlist
                and replacement not in expected
                and project_file(replacement, project).is_file()
                for replacement in replacements
            ),
            "HISTORICAL_REGISTRY_REPLACEMENT_NOT_AUTHORITATIVE",
            path,
        )

    scanner = registry.get("scanner")
    require(isinstance(scanner, dict), "HISTORICAL_REGISTRY_SCANNER_FAIL")
    require(
        scanner.get("scope") == "final_adversarial_narrative_review_v1"
        and scanner.get("scope_paths") == sorted(expected)
        and scanner.get("classified_count") == len(expected)
        and scanner.get("unclassified_count") == 0,
        "HISTORICAL_REGISTRY_SCANNER_COVERAGE_FAIL",
    )
    return {
        "status": "PASS",
        "payload_sha256": registry["payload_sha256"],
        "classified_artifacts": len(expected),
        "unclassified_proof_like_files": 0,
        "promotion_authority_files": 0,
        "classification_census": dict(
            sorted(Counter(row["classification"] for row in artifacts).items())
        ),
    }


def validate_promotion_manuscript(
    corrected_layer: dict[str, Any], project: Path = PROJECT
) -> dict[str, Any]:
    """Bind the final theorem text to the corrected finite-universe inputs."""

    for relative, expected in PROMOTION_MANUSCRIPT_FILES.items():
        require(
            sha_file(project_file(relative, project)) == expected,
            "PROMOTION_MANUSCRIPT_FILE_DRIFT",
            relative,
        )

    base = project / "work/global_theorem_closure/promotion_manuscript"
    manuscript = (base / "K2P_SAME_PROMOTION_MANUSCRIPT.md").read_text(
        encoding="utf-8"
    )
    quantifier = (base / "QUANTIFIER_AUDIT.md").read_text(encoding="utf-8")
    normalized_manuscript = re.sub(r"\s+", " ", manuscript)
    require("__PENDING_" not in manuscript + quantifier, "PROMOTION_PENDING_TOKEN")
    for marker in (
        "Theorems 8.3, 9.1, 10.1, 11.1, and 12.1 are therefore unconditional",
        "### Theorem 8.3 (K2P-SAME)",
        "### Theorem 9.1 (generic structural identifiability)",
        "### Theorem 10.1 (finite exact reconstruction)",
        "### Theorem 11.1 (continuous-time transfer)",
        "### Theorem 12.1 (weak-class \\(4n-3\\) ambiguity)",
        "Nothing here classifies any other stochastic sign component.",
        "Corrected 997-parent restoration forest",
    ):
        require(
            re.sub(r"\s+", " ", marker) in normalized_manuscript,
            "PROMOTION_MANUSCRIPT_MARKER_MISSING",
            marker,
        )
    for stale in (
        "Promotion still requires",
        "Promotion status: CONDITIONAL",
        "deliberately marked fail-closed",
    ):
        require(stale not in manuscript, "PROMOTION_MANUSCRIPT_STALE_MARKER", stale)

    claim_rows = {
        "Directed-containment classification",
        "No proper one-sided containment",
        "Common-germ sufficiency",
        "Generic identifiability",
        "Exact reconstruction",
        "Continuous-time transfer",
        "Weak sharpness",
    }
    observed_claims = {
        line.split("|", 2)[1].strip()
        for line in quantifier.splitlines()
        if line.startswith("|") and not line.startswith("|---")
    } - {"Claim"}
    require(observed_claims == claim_rows, "PROMOTION_QUANTIFIER_CLAIM_LEDGER_FAIL")
    require("- [ ]" not in quantifier, "PROMOTION_QUANTIFIER_UNCHECKED_ITEM")
    require(quantifier.count("- [x]") == 14, "PROMOTION_CHECKLIST_CENSUS_FAIL")
    require(
        "are all **PASS** under their exact stated hypotheses" in quantifier,
        "PROMOTION_QUANTIFIER_VERDICT_FAIL",
    )

    binding = load_json(base / "PROBE_PROMOTION_PLACEHOLDER.json")
    require(
        binding.get("schema") == "k2p-full-probe-promotion-placeholder-v1",
        "PROMOTION_PROBE_BINDING_SCHEMA_FAIL",
    )
    require(binding.get("promotion_status") == "PASS", "PROMOTION_PROBE_NOT_PASS")
    require("__PENDING_" not in json.dumps(binding), "PROMOTION_PROBE_PENDING_TOKEN")

    probe = corrected_layer.get("probe_producer")
    require(isinstance(probe, dict), "PROMOTION_CORRECTED_PROBE_LAYER_MISSING")
    expected_artifacts = {
        "primary": {
            "path": "work/probe_coherence_corrected/probe_coherence_certificate.json",
            "file_sha256": probe["certificate_file_sha256"],
            "payload_sha256": probe["certificate_payload_sha256"],
            "status": "PASS",
        },
        "independent_replay": {
            "path": "work/global_proof_adversary/probe_full_audit/independent_probe_graph_audit_certificate.json",
            "file_sha256": probe["adversarial_file_sha256"],
            "payload_sha256": probe["adversarial_payload_sha256"],
            "status": "PASS",
        },
        "mutation_report": {
            "path": "work/global_proof_adversary/probe_full_audit/independent_probe_mutation_report.json",
            "file_sha256": sha_file(
                project
                / "work/global_proof_adversary/probe_full_audit/independent_probe_mutation_report.json"
            ),
            "payload_sha256": probe["adversarial_mutation_payload_sha256"],
            "status": "PASS",
        },
    }
    require(binding.get("artifacts") == expected_artifacts, "PROMOTION_PROBE_ARTIFACT_BINDING_FAIL")
    expected_ledgers = {
        "one_port": (
            "work/probe_coherence_corrected/one_port_ledger.jsonl.gz",
            probe["one_port"]["ledger_sha256"],
        ),
        "two_port_parent_inventory": (
            "work/probe_coherence_corrected/two_port_parent_inventory.jsonl.gz",
            probe["two_port_parent_inventory_sha256"],
        ),
        "two_port": (
            "work/probe_coherence_corrected/two_port_ledger.jsonl.gz",
            probe["two_port"]["ledger_sha256"],
        ),
        "exact_transport": (
            "work/probe_coherence_corrected/exact_transport_ledger.jsonl.gz",
            probe["transport_registry"]["file_sha256"],
        ),
        "parent_restriction": (
            "work/probe_coherence_corrected/parent_restriction_ledger.jsonl.gz",
            probe["restriction_registry"]["file_sha256"],
        ),
        "separation_proof_registry": (
            "work/probe_coherence_corrected/separation_proof_registry.json.gz",
            probe["separation_registry_file_sha256"],
        ),
    }
    require(
        binding.get("bound_ledgers")
        == {
            name: {"path": path, "file_sha256": digest}
            for name, (path, digest) in expected_ledgers.items()
        },
        "PROMOTION_PROBE_LEDGER_BINDING_FAIL",
    )
    pass_gates = binding.get("required_pass_gates")
    zero_gates = binding.get("required_zero_gates")
    require(
        isinstance(pass_gates, dict)
        and len(pass_gates) == PROMOTION_GUARD_CENSUS["required_pass_gates"]
        and set(pass_gates.values()) == {"PASS"},
        "PROMOTION_PASS_GATE_FAIL",
    )
    require(
        isinstance(zero_gates, dict)
        and len(zero_gates) == PROMOTION_GUARD_CENSUS["required_zero_gates"]
        and all(type(value) is int and value == 0 for value in zero_gates.values()),
        "PROMOTION_ZERO_GATE_FAIL",
    )
    census = binding.get("census")
    require(isinstance(census, dict), "PROMOTION_PROBE_CENSUS_FAIL")
    require(
        census.get("one_port_directed_rows") == PROBE_INPUT_FIRST_PAIRS
        and census.get("two_port_directed_rows") == PROBE_TWO_PORT_PAIRS,
        "PROMOTION_PROBE_ROW_CENSUS_FAIL",
    )
    combined_root = sha_object(
        {
            "one_port_ordered_hash_root": probe["one_port"]["ordered_row_hash_root"],
            "two_port_parent_inventory_ordered_hash_root": probe[
                "two_port_parent_inventory_hash_root"
            ],
            "two_port_ordered_hash_root": probe["two_port"]["ordered_row_hash_root"],
        }
    )
    require(census.get("terminal_hash_root") == combined_root, "PROMOTION_PROBE_COMBINED_ROOT_FAIL")
    require(
        combined_root
        == "7868fed6f8e0c10fcb9740da8ffdcb7f64ea68939c99cba6f364da4cfd90bf50",
        "PROMOTION_PROBE_COMBINED_ROOT_CONSTANT_FAIL",
    )
    return {
        "status": "PASS",
        "scope": "principal_D_plus_only_no_mixed_sign_claim",
        "outcome": "K2P-SAME",
        "manuscript_sha256": PROMOTION_MANUSCRIPT_FILES[
            "work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md"
        ],
        "quantifier_audit_sha256": PROMOTION_MANUSCRIPT_FILES[
            "work/global_theorem_closure/promotion_manuscript/QUANTIFIER_AUDIT.md"
        ],
        "probe_binding_sha256": PROMOTION_MANUSCRIPT_FILES[
            "work/global_theorem_closure/promotion_manuscript/PROBE_PROMOTION_PLACEHOLDER.json"
        ],
        "promotion_guard_sha256": PROMOTION_MANUSCRIPT_FILES[
            "work/global_theorem_closure/promotion_manuscript/verify_promotion_gate.py"
        ],
        "promotion_guard_stdout_sha256": PROMOTION_GUARD_STDOUT_SHA256,
        "promotion_guard_census": PROMOTION_GUARD_CENSUS,
        "claim_rows": len(claim_rows),
        "checklist_items": 14,
        "probe_combined_root": combined_root,
    }


def legacy_partition_blockers(project: Path = PROJECT) -> list[str]:
    """Refuse downstream ledgers still derived from the revoked oracle.

    Raw-four and theta2 are governed by independently replayed whole-map
    overlays.  The remaining primitive packages must bind their local
    reclassification at their point of use.
    """

    specifications = (
        (
            "CYCLE",
            project
            / "work/cycle_three_port_closure/artifacts/cycle_three_port_summary.json",
            "tree_sunlet_reclassification",
            None,
        ),
        (
            "PROBE",
            project / "work/probe_coherence_closure/probe_certificate.json",
            "tree_sunlet_reclassification",
            None,
        ),
    )
    blockers: list[str] = []
    for label, path, field, legacy_rows in specifications:
        if not path.is_file():
            blockers.append(f"{label}_REGENERATED_LEDGER_MISSING")
            continue
        payload = load_json(path)
        marker = payload.get(field)
        if not isinstance(marker, dict):
            blockers.append(f"LEGACY_{label}_PARTITION_REVOKED")
            continue
        if marker.get("status") != "PASS":
            blockers.append(f"{label}_RECLASSIFICATION_NOT_PASS")
        if legacy_rows is not None and marker.get("legacy_rows") != legacy_rows:
            blockers.append(f"{label}_RECLASSIFICATION_INPUT_CENSUS_FAIL")
        if legacy_rows is not None and marker.get("reclassified_rows") != legacy_rows:
            blockers.append(f"{label}_RECLASSIFICATION_COVERAGE_FAIL")
        if legacy_rows is None:
            input_rows = marker.get("input_rows", marker.get("legacy_rows"))
            reclassified_rows = marker.get(
                "reclassified_rows", marker.get("output_rows")
            )
            if not isinstance(input_rows, int) or input_rows < 0:
                blockers.append(f"{label}_RECLASSIFICATION_INPUT_CENSUS_FAIL")
            elif reclassified_rows != input_rows:
                blockers.append(f"{label}_RECLASSIFICATION_COVERAGE_FAIL")
            category_counts = marker.get("output_category_counts")
            if (
                not isinstance(category_counts, dict)
                or not isinstance(input_rows, int)
                or not all(
                    isinstance(value, int) and value >= 0
                    for value in category_counts.values()
                )
                or sum(category_counts.values()) != input_rows
            ):
                blockers.append(f"{label}_RECLASSIFICATION_PARTITION_FAIL")
        if marker.get("unresolved") != 0:
            blockers.append(f"{label}_RECLASSIFICATION_UNRESOLVED")
        if not isinstance(marker.get("truth_certificate_sha256"), str):
            blockers.append(f"{label}_RECLASSIFICATION_TRUTH_BINDING_MISSING")
    if blockers:
        blockers.append("DOWNSTREAM_TREE_SUNLET_PARTITIONS_NOT_PROMOTABLE")
    return blockers


def validate_quartet_evidence(project: Path = PROJECT) -> dict[str, object]:
    """Bind the literal K2P quartet algebra to every terminal registry use."""

    root = project / "work/quartet_separation_closure"
    spec_path = root / "QUARTET_SEMANTICS_SPEC.json"
    spec = load_json(spec_path)
    require(
        spec.get("schema") == "k2p-quartet-semantics-spec-v2",
        "QUARTET_SPEC_SCHEMA_FAIL",
    )
    require(
        spec.get("character_order") == ["0", "C", "G", "T"]
        and spec.get("group_codes") == {"0": 0, "C": 1, "G": 2, "T": 3}
        and spec.get("edge_spectrum")
        == {"0": "1", "C": "s", "G": "g", "T": "s"}
        and spec.get("equal_nonzero_sector") == ["C", "T"]
        and spec.get("singleton_nonzero_sector") == ["G"],
        "QUARTET_SPEC_CHARACTER_CONVENTION_FAIL",
    )
    require(
        spec.get("domain")
        == {
            "principal": "0<s<1, 0<g<1, g>2s-1",
            "strict_continuous_time": "0<s<1, s^2<g<1",
        },
        "QUARTET_SPEC_DOMAIN_FAIL",
    )
    require(
        spec.get("canonical_coordinates")
        == {"Q0": "CCCC", "QA": "CCTT", "QB": "CTCT", "QC": "CTTC"},
        "QUARTET_SPEC_COORDINATE_FAIL",
    )
    require(
        spec.get("canonical_formulas")
        == {
            "F_A": [[1, "CCCC"], [-1, "CCTT"]],
            "F_B": [[1, "CCCC"], [-1, "CTCT"]],
            "F_C": [[1, "CCCC"], [-1, "CTTC"]],
            "J_A": [[1, "CCCC"], [1, "CCTT"], [-1, "CTCT"], [-1, "CTTC"]],
            "J_B": [[1, "CCCC"], [-1, "CCTT"], [1, "CTCT"], [-1, "CTTC"]],
            "J_C": [[1, "CCCC"], [-1, "CCTT"], [-1, "CTCT"], [1, "CTTC"]],
        },
        "QUARTET_SPEC_FORMULA_FAIL",
    )

    quartet_path = root / "quartet_logic_certificate.json"
    quartet = load_json(quartet_path)
    verify_payload_hash(quartet)
    require(
        quartet.get("schema") == "k2p-displayed-quartet-semantics-v2"
        and quartet.get("status") == "PASS",
        "QUARTET_SCHEMA_FAIL",
    )
    require(
        quartet.get("spec_path")
        == "work/quartet_separation_closure/QUARTET_SEMANTICS_SPEC.json"
        and quartet.get("spec_sha256") == sha_file(spec_path),
        "QUARTET_SPEC_BINDING_FAIL",
    )
    require(
        quartet.get("character_order") == ["0", "C", "G", "T"]
        and quartet.get("edge_spectrum") == ["1", "s", "g", "s"]
        and quartet.get("equal_nonzero_sector") == ["C", "T"]
        and quartet.get("singleton_nonzero_sector") == ["G"]
        and quartet.get("domain") == spec["domain"],
        "QUARTET_CERTIFICATE_CONVENTION_FAIL",
    )
    require(
        quartet.get("canonical_formula_count") == 6
        and len(quartet.get("canonical_formulas", {})) == 6
        and quartet.get("formula_transport_count") == 288
        and len(quartet.get("formula_transports", [])) == 288
        and quartet.get("displayed_set_count") == 7
        and quartet.get("unequal_pair_count") == 21
        and len(quartet.get("displayed_set_witnesses", [])) == 21,
        "QUARTET_CERTIFICATE_CENSUS_FAIL",
    )
    documents = quartet.get("document_sha256")
    expected_document_paths = {
        "proof_compression_submission/article/main.tex",
        "work/adversarial_proof_review/TOPOLOGY_DIRECTIONAL_THEOREM.md",
        "work/global_theorem_closure/GLOBAL_PROOF.md",
        "work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md",
        "work/quartet_separation_closure/PROOF.md",
    }
    require(
        isinstance(documents, dict)
        and set(documents) == expected_document_paths
        == {
            row["path"] for row in spec.get("document_contracts", [])
        },
        "QUARTET_DOCUMENT_BINDING_SET_FAIL",
    )
    for relative, digest in documents.items():
        require(
            sha_file(project_file(relative, project)) == digest,
            "QUARTET_DOCUMENT_BINDING_HASH_FAIL",
            relative,
        )

    semantic_mutations = load_json(
        root / "quartet_semantics_mutation_certificate.json"
    )
    verify_payload_hash(semantic_mutations)
    require(
        semantic_mutations.get("schema") == "k2p-quartet-semantics-mutations-v2"
        and semantic_mutations.get("status") == "PASS"
        and semantic_mutations.get("verifier_sha256")
        == sha_file(root / "verify_quartet_logic.py")
        and semantic_mutations.get("spec_sha256") == sha_file(spec_path)
        and semantic_mutations.get("case_count") == 8,
        "QUARTET_SEMANTIC_MUTATION_BINDING_FAIL",
    )
    semantic_case_names = [
        "spectrum_G_T_swap",
        "wrong_F_coordinate",
        "wrong_J_coefficient",
        "wrong_character_order",
        "wrong_coordinate_dictionary",
        "wrong_D_plus_declaration",
        "printed_formula_reverted_to_wrong_sector",
        "optimized_python",
    ]
    require(
        [row.get("case") for row in semantic_mutations.get("cases", [])]
        == semantic_case_names
        and all(
            row.get("status") == "PASS"
            and isinstance(row.get("expected_marker"), str)
            and row.get("observed_returncode") != 0
            for row in semantic_mutations.get("cases", [])
        ),
        "QUARTET_SEMANTIC_MUTATION_CENSUS_FAIL",
    )

    terminal_path = root / "quartet_terminal_binding_certificate.json"
    terminal = load_json(terminal_path)
    verify_payload_hash(terminal)
    require(
        terminal.get("schema") == "k2p-quartet-terminal-binding-v1"
        and terminal.get("status") == "PASS"
        and terminal.get("imports_graph_or_classifier_code") is False,
        "QUARTET_TERMINAL_SCHEMA_FAIL",
    )
    semantics_binding = terminal.get("semantics_certificate")
    require(
        isinstance(semantics_binding, dict)
        and semantics_binding.get("path")
        == "work/quartet_separation_closure/quartet_logic_certificate.json"
        and semantics_binding.get("sha256") == sha_file(quartet_path)
        and semantics_binding.get("payload_sha256") == quartet["payload_sha256"]
        and semantics_binding.get("spec_sha256") == sha_file(spec_path)
        and semantics_binding.get("canonical_formula_count") == 6
        and semantics_binding.get("formula_transport_count") == 288,
        "QUARTET_TERMINAL_SEMANTICS_BINDING_FAIL",
    )
    require(
        terminal.get("coordinate_convention")
        == {
            "character_order": ["0", "C", "G", "T"],
            "edge_spectrum": ["1", "s", "g", "s"],
            "equal_nonzero_sector": ["C", "T"],
            "singleton_nonzero_sector": ["G"],
            "unlisted_marginal_leaf_characters": "0",
        },
        "QUARTET_TERMINAL_CONVENTION_FAIL",
    )
    aggregate = terminal.get("aggregate")
    require(
        isinstance(aggregate, dict)
        and aggregate.get("layer_count") == 6
        and aggregate.get("quartet_terminal_rows") == 4_414_710
        and aggregate.get("per_layer_certificate_ids") == 888
        and aggregate.get("all_registry_certificates_used") is True
        and aggregate.get("missing_references") == 0
        and aggregate.get("dangling_certificates") == 0,
        "QUARTET_TERMINAL_AGGREGATE_FAIL",
    )
    layer_census = {
        "raw4": (360_408, 18),
        "theta2": (2_942_592, 19),
        "theta2_restoration": (760, 24),
        "cycle": (535_920, 97),
        "restoration": (36_006, 92),
        "probe": (539_024, 638),
    }
    terminal_layers = terminal.get("layers")
    require(
        isinstance(terminal_layers, dict) and set(terminal_layers) == set(layer_census),
        "QUARTET_TERMINAL_LAYER_SET_FAIL",
    )
    for name, (rows, certificates) in layer_census.items():
        layer = terminal_layers[name]
        require(
            layer.get("quartet_terminal_rows") == rows
            and layer.get("certificate_count") == certificates,
            "QUARTET_TERMINAL_LAYER_CENSUS_FAIL",
            name,
        )

    terminal_mutations = load_json(
        root / "quartet_terminal_binding_mutation_certificate.json"
    )
    verify_payload_hash(terminal_mutations)
    terminal_case_names = [
        "resealed_spectrum_convention_mutation",
        "resealed_coordinate_word_mutation",
        "resealed_distinguished_split_mutation",
        "resealed_zero_positive_side_mutation",
        "resealed_quartet_label_transport_mutation",
        "rekeyed_relinked_restoration_set_mutation",
        "compact_split_hash_mutation",
        "unknown_terminal_reference",
        "omitted_terminal_reference",
        "valid_proof_substitution_composed_graph_gate",
        "complete_source_target_reversal_composed_graph_gate",
        "optimized_python",
    ]
    require(
        terminal_mutations.get("schema")
        == "k2p-quartet-terminal-binding-mutations-v1"
        and terminal_mutations.get("status") == "PASS"
        and terminal_mutations.get("case_count") == 12
        and terminal_mutations.get("binder_sha256")
        == sha_file(root / "verify_quartet_terminal_bindings.py")
        and terminal_mutations.get("semantics_certificate_sha256")
        == sha_file(quartet_path)
        and terminal_mutations.get("authoritative_ledgers_modified") is False
        and terminal_mutations.get("temporary_in_memory_or_temp_directory_mutations_only")
        is True
        and [row.get("case") for row in terminal_mutations.get("cases", [])]
        == terminal_case_names
        and all(row.get("status") == "PASS" for row in terminal_mutations.get("cases", [])),
        "QUARTET_TERMINAL_MUTATION_FAIL",
    )
    composed_cases = {
        row["case"]: row
        for row in terminal_mutations["cases"]
        if row["case"]
        in {
            "valid_proof_substitution_composed_graph_gate",
            "complete_source_target_reversal_composed_graph_gate",
        }
    }
    require(
        set(composed_cases)
        == {
            "valid_proof_substitution_composed_graph_gate",
            "complete_source_target_reversal_composed_graph_gate",
        }
        and all(
            [(guard.get("family"), guard.get("rejected")) for guard in row.get("graph_guards", [])]
            == [("raw4", True), ("theta2", True)]
            for row in composed_cases.values()
        ),
        "QUARTET_TERMINAL_COMPOSED_GRAPH_GUARD_FAIL",
    )
    return {
        "semantics_payload_sha256": quartet["payload_sha256"],
        "terminal_binding_payload_sha256": terminal["payload_sha256"],
        "formula_transports": 288,
        "displayed_set_pairs": 21,
        "quartet_terminal_rows": 4_414_710,
        "terminal_certificate_ids": 888,
        "semantic_mutations": 8,
        "terminal_binding_mutations": 12,
        "unresolved": 0,
    }


def validate_canonicalizer_evidence(project: Path = PROJECT) -> dict[str, object]:
    """Validate the complete licensed orbit and strict-relation comparison."""

    root = project / "work/canonicalizer_completeness"
    certificate = load_json(root / "canonicalizer_completeness_certificate.json")
    verify_payload_hash(certificate)
    require(
        certificate.get("schema") == "k2p-canonicalizer-completeness-v1"
        and certificate.get("status") == "PASS",
        "CANONICALIZER_COMPLETENESS_SCHEMA_FAIL",
    )
    inputs = certificate.get("inputs")
    require(
        isinstance(inputs, dict)
        and inputs.get("atlas_sha256")
        == sha_file(project / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py")
        and inputs.get("auditor_sha256") == sha_file(root / "canonicalizer_audit.py")
        and inputs.get("raw_ledger_sha256")
        == sha_file(project / "work/raw_ledger_audit/artifacts/raw_directional_ledger.jsonl.gz"),
        "CANONICALIZER_COMPLETENESS_INPUT_BINDING_FAIL",
    )
    descriptor = certificate.get("descriptor_audit")
    relation = certificate.get("relation_audit")
    require(
        isinstance(descriptor, dict)
        and descriptor.get("primitive_archetypes_compared") == 10_084
        and descriptor.get("slow_fast_disagreements") == 0
        and descriptor.get("primitive_archetype_families")
        == {
            "raw4_sources": 6,
            "raw4_targets": 2_814,
            "theta2_sources": 4,
            "theta2_targets": 6_138,
            "cycle_sources": 2,
            "cycle_targets": 1_120,
        },
        "CANONICALIZER_DESCRIPTOR_CENSUS_FAIL",
    )
    require(
        isinstance(relation, dict)
        and relation.get("rank_and_topology_eligible_presentations") == 4_012
        and relation.get("disagreements") == 0
        and relation.get("strict_triangle_presentations") == 54
        and relation.get("strict_relation_status_triples")
        == {
            "isomorphic/isomorphic/isomorphic": 26,
            "none/none/none": 3_932,
            "triangle/triangle/triangle": 54,
        },
        "CANONICALIZER_RELATION_CENSUS_FAIL",
    )
    semantic_contract = certificate.get("semantic_mutation_contract")
    require(
        isinstance(semantic_contract, dict)
        and semantic_contract.get("nonordinary_triangle", {}).get("conclusion")
        == "rejected"
        and semantic_contract.get("selected_triangle_mismatch", {}).get("conclusion")
        == "rejected",
        "CANONICALIZER_SEMANTIC_CONTRACT_FAIL",
    )
    mutations = load_json(
        root / "canonicalizer_completeness_mutation_certificate.json"
    )
    verify_payload_hash(mutations)
    require(
        mutations.get("schema") == "k2p-canonicalizer-completeness-mutations-v1"
        and mutations.get("status") == "PASS"
        and mutations.get("atlas_sha256") == inputs["atlas_sha256"]
        and mutations.get("auditor_sha256") == inputs["auditor_sha256"]
        and mutations.get("rejected") == 2
        and mutations.get("survived") == 0
        and [row.get("name") for row in mutations.get("mutations", [])]
        == ["accept_nonordinary_split_heads", "erase_without_marking_selected_triangle"]
        and all(
            row.get("rejected") is True and row.get("exit_code") != 0
            for row in mutations.get("mutations", [])
        ),
        "CANONICALIZER_MUTATION_FAIL",
    )
    return {
        "payload_sha256": certificate["payload_sha256"],
        "primitive_archetypes_compared": 10_084,
        "strict_relations_compared": 4_012,
        "strict_relation_disagreements": 0,
        "mutations_rejected": 2,
    }


def validate_parameter_transport_evidence(project: Path = PROJECT) -> dict[str, object]:
    """Bind paired edge products and every graph-derived inheritance action."""

    root = project / "work/canonicalizer_completeness/inheritance_transport"
    certificate = load_json(root / "parameter_transport_certificate.json")
    verify_payload_hash(certificate)
    require(
        certificate.get("schema")
        == "k2p_graph_derived_parameter_transport_certificate_v1"
        and certificate.get("status") == "PASS",
        "PARAMETER_TRANSPORT_SCHEMA_FAIL",
    )
    inputs = certificate.get("inputs")
    expected_inputs = {
        "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py",
        "work/adversarial_proof_review/probe_input_contract.json",
        "work/adversarial_proof_review/verify_probe_input_contract.py",
        "work/canonicalizer_completeness/inheritance_transport/build_parameter_transport_certificate.py",
        "work/canonicalizer_completeness/inheritance_transport/run_parameter_transport_mutations.py",
        "work/canonicalizer_completeness/inheritance_transport/verify_parameter_transport_certificate.py",
        "work/cycle_three_port_closure/cycle_common.py",
        "work/cycle_three_port_closure/generate_cycle_closure.py",
        "work/global_proof_adversary/probe_full_audit/independent_probe_graph_audit.py",
        "work/probe_coherence_corrected/exact_transport_ledger.jsonl.gz",
        "work/probe_coherence_corrected/one_port_ledger.jsonl.gz",
        "work/probe_coherence_corrected/parent_restriction_ledger.jsonl.gz",
        "work/probe_coherence_corrected/two_port_ledger.jsonl.gz",
        "work/probe_coherence_corrected/two_port_parent_inventory.jsonl.gz",
        "work/restoration_forest/enumerate_five_port.py",
        "work/restoration_sign_reclassification/corrected_restoration_forest.json",
    }
    require(
        isinstance(inputs, dict) and set(inputs) == expected_inputs,
        "PARAMETER_TRANSPORT_INPUT_SET_FAIL",
    )
    for relative, record in inputs.items():
        path = project_file(relative, project)
        require(
            isinstance(record, dict)
            and record.get("bytes") == path.stat().st_size
            and record.get("sha256") == sha_file(path),
            "PARAMETER_TRANSPORT_INPUT_BINDING_FAIL",
            relative,
        )
    ledgers = certificate.get("ledgers")
    expected_ledgers = {
        "probe_relations": (
            "probe_relation_parameter_transports.jsonl.gz",
            67_741,
            {
                "inheritance:complement": 36_743,
                "inheritance:identity": 91_530,
                "inheritance:triangle_local_section": 3_745,
                "occurrence:probe_anchor": 176,
                "occurrence:probe_one_port_equality": 2_107,
                "occurrence:probe_reverse_one_port_marginal": 32_729,
                "occurrence:probe_two_port_equality": 32_729,
            },
        ),
        "probe_restrictions": (
            "probe_restriction_parameter_transports.jsonl.gz",
            71_022,
            {
                "inheritance:complement": 8_660,
                "inheritance:identity": 129_376,
                "occurrence:probe_one_port_restriction": 4_412,
                "occurrence:probe_two_port_restriction": 66_610,
            },
        ),
        "restoration_restrictions": (
            "restoration_restriction_parameter_transports.jsonl.gz",
            5_540,
            {
                "inheritance:complement": 1_754,
                "inheritance:identity": 9_326,
                "inheritance:root_suppressed_incoming": 548,
                "occurrence:restoration_first_source_restriction": 42,
                "occurrence:restoration_first_target_restriction": 4_986,
                "occurrence:restoration_second_source_restriction": 256,
                "occurrence:restoration_second_target_restriction": 256,
            },
        ),
    }
    require(
        isinstance(ledgers, dict) and set(ledgers) == set(expected_ledgers),
        "PARAMETER_TRANSPORT_LEDGER_SET_FAIL",
    )
    for key, (filename, rows, counts) in expected_ledgers.items():
        record = ledgers[key]
        path = root / filename
        require(
            record.get("path") == filename
            and record.get("rows") == rows
            and record.get("counts") == counts
            and record.get("bytes") == path.stat().st_size
            and record.get("sha256") == sha_file(path),
            "PARAMETER_TRANSPORT_LEDGER_BINDING_FAIL",
            key,
        )
    closure = certificate.get("closure")
    require(
        closure
        == {
            "all_exact_transport_records_used": 67_741,
            "all_frozen_parent_restriction_records_used": 4_379,
            "restoration_canonical_parents": 997,
            "restoration_first_source_classes": 42,
            "restoration_first_target_classes": 4_986,
            "restoration_member_roots": 2_540,
            "restoration_second_edges": 256,
            "unresolved_parameter_transports": 0,
        },
        "PARAMETER_TRANSPORT_CLOSURE_FAIL",
    )
    mutations = load_json(root / "parameter_transport_mutation_report.json")
    verify_payload_hash(mutations)
    mutation_names = [
        "required_complement_removed",
        "illicit_complement_injected",
        "parent_order_reversal_unpaired",
        "triangle_reticulation_false_affine_map",
        "triangle_edge_false_product_map",
        "restriction_complement_removed",
        "serial_product_factor_omitted",
        "paired_s_g_action_broken",
        "root_suppressed_incoming_incidence_hidden",
        "source_target_reversal_without_inverse_transport",
    ]
    require(
        mutations.get("schema") == "k2p_parameter_transport_mutations_v1"
        and mutations.get("status") == "PASS"
        and mutations.get("certificate_payload_sha256") == certificate["payload_sha256"]
        and mutations.get("rejected") == 10
        and mutations.get("survived") == 0
        and [row.get("name") for row in mutations.get("cases", [])] == mutation_names
        and all(
            row.get("status") == "REJECTED"
            and row.get("rederived_exact_row_mismatch") is True
            for row in mutations.get("cases", [])
        ),
        "PARAMETER_TRANSPORT_MUTATION_FAIL",
    )
    return {
        "payload_sha256": certificate["payload_sha256"],
        "probe_relation_records": 67_741,
        "probe_restriction_occurrences": 71_022,
        "restoration_restriction_occurrences": 5_540,
        "unresolved": 0,
        "mutations_rejected": 10,
    }


def validate_semantics(project: Path = PROJECT) -> tuple[dict[str, object], list[str]]:
    """Validate all current certificate ledgers and return promotion blockers."""

    blockers: list[str] = []
    layers: dict[str, object] = {}

    domain = load_json(project / "work/domain_rooting_closure/domain_rooting_certificate.json")
    verify_payload_hash(domain)
    require(domain.get("schema") == "k2p-domain-rooting-v1", "DOMAIN_SCHEMA_FAIL")
    require(domain.get("rational_grid_checks") == 1444, "DOMAIN_GRID_CENSUS_FAIL")
    layers["domain_rooting"] = {"payload_sha256": domain["payload_sha256"]}

    runtime_partitions = validate_runtime_evidence(project)
    layers["runtime_evidence"] = runtime_partitions["runtime_evidence"]
    layers["historical_revoked_runtime_provenance"] = runtime_partitions[
        "historical_revoked_runtime_provenance"
    ]
    layers["historical_artifact_registry"] = (
        validate_historical_artifact_registry(project)
    )

    triangle = load_json(HERE / "triangle_sunlet_certificate.json")
    verify_payload_hash(triangle)
    require(triangle.get("status") == "PASS", "THREE_PORT_NO_ASSERT_NOT_PASS")
    require(
        triangle.get("rank_nine_split", {}).get("product") == "1/8",
        "THREE_PORT_RANK_SPLIT_FAIL",
    )
    triangle_source = (HERE / "no_assert_triangle_sunlet.py").read_text(
        encoding="utf-8"
    )
    require(
        not any(
            isinstance(node, ast.Assert)
            for node in ast.walk(ast.parse(triangle_source))
        ),
        "THREE_PORT_REPLAYER_CONTAINS_ASSERT_STATEMENT",
    )
    layers["three_port"] = {"payload_sha256": triangle["payload_sha256"]}

    layers["quartet_tree_of_blobs"] = validate_quartet_evidence(project)
    layers["canonicalizer_completeness"] = validate_canonicalizer_evidence(project)
    layers["parameter_transport"] = validate_parameter_transport_evidence(project)

    bridge = load_json(project / "work/bridge_marginal_closure/certificate.json")
    verify_payload_hash(bridge)
    require(
        bridge.get("schema") == "k2p-bridge-marginal-regression-v1",
        "BRIDGE_SCHEMA_FAIL",
    )
    adversarial = load_json(project / "work/adversarial_proof_review/audit_certificate.json")
    verify_payload_hash(adversarial)
    require(adversarial.get("status") == "PASS", "ANALYTIC_ADVERSARIAL_NOT_PASS")
    layers["bridge_marginal_gluing"] = {
        "primary_payload_sha256": bridge["payload_sha256"],
        "adversarial_payload_sha256": adversarial["payload_sha256"],
    }
    component_scale = load_json(
        project / "work/global_proof_adversary/component_scale_certificate.json"
    )
    verify_payload_hash(component_scale)
    require(
        component_scale.get("schema") == "k2p-global-component-scale-audit-v1",
        "GLOBAL_COMPONENT_SCALE_SCHEMA_FAIL",
    )
    require(component_scale.get("status") == "PASS", "GLOBAL_COMPONENT_SCALE_NOT_PASS")
    require(
        component_scale.get("scope")
        == "principal D_plus strong-class bridge components; no finite relation claim",
        "GLOBAL_COMPONENT_SCALE_SCOPE_FAIL",
    )
    require(
        component_scale.get("atlas_sha256")
        == sha_file(
            project
            / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
        ),
        "GLOBAL_COMPONENT_SCALE_ATLAS_BINDING_FAIL",
    )
    symmetry = component_scale.get("symmetry_constraints")
    require(isinstance(symmetry, dict) and symmetry.get("status") == "PASS", "GLOBAL_COMPONENT_SCALE_SYMMETRY_FAIL")
    unmarked = symmetry.get("unmarked")
    require(
        isinstance(unmarked, list)
        and len(unmarked) == 8
        and unmarked[0] == {"constraint_rank": 1, "degree": 2, "kernel_dimension": 1}
        and all(
            row == {
                "constraint_rank": degree,
                "degree": degree,
                "kernel_dimension": 0,
            }
            for degree, row in zip(range(3, 10), unmarked[1:])
        ),
        "GLOBAL_COMPONENT_SCALE_UNMARKED_RANK_FAIL",
    )
    primitive_supports = component_scale.get("primitive_supports")
    require(
        isinstance(primitive_supports, dict)
        and primitive_supports.get("status") == "PASS"
        and primitive_supports.get("ordinary_tree_minimum_ports") == 3
        and primitive_supports.get("rows")
        == [
            {"core": "cycle", "minimum_physical_boundary_ports": 3, "rigid_supports": 2},
            {"core": "theta0", "minimum_physical_boundary_ports": 4, "rigid_supports": 2},
            {"core": "theta1", "minimum_physical_boundary_ports": 4, "rigid_supports": 2},
            {"core": "theta2", "minimum_physical_boundary_ports": 5, "rigid_supports": 4},
            {"core": "theta3", "minimum_physical_boundary_ports": 4, "rigid_supports": 2},
        ],
        "GLOBAL_COMPONENT_SCALE_PRIMITIVE_SUPPORT_FAIL",
    )
    k4_minus_edge = component_scale.get("K4_minus_edge_exclusion")
    require(
        isinstance(k4_minus_edge, dict)
        and k4_minus_edge.get("status") == "PASS"
        and k4_minus_edge.get("rooted_binary_DAG_presentations") == 25
        and k4_minus_edge.get("tree_child_presentations") == 0,
        "GLOBAL_COMPONENT_SCALE_K4_MINUS_EDGE_FAIL",
    )
    layers["global_analytic_audit"] = {
        "component_scale_payload_sha256": component_scale["payload_sha256"],
        "audit_sha256": sha_file(project / "work/global_proof_adversary/AUDIT.md"),
        "finite_gate_dependency": "PASS_CONDITIONAL_ON_CORRECTED_FINITE_UNIVERSE",
    }

    raw = load_json(project / "work/raw_ledger_audit/artifacts/raw_ledger_summary.json")
    verify_payload_hash(raw, "payload_sha256_without_hash")
    primitive = raw.get("primitive_counts", {})
    require(primitive.get("raw_total") == RAW_FOUR_TOTAL, "RAW4_TOTAL_FAIL")
    rank = load_json(project / "work/rank_upper_certificates/rank_upper_replay.json")
    require(rank.get("status") == "pass", "RANK_REPLAY_NOT_PASS")
    require(rank.get("descriptor_count") == 4379, "RANK_DESCRIPTOR_COUNT_FAIL")
    require(rank.get("zero_unresolved") is True, "RANK_UNRESOLVED_FAIL")
    require(rank.get("base_recomputed") is True, "RANK_BASE_NOT_RECOMPUTED")
    rank_mutations = load_json(project / "work/rank_upper_certificates/mutation_report.json")
    require(rank_mutations.get("status") == "pass", "RANK_MUTATIONS_NOT_PASS")
    require(rank_mutations.get("survivors") == 0, "RANK_MUTATION_SURVIVOR")
    raw_mutations = load_json(
        project / "work/raw_ledger_audit/artifacts/raw_ledger_mutation_report.json"
    )
    require(raw_mutations.get("status") == "PASS", "RAW4_MUTATIONS_NOT_PASS")
    require(raw_mutations.get("survivors") == 0, "RAW4_MUTATION_SURVIVOR")
    layers["four_port_legacy_provenance"] = {
        "raw_total": RAW_FOUR_TOTAL,
        "rank_descriptors": 4379,
        "rank_unresolved": 0,
        "coverage_status": "REVOKED_PARTITION_NOT_USED_FOR_PROMOTION",
    }

    corrected_layer, corrected_blockers = validate_corrected_finite_universe(project)
    layers["corrected_four_port_finite_universe"] = corrected_layer
    blockers.extend(corrected_blockers)

    direct = load_json(
        project
        / "package/referee/k2p_offline_sweep_portable/proofs/four_port_direct_residual_closure_certificate.json"
    )
    verify_payload_hash(direct, "payload_sha256_without_hash")
    require(direct.get("remaining_unproved_among_36") == 0, "DIRECT36_UNPROVED_FAIL")
    require(direct.get("binding_gaps") in (0, []), "DIRECT36_BINDING_GAP")
    require(
        direct.get("proof_family_counts")
        == {
            "lower_theta_quartic": 12,
            "theta0_quintic_port_orbit": 22,
            "theta3_cubic": 2,
        },
        "DIRECT36_FAMILY_CENSUS_FAIL",
    )
    coverage = direct.get("coverage")
    require(isinstance(coverage, list) and len(coverage) == 36, "DIRECT36_COVERAGE_FAIL")
    require(
        Counter(row.get("family") for row in coverage) == Counter(direct["proof_family_counts"]),
        "DIRECT36_FAMILY_ASSIGNMENT_FAIL",
    )
    require(
        all(row.get("target_pullback_zero") is True for row in coverage),
        "DIRECT36_TARGET_PULLBACK_FAIL",
    )
    layers["four_port_direct36_standalone"] = {
        "candidate_count": 36,
        "family_counts": direct["proof_family_counts"],
        "remaining_unproved": 0,
        "coverage_status": "STANDALONE_CERTIFICATES_NOT_A_COMPLETENESS_PARTITION",
    }

    theta2 = load_json(
        project / "work/theta2_five_port_closure/artifacts/theta2_five_port_summary.json"
    )
    verify_payload_hash(theta2, "payload_sha256_without_hash")
    require(
        theta2.get("primitive_counts", {}).get("raw_total") == THETA2_TOTAL,
        "THETA2_RAW_TOTAL_FAIL",
    )
    require(theta2.get("unresolved_class_count") == 0, "THETA2_UNRESOLVED_FAIL")
    require(sum(theta2.get("class_partition", {}).values()) == 480, "THETA2_CLASS_COUNT_FAIL")
    layers["theta2_legacy_provenance"] = {
        "raw_total": THETA2_TOTAL,
        "classes": 480,
        "unresolved": 0,
        "coverage_status": "HISTORICAL_ROOTED_PARTITION_NOT_USED_FOR_PROMOTION",
    }
    layers["theta2_full_map_truth"] = validate_theta2_full_map_truth(project)

    cycle = load_json(
        project / "work/cycle_three_port_closure/artifacts/cycle_three_port_summary.json"
    )
    verify_payload_hash(cycle)
    require(cycle.get("status") == "PASS", "CYCLE_STATUS_FAIL")
    require(
        cycle.get("restoration", {}).get("unresolved") == 0,
        "CYCLE_UNRESOLVED_FAIL",
    )
    layers["cycle_three_port_legacy_provenance"] = {
        "base_raw": cycle.get("base", {}).get("raw_relations"),
        "restoration_raw": cycle.get("restoration", {}).get("physical_completions"),
        "physical_anchors": cycle.get("physical_anchors", {}).get("total"),
        "unresolved": 0,
        "coverage_status": "HISTORICAL_ROOTED_PARTITION_NOT_USED_FOR_PROMOTION",
    }

    locator = corrected_locator(project)
    layers["historical_downstream_truth_paths"] = {
        "status": "NOT_PROMOTION_EVIDENCE",
        "replacement_locator_status": locator["status"],
    }

    primary_sharpness = load_json(
        project / "work/weak_sharpness_closure/weak_sharpness_certificate.json"
    )
    verify_payload_hash(primary_sharpness)
    independent_sharpness = load_json(
        project / "work/weak_sharpness_audit/audit_certificate.json"
    )
    verify_payload_hash(independent_sharpness)
    require(
        primary_sharpness.get("cherry_extension", {}).get("dimension_formula")
        == "9+4*(n-3)=4*n-3",
        "SHARPNESS_DIMENSION_FAIL",
    )
    require(
        independent_sharpness.get("cherry", {}).get("iteration_dimension")
        == "9+4*(n-3)=4*n-3",
        "SHARPNESS_AUDIT_DIMENSION_FAIL",
    )
    layers["weak_sharpness"] = {
        "primary_payload_sha256": primary_sharpness["payload_sha256"],
        "independent_payload_sha256": independent_sharpness["payload_sha256"],
        "dimension": "4*n-3",
    }

    layers["theorem_promotion"] = validate_promotion_manuscript(
        corrected_layer, project
    )
    return layers, sorted(set(blockers))


def lock_payload(project: Path = PROJECT) -> dict[str, Any]:
    files, missing = build_file_ledger(project)
    try:
        nested = validate_nested_manifests(project)
    except ReleaseFailure as error:
        nested = {"validation_error": str(error)}
    try:
        layers, blockers = validate_semantics(project)
    except ReleaseFailure as error:
        layers, blockers = {}, [str(error)]
    blockers.extend(declared_corrected_locator_blockers(project))
    blockers.extend(f"MISSING_REQUIRED_FILE:{relative}" for relative in missing)
    if "validation_error" in nested:
        blockers.append(f"NESTED_MANIFEST_FAIL:{nested['validation_error']}")
    blockers = sorted(set(blockers))
    payload: dict[str, Any] = {
        "schema": LOCK_SCHEMA,
        "candidate_outcome": EXPECTED_OUTCOME,
        "scope": "binary strongly tree-child level-2 semi-directed networks under K2P on the principal D_plus domain; strict continuous-time corollary; no mixed-sign claim",
        "promotion_ready": not blockers,
        "blockers": blockers,
        "missing_required_files": missing,
        "files": files,
        "nested_manifests": nested,
        "layers": layers,
        "execution_policy": {
            "python_optimized_mode": "forbidden and explicitly rejected",
            "quick": "hashes, nested manifests, full structural certificate scans, literal quartet terminal rebinding, canonicalizer semantic replay, graph-derived parameter-transport scan, independent three-port arithmetic, and non-generative package replays",
            "full": "quick plus complete canonicalizer comparison, graph-derived parameter-transport regeneration, primitive regeneration, exact rank recomputation, direct overlay full qualification, restoration regeneration, theta2 regeneration, and probe regeneration",
            "mutations": [
                "omitted raw row",
                "false rank exclusion",
                "missing child",
                "wrong parent",
                "broken transport",
                "wrong K2P quartet spectrum or coordinate",
                "omitted or reassigned quartet terminal binding",
                "nonordinary or wrongly selected triangle acceptance",
                "missing or illicit inheritance complement",
                "broken paired s/g serial product",
                "source-target reversal without inverse parameter transport",
                "reassigned cubic certificate",
                "reassigned quartic certificate",
                "reassigned quintic certificate",
                "reassigned quadratic certificate",
                "tree-sunlet false-oracle reintroduction",
            ],
        },
    }
    payload["payload_sha256"] = sha_object(payload)
    return payload


def validate_lock(lock: dict[str, Any], project: Path = PROJECT) -> dict[str, object]:
    verify_payload_hash(lock)
    require(lock.get("schema") == LOCK_SCHEMA, "LOCK_SCHEMA_FAIL")
    require(lock.get("candidate_outcome") == EXPECTED_OUTCOME, "LOCK_OUTCOME_FAIL")
    validate_locked_files(lock, project)
    try:
        nested = validate_nested_manifests(project)
    except ReleaseFailure as error:
        nested = {"validation_error": str(error)}
    require(lock.get("nested_manifests") == nested, "LOCK_NESTED_MANIFEST_DRIFT")
    try:
        layers, blockers = validate_semantics(project)
    except ReleaseFailure as error:
        layers, blockers = {}, [str(error)]
    blockers.extend(declared_corrected_locator_blockers(project))
    blockers.extend(
        f"MISSING_REQUIRED_FILE:{relative}"
        for relative in lock.get("missing_required_files", [])
    )
    if "validation_error" in nested:
        blockers.append(f"NESTED_MANIFEST_FAIL:{nested['validation_error']}")
    blockers = sorted(set(blockers))
    require(lock.get("layers") == layers, "LOCK_LAYER_SEMANTIC_DRIFT")
    require(lock.get("blockers") == blockers, "LOCK_BLOCKER_DRIFT")
    require(lock.get("promotion_ready") is (not blockers), "LOCK_READY_FLAG_DRIFT")
    return {
        "lock_payload_sha256": lock["payload_sha256"],
        "locked_files": len(lock["files"]),
        "layers": len(layers),
        "promotion_ready": not blockers,
        "blockers": blockers,
    }


def child_environment() -> dict[str, str]:
    environment = dict(os.environ)
    environment.pop("PYTHONOPTIMIZE", None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONHASHSEED"] = "0"
    return environment
