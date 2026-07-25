#!/usr/bin/env python3
"""Riemannian active-bundle search for spherical minimax codes.

This is numerical discovery code, not a proof.  It minimizes

    max_{i<j} <x_i,x_j>,   x_i in S^4,

using two genuinely different local models.  Log-sum-exp continuation first
enters a useful contact basin.  A nonsmooth phase then solves a proximal
bundle quadratic program for the currently important pair constraints and
retracts the proposed tangent step onto the product of spheres.  Deterministic
facet-escape kicks deliberately cross contact-combinatorics boundaries before
the bundle model is rebuilt.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import platform
import sys
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import minimize


DIMENSION = 5
STATUS = "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE"


def unit_rows(array: np.ndarray) -> np.ndarray:
    array = np.asarray(array, dtype=float)
    if array.ndim != 2 or array.shape[1] != DIMENSION:
        raise ValueError("coordinates must be an N by 5 array")
    norms = np.linalg.norm(array, axis=1)
    if float(np.min(norms)) <= 1e-13:
        raise ValueError("cannot normalize a zero row")
    return array / norms[:, None]


def pair_indices(n: int) -> tuple[np.ndarray, np.ndarray]:
    return np.triu_indices(n, 1)


def pair_values(array: np.ndarray) -> np.ndarray:
    x = unit_rows(array)
    ii, jj = pair_indices(len(x))
    return np.sum(x[ii] * x[jj], axis=1)


def maximum(array: np.ndarray) -> float:
    return float(np.max(pair_values(array)))


def tangent_noise(
    x: np.ndarray, rng: np.random.Generator, scale: float, weights=None
) -> np.ndarray:
    x = unit_rows(x)
    noise = rng.normal(size=x.shape)
    noise -= np.sum(noise * x, axis=1)[:, None] * x
    if weights is not None:
        noise *= np.asarray(weights)[:, None]
    return unit_rows(x + scale * noise)


def smooth_max_value_gradient(flat: np.ndarray, n: int, beta: float):
    """Log-sum-exp objective and exact Euclidean gradient through normalization."""
    raw = np.asarray(flat, dtype=float).reshape(n, DIMENSION)
    norms = np.linalg.norm(raw, axis=1)
    if float(np.min(norms)) <= 1e-13:
        return 1e30, np.zeros_like(flat)
    x = raw / norms[:, None]
    ii, jj = pair_indices(n)
    values = np.sum(x[ii] * x[jj], axis=1)
    top = float(np.max(values))
    exponentials = np.exp(beta * (values - top))
    weights = exponentials / float(np.sum(exponentials))
    value = top + math.log(float(np.sum(exponentials))) / beta
    ambient = np.zeros_like(x)
    np.add.at(ambient, ii, weights[:, None] * x[jj])
    np.add.at(ambient, jj, weights[:, None] * x[ii])
    tangent = ambient - np.sum(ambient * x, axis=1)[:, None] * x
    return float(value), (tangent / norms[:, None]).ravel()


def smooth_continuation(
    x: np.ndarray,
    betas: tuple[float, ...],
    iterations: int,
) -> tuple[np.ndarray, list[dict]]:
    x = unit_rows(x)
    history = []
    for beta in betas:
        result = minimize(
            smooth_max_value_gradient,
            x.ravel(),
            args=(len(x), float(beta)),
            jac=True,
            method="L-BFGS-B",
            options={
                "maxiter": int(iterations),
                "ftol": 2e-15,
                "gtol": 2e-9,
                "maxls": 60,
                "maxcor": 35,
            },
        )
        x = unit_rows(result.x.reshape(len(x), DIMENSION))
        history.append(
            {
                "beta": float(beta),
                "iterations": int(result.nit),
                "evaluations": int(result.nfev),
                "success": bool(result.success),
                "message": str(result.message),
                "smooth_value": float(result.fun),
                "true_maximum": maximum(x),
                "contact_graph": contact_summary(x, 1e-6, include_edges=False),
            }
        )
    return x, history


def pair_tangent_gradients(x: np.ndarray, edge_ids: np.ndarray) -> np.ndarray:
    """Rows are product-sphere tangent gradients of selected pair products."""
    x = unit_rows(x)
    ii, jj = pair_indices(len(x))
    chosen_i = ii[edge_ids]
    chosen_j = jj[edge_ids]
    products = np.sum(x[chosen_i] * x[chosen_j], axis=1)
    gradients = np.zeros((len(edge_ids), x.size))
    for row, (first, second, product) in enumerate(
        zip(chosen_i, chosen_j, products)
    ):
        gradients[row, DIMENSION * first : DIMENSION * (first + 1)] = (
            x[second] - product * x[first]
        )
        gradients[row, DIMENSION * second : DIMENSION * (second + 1)] = (
            x[first] - product * x[second]
        )
    return gradients


def project_simplex(vector: np.ndarray) -> np.ndarray:
    """Euclidean projection onto the probability simplex."""
    vector = np.asarray(vector, dtype=float)
    ordered = np.sort(vector)[::-1]
    partial = np.cumsum(ordered) - 1.0
    indices = np.arange(1, len(vector) + 1)
    positive = ordered - partial / indices > 0.0
    rho = int(np.flatnonzero(positive)[-1])
    threshold = partial[rho] / float(rho + 1)
    projected = np.maximum(vector - threshold, 0.0)
    projected /= float(np.sum(projected))
    return projected


def simplex_quadratic_away_frank_wolfe(
    gradients: np.ndarray,
    offsets: np.ndarray,
    multiplier: float,
    initial: np.ndarray,
    max_iterations: int = 900,
) -> tuple[np.ndarray, dict]:
    """Solve the convex bundle dual by an away-step Frank--Wolfe method.

    Matrix-vector products use the thin pair-gradient matrix rather than a
    dense cut-by-cut Hessian.  Away steps identify and delete obsolete bundle
    cuts, making this both an active-set method and substantially faster than
    a generic constrained optimizer.
    """
    alpha = project_simplex(initial)
    gap = math.inf
    away_steps = 0
    for iteration in range(max_iterations):
        combination = alpha @ gradients
        gradient = multiplier * (gradients @ combination) - offsets
        average = float(gradient @ alpha)
        toward = int(np.argmin(gradient))
        fw_gap = average - float(gradient[toward])
        active = np.flatnonzero(alpha > 2e-15)
        away = int(active[np.argmax(gradient[active])])
        away_gap = float(gradient[away]) - average
        gap = max(fw_gap, 0.0)
        if gap < 2e-10:
            break
        if away_gap > fw_gap and alpha[away] < 1.0 - 2e-15:
            direction_alpha = alpha.copy()
            direction_alpha[away] -= 1.0
            direction_combination = combination - gradients[away]
            gamma_max = float(alpha[away] / (1.0 - alpha[away]))
            away_steps += 1
        else:
            direction_alpha = -alpha
            direction_alpha[toward] += 1.0
            direction_combination = gradients[toward] - combination
            gamma_max = 1.0
        derivative = float(gradient @ direction_alpha)
        curvature = multiplier * float(
            direction_combination @ direction_combination
        )
        if curvature <= 1e-30:
            gamma = gamma_max
        else:
            gamma = min(gamma_max, max(0.0, -derivative / curvature))
        if gamma <= 1e-16:
            break
        alpha += gamma * direction_alpha
        alpha[alpha < 2e-15] = 0.0
        alpha /= float(np.sum(alpha))
    combination = alpha @ gradients
    objective = float(
        0.5 * multiplier * (combination @ combination) - offsets @ alpha
    )
    return alpha, {
        "success": gap < 2e-7,
        "iterations": iteration + 1,
        "frank_wolfe_gap": gap,
        "away_steps": away_steps,
        "objective": objective,
    }


def solve_proximal_bundle(
    x: np.ndarray,
    radius: float,
    band: float,
    max_cuts: int = 240,
    warm_alpha: np.ndarray | None = None,
) -> tuple[np.ndarray, dict]:
    """Solve a dual proximal bundle QP for near-active pair constraints.

    If ``a_e=f_e(x)-max(f(x))`` and ``g_e`` is the Riemannian gradient, the
    local model is

        min_d max_e (a_e + g_e d) + ||d||^2/(2 mu).

    Its simplex dual is solved by SLSQP.  ``mu`` is adjusted so the tangent
    proposal fits the requested trust radius.
    """
    x = unit_rows(x)
    values = pair_values(x)
    top = float(np.max(values))
    order = np.argsort(values)[::-1]
    active_count = int(np.sum(values >= top - band))
    cut_count = min(max(max(active_count, 12), min(48, len(order))), max_cuts)
    edge_ids = np.asarray(order[:cut_count], dtype=int)
    offsets = values[edge_ids] - top
    gradients = pair_tangent_gradients(x, edge_ids)
    size = len(edge_ids)
    if warm_alpha is None or len(warm_alpha) != size:
        alpha0 = np.zeros(size)
        exact = np.flatnonzero(offsets >= -1e-11)
        alpha0[exact if len(exact) else [0]] = 1.0 / max(1, len(exact))
    else:
        alpha0 = np.maximum(np.asarray(warm_alpha), 0.0)
        alpha0 /= float(np.sum(alpha0))

    multiplier = max(radius, 1e-8)
    solve_record = None
    alpha = alpha0
    direction = np.zeros(x.size)
    for _ in range(3):
        alpha, solve_record = simplex_quadratic_away_frank_wolfe(
            gradients,
            offsets,
            multiplier,
            alpha,
        )
        direction = -multiplier * (alpha @ gradients)
        direction_norm = float(np.linalg.norm(direction))
        if direction_norm <= radius * 1.02 or direction_norm <= 1e-15:
            break
        multiplier *= radius / direction_norm

    direction_norm = float(np.linalg.norm(direction))
    linear_values = offsets + gradients @ direction
    model_peak = float(np.max(linear_values))
    model_with_prox = model_peak + (
        direction_norm**2 / (2.0 * multiplier)
        if multiplier > 0.0
        else math.inf
    )
    support = np.flatnonzero(alpha > 1e-7)
    ii, jj = pair_indices(len(x))
    return direction.reshape(x.shape), {
        "cut_count": int(size),
        "band_active_count": active_count,
        "radius": float(radius),
        "proximal_multiplier": float(multiplier),
        "direction_norm": direction_norm,
        "model_peak": model_peak,
        "model_with_prox": float(model_with_prox),
        "dual_success": bool(solve_record["success"]),
        "dual_iterations": int(solve_record["iterations"]),
        "dual_frank_wolfe_gap": float(solve_record["frank_wolfe_gap"]),
        "dual_away_steps": int(solve_record["away_steps"]),
        "dual_objective": float(solve_record["objective"]),
        "dual_support_size": int(len(support)),
        "dual_support_edges": [
            [int(ii[edge_ids[k]]), int(jj[edge_ids[k]])] for k in support
        ],
        "dual_support_weights": [float(alpha[k]) for k in support],
    }


def retract(x: np.ndarray, tangent: np.ndarray) -> np.ndarray:
    """Second-order product-sphere retraction."""
    x = unit_rows(x)
    tangent = tangent - np.sum(tangent * x, axis=1)[:, None] * x
    return unit_rows(x + tangent)


def bundle_refine(
    x: np.ndarray,
    iterations: int,
    initial_radius: float = 0.08,
) -> tuple[np.ndarray, list[dict]]:
    """Trust/rejection loop for the nonsmooth pair-constraint bundle."""
    x = unit_rows(x)
    radius = float(initial_radius)
    history = []
    stagnation = 0
    bands = (3e-3, 1e-3, 3e-4, 1e-4, 3e-5, 1e-5)
    for iteration in range(iterations):
        before = maximum(x)
        band = max(bands[min(iteration // 12, len(bands) - 1)], 2.5 * radius**2)
        accepted = False
        attempt_summaries = []
        for attempt in range(7):
            direction, record = solve_proximal_bundle(
                x, radius=radius, band=band
            )
            trial = retract(x, direction)
            after = maximum(trial)
            actual_drop = before - after
            predicted_drop = max(0.0, -record["model_peak"])
            ratio = (
                actual_drop / predicted_drop
                if predicted_drop > 1e-16
                else -math.inf
            )
            record.update(
                {
                    "attempt": attempt,
                    "trial_maximum": after,
                    "actual_drop": actual_drop,
                    "predicted_drop": predicted_drop,
                    "agreement_ratio": (
                        float(ratio) if math.isfinite(ratio) else None
                    ),
                }
            )
            support_digest = hashlib.sha256(
                json.dumps(
                    record["dual_support_edges"], separators=(",", ":")
                ).encode()
            ).hexdigest()
            attempt_summaries.append(
                {
                    "attempt": attempt,
                    "cut_count": record["cut_count"],
                    "band_active_count": record["band_active_count"],
                    "radius": record["radius"],
                    "proximal_multiplier": record[
                        "proximal_multiplier"
                    ],
                    "direction_norm": record["direction_norm"],
                    "model_peak": record["model_peak"],
                    "model_with_prox": record["model_with_prox"],
                    "dual_success": record["dual_success"],
                    "dual_iterations": record["dual_iterations"],
                    "dual_frank_wolfe_gap": record[
                        "dual_frank_wolfe_gap"
                    ],
                    "dual_away_steps": record["dual_away_steps"],
                    "dual_support_size": record["dual_support_size"],
                    "dual_support_edge_sha256": support_digest,
                    "trial_maximum": after,
                    "actual_drop": actual_drop,
                    "predicted_drop": predicted_drop,
                    "agreement_ratio": record["agreement_ratio"],
                }
            )
            if actual_drop > max(2e-14, 0.02 * predicted_drop):
                x = trial
                accepted = True
                if ratio > 0.65:
                    radius = min(0.14, radius * 1.45)
                elif ratio < 0.20:
                    radius *= 0.65
                stagnation = 0
                break
            radius *= 0.45
        if not accepted:
            stagnation += 1
            radius = max(radius, 2e-7)
        history.append(
            {
                "iteration": iteration,
                "before_maximum": before,
                "after_maximum": maximum(x),
                "band": float(band),
                "accepted": accepted,
                "next_radius": float(radius),
                "attempt_count": len(attempt_summaries),
                # The accepted attempt, or the smallest-radius rejected
                # attempt, contains the decisive trust-region diagnostic.
                "decisive_attempt": attempt_summaries[-1],
                "contact_graph": contact_summary(x, 1e-6, include_edges=False),
            }
        )
        if stagnation >= 4 or radius < 1e-8:
            break
    return x, history


def d5_roots() -> np.ndarray:
    rows = []
    for first in range(DIMENSION):
        for second in range(first + 1, DIMENSION):
            for sign_first in (-1.0, 1.0):
                for sign_second in (-1.0, 1.0):
                    row = np.zeros(DIMENSION)
                    row[first] = sign_first / math.sqrt(2.0)
                    row[second] = sign_second / math.sqrt(2.0)
                    rows.append(row)
    return np.asarray(rows)


def farthest_insert(
    x: np.ndarray, target_n: int, rng: np.random.Generator, samples: int = 30000
) -> np.ndarray:
    x = unit_rows(x)
    while len(x) < target_n:
        candidates = unit_rows(rng.normal(size=(samples, DIMENSION)))
        score = np.max(candidates @ x.T, axis=1)
        x = np.vstack([x, candidates[int(np.argmin(score))]])
    return x


def load_runs(path: Path) -> list[tuple[int, np.ndarray, str, float]]:
    """Read all coordinate layouts used by earlier construction rounds."""
    with path.open() as stream:
        payload = json.load(stream)
    answer = []
    for index, record in enumerate(payload.get("runs", [])):
        raw = None
        if "coordinates" in record:
            raw = record["coordinates"]
        elif "coordinates_float64" in record:
            raw = record["coordinates_float64"]
        elif isinstance(record.get("best"), dict):
            raw = record["best"].get("coordinates_float64")
        if raw is None:
            continue
        x = unit_rows(np.asarray(raw, dtype=float))
        answer.append(
            (len(x), x, f"{path.name}:run{index}", maximum(x))
        )
    return answer


def connected_components(n: int, edges: list[list[int]]) -> list[int]:
    adjacency = [[] for _ in range(n)]
    for first, second in edges:
        adjacency[first].append(second)
        adjacency[second].append(first)
    seen = set()
    sizes = []
    for start in range(n):
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        size = 0
        while stack:
            vertex = stack.pop()
            size += 1
            for neighbor in adjacency[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        sizes.append(size)
    return sorted(sizes, reverse=True)


def contact_summary(
    x: np.ndarray, tolerance: float, include_edges: bool = True
) -> dict:
    x = unit_rows(x)
    values = pair_values(x)
    top = float(np.max(values))
    ii, jj = pair_indices(len(x))
    chosen = values >= top - tolerance
    edges = np.column_stack([ii[chosen], jj[chosen]]).tolist()
    degrees = np.bincount(np.asarray(edges, dtype=int).ravel(), minlength=len(x))
    unique, counts = np.unique(degrees, return_counts=True)
    canonical = json.dumps(edges, separators=(",", ":")).encode()
    answer = {
        "tolerance": float(tolerance),
        "edge_count": int(len(edges)),
        "degree_histogram": {
            str(int(degree)): int(count)
            for degree, count in zip(unique, counts)
        },
        "component_sizes": connected_components(len(x), edges),
        "edge_sha256": hashlib.sha256(canonical).hexdigest(),
    }
    if include_edges:
        answer["edges"] = edges
    return answer


def diagnostics(x: np.ndarray) -> dict:
    x = unit_rows(x)
    gram = x @ x.T
    ii, jj = pair_indices(len(x))
    values = gram[ii, jj]
    top = float(np.max(values))
    answer = {
        "n": len(x),
        "maximum": top,
        "gap_above_one_half": top - 0.5,
        "minimum": float(np.min(values)),
        "row_norm_max_error": float(
            np.max(np.abs(np.sum(x * x, axis=1) - 1.0))
        ),
        "deep_negative_pairs_below_minus_half": int(np.sum(values < -0.5)),
        "pair_quantiles": {
            f"{q:.3f}": float(np.quantile(values, q))
            for q in (0.0, 0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99, 1.0)
        },
        "gram_eigenvalues": np.linalg.eigvalsh(gram).tolist(),
        "coordinates_float64": x.tolist(),
    }
    for tolerance in (1e-4, 1e-6, 1e-8):
        answer[f"active_{tolerance:.0e}"] = contact_summary(
            x, tolerance, include_edges=True
        )
    exact_ids = np.flatnonzero(values >= top - 1e-8)
    gradients = pair_tangent_gradients(x, exact_ids)
    q = gradients @ gradients.T
    size = len(exact_ids)
    initial = np.ones(size) / size
    result = minimize(
        lambda alpha: float(0.5 * alpha @ q @ alpha),
        initial,
        jac=lambda alpha: q @ alpha,
        method="SLSQP",
        bounds=[(0.0, 1.0)] * size,
        constraints={
            "type": "eq",
            "fun": lambda alpha: float(np.sum(alpha) - 1.0),
            "jac": lambda alpha: np.ones_like(alpha),
        },
        options={"maxiter": 500, "ftol": 1e-14, "disp": False},
    )
    alpha = np.maximum(result.x, 0.0)
    alpha /= float(np.sum(alpha))
    answer["clarke_stationarity_1e-8"] = {
        "active_count": int(size),
        "minimum_convex_gradient_norm": float(
            np.linalg.norm(alpha @ gradients)
        ),
        "positive_multiplier_count_1e-7": int(np.sum(alpha > 1e-7)),
        "solver_success": bool(result.success),
        "solver_message": str(result.message),
    }
    return answer


def graph_jaccard(first: dict, second: dict) -> float:
    a = {tuple(edge) for edge in first["edges"]}
    b = {tuple(edge) for edge in second["edges"]}
    return float(len(a & b) / len(a | b)) if a or b else 1.0


def run_trajectory(
    n: int,
    seed: int,
    origin: str,
    initial: np.ndarray,
    smooth_iterations: int,
    bundle_iterations: int,
    escapes: int,
) -> dict:
    rng = np.random.default_rng(seed)
    started = time.time()
    initial = unit_rows(initial)
    seed_contact = contact_summary(initial, 1e-6, include_edges=True)
    x, smooth = smooth_continuation(
        initial,
        (24.0, 72.0, 216.0, 648.0, 1944.0, 5832.0),
        smooth_iterations,
    )
    x, first_bundle = bundle_refine(x, bundle_iterations)
    endpoints = [
        {
            "label": "seed_baseline",
            "maximum": maximum(initial),
            "contact": seed_contact,
        },
        {
            "label": "initial_bundle",
            "maximum": maximum(x),
            "contact": contact_summary(x, 1e-6, include_edges=True),
        }
    ]
    phases = []
    if maximum(initial) <= maximum(x):
        best = initial.copy()
    else:
        best = x.copy()
    best_maximum = maximum(best)
    for escape_index in range(escapes):
        graph = contact_summary(x, 2e-4, include_edges=True)
        degrees = np.zeros(n)
        for first, second in graph["edges"]:
            degrees[first] += 1.0
            degrees[second] += 1.0
        max_degree = max(float(np.max(degrees)), 1.0)
        row_weights = 0.35 + (max_degree - degrees) / max_degree
        scale = (0.006, 0.016, 0.035, 0.07)[
            escape_index % 4
        ]
        kicked = tangent_noise(x, rng, scale, row_weights)
        kicked_maximum = maximum(kicked)
        candidate, smooth_escape = smooth_continuation(
            kicked,
            (288.0, 1152.0, 4608.0),
            max(80, smooth_iterations // 2),
        )
        candidate, bundle_escape = bundle_refine(
            candidate, bundle_iterations, initial_radius=0.055
        )
        candidate_maximum = maximum(candidate)
        accepted = candidate_maximum < best_maximum
        if accepted:
            best = candidate.copy()
            best_maximum = candidate_maximum
        # Continue from every escaped basin, including uphill ones.  This is
        # what permits a later escape to traverse a different contact complex.
        x = candidate
        endpoint = {
            "label": f"escape_{escape_index}",
            "maximum": candidate_maximum,
            "contact": contact_summary(candidate, 1e-6, include_edges=True),
        }
        endpoints.append(endpoint)
        phases.append(
            {
                "escape": escape_index,
                "scale": scale,
                "kicked_maximum": kicked_maximum,
                "smooth_history": smooth_escape,
                "bundle_history": bundle_escape,
                "endpoint_maximum": candidate_maximum,
                "accepted_as_run_best": accepted,
            }
        )
    persistence = []
    for first, second in zip(endpoints, endpoints[1:]):
        persistence.append(
            {
                "from": first["label"],
                "to": second["label"],
                "jaccard_1e-6": graph_jaccard(
                    first["contact"], second["contact"]
                ),
                "same_edge_hash": (
                    first["contact"]["edge_sha256"]
                    == second["contact"]["edge_sha256"]
                ),
            }
        )
    return {
        "n": n,
        "seed": int(seed),
        "origin": origin,
        "initial_maximum": maximum(initial),
        "smooth_history": smooth,
        "initial_bundle_history": first_bundle,
        "escape_phases": phases,
        "contact_endpoint_persistence": persistence,
        "best": diagnostics(best),
        "elapsed_seconds": time.time() - started,
    }


def halfspace_depth_probe(x: np.ndarray, tolerance: float = 1e-10) -> dict:
    """Numerically enumerate origin hyperplanes supported by four points.

    This is a diagnostic only.  Near-degeneracies are retained as boundary
    points rather than assigned a sign.
    """
    x = unit_rows(x)
    best = None
    histograms: dict[str, int] = {}
    examined = 0
    skipped = 0
    for indices in itertools.combinations(range(len(x)), 4):
        rows = x[list(indices)]
        _, singular, right = np.linalg.svd(rows, full_matrices=True)
        if singular[-1] < 1e-10:
            skipped += 1
            continue
        normal = right[-1]
        dots = x @ normal
        positive = int(np.sum(dots > tolerance))
        negative = int(np.sum(dots < -tolerance))
        boundary = len(x) - positive - negative
        split = [min(positive, negative), boundary, max(positive, negative)]
        key = f"{split[0]}/{split[1]}/{split[2]}"
        histograms[key] = histograms.get(key, 0) + 1
        record = {
            "support_indices": list(indices),
            "strict_negative": negative,
            "boundary": boundary,
            "strict_positive": positive,
            "min_strict_side": min(positive, negative),
            "min_closed_side": min(positive + boundary, negative + boundary),
            "normal": normal.tolist(),
            "max_support_residual": float(np.max(np.abs(dots[list(indices)]))),
            "next_nonboundary_abs_dot": float(
                min(
                    (
                        abs(value)
                        for index, value in enumerate(dots)
                        if index not in indices and abs(value) > tolerance
                    ),
                    default=0.0,
                )
            ),
        }
        if best is None or (
            record["min_strict_side"],
            record["min_closed_side"],
            record["boundary"],
        ) < (
            best["min_strict_side"],
            best["min_closed_side"],
            best["boundary"],
        ):
            best = record
        examined += 1
    return {
        "status": STATUS,
        "tolerance": tolerance,
        "hyperplanes_examined": examined,
        "rank_deficient_supports_skipped": skipped,
        "shallowest_split": best,
        "split_histogram": histograms,
        "warning": (
            "Floating-point diagnostic only; boundary classifications and "
            "the completeness of the support enumeration are not certified."
        ),
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def choose_initials(
    n: int,
    seed: int,
    inherited_by_source: list[tuple[str, np.ndarray]],
    random_starts: int,
) -> list[tuple[str, np.ndarray, int]]:
    rng = np.random.default_rng(seed)
    initials = []
    for source, x in inherited_by_source:
        initials.append((f"inherited:{source}", x.copy(), int(rng.integers(2**31))))
    if inherited_by_source:
        best_source, best = min(
            inherited_by_source, key=lambda item: maximum(item[1])
        )
        initials.append(
            (
                f"asymmetric_perturbation:{best_source}",
                tangent_noise(best, rng, 0.055),
                int(rng.integers(2**31)),
            )
        )
    initials.append(
        (
            "D5_plus_farthest_sampled_holes",
            farthest_insert(d5_roots(), n, rng),
            int(rng.integers(2**31)),
        )
    )
    for index in range(random_starts):
        initials.append(
            (
                f"asymmetric_gaussian_{index}",
                unit_rows(rng.normal(size=(n, DIMENSION))),
                int(rng.integers(2**31)),
            )
        )
    return initials


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", nargs="+", type=int, default=[41, 42, 43, 44])
    parser.add_argument("--seed", type=int, default=2026072360)
    parser.add_argument("--inherit", nargs="+", type=Path, required=True)
    parser.add_argument("--random-starts", type=int, default=1)
    parser.add_argument("--smooth-iterations", type=int, default=220)
    parser.add_argument("--bundle-iterations", type=int, default=36)
    parser.add_argument("--escapes", type=int, default=3)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--depth-output", type=Path)
    arguments = parser.parse_args(argv)
    if arguments.random_starts < 1:
        parser.error("--random-starts must be positive")
    started = time.time()
    sources = []
    loaded = []
    for path in arguments.inherit:
        sources.append({"path": str(path), "sha256": sha256(path)})
        loaded.append((path, load_runs(path)))
    runs = []
    for n in arguments.n:
        inherited = []
        for path, records in loaded:
            candidates = [record for record in records if record[0] == n]
            if candidates:
                _, x, label, value = min(candidates, key=lambda record: record[3])
                inherited.append((f"{path.name}:{label}:max={value:.16g}", x))
        initials = choose_initials(
            n,
            arguments.seed + 1009 * n,
            inherited,
            arguments.random_starts,
        )
        for index, (origin, initial, trajectory_seed) in enumerate(initials):
            print(
                f"N={n} trajectory={index} seed={trajectory_seed} origin={origin}",
                flush=True,
            )
            run = run_trajectory(
                n,
                trajectory_seed,
                origin,
                initial,
                arguments.smooth_iterations,
                arguments.bundle_iterations,
                arguments.escapes,
            )
            print(f"  best={run['best']['maximum']:.16f}", flush=True)
            runs.append(run)
    payload = {
        "status": STATUS,
        "method": (
            "log-sum-exp Riemannian continuation followed by a nonsmooth "
            "proximal active-constraint bundle trust method and facet escapes"
        ),
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "parameters": {
            "n": arguments.n,
            "seed": arguments.seed,
            "random_starts": arguments.random_starts,
            "smooth_iterations": arguments.smooth_iterations,
            "bundle_iterations": arguments.bundle_iterations,
            "escapes": arguments.escapes,
        },
        "inherited_inputs": sources,
        "elapsed_seconds": time.time() - started,
        "runs": runs,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    with arguments.output.open("w") as stream:
        json.dump(payload, stream, indent=2, sort_keys=True)
        stream.write("\n")

    if arguments.depth_output is not None:
        n41 = [run for run in runs if run["n"] == 41]
        if not n41:
            raise ValueError("depth output requested without N=41 run")
        best41 = min(n41, key=lambda run: run["best"]["maximum"])
        depth = {
            "source_artifact": str(arguments.output),
            "source_artifact_sha256": sha256(arguments.output),
            "source_seed": best41["seed"],
            "source_origin": best41["origin"],
            "source_maximum": best41["best"]["maximum"],
            "probe": halfspace_depth_probe(
                np.asarray(best41["best"]["coordinates_float64"])
            ),
        }
        arguments.depth_output.parent.mkdir(parents=True, exist_ok=True)
        with arguments.depth_output.open("w") as stream:
            json.dump(depth, stream, indent=2, sort_keys=True)
            stream.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
