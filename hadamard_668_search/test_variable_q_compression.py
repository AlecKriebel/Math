import unittest

from variable_q_base import LONG, MARGIN_SHARDS, SHORT
from variable_q_compression import (
    ENERGY,
    TARGET_SIGNATURE,
    compressed_psds,
    compressed_signature,
    compression_candidates,
    compression_identity,
    compress_modulo_six,
    shard_compression_analysis,
)


class VariableQCompressionTests(unittest.TestCase):
    def test_compression_identity_for_both_lengths(self) -> None:
        for length, modulus in ((LONG, 29), (SHORT, 31)):
            sequence = tuple(1 if (17 * index + 5) % modulus < modulus // 2 else -1 for index in range(length))
            compressed = compress_modulo_six(sequence)
            self.assertEqual(compression_identity(sequence)[:4], compressed_signature(compressed))

    def test_fourier_formulas(self) -> None:
        vector = (-4, 2, 8, -6, 0, 4)
        signature = compressed_signature(vector)
        psds = compressed_psds(signature)
        self.assertEqual(psds[0], sum(vector) ** 2)
        self.assertEqual(psds[3], sum(value if index % 2 == 0 else -value for index, value in enumerate(vector)) ** 2)
        self.assertTrue(all(value >= 0 for value in psds))

    def test_candidate_margins_alphabets_and_bounds(self) -> None:
        ordinary, alternating = MARGIN_SHARDS[235]
        for length, row_sum, alt_sum in zip((LONG, LONG, SHORT, SHORT), ordinary, alternating, strict=True):
            candidates = compression_candidates(length, row_sum, alt_sum)
            self.assertTrue(candidates)
            for vector in candidates:
                self.assertEqual(sum(vector), row_sum)
                self.assertEqual(
                    sum(value if index % 2 == 0 else -value for index, value in enumerate(vector)),
                    alt_sum,
                )
                signature = compressed_signature(vector)
                self.assertLessEqual(signature[0], ENERGY)
                self.assertTrue(all(0 <= value <= ENERGY for value in compressed_psds(signature)))

    def test_exact_signature_join(self) -> None:
        analysis = shard_compression_analysis(235)
        self.assertTrue(analysis["compression_feasible"])
        self.assertGreater(analysis["matching_pair_sum_count"], 0)
        self.assertEqual(TARGET_SIGNATURE, (334, 0, 0, 0))


if __name__ == "__main__":
    unittest.main()
