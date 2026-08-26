#!/usr/bin/env python3
"""Fail-closed mutations for the corrected raw-four terminal overlay."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
CERTIFICATE = HERE / "raw4_corrected_terminal_ledger.json"
VERIFIER = HERE / "verify_raw4_corrected_terminal_ledger.py"
AUTHORITATIVE_OUTPUT = HERE / "raw4_mutation_certificate.json"
FORBIDDEN_FAILURE_MARKERS = (
    "Traceback (most recent call last)",
    "ModuleNotFoundError",
    "ImportError",
    "No module named",
)
MUTATION_DIAGNOSTICS = {
    "omitted_raw_record": "RAW4_CORRECTED_REPLAY_FAIL:coverage census",
    "reassigned_raw_record": "RAW4_CORRECTED_REPLAY_FAIL:coverage raw-id uniqueness",
    "wrong_port_transport": "RAW4_CORRECTED_REPLAY_FAIL:raw permutation:0",
    "reassigned_polynomial_certificate": "RAW4_CORRECTED_REPLAY_FAIL:source pullback:0",
    "mutated_Bernstein_coefficient": (
        "RAW4_CORRECTED_REPLAY_FAIL:Bernstein certificate mismatch:"
        "34a10e594f28cf98f8badff8b10241ab09fb5dfc203c7a6c0b5f940cfc419aa6"
    ),
    "mutated_Bernstein_tensor_entry_count": (
        "RAW4_CORRECTED_REPLAY_FAIL:Bernstein certificate mismatch:"
        "34a10e594f28cf98f8badff8b10241ab09fb5dfc203c7a6c0b5f940cfc419aa6"
    ),
    "reversed_sign_conclusion": (
        "RAW4_CORRECTED_REPLAY_FAIL:Bernstein certificate mismatch:"
        "34a10e594f28cf98f8badff8b10241ab09fb5dfc203c7a6c0b5f940cfc419aa6"
    ),
    "reassigned_descriptor_class": "RAW4_CORRECTED_REPLAY_FAIL:descriptor class:0",
    "python_optimized_mode": (
        "RAW4_CORRECTED_REPLAY_FAIL:"
        "RAW4_CORRECTED_REPLAY_OPTIMIZED_MODE_FORBIDDEN"
    ),
}


class MutationFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise MutationFailure(message)


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def atomic_write_bytes(path, payload):
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
    finally:
        if temporary.exists():
            temporary.unlink()


def validate_output_path(output, allow_authoritative_output):
    lexical = Path(os.path.abspath(os.fspath(output)))
    normalized = lexical.parent.resolve() / lexical.name
    authoritative = (
        AUTHORITATIVE_OUTPUT.parent.resolve() / AUTHORITATIVE_OUTPUT.name
    )
    sources = (CERTIFICATE.resolve(), VERIFIER.resolve(), Path(__file__).resolve())
    if lexical.exists():
        require(not lexical.is_symlink(), "RAW4_MUTATION_OUTPUT_POLICY_FAIL:output symlink forbidden")
        require(
            not any(os.path.samefile(lexical, source) for source in sources),
            "RAW4_MUTATION_OUTPUT_POLICY_FAIL:output hardlink collides with source",
        )
    if allow_authoritative_output:
        require(
            normalized == authoritative and not lexical.is_symlink(),
            "RAW4_MUTATION_OUTPUT_POLICY_FAIL:authoritative override licenses only raw4_mutation_certificate.json",
        )
        ancestor = lexical.parent
        while True:
            require(not ancestor.is_symlink(), "RAW4_MUTATION_OUTPUT_POLICY_FAIL:authoritative ancestor symlink forbidden")
            if ancestor.resolve() == PROJECT.resolve():
                break
            require(ancestor != ancestor.parent, "RAW4_MUTATION_OUTPUT_POLICY_FAIL:authoritative project ancestor missing")
            ancestor = ancestor.parent
        return normalized
    try:
        normalized.relative_to(PROJECT.resolve())
    except ValueError:
        return normalized
    raise MutationFailure("RAW4_MUTATION_OUTPUT_POLICY_FAIL:routine mutation output must be outside project source tree")


def rehash(document):
    document["coverage_row_hashes"] = [sha(row) for row in document["coverage"]]
    document["coverage_hash_root"] = sha(document["coverage_row_hashes"])
    document.pop("payload_sha256", None)
    document["payload_sha256"] = sha(document)
    return document


def mutate_omitted_raw(document):
    removed = document["coverage"].pop(0)
    document["corrected_rows"] -= 1
    document["raw_id_unique"] -= 1
    document["corrected_category_census"]["exact_exclusion"] -= 1
    document["corrected_reason_census"]["full_map_Ti_strict_sign"] -= 1
    class_id = removed["descriptor_pair_class_id"]
    document["descriptor_pair_classes"][class_id]["raw_multiplicity"] -= 1
    key = f"{removed['source_pullback_sha256']}:{removed['target_pullback_sha256']}"
    document["canonical_relation_class_multiplicities"][key] -= 1


def mutate_reassigned_raw(document):
    document["coverage"][0]["raw_id"] = document["coverage"][1]["raw_id"]


def mutate_wrong_transport(document):
    row = document["coverage"][0]
    row["port_permutation"][0], row["port_permutation"][1] = (
        row["port_permutation"][1],
        row["port_permutation"][0],
    )


def mutate_reassigned_polynomial(document):
    row = document["coverage"][0]
    alternatives = sorted(
        set(document["sign_certificates"]) - {row["source_pullback_sha256"]}
    )
    old_key = f"{row['source_pullback_sha256']}:{row['target_pullback_sha256']}"
    new_hash = alternatives[0]
    new_key = f"{new_hash}:{row['target_pullback_sha256']}"
    document["canonical_relation_class_multiplicities"][old_key] -= 1
    document["canonical_relation_class_multiplicities"][new_key] = (
        document["canonical_relation_class_multiplicities"].get(new_key, 0) + 1
    )
    row["source_pullback_sha256"] = new_hash
    row["source_pullback_term_count"] = document["sign_certificates"][new_hash][
        "source_pullback_term_count"
    ]


def mutate_bernstein_coefficient(document):
    key = sorted(document["sign_certificates"])[0]
    sign = document["sign_certificates"][key]["sign_certificate"]
    sign["minimum_coefficient"] = "-999999"
    sign.pop("certificate_sha256", None)
    sign["certificate_sha256"] = sha(sign)


def mutate_bernstein_tensor_count(document):
    key = sorted(document["sign_certificates"])[0]
    sign = document["sign_certificates"][key]["sign_certificate"]
    sign["negative_coefficients"] += 1
    sign["zero_coefficients"] -= 1
    sign.pop("certificate_sha256", None)
    sign["certificate_sha256"] = sha(sign)


def mutate_reversed_sign(document):
    key = sorted(document["sign_certificates"])[0]
    sign = document["sign_certificates"][key]["sign_certificate"]
    sign["conclusion"] = "strictly_positive"
    sign.pop("certificate_sha256", None)
    sign["certificate_sha256"] = sha(sign)


def mutate_descriptor_reassignment(document):
    document["coverage"][0]["descriptor_pair_class_id"] = 1


def decoded(value):
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def invoke_verifier(certificate_path, report_path, timeout, optimized=False):
    stale_report_removed = report_path.exists()
    report_path.unlink(missing_ok=True)
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(
        [
            str(VERIFIER),
            "--certificate",
            str(certificate_path),
            "--report",
            str(report_path),
        ]
    )
    environment = dict(os.environ)
    environment["PYTHONHASHSEED"] = "17"
    try:
        completed = subprocess.run(
            command,
            text=True,
            capture_output=True,
            env=environment,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        return {
            "returncode": None,
            "output": (decoded(error.stdout) + decoded(error.stderr)).strip(),
            "success_artifact_present": report_path.exists(),
            "timeout": True,
            "signal": False,
            "stale_report_removed": stale_report_removed,
        }
    return {
        "returncode": completed.returncode,
        "output": (completed.stdout + completed.stderr).strip(),
        "success_artifact_present": report_path.exists(),
        "timeout": False,
        "signal": completed.returncode < 0,
        "stale_report_removed": stale_report_removed,
    }


def qualify_mutation_failure(name, result):
    expected = MUTATION_DIAGNOSTICS[name]
    output = result.get("output", "")
    semantic_lines = [
        line.strip()
        for line in output.splitlines()
        if line.strip().startswith("RAW4_CORRECTED_REPLAY_FAIL:")
    ]
    require(result.get("timeout") is False, f"mutation timeout:{name}")
    require(result.get("signal") is False, f"mutation signal:{name}")
    require(result.get("returncode") == 1, f"mutation exit:{name}")
    require(
        not any(marker in output for marker in FORBIDDEN_FAILURE_MARKERS),
        f"mutation unrelated crash:{name}",
    )
    require(
        result.get("success_artifact_present") is False,
        f"mutation success artifact:{name}",
    )
    require(semantic_lines == [expected], f"mutation diagnostic:{name}:{semantic_lines}")
    return {
        "mutation": name,
        "rejected": True,
        "return_code": 1,
        "expected_diagnostic": expected,
        "observed_diagnostic": expected,
        "success_artifact_absent": True,
        "timeout": False,
        "signal": False,
        "unrelated_crash": False,
        "production_verifier_invoked": True,
    }


def run_clean_baseline(timeout):
    with tempfile.TemporaryDirectory(prefix="k2p-raw4-full-map-baseline-") as temporary:
        report_path = Path(temporary) / "report.json"
        result = invoke_verifier(CERTIFICATE, report_path, timeout)
        require(result["timeout"] is False, "clean baseline timeout")
        require(result["signal"] is False, "clean baseline signal")
        require(result["returncode"] == 0, f"clean baseline exit:{result}")
        require(
            not any(marker in result["output"] for marker in FORBIDDEN_FAILURE_MARKERS),
            "clean baseline unrelated crash",
        )
        require(result["success_artifact_present"] is True, "clean baseline report absent")
        report = json.loads(report_path.read_text())
        unhashed = dict(report)
        payload = unhashed.pop("payload_sha256")
        require(payload == sha(unhashed), "clean baseline report payload")
        require(
            report.get("schema") == "k2p-raw4-corrected-independent-replay-v1"
            and report.get("status") == "PASS"
            and report.get("raw_rows_replayed") == 16_974
            and report.get("strict_source_negative_rows") == 16_974
            and report.get("target_zero_rows") == 16_974
            and report.get("sign_classes_replayed") == 8
            and report.get("unresolved") == 0
            and report.get("false_graph_terminal_conflicts") == 0,
            "clean baseline semantics",
        )
        return {
            "return_code": 0,
            "status": "PASS",
            "report_schema": report["schema"],
            "report_status": report["status"],
            "raw_rows_replayed": 16_974,
            "strict_source_negative_rows": 16_974,
            "target_zero_rows": 16_974,
            "sign_classes_replayed": 8,
            "unresolved": 0,
            "false_graph_terminal_conflicts": 0,
            "success_artifact_present": True,
            "timeout": False,
            "signal": False,
        }


def run_negative_controls():
    name = "omitted_raw_record"
    expected = MUTATION_DIAGNOSTICS[name]
    valid = {
        "returncode": 1,
        "output": expected,
        "success_artifact_present": False,
        "timeout": False,
        "signal": False,
        "stale_report_removed": False,
    }
    variants = {
        "wrong_diagnostic_not_qualified": {**valid, "output": expected + ":wrong"},
        "traceback_not_qualified": {**valid, "output": "Traceback (most recent call last)\n" + expected},
        "import_error_not_qualified": {**valid, "output": "ModuleNotFoundError: No module named x\n" + expected},
        "timeout_not_qualified": {**valid, "returncode": None, "timeout": True},
        "signal_not_qualified": {**valid, "returncode": -9, "signal": True},
        "non_one_exit_not_qualified": {**valid, "returncode": 2},
        "success_artifact_not_qualified": {**valid, "success_artifact_present": True},
        "missing_diagnostic_not_qualified": {**valid, "output": ""},
    }
    outcome = {}
    for control, result in variants.items():
        try:
            qualify_mutation_failure(name, result)
        except MutationFailure:
            outcome[control] = True
        else:
            raise MutationFailure(f"negative control qualified:{control}")
    return outcome


def optimized_driver_stale_output_control(timeout):
    with tempfile.TemporaryDirectory(prefix="k2p-raw4-driver-optimized-") as temporary:
        output = Path(temporary) / "stale-pass.json"
        output.write_text('{"status":"PASS"}\n')
        completed = subprocess.run(
            [sys.executable, "-O", str(Path(__file__).resolve()), "--output", str(output)],
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        diagnostic = (completed.stdout + completed.stderr).strip()
        require(completed.returncode == 1, "optimized driver exit")
        require(
            diagnostic == "RAW4_MUTATION_DRIVER_FAIL:RAW4_MUTATION_DRIVER_OPTIMIZED_MODE_FORBIDDEN",
            f"optimized driver diagnostic:{diagnostic}",
        )
        require(not output.exists(), "optimized driver stale PASS artifact")
    return {
        "return_code": 1,
        "expected_diagnostic": (
            "RAW4_MUTATION_DRIVER_FAIL:RAW4_MUTATION_DRIVER_OPTIMIZED_MODE_FORBIDDEN"
        ),
        "observed_diagnostic_exact": True,
        "preexisting_success_artifact_removed": True,
        "success_artifact_absent": True,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow-authoritative-output", action="store_true")
    parser.add_argument("--timeout-seconds", type=float, default=1200.0)
    args = parser.parse_args()
    require(args.timeout_seconds > 0, "invalid timeout")
    output = validate_output_path(args.output, args.allow_authoritative_output)
    output.unlink(missing_ok=True)
    if not __debug__:
        raise MutationFailure("RAW4_MUTATION_DRIVER_OPTIMIZED_MODE_FORBIDDEN")

    sources_before = {
        "certificate": sha_file(CERTIFICATE),
        "verifier": sha_file(VERIFIER),
        "runner": sha_file(Path(__file__).resolve()),
    }
    original = json.loads(CERTIFICATE.read_text())
    claimed_payload = original["payload_sha256"]
    unhashed = dict(original)
    unhashed.pop("payload_sha256")
    require(claimed_payload == sha(unhashed), "source certificate payload")
    clean_baseline = run_clean_baseline(args.timeout_seconds)
    mutations = [
        ("omitted_raw_record", mutate_omitted_raw),
        ("reassigned_raw_record", mutate_reassigned_raw),
        ("wrong_port_transport", mutate_wrong_transport),
        ("reassigned_polynomial_certificate", mutate_reassigned_polynomial),
        ("mutated_Bernstein_coefficient", mutate_bernstein_coefficient),
        ("mutated_Bernstein_tensor_entry_count", mutate_bernstein_tensor_count),
        ("reversed_sign_conclusion", mutate_reversed_sign),
        ("reassigned_descriptor_class", mutate_descriptor_reassignment),
    ]
    results = []
    with tempfile.TemporaryDirectory(prefix="k2p-raw4-full-map-mutations-") as temporary:
        temporary = Path(temporary)
        for name, mutation in mutations:
            candidate = copy.deepcopy(original)
            mutation(candidate)
            rehash(candidate)
            candidate_path = temporary / f"{name}.json"
            candidate_path.write_bytes(encoded(candidate))
            report_path = temporary / f"{name}.report.json"
            result = invoke_verifier(
                candidate_path, report_path, args.timeout_seconds
            )
            qualified = qualify_mutation_failure(name, result)
            qualified["test_type"] = "complete_resealed_certificate_attack"
            qualified["certificate_resealed"] = True
            results.append(qualified)
            print(json.dumps(qualified, sort_keys=True), flush=True)

        optimized_report = temporary / "optimized.report.json"
        optimized_report.write_text('{"status":"PASS"}\n')
        result = invoke_verifier(
            CERTIFICATE,
            optimized_report,
            args.timeout_seconds,
            optimized=True,
        )
        require(result["stale_report_removed"] is True, "optimized stale report not removed")
        qualified = qualify_mutation_failure("python_optimized_mode", result)
        qualified["test_type"] = "production_verifier_optimized_mode_attack"
        qualified["preexisting_success_artifact_removed"] = True
        results.append(qualified)
        print(json.dumps(qualified, sort_keys=True), flush=True)

    negative_controls = run_negative_controls()
    optimized_driver_control = optimized_driver_stale_output_control(
        min(args.timeout_seconds, 60.0)
    )
    sources_after = {
        "certificate": sha_file(CERTIFICATE),
        "verifier": sha_file(VERIFIER),
        "runner": sha_file(Path(__file__).resolve()),
    }
    require(sources_after == sources_before, "source tree drift")
    report = {
        "schema": "k2p-raw4-corrected-mutations-v2",
        "status": "PASS",
        "source_certificate_sha256": sources_before["certificate"],
        "source_certificate_payload_sha256": claimed_payload,
        "production_verifier_sha256": sources_before["verifier"],
        "mutation_runner_sha256": sources_before["runner"],
        "clean_baseline": clean_baseline,
        "diagnostic_contract": MUTATION_DIAGNOSTICS,
        "mutation_count": len(results),
        "semantic_certificate_attack_count": len(mutations),
        "mutations_rejected": len(results),
        "survived": 0,
        "results": results,
        "qualification_negative_controls": negative_controls,
        "optimized_driver_stale_output_control": optimized_driver_control,
        "execution_contract": {
            "clean_baseline_required": True,
            "exact_per_case_diagnostics_required": True,
            "return_code_one_required": True,
            "traceback_and_import_failures_rejected": True,
            "timeouts_signals_and_non_one_exits_rejected": True,
            "success_artifacts_on_failure_rejected": True,
            "routine_output_caller_owned_external": True,
            "authoritative_output_requires_explicit_exact_override": True,
            "optimized_mode_removes_preexisting_output": True,
            "absolute_paths_recorded": False,
            "runtime_fields_recorded": False,
        },
        "source_tree_drift": 0,
    }
    require(
        report["mutation_count"] == report["mutations_rejected"] == 9,
        "mutation census",
    )
    report["payload_sha256"] = sha(report)
    atomic_write_bytes(output, encoded(report))
    print(
        json.dumps(
            {
                "status": "PASS",
                "mutations": 9,
                "semantic_certificate_attacks": 8,
                "negative_controls": len(negative_controls),
                "survived": 0,
                "payload_sha256": report["payload_sha256"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    try:
        main()
    except (
        MutationFailure,
        AssertionError,
        KeyError,
        IndexError,
        OSError,
        ValueError,
        json.JSONDecodeError,
        subprocess.TimeoutExpired,
    ) as error:
        raise SystemExit(f"RAW4_MUTATION_DRIVER_FAIL:{error}") from error
