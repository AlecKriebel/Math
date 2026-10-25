#!/usr/bin/env python3
"""Fail-closed mutations for the unified five-family certificate."""

from __future__ import annotations

import argparse
import copy
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

from release_common import (
    HERE,
    PROJECT,
    corrected_locator,
    load_json,
    require,
    sha_file,
    sha_object,
    verify_payload_hash,
)


CERTIFICATE = HERE / "corrected_universe_certificate.json"
VERIFIER = HERE / "verify_corrected_universe_independent.py"
DEFAULT_OUTPUT = HERE / "corrected_universe_mutation_report.json"
AUTHORITATIVE_OUTPUT = DEFAULT_OUTPUT
EXPECTED_REPLAY = HERE / "corrected_universe_independent_replay.json"
FORBIDDEN_FAILURE_MARKERS = (
    "Traceback (most recent call last)",
    "ModuleNotFoundError",
    "ImportError",
    "No module named",
)
MUTATION_DIAGNOSTICS = {
    "omitted_raw_row": "CORRECTED_UNIVERSE_REPLAY_FAIL:UNIFIED_REPLAY_CERTIFICATE_MISMATCH",
    "false_rank_exclusion": "CORRECTED_UNIVERSE_REPLAY_FAIL:UNIFIED_REPLAY_CERTIFICATE_MISMATCH",
    "missing_child": "CORRECTED_UNIVERSE_REPLAY_FAIL:UNIFIED_REPLAY_CERTIFICATE_MISMATCH",
    "wrong_parent": "CORRECTED_UNIVERSE_REPLAY_FAIL:UNIFIED_REPLAY_CERTIFICATE_MISMATCH",
    "broken_transport": "CORRECTED_UNIVERSE_REPLAY_FAIL:UNIFIED_REPLAY_CERTIFICATE_MISMATCH",
    "reassigned_quadratic_certificate": "CORRECTED_UNIVERSE_REPLAY_FAIL:UNIFIED_REPLAY_CERTIFICATE_MISMATCH",
    "reassigned_cubic_certificate": "CORRECTED_UNIVERSE_REPLAY_FAIL:UNIFIED_REPLAY_CERTIFICATE_MISMATCH",
    "reassigned_quartic_certificate": "CORRECTED_UNIVERSE_REPLAY_FAIL:UNIFIED_REPLAY_CERTIFICATE_MISMATCH",
    "reassigned_quintic_certificate": "CORRECTED_UNIVERSE_REPLAY_FAIL:UNIFIED_REPLAY_CERTIFICATE_MISMATCH",
    "raw4424_false_tree_sunlet_reintroduction": "CORRECTED_UNIVERSE_REPLAY_FAIL:UNIFIED_REPLAY_CERTIFICATE_MISMATCH",
    "rooted_restriction_reintroduction": "CORRECTED_UNIVERSE_REPLAY_FAIL:UNIFIED_REPLAY_ROOTED_REASON_FAIL",
    "source_tree_write": "CORRECTED_UNIVERSE_REPLAY_FAIL:UNIFIED_REPLAY_CERTIFICATE_MISMATCH",
    "omitted_probe_one_port_row": "CORRECTED_UNIVERSE_REPLAY_FAIL:UNIFIED_REPLAY_CERTIFICATE_MISMATCH",
    "omitted_probe_two_port_parent": "CORRECTED_UNIVERSE_REPLAY_FAIL:UNIFIED_REPLAY_CERTIFICATE_MISMATCH",
    "omitted_probe_two_port_row": "CORRECTED_UNIVERSE_REPLAY_FAIL:UNIFIED_REPLAY_CERTIFICATE_MISMATCH",
    "wrong_probe_parent": "CORRECTED_UNIVERSE_REPLAY_FAIL:UNIFIED_REPLAY_CERTIFICATE_MISMATCH",
    "broken_probe_transport": "CORRECTED_UNIVERSE_REPLAY_FAIL:UNIFIED_REPLAY_CERTIFICATE_MISMATCH",
    "broken_probe_restriction": "CORRECTED_UNIVERSE_REPLAY_FAIL:UNIFIED_REPLAY_CERTIFICATE_MISMATCH",
    "reassigned_probe_Ti_certificate": "CORRECTED_UNIVERSE_REPLAY_FAIL:UNIFIED_REPLAY_CERTIFICATE_MISMATCH",
    "reversed_probe_order_class": "CORRECTED_UNIVERSE_REPLAY_FAIL:UNIFIED_REPLAY_CERTIFICATE_MISMATCH",
    "inconsistent_probe_global_triangle": "CORRECTED_UNIVERSE_REPLAY_FAIL:UNIFIED_REPLAY_CERTIFICATE_MISMATCH",
    "optimized_mode": "CORRECTED_UNIVERSE_REPLAY_OPTIMIZED_MODE_FORBIDDEN",
}


def qualified_python() -> str:
    candidate = PROJECT / ".venv/bin/python"
    return str(candidate if candidate.is_file() else Path(sys.executable))


def fingerprint() -> dict[str, str]:
    # The caller-owned report is deliberately absent while the suite runs, so
    # it cannot be part of the immutable-input fingerprint.  Every other
    # located byte remains checked against the locator before and after the
    # mutations.
    locator = corrected_locator()
    result: dict[str, str] = {}
    for role, row in sorted(locator["artifacts"].items()):
        if role == "corrected_universe_mutation_report":
            continue
        path = PROJECT / row["path"]
        digest = sha_file(path)
        require(digest == row["sha256"], "CORRECTED_LOCATOR_ARTIFACT_DRIFT", role)
        result[role] = digest
    return result


def validate_output_path(output: Path, allow_authoritative_output: bool) -> Path:
    lexical = Path(os.path.abspath(os.fspath(output)))
    normalized = lexical.parent.resolve() / lexical.name
    resolved = lexical.resolve()
    authoritative = AUTHORITATIVE_OUTPUT.parent.resolve() / AUTHORITATIVE_OUTPUT.name
    if allow_authoritative_output:
        if normalized != authoritative or lexical.is_symlink():
            raise SystemExit(
                "CORRECTED_UNIVERSE_MUTATION_OUTPUT_POLICY_FAIL: authoritative "
                "override licenses only the canonical unified mutation report"
            )
        return normalized
    project_root = PROJECT.resolve()
    for candidate in (normalized, resolved):
        try:
            candidate.relative_to(project_root)
        except ValueError:
            continue
        break
    else:
        return normalized
    raise SystemExit(
        "CORRECTED_UNIVERSE_MUTATION_OUTPUT_POLICY_FAIL: routine output must be "
        "outside the project source tree"
    )


def seal(certificate: dict[str, Any]) -> None:
    certificate.pop("payload_sha256", None)
    certificate["payload_sha256"] = sha_object(certificate)


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def atomic_write_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o644)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        temporary.unlink(missing_ok=True)


def encoded_json(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def decoded_timeout_output(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def invoke_verifier(
    certificate: Path,
    output: Path,
    timeout: float,
    *,
    optimized: bool = False,
) -> dict[str, object]:
    output.unlink(missing_ok=True)
    command = [qualified_python()]
    if optimized:
        command.append("-O")
    command.extend(
        [
            "-B",
            str(VERIFIER),
            "--certificate",
            str(certificate),
            "--output",
            str(output),
        ]
    )
    try:
        result = subprocess.run(
            command,
            cwd=PROJECT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        return {
            "returncode": None,
            "diagnostic": (
                decoded_timeout_output(error.stdout)
                + decoded_timeout_output(error.stderr)
            ).strip(),
            "success_artifact_present": output.exists(),
            "timeout": True,
            "signal": False,
        }
    return {
        "returncode": result.returncode,
        "diagnostic": (result.stdout + result.stderr).strip(),
        "success_artifact_present": output.exists(),
        "timeout": False,
        "signal": result.returncode < 0,
    }


def qualify_mutation_failure(
    name: str, result: dict[str, object]
) -> dict[str, object]:
    expected = MUTATION_DIAGNOSTICS[name]
    require(result.get("timeout") is False, "UNIFIED_MUTATION_TIMEOUT", name)
    require(result.get("signal") is False, "UNIFIED_MUTATION_SIGNAL", name)
    require(result.get("returncode") == 1, "UNIFIED_MUTATION_EXIT", name)
    diagnostic = result.get("diagnostic")
    require(isinstance(diagnostic, str), "UNIFIED_MUTATION_DIAGNOSTIC_TYPE", name)
    require(
        not any(marker in diagnostic for marker in FORBIDDEN_FAILURE_MARKERS),
        "UNIFIED_MUTATION_UNRELATED_CRASH",
        name,
    )
    require(
        result.get("success_artifact_present") is False,
        "UNIFIED_MUTATION_SUCCESS_ARTIFACT",
        name,
    )
    require(diagnostic == expected, "UNIFIED_MUTATION_WRONG_DIAGNOSTIC", name)
    return {
        "name": name,
        "rejected": True,
        "returncode": 1,
        "expected_diagnostic": expected,
        "observed_diagnostic": expected,
        "success_artifact_absent": True,
        "timeout": False,
        "signal": False,
    }


def qualify_clean_baseline(output: Path, result: dict[str, object]) -> dict[str, object]:
    require(result.get("timeout") is False, "UNIFIED_MUTATION_BASELINE_TIMEOUT")
    require(result.get("signal") is False, "UNIFIED_MUTATION_BASELINE_SIGNAL")
    require(result.get("returncode") == 0, "UNIFIED_MUTATION_BASELINE_EXIT")
    diagnostic = result.get("diagnostic")
    require(isinstance(diagnostic, str), "UNIFIED_MUTATION_BASELINE_DIAGNOSTIC")
    require(
        not any(marker in diagnostic for marker in FORBIDDEN_FAILURE_MARKERS),
        "UNIFIED_MUTATION_BASELINE_CRASH",
    )
    require(
        result.get("success_artifact_present") is True and output.is_file(),
        "UNIFIED_MUTATION_BASELINE_REPORT_ABSENT",
    )
    report = load_json(output)
    verify_payload_hash(report)
    expected = load_json(EXPECTED_REPLAY)
    verify_payload_hash(expected)
    require(report == expected, "UNIFIED_MUTATION_BASELINE_REPORT_DRIFT")
    require(
        report.get("schema")
        == "k2p-corrected-finite-universe-independent-replay-v2"
        and report.get("status") == "PASS"
        and report.get("family_count") == 5
        and report.get("unresolved") == 0
        and report.get("rooted_reason_count") == 0
        and report.get("source_tree_drift") == 0,
        "UNIFIED_MUTATION_BASELINE_SEMANTICS",
    )
    return {
        "returncode": 0,
        "status": "PASS",
        "report_schema": report["schema"],
        "report_status": report["status"],
        "report_payload_sha256": report["payload_sha256"],
        "success_artifact_present": True,
        "family_count": 5,
        "unresolved": 0,
        "rooted_reason_count": 0,
        "source_tree_drift": 0,
        "timeout": False,
        "signal": False,
    }


def set_zero_digest(container: dict[str, Any], field: str) -> None:
    container[field] = "0" * 64


def mutation_cases() -> list[tuple[str, Callable[[dict[str, Any]], None]]]:
    return [
        ("omitted_raw_row", lambda c: c["families"]["raw4"].__setitem__("input_count", c["families"]["raw4"]["input_count"] - 1)),
        ("false_rank_exclusion", lambda c: c["families"]["raw4"]["output_category_counts"].update({"exact_rank_exclusion": c["families"]["raw4"]["output_category_counts"]["exact_rank_exclusion"] + 1, "displayed_quartet_exclusion": c["families"]["raw4"]["output_category_counts"]["displayed_quartet_exclusion"] - 1})),
        ("missing_child", lambda c: c["families"]["restoration"]["generated_children"].__setitem__("count", c["families"]["restoration"]["generated_children"]["count"] - 1)),
        ("wrong_parent", lambda c: set_zero_digest(c["restoration_forest"], "class_parent_id_hash_root")),
        ("broken_transport", lambda c: set_zero_digest(c["restoration_forest"], "transport_restriction_hash_root")),
        ("reassigned_quadratic_certificate", lambda c: set_zero_digest(c["artifact_sha256"], "theta2_corrected_composite_summary")),
        ("reassigned_cubic_certificate", lambda c: set_zero_digest(c["artifact_sha256"], "raw4_terminal_certificate_registry")),
        ("reassigned_quartic_certificate", lambda c: c["artifact_sha256"].__setitem__("raw4_terminal_certificate_registry", "1" * 64)),
        ("reassigned_quintic_certificate", lambda c: c["artifact_sha256"].__setitem__("raw4_terminal_certificate_registry", "2" * 64)),
        ("raw4424_false_tree_sunlet_reintroduction", lambda c: c["families"]["raw4"].__setitem__("forbidden_rooted_reason_count", 1)),
        ("rooted_restriction_reintroduction", lambda c: c.__setitem__("rooted_reason_count", 1)),
        ("source_tree_write", lambda c: set_zero_digest(c, "source_tree_fingerprint_sha256")),
        ("omitted_probe_one_port_row", lambda c: c["probe_coherence"]["one_port"].__setitem__("raw_pair_count", c["probe_coherence"]["one_port"]["raw_pair_count"] - 1)),
        ("omitted_probe_two_port_parent", lambda c: c["probe_coherence"]["two_port"].__setitem__("parent_count", c["probe_coherence"]["two_port"]["parent_count"] - 1)),
        ("omitted_probe_two_port_row", lambda c: c["probe_coherence"]["two_port"].__setitem__("raw_pair_count", c["probe_coherence"]["two_port"]["raw_pair_count"] - 1)),
        ("wrong_probe_parent", lambda c: set_zero_digest(c["probe_coherence"]["two_port"], "parent_inventory_hash_root")),
        ("broken_probe_transport", lambda c: set_zero_digest(c["probe_coherence"], "transport_restriction_hash_root")),
        ("broken_probe_restriction", lambda c: set_zero_digest(c["probe_coherence"]["parent_restriction_registry"], "ordered_hash_root")),
        ("reassigned_probe_Ti_certificate", lambda c: set_zero_digest(c["probe_coherence"], "separation_registry_payload_sha256")),
        ("reversed_probe_order_class", lambda c: c["probe_coherence"]["two_port"].__setitem__("reversed_marginals_missing", 1)),
        ("inconsistent_probe_global_triangle", lambda c: c["probe_coherence"].__setitem__("incoherent", 1)),
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow-authoritative-output", action="store_true")
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    args = parser.parse_args()
    output_path = validate_output_path(args.output, args.allow_authoritative_output)
    output_path.unlink(missing_ok=True)
    if not __debug__:
        raise SystemExit("CORRECTED_UNIVERSE_MUTATIONS_OPTIMIZED_MODE_FORBIDDEN")
    require(args.timeout_seconds > 0, "UNIFIED_MUTATION_TIMEOUT_FAIL")
    source = load_json(CERTIFICATE)
    verify_payload_hash(source)
    before = fingerprint()
    results: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="k2p-unified-mutations-") as directory:
        root = Path(directory)
        baseline_output = root / "clean-baseline-replay.json"
        baseline = qualify_clean_baseline(
            baseline_output,
            invoke_verifier(CERTIFICATE, baseline_output, args.timeout_seconds),
        )
        for ordinal, (name, mutate) in enumerate(mutation_cases()):
            candidate = copy.deepcopy(source)
            mutate(candidate)
            seal(candidate)
            path = root / f"{ordinal:02d}-{name}.json"
            output = root / f"{ordinal:02d}-{name}-replay.json"
            write_json(path, candidate)
            results.append(
                qualify_mutation_failure(
                    name,
                    invoke_verifier(path, output, args.timeout_seconds),
                )
            )
        optimized_output = root / "optimized-replay.json"
        results.append(
            qualify_mutation_failure(
                "optimized_mode",
                invoke_verifier(
                    CERTIFICATE,
                    optimized_output,
                    args.timeout_seconds,
                    optimized=True,
                ),
            )
        )
    after = fingerprint()
    require(before == after, "UNIFIED_MUTATION_SOURCE_TREE_DRIFT")
    report = {
        "schema": "k2p-corrected-finite-universe-mutations-v3",
        "status": "PASS",
        "clean_baseline": baseline,
        "diagnostic_contract": MUTATION_DIAGNOSTICS,
        "source_certificate_sha256": sha_file(CERTIFICATE),
        "source_verifier_sha256": sha_file(VERIFIER),
        "mutation_runner_sha256": sha_file(Path(__file__).resolve()),
        "temporary_copies_only": True,
        "test_count": len(results),
        "survivors": 0,
        "source_tree_drift": 0,
        "execution_contract": {
            "clean_baseline_requires_exact_authoritative_replay": True,
            "mutations_require_exit_code_one": True,
            "mutations_require_exact_diagnostics": True,
            "traceback_import_timeout_signal_rejected": True,
            "success_artifact_must_be_absent": True,
            "caller_owned_output_required": True,
        },
        "tests": results,
    }
    report["payload_sha256"] = sha_object(report)
    atomic_write_bytes(output_path, encoded_json(report))
    print(json.dumps({"status": "PASS", "tests": len(results), "payload_sha256": report["payload_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        raise SystemExit(f"CORRECTED_UNIVERSE_MUTATIONS_FAIL:{error}") from error
