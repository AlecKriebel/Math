#!/usr/bin/env python3
"""Build the exact theorem-to-artifact crosswalk for the submission draft."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any


PROJECT = Path(__file__).resolve().parents[2]
SUBMISSION = PROJECT / "proof_compression_submission"
OUTPUT = Path(__file__).with_name("THEOREM_ARTIFACT_CROSSWALK.json")
MARKDOWN = Path(__file__).with_name("THEOREM_ARTIFACT_CROSSWALK.md")
LOCK_RELATIVE = "work/final_theorem_release/RELEASE_LOCK.json"
LOCK_SHA256 = "58e32bd29f7a039e3da4e47398e32ee8277ad46cf62271a7ed80bf41688b18fb"
LOCK_PAYLOAD_SHA256 = "3b7de4c60315a5820a2623de860f493d6b76a645b5c674ffda89f12fc31a5c90"
CONTENT_ROOT_SHA256 = "7004e3e26bf359d0a11c07fd51cb1636859b30b07a97ca6c9cfd0dcd082dfc92"
FULL_REPLAY_REPORT = "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json"
FULL_REPLAY_TELEMETRY = "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json"


def fail(message: str) -> None:
    raise SystemExit(message)


def reject_optimized_mode() -> None:
    if not __debug__:
        fail("optimized Python is forbidden")


def safe_relative(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        fail(f"unsafe project-relative path: {value!r}")
    return path


def project_path(relative: str) -> Path:
    return PROJECT.joinpath(*safe_relative(relative).parts)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_hash(value: Any) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return sha256_bytes(data)


def read_json(relative: str) -> dict[str, Any]:
    value = json.loads(project_path(relative).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        fail(f"expected JSON object: {relative}")
    return value


def declared_schema(relative: str, data: bytes) -> str | None:
    if relative.endswith(".json"):
        value = json.loads(data)
        if not isinstance(value, dict):
            return None
        schema = value.get("schema")
        return schema if isinstance(schema, str) else None
    return None


def artifact(relative: str, role: str, frozen: bool, lock: dict[str, Any]) -> dict[str, Any]:
    path = project_path(relative)
    if not path.is_file() or path.is_symlink():
        fail(f"missing or symbolic artifact: {relative}")
    data = path.read_bytes()
    digest = sha256_bytes(data)
    if relative == LOCK_RELATIVE:
        if digest != LOCK_SHA256:
            fail("frozen release lock drift")
    elif frozen:
        locked = lock.get("_transitive_files", {}).get(relative)
        if not isinstance(locked, dict):
            fail(f"artifact is not in the transitive frozen ledger: {relative}")
        if digest != locked.get("sha256") or len(data) != locked.get("bytes"):
            fail(f"transitive frozen binding mismatch: {relative}")
    row: dict[str, Any] = {
        "bytes": len(data),
        "declared_schema": declared_schema(relative, data),
        "frozen": frozen,
        "path": relative,
        "role": role,
        "sha256": digest,
    }
    if relative.endswith(".py"):
        row["media_type"] = "text/x-python"
    elif relative.endswith(".md"):
        row["media_type"] = "text/markdown"
    elif relative.endswith(".json"):
        row["media_type"] = "application/json"
    elif relative.endswith(".txt"):
        row["media_type"] = "text/plain"
    else:
        row["media_type"] = "application/octet-stream"
    return row


def unknown_runtime() -> dict[str, Any]:
    return {
        "end_to_end_seconds": None,
        "status": "unknown",
        "reason": "No byte-bound end-to-end runtime is recorded for this theorem layer.",
    }


def observed_runtime(relative: str, field: str, lock: dict[str, Any]) -> dict[str, Any]:
    value = read_json(relative).get(field)
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
        fail(f"missing recorded runtime {relative}:{field}")
    source = artifact(relative, "runtime observation source", True, lock)
    return {
        "end_to_end_seconds": None,
        "status": "component_observation_only",
        "observations": [
            {
                "field": field,
                "seconds": value,
                "source_path": relative,
                "source_sha256": source["sha256"],
            }
        ],
        "reason": "The component observation is preserved verbatim; no full- or quick-suite runtime is inferred.",
    }


def clean_full_runtime(lock: dict[str, Any]) -> dict[str, Any]:
    report = read_json(FULL_REPLAY_REPORT)
    telemetry = read_json(FULL_REPLAY_TELEMETRY)
    report_row = artifact(FULL_REPLAY_REPORT, "clean full replay report", False, lock)
    telemetry_row = artifact(FULL_REPLAY_TELEMETRY, "clean full replay telemetry", False, lock)
    if report.get("schema") != "k2p-principal-d-plus-final-theorem-replay-report-v1":
        fail("clean full replay report schema mismatch")
    if report.get("status") != "PASS" or report.get("promotion_ready") is not True or report.get("blockers"):
        fail("clean full replay did not pass")
    if report.get("mode") != "full" or len(report.get("layer_replays", [])) != 35:
        fail("clean full replay layer census mismatch")
    if report.get("lock_payload_sha256") != LOCK_PAYLOAD_SHA256:
        fail("clean full replay lock binding mismatch")
    if telemetry.get("schema") != "k2p-final-clean-full-replay-telemetry-v1" or telemetry.get("status") != "PASS":
        fail("clean full replay telemetry schema/status mismatch")
    if telemetry.get("report", {}).get("sha256") != report_row["sha256"]:
        fail("clean full replay report/telemetry hash mismatch")
    if telemetry.get("report", {}).get("lock_payload_sha256") != LOCK_PAYLOAD_SHA256:
        fail("clean full replay telemetry lock binding mismatch")
    timing = telemetry.get("time_l", {})
    if timing.get("real_seconds") != 5172.89:
        fail("clean full replay wall-time drift")
    return {
        "end_to_end_seconds": 5172.89,
        "status": "clean_full_replay",
        "clean_detached_checkout": True,
        "git_commit": telemetry.get("git_commit"),
        "internal_elapsed_seconds": report.get("elapsed_seconds"),
        "layer_count": len(report["layer_replays"]),
        "maximum_resident_set_size_bytes": timing.get("maximum_resident_set_size_bytes"),
        "peak_memory_footprint_bytes": timing.get("peak_memory_footprint_bytes"),
        "report_path": FULL_REPLAY_REPORT,
        "report_sha256": report_row["sha256"],
        "telemetry_path": FULL_REPLAY_TELEMETRY,
        "telemetry_sha256": telemetry_row["sha256"],
    }


def build() -> dict[str, Any]:
    reject_optimized_mode()
    lock_bytes = project_path(LOCK_RELATIVE).read_bytes()
    if sha256_bytes(lock_bytes) != LOCK_SHA256:
        fail("frozen release lock byte hash mismatch")
    lock = json.loads(lock_bytes)
    if not isinstance(lock, dict):
        fail("frozen release lock is not a JSON object")
    if lock.get("schema") != "k2p-principal-d-plus-final-theorem-release-lock-v1":
        fail("frozen release lock schema mismatch")
    if lock.get("payload_sha256") != LOCK_PAYLOAD_SHA256:
        fail("frozen release lock payload mismatch")
    if lock.get("promotion_ready") is not True or lock.get("blockers") or lock.get("missing_required_files"):
        fail("frozen theorem release is not promotion-ready")
    content_ledger = read_json("output/referee/REFEREE_BUNDLE_CONTENTS.json")
    frozen_files = content_ledger.get("files")
    if not isinstance(frozen_files, dict) or len(frozen_files) != 374:
        fail("transitive frozen content ledger file count mismatch")
    if content_ledger.get("schema") != "k2p-principal-d-plus-referee-content-ledger-v1":
        fail("transitive frozen content ledger schema mismatch")
    if content_ledger.get("release_lock_sha256") != LOCK_SHA256:
        fail("transitive frozen content ledger lock binding mismatch")
    if content_ledger.get("release_lock_payload_sha256") != LOCK_PAYLOAD_SHA256:
        fail("transitive frozen content ledger payload binding mismatch")
    if content_ledger.get("total_bytes") != 434698345:
        fail("transitive frozen content ledger byte count mismatch")
    if canonical_hash(frozen_files) != CONTENT_ROOT_SHA256:
        fail("transitive frozen content root mismatch")
    if content_ledger.get("content_ledger_root_sha256") != CONTENT_ROOT_SHA256:
        fail("declared transitive frozen content root mismatch")
    lock["_transitive_files"] = frozen_files

    def rows(specifications: list[tuple[str, str, bool]]) -> list[dict[str, Any]]:
        return [artifact(path, role, frozen, lock) for path, role, frozen in specifications]

    outer_mutation = (
        "work/final_theorem_release/run_release_mutations.py",
        "outer fail-closed mutation orchestrator",
        True,
    )
    claims: list[dict[str, Any]] = [
        {
            "claim_id": "C01-domain-rooting-subdivision",
            "claim": "Principal stochastic and continuous-time K2P domains, edge subdivision, and rerooting invariance.",
            "proof_status": "frozen_authoritative",
            "compression_status": "hand_proof_plus_small_exact_certificate",
            "authoritative_artifacts": rows([
                ("work/domain_rooting_closure/PROOF.md", "proof", True),
                ("work/domain_rooting_closure/domain_rooting_certificate.json", "exact certificate", True),
            ]),
            "producer_artifacts": rows([
                ("work/domain_rooting_closure/verify_domain_rooting.py", "certificate producer and replayer", True),
            ]),
            "replay_artifacts": rows([
                ("work/domain_rooting_closure/verify_domain_rooting.py", "exact replay", True),
            ]),
            "mutation_artifacts": rows([outer_mutation]),
            "environment_profile": "frozen-python-k2p-v1",
            "runtime": unknown_runtime(),
        },
        {
            "claim_id": "C02-quartet-tree-of-blobs",
            "claim": "Pointwise quartet signs, labelled tree-of-blobs recovery, and source-to-target topology direction.",
            "proof_status": "frozen_authoritative",
            "compression_status": "hand_proof_plus_finite_split_logic",
            "authoritative_artifacts": rows([
                ("work/quartet_separation_closure/PROOF.md", "proof", True),
                ("work/quartet_separation_closure/quartet_logic_certificate.json", "quartet logic certificate", True),
                ("work/adversarial_proof_review/topology_direction_certificate.json", "direction certificate", True),
            ]),
            "producer_artifacts": rows([
                ("work/quartet_separation_closure/verify_quartet_logic.py", "quartet certificate producer", True),
                ("work/adversarial_proof_review/verify_topology_direction.py", "topology direction producer", True),
            ]),
            "replay_artifacts": rows([
                ("work/quartet_separation_closure/verify_quartet_logic.py", "exact quartet replay", True),
                ("work/adversarial_proof_review/verify_topology_direction.py", "independent topology replay", True),
            ]),
            "mutation_artifacts": rows([outer_mutation]),
            "environment_profile": "frozen-python-k2p-v1",
            "runtime": unknown_runtime(),
        },
        {
            "claim_id": "C03-bridge-marginal-local-product",
            "claim": "Complete two-sector bridge fibre, marginal submersions, physical local product, and simultaneous gluing.",
            "proof_status": "frozen_authoritative",
            "compression_status": "hand_proof_with_exact_regression_certificate",
            "authoritative_artifacts": rows([
                ("work/bridge_marginal_closure/PROOF.md", "proof", True),
                ("work/bridge_marginal_closure/certificate.json", "exact regression certificate", True),
                ("work/adversarial_proof_review/PHYSICAL_LOCAL_PRODUCT_REPAIR.md", "adversarial repair proof", True),
            ]),
            "producer_artifacts": rows([
                ("work/bridge_marginal_closure/verify_bridge_marginal.py", "certificate producer", True),
            ]),
            "replay_artifacts": rows([
                ("work/adversarial_proof_review/verify_adversarial.py", "adversarial replay", True),
            ]),
            "mutation_artifacts": rows([
                ("work/adversarial_proof_review/test_mutations.py", "layer mutation runner", True),
                ("work/adversarial_proof_review/mutation_certificate.json", "mutation report", True),
                outer_mutation,
            ]),
            "environment_profile": "frozen-python-k2p-v1",
            "runtime": unknown_runtime(),
        },
        {
            "claim_id": "C04-primitive-grammar-and-completion-count",
            "claim": "Cycle/theta primitive grammar and exact 831, 1,983, 4,155 completion counts, yielding 405,216 raw four-port, 2,946,240 theta2, and 13,440 cycle presentations.",
            "proof_status": "derived_from_frozen_grammar",
            "compression_status": "PC-PARTIAL_exact_count_formula",
            "authoritative_artifacts": rows([
                ("proof_compression_submission/analysis/FINITE_UNIVERSE_COMPLETENESS.md", "derived counting proof", False),
                ("proof_compression_submission/analysis/FAMILY_COVERAGE_EQUIVALENCE_CERTIFICATE.json", "coverage-equivalence certificate", False),
                ("work/final_theorem_release/corrected_universe_certificate.json", "frozen exact universe authority", True),
            ]),
            "producer_artifacts": rows([
                ("proof_compression_submission/analysis/derive_baseline_and_universe.py", "independent grammar parser and counter", False),
            ]),
            "replay_artifacts": rows([
                ("proof_compression_submission/analysis/verify_family_coverage_equivalence.py", "direction-safe equivalence replay", False),
                ("work/final_theorem_release/verify_corrected_universe_independent.py", "frozen independent universe replay", True),
            ]),
            "mutation_artifacts": rows([
                ("work/final_theorem_release/run_corrected_universe_mutations.py", "corrected-universe mutation runner", True),
                ("work/final_theorem_release/corrected_universe_mutation_report.json", "corrected-universe mutation report", True),
                outer_mutation,
            ]),
            "environment_profile": "frozen-python-k2p-v1",
            "runtime": unknown_runtime(),
        },
        {
            "claim_id": "C05-raw-four-rank-filter",
            "claim": "Every raw four-port direction appears once and the exact rank exclusions use universal symbolic upper certificates plus 75 exceptional orbit representatives.",
            "proof_status": "frozen_authoritative_computation",
            "compression_status": "PC-PARTIAL_3515_universal_plus_75_exception_representatives_cover_864",
            "authoritative_artifacts": rows([
                ("work/raw_ledger_audit/artifacts/raw_ledger_summary.json", "raw census and bindings", True),
                ("work/rank_upper_certificates/rank_upper_coverage.json", "rank-upper coverage", True),
                ("work/rank_upper_certificates/manifest.json", "rank certificate manifest", True),
            ]),
            "producer_artifacts": rows([
                ("work/raw_ledger_audit/generate_raw_ledger.py", "raw ledger generator", True),
                ("work/rank_upper_certificates/build_rank_upper_coverage.py", "rank coverage producer", True),
            ]),
            "replay_artifacts": rows([
                ("work/raw_ledger_audit/verify_raw_ledger.py", "raw ledger verifier", True),
                ("work/rank_upper_certificates/rank_upper_replay.json", "rank independent replay report", True),
            ]),
            "mutation_artifacts": rows([
                ("work/raw_ledger_audit/test_mutations.py", "raw-ledger mutation runner", True),
                ("work/raw_ledger_audit/artifacts/raw_ledger_mutation_report.json", "raw-ledger mutation report", True),
                ("work/rank_upper_certificates/mutation_report.json", "rank mutation report", True),
                outer_mutation,
            ]),
            "environment_profile": "frozen-python-k2p-v1",
            "runtime": observed_runtime("work/raw_ledger_audit/artifacts/raw_ledger_summary.json", "generation_seconds", lock),
        },
        {
            "claim_id": "C06-direct-separator-families",
            "claim": "Direct terminal relations are exhausted by exact isomorphism/triangle terminals and direction-safe quadratic, cubic, quartic, quintic, or F2/F3/F4 certificates.",
            "proof_status": "frozen_authoritative_computation",
            "compression_status": "PC-PARTIAL_quadratic_literals_and_certified_high_degree_families",
            "authoritative_artifacts": rows([
                ("proof_compression_submission/templates/DIRECT_CERTIFICATE_TEMPLATE_TABLE.json", "compressed direction-safe template table", False),
                ("proof_compression_submission/templates/PRINTED_CERTIFICATE_APPENDIX.json", "sealed printed-formula and worked-example appendix", False),
                ("proof_compression_submission/supplement/certificate_appendix.tex", "generated reader appendix", False),
                ("package/referee/k2p_offline_sweep_portable/proofs/four_port_direct_residual_closure_certificate.json", "frozen direct-36 certificate", True),
                ("package/referee/k2p_offline_sweep_portable/DIRECT_CLOSURE_LOCK.json", "nested direct closure lock", True),
            ]),
            "producer_artifacts": rows([
                ("proof_compression_submission/templates/derive_direct_templates.py", "literal-body and certified-orbit grouper", False),
                ("proof_compression_submission/templates/build_printed_certificate_appendix.py", "printed appendix producer and deterministic checker", False),
            ]),
            "replay_artifacts": rows([
                ("package/referee/k2p_offline_sweep_portable/verify_direct_closure_release.py", "direct closure replay", True),
                ("proof_compression_submission/templates/verify_printed_certificate_appendix.py", "independent printed-formula and worked-example replay", False),
            ]),
            "mutation_artifacts": rows([
                ("package/referee/k2p_offline_sweep_portable/test_direct_closure_release_mutations.py", "direct certificate mutation runner", True),
                ("proof_compression_submission/templates/test_printed_certificate_appendix_mutations.py", "printed appendix mutation runner", False),
                outer_mutation,
            ]),
            "environment_profile": "frozen-python-k2p-v1",
            "runtime": unknown_runtime(),
        },
        {
            "claim_id": "C07-corrected-full-map-finite-universe",
            "claim": "Whole-map T_i directions, corrected raw4/theta2/cycle ledgers, terminal classification, and exact composite coverage are mutually consistent.",
            "proof_status": "frozen_authoritative_computation",
            "compression_status": "PC-PARTIAL_family_coverage_replayed_but_exact_ledgers_retained",
            "authoritative_artifacts": rows([
                ("work/final_theorem_release/corrected_universe_certificate.json", "corrected universe certificate", True),
                ("work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_summary.json", "raw4 corrected summary", True),
                ("work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_summary.json", "theta2 corrected summary", True),
                ("work/final_theorem_release/full_map_reseal_audit.json", "exact truth-certificate reseal differential", True),
                ("work/final_theorem_release/composite_reseal_diff_audit.json", "exact composite-ledger reseal differential", True),
                ("proof_compression_submission/analysis/FAMILY_COVERAGE_EQUIVALENCE_CERTIFICATE.json", "compressed family equivalence certificate", False),
            ]),
            "producer_artifacts": rows([
                ("work/corrected_composite_ledgers/generate_corrected_composites.py", "corrected composite generator", True),
                ("work/final_theorem_release/verify_full_map_reseal.py", "truth-certificate reseal producer and validator", True),
                ("work/final_theorem_release/verify_composite_reseal_diff.py", "composite differential reconstructor", True),
                ("proof_compression_submission/analysis/verify_family_coverage_equivalence.py", "compressed family builder and verifier", False),
            ]),
            "replay_artifacts": rows([
                ("work/corrected_composite_ledgers/verify_corrected_composites_independent.py", "independent corrected composite replay", True),
                ("work/corrected_composite_ledgers/artifacts/release_contract_replay.json", "release-contract replay", True),
                ("work/final_theorem_release/verify_full_map_reseal.py", "byte-exact reseal replay", True),
                ("work/final_theorem_release/verify_composite_reseal_diff.py", "prior-ledger byte reconstruction replay", True),
            ]),
            "mutation_artifacts": rows([
                ("work/corrected_composite_ledgers/run_composite_mutations.py", "corrected composite mutation runner", True),
                ("work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_mutations.json", "raw4 mutation report", True),
                ("work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_mutations.json", "theta2 mutation report", True),
                ("work/final_theorem_release/verify_full_map_reseal.py", "domain and stale-seal mutation gate", True),
                outer_mutation,
            ]),
            "environment_profile": "frozen-python-k2p-v1",
            "runtime": observed_runtime("work/raw4_sign_reclassification/raw4_corrected_replay_certificate.json", "runtime_seconds", lock),
        },
        {
            "claim_id": "C08-restoration-forest",
            "claim": "All 997 restoration obligations form a terminating, transport-coherent 36,824-edge forest with zero unresolved records.",
            "proof_status": "frozen_authoritative_computation",
            "compression_status": "PC-PARTIAL_297_descriptive_archetypes_not_a_transport_quotient",
            "authoritative_artifacts": rows([
                ("work/restoration_sign_reclassification/corrected_restoration_forest.json", "exact corrected forest", True),
                ("proof_compression_submission/restoration/RESTORATION_ARCHETYPES.json", "descriptive archetype index", False),
                ("proof_compression_submission/restoration/RESTORATION_ARCHETYPE_VERIFICATION.json", "archetype verification report", False),
            ]),
            "producer_artifacts": rows([
                ("work/restoration_sign_reclassification/build_corrected_restoration_forest.py", "exact forest producer", True),
                ("proof_compression_submission/restoration/analyze_restoration_archetypes.py", "archetype producer", False),
            ]),
            "replay_artifacts": rows([
                ("work/restoration_sign_reclassification/verify_corrected_restoration_forest.py", "independent exact forest replay", True),
                ("work/restoration_sign_reclassification/corrected_restoration_replay_certificate.json", "exact forest replay report", True),
                ("proof_compression_submission/restoration/verify_restoration_archetypes.py", "independent archetype replay", False),
            ]),
            "mutation_artifacts": rows([
                ("work/restoration_sign_reclassification/mutate_corrected_restoration_forest.py", "exact forest mutation runner", True),
                ("work/restoration_sign_reclassification/corrected_restoration_mutation_certificate.json", "exact forest mutation report", True),
                outer_mutation,
            ]),
            "environment_profile": "frozen-python-k2p-v1",
            "runtime": observed_runtime("work/restoration_sign_reclassification/corrected_restoration_replay_certificate.json", "runtime_seconds", lock),
        },
        {
            "claim_id": "C09-coherent-probe-word-reconstruction",
            "claim": "The exact one-/two-port probes determine arbitrary attachment words, including all site types, automorphisms, and ordinary-triangle transports.",
            "proof_status": "uniform_word_theorem_from_frozen_finite_premises",
            "compression_status": "PC-PARTIAL_uniform_induction_with_load_bearing_probe_ledgers",
            "authoritative_artifacts": rows([
                ("work/probe_coherence_corrected/probe_coherence_certificate.json", "exact probe closure certificate", True),
                ("proof_compression_submission/probe/PROBE_WORD_THEOREM.md", "uniform word theorem", False),
                ("proof_compression_submission/probe/PROBE_WORD_COVERAGE.json", "word theorem coverage certificate", False),
            ]),
            "producer_artifacts": rows([
                ("work/probe_coherence_corrected/build_probe_coherence_corrected.py", "exact probe producer", True),
            ]),
            "replay_artifacts": rows([
                ("work/probe_coherence_corrected/verify_probe_coherence_corrected.py", "independent exact probe replay", True),
                ("work/global_proof_adversary/probe_full_audit/independent_probe_graph_audit.py", "independent primitive graph audit", True),
                ("proof_compression_submission/probe/verify_probe_word_theorem.py", "word-theorem premise and scope verifier", False),
            ]),
            "mutation_artifacts": rows([
                ("work/probe_coherence_corrected/run_probe_coherence_mutations.py", "probe mutation runner", True),
                ("work/probe_coherence_corrected/probe_coherence_mutation_certificate.json", "probe mutation report", True),
                ("work/global_proof_adversary/probe_full_audit/independent_probe_mutation_report.json", "adversarial probe mutation report", True),
                outer_mutation,
            ]),
            "environment_profile": "frozen-python-k2p-v1",
            "runtime": unknown_runtime(),
        },
        {
            "claim_id": "C10-three-port-triangle-and-genericity",
            "claim": "Three-port tree/sunlet separation and the ordinary-triangle common germ close the local equality alternatives used in global genericity.",
            "proof_status": "frozen_authoritative",
            "compression_status": "hand_proof_plus_no_assert_exact_replay",
            "authoritative_artifacts": rows([
                ("package/original/checkpoint_2/continuation_2/K2P_TREE_SUNLET_SIGN_CERTIFICATE.md", "three-port sign proof", True),
                ("package/original/checkpoint_2/continuation_2/K2P_TRIANGLE_GERM_EXACT.md", "triangle common-germ proof", True),
                ("work/final_theorem_release/triangle_sunlet_certificate.json", "no-assert exact certificate", True),
            ]),
            "producer_artifacts": rows([
                ("work/final_theorem_release/no_assert_triangle_sunlet.py", "three-port exact producer", True),
            ]),
            "replay_artifacts": rows([
                ("package/original/checkpoint_2/continuation_2/verify_triangle_and_sunlet.py", "legacy independent arithmetic replay", True),
                ("work/final_theorem_release/no_assert_triangle_sunlet.py", "promotion-grade no-assert replay", True),
            ]),
            "mutation_artifacts": rows([outer_mutation]),
            "environment_profile": "frozen-python-k2p-v1",
            "runtime": unknown_runtime(),
        },
        {
            "claim_id": "C11-global-K2P-SAME-and-reconstruction",
            "claim": "Unconditional K2P-SAME directed-containment classification, generic identifiability, and reconstruction on the principal domain.",
            "proof_status": "frozen_promotion_ready",
            "compression_status": "theorem_unchanged_PC-PARTIAL_submission_compression",
            "authoritative_artifacts": rows([
                ("work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md", "authoritative theorem manuscript", True),
                ("work/global_theorem_closure/promotion_manuscript/PROBE_PROMOTION_PLACEHOLDER.json", "completed probe promotion binding", True),
                (LOCK_RELATIVE, "unified release lock", True),
            ]),
            "producer_artifacts": rows([
                ("work/final_theorem_release/build_release_lock.py", "release lock producer", True),
            ]),
            "replay_artifacts": rows([
                ("work/final_theorem_release/verify_final_theorem_release.py", "quick/full theorem replay", True),
                ("work/final_theorem_release/corrected_universe_independent_replay.json", "locked independent corrected-universe replay report", True),
                ("work/global_theorem_closure/promotion_manuscript/verify_promotion_gate.py", "promotion gate", True),
                (FULL_REPLAY_REPORT, "clean detached full replay report", False),
                (FULL_REPLAY_TELEMETRY, "clean detached full replay telemetry", False),
            ]),
            "mutation_artifacts": rows([outer_mutation]),
            "environment_profile": "frozen-python-k2p-v1",
            "runtime": clean_full_runtime(lock),
        },
        {
            "claim_id": "C12-strict-continuous-time-corollary",
            "claim": "The classification and reconstruction restrict to the strict continuous-time cone 0<s<1 and s^2<g<1.",
            "proof_status": "frozen_authoritative_corollary",
            "compression_status": "hand_gluing_corollary",
            "authoritative_artifacts": rows([
                ("work/domain_rooting_closure/PROOF.md", "continuous-time domain and subdivision proof", True),
                ("work/bridge_marginal_closure/PROOF.md", "physical simultaneous gluing proof", True),
                ("work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md", "corollary statement and proof", True),
            ]),
            "producer_artifacts": rows([
                ("work/domain_rooting_closure/verify_domain_rooting.py", "continuous-time exact checks", True),
            ]),
            "replay_artifacts": rows([
                ("work/bridge_marginal_closure/verify_bridge_marginal.py", "gluing regression replay", True),
            ]),
            "mutation_artifacts": rows([outer_mutation]),
            "environment_profile": "frozen-python-k2p-v1",
            "runtime": unknown_runtime(),
        },
        {
            "claim_id": "C13-weak-class-sharpness",
            "claim": "A full-dimensional 4n-3 weakly tree-child ambiguity proves sharpness of strong tree-childness.",
            "proof_status": "frozen_authoritative_with_independent_audit",
            "compression_status": "explicit_construction_plus_independent_audit",
            "authoritative_artifacts": rows([
                ("work/weak_sharpness_closure/PROOF.md", "sharpness proof", True),
                ("work/weak_sharpness_closure/weak_sharpness_certificate.json", "exact sharpness certificate", True),
                ("proof_compression_submission/analysis/WEAK_SHARPNESS_COLUMN_CROSSWALK.json", "derived named-column crosswalk", False),
            ]),
            "producer_artifacts": rows([
                ("work/weak_sharpness_closure/verify_weak_sharpness.py", "sharpness certificate producer", True),
                ("proof_compression_submission/analysis/build_weak_sharpness_column_crosswalk.py", "graph-derived named-column producer", False),
            ]),
            "replay_artifacts": rows([
                ("work/weak_sharpness_audit/PROOF_AUDIT.md", "independent proof audit", True),
                ("work/weak_sharpness_audit/audit_weak_sharpness.py", "independent exact replay", True),
                ("work/weak_sharpness_audit/audit_certificate.json", "independent audit report", True),
                ("proof_compression_submission/analysis/verify_weak_sharpness_column_crosswalk.py", "independent graph and determinant crosswalk replay", False),
            ]),
            "mutation_artifacts": rows([
                ("work/weak_sharpness_audit/test_mutations.py", "sharpness mutation runner", True),
                ("work/weak_sharpness_audit/mutation_report.json", "sharpness mutation report", True),
                ("proof_compression_submission/analysis/test_weak_sharpness_column_crosswalk_mutations.py", "named-column mutation runner", False),
                outer_mutation,
            ]),
            "environment_profile": "frozen-python-k2p-v1",
            "runtime": unknown_runtime(),
        },
    ]

    compression_table = [
        {"layer": "primitive completion arithmetic", "before": "six enumerated grammar cases", "after": "one binomial-sum formula", "exact_residue": "all labelled directed records", "status": "proved exact count compression"},
        {"layer": "four-port quadratics", "before": 839, "after": 8, "unit_before": "canonical certificate classes", "unit_after": "literal polynomial bodies", "exact_residue": "all coordinate transports", "status": "direction-safe literal compression"},
        {"layer": "theta2 quadratics", "before": 96, "after": 4, "unit_before": "canonical certificate classes", "unit_after": "literal polynomial bodies", "exact_residue": "all coordinate transports", "status": "direction-safe literal compression"},
        {"layer": "cycle quadratics", "before": 54, "after": 6, "unit_before": "canonical certificate classes", "unit_after": "literal polynomial bodies", "exact_residue": "all coordinate transports", "status": "direction-safe literal compression"},
        {"layer": "restoration quadratics", "before": 6, "after": 5, "unit_before": "canonical certificate classes", "unit_after": "literal polynomial bodies", "exact_residue": "all coordinate transports", "status": "direction-safe literal compression"},
        {"layer": "direct-36 high-degree", "before": 36, "after": 27, "unit_before": "directional records", "unit_after": "direction-specific bodies", "certified_proposition_families": 3, "stored_base_formulas": 5, "exact_residue": "all 36 bindings", "status": "certified family compression; not three literal polynomials"},
        {"layer": "rank upper certificates", "before": 4379, "after": "3515 universal + 75 exceptional representatives", "unit_before": "target descriptors", "unit_after": "certified mechanisms/representatives", "exceptional_descriptors_covered": 864, "exact_residue": "75 syzygy certificates and orbit actions", "status": "frozen exact orbit compression"},
        {"layer": "restoration parents", "before": 997, "after": 297, "unit_before": "canonical parents", "unit_after": "descriptive archetypes", "exact_residue": "997 assignments, 2,540 roots, 36,824 edges, 16 algebra transports", "status": "PC-PARTIAL; not a proved transport quotient"},
        {"layer": "probe reconstruction", "before": "176 anchors + 29,964 one-port + 544,571 two-port rows", "after": "uniform arbitrary-word induction", "exact_residue": "176 anchors, 29,964 one-port rows, 544,571 two-port rows, 67,741 transports, 4,379 restrictions", "status": "PC-PARTIAL; finite premises remain load-bearing"},
    ]

    result: dict[str, Any] = {
        "schema": "k2p-theorem-artifact-reproducibility-crosswalk-v1",
        "status": "PASS_PC_PARTIAL",
        "scope": "Submission crosswalk derived from, but not replacing, the immutable principal-D_plus theorem release.",
        "frozen_release": {
            "candidate_outcome": "K2P-SAME",
            "content_ledger_root_sha256": CONTENT_ROOT_SHA256,
            "file_count_including_release_lock": 374,
            "release_lock_path": LOCK_RELATIVE,
            "release_lock_payload_sha256": LOCK_PAYLOAD_SHA256,
            "release_lock_sha256": LOCK_SHA256,
            "total_bytes_including_release_lock": 434698345,
        },
        "compression_boundary": {
            "status": "PC-PARTIAL",
            "theorem_status_changed": False,
            "exact_ledgers_discarded": False,
            "unsafe_equivalences_used": [],
            "note": "Literal equality and descriptive fingerprints are not promoted to graph/transport orbits without exact transport certificates.",
        },
        "environment_profiles": {
            "frozen-python-k2p-v1": {
                "minimum_python": "3.10",
                "qualified_python": "3.14.6",
                "requirements": artifact("work/final_theorem_release/requirements.txt", "locked dependency versions", True, lock),
                "networkx": "3.5",
                "sympy": "1.14.0",
                "optimized_python": "forbidden",
                "end_to_end_quick_runtime_seconds": None,
                "end_to_end_full_runtime_seconds": 5172.89,
                "full_replay_internal_elapsed_seconds": 5172.248447,
                "full_replay_maximum_resident_set_size_bytes": 1960001536,
                "full_replay_peak_memory_footprint_bytes": 491504408,
                "full_replay_report": artifact(FULL_REPLAY_REPORT, "clean full replay report", False, lock),
                "full_replay_telemetry": artifact(FULL_REPLAY_TELEMETRY, "clean full replay telemetry", False, lock),
                "runtime_status": "clean_detached_full_replay_pass",
            }
        },
        "pending_human_metadata": [
            "corresponding email address",
            "author-contribution statement",
            "funding declaration",
            "competing-interests declaration",
            "article license",
            "code license",
            "data license",
            "immutable submission tag",
            "whether and when to mint a GitHub/Zenodo DOI release",
        ],
        "claims": claims,
        "compression_table": compression_table,
    }
    result["payload_sha256"] = canonical_hash(result)
    return result


def render_markdown(value: dict[str, Any]) -> str:
    lines = [
        "# Theorem-to-artifact reproducibility crosswalk",
        "",
        "Status: **PASS / PC-PARTIAL**. The promoted K2P-SAME theorem remains",
        "unchanged, and the immutable computational-evidence lock remains",
        "promotion-ready; this crosswalk compresses the proof presentation and",
        "does not replace any exact ledger or transport certificate.",
        "",
        "Every path is relative to the `k2p_level2_identifiability_closure` root.",
        "A null declared schema means that the artifact is executable source or",
        "prose rather than a top-level JSON object with a `schema` field.",
        "",
        "## Claim crosswalk",
        "",
        "| ID | Theorem layer | Authority | Producer | Replay | Mutation | Runtime |",
        "|---|---|---|---|---|---|---|",
    ]
    for claim in value["claims"]:
        def names(key: str) -> str:
            return "<br>".join(f"`{row['path']}` (`{row['sha256'][:12]}...`)" for row in claim[key])

        runtime = claim["runtime"]
        if runtime["status"] == "component_observation_only":
            observation = runtime["observations"][0]
            runtime_text = f"component {observation['seconds']:.6f}s; end-to-end unknown"
        elif runtime["status"] == "clean_full_replay":
            runtime_text = f"clean full replay {runtime['end_to_end_seconds']:.2f}s"
        else:
            runtime_text = "unknown"
        lines.append(
            "| {id} | {claim} | {authority} | {producer} | {replay} | {mutation} | {runtime} |".format(
                id=claim["claim_id"],
                claim=claim["claim"],
                authority=names("authoritative_artifacts"),
                producer=names("producer_artifacts"),
                replay=names("replay_artifacts"),
                mutation=names("mutation_artifacts"),
                runtime=runtime_text,
            )
        )
    lines.extend([
        "",
        "## Compression table",
        "",
        "| Layer | Before | Compressed statement | Exact residue | Status |",
        "|---|---:|---|---|---|",
    ])
    for row in value["compression_table"]:
        lines.append(
            f"| {row['layer']} | {row['before']} | {row['after']} | {row['exact_residue']} | {row['status']} |"
        )
    lines.extend([
        "",
        "## Environment and runtime boundary",
        "",
        "The source requires Python 3.10 or newer. The frozen computational-evidence lock was qualified",
        "with Python 3.14.6, NetworkX 3.5, and SymPy 1.14.0. Optimized Python is",
        "forbidden. Component observations are reproduced only where a locked JSON",
        "field records them. A detached clean-checkout full replay passed all 35",
        "layers in 5,172.89 seconds; its exact report and macOS telemetry are bound",
        "above. No quick-suite runtime is inferred by adding component timings.",
        "",
        "## Pending human metadata",
        "",
    ])
    lines.extend(f"- {item}" for item in value["pending_human_metadata"])
    lines.extend([
        "",
        f"Frozen lock SHA-256: `{LOCK_SHA256}`.",
        "",
        f"Crosswalk payload SHA-256: `{value['payload_sha256']}`.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    reject_optimized_mode()
    check = "--check" in sys.argv[1:]
    if any(argument not in {"--check"} for argument in sys.argv[1:]):
        fail("usage: build_theorem_artifact_crosswalk.py [--check]")
    value = build()
    encoded = json.dumps(value, indent=2, sort_keys=True) + "\n"
    markdown = render_markdown(value)
    if check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != encoded:
            fail("theorem artifact crosswalk JSON is stale")
        if not MARKDOWN.is_file() or MARKDOWN.read_text(encoding="utf-8") != markdown:
            fail("theorem artifact crosswalk Markdown is stale")
    else:
        OUTPUT.write_text(encoded, encoding="utf-8")
        MARKDOWN.write_text(markdown, encoding="utf-8")
    print(json.dumps({"claims": len(value["claims"]), "payload_sha256": value["payload_sha256"], "status": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
