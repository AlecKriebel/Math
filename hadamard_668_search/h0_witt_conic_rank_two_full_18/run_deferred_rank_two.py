#!/usr/bin/env python3
"""Atomic, resumable continuation of the h=0 quadratic rank-two census.

Each selected orbit is completely enumerated into one atomic JSON result.
Existing results are skipped only after their semantic hash and frozen
input hashes validate.  Any exact digit-two point is immediately replayed
at the following digit and against the exact row-margin catalog before a
DIGIT2_WITNESS line is emitted.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import resource
import sys
import time

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
ALL_ORBIT = SEARCH / "h0_witt_conic_rank_two_all_orbits"
BASE = SEARCH / "h0_witt_conic_rank_two_orbit07"
RANK_ONE = SEARCH / "h0_witt_conic_rank_one"
SECOND = SEARCH / "phase_second_digit"
TRIAGE = SEARCH / "h0_new_orbits_lift_triage"
sys.path[:0] = [
    str(ALL_ORBIT),
    str(BASE),
    str(RANK_ONE),
    str(SECOND),
    str(TRIAGE),
    str(SEARCH),
]

import verify_all_orbit_rank_two as all_orbit  # noqa: E402


MODULUS = 3
BATCH_SIZE = 32_768
PROGRESS_BATCHES = 256
SCHEMA = "h668-h0-witt-conic-rank-two-orbit-result-v1"
DEFAULT_OUTPUT = HERE / "output"
DEFERRED_LABELS = (
    "orbit-01",
    "orbit-02",
    "orbit-03",
    "orbit-04",
    "orbit-06",
    "orbit-08",
    "orbit-10",
    "orbit-11",
    "orbit-12",
    "orbit-13",
    "orbit-15",
    "orbit-16",
    "orbit-18",
)


def compact_hash(value: object) -> str:
    return all_orbit.compact_hash(value)


def input_hashes() -> dict[str, str]:
    return {
        "classification_sha256": sha256(
            all_orbit.CLASSIFICATION.read_bytes()
        ).hexdigest(),
        "final_scan_sha256": sha256(
            all_orbit.FINAL_SCAN.read_bytes()
        ).hexdigest(),
        "all_orbit_verifier_sha256": sha256(
            Path(all_orbit.__file__).read_bytes()
        ).hexdigest(),
        "base_rank_two_verifier_sha256": sha256(
            Path(all_orbit.base.__file__).read_bytes()
        ).hexdigest(),
    }


def semantic_payload(result: dict[str, object]) -> dict[str, object]:
    return {
        key: value
        for key, value in result.items()
        if key not in ("runtime", "semantic_sha256")
    }


def validate_result(
    path: Path,
    expected_label: str,
    expected_inputs: dict[str, str],
) -> dict[str, object]:
    stored = json.loads(path.read_text())
    if stored["schema"] != SCHEMA or not stored["complete"]:
        raise AssertionError(f"{path}: result is not complete")
    if stored["record"]["profile"]["label"] != expected_label:
        raise AssertionError(f"{path}: orbit label changed")
    if stored["inputs"] != expected_inputs:
        raise AssertionError(f"{path}: frozen inputs changed")
    if compact_hash(semantic_payload(stored)) != stored["semantic_sha256"]:
        raise AssertionError(f"{path}: semantic hash failed")
    pilot = stored["record"]["pilot"]
    quotient = stored["record"]["quotient"]
    if pilot["status"] != "EXHAUSTIVE":
        raise AssertionError(f"{path}: orbit was not exhausted")
    denominator = quotient["physical_image_denominator"]
    if (
        pilot["coverage_numerator"] != denominator
        or pilot["coverage_denominator"] != denominator
        or sum(pilot["score_histogram"].values()) != denominator
    ):
        raise AssertionError(f"{path}: coverage accounting failed")
    return stored


def direct_score_replays(
    profiles,
    affine_origin: np.ndarray,
    affine_basis: np.ndarray,
    constants: np.ndarray,
    linears: np.ndarray,
    polars: np.ndarray,
    first_point_by_score: dict[int, np.ndarray],
) -> list[dict[str, object]]:
    result = []
    for score, affine_point in sorted(first_point_by_score.items()):
        placement, active = all_orbit.base.direct_replay(
            profiles,
            affine_origin,
            affine_basis,
            affine_point,
            score,
        )
        derived = tuple(
            int(value)
            for value in all_orbit.base.rank_one.evaluate_quadratics(
                affine_point[None, :], constants, linears, polars
            )[0]
        )
        if active != derived:
            raise AssertionError("direct and derived second digits differ")
        result.append(
            {
                "score": score,
                "affine_point_sha256": compact_hash(
                    tuple(map(int, affine_point))
                ),
                "placement_sha256": compact_hash(
                    tuple(map(int, placement))
                ),
                "active_second_digit_values": active,
            }
        )
    return result


def compute_orbit(
    orbit: dict[str, object],
    scan_record: dict[str, object],
    catalog: set[tuple[int, ...]],
) -> dict[str, object]:
    profiles, quotient, arrays = all_orbit.prepare_quotient(orbit)
    dimension = int(quotient["physical_image_dimension"])
    total_points = int(quotient["physical_image_denominator"])
    (
        affine_origin_raw,
        affine_basis_raw,
        constants_raw,
        linears_raw,
        polars_raw,
    ) = all_orbit.base.rank_one.exact_quadratic_forms(profiles)
    affine_origin = all_orbit.base.normalize(
        np.asarray(affine_origin_raw)
    )
    affine_basis = all_orbit.base.normalize(
        np.asarray(affine_basis_raw)
    )
    constants = all_orbit.base.normalize(np.asarray(constants_raw))
    linears = all_orbit.base.normalize(np.asarray(linears_raw))
    polars = all_orbit.base.normalize(np.asarray(polars_raw))
    affine_offset, family_basis, selected = (
        all_orbit.base.map_to_affine_coordinates(
            arrays["physical_offset"],
            arrays["physical_basis"],
            affine_origin,
            affine_basis,
        )
    )
    (
        restricted_constants,
        restricted_linears,
        restricted_polars,
    ) = all_orbit.base.restrict_quadratics(
        affine_offset, family_basis, constants, linears, polars
    )

    histogram = np.zeros(len(constants) + 1, dtype=np.int64)
    first_point_by_score: dict[int, np.ndarray] = {}
    survivors: list[dict[str, object]] = []
    coordinate_hasher = sha256()
    score_hasher = sha256()
    batches = (total_points + BATCH_SIZE - 1) // BATCH_SIZE
    started = time.perf_counter()
    for batch_index, start in enumerate(
        range(0, total_points, BATCH_SIZE), start=1
    ):
        coordinates = all_orbit.base.ternary_batch(
            start,
            min(start + BATCH_SIZE, total_points),
            dimension,
        )
        coordinate_hasher.update(
            np.asarray(coordinates, dtype=np.uint8).tobytes(order="C")
        )
        values = all_orbit.base.rank_one.evaluate_quadratics(
            coordinates,
            restricted_constants,
            restricted_linears,
            restricted_polars,
        )
        scores = np.sum(values == 0, axis=1).astype(np.uint8)
        score_hasher.update(scores.tobytes(order="C"))
        histogram += np.bincount(scores, minlength=len(histogram))
        for score in np.unique(scores):
            integer_score = int(score)
            if integer_score not in first_point_by_score:
                offset = int(np.flatnonzero(scores == score)[0])
                first_point_by_score[integer_score] = (
                    affine_offset + coordinates[offset] @ family_basis
                ) % MODULUS

        for offset in np.flatnonzero(scores == len(constants)):
            affine_point = (
                affine_offset + coordinates[int(offset)] @ family_basis
            ) % MODULUS
            survivor = all_orbit.survivor_record(
                orbit,
                profiles,
                affine_origin,
                affine_basis,
                affine_point,
                catalog,
            )
            survivors.append(survivor)
            alert = {
                "profile_label": orbit["label"],
                "profile_digest": orbit["production_digest"],
                "survivor_index": len(survivors) - 1,
                "assignment": survivor,
            }
            print(
                "DIGIT2_WITNESS="
                + json.dumps(alert, separators=(",", ":")),
                flush=True,
            )
            if len(survivors) > 10_000:
                raise RuntimeError(
                    "survivor replay count exceeded the 2 GB safety gate"
                )

        if (
            batch_index % PROGRESS_BATCHES == 0
            or batch_index == batches
        ):
            elapsed = time.perf_counter() - started
            print(
                f"PROGRESS {orbit['label']} batches={batch_index}/{batches} "
                f"states={min(start + BATCH_SIZE, total_points)}/"
                f"{total_points} digit2={len(survivors)} "
                f"elapsed={elapsed:.1f}s",
                flush=True,
            )

    if int(histogram.sum()) != total_points:
        raise AssertionError("orbit histogram lost states")
    maximum_score = max(
        score for score, count in enumerate(histogram) if count
    )
    pilot = {
        "status": "EXHAUSTIVE",
        "coverage_numerator": total_points,
        "coverage_denominator": total_points,
        "batch_size": BATCH_SIZE,
        "batches": batches,
        "affine_coordinate_columns": selected,
        "affine_offset_sha256": all_orbit.array_hash(affine_offset),
        "affine_family_basis_sha256": all_orbit.array_hash(family_basis),
        "restricted_constants_sha256": all_orbit.array_hash(
            restricted_constants
        ),
        "restricted_linears_sha256": all_orbit.array_hash(
            restricted_linears
        ),
        "restricted_polars_sha256": all_orbit.array_hash(
            restricted_polars
        ),
        "coordinate_stream_sha256": coordinate_hasher.hexdigest(),
        "score_stream_sha256": score_hasher.hexdigest(),
        "score_histogram": {
            str(score): int(count)
            for score, count in enumerate(histogram)
            if count
        },
        "maximum_active_second_digit_equations": maximum_score,
        "active_second_digit_equations": len(constants),
        "exact_second_digit_survivors": len(survivors),
        "two_consecutive_digit_survivors": sum(
            survivor["following_digit_defect"] == 0
            for survivor in survivors
        ),
        "margin_compatible_second_digit_survivors": sum(
            survivor["row_margin_catalog_member"]
            for survivor in survivors
        ),
        "two_consecutive_and_margin_survivors": sum(
            survivor["following_digit_defect"] == 0
            and survivor["row_margin_catalog_member"]
            for survivor in survivors
        ),
        "survivors": survivors,
        "direct_score_replays": direct_score_replays(
            profiles,
            affine_origin,
            affine_basis,
            constants,
            linears,
            polars,
            first_point_by_score,
        ),
    }
    return {
        "profile": {
            "label": orbit["label"],
            "digest": orbit["production_digest"],
            "ids_a": orbit["profile_ids_a"],
            "ids_b": orbit["profile_ids_b"],
            "target": orbit["target"],
            "classification_record_sha256": orbit["record_sha256"],
            "compatible_catalog_rows": scan_record[
                "row_margin_transfer"
            ]["compatible_catalog_rows"],
            "accepted_raw_assignments": scan_record[
                "row_margin_transfer"
            ]["accepted_raw_assignments"],
        },
        "quotient": quotient,
        "pilot": pilot,
    }


def write_atomic(path: Path, value: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    with temporary.open("w", encoding="utf-8") as handle:
        handle.write(rendered)
        handle.flush()
        os.fsync(handle.fileno())
    temporary.replace(path)


def run_one(
    label: str,
    output: Path,
    orbits: dict[str, dict[str, object]],
    scanned: dict[str, dict[str, object]],
    catalog: set[tuple[int, ...]],
    hashes: dict[str, str],
) -> None:
    if label not in orbits:
        raise ValueError(f"unknown profile label {label}")
    orbit = orbits[label]
    result_path = output / f"{label}.json"
    if result_path.exists():
        stored = validate_result(result_path, label, hashes)
        print(
            f"SKIP {label} complete states="
            f"{stored['record']['pilot']['coverage_denominator']}",
            flush=True,
        )
        return
    _, quotient, _ = all_orbit.prepare_quotient(orbit)
    dimension = int(quotient["physical_image_dimension"])
    if dimension <= all_orbit.DIMENSION_GATE:
        raise ValueError(
            f"{label} dimension {dimension} belongs to bounded certificate"
        )
    print(
        f"BEGIN {label} dimension={dimension} "
        f"states={quotient['physical_image_denominator']}",
        flush=True,
    )
    wall_start = time.perf_counter()
    usage_start = resource.getrusage(resource.RUSAGE_SELF)
    record = compute_orbit(
        orbit, scanned[orbit["production_digest"]], catalog
    )
    usage_stop = resource.getrusage(resource.RUSAGE_SELF)
    result: dict[str, object] = {
        "schema": SCHEMA,
        "complete": True,
        "inputs": hashes,
        "record": record,
    }
    result["semantic_sha256"] = compact_hash(semantic_payload(result))
    result["runtime"] = {
        "wall_seconds": time.perf_counter() - wall_start,
        "user_seconds": usage_stop.ru_utime - usage_start.ru_utime,
        "system_seconds": usage_stop.ru_stime - usage_start.ru_stime,
        "maximum_resident_set_bytes": resource.getrusage(
            resource.RUSAGE_SELF
        ).ru_maxrss,
        "thread_limits_required": (
            "OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 "
            "VECLIB_MAXIMUM_THREADS=1"
        ),
    }
    write_atomic(result_path, result)
    validate_result(result_path, label, hashes)
    pilot = record["pilot"]
    print(
        f"COMPLETE {label} max="
        f"{pilot['maximum_active_second_digit_equations']}/18 "
        f"digit2={pilot['exact_second_digit_survivors']} "
        f"digit3={pilot['two_consecutive_digit_survivors']} "
        f"margin={pilot['margin_compatible_second_digit_survivors']} "
        f"path={result_path}",
        flush=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path, default=DEFAULT_OUTPUT
    )
    parser.add_argument(
        "--orbit",
        action="append",
        choices=DEFERRED_LABELS,
        help="specific deferred orbit; repeatable (default: all)",
    )
    args = parser.parse_args()
    _, orbit_records, scanned = all_orbit.load_inputs()
    orbits = {record["label"]: record for record in orbit_records}
    catalog = set(all_orbit.row_sum_catalog())
    if len(catalog) != 1_756:
        raise AssertionError("row-margin catalog changed")
    hashes = input_hashes()
    labels = tuple(args.orbit) if args.orbit else DEFERRED_LABELS
    for label in labels:
        run_one(
            label,
            args.output,
            orbits,
            scanned,
            catalog,
            hashes,
        )
    print(f"PASS completed_or_skipped={len(labels)}", flush=True)


if __name__ == "__main__":
    main()
