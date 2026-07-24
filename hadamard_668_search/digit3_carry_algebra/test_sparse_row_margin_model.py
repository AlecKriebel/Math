#!/usr/bin/env python3
"""Regression tests for exact six-sum row-margin membership."""

from __future__ import annotations

import random
from pathlib import Path
import sys
import unittest

from ortools.sat.python import cp_model


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import solve_sparse_histogram_cp_sat as sparse


class SparseRowMarginTests(unittest.TestCase):
    def test_affine_phase_sum_table(self) -> None:
        candidate = sparse.second.CANDIDATES[0]
        profiles = sparse.second.profiles_from_ids(
            candidate[3], candidate[4]
        )
        baseline, effects = sparse.phase_sum_affine_data(profiles)
        rng = random.Random(668)
        points = [(0,) * 54, (1,) * 54, (2,) * 54]
        points.extend(
            tuple(rng.randrange(3) for _ in range(54))
            for _ in range(20)
        )
        for point in points:
            self.assertEqual(
                sparse.evaluate_phase_sum_affine(
                    baseline, effects, point
                ),
                sparse.flattened_phase_sums(profiles, point),
            )

    def test_membership_component_has_exact_witness(self) -> None:
        candidate = sparse.second.CANDIDATES[0]
        profiles = sparse.second.profiles_from_ids(
            candidate[3], candidate[4]
        )
        model = cp_model.CpModel()
        placement = tuple(
            model.new_int_var(0, 2, f"placement_{index}")
            for index in range(54)
        )
        sparse.add_row_margin_membership(
            model,
            placement,
            profiles,
            candidate[3],
            candidate[4],
        )
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 10
        status = solver.solve(model)
        self.assertIn(status, (cp_model.FEASIBLE, cp_model.OPTIMAL))
        point = tuple(solver.value(variable) for variable in placement)
        masks = sparse.second.masks_from_trits(profiles, point)
        sums = sparse.phase_sums_from_masks(*masks)
        catalog = sparse.catalog_phase_sum_intersection(
            candidate[3], candidate[4]
        )
        self.assertIn(
            sums, {value for value, _ in catalog["phase_sum_corpus"]}
        )


if __name__ == "__main__":
    unittest.main()
