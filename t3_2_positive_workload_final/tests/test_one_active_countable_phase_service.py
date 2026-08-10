from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import stoichiometric_gate_feasibility as feasibility


PAIR = (
    closure.mask(("A", "AC")),
    closure.mask(("B", "C", "2B", "AB")),
)


def solve_linear(matrix, right):
    size = len(right)
    augmented = [list(map(float, row)) + [float(value)]
                 for row, value in zip(matrix, right)]
    for column in range(size):
        pivot = max(range(column, size),
                    key=lambda row: abs(augmented[row][column]))
        augmented[column], augmented[pivot] = (
            augmented[pivot], augmented[column]
        )
        scale = augmented[column][column]
        if abs(scale) < 1e-14:
            raise AssertionError("singular occupation system")
        augmented[column] = [value / scale
                             for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                value - factor * pivot_value
                for value, pivot_value
                in zip(augmented[row], augmented[column])
            ]
    return [row[-1] for row in augmented]


def expected_occupation_before_upper_hit(maximum, alpha=1.0, beta=1.0):
    """E_1 integral C_s ds before immigration-death hits M+1."""

    size = maximum + 1
    minus_generator = [[0.0] * size for _ in range(size)]
    reward = [float(state) for state in range(size)]
    for state in range(size):
        birth = alpha
        death = beta * state
        minus_generator[state][state] = birth + death
        if state + 1 < size:
            minus_generator[state][state + 1] = -birth
        if state:
            minus_generator[state][state - 1] = -death
    return solve_linear(minus_generator, reward)[1]


class OneActiveCountablePhaseServiceTests(unittest.TestCase):
    def test_pair_is_an_exact_candidate_one_active_residual(self):
        self.assertIn(
            PAIR,
            closure.residual_pairs(closure.POSITIVE_SHIELDED_MASKS),
        )
        failures = feasibility.feasible_failing_descriptors(PAIR)
        self.assertEqual(len(failures), 3)
        self.assertTrue(
            all(descriptor.weight == (1, 0, 0)
                for descriptor in failures)
        )
        self.assertEqual(
            {descriptor.caps for descriptor in failures},
            {(2, 0, 0), (2, 0, 1), (2, 0, 2)},
        )
        self.assertTrue(
            all(
                tier._gate_mode(PAIR, descriptor)
                == "disabled_source_promotion"
                for descriptor in failures
            )
        )

    def test_displayed_orientation_is_strong(self):
        flat_edges = (("A", "AC"), ("AC", "A"))
        mixed_edges = (
            ("AB", "C"),
            ("C", "B"),
            ("B", "AB"),
            ("B", "2B"),
            ("2B", "B"),
        )

        def reachable(nodes, edges, start):
            seen = {start}
            changed = True
            while changed:
                changed = False
                for source, target in edges:
                    if source in seen and target not in seen:
                        seen.add(target)
                        changed = True
            return seen == set(nodes)

        self.assertTrue(
            all(reachable(("A", "AC"), flat_edges, node)
                for node in ("A", "AC"))
        )
        self.assertTrue(
            all(
                reachable(("AB", "C", "B", "2B"), mixed_edges, node)
                for node in ("AB", "C", "B", "2B")
            )
        )

    def test_fixed_box_service_bound_decays_as_inverse_active_level(self):
        occupation = expected_occupation_before_upper_hit(5)
        self.assertGreater(occupation, 0.0)
        bounds = [occupation / active for active in (100, 1000, 10000)]
        self.assertGreater(bounds[0], bounds[1])
        self.assertGreater(bounds[1], bounds[2])
        self.assertAlmostEqual(bounds[0] / bounds[1], 10.0, places=10)
        self.assertAlmostEqual(bounds[1] / bounds[2], 10.0, places=10)

    def test_successful_immigrant_rate_has_uniform_margin(self):
        alpha = 2.0
        beta = 3.0
        service = 5.0
        margin = alpha * service / (beta + service)
        rates = [
            active * alpha * service / (active * beta + service)
            for active in (1, 10, 100, 1000)
        ]
        self.assertTrue(all(rate >= margin for rate in rates))
        self.assertTrue(
            all(later >= earlier for earlier, later in zip(rates, rates[1:]))
        )


if __name__ == "__main__":
    unittest.main()
