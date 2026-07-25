#!/usr/bin/env python3
"""Exact local rank-two correction audit at the anti-tensor near misses.

The certified rank-one anti-tensor audit found two profiles whose best
points satisfy 18 of the 20 placement-digit-two equations.  At each pinned
near miss u, this verifier adds one further separable opposite component
in each channel,

    v_X(j,s) = h_j F_X(j mod 6) G_X(s).

The row functions G_X run through all 13 projective directions in F_3^3,
including the constant direction.  For each of the 13^2 direction pairs,
linear algebra first computes every correction v preserving placement
digit one.  Only that small union is evaluated in all twenty exact
placement-digit-two quadratics.

The verifier also checks the inhomogeneous linearized (Newton) correction
equations at every chart.  That calculation is diagnostic: the exact
finite correction exclusion is the primary theorem.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys
from typing import Sequence


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
ANTI_TENSOR = SEARCH_ROOT / "five_orbit_family_audit"
sys.path.insert(0, str(ANTI_TENSOR))

import verify_anti_tensor_family as anti  # noqa: E402


MODULUS = 3
TRIT_COUNT = 54
EXPECTED_SEMANTIC_SHA256 = (
    "ed254a1e0a884227b447d31910298ea09ef9d7080b244bce3934c459bed9c4b8"
)

Vector = tuple[int, ...]
Direction = tuple[int, int, int]


PINNED_BASES: dict[str, tuple[Vector, ...]] = {
    "h2-422220-2": (
        (
            0, 0, 2, 2, 1, 2, 2, 2, 1, 1, 1, 0, 0, 2, 1, 1, 0, 1,
            2, 2, 0, 0, 0, 2, 2, 2, 2, 1, 2, 0, 1, 2, 0, 1, 2, 2,
            0, 0, 2, 0, 0, 0, 1, 1, 1, 2, 0, 1, 2, 1, 2, 1, 0, 1,
        ),
        (
            2, 1, 1, 0, 1, 2, 2, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 1,
            2, 2, 2, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 2, 0, 1, 2, 1,
            2, 1, 0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 2, 0, 0, 2, 0,
        ),
    ),
    "h2-422220-3": (
        (
            2, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 2, 1, 1, 1, 2, 0,
            2, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 1, 0, 2, 0, 1, 1,
            1, 1, 1, 2, 0, 0, 1, 2, 1, 1, 0, 0, 1, 2, 1, 1, 1, 1,
        ),
    ),
}


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


def packed_hash(vectors: Sequence[Vector]) -> str:
    if any(len(vector) != TRIT_COUNT for vector in vectors):
        raise AssertionError("packed correction width changed")
    return sha256(b"".join(bytes(vector) for vector in vectors)).hexdigest()


def add(left: Sequence[int], right: Sequence[int], scale: int = 1) -> Vector:
    return tuple(
        (int(x) + scale * int(y)) % MODULUS
        for x, y in zip(left, right)
    )


def all_row_directions() -> tuple[Direction, ...]:
    """Return P^2(F_3), including the constant-function line."""

    result = tuple(sorted({
        anti.canonical_projective(vector)
        for vector in product(range(MODULUS), repeat=3)
        if any(vector)
    }))
    if len(result) != 13 or (1, 1, 1) not in result:
        raise AssertionError("projective row-direction census changed")
    return result


def correction_features(
    coordinates: Sequence[tuple[int, int, int]],
    direction_a: Direction,
    direction_b: Direction,
) -> tuple[Vector, ...]:
    """Return the 54 by 12 feature matrix of a separable correction."""

    rows = []
    directions = (direction_a, direction_b)
    for channel, class_index, residue in coordinates:
        row = [0] * 12
        row[6 * channel + class_index % 6] = (
            anti.structured.opposite_sign(class_index)
            * directions[channel][residue]
        ) % MODULUS
        rows.append(tuple(row))
    return tuple(rows)


def correction_image_basis(
    coefficient_rows: Sequence[Sequence[int]],
    features: Sequence[Sequence[int]],
) -> tuple[Vector, ...]:
    """Eliminate parameters and return distinct first-digit-zero vectors."""

    parameter_count = len(features[0])
    restricted = tuple(
        tuple(
            sum(
                int(row[coordinate]) * int(features[coordinate][parameter])
                for coordinate in range(TRIT_COUNT)
            ) % MODULUS
            for parameter in range(parameter_count)
        )
        for row in coefficient_rows
    )
    parameter_kernel = anti.structured.nullspace_basis(
        restricted, parameter_count
    )
    image = tuple(
        anti.structured.matrix_vector(features, vector)
        for vector in parameter_kernel
    )
    basis = anti.structured.independent_span(image)
    for vector in basis:
        if any(
            sum(int(x) * int(y) for x, y in zip(row, vector)) % MODULUS
            for row in coefficient_rows
        ):
            raise AssertionError("correction escaped the first-digit kernel")
    return basis


def planes_containing(direction: Direction) -> tuple[tuple[Direction, ...], ...]:
    """Return the four two-dimensional subspaces containing one line."""

    planes: dict[tuple[Direction, ...], tuple[Direction, ...]] = {}
    for second in product(range(MODULUS), repeat=3):
        basis = anti.structured.independent_span((direction, second))
        if len(basis) != 2:
            continue
        span = tuple(sorted(
            tuple(
                sum(
                    coefficients[index] * basis[index][coordinate]
                    for index in range(2)
                ) % MODULUS
                for coordinate in range(3)
            )
            for coefficients in product(range(MODULUS), repeat=2)
        ))
        planes[span] = basis
    result = tuple(planes[key] for key in sorted(planes))
    if len(result) != 4:
        raise AssertionError("planes through a projective line changed")
    return result


def full_rank_two_features(
    coordinates: Sequence[tuple[int, int, int]],
    plane_a: Sequence[Direction],
    plane_b: Sequence[Direction],
) -> tuple[Vector, ...]:
    """Return P(x,s)+h*H(z,s), with each row of H in a fixed plane."""

    if len(plane_a) != 2 or len(plane_b) != 2:
        raise ValueError("a rank-two chart needs two row directions")
    rows = []
    planes = (plane_a, plane_b)
    for channel, class_index, residue in coordinates:
        row = [0] * 36
        offset = 18 * channel
        x = class_index % 3
        row[offset:offset + 6] = (
            1, x, residue, x * x, x * residue, residue * residue
        )
        for direction_index, direction in enumerate(planes[channel]):
            row[
                offset + 6 + 6 * direction_index + class_index % 6
            ] = (
                anti.structured.opposite_sign(class_index)
                * direction[residue]
            ) % MODULUS
        rows.append(tuple(value % MODULUS for value in row))
    return tuple(rows)


def linearized_rows(
    term_data: Sequence[tuple[Sequence[object], int]],
    base: Vector,
    residual: Vector,
    basis: Sequence[Vector],
) -> tuple[tuple[int, ...], ...]:
    """Return Dq_base(step)=-q(base) in coordinates on ``basis``."""

    derivative_columns = []
    for vector in basis:
        plus = anti.symbolic_second_digits(
            term_data, add(base, vector)
        )
        minus = anti.symbolic_second_digits(
            term_data, add(base, vector, 2)
        )
        # If q(u+t v)=a+b*t+c*t^2, then
        # b=(q(u+v)-q(u-v))/2=2*(plus-minus) in F_3.
        derivative_columns.append(tuple(
            2 * (left - right) % MODULUS
            for left, right in zip(plus, minus)
        ))
    return tuple(
        tuple(
            derivative_columns[column][row]
            for column in range(len(basis))
        ) + ((-residual[row]) % MODULUS,)
        for row in range(20)
    )


def original_chart_memberships(
    coordinates: Sequence[tuple[int, int, int]],
    point: Vector,
) -> tuple[tuple[Direction, Direction], ...]:
    """Find the certified rank-one charts containing a pinned point."""

    memberships = []
    for direction_a in anti.nonconstant_row_directions():
        for direction_b in anti.nonconstant_row_directions():
            features = anti.chart(
                direction_a, direction_b
            ).feature_matrix(coordinates)
            equations = tuple(
                tuple(row) + (point[index],)
                for index, row in enumerate(features)
            )
            if anti.structured.canonical_solution(equations, 24) is not None:
                memberships.append((direction_a, direction_b))
    return tuple(memberships)


def histogram(counter: Counter[int]) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter)}


def source_audit_record(profile: str) -> dict[str, object]:
    stored = json.loads(
        (ANTI_TENSOR / "anti_tensor_family_certificate.json").read_text()
    )
    if stored["full_semantic_sha256"] != anti.EXPECTED_SEMANTIC_SHA256:
        raise AssertionError("source anti-tensor certificate hash changed")
    for record in stored["profiles"]:
        if record["profile"] == profile:
            return record
    raise AssertionError(f"source audit lost profile {profile}")


def audit_profile(profile: str) -> dict[str, object]:
    candidate = next(
        candidate for candidate in anti.CANDIDATES
        if candidate[0] == profile
    )
    profiles = anti.profiles_from_ids(candidate[3], candidate[4])
    coordinates = anti.active_trit_coordinates(profiles)
    equations = anti.first_digit_equations(profiles)
    augmented = anti.augmented_system(equations)
    coefficient_rows = tuple(row[:-1] for row in augmented)
    term_data = anti.second_digit_term_data(profiles)
    directions = all_row_directions()

    chart_spaces = []
    image_dimension_histogram: Counter[int] = Counter()
    correction_union: set[Vector] = set()
    chart_records = []
    for direction_a in directions:
        for direction_b in directions:
            features = correction_features(
                coordinates, direction_a, direction_b
            )
            basis = correction_image_basis(coefficient_rows, features)
            image_dimension_histogram[len(basis)] += 1
            chart_corrections = tuple(
                anti.structured.affine_points((0,) * TRIT_COUNT, basis)
            )
            correction_union.update(chart_corrections)
            chart_records.append({
                "directions": (direction_a, direction_b),
                "image_dimension": len(basis),
                "basis_packed_sha256": packed_hash(tuple(basis)),
            })

    corrections = tuple(sorted(correction_union))
    bases = PINNED_BASES[profile]
    source = source_audit_record(profile)
    source_histogram = source["second_digit_zero_row_histogram"]
    if int(source["maximum_second_digit_zero_rows"]) != 18:
        raise AssertionError("source profile is no longer an 18/20 near miss")
    if int(source_histogram.get("18", 0)) != len(bases):
        raise AssertionError("pinned near misses no longer exhaust source maximum")

    base_records = []
    for base_index, base in enumerate(bases):
        if len(base) != TRIT_COUNT:
            raise AssertionError("pinned base width changed")
        first = anti.symbolic_first_digits(equations, base)
        direct_first = anti.direct_first_digits(profiles, base)
        residual = anti.symbolic_second_digits(term_data, base)
        direct_residual = anti.direct_second_digits(profiles, base)
        if first != (0,) * 20 or direct_first != first:
            raise AssertionError("pinned near miss failed placement digit one")
        if direct_residual != residual:
            raise AssertionError("pinned near-miss residual replay failed")
        if sum(value == 0 for value in residual) != 18:
            raise AssertionError("pinned point is not an 18/20 near miss")

        memberships = original_chart_memberships(coordinates, base)
        if len(memberships) != 1:
            raise AssertionError("pinned rank-one chart is not unique")

        exact_histogram: Counter[int] = Counter()
        exact_by_score: dict[int, list[Vector]] = {}
        residual_by_correction: dict[Vector, Vector] = {}
        for correction in corrections:
            point = add(base, correction)
            if anti.symbolic_first_digits(equations, point) != (0,) * 20:
                raise AssertionError("corrected point failed placement digit one")
            result = anti.symbolic_second_digits(term_data, point)
            score = sum(value == 0 for value in result)
            exact_histogram[score] += 1
            exact_by_score.setdefault(score, []).append(correction)
            residual_by_correction[correction] = result

        maximum = max(exact_by_score)
        best_corrections = tuple(sorted(exact_by_score[maximum]))
        survivors = tuple(sorted(exact_by_score.get(20, ())))
        if survivors:
            raise AssertionError("a rank-two correction witness was found")

        # Detached direct-Eisenstein replays at deterministic points,
        # including every best correction.
        replay_corrections = {
            corrections[0],
            corrections[len(corrections) // 2],
            corrections[-1],
            *best_corrections,
        }
        for correction in replay_corrections:
            point = add(base, correction)
            if anti.direct_first_digits(profiles, point) != (0,) * 20:
                raise AssertionError("direct corrected digit-one replay failed")
            if anti.direct_second_digits(
                profiles, point
            ) != residual_by_correction[correction]:
                raise AssertionError("direct corrected digit-two replay failed")

        # Solve Dq_u(v)=-q(u) on every first-digit-preserving correction
        # chart.  This is a linearized diagnostic, not the exact exclusion.
        linearized_rank_histogram: Counter[str] = Counter()
        linearized_solvable_charts = 0
        for record, direction_a, direction_b in zip(
            chart_records,
            (
                direction_a
                for direction_a in directions
                for _ in directions
            ),
            (
                direction_b
                for _ in directions
                for direction_b in directions
            ),
        ):
            features = correction_features(
                coordinates, direction_a, direction_b
            )
            basis = correction_image_basis(coefficient_rows, features)
            linearized = linearized_rows(
                term_data, base, residual, basis
            )
            coefficient_rank = anti.structured.matrix_rank(
                tuple(row[:-1] for row in linearized)
            )
            augmented_rank = anti.structured.matrix_rank(linearized)
            key = (
                f"dim={len(basis)},rank={coefficient_rank},"
                f"augmented={augmented_rank}"
            )
            linearized_rank_histogram[key] += 1
            if coefficient_rank == augmented_rank:
                linearized_solvable_charts += 1
            if int(record["image_dimension"]) != len(basis):
                raise AssertionError("chart replay dimension changed")

        if linearized_solvable_charts:
            raise AssertionError("linearized correction obstruction disappeared")

        # Broader diagnostic: permit the quadratic background and the
        # original tensor component to rebalance in every rank-two plane
        # chart containing the unique rank-one chart.  This does not
        # enumerate, solve, or exclude the nonlinear rank-two charts.
        original_directions = memberships[0]
        planes_a = planes_containing(original_directions[0])
        planes_b = planes_containing(original_directions[1])
        full_dimension_histogram: Counter[int] = Counter()
        full_linearized_rank_histogram: Counter[str] = Counter()
        full_solvable_records = []
        full_newton_steps: set[Vector] = set()
        for plane_a_index, plane_a in enumerate(planes_a):
            for plane_b_index, plane_b in enumerate(planes_b):
                features = full_rank_two_features(
                    coordinates, plane_a, plane_b
                )
                basis = correction_image_basis(
                    coefficient_rows, features
                )
                full_dimension_histogram[len(basis)] += 1
                linearized = linearized_rows(
                    term_data, base, residual, basis
                )
                coefficient_rank = anti.structured.matrix_rank(
                    tuple(row[:-1] for row in linearized)
                )
                augmented_rank = anti.structured.matrix_rank(linearized)
                key = (
                    f"dim={len(basis)},rank={coefficient_rank},"
                    f"augmented={augmented_rank}"
                )
                full_linearized_rank_histogram[key] += 1
                if coefficient_rank != augmented_rank:
                    continue

                coefficient_origin = anti.structured.canonical_solution(
                    linearized, len(basis)
                )
                if coefficient_origin is None:
                    raise AssertionError("consistent Newton chart lost origin")
                coefficient_kernel = anti.structured.nullspace_basis(
                    tuple(row[:-1] for row in linearized), len(basis)
                )
                chart_steps = set()
                for coefficients in anti.structured.affine_points(
                    coefficient_origin, coefficient_kernel
                ):
                    step = tuple(
                        sum(
                            coefficients[column] * basis[column][coordinate]
                            for column in range(len(basis))
                        ) % MODULUS
                        for coordinate in range(TRIT_COUNT)
                    )
                    chart_steps.add(step)
                    full_newton_steps.add(step)
                full_solvable_records.append({
                    "plane_indices": (plane_a_index, plane_b_index),
                    "plane_a": plane_a,
                    "plane_b": plane_b,
                    "first_digit_image_dimension": len(basis),
                    "linearized_rank": coefficient_rank,
                    "newton_step_sha256": tuple(
                        compact_hash(step) for step in sorted(chart_steps)
                    ),
                })

        full_newton_score_histogram: Counter[int] = Counter()
        full_newton_survivors = []
        for step in sorted(full_newton_steps):
            point = add(base, step)
            if anti.symbolic_first_digits(equations, point) != (0,) * 20:
                raise AssertionError("full-chart Newton step lost digit one")
            result = anti.symbolic_second_digits(term_data, point)
            score = sum(value == 0 for value in result)
            full_newton_score_histogram[score] += 1
            if score == 20:
                full_newton_survivors.append(step)
        if full_newton_survivors:
            raise AssertionError("a full-chart Newton step became exact")

        base_records.append({
            "base_index": base_index,
            "base_trit_sha256": compact_hash(base),
            "rank_one_chart_membership": memberships,
            "second_digit_residual": residual,
            "missing_rows": tuple(
                index for index, value in enumerate(residual) if value
            ),
            "correction_score_histogram": histogram(exact_histogram),
            "maximum_corrected_zero_rows": maximum,
            "best_correction_count": len(best_corrections),
            "best_correction_sha256": tuple(
                compact_hash(vector) for vector in best_corrections
            ),
            "exact_twenty_row_survivors": len(survivors),
            "linearized_rank_histogram": {
                key: linearized_rank_histogram[key]
                for key in sorted(linearized_rank_histogram)
            },
            "linearized_solvable_charts": linearized_solvable_charts,
            "full_rank_two_charts_through_base": 16,
            "full_rank_two_first_digit_image_dimension_histogram": histogram(
                full_dimension_histogram
            ),
            "full_rank_two_linearized_rank_histogram": {
                key: full_linearized_rank_histogram[key]
                for key in sorted(full_linearized_rank_histogram)
            },
            "full_rank_two_linearized_solvable_charts": len(
                full_solvable_records
            ),
            "full_rank_two_linearized_solvable_chart_records": tuple(
                full_solvable_records
            ),
            "distinct_full_rank_two_newton_steps": len(full_newton_steps),
            "full_rank_two_newton_exact_score_histogram": histogram(
                full_newton_score_histogram
            ),
            "full_rank_two_newton_exact_survivors": len(
                full_newton_survivors
            ),
            "direct_replay_corrections": len(replay_corrections),
        })

    result: dict[str, object] = {
        "profile": profile,
        "projective_correction_charts": len(directions) ** 2,
        "correction_image_dimension_histogram": histogram(
            image_dimension_histogram
        ),
        "chart_records_sha256": compact_hash(chart_records),
        "first_digit_preserving_correction_incidences": sum(
            count * MODULUS ** dimension
            for dimension, count in image_dimension_histogram.items()
        ),
        "distinct_first_digit_preserving_corrections": len(corrections),
        "correction_union_packed_sha256": packed_hash(corrections),
        "bases": tuple(base_records),
    }

    if profile == "h2-422220-2":
        difference = add(bases[0], bases[1], 2)
        # add(u0,u1,2)=u0-u1, so negate once to obtain u1-u0.
        difference = tuple(-value % MODULUS for value in difference)
        if add(bases[0], difference) != bases[1]:
            raise AssertionError("near-miss secant relation changed")
        third = add(bases[0], difference, 2)
        third_residual = anti.symbolic_second_digits(term_data, third)
        result["near_miss_secant"] = {
            "difference_sha256": compact_hash(difference),
            "difference_is_allowed_correction": difference in correction_union,
            "third_point_zero_rows": sum(
                value == 0 for value in third_residual
            ),
            "third_point_residual": third_residual,
            "same_unique_rank_one_chart": (
                base_records[0]["rank_one_chart_membership"]
                == base_records[1]["rank_one_chart_membership"]
            ),
        }
        if not result["near_miss_secant"]["difference_is_allowed_correction"]:
            raise AssertionError("near-miss secant left correction union")
        if not result["near_miss_secant"]["same_unique_rank_one_chart"]:
            raise AssertionError("near misses no longer share one rank-one chart")

    return result


def build_certificate() -> dict[str, object]:
    audits = tuple(
        audit_profile(profile)
        for profile in ("h2-422220-2", "h2-422220-3")
    )
    return {
        "schema": "lp333-anti-tensor-local-rank-two-correction-v1",
        "scope": (
            "Exact fixed-background secant audit at the three certified "
            "18/20 rank-one anti-tensor near misses."
        ),
        "correction_family": (
            "v_X(j,s)=h_j F_X(j mod 6)G_X(s), with each G_X ranging "
            "over all 13 projective row directions and F_X arbitrary."
        ),
        "projective_row_directions": all_row_directions(),
        "projective_row_direction_sha256": compact_hash(
            all_row_directions()
        ),
        "audits": audits,
        "totals": {
            "profiles": len(audits),
            "near_miss_bases": sum(
                len(audit["bases"]) for audit in audits
            ),
            "projective_charts": sum(
                int(audit["projective_correction_charts"])
                for audit in audits
            ),
            "distinct_correction_base_incidents": sum(
                int(audit["distinct_first_digit_preserving_corrections"])
                * len(audit["bases"])
                for audit in audits
            ),
            "exact_twenty_row_survivors": sum(
                int(base["exact_twenty_row_survivors"])
                for audit in audits
                for base in audit["bases"]
            ),
            "linearized_solvable_charts": sum(
                int(base["linearized_solvable_charts"])
                for audit in audits
                for base in audit["bases"]
            ),
        },
        "claim_boundary": {
            "exact": (
                "No first-digit-preserving separable correction of the "
                "displayed form, added to any pinned base while holding "
                "its background and first tensor component fixed, solves "
                "all twenty second-digit equations."
            ),
            "local": (
                "This excludes the 169-chart correction star at three "
                "near misses, not the complete rank-at-most-two family."
            ),
            "linearized": (
                "The Newton systems are inconsistent on every correction "
                "chart; this is diagnostic and is not used to infer the "
                "exact exclusion."
            ),
            "full_rank_two_diagnostic": (
                "The 16 rebalanced rank-two charts through each base are "
                "tested only at the linearized Newton level. Solvable "
                "linearizations and their finitely many Newton steps are "
                "recorded, but no nonlinear chart is excluded."
            ),
            "lp333": "No Legendre pair of length 333 is constructed or excluded.",
            "h668": "No Hadamard matrix of order 668 is constructed or excluded.",
        },
    }


def main() -> None:
    certificate = build_certificate()
    semantic_hash = compact_hash(certificate)
    if EXPECTED_SEMANTIC_SHA256 and semantic_hash != EXPECTED_SEMANTIC_SHA256:
        raise AssertionError(
            "anti-tensor correction semantic certificate changed: "
            f"{semantic_hash}"
        )
    print(
        "PASS anti-tensor rank-two correction audit "
        f"hash={semantic_hash} "
        f"exact={certificate['totals']['exact_twenty_row_survivors']} "
        f"linearized={certificate['totals']['linearized_solvable_charts']}"
    )
    for audit in certificate["audits"]:
        print(
            f"{audit['profile']}: "
            f"corrections={audit['distinct_first_digit_preserving_corrections']} "
            f"dimensions={audit['correction_image_dimension_histogram']}"
        )
        for base in audit["bases"]:
            print(
                f"  base={base['base_index']} "
                f"best={base['maximum_corrected_zero_rows']}/20 "
                f"survivors={base['exact_twenty_row_survivors']} "
                f"linearized={base['linearized_solvable_charts']}"
            )


if __name__ == "__main__":
    main()
