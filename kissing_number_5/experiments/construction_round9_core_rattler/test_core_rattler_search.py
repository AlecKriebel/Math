"""Tests for round-9 numerical discovery and its independent checker."""

from __future__ import annotations

import math
import unittest
from pathlib import Path

import numpy as np

from . import check_results
from . import core_rattler_search as search


class SearchPrimitiveTests(unittest.TestCase):
    def test_d5_is_exact_float_lower_bound_model(self):
        roots = search.d5_roots()
        self.assertEqual(roots.shape, (40, 5))
        self.assertLessEqual(
            np.max(np.abs(np.sum(roots * roots, axis=1) - 1.0)), 3e-16
        )
        self.assertLessEqual(abs(search.maximum(roots) - 0.5), 3e-16)

    def test_all_coordinate_gradient(self):
        rng = np.random.default_rng(2026072391)
        x = search.unit_rows(rng.normal(size=(8, 5)))
        direction = rng.normal(size=x.size)
        direction /= np.linalg.norm(direction)
        step = 1e-6
        _, gradient = search.smooth_all(x.ravel(), len(x), 37.0)
        finite_difference = (
            search.smooth_all(x.ravel() + step * direction, len(x), 37.0)[0]
            - search.smooth_all(x.ravel() - step * direction, len(x), 37.0)[0]
        ) / (2.0 * step)
        self.assertLess(abs(finite_difference - gradient @ direction), 2e-9)

    def test_block_gradient(self):
        rng = np.random.default_rng(2026072392)
        x = search.unit_rows(rng.normal(size=(9, 5)))
        fixed, block = x[:5], x[5:]
        direction = rng.normal(size=block.size)
        direction /= np.linalg.norm(direction)
        step = 1e-6
        _, gradient = search.smooth_block(
            block.ravel(), fixed, len(block), 41.0
        )
        finite_difference = (
            search.smooth_block(
                block.ravel() + step * direction, fixed, len(block), 41.0
            )[0]
            - search.smooth_block(
                block.ravel() - step * direction, fixed, len(block), 41.0
            )[0]
        ) / (2.0 * step)
        self.assertLess(abs(finite_difference - gradient @ direction), 2e-9)

    def test_complete_facet_scan_on_cross_polytope(self):
        cross_polytope = np.vstack([np.eye(5), -np.eye(5)])
        candidates, audit = search.facet_hole_candidates(cross_polytope, 5)
        self.assertTrue(audit["available"])
        self.assertTrue(audit["origin_strictly_inside"])
        self.assertGreaterEqual(len(candidates), 1)
        self.assertLess(
            abs(candidates[0][1] - 1.0 / math.sqrt(5.0)), 2e-14
        )

    def test_exact_finite_graph_independence(self):
        # C5 has independence number two and minimum vertex cover three.
        edges = [[i, (i + 1) % 5] for i in range(5)]
        independent, nodes = search.exact_maximum_independent_set(5, edges)
        self.assertEqual(len(independent), 2)
        self.assertGreater(nodes, 0)
        other, other_nodes = check_results.maximum_independent_set(5, edges)
        self.assertEqual(independent, other)
        self.assertEqual(nodes, other_nodes)


class ReleasedArtifactTest(unittest.TestCase):
    def test_released_portfolio(self):
        path = (
            Path(__file__).resolve().parent
            / "results"
            / "core_rattler_portfolio.json"
        )
        if not path.exists():
            self.skipTest("released portfolio has not been generated yet")
        old_cwd = Path.cwd()
        try:
            # The stored inherited path is relative to the project package.
            import os

            os.chdir(Path(__file__).resolve().parents[2])
            report = check_results.verify(path)
        finally:
            os.chdir(old_cwd)
        self.assertEqual(
            report["status"], "PASS — BINARY64 ARTIFACT INTEGRITY ONLY"
        )


if __name__ == "__main__":
    unittest.main()
