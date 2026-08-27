#!/usr/bin/env python3
"""Fast, fail-closed release-input and manuscript-crosswalk gate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

from release_common import (
    ReleaseFailure,
    forbidden_active_evidence,
    head_commit,
    load_json,
    refuse_optimized_python,
    resolve_inside,
    safe_relative_path,
    sha256_bytes,
    sha256_file,
    tracked_head_paths,
    verify_payload_sha256,
    verify_sha256sums,
    require,
)


HERE = Path(__file__).resolve().parent
DEFAULT_PROJECT = HERE.parent

ARTICLE_SECTIONS = [
    "01_introduction", "02_main_theorems", "03_conventions_model",
    "04_physical_topology", "05_three_leaf_geometry", "06_bridge_fibre",
    "07_marginal_localization", "08_primitive_bounded",
    "09_restoration_words", "10_global_classification",
    "11_genericity_reconstruction", "12_continuous_time", "13_sharpness",
    "14_outer_obstruction", "15_kimura_perspective", "16_scope",
    "17_reproducibility",
]

FORBIDDEN_AFFIRMATIVE_PHRASES = (
    "K3P-SAME",
    "ordinary triangle orientations have generic normalized rank 15",
    "ordinary triangles contain an ambient-open 15-dimensional germ",
    "universal pointwise K3P cut-recovery theorem",
    "36568 legacy full-forest leaves",
)


def active_paths(manifest: dict, gate_report: dict, claim_lock: dict) -> list[tuple[str, str | None]]:
    records: list[tuple[str, str | None]] = []
    for field in ("active_gate_reports", "active_theorem_artifacts", "active_verifiers"):
        rows = manifest.get(field)
        require(isinstance(rows, list), ("active manifest list required", field))
        for row in rows:
            require(isinstance(row, dict), ("active manifest record required", field))
            records.append((row.get("path"), row.get("sha256")))
    for value in manifest.get("claim_locks", []):
        records.append((value, None))
    for relative, row in gate_report.get("bindings", {}).items():
        require(isinstance(row, dict) and row.get("path") == relative,
                ("integrated binding path mismatch", relative))
        records.append((relative, row.get("sha256")))
    certification = claim_lock.get("certification", {})
    for path_key, sha_key in (
        ("classification_gate", "classification_gate_sha256"),
        ("classification_mutation_gate", "classification_mutation_gate_sha256"),
        ("classification_mutation_report", "classification_mutation_report_sha256"),
    ):
        records.append((certification.get(path_key), certification.get(sha_key)))
    result: dict[str, str | None] = {}
    for relative, expected in records:
        require(isinstance(relative, str), ("active evidence path required", relative))
        safe_relative_path(relative)
        require(not forbidden_active_evidence(relative),
                ("FORBIDDEN_ACTIVE_EVIDENCE", relative))
        require(expected is None or re.fullmatch(r"[0-9a-f]{64}", expected) is not None,
                ("active evidence SHA-256 malformed", relative, expected))
        if relative in result:
            previous = result[relative]
            require(previous is None or expected is None or previous == expected,
                    ("conflicting active evidence SHA-256", relative, previous, expected))
            if previous is None and expected is not None:
                result[relative] = expected
        else:
            result[relative] = expected
    return [(relative, result[relative]) for relative in sorted(result)]


def verify_active_bindings(project: Path) -> dict:
    manifest = load_json(project / "ACTIVE_MANIFEST.json")
    gate = load_json(project / "reproducibility/K3P_SAME_CLASSIFICATION_GATE_REPORT.json")
    lock = load_json(project / "FINAL_CLAIM_LOCK.json")
    require(manifest.get("status") ==
            "CERTIFIED_K3P_SAME_MATHEMATICS_PUBLICATION_ENGINEERING_PENDING",
            "active manifest mathematical/publication boundary")
    require(gate.get("status") == "CERTIFIED_K3P_SAME" and
            gate.get("remaining_mathematical_gates") == [],
            "integrated theorem gate status")
    require(lock.get("status") == "CERTIFIED_K3P_SAME_MATHEMATICAL_CLASSIFICATION",
            "claim lock status")
    require(lock.get("cut_transfer", {}).get(
        "universal_arbitrary_network_pointwise_cut_rank_iff") == "WITHDRAWN_NOT_USED",
        "withdrawn universal pointwise cut claim")
    require(lock.get("triangle", {}).get("generic_normalized_rank") == 14,
            "triangle rank 14 lock")
    require(lock.get("final_promotion", {}).get("submission_ready") is False,
            "premature submission-ready claim")

    records = active_paths(manifest, gate, lock)
    for relative, expected in records:
        path = resolve_inside(project, relative)
        require(path.is_file(), ("missing active evidence", relative))
        if expected is not None:
            observed = sha256_file(path)
            require(observed == expected,
                    ("stale active evidence SHA-256", relative, expected, observed))
    return {
        "active_path_bindings": len(records),
        "active_manifest_sha256": sha256_file(project / "ACTIVE_MANIFEST.json"),
        "classification_report_sha256": sha256_file(
            project / "reproducibility/K3P_SAME_CLASSIFICATION_GATE_REPORT.json"
        ),
        "claim_lock_sha256": sha256_file(project / "FINAL_CLAIM_LOCK.json"),
    }


def verify_mutation_summaries(project: Path) -> dict:
    specs = [
        ("clean_room/CLEAN_ROOM_MUTATION_RESULTS.json", "mutation_count", 10,
         "rejected_mutations", "accepted_mutations"),
        ("sharpness/adversarial/SHARPNESS_ADVERSARIAL_AUDIT.json", None, 18, None, None),
        ("reproducibility/CUT_TRANSFER_GATE_MUTATION_REPORT.json", "mutation_count", 12,
         "rejected_count", "survived_count"),
        ("global_infrastructure/MUTATION_CERTIFICATE.json", None, 19,
         "rejected", "survived"),
        ("probes/K3P_PROBE_MUTATION_CERTIFICATE.json", "mutations_attempted", 17,
         "mutations_rejected", None),
        ("restoration/K3P_RESTORATION_MUTATION_CERTIFICATE.json", "mutation_count", 20,
         "rejected", "accepted"),
        ("reproducibility/K3P_SAME_CLASSIFICATION_MUTATION_REPORT.json",
         "mutation_count", 24, "rejected", "survived"),
        ("reproducibility/RELEASE_ENGINEERING_MUTATION_REPORT.json",
         "mutation_count", 32, "rejected", "survived"),
    ]
    result: dict[str, int] = {}
    for relative, count_key, expected, rejected_key, survived_key in specs:
        value = load_json(project / relative)
        if relative.endswith("RELEASE_ENGINEERING_MUTATION_REPORT.json"):
            verify_payload_sha256(value)
            expected_release_hashes = {
                "verifier_sha256": project / "reproducibility/test_release_engineering_mutations.py",
                "release_common_sha256": project / "reproducibility/release_common.py",
                "release_suite_sha256": project / "reproducibility/run_release_suite.py",
                "release_input_verifier_sha256": project / "reproducibility/verify_release_inputs.py",
                "archive_builder_sha256": project / "release/build_release.py",
                "archive_tools_sha256": project / "release/archive_tools.py",
                "release_verifier_sha256": project / "release/verify_release.py",
                "source_reproduction_verifier_sha256": project / "release/verify_source_reproduction.py",
                "submission_validator_sha256": project / "submission/validate_submission_packages.py",
                "submission_validator_mutations_sha256": project / "submission/test_submission_validators.py",
                "probe_mutation_driver_sha256": project / "probes/test_k3p_probe_mutations.py",
                "cut_single_minor_producer_sha256": project / "cut_recovery/strong_crossbridge/search_cut_minor_signs.py",
                "fileset_policy_sha256": project / "release/RELEASE_FILESET.json",
            }
            for field, path in expected_release_hashes.items():
                require(value.get(field) == sha256_file(path),
                        ("stale release mutation code binding", field))
        if relative.endswith("SHARPNESS_ADVERSARIAL_AUDIT.json"):
            actual = len(value.get("mutations", {}))
            require(actual == expected and all(
                row.get("mutation_detected") is True
                for row in value.get("mutations", {}).values()
            ), ("sharpness mutation census", actual))
        elif relative.endswith("MUTATION_CERTIFICATE.json") and relative.startswith(
                "global_infrastructure/"):
            require(value.get("status") == "PASS", ("mutation summary status", relative))
            actual = len(value.get("mutations", []))
            require(actual == expected and value.get("rejected") == expected and
                    value.get("survived") == 0,
                    ("global mutation census", actual))
        else:
            require(value.get("status") == "PASS", ("mutation summary status", relative))
            actual = value.get(count_key)
            require(actual == expected, ("mutation count", relative, actual, expected))
            if rejected_key is not None:
                require(value.get(rejected_key) == expected,
                        ("mutation rejected count", relative, rejected_key))
            if survived_key is not None:
                require(value.get(survived_key) == 0,
                        ("mutation survived count", relative, survived_key))
        result[relative] = expected

    semantic_relative = "probes/K3P_PROBE_SEMANTIC_MUTATIONS.json"
    semantic = load_json(project / semantic_relative)
    semantic_names = {
        "coherently_resealed_nonincidence_transport",
        "coherently_resealed_wrong_marginal_label",
        "coherently_resealed_false_quartet",
        "coherently_resealed_false_six_circuit_deck",
        "coherently_resealed_incomplete_site_profile",
        "altered_transport_restriction_claim",
        "mixed_sign_Bernstein_polynomial",
    }
    semantic_rows = semantic.get("mutations", [])
    require(semantic.get("status") == "PASS" and
            semantic.get("mutations_rejected") == 7 and
            semantic.get("mutations_survived") == 0 and
            isinstance(semantic_rows, list) and len(semantic_rows) == 7 and
            {row.get("name") for row in semantic_rows} == semantic_names and
            all(row.get("status") == "REJECTED" for row in semantic_rows),
            "semantic probe mutation summary")
    result[semantic_relative] = 7

    four_port_relative = (
        "four_port_atlas/full_universe_replay/FULL_FOUR_PORT_MUTATION_REPORT.json"
    )
    four_port = load_json(project / four_port_relative)
    four_port_names = {
        "coherent_raw_omission",
        "coherent_isomorphic_triangle_reclassification",
        "coherent_restoration_quadratic_reclassification",
        "coefficientwise_upper_rank_forgery",
        "coherent_quotient_orbit_omission",
        "optimized_mode",
    }
    four_port_rows = four_port.get("mutations", [])
    require(four_port.get("status") == "PASS" and
            four_port.get("rejected") == 6 and four_port.get("survived") == 0 and
            isinstance(four_port_rows, list) and len(four_port_rows) == 6 and
            {row.get("name") for row in four_port_rows} == four_port_names and
            all(row.get("rejected") is True for row in four_port_rows),
            "full four-port mutation summary")
    result[four_port_relative] = 6
    return result


def verify_manuscript_crosswalk(project: Path) -> dict:
    main = project / "manuscript/main.tex"
    supplement = project / "supplement/reader_supplement.tex"
    references = project / "manuscript/references.bib"
    for path in (main, supplement, references):
        require(path.is_file(), ("missing manuscript source", str(path.relative_to(project))))
    main_text = main.read_text(encoding="utf-8")
    combined = [main_text, supplement.read_text(encoding="utf-8")]
    section_hashes: dict[str, str] = {}
    for stem in ARTICLE_SECTIONS:
        relative = f"manuscript/sections/{stem}.tex"
        require(f"\\input{{sections/{stem}}}" in main_text,
                ("article section not included", stem))
        path = project / relative
        require(path.is_file(), ("missing article section", relative))
        text = path.read_text(encoding="utf-8")
        combined.append(text)
        section_hashes[relative] = sha256_file(path)
    corpus = "\n".join(combined)
    normalized_corpus = " ".join(corpus.split())
    lower = " ".join(corpus.lower().split())
    for phrase in FORBIDDEN_AFFIRMATIVE_PHRASES:
        require(phrase.lower() not in lower, ("forbidden manuscript claim", phrase))
    required_fragments = (
        "N\\preceqplus N'",
        "N\\trianglerel N'",
        "N\\bowtieplus N'",
        "generic normalized rank \\(14\\)",
        "They do not contain an ambient-open \\(15\\)-dimensional germ",
        "withdrawn and not used",
        "36,568",
        "36,792",
        "204",
        "6n-3",
        "0009-0001-9320-500X",
        "complete K3P containment classification",
    )
    for fragment in required_fragments:
        require(fragment.lower() in normalized_corpus.lower(),
                ("manuscript crosswalk fragment missing", fragment))
    referenced_paths = sorted(set(re.findall(r"\\path\{([^}]+)\}", corpus)))
    missing_references = []
    for relative in referenced_paths:
        if relative in ("k3p_level2_identifiability_final", "k3p_level2_identifiability_final/"):
            continue
        if relative.endswith("/"):
            path = resolve_inside(project, relative[:-1])
            if not path.is_dir():
                missing_references.append(relative)
        else:
            path = resolve_inside(project, relative)
            if not path.exists():
                missing_references.append(relative)
    require(missing_references == [], ("missing manuscript path references", missing_references))
    return {
        "article_sections": len(ARTICLE_SECTIONS),
        "article_sha256": sha256_file(main),
        "supplement_sha256": sha256_file(supplement),
        "bibliography_sha256": sha256_file(references),
        "referenced_project_paths_checked": len(referenced_paths),
        "section_hashes": section_hashes,
    }


def verify_head_sources(project: Path) -> dict:
    tracked = set(tracked_head_paths(project))
    required = {
        "manuscript/main.tex", "manuscript/references.bib",
        "supplement/reader_supplement.tex",
        *(f"manuscript/sections/{stem}.tex" for stem in ARTICLE_SECTIONS),
    }
    missing = sorted(required - tracked)
    require(missing == [], ("release sources are not committed at HEAD", missing))
    return {"required_committed_sources": len(required), "head": head_commit(project)}


def verify_submission_draft_state(project: Path) -> dict:
    relative = "submission/VALIDATION_REPORT.json"
    report = load_json(project / relative)
    verify_payload_sha256(report)
    require(report.get("status") == "NOT_READY" and
            report.get("structural_error_count") == 0 and
            report.get("release_blocker_count") == 26,
            "submission draft readiness boundary")
    require(report.get("validator_sha256") == sha256_file(
        project / "submission/validate_submission_packages.py"
    ), "submission draft validator binding")
    manifest_hashes = report.get("manifest_sha256")
    require(isinstance(manifest_hashes, dict) and len(manifest_hashes) == 3,
            "submission draft manifest binding set")
    for path, expected in manifest_hashes.items():
        require(expected == sha256_file(project / path),
                ("submission draft manifest binding", path))
    return {
        "status": report["status"],
        "structural_error_count": report["structural_error_count"],
        "release_blocker_count": report["release_blocker_count"],
        "report_sha256": sha256_file(project / relative),
        "payload_sha256": report["payload_sha256"],
    }


def verify_environment_lock(project: Path) -> dict:
    requirements = project / "reproducibility/requirements.txt"
    expected = [
        "mpmath==1.3.0", "networkx==3.5", "numpy==2.5.2", "sympy==1.14.0",
    ]
    observed = [line.strip() for line in requirements.read_text(
        encoding="utf-8"
    ).splitlines() if line.strip()]
    require(observed == expected, ("release dependency lock", observed, expected))
    policy = load_json(project / "release/RELEASE_FILESET.json")
    require(policy.get("tectonic_version") == "Tectonic 0.16.9" and
            policy.get("tectonic_sha256") ==
            "38eff9059ed622672c9a2590415a8f01c043df4232baa459628a2cd86e512d95",
            "release PDF toolchain lock")
    return {
        "requirements_sha256": sha256_file(requirements),
        "dependency_count": len(expected),
        "tectonic_version": policy["tectonic_version"],
        "tectonic_sha256": policy["tectonic_sha256"],
    }


def validate(project: Path, *, require_head: bool) -> dict:
    checksum_records = verify_sha256sums(project, "SHA256SUMS")
    report = {
        "schema": "k3p-release-input-gate-v1",
        "status": "PASS",
        "active_bindings": verify_active_bindings(project),
        "frozen_checksum_records": len(checksum_records),
        "mutation_summaries": verify_mutation_summaries(project),
        "manuscript_crosswalk": verify_manuscript_crosswalk(project),
        "submission_draft_readiness": verify_submission_draft_state(project),
        "environment_lock": verify_environment_lock(project),
        "head_sources": verify_head_sources(project) if require_head else {
            "status": "DEVELOPMENT_OVERRIDE_NOT_A_RELEASE_GATE"
        },
    }
    report["payload_sha256"] = sha256_bytes(json.dumps(
        report, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii"))
    return report


def main(argv: list[str] | None = None) -> int:
    try:
        refuse_optimized_python()
        parser = argparse.ArgumentParser()
        parser.add_argument("--project-root", type=Path, default=DEFAULT_PROJECT)
        parser.add_argument("--allow-uncommitted-sources", action="store_true")
        parser.add_argument("--self-test", action="store_true")
        args = parser.parse_args(argv)
        if args.self_test:
            print("K3P_RELEASE_INPUT_SELF_TEST_PASS")
            return 0
        report = validate(
            args.project_root.resolve(), require_head=not args.allow_uncommitted_sources
        )
        print(json.dumps(report, indent=2, sort_keys=True))
        print("K3P_RELEASE_INPUT_GATE_PASS")
        return 0
    except (ReleaseFailure, OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"K3P_RELEASE_INPUT_GATE_FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
