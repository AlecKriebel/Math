#!/usr/bin/env python3
"""Exact root-of-unity filter for unrestricted common-type five-comb packing.

For a base sequence, the summed power spectrum is the constant 334.
This model imposes that algebraic identity at

    1, -1, i, zeta_8, zeta_16, zeta_32,

but deliberately omits the 83 individual aperiodic equations.  At
``zeta_16`` a comb word is evaluated at ``i``; this is the first root in
the chain that distinguishes word phases invisible at roots of order at
most eight.  ``zeta_32`` then evaluates the word at ``zeta_8`` and is the
next exact rung of the dyadic spectral ladder.

All 4,096 normalized projective labelings are retained simultaneously via
the exact rank-nine hole-quotient equations.  The full modulo-four system
then couples those labels to the fourteen physical hole signs.  Type
placement and carrier orientations remain arbitrary.  Thus infeasibility
is an exact obstruction for one complementary-quartet common-type family;
feasibility is only a spectral relaxation, not a base sequence.
"""

from __future__ import annotations

import argparse
from itertools import product
import json
from pathlib import Path
from typing import Iterable, Sequence

from ortools.sat.python import cp_model

from check_five_comb_mub_reductions import (
    HOLE_POSITIONS,
    LENGTHS,
    PROJECTIVE_RREF,
    QUARTETS,
    SHIFTS,
    VECTORS,
    position_incidence,
)
from search_five_comb_unrestricted_projective_cp_sat import (
    SLOT_COUNT,
    TYPE_COUNT,
    add_bool_lex_less_or_equal,
    add_physical_high_lag_boundary_table,
    reconstruct,
    scalar_carrier,
    xor_var,
)


ROOT_ORDERS = (1, 2, 4, 8, 16, 32)
FULL_MOD4_TARGET = (1 << 83) - 1


def root_weight(order: int, position: int) -> tuple[int, ...]:
    """Represent zeta_order**position in its power-of-two basis."""

    if order == 1:
        return (1,)
    if order not in ROOT_ORDERS[1:]:
        raise ValueError("root order must be 1, 2, 4, 8, 16, or 32")
    degree = order // 2
    exponent = position % order
    sign = 1
    if exponent >= degree:
        exponent -= degree
        sign = -1
    result = [0] * degree
    result[exponent] = sign
    return tuple(result)


def reduce_root_power(order: int, exponent: int) -> tuple[int, int]:
    """Return sign and basis exponent for a possibly negative power."""

    if order == 1:
        return 1, 0
    degree = order // 2
    exponent %= order
    if exponent >= degree:
        return -1, exponent - degree
    return 1, exponent


def spectral_norm_coefficients(
    sequences: Sequence[Sequence[int]],
    order: int,
) -> tuple[int, ...]:
    """Return the exact basis coefficients of sum |X(zeta_order)|^2."""

    degree = 1 if order == 1 else order // 2
    result = [0] * degree
    for sequence in sequences:
        value = [0] * degree
        for position, coefficient in enumerate(sequence):
            weight = root_weight(order, position)
            for coordinate in range(degree):
                value[coordinate] += coefficient * weight[coordinate]
        for left in range(degree):
            for right in range(degree):
                sign, coordinate = reduce_root_power(
                    order, left - right
                )
                result[coordinate] += (
                    sign * value[left] * value[right]
                )
    return tuple(result)


def full_projective_slot_states() -> tuple[tuple[int, ...], ...]:
    """Return exact, unquotiented mod-four signatures for all labels."""

    states = []
    for shift in SHIFTS:
        slot_states = []
        for vector in VECTORS:
            signature = 0
            for tooth in range(5):
                for row in range(4):
                    if vector[row] < 0:
                        signature ^= position_incidence(
                            row, shift + 4 * tooth
                        )
                        signature ^= position_incidence(
                            row, shift + 42 + 4 * tooth
                        )
            slot_states.append(signature)
        states.append(tuple(slot_states))
    result = tuple(states)
    for slot, slot_states in enumerate(result):
        for label in range(8):
            recovered = slot_states[0]
            for bit in range(3):
                if (label >> bit) & 1:
                    recovered ^= (
                        slot_states[1 << bit] ^ slot_states[0]
                    )
            if recovered != slot_states[label]:
                raise AssertionError(
                    f"full slot {slot} signature is not affine"
                )
    return result


FULL_PROJECTIVE_SLOT_STATES = full_projective_slot_states()
HOLE_INCIDENCES = tuple(
    position_incidence(row, position) for row, position in HOLE_POSITIONS
)


def full_mod4_syndrome(
    labels: Sequence[int],
    holes: Sequence[int],
) -> int:
    """Return the physical 83-bit negative-entry incidence signature."""

    signature = 0
    for slot, label in enumerate(labels):
        signature ^= FULL_PROJECTIVE_SLOT_STATES[slot][label]
    for hole, incidence in zip(holes, HOLE_INCIDENCES, strict=True):
        if hole:
            signature ^= incidence
    return signature


def add_small_parity_equation(
    model: cp_model.CpModel,
    variables: Sequence[cp_model.IntVar],
    right_hand_side: int,
) -> None:
    rows = tuple(
        values
        for values in product((0, 1), repeat=len(variables))
        if sum(values) % 2 == right_hand_side
    )
    model.add_allowed_assignments(variables, rows)


def add_xor_equation(
    model: cp_model.CpModel,
    variables: Sequence[cp_model.IntVar],
    right_hand_side: int,
    fixed_one: cp_model.IntVar,
) -> None:
    """Add XOR(variables) == right_hand_side."""

    if not variables:
        if right_hand_side:
            model.add(0 == 1)
        return
    literals = list(variables)
    # AddBoolXOr requires an odd number of true literals.
    if right_hand_side == 0:
        literals.append(fixed_one)
    model.add_bool_xor(literals)


def add_wide_table(
    model: cp_model.CpModel,
    selectors: Sequence[cp_model.IntVar],
    rows: Sequence[tuple[int, ...]],
    output_count: int,
    name: str,
) -> tuple[cp_model.IntVar, ...]:
    selector_count = len(selectors)
    outputs = []
    for coordinate in range(output_count):
        values = tuple(
            row[selector_count + coordinate] for row in rows
        )
        outputs.append(
            model.new_int_var(
                min(values),
                max(values),
                f"{name}_{coordinate}",
            )
        )
    model.add_allowed_assignments([*selectors, *outputs], rows)
    return tuple(outputs)


def add_norm_identity(
    model: cp_model.CpModel,
    row_values: Sequence[Sequence[cp_model.IntVar]],
    order: int,
) -> None:
    """Impose sum |X(zeta_order)|^2 = 334 in the exact power basis."""

    degree = 1 if order == 1 else order // 2
    coefficient_terms: list[list[cp_model.LinearExpr]] = [
        [] for _ in range(degree)
    ]
    for row, values in enumerate(row_values):
        if len(values) != degree:
            raise AssertionError("spectral coordinate count changed")
        for left in range(degree):
            for right in range(left, degree):
                product_variable = model.new_int_var(
                    -84 * 84,
                    84 * 84,
                    f"norm_{order}_{row}_{left}_{right}",
                )
                model.add_multiplication_equality(
                    product_variable,
                    [values[left], values[right]],
                )
                ordered_pairs = ((left, right),)
                if left != right:
                    ordered_pairs += ((right, left),)
                for first, second in ordered_pairs:
                    sign, coordinate = reduce_root_power(
                        order, first - second
                    )
                    coefficient_terms[coordinate].append(
                        sign * product_variable
                    )
    model.add(sum(coefficient_terms[0]) == 334)
    for coordinate in range(1, degree):
        model.add(sum(coefficient_terms[coordinate]) == 0)


def build_model(
    quartet_index: int,
    orders: Iterable[int] = ROOT_ORDERS,
) -> tuple[
    cp_model.CpModel,
    tuple[cp_model.IntVar, ...],
    tuple[cp_model.IntVar, ...],
    tuple[cp_model.IntVar, ...],
    tuple[cp_model.IntVar, ...],
]:
    if not 0 <= quartet_index < len(QUARTETS):
        raise ValueError("quartet index must lie in 0..47")
    selected_orders = tuple(sorted(set(orders)))
    if not selected_orders or any(order not in ROOT_ORDERS for order in selected_orders):
        raise ValueError("orders must be a nonempty subset of 1,2,4,8,16,32")

    quartet = QUARTETS[quartet_index]
    carriers = tuple(
        tuple(
            scalar_carrier(quartet, slot, carrier_type)
            for carrier_type in range(TYPE_COUNT)
        )
        for slot in range(SLOT_COUNT)
    )
    model = cp_model.CpModel()

    label_bits = tuple(
        tuple(
            model.new_bool_var(f"label_{slot}_bit_{bit}")
            for bit in range(3)
        )
        for slot in range(SLOT_COUNT)
    )
    labels = tuple(
        model.new_int_var(0, 7, f"label_{slot}")
        for slot in range(SLOT_COUNT)
    )
    for slot in range(SLOT_COUNT):
        model.add(
            labels[slot]
            == label_bits[slot][0]
            + 2 * label_bits[slot][1]
            + 4 * label_bits[slot][2]
        )
    for bit in range(3):
        model.add(label_bits[0][bit] == 0)
    flat_label_bits = tuple(bit for slot in label_bits for bit in slot)
    for indices, right_hand_side in PROJECTIVE_RREF:
        add_small_parity_equation(
            model,
            tuple(flat_label_bits[index] for index in indices),
            right_hand_side,
        )
    middle = tuple(label_bits[slot][1] for slot in range(1, SLOT_COUNT))
    low = tuple(label_bits[slot][0] for slot in range(1, SLOT_COUNT))
    high = tuple(label_bits[slot][2] for slot in range(1, SLOT_COUNT))
    low_xor_high = tuple(
        xor_var(model, low[index], high[index], f"row_mask_{index}")
        for index in range(SLOT_COUNT - 1)
    )
    for name, mask in (
        ("swap_long", low),
        ("swap_both", high),
        ("swap_short", low_xor_high),
    ):
        transformed = tuple(
            xor_var(
                model,
                middle[index],
                mask[index],
                f"{name}_middle_{index}",
            )
            for index in range(SLOT_COUNT - 1)
        )
        add_bool_lex_less_or_equal(model, middle, transformed, name)
    model.add_bool_or(
        (
            label_bits[2][0],
            label_bits[7][2],
            label_bits[1][1],
            label_bits[7][1],
        )
    )

    types = tuple(
        model.new_int_var(0, TYPE_COUNT - 1, f"type_{slot}")
        for slot in range(SLOT_COUNT)
    )
    model.add_all_different(types)
    orientations = tuple(
        model.new_bool_var(f"orientation_{slot}")
        for slot in range(SLOT_COUNT)
    )
    model.add(orientations[0] == 0)
    if 1 in selected_orders and 2 in selected_orders:
        model.add(orientations[1] == 0)
    holes = tuple(
        model.new_bool_var(f"hole_{index}")
        for index in range(len(HOLE_POSITIONS))
    )

    # Couple the projective labels to the physical hole signs.  The actual
    # word, polarization, and carrier orientation have zero full incidence;
    # only the projective row signs enter this parity system.
    fixed_one = model.new_bool_var("fixed_one")
    model.add(fixed_one == 1)
    baseline = FULL_MOD4_TARGET
    for slot_states in FULL_PROJECTIVE_SLOT_STATES:
        baseline ^= slot_states[0]
    for equation in range(83):
        variables = []
        for slot, slot_states in enumerate(FULL_PROJECTIVE_SLOT_STATES):
            for bit in range(3):
                delta = slot_states[1 << bit] ^ slot_states[0]
                if (delta >> equation) & 1:
                    variables.append(label_bits[slot][bit])
        for hole, incidence in zip(holes, HOLE_INCIDENCES, strict=True):
            if (incidence >> equation) & 1:
                variables.append(hole)
        add_xor_equation(
            model,
            variables,
            (baseline >> equation) & 1,
            fixed_one,
        )

    # Explicit form of the complete normalized physical modulo-four fiber,
    # followed by the lag-82 and redundant mod-eight propagation cuts.
    model.add(holes[0] == holes[4])
    model.add(holes[1] == holes[5])
    model.add(holes[2] == holes[6])
    model.add(holes[3] + holes[7] == 1)
    model.add(holes[8] == holes[11])
    model.add(holes[10] == holes[13])
    model.add(holes[2] + holes[10] == 1)
    model.add_bool_xor(holes[:8])
    add_small_parity_equation(
        model,
        (holes[8], holes[10], holes[11], holes[13]),
        0,
    )
    add_physical_high_lag_boundary_table(
        model,
        label_bits,
        types,
        orientations,
        holes,
        quartet,
    )

    for order in selected_orders:
        degree = 1 if order == 1 else order // 2
        row_values: list[tuple[cp_model.IntVar, ...]] = []
        for row in range(4):
            coordinate_terms: list[list[cp_model.LinearExpr]] = [
                [] for _ in range(degree)
            ]
            for slot in range(SLOT_COUNT):
                table_rows = []
                for label in range(8):
                    projective_sign = VECTORS[label][row]
                    for carrier_type in range(TYPE_COUNT):
                        carrier = carriers[slot][carrier_type]
                        base = [0] * degree
                        for position, coefficient in carrier.items():
                            weight = root_weight(order, position)
                            for coordinate in range(degree):
                                base[coordinate] += (
                                    coefficient * weight[coordinate]
                                )
                        for orientation in (0, 1):
                            multiplier = (
                                -projective_sign
                                if orientation
                                else projective_sign
                            )
                            table_rows.append(
                                (
                                    label,
                                    carrier_type,
                                    orientation,
                                    *(
                                        multiplier * value
                                        for value in base
                                    ),
                                )
                            )
                contributions = add_wide_table(
                    model,
                    (labels[slot], types[slot], orientations[slot]),
                    table_rows,
                    degree,
                    f"root_{order}_row_{row}_slot_{slot}",
                )
                for coordinate, contribution in enumerate(contributions):
                    coordinate_terms[coordinate].append(contribution)

            for hole_index, (hole_row, position) in enumerate(HOLE_POSITIONS):
                if hole_row != row:
                    continue
                weight = root_weight(order, position)
                for coordinate in range(degree):
                    coordinate_terms[coordinate].append(
                        weight[coordinate] * (1 - 2 * holes[hole_index])
                    )

            values = []
            for coordinate in range(degree):
                value = model.new_int_var(
                    -LENGTHS[row],
                    LENGTHS[row],
                    f"root_{order}_row_{row}_value_{coordinate}",
                )
                model.add(value == sum(coordinate_terms[coordinate]))
                values.append(value)
            row_values.append(tuple(values))
        add_norm_identity(model, row_values, order)

    return model, labels, types, orientations, holes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quartet", type=int, required=True)
    parser.add_argument(
        "--orders",
        default="1,2,4,8,16,32",
        help="comma-separated nonempty subset of 1,2,4,8,16,32",
    )
    parser.add_argument("--time-limit", type=float, default=600.0)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--max-memory-mb", type=int, default=4096)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    orders = tuple(int(value) for value in args.orders.split(","))
    model, label_vars, type_vars, orientation_vars, hole_vars = build_model(
        args.quartet, orders
    )
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.time_limit
    solver.parameters.num_search_workers = args.workers
    solver.parameters.max_memory_in_mb = args.max_memory_mb
    status = solver.solve(model)
    status_name = solver.status_name(status)
    print(f"status={status_name}")
    print(f"quartet={args.quartet}")
    print("orders=" + ",".join(str(order) for order in sorted(set(orders))))
    print(f"wall_time={solver.wall_time:.6f}")
    print(f"conflicts={solver.num_conflicts}")
    print(f"branches={solver.num_branches}")
    print(f"booleans={solver.num_booleans}")
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return 2 if status == cp_model.UNKNOWN else 1

    labels = tuple(solver.value(variable) for variable in label_vars)
    types = tuple(solver.value(variable) for variable in type_vars)
    orientations = tuple(solver.value(variable) for variable in orientation_vars)
    holes = tuple(solver.value(variable) for variable in hole_vars)
    sequences = reconstruct(
        args.quartet, labels, types, orientations, holes
    )
    expected = {
        order: (334,) + (0,) * ((1 if order == 1 else order // 2) - 1)
        for order in set(orders)
    }
    for order, target in expected.items():
        if spectral_norm_coefficients(sequences, order) != target:
            raise AssertionError("solver emitted an invalid spectral witness")

    # The full mod-four equations say every aperiodic distance is odd.
    for lag in range(1, 84):
        distance = sum(
            sequence[position] != sequence[position + lag]
            for sequence in sequences
            for position in range(len(sequence) - lag)
        )
        if distance % 2 != 1:
            raise AssertionError("solver emitted an invalid mod-four witness")

    print("labels=" + ",".join(str(value) for value in labels))
    print("types=" + ",".join(str(value) for value in types))
    print("orientations=" + ",".join(str(value) for value in orientations))
    print("holes=" + ",".join(str(value) for value in holes))
    if args.output:
        payload = {
            "format": "h668-five-comb-spectral16-relaxation-v1",
            "quartet_index": args.quartet,
            "orders": list(sorted(set(orders))),
            "labels": list(labels),
            "types": list(types),
            "orientations": list(orientations),
            "holes": list(holes),
            "norm_coefficients": {
                str(order): list(spectral_norm_coefficients(sequences, order))
                for order in sorted(set(orders))
            },
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"witness={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
