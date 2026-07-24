#!/usr/bin/env python3
"""Semantic, producer, compact-format, and plan tests for E=2 replacement."""

from __future__ import annotations

import hashlib
import itertools
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "verify"))

from core_completion_k2 import build_k2_completion_instance  # noqa: E402
from e2_triple_replacement_compact import (  # noqa: E402
    STATUS_LIMIT,
    STATUS_OBSERVED_UNSAT,
    STATUS_STRUCTURAL,
    TRIPLES,
    iter_records,
    validate_file,
)
from e2_triple_replacement_coverage import (  # noqa: E402
    forbidden_five_sets,
    retained_count,
)
from e2_triple_replacement_screen import (  # noqa: E402
    induced_core_three,
    make_plan,
    validate_plan,
    validate_sources,
)
from graph_io import read_graph  # noqa: E402


CORPUS = ROOT / "data" / "e2_complement_class_representatives.g6"
SOLVER = ROOT / "build" / "e2_triple_replacement_solver"
CHECKER = ROOT / "verify" / "e2_triple_replacement_coverage.py"
PARSER_SOURCE = ROOT / "src" / "e2_triple_replacement_compact.py"
TESTS = ROOT / "tests" / "e2_triple_replacement_tests.py"
EXHAUSTIVE = ROOT / "verify" / "exhaustive_verify.py"
BITSET = ROOT / "build" / "bitset_verify"
CORPUS_SHA256 = hashlib.sha256(CORPUS.read_bytes()).hexdigest()


class E2TripleReplacementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not SOLVER.exists():
            raise unittest.SkipTest("replacement solver binary is absent")
        cls.graphs = {index: read_graph(CORPUS, index) for index in (1, 2)}
        cls.conflicts = {
            index: forbidden_five_sets(graph)
            for index, graph in cls.graphs.items()
        }

    def test_frozen_sources_match_certified_models(self) -> None:
        sources = validate_sources(CORPUS)
        self.assertEqual([source["input_index"] for source in sources], [1, 2])
        self.assertEqual(
            [source["source_catalog_line"] for source in sources], [42, 256]
        )
        self.assertEqual(
            [source["source_model_index"] for source in sources], [0, 1]
        )
        self.assertEqual(
            [conflict[0] for conflict in self.conflicts[1]],
            ["clique", "clique"],
        )
        self.assertEqual(
            [conflict[0] for conflict in self.conflicts[2]],
            ["independent", "independent"],
        )

    def test_exact_structural_partition(self) -> None:
        for index in (1, 2):
            retained = [
                retained_count(self.conflicts[index], triple)
                for triple in TRIPLES
            ]
            self.assertEqual(sum(value > 0 for value in retained), 9_102)
            self.assertEqual(sum(value == 0 for value in retained), 3_239)
            self.assertEqual(
                {
                    value: retained.count(value)
                    for value in sorted(set(retained))
                },
                {0: 3_239, 1: 1_332, 2: 7_770},
            )

    def run_one(self, input_index: int, ordinal: int, output: Path) -> object:
        completed = subprocess.run(
            (
                str(SOLVER),
                "--graph",
                str(CORPUS),
                "--records",
                str(output),
                "--input-index",
                str(input_index),
                "--triple-start",
                str(ordinal),
                "--triple-end",
                str(ordinal + 1),
                "--corpus-sha256",
                CORPUS_SHA256,
                "--node-limit",
                "100000",
                "--seconds-limit",
                "0.5",
                "--record-byte-cap",
                "128",
            ),
            text=True,
            capture_output=True,
            check=False,
            timeout=10,
        )
        self.assertIn(completed.returncode, (0, 2), completed.stderr)
        audit = validate_file(
            output,
            expected_input_index=input_index,
            expected_range=(ordinal, ordinal + 1),
            expected_corpus_sha256=CORPUS_SHA256,
            node_limit=100_000,
        )
        self.assertEqual(audit["record_count"], 1)
        return next(
            iter_records(
                output,
                expected_input_index=input_index,
                expected_range=(ordinal, ordinal + 1),
                expected_corpus_sha256=CORPUS_SHA256,
            )
        )

    def test_structural_and_solver_records(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            structural = self.run_one(1, 0, root / "structural.bin")
            self.assertEqual(structural.status, STATUS_STRUCTURAL)
            self.assertEqual(structural.retained_conflicts, 2)

            for input_index in (1, 2):
                ordinal = next(
                    position
                    for position, triple in enumerate(TRIPLES)
                    if retained_count(
                        self.conflicts[input_index], triple
                    )
                    == 0
                )
                record = self.run_one(
                    input_index,
                    ordinal,
                    root / f"eligible_{input_index}.bin",
                )
                self.assertIn(
                    record.status,
                    (STATUS_OBSERVED_UNSAT, STATUS_LIMIT),
                )
                self.assertEqual(record.retained_conflicts, 0)
                core, _ = induced_core_three(
                    self.graphs[input_index], TRIPLES[ordinal]
                )
                independent = build_k2_completion_instance(core)
                self.assertEqual(record.clauses, len(independent.clauses))
                self.assertEqual(
                    record.core_k4,
                    independent.clique_counts_by_new_count[0] // 3,
                )
                self.assertEqual(
                    record.core_i4,
                    independent.independent_counts_by_new_count[0] // 3,
                )
                self.assertEqual(
                    record.core_k3,
                    independent.clique_counts_by_new_count[1] // 3,
                )
                self.assertEqual(
                    record.core_i3,
                    independent.independent_counts_by_new_count[1] // 3,
                )

    def test_compact_parser_rejects_corruption(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.bin"
            self.run_one(1, 0, path)
            payload = bytearray(path.read_bytes())
            payload[0] ^= 1
            corrupt = Path(directory) / "corrupt.bin"
            corrupt.write_bytes(payload)
            with self.assertRaises(ValueError):
                validate_file(corrupt)

    def test_plan_is_exact_and_hash_bound(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plan_path = Path(directory) / "plan.json"
            output_dir = (
                ROOT
                / "results"
                / "constructive"
                / "e2_triple_replacement_test_unused"
            )
            plan = make_plan(
                plan_path=plan_path,
                solver=SOLVER,
                corpus=CORPUS,
                output_dir=output_dir,
                checker=CHECKER,
                parser_source=PARSER_SOURCE,
                tests=TESTS,
                exhaustive=EXHAUSTIVE,
                bitset=BITSET,
                shard_size=1_000,
                node_limit=100_000,
                seconds_limit=0.5,
                shard_timeout=300,
                output_byte_cap=50_000_000,
                reserve_bytes=1,
            )
            self.assertEqual(plan["total_labeled_triples"], 24_682)
            self.assertEqual(plan["expected_solver_eligible"], 6_478)
            self.assertFalse(plan["deduplication"])
            checked = validate_plan(plan_path)
            self.assertEqual(checked["shard_count"], 26)
            with self.assertRaises(FileExistsError):
                make_plan(
                    plan_path=plan_path,
                    solver=SOLVER,
                    corpus=CORPUS,
                    output_dir=output_dir,
                    checker=CHECKER,
                    parser_source=PARSER_SOURCE,
                    tests=TESTS,
                    exhaustive=EXHAUSTIVE,
                    bitset=BITSET,
                    shard_size=1_000,
                    node_limit=100_000,
                    seconds_limit=0.5,
                    shard_timeout=300,
                    output_byte_cap=50_000_000,
                    reserve_bytes=1,
                )


if __name__ == "__main__":
    unittest.main()
