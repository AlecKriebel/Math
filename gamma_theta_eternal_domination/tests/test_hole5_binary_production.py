from __future__ import annotations

import ast
import hashlib
import json
import signal
import subprocess
import sys
import tempfile
import unittest
from contextlib import ExitStack, contextmanager
from pathlib import Path
from typing import Iterator
from unittest.mock import patch


CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from synthesis_k3.cegar import (  # noqa: E402
    ChildResult,
    ParsedSolverResult,
)
from synthesis_k3.hole5_binary_production import (  # noqa: E402
    ADDITION_PROOF_NAME,
    CERTIFICATE_NAME,
    EXPECTED_CADICAL_ARCHIVE_SHA256,
    EXPECTED_CADICAL_BINARY_SHA256,
    EXPECTED_DRAT_TRIM_ARCHIVE_SHA256,
    EXPECTED_DRAT_TRIM_BINARY_SHA256,
    EXPECTED_PACKAGE_MANIFEST_SHA256,
    OUTCOME_NAME,
    RAW_PROOF_NAME,
    RESULT_NAME,
    RUN_CONFIG_NAME,
    SAT_CANDIDATE_NAME,
    RUNTIME_SOURCE_RELATIVE_PATHS,
    _checker_command,
    _independent_tool_hash_gate,
    _parser_command,
    _solver_command,
    run_production,
)
from synthesis_k3.template_color_bank import sha256_file  # noqa: E402
from synthesis_k3.cegar import verify_pinned_tools  # noqa: E402


SOURCE_PACKAGE = (
    CAMPAIGN / "results/synthesis_k3_template_bank_packages/hole5"
)
RETAINED_PACKAGE = (
    CAMPAIGN / "results/synthesis_k3_hole5_signature_package"
)
CADICAL = CAMPAIGN / "tools/cadical_3_0_1/build/cadical"
DRAT_TRIM = CAMPAIGN / "tools/drat_trim_2023_05_22/drat-trim"
PARSER = CAMPAIGN / "reviews/hole5_binary_drat_hostile_probe.py"
FAKE_HEAD = "a" * 40


def fake_git_binding(
    sources: object,
    *,
    head: str | None = None,
) -> dict[str, object]:
    del sources
    return {
        "head_commit": FAKE_HEAD if head is None else head,
        "repository_relative_campaign_path": "gamma_theta_eternal_domination",
        "runtime_sources_match_head": True,
        "runtime_source_mismatches": [],
        "global_worktree_cleanliness_required": False,
    }


@contextmanager
def patched_source_bindings() -> Iterator[None]:
    with ExitStack() as stack:
        stack.enter_context(
            patch(
                "synthesis_k3.hole5_binary_production.git_source_binding",
                side_effect=fake_git_binding,
            )
        )
        yield


def child_result(
    *,
    command: tuple[str, ...],
    stdout_path: Path,
    stderr_path: Path,
    exit_code: int,
    timed_out: bool = False,
    memory_limit_exceeded: bool = False,
    termination_signal: int | None = None,
    wall_limit_seconds: int,
    memory_limit_mib: int,
    file_limit_mib: int,
) -> ChildResult:
    executable_hash = sha256_file(Path(command[0]))
    return ChildResult(
        command=command,
        command_sha256="0" * 64,
        executable_sha256_before=executable_hash,
        executable_sha256_after=executable_hash,
        exit_code=exit_code,
        termination_signal=termination_signal,
        timed_out=timed_out,
        memory_limit_exceeded=memory_limit_exceeded,
        started_unix_ns=1,
        finished_unix_ns=2,
        wall_seconds=0.01,
        user_cpu_seconds=0.0,
        system_cpu_seconds=0.0,
        maximum_resident_set_size_mib=1.0,
        maximum_resident_set_size_raw=1,
        maximum_resident_set_size_raw_unit="bytes",
        peak_polled_resident_set_size_mib=1.0,
        available_memory_before_bytes=8 << 30,
        wall_limit_seconds=wall_limit_seconds,
        memory_limit_mib=memory_limit_mib,
        file_limit_mib=file_limit_mib,
        stdout_path=str(stdout_path),
        stdout_sha256=sha256_file(stdout_path),
        stderr_path=str(stderr_path),
        stderr_sha256=sha256_file(stderr_path),
    )


class FakePipeline:
    """Mock only bounded execution; use the real clean-room parser on bytes."""

    def __init__(self, scenario: str):
        self.scenario = scenario
        self.calls: list[tuple[str, ...]] = []

    def __call__(self, **keywords: object) -> ChildResult:
        command = tuple(keywords["command"])  # type: ignore[arg-type]
        stdout_path = keywords["stdout_path"]  # type: ignore[assignment]
        stderr_path = keywords["stderr_path"]  # type: ignore[assignment]
        self.calls.append(command)
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

        if command[0] == str(CADICAL.resolve()):
            result_path = Path(command[command.index("-w") + 1])
            raw_proof = Path(command[-1])
            if self.scenario == "timeout":
                raw_proof.write_bytes(b"a")
                return child_result(
                    **common,
                    exit_code=-int(signal.SIGTERM),
                    timed_out=True,
                    termination_signal=int(signal.SIGTERM),
                )
            if self.scenario == "file_limit":
                raw_proof.write_bytes(b"a\x80")
                return child_result(
                    **common,
                    exit_code=-int(signal.SIGXFSZ),
                    termination_signal=int(signal.SIGXFSZ),
                )
            if self.scenario == "unknown":
                result_path.write_bytes(b"s UNKNOWN\n")
                raw_proof.write_bytes(b"")
                return child_result(**common, exit_code=0)
            if self.scenario == "sat":
                result_path.write_bytes(b"s SATISFIABLE\nv 1 0\n")
                raw_proof.write_bytes(b"")
                return child_result(**common, exit_code=10)
            result_path.write_bytes(b"s UNSATISFIABLE\n")
            # a 1; d 2; a -1; a empty.  Canonical and complete.
            raw_proof.write_bytes(
                bytes.fromhex("61 02 00 64 04 00 61 03 00 61 00")
            )
            return child_result(**common, exit_code=20)

        if str(PARSER.resolve()) in command:
            completed = subprocess.run(
                command,
                cwd=CAMPAIGN,
                env={},
                stdin=subprocess.DEVNULL,
                capture_output=True,
                timeout=10,
                check=False,
            )
            if self.scenario == "parser_exit":
                stdout_path.write_bytes(completed.stdout)
                stderr_path.write_bytes(b"forced parser failure\n")
                return child_result(**common, exit_code=1)
            if self.scenario == "parser_bad_report":
                stdout_path.write_bytes(b"{}\n")
                stderr_path.write_bytes(b"")
                return child_result(**common, exit_code=0)
            stdout_path.write_bytes(completed.stdout)
            stderr_path.write_bytes(completed.stderr)
            return child_result(
                **common, exit_code=completed.returncode
            )

        if command[0] == str(DRAT_TRIM.resolve()):
            if self.scenario == "checker_exit":
                stdout_path.write_bytes(b"")
                stderr_path.write_bytes(b"forced checker failure\n")
                return child_result(**common, exit_code=1)
            if self.scenario == "checker_warning":
                stdout_path.write_bytes(
                    b"s VERIFIED\nc 0 RAT lemmas in core\n"
                )
                stderr_path.write_bytes(b"WARNING: hostile mutation\n")
                return child_result(**common, exit_code=0)
            if self.scenario == "checker_nonzero_rat":
                stdout_path.write_bytes(
                    b"s VERIFIED\nc 100 RAT lemmas in core\n"
                )
                stderr_path.write_bytes(b"")
                return child_result(**common, exit_code=0)
            if self.scenario == "checker_duplicate_status":
                stdout_path.write_bytes(
                    b"s VERIFIED\ns VERIFIED\n"
                    b"c 0 RAT lemmas in core\n"
                )
                stderr_path.write_bytes(b"")
                return child_result(**common, exit_code=0)
            stdout_path.write_bytes(
                b"c forward verification\n"
                b"s VERIFIED\n"
                b"c 0 RAT lemmas in core; 0 redundant literals\n"
            )
            stderr_path.write_bytes(b"")
            return child_result(**common, exit_code=0)

        raise AssertionError(f"unexpected mocked command {command}")


@unittest.skipUnless(
    SOURCE_PACKAGE.is_dir()
    and RETAINED_PACKAGE.is_dir()
    and CADICAL.is_file()
    and DRAT_TRIM.is_file()
    and PARSER.is_file(),
    "retained package or pinned tool absent",
)
class ProductionRunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temporary.name).resolve()
        cls.package = RETAINED_PACKAGE
        cls.package_manifest_sha256 = EXPECTED_PACKAGE_MANIFEST_SHA256

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def run_mocked(
        self,
        scenario: str,
        *,
        output_name: str,
    ) -> tuple[dict[str, object], FakePipeline, Path]:
        output = self.root / output_name
        pipeline = FakePipeline(scenario)
        with patched_source_bindings(), patch(
            "synthesis_k3.hole5_binary_production.run_bounded_child",
            side_effect=pipeline,
        ):
            if scenario == "sat":
                complete_model = {
                    variable: False for variable in range(1, 6_887)
                }
                with patch(
                    "synthesis_k3.hole5_binary_production."
                    "parse_solver_result_file",
                    return_value=ParsedSolverResult(
                        "SAT", complete_model
                    ),
                ), patch(
                    "synthesis_k3.hole5_binary_production."
                    "validate_model_satisfies_cnf",
                ):
                    outcome = self._invoke(output)
            else:
                outcome = self._invoke(output)
        return outcome, pipeline, output

    def _invoke(self, output: Path) -> dict[str, object]:
        return run_production(
            package_directory=self.package,
            source_package_directory=SOURCE_PACKAGE,
            output_directory=output,
            expected_package_manifest_sha256=(
                self.package_manifest_sha256
            ),
            expected_head_commit=FAKE_HEAD,
            cadical_path=CADICAL,
            drat_trim_path=DRAT_TRIM,
            seed=7,
            solver_seconds=5,
            parser_seconds=5,
            checker_seconds=5,
            solver_memory_mib=64,
            parser_memory_mib=64,
            checker_memory_mib=64,
            file_limit_mib=1,
            disk_reserve_mib=4_096,
            validation_gate=True,
            hostile_audit_gate=True,
        )

    def test_commands_are_explicit_binary_isolated_and_strict_rup(self) -> None:
        result = self.root / "r"
        cnf = self.package / "instance.cnf"
        raw = self.root / "raw"
        addition = self.root / "addition"
        solver = _solver_command(
            CADICAL,
            seed=9,
            internal_seconds=10,
            result_path=result,
            cnf_path=cnf,
            proof_path=raw,
        )
        self.assertIn("--binary", solver)
        self.assertNotIn("--no-binary", solver)
        self.assertEqual(solver[1], "--seed=9")
        parser = _parser_command(
            Path(sys.executable).resolve(),
            PARSER,
            raw_proof=raw,
            addition_proof=addition,
        )
        self.assertEqual(parser[1:3], ("-I", "-B"))
        self.assertEqual(parser[-2:], ("--max-var", "6886"))
        checker = _checker_command(
            DRAT_TRIM,
            cnf_path=cnf,
            proof_path=addition,
            internal_seconds=11,
        )
        self.assertEqual(
            checker[-6:], ("-i", "-f", "-W", "-U", "-t", "11")
        )

    def test_unsat_pipeline_preserves_raw_and_emits_certificate(self) -> None:
        outcome, pipeline, output = self.run_mocked(
            "unsat", output_name="unsat-success"
        )
        self.assertEqual(
            outcome["status"], "UNSAT_VERIFIED_FINITE_CERTIFICATE"
        )
        self.assertEqual(
            outcome["claim_status"], "VERIFIED_FINITE_CERTIFICATE"
        )
        self.assertEqual(len(pipeline.calls), 3)
        self.assertEqual(
            (output / RAW_PROOF_NAME).read_bytes(),
            bytes.fromhex("61 02 00 64 04 00 61 03 00 61 00"),
        )
        self.assertEqual(
            (output / ADDITION_PROOF_NAME).read_bytes(),
            bytes.fromhex("61 02 00 61 03 00 61 00"),
        )
        self.assertTrue((output / CERTIFICATE_NAME).is_file())
        certificate = json.loads(
            (output / CERTIFICATE_NAME).read_text(encoding="utf-8")
        )
        self.assertTrue(
            certificate["raw_binary_proof"]["preserved"]
        )
        self.assertEqual(
            certificate["claim_status"],
            "NO_STANDALONE_MATHEMATICAL_CLAIM",
        )
        self.assertEqual(
            certificate["activation_condition"]["required_file"],
            OUTCOME_NAME,
        )
        self.assertEqual(
            certificate["checker_command"][-6:],
            ["-i", "-f", "-W", "-U", "-t", "5"],
        )
        self.assertTrue((output / OUTCOME_NAME).is_file())

    def test_parser_report_mutation_is_fail_closed_before_checker(self) -> None:
        outcome, pipeline, output = self.run_mocked(
            "parser_bad_report", output_name="parser-bad"
        )
        self.assertEqual(
            outcome["status"], "PARSER_ARTIFACT_INVALID_NONCLAIM"
        )
        self.assertEqual(
            outcome["claim_status"], "NO_MATHEMATICAL_CLAIM"
        )
        self.assertEqual(len(pipeline.calls), 2)
        self.assertFalse((output / CERTIFICATE_NAME).exists())

    def test_checker_warning_and_nonzero_exit_are_nonclaims(self) -> None:
        for scenario, expected in (
            ("checker_warning", "CHECKER_ARTIFACT_INVALID_NONCLAIM"),
            ("checker_nonzero_rat", "CHECKER_ARTIFACT_INVALID_NONCLAIM"),
            (
                "checker_duplicate_status",
                "CHECKER_ARTIFACT_INVALID_NONCLAIM",
            ),
            ("checker_exit", "CHECKER_EXIT_NONCLAIM"),
        ):
            with self.subTest(scenario=scenario):
                outcome, pipeline, output = self.run_mocked(
                    scenario, output_name=scenario
                )
                self.assertEqual(outcome["status"], expected)
                self.assertEqual(
                    outcome["claim_status"],
                    "NO_MATHEMATICAL_CLAIM",
                )
                self.assertEqual(len(pipeline.calls), 3)
                self.assertFalse((output / CERTIFICATE_NAME).exists())

    def test_post_certificate_mutation_demotes_claim(self) -> None:
        output = self.root / "post-certificate-mutation"
        pipeline = FakePipeline("unsat")
        with patched_source_bindings(), patch(
            "synthesis_k3.hole5_binary_production.run_bounded_child",
            side_effect=pipeline,
        ), patch(
            "synthesis_k3.hole5_binary_production._verify_all_bindings",
            side_effect=[
                None,
                RuntimeError("hostile post-certificate mutation"),
                None,
            ],
        ):
            outcome = self._invoke(output)
        self.assertEqual(
            outcome["status"], "POST_CERTIFICATE_MUTATION_NONCLAIM"
        )
        self.assertEqual(
            outcome["claim_status"], "NO_MATHEMATICAL_CLAIM"
        )
        certificate = json.loads(
            (output / CERTIFICATE_NAME).read_text(encoding="utf-8")
        )
        self.assertEqual(
            certificate["claim_status"],
            "NO_STANDALONE_MATHEMATICAL_CLAIM",
        )

    def test_timeout_file_limit_and_unknown_are_explicit_nonclaims(self) -> None:
        for scenario, expected in (
            ("timeout", "SOLVER_TIMEOUT_NONCLAIM"),
            ("file_limit", "SOLVER_FILE_LIMIT_NONCLAIM"),
            ("unknown", "INCONCLUSIVE_SOLVER_UNKNOWN"),
        ):
            with self.subTest(scenario=scenario):
                outcome, pipeline, output = self.run_mocked(
                    scenario, output_name=f"solver-{scenario}"
                )
                self.assertEqual(outcome["status"], expected)
                self.assertEqual(
                    outcome["claim_status"],
                    "NO_MATHEMATICAL_CLAIM",
                )
                self.assertEqual(len(pipeline.calls), 1)
                self.assertTrue((output / RAW_PROOF_NAME).exists())
                self.assertFalse((output / CERTIFICATE_NAME).exists())

    def test_sat_model_is_preserved_but_candidate_only(self) -> None:
        outcome, pipeline, output = self.run_mocked(
            "sat", output_name="sat"
        )
        self.assertEqual(
            outcome["status"], "SAT_MODEL_VERIFIED_CANDIDATE_ONLY"
        )
        self.assertEqual(outcome["claim_status"], "CANDIDATE_ONLY")
        self.assertEqual(len(pipeline.calls), 1)
        self.assertTrue((output / RESULT_NAME).is_file())
        self.assertTrue((output / SAT_CANDIDATE_NAME).is_file())
        candidate = json.loads(
            (output / SAT_CANDIDATE_NAME).read_text(encoding="utf-8")
        )
        self.assertFalse(candidate["counterexample_claim"])

    def test_both_explicit_gates_and_no_overwrite_are_enforced(self) -> None:
        for validation, hostile in ((False, True), (True, False)):
            output = self.root / f"gate-{validation}-{hostile}"
            with self.assertRaises(PermissionError):
                run_production(
                    package_directory=self.package,
                    source_package_directory=SOURCE_PACKAGE,
                    output_directory=output,
                    expected_package_manifest_sha256=(
                        self.package_manifest_sha256
                    ),
                    expected_head_commit=FAKE_HEAD,
                    cadical_path=CADICAL,
                    drat_trim_path=DRAT_TRIM,
                    seed=0,
                    solver_seconds=1,
                    parser_seconds=1,
                    checker_seconds=1,
                    solver_memory_mib=64,
                    parser_memory_mib=64,
                    checker_memory_mib=64,
                    file_limit_mib=1,
                    disk_reserve_mib=4_096,
                    validation_gate=validation,
                    hostile_audit_gate=hostile,
                )
            self.assertFalse(output.exists())

        existing = self.root / "existing"
        existing.mkdir()
        marker = existing / "keep"
        marker.write_bytes(b"keep")
        with self.assertRaises(FileExistsError):
            self._invoke(existing)
        self.assertEqual(marker.read_bytes(), b"keep")

    def test_wrong_manifest_hash_and_uncommitted_source_refuse_prelaunch(self) -> None:
        wrong_output = self.root / "wrong-manifest"
        with patched_source_bindings():
            with self.assertRaises(ValueError):
                run_production(
                    package_directory=self.package,
                    source_package_directory=SOURCE_PACKAGE,
                    output_directory=wrong_output,
                    expected_package_manifest_sha256="0" * 64,
                    expected_head_commit=FAKE_HEAD,
                    cadical_path=CADICAL,
                    drat_trim_path=DRAT_TRIM,
                    seed=0,
                    solver_seconds=1,
                    parser_seconds=1,
                    checker_seconds=1,
                    solver_memory_mib=64,
                    parser_memory_mib=64,
                    checker_memory_mib=64,
                    file_limit_mib=1,
                    disk_reserve_mib=4_096,
                    validation_gate=True,
                    hostile_audit_gate=True,
                )
        self.assertFalse(wrong_output.exists())

        source_output = self.root / "source-mismatch"
        with patch(
            "synthesis_k3.hole5_binary_production.git_source_binding",
            return_value={
                **fake_git_binding(None),
                "runtime_sources_match_head": False,
            },
        ):
            with self.assertRaises(RuntimeError):
                self._invoke(source_output)
        self.assertFalse(source_output.exists())

    def test_cadical_seed_range_is_exact_and_prelaunch(self) -> None:
        output = self.root / "bad-seed"
        with self.assertRaises(ValueError):
            run_production(
                package_directory=self.package,
                source_package_directory=SOURCE_PACKAGE,
                output_directory=output,
                expected_package_manifest_sha256=(
                    self.package_manifest_sha256
                ),
                expected_head_commit=FAKE_HEAD,
                cadical_path=CADICAL,
                drat_trim_path=DRAT_TRIM,
                seed=2_000_000_001,
                solver_seconds=1,
                parser_seconds=1,
                checker_seconds=1,
                solver_memory_mib=64,
                parser_memory_mib=64,
                checker_memory_mib=64,
                file_limit_mib=1,
                disk_reserve_mib=4_096,
                validation_gate=True,
                hostile_audit_gate=True,
            )
        self.assertFalse(output.exists())

    def test_output_cannot_modify_an_input_package(self) -> None:
        output = self.package / "forbidden-production-child"
        with patched_source_bindings(), self.assertRaises(ValueError):
            self._invoke(output)
        self.assertFalse(output.exists())

    def test_runtime_manifest_covers_local_import_closure(self) -> None:
        declared = set(RUNTIME_SOURCE_RELATIVE_PATHS)
        pending = ["src/synthesis_k3/hole5_binary_production.py"]
        observed: set[str] = set()
        while pending:
            relative = pending.pop()
            if relative in observed:
                continue
            observed.add(relative)
            tree = ast.parse((CAMPAIGN / relative).read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not isinstance(node, ast.ImportFrom) or node.level != 1:
                    continue
                modules: list[str] = []
                if node.module is not None:
                    modules.append(node.module)
                else:
                    modules.extend(alias.name for alias in node.names)
                for module in modules:
                    dependency = (
                        "src/synthesis_k3/"
                        + module.replace(".", "/")
                        + ".py"
                    )
                    if (CAMPAIGN / dependency).is_file():
                        pending.append(dependency)
        self.assertIn("src/synthesis_k3/__init__.py", declared)
        self.assertEqual(observed - declared, set())
        self.assertIn("src/synthesis_k3/coloring.py", observed)
        self.assertIn("src/synthesis_k3/generate.py", observed)

    def test_independent_tool_hash_gate_uses_exact_bytes(self) -> None:
        cadical, checker = verify_pinned_tools(CADICAL, DRAT_TRIM)
        _independent_tool_hash_gate(cadical, checker)
        expected = (
            (CADICAL, EXPECTED_CADICAL_BINARY_SHA256),
            (
                CAMPAIGN / "tools/cadical_3_0_1.tar.gz",
                EXPECTED_CADICAL_ARCHIVE_SHA256,
            ),
            (DRAT_TRIM, EXPECTED_DRAT_TRIM_BINARY_SHA256),
            (
                CAMPAIGN / "tools/drat_trim_2023_05_22.tar.gz",
                EXPECTED_DRAT_TRIM_ARCHIVE_SHA256,
            ),
        )
        for path, digest in expected:
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(), digest
            )


if __name__ == "__main__":
    unittest.main()
