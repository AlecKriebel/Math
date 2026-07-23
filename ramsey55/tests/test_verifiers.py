#!/usr/bin/env python3
"""Cross-check the two verifier paths on deterministic fixtures."""

from __future__ import annotations

import itertools
import json
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from graph_io import complement, decode_graph6, encode_graph6  # noqa: E402

sys.path.insert(0, str(ROOT / "verify"))
from exhaustive_verify import count_forbidden  # noqa: E402


def from_edges(n: int, edges: set[tuple[int, int]]) -> list[int]:
    adjacency = [0] * n
    for left, right in edges:
        adjacency[left] |= 1 << right
        adjacency[right] |= 1 << left
    return adjacency


def complete_graph(n: int) -> list[int]:
    return [((1 << n) - 1) & ~(1 << vertex) for vertex in range(n)]


def paley17() -> list[int]:
    residues = {1, 2, 4, 8, 9, 13, 15, 16}
    return from_edges(
        17,
        {
            (left, right)
            for left in range(17)
            for right in range(left + 1, 17)
            if (left - right) % 17 in residues
        },
    )


class VerifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cpp_verifier = ROOT / "build" / "bitset_verify"
        if not cls.cpp_verifier.exists():
            raise RuntimeError("compile build/bitset_verify before running tests")

    def run_cpp(self, adjacency: list[int], k: int) -> tuple[int, dict]:
        with tempfile.NamedTemporaryFile("w", suffix=".g6", delete=False) as handle:
            handle.write(encode_graph6(adjacency) + "\n")
            path = Path(handle.name)
        try:
            run = subprocess.run(
                [str(self.cpp_verifier), str(path), "--k", str(k)],
                text=True,
                capture_output=True,
                check=False,
            )
            return run.returncode, json.loads(run.stdout)
        finally:
            path.unlink()

    def assert_agree(self, adjacency: list[int], k: int) -> None:
        clique_count, independent_count = count_forbidden(adjacency, k)
        returncode, cpp = self.run_cpp(adjacency, k)
        valid = clique_count == 0 and independent_count == 0
        self.assertEqual(returncode == 0, valid)
        self.assertEqual(cpp["valid"], valid)
        self.assertEqual(cpp["clique_k_found"], clique_count > 0)
        self.assertEqual(cpp["independent_k_found"], independent_count > 0)
        self.assertEqual(cpp["edge_count"], sum(row.bit_count() for row in adjacency) // 2)
        self.assertEqual(cpp["degree_sequence"], sorted(row.bit_count() for row in adjacency))

    def test_graph6_known_c5(self) -> None:
        cycle = from_edges(5, {(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)})
        self.assertEqual(encode_graph6(cycle), "Dhc")
        self.assertEqual(decode_graph6("Dhc"), cycle)

    def test_complete_and_empty_k5(self) -> None:
        self.assert_agree(complete_graph(5), 5)
        self.assert_agree([0] * 5, 5)

    def test_known_small_c5_ramsey_graph(self) -> None:
        cycle = decode_graph6("Dhc")
        self.assertEqual(count_forbidden(cycle, 3), (0, 0))
        self.assert_agree(cycle, 3)

    def test_known_paley17_ramsey_graph(self) -> None:
        graph = paley17()
        self.assertEqual(sum(row.bit_count() for row in graph) // 2, 68)
        self.assertEqual(count_forbidden(graph, 4), (0, 0))
        self.assert_agree(graph, 4)

    def test_random_graphs_and_complements(self) -> None:
        rng = random.Random(20260723)
        for n in (8, 10, 12):
            edges = {
                pair
                for pair in itertools.combinations(range(n), 2)
                if rng.getrandbits(1)
            }
            graph = from_edges(n, edges)
            dual = complement(graph)
            original_counts = count_forbidden(graph, 5)
            dual_counts = count_forbidden(dual, 5)
            self.assertEqual(original_counts, tuple(reversed(dual_counts)))
            self.assertEqual(decode_graph6(encode_graph6(graph)), graph)
            self.assert_agree(graph, 5)
            self.assert_agree(dual, 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
