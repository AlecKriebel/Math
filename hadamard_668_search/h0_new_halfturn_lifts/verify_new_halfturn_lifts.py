#!/usr/bin/env python3
"""Detached replay of the bounded three-profile half-turn lift certificate.

The verifier reconstructs each exact length-37 profile directly, checks its
complete antisymmetric weight enumerator in two ways (primal enumeration and
the MacWilliams transform of an independently enumerated dual code), and
reruns every digit-two slice named by the certificate.
"""

from __future__ import annotations

from math import comb
import json
from pathlib import Path
import sys
from typing import Sequence

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
EXACT_ROOT = SEARCH_ROOT / "dense_shell_exact_profile_h0"
PHASE_ROOT = SEARCH_ROOT / "phase_second_digit"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(EXACT_ROOT))
sys.path.insert(0, str(PHASE_ROOT))
sys.path.insert(0, str(SEARCH_ROOT))

import search_new_halfturn_lifts as search  # noqa: E402
import verify_phase_second_digit as second  # noqa: E402
import verify_exact_profile_h0 as exact_profile  # noqa: E402
from verify_lp333_order3_phase_transfer import (  # noqa: E402
    catalog_phase_sum_intersection,
)


CERTIFICATE = HERE / "certificate.json"


def json_normalize(value: object) -> object:
    return json.loads(json.dumps(value, sort_keys=True))


def certificate_shell_view(record: dict[str, object]) -> dict[str, object]:
    keys = (
        "signed_anti_words",
        "consistent_slices",
        "odd_rank_histogram",
        "affine_dimension_histogram",
        "digit_two_points",
        "row_margin_compatible_points",
        "digit_three_histogram",
        "minimum_digit_three_defect",
        "full_digit_three_points",
        "anti_coordinate_sha256",
    )
    return {key: record[key] for key in keys}


def exact_profile_replay(record: dict[str, object]) -> None:
    """Directly replay all 37 correlations in integer Eisenstein arithmetic."""

    ids_a = tuple(map(int, record["ids_a"]))  # type: ignore[arg-type]
    ids_b = tuple(map(int, record["ids_b"]))  # type: ignore[arg-type]
    target = tuple(map(int, record["target"]))  # type: ignore[arg-type]
    classes, class_of = exact_profile.cyclotomic_classes((1, 26, 10), 2)
    if len(classes) != 12:
        raise AssertionError("the order-three class system changed")
    compressed = exact_profile.compressed_values(ids_a, ids_b)
    if exact_profile.aggregate(compressed) != target:
        raise AssertionError("the profile aggregate target changed")
    physical = exact_profile.expand_physical(compressed, class_of)
    correlations = exact_profile.physical_correlations(physical)
    if correlations[0] != (167, 0):
        raise AssertionError("the zero-lag correlation changed")
    if correlations[1:] != ((0, 0),) * 36:
        raise AssertionError("a nonzero profile correlation is not zero")
    target_index = exact_profile.TARGETS.index(target)
    digest = exact_profile.production_digest(
        ids_a + ids_b,
        ((0, 0),) * 6,
        target_index,
    )
    if digest != record["digest"]:
        raise AssertionError("the detached production digest changed")
    orbit = {
        exact_profile.transform_assignment(ids_a + ids_b, element)
        for element in range(exact_profile.GROUP_ORDER)
    }
    stabilizer = tuple(
        element
        for element in range(exact_profile.GROUP_ORDER)
        if exact_profile.transform_assignment(
            ids_a + ids_b, element
        )
        == ids_a + ids_b
    )
    if len(orbit) * len(stabilizer) != exact_profile.GROUP_ORDER:
        raise AssertionError("orbit-stabilizer failed")
    if stabilizer != (0, 12):
        raise AssertionError("the profile is not fixed by exactly the half-turn")


def enumerate_code_histogram(
    generator: Sequence[Sequence[int]],
    chunk_size: int = 300_000,
) -> dict[int, int]:
    matrix = np.asarray(generator, dtype=np.int16)
    dimension, length = matrix.shape
    powers = 3 ** np.arange(dimension, dtype=np.int64)
    histogram = np.zeros(length + 1, dtype=np.int64)
    for lower in range(0, 3**dimension, chunk_size):
        numbers = np.arange(
            lower,
            min(lower + chunk_size, 3**dimension),
            dtype=np.int64,
        )
        coefficients = (
            (numbers[:, None] // powers[None, :]) % 3
        ).astype(np.int16)
        words = (coefficients @ matrix) % 3
        histogram += np.bincount(
            np.count_nonzero(words, axis=1),
            minlength=length + 1,
        )
    return {
        weight: int(count)
        for weight, count in enumerate(histogram)
        if int(count)
    }


def macwilliams_primal_histogram(
    dual_histogram: dict[int, int],
    length: int,
    dual_dimension: int,
) -> dict[int, int]:
    """Apply the exact q=3 MacWilliams transform to the dual enumerator."""

    denominator = 3**dual_dimension
    result = {}
    for weight in range(length + 1):
        numerator = 0
        for dual_weight, multiplicity in dual_histogram.items():
            krawtchouk = 0
            for selected in range(
                max(0, weight - (length - dual_weight)),
                min(weight, dual_weight) + 1,
            ):
                krawtchouk += (
                    (-1) ** selected
                    * 2 ** (weight - selected)
                    * comb(dual_weight, selected)
                    * comb(
                        length - dual_weight,
                        weight - selected,
                    )
                )
            numerator += multiplicity * krawtchouk
        if numerator % denominator:
            raise AssertionError("MacWilliams transform was not integral")
        coefficient = numerator // denominator
        if coefficient:
            result[weight] = coefficient
    return result


def independent_weight_enumerator(
    anti_generator: np.ndarray,
) -> dict[int, int]:
    """Enumerate the 3^12 dual and recover the 3^15 primal enumerator."""

    generator_tuple = tuple(
        tuple(map(int, row)) for row in anti_generator.tolist()
    )
    dual_basis = second.nullspace_basis(
        generator_tuple,
        columns=anti_generator.shape[1],
    )
    if len(dual_basis) != anti_generator.shape[1] - anti_generator.shape[0]:
        raise AssertionError("the anti-code dual dimension changed")
    dual_histogram = enumerate_code_histogram(dual_basis)
    return macwilliams_primal_histogram(
        dual_histogram,
        anti_generator.shape[1],
        len(dual_basis),
    )


def verify() -> dict[str, object]:
    certificate = json.loads(CERTIFICATE.read_text())
    if certificate["schema"] != "lp333-new-halfturn-lifts-v1":
        raise AssertionError("unexpected certificate schema")
    semantic_sha256 = certificate.pop("semantic_sha256")
    if search.compact_hash(certificate) != semantic_sha256:
        raise AssertionError("certificate semantic hash changed")

    if len(certificate["profiles"]) != len(search.PROFILE_RECORDS):
        raise AssertionError("the certificate lost a profile")
    replay_records = []
    for source, expected in zip(
        search.PROFILE_RECORDS,
        certificate["profiles"],
    ):
        for key in ("digest", "ids_a", "ids_b", "target"):
            if json_normalize(source[key]) != expected[key]:
                raise AssertionError(f"{source['digest']}: source {key} changed")
        exact_profile_replay(expected)
        data = search.reconstruct_profile(
            source["ids_a"], source["ids_b"]
        )
        if (
            data["first_dimension"],
            len(data["fixed_basis"]),
            len(data["anti_basis"]),
        ) != (36, 21, 15):
            raise AssertionError("the 36=21+15 eigenspace split changed")
        census = search.anti_code_census(data)
        if list(census["shell_weights"]) != expected[
            "selected_shell_weights"
        ]:
            raise AssertionError("the selected shell weights changed")
        if [
            len(census["shell_coordinates"][weight])
            for weight in census["shell_weights"]
        ] != expected["selected_shell_sizes"]:
            raise AssertionError("a selected shell size changed")
        if json_normalize(census["weight_histogram"]) != expected[
            "anti_weight_histogram"
        ]:
            raise AssertionError("the primal anti enumerator changed")
        dual_recovery = independent_weight_enumerator(census["generator"])
        if dual_recovery != census["weight_histogram"]:
            raise AssertionError(
                "the dual MacWilliams anti enumerator disagrees"
            )

        catalog = catalog_phase_sum_intersection(
            source["ids_a"], source["ids_b"]
        )
        allowed_margin_targets = tuple(
            tuple(
                coordinate
                for channel in sums
                for value in channel
                for coordinate in value
            )
            for sums, _ in catalog["phase_sum_corpus"]
        )
        allowed_margin_sums = set(allowed_margin_targets)
        if len(allowed_margin_sums) != expected[
            "exact_row_margin_catalog_size"
        ]:
            raise AssertionError("the exact row-margin catalog changed")

        shell_records = {}
        for weight in census["shell_weights"]:
            actual = search.shell_lift_census(
                data,
                census["shell_coordinates"][weight],
                allowed_margin_sums,
            )
            if json_normalize(
                certificate_shell_view(actual)
            ) != expected["shell_records"][str(weight)]:
                raise AssertionError(
                    f"{source['digest']}: weight-{weight} lift changed"
                )
            if actual["row_margin_compatible_points"] != 0:
                raise AssertionError("a certified shell reached a row margin")
            if actual["full_digit_three_points"] != 0:
                raise AssertionError("a certified shell reached digit three")
            shell_records[str(weight)] = actual
        replay_records.append({
            "digest": source["digest"],
            "profile_exact_all_37_lags": True,
            "eigenspace_dimensions": (21, 15),
            "anti_code_parameters": (
                census["length"],
                census["dimension"],
                census["shell_weights"][0],
            ),
            "dual_macwilliams_check": True,
            "shell_records": shell_records,
        })
    return {
        "schema": "lp333-new-halfturn-lifts-replay-v1",
        "profiles": replay_records,
        "status": (
            "all selected anti shells fail the exact row-margin join "
            "and full digit three"
        ),
    }


def main() -> None:
    result = verify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print(f"semantic_sha256={search.compact_hash(result)}")
    print("PASS")


if __name__ == "__main__":
    main()
