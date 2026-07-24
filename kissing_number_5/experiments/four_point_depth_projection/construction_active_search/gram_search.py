#!/usr/bin/env python3
"""Deterministic alternating Gram feasibility search for N=41,...,44.

The iteration alternates two deliberately nonsmooth operations:

* an off-diagonal half-space projection, with a Dykstra residual and extra
  weight on the largest violations; and
* spectral truncation to the PSD cone of rank at most five, followed by
  diagonal congruence normalization.

Stagnating iterations receive seeded, multi-entry Gram perturbations.  This is
not an optimizer certificate.  Its output is a reproducible construction
search record, and all reported point-code quantities are recomputed from the
returned coordinates rather than from the projected intermediate matrices.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from gram_inventory import coordinate_sha256, diagnostics, sha256_file


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
DEFAULT_OUTPUT = HERE / "gram_search_results.json"
CAP = 0.5
DIMENSION = 5


@dataclass(frozen=True)
class Schedule:
    name: str
    relaxation: float
    memory_scale: float
    memory_decay: float
    active_boost: float
    strict_margin: float


SCHEDULES = (
    Schedule("plain_ap", 0.65, 0.0, 0.0, 0.0, 0.0),
    Schedule("weighted_ap", 0.85, 0.0, 0.0, 0.75, 0.0),
    Schedule("dykstra_light", 0.80, 0.20, 0.92, 0.50, 0.0),
    Schedule("dykstra_strict", 1.05, 0.35, 0.88, 0.80, 2.5e-4),
    Schedule("overrelaxed", 1.35, 0.10, 0.75, 1.10, 0.0),
)


def normalize_rows(points: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(points, axis=1)
    if np.any(norms <= 1e-14):
        raise FloatingPointError("spectral factor has a nearly zero row")
    return points / norms[:, None]


def project_psd_rank_correlation(
    matrix: np.ndarray, rank: int = DIMENSION
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return coordinates, their correlation Gram matrix, and raw eigenvalues."""
    symmetric = 0.5 * (matrix + matrix.T)
    eigenvalues, eigenvectors = np.linalg.eigh(symmetric)
    kept = np.maximum(eigenvalues[-rank:], 0.0)
    if kept[-1] <= 1e-14 or np.count_nonzero(kept > 1e-14) < rank:
        # Keeping a tiny positive floor prevents accidental collapse to a
        # lower-dimensional duplicate-point basin.  The returned matrix is
        # still PSD and has rank at most five in floating arithmetic.
        scale = max(float(kept[-1]), 1.0)
        kept = np.maximum(kept, scale * 1e-12)
    points = eigenvectors[:, -rank:] * np.sqrt(kept)[None, :]
    points = normalize_rows(points)
    gram = points @ points.T
    return points, gram, eigenvalues


def upper_values(gram: np.ndarray) -> tuple[tuple[np.ndarray, np.ndarray], np.ndarray]:
    upper = np.triu_indices(len(gram), 1)
    return upper, gram[upper]


def objective(points: np.ndarray) -> dict[str, float | int]:
    gram = points @ points.T
    _, values = upper_values(gram)
    excess = np.maximum(values - CAP, 0.0)
    return {
        "maximum_inner_product": float(np.max(values)),
        "gap_above_one_half": float(np.max(values) - CAP),
        "violating_pair_count": int(np.count_nonzero(excess > 0.0)),
        "violation_l2": float(np.linalg.norm(excess)),
        "violation_l1": float(np.sum(excess)),
    }


def is_better(left: dict[str, Any], right: dict[str, Any]) -> bool:
    """Lexicographic construction objective, led by maximum inner product."""
    return (
        left["maximum_inner_product"],
        left["violation_l2"],
        left["violation_l1"],
    ) < (
        right["maximum_inner_product"],
        right["violation_l2"],
        right["violation_l1"],
    )


def halfspace_correction(
    gram: np.ndarray,
    memory: np.ndarray,
    schedule: Schedule,
) -> tuple[np.ndarray, np.ndarray]:
    """Dykstra-weighted projection toward diag=1 and offdiag <= 1/2."""
    n = len(gram)
    upper = np.triu_indices(n, 1)
    shifted = 0.5 * (
        gram
        + schedule.memory_scale * memory
        + (gram + schedule.memory_scale * memory).T
    )
    projected = shifted.copy()
    target = CAP - schedule.strict_margin
    clipped = np.minimum(projected[upper], target)
    projected[upper] = clipped
    projected[(upper[1], upper[0])] = clipped
    np.fill_diagonal(projected, 1.0)

    new_memory = schedule.memory_decay * (shifted - projected)
    np.fill_diagonal(new_memory, 0.0)
    corrected = gram + schedule.relaxation * (projected - gram)

    # The Euclidean half-space projection minimizes squared violation and can
    # neglect the largest few entries.  This deterministic weight preserves
    # the direction of every valid half-space correction while emphasizing
    # the current maximum violations.
    current_values = gram[upper]
    violations = np.maximum(current_values - target, 0.0)
    max_violation = float(np.max(violations))
    if schedule.active_boost > 0.0 and max_violation > 0.0:
        weights = (violations / max_violation) ** 2
        correction = schedule.active_boost * weights * violations
        values = corrected[upper] - correction
        corrected[upper] = values
        corrected[(upper[1], upper[0])] = values
    np.fill_diagonal(corrected, 1.0)
    return corrected, new_memory


def multi_entry_kick(
    gram: np.ndarray,
    rng: np.random.Generator,
    amplitude: float,
    edge_count: int,
    active_band: float,
) -> np.ndarray:
    """Lower a seeded random block of high Gram entries before rank projection."""
    if amplitude <= 0.0 or edge_count <= 0:
        return gram.copy()
    upper, values = upper_values(gram)
    maximum = float(np.max(values))
    eligible = np.flatnonzero(values >= maximum - active_band)
    if len(eligible) < edge_count:
        count = min(edge_count, len(values))
        eligible = np.argpartition(values, -count)[-count:]
    count = min(edge_count, len(eligible))
    selected = rng.choice(eligible, size=count, replace=False)
    magnitudes = amplitude * rng.uniform(0.5, 1.5, size=count)
    kicked = gram.copy()
    rows = upper[0][selected]
    columns = upper[1][selected]
    kicked[(rows, columns)] -= magnitudes
    kicked[(columns, rows)] -= magnitudes
    np.fill_diagonal(kicked, 1.0)
    return kicked


def load_warm_start(n: int) -> tuple[np.ndarray, dict[str, Any]]:
    if n == 41:
        path = REPO / "experiments/input/spherical_codes_5_41.txt"
        points = np.loadtxt(path, delimiter=",", dtype=np.float64)
        locator = "comma-separated rows"
    elif n in (42, 43):
        path = (
            REPO
            / "experiments/construction_round9_core_rattler/results/"
            "core_rattler_portfolio.json"
        )
        payload = json.loads(path.read_text())
        index = n - 41
        points = np.asarray(
            payload["runs"][index]["best"]["coordinates_float64"],
            dtype=np.float64,
        )
        locator = f"$.runs[{index}].best.coordinates_float64"
    elif n == 44:
        path = (
            REPO
            / "experiments/construction_round6_bundle/results/"
            "bundle_portfolio.json"
        )
        payload = json.loads(path.read_text())
        points = np.asarray(
            payload["runs"][19]["best"]["coordinates_float64"],
            dtype=np.float64,
        )
        locator = "$.runs[19].best.coordinates_float64"
    else:
        raise ValueError(f"unsupported N={n}")
    points = normalize_rows(points)
    if points.shape != (n, DIMENSION):
        raise ValueError(f"bad warm-start shape {points.shape}, expected {(n, 5)}")
    return points, {
        "source_file": str(path.relative_to(REPO)),
        "source_file_sha256": sha256_file(path),
        "source_locator": locator,
        "coordinate_little_endian_float64_sha256": coordinate_sha256(points),
    }


def initial_amplitude(restart: int) -> float:
    if restart == 0:
        return 0.0
    return (0.0015, 0.003, 0.006, 0.012, 0.024)[(restart - 1) % 5]


def run_restart(
    warm: np.ndarray,
    n: int,
    restart: int,
    iterations: int,
    seed: int,
    kick_period: int,
    checkpoint_period: int,
) -> tuple[dict[str, Any], np.ndarray]:
    rng = np.random.default_rng(seed)
    schedule = SCHEDULES[restart % len(SCHEDULES)]
    points = warm.copy()
    gram = points @ points.T
    amplitude = initial_amplitude(restart)
    if amplitude:
        kicked = multi_entry_kick(
            gram,
            rng,
            amplitude=amplitude,
            edge_count=min(n * 2, n * (n - 1) // 2),
            active_band=max(0.01, 2.5 * amplitude),
        )
        points, gram, _ = project_psd_rank_correlation(kicked)

    memory = np.zeros_like(gram)
    baseline_objective = objective(points)
    best_objective = dict(baseline_objective)
    best_points = points.copy()
    best_iteration = 0
    last_improvement = 0
    kick_count = 0
    checkpoints: list[dict[str, Any]] = []
    raw_rank_projection_min_eigenvalue = float("inf")

    for iteration in range(1, iterations + 1):
        corrected, memory = halfspace_correction(gram, memory, schedule)
        points, gram, raw_eigenvalues = project_psd_rank_correlation(corrected)
        raw_rank_projection_min_eigenvalue = min(
            raw_rank_projection_min_eigenvalue, float(raw_eigenvalues[-5])
        )
        current_objective = objective(points)
        if is_better(current_objective, best_objective):
            best_objective = dict(current_objective)
            best_points = points.copy()
            best_iteration = iteration
            last_improvement = iteration

        if current_objective["maximum_inner_product"] <= CAP:
            break

        if (
            kick_period > 0
            and iteration - last_improvement >= kick_period
            and iteration < iterations
        ):
            kick_count += 1
            kick_amplitude = max(0.001, amplitude) * (
                0.70 ** min(kick_count - 1, 6)
            )
            kicked = multi_entry_kick(
                gram,
                rng,
                amplitude=kick_amplitude,
                edge_count=min(n + 3 * kick_count, n * 3),
                active_band=max(0.008, 3.0 * kick_amplitude),
            )
            points, gram, _ = project_psd_rank_correlation(kicked)
            memory.fill(0.0)
            last_improvement = iteration

        if checkpoint_period > 0 and iteration % checkpoint_period == 0:
            checkpoints.append(
                {
                    "iteration": iteration,
                    **current_objective,
                    "best_maximum_inner_product": best_objective[
                        "maximum_inner_product"
                    ],
                }
            )

    elapsed_objective = objective(points)
    return (
        {
            "n": n,
            "restart": restart,
            "seed": seed,
            "schedule": asdict(schedule),
            "iterations_requested": iterations,
            "iterations_completed": iteration,
            "initial_perturbation_amplitude": amplitude,
            "multi_entry_kick_count": kick_count,
            "initial_objective": baseline_objective,
            "terminal_objective": elapsed_objective,
            "best_objective": best_objective,
            "best_iteration": best_iteration,
            "best_coordinate_little_endian_float64_sha256": coordinate_sha256(
                best_points
            ),
            "minimum_fifth_largest_raw_projection_eigenvalue": (
                raw_rank_projection_min_eigenvalue
            ),
            "checkpoints": checkpoints,
        },
        best_points,
    )


def environment_record() -> dict[str, Any]:
    return {
        "python": sys.version,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "byteorder": sys.byteorder,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, nargs="+", default=[41, 42, 43, 44])
    parser.add_argument("--restarts", type=int, default=12)
    parser.add_argument("--iterations", type=int, default=3000)
    parser.add_argument("--seed-base", type=int, default=2026072300)
    parser.add_argument("--kick-period", type=int, default=240)
    parser.add_argument("--checkpoint-period", type=int, default=500)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    if args.restarts < 1 or args.iterations < 1:
        parser.error("restarts and iterations must be positive")
    started = time.monotonic()
    all_runs: list[dict[str, Any]] = []
    best_by_n: dict[str, Any] = {}
    candidate_found = False

    for n in args.n:
        warm, source = load_warm_start(n)
        warm_objective = objective(warm)
        global_best = dict(warm_objective)
        global_points = warm.copy()
        winning_run: int | None = None
        print(
            f"N={n} warm max={warm_objective['maximum_inner_product']:.17g}",
            flush=True,
        )
        for restart in range(args.restarts):
            seed = args.seed_base + 100 * (n - 41) + restart
            record, points = run_restart(
                warm,
                n=n,
                restart=restart,
                iterations=args.iterations,
                seed=seed,
                kick_period=args.kick_period,
                checkpoint_period=args.checkpoint_period,
            )
            all_runs.append(record)
            if is_better(record["best_objective"], global_best):
                global_best = dict(record["best_objective"])
                global_points = points.copy()
                winning_run = restart
                print(
                    f"  IMPROVED restart={restart} seed={seed} "
                    f"max={global_best['maximum_inner_product']:.17g}",
                    flush=True,
                )
            else:
                print(
                    f"  restart={restart} seed={seed} "
                    f"best={record['best_objective']['maximum_inner_product']:.17g}",
                    flush=True,
                )
            if global_best["maximum_inner_product"] <= CAP:
                candidate_found = True
                break
        best_diagnostics = diagnostics(global_points)
        best_by_n[str(n)] = {
            "warm_start": source,
            "warm_start_objective": warm_objective,
            "winning_restart": winning_run,
            "strictly_beats_warm_start": (
                global_best["maximum_inner_product"]
                < warm_objective["maximum_inner_product"]
            ),
            "meets_kissing_threshold_binary64": (
                global_best["maximum_inner_product"] <= CAP
            ),
            "best_objective": global_best,
            "coordinates_float64": global_points.tolist(),
            "diagnostics": best_diagnostics,
        }

    output = {
        "schema": "kissing5-alternating-gram-search-v1",
        "evidence_status": "NUMERICAL EVIDENCE ONLY",
        "method": (
            "Dykstra-weighted half-space corrections alternating with "
            "diag-one PSD rank-at-most-five spectral projection"
        ),
        "threshold": CAP,
        "dimension": DIMENSION,
        "parameters": {
            "n": args.n,
            "restarts": args.restarts,
            "iterations": args.iterations,
            "seed_base": args.seed_base,
            "kick_period": args.kick_period,
            "checkpoint_period": args.checkpoint_period,
            "schedules": [asdict(schedule) for schedule in SCHEDULES],
        },
        "environment": environment_record(),
        "elapsed_seconds": time.monotonic() - started,
        "candidate_at_or_below_threshold_found": candidate_found,
        "best_by_n": best_by_n,
        "runs": all_runs,
    }
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(f"wrote {args.output}", flush=True)


if __name__ == "__main__":
    main()
