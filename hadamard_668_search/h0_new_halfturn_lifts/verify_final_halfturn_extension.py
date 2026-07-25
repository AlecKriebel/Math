#!/usr/bin/env python3
"""Verify the final six-profile half-turn catalog and two-profile extension.

The default mode is a lightweight detached catalog/artifact audit.  Passing
``--full-extension`` additionally re-enumerates the complete anti codes and
all two-lowest-shell slices for the two profiles first seen after the v1
certificate was frozen.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
BASELINE_ROOT = SEARCH_ROOT / "h0_minimal_anti_code"
PHASE_ROOT = SEARCH_ROOT / "phase_second_digit"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(BASELINE_ROOT))
sys.path.insert(0, str(PHASE_ROOT))
sys.path.insert(0, str(SEARCH_ROOT))

import search_new_halfturn_lifts as search  # noqa: E402
import verify_h0_minimal_anti_code as baseline  # noqa: E402
import verify_new_halfturn_lifts as v1_verifier  # noqa: E402
from halfturn_profile_catalog import (  # noqa: E402
    profiles_from_strict_aggregate,
)
from verify_lp333_order3_phase_transfer import (  # noqa: E402
    catalog_phase_sum_intersection,
)


CERTIFICATE = HERE / "final_certificate_v2.json"
DEFAULT_AGGREGATE = (
    SEARCH_ROOT
    / "dense_shell_classifier_pilot"
    / "output"
    / "production-v2"
    / "aggregate-h0.json"
)
V1_CERTIFICATE = HERE / "certificate.json"
BASELINE_VERIFIER = BASELINE_ROOT / "verify_h0_minimal_anti_code.py"


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def json_normalize(value: object) -> object:
    return json.loads(json.dumps(value, sort_keys=True))


def shell_summary(record: dict[str, object]) -> dict[str, object]:
    keys = (
        "signed_anti_words",
        "consistent_slices",
        "digit_two_points",
        "row_margin_compatible_points",
        "full_digit_three_points",
        "minimum_digit_three_defect",
    )
    return {key: record[key] for key in keys}


def extended_shell_summary(record: dict[str, object]) -> dict[str, object]:
    keys = (
        "signed_anti_words",
        "consistent_slices",
        "odd_rank_histogram",
        "affine_dimension_histogram",
        "digit_two_points",
        "row_margin_compatible_points",
        "full_digit_three_points",
        "minimum_digit_three_defect",
        "anti_coordinate_sha256",
        "digit_three_histogram",
    )
    return {key: record[key] for key in keys}


def totals_for_profiles(
    profiles: list[dict[str, object]],
) -> dict[str, int]:
    shells = [
        shell
        for profile in profiles
        for shell in profile["shells"].values()  # type: ignore[union-attr]
    ]
    return {
        "signed_anti_words": sum(
            int(shell["signed_anti_words"]) for shell in shells
        ),
        "consistent_slices": sum(
            int(shell["consistent_slices"]) for shell in shells
        ),
        "digit_two_points": sum(
            int(shell["digit_two_points"]) for shell in shells
        ),
        "row_margin_compatible_points": sum(
            int(shell["row_margin_compatible_points"]) for shell in shells
        ),
        "full_digit_three_points": sum(
            int(shell["full_digit_three_points"]) for shell in shells
        ),
        "minimum_digit_three_defect": min(
            int(shell["minimum_digit_three_defect"]) for shell in shells
        ),
    }


def verify_artifact_chain(
    certificate: dict[str, object],
) -> None:
    coverage = certificate["coverage_classes"]
    if not isinstance(coverage, dict):
        raise AssertionError("coverage classes are malformed")
    baseline_record = coverage["original_baseline"]
    v1_record = coverage["prior_three_profile_v1"]
    if file_sha256(BASELINE_VERIFIER) != baseline_record["artifact_sha256"]:
        raise AssertionError("the original baseline verifier changed")
    if file_sha256(V1_CERTIFICATE) != v1_record["artifact_sha256"]:
        raise AssertionError("the v1 certificate file changed")
    v1 = json.loads(V1_CERTIFICATE.read_text(encoding="utf-8"))
    semantic = v1.pop("semantic_sha256")
    if semantic != v1_record["result_semantic_sha256"]:
        raise AssertionError("the recorded v1 semantic hash changed")
    if search.compact_hash(v1) != semantic:
        raise AssertionError("the v1 certificate payload changed")

    # Reconstruct the baseline numerical summary from the frozen verifier's
    # exact expected tables, without rerunning its expensive slice census.
    if (
        len(baseline.EXPECTED_MINIMUM_COORDINATES),
        sum(row["digit_two_points"] for row in baseline.EXPECTED_SLICE_RECORDS),
        len(baseline.EXPECTED_WEIGHT_FIVE_COORDINATES),
        2
        * sum(
            row["digit_two_points"]
            for row in baseline.EXPECTED_WEIGHT_FIVE_RECORDS
        ),
    ) != (6, 266, 7, 392):
        raise AssertionError("the frozen original baseline tables changed")

    v1_by_digest = {
        profile["digest"]: profile for profile in v1["profiles"]
    }
    final_v1 = [
        profile
        for profile in certificate["profiles"]
        if profile["coverage_class"] == "prior_three_profile_v1"
    ]
    if set(v1_by_digest) != {
        profile["digest"] for profile in final_v1
    }:
        raise AssertionError("the v1 profile set changed")
    for profile in final_v1:
        source = v1_by_digest[profile["digest"]]
        for key in ("ids_a", "ids_b", "target", "anti_code_parameters"):
            if source[key] != profile[key]:
                raise AssertionError(
                    f"{profile['digest']}: inherited v1 {key} changed"
                )
        expected_shells = {
            weight: shell_summary(record)
            for weight, record in source["shell_records"].items()
        }
        if expected_shells != profile["shells"]:
            raise AssertionError(
                f"{profile['digest']}: inherited v1 shells changed"
            )


def verify_catalog(
    certificate: dict[str, object],
    aggregate_path: Path,
) -> tuple[dict[str, object], dict[str, dict[str, object]]]:
    catalog = profiles_from_strict_aggregate(aggregate_path)
    aggregate_record = certificate["strict_aggregate"]
    if not isinstance(aggregate_record, dict):
        raise AssertionError("strict aggregate record is malformed")
    expected_counts = (
        aggregate_record["exact_h0_profile_orbits"],
        aggregate_record["halfturn_fixed_profile_orbits"],
    )
    if (
        catalog["all_exact_h0_orbits"],
        catalog["halfturn_fixed_orbits"],
    ) != expected_counts:
        raise AssertionError("the final aggregate profile counts changed")
    if (
        catalog["aggregate_source_sha256"]
        != aggregate_record["source_sha256"]
        or catalog["aggregate_binary_sha256"]
        != aggregate_record["binary_sha256"]
    ):
        raise AssertionError("the final aggregate provenance changed")

    final_profiles = certificate["profiles"]
    if not isinstance(final_profiles, list):
        raise AssertionError("the final certificate profile list is malformed")
    if [profile["digest"] for profile in catalog["profiles"]] != [
        profile["digest"] for profile in final_profiles
    ]:
        raise AssertionError("automatic half-turn discovery changed")
    by_digest = {profile["digest"]: profile for profile in final_profiles}
    for discovered in catalog["profiles"]:
        frozen = by_digest[discovered["digest"]]
        for key in (
            "ids_a",
            "ids_b",
            "target",
            "target_index",
            "stabilizer_elements",
        ):
            if json_normalize(discovered[key]) != frozen[key]:
                raise AssertionError(
                    f"{discovered['digest']}: catalog {key} changed"
                )
        data = search.reconstruct_profile(
            discovered["ids_a"], discovered["ids_b"]
        )
        if (
            len(data["fixed_basis"]),
            len(data["anti_basis"]),
        ) != tuple(frozen["eigenspace_dimensions"]):
            raise AssertionError(
                f"{discovered['digest']}: eigenspace split changed"
            )
    return catalog, by_digest


def full_new_extension_replay(
    catalog: dict[str, object],
    frozen_by_digest: dict[str, dict[str, object]],
) -> tuple[dict[str, object], ...]:
    replay_records = []
    for discovered in catalog["profiles"]:
        digest = str(discovered["digest"])
        frozen = frozen_by_digest[digest]
        if frozen["coverage_class"] != "two_new_final_extension":
            continue
        data = search.reconstruct_profile(
            discovered["ids_a"], discovered["ids_b"]
        )
        census = search.anti_code_census(data)
        if list((
            census["length"],
            census["dimension"],
            census["shell_weights"][0],
        )) != frozen["anti_code_parameters"]:
            raise AssertionError(f"{digest}: anti-code parameters changed")
        if search.compact_hash(census["weight_histogram"]) != frozen[
            "anti_weight_histogram_sha256"
        ]:
            raise AssertionError(f"{digest}: anti enumerator changed")
        if (
            v1_verifier.independent_weight_enumerator(census["generator"])
            != census["weight_histogram"]
        ):
            raise AssertionError(
                f"{digest}: dual MacWilliams check failed"
            )

        margin_catalog = catalog_phase_sum_intersection(
            discovered["ids_a"], discovered["ids_b"]
        )
        allowed = {
            tuple(
                coordinate
                for channel in sums
                for value in channel
                for coordinate in value
            )
            for sums, _ in margin_catalog["phase_sum_corpus"]
        }
        if len(allowed) != 96:
            raise AssertionError(f"{digest}: row-margin corpus changed")
        shell_records = {}
        for weight in census["shell_weights"]:
            actual = search.shell_lift_census(
                data,
                census["shell_coordinates"][weight],
                allowed,
            )
            expected = frozen["shells"][str(weight)]
            if json_normalize(
                extended_shell_summary(actual)
            ) != expected:
                raise AssertionError(
                    f"{digest}: weight-{weight} extension changed"
                )
            shell_records[str(weight)] = actual
        replay_records.append({
            "digest": digest,
            "dual_macwilliams_check": True,
            "shell_records": shell_records,
        })
    if len(replay_records) != 2:
        raise AssertionError("the final extension lost a new profile")
    return tuple(replay_records)


def verify(aggregate_path: Path, full_extension: bool) -> dict[str, object]:
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["schema"] != "lp333-h0-halfturn-final-extension-v2":
        raise AssertionError("unexpected final certificate schema")
    semantic = certificate.pop("semantic_sha256")
    if search.compact_hash(certificate) != semantic:
        raise AssertionError("the final certificate payload changed")

    verify_artifact_chain(certificate)
    catalog, by_digest = verify_catalog(certificate, aggregate_path)
    coverage = certificate["coverage_classes"]
    for coverage_class, record in coverage.items():
        profiles = [
            profile
            for profile in certificate["profiles"]
            if profile["coverage_class"] == coverage_class
        ]
        if [profile["digest"] for profile in profiles] != record[
            "profile_digests"
        ]:
            raise AssertionError(
                f"{coverage_class}: profile digest list changed"
            )
        totals = totals_for_profiles(profiles)
        for key, value in totals.items():
            if record[key] != value:
                raise AssertionError(
                    f"{coverage_class}: total {key} changed"
                )
    combined = totals_for_profiles(certificate["profiles"])
    if {
        "halfturn_profiles": len(certificate["profiles"]),
        **combined,
    } != certificate["combined_two_lowest_shell_coverage"]:
        raise AssertionError("the combined six-profile totals changed")

    extension_replay = (
        full_new_extension_replay(catalog, by_digest)
        if full_extension
        else ()
    )
    return {
        "schema": "lp333-h0-halfturn-final-extension-replay-v2",
        "mode": (
            "full-two-new-extension"
            if full_extension
            else "catalog-and-artifact-chain-only"
        ),
        "exact_h0_profile_orbits": catalog["all_exact_h0_orbits"],
        "halfturn_fixed_profile_orbits": catalog[
            "halfturn_fixed_orbits"
        ],
        "combined_two_lowest_shell_coverage": certificate[
            "combined_two_lowest_shell_coverage"
        ],
        "extension_replay": extension_replay,
        "status": "PASS",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--aggregate",
        type=Path,
        default=DEFAULT_AGGREGATE,
    )
    parser.add_argument(
        "--full-extension",
        action="store_true",
        help="rerun both new profiles' complete two-shell searches",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = verify(args.aggregate.resolve(), args.full_extension)
    print(json.dumps(result, indent=2, sort_keys=True))
    print(f"semantic_sha256={search.compact_hash(result)}")
    print("PASS")


if __name__ == "__main__":
    main()
