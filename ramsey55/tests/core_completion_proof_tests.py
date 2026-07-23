#!/usr/bin/env python3
"""Regression and semantic-audit tests for the fixed-core certificate."""

from __future__ import annotations

import hashlib
import itertools
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))

from core_completion_proof_check import (  # noqa: E402
    MAGIC,
    TreeChecker,
    build_formula,
    canonical_dimacs,
    decode_short_graph6,
    delete_vertex,
)


GRAPH = ROOT / "data" / "exoo42_constructed.g6"
PROOF = ROOT / "certificates" / "core_completion_proof_delete0.bin"


class CoreCompletionProofTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        graph_raw = GRAPH.read_bytes()
        cls.core = delete_vertex(decode_short_graph6(graph_raw), 0)
        cls.formula = build_formula(cls.core)
        cls.proof_raw = PROOF.read_bytes()
        if cls.proof_raw[:8] != MAGIC:
            raise AssertionError("test proof has wrong magic")
        cls.tree = cls.proof_raw[15:]

    def test_formula_counts_hash_and_complete_tree(self) -> None:
        self.assertEqual(len(self.core), 41)
        self.assertEqual(self.formula.core_k4, 1040)
        self.assertEqual(self.formula.core_i4, 1055)
        self.assertEqual(self.formula.core_k3, 1250)
        self.assertEqual(self.formula.core_i3, 1230)
        self.assertEqual(self.formula.negative_count, 3330)
        self.assertEqual(self.formula.positive_count, 3340)
        self.assertEqual(len(self.formula.clauses), 6670)
        self.assertEqual(
            hashlib.sha256(canonical_dimacs(self.formula)).hexdigest(),
            "722b8b85d44e3fbbfa8546dbca8a2a5a2eb550e3df51a3c127ff47802b028f59",
        )
        self.assertEqual(
            hashlib.sha256(self.proof_raw).hexdigest(),
            "5301f7a48408c90aad8940224b437a01b9bc9f6aabf64286b72984bad4ac72ed",
        )
        stats = TreeChecker(self.tree, self.formula.clauses).run()
        self.assertEqual(stats.nodes, 187)
        self.assertEqual(stats.branches, 93)
        self.assertEqual(stats.leaves, 94)
        self.assertEqual(stats.unit_assignments, 2408)
        self.assertEqual(stats.max_depth, 13)

    def test_direct_five_subset_reconstruction_matches_formula(self) -> None:
        # Reconstruct constraints by considering every relevant 5-subset,
        # independently of the checker generator's 4-set/3-set decomposition.
        a_vertex = 41
        b_vertex = 42
        direct: list[tuple[int, bool]] = []
        for vertices in itertools.combinations(range(43), 5):
            if a_vertex not in vertices and b_vertex not in vertices:
                continue
            fixed_edges: list[int] = []
            variable_edges: list[int] = []
            for left, right in itertools.combinations(vertices, 2):
                if right < a_vertex:
                    fixed_edges.append((self.core[left] >> right) & 1)
                elif left < a_vertex and right == a_vertex:
                    variable_edges.append(left)
                elif left < a_vertex and right == b_vertex:
                    variable_edges.append(41 + left)
                else:
                    self.assertEqual((left, right), (a_vertex, b_vertex))
                    variable_edges.append(82)
            mask = sum(1 << variable for variable in variable_edges)
            if all(fixed_edges):
                direct.append((mask, False))
            if not any(fixed_edges):
                direct.append((mask, True))
        self.assertEqual(len(direct), 6670)
        self.assertEqual(len(set(direct)), 6670)
        self.assertEqual(set(direct), set(self.formula.clauses))

    def test_truncated_trailing_and_invalid_trees_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "truncated"):
            TreeChecker(self.tree[:-1], self.formula.clauses).run()
        with self.assertRaisesRegex(ValueError, "trailing"):
            TreeChecker(self.tree + b"\xff", self.formula.clauses).run()
        with self.assertRaisesRegex(ValueError, "invalid branch"):
            TreeChecker(
                bytes([254]) + self.tree[1:], self.formula.clauses
            ).run()


if __name__ == "__main__":
    unittest.main()
