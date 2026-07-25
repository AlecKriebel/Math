#!/usr/bin/env python3
"""Round-9 unrestricted numerical search for 41--44 points on S^4.

This is discovery code, not a proof.  It combines:

* exact binary64 scans of every pair after every accepted macro move;
* deletion and global multistart cap reinsertion in blocks of size 2--8;
* joint block and all-vertex log-sum-exp continuation;
* a nonsmooth active-bundle refinement imported from the independently
  tested round-6 implementation;
* threshold-violation replica exchange with asymmetric multivertex moves.

No symmetry, antipodality, lattice, tight-frame, or prescribed-contact-graph
constraint is imposed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import sys
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import minimize
from scipy.spatial import ConvexHull, QhullError

from ..construction_round6_bundle.bundle_search import bundle_refine


DIMENSION = 5
TARGET = 0.5
STATUS = "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE"


def unit_rows(array: np.ndarray) -> np.ndarray:
    """Normalize an N by 5 array, rejecting zero rows."""
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
    first, second = pair_indices(len(x))
    return np.sum(x[first] * x[second], axis=1)


def maximum(array: np.ndarray) -> float:
    """Recompute the literal binary64 maximum over every unordered pair."""
    return float(np.max(pair_values(array)))


def d5_roots() -> np.ndarray:
    roots = []
    for first in range(DIMENSION):
        for second in range(first + 1, DIMENSION):
            for sign_first in (-1.0, 1.0):
                for sign_second in (-1.0, 1.0):
                    vector = np.zeros(DIMENSION)
                    vector[first] = sign_first / math.sqrt(2.0)
                    vector[second] = sign_second / math.sqrt(2.0)
                    roots.append(vector)
    answer = np.asarray(roots)
    if answer.shape != (40, DIMENSION) or abs(maximum(answer) - 0.5) > 1e-14:
        raise AssertionError("D5 root generator failed its internal audit")
    return answer


def tangent_kick(
    x: np.ndarray,
    rng: np.random.Generator,
    scale: float,
    indices: np.ndarray | list[int] | None = None,
) -> np.ndarray:
    x = unit_rows(x)
    if indices is None:
        indices = np.arange(len(x))
    indices = np.asarray(indices, dtype=int)
    answer = x.copy()
    noise = rng.normal(size=(len(indices), DIMENSION))
    noise -= np.sum(noise * answer[indices], axis=1)[:, None] * answer[indices]
    answer[indices] += float(scale) * noise
    return unit_rows(answer)


def _logsumexp(values: np.ndarray, beta: float) -> tuple[float, np.ndarray]:
    top = float(np.max(values))
    raw = np.exp(float(beta) * (values - top))
    denominator = float(np.sum(raw))
    return top + math.log(denominator) / float(beta), raw / denominator


def smooth_all(flat: np.ndarray, n: int, beta: float):
    raw = np.asarray(flat, dtype=float).reshape(n, DIMENSION)
    norms = np.linalg.norm(raw, axis=1)
    if float(np.min(norms)) <= 1e-13:
        return 1e30, np.zeros_like(flat)
    x = raw / norms[:, None]
    first, second = pair_indices(n)
    products = np.sum(x[first] * x[second], axis=1)
    value, weights = _logsumexp(products, beta)
    ambient = np.zeros_like(x)
    np.add.at(ambient, first, weights[:, None] * x[second])
    np.add.at(ambient, second, weights[:, None] * x[first])
    tangent = ambient - np.sum(ambient * x, axis=1)[:, None] * x
    return float(value), (tangent / norms[:, None]).ravel()


def smooth_block(flat: np.ndarray, fixed: np.ndarray, count: int, beta: float):
    """Smooth maximum involving a movable block and a fixed point set."""
    fixed = unit_rows(fixed) if len(fixed) else np.empty((0, DIMENSION))
    raw = np.asarray(flat, dtype=float).reshape(count, DIMENSION)
    norms = np.linalg.norm(raw, axis=1)
    if float(np.min(norms)) <= 1e-13:
        return 1e30, np.zeros_like(flat)
    block = raw / norms[:, None]
    values = []
    tags = []
    if len(fixed):
        cross = block @ fixed.T
        values.extend(cross.ravel().tolist())
        tags.extend(("cross", i, j) for i in range(count) for j in range(len(fixed)))
    if count >= 2:
        first, second = pair_indices(count)
        internal = np.sum(block[first] * block[second], axis=1)
        values.extend(internal.tolist())
        tags.extend(
            ("internal", int(i), int(j)) for i, j in zip(first, second)
        )
    values_array = np.asarray(values, dtype=float)
    value, weights = _logsumexp(values_array, beta)
    ambient = np.zeros_like(block)
    for weight, tag in zip(weights, tags):
        if tag[0] == "cross":
            _, i, j = tag
            ambient[i] += weight * fixed[j]
        else:
            _, i, j = tag
            ambient[i] += weight * block[j]
            ambient[j] += weight * block[i]
    tangent = ambient - np.sum(ambient * block, axis=1)[:, None] * block
    return float(value), (tangent / norms[:, None]).ravel()


def smooth_continuation(
    x: np.ndarray,
    betas: tuple[float, ...],
    iterations: int,
) -> tuple[np.ndarray, list[dict]]:
    x = unit_rows(x)
    history = []
    for beta in betas:
        before = maximum(x)
        result = minimize(
            smooth_all,
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
                "before_maximum": before,
                "after_maximum": maximum(x),
                "iterations": int(result.nit),
                "success": bool(result.success),
                "message": str(result.message),
            }
        )
    return x, history


def polish_block(
    fixed: np.ndarray,
    block: np.ndarray,
    betas: tuple[float, ...] = (48.0, 192.0, 768.0, 3072.0),
    iterations: int = 180,
) -> tuple[np.ndarray, list[dict]]:
    fixed = unit_rows(fixed) if len(fixed) else np.empty((0, DIMENSION))
    block = unit_rows(block)
    history = []
    for beta in betas:
        before = maximum(np.vstack([fixed, block])) if len(fixed) else maximum(block)
        result = minimize(
            smooth_block,
            block.ravel(),
            args=(fixed, len(block), float(beta)),
            jac=True,
            method="L-BFGS-B",
            options={
                "maxiter": int(iterations),
                "ftol": 2e-15,
                "gtol": 2e-9,
                "maxls": 60,
                "maxcor": 25,
            },
        )
        block = unit_rows(result.x.reshape(len(block), DIMENSION))
        after = maximum(np.vstack([fixed, block])) if len(fixed) else maximum(block)
        history.append(
            {
                "beta": float(beta),
                "before_maximum": before,
                "after_maximum": after,
                "iterations": int(result.nit),
                "success": bool(result.success),
            }
        )
    return block, history


def epigraph_all(x: np.ndarray, max_iterations: int = 700):
    """Direct all-pairs minimax SQP, followed by an independent max scan."""
    x = unit_rows(x)
    n = len(x)
    first, second = pair_indices(n)
    initial = np.r_[x.ravel(), maximum(x)]

    def objective(variable):
        return float(variable[-1])

    def objective_jac(variable):
        answer = np.zeros_like(variable)
        answer[-1] = 1.0
        return answer

    def inequalities(variable):
        points = variable[:-1].reshape(n, DIMENSION)
        return variable[-1] - np.sum(points[first] * points[second], axis=1)

    def inequalities_jac(variable):
        points = variable[:-1].reshape(n, DIMENSION)
        answer = np.zeros((len(first), len(variable)))
        rows = np.arange(len(first))
        for coordinate in range(DIMENSION):
            answer[rows, DIMENSION * first + coordinate] = -points[
                second, coordinate
            ]
            answer[rows, DIMENSION * second + coordinate] = -points[
                first, coordinate
            ]
        answer[:, -1] = 1.0
        return answer

    def equalities(variable):
        points = variable[:-1].reshape(n, DIMENSION)
        return np.sum(points * points, axis=1) - 1.0

    def equalities_jac(variable):
        points = variable[:-1].reshape(n, DIMENSION)
        answer = np.zeros((n, len(variable)))
        rows = np.arange(n)
        for coordinate in range(DIMENSION):
            answer[rows, DIMENSION * rows + coordinate] = (
                2.0 * points[:, coordinate]
            )
        return answer

    result = minimize(
        objective,
        initial,
        jac=objective_jac,
        constraints=[
            {"type": "ineq", "fun": inequalities, "jac": inequalities_jac},
            {"type": "eq", "fun": equalities, "jac": equalities_jac},
        ],
        method="SLSQP",
        options={"maxiter": int(max_iterations), "ftol": 2e-13, "disp": False},
    )
    answer = unit_rows(result.x[:-1].reshape(n, DIMENSION))
    return answer, {
        "success": bool(result.success),
        "status": int(result.status),
        "message": str(result.message),
        "iterations": int(result.nit),
        "reported_epigraph": float(result.x[-1]),
        "recomputed_maximum": maximum(answer),
    }


def epigraph_block(
    fixed: np.ndarray, block: np.ndarray, max_iterations: int = 600
):
    """Direct minimax SQP with only ``block`` movable."""
    fixed = unit_rows(fixed)
    block = unit_rows(block)
    count = len(block)
    internal_first, internal_second = pair_indices(count)
    fixed_maximum = maximum(fixed) if len(fixed) >= 2 else -1.0
    initial_maximum = maximum(np.vstack([fixed, block]))
    initial = np.r_[block.ravel(), initial_maximum]
    cross_count = count * len(fixed)
    internal_count = len(internal_first)

    def objective(variable):
        return float(variable[-1])

    def objective_jac(variable):
        answer = np.zeros_like(variable)
        answer[-1] = 1.0
        return answer

    def inequalities(variable):
        points = variable[:-1].reshape(count, DIMENSION)
        cross = (variable[-1] - points @ fixed.T).ravel()
        internal = variable[-1] - np.sum(
            points[internal_first] * points[internal_second], axis=1
        )
        return np.r_[variable[-1] - fixed_maximum, cross, internal]

    def inequalities_jac(variable):
        points = variable[:-1].reshape(count, DIMENSION)
        answer = np.zeros(
            (1 + cross_count + internal_count, len(variable))
        )
        answer[:, -1] = 1.0
        for movable in range(count):
            rows = 1 + movable * len(fixed) + np.arange(len(fixed))
            for coordinate in range(DIMENSION):
                answer[rows, DIMENSION * movable + coordinate] = -fixed[
                    :, coordinate
                ]
        rows = 1 + cross_count + np.arange(internal_count)
        for coordinate in range(DIMENSION):
            answer[
                rows, DIMENSION * internal_first + coordinate
            ] = -points[internal_second, coordinate]
            answer[
                rows, DIMENSION * internal_second + coordinate
            ] = -points[internal_first, coordinate]
        return answer

    def equalities(variable):
        points = variable[:-1].reshape(count, DIMENSION)
        return np.sum(points * points, axis=1) - 1.0

    def equalities_jac(variable):
        points = variable[:-1].reshape(count, DIMENSION)
        answer = np.zeros((count, len(variable)))
        rows = np.arange(count)
        for coordinate in range(DIMENSION):
            answer[rows, DIMENSION * rows + coordinate] = (
                2.0 * points[:, coordinate]
            )
        return answer

    result = minimize(
        objective,
        initial,
        jac=objective_jac,
        constraints=[
            {"type": "ineq", "fun": inequalities, "jac": inequalities_jac},
            {"type": "eq", "fun": equalities, "jac": equalities_jac},
        ],
        method="SLSQP",
        options={"maxiter": int(max_iterations), "ftol": 2e-13, "disp": False},
    )
    answer = unit_rows(result.x[:-1].reshape(count, DIMENSION))
    return answer, {
        "success": bool(result.success),
        "status": int(result.status),
        "message": str(result.message),
        "iterations": int(result.nit),
        "reported_epigraph": float(result.x[-1]),
        "recomputed_maximum": maximum(np.vstack([fixed, answer])),
    }


def smooth_hole(raw: np.ndarray, fixed: np.ndarray, beta: float):
    norm = float(np.linalg.norm(raw))
    if norm <= 1e-13:
        return 1e30, np.zeros_like(raw)
    point = raw / norm
    products = fixed @ point
    value, weights = _logsumexp(products, beta)
    ambient = fixed.T @ weights
    tangent = ambient - float(ambient @ point) * point
    return float(value), tangent / norm


def epigraph_hole(fixed: np.ndarray, start: np.ndarray) -> tuple[np.ndarray, dict]:
    """Solve the one-point cap insertion problem locally with direct SQP."""
    fixed = unit_rows(fixed)
    start = np.asarray(start, dtype=float)
    start /= np.linalg.norm(start)
    initial = np.r_[start, float(np.max(fixed @ start))]

    def objective(variable):
        return float(variable[-1])

    def objective_jac(variable):
        answer = np.zeros(DIMENSION + 1)
        answer[-1] = 1.0
        return answer

    def inequalities(variable):
        return variable[-1] - fixed @ variable[:DIMENSION]

    def inequalities_jac(variable):
        answer = np.empty((len(fixed), DIMENSION + 1))
        answer[:, :DIMENSION] = -fixed
        answer[:, -1] = 1.0
        return answer

    def equality(variable):
        return float(variable[:DIMENSION] @ variable[:DIMENSION] - 1.0)

    def equality_jac(variable):
        answer = np.zeros(DIMENSION + 1)
        answer[:DIMENSION] = 2.0 * variable[:DIMENSION]
        return answer

    result = minimize(
        objective,
        initial,
        jac=objective_jac,
        constraints=[
            {"type": "ineq", "fun": inequalities, "jac": inequalities_jac},
            {"type": "eq", "fun": equality, "jac": equality_jac},
        ],
        method="SLSQP",
        options={"maxiter": 500, "ftol": 2e-13, "disp": False},
    )
    point = result.x[:DIMENSION]
    point /= np.linalg.norm(point)
    return point, {
        "success": bool(result.success),
        "iterations": int(result.nit),
        "reported_epigraph": float(result.x[-1]),
        "recomputed_maximum": float(np.max(fixed @ point)),
    }


def facet_hole_candidates(
    fixed: np.ndarray, maximum_candidates: int
) -> tuple[list[tuple[np.ndarray, float]], dict]:
    """Enumerate centered-inball contact facets of ``conv(fixed)``.

    When the origin is in the strict interior of the full-dimensional convex
    hull P, the one-point insertion optimum is

        min_{||y||=1} max_{p in P} <p,y>

    and equals the radius of the largest origin-centered ball contained in P.
    The latter is the minimum origin-to-facet distance.  Qhull returns every
    triangulated facet equation, so scanning its outward unit normals solves
    this one-point subproblem globally, modulo floating-point arithmetic.

    Repeated normals from triangulated nonsimplicial facets are removed.
    """
    fixed = unit_rows(fixed)
    if len(fixed) < DIMENSION + 1:
        return [], {
            "available": False,
            "reason": "too_few_points",
            "origin_strictly_inside": False,
        }
    if np.linalg.matrix_rank(fixed - np.mean(fixed, axis=0)) < DIMENSION:
        return [], {
            "available": False,
            "reason": "affine_rank_below_five",
            "origin_strictly_inside": False,
        }
    try:
        hull = ConvexHull(fixed)
    except QhullError as error:
        return [], {
            "available": False,
            "reason": f"qhull_error:{error.__class__.__name__}",
            "origin_strictly_inside": False,
        }
    equations = np.asarray(hull.equations, dtype=float)
    normals = equations[:, :DIMENSION]
    normal_norms = np.linalg.norm(normals, axis=1)
    normals = normals / normal_norms[:, None]
    offsets = equations[:, -1] / normal_norms
    origin_strictly_inside = bool(float(np.max(offsets)) < -1e-10)
    if not origin_strictly_inside:
        return [], {
            "available": False,
            "reason": "origin_not_certified_strictly_inside_binary64_hull",
            "origin_strictly_inside": False,
            "maximum_origin_equation_value": float(np.max(offsets)),
            "raw_facet_count": len(equations),
        }
    scores = np.max(fixed @ normals.T, axis=0)
    order = np.argsort(scores)
    candidates: list[tuple[np.ndarray, float]] = []
    for index in order:
        normal = normals[int(index)]
        score = float(scores[int(index)])
        if any(
            float(np.linalg.norm(normal - old_normal)) <= 2e-9
            for old_normal, _ in candidates
        ):
            continue
        candidates.append((normal.copy(), score))
        if len(candidates) >= int(maximum_candidates):
            break
    return candidates, {
        "available": True,
        "reason": "complete_facet_scan_binary64",
        "origin_strictly_inside": True,
        "maximum_origin_equation_value": float(np.max(offsets)),
        "raw_facet_count": len(equations),
        "distinct_candidates_returned": len(candidates),
        "minimum_facet_distance": float(np.min(-offsets)),
        "minimum_recomputed_support": (
            candidates[0][1] if candidates else None
        ),
        "facet_distance_support_discrepancy": (
            float(abs(np.min(-offsets) - candidates[0][1]))
            if candidates
            else None
        ),
    }


def global_hole(
    fixed: np.ndarray,
    rng: np.random.Generator,
    samples: int,
    local_starts: int,
) -> tuple[np.ndarray, dict]:
    """Complete binary64 facet scan plus independent multistart local audit."""
    fixed = unit_rows(fixed)
    facet_candidates, facet_audit = facet_hole_candidates(
        fixed, maximum_candidates=max(4, local_starts)
    )
    candidates = unit_rows(rng.normal(size=(int(samples), DIMENSION)))
    scores = np.max(candidates @ fixed.T, axis=1)
    order = np.argsort(scores)[: int(local_starts)]
    records = []
    for index in order:
        point = candidates[int(index)]
        smooth_history = []
        for beta in (32.0, 128.0, 512.0, 2048.0):
            result = minimize(
                smooth_hole,
                point,
                args=(fixed, beta),
                jac=True,
                method="L-BFGS-B",
                options={
                    "maxiter": 160,
                    "ftol": 2e-15,
                    "gtol": 1e-10,
                    "maxls": 50,
                },
            )
            point = result.x / np.linalg.norm(result.x)
            smooth_history.append(float(np.max(fixed @ point)))
        point, sqp = epigraph_hole(fixed, point)
        records.append(
            {
                "sample_index": int(index),
                "sample_score": float(scores[index]),
                "smooth_maxima": smooth_history,
                "sqp": sqp,
                "point": point,
            }
        )
    local_best = min(
        records, key=lambda record: record["sqp"]["recomputed_maximum"]
    )
    all_candidates = [
        (
            local_best["point"].copy(),
            local_best["sqp"]["recomputed_maximum"],
            "random_multistart_sqp",
        )
    ]
    all_candidates.extend(
        (point.copy(), float(score), "complete_facet_scan_binary64")
        for point, score in facet_candidates
    )
    best_point, best_score, source = min(
        all_candidates, key=lambda item: item[1]
    )
    return best_point, {
        "samples": int(samples),
        "local_starts": int(local_starts),
        "best_sample_score": float(np.min(scores)),
        "best_sqp": local_best["sqp"],
        "facet_scan": facet_audit,
        "selected_source": source,
        "selected_recomputed_maximum": float(best_score),
    }


def beam_reinsert(
    fixed: np.ndarray,
    count: int,
    rng: np.random.Generator,
    beam_width: int,
    facet_choices: int,
    hole_samples: int,
    hole_starts: int,
) -> tuple[list[np.ndarray], dict]:
    """Beam over globally solved one-point insertion choices.

    Each individual extension is a complete binary64 facet scan whenever the
    origin is strictly inside the current convex hull.  Selecting a sequence
    of ``count`` extensions remains a beam heuristic and is not described as
    a global solution of the multipoint replacement problem.
    """
    fixed = unit_rows(fixed)
    states = [
        {
            "current": fixed.copy(),
            "inserted": [],
            "path": [],
        }
    ]
    stage_log = []
    for stage in range(int(count)):
        expanded = []
        for state_index, state in enumerate(states):
            facet_candidates, facet_audit = facet_hole_candidates(
                state["current"], maximum_candidates=facet_choices
            )
            choices = [
                (point, score, "complete_facet_scan_binary64")
                for point, score in facet_candidates
            ]
            if not choices:
                point, fallback = global_hole(
                    state["current"], rng, hole_samples, hole_starts
                )
                choices = [
                    (
                        point,
                        fallback["selected_recomputed_maximum"],
                        fallback["selected_source"],
                    )
                ]
                facet_audit = fallback["facet_scan"]
            for choice_index, (point, score, source) in enumerate(choices):
                current = np.vstack([state["current"], point])
                path = state["path"] + [
                    {
                        "stage": stage,
                        "parent_state": state_index,
                        "choice_index": choice_index,
                        "source": source,
                        "one_point_global_score": float(score),
                        "facet_audit": facet_audit,
                    }
                ]
                expanded.append(
                    {
                        "current": current,
                        "inserted": state["inserted"] + [point.copy()],
                        "path": path,
                        "ranking": (
                            maximum(current),
                            threshold_violation_energy(current),
                        ),
                    }
                )
        expanded.sort(key=lambda state: state["ranking"])
        retained = []
        signatures = []
        for state in expanded:
            inserted = np.asarray(state["inserted"])
            signature = np.sort(pair_values(state["current"]))
            if any(
                float(np.max(np.abs(signature - old))) <= 2e-10
                for old in signatures
            ):
                continue
            retained.append(state)
            signatures.append(signature)
            if len(retained) >= int(beam_width):
                break
        states = retained or expanded[:1]
        stage_log.append(
            {
                "stage": stage,
                "expanded_states": len(expanded),
                "retained_states": len(states),
                "best_partial_maximum": min(
                    maximum(state["current"]) for state in states
                ),
                "best_partial_threshold_energy": min(
                    threshold_violation_energy(state["current"])
                    for state in states
                ),
            }
        )
    blocks = [np.asarray(state["inserted"]) for state in states]
    return blocks, {
        "beam_width": int(beam_width),
        "facet_choices_per_state": int(facet_choices),
        "stages": stage_log,
        "final_paths": [state["path"] for state in states],
    }


def threshold_violation_energy(x: np.ndarray, target: float = TARGET) -> float:
    excess = np.maximum(pair_values(x) - float(target), 0.0)
    # L2 violations distinguish broad threshold breaches; the tiny max term
    # prevents configurations with one large residual from looking deceptively
    # good merely because they have few violating pairs.
    return float(excess @ excess + 1e-4 * np.max(excess) ** 2)


def replica_exchange(
    initial: np.ndarray,
    rng: np.random.Generator,
    sweeps: int,
) -> tuple[list[np.ndarray], dict]:
    """Threshold-energy replica exchange with asymmetric 2--8 vertex moves."""
    initial = unit_rows(initial)
    temperatures = np.asarray((2e-5, 8e-5, 3.2e-4, 1.28e-3), dtype=float)
    scales = np.asarray((0.018, 0.035, 0.07, 0.14), dtype=float)
    replicas = [
        tangent_kick(initial, rng, scale * 0.45) for scale in scales
    ]
    energies = np.asarray([threshold_violation_energy(x) for x in replicas])
    best = [(float(energy), x.copy()) for energy, x in zip(energies, replicas)]
    accepted = np.zeros(len(replicas), dtype=int)
    proposed = np.zeros(len(replicas), dtype=int)
    exchanges = np.zeros(len(replicas) - 1, dtype=int)
    exchange_attempts = np.zeros(len(replicas) - 1, dtype=int)
    for sweep in range(int(sweeps)):
        for replica in range(len(replicas)):
            count = 2 + ((sweep + 3 * replica) % 7)
            indices = np.sort(rng.choice(len(initial), count, replace=False))
            candidate = tangent_kick(
                replicas[replica], rng, scales[replica], indices
            )
            energy = threshold_violation_energy(candidate)
            delta = energy - energies[replica]
            proposed[replica] += 1
            if delta <= 0.0 or rng.random() < math.exp(
                -min(delta / temperatures[replica], 700.0)
            ):
                replicas[replica] = candidate
                energies[replica] = energy
                accepted[replica] += 1
                if energy < best[replica][0]:
                    best[replica] = (float(energy), candidate.copy())
        parity = sweep % 2
        for low in range(parity, len(replicas) - 1, 2):
            high = low + 1
            exchange_attempts[low] += 1
            exponent = (
                (1.0 / temperatures[low] - 1.0 / temperatures[high])
                * (energies[low] - energies[high])
            )
            if exponent >= 0.0 or rng.random() < math.exp(max(exponent, -700.0)):
                replicas[low], replicas[high] = replicas[high], replicas[low]
                energies[low], energies[high] = energies[high], energies[low]
                exchanges[low] += 1
    candidates = [entry[1] for entry in best]
    return candidates, {
        "sweeps": int(sweeps),
        "temperatures": temperatures.tolist(),
        "move_scales": scales.tolist(),
        "acceptance_counts": accepted.tolist(),
        "proposal_counts": proposed.tolist(),
        "exchange_counts": exchanges.tolist(),
        "exchange_attempts": exchange_attempts.tolist(),
        "best_threshold_energies": [entry[0] for entry in best],
        "best_exact_pair_maxima": [maximum(entry[1]) for entry in best],
    }


def connected_components(n: int, edges: list[list[int]]) -> list[list[int]]:
    adjacency = [[] for _ in range(n)]
    for first, second in edges:
        adjacency[first].append(second)
        adjacency[second].append(first)
    seen: set[int] = set()
    components = []
    for start in range(n):
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        component = []
        while stack:
            vertex = stack.pop()
            component.append(vertex)
            for neighbor in adjacency[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        components.append(sorted(component))
    return sorted(components, key=lambda item: (-len(item), item))


def active_graph(x: np.ndarray, tolerance: float) -> dict:
    x = unit_rows(x)
    first, second = pair_indices(len(x))
    values = np.sum(x[first] * x[second], axis=1)
    top = float(np.max(values))
    chosen = values >= top - float(tolerance)
    edges = np.column_stack([first[chosen], second[chosen]]).astype(int).tolist()
    degrees = np.bincount(
        np.asarray(edges, dtype=int).ravel(), minlength=len(x)
    )
    unique, counts = np.unique(degrees, return_counts=True)
    components = connected_components(len(x), edges)
    return {
        "tolerance": float(tolerance),
        "maximum": top,
        "edge_count": len(edges),
        "edges": edges,
        "degree_sequence": degrees.astype(int).tolist(),
        "degree_histogram": {
            str(int(degree)): int(count)
            for degree, count in zip(unique, counts)
        },
        "components": components,
        "component_sizes": [len(component) for component in components],
        "isolated_vertices": np.flatnonzero(degrees == 0).astype(int).tolist(),
    }


def edge_jaccard(first: dict, second: dict) -> float:
    left = {tuple(edge) for edge in first["edges"]}
    right = {tuple(edge) for edge in second["edges"]}
    return float(len(left & right) / len(left | right)) if left or right else 1.0


def exact_maximum_independent_set(
    vertex_count: int, edges: list[list[int]]
) -> tuple[list[int], int]:
    """Exact bitset branch-and-bound on a finite graph.

    This certifies only the integer graph supplied to it.  When that graph was
    extracted from floating coordinates, it does not turn the underlying
    geometric contact claims into exact mathematics.
    """
    adjacency = [0] * vertex_count
    for first, second in edges:
        adjacency[first] |= 1 << second
        adjacency[second] |= 1 << first
    best: list[int] = []
    nodes = 0

    def search(candidates: int, selected: list[int]) -> None:
        nonlocal best, nodes
        nodes += 1
        if len(selected) + candidates.bit_count() <= len(best):
            return
        if candidates == 0:
            if len(selected) > len(best):
                best = selected.copy()
            return
        vertices = []
        remaining = candidates
        while remaining:
            bit = remaining & -remaining
            vertex = bit.bit_length() - 1
            vertices.append(vertex)
            remaining ^= bit
        pivot = max(
            vertices,
            key=lambda vertex: (adjacency[vertex] & candidates).bit_count(),
        )
        search(
            candidates & ~(1 << pivot) & ~adjacency[pivot],
            selected + [pivot],
        )
        search(candidates & ~(1 << pivot), selected)

    search((1 << vertex_count) - 1, [])
    return sorted(best), nodes


def diagnostics(x: np.ndarray) -> dict:
    x = unit_rows(x)
    gram = x @ x.T
    values = pair_values(x)
    eigenvalues = np.linalg.eigvalsh(gram)
    top = float(np.max(values))
    result = {
        "n": len(x),
        "maximum": top,
        "gap_above_one_half": top - TARGET,
        "minimum": float(np.min(values)),
        "row_norm_max_error": float(
            np.max(np.abs(np.sum(x * x, axis=1) - 1.0))
        ),
        "pairs_above_one_half": int(np.sum(values > TARGET)),
        "pairs_below_minus_one_half": int(np.sum(values < -TARGET)),
        "threshold_violation_energy": threshold_violation_energy(x),
        "pair_quantiles": {
            f"{q:.3f}": float(np.quantile(values, q))
            for q in (0.0, 0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99, 1.0)
        },
        "gram_eigenvalues": eigenvalues.tolist(),
        "positive_gram_eigenvalues": eigenvalues[-DIMENSION:].tolist(),
        "gram_tail_max_abs": float(np.max(np.abs(eigenvalues[:-DIMENSION]))),
        "coordinates_float64": x.tolist(),
    }
    for tolerance in (1e-4, 1e-6, 1e-8):
        result[f"active_{tolerance:.0e}"] = active_graph(x, tolerance)
    return result


def load_best_prior(path: Path) -> dict[int, dict]:
    payload = json.loads(path.read_text())
    answer: dict[int, dict] = {}
    for index, run in enumerate(payload["runs"]):
        best = run.get("best", {})
        coordinates = best.get("coordinates_float64")
        if coordinates is None:
            continue
        x = unit_rows(np.asarray(coordinates, dtype=float))
        n = len(x)
        record = {
            "run_index": index,
            "seed": int(run["seed"]),
            "origin": run["origin"],
            "maximum": maximum(x),
            "coordinates": x,
        }
        if n not in answer or record["maximum"] < answer[n]["maximum"]:
            answer[n] = record
    return answer


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def stress_scores(x: np.ndarray, beta: float = 1600.0) -> np.ndarray:
    x = unit_rows(x)
    first, second = pair_indices(len(x))
    values = np.sum(x[first] * x[second], axis=1)
    _, weights = _logsumexp(values, beta)
    stress = np.zeros(len(x))
    np.add.at(stress, first, weights)
    np.add.at(stress, second, weights)
    return stress


def choose_deletion(
    x: np.ndarray,
    count: int,
    rng: np.random.Generator,
    variant: int,
) -> np.ndarray:
    """Choose a deterministic stress/core/rattler-aware deletion block."""
    graph = active_graph(x, 1e-6)
    degrees = np.asarray(graph["degree_sequence"], dtype=float)
    stress = stress_scores(x)
    if variant % 3 == 0:
        score = stress + 1e-5 * degrees
        return np.sort(np.argsort(score)[-count:])
    if variant % 3 == 1:
        # Grow a contact-connected high-stress cluster.
        adjacency = [set() for _ in range(len(x))]
        for first, second in graph["edges"]:
            adjacency[first].add(second)
            adjacency[second].add(first)
        selected = [int(np.argmax(stress + 1e-5 * degrees))]
        while len(selected) < count:
            frontier = set()
            for vertex in selected:
                frontier.update(adjacency[vertex])
            frontier.difference_update(selected)
            candidates = list(frontier) or [
                index for index in range(len(x)) if index not in selected
            ]
            selected.append(
                max(candidates, key=lambda index: (stress[index], degrees[index]))
            )
        return np.sort(np.asarray(selected, dtype=int))
    # Mix rattlers/low-contact rows with stressed core rows.  This is
    # especially targeted at the 35+6 structure, without presupposing it.
    low_count = min(count // 2, int(np.sum(degrees == 0)))
    low = np.argsort(degrees + 1e-3 * stress)[:low_count]
    remaining = np.asarray([i for i in range(len(x)) if i not in set(low)])
    probabilities = stress[remaining] + 0.03 / (1.0 + degrees[remaining])
    probabilities /= float(np.sum(probabilities))
    high = rng.choice(remaining, count - low_count, replace=False, p=probabilities)
    return np.sort(np.r_[low, high].astype(int))


def delete_reinsert(
    initial: np.ndarray,
    deleted: np.ndarray,
    rng: np.random.Generator,
    hole_samples: int,
    hole_starts: int,
    beam_width: int,
    facet_choices: int,
    search_iterations: int,
) -> tuple[np.ndarray, dict]:
    initial = unit_rows(initial)
    deleted = np.sort(np.asarray(deleted, dtype=int))
    fixed = np.delete(initial, deleted, axis=0)
    blocks, insertion_log = beam_reinsert(
        fixed,
        len(deleted),
        rng,
        beam_width,
        facet_choices,
        hole_samples,
        hole_starts,
    )
    polished_blocks = []
    block_histories = []
    block_sqp_records = []
    for block in blocks:
        polished, history = polish_block(
            fixed,
            block,
            iterations=max(80, search_iterations // 2),
        )
        polished, sqp_record = epigraph_block(fixed, polished)
        polished_blocks.append(polished)
        block_histories.append(history)
        block_sqp_records.append(sqp_record)
    block_index, block = min(
        enumerate(polished_blocks),
        key=lambda item: maximum(np.vstack([fixed, item[1]])),
    )
    block_history = block_histories[block_index]
    block_sqp = block_sqp_records[block_index]
    candidate = np.vstack([fixed, block])
    after_insertion = maximum(candidate)
    candidate, release_history = smooth_continuation(
        candidate,
        (96.0, 384.0, 1536.0, 6144.0),
        search_iterations,
    )
    candidate, bundle_history = bundle_refine(
        candidate, iterations=16, initial_radius=0.05
    )
    candidate, all_sqp = epigraph_all(candidate)
    return candidate, {
        "deleted_indices": deleted.tolist(),
        "deleted_count": len(deleted),
        "before_maximum": maximum(initial),
        "after_beam_insertion_and_block_polish": after_insertion,
        "insertion_log": insertion_log,
        "selected_beam_state": int(block_index),
        "block_history": block_history,
        "block_sqp": block_sqp,
        "release_history": release_history,
        "bundle_iterations": len(bundle_history),
        "all_vertex_sqp": all_sqp,
        "after_maximum": maximum(candidate),
    }


def rebuild_from_fixed_core(
    core: np.ndarray,
    target_n: int,
    rng: np.random.Generator,
    hole_samples: int,
    hole_starts: int,
    beam_width: int,
    facet_choices: int,
    search_iterations: int,
) -> tuple[np.ndarray, dict]:
    """Insert to ``target_n`` and then release every coordinate."""
    core = unit_rows(core)
    insert_count = target_n - len(core)
    if insert_count < 0:
        raise ValueError("core is larger than the requested target")
    if insert_count:
        blocks, beam_log = beam_reinsert(
            core,
            insert_count,
            rng,
            beam_width,
            facet_choices,
            hole_samples,
            hole_starts,
        )
        alternatives = []
        for block in blocks:
            block, block_history = polish_block(
                core,
                block,
                iterations=max(80, search_iterations // 2),
            )
            block, block_sqp = epigraph_block(core, block)
            candidate = np.vstack([core, block])
            alternatives.append(
                (
                    maximum(candidate),
                    candidate,
                    block_history,
                    block_sqp,
                )
            )
        before_release, candidate, block_history, block_sqp = min(
            alternatives, key=lambda entry: entry[0]
        )
    else:
        candidate = core.copy()
        beam_log = None
        block_history = []
        block_sqp = None
        before_release = maximum(candidate)
    candidate, release_history = smooth_continuation(
        candidate,
        (48.0, 192.0, 768.0, 3072.0, 12288.0),
        search_iterations,
    )
    candidate, bundle_history = bundle_refine(
        candidate, iterations=20, initial_radius=0.065
    )
    candidate, all_sqp = epigraph_all(candidate)
    return candidate, {
        "core_size": len(core),
        "core_maximum": maximum(core),
        "insert_count": insert_count,
        "beam_log": beam_log,
        "selected_block_history": block_history,
        "selected_block_sqp": block_sqp,
        "before_all_vertex_release": before_release,
        "release_history": release_history,
        "bundle_iterations": len(bundle_history),
        "all_vertex_sqp": all_sqp,
        "final_maximum": maximum(candidate),
    }


def challenge_one(
    n: int,
    inherited: dict,
    seed: int,
    hole_samples: int,
    hole_starts: int,
    search_iterations: int,
    replica_sweeps: int,
    random_starts: int,
    beam_width: int,
    facet_choices: int,
    core_random_starts: int,
) -> dict:
    rng = np.random.default_rng(seed)
    started = time.time()
    original = unit_rows(inherited["coordinates"])
    candidates: list[tuple[str, np.ndarray]] = [("inherited", original.copy())]
    surgery_records = []

    graph = active_graph(original, 1e-6)
    components = graph["components"]
    core = np.asarray(components[0], dtype=int)
    rattlers = np.asarray(
        sorted(vertex for component in components[1:] for vertex in component),
        dtype=int,
    )
    core_analysis = {
        "active_tolerance": 1e-6,
        "core_indices": core.tolist(),
        "rattler_indices": rattlers.tolist(),
        "core_size": len(core),
        "rattler_count": len(rattlers),
        "inherited_core_maximum": (
            maximum(original[core]) if len(core) >= 2 else None
        ),
    }
    if len(core) >= 2:
        core_position = {int(vertex): index for index, vertex in enumerate(core)}
        core_edges = [
            [core_position[first], core_position[second]]
            for first, second in graph["edges"]
            if first in core_position and second in core_position
        ]
        independent_local, search_nodes = exact_maximum_independent_set(
            len(core), core_edges
        )
        independent_global = [int(core[index]) for index in independent_local]
        core_values = pair_values(original[core])
        active_threshold = maximum(original) - 1e-6
        inactive = core_values[core_values < active_threshold]
        core_analysis.update(
            {
                "active_core_edge_count": len(core_edges),
                "finite_graph_maximum_independent_set_size": len(
                    independent_local
                ),
                "finite_graph_maximum_independent_set_indices": (
                    independent_global
                ),
                "finite_graph_minimum_vertex_cover_size": (
                    len(core) - len(independent_local)
                ),
                "finite_graph_branch_nodes": search_nodes,
                "largest_inactive_core_pair": (
                    float(np.max(inactive)) if len(inactive) else None
                ),
                "active_to_inactive_core_pair_gap": (
                    float(maximum(original) - np.max(inactive))
                    if len(inactive)
                    else None
                ),
                "frozen_deletion_2_to_8_obstruction": (
                    "Every deletion of at most eight core vertices leaves an "
                    "edge of the extracted active graph, since its exact "
                    "finite-graph minimum vertex cover has size "
                    f"{len(core) - len(independent_local)}. Therefore a "
                    "locked-remainder replacement cannot lower the inherited "
                    "maximum; only the subsequent all-vertex release can."
                ),
            }
        )

    # Release the active core separately, then globally reinsert every
    # contact-free row.  For N=41 this directly interrogates the 35+6 basin.
    if len(rattlers):
        refined_core, core_history = smooth_continuation(
            original[core],
            (96.0, 384.0, 1536.0, 6144.0),
            search_iterations,
        )
        refined_core, core_bundle_history = bundle_refine(
            refined_core, iterations=16, initial_radius=0.05
        )
        refined_core, core_sqp = epigraph_all(refined_core)
        core_analysis["refined_core_maximum"] = maximum(refined_core)
        core_analysis["core_release_history"] = core_history
        core_analysis["core_bundle_iterations"] = len(core_bundle_history)
        core_analysis["core_sqp"] = core_sqp
        rebuilt_blocks, rebuild_log = beam_reinsert(
            refined_core,
            len(rattlers),
            rng,
            beam_width,
            facet_choices,
            hole_samples,
            hole_starts,
        )
        polished_rebuilds = []
        for block in rebuilt_blocks:
            polished_block, block_history = polish_block(
                refined_core,
                block,
                iterations=max(80, search_iterations // 2),
            )
            polished_block, block_sqp = epigraph_block(
                refined_core, polished_block
            )
            polished_rebuilds.append(
                (
                    maximum(np.vstack([refined_core, polished_block])),
                    polished_block,
                    block_history,
                    block_sqp,
                )
            )
        _, rebuilt_block, rebuild_block_history, rebuild_block_sqp = min(
            polished_rebuilds, key=lambda entry: entry[0]
        )
        rebuilt = np.vstack([refined_core, rebuilt_block])
        rebuilt, release = smooth_continuation(
            rebuilt,
            (96.0, 384.0, 1536.0, 6144.0),
            search_iterations,
        )
        rebuilt, bundle = bundle_refine(
            rebuilt, iterations=16, initial_radius=0.05
        )
        rebuilt, rebuild_all_sqp = epigraph_all(rebuilt)
        core_analysis["rebuild_beam_log"] = rebuild_log
        core_analysis["rebuild_block_history"] = rebuild_block_history
        core_analysis["rebuild_block_sqp"] = rebuild_block_sqp
        core_analysis["rebuild_release_history"] = release
        core_analysis["rebuild_bundle_iterations"] = len(bundle)
        core_analysis["rebuild_all_vertex_sqp"] = rebuild_all_sqp
        core_analysis["rebuilt_maximum"] = maximum(rebuilt)
        candidates.append(("core_release_and_global_rattler_rebuild", rebuilt))

    # Challenge the 35+6 interpretation from unrelated low-coherence cores.
    # The 35-point core is optimized with every coordinate free, and only
    # afterward are six points inserted.  These runs can leave the inherited
    # contact topology completely.
    alternative_core_records = []
    if n == 41:
        for core_start in range(int(core_random_starts)):
            random_core = unit_rows(rng.normal(size=(35, DIMENSION)))
            initial_core_maximum = maximum(random_core)
            random_core, core_history = smooth_continuation(
                random_core,
                (24.0, 72.0, 216.0, 648.0, 1944.0, 5832.0),
                search_iterations,
            )
            random_core, core_sqp = epigraph_all(random_core)
            rebuilt, rebuild_record = rebuild_from_fixed_core(
                random_core,
                n,
                rng,
                hole_samples,
                hole_starts,
                beam_width,
                facet_choices,
                search_iterations,
            )
            label = f"independent_random_35_core_{core_start}"
            alternative_core_records.append(
                {
                    "label": label,
                    "initial_core_maximum": initial_core_maximum,
                    "optimized_core_maximum": maximum(random_core),
                    "core_history": core_history,
                    "core_sqp": core_sqp,
                    "rebuild": rebuild_record,
                }
            )
            candidates.append((label, rebuilt))

        # A deliberately asymmetric 35-root subset offers a core with exact
        # mathematical maximum 1/2 before floating release.
        roots = d5_roots()
        removed_roots = np.sort(rng.choice(40, 5, replace=False))
        d5_core = np.delete(roots, removed_roots, axis=0)
        rebuilt, rebuild_record = rebuild_from_fixed_core(
            d5_core,
            n,
            rng,
            hole_samples,
            hole_starts,
            beam_width,
            facet_choices,
            search_iterations,
        )
        alternative_core_records.append(
            {
                "label": "asymmetric_D5_35_root_core",
                "removed_root_indices": removed_roots.tolist(),
                "optimized_core_maximum": maximum(d5_core),
                "rebuild": rebuild_record,
            }
        )
        candidates.append(("asymmetric_D5_35_root_core", rebuilt))

    # The full D5 code plus one to four globally chosen cap insertions is
    # included for every N as an independent lattice-origin start.  All rows
    # are released immediately afterward, so no lattice restriction remains.
    d5_candidate, d5_record = rebuild_from_fixed_core(
        d5_roots(),
        n,
        rng,
        hole_samples,
        hole_starts,
        beam_width,
        facet_choices,
        search_iterations,
    )
    candidates.append(("D5_plus_global_cap_beam_then_release", d5_candidate))

    # Large active-core quakes move all vertices of the principal component
    # together.  Their scales deliberately extend far beyond the small
    # tangent escapes that previously returned to the 0.51499 basin.
    core_quake_records = []
    inherited_graph = active_graph(original, 1e-6)
    for quake_index, scale in enumerate((0.12, 0.25, 0.50, 0.90)):
        quaked = tangent_kick(original, rng, scale, core)
        kicked_maximum = maximum(quaked)
        quaked, history = smooth_continuation(
            quaked,
            (24.0, 72.0, 216.0, 648.0, 1944.0, 5832.0, 17496.0),
            search_iterations,
        )
        quaked, bundle = bundle_refine(
            quaked, iterations=22, initial_radius=0.09
        )
        quaked, sqp = epigraph_all(quaked)
        quake_graph = active_graph(quaked, 1e-6)
        label = f"active_core_quake_scale_{scale:.2f}"
        core_quake_records.append(
            {
                "label": label,
                "scale": scale,
                "moved_vertex_count": len(core),
                "kicked_maximum": kicked_maximum,
                "release_history": history,
                "bundle_iterations": len(bundle),
                "all_vertex_sqp": sqp,
                "final_maximum": maximum(quaked),
                "active_edge_jaccard_with_inherited": edge_jaccard(
                    inherited_graph, quake_graph
                ),
            }
        )
        candidates.append((label, quaked))

    # Every block size 2--8 is tested.  Variants rotate between high-stress,
    # contact-connected, and low-degree-plus-stress selections.
    current_anchor = original.copy()
    for count in range(2, 9):
        deleted = choose_deletion(
            current_anchor, count, rng, variant=count
        )
        candidate, record = delete_reinsert(
            current_anchor,
            deleted,
            rng,
            hole_samples,
            hole_starts,
            beam_width,
            facet_choices,
            search_iterations,
        )
        record["label"] = f"delete_reinsert_{count}"
        record["improves_inherited"] = maximum(candidate) < maximum(original)
        surgery_records.append(record)
        candidates.append((record["label"], candidate))
        # Chained improvement is allowed, but a failed move never degrades the
        # anchor from which the next block size starts.
        if maximum(candidate) < maximum(current_anchor):
            current_anchor = candidate.copy()

    # Replica exchange is run both from the inherited basin and from a fresh
    # asymmetric Gaussian cloud.  Only exact-pair-scan records are promoted.
    replica_records = []
    replica_inputs = [("inherited", original)]
    for index in range(random_starts):
        replica_inputs.append(
            (
                f"asymmetric_gaussian_{index}",
                unit_rows(rng.normal(size=(n, DIMENSION))),
            )
        )
    for label, start in replica_inputs:
        raw_candidates, record = replica_exchange(start, rng, replica_sweeps)
        polished_maxima = []
        for replica_index, raw in enumerate(raw_candidates):
            polished, _ = smooth_continuation(
                raw,
                (48.0, 192.0, 768.0, 3072.0, 12288.0),
                search_iterations,
            )
            polished, bundle = bundle_refine(
                polished, iterations=14, initial_radius=0.06
            )
            polished, sqp = epigraph_all(polished)
            polished_maxima.append(maximum(polished))
            candidates.append(
                (f"replica:{label}:{replica_index}", polished)
            )
        record["origin"] = label
        record["polished_exact_pair_maxima"] = polished_maxima
        replica_records.append(record)

    label, best = min(candidates, key=lambda item: maximum(item[1]))
    best_diagnostics = diagnostics(best)
    threshold_triggered = best_diagnostics["maximum"] <= TARGET
    # A floating result at the threshold is never silently upgraded.  The
    # caller must run a separate exact/interval reconstruction workflow.
    disposition = (
        "THRESHOLD HIT — UNVERIFIED; EXACT/INTERVAL RECONSTRUCTION REQUIRED"
        if threshold_triggered
        else "NO THRESHOLD-FEASIBLE FLOATING CANDIDATE"
    )
    return {
        "n": n,
        "seed": int(seed),
        "inherited": {
            "run_index": inherited["run_index"],
            "seed": inherited["seed"],
            "origin": inherited["origin"],
            "maximum": inherited["maximum"],
        },
        "core_rattler_analysis": core_analysis,
        "alternative_core_records": alternative_core_records,
        "d5_release_record": d5_record,
        "core_quake_records": core_quake_records,
        "surgery_records": surgery_records,
        "replica_records": replica_records,
        "candidate_count": len(candidates),
        "best_label": label,
        "best": best_diagnostics,
        "threshold_triggered": threshold_triggered,
        "disposition": disposition,
        "elapsed_seconds": time.time() - started,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--n", type=int, nargs="+", default=[41, 42, 43, 44])
    parser.add_argument("--seed", type=int, default=2026072390)
    parser.add_argument("--hole-samples", type=int, default=4096)
    parser.add_argument("--hole-starts", type=int, default=6)
    parser.add_argument("--search-iterations", type=int, default=160)
    parser.add_argument("--replica-sweeps", type=int, default=240)
    parser.add_argument("--random-starts", type=int, default=1)
    parser.add_argument("--beam-width", type=int, default=4)
    parser.add_argument("--facet-choices", type=int, default=3)
    parser.add_argument("--core-random-starts", type=int, default=3)
    arguments = parser.parse_args(argv)
    if any(n < 41 or n > 44 for n in arguments.n):
        parser.error("this challenge is scoped to 41 <= N <= 44")
    if arguments.hole_samples < arguments.hole_starts:
        parser.error("--hole-samples must be at least --hole-starts")
    inherited = load_best_prior(arguments.input)
    missing = sorted(set(arguments.n) - set(inherited))
    if missing:
        parser.error(f"input has no coordinates for N={missing}")
    started = time.time()
    runs = []
    for n in arguments.n:
        print(f"N={n}: unrestricted core/rattler challenge", flush=True)
        run = challenge_one(
            n,
            inherited[n],
            seed=arguments.seed + 1009 * n,
            hole_samples=arguments.hole_samples,
            hole_starts=arguments.hole_starts,
            search_iterations=arguments.search_iterations,
            replica_sweeps=arguments.replica_sweeps,
            random_starts=arguments.random_starts,
            beam_width=arguments.beam_width,
            facet_choices=arguments.facet_choices,
            core_random_starts=arguments.core_random_starts,
        )
        print(
            f"  best={run['best']['maximum']:.16f} "
            f"label={run['best_label']}",
            flush=True,
        )
        runs.append(run)
    output = {
        "status": STATUS,
        "statement": (
            "All coordinates and optimization results are binary64 numerical "
            "evidence only. A threshold hit is explicitly withheld from any "
            "construction claim until exact or directed-interval verification."
        ),
        "method": (
            "unrestricted 2--8 vertex deletion/global cap reinsertion, "
            "joint block and all-vertex continuation, active-set bundle "
            "refinement, and threshold-energy replica exchange"
        ),
        "input": {
            "path": str(arguments.input),
            "sha256": sha256(arguments.input),
        },
        "parameters": {
            "n": arguments.n,
            "master_seed": arguments.seed,
            "hole_samples": arguments.hole_samples,
            "hole_starts": arguments.hole_starts,
            "search_iterations": arguments.search_iterations,
            "replica_sweeps": arguments.replica_sweeps,
            "random_starts": arguments.random_starts,
            "beam_width": arguments.beam_width,
            "facet_choices": arguments.facet_choices,
            "core_random_starts": arguments.core_random_starts,
        },
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "runs": runs,
        "elapsed_seconds": time.time() - started,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
