#!/usr/bin/env python3
"""Tests for the second-barrier E=2 discovery audit."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from e2_second_barrier_discovery_audit import (  # noqa: E402
    ORDER,
    claim_boundary,
    e2_geometry,
    five_cliques,
)
from graph_io import decode_graph6  # noqa: E402


class E2SecondBarrierDiscoveryAuditTests(unittest.TestCase):
    def test_five_clique_enumerator(self) -> None:
        adjacency = [0] * ORDER
        for left in range(6):
            for right in range(left + 1, 6):
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
        self.assertEqual(len(five_cliques(adjacency)), 6)

    def test_known_endpoint_geometry(self) -> None:
        path = (
            ROOT
            / "results/constructive/catalog_seed_search_stratified_v1"
            / "line_001.g6"
        )
        graph = path.read_text(encoding="ascii").strip()
        self.assertEqual(len(decode_graph6(graph)), ORDER)
        geometry, cliques, independent = e2_geometry(graph)
        self.assertEqual(
            geometry, "same_colour_pair;overlap=4"
        )
        self.assertEqual(len(cliques) + len(independent), 2)

    def test_claim_boundary_uses_actual_corpus_sizes(self) -> None:
        boundary = claim_boundary(1878, 22)
        self.assertIn("1,878 retained", boundary)
        self.assertIn("22 known", boundary)
        self.assertNotIn("1,670", boundary)


if __name__ == "__main__":
    unittest.main()
