#!/usr/bin/env python3
"""Exact linear audit of the rank-two feature law under the 24-action.

The expensive census in this directory used one frozen canonical
representative from each of the 18 dense-shell h=0 action orbits.  This
script checks whether the physical evaluation space of that feature law is
preserved by the classification action.  Only linear ranks are computed;
no placement point is enumerated.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
CLASSIFICATION_DIR = SEARCH / "dense_shell_h0_complete_classification"
LEGACY_DIR = SEARCH / "h0_witt_conic_rank_two_all_orbits"
CLASSIFICATION = CLASSIFICATION_DIR / "certificate.json"
CLASSIFICATION_VERIFIER = (
    CLASSIFICATION_DIR / "verify_h0_complete_classification.py"
)
LEGACY_VERIFIER = LEGACY_DIR / "verify_all_orbit_rank_two.py"
CERTIFICATE = HERE / "ACTION_NONINVARIANCE_CERTIFICATE.json"

sys.path[:0] = [str(CLASSIFICATION_DIR), str(LEGACY_DIR)]

import verify_h0_complete_classification as classification  # noqa: E402
import verify_all_orbit_rank_two as rank_two  # noqa: E402


GROUP_ORDER = 24
EXPECTED_CLASSIFICATION_SHA256 = (
    "d494ae04404185342797b98ab44eb7eb72868d8bc8ceabd4ae2637c695e23fb9"
)
EXPECTED_CLASSIFICATION_VERIFIER_SHA256 = (
    "415f9e46abc3df21a1981a094d2afd3bf3dae7c64eb03d1ce5fdf694b8e7ac69"
)
EXPECTED_LEGACY_VERIFIER_SHA256 = (
    "2ce1dfa5e289454125859e5f563e4ea9635845129a81ab260456964ff4dba27b"
)
EXPECTED_BASE_VERIFIER_SHA256 = (
    "2b9200f4c69bd22ed10eae62e814d0313f6d70f764697f5fd8b048146d880f1c"
)


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_json(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode("ascii")


def semantic_sha256(value: dict[str, object]) -> str:
    payload = {
        key: item
        for key, item in value.items()
        if key != "semantic_sha256"
    }
    return sha256(canonical_json(payload)).hexdigest()


def distribution(values: list[int]) -> dict[str, int]:
    return {
        str(key): count
        for key, count in sorted(Counter(values).items())
    }


def image_sha256(image: tuple[int, ...]) -> str:
    return sha256(canonical_json(list(image))).hexdigest()


def assert_frozen_inputs() -> dict[str, str]:
    hashes = {
        "classification_sha256": file_sha256(CLASSIFICATION),
        "classification_action_verifier_sha256": file_sha256(
            CLASSIFICATION_VERIFIER
        ),
        "legacy_rank_two_verifier_sha256": file_sha256(LEGACY_VERIFIER),
        "base_rank_two_verifier_sha256": file_sha256(
            Path(rank_two.base.__file__)
        ),
    }
    expected = {
        "classification_sha256": EXPECTED_CLASSIFICATION_SHA256,
        "classification_action_verifier_sha256":
            EXPECTED_CLASSIFICATION_VERIFIER_SHA256,
        "legacy_rank_two_verifier_sha256":
            EXPECTED_LEGACY_VERIFIER_SHA256,
        "base_rank_two_verifier_sha256": EXPECTED_BASE_VERIFIER_SHA256,
    }
    if hashes != expected:
        raise AssertionError(
            f"frozen action-audit inputs changed: {hashes}"
        )
    return hashes


def build_certificate() -> dict[str, object]:
    hashes = assert_frozen_inputs()
    source = json.loads(CLASSIFICATION.read_text())
    if source["schema"] != (
        "h668-dense-shell-h0-complete-classification-v1"
    ):
        raise AssertionError("classification schema changed")
    profiles = source["profiles"]
    if len(profiles) != 18:
        raise AssertionError("classification no longer has 18 orbits")
    classification.reconstruct_action()

    orbit_records = []
    global_images: dict[tuple[int, ...], int] = {}
    incidence_dimensions: list[int] = []
    noninvariant_labels = []
    canonical_dimensions = []

    for record in profiles:
        label = str(record["label"])
        joined = tuple(
            map(
                int,
                record["profile_ids_a"] + record["profile_ids_b"],
            )
        )
        images = [
            classification.transform_assignment(joined, group)
            for group in range(GROUP_ORDER)
        ]
        unique_images = tuple(sorted(set(images)))
        stabilizers = [
            group for group, image in enumerate(images)
            if image == joined
        ]
        if (
            joined != unique_images[0]
            or len(unique_images) != int(record["orbit_size"])
            or stabilizers != record["stabilizer_elements"]
            or len(stabilizers) * len(unique_images) != GROUP_ORDER
        ):
            raise AssertionError(f"{label}: action orbit replay failed")
        if classification.sha256_json(
            [list(image) for image in unique_images]
        ) != record["orbit_sha256"]:
            raise AssertionError(f"{label}: action orbit hash changed")

        dimensions_by_group = []
        quotient_sha256_by_group = []
        for group, image in enumerate(images):
            transformed = {
                "label": f"{label}/action-{group:02d}",
                "profile_ids_a": image[:12],
                "profile_ids_b": image[12:],
            }
            _, quotient, _ = rank_two.prepare_quotient(transformed)
            dimension = int(quotient["physical_image_dimension"])
            if int(quotient["physical_image_denominator"]) != 3**dimension:
                raise AssertionError(
                    f"{label}/action-{group:02d}: denominator changed"
                )
            dimensions_by_group.append(dimension)
            incidence_dimensions.append(dimension)
            quotient_sha256_by_group.append(
                sha256(canonical_json(quotient)).hexdigest()
            )
            previous = global_images.setdefault(image, dimension)
            if previous != dimension:
                raise AssertionError(
                    "one physical profile acquired two dimensions"
                )

        dimension_by_image: dict[tuple[int, ...], int] = {}
        groups_by_image: dict[tuple[int, ...], list[int]] = {}
        for group, (image, dimension) in enumerate(
            zip(images, dimensions_by_group, strict=True)
        ):
            dimension_by_image.setdefault(image, dimension)
            groups_by_image.setdefault(image, []).append(group)
        if len(dimension_by_image) != len(unique_images):
            raise AssertionError(f"{label}: image deduplication failed")

        canonical_dimension = dimensions_by_group[0]
        canonical_dimensions.append(canonical_dimension)
        changing_groups = [
            group
            for group, dimension in enumerate(dimensions_by_group)
            if dimension != canonical_dimension
        ]
        invariant = not changing_groups
        if not invariant:
            noninvariant_labels.append(label)
        witness = None
        if changing_groups:
            group = changing_groups[0]
            witness = {
                "group_element": group,
                "canonical_dimension": canonical_dimension,
                "transformed_dimension": dimensions_by_group[group],
                "transformed_image_sha256": image_sha256(images[group]),
                "action_signature": [
                    list(item)
                    for item in classification.action_signature(group)
                ],
            }

        distinct_dimensions = [
            dimension_by_image[image] for image in unique_images
        ]
        orbit_records.append(
            {
                "label": label,
                "classification_record_sha256": record["record_sha256"],
                "classification_orbit_sha256": record["orbit_sha256"],
                "canonical_image_sha256": image_sha256(joined),
                "canonical_physical_image_dimension":
                    canonical_dimension,
                "classification_orbit_size": len(unique_images),
                "stabilizer_order": len(stabilizers),
                "stabilizer_elements": stabilizers,
                "dimension_is_action_invariant": invariant,
                "incidence_dimension_distribution": distribution(
                    dimensions_by_group
                ),
                "distinct_image_dimension_distribution": distribution(
                    distinct_dimensions
                ),
                "dimensions_by_group_element": dimensions_by_group,
                "image_sha256_by_group_element": [
                    image_sha256(image) for image in images
                ],
                "quotient_sha256_by_group_element":
                    quotient_sha256_by_group,
                "first_dimension_change_witness": witness,
                "distinct_images": [
                    {
                        "image_sha256": image_sha256(image),
                        "dimension": dimension_by_image[image],
                        "group_elements": groups_by_image[image],
                    }
                    for image in unique_images
                ],
            }
        )

    if len(global_images) != 360:
        raise AssertionError("classification action no longer has 360 images")
    if len(incidence_dimensions) != 18 * GROUP_ORDER:
        raise AssertionError("action incidence count changed")
    canonical_images = {
        tuple(map(int, record["profile_ids_a"] + record["profile_ids_b"]))
        for record in profiles
    }
    if len(canonical_images) != 18:
        raise AssertionError("canonical representatives are not distinct")
    if not canonical_images <= set(global_images):
        raise AssertionError("canonical images left action universe")
    untested_images = set(global_images) - canonical_images
    if len(untested_images) != 342:
        raise AssertionError("noncanonical action-image gap changed")

    expected_noninvariant = [
        "orbit-02",
        "orbit-04",
        "orbit-05",
        "orbit-08",
        "orbit-10",
        "orbit-17",
    ]
    if noninvariant_labels != expected_noninvariant:
        raise AssertionError(
            f"noninvariant labels changed: {noninvariant_labels}"
        )
    expected_incidence_distribution = {
        "14": 24,
        "15": 8,
        "16": 80,
        "17": 96,
        "18": 224,
    }
    expected_distinct_distribution = {
        "14": 12,
        "15": 8,
        "16": 56,
        "17": 96,
        "18": 188,
    }
    if distribution(incidence_dimensions) != (
        expected_incidence_distribution
    ):
        raise AssertionError("global incidence distribution changed")
    if distribution(list(global_images.values())) != (
        expected_distinct_distribution
    ):
        raise AssertionError("global distinct-image distribution changed")
    action_universe_states = sum(
        3**dimension for dimension in global_images.values()
    )
    canonical_states = sum(3**dimension for dimension in canonical_dimensions)
    remaining_states = action_universe_states - canonical_states
    if (
        action_universe_states,
        canonical_states,
        remaining_states,
    ) != (87_815_310_840, 3_663_754_254, 84_151_556_586):
        raise AssertionError("action-universe workload changed")

    certificate: dict[str, object] = {
        "schema": (
            "h668-h0-witt-conic-rank-two-action-noninvariance-v1"
        ),
        "scope": {
            "statement": (
                "Exact linear-rank audit of the arbitrary-quadratic "
                "antipodal rank-at-most-two feature law on every image "
                "of the 18 dense-shell h=0 representatives under the "
                "24-element classification action."
            ),
            "enumerates_placement_points": False,
            "mathematical_consequence": (
                "The feature law is not invariant under the "
                "classification action: six classification orbits have "
                "more than one physical image dimension. Therefore a "
                "census on the 18 canonical representatives does not "
                "cover the other 342 distinct action images."
            ),
            "not_claimed": (
                "No second-digit outcome is claimed for the 342 "
                "noncanonical action images."
            ),
        },
        "inputs": {
            **hashes,
            "classification_path": str(
                CLASSIFICATION.relative_to(SEARCH)
            ),
            "classification_action_verifier_path": str(
                CLASSIFICATION_VERIFIER.relative_to(SEARCH)
            ),
            "legacy_rank_two_verifier_path": str(
                LEGACY_VERIFIER.relative_to(SEARCH)
            ),
            "base_rank_two_verifier_path": str(
                Path(rank_two.base.__file__).resolve().relative_to(SEARCH)
            ),
        },
        "census": {
            "classification_orbits": 18,
            "action_group_order": GROUP_ORDER,
            "action_incidences": len(incidence_dimensions),
            "distinct_shell_profiles": len(global_images),
            "canonical_representative_gauges_enumerated_elsewhere": 18,
            "noncanonical_action_images_not_enumerated": len(
                untested_images
            ),
            "dimension_invariant_classification_orbits":
                18 - len(noninvariant_labels),
            "dimension_noninvariant_classification_orbits":
                len(noninvariant_labels),
            "dimension_noninvariant_labels": noninvariant_labels,
            "canonical_dimension_distribution": distribution(
                canonical_dimensions
            ),
            "action_incidence_dimension_distribution":
                expected_incidence_distribution,
            "distinct_image_dimension_distribution":
                expected_distinct_distribution,
            "physical_quotient_state_workload_across_360_images":
                action_universe_states,
            "canonical_18_state_workload_enumerated_elsewhere":
                canonical_states,
            "remaining_342_state_workload_if_enumerated_independently":
                remaining_states,
            "workload_qualification": (
                "These are exact per-image quotient-state counts summed "
                "as an enumeration workload. They are not asserted to be "
                "a disjoint union of ambient placement sets."
            ),
            "noncanonical_image_set_sha256": sha256(
                canonical_json(
                    sorted(image_sha256(image) for image in untested_images)
                )
            ).hexdigest(),
            "complete_image_set_sha256": sha256(
                canonical_json(
                    sorted(image_sha256(image) for image in global_images)
                )
            ).hexdigest(),
        },
        "orbits": orbit_records,
    }
    certificate["semantic_sha256"] = semantic_sha256(certificate)
    return certificate


def write_atomic(path: Path, value: dict[str, object]) -> None:
    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        handle.write(rendered)
        handle.flush()
        os.fsync(handle.fileno())
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write-certificate",
        action="store_true",
        help="atomically freeze the exact linear action audit",
    )
    args = parser.parse_args()
    built = build_certificate()
    if args.write_certificate:
        write_atomic(CERTIFICATE, built)
    else:
        pinned = json.loads(CERTIFICATE.read_text())
        if semantic_sha256(pinned) != pinned["semantic_sha256"]:
            raise AssertionError("pinned certificate self-hash failed")
        if canonical_json(built) != canonical_json(pinned):
            raise AssertionError("pinned action certificate changed")
    census = built["census"]
    print(
        "action_images="
        f"{census['distinct_shell_profiles']} "
        "canonical_enumerated="
        f"{census['canonical_representative_gauges_enumerated_elsewhere']} "
        "noncanonical_unenumerated="
        f"{census['noncanonical_action_images_not_enumerated']}"
    )
    print(
        "dimension_noninvariant_labels="
        + ",".join(census["dimension_noninvariant_labels"])
    )
    print(
        "distinct_dimension_distribution="
        + json.dumps(
            census["distinct_image_dimension_distribution"],
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    print(f"semantic_sha256={built['semantic_sha256']}")
    print("PASS: 18x24 action non-invariance audit replayed")


if __name__ == "__main__":
    main()
