from __future__ import annotations

import unittest

from ortools.sat.python import cp_model

from construction import goethals_seidel, verify_hadamard
from good_167 import (
    GOOD_167_ROW_SUM_PROFILES,
    good_row_sum_profiles,
    product_cycle_order,
    validate_good_quadruple,
)
from good_167_linear import c_linear_system, derive_s, recover_c_d, solve_linear_system
from search_good_167_cp_sat import _decode, build_model
from verify_good_167 import verify_payload
from analyze_sds_167 import (
    common_multiplier_orbit_compatible,
    four_square_profiles,
    good_parameter_sets,
    gs_parameter_sets,
    williamson_product_counts,
)


class Good167Tests(unittest.TestCase):
    def test_arithmetic_profiles(self) -> None:
        self.assertEqual(
            GOOD_167_ROW_SUM_PROFILES,
            ((-21, -1, 15), (-9, 15, 19)),
        )
        self.assertEqual(product_cycle_order(), 83)
        self.assertEqual(good_row_sum_profiles(5), ((-3, -3, 1),))
        self.assertEqual(good_parameter_sets(5), (((2, 2, 1, 1), 1),))

    def test_sds_parameter_audit(self) -> None:
        profiles = four_square_profiles()
        parameters = gs_parameter_sets()
        self.assertEqual(len(profiles), 10)
        self.assertEqual(len(parameters), 10)
        self.assertEqual(
            good_parameter_sets(),
            (((83, 83, 76, 73), 148), ((83, 79, 76, 74), 145)),
        )
        self.assertFalse(
            any(common_multiplier_orbit_compatible(sizes, 83) for sizes, _ in parameters)
        )
        for profile in profiles:
            total, triples = williamson_product_counts(profile)
            self.assertEqual(total, 83 + 2 * triples)
            self.assertGreaterEqual(triples, 0)
            self.assertLessEqual(triples, 83)

    def test_small_exact_model_finds_good_order_seven(self) -> None:
        profiles = good_row_sum_profiles(7)
        self.assertEqual(profiles, ((-5, -1, -1), (3, 3, 3)))
        model, halves = build_model(7, (3, 3, 3))
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 5
        solver.parameters.num_search_workers = 1
        status = solver.solve(model)
        self.assertIn(status, (cp_model.FEASIBLE, cp_model.OPTIMAL))
        candidate = validate_good_quadruple(_decode(solver, halves), 7)
        matrix = goethals_seidel(candidate)
        verify_hadamard(matrix)
        self.assertTrue(
            all(
                matrix[row][column] + matrix[column][row]
                == (2 if row == column else 0)
                for row in range(28)
                for column in range(28)
            )
        )

        a, b, c, d = candidate
        self.assertEqual(tuple(x * y for x, y in zip(derive_s(a, b), c)), d)
        system, _ = c_linear_system(a, b)
        solution = solve_linear_system(system)
        self.assertIsNotNone(solution)
        assert solution is not None
        self.assertFalse(solution.inconsistent)
        recovered = recover_c_d(a, b, sum(c), sum(d))
        self.assertIn(candidate, recovered.candidates)

        # The order-167 verifier is intentionally strict: a valid small
        # regression fixture must not be misreported as H(668).
        with self.assertRaisesRegex(ValueError, "order must be exactly 167"):
            verify_payload(
                {
                    "kind": "circulant_good_matrices",
                    "order": 7,
                    "hadamard_order": 28,
                    "row_sums": [sum(b), sum(c), sum(d)],
                    "sequences": [list(sequence) for sequence in candidate],
                }
            )


if __name__ == "__main__":
    unittest.main()
