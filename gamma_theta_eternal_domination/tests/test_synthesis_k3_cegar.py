from __future__ import annotations

import copy
import gzip
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

from synthesis_k3.cegar import (
    AuditInstrumentation,
    CADICAL_BINARY_SHA256,
    CANDIDATE_MARKER_NAME,
    CHECKPOINT_NAME,
    DRAT_TRIM_BINARY_SHA256,
    N,
    UNSAT_MARKER_NAME,
    _history_chain_step,
    _new_attempt_directory,
    atomic_write,
    audit_run,
    build_k3_encoding,
    build_configuration,
    campaign_root,
    canonical_coloring,
    canonical_json_bytes,
    checkpoint_state_sha256,
    clause_bytes,
    cuts_payload_bytes,
    disk_preflight,
    parse_dimacs_bytes,
    parse_dimacs_file,
    parse_solver_result_bytes,
    run_bounded_child,
    run_cegar,
    run_unsat_proof_replay,
    sha256_bytes,
    sha256_file,
    strict_json_file,
    validate_file_roles,
    validate_model_satisfies_cnf,
    verify_stored_drat_certificate,
)


ROOT = campaign_root()
CADICAL = ROOT / "tools/cadical_3_0_1/build/cadical"
DRAT_TRIM = ROOT / "tools/drat_trim_2023_05_22/drat-trim"


def configuration(run_directory: Path):
    return build_configuration(
        template="hole5",
        run_directory=run_directory,
        cadical_path=CADICAL,
        drat_trim_path=DRAT_TRIM,
        solver_seed=0,
        solver_wall_seconds=10,
        solver_memory_mib=1024,
        checker_wall_seconds=10,
        checker_memory_mib=1024,
    )


def run_kwargs(run_directory: Path) -> dict[str, object]:
    return {
        "template": "hole5",
        "run_directory": run_directory,
        "cadical_path": CADICAL,
        "drat_trim_path": DRAT_TRIM,
        "solver_seed": 0,
        "solver_wall_seconds": 10,
        "solver_memory_mib": 1024,
        "checker_wall_seconds": 10,
        "checker_memory_mib": 1024,
    }


def load_object(path: Path) -> dict[str, object]:
    value = strict_json_file(path)
    if not isinstance(value, dict):
        raise AssertionError(f"{path} is not a JSON object")
    return value


def rebind_first_attempt_and_history(
    run_directory: Path,
    mutate,
) -> None:
    checkpoint_path = run_directory / CHECKPOINT_NAME
    checkpoint = load_object(checkpoint_path)
    reference = checkpoint["attempts"][0]
    attempt_path = Path(reference["manifest_path"])
    attempt = load_object(attempt_path)
    mutate(attempt)
    atomic_write(attempt_path, canonical_json_bytes(attempt))
    digest = sha256_file(attempt_path)
    reference["manifest_sha256"] = digest
    reference["checkpoint_before_sha256"] = attempt[
        "checkpoint_before_sha256"
    ]
    reference["history_chain_before_sha256"] = attempt[
        "history_chain_before_sha256"
    ]
    cut = checkpoint["cuts"][0]
    cut["source_attempt_manifest_sha256"] = digest
    checkpoint["history_chain_sha256"] = _history_chain_step(
        reference["history_chain_before_sha256"],
        attempt_reference=reference,
        cut_record=cut,
        status_value="running",
        terminal=None,
    )
    atomic_write(checkpoint_path, canonical_json_bytes(checkpoint))


def tree_snapshot(root: Path) -> tuple[tuple[str, str, str | None], ...]:
    records = []
    for path in sorted(root.rglob("*")):
        relative = str(path.relative_to(root))
        if path.is_file():
            records.append((relative, "file", sha256_file(path)))
        elif path.is_dir():
            records.append((relative, "directory", None))
        elif path.is_symlink():
            records.append((relative, "symlink", os.readlink(path)))
        else:
            records.append((relative, "other", None))
    return tuple(records)


class ExactFormatTests(unittest.TestCase):
    def test_coloring_canonicalization_quotients_global_permutations(self) -> None:
        first = (0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2)
        permuted = (2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1)
        self.assertEqual(canonical_coloring(first), first)
        self.assertEqual(canonical_coloring(permuted), first)
        with self.assertRaises(ValueError):
            canonical_coloring((True,) * N)
        with self.assertRaises(ValueError):
            canonical_coloring((0,) * (N - 1))

    def test_exact_dimacs_parser(self) -> None:
        parsed = parse_dimacs_bytes(
            b"p cnf 3 3\n1 -2 0\n2 3 0\n-1 0\n"
        )
        self.assertEqual(parsed.variable_count, 3)
        self.assertEqual(parsed.clauses, ((1, -2), (2, 3), (-1,)))
        malformed = (
            b"p cnf 3 2\n1 0\n",
            b"p cnf 3 1\r\n1 0\r\n",
            b"p cnf 3 1\n1 0 2\n",
            b"p cnf 3 1\n4 0\n",
            b"p cnf 3 1\n1 1 0\n",
            b"p cnf 3 1\n1 -1 0\n",
            b"c comment\np cnf 1 0\n",
            b"p cnf 01 0\n",
        )
        for payload in malformed:
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError):
                    parse_dimacs_bytes(payload)

    def test_exact_wrapped_model_parser(self) -> None:
        result = parse_solver_result_bytes(
            b"s SATISFIABLE\nv 1 -2\nv 3 -4 0\n",
            4,
        )
        self.assertEqual(
            result.model,
            {1: True, 2: False, 3: True, 4: False},
        )
        self.assertEqual(
            parse_solver_result_bytes(b"s UNSATISFIABLE\n", 4).status,
            "UNSAT",
        )
        malformed = (
            b"s SATISFIABLE\nv 1 -2 3 0\n",
            b"s SATISFIABLE\nv 1 -2 2 -4 0\n",
            b"s SATISFIABLE\nv 1 -2 3 -4\n",
            b"s SATISFIABLE\nv 1 0\nv -2 3 -4 0\n",
            b"s SATISFIABLE\nv 1 -2 3 -4 -0\n",
            b"s UNSATISFIABLE\nv 1 -2 3 -4 0\n",
            b"s UNKNOWN\ns UNKNOWN\n",
        )
        for payload in malformed:
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError):
                    parse_solver_result_bytes(payload, 4)

    def test_direct_clause_evaluation_rejects_false_model(self) -> None:
        parsed = parse_dimacs_bytes(b"p cnf 2 2\n1 2 0\n-1 0\n")
        validate_model_satisfies_cnf(parsed, {1: False, 2: True})
        with self.assertRaisesRegex(ValueError, "falsifies"):
            validate_model_satisfies_cnf(
                parsed, {1: True, 2: False}
            )
        with self.assertRaisesRegex(ValueError, "domain"):
            validate_model_satisfies_cnf(parsed, {1: False})


class ResourceAndPathTests(unittest.TestCase):
    def test_bounded_child_records_command_logs_wall_cpu_and_rss(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            stdout = root / "stdout"
            stderr = root / "stderr"
            result = run_bounded_child(
                command=(
                    str(Path(sys.executable).resolve()),
                    "-c",
                    "import time; time.sleep(0.05)",
                ),
                cwd=root,
                stdout_path=stdout,
                stderr_path=stderr,
                wall_limit_seconds=2,
                memory_limit_mib=128,
                readonly_paths={},
            )
            self.assertEqual(result.exit_code, 0)
            self.assertFalse(result.timed_out)
            self.assertFalse(result.memory_limit_exceeded)
            self.assertGreater(result.wall_seconds, 0)
            self.assertGreater(
                result.maximum_resident_set_size_mib, 0
            )
            self.assertEqual(result.stdout_sha256, sha256_file(stdout))
            self.assertEqual(result.stderr_sha256, sha256_file(stderr))
            self.assertEqual(
                result.command_sha256,
                sha256_bytes(
                    canonical_json_bytes(list(result.command), pretty=False)
                ),
            )

    @unittest.skipUnless(sys.platform == "darwin", "macOS libproc RSS gate")
    def test_macos_memory_ceiling_kills_an_oversized_child(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            result = run_bounded_child(
                command=(
                    str(Path(sys.executable).resolve()),
                    "-c",
                    "import time; x=bytearray(96<<20); time.sleep(2)",
                ),
                cwd=root,
                stdout_path=root / "stdout",
                stderr_path=root / "stderr",
                wall_limit_seconds=3,
                memory_limit_mib=64,
                readonly_paths={},
            )
            self.assertTrue(result.memory_limit_exceeded)
            self.assertFalse(result.timed_out)
            self.assertLess(result.exit_code, 0)
            self.assertGreater(
                result.peak_polled_resident_set_size_mib, 64
            )

    def test_path_roles_reject_direct_symlink_and_hardlink_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            source = root / "source"
            source.write_bytes(b"trusted")
            with self.assertRaises(ValueError):
                validate_file_roles(
                    readonly={"source": source},
                    writable={"output": source},
                )

            symbolic = root / "symbolic"
            symbolic.symlink_to(source)
            with self.assertRaises(ValueError):
                validate_file_roles(
                    readonly={"source": source},
                    writable={"output": symbolic},
                )
            self.assertEqual(source.read_bytes(), b"trusted")

            hard = root / "hard"
            os.link(source, hard)
            with self.assertRaises(ValueError):
                validate_file_roles(
                    readonly={"source": source},
                    writable={"output": hard},
                )
            self.assertEqual(source.read_bytes(), b"trusted")

    def test_configuration_rejects_protected_or_excessive_run(self) -> None:
        with self.assertRaisesRegex(ValueError, "protected"):
            configuration(ROOT / "src" / "forbidden-run")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            with self.assertRaisesRegex(ValueError, "75%"):
                build_configuration(
                    template="hole5",
                    run_directory=root,
                    cadical_path=CADICAL,
                    drat_trim_path=DRAT_TRIM,
                    solver_seed=0,
                    solver_wall_seconds=10,
                    solver_memory_mib=1 << 20,
                    checker_wall_seconds=10,
                    checker_memory_mib=1024,
                )

    def test_attempt_directory_creation_is_parent_fsynced(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run_directory = root / "run"
            run_directory.mkdir()
            with mock.patch(
                "synthesis_k3.cegar._fsync_directory",
                wraps=__import__(
                    "synthesis_k3.cegar", fromlist=["_fsync_directory"]
                )._fsync_directory,
            ) as synced:
                attempt = _new_attempt_directory(run_directory, 0)
            attempts_parent = (run_directory / "attempts").resolve()
            self.assertTrue(attempt.is_dir())
            self.assertIn(
                attempts_parent,
                [call.args[0].resolve() for call in synced.call_args_list],
            )

    def test_campaign_lock_and_sigterm_cleanup_leave_no_child(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            pid_path = root / "grandchild.pid"
            helper = (
                "from pathlib import Path\n"
                "import sys\n"
                "from synthesis_k3.cegar import run_bounded_child\n"
                "root=Path(sys.argv[1]); pidfile=root/'grandchild.pid'\n"
                "code='import os,sys,time; from pathlib import Path; "
                "Path(sys.argv[1]).write_text(str(os.getpid())); time.sleep(30)'\n"
                "run_bounded_child(command=(str(Path(sys.executable).resolve()),"
                "'-c',code,str(pidfile)),cwd=root,stdout_path=root/'child.out',"
                "stderr_path=root/'child.err',wall_limit_seconds=30,"
                "memory_limit_mib=128,readonly_paths={})\n"
            )
            environment = dict(os.environ)
            environment["PYTHONPATH"] = str(ROOT / "src")
            parent = subprocess.Popen(
                [sys.executable, "-c", helper, str(root)],
                env=environment,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            child_pid: int | None = None
            try:
                deadline = time.monotonic() + 5
                while time.monotonic() < deadline and not pid_path.exists():
                    time.sleep(0.02)
                self.assertTrue(pid_path.is_file())
                child_pid = int(pid_path.read_text(encoding="ascii"))
                with self.assertRaisesRegex(RuntimeError, "campaign solver"):
                    run_bounded_child(
                        command=(
                            str(Path(sys.executable).resolve()),
                            "-c",
                            "pass",
                        ),
                        cwd=root,
                        stdout_path=root / "blocked.stdout",
                        stderr_path=root / "blocked.stderr",
                        wall_limit_seconds=2,
                        memory_limit_mib=128,
                        readonly_paths={},
                    )
                parent.terminate()
                parent.wait(timeout=5)
                deadline = time.monotonic() + 2
                while time.monotonic() < deadline:
                    try:
                        os.kill(child_pid, 0)
                    except ProcessLookupError:
                        break
                    time.sleep(0.02)
                else:
                    self.fail("setsid child survived orchestrator SIGTERM")
            finally:
                if parent.poll() is None:
                    parent.kill()
                    parent.wait(timeout=5)
                if child_pid is not None:
                    try:
                        os.killpg(child_pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass


@unittest.skipUnless(
    CADICAL.is_file()
    and DRAT_TRIM.is_file()
    and sha256_file(CADICAL) == CADICAL_BINARY_SHA256
    and sha256_file(DRAT_TRIM) == DRAT_TRIM_BINARY_SHA256,
    "pinned local SAT tools are unavailable",
)
class PinnedToolSmokeTests(unittest.TestCase):
    def test_trivial_unsat_is_rerun_and_verified_by_drat_trim(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            config = configuration(root)
            cnf = root / "tiny-unsat.cnf"
            atomic_write(cnf, b"p cnf 1 2\n1 0\n-1 0\n")
            parsed = parse_dimacs_file(cnf)
            proof_solver, checker, artifacts = run_unsat_proof_replay(
                configuration=config,
                cnf_path=cnf,
                parsed_cnf=parsed,
                attempt_directory=root,
            )
            self.assertEqual(proof_solver.exit_code, 20)
            self.assertEqual(checker.exit_code, 0)
            self.assertIn("-f", checker.command)
            self.assertIn("-W", checker.command)
            self.assertIn("-I", checker.command)
            self.assertGreater(artifacts["drat_proof"].stat().st_size, 0)
            checker_text = artifacts["checker_stdout"].read_text(
                encoding="ascii"
            )
            self.assertEqual(
                [
                    line.strip()
                    for line in checker_text.splitlines()
                    if line.strip() == "s VERIFIED"
                ],
                ["s VERIFIED"],
            )
            self.assertNotIn("WARNING", checker_text)
            reaudit = verify_stored_drat_certificate(
                configuration=config,
                cnf_path=cnf,
                proof_path=artifacts["drat_proof"],
            )
            self.assertEqual(reaudit.exit_code, 0)

    def test_bounded_multi_iteration_resume_and_full_audit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            first = run_cegar(
                **run_kwargs(root),
                max_iterations=2,
            )
            self.assertEqual(first.status, "iteration_budget_exhausted")
            self.assertEqual(first.cut_count, 2)
            self.assertEqual(first.attempt_count, 2)

            checkpoint = strict_json_file(root / CHECKPOINT_NAME)
            self.assertIsInstance(checkpoint, dict)
            assert isinstance(checkpoint, dict)
            colorings = [
                tuple(record["coloring"])
                for record in checkpoint["cuts"]
            ]
            self.assertEqual(len(colorings), len(set(colorings)))
            self.assertEqual(
                checkpoint["cuts_payload_sha256"],
                sha256_bytes(cuts_payload_bytes(checkpoint["cuts"])),
            )
            first_attempt = strict_json_file(
                Path(checkpoint["attempts"][0]["manifest_path"])
            )
            self.assertIsInstance(first_attempt, dict)
            assert isinstance(first_attempt, dict)
            self.assertTrue(
                first_attempt["validation"][
                    "decoded_candidate_directly_validated"
                ]
            )
            solver_record = first_attempt["initial_solver"]
            self.assertEqual(
                solver_record["command_sha256"],
                sha256_bytes(
                    canonical_json_bytes(
                        solver_record["command"], pretty=False
                    )
                ),
            )
            self.assertGreater(
                solver_record["maximum_resident_set_size_mib"], 0
            )
            self.assertEqual(
                set(first_attempt["reconstructible_artifacts"]),
                {"cuts_input", "cnf"},
            )
            self.assertFalse(
                Path(
                    first_attempt["reconstructible_artifacts"]["cnf"][
                        "raw_path"
                    ]
                ).exists()
            )
            self.assertIn(
                "solver_result", first_attempt["compressed_artifacts"]
            )
            attempt_directory = Path(
                checkpoint["attempts"][0]["manifest_path"]
            ).parent
            retained_bytes = sum(
                path.stat().st_size
                for path in attempt_directory.iterdir()
                if path.is_file()
            )
            self.assertLess(retained_bytes, 100_000)
            self.assertGreater(
                first_attempt["reconstructible_artifacts"]["cnf"][
                    "raw_size_bytes"
                ],
                500_000,
            )

            import synthesis_k3.cegar as cegar_module

            with mock.patch(
                "synthesis_k3.cegar.build_k3_encoding",
                wraps=cegar_module.build_k3_encoding,
            ) as built:
                audit = audit_run(
                    **run_kwargs(root),
                    deep_reconstruct=True,
                )
            self.assertEqual(audit.status, "running_audit_passed")
            self.assertEqual(built.call_count, 2)
            resumed = run_cegar(
                **run_kwargs(root),
                max_iterations=2,
            )
            self.assertEqual(resumed.status, "iteration_budget_exhausted")
            self.assertEqual(resumed.cut_count, 4)
            self.assertEqual(resumed.attempt_count, 4)

    def test_one_session_validates_history_once_and_honors_wall_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            import synthesis_k3.cegar as cegar_module

            with mock.patch(
                "synthesis_k3.cegar.validate_checkpoint_payload",
                wraps=cegar_module.validate_checkpoint_payload,
            ) as validated:
                outcome = run_cegar(
                    **run_kwargs(root),
                    max_iterations=3,
                )
            self.assertEqual(outcome.cut_count, 3)
            self.assertEqual(validated.call_count, 1)
            instrumentation = AuditInstrumentation()
            with mock.patch(
                "synthesis_k3.cegar.validate_model_satisfies_encoding_prefix",
                side_effect=AssertionError(
                    "ordinary history audit must not scan cut prefixes"
                ),
            ):
                audited = audit_run(
                    **run_kwargs(root),
                    instrumentation=instrumentation,
                )
            self.assertEqual(audited.status, "running_audit_passed")
            self.assertEqual(
                instrumentation.attempt_semantic_validations, 3
            )
            self.assertEqual(
                instrumentation.historical_sat_base_cnf_validations, 3
            )
            self.assertEqual(
                instrumentation.historical_own_cut_validations, 3
            )
            self.assertEqual(
                instrumentation.cut_ledger_record_validations, 3
            )
            self.assertEqual(
                instrumentation.decisive_cnf_reconstructions, 0
            )

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            wall_kwargs = run_kwargs(root)
            wall_kwargs.update(
                solver_wall_seconds=1,
                checker_wall_seconds=1,
                session_wall_seconds=1,
            )
            outcome = run_cegar(
                **wall_kwargs,
                max_iterations=50,
            )
            self.assertEqual(outcome.status, "session_wall_exhausted")
            self.assertEqual(outcome.attempt_count, 0)
            self.assertEqual(
                audit_run(
                    **wall_kwargs,
                ).status,
                "running_audit_passed",
            )

    def test_rebound_cross_field_mutations_are_rejected_semantically(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run_cegar(**run_kwargs(root), max_iterations=1)
            checkpoint_path = root / CHECKPOINT_NAME
            checkpoint = load_object(checkpoint_path)
            attempt_path = Path(checkpoint["attempts"][0]["manifest_path"])
            checkpoint_before = checkpoint_path.read_bytes()
            attempt_before = attempt_path.read_bytes()

            def extra_flag(attempt):
                command = attempt["initial_solver"]["command"]
                command.append("--hostile-unrecognized-option")
                attempt["initial_solver"]["command_sha256"] = sha256_bytes(
                    canonical_json_bytes(command, pretty=False)
                )

            def falsify_auxiliary_clause(attempt):
                record = attempt["compressed_artifacts"]["solver_result"]
                gzip_path = Path(record["gzip_path"])
                raw = gzip.decompress(gzip_path.read_bytes())
                encoding = build_k3_encoding("hole5")
                parsed = parse_solver_result_bytes(
                    raw, encoding.cnf.variable_count
                )
                model = dict(parsed.model)
                protected = set(encoding.edge_variables.values()) | set(
                    encoding.family_variables.values()
                )
                for clause in encoding.cnf.clauses:
                    true_literals = [
                        literal
                        for literal in clause
                        if model[abs(literal)] == (literal > 0)
                    ]
                    if (
                        len(true_literals) == 1
                        and abs(true_literals[0]) not in protected
                    ):
                        literal = true_literals[0]
                        model[abs(literal)] = literal < 0
                        break
                else:
                    raise AssertionError(
                        "no singly supported auxiliary clause found"
                    )
                rewritten = (
                    "s SATISFIABLE\nv "
                    + " ".join(
                        str(variable if model[variable] else -variable)
                        for variable in range(
                            1, encoding.cnf.variable_count + 1
                        )
                    )
                    + " 0\n"
                ).encode("ascii")
                packed = gzip.compress(rewritten, compresslevel=9, mtime=0)
                gzip_path.write_bytes(packed)
                record["raw_sha256"] = sha256_bytes(rewritten)
                record["raw_size_bytes"] = len(rewritten)
                record["gzip_sha256"] = sha256_bytes(packed)
                record["gzip_size_bytes"] = len(packed)

            mutations = (
                (
                    lambda attempt: attempt.update(
                        checkpoint_before_sha256="not-a-sha256"
                    ),
                    "predecessor",
                ),
                (
                    lambda attempt: attempt["initial_solver"].update(
                        wall_limit_seconds=-1,
                        memory_limit_mib=-1,
                        file_limit_mib=-1,
                    ),
                    "status/limits",
                ),
                (
                    lambda attempt: attempt["initial_solver"].update(
                        exit_code=20
                    ),
                    "SAT outcome",
                ),
                (extra_flag, "command"),
                (
                    lambda attempt: attempt["artifacts"].update(
                        decoded_candidate=dict(
                            attempt["artifacts"]["coloring"]
                        )
                    ),
                    "noncanonical|alias",
                ),
                (falsify_auxiliary_clause, "falsifies CNF clause"),
            )
            for mutate, expected_error in mutations:
                with self.subTest(mutation=repr(mutate)):
                    atomic_write(attempt_path, attempt_before)
                    atomic_write(checkpoint_path, checkpoint_before)
                    rebind_first_attempt_and_history(root, mutate)
                    with self.assertRaisesRegex(
                        (ValueError, RuntimeError), expected_error
                    ):
                        audit_run(**run_kwargs(root), deep_reconstruct=True)
            atomic_write(attempt_path, attempt_before)
            atomic_write(checkpoint_path, checkpoint_before)

    def test_every_attempt_binds_the_prior_logical_checkpoint(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run_cegar(**run_kwargs(root), max_iterations=2)
            checkpoint_path = root / CHECKPOINT_NAME
            checkpoint = load_object(checkpoint_path)
            first_reference = checkpoint["attempts"][0]
            second_reference = checkpoint["attempts"][1]
            first_cut = checkpoint["cuts"][0]
            first_history = _history_chain_step(
                first_reference["history_chain_before_sha256"],
                attempt_reference=first_reference,
                cut_record=first_cut,
                status_value="running",
                terminal=None,
            )
            prior_checkpoint = dict(checkpoint)
            prior_checkpoint.update(
                status="running",
                attempts=[first_reference],
                cuts=[first_cut],
                cuts_payload_sha256=sha256_bytes(
                    cuts_payload_bytes([first_cut])
                ),
                history_chain_sha256=first_history,
                terminal=None,
            )
            self.assertEqual(
                second_reference["checkpoint_before_sha256"],
                checkpoint_state_sha256(prior_checkpoint),
            )

            second_attempt_path = Path(
                second_reference["manifest_path"]
            )
            second_attempt = load_object(second_attempt_path)
            forged_before = "0" * 64
            self.assertNotEqual(
                forged_before,
                checkpoint_state_sha256(prior_checkpoint),
            )
            second_attempt["checkpoint_before_sha256"] = forged_before
            atomic_write(
                second_attempt_path,
                canonical_json_bytes(second_attempt),
            )
            second_hash = sha256_file(second_attempt_path)
            second_reference["checkpoint_before_sha256"] = forged_before
            second_reference["manifest_sha256"] = second_hash
            checkpoint["cuts"][1][
                "source_attempt_manifest_sha256"
            ] = second_hash
            history = checkpoint["attempts"][0][
                "history_chain_before_sha256"
            ]
            cuts_by_source = {
                cut["source_attempt_index"]: cut
                for cut in checkpoint["cuts"]
            }
            for reference in checkpoint["attempts"]:
                history = _history_chain_step(
                    history,
                    attempt_reference=reference,
                    cut_record=cuts_by_source.get(reference["index"]),
                    status_value="running",
                    terminal=None,
                )
            checkpoint["history_chain_sha256"] = history
            atomic_write(
                checkpoint_path,
                canonical_json_bytes(checkpoint),
            )
            with self.assertRaisesRegex(
                ValueError, "checkpoint-before chronology"
            ):
                audit_run(**run_kwargs(root))

    def test_terminal_attempt_outcomes_are_only_final(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run_cegar(**run_kwargs(root), max_iterations=2)
            checkpoint_path = root / CHECKPOINT_NAME
            original = checkpoint_path.read_bytes()
            for outcome in (
                "candidate_review_pending",
                "unsat_verified",
            ):
                with self.subTest(outcome=outcome):
                    checkpoint = load_object(checkpoint_path)
                    checkpoint["attempts"][0]["outcome"] = outcome
                    atomic_write(
                        checkpoint_path,
                        canonical_json_bytes(checkpoint),
                    )
                    with self.assertRaisesRegex(
                        ValueError,
                        "only as the final matching terminal attempt",
                    ):
                        audit_run(**run_kwargs(root))
                    atomic_write(checkpoint_path, original)

    def test_full_sat_to_unsat_terminal_forgery_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run_cegar(**run_kwargs(root), max_iterations=1)
            checkpoint_path = root / CHECKPOINT_NAME
            checkpoint = load_object(checkpoint_path)
            reference = checkpoint["attempts"][0]
            attempt_path = Path(reference["manifest_path"])
            attempt = load_object(attempt_path)
            attempt["outcome"] = "unsat_verified"
            attempt.pop("committed_cut")
            attempt["validation"] = {
                "initial_unsat": True,
                "identical_cnf_rerun": True,
                "proof_rerun_unsat": True,
                "drat_trim_flags": ["-I", "-f", "-W"],
                "drat_trim_exact_verified_line": True,
                "drat_trim_warning_free": True,
                "cnf_unchanged": True,
                "proof_unchanged_during_check": True,
            }
            artifacts = attempt["artifacts"]
            compressed = attempt["compressed_artifacts"]
            reconstructible = attempt["reconstructible_artifacts"]
            artifacts["drat_proof"] = dict(artifacts["coloring"])
            artifacts["proof_result"] = dict(artifacts["coloring"])
            for new_role, old_role in (
                ("proof_solver_stdout", "solver_stdout"),
                ("checker_stdout", "solver_stdout"),
                ("proof_solver_stderr", "solver_stderr"),
                ("checker_stderr", "solver_stderr"),
            ):
                compressed[new_role] = dict(compressed[old_role])

            cnf_path = reconstructible["cnf"]["raw_path"]
            proof_path = artifacts["drat_proof"]["path"]
            proof_solver = copy.deepcopy(attempt["initial_solver"])
            proof_solver["exit_code"] = 20
            proof_solver["command"] = [
                str(CADICAL.resolve()),
                "--seed=0",
                "-t",
                "10",
                cnf_path,
                proof_path,
            ]
            proof_solver["command_sha256"] = sha256_bytes(
                canonical_json_bytes(
                    proof_solver["command"], pretty=False
                )
            )
            proof_solver["stdout_path"] = compressed[
                "proof_solver_stdout"
            ]["raw_path"]
            proof_solver["stdout_sha256"] = compressed[
                "proof_solver_stdout"
            ]["raw_sha256"]
            proof_solver["stderr_path"] = compressed[
                "proof_solver_stderr"
            ]["raw_path"]
            proof_solver["stderr_sha256"] = compressed[
                "proof_solver_stderr"
            ]["raw_sha256"]

            proof_checker = copy.deepcopy(attempt["initial_solver"])
            proof_checker["exit_code"] = 0
            proof_checker["command"] = [
                str(DRAT_TRIM.resolve()),
                cnf_path,
                proof_path,
                "-I",
                "-f",
                "-W",
            ]
            proof_checker["command_sha256"] = sha256_bytes(
                canonical_json_bytes(
                    proof_checker["command"], pretty=False
                )
            )
            proof_checker["executable_sha256_before"] = (
                DRAT_TRIM_BINARY_SHA256
            )
            proof_checker["executable_sha256_after"] = (
                DRAT_TRIM_BINARY_SHA256
            )
            proof_checker["stdout_path"] = compressed["checker_stdout"][
                "raw_path"
            ]
            proof_checker["stdout_sha256"] = compressed["checker_stdout"][
                "raw_sha256"
            ]
            proof_checker["stderr_path"] = compressed["checker_stderr"][
                "raw_path"
            ]
            proof_checker["stderr_sha256"] = compressed["checker_stderr"][
                "raw_sha256"
            ]
            attempt["proof_solver"] = proof_solver
            attempt["proof_checker"] = proof_checker
            atomic_write(attempt_path, canonical_json_bytes(attempt))
            attempt_hash = sha256_file(attempt_path)
            reference["outcome"] = "unsat_verified"
            reference["manifest_sha256"] = attempt_hash
            checkpoint["cuts"] = []
            checkpoint["cuts_payload_sha256"] = sha256_bytes(b"[]\n")
            checkpoint["status"] = "unsat_verified"

            marker_path = root / UNSAT_MARKER_NAME
            marker = {
                "schema": "gamma-theta-k3-cegar-terminal-v2",
                "schema_version": 2,
                "kind": "unsat",
                "status": "unsat_verified",
                "configuration_sha256": checkpoint[
                    "configuration_sha256"
                ],
                "run_manifest_sha256": checkpoint["run_manifest_sha256"],
                "checkpoint_before_sha256": attempt[
                    "checkpoint_before_sha256"
                ],
                "history_chain_before_sha256": attempt[
                    "history_chain_before_sha256"
                ],
                "attempt_manifest_path": str(attempt_path.resolve()),
                "attempt_manifest_sha256": attempt_hash,
            }
            atomic_write(marker_path, canonical_json_bytes(marker))
            terminal = {
                "kind": "unsat",
                "path": str(marker_path.resolve()),
                "sha256": sha256_file(marker_path),
            }
            checkpoint["terminal"] = terminal
            checkpoint["history_chain_sha256"] = _history_chain_step(
                reference["history_chain_before_sha256"],
                attempt_reference=reference,
                cut_record=None,
                status_value="unsat_verified",
                terminal=terminal,
            )
            atomic_write(checkpoint_path, canonical_json_bytes(checkpoint))
            with self.assertRaises((ValueError, RuntimeError)):
                audit_run(**run_kwargs(root), deep_reconstruct=True)

    def test_candidate_marker_blocks_every_later_solver_call(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            with mock.patch(
                "synthesis_k3.cegar.find_coloring", return_value=None
            ):
                first = run_cegar(
                    **run_kwargs(root),
                    max_iterations=1,
                )
            self.assertEqual(first.status, "candidate_review_pending")
            marker = root / CANDIDATE_MARKER_NAME
            self.assertTrue(marker.is_file())
            before = sha256_file(root / CHECKPOINT_NAME)
            with mock.patch(
                "synthesis_k3.cegar.run_bounded_child",
                side_effect=AssertionError("solver must not be called"),
            ):
                with self.assertRaisesRegex(ValueError, "three-colorable"):
                    run_cegar(
                        **run_kwargs(root),
                        max_iterations=10,
                    )
            self.assertEqual(sha256_file(root / CHECKPOINT_NAME), before)

    def test_resume_rejects_tampered_model_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run_cegar(**run_kwargs(root), max_iterations=1)
            checkpoint = strict_json_file(root / CHECKPOINT_NAME)
            assert isinstance(checkpoint, dict)
            attempt = strict_json_file(
                Path(checkpoint["attempts"][0]["manifest_path"])
            )
            assert isinstance(attempt, dict)
            model = Path(
                attempt["compressed_artifacts"]["solver_result"][
                    "gzip_path"
                ]
            )
            model.write_bytes(model.read_bytes() + b"tamper")
            with self.assertRaisesRegex(ValueError, "compressed binding"):
                audit_run(**run_kwargs(root))

    def test_resume_rejects_duplicate_partition_even_if_hash_rebound(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run_cegar(**run_kwargs(root), max_iterations=1)
            checkpoint_path = root / CHECKPOINT_NAME
            checkpoint = strict_json_file(checkpoint_path)
            assert isinstance(checkpoint, dict)
            duplicate = dict(checkpoint["cuts"][0])
            duplicate["index"] = 1
            checkpoint["cuts"].append(duplicate)
            checkpoint["cuts_payload_sha256"] = sha256_bytes(
                cuts_payload_bytes(checkpoint["cuts"])
            )
            atomic_write(
                checkpoint_path,
                canonical_json_bytes(checkpoint),
            )
            with self.assertRaisesRegex(ValueError, "repeats|differs"):
                audit_run(**run_kwargs(root))

    def test_disk_preflight_refuses_to_invade_the_reserve(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            config = configuration(root)
            report = disk_preflight(config, 2)
            self.assertEqual(
                report["terminal_workspace_budget_bytes"],
                9 * config.child_file_limit_mib * (1 << 20),
            )
            self.assertEqual(
                report["retained_session_budget_bytes"],
                2 * config.retained_attempt_limit_mib * (1 << 20),
            )
            free_mib = shutil.disk_usage(root).free // (1 << 20)
            with self.assertRaisesRegex(RuntimeError, "disk preflight"):
                run_cegar(
                    **run_kwargs(root),
                    max_iterations=1,
                    disk_reserve_mib=free_mib + 1,
                )
            self.assertFalse((root / "run_manifest.json").exists())

    def test_audit_is_read_only_and_never_initializes_a_run(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            empty = Path(temporary).resolve()
            before = tree_snapshot(empty)
            with self.assertRaisesRegex(ValueError, "run lock"):
                audit_run(**run_kwargs(empty))
            self.assertEqual(tree_snapshot(empty), before)

        with tempfile.TemporaryDirectory() as temporary:
            running = Path(temporary).resolve()
            run_cegar(**run_kwargs(running), max_iterations=2)
            before = tree_snapshot(running)
            self.assertEqual(
                audit_run(**run_kwargs(running)).status,
                "running_audit_passed",
            )
            self.assertEqual(tree_snapshot(running), before)

        with tempfile.TemporaryDirectory() as temporary:
            terminal = Path(temporary).resolve()
            with mock.patch(
                "synthesis_k3.cegar.find_coloring", return_value=None
            ):
                run_cegar(**run_kwargs(terminal), max_iterations=1)
                before = tree_snapshot(terminal)
                instrumentation = AuditInstrumentation()
                self.assertEqual(
                    audit_run(
                        **run_kwargs(terminal),
                        instrumentation=instrumentation,
                    ).status,
                    "candidate_review_pending",
                )
                self.assertEqual(
                    instrumentation.decisive_cnf_reconstructions, 1
                )
            self.assertEqual(tree_snapshot(terminal), before)


class CommandLineGateTests(unittest.TestCase):
    def test_cli_requires_explicit_validation_gate_for_solving(self) -> None:
        from synthesis_k3.cegar import main

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            with self.assertRaisesRegex(SystemExit, "validation-gate-open"):
                main(
                    [
                        "--template",
                        "hole5",
                        "--run-dir",
                        str(root),
                    ]
                )


if __name__ == "__main__":
    unittest.main()
