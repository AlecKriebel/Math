from pathlib import Path
import math
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import stoichiometric_gate_feasibility as feasibility
import two_active_phase_gate as phase


PAIR = (
    closure.mask(("2A", "AB")),
    closure.mask(("0", "A", "B")),
)


def descriptor(weight):
    return next(
        item
        for item in tier.tier_descriptors()
        if item.weight == weight and item.caps == (2, 2, 0)
    )


class TwoActiveSubpowerRegressionTests(unittest.TestCase):
    def test_exact_flat_and_refined_order_types_are_distinct(self):
        flat = descriptor((1, 1, 0))
        refined = descriptor((4, 5, 0))

        self.assertTrue(feasibility.descriptor_feasible(PAIR, flat))
        self.assertEqual(
            phase.incidence_category(PAIR, flat),
            "closed_rank_one_top_phase",
        )

        self.assertTrue(feasibility.descriptor_feasible(PAIR, refined))
        self.assertTrue(tier.universal_orientation_tier_condition(PAIR, refined))
        top_d, _ = tier.tier_sets(PAIR, refined)
        self.assertEqual(
            {tier.NAMES[index] for index in top_d},
            {"AB"},
        )

    def test_subpower_sequence_has_the_refined_order(self):
        ratios = []
        occupation_upper_bounds = []
        for exponent in (6, 8, 10, 12):
            n = 10**exponent
            a = int(n / math.log(n))
            b = n - a
            ratios.append(
                (
                    (a * b) / (a * (a - 1)),
                    (a * (a - 1)) / b,
                    b / a,
                )
            )
            # T=beta=1 in (1.4), with a_n=b and total A+B=n.
            occupation_upper_bounds.append((a / b) * math.exp(n / b))

        self.assertTrue(all(first > 1 for first, _, _ in ratios))
        self.assertTrue(all(second > 1 for _, second, _ in ratios))
        self.assertTrue(all(third > 1 for _, _, third in ratios))
        self.assertTrue(
            all(
                later < earlier
                for earlier, later in zip(
                    occupation_upper_bounds,
                    occupation_upper_bounds[1:],
                )
            )
        )
        self.assertLess(occupation_upper_bounds[-1], 0.2)


if __name__ == "__main__":
    unittest.main()
