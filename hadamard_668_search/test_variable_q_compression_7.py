import unittest

from ortools.sat.python import cp_model

from search_variable_q_cp_sat import add_length_seven_compression_invariants
from variable_q_base import LONG, SHORT, globally_alternate
from variable_q_compression_7 import (
    ENERGY,
    ORDINARY_PROFILE_WITNESSES,
    SIGNATURE_FILTER_COUNTS_LONG,
    SIGNATURE_FILTER_COUNTS_SHORT,
    TARGET_SIGNATURE,
    add_signatures,
    compressed_signature_seven,
    compress_modulo_seven,
    factor12_cell_alphabets,
    factor12_compression_identity,
    primitive_seven_psds_within_bound,
    verify_all_shards_survive,
)


def lift_cell_sums(vector: tuple[int, ...], length: int) -> tuple[int, ...]:
    """Choose one sign sequence with the requested residue sums."""

    signs = [-1] * length
    for residue, target in enumerate(vector):
        positions = list(range(residue, length, 7))
        positive = (len(positions) + target) // 2
        if 2 * positive - len(positions) != target:
            raise AssertionError("cell target has the wrong parity")
        for index in positions[:positive]:
            signs[index] = 1
    return tuple(signs)


class VariableQCompressionSevenTests(unittest.TestCase):
    def test_compression_identity_and_cell_alphabets(self) -> None:
        for length, modulus in ((LONG, 29), (SHORT, 31)):
            sequence = tuple(
                1 if (17 * index + 5) % modulus < modulus // 2 else -1
                for index in range(length)
            )
            compressed = compress_modulo_seven(sequence)
            self.assertEqual(
                factor12_compression_identity(sequence)[:4],
                compressed_signature_seven(compressed),
            )
            self.assertTrue(
                all(
                    value in alphabet
                    for value, alphabet in zip(
                        compressed, factor12_cell_alphabets(length), strict=True
                    )
                )
            )

    def test_all_margin_shards_have_exact_witnesses(self) -> None:
        verify_all_shards_survive()

    def test_exact_primitive_seven_filter_and_recorded_counts(self) -> None:
        witness = ORDINARY_PROFILE_WITNESSES[(14, 8, 7, 5)]
        signatures = tuple(compressed_signature_seven(vector) for vector in witness)
        self.assertEqual(add_signatures(*signatures), TARGET_SIGNATURE)
        self.assertTrue(
            all(
                signature[0] <= ENERGY
                and primitive_seven_psds_within_bound(signature)
                for signature in signatures
            )
        )
        self.assertEqual(SIGNATURE_FILTER_COUNTS_LONG[14], (23261, 4397))
        self.assertEqual(SIGNATURE_FILTER_COUNTS_SHORT[7], (180578, 28485))

    def test_cp_invariant_accepts_an_independent_compressed_witness(self) -> None:
        witness = ORDINARY_PROFILE_WITNESSES[(14, 8, 7, 5)]
        lifted = tuple(
            lift_cell_sums(vector, length)
            for vector, length in zip(
                witness, (LONG, LONG, SHORT, SHORT), strict=True
            )
        )
        model = cp_model.CpModel()
        variables = tuple(
            [
                model.new_bool_var(f"{label}_{index}")
                for index in range(length)
            ]
            for label, length in zip("abcd", (LONG, LONG, SHORT, SHORT), strict=True)
        )
        for bits, sequence in zip(variables, lifted, strict=True):
            for bit, sign in zip(bits, sequence, strict=True):
                model.add(bit == int(sign == 1))
        add_length_seven_compression_invariants(model, variables)
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 1
        solver.parameters.max_memory_in_mb = 256
        self.assertEqual(solver.solve(model), cp_model.OPTIMAL)

        # Alternating the pinned fixture and asking for the alternating
        # compression applies the coordinate involution twice, so the same
        # exact compressed witness must be accepted.
        alternated = tuple(globally_alternate(sequence) for sequence in lifted)
        alt_model = cp_model.CpModel()
        alt_variables = tuple(
            [
                alt_model.new_bool_var(f"{label}_{index}")
                for index in range(length)
            ]
            for label, length in zip(
                "abcd", (LONG, LONG, SHORT, SHORT), strict=True
            )
        )
        for bits, sequence in zip(alt_variables, alternated, strict=True):
            for bit, sign in zip(bits, sequence, strict=True):
                alt_model.add(bit == int(sign == 1))
        add_length_seven_compression_invariants(
            alt_model, alt_variables, coordinate_alternation=True
        )
        alt_solver = cp_model.CpSolver()
        alt_solver.parameters.num_search_workers = 1
        alt_solver.parameters.max_memory_in_mb = 256
        self.assertEqual(alt_solver.solve(alt_model), cp_model.OPTIMAL)


if __name__ == "__main__":
    unittest.main()
