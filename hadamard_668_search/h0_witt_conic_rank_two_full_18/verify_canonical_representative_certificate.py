#!/usr/bin/env python3
"""Detached verifier for the completed 18-canonical-gauge census.

This verifier does not read ``output/`` and does not repeat the
3,663,754,254-point enumeration.  It verifies the frozen provenance and
stream totals, reconstructs every exact quotient, and physically replays all
seven embedded second-digit survivors through the following digit and the
exact row-margin catalog.  It also replays the separate 18x24 action-rank
audit that limits the scope to the 18 chosen gauges.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import resource
import sys

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
LEGACY_DIR = SEARCH / "h0_witt_conic_rank_two_all_orbits"
CERTIFICATE = HERE / "canonical_18_rank_two_certificate.json"
ACTION_CERTIFICATE = HERE / "ACTION_NONINVARIANCE_CERTIFICATE.json"
CLASSIFICATION = (
    SEARCH / "dense_shell_h0_complete_classification" / "certificate.json"
)
CLASSIFICATION_VERIFIER = (
    SEARCH
    / "dense_shell_h0_complete_classification"
    / "verify_h0_complete_classification.py"
)
FINAL_SCAN = (
    SEARCH / "h0_new_orbits_lift_triage" / "FINAL_PRODUCTION_SCAN_18.json"
)
LEGACY_CERTIFICATE = (
    LEGACY_DIR / "all_orbit_rank_two_certificate.json"
)
LEGACY_SCOPE_CORRECTION = LEGACY_DIR / "SCOPE_CORRECTION.json"
LEGACY_VERIFIER = LEGACY_DIR / "verify_all_orbit_rank_two.py"
BASE_VERIFIER = (
    SEARCH
    / "h0_witt_conic_rank_two_orbit07"
    / "verify_witt_conic_rank_two.py"
)
RUNNER = HERE / "run_deferred_rank_two.py"
ACTION_VERIFIER = HERE / "verify_action_noninvariance.py"

sys.path[:0] = [str(HERE), str(LEGACY_DIR)]

import verify_action_noninvariance as action_audit  # noqa: E402
import verify_all_orbit_rank_two as rank_two  # noqa: E402


SAFE_LABELS = {
    "orbit-05",
    "orbit-07",
    "orbit-09",
    "orbit-14",
    "orbit-17",
}
ALL_LABELS = tuple(f"orbit-{index:02d}" for index in range(1, 19))
EXPECTED_SOURCE_HASHES = {
    "classification_sha256":
        "d494ae04404185342797b98ab44eb7eb72868d8bc8ceabd4ae2637c695e23fb9",
    "classification_verifier_sha256":
        "415f9e46abc3df21a1981a094d2afd3bf3dae7c64eb03d1ce5fdf694b8e7ac69",
    "final_scan_sha256":
        "17a1ce10b6b18f22a43fb254fed2aeff824fc43fada75c9d956844437d9dfa06",
    "legacy_verifier_sha256":
        "2ce1dfa5e289454125859e5f563e4ea9635845129a81ab260456964ff4dba27b",
    "base_verifier_sha256":
        "2b9200f4c69bd22ed10eae62e814d0313f6d70f764697f5fd8b048146d880f1c",
    "legacy_certificate_sha256":
        "88eee219d68b4a05fb11631e1ce12fdfdf339f3ea25f735c1343b1e2d1441d95",
    "runner_sha256":
        "9513a9563c8ccf220bda97690559493015dff473d6be2a8186ef7e5c83266161",
}
EXPECTED_ASSIGNMENT_HASHES = {
    "3b21c2cc843d30881c681b083df3aaf31c3e68e0dd1347d2ce2732317a480e6f",
    "3b6cd22272377ce8aafc875e5edb1302b18f4b02ff3646e44ed40f1c60da1cf9",
    "08f51596360e545dd8bcc1e6171ff0f42d18542059f397ff614d9b4e70cfc98c",
    "078fedf40bb23f2c19fd2fc0a2d6aa9b80af3f216767a6a4f1c42e92298d9c15",
    "273dc952dab1c60dd0577505db61f68a2ae769b05072818fe2b692b3e6cfda3a",
    "48f44da4b6acb928b0648b934bb0785a7a9fe57a7a939f603c33e35d56e6aefc",
    "d4ac06dfe4aaf28a1bcec458e04d8e3661744d9719b11e9e92ef494e18925270",
}


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


def verify_source_hashes(certificate: dict[str, object]) -> None:
    actual = {
        "classification_sha256": file_sha256(CLASSIFICATION),
        "classification_verifier_sha256": file_sha256(
            CLASSIFICATION_VERIFIER
        ),
        "final_scan_sha256": file_sha256(FINAL_SCAN),
        "legacy_verifier_sha256": file_sha256(LEGACY_VERIFIER),
        "base_verifier_sha256": file_sha256(BASE_VERIFIER),
        "legacy_certificate_sha256": file_sha256(LEGACY_CERTIFICATE),
        "runner_sha256": file_sha256(RUNNER),
    }
    if actual != EXPECTED_SOURCE_HASHES:
        raise AssertionError(f"frozen source inputs changed: {actual}")
    for key, value in actual.items():
        if certificate["inputs"][key] != value:
            raise AssertionError(f"certificate input hash changed: {key}")
    for path, key in (
        (ACTION_VERIFIER, "action_verifier_sha256"),
        (ACTION_CERTIFICATE, "action_certificate_sha256"),
    ):
        if certificate["inputs"][key] != file_sha256(path):
            raise AssertionError(f"certificate input hash changed: {key}")
    dependencies = certificate["inputs"][
        "replay_dependency_source_sha256"
    ]
    required = {
        "h0_witt_conic_rank_one/verify_witt_conic_rank_one.py",
        "phase_second_digit/verify_phase_second_digit.py",
        "verify_lp333_order3_phase_hensel.py",
        "verify_lp333_order3_phase_transfer.py",
        "verify_lp333_order3_labeled_jet.py",
        "verify_lp333_order3_trit_lift.py",
    }
    if not required <= set(dependencies):
        raise AssertionError("transitive replay dependency set is incomplete")
    for relative, expected_hash in dependencies.items():
        path = SEARCH / relative
        if file_sha256(path) != expected_hash:
            raise AssertionError(
                f"transitive replay dependency changed: {relative}"
            )


def verify_action_scope(certificate: dict[str, object]) -> None:
    pinned = json.loads(ACTION_CERTIFICATE.read_text())
    if semantic_sha256(pinned) != pinned["semantic_sha256"]:
        raise AssertionError("action certificate self-hash failed")
    if pinned["semantic_sha256"] != certificate["inputs"][
        "action_certificate_semantic_sha256"
    ]:
        raise AssertionError("action certificate semantic hash changed")
    rebuilt = action_audit.build_certificate()
    if canonical_json(rebuilt) != canonical_json(pinned):
        raise AssertionError("action certificate linear replay changed")
    if rebuilt["census"][
        "noncanonical_action_images_not_enumerated"
    ] != 342:
        raise AssertionError("canonical-gauge scope gap changed")
    if (
        rebuilt["census"][
            "remaining_342_state_workload_if_enumerated_independently"
        ]
        != 84_151_556_586
    ):
        raise AssertionError("remaining action-image workload changed")


def verify_legacy_scope_correction(
    certificate: dict[str, object],
) -> None:
    correction = json.loads(LEGACY_SCOPE_CORRECTION.read_text())
    if semantic_sha256(correction) != correction["semantic_sha256"]:
        raise AssertionError("legacy scope-correction self-hash failed")
    legacy = correction["legacy_artifact"]
    if (
        legacy["certificate_sha256"] != file_sha256(LEGACY_CERTIFICATE)
        or legacy["verifier_sha256"] != file_sha256(LEGACY_VERIFIER)
        or not legacy["certificate_source_bytes_preserved"]
        or not legacy["verifier_source_bytes_preserved"]
    ):
        raise AssertionError("legacy byte-preservation record changed")
    evidence = correction["evidence"]
    if (
        evidence["action_certificate_sha256"]
        != file_sha256(ACTION_CERTIFICATE)
        or evidence["superseding_certificate_sha256"]
        != file_sha256(CERTIFICATE)
        or evidence["action_certificate_semantic_sha256"]
        != certificate["inputs"][
            "action_certificate_semantic_sha256"
        ]
        or evidence["superseding_certificate_semantic_sha256"]
        != certificate["semantic_sha256"]
    ):
        raise AssertionError("scope-correction evidence changed")
    if (
        correction["correction"][
            "noncanonical_action_images_not_covered"
        ]
        != 342
    ):
        raise AssertionError("legacy corrected scope changed")


def replay_survivor(
    profile: dict[str, object],
    profiles,
    stored: dict[str, object],
    catalog: set[tuple[int, ...]],
) -> None:
    (
        affine_origin_raw,
        affine_basis_raw,
        _,
        _,
        _,
    ) = rank_two.base.rank_one.exact_quadratic_forms(profiles)
    affine_origin = rank_two.base.normalize(
        np.asarray(affine_origin_raw)
    )
    affine_basis = rank_two.base.normalize(
        np.asarray(affine_basis_raw)
    )
    affine_point = rank_two.base.normalize(
        np.asarray(stored["affine_coordinates"], dtype=np.int16)
    )
    replayed = rank_two.survivor_record(
        profile,
        profiles,
        affine_origin,
        affine_basis,
        affine_point,
        catalog,
    )
    if canonical_json(replayed) != canonical_json(stored):
        raise AssertionError(
            f"{profile['label']}: survivor physical replay changed"
        )


def main() -> None:
    certificate = json.loads(CERTIFICATE.read_text())
    if certificate["schema"] != (
        "h668-h0-witt-conic-rank-two-canonical-18-complete-v2"
    ):
        raise AssertionError("canonical certificate schema changed")
    if semantic_sha256(certificate) != certificate["semantic_sha256"]:
        raise AssertionError("canonical certificate self-hash failed")
    verify_source_hashes(certificate)

    legacy = json.loads(LEGACY_CERTIFICATE.read_text())
    if semantic_sha256(legacy) != legacy["semantic_sha256"]:
        raise AssertionError("legacy certificate self-hash failed")
    if legacy["semantic_sha256"] != certificate["inputs"][
        "legacy_certificate_semantic_sha256"
    ]:
        raise AssertionError("legacy certificate semantic hash changed")
    legacy_records = {
        record["profile"]["label"]: record
        for record in legacy["orbits"]
    }

    _, profiles, scanned = rank_two.load_inputs()
    profile_by_label = {
        str(profile["label"]): profile for profile in profiles
    }
    records = certificate["records"]
    if tuple(record["profile"]["label"] for record in records) != (
        ALL_LABELS
    ):
        raise AssertionError("canonical record order changed")
    catalog = set(rank_two.row_sum_catalog())
    if len(catalog) != 1_756:
        raise AssertionError("row-margin catalog changed")

    total_states = 0
    dimensions = []
    exact_survivors = 0
    consecutive_survivors = 0
    margin_survivors = 0
    both_survivors = 0
    survivor_defects = []
    assignment_hashes = set()

    for record in records:
        label = str(record["profile"]["label"])
        profile = profile_by_label[label]
        scan_record = scanned[profile["production_digest"]]
        expected_profile = {
            "label": profile["label"],
            "digest": profile["production_digest"],
            "ids_a": profile["profile_ids_a"],
            "ids_b": profile["profile_ids_b"],
            "target": profile["target"],
            "classification_record_sha256": profile["record_sha256"],
            "compatible_catalog_rows": scan_record[
                "row_margin_transfer"
            ]["compatible_catalog_rows"],
            "accepted_raw_assignments": scan_record[
                "row_margin_transfer"
            ]["accepted_raw_assignments"],
        }
        if record["profile"] != expected_profile:
            raise AssertionError(f"{label}: profile metadata changed")
        reconstructed_profiles, quotient, _ = (
            rank_two.prepare_quotient(profile)
        )
        if quotient != record["quotient"]:
            raise AssertionError(f"{label}: quotient replay changed")
        dimension = int(quotient["physical_image_dimension"])
        denominator = int(quotient["physical_image_denominator"])
        pilot = record["pilot"]
        histogram = {
            int(score): int(count)
            for score, count in pilot["score_histogram"].items()
        }
        if (
            pilot["status"] != "EXHAUSTIVE"
            or int(pilot["coverage_numerator"]) != denominator
            or int(pilot["coverage_denominator"]) != denominator
            or sum(histogram.values()) != denominator
            or max(score for score, count in histogram.items() if count)
            != int(pilot["maximum_active_second_digit_equations"])
            or int(pilot["active_second_digit_equations"]) != 18
            or histogram.get(18, 0)
            != int(pilot["exact_second_digit_survivors"])
        ):
            raise AssertionError(f"{label}: stream accounting changed")

        if label in SAFE_LABELS:
            if canonical_json(record) != canonical_json(
                legacy_records[label]
            ):
                raise AssertionError(
                    f"{label}: legacy exhaustive record changed"
                )
        else:
            provenance = certificate["inputs"][
                "atomic_continuation_results"
            ][label]
            semantic_result = {
                "schema": provenance["source_result_schema"],
                "complete": True,
                "inputs": provenance["source_result_inputs"],
                "record": record,
            }
            if rank_two.compact_hash(semantic_result) != provenance[
                "source_result_semantic_sha256"
            ]:
                raise AssertionError(
                    f"{label}: detached atomic-result hash failed"
                )

        survivors = pilot["survivors"]
        if len(survivors) != int(pilot["exact_second_digit_survivors"]):
            raise AssertionError(f"{label}: survivor count changed")
        for survivor in survivors:
            replay_survivor(
                profile, reconstructed_profiles, survivor, catalog
            )
            assignment_hashes.add(survivor["assignment_sha256"])
            defect = int(survivor["following_digit_defect"])
            survivor_defects.append(defect)
            if defect == 0 or survivor["row_margin_catalog_member"]:
                raise AssertionError(
                    f"{label}: viable survivor unexpectedly appeared"
                )

        total_states += denominator
        dimensions.append(dimension)
        exact_survivors += len(survivors)
        consecutive_survivors += int(
            pilot["two_consecutive_digit_survivors"]
        )
        margin_survivors += int(
            pilot["margin_compatible_second_digit_survivors"]
        )
        both_survivors += int(
            pilot["two_consecutive_and_margin_survivors"]
        )

    if (
        total_states,
        exact_survivors,
        consecutive_survivors,
        margin_survivors,
        both_survivors,
    ) != (3_663_754_254, 7, 0, 0, 0):
        raise AssertionError("canonical outcome totals changed")
    if distribution(dimensions) != {
        "14": 1,
        "16": 4,
        "17": 6,
        "18": 7,
    }:
        raise AssertionError("canonical dimension distribution changed")
    if distribution(survivor_defects) != {
        "10": 2,
        "11": 1,
        "13": 2,
        "14": 2,
    }:
        raise AssertionError("survivor defect distribution changed")
    if assignment_hashes != EXPECTED_ASSIGNMENT_HASHES:
        raise AssertionError("survivor assignment hashes changed")

    outcome = certificate[
        "outcomes_on_18_canonical_representatives"
    ]
    if (
        outcome["exact_second_digit_survivors"],
        outcome["two_consecutive_digit_survivors"],
        outcome["margin_compatible_second_digit_survivors"],
        outcome["two_consecutive_and_margin_survivors"],
    ) != (7, 0, 0, 0):
        raise AssertionError("certificate outcome summary changed")
    verify_action_scope(certificate)
    verify_legacy_scope_correction(certificate)

    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(f"canonical_states_reconciled={total_states}")
    print(
        "survivors_replayed=7 "
        "two_consecutive=0 margin_compatible=0"
    )
    print(
        "scope_replayed=18 canonical gauges; "
        "342 noncanonical action images unenumerated"
    )
    print(f"maximum_resident_set_bytes={rss}")
    print(f"semantic_sha256={certificate['semantic_sha256']}")
    print("PASS: detached canonical census and action scope replayed")


if __name__ == "__main__":
    main()
