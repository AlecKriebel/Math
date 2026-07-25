"""Small deterministic tests for the continuous rank/BV discovery model."""

from fractions import Fraction as Q
import unittest

from experiments.continuous_rank_bv_search.search import (
    Kernel,
    adaptive_grid,
    ceil_sqrt_scaled,
    coefficient_arrays,
    common_pair_capacity,
    default_kernels,
    feasible_orbits,
    gegenbauer_5,
    global_secant_slope,
    gram_determinant,
    parse_grid,
    rational_radius_chord,
    stratified_capacity_rows,
    transverse_q,
    weighted_capacity_rows,
)
from experiments.continuous_rank_bv_search.audit_common_pair_witness import (
    audit,
)
from experiments.continuous_rank_bv_search.audit_capacity_barriers import (
    audit as audit_capacity,
)
from pathlib import Path


class ContinuousRankBVSearchTests(unittest.TestCase):
    def test_grids_and_orbits(self):
        quarter = parse_grid("quarter")
        eighth = parse_grid("eighth")
        self.assertEqual(len(quarter), 7)
        self.assertEqual(len(eighth), 13)
        self.assertEqual(len(feasible_orbits(quarter)), 51)
        self.assertEqual(len(feasible_orbits(eighth)), 297)
        for triple in feasible_orbits(eighth):
            self.assertGreaterEqual(
                gram_determinant(*(eighth[index] for index in triple)),
                0,
            )
        rows = stratified_capacity_rows(eighth, feasible_orbits(eighth))
        self.assertTrue(
            any(
                row["lower"] == row["upper"] == Q(-1, 4)
                and row["high"] == Q(1, 2)
                and row["p"] == Q(2, 3)
                and row["capacity"] == 3
                for row in rows
            )
        )
        weighted = weighted_capacity_rows(eighth, feasible_orbits(eighth))
        contact = next(row for row in weighted if row["high"] == Q(1, 2))
        expected = {
            Q(-1): 0,
            Q(-1, 2): 1,
            Q(-1, 4): 3,
            Q(0): 6,
            Q(1, 4): 7,
            Q(1, 2): 7,
        }
        for node, capacity in expected.items():
            self.assertEqual(
                contact["capacities"][eighth.index(node)], capacity
            )

    def test_polynomial_normalizations(self):
        self.assertEqual(gegenbauer_5(Q(1, 2), 2)[2], Q(1, 16))
        self.assertEqual(
            transverse_q(Q(0), Q(0), Q(1, 2), 3),
            (Q(1), Q(1, 2), Q(0), Q(-1, 4)),
        )
        nodes = parse_grid("quarter")
        orbits = feasible_orbits(nodes)
        constants, alpha, nu = coefficient_arrays(nodes, orbits, 2)
        self.assertEqual(constants[0].shape, (8, 8))
        self.assertEqual(alpha[0].shape, (64, 7))
        self.assertEqual(nu[0].shape, (64, 51))

    def test_rational_outer_slope(self):
        kernel = Kernel("H1", ((1, Q(1)),))
        upper = Q(25, 4)
        slope = global_secant_slope(upper, kernel.rank, 10**6)
        self.assertGreaterEqual(
            slope**2 * kernel.rank * (kernel.rank - 1),
            (kernel.rank - 2) ** 2 * upper,
        )
        root = ceil_sqrt_scaled(Q(2), 10**6)
        self.assertGreaterEqual(root * root, 2)
        self.assertLess((root - Q(1, 10**6)) ** 2, 2)
        self.assertEqual(common_pair_capacity(Q(2, 3)), 3)
        self.assertEqual(common_pair_capacity(Q(2, 3) + Q(1, 1000)), 2)
        slope, intercept, y0, y1 = rational_radius_chord(
            Q(1, 4), Q(1), 5, 10**6
        )
        self.assertEqual(slope * Q(1, 4) + intercept, y0)
        self.assertEqual(slope + intercept, y1)
        for value in (Q(1, 4), Q(1, 2), Q(3, 4), Q(1)):
            radius_squared = Q(9, 20) * value**3
            self.assertGreaterEqual(
                (slope * value + intercept) ** 2, radius_squared
            )

    def test_adaptive_grid_and_kernel_ranks(self):
        grid = parse_grid("quarter")
        refined = adaptive_grid(grid, [0, 1, 0, 0, 0, 0, 0])
        self.assertIn(Q(-7, 8), refined)
        self.assertIn(Q(-5, 8), refined)
        self.assertTrue(all(2 <= kernel.rank < 41 for kernel in default_kernels()))

    def test_exact_common_pair_audit(self):
        root = Path(__file__).resolve().parents[2]
        result = audit(
            root
            / "certificates"
            / "common_pair_capacity_degree4_pseudodistribution.json"
        )
        self.assertEqual(result["kernel_count"], 27)
        self.assertIn(result["minimum_residual_kernel"], result["results"])
        capacity = audit_capacity(
            root
            / "certificates"
            / "fixed41_bv_fullradial_k16_pseudodistribution.json"
        )
        self.assertFalse(capacity["passes_all_stratified_rows"])
        self.assertEqual(
            capacity["minimum_stratified_row"],
            {
                "lower": "-1/4",
                "upper": "-1/4",
                "high": "1/2",
                "p": "2/3",
                "capacity": 3,
            },
        )


if __name__ == "__main__":
    unittest.main()
