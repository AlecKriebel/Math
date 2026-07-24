#!/usr/bin/env python3
"""Focused tests for the E=3/E=4 closure quotient audit."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from e2_low_closure_isomorphism_audit import (  # noqa: E402
    ORDER,
    clique_count,
    normalized_labels,
    partition,
    size_histogram,
)


def disjoint_cliques(sizes: tuple[int, ...]) -> list[int]:
    adjacency = [0] * ORDER
    start = 0
    for size in sizes:
        vertices = range(start, start + size)
        for left in vertices:
            for right in range(left + 1, start + size):
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
        start += size
    return adjacency


class E2LowClosureIsomorphismAuditTests(unittest.TestCase):
    def test_independent_k5_counter(self) -> None:
        self.assertEqual(clique_count([0] * ORDER), 0)
        self.assertEqual(clique_count(disjoint_cliques((5,))), 1)
        self.assertEqual(clique_count(disjoint_cliques((5, 5, 4))), 2)
        self.assertEqual(clique_count(disjoint_cliques((6,))), 6)

    def test_partition_ignores_canonical_label_spelling(self) -> None:
        dense = ["a", "b", "a", "c", "b"]
        sparse = ["x", "y", "x", "z", "y"]
        self.assertEqual(partition(dense), partition(sparse))
        self.assertEqual(size_histogram(dense), {"1": 1, "2": 2})

    def test_complement_normalization(self) -> None:
        self.assertEqual(
            normalized_labels(
                ["z", "a", "same"], ["b", "q", "same"]
            ),
            ["b", "a", "same"],
        )


if __name__ == "__main__":
    unittest.main()
