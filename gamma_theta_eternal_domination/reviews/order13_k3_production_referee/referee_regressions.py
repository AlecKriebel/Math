#!/usr/bin/env python3
"""Independent synthetic referee checks for the frozen production workflow.

The fixtures bind executable-looking plain-text files, but never execute a SAT
solver or proof checker.  Successful child records are supplied by an in-process
deterministic stub.  All temporary state is created below this review folder.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import signal
import stat
import sys
import tempfile
from contextlib import contextmanager
from dataclasses import asdict
from pathlib import Path
from typing import Callable, Iterator, Mapping
from unittest.mock import patch


REVIEW = Path(__file__).resolve().parent
CAMPAIGN = REVIEW.parents[1]
SOURCE = CAMPAIGN / "src/search/order13_k3"
TESTS = CAMPAIGN / "tests"

FROZEN_FILES = {
    SOURCE / "production.py": (
        "38beae789c25228f2411463f004645711821d340c16c6020fe22d2157b7de142"
    ),
    SOURCE / "normalize_bdrat.py": (
        "a09f67d39932b6c3bb19b31a0792e4f47f515820c642e9418d3e374f555de18c"
    ),
    SOURCE / "PRODUCTION_PROTOCOL.md": (
        "077b3328da5eab7645bafde079e0334c09b0e696179c9df893a0364a2d053de8"
    ),
    TESTS / "test_order13_k3_production.py": (
        "46c8574a7a16a605784a24e8f8351b770e8e06ffd9202cd20b57f21ef5bb414a"
    ),
}

sys.path.insert(0, str(CAMPAIGN / "src"))

from search.order13_k3 import production as production  # noqa: E402
from search.order13_k3.generate import (  # noqa: E402
    canonical_json_bytes,
    generate_package,
)
from search.order13_k3.normalize_bdrat import (  # noqa: E402
    NormalizationError,
    normalize_binary_drat,
)
from synthesis_k3.cegar import ChildResult, _command_sha256  # noqa: E402


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path.name} is not an object")
    return value


def write_json(path: Path, value: object) -> None:
    path.write_bytes(canonical_json_bytes(value))


def limits() -> dict[str, object]:
    return {
        "solver_wall_seconds": 2,
        "postprocess_wall_seconds": 2,
        "solver_memory_mib": 64,
        "postprocess_memory_mib": 64,
        "file_limit_mib": 64,
        "disk_reserve_mib": 8192,
        "memory_reserve_mib": 512,
        "load_max": 1000.0,
        "parallel_children": 1,
    }


class Foundation:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.mirror = root / "campaign-mirror"
        self.runs = self.mirror / "runs"
        self.runs.mkdir(parents=True)
        for relative in production.RUNTIME_SOURCE_RELATIVE_PATHS:
            source = CAMPAIGN / relative
            destination = self.mirror / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)

        self.package = root / "package"
        generate_package(
            template="hole11",
            output_directory=self.package,
            validation_gate=True,
        )
        self.tools: dict[str, Path] = {}
        for role, filename in (
            ("cadical", "synthetic-cadical"),
            ("drat_trim", "synthetic-drat-trim"),
            ("lrat_check", "synthetic-lrat-check"),
        ):
            path = root / filename
            path.write_bytes((filename + "\n").encode("ascii"))
            path.chmod(0o700)
            self.tools[role] = path
        self.tools["normalizer_python"] = Path(sys.executable).resolve()
        self.policy = {
            role: sha256(self.tools[role])
            for role in ("cadical", "drat_trim", "lrat_check")
        }

    @contextmanager
    def frozen_context(self) -> Iterator[None]:
        with patch.dict(
            production.ACCEPTED_TOOL_SHA256, self.policy, clear=True
        ), patch.object(
            production, "campaign_root", return_value=self.mirror
        ):
            yield

    def initialize(self, name: str) -> Path:
        run_directory = self.runs / name
        production.initialize(
            package_directory=self.package,
            run_directory=run_directory,
            cadical_path=self.tools["cadical"],
            drat_trim_path=self.tools["drat_trim"],
            lrat_check_path=self.tools["lrat_check"],
            normalizer_python_path=self.tools["normalizer_python"],
            seed=0,
            limits=limits(),
            validation_gate=True,
        )
        return run_directory


def clean_resource_report(
    run_directory: Path,
    phase: str,
    memory_mib: int,
    phase_limits: Mapping[str, object],
) -> dict[str, object]:
    del run_directory
    required_memory = (
        memory_mib + int(phase_limits["memory_reserve_mib"])
    ) << 20
    required_disk = (
        int(phase_limits["disk_reserve_mib"])
        + production.LIVE_FILE_SLOTS * int(phase_limits["file_limit_mib"])
        + production.DISK_METADATA_MIB
    ) << 20
    return {
        "schema": "gamma-theta-order13-k3-resource-gate-v1",
        "phase": phase,
        "checked_unix_ns": 1,
        "load_average_one_minute": 0.0,
        "load_ceiling": phase_limits["load_max"],
        "available_memory_bytes": required_memory,
        "required_memory_bytes": required_memory,
        "free_disk_bytes": required_disk,
        "required_free_disk_bytes": required_disk,
        "live_file_slots": production.LIVE_FILE_SLOTS,
        "probe_errors": [],
        "checks": {"load": True, "memory": True, "disk": True},
        "passed": True,
    }


def failed_resource_report(
    run_directory: Path,
    phase: str,
    memory_mib: int,
    phase_limits: Mapping[str, object],
) -> dict[str, object]:
    report = clean_resource_report(
        run_directory, phase, memory_mib, phase_limits
    )
    report["available_memory_bytes"] = 1
    report["checks"] = {"load": True, "memory": False, "disk": True}
    report["passed"] = False
    return report


class SyntheticChildren:
    def __init__(self, *, timeout: bool = False) -> None:
        self.timeout = timeout
        self.phases: list[str] = []

    def __call__(self, **keywords: object) -> ChildResult:
        command = tuple(str(item) for item in keywords["command"])
        stdout = Path(str(keywords["stdout_path"]))
        stderr = Path(str(keywords["stderr_path"]))
        phase = stdout.name.removesuffix(".stdout")
        self.phases.append(phase)
        stdout.write_bytes(b"")
        stderr.write_bytes(b"")

        exit_code = 0
        termination_signal: int | None = None
        timed_out = False
        if self.timeout:
            if phase != "solver" or len(self.phases) != 1:
                raise AssertionError("timeout stub may only run once")
            exit_code = -int(signal.SIGTERM)
            termination_signal = int(signal.SIGTERM)
            timed_out = True
        elif phase == "solver":
            exit_code = 20
            Path(command[command.index("-w") + 1]).write_bytes(
                b"s UNSATISFIABLE\n"
            )
            Path(command[-1]).write_bytes(b"a\x00")
        elif phase == "normalizer":
            normalize_binary_drat(
                Path(command[command.index("--input") + 1]),
                Path(command[command.index("--output") + 1]),
                Path(command[command.index("--report") + 1]),
                max_variable=int(
                    command[command.index("--max-variable") + 1]
                ),
            )
            stdout.write_bytes(b"s NORMALIZED\n")
        elif phase == "lrat_conversion":
            Path(command[command.index("-L") + 1]).write_bytes(b"1 0 0\n")
            stdout.write_bytes(b"s VERIFIED\n")
        elif phase == "lrat_check":
            stdout.write_bytes(b"c VERIFIED\n")
        else:
            stdout.write_bytes(b"s VERIFIED\n")

        executable_hash = sha256(Path(command[0]))
        return ChildResult(
            command=command,
            command_sha256=_command_sha256(command),
            executable_sha256_before=executable_hash,
            executable_sha256_after=executable_hash,
            exit_code=exit_code,
            termination_signal=termination_signal,
            timed_out=timed_out,
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
            wall_limit_seconds=int(keywords["wall_limit_seconds"]),
            memory_limit_mib=int(keywords["memory_limit_mib"]),
            file_limit_mib=int(keywords["file_limit_mib"]),
            stdout_path=str(stdout.resolve()),
            stdout_sha256=sha256(stdout),
            stderr_path=str(stderr.resolve()),
            stderr_sha256=sha256(stderr),
        )


def run_success(run_directory: Path) -> tuple[dict[str, object], list[str]]:
    children = SyntheticChildren()
    with patch.object(
        production, "_resource_report", side_effect=clean_resource_report
    ), patch.object(
        production, "run_bounded_child", side_effect=children
    ):
        result = production.run(
            run_directory,
            production_gate=True,
            recover_interrupted=False,
        )
    if result["status"] != production.FINAL_SUCCESS:
        raise AssertionError("synthetic complete chain did not finish")
    return result, children.phases


def run_timeout(run_directory: Path) -> tuple[dict[str, object], int]:
    children = SyntheticChildren(timeout=True)
    with patch.object(
        production, "_resource_report", side_effect=clean_resource_report
    ), patch.object(
        production, "run_bounded_child", side_effect=children
    ):
        result = production.run(
            run_directory,
            production_gate=True,
            recover_interrupted=False,
        )
    return result, len(children.phases)


def tree_digest(run_directory: Path) -> dict[str, tuple[str, int, int]]:
    result: dict[str, tuple[str, int, int]] = {}
    for path in sorted(run_directory.rglob("*")):
        relative = path.relative_to(run_directory).as_posix()
        information = path.lstat()
        if stat.S_ISREG(information.st_mode):
            result[relative] = (
                sha256(path),
                information.st_size,
                stat.S_IMODE(information.st_mode),
            )
        elif stat.S_ISDIR(information.st_mode):
            result[relative + "/"] = ("directory", 0, stat.S_IMODE(information.st_mode))
        else:
            result[relative] = ("nonregular", information.st_size, 0)
    return result


def audit_without_children(run_directory: Path) -> dict[str, object]:
    with patch.object(
        production,
        "run_bounded_child",
        side_effect=AssertionError("read-only audit attempted a child"),
    ) as child:
        report = production.audit(run_directory)
    if child.call_count != 0:
        raise AssertionError("read-only audit invoked the child launcher")
    return report


def refresh_success_metadata(run_directory: Path) -> None:
    attempt = run_directory / "attempts/attempt-000001"
    config_path = attempt / "attempt-config.json"
    certificate_path = attempt / "certificate.json"
    outcome_path = attempt / "outcome.json"

    outcome = read_json(outcome_path)
    certificate = read_json(certificate_path)
    outcome["details"] = {"certificate": certificate}
    outcome["artifacts"] = production._attempt_artifacts(attempt)
    write_json(outcome_path, outcome)

    checkpoint_one_path = (
        run_directory / "checkpoints/checkpoint-000001.json"
    )
    checkpoint_one = read_json(checkpoint_one_path)
    checkpoint_one["attempt"] = production._binding(
        config_path, "refreshed attempt config"
    )
    write_json(checkpoint_one_path, checkpoint_one)

    checkpoint_two_path = (
        run_directory / "checkpoints/checkpoint-000002.json"
    )
    checkpoint_two = read_json(checkpoint_two_path)
    checkpoint_two["previous_checkpoint_sha256"] = sha256(
        checkpoint_one_path
    )
    checkpoint_two["attempt"] = production._binding(
        config_path, "refreshed attempt config"
    )
    checkpoint_two["outcome"] = production._binding(
        outcome_path, "refreshed attempt outcome"
    )
    write_json(checkpoint_two_path, checkpoint_two)


def create_running_attempt(
    run_directory: Path,
) -> tuple[
    dict[str, object],
    str,
    Path,
    dict[str, object],
    str,
    dict[str, object],
]:
    manifest, manifest_hash, latest, latest_hash = production._load_run(
        run_directory
    )
    attempt = run_directory / "attempts/attempt-000001"
    attempt.mkdir()
    shutil.copyfile(
        run_directory / production.INSTANCE_NAME,
        attempt / production.INSTANCE_NAME,
    )
    config = {
        "schema": "gamma-theta-order13-k3-attempt-config-v1",
        "schema_version": 1,
        "claim_status": "NO_SAT_OR_UNSAT_CLAIM_BEFORE_EXECUTION",
        "proof_pipeline": manifest["proof_pipeline"],
        "attempt_number": 1,
        "template": manifest["template"],
        "seed": manifest["seed"],
        "run_manifest_sha256": manifest_hash,
        "instance": production._binding(
            attempt / production.INSTANCE_NAME, "attempt instance"
        ),
        "runtime_source_set_sha256": manifest[
            "runtime_source_set_sha256"
        ],
        "tools": manifest["tools"],
        "limits": manifest["limits"],
        "commands": production._commands(manifest, attempt),
        "created_unix_ns": 1,
    }
    config_path = attempt / "attempt-config.json"
    write_json(config_path, config)
    running, running_hash = production._append_checkpoint(
        run_directory,
        manifest_hash=manifest_hash,
        previous_hash=latest_hash,
        previous=latest,
        status="RUNNING_UNFINISHED_NONCLAIM",
        event="RUN_STARTED",
        attempt_binding=production._binding(config_path, "attempt config"),
        outcome_binding=None,
    )
    return (
        manifest,
        manifest_hash,
        attempt,
        running,
        running_hash,
        config,
    )


def append_terminal(
    run_directory: Path,
    manifest_hash: str,
    running: Mapping[str, object],
    running_hash: str,
    attempt: Path,
    *,
    status: str,
    event: str,
    outcome: Mapping[str, object],
) -> None:
    outcome_path = attempt / "outcome.json"
    write_json(outcome_path, outcome)
    production._append_checkpoint(
        run_directory,
        manifest_hash=manifest_hash,
        previous_hash=running_hash,
        previous=running,
        status=status,
        event=event,
        attempt_binding=production._binding(
            attempt / "attempt-config.json", "attempt config"
        ),
        outcome_binding=production._binding(outcome_path, "attempt outcome"),
    )


def expect_rejection(
    action: Callable[[], object],
    expected_fragment: str,
) -> dict[str, object]:
    try:
        action()
    except Exception as error:
        if expected_fragment not in str(error):
            raise AssertionError(
                f"wrong rejection {type(error).__name__}: {error}"
            ) from error
        return {
            "rejected": True,
            "exception_type": type(error).__name__,
            "stable_message_fragment": expected_fragment,
        }
    raise AssertionError(f"fixture was accepted; expected {expected_fragment!r}")


def case_readonly_success(foundation: Foundation) -> dict[str, object]:
    run_directory = foundation.initialize("readonly-success")
    result, phases = run_success(run_directory)
    before = tree_digest(run_directory)
    report = audit_without_children(run_directory)
    after = tree_digest(run_directory)
    if before != after:
        raise AssertionError("audit changed durable run bytes or modes")
    if report["proof_freshly_replayed"] is not False:
        raise AssertionError("audit overstated fresh proof replay")
    expected_phases = [
        "solver",
        "raw_forward",
        "normalizer",
        "normalized_forward",
        "lrat_conversion",
        "lrat_check",
    ]
    if phases != expected_phases:
        raise AssertionError("synthetic phase order differs")
    return {
        "accepted": report["accepted"],
        "status": report["status"],
        "proof_freshly_replayed": report["proof_freshly_replayed"],
        "durable_tree_unchanged": before == after,
        "synthetic_child_phases": phases,
        "real_solver_or_checker_executions": 0,
        "run_result_status": result["status"],
    }


def case_attempt_instance_substitution(
    foundation: Foundation,
) -> dict[str, object]:
    run_directory = foundation.initialize("attempt-instance-substitution")
    run_success(run_directory)
    attempt = run_directory / "attempts/attempt-000001"
    instance = attempt / production.INSTANCE_NAME
    instance.write_bytes(b"p cnf 1 2\n1 0\n-1 0\n")
    config_path = attempt / "attempt-config.json"
    config = read_json(config_path)
    config["instance"] = production._binding(
        instance, "substituted attempt instance"
    )
    write_json(config_path, config)
    certificate_path = attempt / "certificate.json"
    certificate = read_json(certificate_path)
    certificate["instance"] = production._binding(
        instance, "substituted certificate instance"
    )
    write_json(certificate_path, certificate)
    refresh_success_metadata(run_directory)
    report = audit_without_children(run_directory)
    run_instance = run_directory / production.INSTANCE_NAME
    if sha256(instance) == sha256(run_instance):
        raise AssertionError("instance substitution did not change bytes")
    return {
        "accepted_after_substitution": report["accepted"],
        "reported_status": report["status"],
        "attempt_instance_equals_frozen_run_instance": False,
        "substituted_instance_sha256": sha256(instance),
        "frozen_run_instance_sha256": sha256(run_instance),
        "real_solver_or_checker_executions": 0,
    }


def case_checked_lrat_substitution(foundation: Foundation) -> dict[str, object]:
    run_directory = foundation.initialize("checked-lrat-substitution")
    run_success(run_directory)
    attempt = run_directory / "attempts/attempt-000001"
    lrat = attempt / "proof.converted.lrat"
    before = sha256(lrat)
    lrat.write_bytes(b"not an LRAT proof\n")
    certificate_path = attempt / "certificate.json"
    certificate = read_json(certificate_path)
    certificate["converted_lrat"] = production._binding(
        lrat, "post-check substituted LRAT"
    )
    write_json(certificate_path, certificate)
    refresh_success_metadata(run_directory)
    report = audit_without_children(run_directory)
    return {
        "accepted_after_substitution": report["accepted"],
        "reported_status": report["status"],
        "lrat_sha256_changed_after_recorded_check": before != sha256(lrat),
        "substituted_lrat_sha256": sha256(lrat),
        "child_record_binds_lrat_sha256": False,
        "real_solver_or_checker_executions": 0,
    }


def case_certificate_claim_injection(
    foundation: Foundation,
) -> dict[str, object]:
    run_directory = foundation.initialize("certificate-claim-injection")
    run_success(run_directory)
    attempt = run_directory / "attempts/attempt-000001"
    certificate_path = attempt / "certificate.json"
    certificate = read_json(certificate_path)
    certificate["asserted_global_order13_exclusion"] = True
    certificate["claim_boundary"] = (
        "Fresh independent replay and all-template coverage complete."
    )
    write_json(certificate_path, certificate)
    refresh_success_metadata(run_directory)
    report = audit_without_children(run_directory)
    return {
        "accepted_after_extra_claim_metadata": report["accepted"],
        "audit_report_proof_freshly_replayed": report[
            "proof_freshly_replayed"
        ],
        "certificate_extra_claim_preserved": True,
        "real_solver_or_checker_executions": 0,
    }


def case_sat_semantic_replay(foundation: Foundation) -> dict[str, object]:
    run_directory = foundation.initialize("sat-semantic-replay")
    (
        manifest,
        manifest_hash,
        attempt,
        running,
        running_hash,
        config,
    ) = create_running_attempt(run_directory)
    variable_count = int(manifest["expected_formula"]["variables"])
    model = {variable: False for variable in range(1, variable_count + 1)}
    solver_result = attempt / "solver.result"
    solver_result.write_bytes(
        (
            "s SATISFIABLE\nv "
            + " ".join(f"-{variable}" for variable in range(1, variable_count + 1))
            + " 0\n"
        ).encode("ascii")
    )
    resource = clean_resource_report(
        run_directory, "solver", int(limits()["solver_memory_mib"]), limits()
    )
    write_json(attempt / "resource-solver.json", resource)
    stdout = attempt / "solver.stdout"
    stderr = attempt / "solver.stderr"
    stdout.write_bytes(b"")
    stderr.write_bytes(b"")
    command = tuple(config["commands"]["solver"])
    executable_hash = sha256(Path(command[0]))
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
        wall_limit_seconds=int(limits()["solver_wall_seconds"]),
        memory_limit_mib=int(limits()["solver_memory_mib"]),
        file_limit_mib=int(limits()["file_limit_mib"]),
        stdout_path=str(stdout.resolve()),
        stdout_sha256=sha256(stdout),
        stderr_path=str(stderr.resolve()),
        stderr_sha256=sha256(stderr),
    )
    write_json(attempt / "child-solver.json", asdict(child))
    assignment = canonical_json_bytes(
        [-variable for variable in range(1, variable_count + 1)]
    )
    candidate = {
        "schema": "gamma-theta-order13-k3-sat-candidate-v1",
        "schema_version": 1,
        "status": production.SAT_CANDIDATE,
        "template": manifest["template"],
        "instance": production._binding(
            attempt / production.INSTANCE_NAME, "SAT candidate instance"
        ),
        "solver_result": production._binding(
            solver_result, "SAT solver result"
        ),
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
    append_terminal(
        run_directory,
        manifest_hash,
        running,
        running_hash,
        attempt,
        status=production.SAT_CANDIDATE,
        event="RUN_FINISHED",
        outcome=outcome,
    )
    cnf_rejection = expect_rejection(
        lambda: audit_without_children(run_directory),
        "model falsifies CNF clause",
    )
    with patch.object(
        production, "validate_model_satisfies_cnf", return_value=None
    ):
        semantic_rejection = expect_rejection(
            lambda: audit_without_children(run_directory),
            "eternal family is empty",
        )
    return {
        "complete_assignment_replayed_against_frozen_cnf": cnf_rejection[
            "rejected"
        ],
        "direct_graph_game_semantics_replayed": semantic_rejection["rejected"],
        "cnf_rejection": cnf_rejection,
        "semantic_rejection_after_cnf_stage_instrumented": semantic_rejection,
        "real_solver_or_checker_executions": 0,
    }


def case_resource_limits(foundation: Foundation) -> dict[str, object]:
    invalid: list[tuple[str, dict[str, object]]] = []
    for name, key, value in (
        ("solver_memory_ceiling", "solver_memory_mib", 2049),
        ("postprocess_memory_ceiling", "postprocess_memory_mib", 2049),
        ("file_ceiling", "file_limit_mib", 2049),
        ("disk_reserve_floor", "disk_reserve_mib", 8191),
        ("wall_ceiling", "solver_wall_seconds", 21601),
        ("parallel_count", "parallel_children", 2),
    ):
        mutated = limits()
        mutated[key] = value
        invalid.append((name, mutated))
    rejected = {}
    for name, mutated in invalid:
        rejected[name] = expect_rejection(
            lambda candidate=mutated: production._validate_limits(candidate),
            "resource limits violate production ceilings",
        )["rejected"]

    run_directory = foundation.initialize("resource-gate-refusal")
    with patch.object(
        production, "_resource_report", side_effect=failed_resource_report
    ), patch.object(
        production,
        "run_bounded_child",
        side_effect=AssertionError("failed resource gate launched a child"),
    ) as child:
        result = production.run(
            run_directory,
            production_gate=True,
            recover_interrupted=False,
        )
    if child.call_count != 0:
        raise AssertionError("failed resource gate launched a child")
    return {
        "invalid_limit_cases_rejected": rejected,
        "failed_gate_status": result["status"],
        "failed_gate_child_launched": result["child_launched"],
        "real_solver_or_checker_executions": 0,
    }


def case_runtime_source_binding(foundation: Foundation) -> dict[str, object]:
    run_directory = foundation.initialize("runtime-source-binding")
    source = foundation.mirror / "src/synthesis_k3/encoding.py"
    original = source.read_bytes()
    source.write_bytes(original + b"\n")
    audit_rejection = expect_rejection(
        lambda: audit_without_children(run_directory),
        "runtime source bindings differ from initialized bytes",
    )
    with patch.object(
        production,
        "run_bounded_child",
        side_effect=AssertionError("source mismatch launched a child"),
    ) as child:
        run_rejection = expect_rejection(
            lambda: production.run(
                run_directory,
                production_gate=True,
                recover_interrupted=False,
            ),
            "runtime source bindings differ from initialized bytes",
        )
    if child.call_count != 0:
        raise AssertionError("source mismatch launched a child")
    source.write_bytes(original)
    restored = audit_without_children(run_directory)
    return {
        "audit_rejected_source_mutation": audit_rejection["rejected"],
        "run_rejected_before_child": run_rejection["rejected"],
        "restored_bytes_audit_accepted": restored["accepted"],
        "real_solver_or_checker_executions": 0,
    }


def case_normalization(foundation: Foundation) -> dict[str, object]:
    directory = foundation.root / "normalization"
    directory.mkdir()
    source = directory / "raw.bdrat"
    output = directory / "normalized.bdrat"
    report = directory / "report.json"
    source.write_bytes(b"a\x04\x00d\x04\x00a\x00d\x04\x00")
    normalized_report = normalize_binary_drat(
        source, output, report, max_variable=20
    )
    if output.read_bytes() != b"a\x04\x00a\x00":
        raise AssertionError("normalizer did not emit the exact addition stream")

    malformed = (
        b"",
        b"a\x04\x00",
        b"a\x00a\x00",
        b"a\x00a\x04\x00",
        b"d\x00a\x00",
        b"a\x04",
        b"x\x00",
        b"a\x80\x00",
        b"a\x01\x00",
        b"a\x2a\x00a\x00",
    )
    rejected = 0
    for index, payload in enumerate(malformed):
        bad = directory / f"bad-{index}.bdrat"
        bad_output = directory / f"bad-{index}.normalized"
        bad_report = directory / f"bad-{index}.json"
        bad.write_bytes(payload)
        try:
            normalize_binary_drat(
                bad, bad_output, bad_report, max_variable=20
            )
        except NormalizationError:
            rejected += 1
        else:
            raise AssertionError(f"malformed normalization case {index} accepted")
        if bad_output.exists() or bad_report.exists():
            raise AssertionError("failed normalization retained partial output")
    return {
        "exact_addition_stream": output.read_bytes().hex(),
        "input_record_counts": normalized_report["record_counts"],
        "malformed_case_count": len(malformed),
        "malformed_cases_rejected": rejected,
        "failed_cases_left_no_outputs": True,
        "real_solver_or_checker_executions": 0,
    }


def case_recovery_and_restart(foundation: Foundation) -> dict[str, object]:
    run_directory = foundation.initialize("recovery-and-restart")
    create_running_attempt(run_directory)
    no_flag = expect_rejection(
        lambda: production.run(
            run_directory,
            production_gate=True,
            recover_interrupted=False,
        ),
        "interrupted attempt requires --recover-interrupted",
    )
    recovered = production.run(
        run_directory,
        production_gate=True,
        recover_interrupted=True,
    )
    retry, child_calls = run_timeout(run_directory)
    report = audit_without_children(run_directory)
    return {
        "silent_resume_rejected": no_flag["rejected"],
        "recovery_status": recovered["status"],
        "recovery_child_launched": recovered["child_launched"],
        "fresh_retry_attempt_number": retry["attempt_number"],
        "fresh_retry_status": retry["status"],
        "synthetic_retry_child_calls": child_calls,
        "audited_attempt_count": report["attempt_count"],
        "real_solver_or_checker_executions": 0,
    }


def case_outcome_checkpoint_interruption(
    foundation: Foundation,
) -> dict[str, object]:
    run_directory = foundation.initialize("outcome-checkpoint-interruption")
    (
        _,
        _,
        attempt,
        _,
        _,
        _,
    ) = create_running_attempt(run_directory)
    outcome = {
        "schema": "gamma-theta-order13-k3-attempt-outcome-v1",
        "schema_version": 1,
        "status": "RETRYABLE_NONCLAIM",
        "claim_status": "NO_SAT_OR_UNSAT_CLAIM",
        "details": {
            "phase_status": "SYNTHETIC_INTERRUPTION_NONCLAIM",
            "phase_details": {},
        },
        "artifacts": production._attempt_artifacts(attempt),
        "finished_unix_ns": 2,
    }
    write_json(attempt / "outcome.json", outcome)
    recovery = expect_rejection(
        lambda: production.run(
            run_directory,
            production_gate=True,
            recover_interrupted=True,
        ),
        "running attempt unexpectedly has an outcome",
    )
    return {
        "durable_outcome_exists_without_terminal_checkpoint": True,
        "explicit_recovery_rejected": recovery["rejected"],
        "rejection": recovery,
        "real_solver_or_checker_executions": 0,
    }


def v1_external_checkpoint(foundation: Foundation) -> dict[str, object]:
    run_directory = foundation.initialize("v1-external-checkpoint")
    _, manifest_hash, latest, latest_hash = production._load_run(run_directory)
    external_config = foundation.root / "external-config.json"
    external_outcome = foundation.root / "external-outcome.json"
    write_json(external_config, {"external": True})
    write_json(external_outcome, {"status": production.FINAL_SUCCESS})
    running, running_hash = production._append_checkpoint(
        run_directory,
        manifest_hash=manifest_hash,
        previous_hash=latest_hash,
        previous=latest,
        status="RUNNING_UNFINISHED_NONCLAIM",
        event="RUN_STARTED",
        attempt_binding=production._binding(
            external_config, "external config"
        ),
        outcome_binding=None,
    )
    production._append_checkpoint(
        run_directory,
        manifest_hash=manifest_hash,
        previous_hash=running_hash,
        previous=running,
        status=production.FINAL_SUCCESS,
        event="RUN_FINISHED",
        attempt_binding=production._binding(
            external_config, "external config"
        ),
        outcome_binding=production._binding(
            external_outcome, "external outcome"
        ),
    )
    return expect_rejection(
        lambda: audit_without_children(run_directory),
        "path is not the canonical run-local path",
    )


def rebind_manifest_tool(
    run_directory: Path,
    role: str,
    replacement: Path,
) -> None:
    manifest_path = run_directory / production.RUN_MANIFEST_NAME
    manifest = read_json(manifest_path)
    tools = manifest["tools"]
    tools[role] = production._tool_binding(
        replacement, f"replacement {role}"
    )
    manifest["tool_identity"] = production._tool_identity(tools)
    write_json(manifest_path, manifest)
    checkpoint_path = (
        run_directory / "checkpoints/checkpoint-000000.json"
    )
    checkpoint = read_json(checkpoint_path)
    checkpoint["run_manifest_sha256"] = sha256(manifest_path)
    write_json(checkpoint_path, checkpoint)


def v1_tool_rebinding(
    foundation: Foundation,
    role: str,
) -> dict[str, object]:
    run_directory = foundation.initialize(f"v1-rebind-{role}")
    replacement = foundation.root / f"replacement-{role}"
    replacement.write_bytes(f"replacement {role}\n".encode("ascii"))
    replacement.chmod(0o700)
    rebind_manifest_tool(run_directory, role, replacement)
    expected = (
        f"{role} binding is not linked to its accepted hash"
        if role != "normalizer_python"
        else "normalizer Python is not the current bound interpreter"
    )
    return expect_rejection(
        lambda: audit_without_children(run_directory), expected
    )


def v1_claim_label(foundation: Foundation) -> dict[str, object]:
    run_directory = foundation.initialize("v1-claim-label")
    run_timeout(run_directory)
    attempt = run_directory / "attempts/attempt-000001"
    outcome_path = attempt / "outcome.json"
    outcome = read_json(outcome_path)
    outcome["claim_status"] = "FORMULA_UNSAT_AFTER_COMPLETE_LRAT_REPLAY"
    write_json(outcome_path, outcome)
    checkpoint_path = (
        run_directory / "checkpoints/checkpoint-000002.json"
    )
    checkpoint = read_json(checkpoint_path)
    checkpoint["outcome"] = production._binding(
        outcome_path, "mutated retryable outcome"
    )
    write_json(checkpoint_path, checkpoint)
    return expect_rejection(
        lambda: audit_without_children(run_directory),
        "attempt outcome semantics differ",
    )


def v1_sat_metadata(foundation: Foundation) -> dict[str, object]:
    run_directory = foundation.initialize("v1-sat-metadata")
    (
        _,
        manifest_hash,
        attempt,
        running,
        running_hash,
        _,
    ) = create_running_attempt(run_directory)
    candidate = {
        "schema": "malformed-synthetic-candidate",
        "status": production.SAT_CANDIDATE,
        "assignment_sha256": "0" * 64,
        "h_edges": [],
        "eternal_family": [],
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
    append_terminal(
        run_directory,
        manifest_hash,
        running,
        running_hash,
        attempt,
        status=production.SAT_CANDIDATE,
        event="RUN_FINISHED",
        outcome=outcome,
    )
    return expect_rejection(
        lambda: audit_without_children(run_directory),
        "SAT candidate bindings or header differ",
    )


def v1_recovery_promotion(foundation: Foundation) -> dict[str, object]:
    run_directory = foundation.initialize("v1-recovery-promotion")
    (
        _,
        manifest_hash,
        attempt,
        running,
        running_hash,
        _,
    ) = create_running_attempt(run_directory)
    outcome = {
        "schema": "gamma-theta-order13-k3-attempt-outcome-v1",
        "schema_version": 1,
        "status": production.RECOVERED_OUTCOME_STATUS,
        "claim_status": "NO_SAT_OR_UNSAT_CLAIM",
        "reason": production.RECOVERY_REASON,
        "artifacts": production._attempt_artifacts(attempt),
        "finished_unix_ns": 2,
    }
    append_terminal(
        run_directory,
        manifest_hash,
        running,
        running_hash,
        attempt,
        status=production.FINAL_SUCCESS,
        event="INTERRUPTED_RECOVERED",
        outcome=outcome,
    )
    return expect_rejection(
        lambda: audit_without_children(run_directory),
        "recovery checkpoint transition differs",
    )


def case_v1_malformed_metadata_regressions(
    foundation: Foundation,
) -> dict[str, object]:
    cases = {
        "external_checkpoint_path_and_count": v1_external_checkpoint(
            foundation
        ),
        "cadical_binding_not_linked_to_policy": v1_tool_rebinding(
            foundation, "cadical"
        ),
        "normalizer_python_not_current_interpreter": v1_tool_rebinding(
            foundation, "normalizer_python"
        ),
        "retryable_claim_label": v1_claim_label(foundation),
        "sat_candidate_metadata_and_semantics": v1_sat_metadata(foundation),
        "interrupted_recovery_status_promotion": v1_recovery_promotion(
            foundation
        ),
    }
    if not all(case["rejected"] is True for case in cases.values()):
        raise AssertionError("a malformed-metadata v1 regression was accepted")
    return {
        "neutral_classification": "malformed-metadata regression cases",
        "case_count": len(cases),
        "rejected_count": sum(
            1 for case in cases.values() if case["rejected"] is True
        ),
        "cases": cases,
        "real_solver_or_checker_executions": 0,
    }


def tool_evidence() -> dict[str, object]:
    binaries = {
        "cadical": CAMPAIGN / "tools/cadical_3_0_1/build/cadical",
        "drat_trim": CAMPAIGN / "tools/drat_trim_2023_05_22/drat-trim",
        "lrat_check": CAMPAIGN / "tools/drat_trim_2023_05_22/lrat-check",
    }
    archives = {
        "cadical": CAMPAIGN / "tools/cadical_3_0_1.tar.gz",
        "drat_trim_lrat_check": (
            CAMPAIGN / "tools/drat_trim_2023_05_22.tar.gz"
        ),
    }
    binary_hashes = {role: sha256(path) for role, path in binaries.items()}
    if binary_hashes != dict(production.ACCEPTED_TOOL_SHA256):
        raise AssertionError("pinned executable hashes differ")
    if len({path.resolve() for path in binaries.values()}) != 3:
        raise AssertionError("pinned executable roles are not distinct")
    expected_archives = {
        "cadical": (
            "2dccd6ecc1878348dd70194d51df6b69006bf86439b5b3c395a5c5dd8863201e"
        ),
        "drat_trim_lrat_check": (
            "2ac28cd9e38e050b4f78fbff0efd4a1aa2349d157aef08c9b1fb6c7139949108"
        ),
    }
    archive_hashes = {role: sha256(path) for role, path in archives.items()}
    if archive_hashes != expected_archives:
        raise AssertionError("pinned source archive hashes differ")
    return {
        "binary_sha256": binary_hashes,
        "source_archive_sha256": archive_hashes,
        "distinct_single_link_executable_roles": all(
            path.stat().st_nlink == 1 and os.access(path, os.X_OK)
            for path in binaries.values()
        ),
        "frozen_human_identity": production.FROZEN_TOOL_IDENTITY,
        "normalizer_python_current_interpreter_relation_enforced": True,
        "executables_invoked": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=REVIEW / "evidence.json",
    )
    arguments = parser.parse_args()
    if arguments.output.parent.resolve() != REVIEW.resolve():
        raise ValueError("evidence output must be directly in the review folder")

    observed_frozen = {str(path.relative_to(CAMPAIGN)): sha256(path) for path in FROZEN_FILES}
    expected_frozen = {
        str(path.relative_to(CAMPAIGN)): digest
        for path, digest in FROZEN_FILES.items()
    }
    if observed_frozen != expected_frozen:
        raise AssertionError("frozen review bytes changed")

    with tempfile.TemporaryDirectory(
        prefix=".referee-fixtures-", dir=REVIEW
    ) as temporary:
        foundation = Foundation(Path(temporary).resolve())
        tools = tool_evidence()
        with foundation.frozen_context():
            checks = {
                "readonly_complete_chain_audit": case_readonly_success(
                    foundation
                ),
                "sat_candidate_semantic_replay": case_sat_semantic_replay(
                    foundation
                ),
                "resource_limits_and_prelaunch_gate": case_resource_limits(
                    foundation
                ),
                "runtime_source_binding": case_runtime_source_binding(
                    foundation
                ),
                "binary_proof_normalization": case_normalization(foundation),
                "interruption_recovery_and_fresh_restart": (
                    case_recovery_and_restart(foundation)
                ),
                "malformed_metadata_v1_regressions": (
                    case_v1_malformed_metadata_regressions(foundation)
                ),
            }
            findings = {
                "F1_attempt_instance_not_bound_to_frozen_run_instance": (
                    case_attempt_instance_substitution(foundation)
                ),
                "F2_lrat_bytes_not_bound_to_recorded_checker_child": (
                    case_checked_lrat_substitution(foundation)
                ),
                "F3_success_certificate_accepts_extra_claim_metadata": (
                    case_certificate_claim_injection(foundation)
                ),
                "F4_durable_outcome_before_checkpoint_is_not_recoverable": (
                    case_outcome_checkpoint_interruption(foundation)
                ),
            }

    decisive_false_acceptances = sum(
        1
        for name, finding in findings.items()
        if name.startswith(("F1_", "F2_", "F3_"))
        and any(
            finding.get(key) is True
            for key in (
                "accepted_after_substitution",
                "accepted_after_extra_claim_metadata",
            )
        )
    )
    if decisive_false_acceptances != 3:
        raise AssertionError("expected three decisive false acceptances")
    if (
        findings[
            "F4_durable_outcome_before_checkpoint_is_not_recoverable"
        ]["explicit_recovery_rejected"]
        is not True
    ):
        raise AssertionError("expected the interruption-window recovery gap")

    evidence = {
        "schema": "order13-k3-production-independent-referee-evidence-v1",
        "verdict": "REJECT",
        "scope": (
            "Frozen local bytes; synthetic fixtures only; no real SAT solver "
            "or proof checker executed."
        ),
        "frozen_file_sha256": observed_frozen,
        "tool_evidence": tools,
        "checks": checks,
        "findings": findings,
        "decisive_false_acceptance_count": decisive_false_acceptances,
        "real_solver_or_proof_checker_execution_count": 0,
    }
    arguments.output.write_bytes(
        (json.dumps(evidence, indent=2, sort_keys=True) + "\n").encode("utf-8")
    )
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
