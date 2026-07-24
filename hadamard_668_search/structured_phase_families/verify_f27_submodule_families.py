#!/usr/bin/env python3
"""Test minimal F27-submodule phase families on the five h=2 profiles.

The six certified class polar operators span F_27 x F_27 on F_3^12.  Each
central six-space has F_27-multiplicity two and therefore 28 minimal
three-dimensional invariant submodules.  This verifier constructs all 56
submodules exactly.

For a fixed profile, the active trits with one channel and one row residue
are embedded as a supported vector in F_3^12.  Channel A must use one common
minimal submodule across its three residues; channel B may independently use
another.  All 56^2 asymmetric choices are intersected with the first
placement digit, deduplicated, and replayed through the second digit.
"""

from __future__ import annotations

from collections import Counter
from itertools import product
import json
from pathlib import Path
import sys
from typing import Sequence


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
SHELL_TWO = SEARCH_ROOT / "shell_two_exact"
SECOND_DIGIT = SEARCH_ROOT / "phase_second_digit"
sys.path.insert(0, str(SHELL_TWO))
sys.path.insert(0, str(SECOND_DIGIT))
sys.path.insert(0, str(SEARCH_ROOT))
sys.path.insert(0, str(HERE))

import verify_lp333_order3_dense_shell_quadratic_algebra as algebra  # noqa: E402
from verify_shell_two_exact_orbits import CANDIDATES  # noqa: E402
from verify_lp333_order3_phase_hensel import (  # noqa: E402
    augmented_system,
    canonical_solution,
    direct_first_digits,
    first_digit_equations,
    matrix_rank,
    matrix_rref,
    profiles_from_ids,
    symbolic_first_digits,
)
from verify_lp333_order3_trit_lift import (  # noqa: E402
    active_trit_coordinates,
)
from verify_phase_second_digit import (  # noqa: E402
    direct_second_digits,
    second_digit_term_data,
    symbolic_second_digits,
)
from verify_structured_phase_families import (  # noqa: E402
    SUPERGROUP_GENERATORS,
    compact_hash,
    multiplier_constraints,
    point_satisfies_constraints,
)


MODULUS = 3
CLASS_COUNT = 12
EXPECTED_SEMANTIC_SHA256 = (
    "15978fe122ffaaba6a752ac6d5995aefabe5b0ba89fd200bb990408189aab61f"
)
CENTRAL_IDEMPOTENTS = (
    (2, 0, 2, 0, 2, 0),
    (0, 2, 0, 2, 0, 2),
)

Vector = tuple[int, ...]
Basis = tuple[Vector, ...]


def matrix_vector(
    matrix: Sequence[Sequence[int]],
    vector: Sequence[int],
) -> Vector:
    return tuple(
        sum(
            int(matrix[row][column]) * int(vector[column])
            for column in range(len(vector))
        )
        % MODULUS
        for row in range(len(matrix))
    )


def independent_span(vectors: Sequence[Sequence[int]]) -> Basis:
    result: list[Vector] = []
    rank = 0
    for vector in vectors:
        normalized = tuple(int(value) % MODULUS for value in vector)
        new_rank = matrix_rank(tuple((*result, normalized)))
        if new_rank > rank:
            result.append(normalized)
            rank = new_rank
    return tuple(result)


def row_space_key(vectors: Sequence[Sequence[int]]) -> Basis:
    if not vectors:
        return ()
    rref, _, _ = matrix_rref(vectors)
    return tuple(row for row in rref if any(row))


def nullspace_basis(
    rows: Sequence[Sequence[int]],
    columns: int,
) -> Basis:
    if rows and any(len(row) != columns for row in rows):
        raise ValueError("matrix width changed")
    rref, pivots, _ = matrix_rref(rows)
    pivot_set = set(pivots)
    result = []
    for free in range(columns):
        if free in pivot_set:
            continue
        vector = [0] * columns
        vector[free] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -rref[row][free] % MODULUS
        result.append(tuple(vector))
    return tuple(result)


def image_basis(matrix: Sequence[Sequence[int]]) -> Basis:
    columns = tuple(
        tuple(matrix[row][column] for row in range(len(matrix)))
        for column in range(len(matrix[0]))
    )
    return independent_span(columns)


def field_generator(
    idempotent: Sequence[int],
) -> tuple[int, ...]:
    """Choose the first element generating the three-dimensional ideal."""

    for candidate in sorted(algebra.ideal_generated_by(tuple(idempotent))):
        square = algebra.algebra_product(candidate, candidate)
        if matrix_rank((tuple(idempotent), candidate, square)) == 3:
            return candidate
    raise AssertionError("an F27 component lost its field generator")


def minimal_submodules() -> tuple[dict[str, object], ...]:
    """Construct the 28 F27-lines in each central six-space."""

    records = []
    for component, idempotent in enumerate(CENTRAL_IDEMPOTENTS):
        projector = algebra.combine(idempotent)
        ambient = image_basis(projector)
        if len(ambient) != 6:
            raise AssertionError("central image dimension changed")
        generator_coordinates = field_generator(idempotent)
        generator = algebra.combine(generator_coordinates)
        submodules: dict[Basis, Basis] = {}
        for coefficients in product(range(MODULUS), repeat=6):
            if not any(coefficients):
                continue
            vector = tuple(
                sum(
                    coefficients[index] * ambient[index][coordinate]
                    for index in range(6)
                )
                % MODULUS
                for coordinate in range(CLASS_COUNT)
            )
            first = matrix_vector(generator, vector)
            second = matrix_vector(generator, first)
            basis = independent_span((vector, first, second))
            if len(basis) != 3:
                raise AssertionError("a nonzero F27 orbit lost dimension")
            key = row_space_key(basis)
            submodules[key] = key
        if len(submodules) != 28:
            raise AssertionError("an F27 projective line lost a point")

        for basis in submodules.values():
            for operator in algebra.POLAR:
                for vector in basis:
                    image = matrix_vector(operator, vector)
                    if matrix_rank(tuple((*basis, image))) != 3:
                        raise AssertionError(
                            "declared submodule is not invariant"
                        )
        records.extend({
            "component": component,
            "idempotent": idempotent,
            "generator": generator_coordinates,
            "basis": basis,
        } for basis in sorted(submodules))
    if len(records) != 56:
        raise AssertionError("minimal submodule census changed")
    return tuple(records)


def slice_intersection_basis(
    profiles: Sequence[Sequence[Sequence[int]]],
    coordinate_index: dict[tuple[int, int, int], int],
    channel: int,
    residue: int,
    submodule: Sequence[Sequence[int]],
) -> Basis:
    """Intersect one minimal submodule with the active coordinate support."""

    active_classes = {
        class_index
        for class_index in range(CLASS_COUNT)
        if profiles[channel][class_index][residue] in (1, 2)
    }
    outside_rows = tuple(
        tuple(submodule[basis_index][class_index] for basis_index in range(3))
        for class_index in range(CLASS_COUNT)
        if class_index not in active_classes
    )
    coefficient_kernel = nullspace_basis(outside_rows, 3)
    embedded = []
    for coefficients in coefficient_kernel:
        local = tuple(
            sum(
                coefficients[index] * submodule[index][class_index]
                for index in range(3)
            )
            % MODULUS
            for class_index in range(CLASS_COUNT)
        )
        vector = [0] * len(coordinate_index)
        for class_index in active_classes:
            vector[
                coordinate_index[(channel, class_index, residue)]
            ] = local[class_index]
        embedded.append(tuple(vector))
    return independent_span(embedded)


def compose_first_digit(
    equation_rows: Sequence[Sequence[int]],
    basis: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            sum(
                row[coordinate] * basis[column][coordinate]
                for coordinate in range(len(basis[column]))
            )
            % MODULUS
            for column in range(len(basis))
        )
        + (row[-1] % MODULUS,)
        for row in equation_rows
    )


def affine_trit_space(
    rows: Sequence[Sequence[int]],
    basis: Sequence[Sequence[int]],
) -> tuple[Vector, Basis] | None:
    parameter_count = len(basis)
    parameter_origin = canonical_solution(rows, parameter_count)
    if parameter_origin is None:
        return None
    parameter_kernel = nullspace_basis(
        tuple(row[:-1] for row in rows), parameter_count
    )
    trit_origin = tuple(
        sum(
            parameter_origin[column] * basis[column][coordinate]
            for column in range(parameter_count)
        )
        % MODULUS
        for coordinate in range(len(basis[0]))
    ) if basis else (0,) * 54
    trit_basis = independent_span(tuple(
        tuple(
            sum(
                parameter_vector[column] * basis[column][coordinate]
                for column in range(parameter_count)
            )
            % MODULUS
            for coordinate in range(len(basis[0]))
        )
        for parameter_vector in parameter_kernel
    ))
    return trit_origin, trit_basis


def affine_points(origin: Sequence[int], basis: Sequence[Sequence[int]]):
    for coefficients in product(range(MODULUS), repeat=len(basis)):
        yield tuple(
            (
                origin[coordinate]
                + sum(
                    coefficients[index] * basis[index][coordinate]
                    for index in range(len(basis))
                )
            )
            % MODULUS
            for coordinate in range(len(origin))
        )


def audit_profile(
    candidate: Sequence[object],
    submodules: Sequence[dict[str, object]],
) -> dict[str, object]:
    label, partition, target, identifiers_a, identifiers_b = candidate
    profiles = profiles_from_ids(identifiers_a, identifiers_b)
    coordinates = active_trit_coordinates(profiles)
    if len(coordinates) != 54:
        raise AssertionError("shell-two active dimension changed")
    coordinate_index = {
        coordinate: index for index, coordinate in enumerate(coordinates)
    }
    equations = first_digit_equations(profiles)
    equation_rows = augmented_system(equations)

    channel_bases: dict[tuple[int, int], Basis] = {}
    slice_dimensions: dict[tuple[int, int, int], int] = {}
    for submodule_index, record in enumerate(submodules):
        submodule = record["basis"]
        assert isinstance(submodule, tuple)
        for channel in range(2):
            embedded = []
            for residue in range(3):
                intersection = slice_intersection_basis(
                    profiles,
                    coordinate_index,
                    channel,
                    residue,
                    submodule,
                )
                embedded.extend(intersection)
                slice_dimensions[
                    (submodule_index, channel, residue)
                ] = len(intersection)
            channel_bases[(submodule_index, channel)] = independent_span(
                embedded
            )

    placements: set[Vector] = set()
    solution_dimension_histogram: Counter[int] = Counter()
    compatible_pairs = []
    for submodule_a in range(len(submodules)):
        for submodule_b in range(len(submodules)):
            basis = independent_span(
                channel_bases[(submodule_a, 0)]
                + channel_bases[(submodule_b, 1)]
            )
            restricted = compose_first_digit(equation_rows, basis)
            affine = affine_trit_space(restricted, basis)
            if affine is None:
                continue
            origin, kernel = affine
            solution_dimension_histogram[len(kernel)] += 1
            compatible_pairs.append((submodule_a, submodule_b, len(kernel)))
            placements.update(affine_points(origin, kernel))

    term_data = second_digit_term_data(profiles)
    second_digit_survivors = []
    zero_row_histogram: Counter[int] = Counter()
    nearest = None
    nearest_residual = None
    maximum_zero_rows = -1
    supergroup_constraints = {
        identifier: multiplier_constraints(profiles, generator)
        for identifier, generator in SUPERGROUP_GENERATORS
    }
    fixed_counts = Counter()
    supergroup_free = 0
    for trits in sorted(placements):
        if symbolic_first_digits(equations, trits) != (0,) * 20:
            raise AssertionError("submodule point left first-digit space")
        residual = symbolic_second_digits(term_data, trits)
        zero_rows = sum(value == 0 for value in residual)
        zero_row_histogram[zero_rows] += 1
        if zero_rows > maximum_zero_rows:
            maximum_zero_rows = zero_rows
            nearest = trits
            nearest_residual = residual
        if zero_rows == 20:
            second_digit_survivors.append(trits)
        memberships = tuple(
            identifier
            for identifier, constraints in supergroup_constraints.items()
            if point_satisfies_constraints(trits, constraints)
        )
        fixed_counts.update(memberships)
        if not memberships:
            supergroup_free += 1

    if placements:
        assert nearest is not None and nearest_residual is not None
        if direct_first_digits(profiles, nearest) != (0,) * 20:
            raise AssertionError("nearest submodule point failed digit one")
        if direct_second_digits(profiles, nearest) != nearest_residual:
            raise AssertionError("nearest submodule point failed digit two")
    else:
        nearest = None
        nearest_residual = None
        maximum_zero_rows = None

    return {
        "profile": label,
        "partition": partition,
        "target": target,
        "submodule_pairs_tested": len(submodules) ** 2,
        "compatible_submodule_pairs": len(compatible_pairs),
        "compatible_pair_solution_dimension_histogram": {
            str(key): solution_dimension_histogram[key]
            for key in sorted(solution_dimension_histogram)
        },
        "compatible_pairs_sha256": compact_hash(compatible_pairs),
        "distinct_first_digit_placements": len(placements),
        "first_digit_placements_sha256": compact_hash(
            tuple(sorted(placements))
        ),
        "minimal_supergroup_fixed_counts": {
            identifier: fixed_counts[identifier]
            for identifier, _ in SUPERGROUP_GENERATORS
        },
        "proper_supergroup_free_placements": supergroup_free,
        "second_digit_survivors": len(second_digit_survivors),
        "second_digit_zero_row_histogram": {
            str(key): zero_row_histogram[key]
            for key in sorted(zero_row_histogram)
        },
        "maximum_second_digit_zero_rows": maximum_zero_rows,
        "nearest_trits": nearest,
        "nearest_second_digit_residual": nearest_residual,
        "nearest_trit_sha256": (
            None if nearest is None else compact_hash(nearest)
        ),
        "slice_intersection_dimension_sha256": compact_hash(
            tuple(sorted(slice_dimensions.items()))
        ),
    }


def build_certificate() -> dict[str, object]:
    algebra.verify_pencil_algebra()
    submodules = minimal_submodules()
    audits = tuple(
        audit_profile(candidate, submodules) for candidate in CANDIDATES
    )
    return {
        "schema": "lp333-shell-two-f27-minimal-submodules-v1",
        "scope": (
            "All channel-asymmetric pairs of minimal F27 submodules from "
            "the certified F27xF27 class-operator algebra, intersected "
            "with all five shell-two profiles through placement digit two."
        ),
        "central_components": 2,
        "central_component_dimension": 6,
        "minimal_submodule_dimension": 3,
        "minimal_submodules_per_component": 28,
        "minimal_submodules_total": len(submodules),
        "submodule_semantic_sha256": compact_hash(submodules),
        "audits": audits,
        "total_distinct_first_digit_placements": sum(
            int(audit["distinct_first_digit_placements"])
            for audit in audits
        ),
        "total_proper_supergroup_free_placements": sum(
            int(audit["proper_supergroup_free_placements"])
            for audit in audits
        ),
        "total_second_digit_survivors": sum(
            int(audit["second_digit_survivors"]) for audit in audits
        ),
    }


def main() -> None:
    certificate = build_certificate()
    semantic_sha256 = compact_hash(certificate)
    if (
        EXPECTED_SEMANTIC_SHA256
        and semantic_sha256 != EXPECTED_SEMANTIC_SHA256
    ):
        raise AssertionError("F27-submodule semantic certificate changed")
    print(
        f"submodules={certificate['minimal_submodules_total']} "
        f"first_digit={certificate['total_distinct_first_digit_placements']} "
        f"supergroup_free="
        f"{certificate['total_proper_supergroup_free_placements']} "
        f"second_digit={certificate['total_second_digit_survivors']}"
    )
    for audit in certificate["audits"]:
        print(
            f"{audit['profile']}: "
            f"pairs={audit['compatible_submodule_pairs']} "
            f"first={audit['distinct_first_digit_placements']} "
            f"free={audit['proper_supergroup_free_placements']} "
            f"second={audit['second_digit_survivors']} "
            f"best={audit['maximum_second_digit_zero_rows']}"
        )
    print(f"semantic_sha256={semantic_sha256}")


if __name__ == "__main__":
    main()
