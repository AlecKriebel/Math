#!/usr/bin/env python3
"""Semantic and producer tests for delete-two/add-three completions."""

from __future__ import annotations

import json
import random
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core_completion_k2 import (  # noqa: E402
    build_k2_completion_instance,
    completed_adjacency_k2,
    formula_is_satisfied,
    induced_core_two,
    variable_for_unknown_edge,
)
from core_completion_sat import count_forbidden_sets  # noqa: E402
from graph_io import read_graph  # noqa: E402


CATALOG = ROOT / "data" / "r55_42some.g6"
SOURCE = ROOT / "src" / "core_completion_k2_persistent_solver.cpp"
PAIRS = ROOT / "tests" / "core_completion_k2_smoke.pairs"


class CoreCompletionK2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        compiler = shutil.which("clang++") or shutil.which("c++")
        if compiler is None:
            raise unittest.SkipTest("no C++17 compiler available")
        cls.temporary = tempfile.TemporaryDirectory()
        cls.solver = Path(cls.temporary.name) / "solver"
        compiled = subprocess.run(
            (
                compiler,
                "-O2",
                "-std=c++17",
                "-Wall",
                "-Wextra",
                str(SOURCE),
                "-o",
                str(cls.solver),
            ),
            text=True,
            capture_output=True,
            check=False,
        )
        if compiled.returncode:
            raise AssertionError(compiled.stderr)
        graph = read_graph(CATALOG, 1)
        cls.core, cls.retained = induced_core_two(graph, 0, 1)
        cls.instance = build_k2_completion_instance(cls.core)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def test_variable_numbering(self) -> None:
        self.assertEqual(variable_for_unknown_edge(40, 0, 40), 1)
        self.assertEqual(variable_for_unknown_edge(40, 39, 42), 120)
        self.assertEqual(variable_for_unknown_edge(40, 40, 41), 121)
        self.assertEqual(variable_for_unknown_edge(40, 40, 42), 122)
        self.assertEqual(variable_for_unknown_edge(40, 41, 42), 123)
        self.assertEqual(self.instance.variable_count, 123)

    def test_cpp_formula_counts_match_independent_python(self) -> None:
        solved = subprocess.run(
            (
                str(self.solver),
                "--graph",
                str(CATALOG),
                "--pairs",
                str(PAIRS),
                "--node-limit",
                "100000",
                "--seconds-limit",
                "1",
            ),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertIn(solved.returncode, (0, 2, 10))
        records = [
            json.loads(line)
            for line in solved.stdout.splitlines()
            if line.strip()
        ]
        pair = records[0]
        clique = self.instance.clique_counts_by_new_count
        independent = self.instance.independent_counts_by_new_count
        self.assertEqual(pair["variables"], self.instance.variable_count)
        self.assertEqual(pair["clauses"], len(self.instance.clauses))
        self.assertEqual(pair["negative_clauses"], sum(clique))
        self.assertEqual(pair["positive_clauses"], sum(independent))
        self.assertEqual(
            (3 * pair["core_k4"], 3 * pair["core_k3"], pair["core_edges"]),
            clique,
        )
        self.assertEqual(
            (
                3 * pair["core_i4"],
                3 * pair["core_i3"],
                pair["core_nonedges"],
            ),
            independent,
        )

    def test_formula_matches_completed_graph_semantics(self) -> None:
        for seed in range(3):
            generator = random.Random(seed)
            assignment = [
                bool(generator.getrandbits(1))
                for _ in range(self.instance.variable_count)
            ]
            completed = completed_adjacency_k2(self.core, assignment)
            forbidden = count_forbidden_sets(completed, 5)
            self.assertEqual(
                formula_is_satisfied(
                    self.instance.clauses, assignment
                ),
                forbidden == (0, 0),
            )


if __name__ == "__main__":
    unittest.main()
