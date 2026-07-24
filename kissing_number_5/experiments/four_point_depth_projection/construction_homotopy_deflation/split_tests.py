#!/usr/bin/env python3
"""Regression tests for continuous split cardinality homotopy."""

from __future__ import annotations

import math
import unittest

import numpy as np

from experiments.four_point_depth_projection.construction_homotopy_deflation import (
    split_homotopy_search as search,
)


class SplitHomotopyTests(unittest.TestCase):
    def test_four_exact_sources(self):
        codes = search.exact_known_codes()
        self.assertEqual(set(codes), {"D5", "L5", "Q5", "R5"})
        histograms = []
        for name, code in codes.items():
            self.assertEqual(len(code), 40)
            self.assertEqual(len(set(code)), 40)
            histogram = search.exact_pair_histogram(code)
            self.assertEqual(histogram["1"], 240)
            histograms.append(tuple(sorted(histogram.items())))
            x = search.floating_code(code)
            self.assertLessEqual(search.maximum(x), np.nextafter(0.5, np.inf))
        self.assertEqual(len(set(histograms)), 4)

    def test_split_pair_has_prescribed_separation(self):
        source = search.floating_code(search.exact_known_codes()["D5"])
        rng = np.random.default_rng(101)
        parents = [3, 17, 28]
        directions = search.asymmetric_split_directions(source, parents, rng)
        x, pairs, mapping = search.make_split_configuration(
            source, parents, directions, separation=0.21
        )
        self.assertEqual(x.shape, (43, 5))
        self.assertEqual(len(mapping), 40)
        for first, second in pairs:
            self.assertAlmostEqual(float(x[first] @ x[second]), math.cos(0.21))
        y = search.force_pair_separation(x, pairs, separation=1.13)
        for first, second in pairs:
            self.assertAlmostEqual(float(y[first] @ y[second]), math.cos(1.13))

    def test_neighborhood_release_is_monotone(self):
        source = search.floating_code(search.exact_known_codes()["Q5"])
        adjacency = search.source_contact_adjacency(source)
        previous: set[int] = set()
        for radius in (0, 1, 2, 3, None):
            current = search.source_neighborhood(adjacency, [2, 19], radius)
            self.assertTrue(previous <= current)
            previous = current
        self.assertEqual(previous, set(range(40)))

    def test_parent_selection_is_deterministic_and_distinct(self):
        source = search.floating_code(search.exact_known_codes()["R5"])
        first = search.select_split_parents(
            source, 4, np.random.default_rng(77), variant=1
        )
        second = search.select_split_parents(
            source, 4, np.random.default_rng(77), variant=1
        )
        self.assertEqual(first, second)
        self.assertEqual(len(set(first)), 4)

    def test_partial_epigraph_preserves_pair_constraint(self):
        source = search.floating_code(search.exact_known_codes()["L5"])
        rng = np.random.default_rng(9)
        parents = [5]
        directions = search.asymmetric_split_directions(source, parents, rng)
        x, pairs, mapping = search.make_split_configuration(
            source, parents, directions, separation=0.4
        )
        movable = search.current_movable_indices(
            search.source_neighborhood(
                search.source_contact_adjacency(source), parents, radius=0
            ),
            mapping,
        )
        y, record = search.epigraph_refine(
            x,
            movable=movable,
            split_pairs=pairs,
            prescribed_pair_inner=math.cos(0.4),
            max_iterations=20,
        )
        self.assertTrue(record["success"])
        self.assertLess(record["pair_equality_max_error"], 2e-10)
        self.assertAlmostEqual(float(y[pairs[0][0]] @ y[pairs[0][1]]), math.cos(0.4))

    def test_diagnostics_rank_five(self):
        source = search.floating_code(search.exact_known_codes()["D5"])
        diagnostic = search.diagnostics(source)
        self.assertEqual(len(diagnostic["positive_gram_eigenvalues"]), 5)
        self.assertLess(diagnostic["gram_tail_max_abs"], 1e-13)
        self.assertEqual(diagnostic["active_1e-8"]["edge_count"], 240)


if __name__ == "__main__":
    unittest.main()
