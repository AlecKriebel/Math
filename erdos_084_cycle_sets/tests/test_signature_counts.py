from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from signature_counts import (  # noqa: E402
    generator_mask,
    p_elements,
    signature_family,
    statistics,
    value_bit,
)


class SignatureCountTests(unittest.TestCase):
    def test_p_mask_decoding(self) -> None:
        self.assertEqual(list(p_elements(3, 0b100101)), [1, 3, 6])

    def test_generator_example(self) -> None:
        # k=2, P={1,4}, b=2:
        # {2,-2} union ({1,-2} intersect [-2,2]) = {-2,1,2}.
        p_mask = (1 << 0) | (1 << 3)
        expected = value_bit(2, -2) | value_bit(2, 1) | value_bit(2, 2)
        self.assertEqual(generator_mask(2, p_mask, 2), expected)

    def test_known_small_families(self) -> None:
        self.assertEqual(sum(len(signature_family(1, p)) for p in range(4)), 10)
        self.assertEqual(sum(len(signature_family(2, p)) for p in range(16)), 102)

    def test_known_statistics_through_k3(self) -> None:
        expected = {
            1: (10, 7, 2, 2, 2),
            2: (102, 67, 12, 12, 12),
            3: (1020, 508, 94, 108, 90),
        }
        for k, values in expected.items():
            row = statistics(k, verify_trace_equivalence=True)
            self.assertEqual(
                (
                    row.s,
                    row.e,
                    row.trace_total,
                    row.restricted_collision_energy,
                    row.restricted_distinct_outputs,
                ),
                values,
            )

    def test_restricted_witness_total(self) -> None:
        # The closed formula applies for k>=2.
        for k in range(2, 5):
            row = statistics(k)
            self.assertEqual(row.restricted_witnesses, 12 * 8 ** (k - 2))


if __name__ == "__main__":
    unittest.main()
