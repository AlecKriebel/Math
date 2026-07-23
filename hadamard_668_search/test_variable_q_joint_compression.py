from __future__ import annotations

import unittest

from variable_q_base import LONG, MARGIN_SHARDS, SHORT, alternating_sum, sign_sum
from variable_q_joint_compression import (
    build_model,
    joint_cell_pairs,
    joint_compress,
)


class VariableQJointCompressionTests(unittest.TestCase):
    def test_cell_pair_tables_are_exact(self) -> None:
        for length in (LONG, SHORT):
            for residue in range(7):
                positions = tuple(range(residue, length, 7))
                observed = set()
                for mask in range(1 << len(positions)):
                    signs = tuple(
                        -1 if (mask >> index) & 1 else 1
                        for index in range(len(positions))
                    )
                    observed.add(
                        (
                            sum(signs),
                            sum(
                                (1 if position % 2 == 0 else -1) * sign
                                for position, sign in zip(
                                    positions, signs, strict=True
                                )
                            ),
                        )
                    )
                self.assertEqual(set(joint_cell_pairs(length, residue)), observed)

    def test_joint_compression_preserves_both_margins(self) -> None:
        for length, modulus in ((LONG, 29), (SHORT, 31)):
            sequence = tuple(
                1 if (17 * index + 5) % modulus < modulus // 2 else -1
                for index in range(length)
            )
            raw, alt = joint_compress(sequence)
            self.assertEqual(sum(raw), sign_sum(sequence))
            self.assertEqual(sum(alt), alternating_sum(sequence))
            self.assertTrue(
                all(
                    pair in joint_cell_pairs(length, residue)
                    for residue, pair in enumerate(zip(raw, alt, strict=True))
                )
            )

    def test_all_joint_models_validate(self) -> None:
        for shard in range(len(MARGIN_SHARDS)):
            model, _variables = build_model(shard)
            self.assertEqual(model.validate(), "")


if __name__ == "__main__":
    unittest.main()
