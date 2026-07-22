from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
import unittest

from ortools.sat.python import cp_model

from construction import goethals_seidel, verify_hadamard
from good_167 import (
    GOOD_167_ROW_SUM_PROFILES,
    good_row_sum_profiles,
    product_cycle_order,
    product_theorem_holds,
    summed_periodic_correlations,
    validate_good_quadruple,
)
from good_167_linear import c_linear_system, derive_s, recover_c_d, solve_linear_system
from search_good_167_cp_sat import (
    _add_lexicographic_greater_or_equal,
    _canonicalize_common_decimation,
    _decimate_sequence,
    _decode,
    _doubling_cycle_variable_order,
    _edge_orbit_representatives,
    _half_literal_descriptor,
    build_model,
    load_local_hint,
)
from verify_good_167 import verify_payload
from analyze_sds_167 import (
    common_multiplier_orbit_compatible,
    four_square_profiles,
    good_parameter_sets,
    gs_parameter_sets,
    williamson_product_counts,
)


class Good167Tests(unittest.TestCase):
    HERE = Path(__file__).resolve().parent

    def test_lexicographic_encoding_truth_table(self) -> None:
        for width in range(1, 5):
            for left_value in range(1 << width):
                for right_value in range(1 << width):
                    model = cp_model.CpModel()
                    left = [model.new_bool_var(f"left_{index}")
                            for index in range(width)]
                    right = [model.new_bool_var(f"right_{index}")
                             for index in range(width)]
                    _add_lexicographic_greater_or_equal(
                        model, left, right, "lex"
                    )
                    left_word = tuple(
                        (left_value >> (width - 1 - index)) & 1
                        for index in range(width)
                    )
                    right_word = tuple(
                        (right_value >> (width - 1 - index)) & 1
                        for index in range(width)
                    )
                    for variable, value in zip(left, left_word, strict=True):
                        model.add(variable == value)
                    for variable, value in zip(right, right_word, strict=True):
                        model.add(variable == value)
                    solver = cp_model.CpSolver()
                    solver.parameters.num_search_workers = 1
                    status = solver.solve(model)
                    expected = left_word >= right_word
                    self.assertEqual(
                        status in (cp_model.FEASIBLE, cp_model.OPTIMAL),
                        expected,
                    )

    def test_half_edge_orbits_reconstruct_directed_distances(self) -> None:
        for n in (7, 167):
            half = (n - 1) // 2
            half_bits = tuple((5 * index + 1) % 7 < 3 for index in range(half))
            symmetric = (False, *half_bits, *reversed(half_bits))
            skew = (
                False,
                *half_bits,
                *(not value for value in reversed(half_bits)),
            )
            for lag in range(1, half + 1):
                symmetric_representatives = _edge_orbit_representatives(
                    n, lag, skew=False
                )
                skew_representatives = _edge_orbit_representatives(
                    n, lag, skew=True
                )
                self.assertEqual(len(symmetric_representatives), half)
                self.assertEqual(len(skew_representatives), half - 1)
                directed_symmetric = sum(
                    symmetric[index] != symmetric[(index + lag) % n]
                    for index in range(n)
                )
                directed_skew = sum(
                    skew[index] != skew[(index + lag) % n]
                    for index in range(n)
                )
                self.assertEqual(
                    directed_symmetric,
                    2 * sum(
                        symmetric[index] != symmetric[(index + lag) % n]
                        for index in symmetric_representatives
                    ),
                )
                self.assertEqual(
                    directed_skew,
                    2 + 2 * sum(
                        skew[index] != skew[(index + lag) % n]
                        for index in skew_representatives
                    ),
                )
        self.assertEqual(
            set(_doubling_cycle_variable_order(167) or ()), set(range(83))
        )

    def test_pair_cache_descriptors_reconstruct_every_representative(self) -> None:
        for n in (7, 167):
            half = (n - 1) // 2
            assignments = range(1 << half) if n == 7 else range(16)
            for skew in (False, True):
                pair_counts: Counter[tuple[int, int]] = Counter()
                pair_complements: Counter[tuple[int, int, bool]] = Counter()
                singleton_count = 0
                for lag in range(1, half + 1):
                    representatives = _edge_orbit_representatives(
                        n, lag, skew=skew
                    )
                    for index in representatives:
                        left = _half_literal_descriptor(n, index, skew=skew)
                        right = _half_literal_descriptor(
                            n, index + lag, skew=skew
                        )
                        bases = tuple(base for base, _complement in (left, right))
                        if None in bases:
                            singleton_count += 1
                        else:
                            first, second = sorted(bases)
                            self.assertNotEqual(first, second)
                            pair_counts[(first, second)] += 1
                            pair_complements[
                                (first, second, left[1] != right[1])
                            ] += 1

                    for raw in assignments:
                        half_bits = tuple(
                            bool((raw >> variable) & 1)
                            for variable in range(half)
                        )
                        full = (False, *half_bits)
                        reflected = tuple(reversed(half_bits))
                        full += tuple(
                            not value if skew else value for value in reflected
                        )
                        reduced = 0
                        for index in representatives:
                            descriptors = (
                                _half_literal_descriptor(n, index, skew=skew),
                                _half_literal_descriptor(
                                    n, index + lag, skew=skew
                                ),
                            )
                            values = tuple(
                                complement
                                if base is None
                                else half_bits[base] != complement
                                for base, complement in descriptors
                            )
                            reduced += values[0] != values[1]
                        directed = sum(
                            full[index] != full[(index + lag) % n]
                            for index in range(n)
                        )
                        self.assertEqual(
                            directed,
                            2 * reduced + (2 if skew else 0),
                        )

                self.assertEqual(
                    pair_counts,
                    Counter(
                        {
                            (first, second): 2
                            for first in range(half)
                            for second in range(first + 1, half)
                        }
                    ),
                )
                self.assertEqual(singleton_count, 0 if skew else half)
                if skew:
                    self.assertTrue(
                        all(
                            pair_complements[(pair[0], pair[1], False)] == 1
                            and pair_complements[(pair[0], pair[1], True)] == 1
                            for pair in pair_counts
                        )
                    )

    def test_pair_cached_order_167_model_counts(self) -> None:
        plain, _ = build_model(
            167,
            GOOD_167_ROW_SUM_PROFILES[0],
            common_decimation_necklace=False,
        )
        self.assertEqual(len(plain.proto.variables), 13_945)
        self.assertEqual(len(plain.proto.constraints), 13_782)

        necklace, _ = build_model(167, GOOD_167_ROW_SUM_PROFILES[0])
        self.assertEqual(len(necklace.proto.variables), 20_669)
        self.assertEqual(len(necklace.proto.constraints), 54_126)

    def test_arithmetic_profiles(self) -> None:
        self.assertEqual(
            GOOD_167_ROW_SUM_PROFILES,
            ((-21, -1, 15), (-9, 15, 19)),
        )
        self.assertEqual(product_cycle_order(), 83)
        self.assertEqual(good_row_sum_profiles(5), ((-3, -3, 1),))
        self.assertEqual(good_parameter_sets(5), (((2, 2, 1, 1), 1),))

    def test_sds_parameter_audit(self) -> None:
        profiles = four_square_profiles()
        parameters = gs_parameter_sets()
        self.assertEqual(len(profiles), 10)
        self.assertEqual(len(parameters), 10)
        self.assertEqual(
            good_parameter_sets(),
            (((83, 83, 76, 73), 148), ((83, 79, 76, 74), 145)),
        )
        self.assertFalse(
            any(common_multiplier_orbit_compatible(sizes, 83) for sizes, _ in parameters)
        )
        for profile in profiles:
            total, triples = williamson_product_counts(profile)
            self.assertEqual(total, 83 + 2 * triples)
            self.assertGreaterEqual(triples, 0)
            self.assertLessEqual(triples, 83)

    def test_small_exact_model_finds_good_order_seven(self) -> None:
        profiles = good_row_sum_profiles(7)
        self.assertEqual(profiles, ((-5, -1, -1), (3, 3, 3)))
        model, halves = build_model(7, (3, 3, 3))
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 5
        solver.parameters.num_search_workers = 1
        status = solver.solve(model)
        self.assertIn(status, (cp_model.FEASIBLE, cp_model.OPTIMAL))
        candidate = validate_good_quadruple(_decode(solver, halves), 7)
        matrix = goethals_seidel(candidate)
        verify_hadamard(matrix)
        self.assertTrue(
            all(
                matrix[row][column] + matrix[column][row]
                == (2 if row == column else 0)
                for row in range(28)
                for column in range(28)
            )
        )

        hinted_model, hinted_halves = build_model(
            7,
            (3, 3, 3),
            hint_sequences=candidate,
            max_symmetric_hint_distance=0,
        )
        self.assertEqual(len(hinted_model.proto.solution_hint.vars), 12)
        hinted_solver = cp_model.CpSolver()
        hinted_solver.parameters.max_time_in_seconds = 5
        hinted_solver.parameters.num_search_workers = 1
        hinted_solver.parameters.repair_hint = True
        self.assertIn(
            hinted_solver.solve(hinted_model),
            (cp_model.FEASIBLE, cp_model.OPTIMAL),
        )
        validate_good_quadruple(_decode(hinted_solver, hinted_halves), 7)

        full_model, _ = build_model(
            7,
            (3, 3, 3),
            half_edges=False,
            common_decimation_necklace=False,
        )
        full_solver = cp_model.CpSolver()
        full_solver.parameters.max_time_in_seconds = 5
        full_solver.parameters.num_search_workers = 1
        self.assertIn(
            full_solver.solve(full_model),
            (cp_model.FEASIBLE, cp_model.OPTIMAL),
        )

        a, b, c, d = candidate
        self.assertEqual(tuple(x * y for x, y in zip(derive_s(a, b), c)), d)
        system, _ = c_linear_system(a, b)
        solution = solve_linear_system(system)
        self.assertIsNotNone(solution)
        assert solution is not None
        self.assertFalse(solution.inconsistent)
        recovered = recover_c_d(a, b, sum(c), sum(d))
        self.assertIn(candidate, recovered.candidates)

        # The order-167 verifier is intentionally strict: a valid small
        # regression fixture must not be misreported as H(668).
        with self.assertRaisesRegex(ValueError, "order must be exactly 167"):
            verify_payload(
                {
                    "kind": "circulant_good_matrices",
                    "order": 7,
                    "hadamard_order": 28,
                    "row_sums": [sum(b), sum(c), sum(d)],
                    "sequences": [list(sequence) for sequence in candidate],
                }
            )

    def test_local_checkpoints_become_exact_structural_hints(self) -> None:
        expected = (
            (
                27,
                162,
                (
                    0x438A568C81FC74964C57A,
                    0x67D603A6AE629397CAF9F,
                    0x3A3BB6F6E04179CC0BB06,
                    0x00CB0CD42EE6A791E0A9B,
                ),
            ),
            (
                2,
                4,
                (
                    0x0EFA7544A30C6D6B43A5E,
                    0x6BB3910B7FADD9639A218,
                    0x347A04FC745A19781C81B,
                    0x680049B84E6B82BBA33D1,
                ),
            ),
        )

        for profile, row_sums in enumerate(GOOD_167_ROW_SUM_PROFILES):
            path = (
                self.HERE
                / "output"
                / (
                    "good_167_local_steepest_profile0.json"
                    if profile == 0
                    else "good_167_local_triangle_profile1.json"
                )
            )
            source = json.loads(path.read_text())
            sequences, diagnostics = load_local_hint(
                path,
                row_sums,
                common_decimation_necklace=True,
            )
            expected_shift, expected_multiplier, expected_masks = expected[profile]
            masks = tuple(
                sum(
                    1 << (index - 1)
                    for index in range(1, 84)
                    if sequence[index] == -1
                )
                for sequence in sequences
            )
            self.assertEqual(masks, expected_masks)
            self.assertEqual(diagnostics["decimation_shift"], expected_shift)
            self.assertEqual(diagnostics["decimation_multiplier"], expected_multiplier)
            self.assertEqual(tuple(sum(sequence) for sequence in sequences[1:]), row_sums)
            self.assertEqual(sequences[0][1], 1)
            self.assertTrue(product_theorem_holds(*sequences))

            transformed_quarters = tuple(
                value // 4
                for value in summed_periodic_correlations(sequences)[1:84]
            )
            self.assertEqual(
                sorted(transformed_quarters), sorted(source["quarter_residuals"])
            )
            self.assertEqual(
                sum(value * value for value in transformed_quarters),
                diagnostics["energy"],
            )

            model, halves = build_model(
                167,
                row_sums,
                hint_sequences=sequences,
            )
            actual_hint = dict(
                zip(
                    model.proto.solution_hint.vars,
                    model.proto.solution_hint.values,
                    strict=True,
                )
            )
            expected_hint = {
                bit.index: int(sequence[index] == -1)
                for sequence, bits in zip(sequences, halves, strict=True)
                for index, bit in enumerate(bits, start=1)
            }
            self.assertEqual(len(actual_hint), 332)
            self.assertEqual(actual_hint, expected_hint)
            self.assertEqual(len(model.proto.variables), 20_669)
            self.assertEqual(len(model.proto.constraints), 54_126)

            for multiplier in (1, 2, 4, 83, 166):
                decimated = tuple(
                    _decimate_sequence(sequence, multiplier)
                    for sequence in sequences
                )
                recanonicalized, _shift, _multiplier = (
                    _canonicalize_common_decimation(decimated, row_sums)
                )
                self.assertEqual(recanonicalized, sequences)

        profile_zero = json.loads(
            (
                self.HERE
                / "output"
                / "good_167_local_steepest_profile0.json"
            ).read_text()
        )
        with self.assertRaisesRegex(ValueError, "does not match"):
            from search_good_167_cp_sat import _local_checkpoint_hint

            _local_checkpoint_hint(
                profile_zero,
                GOOD_167_ROW_SUM_PROFILES[1],
                common_decimation_necklace=True,
            )

        with self.assertRaisesRegex(ValueError, "requires hint sequences"):
            build_model(
                167,
                GOOD_167_ROW_SUM_PROFILES[0],
                max_symmetric_hint_distance=2,
            )


if __name__ == "__main__":
    unittest.main()
