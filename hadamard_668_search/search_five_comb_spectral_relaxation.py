#!/usr/bin/env python3
"""Solve the low-order spectral relaxation of common-type five-comb packing.

This deliberately omits the individual aperiodic-correlation equations.  It
keeps only the exact norm identities at 1, -1, i, and a primitive eighth
root.  The four complementary length-five words have, at either fourth-root
evaluation, two absolute values 1 and two absolute values 3.  Carrier
orientations absorb their signs, so the relaxation is independent of which
of the 48 complementary quartets was chosen.
"""

from __future__ import annotations

import argparse
from itertools import permutations

from ortools.sat.python import cp_model

from check_five_comb_mub_reductions import (
    HOLE_POSITIONS,
    SHIFTS,
    TARGET,
    VECTORS,
    position_incidence,
    row_sign_representative,
    slot_syndrome,
)


def projective_representatives() -> tuple[tuple[int, ...], ...]:
    syndromes = tuple(
        tuple(slot_syndrome(shift, vector, vector) for vector in VECTORS)
        for shift in SHIFTS
    )
    survivors = []
    for labeling in permutations(range(8)):
        syndrome = TARGET
        for slot, label in enumerate(labeling):
            syndrome ^= syndromes[slot][label]
        if syndrome == 0:
            survivors.append(row_sign_representative(labeling))
    result = tuple(sorted(set(survivors)))
    if len(result) != 8:
        raise AssertionError("projective quotient changed")
    return result


PROJECTIVE_REPRESENTATIVES = projective_representatives()

# Up to a carrier orientation, the 48 quartets have only three joint spectra
# (W(1), W(-1)).  Each word occurs with both polarizations.
WORD_SPECTRUM_CLASSES = (
    ((1, 1), (1, -3), (3, -1), (3, 3)),
    ((1, -3), (1, -3), (3, -1), (3, -1)),
    ((1, 1), (1, 1), (3, 3), (3, 3)),
)


def zeta8_coefficients(exponent: int, polarization: int) -> tuple[int, ...]:
    result = [0, 0, 0, 0]
    for power, sign in ((exponent, 1), (exponent + 2, polarization)):
        power %= 8
        if power >= 4:
            power -= 4
            sign = -sign
        result[power] += sign
    return tuple(result)


def add_square(
    model: cp_model.CpModel, value: cp_model.IntVar, bound: int, name: str
) -> cp_model.IntVar:
    square = model.new_int_var(0, bound * bound, name)
    model.add_multiplication_equality(square, [value, value])
    return square


def add_product(
    model: cp_model.CpModel,
    left: cp_model.IntVar,
    right: cp_model.IntVar,
    bound: int,
    name: str,
) -> cp_model.IntVar:
    result = model.new_int_var(-bound * bound, bound * bound, name)
    model.add_multiplication_equality(result, [left, right])
    return result


def build_model(
    projective_index: int,
    roots: frozenset[str],
    spectrum_class: int = 2,
) -> tuple[
    cp_model.CpModel,
    tuple[cp_model.IntVar, ...],
    tuple[cp_model.IntVar, ...],
    tuple[cp_model.IntVar, ...],
]:
    labels = PROJECTIVE_REPRESENTATIVES[projective_index]
    items_catalog = tuple(
        (at_one, at_minus_one, polarization)
        for at_one, at_minus_one in WORD_SPECTRUM_CLASSES[spectrum_class]
        for polarization in (1, -1)
    )
    model = cp_model.CpModel()
    items = tuple(model.new_int_var(0, 7, f"item_{slot}") for slot in range(8))
    model.add_all_different(items)
    orientations = tuple(
        model.new_bool_var(f"orientation_{slot}") for slot in range(8)
    )
    holes = tuple(model.new_bool_var(f"hole_{index}") for index in range(14))
    model.add(orientations[0] == 0)
    carrier_signature = 0
    for shift, label in zip(SHIFTS, labels, strict=True):
        carrier_signature ^= slot_syndrome(
            shift, VECTORS[label], VECTORS[label]
        )
    required_hole_signature = ((1 << 83) - 1) ^ carrier_signature
    hole_incidence = tuple(
        position_incidence(row, position)
        for row, position in HOLE_POSITIONS
    )
    hole_fiber = []
    for mask in range(1 << len(HOLE_POSITIONS)):
        signature = 0
        for index, incidence in enumerate(hole_incidence):
            if (mask >> index) & 1:
                signature ^= incidence
        if signature == required_hole_signature:
            hole_fiber.append(
                tuple((mask >> index) & 1 for index in range(14))
            )
    if len(hole_fiber) != 256:
        raise AssertionError("modulo-four hole fiber changed")
    model.add_allowed_assignments(holes, hole_fiber)

    # Coordinates are evaluations at 1, -1, then real/imaginary at i, then
    # coefficients on 1,zeta,zeta^2,zeta^3 at zeta^8=1, zeta^4=-1.
    coordinate_count = 8
    row_values: list[list[cp_model.IntVar]] = [
        [] for _ in range(4)
    ]
    for row in range(4):
        for coordinate in range(coordinate_count):
            terms = []
            for slot, shift in enumerate(SHIFTS):
                vector_sign = VECTORS[labels[slot]][row]
                z8 = zeta8_coefficients(shift, 1)
                values = []
                for item, (
                    at_one,
                    at_minus_one,
                    polarization,
                ) in enumerate(items_catalog):
                    base = [0] * coordinate_count
                    if polarization == 1:
                        base[0] = 2 * at_one
                        base[1] = 2 * at_one * (-1 if shift & 1 else 1)
                    else:
                        phase = shift % 4
                        if phase == 0:
                            base[2] = 2 * at_one
                        elif phase == 1:
                            base[3] = 2 * at_one
                        elif phase == 2:
                            base[2] = -2 * at_one
                        else:
                            base[3] = -2 * at_one
                    z8 = zeta8_coefficients(shift, polarization)
                    for index in range(4):
                        base[4 + index] = at_minus_one * z8[index]
                    for orientation in (0, 1):
                        multiplier = vector_sign * (-1 if orientation else 1)
                        values.append(
                            (item, orientation, multiplier * base[coordinate])
                        )
                contribution = model.new_int_var(
                    -6, 6, f"carrier_{row}_{coordinate}_{slot}"
                )
                model.add_allowed_assignments(
                    [items[slot], orientations[slot], contribution], values
                )
                terms.append(contribution)

            for hole_index, (hole_row, position) in enumerate(HOLE_POSITIONS):
                if hole_row != row:
                    continue
                base = [0] * coordinate_count
                base[0] = 1
                base[1] = -1 if position & 1 else 1
                phase = position % 4
                if phase == 0:
                    base[2] = 1
                elif phase == 1:
                    base[3] = 1
                elif phase == 2:
                    base[2] = -1
                else:
                    base[3] = -1
                power = position % 8
                z8_sign = 1
                if power >= 4:
                    power -= 4
                    z8_sign = -1
                base[4 + power] = z8_sign
                terms.append(base[coordinate] * (1 - 2 * holes[hole_index]))
            value = model.new_int_var(
                -84, 84, f"value_{row}_{coordinate}"
            )
            model.add(value == sum(terms))
            row_values[row].append(value)

    for coordinate, root_name in ((0, "1"), (1, "-1")):
        if root_name not in roots:
            continue
        model.add(
            sum(
                add_square(
                    model,
                    row_values[row][coordinate],
                    84,
                    f"square_{coordinate}_{row}",
                )
                for row in range(4)
            )
            == 334
        )
    if "i" in roots:
        model.add(
            sum(
                add_square(
                    model,
                    row_values[row][coordinate],
                    84,
                    f"i_{row}_{coordinate}",
                )
                for row in range(4)
                for coordinate in (2, 3)
            )
            == 334
        )
    if "z8" in roots:
        model.add(
            sum(
                add_square(
                    model,
                    row_values[row][coordinate],
                    84,
                    f"z8a_{row}_{coordinate}",
                )
                for row in range(4)
                for coordinate in range(4, 8)
            )
            == 334
        )
        radical_terms = []
        for row in range(4):
            x0, x1, x2, x3 = row_values[row][4:8]
            left = model.new_int_var(-168, 168, f"z8_left_{row}")
            right = model.new_int_var(-168, 168, f"z8_right_{row}")
            model.add(left == x1 - x3)
            model.add(right == x1 + x3)
            radical_terms.append(
                add_product(model, x0, left, 168, f"z8b0_{row}")
            )
            radical_terms.append(
                add_product(model, x2, right, 168, f"z8b2_{row}")
            )
        model.add(sum(radical_terms) == 0)
    return model, items, orientations, holes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--projective", type=int, default=0)
    parser.add_argument("--spectrum-class", type=int, choices=range(3), default=2)
    parser.add_argument("--time-limit", type=float, default=60.0)
    parser.add_argument(
        "--roots",
        default="1,-1,i,z8",
        help="comma-separated subset of 1,-1,i,z8",
    )
    args = parser.parse_args()
    roots = frozenset(args.roots.split(","))
    if not roots <= {"1", "-1", "i", "z8"}:
        raise ValueError("roots must be drawn from 1,-1,i,z8")
    model, items, orientations, holes = build_model(
        args.projective, roots, args.spectrum_class
    )
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.time_limit
    solver.parameters.num_search_workers = 1
    solver.parameters.max_memory_in_mb = 1024
    status = solver.solve(model)
    print(f"status={solver.status_name(status)}")
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return 2 if status == cp_model.UNKNOWN else 1
    print("items=" + ",".join(str(solver.value(value)) for value in items))
    print(
        "orientations="
        + ",".join(str(solver.value(value)) for value in orientations)
    )
    print("holes=" + ",".join(str(solver.value(value)) for value in holes))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
