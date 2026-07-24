#!/usr/bin/env python3

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from e2_core_deletion_catalog_expansion import (  # noqa: E402
    bitset_ramsey_valid,
    data_lines,
    delete_vertex,
    homogeneous_five_sets,
)
from graph_io import decode_graph6  # noqa: E402


class E2CoreDeletionTests(unittest.TestCase):
    def test_all_four_core_deletions_are_valid(self) -> None:
        candidate = (
            ROOT
            / "results"
            / "constructive"
            / "catalog_seed_search_stratified_v1"
            / "line_001.g6"
        )
        adjacency = decode_graph6(data_lines(candidate)[0])
        conflicts = homogeneous_five_sets(adjacency)
        self.assertEqual(len(conflicts), 2)
        self.assertEqual(conflicts[0][0], conflicts[1][0])
        core = sorted(set(conflicts[0][1]) & set(conflicts[1][1]))
        self.assertEqual(len(core), 4)
        for removed in core:
            derived = delete_vertex(adjacency, removed)
            self.assertEqual(len(derived), 42)
            self.assertEqual(homogeneous_five_sets(derived), [])
            self.assertTrue(bitset_ramsey_valid(derived))

    def test_delete_vertex_relabels_edges_exactly(self) -> None:
        adjacency = [
            (1 << 1) | (1 << 3),
            (1 << 0) | (1 << 2),
            1 << 1,
            1 << 0,
        ]
        self.assertEqual(delete_vertex(adjacency, 1), [1 << 2, 0, 1])


if __name__ == "__main__":
    unittest.main()
