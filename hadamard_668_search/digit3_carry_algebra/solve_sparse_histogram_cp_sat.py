#!/usr/bin/env python3
"""Sparse original-trit CP-SAT model for phase prefixes and exactness.

Each phase exponent depends on at most two of the 54 original placement
trits, so it is represented by a table of at most nine rows.  Per displayed
correlation row, the signed exponent histogram (n0,n1,n2) is constrained
through

    A = n0 - n2 - target,
    Q = (n0 + n1 - 2*n2 - target)/3.

The exact equation is the cardinality condition

    n0 - target = n1 = n2,

equivalently A=Q=0.  Prefix modes use the congruence lattice in the
companion carry audit.  All witnesses are independently replayed.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import itertools
import json
from pathlib import Path
import sys
import time

from ortools.sat.python import cp_model


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
SECOND_DIGIT = SEARCH_ROOT / "phase_second_digit"
HIGHER_DIGITS = SECOND_DIGIT / "higher_digits"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(SECOND_DIGIT))
sys.path.insert(0, str(HIGHER_DIGITS))
sys.path.insert(0, str(SEARCH_ROOT))

import audit_digit3_carry as carry  # noqa: E402
import solve_carry_cp_sat as compact  # noqa: E402
import solve_lambda_prefix_sat as prefix  # noqa: E402
import verify_e1_origin_exact_dp as e1_exact  # noqa: E402
import verify_full_second_digit_witness as full_witness  # noqa: E402
import verify_phase_second_digit as second  # noqa: E402
from verify_lp333_order3_phase_transfer import (  # noqa: E402
    catalog_phase_sum_intersection,
    phase_sums_from_masks,
)


def add_orientation_one_hot(
    model: cp_model.CpModel,
    orientation: cp_model.IntVar,
    name: str,
):
    indicators = tuple(
        model.new_bool_var(f"{name}_is_{value}") for value in range(3)
    )
    model.add_allowed_assignments(
        (orientation, *indicators),
        (
            (0, 1, 0, 0),
            (1, 0, 1, 0),
            (2, 0, 0, 1),
        ),
    )
    return indicators


def flattened_phase_sums(profiles, point) -> tuple[int, ...]:
    masks = second.masks_from_trits(profiles, point)
    return tuple(
        coordinate
        for channel in phase_sums_from_masks(*masks)
        for value in channel
        for coordinate in value
    )


def phase_sum_affine_data(profiles):
    """Derive the separable twelve-coordinate phase-sum table exactly."""

    variable_count = len(second.active_trit_coordinates(profiles))
    zero = (0,) * variable_count
    baseline = flattened_phase_sums(profiles, zero)
    effects = []
    for index in range(variable_count):
        values = [baseline]
        for value in (1, 2):
            point = list(zero)
            point[index] = value
            values.append(flattened_phase_sums(profiles, tuple(point)))
        effects.append(tuple(values))
    return baseline, tuple(effects)


def evaluate_phase_sum_affine(baseline, effects, point):
    if len(effects) != len(point):
        raise ValueError("the phase-sum affine point has the wrong size")
    return tuple(
        int(baseline[coordinate])
        + sum(
            int(effects[index][int(value)][coordinate])
            - int(baseline[coordinate])
            for index, value in enumerate(point)
        )
        for coordinate in range(12)
    )


def add_row_margin_membership(
    model: cp_model.CpModel,
    placement,
    profiles,
    identifiers_a,
    identifiers_b,
    target_index: int | None = None,
) -> dict[str, object]:
    """Require the exact six phase sums to occur in the margin catalog."""

    coordinates = second.active_trit_coordinates(profiles)
    if len(coordinates) != len(placement):
        raise AssertionError("the active placement coordinates changed")

    baseline, effects = phase_sum_affine_data(profiles)
    indicators = tuple(
        add_orientation_one_hot(
            model, variable, f"margin_placement_{index}"
        )
        for index, variable in enumerate(placement)
    )

    sum_variables = []
    for sum_index in range(12):
        phase_sum = model.new_int_var(
            -37,
            37,
            f"phase_sum_{sum_index}",
        )
        expression = int(baseline[sum_index])
        for index in range(len(coordinates)):
            expression += sum(
                (
                    int(effects[index][value][sum_index])
                    - int(baseline[sum_index])
                )
                * indicators[index][value]
                for value in range(3)
            )
        model.add(phase_sum == expression)
        sum_variables.append(phase_sum)

    catalog = catalog_phase_sum_intersection(
        identifiers_a, identifiers_b
    )
    allowed = tuple(
        tuple(
            coordinate
            for channel in sums
            for value in channel
            for coordinate in value
        )
        for sums, _ in catalog["phase_sum_corpus"]
    )
    if len(allowed) != int(catalog["compatible_catalog_rows"]):
        raise AssertionError("the compatible phase-sum corpus changed")
    if target_index is not None:
        if not 0 <= target_index < len(allowed):
            raise ValueError("the row-margin target index is out of range")
        selected = (allowed[target_index],)
    else:
        selected = allowed
    model.add_allowed_assignments(tuple(sum_variables), selected)
    return {
        "row_margin_membership": True,
        "row_margin_phase_sum_variables": len(sum_variables),
        "row_margin_orientation_indicators": 3 * len(indicators),
        "row_margin_compatible_targets": len(allowed),
        "row_margin_selected_target_index": target_index,
        "row_margin_selected_targets": len(selected),
        "row_margin_accepted_assignments": int(
            catalog["accepted_assignments"]
        ),
        "row_margin_phase_sum_corpus_sha256": catalog[
            "phase_sum_corpus_sha256"
        ],
    }


def add_exact_e1_origin_histogram(
    model: cp_model.CpModel,
    placement,
    form_variables,
    rows,
    profiles,
) -> dict[str, int]:
    """Expose the 30 admissible local orientation-count pairs."""

    _, grouped = rows[7]
    coordinates = second.active_trit_coordinates(profiles)
    blocks = defaultdict(list)
    for form, multiplicity in grouped:
        touched = {
            coordinates[variable][:2] for variable, _ in form[1]
        }
        if len(touched) != 1:
            raise AssertionError("the delayed row crossed local blocks")
        blocks[next(iter(touched))].append((form, multiplicity // 3))
    singleton_indicators = []
    triple_indicators = []
    for block_index, block in enumerate(
        block for _, block in sorted(blocks.items())
    ):
        if len(block) == 1:
            form, epsilon = block[0]
            if epsilon != -1:
                raise AssertionError("a singleton orientation changed sign")
            orientation = form_variables[form][0]
            singleton_indicators.append(
                add_orientation_one_hot(
                    model, orientation, f"e1_singleton_{block_index}"
                )
            )
            continue
        if len(block) != 3 or any(epsilon != 1 for _, epsilon in block):
            raise AssertionError("a three-cycle catalog changed")
        variables = tuple(
            sorted(
                {
                    variable
                    for (_, coefficients), _ in block
                    for variable, _ in coefficients
                }
            )
        )
        if len(variables) != 3:
            raise AssertionError("a three-cycle lost a local trit")
        orientation = model.new_int_var(
            0, 2, f"e1_three_cycle_{block_index}"
        )
        allowed = []
        for values in itertools.product(range(3), repeat=3):
            assignment = dict(zip(variables, values))
            exact = [0, 0]
            for (constant, coefficients), _ in block:
                exponent = (
                    constant
                    + sum(
                        coefficient * assignment[variable]
                        for variable, coefficient in coefficients
                    )
                ) % 3
                exact[0] += e1_exact.ROOTS[exponent][0]
                exact[1] += e1_exact.ROOTS[exponent][1]
            try:
                value = e1_exact.LAMBDA_ROOTS.index(tuple(exact))
            except ValueError as error:
                raise AssertionError(
                    "a three-cycle left lambda times a root"
                ) from error
            allowed.append((*values, value))
        model.add_allowed_assignments(
            tuple(placement[variable] for variable in variables)
            + (orientation,),
            allowed,
        )
        triple_indicators.append(
            add_orientation_one_hot(
                model, orientation, f"e1_three_cycle_{block_index}"
            )
        )

    if len(singleton_indicators) != 12 or len(triple_indicators) != 10:
        raise AssertionError("the delayed block census changed")
    singleton_counts = tuple(
        model.new_int_var(0, 12, f"e1_singleton_count_{value}")
        for value in range(3)
    )
    triple_counts = tuple(
        model.new_int_var(0, 10, f"e1_three_cycle_count_{value}")
        for value in range(3)
    )
    for value in range(3):
        model.add(
            singleton_counts[value]
            == sum(indicators[value] for indicators in singleton_indicators)
        )
        model.add(
            triple_counts[value]
            == sum(indicators[value] for indicators in triple_indicators)
        )
    _, admissible = e1_exact.composition_count()
    model.add_allowed_assignments(
        (*singleton_counts, *triple_counts),
        tuple(
            tuple(record["singleton_counts"])
            + tuple(record["three_cycle_counts"])
            for record in admissible
        ),
    )
    return {
        "e1_exact_orientation_blocks": 22,
        "e1_exact_new_orientation_variables": 10,
        "e1_exact_orientation_indicators": 66,
        "e1_exact_count_variables": 6,
        "e1_exact_admissible_count_pairs": len(admissible),
    }


def build_model(
    candidate_index: int,
    mode: str,
    row_margin_aware: bool = False,
    row_margin_target_index: int | None = None,
):
    candidate = second.CANDIDATES[candidate_index]
    profiles = second.profiles_from_ids(candidate[3], candidate[4])
    rows = prefix.grouped_term_rows(profiles)
    model = cp_model.CpModel()
    placement = tuple(
        model.new_int_var(0, 2, f"placement_{index}")
        for index in range(54)
    )
    all_forms = tuple(
        sorted({form for _, grouped in rows for form, _ in grouped})
    )
    form_variables = {}
    table_rows = 0
    support_histogram: dict[int, int] = {}
    for form_index, (constant, coefficients) in enumerate(all_forms):
        exponent = model.new_int_var(0, 2, f"L_{form_index}")
        indicator_two = model.new_bool_var(f"Z_{form_index}")
        sources = tuple(
            placement[int(variable)] for variable, _ in coefficients
        )
        allowed = []
        for values in itertools.product(range(3), repeat=len(sources)):
            value = (
                int(constant)
                + sum(
                    int(coefficient) * source
                    for (_, coefficient), source in zip(coefficients, values)
                )
            ) % 3
            allowed.append((*values, value, int(value == 2)))
        model.add_allowed_assignments(
            (*sources, exponent, indicator_two), allowed
        )
        table_rows += len(allowed)
        support_histogram[len(sources)] = (
            support_histogram.get(len(sources), 0) + 1
        )
        form_variables[(constant, coefficients)] = (
            exponent,
            indicator_two,
        )

    # State the rank-18 first layer explicitly.  It is logically implied by
    # every mode below, but exposing the sparse linear equations gives the
    # solver substantially earlier propagation than recovering them through
    # hundreds of phase tables.
    first_equations = second.first_digit_equations(profiles)
    for row_index, equation in enumerate(first_equations):
        compact.add_congruence(
            model,
            int(equation.affine[0]),
            [
                (int(coefficient), placement[index])
                for index, coefficient in enumerate(equation.affine[1:])
                if int(coefficient)
            ],
            3,
            f"first_{row_index}",
        )

    # E1(origin) is delayed: all its multiplicities are divisible by 3.
    # Dividing its A equation by 3 exposes one further independent linear
    # condition at digit 3, reducing the first-layer dimension 36 -> 35.
    delayed_target, delayed_grouped = rows[7]
    delayed_constant = (
        sum(multiplicity for _, multiplicity in delayed_grouped)
        - int(delayed_target)
    ) // 3
    delayed_coefficients = [0] * 54
    for (constant, coefficients), multiplicity in delayed_grouped:
        if multiplicity % 3:
            raise AssertionError("the delayed row lost divisibility by 3")
        epsilon = multiplicity // 3
        delayed_constant -= epsilon * int(constant)
        for variable, coefficient in coefficients:
            delayed_coefficients[int(variable)] -= (
                epsilon * int(coefficient)
            )
    if mode != "digit2":
        compact.add_congruence(
            model,
            delayed_constant,
            [
                (coefficient, placement[index])
                for index, coefficient in enumerate(delayed_coefficients)
                if coefficient
            ],
            3,
            "delayed_e1_origin_digit3",
        )

    row_margin_statistics: dict[str, object] = {}
    if row_margin_aware:
        row_margin_statistics = add_row_margin_membership(
            model,
            placement,
            profiles,
            candidate[3],
            candidate[4],
            row_margin_target_index,
        )
    elif row_margin_target_index is not None:
        raise ValueError(
            "a row-margin target requires row-margin membership"
        )

    exact_e1_statistics = {}
    if mode in ("digit3_exact_row7", "exact"):
        exact_e1_statistics = add_exact_e1_origin_histogram(
            model, placement, form_variables, rows, profiles
        )

    for row_index in range(1, 20):
        target, grouped = rows[row_index]
        constant_at_zero = sum(
            multiplicity for _, multiplicity in grouped
        ) - int(target)
        if constant_at_zero % 3:
            raise AssertionError("the shell-zero constant changed")
        a_terms = [
            (-multiplicity, form_variables[form][0])
            for form, multiplicity in grouped
        ]
        q_terms = [
            (-multiplicity, form_variables[form][1])
            for form, multiplicity in grouped
        ]
        if mode == "digit2":
            if row_index != 7:
                compact.add_congruence(
                    model,
                    constant_at_zero // 3,
                    q_terms,
                    3,
                    f"row_{row_index}_Q",
                )
        elif mode == "digit3" or (
            mode == "digit3_exact_row7" and row_index != 7
        ):
            compact.add_congruence(
                model,
                constant_at_zero,
                a_terms,
                9,
                f"row_{row_index}_A",
            )
            compact.add_congruence(
                model,
                constant_at_zero // 3,
                q_terms,
                3,
                f"row_{row_index}_Q",
            )
        elif mode == "digit3_exact_row7" and row_index == 7:
            model.add(
                constant_at_zero
                + sum(
                    coefficient * variable
                    for coefficient, variable in a_terms
                )
                == 0
            )
            model.add(
                constant_at_zero // 3
                + sum(
                    coefficient * variable
                    for coefficient, variable in q_terms
                )
                == 0
            )
        elif mode == "digit4":
            compact.add_congruence(
                model,
                constant_at_zero,
                a_terms,
                9,
                f"row_{row_index}_A",
            )
            compact.add_congruence(
                model,
                constant_at_zero // 3,
                q_terms,
                9,
                f"row_{row_index}_Q",
            )
        elif mode == "exact":
            model.add(
                constant_at_zero
                + sum(
                    coefficient * variable
                    for coefficient, variable in a_terms
                )
                == 0
            )
            model.add(
                constant_at_zero // 3
                + sum(
                    coefficient * variable
                    for coefficient, variable in q_terms
                )
                == 0
            )
        else:
            raise ValueError(
                "mode must be digit2, digit3, digit3_exact_row7, "
                "digit4, or exact"
            )

    statistics = {
        "mode": mode,
        "placement_variables": len(placement),
        "unique_sparse_phase_forms": len(all_forms),
        "phase_form_support_histogram": support_histogram,
        "phase_table_rows": table_rows,
        "explicit_first_digit_rows": len(first_equations),
        "explicit_delayed_digit3_rows": int(mode != "digit2"),
        **row_margin_statistics,
        **exact_e1_statistics,
        "model_variables": len(model.proto.variables),
        "model_constraints": len(model.proto.constraints),
        "linear_constraints": sum(
            constraint.HasField("linear")
            for constraint in model.proto.constraints
        ),
        "table_constraints": sum(
            constraint.HasField("table")
            for constraint in model.proto.constraints
        ),
    }
    return model, placement, profiles, rows, statistics


def solve(
    candidate_index: int,
    mode: str,
    seconds: float,
    workers: int,
    seed: int,
    initial_placement: tuple[int, ...] | None,
    row_margin_aware: bool = False,
    row_margin_target_index: int | None = None,
) -> dict[str, object]:
    started = time.monotonic()
    model, placement, profiles, rows, construction = build_model(
        candidate_index,
        mode,
        row_margin_aware,
        row_margin_target_index,
    )
    if initial_placement is not None:
        if len(initial_placement) != 54:
            raise ValueError("the initial placement must have 54 trits")
        for variable, value in zip(placement, initial_placement):
            model.add_hint(variable, int(value))
    built = time.monotonic()
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = float(seconds)
    solver.parameters.num_search_workers = int(workers)
    solver.parameters.random_seed = int(seed)
    solver.parameters.cp_model_presolve = True
    status = solver.solve(model)
    finished = time.monotonic()

    candidate = second.CANDIDATES[candidate_index]
    result: dict[str, object] = {
        "schema": "lp333-order3-sparse-histogram-cp-sat-v1",
        "scope": (
            "Bounded sparse phase-histogram search. UNKNOWN is not an "
            "exclusion."
        ),
        "label": candidate[0],
        "candidate_index": candidate_index,
        "status": solver.status_name(status),
        "row_margin_aware": row_margin_aware,
        "row_margin_target_index": row_margin_target_index,
        "construction": construction,
        "solver": {
            "seconds": seconds,
            "workers": workers,
            "seed": seed,
            "build_seconds": built - started,
            "solve_seconds": finished - built,
            "branches": solver.num_branches,
            "conflicts": solver.num_conflicts,
            "wall_time": solver.wall_time,
        },
    }
    if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        point = tuple(int(solver.value(variable)) for variable in placement)
        exact_values = second.displayed_values(profiles, point)
        digits = tuple(
            second.lambda_digits(value, 10) for value in exact_values
        )
        required_digit = {
            "digit2": 2,
            "digit3": 3,
            "digit3_exact_row7": 3,
            "digit4": 4,
            "exact": 8,
        }[mode]
        if mode == "exact":
            if any(value != (0, 0) for value in exact_values):
                raise AssertionError("exact histogram witness was not exact")
        elif any(
            any(row[: required_digit + 1]) for row in digits
        ):
            raise AssertionError("histogram prefix failed exact replay")
        if (
            mode == "digit3_exact_row7"
            and exact_values[7] != (0, 0)
        ):
            raise AssertionError("the exact E1-origin row failed replay")
        masks_a, masks_b = second.masks_from_trits(profiles, point)
        phase_sums = phase_sums_from_masks(masks_a, masks_b)
        if row_margin_aware:
            catalog = catalog_phase_sum_intersection(
                candidate[3], candidate[4]
            )
            if phase_sums not in {
                sums for sums, _ in catalog["phase_sum_corpus"]
            }:
                raise AssertionError(
                    "a row-margin-aware witness missed the exact corpus"
                )
        columns = full_witness.expand_columns(masks_a, masks_b)
        proper_fixed = tuple(
            full_witness.fixed_by_multiplier(columns, multiplier)
            for multiplier in full_witness.SUPERGROUP_GENERATORS
        )
        result.update(
            {
                "placement_trits": point,
                "placement_trits_sha256": carry.compact_hash(point),
                "phase_sums": phase_sums,
                "row_margin_join_holds": row_margin_aware,
                "displayed_exact_values": exact_values,
                "lambda_digits_through_9": digits,
                "proper_supergroup_fixed": proper_fixed,
                "next_digit_nonzero_rows": (
                    0
                    if mode == "exact"
                    else sum(
                        row[required_digit + 1] != 0 for row in digits
                    )
                ),
            }
        )
    result["semantic_sha256"] = carry.compact_hash(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=int, default=1, choices=range(5))
    parser.add_argument(
        "--mode",
        choices=(
            "digit2",
            "digit3",
            "digit3_exact_row7",
            "digit4",
            "exact",
        ),
        default="digit3",
    )
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--seed", type=int, default=668)
    parser.add_argument("--initial-certificate", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--row-margins",
        action="store_true",
        help="require exact membership in the compatible six-sum corpus",
    )
    parser.add_argument(
        "--row-margin-target",
        type=int,
        help="fix one zero-based target within the compatible corpus",
    )
    args = parser.parse_args()
    initial = None
    if args.initial_certificate is not None:
        stored = json.loads(args.initial_certificate.read_text())
        if int(stored["candidate_index"]) != args.candidate:
            raise ValueError("initial certificate profile mismatch")
        initial = tuple(map(int, stored["placement_trits"]))
    result = solve(
        args.candidate,
        args.mode,
        args.seconds,
        args.workers,
        args.seed,
        initial,
        args.row_margins,
        args.row_margin_target,
    )
    payload = json.dumps(result, indent=2)
    if args.output is not None:
        args.output.write_text(payload + "\n")
    print(payload)


if __name__ == "__main__":
    main()
