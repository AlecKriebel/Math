import unittest

from run_variable_q_shards import parse_shards
from variable_q_base import (
    ALTERNATION_FIXED_SHARDS,
    ALTERNATION_SHARD_PARTNERS,
    LONG,
    MARGIN_SHARDS,
    MARGIN_SHARD_REPRESENTATIVES,
    SHORT,
    alternating_sum,
    base_correlations,
    canonical_alternation_transform,
    sign_sum,
)


def sequence_with_margins(length: int, ordinary: int, alternating: int) -> tuple[int, ...]:
    result = [0] * length
    for parity, target in (
        (0, (ordinary + alternating) // 2),
        (1, (ordinary - alternating) // 2),
    ):
        positions = list(range(parity, length, 2))
        plus_count = (len(positions) + target) // 2
        for ordinal, position in enumerate(positions):
            result[position] = 1 if ordinal < plus_count else -1
    return tuple(result)


class VariableQBaseSymmetryTests(unittest.TestCase):
    def test_global_alternation_shard_orbits(self) -> None:
        self.assertEqual(len(MARGIN_SHARDS), 288)
        self.assertEqual(len(MARGIN_SHARD_REPRESENTATIVES), 156)
        self.assertEqual(len(ALTERNATION_FIXED_SHARDS), 24)
        for shard, partner in enumerate(ALTERNATION_SHARD_PARTNERS):
            self.assertEqual(ALTERNATION_SHARD_PARTNERS[partner], shard)
            self.assertIn(min(shard, partner), MARGIN_SHARD_REPRESENTATIVES)
        self.assertEqual(parse_shards("all"), MARGIN_SHARD_REPRESENTATIVES)
        self.assertEqual(parse_shards("0-287"), tuple(range(288)))

    def test_transform_maps_every_shard_and_preserves_equations(self) -> None:
        lengths = (LONG, LONG, SHORT, SHORT)
        for shard, (ordinary, alternating) in enumerate(MARGIN_SHARDS):
            sequences = tuple(
                sequence_with_margins(length, row_sum, alt_sum)
                for length, row_sum, alt_sum in zip(
                    lengths, ordinary, alternating, strict=True
                )
            )
            transformed = canonical_alternation_transform(*sequences)
            partner_margins = MARGIN_SHARDS[ALTERNATION_SHARD_PARTNERS[shard]]
            self.assertEqual(
                tuple(sign_sum(sequence) for sequence in transformed),
                partner_margins[0],
            )
            self.assertEqual(
                tuple(alternating_sum(sequence) for sequence in transformed),
                partner_margins[1],
            )
            before = base_correlations(*sequences)
            after = base_correlations(*transformed)
            self.assertEqual(
                after,
                tuple(((-1) ** lag) * value for lag, value in enumerate(before)),
            )
            if shard in ALTERNATION_FIXED_SHARDS:
                self.assertEqual(
                    canonical_alternation_transform(*transformed), sequences
                )


if __name__ == "__main__":
    unittest.main()
