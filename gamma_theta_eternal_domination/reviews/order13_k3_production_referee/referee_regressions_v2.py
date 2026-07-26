#!/usr/bin/env python3
"""Independent synthetic follow-up for the repaired production workflow.

This module reuses only fixture helpers from the preserved v1 referee script.
It never calls that script's main routine and never changes any v1 artifact.
Executable-looking fixture files are plain text and are never executed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import tempfile
from dataclasses import asdict
from pathlib import Path
from typing import Mapping
from unittest.mock import patch


REVIEW = Path(__file__).resolve().parent
CAMPAIGN = REVIEW.parents[1]
sys.path.insert(0, str(REVIEW))
sys.path.insert(0, str(CAMPAIGN / "src"))

import referee_regressions as base  # noqa: E402

from search.order13_k3 import production  # noqa: E402
from search.order13_k3.generate import canonical_json_bytes  # noqa: E402
from synthesis_k3.cegar import ChildResult, _command_sha256  # noqa: E402


FINAL_FROZEN = {
    "src/search/order13_k3/production.py": (
        "0d4ab4e0bcd8d7175a2ba5339bd861c1ffac5da011d119a51565f0f8dc9e789b"
    ),
    "src/search/order13_k3/normalize_bdrat.py": (
        "a09f67d39932b6c3bb19b31a0792e4f47f515820c642e9418d3e374f555de18c"
    ),
    "src/search/order13_k3/PRODUCTION_PROTOCOL.md": (
        "b1e1cbd45a6388a2437be4ba490cd8b5163b12ddec8e36020380c09b99294e62"
    ),
    "tests/test_order13_k3_production.py": (
        "5ac5f1a071d02db17c14d4e2a0f7715422c28ee4d9fa3099ee0531b00a4f1a8b"
    ),
}
PRESERVED_V1 = {
    "REVIEW.md": (
        "81773a5295046a7e37eaf16897edfe710aff7f1ae873402cda64da9d5e32131f"
    ),
    "evidence.json": (
        "3d849ca9493dba7786a899ce9a0cf7c35101b7f342d531103cbc65c510db29fe"
    ),
    "referee_regressions.py": (
        "5681a4672abf882b408de287ef781b72063915d31e6d068cef143face119e1f8"
    ),
    "run_readonly_upstream_tests.py": (
        "713ec705aa77aa7f316ef7357473d7466fd00fdd82f84aff799fbc97f882b022"
    ),
    "RESEARCH_LOG.md": (
        "6c02761363fe8420b300f4f0c8764d478c93df9c85398684be6d22bf8b21647b"
    ),
}


def read_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path.name} is not a JSON object")
    return value


def write_json(path: Path, value: object) -> None:
    path.write_bytes(canonical_json_bytes(value))


def verify_bound_bytes() -> tuple[dict[str, str], dict[str, str]]:
    frozen = {
        relative: base.sha256(CAMPAIGN / relative)
        for relative in FINAL_FROZEN
    }
    preserved = {
        name: base.sha256(REVIEW / name)
        for name in PRESERVED_V1
    }
    if frozen != FINAL_FROZEN:
        raise AssertionError("final frozen implementation bytes changed")
    if preserved != PRESERVED_V1:
        raise AssertionError("a preserved v1 referee artifact changed")
    return frozen, preserved


def refresh_terminal(
    run_directory: Path,
    *,
    sync_certificate: bool,
) -> None:
    attempt = run_directory / "attempts/attempt-000001"
    config_path = attempt / "attempt-config.json"
    outcome_path = attempt / "outcome.json"
    outcome = read_json(outcome_path)
    if sync_certificate:
        certificate = read_json(attempt / "certificate.json")
        outcome["details"] = {"certificate": certificate}
    outcome["artifacts"] = production._attempt_artifacts(attempt)
    write_json(outcome_path, outcome)

    first_path = run_directory / "checkpoints/checkpoint-000001.json"
    first = read_json(first_path)
    first["attempt"] = production._binding(
        config_path, "v2 refreshed attempt config"
    )
    write_json(first_path, first)

    second_path = run_directory / "checkpoints/checkpoint-000002.json"
    second = read_json(second_path)
    second["previous_checkpoint_sha256"] = base.sha256(first_path)
    second["attempt"] = production._binding(
        config_path, "v2 refreshed attempt config"
    )
    second["outcome"] = production._binding(
        outcome_path, "v2 refreshed outcome"
    )
    write_json(second_path, second)


def update_phase_binding(
    attempt: Path,
    phase: str,
    section: str,
    role: str,
    path: Path,
) -> None:
    record_path = attempt / f"child-{phase}.json"
    record = read_json(record_path)
    mapping = record.get(section)
    if not isinstance(mapping, dict) or role not in mapping:
        raise AssertionError(f"{phase} {section} lacks {role}")
    mapping[role] = production._binding(
        path, f"v2 updated {phase} {section} {role}"
    )
    write_json(record_path, record)


def expect_rejection(
    action: object,
    fragment: str,
) -> dict[str, object]:
    return base.expect_rejection(action, fragment)


def new_success(
    foundation: base.Foundation,
    name: str,
) -> tuple[Path, list[str]]:
    run_directory = foundation.initialize(name)
    _, phases = base.run_success(run_directory)
    report = base.audit_without_children(run_directory)
    if report["status"] != production.FINAL_SUCCESS:
        raise AssertionError("v2 positive success did not audit")
    return run_directory, phases


def case_f1_attempt_formula(foundation: base.Foundation) -> dict[str, object]:
    run_directory, _ = new_success(foundation, "v2-f1-instance")
    attempt = run_directory / "attempts/attempt-000001"
    instance = attempt / production.INSTANCE_NAME
    instance.write_bytes(b"p cnf 1 2\n1 0\n-1 0\n")

    config_path = attempt / "attempt-config.json"
    config = read_json(config_path)
    config["instance"] = production._binding(
        instance, "v2 coherently substituted instance"
    )
    write_json(config_path, config)

    certificate_path = attempt / "certificate.json"
    certificate = read_json(certificate_path)
    certificate["instance"] = production._binding(
        instance, "v2 substituted certificate instance"
    )
    write_json(certificate_path, certificate)

    for phase in (
        "solver",
        "raw_forward",
        "normalized_forward",
        "lrat_conversion",
        "lrat_check",
    ):
        for section in (
            "readonly_inputs_before",
            "readonly_inputs_after",
        ):
            update_phase_binding(
                attempt, phase, section, "instance", instance
            )
    refresh_terminal(run_directory, sync_certificate=True)
    rejection = expect_rejection(
        lambda: base.audit_without_children(run_directory),
        "attempt configuration differs from frozen inputs",
    )
    return {
        "exact_attack_rejected": rejection["rejected"],
        "all_phase_instance_bindings_coherently_refreshed": True,
        "attempt_instance_equals_frozen_run_instance": False,
        "attempt_instance_sha256": base.sha256(instance),
        "frozen_run_instance_sha256": base.sha256(
            run_directory / production.INSTANCE_NAME
        ),
        "rejection": rejection,
        "real_solver_or_checker_executions": 0,
    }


def mutate_lrat_and_certificate(run_directory: Path) -> Path:
    attempt = run_directory / "attempts/attempt-000001"
    lrat = attempt / "proof.converted.lrat"
    lrat.write_bytes(b"not an LRAT proof\n")
    certificate_path = attempt / "certificate.json"
    certificate = read_json(certificate_path)
    certificate["converted_lrat"] = production._binding(
        lrat, "v2 substituted LRAT"
    )
    write_json(certificate_path, certificate)
    return lrat


def case_f2_phase_crosslinks(
    foundation: base.Foundation,
) -> dict[str, object]:
    exact_run, _ = new_success(foundation, "v2-f2-exact")
    exact_lrat = mutate_lrat_and_certificate(exact_run)
    refresh_terminal(exact_run, sync_certificate=True)
    exact = expect_rejection(
        lambda: base.audit_without_children(exact_run),
        "lrat_conversion phase input/output bindings differ",
    )

    downstream_run, _ = new_success(foundation, "v2-f2-downstream")
    downstream_attempt = downstream_run / "attempts/attempt-000001"
    downstream_lrat = mutate_lrat_and_certificate(downstream_run)
    update_phase_binding(
        downstream_attempt,
        "lrat_conversion",
        "produced_outputs",
        "converted_lrat",
        downstream_lrat,
    )
    refresh_terminal(downstream_run, sync_certificate=True)
    downstream = expect_rejection(
        lambda: base.audit_without_children(downstream_run),
        "lrat_check phase input/output bindings differ",
    )

    before_run, _ = new_success(foundation, "v2-f2-before")
    before_attempt = before_run / "attempts/attempt-000001"
    before_record_path = before_attempt / "child-lrat_check.json"
    before_record = read_json(before_record_path)
    before_record["readonly_inputs_before"]["LRAT"]["sha256"] = "0" * 64
    write_json(before_record_path, before_record)
    refresh_terminal(before_run, sync_certificate=True)
    before = expect_rejection(
        lambda: base.audit_without_children(before_run),
        "lrat_check phase input/output bindings differ",
    )

    after_run, _ = new_success(foundation, "v2-f2-after")
    after_attempt = after_run / "attempts/attempt-000001"
    after_record_path = after_attempt / "child-lrat_check.json"
    after_record = read_json(after_record_path)
    after_record["readonly_inputs_after"]["LRAT"]["sha256"] = "0" * 64
    write_json(after_record_path, after_record)
    refresh_terminal(after_run, sync_certificate=True)
    after = expect_rejection(
        lambda: base.audit_without_children(after_run),
        "lrat_check phase input/output bindings differ",
    )

    return {
        "exact_postcheck_substitution_rejected": exact["rejected"],
        "conversion_output_refresh_still_caught_by_checker_input": downstream[
            "rejected"
        ],
        "forged_readonly_before_rejected": before["rejected"],
        "forged_readonly_after_rejected": after["rejected"],
        "substituted_lrat_sha256": base.sha256(exact_lrat),
        "exact_rejection": exact,
        "downstream_rejection": downstream,
        "before_rejection": before,
        "after_rejection": after,
        "real_solver_or_checker_executions": 0,
    }


def case_output_crosslink_matrix(
    foundation: base.Foundation,
) -> dict[str, object]:
    results: dict[str, dict[str, object]] = {}

    raw_run, _ = new_success(foundation, "v2-crosslink-raw")
    raw_attempt = raw_run / "attempts/attempt-000001"
    raw = raw_attempt / "proof.raw.bdrat"
    raw.write_bytes(b"a\x04\x00a\x00")
    update_phase_binding(
        raw_attempt,
        "solver",
        "produced_outputs",
        "raw_binary_drat",
        raw,
    )
    raw_certificate = read_json(raw_attempt / "certificate.json")
    raw_certificate["raw_binary_drat"] = production._binding(
        raw, "v2 changed raw proof"
    )
    write_json(raw_attempt / "certificate.json", raw_certificate)
    refresh_terminal(raw_run, sync_certificate=True)
    results["solver_raw_to_raw_forward"] = expect_rejection(
        lambda: base.audit_without_children(raw_run),
        "raw_forward phase input/output bindings differ",
    )

    normalized_run, _ = new_success(
        foundation, "v2-crosslink-normalized"
    )
    normalized_attempt = normalized_run / "attempts/attempt-000001"
    normalized = normalized_attempt / "proof.normalized.rup.bdrat"
    normalized.write_bytes(b"a\x04\x00a\x00")
    update_phase_binding(
        normalized_attempt,
        "normalizer",
        "produced_outputs",
        "normalized_binary_rup",
        normalized,
    )
    normalized_certificate = read_json(
        normalized_attempt / "certificate.json"
    )
    normalized_certificate["normalized_binary_rup"] = production._binding(
        normalized, "v2 changed normalized proof"
    )
    write_json(
        normalized_attempt / "certificate.json", normalized_certificate
    )
    refresh_terminal(normalized_run, sync_certificate=True)
    results["normalizer_output_to_forward_check"] = expect_rejection(
        lambda: base.audit_without_children(normalized_run),
        "normalized_forward phase input/output bindings differ",
    )

    result_run, _ = new_success(foundation, "v2-crosslink-result")
    result_attempt = result_run / "attempts/attempt-000001"
    solver_result = result_attempt / "solver.result"
    solver_result.write_bytes(b"s UNKNOWN\n")
    update_phase_binding(
        result_attempt,
        "solver",
        "produced_outputs",
        "solver_result",
        solver_result,
    )
    refresh_terminal(result_run, sync_certificate=True)
    results["solver_result_semantic_replay"] = expect_rejection(
        lambda: base.audit_without_children(result_run),
        "successful attempt solver result is not UNSAT",
    )

    report_run, _ = new_success(foundation, "v2-crosslink-report")
    report_attempt = report_run / "attempts/attempt-000001"
    report_path = report_attempt / "normalization-report.json"
    report = read_json(report_path)
    report["asserted_proof_verified"] = True
    write_json(report_path, report)
    update_phase_binding(
        report_attempt,
        "normalizer",
        "produced_outputs",
        "normalization_report",
        report_path,
    )
    report_certificate = read_json(report_attempt / "certificate.json")
    report_certificate["normalization_report"] = production._binding(
        report_path, "v2 claim-injected normalization report"
    )
    write_json(report_attempt / "certificate.json", report_certificate)
    refresh_terminal(report_run, sync_certificate=True)
    results["normalization_report_exact_shape"] = expect_rejection(
        lambda: base.audit_without_children(report_run),
        "normalization report semantics differ",
    )

    if not all(item["rejected"] is True for item in results.values()):
        raise AssertionError("an output crosslink mutation was accepted")
    return {
        "case_count": len(results),
        "rejected_count": sum(
            1 for result in results.values() if result["rejected"] is True
        ),
        "cases": results,
        "real_solver_or_checker_executions": 0,
    }


def case_f3_exact_claim_shapes(
    foundation: base.Foundation,
) -> dict[str, object]:
    results: dict[str, dict[str, object]] = {}
    for case in ("extra_key", "claim_boundary"):
        run_directory, _ = new_success(foundation, f"v2-f3-{case}")
        attempt = run_directory / "attempts/attempt-000001"
        certificate_path = attempt / "certificate.json"
        certificate = read_json(certificate_path)
        if case == "extra_key":
            certificate["asserted_global_order13_exclusion"] = True
        else:
            certificate["claim_boundary"] = (
                "Fresh replay and complete coverage falsely asserted."
            )
        write_json(certificate_path, certificate)
        refresh_terminal(run_directory, sync_certificate=True)
        results[case] = expect_rejection(
            lambda target=run_directory: base.audit_without_children(target),
            "template certificate bindings differ",
        )

    details_run, _ = new_success(foundation, "v2-f3-details")
    details_attempt = details_run / "attempts/attempt-000001"
    details_outcome_path = details_attempt / "outcome.json"
    details_outcome = read_json(details_outcome_path)
    details_outcome["details"]["asserted_fresh_replay"] = True
    write_json(details_outcome_path, details_outcome)
    refresh_terminal(details_run, sync_certificate=False)
    results["outcome_details"] = expect_rejection(
        lambda: base.audit_without_children(details_run),
        "successful outcome does not bind its certificate",
    )
    if not all(item["rejected"] is True for item in results.values()):
        raise AssertionError("an exact claim-shape mutation was accepted")
    return {
        "case_count": len(results),
        "rejected_count": sum(
            1 for result in results.values() if result["rejected"] is True
        ),
        "cases": results,
        "real_solver_or_checker_executions": 0,
    }


def make_retry_outcome(attempt: Path) -> dict[str, object]:
    return {
        "schema": "gamma-theta-order13-k3-attempt-outcome-v1",
        "schema_version": 1,
        "status": "RETRYABLE_NONCLAIM",
        "claim_status": "NO_SAT_OR_UNSAT_CLAIM",
        "details": {
            "phase_status": "SYNTHETIC_CRASH_WINDOW_NONCLAIM",
            "phase_details": {},
        },
        "artifacts": production._attempt_artifacts(attempt),
        "finished_unix_ns": 2,
    }


class SyntheticPreRunStartedCrash(BaseException):
    """Injected process loss before RUN_STARTED becomes durable."""


def case_pre_run_started_crash_windows(
    foundation: base.Foundation,
) -> dict[str, object]:
    """Exercise every durable prefix between attempt mkdir and RUN_STARTED."""

    results: dict[str, dict[str, object]] = {}
    original_binding = production._binding

    def injected_binding(label_to_crash: str):
        def binding(path: Path, label: str) -> dict[str, object]:
            if label == label_to_crash:
                raise SyntheticPreRunStartedCrash(label)
            return original_binding(path, label)

        return binding

    for window in (
        "after_attempt_mkdir",
        "after_instance_copy_and_fsync",
        "after_attempt_config_durable_write",
        "before_run_started_checkpoint_append",
    ):
        run_directory = foundation.initialize(f"v2-pre-run-started-{window}")
        checkpoint_zero = (
            run_directory / "checkpoints/checkpoint-000000.json"
        )
        checkpoint_zero_sha256 = base.sha256(checkpoint_zero)

        if window == "after_attempt_mkdir":
            injection = patch.object(
                production.shutil,
                "copyfile",
                side_effect=SyntheticPreRunStartedCrash(window),
            )
        elif window == "after_instance_copy_and_fsync":
            injection = patch.object(
                production,
                "_binding",
                side_effect=injected_binding("attempt instance"),
            )
        elif window == "after_attempt_config_durable_write":
            injection = patch.object(
                production,
                "_binding",
                side_effect=injected_binding("attempt config"),
            )
        else:
            injection = patch.object(
                production,
                "_append_checkpoint",
                side_effect=SyntheticPreRunStartedCrash(window),
            )

        crashed = False
        with injection, patch.object(
            production,
            "run_bounded_child",
            side_effect=AssertionError(
                "pre-RUN_STARTED crash fixture attempted a child"
            ),
        ) as child:
            try:
                production.run(
                    run_directory,
                    production_gate=True,
                    recover_interrupted=False,
                )
            except SyntheticPreRunStartedCrash:
                crashed = True
        if not crashed:
            raise AssertionError(f"{window} injection did not interrupt")
        if child.call_count != 0:
            raise AssertionError(f"{window} launched a child")

        attempt = run_directory / "attempts/attempt-000001"
        durable_entries = sorted(path.name for path in attempt.iterdir())
        expected_entries = {
            "after_attempt_mkdir": [],
            "after_instance_copy_and_fsync": [production.INSTANCE_NAME],
            "after_attempt_config_durable_write": [
                "attempt-config.json",
                production.INSTANCE_NAME,
            ],
            "before_run_started_checkpoint_append": [
                "attempt-config.json",
                production.INSTANCE_NAME,
            ],
        }[window]
        if durable_entries != expected_entries:
            raise AssertionError(
                f"{window} durable prefix differs: {durable_entries}"
            )
        checkpoints = sorted(
            path.name
            for path in (run_directory / "checkpoints").iterdir()
        )
        if (
            checkpoints != ["checkpoint-000000.json"]
            or base.sha256(checkpoint_zero) != checkpoint_zero_sha256
            or (attempt / "outcome.json").exists()
        ):
            raise AssertionError(f"{window} unexpectedly changed claim state")

        audit = expect_rejection(
            lambda target=run_directory: base.audit_without_children(target),
            "attempt directory count differs from checkpoint",
        )
        recovery = expect_rejection(
            lambda target=run_directory: production.run(
                target,
                production_gate=True,
                recover_interrupted=True,
            ),
            "attempt directory count differs from checkpoint",
        )
        ordinary_retry = expect_rejection(
            lambda target=run_directory: production.run(
                target,
                production_gate=True,
                recover_interrupted=False,
            ),
            "attempt directory count differs from checkpoint",
        )
        results[window] = {
            "injection_observed": True,
            "durable_attempt_entries": durable_entries,
            "checkpoint_zero_unchanged": True,
            "child_launched": False,
            "outcome_written": False,
            "audit_fails_closed": audit["rejected"],
            "explicit_recovery_fails_closed": recovery["rejected"],
            "ordinary_retry_fails_closed": ordinary_retry["rejected"],
            "explicit_retryable_nonclaim_record_created": False,
            "fresh_attempt_can_start_without_manual_tree_edit": False,
            "audit_rejection": audit,
            "recovery_rejection": recovery,
            "ordinary_retry_rejection": ordinary_retry,
        }

    all_fail_closed = all(
        case["audit_fails_closed"]
        and case["explicit_recovery_fails_closed"]
        and case["ordinary_retry_fails_closed"]
        for case in results.values()
    )
    if not all_fail_closed:
        raise AssertionError("a pre-RUN_STARTED crash window failed open")
    return {
        "window_count": len(results),
        "all_windows_fail_closed_without_claim": all_fail_closed,
        "safe_explicit_retryable_nonclaim_path_exists": False,
        "fresh_retry_without_manual_tree_edit_exists": False,
        "meets_blanket_interruption_resumability_statement": False,
        "protocol_tension": (
            "The protocol says an interrupted attempt can be explicitly "
            "recovered and a later run starts fresh, but also classifies "
            "orphan directories as audit failures. In all four pre-"
            "RUN_STARTED durable prefixes, --recover-interrupted is rejected "
            "before it can append a retryable-nonclaim checkpoint."
        ),
        "cases": results,
        "real_solver_or_checker_executions": 0,
    }


def case_f4_quarantine(foundation: base.Foundation) -> dict[str, object]:
    retry_run = foundation.initialize("v2-f4-retry-outcome")
    _, _, retry_attempt, _, _, _ = base.create_running_attempt(retry_run)
    write_json(retry_attempt / "outcome.json", make_retry_outcome(retry_attempt))
    ordinary = production.run(
        retry_run,
        production_gate=True,
        recover_interrupted=True,
    )
    ordinary_checkpoint = read_json(
        retry_run / "checkpoints/checkpoint-000002.json"
    )
    ordinary_audit = base.audit_without_children(retry_run)

    success_run, _ = new_success(foundation, "v2-f4-success-outcome")
    success_checkpoint = (
        success_run / "checkpoints/checkpoint-000002.json"
    )
    success_checkpoint.unlink()
    quarantined_success = production.run(
        success_run,
        production_gate=True,
        recover_interrupted=True,
    )
    success_quarantine_checkpoint = read_json(
        success_run / "checkpoints/checkpoint-000002.json"
    )
    success_audit = base.audit_without_children(success_run)
    retry_after_quarantine, child_calls = base.run_timeout(success_run)

    partial_run = foundation.initialize("v2-f4-partial")
    _, _, partial_attempt, _, _, _ = base.create_running_attempt(partial_run)
    (partial_attempt / "outcome.json").write_bytes(b"{partial")
    partial = expect_rejection(
        lambda: production.run(
            partial_run,
            production_gate=True,
            recover_interrupted=True,
        ),
        "malformed JSON",
    )

    orphan_run = foundation.initialize("v2-f4-precheckpoint-orphan")
    (orphan_run / "attempts/attempt-000001").mkdir()
    orphan = expect_rejection(
        lambda: production.run(
            orphan_run,
            production_gate=True,
            recover_interrupted=True,
        ),
        "attempt directory count differs from checkpoint",
    )

    required = (
        ordinary["status"] == "RETRYABLE_NONCLAIM"
        and ordinary["durable_outcome_quarantined"] is True
        and ordinary_checkpoint["event"]
        == "UNTRACKED_OUTCOME_QUARANTINED"
        and ordinary_audit["status"] == "RETRYABLE_NONCLAIM"
        and quarantined_success["status"] == "RETRYABLE_NONCLAIM"
        and quarantined_success["durable_outcome_quarantined"] is True
        and success_quarantine_checkpoint["event"]
        == "UNTRACKED_OUTCOME_QUARANTINED"
        and success_audit["status"] == "RETRYABLE_NONCLAIM"
        and retry_after_quarantine["attempt_number"] == 2
    )
    if not required:
        raise AssertionError("durable-outcome quarantine semantics differ")
    return {
        "ordinary_durable_outcome_quarantined": True,
        "uncheckpointed_success_never_promoted": True,
        "ordinary_checkpoint_event": ordinary_checkpoint["event"],
        "success_checkpoint_event": success_quarantine_checkpoint["event"],
        "post_quarantine_status": success_audit["status"],
        "fresh_retry_attempt_number": retry_after_quarantine[
            "attempt_number"
        ],
        "synthetic_retry_child_calls": child_calls,
        "partial_outcome_fails_closed": partial["rejected"],
        "precheckpoint_orphan_fails_closed": orphan["rejected"],
        "manual_remediation_observations": {
            "partial_outcome": partial,
            "precheckpoint_orphan": orphan,
        },
        "real_solver_or_checker_executions": 0,
    }


def case_sat_semantic_replay(
    foundation: base.Foundation,
) -> dict[str, object]:
    run_directory = foundation.initialize("v2-sat-semantic")
    (
        manifest,
        manifest_hash,
        attempt,
        running,
        running_hash,
        config,
    ) = base.create_running_attempt(run_directory)
    variable_count = int(manifest["expected_formula"]["variables"])
    solver_result = attempt / "solver.result"
    solver_result.write_bytes(
        (
            "s SATISFIABLE\nv "
            + " ".join(
                f"-{variable}" for variable in range(1, variable_count + 1)
            )
            + " 0\n"
        ).encode("ascii")
    )
    write_json(
        attempt / "resource-solver.json",
        base.clean_resource_report(
            run_directory,
            "solver",
            int(base.limits()["solver_memory_mib"]),
            base.limits(),
        ),
    )
    stdout = attempt / "solver.stdout"
    stderr = attempt / "solver.stderr"
    stdout.write_bytes(b"")
    stderr.write_bytes(b"")
    command = tuple(config["commands"]["solver"])
    executable_hash = base.sha256(Path(command[0]))
    child = ChildResult(
        command=command,
        command_sha256=_command_sha256(command),
        executable_sha256_before=executable_hash,
        executable_sha256_after=executable_hash,
        exit_code=10,
        termination_signal=None,
        timed_out=False,
        memory_limit_exceeded=False,
        started_unix_ns=1,
        finished_unix_ns=2,
        wall_seconds=0.001,
        user_cpu_seconds=0.0,
        system_cpu_seconds=0.0,
        maximum_resident_set_size_mib=1.0,
        maximum_resident_set_size_raw=1,
        maximum_resident_set_size_raw_unit="bytes",
        peak_polled_resident_set_size_mib=1.0,
        available_memory_before_bytes=16 << 30,
        wall_limit_seconds=int(base.limits()["solver_wall_seconds"]),
        memory_limit_mib=int(base.limits()["solver_memory_mib"]),
        file_limit_mib=int(base.limits()["file_limit_mib"]),
        stdout_path=str(stdout.resolve()),
        stdout_sha256=base.sha256(stdout),
        stderr_path=str(stderr.resolve()),
        stderr_sha256=base.sha256(stderr),
    )
    instance_binding = production._binding(
        attempt / production.INSTANCE_NAME, "v2 SAT instance"
    )
    result_binding = production._binding(
        solver_result, "v2 SAT solver result"
    )
    phase_record = {
        "schema": "gamma-theta-order13-k3-phase-record-v1",
        "schema_version": 1,
        "phase": "solver",
        "readonly_inputs_before": {"instance": instance_binding},
        "readonly_inputs_after": {"instance": instance_binding},
        "produced_outputs": {
            "solver_result": result_binding,
            "raw_binary_drat": None,
        },
        "child": asdict(child),
    }
    write_json(attempt / "child-solver.json", phase_record)

    assignment = canonical_json_bytes(
        [-variable for variable in range(1, variable_count + 1)]
    )
    candidate = {
        "schema": "gamma-theta-order13-k3-sat-candidate-v1",
        "schema_version": 1,
        "status": production.SAT_CANDIDATE,
        "template": manifest["template"],
        "instance": instance_binding,
        "solver_result": result_binding,
        "assignment_sha256": hashlib.sha256(assignment).hexdigest(),
        "h_edges": [],
        "eternal_family": [],
        "required_next_action": (
            "Freeze and run a standalone candidate verifier independent "
            "of this search and decoding core."
        ),
    }
    write_json(attempt / "candidate.json", candidate)
    outcome = {
        "schema": "gamma-theta-order13-k3-attempt-outcome-v1",
        "schema_version": 1,
        "status": production.SAT_CANDIDATE,
        "claim_status": "SAT_CANDIDATE_ONLY",
        "details": {"candidate": candidate},
        "artifacts": production._attempt_artifacts(attempt),
        "finished_unix_ns": 2,
    }
    base.append_terminal(
        run_directory,
        manifest_hash,
        running,
        running_hash,
        attempt,
        status=production.SAT_CANDIDATE,
        event="RUN_FINISHED",
        outcome=outcome,
    )
    cnf = expect_rejection(
        lambda: base.audit_without_children(run_directory),
        "model falsifies CNF clause",
    )
    with patch.object(
        production, "validate_model_satisfies_cnf", return_value=None
    ):
        semantics = expect_rejection(
            lambda: base.audit_without_children(run_directory),
            "eternal family is empty",
        )
    return {
        "complete_assignment_replayed_against_frozen_cnf": cnf["rejected"],
        "direct_graph_game_semantics_replayed": semantics["rejected"],
        "phase_record_shape_and_bindings_accepted_before_semantics": True,
        "cnf_rejection": cnf,
        "semantic_rejection_after_cnf_stage_instrumented": semantics,
        "real_solver_or_checker_executions": 0,
    }


def case_positive_phase_records(
    foundation: base.Foundation,
) -> dict[str, object]:
    run_directory, phases = new_success(foundation, "v2-phase-positive")
    attempt = run_directory / "attempts/attempt-000001"
    expected = {
        "solver": (
            {"instance"},
            {"solver_result", "raw_binary_drat"},
        ),
        "raw_forward": ({"instance", "raw proof"}, set()),
        "normalizer": (
            {"raw proof", "normalizer source"},
            {"normalized_binary_rup", "normalization_report"},
        ),
        "normalized_forward": (
            {"instance", "normalized proof"},
            set(),
        ),
        "lrat_conversion": (
            {"instance", "normalized proof"},
            {"converted_lrat"},
        ),
        "lrat_check": ({"instance", "LRAT"}, set()),
    }
    observed: dict[str, dict[str, object]] = {}
    for phase in phases:
        record = read_json(attempt / f"child-{phase}.json")
        before = record["readonly_inputs_before"]
        after = record["readonly_inputs_after"]
        produced = record["produced_outputs"]
        expected_readonly, expected_produced = expected[phase]
        if (
            before != after
            or set(before) != expected_readonly
            or set(produced) != expected_produced
        ):
            raise AssertionError(f"{phase} positive phase record differs")
        observed[phase] = {
            "readonly_roles": sorted(before),
            "produced_roles": sorted(produced),
            "before_equals_after": before == after,
        }
    lrat = production._binding(
        attempt / "proof.converted.lrat", "v2 positive LRAT"
    )
    conversion = read_json(attempt / "child-lrat_conversion.json")
    checker = read_json(attempt / "child-lrat_check.json")
    certificate = read_json(attempt / "certificate.json")
    if not (
        conversion["produced_outputs"]["converted_lrat"] == lrat
        and checker["readonly_inputs_before"]["LRAT"] == lrat
        and checker["readonly_inputs_after"]["LRAT"] == lrat
        and certificate["converted_lrat"] == lrat
    ):
        raise AssertionError("positive LRAT crosslink differs")
    return {
        "phase_count": len(observed),
        "phases": observed,
        "lrat_conversion_checker_certificate_crosslink": True,
        "real_solver_or_checker_executions": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=REVIEW / "evidence_v2.json",
    )
    arguments = parser.parse_args()
    if arguments.output.parent.resolve() != REVIEW.resolve():
        raise ValueError("v2 evidence must be written in the review directory")
    frozen_before, preserved_before = verify_bound_bytes()

    with tempfile.TemporaryDirectory(
        prefix=".referee-v2-fixtures-", dir=REVIEW
    ) as temporary:
        foundation = base.Foundation(Path(temporary).resolve())
        tools = base.tool_evidence()
        with foundation.frozen_context():
            checks = {
                "positive_phase_records": case_positive_phase_records(
                    foundation
                ),
                "readonly_complete_chain_audit": (
                    base.case_readonly_success(foundation)
                ),
                "sat_candidate_semantic_replay": case_sat_semantic_replay(
                    foundation
                ),
                "resource_limits_and_prelaunch_gate": (
                    base.case_resource_limits(foundation)
                ),
                "runtime_source_binding": base.case_runtime_source_binding(
                    foundation
                ),
                "binary_proof_normalization": base.case_normalization(
                    foundation
                ),
                "interruption_recovery_and_fresh_restart": (
                    base.case_recovery_and_restart(foundation)
                ),
                "pre_RUN_STARTED_crash_windows": (
                    case_pre_run_started_crash_windows(foundation)
                ),
                "malformed_metadata_v1_regressions": (
                    base.case_v1_malformed_metadata_regressions(foundation)
                ),
                "adjacent_output_crosslink_matrix": (
                    case_output_crosslink_matrix(foundation)
                ),
            }
            repaired_findings = {
                "F1_attempt_formula_content_equality": (
                    case_f1_attempt_formula(foundation)
                ),
                "F2_phase_input_output_crosslinks": (
                    case_f2_phase_crosslinks(foundation)
                ),
                "F3_exact_certificate_and_details_shape": (
                    case_f3_exact_claim_shapes(foundation)
                ),
                "F4_durable_outcome_quarantine": (
                    case_f4_quarantine(foundation)
                ),
            }

    frozen_after, preserved_after = verify_bound_bytes()
    if frozen_before != frozen_after or preserved_before != preserved_after:
        raise AssertionError("review execution changed frozen or preserved bytes")

    required = (
        repaired_findings[
            "F1_attempt_formula_content_equality"
        ]["exact_attack_rejected"]
        and repaired_findings[
            "F2_phase_input_output_crosslinks"
        ]["exact_postcheck_substitution_rejected"]
        and repaired_findings[
            "F2_phase_input_output_crosslinks"
        ]["conversion_output_refresh_still_caught_by_checker_input"]
        and repaired_findings[
            "F3_exact_certificate_and_details_shape"
        ]["rejected_count"]
        == 3
        and repaired_findings[
            "F4_durable_outcome_quarantine"
        ]["uncheckpointed_success_never_promoted"]
        and checks[
            "malformed_metadata_v1_regressions"
        ]["rejected_count"]
        == 6
        and checks[
            "adjacent_output_crosslink_matrix"
        ]["rejected_count"]
        == 4
    )
    if not required:
        raise AssertionError("a decisive repaired-v2 requirement failed")
    resumability = checks["pre_RUN_STARTED_crash_windows"]
    verdict = (
        "ACCEPT"
        if resumability["safe_explicit_retryable_nonclaim_path_exists"]
        else "REJECT"
    )

    evidence = {
        "schema": "order13-k3-production-independent-referee-evidence-v2",
        "verdict": verdict,
        "scope": (
            "Final repaired frozen local bytes; synthetic fixtures only; no "
            "real SAT solver or proof checker executed."
        ),
        "final_frozen_file_sha256": frozen_after,
        "preserved_v1_artifact_sha256": preserved_after,
        "tool_evidence": tools,
        "checks": checks,
        "repaired_findings": repaired_findings,
        "adjacent_recovery_observation": (
            "Partial outcome bytes and every tested pre-RUN_STARTED orphan "
            "prefix fail closed but require manual remediation. None can "
            "produce a SAT/UNSAT claim, yet --recover-interrupted cannot "
            "record a retryable nonclaim or enable a fresh attempt."
        ),
        "real_solver_or_proof_checker_execution_count": 0,
    }
    arguments.output.write_bytes(
        (json.dumps(evidence, indent=2, sort_keys=True) + "\n").encode("utf-8")
    )
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
