#!/usr/bin/env python3
"""Cross-layer fail-closed mutation suite for the final theorem release."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from release_common import (
    HERE,
    PROJECT,
    ReleaseFailure,
    child_environment,
    corrected_locator,
    load_json,
    locator_artifacts,
    require,
    sha_file,
    sha_object,
    validate_corrected_finite_universe,
    validate_historical_artifact_registry,
    validate_promotion_manuscript,
    validate_restoration_v3_package,
    validate_probe_transport_restrictions,
    validate_runtime_environment,
)


def python() -> str:
    candidate = PROJECT / ".venv/bin/python"
    return str(candidate if candidate.is_file() else Path(sys.executable))


def run(
    name: str,
    command: list[str],
    *,
    cwd: Path = PROJECT,
    timeout: float = 600,
) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            env=child_environment(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise ReleaseFailure(f"MUTATION_TIMEOUT:{name}") from error


def accepted_rejection(
    name: str,
    result: subprocess.CompletedProcess[bytes],
    markers: tuple[bytes, ...],
) -> dict[str, object]:
    output = result.stdout + result.stderr
    require(result.returncode != 0, "MUTATION_SURVIVED", name)
    require(
        any(marker in output for marker in markers),
        "MUTATION_WRONG_REJECTION",
        {"name": name, "tail": output[-4000:]},
    )
    print(f"K2P_FINAL_MUTATION_REJECTED name={name}", flush=True)
    return {
        "name": name,
        "status": "REJECTED",
        "returncode": result.returncode,
        "output_sha256": hashlib.sha256(output).hexdigest(),
    }


def resign(payload: dict[str, Any], field: str = "payload_sha256") -> None:
    payload.pop(field, None)
    payload[field] = sha_object(payload)


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def raw_mutations(rows: list[dict[str, object]], temporary: Path, timeout: float) -> None:
    report = temporary / "raw_mutations.json"
    result = run(
        "raw_ledger_mutations",
        [
            python(),
            "-B",
            str(PROJECT / "work/raw_ledger_audit/test_mutations.py"),
            "--report",
            str(report),
        ],
        timeout=timeout,
    )
    require(result.returncode == 0, "RAW_MUTATION_SUITE_FAIL", (result.stdout + result.stderr)[-4000:])
    payload = load_json(report)
    require(payload.get("status") == "PASS", "RAW_MUTATION_REPORT_NOT_PASS")
    require(payload.get("survivors") == 0, "RAW_MUTATION_SURVIVOR")
    names = set(payload.get("tests", []))
    require("omitted_raw_row" in names, "OMITTED_RAW_MUTATION_MISSING")
    require("false_rank_exclusion" in names, "FALSE_RANK_MUTATION_MISSING")
    for name in ("omitted_raw_row", "false_rank_exclusion"):
        rows.append({"name": name, "status": "REJECTED", "source": "raw-ledger suite"})
        print(f"K2P_FINAL_MUTATION_REJECTED name={name}", flush=True)


def corrected_raw4_mutations(
    rows: list[dict[str, object]], temporary: Path, timeout: float
) -> None:
    root = temporary / "corrected_raw4_project"
    overlay = root / "work/raw4_sign_reclassification"
    overlay.mkdir(parents=True)
    for name in (
        "mutation_tests.py",
        "verify_raw4_corrected_terminal_ledger.py",
        "raw4_corrected_terminal_ledger.json",
    ):
        shutil.copy2(
            PROJECT / "work/raw4_sign_reclassification" / name,
            overlay / name,
        )
    raw = root / "work/raw_ledger_audit"
    raw.mkdir(parents=True)
    (raw / "artifacts").symlink_to(
        PROJECT / "work/raw_ledger_audit/artifacts", target_is_directory=True
    )
    atlas = root / "package/referee/k2p_offline_sweep_portable/atlas"
    atlas.parent.mkdir(parents=True)
    atlas.symlink_to(
        PROJECT / "package/referee/k2p_offline_sweep_portable/atlas",
        target_is_directory=True,
    )
    result = run(
        "corrected_raw4_mutations",
        [python(), "-B", str(overlay / "mutation_tests.py")],
        cwd=root,
        timeout=timeout,
    )
    output = result.stdout + result.stderr
    require(
        result.returncode == 0 and b'"status": "PASS"' in output,
        "CORRECTED_RAW4_MUTATION_SUITE_FAIL",
        output[-4000:],
    )
    observed = overlay / "raw4_mutation_certificate.json"
    expected = (
        PROJECT
        / "work/raw4_sign_reclassification/raw4_mutation_certificate.json"
    )
    require(
        observed.read_bytes() == expected.read_bytes(),
        "CORRECTED_RAW4_MUTATION_REPORT_BYTE_DRIFT",
    )
    report = load_json(observed)
    require(report.get("survived") == 0, "CORRECTED_RAW4_MUTATION_SURVIVOR")
    rows.append(
        {
            "name": "corrected_raw4_overlay_mutations",
            "status": "REJECTED",
            "source": "authoritative v2 full-map overlay, 9/9 mutations",
            "mutation_payload_sha256": report["payload_sha256"],
        }
    )
    print(
        "K2P_FINAL_MUTATION_REJECTED name=corrected_raw4_overlay_mutations",
        flush=True,
    )


def theta2_full_map_mutations(
    rows: list[dict[str, object]], temporary: Path, timeout: float
) -> None:
    root = temporary / "theta2_full_map_project"
    package = root / "work/theta2_sign_reclassification"
    package.mkdir(parents=True)
    for name in ("mutation_tests.py", "verify_theta2_full_map_independent.py"):
        shutil.copy2(
            PROJECT / "work/theta2_sign_reclassification" / name,
            package / name,
        )
    adversarial = root / "work/adversarial_proof_review"
    adversarial.mkdir(parents=True)
    shutil.copy2(
        PROJECT
        / "work/adversarial_proof_review/theta2_tree_sunlet_full_map_certificate.json",
        adversarial / "theta2_tree_sunlet_full_map_certificate.json",
    )
    theta2 = root / "work/theta2_five_port_closure"
    theta2.mkdir(parents=True)
    (theta2 / "artifacts").symlink_to(
        PROJECT / "work/theta2_five_port_closure/artifacts",
        target_is_directory=True,
    )
    atlas = root / "package/referee/k2p_offline_sweep_portable/atlas"
    atlas.parent.mkdir(parents=True)
    atlas.symlink_to(
        PROJECT / "package/referee/k2p_offline_sweep_portable/atlas",
        target_is_directory=True,
    )
    result = run(
        "theta2_full_map_mutations",
        [python(), "-B", str(package / "mutation_tests.py")],
        cwd=root,
        timeout=timeout,
    )
    output = result.stdout + result.stderr
    require(
        result.returncode == 0 and b'"status": "PASS"' in output,
        "THETA2_FULL_MAP_MUTATION_SUITE_FAIL",
        output[-4000:],
    )
    observed = package / "theta2_mutation_certificate.json"
    expected = PROJECT / "work/theta2_sign_reclassification/theta2_mutation_certificate.json"
    require(
        observed.read_bytes() == expected.read_bytes(),
        "THETA2_FULL_MAP_MUTATION_REPORT_BYTE_DRIFT",
    )
    report = load_json(observed)
    require(report.get("survived") == 0, "THETA2_FULL_MAP_MUTATION_SURVIVOR")
    rows.append(
        {
            "name": "theta2_full_map_mutations",
            "status": "REJECTED",
            "source": "independent whole-map theta2 suite, 10/10 mutations",
            "mutation_payload_sha256": report["payload_sha256"],
        }
    )
    print(
        "K2P_FINAL_MUTATION_REJECTED name=theta2_full_map_mutations",
        flush=True,
    )


def theta2_quadratic_mutation(
    rows: list[dict[str, object]], temporary: Path, timeout: float
) -> None:
    report = temporary / "theta2_mutations.json"
    result = run(
        "theta2_mutations",
        [
            python(),
            "-B",
            str(PROJECT / "work/theta2_five_port_closure/test_mutations.py"),
            "--report",
            str(report),
        ],
        timeout=timeout,
    )
    require(result.returncode == 0, "THETA2_MUTATION_SUITE_FAIL", (result.stdout + result.stderr)[-4000:])
    payload = load_json(report)
    require(payload.get("status") == "PASS", "THETA2_MUTATION_REPORT_NOT_PASS")
    require(payload.get("survivors") == 0, "THETA2_MUTATION_SURVIVOR")
    require(
        "retained_class_reassignment" in payload.get("tests", []),
        "QUADRATIC_REASSIGNMENT_MUTATION_MISSING",
    )
    require(
        "seven_port_row_omission" in payload.get("tests", []),
        "THETA2_CHILD_OMISSION_MUTATION_MISSING",
    )
    rows.extend(
        (
            {
                "name": "reassigned_quadratic_certificate",
                "status": "REJECTED",
                "source": "theta2 retained-class reassignment",
            },
            {
                "name": "missing_theta2_seven_port_child",
                "status": "REJECTED",
                "source": "theta2 restoration suite",
            },
        )
    )
    print("K2P_FINAL_MUTATION_REJECTED name=reassigned_quadratic_certificate", flush=True)
    print("K2P_FINAL_MUTATION_REJECTED name=missing_theta2_seven_port_child", flush=True)


def restoration_v3_mutation_gate(rows: list[dict[str, object]]) -> None:
    """Bind the frozen 13-case clean-forest mutation suite.

    The producer runs every mutation in an independent temporary copy.  The
    outer suite revalidates the report, its source/verifier bindings, and its
    exact coverage instead of mutating the revoked historical forest.
    """

    paths = locator_artifacts(corrected_locator())
    summary = validate_restoration_v3_package(paths)
    report = load_json(paths["restoration_v3_mutation_report"])
    names = {row.get("mutation") for row in report.get("cases", [])}
    require(
        {
            "omitted_clean_first_edge",
            "omitted_second_child",
            "wrong_second_parent",
            "wrong_first_parent_transport",
            "broken_target_transport_payload",
            "reassigned_quartet_certificate",
            "reassigned_Ti_presentation",
            "reassigned_F_2_112_quartic",
            "optimized_mode",
        }
        <= names,
        "RESTORATION_V3_CROSS_LAYER_MUTATION_COVERAGE_FAIL",
    )
    rows.append(
        {
            "name": "corrected_restoration_v3_mutations",
            "status": "REJECTED",
            "source": (
                "frozen clean-forest suite, 13/13: omitted child, wrong "
                "parent, broken transport, reassigned quartet/T_i/quartic"
            ),
            "mutation_payload_sha256": summary["mutation_payload_sha256"],
        }
    )
    print(
        "K2P_FINAL_MUTATION_REJECTED name=corrected_restoration_v3_mutations",
        flush=True,
    )


def corrected_composite_mutation_gate(
    rows: list[dict[str, object]],
) -> dict[str, Any]:
    """Bind both frozen primitive-composite mutation reports.

    The producer already executes all cases in independent temporary copies.
    The outer suite revalidates the complete located package, including report
    bytes and source bindings, so a report cannot be substituted independently
    of its ledger or summary.  Full-probe blockers do not weaken this primitive
    gate.
    """

    summary, _blockers = validate_corrected_finite_universe()
    raw4 = summary["raw4_composite"]
    theta2 = summary["theta2_composite"]
    rows.append(
        {
            "name": "corrected_primitive_composite_mutations",
            "status": "REJECTED",
            "source": (
                "frozen raw4 14/14 and theta2 12/12 suites: omitted raw row, "
                "false rank, missing child, wrong parent, broken transport, "
                "and reassigned quadratic/cubic/quartic/quintic certificates"
            ),
            "raw4_mutation_payload_sha256": raw4["mutation_payload_sha256"],
            "theta2_mutation_payload_sha256": theta2["mutation_payload_sha256"],
            "producer_mutation_count": 26,
        }
    )
    print(
        "K2P_FINAL_MUTATION_REJECTED "
        "name=corrected_primitive_composite_mutations",
        flush=True,
    )
    return summary


def corrected_probe_mutation_gate(
    rows: list[dict[str, object]], summary: dict[str, Any]
) -> None:
    """Bind the frozen two-stage probe mutations to both Cartesian ledgers."""

    probe = summary["probe_producer"]
    require(
        probe["status"] == "PASS",
        "CORRECTED_PROBE_MUTATION_GATE_STATUS_FAIL",
    )
    rows.append(
        {
            "name": "corrected_two_stage_probe_mutations",
            "status": "REJECTED",
            "source": (
                "frozen 15/15 suite plus nondefault hash-seed replay: omitted "
                "one-/two-port rows and parent, wrong parents, reversed order, "
                "global triangle, exact transport/restriction, T_i/Bernstein, "
                "classifier precedence, and optimized mode"
            ),
            "mutation_payload_sha256": probe["mutation_payload_sha256"],
            "site_partition_payload_sha256": probe[
                "site_partition_payload_sha256"
            ],
            "producer_mutation_count": 15,
        }
    )
    print(
        "K2P_FINAL_MUTATION_REJECTED "
        "name=corrected_two_stage_probe_mutations",
        flush=True,
    )


def promotion_package_mutations(
    rows: list[dict[str, object]],
    temporary: Path,
    corrected_summary: dict[str, Any],
) -> None:
    """Mutate every promotion-document binding in isolated project copies."""

    source = PROJECT / "work/global_theorem_closure/promotion_manuscript"

    def mutate_manuscript(root: Path) -> None:
        path = root / "K2P_SAME_PROMOTION_MANUSCRIPT.md"
        text = path.read_text(encoding="utf-8")
        path.write_text(
            text.replace("are therefore unconditional", "remain conditional", 1),
            encoding="utf-8",
        )

    def mutate_quantifier(root: Path) -> None:
        path = root / "QUANTIFIER_AUDIT.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace("- [x]", "- [ ]", 1),
            encoding="utf-8",
        )

    def mutate_binding(root: Path, action: str) -> None:
        path = root / "PROBE_PROMOTION_PLACEHOLDER.json"
        payload = load_json(path)
        if action == "pass":
            first = sorted(payload["required_pass_gates"])[0]
            payload["required_pass_gates"][first] = "FAIL"
        elif action == "zero":
            first = sorted(payload["required_zero_gates"])[0]
            payload["required_zero_gates"][first] = 1
        elif action == "ledger":
            payload["bound_ledgers"]["one_port"]["path"] = (
                "work/probe_coherence_corrected/two_port_ledger.jsonl.gz"
            )
        elif action == "root":
            payload["census"]["terminal_hash_root"] = "0" * 64
        else:  # pragma: no cover - local closed case table
            raise ReleaseFailure(f"PROMOTION_MUTATION_ACTION_FAIL:{action}")
        write_json(path, payload)

    cases = (
        ("promotion_theorem_status", mutate_manuscript),
        ("promotion_quantifier_checklist", mutate_quantifier),
        ("promotion_pass_gate", lambda root: mutate_binding(root, "pass")),
        ("promotion_zero_gate", lambda root: mutate_binding(root, "zero")),
        ("promotion_ledger_path", lambda root: mutate_binding(root, "ledger")),
        ("promotion_combined_root", lambda root: mutate_binding(root, "root")),
    )
    for ordinal, (name, mutate) in enumerate(cases):
        project = temporary / f"promotion-{ordinal}"
        package = project / "work/global_theorem_closure/promotion_manuscript"
        package.parent.mkdir(parents=True)
        shutil.copytree(source, package)
        mutate(package)
        try:
            validate_promotion_manuscript(corrected_summary, project)
        except ReleaseFailure as error:
            require(
                str(error).startswith("PROMOTION_"),
                "PROMOTION_MUTATION_WRONG_REJECTION",
                {"name": name, "error": str(error)},
            )
        else:
            raise ReleaseFailure(f"MUTATION_SURVIVED:{name}")
        rows.append({"name": name, "status": "REJECTED", "source": "promotion package byte and semantic gate"})
        print(f"K2P_FINAL_MUTATION_REJECTED name={name}", flush=True)


def historical_registry_mutations(rows: list[dict[str, object]]) -> None:
    """Reject attempts to make quarantined narratives theorem authority."""

    source = load_json(HERE / "HISTORICAL_ARTIFACT_REGISTRY.json")

    def promote_legacy(payload: dict[str, Any]) -> None:
        payload["artifacts"][0]["promotion_authority"] = True

    def remove_replacement(payload: dict[str, Any]) -> None:
        payload["artifacts"][0]["authoritative_replacements"] = []

    def omit_scanner_row(payload: dict[str, Any]) -> None:
        payload["scanner"]["scope_paths"].pop()
        payload["scanner"]["classified_count"] -= 1

    for name, mutate in (
        ("historical_artifact_promoted", promote_legacy),
        ("historical_authoritative_replacement_removed", remove_replacement),
        ("historical_scanner_record_omitted", omit_scanner_row),
    ):
        payload = copy.deepcopy(source)
        mutate(payload)
        resign(payload)
        try:
            validate_historical_artifact_registry(PROJECT, payload)
        except ReleaseFailure as error:
            require(
                str(error).startswith("HISTORICAL_"),
                "HISTORICAL_REGISTRY_MUTATION_WRONG_REJECTION",
                {"name": name, "error": str(error)},
            )
        else:
            raise ReleaseFailure(f"MUTATION_SURVIVED:{name}")
        rows.append(
            {
                "name": name,
                "status": "REJECTED",
                "source": "historical artifact quarantine registry",
            }
        )
        print(f"K2P_FINAL_MUTATION_REJECTED name={name}", flush=True)


def probe_wrong_parent(
    rows: list[dict[str, object]], temporary: Path, timeout: float
) -> None:
    certificate = load_json(
        PROJECT / "work/probe_coherence_closure/probe_certificate.json"
    )
    child = certificate["one_port"]["survivors"][0]
    anchors = certificate["anchors"]["records"]
    replacement = next(row for row in anchors if row["anchor_id"] != child["parent_id"])
    child["parent_id"] = replacement["anchor_id"]
    child["parent_transport_sha256"] = replacement["transport_sha256"]
    child["relation_id"] = (
        f"A+p:{child['parent_id']}:{child['source_insertion_index']}:"
        f"{child['target_insertion_index']}"
    )
    resign(certificate)
    path = temporary / "probe_wrong_parent.json"
    write_json(path, certificate)
    result = run(
        "wrong_probe_parent",
        [
            python(),
            "-B",
            str(
                PROJECT
                / "work/adversarial_proof_review/verify_probe_certificate_structure.py"
            ),
            "--certificate",
            str(path),
        ],
        timeout=timeout,
    )
    rows.append(
        accepted_rejection(
            "wrong_probe_parent",
            result,
            (b"PROBE_STRUCTURAL_REPLAY_FAIL",),
        )
    )


def probe_broken_transport(rows: list[dict[str, object]]) -> None:
    certificate = load_json(
        PROJECT / "work/probe_coherence_closure/probe_certificate.json"
    )
    child = certificate["one_port"]["survivors"][0]
    mapping = child["transport"]["vertex_map"]
    require(len(mapping) >= 2, "BROKEN_TRANSPORT_MUTATION_TARGET_MISSING")
    mapping[0][1], mapping[1][1] = mapping[1][1], mapping[0][1]
    child["transport_sha256"] = sha_object(child["transport"])
    resign(certificate)
    try:
        validate_probe_transport_restrictions(certificate)
    except ReleaseFailure as error:
        require(
            "PROBE_LITERAL_TRANSPORT_RESTRICTION_FAIL" in str(error),
            "BROKEN_TRANSPORT_WRONG_REJECTION",
            error,
        )
    else:
        raise ReleaseFailure("MUTATION_SURVIVED:broken_probe_transport")
    rows.append(
        {
            "name": "broken_probe_transport",
            "status": "REJECTED",
            "source": "independent literal parent-map restriction",
        }
    )
    print("K2P_FINAL_MUTATION_REJECTED name=broken_probe_transport", flush=True)


def clone_direct_release(source: Path, destination: Path) -> None:
    # Never hard-link mutation inputs.  A later write through a hard link
    # changes the supposedly immutable source inode as well as the clone.
    shutil.copytree(
        source,
        destination,
        copy_function=shutil.copy2,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", ".DS_Store"),
    )


def direct_source_fingerprint() -> dict[str, str]:
    """Guard the immutable direct release against mutation-suite writes."""

    root = PROJECT / "package/referee/k2p_offline_sweep_portable"
    relatives = (
        "DIRECT_CLOSURE_LOCK.json",
        "build_direct_closure_lock.py",
        "verify_direct_closure_release.py",
        "proofs/four_port_direct_residual_closure_certificate.json",
    )
    return {relative: sha_file(root / relative) for relative in relatives}


def release_source_fingerprint() -> dict[str, str]:
    lock = load_json(HERE / "RELEASE_LOCK.json")
    files = lock.get("files")
    require(isinstance(files, dict), "MUTATION_SOURCE_LOCK_FILES_FAIL")
    result: dict[str, str] = {}
    for relative in sorted(files):
        path = PROJECT / relative
        require(path.is_file(), "MUTATION_SOURCE_FILE_MISSING", relative)
        result[relative] = sha_file(path)
    return result


@contextmanager
def immutable_release_sources():
    before = release_source_fingerprint()
    try:
        yield
    finally:
        require(
            release_source_fingerprint() == before,
            "MUTATION_SOURCE_TREE_FINGERPRINT_DRIFT",
        )


def reassign_direct_family(
    rows: list[dict[str, object]],
    temporary: Path,
    timeout: float,
    family: str,
    replacement_family: str,
) -> None:
    source = PROJECT / "package/referee/k2p_offline_sweep_portable"
    source_before = direct_source_fingerprint()
    try:
        root = temporary / f"direct_{family}"
        clone_direct_release(source, root)
        overlay_path = root / "proofs/four_port_direct_residual_closure_certificate.json"
        overlay = load_json(overlay_path)
        row = next(item for item in overlay["coverage"] if item["family"] == family)
        row["family"] = replacement_family
        resign(overlay, "payload_sha256_without_hash")
        write_json(overlay_path, overlay)
        rebuild = run(
            f"rebuild_direct_lock_{family}",
            [python(), "-B", str(root / "build_direct_closure_lock.py")],
            cwd=root,
            timeout=timeout,
        )
        require(rebuild.returncode == 0, "DIRECT_MUTATION_RELOCK_FAIL", family)
        result = run(
            f"reassigned_{family}",
            [
                python(),
                "-B",
                str(root / "verify_direct_closure_release.py"),
                "--package-root",
                str(root),
                "--quick",
                "--timeout-seconds",
                str(timeout),
            ],
            cwd=root,
            timeout=timeout + 30,
        )
        label = {
            "theta3_cubic": "reassigned_cubic_certificate",
            "lower_theta_quartic": "reassigned_quartic_certificate",
            "theta0_quintic_port_orbit": "reassigned_quintic_certificate",
        }[family]
        rows.append(
            accepted_rejection(
                label,
                result,
                (b"DIRECT_OVERLAY", b"RELEASE_PROOF", b"RELEASE_LOCK"),
            )
        )
    finally:
        require(
            direct_source_fingerprint() == source_before,
            "DIRECT_SOURCE_CHANGED_BY_MUTATION_SUITE",
            family,
        )


def optimized_mode_mutation(rows: list[dict[str, object]], timeout: float) -> None:
    result = run(
        "optimized_mode",
        [
            python(),
            "-O",
            "-B",
            str(HERE / "verify_final_theorem_release.py"),
            "--quick",
        ],
        timeout=timeout,
    )
    rows.append(
        accepted_rejection(
            "optimized_mode",
            result,
            (b"FINAL_THEOREM_RELEASE_OPTIMIZED_MODE_FORBIDDEN",),
        )
    )


def fail_closed_evidence_mutation_suites(
    rows: list[dict[str, object]], temporary: Path, timeout: float
) -> None:
    """Replay the quartet, canonicalizer, and parameter-transport attacks."""

    quartet = PROJECT / "work/quartet_separation_closure"
    semantic_certificate = quartet / "quartet_semantics_mutation_certificate.json"
    semantic_expected = semantic_certificate.read_bytes()
    semantic_result = run(
        "quartet_semantics_mutations",
        [python(), "-B", str(quartet / "test_quartet_semantics_mutations.py")],
        timeout=timeout,
    )
    semantic_output = semantic_result.stdout + semantic_result.stderr
    require(
        semantic_result.returncode == 0
        and b"K2P_QUARTET_SEMANTICS_MUTATIONS_PASS" in semantic_output,
        "QUARTET_SEMANTICS_MUTATION_SUITE_FAIL",
        semantic_output[-4000:],
    )
    require(
        semantic_certificate.read_bytes() == semantic_expected,
        "QUARTET_SEMANTICS_MUTATION_REPORT_BYTE_DRIFT",
    )
    semantic = load_json(semantic_certificate)
    require(
        semantic.get("status") == "PASS"
        and semantic.get("case_count") == 8
        and all(row.get("status") == "PASS" for row in semantic.get("cases", [])),
        "QUARTET_SEMANTICS_MUTATION_REPORT_FAIL",
    )
    rows.append(
        {
            "name": "quartet_semantics_mutations",
            "status": "REJECTED",
            "source": "8/8 literal spectrum, coordinate, domain, document, and optimized-mode attacks",
            "mutation_payload_sha256": semantic["payload_sha256"],
            "producer_mutation_count": 8,
        }
    )
    print(
        "K2P_FINAL_MUTATION_REJECTED name=quartet_semantics_mutations",
        flush=True,
    )

    terminal_output_path = temporary / "quartet_terminal_binding_mutations.json"
    terminal_result = run(
        "quartet_terminal_binding_mutations",
        [
            python(),
            "-B",
            str(quartet / "test_quartet_terminal_binding_mutations.py"),
            "--output",
            str(terminal_output_path),
        ],
        timeout=max(timeout, 600.0),
    )
    terminal_output = terminal_result.stdout + terminal_result.stderr
    require(
        terminal_result.returncode == 0
        and b"K2P_QUARTET_TERMINAL_BINDING_MUTATIONS_PASS" in terminal_output,
        "QUARTET_TERMINAL_MUTATION_SUITE_FAIL",
        terminal_output[-4000:],
    )
    terminal_expected = quartet / "quartet_terminal_binding_mutation_certificate.json"
    require(
        terminal_output_path.read_bytes() == terminal_expected.read_bytes(),
        "QUARTET_TERMINAL_MUTATION_REPORT_BYTE_DRIFT",
    )
    terminal = load_json(terminal_output_path)
    require(
        terminal.get("status") == "PASS"
        and terminal.get("case_count") == 12
        and all(row.get("status") == "PASS" for row in terminal.get("cases", [])),
        "QUARTET_TERMINAL_MUTATION_REPORT_FAIL",
    )
    rows.append(
        {
            "name": "quartet_terminal_binding_mutations",
            "status": "REJECTED",
            "source": "12/12 resealed algebra, split, reference, reassignment, reversal, and optimized-mode attacks",
            "mutation_payload_sha256": terminal["payload_sha256"],
            "producer_mutation_count": 12,
        }
    )
    print(
        "K2P_FINAL_MUTATION_REJECTED name=quartet_terminal_binding_mutations",
        flush=True,
    )

    canonicalizer = PROJECT / "work/canonicalizer_completeness"
    canonicalizer_certificate = (
        canonicalizer / "canonicalizer_completeness_mutation_certificate.json"
    )
    canonicalizer_expected = canonicalizer_certificate.read_bytes()
    canonicalizer_result = run(
        "canonicalizer_completeness_mutations",
        [python(), "-B", str(canonicalizer / "test_canonicalizer_mutations.py")],
        timeout=timeout,
    )
    canonicalizer_output = canonicalizer_result.stdout + canonicalizer_result.stderr
    require(
        canonicalizer_result.returncode == 0
        and b"K2P_CANONICALIZER_MUTATIONS_PASS" in canonicalizer_output,
        "CANONICALIZER_MUTATION_SUITE_FAIL",
        canonicalizer_output[-4000:],
    )
    require(
        canonicalizer_certificate.read_bytes() == canonicalizer_expected,
        "CANONICALIZER_MUTATION_REPORT_BYTE_DRIFT",
    )
    canonicalizer_report = load_json(canonicalizer_certificate)
    require(
        canonicalizer_report.get("status") == "PASS"
        and canonicalizer_report.get("rejected") == 2
        and canonicalizer_report.get("survived") == 0,
        "CANONICALIZER_MUTATION_REPORT_FAIL",
    )
    rows.append(
        {
            "name": "canonicalizer_completeness_mutations",
            "status": "REJECTED",
            "source": "2/2 nonordinary-triangle and selected-triangle marker attacks",
            "mutation_payload_sha256": canonicalizer_report["payload_sha256"],
            "producer_mutation_count": 2,
        }
    )
    print(
        "K2P_FINAL_MUTATION_REJECTED name=canonicalizer_completeness_mutations",
        flush=True,
    )

    transport = canonicalizer / "inheritance_transport"
    transport_certificate = transport / "parameter_transport_mutation_report.json"
    transport_expected = transport_certificate.read_bytes()
    transport_result = run(
        "parameter_transport_mutations",
        [python(), "-B", str(transport / "run_parameter_transport_mutations.py")],
        timeout=max(timeout, 600.0),
    )
    transport_output = transport_result.stdout + transport_result.stderr
    require(
        transport_result.returncode == 0
        and b"PARAMETER_TRANSPORT_MUTATIONS_PASS" in transport_output,
        "PARAMETER_TRANSPORT_MUTATION_SUITE_FAIL",
        transport_output[-4000:],
    )
    require(
        transport_certificate.read_bytes() == transport_expected,
        "PARAMETER_TRANSPORT_MUTATION_REPORT_BYTE_DRIFT",
    )
    transport_report = load_json(transport_certificate)
    require(
        transport_report.get("status") == "PASS"
        and transport_report.get("rejected") == 10
        and transport_report.get("survived") == 0,
        "PARAMETER_TRANSPORT_MUTATION_REPORT_FAIL",
    )
    rows.append(
        {
            "name": "parameter_transport_mutations",
            "status": "REJECTED",
            "source": "10/10 paired-edge, parent-flip, triangle-local, restriction, root-suppression, and reversal attacks",
            "mutation_payload_sha256": transport_report["payload_sha256"],
            "producer_mutation_count": 10,
        }
    )
    print(
        "K2P_FINAL_MUTATION_REJECTED name=parameter_transport_mutations",
        flush=True,
    )


def truth_oracle_mutation_gate(rows: list[dict[str, object]]) -> list[str]:
    paths = locator_artifacts(corrected_locator())
    report = load_json(paths["corrected_universe_mutation_report"])
    require(report.get("status") == "PASS", "TREE_SUNLET_MUTATIONS_NOT_PASS")
    require(report.get("survivors") == 0, "TREE_SUNLET_MUTATION_SURVIVOR")
    tests = report.get("tests", [])
    names = {
        row.get("name") if isinstance(row, dict) else row
        for row in tests
    }
    require(
        "raw4424_false_tree_sunlet_reintroduction" in names,
        "RAW4424_FALSE_ORACLE_MUTATION_MISSING",
    )
    rows.append(
        {
            "name": "raw4424_false_tree_sunlet_reintroduction",
            "status": "REJECTED",
            "source": "frozen unified corrected-universe mutation suite",
        }
    )
    print(
        "K2P_FINAL_MUTATION_REJECTED "
        "name=raw4424_false_tree_sunlet_reintroduction",
        flush=True,
    )
    return []


def main() -> int:
    if not __debug__:
        raise SystemExit("FINAL_RELEASE_MUTATIONS_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout-seconds", type=float, default=1200.0)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--audit-blocked", action="store_true")
    args = parser.parse_args()
    require(args.timeout_seconds > 0, "INVALID_MUTATION_TIMEOUT")
    validate_runtime_environment()
    started = time.perf_counter()
    direct_before = direct_source_fingerprint()
    rows: list[dict[str, object]] = []
    blockers: list[str] = []
    with immutable_release_sources():
        with tempfile.TemporaryDirectory(prefix="k2p-final-mutations-") as directory:
            temporary = Path(directory)
            optimized_mode_mutation(rows, args.timeout_seconds)
            fail_closed_evidence_mutation_suites(
                rows, temporary, args.timeout_seconds
            )
            raw_mutations(rows, temporary, args.timeout_seconds)
            corrected_raw4_mutations(rows, temporary, args.timeout_seconds)
            theta2_full_map_mutations(rows, temporary, args.timeout_seconds)
            theta2_quadratic_mutation(rows, temporary, args.timeout_seconds)
            corrected_summary = corrected_composite_mutation_gate(rows)
            restoration_v3_mutation_gate(rows)
            corrected_probe_mutation_gate(rows, corrected_summary)
            promotion_package_mutations(rows, temporary, corrected_summary)
            historical_registry_mutations(rows)
            reassign_direct_family(
                rows,
                temporary,
                args.timeout_seconds,
                "theta3_cubic",
                "lower_theta_quartic",
            )
            reassign_direct_family(
                rows,
                temporary,
                args.timeout_seconds,
                "lower_theta_quartic",
                "theta0_quintic_port_orbit",
            )
            reassign_direct_family(
                rows,
                temporary,
                args.timeout_seconds,
                "theta0_quintic_port_orbit",
                "theta3_cubic",
            )
            blockers.extend(truth_oracle_mutation_gate(rows))
    require(
        direct_source_fingerprint() == direct_before,
        "DIRECT_SOURCE_CHANGED_BY_MUTATION_SUITE",
    )
    report = {
        "schema": "k2p-principal-d-plus-final-release-mutations-v1",
        "status": "PASS" if not blockers else "BLOCKED",
        "blockers": blockers,
        "survivors": 0,
        "required_mutation_count": 27,
        "observed_mutation_count": len(rows),
        "mutations": rows,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if blockers:
        print("K2P_FINAL_RELEASE_MUTATIONS_BLOCKED")
        print(json.dumps(report, sort_keys=True))
        return 2 if args.audit_blocked else 1
    require(len(rows) == 27, "FINAL_MUTATION_CENSUS_FAIL", len(rows))
    print("K2P_FINAL_RELEASE_MUTATIONS_PASS")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ReleaseFailure as error:
        raise SystemExit(f"FINAL_RELEASE_MUTATIONS_FAIL:{error}") from error
