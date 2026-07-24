#!/usr/bin/env python3
"""Focused tests for partial-assignment exact residual completion."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from extension_sat_solver import parse_dimacs  # noqa: E402
from graph_io import encode_graph6  # noqa: E402
from residual_completion import (  # noqa: E402
    DEFAULT_DRAT_TRIM,
    DEFAULT_LRAT_CHECK,
    DEFAULT_PYSAT_PATH,
    DEFAULT_PYTHON,
    PINNED_HASHES,
    Candidate,
    Toolchain,
    WorkflowError,
    checker_says_verified,
    load_candidate,
    render_completion_cnf,
    run_bounded,
    select_fixed_variables,
    sha256_file,
    verify_toolchain,
)


def write_graph(path: Path, order: int, edges: tuple[tuple[int, int], ...]) -> str:
    adjacency = [0] * order
    for left, right in edges:
        adjacency[left] |= 1 << right
        adjacency[right] |= 1 << left
    graph6 = encode_graph6(adjacency)
    path.write_text(graph6 + "\n", encoding="ascii")
    return graph6


class ResidualCompletionTests(unittest.TestCase):
    def test_selection_modes_and_conflict_union(self) -> None:
        clauses = [(1, 2), (-1, 3), (-2, -3)]
        assignment = (False, False, False)
        fixed, free, conflicts = select_fixed_variables(
            3, clauses, assignment, mode="conflict-union"
        )
        self.assertEqual(conflicts, (1,))
        self.assertEqual(fixed, (3,))
        self.assertEqual(free, (1, 2))

        fixed, free, _ = select_fixed_variables(
            3,
            clauses,
            assignment,
            mode="explicit-fixed",
            explicit_variables=(2,),
        )
        self.assertEqual(fixed, (2,))
        self.assertEqual(free, (1, 3))

        fixed, free, _ = select_fixed_variables(
            3,
            clauses,
            assignment,
            mode="explicit-free",
            explicit_variables=(2,),
        )
        self.assertEqual(fixed, (1, 3))
        self.assertEqual(free, (2,))

    def test_assumption_cnf_is_deterministic_and_exact(self) -> None:
        clauses = [(1, -2), (2, 3)]
        assignment = (True, False, True)
        keywords = {
            "base_cnf_sha256": "a" * 64,
            "candidate_assignment_sha256": "b" * 64,
            "selection_mode": "explicit-fixed",
        }
        first = render_completion_cnf(
            3, clauses, (1, 3), assignment, **keywords
        )
        second = render_completion_cnf(
            3, clauses, (1, 3), assignment, **keywords
        )
        self.assertEqual(first, second)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "completion.cnf"
            path.write_text(first, encoding="ascii")
            variables, parsed = parse_dimacs(path)
        self.assertEqual(variables, 3)
        self.assertEqual(parsed, [(1, -2), (2, 3), (1,), (3,)])

    def test_candidate_graph_boundary_check(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_path = root / "base.g6"
            base_graph6 = write_graph(base_path, 6, ())
            metadata = {
                "order": 6,
                "base_graph6": base_graph6,
                "free_edges": [[0, 1], [0, 2]],
            }
            valid_path = root / "valid.g6"
            write_graph(valid_path, 6, ((0, 1),))
            valid = load_candidate(valid_path, metadata, 2)
            self.assertEqual(valid.assignment, (True, False))
            self.assertEqual(valid.fixed_boundary_mismatch_count, 0)

            invalid_path = root / "invalid.g6"
            write_graph(invalid_path, 6, ((0, 1), (3, 4)))
            with self.assertRaisesRegex(WorkflowError, "outside"):
                load_candidate(invalid_path, metadata, 2)

    def test_production_conflict_union_leaves_fourteen_variables(self) -> None:
        cnf = ROOT / "certificates" / "residual_lns_incident_six.cnf"
        metadata_path = (
            ROOT / "certificates" / "residual_lns_incident_six.metadata.json"
        )
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        variable_count, clauses = parse_dimacs(cnf)
        true_set = set(metadata["base_true_variables"])
        assignment = tuple(
            variable in true_set
            for variable in range(1, variable_count + 1)
        )
        fixed, free, conflicts = select_fixed_variables(
            variable_count,
            clauses,
            assignment,
            mode="conflict-union",
        )
        self.assertEqual(conflicts, (29_512, 30_993))
        self.assertEqual(len(fixed), 223)
        self.assertEqual(
            free,
            (19, 22, 53, 56, 57, 60, 91, 94, 95, 137, 138, 231, 232, 237),
        )

    def test_pinned_toolchain_hashes(self) -> None:
        toolchain = Toolchain(
            python=DEFAULT_PYTHON,
            pysat_path=DEFAULT_PYSAT_PATH,
            drat_trim=DEFAULT_DRAT_TRIM,
            lrat_check=DEFAULT_LRAT_CHECK,
            hashes=PINNED_HASHES,
        )
        result = verify_toolchain(toolchain)
        self.assertEqual(result["sha256"], PINNED_HASHES)

    def test_glucose_proof_passes_both_checkers_and_tamper_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cnf = root / "unsat.cnf"
            # All four assignments of two variables are forbidden.
            cnf.write_text(
                "p cnf 2 4\n"
                "1 2 0\n"
                "1 -2 0\n"
                "-1 2 0\n"
                "-1 -2 0\n",
                encoding="ascii",
            )
            proof = root / "proof.drat"
            lrat = root / "proof.lrat"
            environment = os.environ.copy()
            environment["PYTHONPATH"] = str(DEFAULT_PYSAT_PATH)
            worker = ROOT / "src" / "residual_completion_glucose.py"
            solved = subprocess.run(
                (
                    str(DEFAULT_PYTHON),
                    str(worker),
                    str(cnf),
                    "--proof",
                    str(proof),
                ),
                text=True,
                capture_output=True,
                check=False,
                env=environment,
            )
            self.assertEqual(solved.returncode, 20, solved.stderr)
            worker_result = json.loads(solved.stdout)
            self.assertEqual(worker_result["status"], "UNSAT")
            self.assertEqual(worker_result["proof_sha256"], sha256_file(proof))

            drat = subprocess.run(
                (
                    str(DEFAULT_DRAT_TRIM),
                    str(cnf),
                    str(proof),
                    "-I",
                    "-L",
                    str(lrat),
                ),
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(drat.returncode, 0, drat.stdout + drat.stderr)
            self.assertTrue(checker_says_verified(drat.stdout + drat.stderr))
            checked = subprocess.run(
                (str(DEFAULT_LRAT_CHECK), str(cnf), str(lrat)),
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(
                checked.returncode, 0, checked.stdout + checked.stderr
            )
            self.assertTrue(
                checker_says_verified(checked.stdout + checked.stderr)
            )

            # An empty file makes drat-trim fall back to standard input and
            # wait indefinitely.  Use a nonempty but incomplete trace so the
            # rejection path remains deterministic and bounded.
            proof.write_text("d 1 2 0\n", encoding="ascii")
            rejected = subprocess.run(
                (
                    str(DEFAULT_DRAT_TRIM),
                    str(cnf),
                    str(proof),
                    "-I",
                ),
                text=True,
                capture_output=True,
                check=False,
                timeout=5,
            )
            self.assertFalse(
                checker_says_verified(rejected.stdout + rejected.stderr)
            )

    def test_sat_worker_model_and_bounded_timeout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cnf = root / "sat.cnf"
            cnf.write_text("p cnf 2 2\n1 2 0\n-1 2 0\n", encoding="ascii")
            proof = root / "unused.drat"
            environment = os.environ.copy()
            environment["PYTHONPATH"] = str(DEFAULT_PYSAT_PATH)
            worker = ROOT / "src" / "residual_completion_glucose.py"
            solved = subprocess.run(
                (
                    str(DEFAULT_PYTHON),
                    str(worker),
                    str(cnf),
                    "--proof",
                    str(proof),
                ),
                text=True,
                capture_output=True,
                check=False,
                env=environment,
            )
            self.assertEqual(solved.returncode, 10, solved.stderr)
            result = json.loads(solved.stdout)
            self.assertEqual(result["status"], "SAT")
            self.assertFalse(proof.exists())

            state, completed, elapsed = run_bounded(
                (
                    sys.executable,
                    "-c",
                    "import time; time.sleep(0.5)",
                ),
                timeout=0.01,
            )
            self.assertEqual(state, "TIMEOUT")
            self.assertIsNone(completed)
            self.assertLess(elapsed, 0.5)


if __name__ == "__main__":
    unittest.main()
