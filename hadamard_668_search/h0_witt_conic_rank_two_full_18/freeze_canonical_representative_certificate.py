#!/usr/bin/env python3
"""Freeze the completed census on the 18 canonical representative gauges.

Five records come from the frozen dimension-gated v1 certificate and
thirteen records come from the atomic continuation results.  The resulting
certificate is detached: every mathematical record and survivor assignment
is embedded, so later verification does not depend on the ignored production
output directory.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import argparse
import json
import os
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
LEGACY_DIR = SEARCH / "h0_witt_conic_rank_two_all_orbits"
LEGACY_CERTIFICATE = LEGACY_DIR / "all_orbit_rank_two_certificate.json"
LEGACY_VERIFIER = LEGACY_DIR / "verify_all_orbit_rank_two.py"
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
BASE_VERIFIER = (
    SEARCH
    / "h0_witt_conic_rank_two_orbit07"
    / "verify_witt_conic_rank_two.py"
)
RUNNER = HERE / "run_deferred_rank_two.py"
ACTION_VERIFIER = HERE / "verify_action_noninvariance.py"
ACTION_CERTIFICATE = HERE / "ACTION_NONINVARIANCE_CERTIFICATE.json"
OUTPUT = HERE / "output" / "production"
CERTIFICATE = HERE / "canonical_18_rank_two_certificate.json"

sys.path[:0] = [str(HERE), str(LEGACY_DIR)]

import run_deferred_rank_two as runner  # noqa: E402
import verify_all_orbit_rank_two as rank_two  # noqa: E402


SAFE_LABELS = (
    "orbit-05",
    "orbit-07",
    "orbit-09",
    "orbit-14",
    "orbit-17",
)
DEFERRED_LABELS = runner.DEFERRED_LABELS
ALL_LABELS = tuple(f"orbit-{index:02d}" for index in range(1, 19))
EXPECTED_HASHES = {
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


def validate_self_hash(value: dict[str, object], name: str) -> None:
    if semantic_sha256(value) != value["semantic_sha256"]:
        raise AssertionError(f"{name}: semantic self-hash failed")


def distribution(values: list[int]) -> dict[str, int]:
    return {
        str(key): count
        for key, count in sorted(Counter(values).items())
    }


def frozen_hashes() -> dict[str, str]:
    hashes = {
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
    if hashes != EXPECTED_HASHES:
        raise AssertionError(f"frozen census inputs changed: {hashes}")
    return hashes


def replay_dependency_hashes() -> dict[str, str]:
    """Pin every loaded project-local Python source used by the replay."""
    result = {}
    for module in tuple(sys.modules.values()):
        raw_path = getattr(module, "__file__", None)
        if not raw_path:
            continue
        path = Path(raw_path).resolve()
        if path.suffix != ".py":
            continue
        try:
            relative = path.relative_to(SEARCH)
        except ValueError:
            continue
        result[str(relative)] = file_sha256(path)
    required = {
        "h0_witt_conic_rank_one/verify_witt_conic_rank_one.py",
        "phase_second_digit/verify_phase_second_digit.py",
        "verify_lp333_order3_phase_hensel.py",
        "verify_lp333_order3_phase_transfer.py",
        "verify_lp333_order3_labeled_jet.py",
        "verify_lp333_order3_trit_lift.py",
    }
    missing = required - set(result)
    if missing:
        raise AssertionError(
            f"transitive replay dependencies were not loaded: {missing}"
        )
    return dict(sorted(result.items()))


def validate_legacy_certificate(
    legacy: dict[str, object],
) -> dict[str, dict[str, object]]:
    if legacy["schema"] != "h668-h0-witt-conic-rank-two-all-orbits-v1":
        raise AssertionError("legacy certificate schema changed")
    validate_self_hash(legacy, "legacy certificate")
    records = {
        record["profile"]["label"]: record
        for record in legacy["orbits"]
    }
    if tuple(sorted(records)) != ALL_LABELS:
        raise AssertionError("legacy certificate profile set changed")
    for label in SAFE_LABELS:
        pilot = records[label]["pilot"]
        if pilot["status"] != "EXHAUSTIVE":
            raise AssertionError(f"{label}: safe legacy record not exhaustive")
        if int(pilot["exact_second_digit_survivors"]) != 0:
            raise AssertionError(f"{label}: legacy outcome changed")
    return records


def load_atomic_results() -> tuple[
    dict[str, dict[str, object]],
    dict[str, dict[str, object]],
]:
    expected_inputs = runner.input_hashes()
    results = {}
    provenance = {}
    for label in DEFERRED_LABELS:
        path = OUTPUT / f"{label}.json"
        stored = runner.validate_result(path, label, expected_inputs)
        results[label] = stored["record"]
        provenance[label] = {
            "source_result_path": str(path.relative_to(SEARCH)),
            "source_result_file_sha256": file_sha256(path),
            "source_result_semantic_sha256": stored["semantic_sha256"],
            "source_result_schema": stored["schema"],
            "source_result_inputs": stored["inputs"],
            "runtime": stored["runtime"],
        }
    return results, provenance


def build_certificate() -> dict[str, object]:
    hashes = frozen_hashes()
    legacy = json.loads(LEGACY_CERTIFICATE.read_text())
    legacy_records = validate_legacy_certificate(legacy)
    continued_records, result_provenance = load_atomic_results()
    classification, profiles, scanned = rank_two.load_inputs()
    profile_by_label = {
        str(record["label"]): record for record in profiles
    }

    action_certificate = json.loads(ACTION_CERTIFICATE.read_text())
    validate_self_hash(action_certificate, "action certificate")
    if action_certificate["census"][
        "noncanonical_action_images_not_enumerated"
    ] != 342:
        raise AssertionError("action scope gap changed")

    merged_records = []
    dimensions = []
    denominators = []
    exact_survivors = 0
    consecutive_survivors = 0
    margin_survivors = 0
    consecutive_and_margin_survivors = 0
    survivor_defects = []
    survivor_labels = []

    for label in ALL_LABELS:
        record = (
            legacy_records[label]
            if label in SAFE_LABELS
            else continued_records[label]
        )
        profile = profile_by_label[label]
        expected_profile = {
            "label": profile["label"],
            "digest": profile["production_digest"],
            "ids_a": profile["profile_ids_a"],
            "ids_b": profile["profile_ids_b"],
            "target": profile["target"],
            "classification_record_sha256": profile["record_sha256"],
            "compatible_catalog_rows": scanned[
                profile["production_digest"]
            ]["row_margin_transfer"]["compatible_catalog_rows"],
            "accepted_raw_assignments": scanned[
                profile["production_digest"]
            ]["row_margin_transfer"]["accepted_raw_assignments"],
        }
        if record["profile"] != expected_profile:
            raise AssertionError(f"{label}: profile provenance changed")
        _, replayed_quotient, _ = rank_two.prepare_quotient(profile)
        if record["quotient"] != replayed_quotient:
            raise AssertionError(f"{label}: quotient replay changed")
        pilot = record["pilot"]
        quotient = record["quotient"]
        denominator = int(quotient["physical_image_denominator"])
        dimension = int(quotient["physical_image_dimension"])
        if (
            pilot["status"] != "EXHAUSTIVE"
            or int(pilot["coverage_numerator"]) != denominator
            or int(pilot["coverage_denominator"]) != denominator
            or sum(map(int, pilot["score_histogram"].values()))
            != denominator
            or int(pilot["active_second_digit_equations"]) != 18
            or int(pilot["score_histogram"].get("18", 0))
            != int(pilot["exact_second_digit_survivors"])
        ):
            raise AssertionError(f"{label}: census accounting failed")
        survivors = pilot["survivors"]
        if len(survivors) != int(pilot["exact_second_digit_survivors"]):
            raise AssertionError(f"{label}: survivor count changed")
        exact_survivors += len(survivors)
        consecutive_survivors += int(
            pilot["two_consecutive_digit_survivors"]
        )
        margin_survivors += int(
            pilot["margin_compatible_second_digit_survivors"]
        )
        consecutive_and_margin_survivors += int(
            pilot["two_consecutive_and_margin_survivors"]
        )
        for survivor in survivors:
            defect = int(survivor["following_digit_defect"])
            survivor_defects.append(defect)
            survivor_labels.append(label)
            if defect == 0 or survivor["row_margin_catalog_member"]:
                raise AssertionError(
                    f"{label}: unexpected viable survivor"
                )
        dimensions.append(dimension)
        denominators.append(denominator)
        merged_records.append(record)

    if (
        len(merged_records),
        sum(denominators),
        exact_survivors,
        consecutive_survivors,
        margin_survivors,
        consecutive_and_margin_survivors,
    ) != (18, 3_663_754_254, 7, 0, 0, 0):
        raise AssertionError("full canonical census totals changed")
    expected_dimension_distribution = {
        "14": 1,
        "16": 4,
        "17": 6,
        "18": 7,
    }
    if distribution(dimensions) != expected_dimension_distribution:
        raise AssertionError("canonical dimension distribution changed")
    expected_defect_distribution = {
        "10": 2,
        "11": 1,
        "13": 2,
        "14": 2,
    }
    if distribution(survivor_defects) != expected_defect_distribution:
        raise AssertionError("following-digit defect distribution changed")

    runtime_values = [
        item["runtime"] for item in result_provenance.values()
    ]
    deferred_runtime = {
        "wall_seconds_sum": sum(
            float(item["wall_seconds"]) for item in runtime_values
        ),
        "user_seconds_sum": sum(
            float(item["user_seconds"]) for item in runtime_values
        ),
        "system_seconds_sum": sum(
            float(item["system_seconds"]) for item in runtime_values
        ),
        "maximum_resident_set_bytes_max": max(
            int(item["maximum_resident_set_bytes"])
            for item in runtime_values
        ),
        "qualification": (
            "Aggregate of the thirteen continuation records only; the "
            "five legacy-safe runs have no runtime field in the v1 "
            "certificate."
        ),
    }

    certificate: dict[str, object] = {
        "schema": (
            "h668-h0-witt-conic-rank-two-canonical-18-complete-v2"
        ),
        "scope": {
            "statement": (
                "Complete exact quotient census of the "
                "arbitrary-quadratic antipodal rank-at-most-two center "
                "family on exactly the 18 frozen canonical "
                "representative gauges in the dense-shell h=0 "
                "classification."
            ),
            "canonical_representative_gauges": 18,
            "classification_action_orbits": 18,
            "distinct_profiles_in_action_universe": 360,
            "noncanonical_action_images_not_enumerated": 342,
            "action_invariance": False,
            "qualification": (
                "The center-feature law is gauge-dependent. This "
                "certificate makes no second-digit claim for the 342 "
                "other action images and is not an LP(333) or H(668) "
                "exclusion."
            ),
        },
        "inputs": {
            **hashes,
            "classification_path": str(
                CLASSIFICATION.relative_to(SEARCH)
            ),
            "classification_verifier_path": str(
                CLASSIFICATION_VERIFIER.relative_to(SEARCH)
            ),
            "final_scan_path": str(FINAL_SCAN.relative_to(SEARCH)),
            "legacy_verifier_path": str(
                LEGACY_VERIFIER.relative_to(SEARCH)
            ),
            "base_verifier_path": str(BASE_VERIFIER.relative_to(SEARCH)),
            "legacy_certificate_path": str(
                LEGACY_CERTIFICATE.relative_to(SEARCH)
            ),
            "runner_path": str(RUNNER.relative_to(SEARCH)),
            "action_verifier_path": str(
                ACTION_VERIFIER.relative_to(SEARCH)
            ),
            "action_verifier_sha256": file_sha256(ACTION_VERIFIER),
            "action_certificate_path": str(
                ACTION_CERTIFICATE.relative_to(SEARCH)
            ),
            "action_certificate_sha256": file_sha256(
                ACTION_CERTIFICATE
            ),
            "action_certificate_semantic_sha256":
                action_certificate["semantic_sha256"],
            "legacy_certificate_semantic_sha256":
                legacy["semantic_sha256"],
            "replay_dependency_source_sha256":
                replay_dependency_hashes(),
            "atomic_continuation_results": result_provenance,
        },
        "family": {
            **legacy["family"],
            "gauge_dependence_qualification": (
                "The feature evaluation rank is not invariant under the "
                "24-element classification action; see the separately "
                "replayable action certificate."
            ),
        },
        "coverage": {
            "canonical_representatives_total": 18,
            "canonical_representatives_exhausted": 18,
            "canonical_representatives_deferred": 0,
            "canonical_physical_quotient_states_exhausted":
                sum(denominators),
            "canonical_physical_quotient_states_total":
                sum(denominators),
            "canonical_dimension_distribution":
                expected_dimension_distribution,
            "action_universe_distinct_profiles": 360,
            "action_universe_profiles_exhausted": 18,
            "action_universe_profiles_not_enumerated": 342,
            "action_universe_physical_state_workload":
                action_certificate["census"][
                    "physical_quotient_state_workload_across_360_images"
                ],
            "remaining_action_image_physical_state_workload":
                action_certificate["census"][
                    "remaining_342_state_workload_if_enumerated_independently"
                ],
            "action_workload_qualification":
                action_certificate["census"]["workload_qualification"],
        },
        "outcomes_on_18_canonical_representatives": {
            "exact_second_digit_survivors": exact_survivors,
            "two_consecutive_digit_survivors": consecutive_survivors,
            "margin_compatible_second_digit_survivors": margin_survivors,
            "two_consecutive_and_margin_survivors":
                consecutive_and_margin_survivors,
            "survivor_profile_labels": survivor_labels,
            "following_digit_defect_distribution":
                expected_defect_distribution,
            "conclusion": (
                "Seven exact second-digit points occur, but none extends "
                "through the following digit and none belongs to the "
                "exact row-margin catalog."
            ),
        },
        "runtime": {
            "deferred_continuation": deferred_runtime,
            "thread_limit": (
                "OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 "
                "VECLIB_MAXIMUM_THREADS=1"
            ),
        },
        "records": merged_records,
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
        help="atomically freeze the merged canonical-gauge certificate",
    )
    args = parser.parse_args()
    built = build_certificate()
    if args.write_certificate:
        write_atomic(CERTIFICATE, built)
    else:
        pinned = json.loads(CERTIFICATE.read_text())
        validate_self_hash(pinned, "pinned canonical certificate")
        if canonical_json(built) != canonical_json(pinned):
            raise AssertionError("pinned canonical certificate changed")
    outcome = built["outcomes_on_18_canonical_representatives"]
    coverage = built["coverage"]
    print(
        "canonical_states_exhausted="
        f"{coverage['canonical_physical_quotient_states_exhausted']}/"
        f"{coverage['canonical_physical_quotient_states_total']}"
    )
    print(
        "exact_second_digit_survivors="
        f"{outcome['exact_second_digit_survivors']} "
        "two_consecutive_digit_survivors="
        f"{outcome['two_consecutive_digit_survivors']} "
        "margin_compatible_survivors="
        f"{outcome['margin_compatible_second_digit_survivors']}"
    )
    print(
        "scope=18 canonical gauges; "
        "342 noncanonical action images unenumerated"
    )
    print(f"semantic_sha256={built['semantic_sha256']}")
    print("PASS: canonical 18-representative certificate frozen/replayed")


if __name__ == "__main__":
    main()
