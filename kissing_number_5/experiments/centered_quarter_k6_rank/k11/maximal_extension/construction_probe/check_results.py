#!/usr/bin/env python3
"""Independent numerical consistency check for the K40-seeded N41 probe."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np


HERE = Path(__file__).resolve().parent
RESULTS_PATH = HERE / "n41_probe_results.json"
RESULTS_SHA256 = (
    "2049ff1827e1f30298bf9a289be9773e498dd1f0dc4c5adb24f7a104c1c99465"
)
CLASSIFICATION_SHA256 = (
    "ccabd04602c5481d40fa16d5979a7cbcb04fa3ece357f3c97d39e881f1bef0a0"
)
EXPECTED_ATOMS = (6, 7, 9, 10, 18, 23, 27, 41, 43, 44, 47, 49, 50)
EXPECTED_MODES = ("insert_release", "replace_one_by_two")
STATUS = "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE"


class ResultsError(RuntimeError):
    """Raised when stored floating-point diagnostics are inconsistent."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ResultsError(message)


def close(first: float, second: float, tolerance: float = 2e-12) -> bool:
    return abs(first - second) <= tolerance * max(1.0, abs(first), abs(second))


def coordinates(value: Any, label: str) -> np.ndarray:
    try:
        array = np.asarray(value, dtype=np.float64)
    except (TypeError, ValueError) as error:
        raise ResultsError(f"{label}: invalid coordinates") from error
    require(array.shape == (41, 5), f"{label}: coordinates are not 41 by 5")
    require(np.all(np.isfinite(array)), f"{label}: nonfinite coordinate")
    norms = np.linalg.norm(array, axis=1)
    require(float(np.min(norms)) > 1e-12, f"{label}: zero coordinate row")
    return array


def diagnostics(array: np.ndarray) -> dict[str, Any]:
    norms = np.linalg.norm(array, axis=1)
    array = array / norms[:, None]
    first, second = np.triu_indices(41, 1)
    values = np.sum(array[first] * array[second], axis=1)
    eigenvalues = np.linalg.eigvalsh(array @ array.T)
    return {
        "maximum": float(np.max(values)),
        "minimum": float(np.min(values)),
        "violating_pairs_above_half": int(np.sum(values > 0.5)),
        "pairs_within_1e-6_of_maximum": int(
            np.sum(values >= float(np.max(values)) - 1e-6)
        ),
        "quantiles": {
            str(level): float(np.quantile(values, level))
            for level in (0.5, 0.9, 0.95, 0.99)
        },
        "gram_eigenvalues": [float(value) for value in eigenvalues],
        "maximum_norm_error": float(
            np.max(np.abs(np.linalg.norm(array, axis=1) - 1.0))
        ),
        "coordinate_sha256_float64": hashlib.sha256(
            np.asarray(array, dtype="<f8").tobytes()
        ).hexdigest(),
    }


def compare_diagnostics(
    stored: dict[str, Any],
    recomputed: dict[str, Any],
    label: str,
) -> None:
    require(type(stored) is dict, f"{label}: diagnostics are not an object")
    for key in (
        "maximum",
        "minimum",
        "maximum_norm_error",
    ):
        require(
            close(float(stored[key]), recomputed[key]),
            f"{label}: inconsistent {key}",
        )
    for key in (
        "violating_pairs_above_half",
        "pairs_within_1e-6_of_maximum",
    ):
        require(stored[key] == recomputed[key], f"{label}: inconsistent {key}")
    require(
        stored["coordinate_sha256_float64"]
        == recomputed["coordinate_sha256_float64"],
        f"{label}: coordinate hash mismatch",
    )
    for level, value in recomputed["quantiles"].items():
        require(
            close(float(stored["quantiles"][level]), value),
            f"{label}: inconsistent quantile {level}",
        )
    require(
        len(stored["gram_eigenvalues"]) == 41,
        f"{label}: wrong eigenvalue count",
    )
    require(
        all(
            close(float(first), second, 8e-12)
            for first, second in zip(
                stored["gram_eigenvalues"],
                recomputed["gram_eigenvalues"],
                strict=True,
            )
        ),
        f"{label}: inconsistent Gram eigenvalues",
    )


def verify(
    results_path: Path = RESULTS_PATH,
    expected_results_sha256: str = RESULTS_SHA256,
) -> dict[str, Any]:
    require(
        hashlib.sha256(results_path.read_bytes()).hexdigest()
        == expected_results_sha256,
        "results SHA-256 mismatch",
    )
    result = json.loads(results_path.read_text())
    require(type(result) is dict, "results are not an object")
    require(
        result.get("schema") == "kissing5.k11_k40_seeded_n41_probe.v1",
        "wrong results schema",
    )
    require(result.get("status") == STATUS, "result is not labeled numerical")
    require(
        result.get("classification_sha256") == CLASSIFICATION_SHA256,
        "classification source hash mismatch",
    )
    runs = result.get("runs")
    require(type(runs) is list and len(runs) == 26, "wrong run count")
    require(result.get("run_count") == len(runs), "wrong stored run count")
    require(
        Counter((run["atom_index"], run["mode"]) for run in runs)
        == Counter(
            (atom, mode) for atom in EXPECTED_ATOMS for mode in EXPECTED_MODES
        ),
        "portfolio does not contain both modes for all thirteen atoms",
    )

    final_maxima = []
    fixed_holes = {
        (known_type, mode): []
        for known_type in ("D5", "L5")
        for mode in EXPECTED_MODES
    }
    for run_index, run in enumerate(runs):
        label = f"run {run_index}"
        require(run.get("known_type") in ("D5", "L5"), f"{label}: wrong type")
        require(type(run.get("seed")) is int, f"{label}: seed is not integer")
        require(
            run["epigraph_refinement"]["solver_success"],
            f"{label}: final solver did not report success",
        )
        stages = run.get("smooth_history")
        require(type(stages) is list and len(stages) == 5, f"{label}: wrong stages")

        for coordinate_key, diagnostic_key in (
            ("unperturbed_coordinates_float64", "unperturbed_diagnostics"),
            ("initial_coordinates_float64", "initial_diagnostics"),
            ("final_coordinates_float64", "final_diagnostics"),
        ):
            array = coordinates(run.get(coordinate_key), f"{label} {coordinate_key}")
            compare_diagnostics(
                run[diagnostic_key],
                diagnostics(array),
                f"{label} {diagnostic_key}",
            )

        unperturbed_maximum = float(
            run["unperturbed_diagnostics"]["maximum"]
        )
        insertion_maximum = max(
            float(record["best_recomputed_maximum"])
            for record in run["fixed_insertion"]
        )
        require(
            close(unperturbed_maximum, max(0.5, insertion_maximum)),
            f"{label}: fixed-insertion summary is inconsistent",
        )
        fixed_holes[(run["known_type"], run["mode"])].extend(
            float(record["best_recomputed_maximum"])
            for record in run["fixed_insertion"]
        )

        require(
            close(
                float(stages[0]["before_maximum"]),
                float(run["initial_diagnostics"]["maximum"]),
            ),
            f"{label}: first smooth stage has wrong input",
        )
        for previous, current in zip(stages, stages[1:]):
            require(
                close(
                    float(previous["after_maximum"]),
                    float(current["before_maximum"]),
                ),
                f"{label}: smooth stage history is discontinuous",
            )
        require(
            close(
                float(stages[-1]["after_maximum"]),
                float(run["epigraph_refinement"]["before_maximum"]),
            ),
            f"{label}: epigraph input is inconsistent",
        )
        final_maximum = float(run["final_diagnostics"]["maximum"])
        require(
            close(
                final_maximum,
                float(run["epigraph_refinement"]["after_maximum"]),
            ),
            f"{label}: epigraph output is inconsistent",
        )
        require(
            final_maximum > 0.5,
            f"{label}: a putative feasible K41 requires exact certification",
        )
        final_maxima.append(final_maximum)

    best_index = min(range(len(runs)), key=lambda index: final_maxima[index])
    best_run = runs[best_index]
    stored_best = result.get("best")
    require(type(stored_best) is dict, "best summary is not an object")
    require(stored_best.get("run_index") == best_index, "wrong best run index")
    require(
        stored_best.get("atom_index") == best_run["atom_index"]
        and stored_best.get("mode") == best_run["mode"]
        and stored_best.get("seed") == best_run["seed"],
        "wrong best run metadata",
    )
    require(
        close(float(stored_best["maximum"]), final_maxima[best_index]),
        "wrong best maximum",
    )
    rounded_basins = Counter(round(value, 12) for value in final_maxima)
    return {
        "status": "PASS",
        "evidence_status": STATUS,
        "runs_checked": len(runs),
        "coordinate_arrays_recomputed": 3 * len(runs),
        "best_recomputed_maximum": final_maxima[best_index],
        "best_atom": best_run["atom_index"],
        "best_mode": best_run["mode"],
        "distinct_rounded_final_basins": {
            str(value): count for value, count in sorted(rounded_basins.items())
        },
        "fixed_insertion_range_by_type_and_mode": {
            f"{known_type}:{mode}": [min(values), max(values)]
            for (known_type, mode), values in fixed_holes.items()
        },
        "all_runs_remain_above_half": True,
        "results_sha256": expected_results_sha256,
    }


def main() -> None:
    print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
