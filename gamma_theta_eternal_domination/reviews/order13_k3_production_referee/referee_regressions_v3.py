#!/usr/bin/env python3
"""Independent synthetic replay for the final precheckpoint-recovery repair.

The preserved v1 and v2 referee modules are imported only for fixture helpers
and already-established hostile cases. Their main routines are never invoked.
Executable-looking fixtures are plain text and no real solver/checker runs.
"""

from __future__ import annotations

import argparse
import json
import os
import stat
import sys
import tempfile
from pathlib import Path
from typing import Callable
from unittest.mock import patch


REVIEW = Path(__file__).resolve().parent
CAMPAIGN = REVIEW.parents[1]
sys.path.insert(0, str(REVIEW))
sys.path.insert(0, str(CAMPAIGN / "src"))

import referee_regressions_v2 as prior  # noqa: E402


base = prior.base
production = prior.production

FINAL_FROZEN = {
    "src/search/order13_k3/production.py": (
        "e7052cd2d758ac653948c2231d3c556dcff822b1a511299ae43026a1de55e811"
    ),
    "src/search/order13_k3/normalize_bdrat.py": (
        "a09f67d39932b6c3bb19b31a0792e4f47f515820c642e9418d3e374f555de18c"
    ),
    "src/search/order13_k3/PRODUCTION_PROTOCOL.md": (
        "f5b6aa63c36fae363fdc2b0c6663f207bab09ad9bf70c525eb75fc4fc3805a34"
    ),
    "tests/test_order13_k3_production.py": (
        "99308d0002712b91427f655d46b1a7f93d467bf63af28b218644df64f38557a5"
    ),
}
PRESERVED_HISTORY = {
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
    "ADDENDUM.md": (
        "9c450c0a37e96d191bf5e9534babd418da44e0a76133bad7e3ba4dab80993f17"
    ),
    "evidence_v2.json": (
        "f9e1ad4fcc5e7ddaa8c446a7b28527622b0f78d790d2b15746668462400d489b"
    ),
    "referee_regressions_v2.py": (
        "aa69db3f287fea20fa9de426e406c8843f47abd65a94fa09966bd6333e841fa7"
    ),
    "run_readonly_upstream_tests_v2.py": (
        "07029364acff8acca83918841db82ad66951e419e93c2e3fee609b23b3a90bc4"
    ),
    "RESEARCH_LOG_V2.md": (
        "5c91df7c1ee62b96291682fc850012dfbe6b7632aa1f42c7bc512417e3626d19"
    ),
}


def read_json(path: Path) -> dict[str, object]:
    return prior.read_json(path)


def write_json(path: Path, value: object) -> None:
    prior.write_json(path, value)


def verify_bound_bytes() -> tuple[dict[str, str], dict[str, str]]:
    frozen = {
        relative: base.sha256(CAMPAIGN / relative)
        for relative in FINAL_FROZEN
    }
    preserved = {
        name: base.sha256(REVIEW / name)
        for name in PRESERVED_HISTORY
    }
    if frozen != FINAL_FROZEN:
        raise AssertionError("final-v3 frozen implementation bytes changed")
    if preserved != PRESERVED_HISTORY:
        raise AssertionError("a preserved v1/v2 referee artifact changed")
    return frozen, preserved


def expect_rejection(
    action: Callable[[], object],
    fragment: str,
) -> dict[str, object]:
    return base.expect_rejection(action, fragment)


def observe_audit(run_directory: Path) -> dict[str, object]:
    try:
        report = base.audit_without_children(run_directory)
    except Exception as error:
        return {
            "accepted": False,
            "exception_type": type(error).__name__,
            "message": str(error),
        }
    return {
        "accepted": True,
        "status": report["status"],
        "proof_freshly_replayed": report["proof_freshly_replayed"],
    }


def synthetic_retry(run_directory: Path) -> dict[str, object]:
    details = {
        "phase_status": "SYNTHETIC_V3_RETRY_NONCLAIM",
        "phase_details": {},
    }
    with patch.object(
        production,
        "_execute",
        return_value=("RETRYABLE_NONCLAIM", details),
    ), patch.object(
        production,
        "run_bounded_child",
        side_effect=AssertionError("synthetic v3 retry launched a child"),
    ) as child:
        result = production.run(
            run_directory,
            production_gate=True,
            recover_interrupted=False,
        )
    if child.call_count != 0:
        raise AssertionError("synthetic v3 retry launched a child")
    return result


def quarantine_directories(run_directory: Path) -> list[Path]:
    return sorted(
        path
        for path in run_directory.parent.glob(
            f"{run_directory.name}.recovery-quarantine-*"
        )
        if path.is_dir() and not path.is_symlink()
    )


def validate_quarantine(
    run_directory: Path,
    quarantine: object,
    *,
    source_path: Path,
    expected_kind: str,
) -> tuple[Path, dict[str, object]]:
    if not isinstance(quarantine, dict) or set(quarantine) != {
        "quarantine_directory",
        "quarantined_path",
        "record",
        "moved_binding",
    }:
        raise AssertionError("quarantine return shape differs")
    container = Path(str(quarantine["quarantine_directory"]))
    destination = Path(str(quarantine["quarantined_path"]))
    if (
        container.parent != run_directory.parent
        or destination.parent != container
        or destination.name != source_path.name
        or not container.is_dir()
        or container.is_symlink()
    ):
        raise AssertionError("quarantine path relation differs")
    record_binding = quarantine["record"]
    if not isinstance(record_binding, dict):
        raise AssertionError("quarantine record binding is absent")
    record_path = Path(str(record_binding.get("path")))
    if production._binding(record_path, "v3 quarantine record") != record_binding:
        raise AssertionError("quarantine record binding differs")
    record = read_json(record_path)
    if (
        set(record)
        != {
            "schema",
            "schema_version",
            "claim_status",
            "reason",
            "original_path",
            "quarantined_path",
            "moved_kind",
            "moved_binding",
            "moved_unix_ns",
        }
        or record.get("schema")
        != "gamma-theta-order13-k3-recovery-quarantine-v1"
        or record.get("schema_version") != 1
        or record.get("claim_status") != "NO_SAT_OR_UNSAT_CLAIM"
        or not isinstance(record.get("reason"), str)
        or not record["reason"]
        or record.get("original_path") != str(source_path.absolute())
        or record.get("quarantined_path") != str(destination.absolute())
        or record.get("moved_kind") != expected_kind
        or type(record.get("moved_unix_ns")) is not int
        or int(record["moved_unix_ns"]) <= 0
    ):
        raise AssertionError("quarantine record semantics differ")
    if expected_kind == "directory":
        if (
            record.get("moved_binding") is not None
            or quarantine.get("moved_binding") is not None
        ):
            raise AssertionError("directory quarantine invented a file binding")
    elif expected_kind == "regular_file":
        moved_binding = production._binding(
            destination, "v3 quarantined regular file"
        )
        if (
            record.get("moved_binding") != moved_binding
            or quarantine.get("moved_binding") != moved_binding
        ):
            raise AssertionError("file quarantine binding differs")
    return destination, record


class SyntheticPreRunStartedCrash(BaseException):
    """Injected process loss before the RUN_STARTED checkpoint."""


def case_pre_run_started_windows(
    foundation: base.Foundation,
) -> dict[str, object]:
    results: dict[str, dict[str, object]] = {}
    original_binding = production._binding

    def injected_binding(label_to_crash: str):
        def binding(path: Path, label: str) -> dict[str, object]:
            if label == label_to_crash:
                raise SyntheticPreRunStartedCrash(label)
            return original_binding(path, label)

        return binding

    stages = (
        "after_attempt_mkdir",
        "after_instance_copy_and_fsync",
        "after_attempt_config_durable_write",
        "immediately_before_RUN_STARTED_append",
    )
    for stage in stages:
        run_directory = foundation.initialize(f"v3-pre-start-{stage}")
        checkpoint_zero = (
            run_directory / "checkpoints/checkpoint-000000.json"
        )
        checkpoint_zero_bytes = checkpoint_zero.read_bytes()
        checkpoint_zero_sha256 = base.sha256(checkpoint_zero)

        if stage == "after_attempt_mkdir":
            injection = patch.object(
                production.shutil,
                "copyfile",
                side_effect=SyntheticPreRunStartedCrash(stage),
            )
        elif stage == "after_instance_copy_and_fsync":
            injection = patch.object(
                production,
                "_binding",
                side_effect=injected_binding("attempt instance"),
            )
        elif stage == "after_attempt_config_durable_write":
            injection = patch.object(
                production,
                "_binding",
                side_effect=injected_binding("attempt config"),
            )
        else:
            injection = patch.object(
                production,
                "_append_checkpoint",
                side_effect=SyntheticPreRunStartedCrash(stage),
            )

        crashed = False
        original_fsync = production.os.fsync
        with injection, patch.object(
            production.os, "fsync", wraps=original_fsync
        ) as fsync_spy, patch.object(
            production,
            "run_bounded_child",
            side_effect=AssertionError("pre-start fixture launched a child"),
        ) as child:
            try:
                production.run(
                    run_directory,
                    production_gate=True,
                    recover_interrupted=False,
                )
            except SyntheticPreRunStartedCrash:
                crashed = True
        if not crashed or child.call_count != 0:
            raise AssertionError(f"{stage} injection did not stop before child")

        attempt = run_directory / "attempts/attempt-000001"
        entries = sorted(path.name for path in attempt.iterdir())
        expected_entries = {
            "after_attempt_mkdir": [],
            "after_instance_copy_and_fsync": [production.INSTANCE_NAME],
            "after_attempt_config_durable_write": [
                "attempt-config.json",
                production.INSTANCE_NAME,
            ],
            "immediately_before_RUN_STARTED_append": [
                "attempt-config.json",
                production.INSTANCE_NAME,
            ],
        }[stage]
        if entries != expected_entries:
            raise AssertionError(f"{stage} durable prefix differs")
        required_fsyncs = {
            "after_attempt_mkdir": 0,
            "after_instance_copy_and_fsync": 1,
            "after_attempt_config_durable_write": 3,
            "immediately_before_RUN_STARTED_append": 3,
        }[stage]
        if fsync_spy.call_count != required_fsyncs:
            raise AssertionError(
                f"{stage} observed {fsync_spy.call_count} fsyncs, "
                f"expected {required_fsyncs}"
            )
        before_tree = base.tree_digest(attempt)
        before_mode = stat.S_IMODE(attempt.stat().st_mode)

        audit_rejection = expect_rejection(
            lambda target=run_directory: base.audit_without_children(target),
            "attempt directory count differs from checkpoint",
        )
        ordinary_rejection = expect_rejection(
            lambda target=run_directory: production.run(
                target,
                production_gate=True,
                recover_interrupted=False,
            ),
            "attempt directory count differs from checkpoint",
        )
        with patch.object(
            production,
            "run_bounded_child",
            side_effect=AssertionError("orphan recovery launched a child"),
        ) as recovery_child:
            recovered = production.run(
                run_directory,
                production_gate=True,
                recover_interrupted=True,
            )
        if recovery_child.call_count != 0:
            raise AssertionError("pre-start recovery launched a child")
        if (
            recovered.get("status") != "RETRYABLE_NONCLAIM"
            or recovered.get("precheckpoint_orphan_quarantined") is not True
            or recovered.get("child_launched") is not False
            or recovered.get("checkpoint_sha256") != checkpoint_zero_sha256
            or attempt.exists()
            or attempt.is_symlink()
        ):
            raise AssertionError(f"{stage} recovery result differs")
        destination, record = validate_quarantine(
            run_directory,
            recovered.get("quarantine"),
            source_path=attempt,
            expected_kind="directory",
        )
        if (
            base.tree_digest(destination) != before_tree
            or stat.S_IMODE(destination.stat().st_mode) != before_mode
        ):
            raise AssertionError(f"{stage} quarantine changed orphan bytes")
        if (
            checkpoint_zero.read_bytes() != checkpoint_zero_bytes
            or sorted(
                path.name
                for path in (run_directory / "checkpoints").iterdir()
            )
            != ["checkpoint-000000.json"]
        ):
            raise AssertionError(f"{stage} changed the checkpoint chain")
        post_recovery_audit = base.audit_without_children(run_directory)
        if (
            post_recovery_audit["status"] != "PENDING"
            or post_recovery_audit["attempt_count"] != 0
        ):
            raise AssertionError(f"{stage} did not restore an auditable tree")

        fresh = synthetic_retry(run_directory)
        final_audit = base.audit_without_children(run_directory)
        if (
            fresh.get("attempt_number") != 1
            or fresh.get("status") != "RETRYABLE_NONCLAIM"
            or final_audit["attempt_count"] != 1
            or final_audit["status"] != "RETRYABLE_NONCLAIM"
        ):
            raise AssertionError(f"{stage} fresh retry relation differs")
        results[stage] = {
            "injection_observed": True,
            "instance_and_config_fsync_call_count": fsync_spy.call_count,
            "durable_attempt_entries": entries,
            "audit_rejected_orphan": audit_rejection["rejected"],
            "ordinary_run_rejected_orphan": ordinary_rejection["rejected"],
            "explicit_recovery_status": recovered["status"],
            "recovery_child_launched": False,
            "checkpoint_zero_unchanged": True,
            "quarantine_tree_byte_and_mode_preserved": True,
            "quarantine_record_claim_status": record["claim_status"],
            "post_recovery_audit_status": post_recovery_audit["status"],
            "fresh_retry_attempt_number": fresh["attempt_number"],
            "fresh_retry_status": fresh["status"],
        }
    return {
        "window_count": len(results),
        "recovered_count": sum(
            1
            for item in results.values()
            if item["explicit_recovery_status"] == "RETRYABLE_NONCLAIM"
        ),
        "all_windows_claim_safe_and_freshly_retryable": all(
            item["recovery_child_launched"] is False
            and item["fresh_retry_attempt_number"] == 1
            and item["quarantine_tree_byte_and_mode_preserved"] is True
            for item in results.values()
        ),
        "cases": results,
        "real_solver_or_checker_executions": 0,
    }


def case_malformed_orphans(
    foundation: base.Foundation,
) -> dict[str, object]:
    results: dict[str, dict[str, object]] = {}
    specifications = {
        "regular_file_instead_of_directory": (
            "precheckpoint orphan attempt differs"
        ),
        "symlink_instead_of_directory": (
            "precheckpoint orphan attempt differs"
        ),
        "wrong_next_number": "precheckpoint orphan attempt differs",
        "two_extra_attempt_entries": (
            "attempt directory count differs from checkpoint"
        ),
        "orphan_while_latest_is_RUNNING": (
            "attempt directory count differs from checkpoint"
        ),
        "orphan_while_latest_is_frozen": (
            "attempt directory count differs from checkpoint"
        ),
    }
    for case, fragment in specifications.items():
        if case == "orphan_while_latest_is_RUNNING":
            run_directory = foundation.initialize(f"v3-malformed-{case}")
            base.create_running_attempt(run_directory)
            orphan = run_directory / "attempts/attempt-000002"
            orphan.mkdir()
        elif case == "orphan_while_latest_is_frozen":
            run_directory, _ = prior.new_success(
                foundation, f"v3-malformed-{case}"
            )
            orphan = run_directory / "attempts/attempt-000002"
            orphan.mkdir()
        else:
            run_directory = foundation.initialize(f"v3-malformed-{case}")
            attempts = run_directory / "attempts"
            if case == "regular_file_instead_of_directory":
                orphan = attempts / "attempt-000001"
                orphan.write_bytes(b"not a directory\n")
            elif case == "symlink_instead_of_directory":
                target = run_directory.parent / f"{run_directory.name}-target"
                target.mkdir()
                orphan = attempts / "attempt-000001"
                orphan.symlink_to(target, target_is_directory=True)
            elif case == "wrong_next_number":
                orphan = attempts / "attempt-000002"
                orphan.mkdir()
            else:
                orphan = attempts / "attempt-000001"
                orphan.mkdir()
                (attempts / "attempt-000002").mkdir()
        before = base.tree_digest(run_directory)
        rejection = expect_rejection(
            lambda target=run_directory: production.run(
                target,
                production_gate=True,
                recover_interrupted=True,
            ),
            fragment,
        )
        after = base.tree_digest(run_directory)
        if (
            before != after
            or quarantine_directories(run_directory)
        ):
            raise AssertionError(f"{case} rejection changed durable bytes")
        results[case] = {
            "rejected": rejection["rejected"],
            "stable_message_fragment": fragment,
            "durable_tree_unchanged": True,
            "quarantine_created": False,
        }
    return {
        "case_count": len(results),
        "rejected_count": sum(
            1 for item in results.values() if item["rejected"] is True
        ),
        "cases": results,
        "real_solver_or_checker_executions": 0,
    }


def case_opaque_orphan_contents(
    foundation: base.Foundation,
) -> dict[str, object]:
    run_directory = foundation.initialize("v3-opaque-orphan-contents")
    orphan = run_directory / "attempts/attempt-000001"
    orphan.mkdir(mode=0o700)
    (orphan / "unknown.bin").write_bytes(b"\x00opaque\xffbytes\n")
    nested = orphan / "untrusted-nested"
    nested.mkdir(mode=0o711)
    (nested / "malformed.json").write_bytes(b'{"partial"')
    external_target = run_directory.parent / "v3-opaque-link-target"
    external_target.write_bytes(b"external target remains outside\n")
    (nested / "opaque-link").symlink_to(external_target)
    before_tree = base.tree_digest(orphan)
    before_mode = stat.S_IMODE(orphan.stat().st_mode)

    audit = expect_rejection(
        lambda: base.audit_without_children(run_directory),
        "attempt directory count differs from checkpoint",
    )
    ordinary = expect_rejection(
        lambda: production.run(
            run_directory,
            production_gate=True,
            recover_interrupted=False,
        ),
        "attempt directory count differs from checkpoint",
    )
    with patch.object(
        production,
        "run_bounded_child",
        side_effect=AssertionError("opaque orphan recovery launched a child"),
    ) as child:
        recovered = production.run(
            run_directory,
            production_gate=True,
            recover_interrupted=True,
        )
    if (
        child.call_count != 0
        or recovered.get("status") != "RETRYABLE_NONCLAIM"
        or recovered.get("precheckpoint_orphan_quarantined") is not True
    ):
        raise AssertionError("opaque orphan recovery differs")
    destination, record = validate_quarantine(
        run_directory,
        recovered.get("quarantine"),
        source_path=orphan,
        expected_kind="directory",
    )
    if (
        base.tree_digest(destination) != before_tree
        or stat.S_IMODE(destination.stat().st_mode) != before_mode
        or external_target.read_bytes() != b"external target remains outside\n"
    ):
        raise AssertionError("opaque orphan contents were changed or followed")
    post = base.audit_without_children(run_directory)
    fresh = synthetic_retry(run_directory)
    if (
        post["status"] != "PENDING"
        or post["attempt_count"] != 0
        or fresh.get("attempt_number") != 1
    ):
        raise AssertionError("opaque orphan did not restore fresh retry")
    return {
        "ordinary_audit_rejected": audit["rejected"],
        "ordinary_run_rejected": ordinary["rejected"],
        "unknown_binary_preserved": True,
        "malformed_nested_JSON_preserved": True,
        "nested_symlink_preserved_without_following_target": True,
        "structural_envelope_only": (
            "exactly one extra, exact next-numbered canonical path, real "
            "directory, latest status RUNNABLE"
        ),
        "contents_parsed_or_trusted": False,
        "quarantine_record_claim_status": record["claim_status"],
        "recovery_status": recovered["status"],
        "recovery_child_launched": False,
        "post_recovery_audit_status": post["status"],
        "fresh_retry_attempt_number": fresh["attempt_number"],
        "assessment": (
            "Opaque non-destructive quarantine is sufficient here because "
            "the canonical directory is atomically removed from the trusted "
            "run tree before retry, no contained bytes are interpreted, and "
            "all claim-bearing run state remains checkpoint-audited."
        ),
        "real_solver_or_checker_executions": 0,
    }


def case_orphan_after_retryable(
    foundation: base.Foundation,
) -> dict[str, object]:
    run_directory = foundation.initialize("v3-orphan-after-retryable")
    first = synthetic_retry(run_directory)
    if first.get("attempt_number") != 1:
        raise AssertionError("first retryable attempt number differs")
    orphan = run_directory / "attempts/attempt-000002"
    orphan.mkdir(mode=0o700)
    (orphan / "opaque-second-attempt.bin").write_bytes(b"opaque attempt two\n")
    before = base.tree_digest(orphan)
    ordinary = expect_rejection(
        lambda: base.audit_without_children(run_directory),
        "attempt directory count differs from checkpoint",
    )
    with patch.object(
        production,
        "run_bounded_child",
        side_effect=AssertionError("retryable orphan recovery launched a child"),
    ) as child:
        recovered = production.run(
            run_directory,
            production_gate=True,
            recover_interrupted=True,
        )
    if (
        child.call_count != 0
        or recovered.get("status") != "RETRYABLE_NONCLAIM"
        or recovered.get("precheckpoint_orphan_quarantined") is not True
    ):
        raise AssertionError("retryable orphan recovery differs")
    destination, record = validate_quarantine(
        run_directory,
        recovered.get("quarantine"),
        source_path=orphan,
        expected_kind="directory",
    )
    if base.tree_digest(destination) != before:
        raise AssertionError("retryable orphan quarantine changed bytes")
    post = base.audit_without_children(run_directory)
    fresh = synthetic_retry(run_directory)
    final = base.audit_without_children(run_directory)
    if (
        post["status"] != "RETRYABLE_NONCLAIM"
        or post["attempt_count"] != 1
        or fresh.get("attempt_number") != 2
        or final["attempt_count"] != 2
    ):
        raise AssertionError("retryable orphan fresh attempt relation differs")
    return {
        "ordinary_audit_rejected": ordinary["rejected"],
        "latest_status_before_orphan": "RETRYABLE_NONCLAIM",
        "opaque_bytes_preserved": True,
        "quarantine_record_claim_status": record["claim_status"],
        "recovery_child_launched": False,
        "post_recovery_status": post["status"],
        "post_recovery_attempt_count": post["attempt_count"],
        "fresh_retry_attempt_number": fresh["attempt_number"],
        "real_solver_or_checker_executions": 0,
    }


def validate_recovered_outcome(
    run_directory: Path,
    attempt: Path,
    *,
    expected_attempt_number: int,
) -> dict[str, object]:
    outcome_path = attempt / "outcome.json"
    outcome = read_json(outcome_path)
    if (
        set(outcome)
        != {
            "schema",
            "schema_version",
            "status",
            "claim_status",
            "reason",
            "artifacts",
            "finished_unix_ns",
        }
        or outcome.get("schema")
        != "gamma-theta-order13-k3-attempt-outcome-v1"
        or outcome.get("schema_version") != 1
        or outcome.get("status") != production.RECOVERED_OUTCOME_STATUS
        or outcome.get("claim_status") != "NO_SAT_OR_UNSAT_CLAIM"
        or outcome.get("reason") != production.RECOVERY_REASON
    ):
        raise AssertionError("canonical recovery outcome differs")
    checkpoint_path = (
        run_directory
        / "checkpoints"
        / f"checkpoint-{2 * expected_attempt_number:06d}.json"
    )
    checkpoint = read_json(checkpoint_path)
    if (
        checkpoint.get("event") != "INTERRUPTED_RECOVERED"
        or checkpoint.get("status") != "RETRYABLE_NONCLAIM"
        or checkpoint.get("attempt_count") != expected_attempt_number
        or checkpoint.get("outcome")
        != production._binding(outcome_path, "v3 recovery outcome")
    ):
        raise AssertionError("canonical recovery checkpoint differs")
    return {
        "outcome_status": outcome["status"],
        "claim_status": outcome["claim_status"],
        "checkpoint_event": checkpoint["event"],
        "checkpoint_status": checkpoint["status"],
    }


def recover_opaque_outcome_case(
    foundation: base.Foundation,
    name: str,
    *,
    complete_success: bool,
) -> dict[str, object]:
    if complete_success:
        run_directory, _ = prior.new_success(foundation, name)
        (
            run_directory / "checkpoints/checkpoint-000002.json"
        ).unlink()
        attempt = run_directory / "attempts/attempt-000001"
    else:
        run_directory = foundation.initialize(name)
        _, _, attempt, _, _, _ = base.create_running_attempt(run_directory)
        (attempt / "outcome.json").write_bytes(b'{"schema":"partial"')
    old_outcome = attempt / "outcome.json"
    old_bytes = old_outcome.read_bytes()
    ordinary_audit = expect_rejection(
        lambda: base.audit_without_children(run_directory),
        "running attempt unexpectedly has an outcome",
    )
    ordinary_run = expect_rejection(
        lambda: production.run(
            run_directory,
            production_gate=True,
            recover_interrupted=False,
        ),
        "running attempt unexpectedly has an outcome",
    )
    with patch.object(
        production,
        "run_bounded_child",
        side_effect=AssertionError("opaque outcome recovery launched a child"),
    ) as child:
        recovered = production.run(
            run_directory,
            production_gate=True,
            recover_interrupted=True,
        )
    if (
        child.call_count != 0
        or recovered.get("status") != "RETRYABLE_NONCLAIM"
        or recovered.get("uncheckpointed_outcome_quarantined") is not True
        or recovered.get("durable_outcome_quarantined") is not True
        or recovered.get("child_launched") is not False
    ):
        raise AssertionError("opaque outcome recovery result differs")
    destination, record = validate_quarantine(
        run_directory,
        recovered.get("quarantine"),
        source_path=old_outcome,
        expected_kind="regular_file",
    )
    if destination.read_bytes() != old_bytes:
        raise AssertionError("opaque outcome bytes changed in quarantine")
    canonical = validate_recovered_outcome(
        run_directory, attempt, expected_attempt_number=1
    )
    audit = base.audit_without_children(run_directory)
    fresh = synthetic_retry(run_directory)
    final_audit = base.audit_without_children(run_directory)
    if (
        audit["status"] != "RETRYABLE_NONCLAIM"
        or audit["attempt_count"] != 1
        or fresh.get("attempt_number") != 2
        or fresh.get("status") != "RETRYABLE_NONCLAIM"
        or final_audit["attempt_count"] != 2
    ):
        raise AssertionError("opaque outcome fresh-retry relation differs")
    return {
        "input_kind": "complete_success" if complete_success else "partial_JSON",
        "ordinary_audit_rejected": ordinary_audit["rejected"],
        "ordinary_run_rejected": ordinary_run["rejected"],
        "opaque_bytes_preserved": True,
        "quarantine_record_claim_status": record["claim_status"],
        "uncheckpointed_success_never_promoted": complete_success,
        "canonical_recovery": canonical,
        "recovery_child_launched": False,
        "post_recovery_audit_status": audit["status"],
        "fresh_retry_attempt_number": fresh["attempt_number"],
        "real_solver_or_checker_executions": 0,
    }


def case_opaque_outcomes(
    foundation: base.Foundation,
) -> dict[str, object]:
    cases = {
        "partial_malformed_outcome": recover_opaque_outcome_case(
            foundation,
            "v3-opaque-partial",
            complete_success=False,
        ),
        "complete_success_outcome": recover_opaque_outcome_case(
            foundation,
            "v3-opaque-success",
            complete_success=True,
        ),
    }
    return {
        "case_count": len(cases),
        "recovered_count": sum(
            1
            for item in cases.values()
            if item["post_recovery_audit_status"] == "RETRYABLE_NONCLAIM"
        ),
        "cases": cases,
        "real_solver_or_checker_executions": 0,
    }


class SyntheticQuarantineCrash(BaseException):
    """Injected process loss during opaque-outcome quarantine."""


def case_orphan_quarantine_crash_safety(
    foundation: base.Foundation,
) -> dict[str, object]:
    results: dict[str, dict[str, object]] = {}
    stages = (
        "before_directory_move",
        "after_directory_move_before_record",
        "after_directory_record_before_return",
    )
    original_replace = production.os.replace
    original_binding = production._binding

    for stage in stages:
        run_directory = foundation.initialize(f"v3-oqcrash-{stage}")
        orphan = run_directory / "attempts/attempt-000001"
        orphan.mkdir(mode=0o700)
        payload_path = orphan / "opaque.bin"
        original_bytes = b"opaque orphan quarantine crash bytes\n"
        payload_path.write_bytes(original_bytes)
        checkpoint_zero = (
            run_directory / "checkpoints/checkpoint-000000.json"
        )
        checkpoint_zero_bytes = checkpoint_zero.read_bytes()

        if stage == "before_directory_move":
            injection = patch.object(
                production.os,
                "replace",
                side_effect=SyntheticQuarantineCrash(stage),
            )
        elif stage == "after_directory_move_before_record":
            def replace_then_crash(source: object, destination: object) -> None:
                original_replace(source, destination)
                raise SyntheticQuarantineCrash(stage)

            injection = patch.object(
                production.os,
                "replace",
                side_effect=replace_then_crash,
            )
        else:
            def record_binding_then_crash(
                path: Path, label: str
            ) -> dict[str, object]:
                if label == "quarantine record":
                    raise SyntheticQuarantineCrash(stage)
                return original_binding(path, label)

            injection = patch.object(
                production,
                "_binding",
                side_effect=record_binding_then_crash,
            )

        crashed = False
        with injection, patch.object(
            production,
            "run_bounded_child",
            side_effect=AssertionError("orphan quarantine crash launched a child"),
        ) as child:
            try:
                production.run(
                    run_directory,
                    production_gate=True,
                    recover_interrupted=True,
                )
            except SyntheticQuarantineCrash:
                crashed = True
        if not crashed or child.call_count != 0:
            raise AssertionError(f"{stage} crash injection was not observed")
        if (
            checkpoint_zero.read_bytes() != checkpoint_zero_bytes
            or len(list((run_directory / "checkpoints").iterdir())) != 1
        ):
            raise AssertionError(f"{stage} changed checkpoint state")

        if orphan.exists() or orphan.is_symlink():
            audit_after_crash = observe_audit(run_directory)
            if audit_after_crash["accepted"]:
                raise AssertionError(f"{stage} left an auditable orphan")
            with patch.object(
                production,
                "run_bounded_child",
                side_effect=AssertionError(
                    "orphan quarantine recovery retry launched a child"
                ),
            ) as retry_child:
                retry = production.run(
                    run_directory,
                    production_gate=True,
                    recover_interrupted=True,
                )
            if (
                retry_child.call_count != 0
                or retry.get("status") != "RETRYABLE_NONCLAIM"
            ):
                raise AssertionError(f"{stage} explicit retry differs")
            recovery_path = "explicit_recovery_retried"
        else:
            audit_after_crash = observe_audit(run_directory)
            if (
                not audit_after_crash["accepted"]
                or audit_after_crash["status"] != "PENDING"
            ):
                raise AssertionError(f"{stage} did not restore auditable PENDING")
            no_interruption = expect_rejection(
                lambda: production.run(
                    run_directory,
                    production_gate=True,
                    recover_interrupted=True,
                ),
                "there is no interrupted attempt to recover",
            )
            if not no_interruption["rejected"]:
                raise AssertionError(f"{stage} invented an interrupted attempt")
            recovery_path = "move_already_restored_run_tree"

        quarantines = quarantine_directories(run_directory)
        matching_payloads = [
            path
            for container in quarantines
            for path in container.rglob("opaque.bin")
            if path.is_file()
            and not path.is_symlink()
            and path.read_bytes() == original_bytes
        ]
        if not matching_payloads:
            raise AssertionError(f"{stage} lost opaque orphan bytes")
        unrecorded = [
            container
            for container in quarantines
            if not (container / "quarantine-record.json").exists()
        ]
        fresh = synthetic_retry(run_directory)
        audit = base.audit_without_children(run_directory)
        if (
            fresh.get("attempt_number") != 1
            or audit["status"] != "RETRYABLE_NONCLAIM"
            or audit["attempt_count"] != 1
        ):
            raise AssertionError(f"{stage} fresh run differs")
        results[stage] = {
            "crash_observed": True,
            "child_launched": False,
            "checkpoint_zero_unchanged": True,
            "audit_after_crash": audit_after_crash,
            "safe_continuation": recovery_path,
            "opaque_original_bytes_preserved": True,
            "quarantine_directory_count": len(quarantines),
            "unrecorded_quarantine_directory_count": len(unrecorded),
            "fresh_retry_attempt_number": fresh["attempt_number"],
        }
    return {
        "stage_count": len(results),
        "safe_continuation_count": sum(
            1
            for item in results.values()
            if item["fresh_retry_attempt_number"] == 1
            and item["opaque_original_bytes_preserved"] is True
        ),
        "cases": results,
        "real_solver_or_checker_executions": 0,
    }


def case_quarantine_crash_safety(
    foundation: base.Foundation,
) -> dict[str, object]:
    results: dict[str, dict[str, object]] = {}
    stages = (
        "before_move",
        "after_move_before_record",
        "after_record_before_recovery_outcome",
        "after_recovery_outcome_before_checkpoint",
    )
    original_replace = production.os.replace
    original_write_exclusive = production._write_exclusive

    for stage in stages:
        run_directory = foundation.initialize(f"v3-qcrash-{stage}")
        _, _, attempt, _, _, _ = base.create_running_attempt(run_directory)
        outcome_path = attempt / "outcome.json"
        original_bytes = b'{"opaque":"partial-v3"'
        outcome_path.write_bytes(original_bytes)
        running_checkpoint = (
            run_directory / "checkpoints/checkpoint-000001.json"
        )
        running_checkpoint_bytes = running_checkpoint.read_bytes()

        if stage == "before_move":
            injection = patch.object(
                production.os,
                "replace",
                side_effect=SyntheticQuarantineCrash(stage),
            )
        elif stage == "after_move_before_record":
            def replace_then_crash(source: object, destination: object) -> None:
                original_replace(source, destination)
                raise SyntheticQuarantineCrash(stage)

            injection = patch.object(
                production.os,
                "replace",
                side_effect=replace_then_crash,
            )
        elif stage == "after_record_before_recovery_outcome":
            def write_then_targeted_crash(path: Path, payload: bytes) -> None:
                if path == outcome_path:
                    raise SyntheticQuarantineCrash(stage)
                original_write_exclusive(path, payload)

            injection = patch.object(
                production,
                "_write_exclusive",
                side_effect=write_then_targeted_crash,
            )
        else:
            injection = patch.object(
                production,
                "_append_checkpoint",
                side_effect=SyntheticQuarantineCrash(stage),
            )

        crashed = False
        with injection, patch.object(
            production,
            "run_bounded_child",
            side_effect=AssertionError("quarantine crash launched a child"),
        ) as child:
            try:
                production.run(
                    run_directory,
                    production_gate=True,
                    recover_interrupted=True,
                )
            except SyntheticQuarantineCrash:
                crashed = True
        if not crashed or child.call_count != 0:
            raise AssertionError(f"{stage} crash injection was not observed")
        if (
            running_checkpoint.read_bytes() != running_checkpoint_bytes
            or (
                run_directory / "checkpoints/checkpoint-000002.json"
            ).exists()
        ):
            raise AssertionError(f"{stage} falsely checkpointed recovery")

        audit_after_crash = observe_audit(run_directory)
        if audit_after_crash["accepted"]:
            if audit_after_crash["status"] != "RUNNING_UNFINISHED_NONCLAIM":
                raise AssertionError(f"{stage} audit promoted a crash state")
        elif "running attempt unexpectedly has an outcome" not in str(
            audit_after_crash["message"]
        ):
            raise AssertionError(f"{stage} audit rejection differs")

        with patch.object(
            production,
            "run_bounded_child",
            side_effect=AssertionError("quarantine retry launched a child"),
        ) as retry_child:
            retry = production.run(
                run_directory,
                production_gate=True,
                recover_interrupted=True,
            )
        if retry_child.call_count != 0 or retry["status"] != "RETRYABLE_NONCLAIM":
            raise AssertionError(f"{stage} recovery retry differs")
        quarantines = quarantine_directories(run_directory)
        matching_payloads = [
            path
            for container in quarantines
            for path in container.rglob("outcome.json")
            if path.is_file()
            and not path.is_symlink()
            and path.read_bytes() == original_bytes
        ]
        if not matching_payloads:
            raise AssertionError(f"{stage} lost the original opaque bytes")
        canonical = validate_recovered_outcome(
            run_directory, attempt, expected_attempt_number=1
        )
        audit = base.audit_without_children(run_directory)
        fresh = synthetic_retry(run_directory)
        if (
            audit["status"] != "RETRYABLE_NONCLAIM"
            or fresh.get("attempt_number") != 2
        ):
            raise AssertionError(f"{stage} was not freshly retryable")
        unrecorded = [
            container
            for container in quarantines
            if not (container / "quarantine-record.json").exists()
        ]
        results[stage] = {
            "crash_observed": True,
            "child_launched": False,
            "terminal_checkpoint_absent_at_crash": True,
            "audit_after_crash": audit_after_crash,
            "retry_recovery_status": retry["status"],
            "canonical_recovery": canonical,
            "opaque_original_bytes_preserved": True,
            "quarantine_directory_count": len(quarantines),
            "unrecorded_quarantine_directory_count": len(unrecorded),
            "fresh_retry_attempt_number": fresh["attempt_number"],
        }
    return {
        "stage_count": len(results),
        "safe_retry_count": sum(
            1
            for item in results.values()
            if item["retry_recovery_status"] == "RETRYABLE_NONCLAIM"
            and item["opaque_original_bytes_preserved"] is True
        ),
        "process_crash_boundary": (
            "A process loss immediately after os.replace but before the "
            "quarantine record can leave an intact, unrecorded sibling "
            "quarantine directory. The main run remains a nonclaim and "
            "explicit recovery remains retryable. Hardware power-loss "
            "durability before the subsequent directory fsync was not "
            "simulated."
        ),
        "cases": results,
        "real_solver_or_checker_executions": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=REVIEW / "evidence_v3.json",
    )
    arguments = parser.parse_args()
    if arguments.output.parent.resolve() != REVIEW.resolve():
        raise ValueError("v3 evidence must be written in the review directory")
    frozen_before, preserved_before = verify_bound_bytes()

    with tempfile.TemporaryDirectory(
        prefix=".referee-v3-fixtures-", dir=REVIEW
    ) as temporary:
        foundation = base.Foundation(Path(temporary).resolve())
        tools = base.tool_evidence()
        with foundation.frozen_context():
            checks = {
                "pre_RUN_STARTED_crash_windows": (
                    case_pre_run_started_windows(foundation)
                ),
                "malformed_symlink_extra_orphans": (
                    case_malformed_orphans(foundation)
                ),
                "opaque_orphan_contents": (
                    case_opaque_orphan_contents(foundation)
                ),
                "pre_RUN_STARTED_orphan_after_RETRYABLE": (
                    case_orphan_after_retryable(foundation)
                ),
                "partial_and_complete_opaque_outcomes": (
                    case_opaque_outcomes(foundation)
                ),
                "crash_during_orphan_quarantine": (
                    case_orphan_quarantine_crash_safety(foundation)
                ),
                "crash_during_quarantine": (
                    case_quarantine_crash_safety(foundation)
                ),
                "positive_phase_records": prior.case_positive_phase_records(
                    foundation
                ),
                "readonly_complete_chain_audit": (
                    base.case_readonly_success(foundation)
                ),
                "sat_candidate_semantic_replay": prior.case_sat_semantic_replay(
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
                "ordinary_interruption_recovery_and_fresh_restart": (
                    base.case_recovery_and_restart(foundation)
                ),
                "malformed_metadata_v1_regressions": (
                    base.case_v1_malformed_metadata_regressions(foundation)
                ),
                "adjacent_output_crosslink_matrix": (
                    prior.case_output_crosslink_matrix(foundation)
                ),
            }
            repaired_findings = {
                "F1_attempt_formula_content_equality": (
                    prior.case_f1_attempt_formula(foundation)
                ),
                "F2_phase_input_output_crosslinks": (
                    prior.case_f2_phase_crosslinks(foundation)
                ),
                "F3_exact_certificate_and_details_shape": (
                    prior.case_f3_exact_claim_shapes(foundation)
                ),
                "F4_all_adjacent_interruption_windows": {
                    "pre_RUN_STARTED": checks[
                        "pre_RUN_STARTED_crash_windows"
                    ],
                    "partial_and_complete_outcomes": checks[
                        "partial_and_complete_opaque_outcomes"
                    ],
                    "crash_during_orphan_quarantine": checks[
                        "crash_during_orphan_quarantine"
                    ],
                    "crash_during_outcome_quarantine": checks[
                        "crash_during_quarantine"
                    ],
                },
            }

    frozen_after, preserved_after = verify_bound_bytes()
    if frozen_before != frozen_after or preserved_before != preserved_after:
        raise AssertionError("v3 replay changed frozen or preserved bytes")

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
        and checks[
            "pre_RUN_STARTED_crash_windows"
        ]["recovered_count"]
        == 4
        and checks[
            "pre_RUN_STARTED_crash_windows"
        ]["all_windows_claim_safe_and_freshly_retryable"]
        and checks[
            "partial_and_complete_opaque_outcomes"
        ]["recovered_count"]
        == 2
        and checks["crash_during_quarantine"]["safe_retry_count"] == 4
        and checks[
            "malformed_symlink_extra_orphans"
        ]["rejected_count"]
        == 6
        and checks[
            "opaque_orphan_contents"
        ]["fresh_retry_attempt_number"]
        == 1
        and checks[
            "pre_RUN_STARTED_orphan_after_RETRYABLE"
        ]["fresh_retry_attempt_number"]
        == 2
        and checks[
            "crash_during_orphan_quarantine"
        ]["safe_continuation_count"]
        == 3
        and checks[
            "malformed_metadata_v1_regressions"
        ]["rejected_count"]
        == 6
        and checks[
            "adjacent_output_crosslink_matrix"
        ]["rejected_count"]
        == 4
    )
    verdict = "ACCEPT" if required else "REJECT"
    if verdict != "ACCEPT":
        raise AssertionError("a decisive final-v3 requirement failed")

    evidence = {
        "schema": "order13-k3-production-independent-referee-evidence-v3",
        "verdict": verdict,
        "scope": (
            "Final-v3 frozen local bytes; synthetic fixtures only; no real "
            "SAT solver or proof checker executed."
        ),
        "final_frozen_file_sha256": frozen_after,
        "preserved_v1_v2_artifact_sha256": preserved_after,
        "tool_evidence": tools,
        "checks": checks,
        "repaired_findings": repaired_findings,
        "quarantine_crash_observation": (
            "All injected process-loss prefixes remained nonclaims and were "
            "explicitly recoverable on retry. A loss after rename but before "
            "record creation can leave preserved bytes in an unrecorded "
            "sibling quarantine; it cannot promote a claim or block recovery."
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
