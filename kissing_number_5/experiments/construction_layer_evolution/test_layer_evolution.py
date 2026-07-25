#!/usr/bin/env python3
"""Focused tests for latitude layers and cardinality-changing moves."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest

import numpy as np


ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "layer_evolution_search", ROOT / "layer_evolution_search.py"
)
SEARCH = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = SEARCH
SPEC.loader.exec_module(SEARCH)


class LayerEvolutionTests(unittest.TestCase):
    def test_exact_sources(self):
        exact = SEARCH.exact_known_codes()
        floating = SEARCH.floating_known_codes()
        self.assertEqual(set(exact), {"D5", "L5", "Q5", "R5"})
        for name in exact:
            self.assertEqual(len(exact[name]), 40)
            self.assertAlmostEqual(SEARCH.max_inner(floating[name]), 0.5, places=14)

    def test_layer_gradient(self):
        rng = np.random.default_rng(77)
        sizes = (4, 5, 4)
        encoding = SEARCH.LayerEncoding.from_sizes(sizes)
        variables = np.r_[
            [-0.55, 0.08, 0.64],
            rng.normal(size=(sum(sizes), 4)).ravel(),
        ]
        value, gradient = SEARCH.layer_objective(variables, encoding, 17.0)
        direction = rng.normal(size=len(variables))
        direction /= np.linalg.norm(direction)
        epsilon = 2e-6
        plus = SEARCH.layer_objective(
            variables + epsilon * direction, encoding, 17.0
        )[0]
        minus = SEARCH.layer_objective(
            variables - epsilon * direction, encoding, 17.0
        )[0]
        finite_difference = (plus - minus) / (2 * epsilon)
        self.assertTrue(np.isfinite(value))
        self.assertAlmostEqual(
            float(gradient @ direction), finite_difference, delta=2e-8
        )

    def test_full_gradient(self):
        rng = np.random.default_rng(91)
        x = rng.normal(size=(12, 5))
        flat = x.ravel()
        value, gradient = SEARCH.logsumexp_pair_objective(flat, 12, 5, 23.0)
        direction = rng.normal(size=len(flat))
        direction /= np.linalg.norm(direction)
        epsilon = 2e-6
        plus = SEARCH.logsumexp_pair_objective(
            flat + epsilon * direction, 12, 5, 23.0
        )[0]
        minus = SEARCH.logsumexp_pair_objective(
            flat - epsilon * direction, 12, 5, 23.0
        )[0]
        self.assertTrue(np.isfinite(value))
        self.assertAlmostEqual(
            float(gradient @ direction), (plus - minus) / (2 * epsilon), delta=2e-8
        )

    def test_cardinality_move(self):
        rng = np.random.default_rng(123)
        source = SEARCH.floating_known_codes()["D5"]
        core, first, record = SEARCH.sampled_blocker_removal(
            source, 3, rng, 250
        )
        self.assertEqual(core.shape, (37, 5))
        self.assertEqual(len(record["removed_indices"]), 3)
        added = SEARCH.seed_added_points(core, first, 4, rng, 200)
        self.assertEqual(added.shape, (4, 5))
        self.assertEqual(len(np.vstack([core, added])), 41)

    def test_latitude_crossover_cardinality(self):
        rng = np.random.default_rng(223)
        known = SEARCH.floating_known_codes()
        unrelated = SEARCH.unit_rows(rng.normal(size=(43, 5)))
        child, record = SEARCH.heterogeneous_latitude_crossover(
            known["Q5"], unrelated, 43, rng, 12
        )
        self.assertEqual(child.shape, (43, 5))
        self.assertEqual(record["quota_first"] + record["quota_second"], 43)
        self.assertTrue(np.allclose(np.sum(child * child, axis=1), 1.0))

    def test_source_layer_insertion(self):
        rng = np.random.default_rng(404)
        source = SEARCH.floating_known_codes()["D5"]
        variables, sizes, record = SEARCH.source_layer_insertion_start(
            source, 41, np.eye(5)[4], rng, 250
        )
        self.assertEqual(sum(sizes), 41)
        self.assertIn(24, sizes)
        encoding = SEARCH.LayerEncoding.from_sizes(sizes)
        x, _, _ = SEARCH.unpack_layer_variables(variables, encoding)
        self.assertEqual(x.shape, (41, 5))
        self.assertAlmostEqual(record["initial_maximum"], SEARCH.max_inner(x))


if __name__ == "__main__":
    unittest.main()
