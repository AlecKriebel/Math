import unittest

from ortools.sat.python import cp_model

from search_variable_q_cp_sat import (
    add_lexicographic_greater_or_equal,
    build_model,
    canonical_alternation_literal_image,
)
from test_variable_q_base import sequence_with_margins
from variable_q_base import (
    ALTERNATION_FIXED_SHARDS,
    LONG,
    MARGIN_SHARDS,
    SHORT,
    canonical_alternation_transform,
)


def make_variables(model: cp_model.CpModel) -> tuple[list[cp_model.IntVar], ...]:
    return tuple(
        [model.new_bool_var(f"{label}_{index}") for index in range(length)]
        for label, length in zip("abcd", (LONG, LONG, SHORT, SHORT), strict=True)
    )


def pin_sequences(
    model: cp_model.CpModel,
    variables: tuple[list[cp_model.IntVar], ...],
    sequences: tuple[tuple[int, ...], ...],
) -> None:
    for bits, sequence in zip(variables, sequences, strict=True):
        for bit, sign in zip(bits, sequence, strict=True):
            model.add(bit == int(sign == 1))


class VariableQCpSatTests(unittest.TestCase):
    def test_global_alternation_literal_image_and_fixed_shard_lex(self) -> None:
        lengths = (LONG, LONG, SHORT, SHORT)
        for shard in ALTERNATION_FIXED_SHARDS:
            ordinary, alternating = MARGIN_SHARDS[shard]
            sequences = tuple(
                sequence_with_margins(length, row_sum, alt_sum)
                for length, row_sum, alt_sum in zip(
                    lengths, ordinary, alternating, strict=True
                )
            )
            transformed = canonical_alternation_transform(*sequences)
            chosen = max(sequences, transformed)
            rejected = min(sequences, transformed)

            model = cp_model.CpModel()
            variables = make_variables(model)
            image = canonical_alternation_literal_image(
                variables, ordinary, alternating
            )
            add_lexicographic_greater_or_equal(
                model,
                [literal for sequence in variables for literal in sequence],
                [literal for sequence in image for literal in sequence],
                "test_global_alternation",
            )
            pin_sequences(model, variables, chosen)
            solver = cp_model.CpSolver()
            solver.parameters.num_search_workers = 1
            self.assertEqual(solver.solve(model), cp_model.OPTIMAL)

            if chosen != rejected:
                rejected_model = cp_model.CpModel()
                rejected_variables = make_variables(rejected_model)
                rejected_image = canonical_alternation_literal_image(
                    rejected_variables, ordinary, alternating
                )
                add_lexicographic_greater_or_equal(
                    rejected_model,
                    [
                        literal
                        for sequence in rejected_variables
                        for literal in sequence
                    ],
                    [
                        literal
                        for sequence in rejected_image
                        for literal in sequence
                    ],
                    "test_global_alternation",
                )
                pin_sequences(rejected_model, rejected_variables, rejected)
                rejected_solver = cp_model.CpSolver()
                rejected_solver.parameters.num_search_workers = 1
                self.assertEqual(
                    rejected_solver.solve(rejected_model), cp_model.INFEASIBLE
                )

    def test_full_models_with_new_invariants_validate(self) -> None:
        for parity_basis in ("quad", "endpoint", "both"):
            ordinary_model, _ = build_model(
                0,
                compression_7=True,
                compression_7_alternating=True,
                parity_basis=parity_basis,
            )
            self.assertEqual(ordinary_model.validate(), "")
        fixed_model, _ = build_model(ALTERNATION_FIXED_SHARDS[0], compression_7=True)
        self.assertEqual(fixed_model.validate(), "")
        self.assertTrue(
            any(
                variable.name.startswith("a_z8_")
                for variable in fixed_model.proto.variables
            )
        )
        self.assertTrue(
            any(
                variable.name.startswith("global_alternation")
                for variable in fixed_model.proto.variables
            )
        )

    def test_hint_hamming_ball_is_exact(self) -> None:
        ordinary, alternating = MARGIN_SHARDS[0]
        hint = tuple(
            sequence_with_margins(length, row_sum, alt_sum)
            for length, row_sum, alt_sum in zip(
                (LONG, LONG, SHORT, SHORT), ordinary, alternating, strict=True
            )
        )
        model, _ = build_model(
            0,
            hint=hint,
            max_hint_distance=0,
            symmetry_breaking=False,
        )
        self.assertEqual(model.validate(), "")
        self.assertTrue(
            any(
                constraint.name == "maximum_hint_hamming_distance"
                for constraint in model.proto.constraints
            )
        )
        self.assertFalse(
            any(
                "reverse" in variable.name or "global_alternation" in variable.name
                for variable in model.proto.variables
            )
        )
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 1
        self.assertEqual(solver.solve(model), cp_model.INFEASIBLE)
        with self.assertRaises(ValueError):
            build_model(0, max_hint_distance=4)


if __name__ == "__main__":
    unittest.main()
