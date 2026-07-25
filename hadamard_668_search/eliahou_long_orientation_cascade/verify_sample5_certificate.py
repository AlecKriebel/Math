#!/usr/bin/env python3
"""Regenerate and verify the pinned 200-support orientation-cascade audit."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path

from audit_orientation_cascade import (
    adjacent_mod8_redundancy_audit,
    find_fixture,
    low_weight_code_span,
    quadratic_next_digit,
)


HERE = Path(__file__).resolve().parent
EXPECTED = HERE / "EXPECTED_SAMPLE5_SUMMARY.json"


def canonical_hash(value: object) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def histogram(records: list[dict], field: str) -> dict[str, int]:
    return {
        ("null" if value is None else str(value)): count
        for value, count in sorted(
            Counter(record[field] for record in records).items(),
            key=lambda item: str(item[0]),
        )
    }


def regenerate() -> dict[str, object]:
    redundancy = [
        adjacent_mod8_redundancy_audit(case_number)
        for case_number in range(1, 21)
    ]
    code_spans = [
        low_weight_code_span(case_number, conditioned)
        for conditioned in (False, True)
        for case_number in range(1, 21)
    ]
    fixtures = [
        quadratic_next_digit(
            find_fixture(
                case_number,
                profile_number,
                seed=(
                    668_320_000
                    + 10_000 * sample_number
                    + 2 * case_number
                    + profile_number
                ),
            )
        )
        for case_number in range(1, 21)
        for profile_number in range(2)
        for sample_number in range(5)
    ]
    consistent = [
        record for record in fixtures if record["mod16_consistent"]
    ]
    unconditioned = [
        record
        for record in code_spans
        if not record["profile_conditioned"]
    ]
    conditioned = [
        record
        for record in code_spans
        if record["profile_conditioned"]
    ]
    polar_ranks: Counter[int] = Counter()
    for record in consistent:
        for rank, count in record[
            "mod32_individual_polar_rank_histogram"
        ].items():
            polar_ranks[int(rank)] += count

    return {
        "schema": "eliahou-long-orientation-cascade-sample5-v1",
        "scope": {
            "cases": 20,
            "profiles_per_case": 2,
            "supports_per_profile": 5,
            "total_supports": len(fixtures),
        },
        "exact_redundancy": {
            "case_count": len(redundancy),
            "anti_mod2_affine_dimensions": histogram(
                redundancy, "anti_mod2_affine_dimension"
            ),
            "plus_mod8_raw_quadratic_row_ranks": histogram(
                redundancy, "plus_mod8_raw_quadratic_row_rank"
            ),
            "plus_mod8_raw_linear_row_ranks": histogram(
                redundancy, "plus_mod8_raw_linear_row_rank"
            ),
            "plus_mod8_restricted_ranks": histogram(
                redundancy, "plus_mod8_restricted_rank"
            ),
            "semantic_sha256": canonical_hash(redundancy),
        },
        "exact_low_weight_code_span": {
            "unconditioned_dimensions": [
                record["code_dimension"] for record in unconditioned
            ],
            "unconditioned_rank_through_weight4": [
                record["rank_generated_by_weight_at_most_4"]
                for record in unconditioned
            ],
            "unconditioned_rank_through_weight6": [
                record["rank_generated_by_weight_at_most_6"]
                for record in unconditioned
            ],
            "profile_conditioned_dimensions": [
                record["code_dimension"] for record in conditioned
            ],
            "profile_conditioned_rank_through_weight4": [
                record["rank_generated_by_weight_at_most_4"]
                for record in conditioned
            ],
            "profile_conditioned_rank_through_weight6": [
                record["rank_generated_by_weight_at_most_6"]
                for record in conditioned
            ],
            "semantic_sha256": canonical_hash(code_spans),
        },
        "bounded_fixture_observations": {
            "fixtures_semantic_sha256": canonical_hash(fixtures),
            "mod16_consistency": histogram(
                fixtures, "mod16_consistent"
            ),
            "mod16_rank": histogram(fixtures, "mod16_rank"),
            "mod16_augmented_rank": histogram(
                fixtures, "mod16_augmented_rank"
            ),
            "mod16_nullity": histogram(
                fixtures, "mod16_orientation_nullity"
            ),
            "mod16_total_orientation_points": sum(
                record["mod16_orientation_points"]
                for record in fixtures
            ),
            "mod16_total_exact_root_points": sum(
                record["mod16_plus_exact_roots_survivors"]
                for record in fixtures
            ),
            "mod16_exact_root_point_min": min(
                record["mod16_plus_exact_roots_survivors"]
                for record in consistent
            ),
            "mod16_exact_root_point_max": max(
                record["mod16_plus_exact_roots_survivors"]
                for record in consistent
            ),
            "mod32_survivors": histogram(
                fixtures, "mod32_survivors"
            ),
            "mod32_total_survivors": sum(
                record["mod32_survivors"] for record in fixtures
            ),
            "mod32_plus_exact_roots_survivors": histogram(
                fixtures, "mod32_plus_exact_roots_survivors"
            ),
            "mod32_total_plus_exact_roots_survivors": sum(
                record["mod32_plus_exact_roots_survivors"]
                for record in fixtures
            ),
            "mod64_total_plus_exact_roots_survivors": sum(
                record["mod64_plus_exact_roots_survivors"]
                for record in fixtures
            ),
            "mod32_quadratic_coefficient_rank": histogram(
                fixtures, "mod32_quadratic_coefficient_rank"
            ),
            "mod32_pure_quadratic_row_rank": histogram(
                fixtures, "mod32_pure_quadratic_row_rank"
            ),
            "mod32_common_polar_radical_dimension": histogram(
                fixtures, "mod32_common_polar_radical_dimension"
            ),
            "mod32_individual_polar_rank_aggregate": {
                str(rank): count
                for rank, count in sorted(polar_ranks.items())
            },
        },
        "claim_boundary": (
            "exact reductions plus a deterministic bounded sample; "
            "no long case excluded and no BS(84,83) constructed"
        ),
    }


def main() -> None:
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    observed = regenerate()
    if observed != expected:
        print(
            json.dumps(
                {"expected": expected, "observed": observed},
                indent=2,
                sort_keys=True,
            )
        )
        raise SystemExit("FAIL: regenerated certificate does not match")
    print(json.dumps(observed, indent=2, sort_keys=True))
    print("PASS: pinned 200-support cascade certificate regenerated")


if __name__ == "__main__":
    main()
