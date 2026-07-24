#!/usr/bin/env python3
"""Independent binary64 verifier for the round-11 construction portfolio.

This checker never promotes numerical coordinates to exact spherical-code
certificates.  It recomputes every reported representative directly from
stored coordinates and checks provenance, schedules, seeds, hashes, and the
required search mechanisms.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results" / "portfolio.json"


class VerificationError(RuntimeError):
    """Raised when a numerical artifact fails an independent check."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def close(left: float, right: float, tolerance: float = 5.0e-13) -> None:
    require(
        math.isclose(left, right, rel_tol=tolerance, abs_tol=tolerance),
        f"floating mismatch: {left!r} versus {right!r}",
    )


def coordinate_hash(array: np.ndarray) -> str:
    canonical = np.asarray(array, dtype="<f8", order="C")
    return hashlib.sha256(canonical.tobytes()).hexdigest()


def explicit_maximum(array: np.ndarray) -> float:
    return max(
        math.fsum(
            float(array[first, coordinate])
            * float(array[second, coordinate])
            for coordinate in range(array.shape[1])
        )
        for first in range(len(array))
        for second in range(first + 1, len(array))
    )


def target_rows(
    cardinality: int, profile_row_types: list[dict[str, object]]
) -> np.ndarray:
    colors = range(-4, 3)
    base = []
    for record in profile_row_types:
        energy = sum(
            color * color * multiplicity
            for color, multiplicity in zip(colors, record["degree"])
        ) / 16
        base.extend([energy] * record["count"])
    require(len(base) == 41, "profile row types do not total 41")
    base_array = np.sort(np.asarray(base, dtype=float))
    if cardinality == 41:
        return base_array
    old_quantiles = (np.arange(41) + 0.5) / 41
    new_quantiles = (np.arange(cardinality) + 0.5) / cardinality
    return (
        np.interp(new_quantiles, old_quantiles, base_array)
        * (cardinality - 1)
        / 40
    )


def recompute(
    coordinates: list[list[float]],
    edge_counts: np.ndarray,
    profile_row_types: list[dict[str, object]],
) -> dict[str, object]:
    array = np.asarray(coordinates, dtype=float)
    require(
        array.ndim == 2 and array.shape[1] == 5,
        "coordinates have wrong shape",
    )
    cardinality = len(array)
    norms = np.sum(array * array, axis=1)
    gram = array @ array.T
    first, second = np.triu_indices(cardinality, 1)
    pairs = gram[first, second]
    maximum = float(np.max(pairs))
    close(maximum, explicit_maximum(array), 2.0e-14)
    violation = np.maximum(pairs - 0.5, 0)
    frame = array.T @ array
    row_energy = np.sum(gram * gram, axis=1) - norms * norms

    centers = np.arange(-4, 3, dtype=float) / 4
    logits = -(pairs[:, None] - centers[None, :]) ** 2 / (2 * 0.10**2)
    logits -= np.max(logits, axis=1, keepdims=True)
    weights = np.exp(logits)
    weights /= np.sum(weights, axis=1, keepdims=True)
    histogram = np.sum(weights, axis=0)
    target_probabilities = edge_counts / np.sum(edge_counts)
    hard_bins = np.argmin(abs(pairs[:, None] - centers[None, :]), axis=1)

    return {
        "shape": array.shape,
        "maximum_inner_product": maximum,
        "minimum_inner_product": float(np.min(pairs)),
        "gap_above_one_half": maximum - 0.5,
        "violating_pair_count": int(np.count_nonzero(violation)),
        "violation_l2": float(np.linalg.norm(violation)),
        "centroid_norm": float(np.linalg.norm(np.mean(array, axis=0))),
        "trace_gram_squared": float(np.sum(frame * frame)),
        "trace_gram_cubed": float(np.trace(frame @ frame @ frame)),
        "frame_eigenvalues": np.linalg.eigvalsh(frame),
        "row_energy_mean": float(np.mean(row_energy)),
        "row_energy_sorted_rmse_to_scaled_x12": float(
            np.sqrt(
                np.mean(
                    (
                        np.sort(row_energy)
                        - target_rows(cardinality, profile_row_types)
                    )
                    ** 2
                )
            )
        ),
        "soft_profile_l2": float(
            np.linalg.norm(
                histogram / len(pairs) - target_probabilities
            )
        ),
        "soft_profile_counts_sigma_0p10": histogram,
        "nearest_quarter_counts": np.bincount(
            hard_bins, minlength=7
        ),
        "coordinate_little_endian_float64_sha256": coordinate_hash(array),
        "unit_norm_maximum_residual": float(np.max(abs(norms - 1))),
    }


def compare_record(
    stored: dict[str, object],
    computed: dict[str, object],
) -> None:
    for key in (
        "maximum_inner_product",
        "minimum_inner_product",
        "gap_above_one_half",
        "violation_l2",
        "centroid_norm",
        "trace_gram_squared",
        "trace_gram_cubed",
        "row_energy_mean",
        "row_energy_sorted_rmse_to_scaled_x12",
        "soft_profile_l2",
        "unit_norm_maximum_residual",
    ):
        close(float(stored[key]), float(computed[key]))
    require(
        stored["violating_pair_count"] == computed["violating_pair_count"],
        "violating-pair count mismatch",
    )
    require(
        stored["coordinate_little_endian_float64_sha256"]
        == computed["coordinate_little_endian_float64_sha256"],
        "coordinate hash mismatch",
    )
    require(
        stored["nearest_quarter_counts"]
        == computed["nearest_quarter_counts"].tolist(),
        "nearest-quarter count mismatch",
    )
    require(
        len(stored["frame_eigenvalues"]) == 5,
        "wrong stored frame spectrum length",
    )
    for stored_value, computed_value in zip(
        stored["frame_eigenvalues"], computed["frame_eigenvalues"]
    ):
        close(float(stored_value), float(computed_value))
    for stored_value, computed_value in zip(
        stored["soft_profile_counts_sigma_0p10"],
        computed["soft_profile_counts_sigma_0p10"],
    ):
        close(float(stored_value), float(computed_value))
    require(
        computed["unit_norm_maximum_residual"] <= 8.0e-16,
        "stored coordinates are not unit vectors to binary64 precision",
    )


def verify(path: Path = RESULTS) -> dict[str, object]:
    source_bytes = path.read_bytes()
    source = json.loads(source_bytes)
    require(
        source["schema"] == "kissing5.construction_round11_x12_profile.v1",
        "wrong portfolio schema",
    )
    require(
        source["evidence_status"]
        == "NUMERICAL EVIDENCE ONLY; NOT AN EXACT CONFIGURATION CERTIFICATE",
        "unsafe evidence status",
    )
    require(
        source["parameters"]["cardinalities"] == [41, 42, 43, 44],
        "wrong cardinality portfolio",
    )
    require(source["parameters"]["replicas"] >= 4, "too few replicas")
    require(source["parameters"]["seed_base"] == 2026072400, "wrong seed base")

    profile_path = ROOT / source["profile_source"]
    require(
        hashlib.sha256(profile_path.read_bytes()).hexdigest()
        == source["profile_source_sha256"],
        "X=12 profile-source hash mismatch",
    )
    edge_counts = np.asarray(source["profile_edge_counts"], dtype=float)
    require(
        edge_counts.tolist() == [6, 72, 102, 174, 181, 34, 251],
        "wrong X=12 edge profile",
    )

    for record in source["baseline_sources"].values():
        baseline_path = ROOT / record["path"]
        require(
            hashlib.sha256(baseline_path.read_bytes()).hexdigest()
            == record["file_sha256"],
            "baseline source hash mismatch",
        )

    runs = source["runs"]
    require(len(runs) == 8, "expected two runs for each cardinality")
    seen = set()
    verified_representatives = 0
    per_run = []
    for run in runs:
        cardinality = run["cardinality"]
        kind = run["kind"]
        require(
            41 <= cardinality <= 44
            and kind in {"profile_guided", "unrestricted"},
            "unknown run target",
        )
        require((cardinality, kind) not in seen, "duplicate run")
        seen.add((cardinality, kind))
        expected_seed = (
            2026072400
            + 100 * (cardinality - 41)
            + (kind == "unrestricted")
        )
        require(run["seed"] == expected_seed, "wrong deterministic seed")
        require(
            run["replica_exchange"]["attempts"] > 0
            and run["replica_exchange"]["accepts"] > 0,
            "replica exchange was not exercised",
        )
        topology = run["topology_change"]
        require(
            topology["candidate_count"] == 4000
            and 0 <= topology["deleted_index"] < cardinality,
            "delete/reinsert mechanism was not exercised",
        )
        origins = {
            record["origin"] for record in run["initial_replicas"]
        }
        require(
            "topology_delete_insert" in origins
            and any(origin.startswith("asymmetric_gaussian_") for origin in origins),
            "required asymmetric/topology starts are missing",
        )
        require(
            run["phases"][-1]["profile_penalties_released"],
            "the final phase retained a profile penalty",
        )
        if kind == "profile_guided":
            require(
                any(
                    not phase["profile_penalties_released"]
                    for phase in run["phases"]
                )
                and all(
                    phase["profile_penalties_released"]
                    for phase in run["phases"][-2:]
                ),
                "guided run did not lock then release its profile",
            )

        for phase in run["phases"]:
            for key in (
                "best_maximum_representative",
                "best_profile_representative",
            ):
                representative = phase[key]
                computed = recompute(
                    representative["coordinates_float64"],
                    edge_counts,
                    source["profile_row_types"],
                )
                require(
                    computed["shape"] == (cardinality, 5),
                    "phase representative has wrong shape",
                )
                compare_record(representative, computed)
                verified_representatives += 1

        best = run["best"]
        computed_best = recompute(
            best["coordinates_float64"],
            edge_counts,
            source["profile_row_types"],
        )
        require(
            computed_best["shape"] == (cardinality, 5),
            "best coordinates have wrong shape",
        )
        compare_record(best, computed_best)
        require(
            computed_best["maximum_inner_product"] > 0.5,
            "a threshold candidate needs exact certification",
        )
        per_run.append(
            {
                "cardinality": cardinality,
                "kind": kind,
                "maximum": computed_best["maximum_inner_product"],
                "coordinate_sha256": computed_best[
                    "coordinate_little_endian_float64_sha256"
                ],
                "exchange_accepts": run["replica_exchange"]["accepts"],
            }
        )

    require(
        seen
        == {
            (cardinality, kind)
            for cardinality in range(41, 45)
            for kind in ("profile_guided", "unrestricted")
        },
        "incomplete target portfolio",
    )
    require(not source["exact_candidate_found"], "unsafe threshold flag")

    best_by_n = {}
    for cardinality in range(41, 45):
        candidates = [
            record for record in per_run if record["cardinality"] == cardinality
        ]
        best = min(candidates, key=lambda record: record["maximum"])
        stored = source["best_by_n"][str(cardinality)]
        close(stored["maximum_inner_product"], best["maximum"])
        require(
            stored["kind"] == best["kind"]
            and stored["coordinate_sha256"] == best["coordinate_sha256"],
            "best-by-N summary mismatch",
        )
        best_by_n[str(cardinality)] = best["maximum"]

    return {
        "status": "numerical portfolio independently recomputed",
        "portfolio_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "verified_phase_representatives": verified_representatives,
        "runs": per_run,
        "best_by_n": best_by_n,
        "exact_candidate_found": False,
    }


def main() -> None:
    try:
        result = verify()
    except (KeyError, TypeError, ValueError, VerificationError) as error:
        print(f"verification failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
