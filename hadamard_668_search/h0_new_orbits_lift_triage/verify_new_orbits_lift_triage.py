#!/usr/bin/env python3
"""Independent replay of the new h=0 orbit lift triage certificates."""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import itertools
import json
from pathlib import Path
from random import Random
import sys

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
SECOND = SEARCH / "phase_second_digit"
THEORY = SEARCH / "h0_orbit2_quadric_theory"
sys.path[:0] = [str(HERE), str(THEORY), str(SECOND), str(SEARCH)]

import scan_production_orbit_retractions as scanner  # noqa: E402
import verify_phase_second_digit as second  # noqa: E402
from verify_lp333_order3_labeled_jet import actual_word  # noqa: E402
from verify_lp333_order3_phase_hensel import (  # noqa: E402
    augmented_system,
    canonical_solution,
    first_digit_equations,
    matrix_rank,
    profiles_from_ids,
)
from verify_lp333_order3_phase_transfer import (  # noqa: E402
    catalog_phase_sum_intersection,
    row_sum_catalog,
)
from verify_quadric_character_compression import (  # noqa: E402
    exact_prefix_zero_fibers,
    scalar_value_counts,
)


CERTIFICATE = HERE / "TRIAGE_CERTIFICATE.json"
FINAL_SCAN = HERE / "FINAL_PRODUCTION_SCAN_18.json"
CLASSIFICATION_CERTIFICATE = (
    SEARCH / "dense_shell_h0_complete_classification" / "certificate.json"
)
MANIFOLD = HERE / "C90C_DIGIT3_MANIFOLD_CHECKPOINT.json"
E686_CHECKPOINT = HERE / "E686_PROVISIONAL_DIGIT2_CHECKPOINT.json"
ACTIVE_ROWS = tuple(range(1, 7)) + tuple(range(8, 20))


def digest(value: object) -> str:
    return sha256(
        json.dumps(
            value, separators=(",", ":"), sort_keys=True
        ).encode()
    ).hexdigest()


def rref_mod3(
    matrix: np.ndarray,
) -> tuple[np.ndarray, tuple[int, ...]]:
    work = np.array(matrix, dtype=np.int16) % 3
    row = 0
    pivots = []
    for column in range(work.shape[1]):
        choices = np.flatnonzero(work[row:, column])
        if not len(choices):
            continue
        pivot = row + int(choices[0])
        work[[row, pivot]] = work[[pivot, row]]
        if work[row, column] == 2:
            work[row] = 2 * work[row] % 3
        for other in range(work.shape[0]):
            if other != row and work[other, column]:
                work[other] = (
                    work[other] - work[other, column] * work[row]
                ) % 3
        pivots.append(column)
        row += 1
        if row == work.shape[0]:
            break
    return work, tuple(pivots)


def rank_mod3(matrix: np.ndarray) -> int:
    return len(rref_mod3(matrix)[1])


def nullspace_mod3(matrix: np.ndarray) -> np.ndarray:
    work, pivots = rref_mod3(matrix)
    free = tuple(
        column
        for column in range(work.shape[1])
        if column not in pivots
    )
    basis = []
    for free_column in free:
        vector = np.zeros(work.shape[1], dtype=np.int16)
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -work[row, free_column] % 3
        basis.append(vector)
    return np.array(basis, dtype=np.int16)


def canonical_linear_solution(
    matrix: np.ndarray, rhs: np.ndarray
) -> np.ndarray:
    variables = matrix.shape[1]
    work, pivots = rref_mod3(np.column_stack((matrix, rhs)))
    if variables in pivots:
        raise AssertionError("linear system became inconsistent")
    result = np.zeros(variables, dtype=np.int16)
    for row, pivot in enumerate(pivots):
        result[pivot] = work[row, -1]
    if not np.array_equal(matrix @ result % 3, rhs % 3):
        raise AssertionError("canonical solution failed replay")
    return result


def projective_vectors(dimension: int):
    for first in range(dimension):
        for tail in itertools.product(
            range(3), repeat=dimension - first - 1
        ):
            yield (0,) * first + (1,) + tuple(tail)


def derive_forms(profile: dict[str, object]):
    ids_a = tuple(map(int, profile["ids_a"]))
    ids_b = tuple(map(int, profile["ids_b"]))
    profiles = profiles_from_ids(ids_a, ids_b)
    equations = first_digit_equations(profiles)
    rows = augmented_system(equations)
    coefficients = tuple(row[:-1] for row in rows)
    origin = canonical_solution(rows, 54)
    if origin is None:
        raise AssertionError("first lift became inconsistent")
    basis = second.nullspace_basis(coefficients, columns=54)
    if matrix_rank(coefficients) != 18 or len(basis) != 36:
        raise AssertionError("first rank/nullity changed")
    constants, linears, polars = second.derive_quadratics(
        second.second_digit_term_data(profiles), origin, basis
    )
    active = tuple(
        index
        for index in range(20)
        if (
            constants[index]
            or any(linears[index])
            or any(value for row in polars[index] for value in row)
        )
    )
    if active != ACTIVE_ROWS:
        raise AssertionError("active quadratic rows changed")
    return (
        profiles,
        origin,
        basis,
        np.array([constants[index] for index in active], dtype=np.int16),
        np.array([linears[index] for index in active], dtype=np.int16),
        np.array([polars[index] for index in active], dtype=np.int16),
    )


def structured_forms(
    constants: np.ndarray,
    linears: np.ndarray,
    polars: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    return tuple(
        np.array(
            [
                values[index]
                + values[index + 6]
                + values[index + 12]
                for index in range(6)
            ],
            dtype=np.int16,
        )
        % 3
        for values in (constants, linears, polars)
    )  # type: ignore[return-value]


def evaluate(
    constant: int,
    linear: np.ndarray,
    polar: np.ndarray,
    point: np.ndarray,
) -> int:
    return int(
        (
            constant
            + linear @ point
            + 2 * np.einsum("i,ij,j", point, polar, point)
        )
        % 3
    )


def retraction_audit(
    linears: np.ndarray,
    polars: np.ndarray,
    expected: dict[str, object],
) -> np.ndarray:
    radical = nullspace_mod3(polars.reshape(-1, 36))
    restriction_rank = rank_mod3(linears @ radical.T % 3)
    assert len(radical) == expected[
        "six_form_common_radical_dimension"
    ]
    assert restriction_rank == expected[
        "six_form_linear_restriction_rank"
    ]
    assert restriction_rank < 6

    good_hyperplanes = []
    for normal in projective_vectors(6):
        equation_basis = nullspace_mod3(
            np.array(normal, dtype=np.int16).reshape(1, 6)
        )
        combined_polars = np.einsum(
            "ae,eij->aij", equation_basis, polars
        ) % 3
        combined_linears = equation_basis @ linears % 3
        common = nullspace_mod3(combined_polars.reshape(-1, 36))
        if rank_mod3(combined_linears @ common.T % 3) == 5:
            good_hyperplanes.append(normal)
    assert len(tuple(projective_vectors(6))) == 364
    assert good_hyperplanes == [
        tuple(map(int, normal))
        for normal in expected["five_hyperplane_normals"]
    ]

    subset = tuple(map(int, expected["selected_subset"]))
    selected_polars = polars[list(subset)]
    selected_linears = linears[list(subset)]
    selected_radical = nullspace_mod3(
        selected_polars.reshape(-1, 36)
    )
    assert len(selected_radical) == expected[
        "selected_common_radical_dimension"
    ]
    restriction = selected_linears @ selected_radical.T % 3
    assert rank_mod3(restriction) == len(subset)
    directions = []
    for coordinate in range(len(subset)):
        target = np.zeros(len(subset), dtype=np.int16)
        target[coordinate] = 1
        coefficient = canonical_linear_solution(restriction, target)
        directions.append(coefficient @ selected_radical % 3)
    direction_matrix = np.array(directions, dtype=np.int16).T % 3
    assert not np.any(
        np.einsum(
            "eij,jk->eik", selected_polars, direction_matrix
        )
        % 3
    )
    assert np.array_equal(
        selected_linears @ direction_matrix % 3,
        np.eye(len(subset), dtype=np.int16),
    )
    assert digest(direction_matrix.tolist()) == expected[
        "selected_direction_sha256"
    ]

    maximum = 5 if good_hyperplanes else len(subset)
    assert maximum == expected[
        "maximum_retraction_dimension_in_structured_span"
    ]
    return direction_matrix


def fixed_margin_translation_audit(
    profiles,
    origin,
    basis,
    directions: np.ndarray,
    expected: dict[str, object],
) -> None:
    roots = ((1, 0), (0, 1), (-1, -1))
    entries = second.phase_entries(profiles)
    character_rows = []
    for channel in range(2):
        for residue in range(3):
            grouped: dict[tuple[int, ...], list[int]] = defaultdict(
                lambda: [0, 0]
            )
            for column in range(37):
                entry = entries[channel][column][residue]
                if entry is None or entry.variable is None:
                    continue
                variable = int(entry.variable)
                exponent = (
                    entry.constant + entry.slope * origin[variable]
                ) % 3
                slope = tuple(
                    entry.slope * basis[index][variable] % 3
                    for index in range(36)
                )
                root = roots[exponent]
                grouped[slope][0] += entry.sign * root[0]
                grouped[slope][1] += entry.sign * root[1]
            character_rows.extend(
                slope
                for slope, coefficient in grouped.items()
                if coefficient != [0, 0] and any(slope)
            )
    matrix = np.array(character_rows, dtype=np.int16)
    rank = rank_mod3(matrix)
    responses = [
        int(np.count_nonzero(matrix @ directions[:, index] % 3))
        for index in range(directions.shape[1])
    ]
    assert len(character_rows) == expected[
        "nonzero_affine_fourier_characters"
    ]
    assert rank == expected["translation_invariance_rank"] == 36
    assert 36 - rank == expected["translation_invariance_dimension"] == 0
    assert responses == expected[
        "selected_direction_nonzero_character_responses"
    ]


def labelled_aggregate(
    masks_a: tuple[int, ...], masks_b: tuple[int, ...]
) -> tuple[int, ...]:
    words = tuple(
        tuple(
            actual_word(channel, class_index, masks[class_index])
            for class_index in range(12)
        )
        for channel, masks in enumerate((masks_a, masks_b))
    )
    aggregate = []
    for row in range(9):
        plus_a = sum(word[row] for word in words[0])
        plus_b = sum(word[row] for word in words[1])
        aggregate.extend((plus_a + plus_b - 12, plus_b - plus_a))
    return tuple(aggregate)


def verify_profile(label: str, stored: dict[str, object]) -> dict[str, object]:
    (
        profiles,
        origin,
        basis,
        constants,
        linears,
        polars,
    ) = derive_forms(stored)
    first = stored["first_layer"]
    second_layer = stored["second_layer"]
    assert digest(origin) == first["origin_sha256"]
    assert digest(basis) == first["basis_sha256"]
    assert digest(constants.tolist()) == second_layer["constants_sha256"]
    assert digest(linears.tolist()) == second_layer["linears_sha256"]
    assert digest(polars.tolist()) == second_layer["polars_sha256"]

    polar_ranks = tuple(rank_mod3(matrix) for matrix in polars)
    actual_histogram = {
        str(rank): count
        for rank, count in sorted(Counter(polar_ranks).items())
    }
    assert actual_histogram == second_layer["polar_rank_histogram"]
    flattened = np.array(
        [
            [
                polars[equation, left, right]
                for left in range(36)
                for right in range(left, 36)
            ]
            for equation in range(18)
        ],
        dtype=np.int16,
    )
    assert rank_mod3(flattened) == second_layer[
        "quadratic_span_rank"
    ]

    g_constants, g_linears, g_polars = structured_forms(
        constants, linears, polars
    )
    exceptions = 0
    zero_numerator = 3**36
    for coordinates in projective_vectors(6):
        coefficient = np.array(coordinates, dtype=np.int16)
        polar = np.einsum("e,eij->ij", coefficient, g_polars) % 3
        linear = coefficient @ g_linears % 3
        polar_rank = rank_mod3(polar)
        augmented_rank = rank_mod3(
            np.column_stack((polar, linear))
        )
        if augmented_rank == polar_rank:
            counts, replayed_rank, balanced = scalar_value_counts(
                int(coefficient @ g_constants % 3), linear, polar
            )
            assert replayed_rank == polar_rank and not balanced
            zero_numerator += 3 * counts[0] - 3**36
            exceptions += 1
        else:
            assert augmented_rank == polar_rank + 1
    structured = stored["structured"]
    assert exceptions == structured["exceptional_projective_lines"]
    assert zero_numerator % 3**6 == 0
    assert zero_numerator // 3**6 == structured[
        "six_equation_zero_fiber"
    ]
    directions = retraction_audit(g_linears, g_polars, structured)
    fixed_margin_translation_audit(
        profiles,
        origin,
        basis,
        directions,
        stored["fixed_row_margin_interaction"],
    )

    prefix_counts = exact_prefix_zero_fibers(
        g_constants,
        g_linears,
        g_polars,
        constants,
        linears,
        polars,
    )
    assert prefix_counts == {
        int(key): int(value)
        for key, value in stored["exact_prefix_zero_fibers"].items()
    }

    transfer = catalog_phase_sum_intersection(
        stored["ids_a"], stored["ids_b"]
    )
    expected_transfer = stored["row_margin_transfer"]
    assert transfer["catalog_rows"] == expected_transfer["catalog_rows"]
    assert transfer["compatible_catalog_rows"] == expected_transfer[
        "compatible_catalog_rows"
    ]
    assert transfer["accepted_assignments"] == expected_transfer[
        "accepted_raw_assignments"
    ]
    assert transfer["phase_sum_corpus_sha256"] == expected_transfer[
        "phase_sum_corpus_sha256"
    ]

    witness = stored["digit2_witness"]
    affine = tuple(map(int, witness["affine_coordinates"]))
    placement = second.lift_affine_point(origin, basis, affine)
    assert digest(placement) == witness["placement_trits_sha256"]
    first_values = second.symbolic_first_digits(
        first_digit_equations(profiles), placement
    )
    symbolic_second = second.symbolic_second_digits(
        second.second_digit_term_data(profiles), placement
    )
    direct_second = second.direct_second_digits(profiles, placement)
    assert first_values == symbolic_second == direct_second == (0,) * 20
    values = second.displayed_values(profiles, placement)
    digits = tuple(second.lambda_digits(value, 12) for value in values)
    counts = tuple(
        sum(row[digit] != 0 for row in digits) for digit in range(12)
    )
    assert digest(values) == witness["displayed_values_sha256"]
    assert counts == tuple(witness["nonzero_rows_by_digit"])
    masks_a, masks_b = second.masks_from_trits(profiles, placement)
    assert digest((masks_a, masks_b)) == witness["masks_sha256"]
    aggregate = labelled_aggregate(masks_a, masks_b)
    assert aggregate == tuple(witness["row_margin_aggregate"])
    member = aggregate in row_sum_catalog()
    assert member is witness["row_margin_catalog_member"] is False

    rng = Random(668_360 + sum(map(ord, label)))
    for _ in range(16):
        point = np.array(
            [rng.randrange(3) for _ in range(36)], dtype=np.int16
        )
        algebraic = tuple(
            evaluate(
                int(constants[index]),
                linears[index],
                polars[index],
                point,
            )
            for index in range(18)
        )
        lifted = second.lift_affine_point(
            origin, basis, tuple(map(int, point))
        )
        physical = second.symbolic_second_digits(
            second.second_digit_term_data(profiles), lifted
        )
        assert physical[0] == physical[7] == 0
        assert algebraic == tuple(
            physical[index] for index in ACTIVE_ROWS
        )
    return {
        "digit2_witness": "PASS",
        "digit3_defect": counts[3],
        "row_margin_catalog_member": member,
        "random_quadratic_replays": 16,
    }


def complete_classification_records() -> dict[str, dict[str, object]]:
    certificate = json.loads(CLASSIFICATION_CERTIFICATE.read_text())
    assert certificate["schema"] == (
        "h668-dense-shell-h0-complete-classification-v1"
    )
    assert len(certificate["profiles"]) == 18
    census = certificate["census"]
    provenance = {
        "aggregate_schema": "dense-shell-production-aggregate-v2",
        "aggregate_file_sha256": census["aggregate_file_sha256"],
        "source_sha256": census["source_sha256"],
        "binary_sha256": census["binary_sha256"],
        "prefix_shards": census["prefix_shards"],
        "upper_exact_scope": census["upper_exact_scope"],
    }
    records = {}
    for stored in certificate["profiles"]:
        record = {
            "digest": stored["production_digest"],
            "ids_a": tuple(map(int, stored["profile_ids_a"])),
            "ids_b": tuple(map(int, stored["profile_ids_b"])),
            "target": tuple(map(int, stored["target"])),
            "target_index": int(stored["target_index"]),
            "source_shards": tuple(stored["source_shards"]),
            "production": provenance,
        }
        if record["digest"] in records:
            raise AssertionError("classification digest repeated")
        records[record["digest"]] = record
    return records


def normalized_json(value: object) -> object:
    return json.loads(json.dumps(value, sort_keys=True))


def verify_final_scan() -> dict[str, object]:
    snapshot = json.loads(FINAL_SCAN.read_text())
    assert snapshot["schema"] == (
        "h668-production-orbit-lift-retraction-scan-v1"
    )
    assert len(snapshot["orbits"]) == snapshot["exact_orbits"] == 18
    current = complete_classification_records()
    assert set(current) == {
        stored["digest"] for stored in snapshot["orbits"]
    }

    maximum_retraction = 0
    maximum_transfer = 0
    maximum_exceptions = 0
    for stored in snapshot["orbits"]:
        audited = scanner.audit_record(
            current[stored["digest"]], transfer=True
        )
        assert normalized_json(audited) == stored
        assert stored["first_layer"]["rank"] == 18
        assert stored["first_layer"]["nullity"] == 36
        second_layer = stored["second_layer"]
        assert second_layer["equations"] == 18
        assert sum(second_layer["polar_rank_histogram"].values()) == 18
        assert second_layer["quadratic_span_rank"] == 18
        characters = stored["structured_characters"]
        assert characters["projective_characters"] == 364
        assert sum(characters["rank_histogram"].values()) == 364
        retraction = stored["structured_retraction"]
        assert retraction["five_hyperplanes_exhausted"] == 364
        transfer = stored["row_margin_transfer"]
        assert transfer["catalog_rows"] == 1756
        maximum_retraction = max(
            maximum_retraction,
            retraction["maximum_retraction_dimension"],
        )
        maximum_transfer = max(
            maximum_transfer, transfer["accepted_raw_assignments"]
        )
        maximum_exceptions = max(
            maximum_exceptions,
            characters["exceptional_projective_lines"],
        )
    return {
        "final_scan_orbits_replayed": len(snapshot["orbits"]),
        "classification_certificate_orbits": len(current),
        "maximum_retraction_dimension": maximum_retraction,
        "maximum_transfer_assignments": maximum_transfer,
        "maximum_exceptional_projective_lines": maximum_exceptions,
    }


def verify_manifold(profile: dict[str, object]) -> dict[str, object]:
    checkpoint = json.loads(MANIFOLD.read_text())
    stored_hash = checkpoint.pop("semantic_sha256")
    assert digest(checkpoint) == stored_hash
    assert checkpoint["status"] == "UNKNOWN"
    assert checkpoint["profile_digest"] == profile["digest"]
    assert checkpoint["best_digit3_defect"] == 6
    assert sum(
        value != 0
        for value in checkpoint[
            "best_digit3_residuals_rows_1_through_19"
        ]
    ) == 6
    assert checkpoint["restoration_successes"] + 1 == checkpoint[
        "distinct_exact_digit2_points"
    ]

    profiles, origin, basis, _, _, _ = derive_forms(profile)
    affine = tuple(map(int, checkpoint["best_affine_coordinates"]))
    placement = second.lift_affine_point(origin, basis, affine)
    replay = checkpoint["best_replay"]
    assert placement == tuple(replay["placement_trits"])
    first = second.symbolic_first_digits(
        first_digit_equations(profiles), placement
    )
    direct_second = second.direct_second_digits(profiles, placement)
    assert first == direct_second == (0,) * 20
    values = second.displayed_values(profiles, placement)
    assert values == tuple(
        tuple(map(int, value)) for value in replay["displayed_exact_values"]
    )
    digits = tuple(second.lambda_digits(value, 12) for value in values)
    counts = tuple(
        sum(row[index] != 0 for row in digits) for index in range(12)
    )
    assert counts == tuple(replay["nonzero_rows_by_digit"])
    # The carry module records A/3; the base-lambda digit uses its negative.
    # They have the same zero set and differ by the unit 2 in F_3.
    assert tuple(2 * row[3] % 3 for row in digits[1:]) == tuple(
        checkpoint["best_digit3_residuals_rows_1_through_19"]
    )
    masks = second.masks_from_trits(profiles, placement)
    assert masks == (
        tuple(replay["masks_a"]),
        tuple(replay["masks_b"]),
    )
    aggregate = labelled_aggregate(*masks)
    assert aggregate == tuple(replay["row_margin_aggregate"])
    assert (aggregate in row_sum_catalog()) is False
    return {
        "status": "UNKNOWN",
        "distinct_exact_digit2_points": checkpoint[
            "distinct_exact_digit2_points"
        ],
        "best_digit3_defect": checkpoint["best_digit3_defect"],
        "semantic_sha256": stored_hash,
    }


def verify_e686_provisional() -> dict[str, object]:
    checkpoint = json.loads(E686_CHECKPOINT.read_text())
    stored_hash = checkpoint.pop("semantic_sha256")
    assert digest(checkpoint) == stored_hash
    assert checkpoint["status"] == "SAT_DIGIT2_ONLY"
    assert checkpoint["profile"]["certification"] == "census-provisional"

    production = checkpoint["production"]
    record = complete_classification_records()[
        checkpoint["profile"]["digest"]
    ]
    assert production["shard_id"] in record["source_shards"]
    assert record["production"]["source_sha256"] == production[
        "source_sha256"
    ]
    assert record["production"]["binary_sha256"] == production[
        "binary_sha256"
    ]
    assert tuple(record["ids_a"]) == tuple(checkpoint["profile"]["ids_a"])
    assert tuple(record["ids_b"]) == tuple(checkpoint["profile"]["ids_b"])
    assert tuple(record["target"]) == tuple(checkpoint["profile"]["target"])

    (
        profiles,
        origin,
        basis,
        constants,
        linears,
        polars,
    ) = derive_forms(checkpoint["profile"])
    g_constants, g_linears, g_polars = structured_forms(
        constants, linears, polars
    )
    subset = tuple(checkpoint["retraction"]["structured_subset"])
    selected_polars = g_polars[list(subset)]
    selected_linears = g_linears[list(subset)]
    radical = nullspace_mod3(selected_polars.reshape(-1, 36))
    assert len(radical) == checkpoint["retraction"][
        "common_radical_dimension"
    ] == 5
    restriction = selected_linears @ radical.T % 3
    assert rank_mod3(restriction) == 5
    directions = []
    for coordinate in range(5):
        target = np.zeros(5, dtype=np.int16)
        target[coordinate] = 1
        coefficients = canonical_linear_solution(restriction, target)
        directions.append(coefficients @ radical % 3)
    direction_matrix = np.array(directions, dtype=np.int16).T % 3
    assert digest(direction_matrix.tolist()) == checkpoint["retraction"][
        "directions_sha256"
    ]
    assert not np.any(
        np.einsum(
            "eij,jk->eik", selected_polars, direction_matrix
        )
        % 3
    )
    assert np.array_equal(
        selected_linears @ direction_matrix % 3,
        np.eye(5, dtype=np.int16),
    )

    witness = checkpoint["best_witness"]
    affine = tuple(map(int, witness["affine_coordinates"]))
    placement = second.lift_affine_point(origin, basis, affine)
    assert placement == tuple(witness["placement_trits"])
    assert digest(placement) == witness["placement_trits_sha256"]
    first = second.symbolic_first_digits(
        first_digit_equations(profiles), placement
    )
    symbolic_second = second.symbolic_second_digits(
        second.second_digit_term_data(profiles), placement
    )
    direct_second = second.direct_second_digits(profiles, placement)
    assert first == symbolic_second == direct_second == (0,) * 20
    values = second.displayed_values(profiles, placement)
    assert values == tuple(
        tuple(map(int, value))
        for value in witness["displayed_exact_values"]
    )
    assert digest(values) == witness["displayed_exact_values_sha256"]
    digits = tuple(second.lambda_digits(value, 12) for value in values)
    counts = tuple(
        sum(row[index] != 0 for row in digits) for index in range(12)
    )
    assert counts == tuple(witness["nonzero_rows_by_digit"])
    assert counts[:3] == (0, 0, 0)
    assert counts[3] == checkpoint["comparison"][
        "e686_best_digit3_defect"
    ] == 10
    masks = second.masks_from_trits(profiles, placement)
    assert masks == (
        tuple(witness["masks_a"]),
        tuple(witness["masks_b"]),
    )
    assert digest(masks) == witness["masks_sha256"]
    aggregate = labelled_aggregate(*masks)
    assert aggregate == tuple(witness["row_margin_aggregate"])
    assert (aggregate in row_sum_catalog()) is witness[
        "row_margin_catalog_member"
    ] is False

    search = checkpoint["search"]
    histogram = {
        int(key): int(value)
        for key, value in search["digit3_defect_histogram"].items()
    }
    assert sum(histogram.values()) == search["digit2_witnesses_found"] == 9
    assert min(histogram) == 10
    assert search["row_margin_catalog_members_found"] == 0
    assert search["cpu_seconds_used"] <= 300
    comparison = checkpoint["comparison"]
    assert comparison["c90c_certified_best_digit3_defect"] == 6
    assert comparison["difference"] == 10 - 6 == 4
    return {
        "status": checkpoint["status"],
        "digit2_witnesses_found": search["digit2_witnesses_found"],
        "best_digit3_defect": counts[3],
        "row_margin_catalog_member": False,
        "semantic_sha256": stored_hash,
    }


def verify() -> dict[str, object]:
    certificate = json.loads(CERTIFICATE.read_text())
    assert certificate["status"] == "PASS"
    profiles = {
        label: verify_profile(label, stored)
        for label, stored in certificate["profiles"].items()
    }
    final_scan = verify_final_scan()
    manifold = verify_manifold(certificate["profiles"]["c90c"])
    e686 = verify_e686_provisional()
    return {
        "e686_provisional": e686,
        "profiles": profiles,
        "final_scan": final_scan,
        "manifold": manifold,
        "status": "PASS",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
    print("PASS: new h=0 orbit lift triage replayed independently")
