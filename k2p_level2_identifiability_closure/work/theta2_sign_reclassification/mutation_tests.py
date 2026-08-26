#!/usr/bin/env python3
"""Fail-closed mutations for the theta2 full-map truth certificate."""

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
CERTIFICATE = PROJECT / "work/adversarial_proof_review/theta2_tree_sunlet_full_map_certificate.json"
VERIFIER = HERE / "verify_theta2_full_map_independent.py"
AUTHORITATIVE_OUTPUT = HERE / "theta2_mutation_certificate.json"
FORBIDDEN_FAILURE_MARKERS = (
    "Traceback (most recent call last)",
    "ModuleNotFoundError",
    "ImportError",
    "No module named",
)
MUTATION_DIAGNOSTICS = {
    "omitted_truth_row": "THETA2_FULL_MAP_REPLAY_FAIL:claimed row count",
    "reassigned_truth_row": "THETA2_FULL_MAP_REPLAY_FAIL:truth row hash:0",
    "missing_target_presentation": (
        "THETA2_FULL_MAP_REPLAY_FAIL:missing target sign presentation:"
        "587840:(4898, (1, 2, 3))"
    ),
    "wrong_target_orientation": (
        "THETA2_FULL_MAP_REPLAY_FAIL:target polynomial hash:"
        "(4898, (1, 2, 3), 1)"
    ),
    "mutated_Bernstein_coefficient": (
        "THETA2_FULL_MAP_REPLAY_FAIL:target Bernstein replay:"
        "04f8d1c7ac725665341a9b238ef9c326127051fa3db5db40533a7e45368712d2"
    ),
    "mutated_Bernstein_tensor_entry_count": (
        "THETA2_FULL_MAP_REPLAY_FAIL:target Bernstein replay:"
        "04f8d1c7ac725665341a9b238ef9c326127051fa3db5db40533a7e45368712d2"
    ),
    "reassigned_relation_multiplicity": (
        "THETA2_FULL_MAP_REPLAY_FAIL:relation class multiplicities"
    ),
    "wrong_source_zero_count": "THETA2_FULL_MAP_REPLAY_FAIL:source-zero count",
    "wrong_graph_relation_count": "THETA2_FULL_MAP_REPLAY_FAIL:relation count",
    "python_optimized_mode": (
        "THETA2_FULL_MAP_REPLAY_FAIL:"
        "THETA2_FULL_MAP_REPLAY_OPTIMIZED_MODE_FORBIDDEN"
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
        require(not lexical.is_symlink(), "THETA2_MUTATION_OUTPUT_POLICY_FAIL:output symlink forbidden")
        require(
            not any(os.path.samefile(lexical, source) for source in sources),
            "THETA2_MUTATION_OUTPUT_POLICY_FAIL:output hardlink collides with source",
        )
    if allow_authoritative_output:
        require(
            normalized == authoritative and not lexical.is_symlink(),
            "THETA2_MUTATION_OUTPUT_POLICY_FAIL:authoritative override licenses only theta2_mutation_certificate.json",
        )
        ancestor = lexical.parent
        while True:
            require(not ancestor.is_symlink(), "THETA2_MUTATION_OUTPUT_POLICY_FAIL:authoritative ancestor symlink forbidden")
            if ancestor.resolve() == PROJECT.resolve():
                break
            require(ancestor != ancestor.parent, "THETA2_MUTATION_OUTPUT_POLICY_FAIL:authoritative project ancestor missing")
            ancestor = ancestor.parent
        return normalized
    try:
        normalized.relative_to(PROJECT.resolve())
    except ValueError:
        return normalized
    raise MutationFailure("THETA2_MUTATION_OUTPUT_POLICY_FAIL:routine mutation output must be outside project source tree")


def rehash(document):
    document["ordered_truth_row_hash_root"] = sha(document["ordered_truth_row_hashes"])
    document.pop("payload_sha256", None)
    document["payload_sha256"] = sha(document)


def mutate_omitted_row(document):
    document["ordered_truth_row_hashes"].pop(0)
    document["claimed_rows"] -= 1
    document["full_map_source_zero_rows"] -= 1
    document["full_map_strict_target_sign_rows"] -= 1


def mutate_reassigned_row(document):
    document["ordered_truth_row_hashes"][0] = document["ordered_truth_row_hashes"][1]


def first_sign(document):
    key = sorted(document["sign_certificates"])[0]
    return key, document["sign_certificates"][key]


def mutate_missing_target_presentation(document):
    _, record = first_sign(document)
    record["target_presentations"].pop(0)


def mutate_wrong_target_orientation(document):
    _, record = first_sign(document)
    presentation = record["target_presentations"][0]
    presentation[2] = next(label for label in presentation[1] if label != presentation[2])


def mutate_bernstein_coefficient(document):
    _, record = first_sign(document)
    sign = record["sign"]
    sign["minimum_coefficient"] = "-123456789"
    sign.pop("certificate_sha256", None)
    sign["certificate_sha256"] = sha(sign)


def mutate_bernstein_tensor_count(document):
    _, record = first_sign(document)
    sign = record["sign"]
    sign["negative_coefficients"] += 1
    sign["zero_coefficients"] -= 1
    sign.pop("certificate_sha256", None)
    sign["certificate_sha256"] = sha(sign)


def mutate_relation_multiplicity(document):
    key = sorted(document["canonical_relation_class_multiplicities"])[0]
    document["canonical_relation_class_multiplicities"][key] += 1


def mutate_source_zero_count(document):
    document["full_map_source_zero_rows"] -= 1


def mutate_graph_relation_count(document):
    document["exact_full_graph_relation_census"] = {"none": 2527, "isomorphic": 1}
    document["false_iso_or_triangle_conflicts"] = 1


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
    environment["PYTHONHASHSEED"] = "29"
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
        if line.strip().startswith("THETA2_FULL_MAP_REPLAY_FAIL:")
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
    with tempfile.TemporaryDirectory(prefix="k2p-theta2-full-map-baseline-") as temporary:
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
            report.get("schema") == "k2p-theta2-full-map-independent-replay-v1"
            and report.get("status") == "PASS"
            and report.get("raw_rows_replayed") == 2_528
            and report.get("source_zero_rows") == 2_528
            and report.get("strict_target_negative_rows") == 2_528
            and report.get("exact_graph_relation_none_rows") == 2_528
            and report.get("sign_classes_replayed") == 85
            and report.get("unresolved") == 0,
            "clean baseline semantics",
        )
        return {
            "return_code": 0,
            "status": "PASS",
            "report_schema": report["schema"],
            "report_status": report["status"],
            "raw_rows_replayed": 2_528,
            "source_zero_rows": 2_528,
            "strict_target_negative_rows": 2_528,
            "exact_graph_relation_none_rows": 2_528,
            "sign_classes_replayed": 85,
            "unresolved": 0,
            "success_artifact_present": True,
            "timeout": False,
            "signal": False,
        }


def run_negative_controls():
    name = "omitted_truth_row"
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
        "traceback_not_qualified": {
            **valid,
            "output": "Traceback (most recent call last)\n" + expected,
        },
        "import_error_not_qualified": {
            **valid,
            "output": "ModuleNotFoundError: No module named x\n" + expected,
        },
        "timeout_not_qualified": {**valid, "returncode": None, "timeout": True},
        "signal_not_qualified": {**valid, "returncode": -9, "signal": True},
        "non_one_exit_not_qualified": {**valid, "returncode": 2},
        "success_artifact_not_qualified": {
            **valid,
            "success_artifact_present": True,
        },
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
    with tempfile.TemporaryDirectory(prefix="k2p-theta2-driver-optimized-") as temporary:
        output = Path(temporary) / "stale-pass.json"
        output.write_text('{"status":"PASS"}\n')
        completed = subprocess.run(
            [
                sys.executable,
                "-O",
                str(Path(__file__).resolve()),
                "--output",
                str(output),
            ],
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        diagnostic = (completed.stdout + completed.stderr).strip()
        require(completed.returncode == 1, "optimized driver exit")
        require(
            diagnostic
            == "THETA2_MUTATION_DRIVER_FAIL:THETA2_MUTATION_DRIVER_OPTIMIZED_MODE_FORBIDDEN",
            f"optimized driver diagnostic:{diagnostic}",
        )
        require(not output.exists(), "optimized driver stale PASS artifact")
    return {
        "return_code": 1,
        "expected_diagnostic": (
            "THETA2_MUTATION_DRIVER_FAIL:"
            "THETA2_MUTATION_DRIVER_OPTIMIZED_MODE_FORBIDDEN"
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
        raise MutationFailure("THETA2_MUTATION_DRIVER_OPTIMIZED_MODE_FORBIDDEN")

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
        ("omitted_truth_row", mutate_omitted_row),
        ("reassigned_truth_row", mutate_reassigned_row),
        ("missing_target_presentation", mutate_missing_target_presentation),
        ("wrong_target_orientation", mutate_wrong_target_orientation),
        ("mutated_Bernstein_coefficient", mutate_bernstein_coefficient),
        ("mutated_Bernstein_tensor_entry_count", mutate_bernstein_tensor_count),
        ("reassigned_relation_multiplicity", mutate_relation_multiplicity),
        ("wrong_source_zero_count", mutate_source_zero_count),
        ("wrong_graph_relation_count", mutate_graph_relation_count),
    ]
    results = []
    with tempfile.TemporaryDirectory(prefix="k2p-theta2-full-map-mutations-") as temporary:
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
        "schema": "k2p-theta2-full-map-mutations-v2",
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
        report["mutation_count"] == report["mutations_rejected"] == 10,
        "mutation census",
    )
    report["payload_sha256"] = sha(report)
    atomic_write_bytes(output, encoded(report))
    print(
        json.dumps(
            {
                "status": "PASS",
                "mutations": 10,
                "semantic_certificate_attacks": 9,
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
        raise SystemExit(f"THETA2_MUTATION_DRIVER_FAIL:{error}") from error
