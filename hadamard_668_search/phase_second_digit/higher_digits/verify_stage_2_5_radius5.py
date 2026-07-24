#!/usr/bin/env python3
"""Reproduce the exact radius-five digit-2 census around stage 2.5."""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path
import sys

try:
    import numpy as np
except ImportError as error:
    raise SystemExit("NumPy is required for the radius-five census") from error


HERE = Path(__file__).resolve().parent
SECOND_DIGIT = HERE.parent
SEARCH_ROOT = SECOND_DIGIT.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(SECOND_DIGIT))
sys.path.insert(0, str(SEARCH_ROOT))

import solve_full_second_digit_sat as quadratic  # noqa: E402
from verify_lp333_order3_phase_transfer import (  # noqa: E402
    catalog_phase_sum_intersection,
    phase_sums_from_masks,
)


CERTIFICATE = HERE / "stage_2_5_radius5.json"
BATCH_COMBINATIONS = 2048


def quadratic_hits_at_radius(
    radius: int,
    center: np.ndarray,
    gradients: np.ndarray,
    polars: np.ndarray,
) -> tuple[tuple[int, ...], ...]:
    if radius == 0:
        return (tuple(map(int, center)),)
    patterns = np.array(
        tuple(itertools.product((1, 2), repeat=radius)),
        dtype=np.int16,
    )
    pending = []
    hits = []

    def scan(batch) -> None:
        indices = np.array(batch, dtype=np.int16)
        linear = np.einsum(
            "ebr,pr->bpe",
            gradients[:, indices],
            patterns,
            optimize=True,
        )
        restricted = polars[
            :,
            indices[:, :, None],
            indices[:, None, :],
        ]
        values = (
            linear
            + 2
            * np.einsum(
                "ebij,pi,pj->bpe",
                restricted,
                patterns,
                patterns,
                optimize=True,
            )
        ) % 3
        for combination_index, pattern_index in np.argwhere(
            np.all(values == 0, axis=2)
        ):
            displacement = np.zeros(36, dtype=np.int16)
            displacement[indices[combination_index]] = patterns[
                pattern_index
            ]
            hits.append(tuple(map(int, (center + displacement) % 3)))

    for combination in itertools.combinations(range(36), radius):
        pending.append(combination)
        if len(pending) == BATCH_COMBINATIONS:
            scan(pending)
            pending = []
    if pending:
        scan(pending)
    return tuple(hits)


def replay_hit(
    point: tuple[int, ...],
    center: tuple[int, ...],
    profiles,
    origin,
    basis,
    candidate,
) -> dict[str, object]:
    placement = quadratic.second.lift_affine_point(origin, basis, point)
    values = quadratic.second.displayed_values(profiles, placement)
    digits = tuple(
        quadratic.second.lambda_digits(value, 10) for value in values
    )
    masks = quadratic.second.masks_from_trits(profiles, placement)
    phase_sums = phase_sums_from_masks(*masks)
    catalog = catalog_phase_sum_intersection(candidate[3], candidate[4])
    row_margin_join = phase_sums in {
        sums for sums, _ in catalog["phase_sum_corpus"]
    }
    return {
        "hamming_radius": sum(
            left != right for left, right in zip(point, center)
        ),
        "affine_coordinates": point,
        "affine_coordinates_sha256": quadratic.compact_hash(point),
        "placement_trits_sha256": quadratic.compact_hash(placement),
        "digit_nonzero_rows_through_8": tuple(
            sum(row[digit] != 0 for row in digits)
            for digit in range(9)
        ),
        "delayed_e1_origin_digits_through_8": digits[7][:9],
        "phase_sums": phase_sums,
        "row_margin_join_holds": row_margin_join,
    }


def normalize_stored_hit(stored: dict[str, object]) -> dict[str, object]:
    return {
        "hamming_radius": int(stored["hamming_radius"]),
        "affine_coordinates": tuple(map(int, stored["affine_coordinates"])),
        "affine_coordinates_sha256": stored["affine_coordinates_sha256"],
        "placement_trits_sha256": stored["placement_trits_sha256"],
        "digit_nonzero_rows_through_8": tuple(
            stored["digit_nonzero_rows_through_8"]
        ),
        "delayed_e1_origin_digits_through_8": tuple(
            stored["delayed_e1_origin_digits_through_8"]
        ),
        "phase_sums": tuple(
            tuple(tuple(value) for value in channel)
            for channel in stored["phase_sums"]
        ),
        "row_margin_join_holds": bool(stored["row_margin_join_holds"]),
    }


def audit() -> dict[str, object]:
    stored = json.loads(CERTIFICATE.read_text())
    if stored["schema"] != "lp333-order3-stage-2-5-radius-5-v1":
        raise AssertionError("the radius-five schema changed")
    candidate_index = int(stored["candidate_index"])
    candidate = quadratic.second.CANDIDATES[candidate_index]
    if stored["label"] != candidate[0]:
        raise AssertionError("the radius-five profile changed")
    (
        profiles,
        origin,
        basis,
        constants,
        linears,
        polars,
    ) = quadratic.exact_forms(candidate_index)
    expected_hits = tuple(
        normalize_stored_hit(hit) for hit in stored["hits"]
    )
    center_tuple = expected_hits[0]["affine_coordinates"]
    if (
        quadratic.compact_hash(center_tuple)
        != stored["center_affine_coordinates_sha256"]
    ):
        raise AssertionError("the radius-five center changed")
    center = np.array(center_tuple, dtype=np.int16)
    constants = np.array(constants, dtype=np.int16)
    linears = np.array(linears, dtype=np.int16)
    polars = np.array(polars, dtype=np.int16)
    center_values = (
        constants
        + linears @ center
        + 2
        * np.einsum(
            "i,eij,j->e", center, polars, center, optimize=True
        )
    ) % 3
    if np.any(center_values):
        raise AssertionError("the radius-five center lost digit 2")
    gradients = (
        linears
        + np.einsum("eij,j->ei", polars, center, optimize=True)
    ) % 3

    hits_by_radius = []
    all_points = []
    for radius in range(int(stored["maximum_hamming_radius"]) + 1):
        hits = quadratic_hits_at_radius(
            radius, center, gradients, polars
        )
        hits_by_radius.append(len(hits))
        all_points.extend(hits)
    expected_points = tuple(
        math.comb(36, radius) * 2**radius
        for radius in range(6)
    )
    if expected_points != tuple(stored["points_by_exact_radius"]):
        raise AssertionError("the Hamming-ball cardinalities changed")
    if tuple(hits_by_radius) != tuple(
        stored["digit2_hits_by_exact_radius"]
    ):
        raise AssertionError("the radius-five digit-2 census changed")
    replayed = tuple(
        replay_hit(
            point,
            center_tuple,
            profiles,
            origin,
            basis,
            candidate,
        )
        for point in all_points
    )
    if replayed != expected_hits:
        raise AssertionError("a radius-five hit replay changed")
    result = {
        "schema": stored["schema"],
        "total_points": sum(expected_points),
        "digit_2_hits_by_radius": tuple(hits_by_radius),
        "stage_2_5_hits": sum(
            hit["delayed_e1_origin_digits_through_8"][3] == 0
            for hit in replayed
        ),
        "row_margin_compatible_hits": sum(
            hit["row_margin_join_holds"] for hit in replayed
        ),
    }
    if result["total_points"] != int(stored["total_points"]):
        raise AssertionError("the radius-five total changed")
    if result["stage_2_5_hits"] != int(stored["stage_2_5_hits"]):
        raise AssertionError("the local stage-2.5 count changed")
    if result["row_margin_compatible_hits"] != int(
        stored["row_margin_compatible_hits"]
    ):
        raise AssertionError("the local row-margin count changed")
    return result


def main() -> None:
    result = audit()
    print(json.dumps(result, indent=2))
    print(f"semantic_sha256={quadratic.compact_hash(result)}")


if __name__ == "__main__":
    main()
