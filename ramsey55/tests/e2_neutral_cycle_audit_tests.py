#!/usr/bin/env python3
"""Unit and retained-instance tests for the independent neutral-cycle audit."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "verify"))

from e2_neutral_cycle_audit import (  # noqa: E402
    all_conflicts,
    build_neutral_cycle,
    edge_hamming,
    toggle_edge,
)
from graph_io import encode_graph6, read_graph  # noqa: E402


class NeutralCycleAuditTests(unittest.TestCase):
    def test_independent_conflict_enumerator_on_order_five(self) -> None:
        complete = tuple(
            ((1 << 5) - 1) & ~(1 << vertex) for vertex in range(5)
        )
        empty = (0, 0, 0, 0, 0)
        self.assertEqual(all_conflicts(complete), (("C5", (0, 1, 2, 3, 4)),))
        self.assertEqual(all_conflicts(empty), (("I5", (0, 1, 2, 3, 4)),))

    def test_toggle_is_involution_and_hamming_one(self) -> None:
        graph = tuple(
            read_graph(
                ROOT
                / "results/constructive/catalog_seed_search_stratified_v1"
                / "line_001.g6"
            )
        )
        changed = toggle_edge(graph, (0, 1))
        self.assertEqual(edge_hamming(graph, changed), 1)
        self.assertEqual(toggle_edge(changed, (0, 1)), graph)

    def test_line_one_exact_neutral_cycle(self) -> None:
        seed = tuple(
            read_graph(
                ROOT
                / "results/constructive/catalog_seed_search_stratified_v1"
                / "line_001.g6"
            )
        )
        final = tuple(
            read_graph(
                ROOT
                / "results/constructive/conflict_block_catalog22_followup_v1"
                / "line_001"
                / "final.g6"
            )
        )
        cycle = build_neutral_cycle(seed)
        self.assertEqual(len(cycle.graphs), 86)
        self.assertEqual(len(set(cycle.graph6)), 86)
        self.assertEqual(len(set(cycle.transition_edges)), 43)
        self.assertEqual(
            {cycle.transition_edges.count(edge) for edge in cycle.transition_edges},
            {2},
        )
        self.assertEqual(
            set(cycle.barrier_profiles),
            {(9, 9, 9, 38), (10, 10, 12, 15)},
        )
        self.assertIn(encode_graph6(list(final)), cycle.graph6)


if __name__ == "__main__":
    unittest.main()
