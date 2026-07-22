"""Regression tests for the fixed-compression Legendre-pair lane."""

from __future__ import annotations

from math import gcd
import unittest

from ortools.sat.python import cp_model

from legendre_333 import (
    FIXED_COMPRESSION_A,
    FIXED_COMPRESSION_B,
    FIXED_PLUS_COUNTS_A,
    FIXED_PLUS_COUNTS_B,
    N,
    compression_37,
    crt_coordinates,
    crt_index,
    crt_matrix,
    periodic_autocorrelation,
    sequence_from_crt_matrix,
    verify_fixed_seed_identities,
    verify_legendre_pair,
    xor_distance,
)
from search_legendre_333_cp_sat import (
    MONOCHROMATIC_TRIPLE_ROWS,
    MOD3_COMPRESSION_TUPLES,
    add_cycle_parity_constraints,
    add_lexicographic_greater_or_equal,
    add_mod111_compression_equations,
    add_xor_difference,
    build_model,
    canonicalize_hint,
    cyclic_shift_cycles,
    fixed_compression_distance_bounds,
    generate_mod3_compression_tuples,
    raw_column_distance_bounds,
)
from verify_legendre_333 import deterministic_margin_sequence
from verify_legendre_symmetry_obstruction import (
    admissible_compression,
    compressed_energy_target,
    skew_mod3_compression,
    symmetric_mod3_compression,
    verify_obstruction,
)


class LegendreArithmeticTests(unittest.TestCase):
    def test_symmetric_and_skew_obstruction(self) -> None:
        self.assertEqual(compressed_energy_target(), 446)
        for parameter in (-111, -1, 1, 111):
            compression = symmetric_mod3_compression(parameter)
            self.assertEqual(sum(compression), 1)
            self.assertEqual(compression[1], compression[2])
            skew_compression = skew_mod3_compression(parameter)
            self.assertEqual(sum(skew_compression), 1)
            self.assertEqual(skew_compression[1], -skew_compression[2])
        self.assertTrue(admissible_compression(symmetric_mod3_compression(55)))
        self.assertFalse(admissible_compression(symmetric_mod3_compression(57)))
        self.assertEqual(verify_obstruction(), 28_224)

    def test_fixed_seed_identities(self) -> None:
        verify_fixed_seed_identities()

    def test_crt_bijection_and_round_trip(self) -> None:
        indices = {
            crt_index(row, column) for row in range(9) for column in range(37)
        }
        self.assertEqual(indices, set(range(N)))
        for row in range(9):
            for column in range(37):
                self.assertEqual(crt_coordinates(crt_index(row, column)), (row, column))

        sequence = tuple(1 if index % 5 in (0, 1) else -1 for index in range(N))
        self.assertEqual(sequence_from_crt_matrix(crt_matrix(sequence)), sequence)

    def test_deterministic_fixture_has_exact_margins(self) -> None:
        a = deterministic_margin_sequence(FIXED_PLUS_COUNTS_A)
        b = deterministic_margin_sequence(FIXED_PLUS_COUNTS_B)
        self.assertEqual(compression_37(a), FIXED_COMPRESSION_A)
        self.assertEqual(compression_37(b), FIXED_COMPRESSION_B)
        self.assertEqual(sum(a), 1)
        self.assertEqual(sum(b), 1)
        report = verify_legendre_pair(a, b)
        self.assertFalse(report.valid)
        self.assertTrue(report.fixed_compression_matches)

    def test_paf_xor_identity(self) -> None:
        a = deterministic_margin_sequence(FIXED_PLUS_COUNTS_A)
        b = deterministic_margin_sequence(FIXED_PLUS_COUNTS_B)
        for lag in range(167):
            paf_sum = periodic_autocorrelation(a, lag) + periodic_autocorrelation(
                b, lag
            )
            xor_sum = xor_distance(a, lag) + xor_distance(b, lag)
            self.assertEqual(paf_sum, 2 * N - 2 * xor_sum)

    def test_mod3_compression_energy_identity(self) -> None:
        sequence = deterministic_margin_sequence(FIXED_PLUS_COUNTS_A)
        compressed = tuple(sum(sequence[residue::3]) for residue in range(3))
        paf_sum = sum(
            periodic_autocorrelation(sequence, lag) for lag in range(0, N, 3)
        )
        self.assertEqual(sum(value * value for value in compressed), paf_sum)

    def test_mod9_compression_paf_identity(self) -> None:
        sequence = deterministic_margin_sequence(FIXED_PLUS_COUNTS_A)
        compressed = tuple(sum(sequence[residue::9]) for residue in range(9))
        for compressed_lag in range(5):
            compressed_paf = sum(
                compressed[row] * compressed[(row + compressed_lag) % 9]
                for row in range(9)
            )
            lifted_paf = sum(
                periodic_autocorrelation(sequence, lag)
                for lag in range(compressed_lag, N, 9)
            )
            self.assertEqual(compressed_paf, lifted_paf)

    def test_mod111_compression_paf_identity(self) -> None:
        sequence = deterministic_margin_sequence(FIXED_PLUS_COUNTS_A)
        compressed = tuple(sum(sequence[residue::111]) for residue in range(111))
        for compressed_lag in range(56):
            compressed_paf = sum(
                compressed[residue]
                * compressed[(residue + compressed_lag) % 111]
                for residue in range(111)
            )
            lifted_paf = sum(
                periodic_autocorrelation(sequence, lag)
                for lag in range(compressed_lag, N, 111)
            )
            self.assertEqual(compressed_paf, lifted_paf)

    def test_mod111_zero_lag_counts_monochromatic_triples(self) -> None:
        a = deterministic_margin_sequence(FIXED_PLUS_COUNTS_A)
        b = deterministic_margin_sequence(FIXED_PLUS_COUNTS_B)
        compressed = [
            tuple(sum(sequence[residue::111]) for residue in range(111))
            for sequence in (a, b)
        ]
        energy = sum(value * value for values in compressed for value in values)
        monochromatic = sum(abs(value) == 3 for values in compressed for value in values)
        self.assertEqual(energy, 222 + 8 * monochromatic)
        self.assertEqual(len(MONOCHROMATIC_TRIPLE_ROWS), 8)
        for first, second, third, same in MONOCHROMATIC_TRIPLE_ROWS:
            self.assertEqual(same, int(first == second == third))

    def test_mod3_compression_table_is_exact(self) -> None:
        self.assertEqual(generate_mod3_compression_tuples(), MOD3_COMPRESSION_TUPLES)
        self.assertEqual(len(MOD3_COMPRESSION_TUPLES), 504)
        self.assertEqual(len(set(MOD3_COMPRESSION_TUPLES)), 504)
        for values in MOD3_COMPRESSION_TUPLES:
            self.assertEqual(len(values), 6)
            self.assertEqual(sum(values[:3]), 1)
            self.assertEqual(sum(values[3:]), 1)
            self.assertEqual(sum(value * value for value in values), 446)
            self.assertTrue(all(value % 2 for value in values))

    def test_fixed_column_distance_bounds(self) -> None:
        self.assertEqual(
            fixed_compression_distance_bounds(37), ((110, 224), (110, 224))
        )
        self.assertEqual(
            fixed_compression_distance_bounds(111), ((112, 222), (112, 222))
        )
        for lag in range(1, 167):
            a_bounds, b_bounds = fixed_compression_distance_bounds(lag)
            self.assertTrue(all(value % 2 == 0 for value in a_bounds + b_bounds))
            self.assertLessEqual(a_bounds[0], a_bounds[1])
            self.assertLessEqual(b_bounds[0], b_bounds[1])

    def test_raw_column_bounds_contain_fixture_distances(self) -> None:
        a = deterministic_margin_sequence(FIXED_PLUS_COUNTS_A)
        b = deterministic_margin_sequence(FIXED_PLUS_COUNTS_B)
        for sequence, plus_counts in (
            (a, FIXED_PLUS_COUNTS_A),
            (b, FIXED_PLUS_COUNTS_B),
        ):
            for lag in range(1, 167):
                lower, upper = raw_column_distance_bounds(plus_counts, lag)
                distance = xor_distance(sequence, lag)
                self.assertLessEqual(lower, distance)
                self.assertLessEqual(distance, upper)

    def test_fixed_seed_dihedral_images_preserve_compression(self) -> None:
        a = deterministic_margin_sequence(FIXED_PLUS_COUNTS_A)
        b = deterministic_margin_sequence(FIXED_PLUS_COUNTS_B)
        for sequence, expected in (
            (a, FIXED_COMPRESSION_A),
            (b, FIXED_COMPRESSION_B),
        ):
            inverted = tuple(sequence[-index % N] for index in range(N))
            self.assertEqual(compression_37(inverted), expected)
            for row_shift in range(9):
                offset = 37 * row_shift
                shifted = tuple(sequence[(index - offset) % N] for index in range(N))
                reflected = tuple(
                    inverted[(index - offset) % N] for index in range(N)
                )
                self.assertEqual(compression_37(shifted), expected)
                self.assertEqual(compression_37(reflected), expected)

    def test_hint_canonicalization_matches_symmetry_modes(self) -> None:
        sequence = deterministic_margin_sequence(FIXED_PLUS_COUNTS_A)
        anchored = canonicalize_hint(sequence, "anchor")
        dihedral = canonicalize_hint(sequence, "dihedral")
        self.assertEqual(anchored[0], 1)
        self.assertEqual(compression_37(anchored), FIXED_COMPRESSION_A)
        self.assertEqual(compression_37(dihedral), FIXED_COMPRESSION_A)
        self.assertGreaterEqual(
            dihedral,
            tuple(dihedral[-index % N] for index in range(N)),
        )


class LegendreCpSatTests(unittest.TestCase):
    @staticmethod
    def _pinned_mod111_energy_model(monochromatic_count: int) -> cp_model.CpModel:
        """Build a fixture with a prescribed number of monochromatic triples."""

        if not 0 <= monochromatic_count <= 222:
            raise ValueError("monochromatic_count must be in [0,222]")
        model = cp_model.CpModel()
        sequences = [
            [model.new_bool_var(f"{prefix}_{index}") for index in range(N)]
            for prefix in ("a", "b")
        ]
        add_mod111_compression_equations(
            model, sequences[0], sequences[1], full=False
        )
        triple_index = 0
        for variables in sequences:
            for residue in range(111):
                values = (
                    (1, 1, 1)
                    if triple_index < monochromatic_count
                    else (1, 1, 0)
                )
                for block, value in enumerate(values):
                    model.add(variables[residue + 111 * block] == value)
                triple_index += 1
        return model

    def test_mod111_energy_encoding_is_exact_when_pinned(self) -> None:
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 1
        self.assertIn(
            solver.solve(self._pinned_mod111_energy_model(55)),
            (cp_model.FEASIBLE, cp_model.OPTIMAL),
        )
        self.assertEqual(
            solver.solve(self._pinned_mod111_energy_model(54)),
            cp_model.INFEASIBLE,
        )

    def test_shift_cycles_cover_positions_and_have_even_xor_weight(self) -> None:
        for lag in range(1, 9):
            cycles = cyclic_shift_cycles(9, lag)
            self.assertEqual(len(cycles), gcd(9, lag))
            flattened = [index for cycle in cycles for index in cycle]
            self.assertEqual(sorted(flattened), list(range(9)))
            for cycle in cycles:
                self.assertEqual(
                    tuple((index + lag) % 9 for index in cycle),
                    cycle[1:] + cycle[:1],
                )
            for word_value in range(1 << 9):
                word = tuple((word_value >> index) & 1 for index in range(9))
                differences = tuple(
                    word[index] ^ word[(index + lag) % 9] for index in range(9)
                )
                self.assertTrue(
                    all(sum(differences[index] for index in cycle) % 2 == 0
                        for cycle in cycles)
                )

    def test_cycle_parity_encoding_keeps_every_binary_word(self) -> None:
        model = cp_model.CpModel()
        variables = [model.new_bool_var(f"x_{index}") for index in range(9)]
        differences = [
            add_xor_difference(
                model,
                variables[index],
                variables[(index + 3) % 9],
                f"difference_{index}",
            )
            for index in range(9)
        ]
        total_half = model.new_int_var(0, 4, "total_half")
        add_cycle_parity_constraints(
            model, differences, 3, total_half, "test_distance"
        )

        class SolutionCounter(cp_model.CpSolverSolutionCallback):
            def __init__(self) -> None:
                super().__init__()
                self.count = 0

            def on_solution_callback(self) -> None:
                self.count += 1

        solver = cp_model.CpSolver()
        solver.parameters.enumerate_all_solutions = True
        counter = SolutionCounter()
        status = solver.solve(model, counter)
        self.assertEqual(status, cp_model.OPTIMAL)
        self.assertEqual(counter.count, 1 << 9)

    def test_lexicographic_constraint_truth_table(self) -> None:
        for left_value in range(8):
            for right_value in range(8):
                model = cp_model.CpModel()
                left = [model.new_bool_var(f"left_{index}") for index in range(3)]
                right = [model.new_bool_var(f"right_{index}") for index in range(3)]
                add_lexicographic_greater_or_equal(model, left, right, "lex")
                left_bits = tuple((left_value >> shift) & 1 for shift in (2, 1, 0))
                right_bits = tuple((right_value >> shift) & 1 for shift in (2, 1, 0))
                for variable, bit in zip(left, left_bits, strict=True):
                    model.add(variable == bit)
                for variable, bit in zip(right, right_bits, strict=True):
                    model.add(variable == bit)
                status = cp_model.CpSolver().solve(model)
                expected_feasible = left_bits >= right_bits
                self.assertEqual(
                    status in (cp_model.FEASIBLE, cp_model.OPTIMAL),
                    expected_feasible,
                )

    def test_native_xor_definition_truth_table(self) -> None:
        for left_value in (0, 1):
            for right_value in (0, 1):
                model = cp_model.CpModel()
                left = model.new_bool_var("left")
                right = model.new_bool_var("right")
                difference = add_xor_difference(model, left, right, "difference")
                model.add(left == left_value)
                model.add(right == right_value)
                solver = cp_model.CpSolver()
                status = solver.solve(model)
                self.assertIn(status, (cp_model.FEASIBLE, cp_model.OPTIMAL))
                self.assertEqual(
                    solver.value(difference), left_value ^ right_value
                )

    def test_diagnostic_model_validates(self) -> None:
        model, _, _ = build_model(symmetry="anchor", last_lag=2)
        self.assertEqual(model.validate(), "")
        stats = model.model_stats()
        self.assertIn("#kBoolXor: 1'332", stats)
        self.assertIn("#kIntProd: 90", stats)
        self.assertIn("#kTable: 1", stats)

        cycle_model, _, _ = build_model(
            symmetry="anchor", last_lag=111, cycle_parity=True
        )
        self.assertEqual(cycle_model.validate(), "")
        self.assertGreater(
            len(cycle_model.proto.variables), len(model.proto.variables)
        )

        energy_model, _, _ = build_model(
            symmetry="anchor", last_lag=2, mod111_compression="energy"
        )
        self.assertEqual(energy_model.validate(), "")
        self.assertIn("#kIntProd: 90", energy_model.model_stats())
        self.assertIn("#kTable: 223", energy_model.model_stats())

        full_model, _, _ = build_model(
            symmetry="anchor", last_lag=1, mod111_compression="full"
        )
        self.assertEqual(full_model.validate(), "")
        self.assertIn("#kIntProd: 12'300", full_model.model_stats())
        self.assertIn("#kTable: 223", full_model.model_stats())

    def test_bad_fixture_is_rejected_by_diagnostic_model(self) -> None:
        a = deterministic_margin_sequence(FIXED_PLUS_COUNTS_A)
        b = deterministic_margin_sequence(FIXED_PLUS_COUNTS_B)
        self.assertNotEqual(
            xor_distance(a, 1) + xor_distance(b, 1), N + 1
        )
        model, a_variables, b_variables = build_model(symmetry="none", last_lag=1)
        for variable, sign in zip(a_variables, a, strict=True):
            model.add(variable == int(sign == 1))
        for variable, sign in zip(b_variables, b, strict=True):
            model.add(variable == int(sign == 1))
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 1
        self.assertEqual(solver.solve(model), cp_model.INFEASIBLE)


if __name__ == "__main__":
    unittest.main()
