#!/usr/bin/env python3
"""Focused exact tests for the sextic-cyclotomic LP(333) CP-SAT model."""

from __future__ import annotations

import tempfile
import unittest
from itertools import product
from pathlib import Path

from ortools.sat.python import cp_model

from check_lp333_sextic_quotient import (
    CLASS_OF,
    N,
    ROOTS,
    ROWS,
    SKELETON_EXPONENTS,
    crt_correlation_real,
    expand_crt_array,
    expand_length333,
    multiply_conjugate,
    phase_sum,
    qpsk_to_sign_pair,
    quotient_correlation_real,
    quotient_phase_table,
    sequence_correlation_real,
)
from legendre_333 import verify_fixed_compression
from search_lp333_sextic_cp_sat import (
    CANONICAL_ZERO_EXPONENTS,
    PRIMARY_SIGN_BITS,
    QUOTIENT_EQUATIONS,
    SIGNATURES,
    SIGNATURE_SHARD_VECTORS,
    SIGN_PAIR_TO_EXPONENT,
    TARGET_XOR_COUNT,
    _add_c3_signature_lex_leader,
    aggregate_signature_table,
    _cached_xor,
    build_model,
    canonical_signatures,
    expand_sign_sequences,
    exponent_to_sign_pair,
    negate_signature_vector,
    real_paf_signature,
    sign_pair_to_exponent,
    signature_catalog_counts,
    signature_triples_for_shard,
    signature_word_table,
    target_phase_word_records,
    validate_quotient_exponents,
    verify_and_save_candidate,
    weighted_xor_count,
)
from verify_lp333_sextic_c3 import (
    literal_c3_canonical,
    verify_c3_reduction,
)


# The audited nonzero skeleton columns have the required alternating phase
# sums.  Replacing only its zero column supplies a deterministic fixture in the
# exact canonical fiber; it is intentionally not a Legendre pair.
FIXTURE_EXPONENTS = tuple(
    (CANONICAL_ZERO_EXPONENTS[row], *SKELETON_EXPONENTS[row][1:])
    for row in range(ROWS)
)


class SexticCpSatTests(unittest.TestCase):
    def test_cached_xor_encoding_and_reuse(self) -> None:
        for left_value in (0, 1):
            for right_value in (0, 1):
                model = cp_model.CpModel()
                left = model.new_bool_var("left")
                right = model.new_bool_var("right")
                cache: dict[tuple[int, int], cp_model.IntVar] = {}
                difference = _cached_xor(model, left, right, cache)
                reversed_difference = _cached_xor(
                    model, right, left, cache
                )
                self.assertEqual(difference.index, reversed_difference.index)
                self.assertEqual(len(cache), 1)
                model.add(left == left_value)
                model.add(right == right_value)
                solver = cp_model.CpSolver()
                self.assertIn(
                    solver.solve(model), (cp_model.FEASIBLE, cp_model.OPTIMAL)
                )
                self.assertEqual(
                    solver.value(difference), left_value ^ right_value
                )

    def test_qpsk_sign_pair_convention(self) -> None:
        self.assertEqual(
            tuple(exponent_to_sign_pair(exponent) for exponent in range(4)),
            ((1, 1), (-1, 1), (-1, -1), (1, -1)),
        )
        self.assertEqual(
            {
                exponent_to_sign_pair(exponent): exponent
                for exponent in range(4)
            },
            SIGN_PAIR_TO_EXPONENT,
        )
        for exponent in range(4):
            signs = exponent_to_sign_pair(exponent)
            self.assertEqual(sign_pair_to_exponent(*signs), exponent)

        # Verify the binary/QPSK real-inner-product identity on all 16 pairs.
        for left in range(4):
            for right in range(4):
                a_left, b_left = exponent_to_sign_pair(left)
                a_right, b_right = exponent_to_sign_pair(right)
                qpsk_twice_real = 2 * multiply_conjugate(
                    ROOTS[left], ROOTS[right]
                )[0]
                self.assertEqual(
                    a_left * a_right + b_left * b_right,
                    qpsk_twice_real,
                )

    def test_model_validity_and_exact_counts(self) -> None:
        bundle = build_model()
        self.assertEqual(bundle.model.validate(), "")
        counts = bundle.exact_counts()
        self.assertEqual(counts["primary_sign_bits"], PRIMARY_SIGN_BITS)
        self.assertEqual(PRIMARY_SIGN_BITS, 108)
        self.assertEqual(counts["cached_xor_variables"], 2862)
        self.assertEqual(counts["signature_variables"], 6)
        self.assertEqual(counts["signature_shard_variables"], 1)
        self.assertEqual(counts["c3_variables"], 2)
        self.assertEqual(counts["total_variables"], 2979)
        self.assertEqual(counts["quotient_lag_constraints"], 34)
        self.assertEqual(counts["compression_constraints"], 12)
        self.assertEqual(counts["signature_constraints"], 8)
        self.assertEqual(counts["c3_constraints"], 7)
        self.assertEqual(counts["total_constraints"], 2923)
        self.assertEqual(
            counts["total_variables"],
            counts["primary_sign_bits"]
            + counts["cached_xor_variables"]
            + counts["signature_variables"]
            + counts["signature_shard_variables"]
            + counts["c3_variables"],
        )
        self.assertEqual(
            counts["total_constraints"],
            counts["cached_xor_variables"] + 12 + 34 + 8 + 7,
        )
        self.assertEqual(len(QUOTIENT_EQUATIONS), 34)

        sharded = build_model(signature_shard=0)
        self.assertEqual(sharded.model.validate(), "")
        sharded_counts = sharded.exact_counts()
        self.assertEqual(sharded_counts["signature_variables"], 6)
        self.assertEqual(sharded_counts["signature_shard_variables"], 0)
        self.assertEqual(sharded_counts["c3_variables"], 2)
        self.assertEqual(sharded_counts["total_variables"], 2978)
        self.assertEqual(sharded_counts["total_constraints"], 2923)

        unsymmetrized = build_model(c3_symmetry=False)
        self.assertEqual(unsymmetrized.model.validate(), "")
        unsymmetrized_counts = unsymmetrized.exact_counts()
        self.assertEqual(unsymmetrized_counts["c3_variables"], 0)
        self.assertEqual(unsymmetrized_counts["c3_constraints"], 0)
        self.assertEqual(unsymmetrized_counts["total_variables"], 2977)
        self.assertEqual(unsymmetrized_counts["total_constraints"], 2916)

    def test_old_model_count_regression(self) -> None:
        bundle = build_model(signature_channel=False)
        self.assertEqual(bundle.model.validate(), "")
        counts = bundle.exact_counts()
        self.assertEqual(counts["primary_sign_bits"], 108)
        self.assertEqual(counts["cached_xor_variables"], 2862)
        self.assertEqual(counts["signature_variables"], 0)
        self.assertEqual(counts["signature_shard_variables"], 0)
        self.assertEqual(counts["c3_variables"], 0)
        self.assertEqual(counts["total_variables"], 2970)
        self.assertEqual(counts["compression_constraints"], 12)
        self.assertEqual(counts["quotient_lag_constraints"], 34)
        self.assertEqual(counts["signature_constraints"], 0)
        self.assertEqual(counts["c3_constraints"], 0)
        self.assertEqual(counts["total_constraints"], 2908)
        with self.assertRaisesRegex(ValueError, "requires the signature channel"):
            build_model(signature_channel=False, signature_shard=0)

    def test_c3_exact_tie_encoding_and_burnside_audit(self) -> None:
        counts = verify_c3_reduction()
        self.assertEqual(
            counts,
            {
                "ordered_signature_sextuples": 1_658_700,
                "fixed_points": 18,
                "signature_sextuple_c3_orbits": 552_912,
                "canonical_signature_sextuples": 552_912,
                "compatible_signature_shards": 298,
                "zero_words": 972,
                "normalization_group_actions": 972,
                "class_rotation_normalization_actions": 5_832,
                "distinct_zero_word_images": 972,
                "surviving_class_rotations": 3,
                "expanded_fixtures": 2,
                "full_correlation_checks": 666,
                "canonical_zero_columns_fixed": 2,
                "multiplier_64_replays": 2,
            },
        )

        # Exercise every strict/tied order pattern using three small pair
        # codes, including p0=p2<p1, which a mere p0-minimum test accepts
        # incorrectly.
        for pair_codes in product(range(3), repeat=3):
            model = cp_model.CpModel()
            signatures = tuple(
                model.new_int_var(0, 27, f"signature_{index}")
                for index in range(6)
            )
            _, constraint_count = _add_c3_signature_lex_leader(
                model, signatures
            )
            self.assertEqual(constraint_count, 7)
            for pair_index, pair_code in enumerate(pair_codes):
                model.add(signatures[2 * pair_index] == 0)
                model.add(signatures[2 * pair_index + 1] == pair_code)
            solver = cp_model.CpSolver()
            status = solver.solve(model)
            feasible = status in (cp_model.FEASIBLE, cp_model.OPTIMAL)
            self.assertEqual(feasible, literal_c3_canonical(pair_codes))

    def test_signature_catalog_tables_and_shards(self) -> None:
        negative_records = target_phase_word_records(-3)
        positive_records = target_phase_word_records(3)
        self.assertEqual(len(negative_records), 7_056)
        self.assertEqual(len(positive_records), 7_056)
        negative_signatures = {signature for _, signature in negative_records}
        positive_signatures = {signature for _, signature in positive_records}
        self.assertEqual(negative_signatures, positive_signatures)
        self.assertEqual(len(negative_signatures), 28)
        self.assertEqual(canonical_signatures(), SIGNATURES)
        self.assertEqual(set(SIGNATURES), negative_signatures)

        for imaginary_sum, records in (
            (-3, negative_records),
            (3, positive_records),
        ):
            table = signature_word_table(imaginary_sum)
            self.assertEqual(len(table), 7_056)
            decoded: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
            for row in table:
                self.assertEqual(len(row), 19)
                word = tuple(
                    sign_pair_to_exponent(
                        1 if row[index] else -1,
                        1 if row[ROWS + index] else -1,
                    )
                    for index in range(ROWS)
                )
                signature = real_paf_signature(word)
                self.assertEqual(phase_sum(word), (0, imaginary_sum))
                self.assertEqual(signature, SIGNATURES[row[-1]])
                decoded.append((word, signature))
            self.assertEqual(tuple(decoded), records)

        self.assertEqual(len(SIGNATURE_SHARD_VECTORS), 298)
        even_sizes = tuple(
            len(signature_triples_for_shard(shard))
            for shard in range(len(SIGNATURE_SHARD_VECTORS))
        )
        odd_sizes = tuple(
            len(signature_triples_for_shard(shard, odd=True))
            for shard in range(len(SIGNATURE_SHARD_VECTORS))
        )
        self.assertEqual(min((*even_sizes, *odd_sizes)), 1)
        self.assertEqual(max((*even_sizes, *odd_sizes)), 195)
        self.assertEqual(
            sum(
                even_sizes[shard] * odd_sizes[shard]
                for shard in range(len(SIGNATURE_SHARD_VECTORS))
            ),
            1_658_700,
        )
        self.assertEqual(
            len(aggregate_signature_table(False)), sum(even_sizes)
        )
        self.assertEqual(
            len(aggregate_signature_table(True)), sum(odd_sizes)
        )
        self.assertEqual(
            signature_catalog_counts(),
            {
                "negative_target_words": 7_056,
                "positive_target_words": 7_056,
                "signatures": 28,
                "signature_shards": 298,
                "minimum_triple_table_rows": 1,
                "maximum_triple_table_rows": 195,
                "unsharded_even_table_rows": 18_354,
                "unsharded_odd_table_rows": 18_354,
                "ordered_signature_sextuples": 1_658_700,
            },
        )
        for shard, vector in enumerate(SIGNATURE_SHARD_VECTORS):
            for triple in signature_triples_for_shard(shard):
                direct = tuple(
                    sum(SIGNATURES[index][coordinate] for index in triple)
                    for coordinate in range(4)
                )
                self.assertEqual(direct, vector)
            for triple in signature_triples_for_shard(shard, odd=True):
                direct = tuple(
                    sum(SIGNATURES[index][coordinate] for index in triple)
                    for coordinate in range(4)
                )
                self.assertEqual(direct, negate_signature_vector(vector))

    def test_weighted_equations_match_quotient_and_full_expansion(self) -> None:
        exponents = validate_quotient_exponents(FIXTURE_EXPONENTS)
        quotient = quotient_phase_table(exponents)
        array = expand_crt_array(exponents)
        qpsk_sequence = expand_length333(array)
        a, b = expand_sign_sequences(exponents)

        for equation in QUOTIENT_EQUATIONS:
            distance = weighted_xor_count(
                exponents, equation.row_lag, equation.matrix
            )
            quotient_value = quotient_correlation_real(
                quotient, equation.row_lag, equation.matrix
            )
            direct_crt = crt_correlation_real(
                array, equation.row_lag, equation.column_lag
            )
            physical_lag = next(
                lag
                for lag in range(N)
                if lag % ROWS == equation.row_lag
                and lag % 37 == equation.column_lag
            )
            direct_qpsk = sequence_correlation_real(qpsk_sequence, physical_lag)
            direct_binary = sum(
                a[index] * a[(index + physical_lag) % N]
                + b[index] * b[(index + physical_lag) % N]
                for index in range(N)
            )
            self.assertEqual(distance, N - quotient_value)
            self.assertEqual(direct_crt, quotient_value)
            self.assertEqual(direct_qpsk, quotient_value)
            self.assertEqual(direct_binary, 2 * quotient_value)
            self.assertEqual(
                direct_binary, 2 * N - 2 * distance
            )

        # The target conversion itself is exact.
        self.assertEqual(TARGET_XOR_COUNT, N - (-1))

    def test_candidate_expansion_and_rejection_replay(self) -> None:
        exponents = validate_quotient_exponents(FIXTURE_EXPONENTS)
        a, b = expand_sign_sequences(exponents)
        self.assertEqual(len(a), N)
        self.assertEqual(len(b), N)
        self.assertEqual(
            tuple(
                qpsk_to_sign_pair(ROOTS[exponents[index % 9][
                    0 if index % 37 == 0 else
                    CLASS_OF[index % 37] + 1
                ]])
                for index in range(N)
            ),
            tuple(zip(a, b, strict=True)),
        )
        fixed, _, _ = verify_fixed_compression(a, b)
        self.assertTrue(fixed)

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "must_not_exist.json"
            with self.assertRaisesRegex(ValueError, "quotient equation"):
                verify_and_save_candidate(output, exponents)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
