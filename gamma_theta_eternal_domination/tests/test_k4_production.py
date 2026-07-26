from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from contextlib import ExitStack, contextmanager
from pathlib import Path
from typing import Iterator
from unittest.mock import patch


CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from search.k4_production import runner as production  # noqa: E402
from synthesis_k3.cegar import ChildResult  # noqa: E402


PARENT = CAMPAIGN / "instances/order12_k4_connected_parent/instance.cnf"
PARENT_MANIFEST = (
    CAMPAIGN / "instances/order12_k4_connected_parent/manifest.json"
)


def fake_source_binding() -> dict[str, object]:
    records: list[object] = []
    return {
        "head_at_creation": "0" * 40,
        "global_worktree_cleanliness_required": False,
        "records": records,
        "source_set_sha256": production.sha256_bytes(
            production.canonical_json_bytes(records)
        ),
    }


def passing_resource_report(
    run_directory: Path,
    *,
    phase: str,
    memory_limit_mib: int,
    limits: object,
) -> dict[str, object]:
    del run_directory, memory_limit_mib, limits
    return {
        "schema": "gamma-theta-k4-resource-gate-v1",
        "phase": phase,
        "checked_unix_ns": 1,
        "load_average_one_minute": 0.0,
        "load_ceiling": 1000.0,
        "available_memory_bytes": 16 << 30,
        "required_memory_bytes": 1,
        "free_disk_bytes": 16 << 30,
        "required_free_disk_bytes": 1,
        "worst_case_live_file_slots": 11,
        "checks": {"load": True, "memory": True, "disk": True},
        "probe_errors": [],
        "passed": True,
    }


@contextmanager
def patched_production_environment(
    *,
    resource_report=passing_resource_report,
    child_runner: object | None = None,
) -> Iterator[None]:
    with ExitStack() as stack:
        stack.enter_context(
            patch.object(
                production,
                "_committed_source_binding",
                side_effect=fake_source_binding,
            )
        )
        stack.enter_context(
            patch.object(
                production,
                "_verify_committed_source_binding",
                return_value=None,
            )
        )
        stack.enter_context(
            patch.object(
                production,
                "_resource_report",
                side_effect=resource_report,
            )
        )
        if child_runner is not None:
            stack.enter_context(
                patch.object(
                    production,
                    "run_bounded_child",
                    side_effect=child_runner,
                )
            )
        yield


def child_result(
    *,
    command: tuple[str, ...],
    stdout_path: Path,
    stderr_path: Path,
    exit_code: int,
    wall_limit_seconds: int,
    memory_limit_mib: int,
    file_limit_mib: int,
    timed_out: bool = False,
    termination_signal: int | None = None,
) -> ChildResult:
    executable_hash = production.sha256_file(Path(command[0]))
    return ChildResult(
        command=command,
        command_sha256="0" * 64,
        executable_sha256_before=executable_hash,
        executable_sha256_after=executable_hash,
        exit_code=exit_code,
        termination_signal=termination_signal,
        timed_out=timed_out,
        memory_limit_exceeded=False,
        started_unix_ns=1,
        finished_unix_ns=2,
        wall_seconds=0.01,
        user_cpu_seconds=0.0,
        system_cpu_seconds=0.0,
        maximum_resident_set_size_mib=1.0,
        maximum_resident_set_size_raw=1,
        maximum_resident_set_size_raw_unit="bytes",
        peak_polled_resident_set_size_mib=1.0,
        available_memory_before_bytes=16 << 30,
        wall_limit_seconds=wall_limit_seconds,
        memory_limit_mib=memory_limit_mib,
        file_limit_mib=file_limit_mib,
        stdout_path=str(stdout_path.resolve()),
        stdout_sha256=production.sha256_file(stdout_path),
        stderr_path=str(stderr_path.resolve()),
        stderr_sha256=production.sha256_file(stderr_path),
    )


class FakeProofPipeline:
    def __init__(self, scenario: str = "verified"):
        self.scenario = scenario
        self.calls: list[tuple[str, ...]] = []

    def __call__(self, **keywords: object) -> ChildResult:
        command = tuple(keywords["command"])  # type: ignore[arg-type]
        stdout_path = keywords["stdout_path"]  # type: ignore[assignment]
        stderr_path = keywords["stderr_path"]  # type: ignore[assignment]
        self.calls.append(command)
        if self.scenario == "interrupt" and len(self.calls) == 1:
            raise KeyboardInterrupt
        stdout_path.write_bytes(b"")
        stderr_path.write_bytes(b"")
        common = {
            "command": command,
            "stdout_path": stdout_path,
            "stderr_path": stderr_path,
            "wall_limit_seconds": keywords["wall_limit_seconds"],
            "memory_limit_mib": keywords["memory_limit_mib"],
            "file_limit_mib": keywords["file_limit_mib"],
        }
        executable = Path(command[0])
        if executable.name == "cadical":
            if self.scenario == "timeout":
                return child_result(
                    **common,
                    exit_code=-int(signal.SIGTERM),
                    timed_out=True,
                    termination_signal=int(signal.SIGTERM),
                )
            result = Path(command[command.index("-w") + 1])
            result.write_bytes(b"s UNSATISFIABLE\n")
            Path(command[-1]).write_bytes(bytes.fromhex("61 00"))
            return child_result(**common, exit_code=20)
        if executable.name == "drat-trim":
            if "-f" in command:
                if "-L" in command:
                    raise AssertionError("forward replay also requested LRAT")
                if self.scenario == "raw_forward_warning":
                    stdout_path.write_bytes(
                        b"s VERIFIED\nc WARNING hostile mutation\n"
                    )
                else:
                    stdout_path.write_bytes(
                        b"c forward verification\ns VERIFIED\n"
                    )
                return child_result(**common, exit_code=0)
            if "-L" not in command:
                raise AssertionError("backward conversion omitted LRAT")
            lrat = Path(command[command.index("-L") + 1])
            lrat.write_bytes(b"114747 0 1 0\n")
            if self.scenario == "lrat_conversion_warning":
                stdout_path.write_bytes(
                    b"s VERIFIED\nc WARNING hostile mutation\n"
                )
            else:
                stdout_path.write_bytes(
                    b"c backward conversion\ns VERIFIED\n"
                )
            return child_result(**common, exit_code=0)
        if executable.name == "lrat-check":
            if self.scenario == "checker_duplicate":
                stdout_path.write_bytes(b"c VERIFIED\nc VERIFIED\n")
            else:
                stdout_path.write_bytes(b"c VERIFIED\n")
            return child_result(**common, exit_code=0)
        raise AssertionError(f"unexpected fake command {command}")


class K4ProductionTests(unittest.TestCase):
    def test_real_git_binding_resolves_campaign_subdirectory(self) -> None:
        # Deliberately do not mock Git.  Without the campaign-relative ``./``
        # prefix, revision lookup incorrectly searches for ``src/...`` at
        # the repository root and makes initialization impossible.
        relative = "src/synthesis_k3/coloring.py"
        with patch.object(
            production,
            "RUNTIME_SOURCE_RELATIVE_PATHS",
            (relative,),
        ):
            binding = production._committed_source_binding()
            production._verify_committed_source_binding(binding)
        self.assertEqual(
            [record["path"] for record in binding["records"]],
            [relative],
        )

    def initialize(self, directory: Path) -> Path:
        run = directory / "run"
        with patched_production_environment():
            report = production.initialize_run(
                run_directory=run,
                parent_cnf=PARENT,
                parent_manifest=PARENT_MANIFEST,
                solver_wall_seconds=10,
                converter_wall_seconds=10,
                checker_wall_seconds=10,
                solver_memory_mib=64,
                postprocess_memory_mib=64,
                file_limit_mib=16,
                disk_reserve_mib=4096,
                memory_reserve_mib=512,
                load_max=1000.0,
                validation_gate_open=True,
            )
        self.assertEqual(report["status"], "INITIALIZED_NO_SOLVER_RUN")
        return run

    def test_exact_parent_and_boolean_partition(self) -> None:
        parent = PARENT.read_bytes()
        self.assertEqual(
            production.sha256_bytes(parent),
            production.EXPECTED_PARENT_CNF_SHA256,
        )
        partition = production._partition_payload(parent, 0)
        production._validate_partition(partition, parent)
        self.assertEqual(
            partition["cube_variables"], [4, 14, 23, 31]
        )
        cases = partition["cases"]
        self.assertEqual(len(cases), 16)
        self.assertEqual(
            {tuple(case["cube_bits"]) for case in cases},
            {
                tuple((mask >> shift) & 1 for shift in (3, 2, 1, 0))
                for mask in range(16)
            },
        )
        for case in cases:
            leaf = production._case_cnf_bytes(
                parent, case["cube_literals"]
            )
            parsed = production.parse_dimacs_bytes(leaf)
            self.assertEqual(parsed.variable_count, 18_381)
            self.assertEqual(len(parsed.clauses), 114_746)
            self.assertEqual(
                sum(map(len, parsed.clauses)), 1_180_020
            )
            self.assertEqual(
                production.sha256_bytes(leaf), case["cnf_sha256"]
            )

    def test_initialization_is_gated_exclusive_and_auditable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            with self.assertRaises(PermissionError):
                production.initialize_run(run_directory=root / "blocked")
            run = self.initialize(root)
            with patched_production_environment():
                audit = production.audit_run(run)
                with self.assertRaises(FileExistsError):
                    production.initialize_run(
                        run_directory=run,
                        validation_gate_open=True,
                    )
            self.assertEqual(
                audit["status"],
                "PASS_READ_ONLY_AUDIT_NO_MATHEMATICAL_CLAIM",
            )
            self.assertEqual(
                audit["case_status_histogram"], {"PENDING": 16}
            )
            self.assertFalse(audit["proofs_freshly_replayed"])

    def test_commands_pin_binary_conversion_and_lrat_replay(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.initialize(Path(temporary).resolve())
            manifest, _ = production._load_run_manifest(run)
            partition = json.loads((run / "partition.json").read_text())
            case = partition["cases"][0]
            attempt = run / "scratch-command-path"
            solver = production._solver_command(manifest, case, attempt)
            raw_forward = production._raw_forward_command(
                manifest, attempt
            )
            conversion = production._lrat_conversion_command(
                manifest, attempt
            )
            checker = production._lrat_check_command(manifest, attempt)
            self.assertIn("--binary", solver)
            self.assertIn(f"--seed={case['seed']}", solver)
            self.assertEqual(
                [
                    flag
                    for flag in ("-i", "-f", "-W", "-L")
                    if flag in raw_forward
                ],
                ["-i", "-f", "-W"],
            )
            self.assertNotIn("-L", raw_forward)
            self.assertNotIn("-U", raw_forward)
            self.assertEqual(
                [
                    flag
                    for flag in ("-i", "-f", "-W", "-L")
                    if flag in conversion
                ],
                ["-i", "-W", "-L"],
            )
            self.assertNotIn("-f", conversion)
            self.assertNotIn("-U", conversion)
            self.assertEqual(Path(checker[0]).name, "lrat-check")
            self.assertEqual(
                production.sha256_file(Path(checker[0])),
                production.LRAT_CHECK_BINARY_SHA256,
            )

    def test_mocked_verified_leaf_preserves_raw_and_lrat_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.initialize(Path(temporary).resolve())
            fake = FakeProofPipeline()
            with patched_production_environment(child_runner=fake):
                report = production.run_next_case(
                    run,
                    production_gate_open=True,
                )
                audit = production.audit_run(run)
            self.assertEqual(report["status"], "UNSAT_LRAT_VERIFIED")
            self.assertEqual(len(fake.calls), 4)
            attempt = (
                run / "cases/case-0000/attempt-000001"
            )
            self.assertTrue((attempt / "proof.raw.bdrat").is_file())
            self.assertTrue((attempt / "proof.converted.lrat").is_file())
            self.assertTrue((attempt / "certificate.json").is_file())
            self.assertEqual(
                audit["case_status_histogram"],
                {"PENDING": 15, "UNSAT_LRAT_VERIFIED": 1},
            )
            self.assertEqual(
                audit["aggregate_status"], "INCOMPLETE_NONCLAIM"
            )

    def test_raw_forward_warning_is_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.initialize(Path(temporary).resolve())
            fake = FakeProofPipeline("raw_forward_warning")
            with patched_production_environment(child_runner=fake):
                report = production.run_next_case(
                    run,
                    production_gate_open=True,
                )
            self.assertEqual(
                report["status"], "RAW_FORWARD_REJECTED_NONCLAIM"
            )
            attempt = run / "cases/case-0000/attempt-000001"
            self.assertTrue((attempt / "proof.raw.bdrat").is_file())
            self.assertFalse((attempt / "proof.converted.lrat").exists())
            self.assertFalse((attempt / "certificate.json").exists())

    def test_lrat_conversion_warning_is_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.initialize(Path(temporary).resolve())
            fake = FakeProofPipeline("lrat_conversion_warning")
            with patched_production_environment(child_runner=fake):
                report = production.run_next_case(
                    run,
                    production_gate_open=True,
                )
            self.assertEqual(
                report["status"],
                "LRAT_CONVERSION_REJECTED_NONCLAIM",
            )
            attempt = run / "cases/case-0000/attempt-000001"
            self.assertTrue((attempt / "proof.raw.bdrat").is_file())
            self.assertTrue((attempt / "proof.converted.lrat").is_file())
            self.assertFalse((attempt / "certificate.json").exists())

    def test_duplicate_lrat_status_is_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.initialize(Path(temporary).resolve())
            fake = FakeProofPipeline("checker_duplicate")
            with patched_production_environment(child_runner=fake):
                report = production.run_next_case(
                    run,
                    production_gate_open=True,
                )
            self.assertEqual(
                report["status"], "LRAT_CHECK_REJECTED_NONCLAIM"
            )
            self.assertFalse(
                (
                    run
                    / "cases/case-0000/attempt-000001/certificate.json"
                ).exists()
            )

    def test_timeout_is_retryable_and_stops_pipeline(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.initialize(Path(temporary).resolve())
            fake = FakeProofPipeline("timeout")
            with patched_production_environment(child_runner=fake):
                report = production.run_next_case(
                    run,
                    production_gate_open=True,
                )
                audit = production.audit_run(run)
            self.assertEqual(report["status"], "SOLVER_TIMEOUT_NONCLAIM")
            self.assertEqual(len(fake.calls), 1)
            self.assertEqual(
                audit["case_status_histogram"],
                {"PENDING": 15, "RETRYABLE_NONCLAIM": 1},
            )

    def test_failed_resource_gate_starts_no_child(self) -> None:
        def failing_resource(*args: object, **kwargs: object) -> dict[str, object]:
            report = passing_resource_report(*args, **kwargs)  # type: ignore[arg-type]
            report["checks"] = {"load": False, "memory": True, "disk": True}
            report["passed"] = False
            return report

        with tempfile.TemporaryDirectory() as temporary:
            run = self.initialize(Path(temporary).resolve())
            fake = FakeProofPipeline()
            with patched_production_environment(
                resource_report=failing_resource,
                child_runner=fake,
            ):
                report = production.run_next_case(
                    run,
                    production_gate_open=True,
                )
            self.assertEqual(
                report["status"], "RESOURCE_GATE_FAILED_NONCLAIM"
            )
            self.assertEqual(fake.calls, [])

    def test_sat_parser_requires_complete_clause_satisfying_model(self) -> None:
        cnf = b"p cnf 2 2\n1 0\n-1 2 0\n"
        status, candidate = production.classify_solver_result(
            cnf, b"s SATISFIABLE\nv 1 2 0\n"
        )
        self.assertEqual(status, "SAT")
        self.assertIsNotNone(candidate)
        with self.assertRaises(ValueError):
            production.classify_solver_result(
                cnf, b"s SATISFIABLE\nv 1 -2 0\n"
            )
        with self.assertRaises(ValueError):
            production.classify_solver_result(
                cnf, b"s SATISFIABLE\nv 1 0\n"
            )

    def test_interrupted_attempt_requires_explicit_recovery(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.initialize(Path(temporary).resolve())
            fake = FakeProofPipeline("interrupt")
            with patched_production_environment(child_runner=fake):
                with self.assertRaises(KeyboardInterrupt):
                    production.run_next_case(
                        run,
                        production_gate_open=True,
                    )
                audit = production.audit_run(run)
                self.assertEqual(
                    audit["case_status_histogram"],
                    {
                        "PENDING": 15,
                        "RUNNING_UNFINISHED_NONCLAIM": 1,
                    },
                )
                with patch.object(
                    production, "_commands_containing", return_value=[]
                ):
                    recovered = production.recover_interrupted_attempt(
                        run, recovery_gate_open=True
                    )
                audit = production.audit_run(run)
            self.assertEqual(
                recovered["status"],
                "INTERRUPTED_ATTEMPT_RECOVERED_NONCLAIM",
            )
            self.assertEqual(
                audit["case_status_histogram"],
                {"PENDING": 15, "RETRYABLE_NONCLAIM": 1},
            )

    def test_public_runner_has_no_child_injection_parameter(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.initialize(Path(temporary).resolve())
            with self.assertRaises(TypeError):
                production.run_next_case(
                    run,
                    production_gate_open=True,
                    child_runner=FakeProofPipeline(),  # type: ignore[call-arg]
                )
            with patched_production_environment():
                audit = production.audit_run(run)
            self.assertEqual(
                audit["case_status_histogram"], {"PENDING": 16}
            )

    def test_reserved_attempt_config_hash_is_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.initialize(Path(temporary).resolve())
            fake = FakeProofPipeline("interrupt")
            with patched_production_environment(child_runner=fake):
                with self.assertRaises(KeyboardInterrupt):
                    production.run_next_case(
                        run,
                        production_gate_open=True,
                    )
            config_path = (
                run
                / "cases/case-0000/attempt-000001/attempt-config.json"
            )
            config = json.loads(config_path.read_text())
            config["created_unix_ns"] += 1
            config_path.write_bytes(production.canonical_json_bytes(config))
            with patched_production_environment():
                with self.assertRaises(ValueError):
                    production.audit_run(run)
                with patch.object(
                    production, "_commands_containing", return_value=[]
                ):
                    with self.assertRaises(ValueError):
                        production.recover_interrupted_attempt(
                            run, recovery_gate_open=True
                        )

    def test_orphan_before_reservation_is_reconciled_nonclaim(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.initialize(Path(temporary).resolve())
            fake = FakeProofPipeline()
            with patched_production_environment(child_runner=fake):
                with patch.object(
                    production,
                    "_append_checkpoint_transition",
                    side_effect=RuntimeError("injected before reservation"),
                ):
                    with self.assertRaises(RuntimeError):
                        production.run_next_case(
                            run,
                            production_gate_open=True,
                        )
                with self.assertRaises(ValueError):
                    production.audit_run(run)
                with patch.object(
                    production, "_commands_containing", return_value=[]
                ):
                    recovered = production.recover_interrupted_attempt(
                        run, recovery_gate_open=True
                    )
                audit = production.audit_run(run)
            self.assertEqual(
                recovered["status"],
                "ORPHAN_ATTEMPT_RECONCILED_NONCLAIM",
            )
            self.assertEqual(
                recovered["reconciliation_mode"],
                "ORPHAN_BEFORE_RESERVATION",
            )
            self.assertEqual(fake.calls, [])
            self.assertEqual(
                audit["case_status_histogram"],
                {"PENDING": 15, "RETRYABLE_NONCLAIM": 1},
            )

    def test_outcome_before_completion_is_reconciled_nonclaim(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.initialize(Path(temporary).resolve())
            fake = FakeProofPipeline()
            original_append = production._append_checkpoint_transition
            calls = 0

            def crash_on_second_append(
                *args: object, **kwargs: object
            ) -> object:
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise RuntimeError("injected before completion checkpoint")
                return original_append(*args, **kwargs)  # type: ignore[arg-type]

            with patched_production_environment(child_runner=fake):
                with patch.object(
                    production,
                    "_append_checkpoint_transition",
                    side_effect=crash_on_second_append,
                ):
                    with self.assertRaises(RuntimeError):
                        production.run_next_case(
                            run,
                            production_gate_open=True,
                        )
                with self.assertRaises(ValueError):
                    production.audit_run(run)
                with patch.object(
                    production, "_commands_containing", return_value=[]
                ):
                    recovered = production.recover_interrupted_attempt(
                        run, recovery_gate_open=True
                    )
                audit = production.audit_run(run)
            self.assertEqual(
                recovered["status"],
                "OUTCOME_CHECKPOINT_RECONCILED_NONCLAIM",
            )
            self.assertEqual(
                recovered["reconciliation_mode"],
                "OUTCOME_BEFORE_COMPLETION_CHECKPOINT",
            )
            self.assertEqual(len(fake.calls), 4)
            self.assertEqual(
                audit["case_status_histogram"],
                {"PENDING": 15, "RETRYABLE_NONCLAIM": 1},
            )

    def test_real_tiny_binary_drat_four_phase_chain(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            attempt = Path(temporary).resolve()
            cnf = (
                b"p cnf 2 4\n"
                b"1 2 0\n"
                b"1 -2 0\n"
                b"-1 2 0\n"
                b"-1 -2 0\n"
            )
            (attempt / "instance.cnf").write_bytes(cnf)
            manifest = {
                "tools": {
                    "cadical": {
                        "path": str(
                            (
                                CAMPAIGN
                                / "tools/cadical_3_0_1/build/cadical"
                            ).resolve()
                        )
                    },
                    "drat_trim": {
                        "path": str(
                            (
                                CAMPAIGN
                                / "tools/drat_trim_2023_05_22/drat-trim"
                            ).resolve()
                        )
                    },
                    "lrat_check": {
                        "path": str(
                            (
                                CAMPAIGN
                                / "tools/drat_trim_2023_05_22/lrat-check"
                            ).resolve()
                        )
                    },
                },
                "limits": {
                    "solver_wall_seconds": 10,
                    "converter_wall_seconds": 10,
                },
            }
            case = {"seed": 7}
            commands = (
                production._solver_command(manifest, case, attempt),
                production._raw_forward_command(manifest, attempt),
                production._lrat_conversion_command(manifest, attempt),
                production._lrat_check_command(manifest, attempt),
            )
            completed: list[subprocess.CompletedProcess[bytes]] = []
            for command in commands:
                completed.append(
                    subprocess.run(
                        command,
                        cwd=CAMPAIGN,
                        env={},
                        stdin=subprocess.DEVNULL,
                        capture_output=True,
                        check=False,
                        timeout=10,
                    )
                )
            self.assertEqual(
                [result.returncode for result in completed],
                [20, 0, 0, 0],
            )
            status, candidate = production.classify_solver_result(
                cnf, (attempt / "solver.result").read_bytes()
            )
            self.assertEqual(status, "UNSAT")
            self.assertIsNone(candidate)
            self.assertGreater(
                (attempt / "proof.raw.bdrat").stat().st_size, 0
            )
            production._strict_converter_success(
                completed[1].stdout, completed[1].stderr
            )
            production._strict_converter_success(
                completed[2].stdout, completed[2].stderr
            )
            self.assertGreater(
                (attempt / "proof.converted.lrat").stat().st_size, 0
            )
            production._strict_lrat_success(
                completed[3].stdout, completed[3].stderr
            )

    @unittest.skipUnless(os.name == "posix", "requires POSIX process groups")
    def test_bounded_child_kills_spawned_process_group_on_timeout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            stdout_path = root / "stdout"
            stderr_path = root / "stderr"
            python = Path(sys.executable).resolve()
            code = (
                "import subprocess,sys,time;"
                "p=subprocess.Popen([sys.executable,'-c','import time;"
                "time.sleep(60)']);"
                "print(p.pid,flush=True);time.sleep(60)"
            )
            child = production.run_bounded_child(
                command=(str(python), "-c", code),
                cwd=root,
                stdout_path=stdout_path,
                stderr_path=stderr_path,
                wall_limit_seconds=1,
                memory_limit_mib=64,
                file_limit_mib=16,
                readonly_paths={},
            )
            self.assertTrue(child.timed_out)
            grandchild = int(stdout_path.read_text().strip())
            alive = True
            deadline = time.monotonic() + 2.0
            while time.monotonic() < deadline:
                try:
                    os.kill(grandchild, 0)
                except ProcessLookupError:
                    alive = False
                    break
                time.sleep(0.05)
            self.assertFalse(alive, "grandchild survived process-group timeout")


if __name__ == "__main__":
    unittest.main()
