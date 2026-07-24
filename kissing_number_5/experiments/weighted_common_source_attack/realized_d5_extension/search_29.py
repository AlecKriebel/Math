#!/usr/bin/env python3
"""Deterministic continuous search for 29 extensions of the fixed support.

This is a discovery program, not a proof or a certificate verifier.  It solves
the epigraph problem

    minimize t
    ||y_a|| = 1,
    <y_a,y_b> <= t,
    <y_a,x_i> <= t,

with the twelve support points fixed.  A result with t <= 1/2 would be a
candidate 41-point kissing configuration; a result with t > 1/2 proves
nothing about nonexistence.
"""

import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
import time

import numpy as np
import scipy
from scipy.optimize import minimize

from support import ROOTS, completion_roots


SCHEMA = "kissing5.realized_d5_extension.search29.v1"
STATUS = "NUMERICAL_EVIDENCE_ONLY"
POINTS = 29
DIMENSION = 5
SUPPORT = np.asarray(ROOTS, dtype=float) / np.sqrt(2.0)
KNOWN_28 = np.asarray(completion_roots(), dtype=float) / np.sqrt(2.0)
PAIR_I, PAIR_J = np.triu_indices(POINTS, 1)
PAIR_COUNT = len(PAIR_I)
SUPPORT_CONSTRAINT_COUNT = POINTS * len(SUPPORT)


def unpack(vector):
    return vector[:-1].reshape(POINTS, DIMENSION), float(vector[-1])


def objective(vector):
    return float(vector[-1])


def objective_jacobian(vector):
    answer = np.zeros_like(vector)
    answer[-1] = 1.0
    return answer


def norm_equalities(vector):
    points, _ = unpack(vector)
    return np.sum(points * points, axis=1) - 1.0


def norm_jacobian(vector):
    points, _ = unpack(vector)
    answer = np.zeros((POINTS, len(vector)))
    for index in range(POINTS):
        answer[index, DIMENSION * index : DIMENSION * (index + 1)] = (
            2.0 * points[index]
        )
    return answer


def epigraph_inequalities(vector):
    points, threshold = unpack(vector)
    pair_values = np.sum(points[PAIR_I] * points[PAIR_J], axis=1)
    support_values = (points @ SUPPORT.T).ravel()
    return np.r_[threshold - pair_values, threshold - support_values]


def epigraph_jacobian(vector):
    points, _ = unpack(vector)
    answer = np.zeros(
        (PAIR_COUNT + SUPPORT_CONSTRAINT_COUNT, len(vector)), dtype=float
    )
    for row, (left, right) in enumerate(zip(PAIR_I, PAIR_J)):
        answer[row, DIMENSION * left : DIMENSION * (left + 1)] = -points[right]
        answer[row, DIMENSION * right : DIMENSION * (right + 1)] = -points[left]
    answer[:PAIR_COUNT, -1] = 1.0
    row = PAIR_COUNT
    for point in range(POINTS):
        for anchor in SUPPORT:
            answer[
                row, DIMENSION * point : DIMENSION * (point + 1)
            ] = -anchor
            answer[row, -1] = 1.0
            row += 1
    return answer


CONSTRAINTS = (
    {"type": "eq", "fun": norm_equalities, "jac": norm_jacobian},
    {
        "type": "ineq",
        "fun": epigraph_inequalities,
        "jac": epigraph_jacobian,
    },
)


def random_polar_point(rng):
    while True:
        point = rng.normal(size=DIMENSION)
        point /= np.linalg.norm(point)
        if np.max(SUPPORT @ point) <= 0.5:
            return point


def initial_points(rng, run, portfolio):
    noise_schedule = (0.005, 0.0125, 0.025, 0.05, 0.1, 0.2)
    if portfolio == "legacy":
        if run % 5:
            noise = noise_schedule[run % len(noise_schedule)]
            points = np.vstack((KNOWN_28, random_polar_point(rng)))
            points += noise * rng.normal(size=points.shape)
            mode = "d5_completion_plus_one"
        else:
            noise = None
            points = np.vstack([random_polar_point(rng) for _ in range(POINTS)])
            mode = "independent_polar_points"
        points /= np.linalg.norm(points, axis=1)[:, None]
        return points, mode, noise
    if portfolio != "diverse":
        raise ValueError("unknown initialization portfolio: %s" % portfolio)
    if run % 7:
        noise = noise_schedule[run % len(noise_schedule)]
        removed = 1 + (run % 8)
        retained_indices = np.sort(
            rng.choice(len(KNOWN_28), size=len(KNOWN_28) - removed, replace=False)
        )
        additions = np.vstack(
            [random_polar_point(rng) for _ in range(removed + 1)]
        )
        points = np.vstack((KNOWN_28[retained_indices], additions))
        points += noise * rng.normal(size=points.shape)
        mode = "d5_surgery_remove_%d_add_%d" % (removed, removed + 1)
    else:
        noise = None
        points = np.vstack([random_polar_point(rng) for _ in range(POINTS)])
        mode = "independent_polar_points"
    points /= np.linalg.norm(points, axis=1)[:, None]
    return points, mode, noise


def diagnostics(points):
    pair_values = np.sum(points[PAIR_I] * points[PAIR_J], axis=1)
    support_values = (points @ SUPPORT.T).ravel()
    all_values = np.r_[pair_values, support_values]
    frame = points.T @ points
    centroid = np.sum(points, axis=0)
    return {
        "maximum": float(np.max(all_values)),
        "maximum_extension_pair": float(np.max(pair_values)),
        "maximum_support_pair": float(np.max(support_values)),
        "minimum_inner_product": float(np.min(all_values)),
        "norm_error": float(np.max(np.abs(np.sum(points * points, axis=1) - 1))),
        "active_within_1e-7": int(np.sum(all_values >= np.max(all_values) - 1e-7)),
        "frame_eigenvalues": [
            float(value) for value in np.linalg.eigvalsh(frame)[::-1]
        ],
        "frame_potential": float(np.sum(frame * frame)),
        "centroid_squared_norm": float(centroid @ centroid),
        "v_trace": float(frame[0, 0] + frame[4, 4]),
    }


def run_search(seed, runs, maxiter, ftol, portfolio):
    rng = np.random.default_rng(seed)
    records = []
    best = None
    started = time.time()
    for run in range(runs):
        points, mode, noise = initial_points(rng, run, portfolio)
        initial_diagnostics = diagnostics(points)
        initial_threshold = initial_diagnostics["maximum"] + 0.01
        vector = np.r_[points.ravel(), initial_threshold]
        run_started = time.time()
        result = minimize(
            objective,
            vector,
            jac=objective_jacobian,
            constraints=CONSTRAINTS,
            method="SLSQP",
            options={"ftol": ftol, "maxiter": maxiter, "disp": False},
        )
        optimized, reported_threshold = unpack(result.x)
        final_diagnostics = diagnostics(optimized)
        record = {
            "run": run,
            "mode": mode,
            "noise": noise,
            "success": bool(result.success),
            "status_code": int(result.status),
            "message": str(result.message),
            "iterations": int(result.nit),
            "reported_threshold": float(reported_threshold),
            "initial": initial_diagnostics,
            "final": final_diagnostics,
            "elapsed_seconds": time.time() - run_started,
        }
        records.append(record)
        if best is None or final_diagnostics["maximum"] < best["diagnostics"]["maximum"]:
            best = {
                "run": run,
                "reported_threshold": float(reported_threshold),
                "diagnostics": final_diagnostics,
                "coordinates": optimized.tolist(),
            }
        print(
            "run %d/%d: max %.15f (%s, %d iterations)"
            % (
                run + 1,
                runs,
                final_diagnostics["maximum"],
                "success" if result.success else "solver warning",
                result.nit,
            ),
            flush=True,
        )
    return {
        "schema": SCHEMA,
        "status": STATUS,
        "scope_warning": (
            "Failure to reach 1/2 is not a nonexistence proof.  Coordinates "
            "and solver statuses are floating-point discovery evidence only."
        ),
        "problem": {
            "fixed_support_points": 12,
            "moving_points": POINTS,
            "dimension": DIMENSION,
            "target_maximum": 0.5,
        },
        "parameters": {
            "seed": seed,
            "runs": runs,
            "maxiter": maxiter,
            "ftol": ftol,
            "portfolio": portfolio,
        },
        "versions": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
        },
        "elapsed_seconds": time.time() - started,
        "best": best,
        "runs": records,
    }


def canonical_json_bytes(data):
    return (json.dumps(data, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=2026072401)
    parser.add_argument("--runs", type=int, default=24)
    parser.add_argument("--maxiter", type=int, default=1800)
    parser.add_argument("--ftol", type=float, default=1e-11)
    parser.add_argument(
        "--portfolio", choices=("diverse", "legacy"), default="diverse"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "search_29_result.json",
    )
    args = parser.parse_args(argv)
    result = run_search(
        args.seed, args.runs, args.maxiter, args.ftol, args.portfolio
    )
    payload = canonical_json_bytes(result)
    args.output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    print("wrote %s" % args.output)
    print("sha256 %s" % digest)
    print("best maximum %.17g" % result["best"]["diagnostics"]["maximum"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
