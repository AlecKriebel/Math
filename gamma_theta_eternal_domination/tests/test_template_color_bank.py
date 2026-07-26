from __future__ import annotations

import json
import signal
import shutil
import subprocess
import sys
import tempfile
import unittest
from itertools import combinations, product
from pathlib import Path
from unittest.mock import patch


CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from synthesis_k3.cegar import ChildResult  # noqa: E402
from synthesis_k3.encoding import build_k3_encoding, same_color_cut  # noqa: E402
from synthesis_k3.template_color_bank import (  # noqa: E402
    BANK_NAME,
    BANK_TEMPLATES,
    CADICAL_BINARY_SHA256,
    CNF_NAME,
    DRAT_TRIM_BINARY_SHA256,
    EXPECTED_BANK_COUNTS,
    EXPECTED_BASE_CNF_COUNTS,
    EXPECTED_CNF_COUNTS,
    MANIFEST_NAME,
    audit_package,
    bank_clause_stream_bytes,
    canonicalize_color_names,
    enumerate_bank,
    first_use_canonical,
    generate_package,
    live_tool_smoke,
    positive_template_edges,
    row_is_template_proper,
    sha256_bytes,
    sha256_file,
    solve_package,
    validate_bank,
)


CADICAL = CAMPAIGN / "tools/cadical_3_0_1/build/cadical"
DRAT_TRIM = CAMPAIGN / "tools/drat_trim_2023_05_22/drat-trim"


class TemplateColorBankTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = {template: enumerate_bank(template) for template in BANK_TEMPLATES}

    def test_exact_counts_order_canonicality_and_forced_edges(self) -> None:
        for template in BANK_TEMPLATES:
            with self.subTest(template=template):
                rows = self.rows[template]
                self.assertEqual(len(rows), EXPECTED_BANK_COUNTS[template])
                self.assertEqual(rows, tuple(sorted(rows)))
                self.assertEqual(len(rows), len(set(rows)))
                for row in rows:
                    self.assertEqual(first_use_canonical(row), row)
                    self.assertTrue(row_is_template_proper(template, row))
                    self.assertEqual(set(row), {0, 1, 2})

    def test_bruteforce_labeled_colorings_have_exactly_the_bank_orbits(self) -> None:
        # This oracle intentionally does not call enumerate_bank's recursion.
        for template in BANK_TEMPLATES:
            with self.subTest(template=template):
                edges = positive_template_edges(template)
                oracle = {
                    canonicalize_color_names(row)
                    for row in product(range(3), repeat=12)
                    if all(row[u] != row[v] for u, v in edges)
                }
                self.assertEqual(oracle, set(self.rows[template]))

    def test_cut_truth_is_exact_coloring_failure(self) -> None:
        # Exhaust every optional edge assignment on a small 5-vertex universe.
        encoding = build_k3_encoding("hole5")
        row = self.rows["hole5"][0]
        universe = tuple(combinations(range(5), 2))
        clause_pairs = {
            pair
            for pair, variable in encoding.edge_variables.items()
            if variable in same_color_cut(encoding, row)
        }
        for mask in range(1 << len(universe)):
            edges = {
                pair for index, pair in enumerate(universe) if mask >> index & 1
            }
            clause_truth = bool(edges & clause_pairs)
            proper = all(row[u] != row[v] for u, v in edges)
            self.assertEqual(clause_truth, not proper)

    def test_exact_cnf_counts_and_deterministic_package_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            for template in BANK_TEMPLATES:
                with self.subTest(template=template):
                    first = root / f"{template}-a"
                    second = root / f"{template}-b"
                    completed = subprocess.run(
                        ["git", "rev-parse", "--verify", "HEAD"],
                        cwd=CAMPAIGN,
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    fixed_head = completed.stdout.strip()
                    with patch(
                        "synthesis_k3.template_color_bank._git_head",
                        return_value=fixed_head,
                    ):
                        generate_package(
                            template=template,
                            output_directory=first,
                            validation_gate=True,
                        )
                        generate_package(
                            template=template,
                            output_directory=second,
                            validation_gate=True,
                        )
                    for name in (BANK_NAME, CNF_NAME, MANIFEST_NAME):
                        self.assertEqual(
                            (first / name).read_bytes(),
                            (second / name).read_bytes(),
                        )
                    manifest = json.loads(
                        (first / MANIFEST_NAME).read_text(encoding="utf-8")
                    )
                    variables, clauses, literals = EXPECTED_CNF_COUNTS[template]
                    _, base_clauses, base_literals = EXPECTED_BASE_CNF_COUNTS[
                        template
                    ]
                    self.assertEqual(manifest["variable_count"], variables)
                    self.assertEqual(manifest["clause_count"], clauses)
                    self.assertEqual(manifest["literal_count"], literals)
                    self.assertEqual(
                        manifest["git_source_binding"]["head_commit"],
                        fixed_head,
                    )
                    self.assertFalse(
                        manifest["git_source_binding"][
                            "global_worktree_cleanliness_required"
                        ]
                    )
                    self.assertEqual(
                        manifest["clause_layout"]["base_clause_count"],
                        base_clauses,
                    )
                    self.assertEqual(
                        manifest["clause_layout"]["base_literal_count"],
                        base_literals,
                    )
                    cnf_lines = (first / CNF_NAME).read_bytes().splitlines(
                        keepends=True
                    )
                    self.assertEqual(
                        b"".join(cnf_lines[base_clauses + 1 :]),
                        bank_clause_stream_bytes(template, self.rows[template]),
                    )
                    report = audit_package(first, exhaustive=True)
                    self.assertTrue(report["exhaustive_oracle_checked"])

    def test_generation_gate_existing_output_and_protected_paths_refuse(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            destination = root / "package"
            with self.assertRaises(PermissionError):
                generate_package(
                    template="hole5",
                    output_directory=destination,
                    validation_gate=False,
                )
            self.assertFalse(destination.exists())
            destination.mkdir()
            marker = destination / "keep"
            marker.write_bytes(b"unchanged")
            with self.assertRaises(FileExistsError):
                generate_package(
                    template="hole5",
                    output_directory=destination,
                    validation_gate=True,
                )
            self.assertEqual(marker.read_bytes(), b"unchanged")

        with self.assertRaises(ValueError):
            generate_package(
                template="hole5",
                output_directory=CAMPAIGN / "src/forbidden-bank",
                validation_gate=True,
            )

    def test_symlink_parent_and_malformed_bank_refuse(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            real = root / "real"
            real.mkdir()
            alias = root / "alias"
            alias.symlink_to(real, target_is_directory=True)
            with self.assertRaises(ValueError):
                generate_package(
                    template="hole5",
                    output_directory=alias / "package",
                    validation_gate=True,
                )

            package = root / "valid"
            generate_package(
                template="hole9",
                output_directory=package,
                validation_gate=True,
            )
            bank = package / BANK_NAME
            original = bank.read_bytes()
            bank.write_bytes(b'[[0,1,2], [0,1,2]]\\n')
            with self.assertRaises(ValueError):
                audit_package(package, exhaustive=False)
            bank.write_bytes(original)
            self.assertEqual(audit_package(package, exhaustive=False)["bank_count"], 765)

    def test_bank_validator_rejects_missing_duplicate_unsorted_and_improper(self) -> None:
        rows = self.rows["hole9"]
        cases = (
            rows[:-1],
            rows[:-1] + (rows[0],),
            (rows[1], rows[0], *rows[2:]),
            ((0,) * 12, *rows[1:]),
        )
        for candidate in cases:
            with self.subTest(first=candidate[0]):
                with self.assertRaises(ValueError):
                    validate_bank("hole9", candidate, exhaustive=False)

    def test_solve_refuses_without_gate_before_creating_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            package = root / "package"
            generate_package(
                template="hole9",
                output_directory=package,
                validation_gate=True,
            )
            output = root / "solve"
            with self.assertRaises(PermissionError):
                solve_package(
                    package_directory=package,
                    output_directory=output,
                    cadical_path=CADICAL,
                    drat_trim_path=DRAT_TRIM,
                    seed=0,
                    solver_wall_seconds=1,
                    checker_wall_seconds=1,
                    solver_memory_mib=64,
                    checker_memory_mib=64,
                    file_limit_mib=8,
                    disk_reserve_mib=1,
                    validation_gate=False,
                )
            self.assertFalse(output.exists())

    def test_file_limit_and_checker_failure_leave_explicit_nonclaims(self) -> None:
        def child(
            *,
            exit_code: int,
            termination_signal: int | None,
            stdout_path: Path,
            stderr_path: Path,
        ) -> ChildResult:
            stdout_path.write_bytes(b"")
            stderr_path.write_bytes(b"")
            return ChildResult(
                command=("/pinned/tool",),
                command_sha256=sha256_bytes(b"command"),
                executable_sha256_before=sha256_bytes(b"tool"),
                executable_sha256_after=sha256_bytes(b"tool"),
                exit_code=exit_code,
                termination_signal=termination_signal,
                timed_out=False,
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
                available_memory_before_bytes=1 << 30,
                wall_limit_seconds=10,
                memory_limit_mib=64,
                file_limit_mib=8,
                stdout_path=str(stdout_path),
                stdout_sha256=sha256_file(stdout_path),
                stderr_path=str(stderr_path),
                stderr_sha256=sha256_file(stderr_path),
            )

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            package = root / "package"
            generate_package(
                template="hole9",
                output_directory=package,
                validation_gate=True,
            )

            def file_limit_child(**keywords: object) -> ChildResult:
                return child(
                    exit_code=-int(signal.SIGXFSZ),
                    termination_signal=int(signal.SIGXFSZ),
                    stdout_path=keywords["stdout_path"],  # type: ignore[arg-type]
                    stderr_path=keywords["stderr_path"],  # type: ignore[arg-type]
                )

            file_output = root / "file-limit"
            with patch(
                "synthesis_k3.template_color_bank.run_bounded_child",
                side_effect=file_limit_child,
            ):
                file_outcome = solve_package(
                    package_directory=package,
                    output_directory=file_output,
                    cadical_path=CADICAL,
                    drat_trim_path=DRAT_TRIM,
                    seed=0,
                    solver_wall_seconds=10,
                    checker_wall_seconds=10,
                    solver_memory_mib=64,
                    checker_memory_mib=64,
                    file_limit_mib=8,
                    disk_reserve_mib=1,
                    validation_gate=True,
                )
            self.assertEqual(
                file_outcome["status"], "INCONCLUSIVE_SOLVER_FILE_LIMIT"
            )
            self.assertEqual(
                file_outcome["claim_status"], "NO_MATHEMATICAL_CLAIM"
            )
            self.assertTrue((file_output / "outcome.json").is_file())

            calls = 0

            def failed_checker(**keywords: object) -> ChildResult:
                nonlocal calls
                calls += 1
                stdout_path = keywords["stdout_path"]
                stderr_path = keywords["stderr_path"]
                if calls == 1:
                    command = keywords["command"]
                    result_index = command.index("-w") + 1
                    Path(command[result_index]).write_text(
                        "s UNSATISFIABLE\n", encoding="ascii"
                    )
                    Path(command[-1]).write_bytes(b"0\n")
                    return child(
                        exit_code=20,
                        termination_signal=None,
                        stdout_path=stdout_path,
                        stderr_path=stderr_path,
                    )
                return child(
                    exit_code=1,
                    termination_signal=None,
                    stdout_path=stdout_path,
                    stderr_path=stderr_path,
                )

            checker_output = root / "checker-failure"
            with patch(
                "synthesis_k3.template_color_bank.run_bounded_child",
                side_effect=failed_checker,
            ):
                checker_outcome = solve_package(
                    package_directory=package,
                    output_directory=checker_output,
                    cadical_path=CADICAL,
                    drat_trim_path=DRAT_TRIM,
                    seed=0,
                    solver_wall_seconds=10,
                    checker_wall_seconds=10,
                    solver_memory_mib=64,
                    checker_memory_mib=64,
                    file_limit_mib=8,
                    disk_reserve_mib=1,
                    validation_gate=True,
                )
            self.assertEqual(
                checker_outcome["status"], "UNSAT_UNVERIFIED_CHECKER_EXIT"
            )
            self.assertEqual(
                checker_outcome["claim_status"], "NO_MATHEMATICAL_CLAIM"
            )
            self.assertTrue((checker_output / "outcome.json").is_file())

    def test_cli_requires_gate_and_does_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary).resolve() / "package"
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "synthesis_k3.template_color_bank",
                    "generate",
                    "--template",
                    "hole9",
                    "--output-dir",
                    str(output),
                ],
                cwd=CAMPAIGN,
                env={"PYTHONPATH": str(CAMPAIGN / "src")},
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertFalse(output.exists())

    @unittest.skipUnless(CADICAL.is_file() and DRAT_TRIM.is_file(), "pinned tools absent")
    def test_live_pinned_solver_and_proof_checker_smoke(self) -> None:
        self.assertEqual(sha256_file(CADICAL), CADICAL_BINARY_SHA256)
        self.assertEqual(sha256_file(DRAT_TRIM), DRAT_TRIM_BINARY_SHA256)
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary).resolve() / "smoke"
            report = live_tool_smoke(
                output_directory=output,
                cadical_path=CADICAL,
                drat_trim_path=DRAT_TRIM,
                validation_gate=True,
            )
            self.assertTrue(report["sat_model_checked"])
            self.assertTrue(report["unsat_proof_checked"])
            self.assertEqual(report["sat_child"]["exit_code"], 10)
            self.assertEqual(report["unsat_child"]["exit_code"], 20)
            self.assertEqual(report["checker_child"]["exit_code"], 0)

    def test_wrong_tool_paths_and_hostile_resource_types_refuse(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            fake = root / "fake-cadical"
            shutil.copyfile(CADICAL, fake)
            fake.chmod(0o755)
            output = root / "smoke"
            with self.assertRaises(ValueError):
                live_tool_smoke(
                    output_directory=output,
                    cadical_path=fake,
                    drat_trim_path=DRAT_TRIM,
                    validation_gate=True,
                )
            self.assertFalse(output.exists())

            package = root / "package"
            generate_package(
                template="hole9",
                output_directory=package,
                validation_gate=True,
            )
            with self.assertRaises(ValueError):
                solve_package(
                    package_directory=package,
                    output_directory=root / "solve",
                    cadical_path=CADICAL,
                    drat_trim_path=DRAT_TRIM,
                    seed=True,
                    solver_wall_seconds=1,
                    checker_wall_seconds=1,
                    solver_memory_mib=64,
                    checker_memory_mib=64,
                    file_limit_mib=8,
                    disk_reserve_mib=1,
                    validation_gate=True,
                )


if __name__ == "__main__":
    unittest.main()
