import json
from pathlib import Path
import unittest

from seed import aperiodic_autocorrelation
from variable_q_base import alternating_sum, sign_sum
from variable_q_parity_neighborhood import (
    apply_flip_key,
    delta_syndrome,
    flip_delta,
    half_residuals,
    key_delta,
    scan_neighborhood,
    zero_syndrome_flip_keys,
)
from verify_variable_q import extract_candidate


CHECKPOINT = (
    Path(__file__).resolve().parent
    / "output"
    / "variable_q_parity_best_canonical.json"
)


class VariableQParityNeighborhoodTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        payload = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
        a, b, c, d, _s, _q = extract_candidate(payload)
        cls.base = (a, b, c, d)

    def test_flip_delta_matches_direct_recomputation(self) -> None:
        sequence = self.base[0]
        flipped = (1, 8, 40, 67)
        changed = tuple(
            -value if index in flipped else value
            for index, value in enumerate(sequence)
        )
        expected = (0,) + tuple(
            (
                aperiodic_autocorrelation(changed, lag)
                - aperiodic_autocorrelation(sequence, lag)
            )
            // 2
            for lag in range(1, 84)
        )
        self.assertEqual(flip_delta(sequence, flipped), expected)

    def test_exact_radius_four_regression(self) -> None:
        result = scan_neighborhood(self.base, max_exchanges=2)
        self.assertEqual(result.initial_energy, 232)
        self.assertEqual(
            tuple(
                (
                    item.exchanges,
                    item.candidates,
                    item.minimum_energy,
                    item.minimizers,
                )
                for item in result.distances
            ),
            ((1, 34, 272, 1), (2, 3646, 248, 1)),
        )
        self.assertTrue(result.strict_local_minimum)
        self.assertFalse(result.exact_found)

    def test_triple_exchange_enumerator_is_distinct_and_feasible(self) -> None:
        keys = zero_syndrome_flip_keys(self.base, exchanges=3)
        self.assertEqual(len(keys), 159558)
        self.assertEqual(len(keys), len(set(keys)))
        before_margins = tuple(
            (sign_sum(sequence), alternating_sum(sequence))
            for sequence in self.base
        )
        before_residual = half_residuals(self.base)
        # Check a deterministic spread without making the unit test evaluate
        # all 159,558 correlation vectors.
        for key in keys[:: max(1, len(keys) // 97)]:
            self.assertEqual(sum(mask.bit_count() for mask in key), 6)
            delta = key_delta(self.base, key)[1:]
            self.assertEqual(delta_syndrome((0, *delta)), 0)
            changed = apply_flip_key(self.base, key)
            self.assertEqual(
                tuple(
                    (sign_sum(sequence), alternating_sum(sequence))
                    for sequence in changed
                ),
                before_margins,
            )
            self.assertEqual(
                half_residuals(changed),
                tuple(
                    value + change
                    for value, change in zip(before_residual, delta, strict=True)
                ),
            )


if __name__ == "__main__":
    unittest.main()
