#!/usr/bin/env python3
"""Hard active-contact surgery for 41--44 points on S^4.

This is numerical discovery code, not a proof of feasibility or
nonexistence.  In particular, a local minimum returned by this program says
nothing about the global kissing-number problem.

Unlike the smooth-max construction searches elsewhere in the repository,
this program never uses log-sum-exp or another differentiable replacement
for the maximum.  Its continuous step is the literal tangent Chebyshev LP

    minimize s
    f_e(X) + D f_e(X)[d] <= max(f(X)) + s

on an explicitly rebuilt band of worst edges.  It supplements this with
single-vertex LP sweeps, greedy vertex-cover block moves, rank-five Gram
clipping/completion, and coordinated directions in the nullspace of the
active-contact Jacobian (after removing the ten infinitesimal rotations).
Graph-guided deletion/reinsertion uses equal-contact intersections rather
than a smooth maximin-hole objective.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import platform
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import linprog


DIMENSION = 5
STATUS = "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE"


def unit_rows(array: np.ndarray) -> np.ndarray:
    x = np.asarray(array, dtype=np.float64)
    if x.ndim != 2 or x.shape[1] != DIMENSION:
        raise ValueError("coordinates must be an N by 5 array")
    norms = np.linalg.norm(x, axis=1)
    if float(np.min(norms)) <= 1e-14:
        raise ValueError("cannot normalize a zero row")
    return x / norms[:, None]


def pair_indices(n: int) -> tuple[np.ndarray, np.ndarray]:
    return np.triu_indices(n, 1)


def pair_values(x: np.ndarray) -> np.ndarray:
    x = unit_rows(x)
    first, second = pair_indices(len(x))
    return np.sum(x[first] * x[second], axis=1)


def maximum(x: np.ndarray) -> float:
    return float(np.max(pair_values(x)))


def tangent_bases(x: np.ndarray) -> np.ndarray:
    """Return deterministic 5-by-4 orthonormal bases of row tangent spaces."""
    x = unit_rows(x)
    bases = np.empty((len(x), DIMENSION, DIMENSION - 1))
    for index, row in enumerate(x):
        # Full SVD fixes a stable orthonormal complement.  Its signs are not
        # mathematically significant, and the search records final arrays.
        _, _, vh = np.linalg.svd(row.reshape(1, DIMENSION), full_matrices=True)
        bases[index] = vh[1:].T
    return bases


def retract(x: np.ndarray, tangent: np.ndarray, scale: float = 1.0) -> np.ndarray:
    x = unit_rows(x)
    tangent = np.asarray(tangent, dtype=float)
    tangent -= np.sum(tangent * x, axis=1)[:, None] * x
    return unit_rows(x + float(scale) * tangent)


def hard_score(x: np.ndarray) -> tuple[float, float, float, float]:
    """Lexicographic order-statistic merit; no smooth maximum surrogate."""
    values = np.sort(pair_values(x))[::-1]
    return (
        float(values[0]),
        float(np.sum(values[: min(24, len(values))])),
        float(np.sum(values[: min(96, len(values))])),
        float(np.sum(np.maximum(values - 0.5, 0.0) ** 2)),
    )


def score_better(
    candidate: tuple[float, ...],
    incumbent: tuple[float, ...],
    primary_slack: float = 2e-13,
) -> bool:
    """Compare a candidate without allowing a material increase of the max."""
    if candidate[0] < incumbent[0] - 2e-13:
        return True
    if candidate[0] > incumbent[0] + primary_slack:
        return False
    for left, right in zip(candidate[1:], incumbent[1:]):
        tolerance = 5e-12 * max(1.0, abs(right))
        if left < right - tolerance:
            return True
        if left > right + tolerance:
            return False
    return False


def active_edges(
    x: np.ndarray, band: float, minimum_edges: int = 16
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    values = pair_values(x)
    first, second = pair_indices(len(x))
    top = float(np.max(values))
    chosen = np.flatnonzero(values >= top - float(band))
    if len(chosen) < minimum_edges:
        chosen = np.argsort(values)[-min(minimum_edges, len(values)) :]
    chosen = chosen[np.argsort(values[chosen])[::-1]]
    return first[chosen], second[chosen], values[chosen], chosen


def contact_jacobian(
    x: np.ndarray,
    first: np.ndarray,
    second: np.ndarray,
    bases: np.ndarray | None = None,
) -> np.ndarray:
    """Jacobian of selected pair products in 4N tangent coordinates."""
    x = unit_rows(x)
    if bases is None:
        bases = tangent_bases(x)
    jacobian = np.zeros((len(first), 4 * len(x)))
    for row, (i, j) in enumerate(zip(first, second)):
        jacobian[row, 4 * i : 4 * i + 4] = bases[i].T @ x[j]
        jacobian[row, 4 * j : 4 * j + 4] = bases[j].T @ x[i]
    return jacobian


def greedy_vertex_cover(
    n: int, first: np.ndarray, second: np.ndarray, cap: int | None = None
) -> list[int]:
    """Deterministic greedy cover of the current active-edge graph."""
    remaining = {(int(i), int(j)) for i, j in zip(first, second)}
    cover: list[int] = []
    while remaining and (cap is None or len(cover) < cap):
        degrees = np.zeros(n, dtype=int)
        for i, j in remaining:
            degrees[i] += 1
            degrees[j] += 1
        vertex = int(np.flatnonzero(degrees == np.max(degrees))[0])
        cover.append(vertex)
        remaining = {
            (i, j) for i, j in remaining if i != vertex and j != vertex
        }
    return cover


def tangent_chebyshev_lp(
    x: np.ndarray,
    radius: float,
    band: float,
    movable: list[int] | np.ndarray | None = None,
    incident_vertex: int | None = None,
) -> tuple[np.ndarray | None, dict]:
    """Solve the hard linearized minimax problem on a selected active set."""
    x = unit_rows(x)
    n = len(x)
    bases = tangent_bases(x)
    all_first, all_second = pair_indices(n)
    all_values = pair_values(x)
    top = float(np.max(all_values))

    if incident_vertex is None:
        first, second, values, ids = active_edges(x, band)
    else:
        mask = (all_first == incident_vertex) | (all_second == incident_vertex)
        ids = np.flatnonzero(mask)
        order = np.argsort(all_values[ids])[::-1]
        ids = ids[order]
        first, second, values = (
            all_first[ids],
            all_second[ids],
            all_values[ids],
        )

    jacobian = contact_jacobian(x, first, second, bases)
    variable_count = 4 * n + 1
    objective = np.zeros(variable_count)
    objective[-1] = 1.0
    inequalities = np.column_stack([jacobian, -np.ones(len(jacobian))])
    right_hand_side = top - values

    if movable is None:
        movable_set = set(range(n))
    else:
        movable_set = {int(v) for v in movable}
    bounds: list[tuple[float | None, float | None]] = []
    for vertex in range(n):
        bound = (-float(radius), float(radius)) if vertex in movable_set else (0.0, 0.0)
        bounds.extend([bound] * 4)
    bounds.append((None, None))
    result = linprog(
        objective,
        A_ub=inequalities,
        b_ub=right_hand_side,
        bounds=bounds,
        method="highs",
        options={"presolve": True},
    )
    record = {
        "solver_success": bool(result.success),
        "solver_status": int(result.status),
        "active_edge_count": int(len(ids)),
        "radius": float(radius),
        "band": float(band),
        "movable_count": int(len(movable_set)),
        "incident_vertex": (
            int(incident_vertex) if incident_vertex is not None else None
        ),
    }
    if not result.success:
        record["message"] = str(result.message)
        return None, record
    coefficients = result.x[:-1].reshape(n, 4)
    tangent = np.einsum("nij,nj->ni", bases, coefficients)
    predicted_slope = float(result.x[-1])
    record.update(
        {
            "predicted_linear_peak_change": predicted_slope,
            "tangent_frobenius_norm": float(np.linalg.norm(tangent)),
            "tangent_max_row_norm": float(
                np.max(np.linalg.norm(tangent, axis=1))
            ),
        }
    )
    return tangent, record


def best_retracted_candidate(
    x: np.ndarray,
    tangent: np.ndarray,
    allow_equal_primary: bool = False,
) -> tuple[np.ndarray, dict]:
    before = hard_score(x)
    best = x
    best_score = before
    best_scale = 0.0
    trials = []
    for scale in (1.0, 0.72, 0.5, 0.32, 0.2, 0.12, 0.06):
        candidate = retract(x, tangent, scale)
        score = hard_score(candidate)
        acceptable = score_better(
            score,
            best_score,
            primary_slack=(2e-13 if allow_equal_primary else 0.0),
        )
        trials.append([float(scale), float(score[0])])
        if acceptable:
            best, best_score, best_scale = candidate, score, float(scale)
    return best, {
        "accepted": bool(best_scale > 0.0),
        "scale": best_scale,
        "before_maximum": before[0],
        "after_maximum": best_score[0],
        "trial_maxima": trials,
    }


def sequential_point_sweep(
    x: np.ndarray, radius: float, count: int
) -> tuple[np.ndarray, dict]:
    """Move stressed points one at a time using literal incident-edge LPs."""
    x = unit_rows(x)
    values = pair_values(x)
    first, second = pair_indices(len(x))
    top = float(np.max(values))
    stress = np.zeros(len(x))
    cutoff = top - max(2e-3, 5.0 * radius)
    weights = np.maximum(values - cutoff, 0.0)
    np.add.at(stress, first, weights)
    np.add.at(stress, second, weights)
    order = np.argsort(stress)[::-1][: min(count, len(x))]
    accepted = 0
    details = []
    for vertex in order:
        tangent, lp_record = tangent_chebyshev_lp(
            x,
            radius=radius,
            band=1.0,
            movable=[int(vertex)],
            incident_vertex=int(vertex),
        )
        if tangent is None:
            details.append({"vertex": int(vertex), "lp": lp_record})
            continue
        candidate, step = best_retracted_candidate(
            x, tangent, allow_equal_primary=True
        )
        if step["accepted"]:
            x = candidate
            accepted += 1
        details.append(
            {
                "vertex": int(vertex),
                "stress": float(stress[vertex]),
                "lp": lp_record,
                "step": step,
            }
        )
    return x, {
        "attempted_vertices": [int(v) for v in order],
        "accepted_moves": accepted,
        "details": details,
    }


def hard_active_refine(
    x: np.ndarray,
    iterations: int,
    initial_radius: float,
    point_sweeps: bool = True,
) -> tuple[np.ndarray, list[dict]]:
    """Trust loop alternating cover-block and full hard active-set LPs."""
    x = unit_rows(x)
    radius = float(initial_radius)
    history = []
    failures = 0
    for iteration in range(iterations):
        before = maximum(x)
        band = max(2e-5, min(0.18, 5.0 * radius))
        first, second, _, _ = active_edges(x, band)
        cover = greedy_vertex_cover(
            len(x), first, second, cap=max(8, int(0.72 * len(x)))
        )
        # Alternate a sparse graph-cover block with a global step.  The former
        # changes which edges can become active; the latter settles the basin.
        movable = cover if iteration % 3 != 2 else list(range(len(x)))
        tangent, lp_record = tangent_chebyshev_lp(
            x, radius=radius, band=band, movable=movable
        )
        if tangent is None:
            accepted = False
            step_record = {"accepted": False}
        else:
            candidate, step_record = best_retracted_candidate(x, tangent)
            accepted = bool(step_record["accepted"])
            if accepted:
                x = candidate

        point_record = None
        if point_sweeps and iteration % 5 == 4:
            candidate, point_record = sequential_point_sweep(
                x, radius=max(radius * 0.65, 2e-4), count=10
            )
            if hard_score(candidate)[0] <= maximum(x) + 2e-13:
                x = candidate

        after = maximum(x)
        if after < before - 5e-12:
            radius = min(0.08, radius * 1.12)
            failures = 0
        else:
            radius *= 0.55
            failures += 1
        history.append(
            {
                "iteration": iteration,
                "before_maximum": before,
                "after_maximum": after,
                "band": band,
                "cover_size": len(cover),
                "movable_size": len(movable),
                "lp": lp_record,
                "step": step_record,
                "point_sweep": point_record,
                "next_radius": radius,
            }
        )
        if failures >= 8 or radius < 2e-7:
            break
    return x, history


def procrustes_align(reference: np.ndarray, candidate: np.ndarray) -> np.ndarray:
    left, _, right = np.linalg.svd(candidate.T @ reference)
    return candidate @ (left @ right)


def gram_clip_completion(
    x: np.ndarray, target: float, rounds: int, blend: float
) -> tuple[np.ndarray, list[dict]]:
    """Alternate hard Gram clipping with projection to PSD rank five."""
    x = unit_rows(x)
    history = []
    for iteration in range(rounds):
        gram = x @ x.T
        clipped = gram.copy()
        mask = (clipped > target) & (~np.eye(len(x), dtype=bool))
        clipped[mask] = target
        eigenvalues, eigenvectors = np.linalg.eigh(clipped)
        positive = np.maximum(eigenvalues[-DIMENSION:], 0.0)
        candidate = eigenvectors[:, -DIMENSION:] * np.sqrt(positive)[None, :]
        candidate = unit_rows(candidate)
        candidate = procrustes_align(x, candidate)
        candidate = unit_rows((1.0 - blend) * x + blend * candidate)
        history.append(
            {
                "iteration": iteration,
                "clipped_ordered_entries": int(np.sum(mask)),
                "clipped_matrix_minimum_eigenvalue": float(eigenvalues[0]),
                "retained_eigenvalues": [float(v) for v in positive],
                "before_maximum": maximum(x),
                "after_maximum": maximum(candidate),
            }
        )
        x = candidate
    return x, history


def rotation_coefficient_basis(
    x: np.ndarray, bases: np.ndarray
) -> np.ndarray:
    """Ten product-sphere tangent directions induced by O(5)."""
    columns = []
    for first in range(DIMENSION):
        for second in range(first + 1, DIMENSION):
            omega = np.zeros((DIMENSION, DIMENSION))
            omega[first, second] = 1.0
            omega[second, first] = -1.0
            ambient = x @ omega
            coefficients = np.einsum("nij,ni->nj", bases, ambient).ravel()
            columns.append(coefficients)
    matrix = np.column_stack(columns)
    q, _ = np.linalg.qr(matrix)
    return q[:, :10]


def contact_nullspace(
    x: np.ndarray, tolerance: float
) -> tuple[np.ndarray, dict]:
    """Nullspace of the active Jacobian, modulo infinitesimal rotations."""
    x = unit_rows(x)
    top = maximum(x)
    first, second, values, _ = active_edges(
        x, band=tolerance, minimum_edges=1
    )
    keep = values >= top - tolerance
    first, second = first[keep], second[keep]
    bases = tangent_bases(x)
    jacobian = contact_jacobian(x, first, second, bases)
    _, singular_values, vh = np.linalg.svd(jacobian, full_matrices=True)
    threshold = max(jacobian.shape) * np.finfo(float).eps * max(
        1.0, float(singular_values[0]) if len(singular_values) else 1.0
    )
    rank = int(np.sum(singular_values > threshold))
    nullspace = vh[rank:].T
    rotations = rotation_coefficient_basis(x, bases)
    projected = nullspace - rotations @ (rotations.T @ nullspace)
    if projected.size:
        u, projected_singular, _ = np.linalg.svd(
            projected, full_matrices=False
        )
        nonrot_rank = int(np.sum(projected_singular > 2e-10))
        nonrot = u[:, :nonrot_rank]
    else:
        projected_singular = np.empty(0)
        nonrot = np.empty((4 * len(x), 0))
        nonrot_rank = 0
    record = {
        "active_edge_count": int(len(first)),
        "jacobian_shape": [int(v) for v in jacobian.shape],
        "jacobian_rank": rank,
        "raw_nullity": int(nullspace.shape[1]),
        "rotation_rank": int(np.linalg.matrix_rank(rotations, tol=1e-10)),
        "nonrotational_nullity": nonrot_rank,
        "smallest_jacobian_singular_values": [
            float(v) for v in singular_values[-min(12, len(singular_values)) :]
        ],
        "projected_null_singular_values": [
            float(v)
            for v in projected_singular[: min(12, len(projected_singular))]
        ],
    }
    return nonrot, record


def null_escape_candidates(
    x: np.ndarray,
    rng: np.random.Generator,
    tolerance: float,
    candidate_count: int,
) -> tuple[list[np.ndarray], dict]:
    x = unit_rows(x)
    bases = tangent_bases(x)
    space, record = contact_nullspace(x, tolerance)
    candidates: list[np.ndarray] = []
    if space.shape[1] == 0:
        return candidates, record
    coefficient_vectors = [space[:, k] for k in range(min(space.shape[1], 6))]
    for _ in range(candidate_count):
        combination = space @ rng.normal(size=space.shape[1])
        coefficient_vectors.append(combination)
    for coefficients in coefficient_vectors:
        tangent = np.einsum(
            "nij,nj->ni", bases, coefficients.reshape(len(x), 4)
        )
        rms = float(np.linalg.norm(tangent) / math.sqrt(len(x)))
        if rms <= 1e-14:
            continue
        tangent /= rms
        for scale in (0.006, 0.018, 0.05, 0.12):
            candidates.append(retract(x, tangent, scale))
            candidates.append(retract(x, tangent, -scale))
    record["generated_candidate_count"] = len(candidates)
    return candidates, record


def equal_contact_candidates(
    fixed: np.ndarray,
    neighbor_pool: np.ndarray,
    rng: np.random.Generator,
    trials: int,
) -> list[np.ndarray]:
    """Generate intersections where five selected fixed contacts are equal."""
    fixed = unit_rows(fixed)
    pool = np.asarray(neighbor_pool, dtype=int)
    candidates: list[np.ndarray] = []
    if len(pool) >= 5:
        seen: set[tuple[int, ...]] = set()
        for _ in range(trials):
            choice = tuple(sorted(int(v) for v in rng.choice(pool, 5, replace=False)))
            if choice in seen:
                continue
            seen.add(choice)
            rows = fixed[np.asarray(choice)]
            differences = rows[1:] - rows[0]
            _, singular, vh = np.linalg.svd(differences, full_matrices=True)
            if len(singular) and singular[-1] < 1e-10:
                # Degenerate contact tuples are allowed, but their nullspace
                # is not a uniquely determined isolated candidate.
                continue
            direction = vh[-1]
            direction /= np.linalg.norm(direction)
            candidates.extend([direction, -direction])
    return candidates


def graph_reinsert(
    x: np.ndarray,
    rng: np.random.Generator,
    block_size: int,
    intersection_trials: int,
    random_trials: int,
) -> tuple[np.ndarray, dict]:
    """Delete a stressed graph block and reinsert via contact intersections."""
    x = unit_rows(x)
    first, second, _, _ = active_edges(x, band=2e-3, minimum_edges=20)
    cover = greedy_vertex_cover(len(x), first, second, cap=block_size)
    if len(cover) < block_size:
        degrees = np.zeros(len(x), dtype=int)
        np.add.at(degrees, first, 1)
        np.add.at(degrees, second, 1)
        for vertex in np.argsort(degrees)[::-1]:
            if int(vertex) not in cover:
                cover.append(int(vertex))
            if len(cover) == block_size:
                break
    removed = set(cover)
    fixed = np.asarray([row for index, row in enumerate(x) if index not in removed])
    reinsertion_records = []
    for old_vertex in cover:
        old = x[old_vertex]
        scores = fixed @ old
        pool = np.argsort(scores)[::-1][: min(15, len(fixed))]
        candidates = equal_contact_candidates(
            fixed, pool, rng, intersection_trials
        )
        random_rows = unit_rows(rng.normal(size=(random_trials, DIMENSION)))
        candidates.extend(random_rows)
        candidate_array = unit_rows(np.asarray(candidates))
        maxima = np.max(candidate_array @ fixed.T, axis=1)
        best_index = int(np.argmin(maxima))
        chosen = candidate_array[best_index]
        fixed = np.vstack([fixed, chosen])
        reinsertion_records.append(
            {
                "old_vertex": int(old_vertex),
                "candidate_count": int(len(candidate_array)),
                "chosen_fixed_maximum": float(maxima[best_index]),
                "chosen_from_equal_contact": bool(
                    best_index < len(candidate_array) - random_trials
                ),
            }
        )
    return unit_rows(fixed), {
        "removed_vertices": cover,
        "block_size": len(cover),
        "reinsertions": reinsertion_records,
        "result_maximum": maximum(fixed),
    }


def random_greedy_start(
    n: int, rng: np.random.Generator, candidates_per_point: int
) -> np.ndarray:
    """Nonsymmetric non-grid random start with discrete farthest sampling."""
    x = unit_rows(rng.normal(size=(1, DIMENSION)))
    while len(x) < n:
        candidates = unit_rows(
            rng.normal(size=(int(candidates_per_point), DIMENSION))
        )
        scores = np.max(candidates @ x.T, axis=1)
        x = np.vstack([x, candidates[int(np.argmin(scores))]])
    return x


def load_stored_near_miss(n: int, repository_root: Path) -> tuple[np.ndarray, str]:
    if n == 41:
        path = repository_root / "experiments/input/spherical_codes_5_41.txt"
        x = np.loadtxt(path, delimiter=",")
        return unit_rows(x), str(path.relative_to(repository_root))
    if n in (42, 43):
        path = (
            repository_root
            / "experiments/construction_round9_core_rattler/results"
            / "core_rattler_portfolio.json"
        )
        payload = json.loads(path.read_text())
        record = next(run for run in payload["runs"] if int(run["n"]) == n)
        x = np.asarray(record["best"]["coordinates_float64"], dtype=float)
        return unit_rows(x), (
            f"{path.relative_to(repository_root)}:runs[n={n}].best"
        )
    if n == 44:
        path = (
            repository_root
            / "experiments/construction_round6_bundle/results"
            / "bundle_portfolio.json"
        )
        payload = json.loads(path.read_text())
        record = payload["runs"][19]
        if int(record["n"]) != 44:
            raise ValueError("expected the stored N=44 near miss at run 19")
        x = np.asarray(record["best"]["coordinates_float64"], dtype=float)
        return unit_rows(x), f"{path.relative_to(repository_root)}:runs[19].best"
    raise ValueError(f"unsupported cardinality {n}")


def connected_components(n: int, edges: list[list[int]]) -> list[int]:
    adjacency = [[] for _ in range(n)]
    for first, second in edges:
        adjacency[first].append(second)
        adjacency[second].append(first)
    seen: set[int] = set()
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


def coordinate_sha256(x: np.ndarray) -> str:
    normalized = np.ascontiguousarray(unit_rows(x), dtype="<f8")
    return hashlib.sha256(normalized.tobytes()).hexdigest()


def contact_summary(x: np.ndarray, tolerance: float) -> dict:
    values = pair_values(x)
    first, second = pair_indices(len(x))
    top = float(np.max(values))
    chosen = values >= top - tolerance
    edges = np.column_stack([first[chosen], second[chosen]]).astype(int).tolist()
    degrees = np.zeros(len(x), dtype=int)
    for i, j in edges:
        degrees[i] += 1
        degrees[j] += 1
    unique, counts = np.unique(degrees, return_counts=True)
    return {
        "tolerance": float(tolerance),
        "edge_count": len(edges),
        "degree_histogram": {
            str(int(degree)): int(count)
            for degree, count in zip(unique, counts)
        },
        "component_sizes": connected_components(len(x), edges),
        "edge_sha256": hashlib.sha256(
            json.dumps(edges, separators=(",", ":")).encode()
        ).hexdigest(),
        "edges": edges,
    }


def diagnostics(x: np.ndarray) -> dict:
    x = unit_rows(x)
    n = len(x)
    gram = x @ x.T
    first, second = pair_indices(n)
    # Use the same literal rowwise binary64 scan as the search objective.
    # Matrix multiplication may associate the five additions differently and
    # can move an exactly tied maximizing pair by one ulp.
    values = pair_values(x)
    top = float(np.max(values))
    maximizing = np.flatnonzero(values == top)
    full_spectrum = np.linalg.eigvalsh(gram)
    coordinate_spectrum = np.linalg.eigvalsh(x.T @ x)
    return {
        "n": n,
        "dimension": DIMENSION,
        "coordinates_float64": x.tolist(),
        "coordinate_little_endian_float64_sha256": coordinate_sha256(x),
        "maximum_inner_product_binary64": top,
        "maximum_inner_product_float_hex": top.hex(),
        "literal_binary64_maximizing_pairs": [
            [int(first[k]), int(second[k])] for k in maximizing
        ],
        "gap_above_one_half": top - 0.5,
        "meets_threshold_binary64": bool(top <= 0.5),
        "minimum_inner_product_binary64": float(np.min(values)),
        "row_norm_max_error": float(
            np.max(np.abs(np.sum(x * x, axis=1) - 1.0))
        ),
        "pairs_above_one_half": int(np.sum(values > 0.5)),
        "pairs_equal_one_half_binary64": int(np.sum(values == 0.5)),
        "positive_gram_eigenvalues": [float(v) for v in coordinate_spectrum],
        "gram_tail_max_abs": float(
            np.max(np.abs(full_spectrum[:-DIMENSION]))
        ),
        "pair_quantiles": {
            f"{q:.3f}": float(np.quantile(values, q))
            for q in (0.0, 0.01, 0.05, 0.5, 0.95, 0.99, 1.0)
        },
        "active_1e-4": contact_summary(x, 1e-4),
        "active_1e-6": contact_summary(x, 1e-6),
        "active_1e-8": contact_summary(x, 1e-8),
    }


def compact_history(history: list[dict]) -> dict:
    return {
        "iterations": len(history),
        "accepted_steps": int(
            sum(bool(item.get("step", {}).get("accepted")) for item in history)
        ),
        "initial_maximum": (
            float(history[0]["before_maximum"]) if history else None
        ),
        "final_maximum": (
            float(history[-1]["after_maximum"]) if history else None
        ),
        "records": history,
    }


def run_trajectory(
    n: int,
    seed: int,
    origin: str,
    initial: np.ndarray,
    refine_iterations: int,
    escape_cycles: int,
) -> dict:
    rng = np.random.default_rng(seed)
    started = time.time()
    initial = unit_rows(initial)
    x, initial_history = hard_active_refine(
        initial,
        iterations=refine_iterations,
        initial_radius=(0.012 if origin == "stored_near_miss" else 0.055),
    )
    best = x.copy() if maximum(x) < maximum(initial) else initial.copy()
    current = x
    phases = []
    for cycle in range(escape_cycles):
        phase: dict = {"cycle": cycle, "start_maximum": maximum(current)}
        null_candidates, null_record = null_escape_candidates(
            current, rng, tolerance=(1e-6 if cycle % 2 == 0 else 1e-4),
            candidate_count=2,
        )
        # Evaluate the most promising null escapes after a short hard settle.
        null_candidates.sort(key=maximum)
        null_trials = []
        for candidate in null_candidates[:6]:
            settled, settle_history = hard_active_refine(
                candidate,
                iterations=max(8, refine_iterations // 3),
                initial_radius=0.018,
                point_sweeps=False,
            )
            null_trials.append(
                {
                    "pre_settle_maximum": maximum(candidate),
                    "post_settle_maximum": maximum(settled),
                    "settle_iterations": len(settle_history),
                }
            )
            if maximum(settled) < maximum(best):
                best = settled.copy()
            if maximum(settled) < maximum(current) + 3e-3:
                current = settled
        phase["nullspace"] = null_record
        phase["null_trials"] = null_trials

        gram_candidate, gram_history = gram_clip_completion(
            current,
            target=maximum(current) - (7e-4 + cycle * 2e-4),
            rounds=2,
            blend=0.45,
        )
        gram_settled, gram_settle = hard_active_refine(
            gram_candidate,
            iterations=max(10, refine_iterations // 2),
            initial_radius=0.012,
            point_sweeps=False,
        )
        phase["gram_completion"] = gram_history
        phase["gram_settle_final_maximum"] = maximum(gram_settled)
        phase["gram_settle_iterations"] = len(gram_settle)
        if maximum(gram_settled) < maximum(best):
            best = gram_settled.copy()
        if maximum(gram_settled) < maximum(current) + 2e-3:
            current = gram_settled

        reinserted, reinsert_record = graph_reinsert(
            current,
            rng,
            block_size=2 + cycle % 3,
            intersection_trials=100,
            random_trials=500,
        )
        reinserted_settled, reinsert_settle = hard_active_refine(
            reinserted,
            iterations=max(12, refine_iterations // 2),
            initial_radius=0.035,
            point_sweeps=True,
        )
        phase["graph_reinsertion"] = reinsert_record
        phase["reinsert_settle_final_maximum"] = maximum(reinserted_settled)
        phase["reinsert_settle_iterations"] = len(reinsert_settle)
        if maximum(reinserted_settled) < maximum(best):
            best = reinserted_settled.copy()
        # Deliberately continue in a changed contact basin even when uphill.
        current = reinserted_settled
        phase["end_maximum"] = maximum(current)
        phase["best_so_far"] = maximum(best)
        phases.append(phase)

    final, final_history = hard_active_refine(
        best,
        iterations=max(refine_iterations, 24),
        initial_radius=0.008,
        point_sweeps=True,
    )
    if maximum(final) < maximum(best):
        best = final
    return {
        "n": n,
        "seed": int(seed),
        "origin": origin,
        "initial": diagnostics(initial),
        "initial_refinement": compact_history(initial_history),
        "escape_phases": phases,
        "final_refinement": compact_history(final_history),
        "best": diagnostics(best),
        "elapsed_seconds": time.time() - started,
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", nargs="+", type=int, default=[41, 42, 43, 44])
    parser.add_argument(
        "--stored-seed", type=int, default=2026072501,
        help="base deterministic seed for stored near-miss paths",
    )
    parser.add_argument(
        "--random-seed", type=int, default=2026072591,
        help="base deterministic seed for random greedy paths",
    )
    parser.add_argument("--refine-iterations", type=int, default=32)
    parser.add_argument("--escape-cycles", type=int, default=2)
    parser.add_argument("--random-candidates-per-point", type=int, default=3000)
    parser.add_argument(
        "--origins",
        nargs="+",
        choices=["stored", "random"],
        default=["stored", "random"],
    )
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    repository_root = Path(__file__).resolve().parents[3]
    runs = []
    for n in arguments.n:
        if n not in (41, 42, 43, 44):
            raise ValueError("this portfolio is scoped to N=41,42,43,44")
        if "stored" in arguments.origins:
            initial, provenance = load_stored_near_miss(n, repository_root)
            runs.append(
                run_trajectory(
                    n=n,
                    seed=arguments.stored_seed + 101 * n,
                    origin="stored_near_miss",
                    initial=initial,
                    refine_iterations=arguments.refine_iterations,
                    escape_cycles=arguments.escape_cycles,
                )
            )
            runs[-1]["input_provenance"] = provenance
        if "random" in arguments.origins:
            seed = arguments.random_seed + 101 * n
            rng = np.random.default_rng(seed)
            initial = random_greedy_start(
                n, rng, arguments.random_candidates_per_point
            )
            runs.append(
                run_trajectory(
                    n=n,
                    seed=seed,
                    origin="random_greedy",
                    initial=initial,
                    refine_iterations=arguments.refine_iterations,
                    escape_cycles=arguments.escape_cycles,
                )
            )

    best_by_n = {}
    for n in arguments.n:
        eligible = [run for run in runs if int(run["n"]) == n]
        chosen = min(
            eligible,
            key=lambda run: run["best"]["maximum_inner_product_binary64"],
        )
        best_by_n[str(n)] = {
            "seed": chosen["seed"],
            "origin": chosen["origin"],
            "maximum_inner_product_binary64": chosen["best"][
                "maximum_inner_product_binary64"
            ],
            "maximum_inner_product_float_hex": chosen["best"][
                "maximum_inner_product_float_hex"
            ],
            "coordinate_little_endian_float64_sha256": chosen["best"][
                "coordinate_little_endian_float64_sha256"
            ],
            "meets_threshold_binary64": chosen["best"][
                "meets_threshold_binary64"
            ],
        }
    payload = {
        "status": STATUS,
        "method": (
            "hard tangent Chebyshev active-set LP; sequential point and "
            "greedy-cover block moves; contact-nullspace escape modulo "
            "rotations; rank-five Gram clipping; graph reinsertion"
        ),
        "smooth_surrogate_used": False,
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
        },
        "parameters": {
            "n": arguments.n,
            "stored_seed": arguments.stored_seed,
            "random_seed": arguments.random_seed,
            "refine_iterations": arguments.refine_iterations,
            "escape_cycles": arguments.escape_cycles,
            "random_candidates_per_point": arguments.random_candidates_per_point,
            "origins": arguments.origins,
        },
        "runs": runs,
        "best_by_n": best_by_n,
        "binary64_threshold_hit": any(
            run["best"]["meets_threshold_binary64"] for run in runs
        ),
        "warning": (
            "All maxima and spectra describe stored binary64 arrays. "
            "Failure to find a configuration is not an upper bound."
        ),
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(best_by_n, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
