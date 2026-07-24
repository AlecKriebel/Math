#!/usr/bin/env python3
"""Focused tests for the dedicated order-three LP(333) quotient model."""

from __future__ import annotations

from itertools import product
from pathlib import Path
import tempfile
import unittest

from ortools.sat.python import cp_model

from search_lp333_order3_cp_sat import (
    ROW_SUM_CATALOG_SIZE,
    _add_c2_coset_lex_leaders,
    _add_c6_lex_leader,
    _add_lex_less_or_equal,
    build_model,
    row_sum_catalog,
)
from verify_lp333_order3_difference_family import WITNESS_CLASS_EXPONENTS
from verify_lp333_order3_quotient import (
    CANONICAL_ZERO_EXPONENTS,
    C2_AFFINE_MULTIPLIER,
    FALSE_CLASS_FIXED_MULTIPLIER,
    QUOTIENT_EQUATIONS,
    SIGN_PAIRS,
    TARGET_XOR_COUNT,
    expand_sign_sequences,
    multiplier_paf_mismatch_count,
    quotient_replay,
    reflect_b_with_opposite_classes,
    rotate_class_pairs,
    validate_quotient_exponents,
    verify_and_save_candidate,
    verify_c2_action,
    verify_c6_action,
    verify_transition_matrices,
)


def witness_quotient() -> tuple[tuple[int, ...], ...]:
    """Transpose the pinned twelve class words into a 9 by 13 table."""

    return tuple(
        (CANONICAL_ZERO_EXPONENTS[row],)
        + tuple(word[row] for word in WITNESS_CLASS_EXPONENTS)
        for row in range(9)
    )


class SolutionCollector(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables: list[cp_model.IntVar]) -> None:
        super().__init__()
        self.variables = variables
        self.solutions: set[tuple[int, ...]] = set()

    def on_solution_callback(self) -> None:
        self.solutions.add(
            tuple(self.value(variable) for variable in self.variables)
        )


class OrderThreeQuotientTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.baseline = build_model(c6_symmetry=False, c2_symmetry=False)
        cls.with_c6 = build_model(c6_symmetry=True, c2_symmetry=False)
        cls.with_full_group = build_model(c6_symmetry=True, c2_symmetry=True)

    def test_transition_equation_and_c6_audits(self) -> None:
        self.assertEqual(
            verify_transition_matrices(),
            {"classes": 12, "class_size": 3, "equations": 58},
        )
        self.assertEqual(len(QUOTIENT_EQUATIONS), 58)
        self.assertEqual(
            verify_c6_action(),
            {"decimation": 226, "action_order": 6, "class_step": 2},
        )
        self.assertEqual(
            verify_c2_action(),
            {
                "multiplier": 323,
                "translation": 111,
                "class_step": 6,
                "false_multiplier": 260,
                "false_multiplier_mismatches": 276,
            },
        )

    def test_row_sum_catalog_is_pinned_and_unique(self) -> None:
        catalog = row_sum_catalog()
        self.assertEqual(len(catalog), ROW_SUM_CATALOG_SIZE)
        self.assertEqual(len(set(catalog)), ROW_SUM_CATALOG_SIZE)
        self.assertTrue(all(len(row) == 18 for row in catalog))

    def test_exact_baseline_model_counts(self) -> None:
        self.assertEqual(
            self.baseline.exact_counts(),
            {
                "primary_sign_bits": 216,
                "cached_xor_variables": 11_556,
                "row_sum_variables": 18,
                "c6_variables": 0,
                "c2_variables": 0,
                "compression_constraints": 24,
                "quotient_lag_constraints": 58,
                "row_sum_constraints": 19,
                "c6_constraints": 0,
                "c2_constraints": 0,
                "total_variables": 11_790,
                "total_constraints": 11_657,
            },
        )
        self.assertEqual(self.baseline.model.validate(), "")

    def test_exact_c6_model_counts(self) -> None:
        self.assertEqual(
            self.with_c6.exact_counts(),
            {
                "primary_sign_bits": 216,
                "cached_xor_variables": 11_556,
                "row_sum_variables": 18,
                "c6_variables": 31,
                "c2_variables": 0,
                "compression_constraints": 24,
                "quotient_lag_constraints": 58,
                "row_sum_constraints": 19,
                "c6_constraints": 106,
                "c2_constraints": 0,
                "total_variables": 11_821,
                "total_constraints": 11_763,
            },
        )
        self.assertEqual(self.with_c6.model.validate(), "")

    def test_exact_full_group_model_counts(self) -> None:
        self.assertEqual(
            self.with_full_group.exact_counts(),
            {
                "primary_sign_bits": 216,
                "cached_xor_variables": 11_556,
                "row_sum_variables": 18,
                "c6_variables": 31,
                "c2_variables": 36,
                "compression_constraints": 24,
                "quotient_lag_constraints": 58,
                "row_sum_constraints": 19,
                "c6_constraints": 106,
                "c2_constraints": 126,
                "total_variables": 11_857,
                "total_constraints": 11_889,
            },
        )
        self.assertEqual(self.with_full_group.model.validate(), "")

    def test_lex_encoding_is_exact_on_all_ternary_necklaces(self) -> None:
        model = cp_model.CpModel()
        variables = [model.new_int_var(0, 2, f"x_{index}") for index in range(6)]
        for shift in range(1, 6):
            _add_lex_less_or_equal(
                model,
                variables,
                variables[shift:] + variables[:shift],
                f"rotation_{shift}",
            )
        collector = SolutionCollector(variables)
        solver = cp_model.CpSolver()
        solver.parameters.enumerate_all_solutions = True
        solver.parameters.num_search_workers = 1
        status = solver.solve(model, collector)
        self.assertEqual(status, cp_model.OPTIMAL)

        expected = {
            word
            for word in product(range(3), repeat=6)
            if all(
                word <= word[shift:] + word[:shift]
                for shift in range(1, 6)
            )
        }
        self.assertEqual(len(expected), 130)
        self.assertEqual(collector.solutions, expected)

    def test_pure_axis_witness_replays_but_is_rejected(self) -> None:
        quotient = validate_quotient_exponents(witness_quotient())
        replay = quotient_replay(quotient)
        self.assertEqual(len(replay), 58)
        zero_column = tuple(
            distance
            for equation, (_, distance) in zip(
                QUOTIENT_EQUATIONS, replay, strict=True
            )
            if equation.column_lag == 0
        )
        self.assertEqual(zero_column, (TARGET_XOR_COUNT,) * 4)
        nonzero = tuple(
            distance
            for equation, (_, distance) in zip(
                QUOTIENT_EQUATIONS, replay, strict=True
            )
            if equation.column_lag != 0
        )
        self.assertEqual(len(nonzero), 54)
        self.assertEqual(
            sum(distance != TARGET_XOR_COUNT for distance in nonzero), 51
        )

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "must_not_exist.json"
            with self.assertRaisesRegex(
                ValueError, "fails an exact lag equation"
            ):
                verify_and_save_candidate(output, quotient)
            self.assertFalse(output.exists())

    def test_corrected_c2_and_false_260_counterexample(self) -> None:
        quotient = witness_quotient()
        reflected = reflect_b_with_opposite_classes(quotient)
        self.assertEqual(
            reflect_b_with_opposite_classes(reflected), quotient
        )
        for shift in range(6):
            self.assertEqual(
                reflect_b_with_opposite_classes(
                    rotate_class_pairs(quotient, shift)
                ),
                rotate_class_pairs(reflected, shift),
            )
        _, b = expand_sign_sequences(quotient)
        self.assertEqual(
            multiplier_paf_mismatch_count(b, C2_AFFINE_MULTIPLIER), 0
        )
        # This pins the concrete failure that exposed the class-fixed error.
        self.assertEqual(
            multiplier_paf_mismatch_count(
                b, FALSE_CLASS_FIXED_MULTIPLIER
            ),
            264,
        )

    def test_full_group_lex_leader_accepts_one_orbit_image(self) -> None:
        quotient = witness_quotient()
        images = {
            rotate_class_pairs(quotient, shift) for shift in range(6)
        } | {
            rotate_class_pairs(
                reflect_b_with_opposite_classes(quotient), shift
            )
            for shift in range(6)
        }
        self.assertEqual(len(images), 12)

        accepted: list[tuple[tuple[int, ...], ...]] = []
        for image in images:
            model = cp_model.CpModel()
            a_rows: list[tuple[int | cp_model.IntVar, ...]] = []
            b_rows: list[tuple[int | cp_model.IntVar, ...]] = []
            for row in range(9):
                a_row: list[int | cp_model.IntVar] = [
                    int(SIGN_PAIRS[image[row][0]][0] == 1)
                ]
                b_row: list[int | cp_model.IntVar] = [
                    int(SIGN_PAIRS[image[row][0]][1] == 1)
                ]
                for class_index in range(12):
                    a_value, b_value = SIGN_PAIRS[
                        image[row][class_index + 1]
                    ]
                    a = model.new_bool_var(f"a_{row}_{class_index}")
                    b = model.new_bool_var(f"b_{row}_{class_index}")
                    model.add(a == int(a_value == 1))
                    model.add(b == int(b_value == 1))
                    a_row.append(a)
                    b_row.append(b)
                a_rows.append(tuple(a_row))
                b_rows.append(tuple(b_row))
            _, _, codes = _add_c6_lex_leader(model, a_rows, b_rows)
            _add_c2_coset_lex_leaders(model, a_rows, b_rows, codes)
            solver = cp_model.CpSolver()
            status = solver.solve(model)
            if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
                accepted.append(image)
        self.assertEqual(len(accepted), 1)

    def test_row_sum_shard_validation(self) -> None:
        fixed = build_model(
            row_sum_index=695, c6_symmetry=False, c2_symmetry=False
        )
        self.assertEqual(fixed.exact_counts(), self.baseline.exact_counts())
        with self.assertRaisesRegex(ValueError, "row-sum index"):
            build_model(row_sum_index=ROW_SUM_CATALOG_SIZE)


if __name__ == "__main__":
    unittest.main()
