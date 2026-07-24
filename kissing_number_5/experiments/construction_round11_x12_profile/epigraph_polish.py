#!/usr/bin/env python3
"""Direct minimax polish of released round-11 representatives.

The profile penalties are absent from every optimization in this file.
SLSQP is used only as a local diagnostic after the profile-guided,
replica-exchange, and topology-changing searches.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import time

import numpy as np
from scipy.optimize import minimize


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = HERE / "results" / "portfolio.json"
OUTPUT = HERE / "results" / "epigraph_polished.json"
SPEC = importlib.util.spec_from_file_location(
    "round11_search", HERE / "search.py"
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load round-11 search helpers")
search = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(search)


def epigraph_refine(
    array: np.ndarray, maximum_iterations: int
) -> tuple[np.ndarray, dict[str, object]]:
    array = search.normalized(array)
    cardinality = len(array)
    first, second = search.pair_indices(cardinality)
    initial = np.r_[array.ravel(), search.max_inner(array)]

    def objective(variable: np.ndarray) -> float:
        return float(variable[-1])

    def objective_jac(variable: np.ndarray) -> np.ndarray:
        answer = np.zeros_like(variable)
        answer[-1] = 1
        return answer

    def inequalities(variable: np.ndarray) -> np.ndarray:
        points = variable[:-1].reshape(cardinality, 5)
        return variable[-1] - np.sum(
            points[first] * points[second], axis=1
        )

    def inequalities_jac(variable: np.ndarray) -> np.ndarray:
        points = variable[:-1].reshape(cardinality, 5)
        answer = np.zeros((len(first), len(variable)))
        rows = np.arange(len(first))
        for coordinate in range(5):
            answer[rows, 5 * first + coordinate] = -points[
                second, coordinate
            ]
            answer[rows, 5 * second + coordinate] = -points[
                first, coordinate
            ]
        answer[:, -1] = 1
        return answer

    def equalities(variable: np.ndarray) -> np.ndarray:
        points = variable[:-1].reshape(cardinality, 5)
        return np.sum(points * points, axis=1) - 1

    def equalities_jac(variable: np.ndarray) -> np.ndarray:
        points = variable[:-1].reshape(cardinality, 5)
        answer = np.zeros((cardinality, len(variable)))
        rows = np.arange(cardinality)
        for coordinate in range(5):
            answer[rows, 5 * rows + coordinate] = (
                2 * points[:, coordinate]
            )
        return answer

    result = minimize(
        objective,
        initial,
        jac=objective_jac,
        constraints=[
            {
                "type": "ineq",
                "fun": inequalities,
                "jac": inequalities_jac,
            },
            {
                "type": "eq",
                "fun": equalities,
                "jac": equalities_jac,
            },
        ],
        method="SLSQP",
        options={
            "maxiter": maximum_iterations,
            "ftol": 2.0e-13,
            "disp": False,
        },
    )
    answer = search.normalized(
        result.x[:-1].reshape(cardinality, 5)
    )
    return answer, {
        "success": bool(result.success),
        "status": int(result.status),
        "message": str(result.message),
        "iterations": int(result.nit),
        "reported_epigraph": float(result.x[-1]),
        "recomputed_maximum": search.max_inner(answer),
    }


def candidate_records(source: dict[str, object]):
    for run in source["runs"]:
        final = run["phases"][-1]["best_maximum_representative"]
        yield run, "released_best_maximum", final
        if run["kind"] == "profile_guided":
            blend = next(
                phase
                for phase in run["phases"]
                if phase["phase"] == "profile_blend"
            )
            yield run, "profile_blend_best_profile", blend[
                "best_profile_representative"
            ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--maxiter", type=int, default=900)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    source_bytes = args.source.read_bytes()
    source = json.loads(source_bytes)
    started = time.time()
    records = []
    for run, locator, candidate in candidate_records(source):
        initial = np.asarray(candidate["coordinates_float64"], dtype=float)
        print(
            f"N={run['cardinality']} {run['kind']} {locator} "
            f"initial={search.max_inner(initial):.12f}",
            flush=True,
        )
        polished, solver = epigraph_refine(initial, args.maxiter)
        if search.max_inner(polished) <= search.max_inner(initial):
            retained = polished
            retained_from = "slsqp"
        else:
            retained = initial
            retained_from = "initial"
        print(
            f"N={run['cardinality']} {run['kind']} {locator} "
            f"polished={search.max_inner(polished):.12f}",
            flush=True,
        )
        records.append(
            {
                "cardinality": run["cardinality"],
                "kind": run["kind"],
                "source_locator": locator,
                "profile_penalties": 0,
                "initial": {
                    **search.diagnostics(initial),
                    "coordinates_float64": initial.tolist(),
                },
                "solver": solver,
                "polished": {
                    **search.diagnostics(polished),
                    "coordinates_float64": polished.tolist(),
                },
                "retained_from": retained_from,
                "retained": {
                    **search.diagnostics(retained),
                    "coordinates_float64": retained.tolist(),
                },
            }
        )
    output = {
        "schema": "kissing5.construction_round11_x12_epigraph_polish.v1",
        "evidence_status": (
            "NUMERICAL EVIDENCE ONLY; NOT AN EXACT CONFIGURATION CERTIFICATE"
        ),
        "source": str(args.source.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "maximum_iterations": args.maxiter,
        "profile_penalties": 0,
        "records": records,
        "elapsed_seconds": time.time() - started,
        "exact_candidate_found": any(
            record["retained"]["maximum_inner_product"] <= 0.5
            for record in records
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    main()
