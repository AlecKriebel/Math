#!/usr/bin/env python3
"""Catalog-line coverage tests for the fixed-core C++ solver/checker pair."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "verify"))

from core_completion_catalog_batch import (  # noqa: E402
    parse_deletions,
    parse_indices,
)
from core_completion_proof_check import (  # noqa: E402
    build_formula,
    decode_short_graph6,
    delete_vertex,
)
from graph_io import read_graph  # noqa: E402


CATALOG = ROOT / "data" / "r55_42some.g6"
SOURCE = ROOT / "src" / "core_completion_proof_solver.cpp"
CHECKER = ROOT / "verify" / "core_completion_proof_check.py"


class CoreCompletionCatalogTests(unittest.TestCase):
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

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def test_index_parsers_cover_boundaries(self) -> None:
        self.assertEqual(parse_indices("1,3-5,328", 328), [1, 3, 4, 5, 328])
        self.assertEqual(parse_deletions("0,17-19,41"), [0, 17, 18, 19, 41])
        self.assertEqual(len(parse_indices("all", 328)), 328)
        self.assertEqual(parse_deletions("all"), list(range(42)))
        with self.assertRaises(ValueError):
            parse_indices("0", 328)
        with self.assertRaises(ValueError):
            parse_deletions("42")

    def test_independent_decoder_selects_nonfirst_and_last_lines(self) -> None:
        raw = CATALOG.read_bytes()
        for line in (1, 2, 328):
            independent = decode_short_graph6(raw, line)
            production = read_graph(CATALOG, line)
            self.assertEqual(independent, production)
            self.assertEqual(len(independent), 42)
        self.assertNotEqual(
            decode_short_graph6(raw, 1), decode_short_graph6(raw, 2)
        )

    def test_cpp_solver_selects_requested_nonfirst_core(self) -> None:
        line = 2
        deleted = 17
        formula = build_formula(
            delete_vertex(decode_short_graph6(CATALOG.read_bytes(), line), deleted)
        )
        run = subprocess.run(
            (
                str(self.solver),
                "--graph",
                str(CATALOG),
                "--line",
                str(line),
                "--delete",
                str(deleted),
                "--node-limit",
                "1",
                "--seconds-limit",
                "60",
                "--progress",
                "0",
            ),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertIn(run.returncode, (2, 20))
        result = json.loads(run.stdout)
        self.assertEqual(result["catalog_line"], line)
        self.assertEqual(result["deleted_vertex"], deleted)
        self.assertEqual(result["core_k4"], formula.core_k4)
        self.assertEqual(result["core_i4"], formula.core_i4)
        self.assertEqual(result["core_k3"], formula.core_k3)
        self.assertEqual(result["core_i3"], formula.core_i3)
        self.assertEqual(result["clauses"], len(formula.clauses))

    def test_v2_proof_binds_catalog_line_and_independently_checks(self) -> None:
        line = 2
        deleted = 17
        proof = Path(self.temporary.name) / "line2-delete17.bin"
        solved = subprocess.run(
            (
                str(self.solver),
                "--graph",
                str(CATALOG),
                "--line",
                str(line),
                "--delete",
                str(deleted),
                "--proof",
                str(proof),
                "--node-limit",
                "1000000",
                "--seconds-limit",
                "60",
                "--progress",
                "0",
            ),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(solved.returncode, 20, solved.stdout + solved.stderr)
        checked = subprocess.run(
            (
                sys.executable,
                str(CHECKER),
                "--graph",
                str(CATALOG),
                "--line",
                str(line),
                "--delete",
                str(deleted),
                "--proof",
                str(proof),
            ),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        result = json.loads(checked.stdout)
        self.assertEqual(result["catalog_line"], line)
        self.assertEqual(result["proof_format"], "CORE2DP2")

        wrong_line = subprocess.run(
            (
                sys.executable,
                str(CHECKER),
                "--graph",
                str(CATALOG),
                "--line",
                "1",
                "--delete",
                str(deleted),
                "--proof",
                str(proof),
            ),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(wrong_line.returncode, 0)
        self.assertIn("catalog line does not match", wrong_line.stderr)


if __name__ == "__main__":
    unittest.main()
