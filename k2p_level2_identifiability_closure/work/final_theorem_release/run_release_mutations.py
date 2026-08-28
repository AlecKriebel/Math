#!/usr/bin/env python3
"""Cross-layer fail-closed mutation suite for the final theorem release."""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
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
    validate_direct_closure_mutation_evidence,
    validate_historical_artifact_registry,
    validate_promotion_manuscript,
    validate_quartet_evidence,
    validate_restoration_v3_package,
    validate_probe_transport_restrictions,
    validate_runtime_environment,
    validate_weak_sharpness_mutation_evidence,
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
    environment_overrides: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[bytes]:
    environment = child_environment()
    if environment_overrides is not None:
        environment.update(environment_overrides)
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise ReleaseFailure(f"MUTATION_TIMEOUT:{name}") from error


OUTER_FAILURE_CODE = re.compile(
    r"(?<![A-Z0-9_])[A-Z][A-Z0-9_]*(?:FAIL|MISMATCH|FORBIDDEN)(?![A-Z0-9_])"
)
OUTER_FORBIDDEN_CRASH_TEXT = (
    b"Traceback (most recent call last)",
    b"AssertionError",
    b"ModuleNotFoundError",
    b"ImportError",
)
REQUIRED_MUTATION_COUNT = 25


def accepted_rejection(
    name: str,
    result: subprocess.CompletedProcess[bytes],
    expected_diagnostic: str,
) -> dict[str, object]:
    output = result.stdout + result.stderr
    require(result.returncode == 1, "MUTATION_EXIT_CODE_FAIL", {
        "name": name,
        "returncode": result.returncode,
    })
    forbidden = [
        marker.decode("utf-8") for marker in OUTER_FORBIDDEN_CRASH_TEXT if marker in output
    ]
    require(
        not forbidden,
        "MUTATION_UNRELATED_CRASH",
        {"name": name, "forbidden": forbidden},
    )
    require(
        b"K2P_FOUR_PORT_DIRECT_CLOSURE_RELEASE_PASS" not in output.splitlines(),
        "MUTATION_SUCCESS_ARTIFACT_PRESENT",
        name,
    )
    observed = set(OUTER_FAILURE_CODE.findall(output.decode("utf-8", "replace")))
    require(
        observed == {expected_diagnostic},
        "MUTATION_WRONG_REJECTION",
        {
            "name": name,
            "expected": expected_diagnostic,
            "observed": sorted(observed),
            "tail": output[-4000:],
        },
    )
    print(f"K2P_FINAL_MUTATION_REJECTED name={name}", flush=True)
    return {
        "name": name,
        "status": "REJECTED",
        "returncode": 1,
        "expected_diagnostic": expected_diagnostic,
        "observed_diagnostic": expected_diagnostic,
        "timeout": False,
        "signal": False,
        "success_artifact_present": False,
        "forbidden_crash_text_present": False,
    }


def validate_report_output_path(output: Path | None) -> Path | None:
    """Resolve optional report output and forbid every source-tree collision."""

    if output is None:
        return None
    lexical = Path(os.path.abspath(os.fspath(output)))
    normalized = lexical.parent.resolve() / lexical.name
    resolved = lexical.resolve()
    try:
        resolved.relative_to(PROJECT.resolve())
    except ValueError:
        return normalized
    raise ReleaseFailure(
        "FINAL_RELEASE_MUTATION_OUTPUT_POLICY_FAIL:report output must be outside "
        "the project source tree"
    )


def prepare_report_output(output: Path | None) -> None:
    """Remove stale caller-owned PASS bytes before any fallible preflight."""

    if output is not None:
        output.unlink(missing_ok=True)


def atomic_write_text(path: Path, text: str) -> None:
    """Fsync and atomically replace without following a late output symlink."""

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o644)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        if temporary.exists():
            temporary.unlink()


def build_report(
    rows: list[dict[str, object]], blockers: list[str]
) -> dict[str, object]:
    """Build the path- and timing-independent outer mutation report."""

    require(
        len(rows) == REQUIRED_MUTATION_COUNT,
        "FINAL_MUTATION_CENSUS_FAIL",
        len(rows),
    )

    payload: dict[str, object] = {
        "schema": "k2p-principal-d-plus-final-release-mutations-v2",
        "status": "PASS" if not blockers else "BLOCKED",
        "blockers": blockers,
        "survivors": 0,
        "required_mutation_count": REQUIRED_MUTATION_COUNT,
        "observed_mutation_count": len(rows),
        "mutations": rows,
        "output_contract_preflight": "PASS",
        "portability_contract": (
            "The report excludes elapsed times, temporary paths, raw child output, "
            "and raw-output hashes; rejection evidence is limited to exact stable "
            "semantic diagnostics and return codes."
        ),
    }
    report = dict(payload)
    report["payload_sha256"] = sha_object(payload)
    return report


def output_contract_preflight(timeout: float) -> None:
    for name, script, marker in (
        (
            "final_mutation_output_contract",
            HERE / "test_release_mutation_output_contract.py",
            b"K2P_FINAL_RELEASE_MUTATION_OUTPUT_CONTRACT_PASS",
        ),
        (
            "nested_mutation_output_contract",
            HERE / "test_nested_mutation_output_contract.py",
            b"K2P_NESTED_MUTATION_OUTPUT_CONTRACT_PASS",
        ),
        (
            "final_replay_output_contract",
            HERE / "test_final_replay_output_contract.py",
            b"K2P_FINAL_REPLAY_OUTPUT_CONTRACT_PASS",
        ),
        (
            "semantic_mutation_diagnostic_contract",
            HERE / "test_semantic_mutation_diagnostic_contracts.py",
            b"K2P_SEMANTIC_MUTATION_DIAGNOSTIC_CONTRACTS_PASS qualified=9 negative_controls=49",
        ),
    ):
        result = run(
            name,
            [python(), "-B", str(script)],
            timeout=timeout,
        )
        output = result.stdout + result.stderr
        require(
            result.returncode == 0 and marker in output,
            "FINAL_RELEASE_MUTATION_OUTPUT_CONTRACT_FAIL",
            f"{name}:{output[-4000:]}",
        )
    print("K2P_FINAL_MUTATION_OUTPUT_CONTRACT_PASS", flush=True)


def resign(payload: dict[str, Any], field: str = "payload_sha256") -> None:
    payload.pop(field, None)
    payload[field] = sha_object(payload)


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


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
    strict_root = root / "work/final_theorem_release"
    strict_root.mkdir(parents=True)
    (strict_root / "strict_json.py").symlink_to(HERE / "strict_json.py")
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
    observed = temporary / "corrected_raw4_full_map_mutations.json"
    result = run(
        "corrected_raw4_mutations",
        [
            python(),
            "-B",
            str(overlay / "mutation_tests.py"),
            "--output",
            str(observed),
            "--timeout-seconds",
            str(timeout),
        ],
        cwd=root,
        timeout=max(10 * timeout + 300.0, 3_600.0),
    )
    output = result.stdout + result.stderr
    require(
        result.returncode == 0 and b'"status": "PASS"' in output,
        "CORRECTED_RAW4_MUTATION_SUITE_FAIL",
        output[-4000:],
    )
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
    strict_root = root / "work/final_theorem_release"
    strict_root.mkdir(parents=True)
    (strict_root / "strict_json.py").symlink_to(HERE / "strict_json.py")
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
    observed = temporary / "theta2_full_map_mutations.json"
    result = run(
        "theta2_full_map_mutations",
        [
            python(),
            "-B",
            str(package / "mutation_tests.py"),
            "--output",
            str(observed),
            "--timeout-seconds",
            str(timeout),
        ],
        cwd=root,
        timeout=max(11 * timeout + 300.0, 3_600.0),
    )
    output = result.stdout + result.stderr
    require(
        result.returncode == 0 and b'"status": "PASS"' in output,
        "THETA2_FULL_MAP_MUTATION_SUITE_FAIL",
        output[-4000:],
    )
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


def weak_sharpness_mutation_gate(
    rows: list[dict[str, object]], temporary: Path, timeout: float
) -> None:
    """Freshly rerun and byte-bind the exact typed weak-sharpness attacks."""

    root = PROJECT / "work/weak_sharpness_audit"
    frozen = root / "mutation_report.json"
    summary = validate_weak_sharpness_mutation_evidence(PROJECT)
    observed = temporary / "weak_sharpness_mutations.json"
    result = run(
        "weak_sharpness_mutations",
        [
            python(),
            "-B",
            str(root / "test_mutations.py"),
            "--output",
            str(observed),
            "--timeout-seconds",
            str(max(timeout, 60.0)),
        ],
        timeout=max(timeout, 120.0),
    )
    output = result.stdout + result.stderr
    require(
        result.returncode == 0
        and b"K2P_WEAK_SHARPNESS_AUDIT_MUTATIONS_PASS" in output.splitlines()
        and observed.is_file(),
        "WEAK_SHARPNESS_FRESH_MUTATION_SUITE_FAIL",
        output[-4000:],
    )
    require(
        observed.read_bytes() == frozen.read_bytes(),
        "WEAK_SHARPNESS_MUTATION_REPORT_BYTE_DRIFT",
    )
    fresh = load_json(observed)
    require(
        fresh.get("payload_sha256") == summary["payload_sha256"]
        and fresh.get("mutation_count") == 21
        and fresh.get("mutations_survived") == 0,
        "WEAK_SHARPNESS_MUTATION_REPORT_FAIL",
    )
    rows.append(
        {
            "name": "weak_sharpness_mutations",
            "status": "REJECTED",
            "source": "21/21 exact typed graph, tensor, rank, cherry, and optimized-mode attacks",
            "mutation_payload_sha256": summary["payload_sha256"],
            "producer_mutation_count": 21,
        }
    )
    print("K2P_FINAL_MUTATION_REJECTED name=weak_sharpness_mutations", flush=True)


def restoration_v3_mutation_gate(
    rows: list[dict[str, object]], temporary: Path, timeout: float
) -> None:
    """Freshly rerun and bind the 13-case clean-forest mutation suite."""

    paths = locator_artifacts(corrected_locator())
    summary = validate_restoration_v3_package(paths)
    frozen_report = load_json(paths["restoration_v3_mutation_report"])
    fresh_path = temporary / "corrected_restoration_mutations.json"
    result = run(
        "corrected_restoration_v3_mutations",
        [
            python(),
            "-B",
            str(paths["restoration_v3_mutation_runner"]),
            "--output",
            str(fresh_path),
        ],
        timeout=max(timeout, 1_200.0),
    )
    output = result.stdout + result.stderr
    require(
        result.returncode == 0
        and b"K2P_CORRECTED_RESTORATION_MUTATIONS_PASS" in output
        and fresh_path.is_file(),
        "RESTORATION_V3_FRESH_MUTATION_SUITE_FAIL",
        output[-4000:],
    )
    report = load_json(fresh_path)
    require(
        report.get("payload_sha256") == frozen_report.get("payload_sha256"),
        "RESTORATION_V3_FRESH_MUTATION_PAYLOAD_DRIFT",
    )
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
                "fresh clean-forest suite, 13/13: omitted child, wrong "
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
    temporary: Path,
    timeout: float,
) -> dict[str, Any]:
    """Rerun both verifier-facing primitive-composite mutation suites.

    Each producer streams complete mutant ledgers one at a time, invokes the
    production independent verifier, and records the intended semantic failure.
    This outer gate writes reports only under its own temporary directory and
    requires them to equal the frozen path-independent reports byte for byte.
    """

    summary, _blockers = validate_corrected_finite_universe()
    raw4 = summary["raw4_composite"]
    theta2 = summary["theta2_composite"]
    runner = PROJECT / "work/corrected_composite_ledgers/run_composite_mutations.py"
    artifacts = PROJECT / "work/corrected_composite_ledgers/artifacts"
    fresh_reports: dict[str, dict[str, Any]] = {}
    for family, expected_count in (("raw4", 14), ("theta2", 12)):
        report = temporary / f"{family}_corrected_composite_mutations.json"
        result = run(
            f"{family}_corrected_composite_mutations",
            [
                python(),
                "-B",
                str(runner),
                "--family",
                family,
                "--output",
                str(report),
                "--timeout-seconds",
                str(timeout),
            ],
            timeout=timeout * expected_count,
        )
        output = result.stdout + result.stderr
        require(
            result.returncode == 0 and report.is_file(),
            "CORRECTED_COMPOSITE_MUTATION_RERUN_FAIL",
            f"{family}:{output[-4000:]}",
        )
        frozen = artifacts / f"{family}_corrected_composite_mutations.json"
        require(
            report.read_bytes() == frozen.read_bytes(),
            "CORRECTED_COMPOSITE_MUTATION_REPORT_BYTE_DRIFT",
            family,
        )
        payload = load_json(report)
        require(
            payload.get("status") == "PASS"
            and payload.get("test_count") == expected_count
            and payload.get("semantic_ledger_attack_count")
            == (12 if family == "raw4" else 10),
            "CORRECTED_COMPOSITE_MUTATION_RERUN_REPORT_FAIL",
            family,
        )
        fresh_reports[family] = payload
    require(
        fresh_reports["raw4"]["payload_sha256"]
        == raw4["mutation_payload_sha256"]
        and fresh_reports["theta2"]["payload_sha256"]
        == theta2["mutation_payload_sha256"],
        "CORRECTED_COMPOSITE_MUTATION_PAYLOAD_BINDING_FAIL",
    )
    rows.append(
        {
            "name": "corrected_primitive_composite_mutations",
            "status": "REJECTED",
            "source": (
                "fresh verifier-facing raw4 14/14 and theta2 12/12 suites: "
                "22 complete disposable-ledger attacks plus optimized-mode "
                "and aggregate source-immutability guards"
            ),
            "raw4_mutation_payload_sha256": fresh_reports["raw4"]["payload_sha256"],
            "theta2_mutation_payload_sha256": fresh_reports["theta2"]["payload_sha256"],
            "producer_mutation_count": 26,
            "verifier_facing_ledger_attack_count": 22,
        }
    )
    print(
        "K2P_FINAL_MUTATION_REJECTED "
        "name=corrected_primitive_composite_mutations",
        flush=True,
    )
    return summary


def corrected_probe_mutation_gate(
    rows: list[dict[str, object]],
    summary: dict[str, Any],
    temporary: Path,
    timeout: float,
) -> None:
    """Freshly rerun the two-stage probe mutations against both ledgers."""

    probe = summary["probe_producer"]
    require(
        probe["status"] == "PASS",
        "CORRECTED_PROBE_MUTATION_GATE_STATUS_FAIL",
    )
    paths = locator_artifacts(corrected_locator())
    frozen_report = load_json(paths["probe_mutation_report"])
    fresh_path = temporary / "corrected_probe_mutations.json"
    result = run(
        "corrected_two_stage_probe_mutations",
        [
            python(),
            "-B",
            str(paths["probe_mutation_runner"]),
            "--output",
            str(fresh_path),
        ],
        timeout=max(timeout, 1_200.0),
    )
    output = result.stdout + result.stderr
    require(
        result.returncode == 0
        and b"K2P_CORRECTED_PROBE_MUTATIONS_PASS" in output
        and fresh_path.is_file(),
        "CORRECTED_PROBE_FRESH_MUTATION_SUITE_FAIL",
        output[-4000:],
    )
    fresh_report = load_json(fresh_path)
    require(
        fresh_report.get("payload_sha256") == frozen_report.get("payload_sha256")
        == probe["mutation_payload_sha256"],
        "CORRECTED_PROBE_FRESH_MUTATION_PAYLOAD_DRIFT",
    )
    rows.append(
        {
            "name": "corrected_two_stage_probe_mutations",
            "status": "REJECTED",
            "source": (
                "fresh 18/18 suite plus nondefault hash-seed replay: omitted "
                "one-/two-port rows and parent, wrong parents, reversed order, "
                "global triangle, exact transport/restriction, T_i/Bernstein, "
                "classifier precedence, duplicate/noncanonical JSON, and "
                "optimized mode"
            ),
            "mutation_payload_sha256": probe["mutation_payload_sha256"],
            "site_partition_payload_sha256": probe[
                "site_partition_payload_sha256"
            ],
            "producer_mutation_count": 18,
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
        (
            "promotion_theorem_status",
            mutate_manuscript,
            "PROMOTION_MANUSCRIPT_FILE_DRIFT:work/global_theorem_closure/"
            "promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md",
        ),
        (
            "promotion_quantifier_checklist",
            mutate_quantifier,
            "PROMOTION_MANUSCRIPT_FILE_DRIFT:work/global_theorem_closure/"
            "promotion_manuscript/QUANTIFIER_AUDIT.md",
        ),
        *(
            (
                name,
                action,
                "PROMOTION_MANUSCRIPT_FILE_DRIFT:work/global_theorem_closure/"
                "promotion_manuscript/PROBE_PROMOTION_PLACEHOLDER.json",
            )
            for name, action in (
                ("promotion_pass_gate", lambda root: mutate_binding(root, "pass")),
                ("promotion_zero_gate", lambda root: mutate_binding(root, "zero")),
                ("promotion_ledger_path", lambda root: mutate_binding(root, "ledger")),
                ("promotion_combined_root", lambda root: mutate_binding(root, "root")),
            )
        ),
    )
    for ordinal, (name, mutate, expected_diagnostic) in enumerate(cases):
        project = temporary / f"promotion-{ordinal}"
        package = project / "work/global_theorem_closure/promotion_manuscript"
        package.parent.mkdir(parents=True)
        shutil.copytree(source, package)
        mutate(package)
        try:
            validate_promotion_manuscript(corrected_summary, project)
        except ReleaseFailure as error:
            require(
                str(error) == expected_diagnostic,
                "PROMOTION_MUTATION_WRONG_REJECTION",
                {
                    "name": name,
                    "expected": expected_diagnostic,
                    "observed": str(error),
                },
            )
        else:
            raise ReleaseFailure(f"MUTATION_SURVIVED:{name}")
        rows.append(
            {
                "name": name,
                "status": "REJECTED",
                "source": "promotion package exact byte-binding gate",
                "expected_diagnostic": expected_diagnostic,
            }
        )
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

    expected_diagnostics = {
        "historical_artifact_promoted": (
            "HISTORICAL_REGISTRY_PROMOTION_AUTHORITY_FAIL:"
            "work/adversarial_proof_review/PROBE_AUDIT.md"
        ),
        "historical_authoritative_replacement_removed": (
            "HISTORICAL_REGISTRY_REPLACEMENT_FAIL:"
            "work/adversarial_proof_review/PROBE_AUDIT.md"
        ),
        "historical_scanner_record_omitted": (
            "HISTORICAL_REGISTRY_SCANNER_COVERAGE_FAIL"
        ),
    }
    for name, mutate in (
        ("historical_artifact_promoted", promote_legacy),
        ("historical_authoritative_replacement_removed", remove_replacement),
        ("historical_scanner_record_omitted", omit_scanner_row),
    ):
        payload = copy.deepcopy(source)
        mutate(payload)
        resign(payload)
        expected_diagnostic = expected_diagnostics[name]
        try:
            validate_historical_artifact_registry(PROJECT, payload)
        except ReleaseFailure as error:
            require(
                str(error) == expected_diagnostic,
                "HISTORICAL_REGISTRY_MUTATION_WRONG_REJECTION",
                {
                    "name": name,
                    "expected": expected_diagnostic,
                    "observed": str(error),
                },
            )
        else:
            raise ReleaseFailure(f"MUTATION_SURVIVED:{name}")
        rows.append(
            {
                "name": name,
                "status": "REJECTED",
                "source": "historical artifact quarantine registry exact binding",
                "expected_diagnostic": expected_diagnostic,
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
            "PROBE_STRUCTURAL_REPLAY_FAIL",
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
        "test_direct_closure_release_mutations.py",
        "direct_closure_mutation_report.json",
        "proofs/four_port_direct_residual_closure_certificate.json",
    )
    return {relative: sha_file(root / relative) for relative in relatives}


def direct_closure_mutation_gate(
    temporary: Path, timeout: float
) -> dict[str, object]:
    """Freshly replay and byte-bind the exact 11-case direct mutation suite."""

    root = PROJECT / "package/referee/k2p_offline_sweep_portable"
    frozen = root / "direct_closure_mutation_report.json"
    summary = validate_direct_closure_mutation_evidence(PROJECT)
    observed = temporary / "direct_closure_mutations.json"
    child_timeout = max(timeout, 240.0)
    result = run(
        "direct_closure_mutation_suite",
        [
            python(),
            "-B",
            str(root / "test_direct_closure_release_mutations.py"),
            "--package-root",
            str(root),
            "--timeout-seconds",
            str(child_timeout),
            "--output",
            str(observed),
        ],
        cwd=root,
        timeout=max(12.0 * child_timeout + 60.0, 600.0),
    )
    output = result.stdout + result.stderr
    require(
        result.returncode == 0
        and b"DIRECT_CLOSURE_RELEASE_MUTATIONS_PASS" in output.splitlines()
        and observed.is_file(),
        "DIRECT_CLOSURE_FRESH_MUTATION_SUITE_FAIL",
        output[-4000:],
    )
    require(
        observed.read_bytes() == frozen.read_bytes(),
        "DIRECT_CLOSURE_MUTATION_REPORT_BYTE_DRIFT",
    )
    fresh = load_json(observed)
    require(
        fresh.get("payload_sha256") == summary["payload_sha256"]
        and fresh.get("case_count") == 11
        and fresh.get("mutations_survived") == 0,
        "DIRECT_CLOSURE_MUTATION_REPORT_FAIL",
    )
    print("K2P_FINAL_DIRECT_MUTATION_PREFLIGHT_PASS cases=11", flush=True)
    return summary


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
    nested_mutation_payload_sha256: str,
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
        row = accepted_rejection(
            label,
            result,
            "DIRECT_OVERLAY_CERTIFICATE_BYTE_MISMATCH",
        )
        row["direct_mutation_payload_sha256"] = nested_mutation_payload_sha256
        rows.append(row)
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
            "FINAL_THEOREM_RELEASE_OPTIMIZED_MODE_FORBIDDEN",
        )
    )


def fail_closed_evidence_mutation_suites(
    rows: list[dict[str, object]], temporary: Path, timeout: float
) -> None:
    """Replay the quartet, canonicalizer, transport, and rank attacks."""

    quartet = PROJECT / "work/quartet_separation_closure"
    relocation_result = run(
        "quartet_semantics_relocation",
        [
            python(),
            "-B",
            str(quartet / "test_quartet_semantics_relocation.py"),
        ],
        timeout=timeout,
    )
    relocation_output = relocation_result.stdout + relocation_result.stderr
    require(
        relocation_result.returncode == 0
        and b"K2P_QUARTET_SEMANTICS_RELOCATION_PASS" in relocation_output,
        "QUARTET_SEMANTICS_RELOCATION_FAIL",
        relocation_output[-4000:],
    )
    semantic_certificate = quartet / "quartet_semantics_mutation_certificate.json"
    semantic_expected = semantic_certificate.read_bytes()
    semantic_output_path = temporary / "quartet_semantics_mutations.json"
    semantic_result = run(
        "quartet_semantics_mutations",
        [
            python(),
            "-B",
            str(quartet / "test_quartet_semantics_mutations.py"),
            "--output",
            str(semantic_output_path),
        ],
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
        semantic_output_path.is_file()
        and semantic_output_path.read_bytes() == semantic_expected,
        "QUARTET_SEMANTICS_MUTATION_REPORT_BYTE_DRIFT",
    )
    semantic = load_json(semantic_output_path)
    require(
        semantic.get("schema") == "k2p-quartet-semantics-mutations-v4"
        and semantic.get("status") == "PASS"
        and semantic.get("case_count") == 8
        and semantic.get("survived") == 0
        and semantic.get("mutation_runner_sha256")
        == sha_file(quartet / "test_quartet_semantics_mutations.py")
        and semantic.get("production_verifier_sha256")
        == sha_file(quartet / "verify_quartet_logic.py")
        and semantic.get("clean_baseline", {}).get("verifier_exit_code") == 0
        and semantic.get("clean_baseline", {}).get(
            "success_artifact_byte_identical_to_stored"
        ) is True
        and semantic.get("source_fingerprints_unchanged") is True
        and all(
            row.get("status") == "REJECTED"
            and row.get("rejected") is True
            and row.get("verifier_exit_code") == 1
            and row.get("observed_semantic_diagnostic")
            == row.get("expected_semantic_diagnostic")
            and row.get("semantic_diagnostic_matched") is True
            and row.get("success_artifact_created") is False
            and row.get("traceback_observed") is False
            and row.get("import_failure_observed") is False
            for row in semantic.get("cases", [])
        ),
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
        terminal.get("schema")
        == "k2p-quartet-terminal-binding-mutations-v2"
        and terminal.get("status") == "PASS"
        and terminal.get("case_count") == 12
        and terminal.get("survived") == 0
        and terminal.get("mutation_runner_sha256")
        == sha_file(quartet / "test_quartet_terminal_binding_mutations.py")
        and terminal.get("binder_sha256")
        == sha_file(quartet / "verify_quartet_terminal_bindings.py")
        and terminal.get("clean_baseline", {}).get("verifier_exit_code") == 0
        and terminal.get("clean_baseline", {}).get("quartet_terminal_rows")
        == 4_414_710
        and terminal.get("clean_baseline", {}).get(
            "success_artifact_byte_identical_to_stored"
        ) is True
        and terminal.get("source_fingerprints_unchanged") is True
        and all(
            row.get("status") == "REJECTED" and row.get("rejected") is True
            for row in terminal.get("cases", [])
        ),
        "QUARTET_TERMINAL_MUTATION_REPORT_FAIL",
    )
    # The freshly generated disposable reports are byte-identical to their
    # authoritative reports above.  Apply the independent strict binder to
    # those authoritative bytes so every case diagnostic/type, clean baseline,
    # graph guard, output policy, and negative control is checked here too.
    validate_quartet_evidence()
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
    canonicalizer_report_path = temporary / "canonicalizer_mutations.json"
    canonicalizer_result = run(
        "canonicalizer_completeness_mutations",
        [
            python(),
            "-B",
            str(canonicalizer / "test_canonicalizer_mutations.py"),
            "--output",
            str(canonicalizer_report_path),
        ],
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
        canonicalizer_report_path.is_file()
        and canonicalizer_report_path.read_bytes() == canonicalizer_expected
        and canonicalizer_certificate.read_bytes() == canonicalizer_expected,
        "CANONICALIZER_MUTATION_REPORT_BYTE_DRIFT",
    )
    canonicalizer_report = load_json(canonicalizer_report_path)
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
    transport_report_path = temporary / "parameter_transport_mutations.json"
    transport_result = run(
        "parameter_transport_mutations",
        [
            python(),
            "-B",
            str(transport / "run_parameter_transport_mutations.py"),
            "--output",
            str(transport_report_path),
            "--timeout-seconds",
            str(max(timeout, 1_200.0)),
        ],
        timeout=max(5 * max(timeout, 1_200.0) + 300.0, 2_400.0),
    )
    transport_output = transport_result.stdout + transport_result.stderr
    require(
        transport_result.returncode == 0
        and b"PARAMETER_TRANSPORT_MUTATIONS_PASS" in transport_output,
        "PARAMETER_TRANSPORT_MUTATION_SUITE_FAIL",
        transport_output[-4000:],
    )
    require(
        transport_report_path.is_file()
        and transport_report_path.read_bytes() == transport_expected
        and transport_certificate.read_bytes() == transport_expected,
        "PARAMETER_TRANSPORT_MUTATION_REPORT_BYTE_DRIFT",
    )
    transport_report = load_json(transport_report_path)
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

    rank = PROJECT / "work/rank_upper_certificates"
    rank_certificate = rank / "mutation_report.json"
    rank_expected = rank_certificate.read_bytes()
    rank_report_path = temporary / "rank_upper_mutations.json"
    rank_result = run(
        "rank_upper_mutations",
        [
            python(),
            "-B",
            str(rank / "mutation_tests.py"),
            "--output",
            str(rank_report_path),
            "--timeout-seconds",
            str(max(timeout, 1_200.0)),
        ],
        timeout=max(2 * max(timeout, 1_200.0) + 300.0, 1_800.0),
        environment_overrides={
            "PYTHONPATH": os.pathsep.join(
                (
                    str(PROJECT / "package/referee/k2p_offline_sweep_portable/atlas"),
                    str(rank),
                )
            )
        },
    )
    rank_output = rank_result.stdout + rank_result.stderr
    require(
        rank_result.returncode == 0
        and b"K2P_RANK_UPPER_MUTATIONS_PASS" in rank_output,
        "RANK_UPPER_MUTATION_SUITE_FAIL",
        rank_output[-4000:],
    )
    require(
        rank_report_path.is_file()
        and rank_report_path.read_bytes() == rank_expected
        and rank_certificate.read_bytes() == rank_expected,
        "RANK_UPPER_MUTATION_REPORT_BYTE_DRIFT",
    )
    rank_report = load_json(rank_report_path)
    require(
        rank_report.get("schema") == "k2p-rank-upper-adversarial-mutations-v2"
        and rank_report.get("status") == "pass"
        and rank_report.get("mutation_count") == 7
        and rank_report.get("complete_production_verifier_attacks") == 1
        and rank_report.get("survivors") == 0
        and rank_report.get("clean_baseline", {}).get(
            "stored_authoritative_replay_byte_identical"
        )
        is True,
        "RANK_UPPER_MUTATION_REPORT_FAIL",
    )
    rows.append(
        {
            "name": "rank_upper_mutations",
            "status": "REJECTED",
            "source": (
                "7/7 rank coverage, syzygy, orbit, port-transport, false-rank, "
                "and complete production-verifier attacks"
            ),
            "mutation_payload_sha256": rank_report["payload_sha256"],
            "producer_mutation_count": 7,
            "complete_production_verifier_attacks": 1,
        }
    )
    print(
        "K2P_FINAL_MUTATION_REJECTED name=rank_upper_mutations",
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout-seconds", type=float, default=1200.0)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--audit-blocked", action="store_true")
    args = parser.parse_args()
    report_output = validate_report_output_path(args.output)
    prepare_report_output(report_output)
    if not __debug__:
        raise SystemExit("FINAL_RELEASE_MUTATIONS_OPTIMIZED_MODE_FORBIDDEN")
    require(args.timeout_seconds > 0, "INVALID_MUTATION_TIMEOUT")
    validate_runtime_environment()
    output_contract_preflight(args.timeout_seconds)
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
            corrected_raw4_mutations(rows, temporary, args.timeout_seconds)
            theta2_full_map_mutations(rows, temporary, args.timeout_seconds)
            corrected_summary = corrected_composite_mutation_gate(
                rows, temporary, args.timeout_seconds
            )
            restoration_v3_mutation_gate(
                rows, temporary, args.timeout_seconds
            )
            corrected_probe_mutation_gate(
                rows, corrected_summary, temporary, args.timeout_seconds
            )
            promotion_package_mutations(rows, temporary, corrected_summary)
            historical_registry_mutations(rows)
            weak_sharpness_mutation_gate(rows, temporary, args.timeout_seconds)
            direct_mutation_summary = direct_closure_mutation_gate(
                temporary, args.timeout_seconds
            )
            reassign_direct_family(
                rows,
                temporary,
                args.timeout_seconds,
                "theta3_cubic",
                "lower_theta_quartic",
                str(direct_mutation_summary["payload_sha256"]),
            )
            reassign_direct_family(
                rows,
                temporary,
                args.timeout_seconds,
                "lower_theta_quartic",
                "theta0_quintic_port_orbit",
                str(direct_mutation_summary["payload_sha256"]),
            )
            reassign_direct_family(
                rows,
                temporary,
                args.timeout_seconds,
                "theta0_quintic_port_orbit",
                "theta3_cubic",
                str(direct_mutation_summary["payload_sha256"]),
            )
            blockers.extend(truth_oracle_mutation_gate(rows))
    require(
        direct_source_fingerprint() == direct_before,
        "DIRECT_SOURCE_CHANGED_BY_MUTATION_SUITE",
    )
    require(
        len(rows) == REQUIRED_MUTATION_COUNT,
        "FINAL_MUTATION_CENSUS_FAIL",
        len(rows),
    )
    report = build_report(rows, blockers)
    if report_output:
        atomic_write_text(
            report_output, json.dumps(report, indent=2, sort_keys=True) + "\n"
        )
    if blockers:
        print("K2P_FINAL_RELEASE_MUTATIONS_BLOCKED")
        print(json.dumps(report, sort_keys=True))
        return 2 if args.audit_blocked else 1
    print("K2P_FINAL_RELEASE_MUTATIONS_PASS")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ReleaseFailure as error:
        raise SystemExit(f"FINAL_RELEASE_MUTATIONS_FAIL:{error}") from error
