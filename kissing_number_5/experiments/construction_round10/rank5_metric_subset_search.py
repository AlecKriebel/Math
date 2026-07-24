#!/usr/bin/env python3
"""Alternating finite-shell subset and general rank-five metric search.

This is floating-point discovery code, not a mathematical certificate.

For a finite root shell R in R^m and a matrix B in R^{m x 5}, the image is

    x_r = r B / ||r B||.

Thus Q = B B^T is a positive-semidefinite metric of rank at most five.  The
search alternates a discrete exact-cardinality subset heuristic on the whole
mapped shell with smooth minimax optimization of B for the chosen subset.
This strictly contains orthogonal-kernel projection as a special case because
the five nonzero singular values of B are free.  After the structured stage,
the best candidates are released into an unrestricted product-of-spheres
continuation and direct epigraph SQP polish.

All stored maxima are recomputed from the stored binary64 coordinates.
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


STATUS = "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE"


def unit_rows(array: np.ndarray) -> np.ndarray:
    array = np.asarray(array, dtype=float)
    norms = np.linalg.norm(array, axis=1)
    if array.ndim != 2 or float(np.min(norms)) <= 1e-13:
        raise ValueError("coordinates must be a matrix with nonzero rows")
    return array / norms[:, None]


def pair_indices(n: int) -> tuple[np.ndarray, np.ndarray]:
    return np.triu_indices(n, 1)


def pair_values(array: np.ndarray) -> np.ndarray:
    x = unit_rows(array)
    ii, jj = pair_indices(len(x))
    return np.sum(x[ii] * x[jj], axis=1)


def maximum_inner_product(array: np.ndarray) -> float:
    return float(np.max(pair_values(array)))


def d_roots(dimension: int) -> tuple[np.ndarray, list[dict]]:
    rows: list[np.ndarray] = []
    labels: list[dict] = []
    for first in range(dimension):
        for second in range(first + 1, dimension):
            for sign_first in (-1, 1):
                for sign_second in (-1, 1):
                    row = np.zeros(dimension)
                    row[first] = sign_first / math.sqrt(2.0)
                    row[second] = sign_second / math.sqrt(2.0)
                    rows.append(row)
                    labels.append(
                        {
                            "kind": f"D{dimension}",
                            "support": [first, second],
                            "signs": [sign_first, sign_second],
                        }
                    )
    return np.asarray(rows), labels


def e6_roots() -> tuple[np.ndarray, list[dict]]:
    d5, labels = d_roots(5)
    rows = [np.r_[row, 0.0] for row in d5]
    answer_labels = [
        {"kind": "E6_D5", **{k: v for k, v in label.items() if k != "kind"}}
        for label in labels
    ]
    for mask in range(1 << 5):
        signs = np.asarray(
            [1 if (mask >> coordinate) & 1 else -1 for coordinate in range(5)]
        )
        sixth = int(np.prod(signs))
        row = np.r_[signs / 2.0, sixth * math.sqrt(3.0) / 2.0]
        rows.append(row / math.sqrt(2.0))
        answer_labels.append(
            {
                "kind": "E6_half",
                "signs_first5": signs.astype(int).tolist(),
                "sign6": sixth,
            }
        )
    roots = np.asarray(rows)
    if roots.shape != (72, 6):
        raise AssertionError("bad E6 enumeration")
    if maximum_inner_product(roots) > 0.500000000001:
        raise AssertionError("E6 root shell check failed")
    return roots, answer_labels


def root_shell(name: str) -> tuple[np.ndarray, list[dict]]:
    if name == "E6":
        return e6_roots()
    if name == "D6":
        return d_roots(6)
    if name == "D7":
        return d_roots(7)
    raise ValueError(f"unknown shell {name}")


def normalize_map(matrix: np.ndarray) -> np.ndarray:
    norm = float(np.linalg.norm(matrix))
    if norm <= 1e-14:
        raise ValueError("zero map")
    return matrix * (math.sqrt(5.0) / norm)


def mapped_points(roots: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    return unit_rows(roots @ matrix)


def initial_map(
    roots: np.ndarray, family: str, seed: int, mode: int
) -> tuple[np.ndarray, str]:
    """Return a deterministic full-column-rank, deliberately anisotropic map."""
    rng = np.random.default_rng(seed)
    ambient = roots.shape[1]
    if mode % 4 == 0 and ambient == 6:
        matrix = np.zeros((6, 5))
        matrix[:5, :] = np.eye(5)
        matrix += 0.025 * rng.normal(size=matrix.shape)
        label = "perturbed_coordinate_projection"
    else:
        gaussian = rng.normal(size=(ambient, 5))
        u, _, vt = np.linalg.svd(gaussian, full_matrices=False)
        # A general PSD rank-five metric: unlike an orthogonal projection,
        # its nonzero eigenvalues are not constrained to be equal.
        spectra = (
            np.asarray([1.45, 1.18, 0.95, 0.76, 0.58]),
            np.asarray([1.75, 1.26, 0.91, 0.70, 0.47]),
            np.asarray([1.25, 1.10, 0.96, 0.81, 0.68]),
        )
        singular = spectra[(mode - 1) % len(spectra)]
        matrix = u @ np.diag(singular) @ vt
        label = f"random_general_metric_spectrum_{(mode - 1) % len(spectra)}"
    matrix = normalize_map(matrix)
    if np.linalg.matrix_rank(matrix, tol=1e-11) != 5:
        raise AssertionError("initial map is not rank five")
    return matrix, label


def smooth_subset_score_from_gram(
    gram: np.ndarray, subset: np.ndarray, beta: float
) -> float:
    block = gram[np.ix_(subset, subset)]
    values = block[np.triu_indices(len(subset), 1)]
    maximum = float(np.max(values))
    return maximum + math.log(float(np.sum(np.exp(beta * (values - maximum))))) / beta


def greedy_delete_subset(
    mapped: np.ndarray, n: int, rng: np.random.Generator, beta: float = 60.0
) -> np.ndarray:
    """Delete crowded shell points until exactly n remain.

    Each deletion minimizes the smooth maximum of the remaining set.  A tiny
    seeded jitter only resolves floating ties, preserving determinism.
    """
    if n > len(mapped):
        raise ValueError("requested subset exceeds shell")
    gram = mapped @ mapped.T
    chosen = list(range(len(mapped)))
    while len(chosen) > n:
        block = gram[np.ix_(chosen, chosen)].copy()
        np.fill_diagonal(block, -np.inf)
        top = float(np.max(block))
        weights = np.exp(beta * np.maximum(block - top, -12.0))
        np.fill_diagonal(weights, 0.0)
        crowding = np.sum(weights, axis=1)
        crowding += 1e-12 * rng.normal(size=len(chosen))
        del chosen[int(np.argmax(crowding))]
    return np.asarray(sorted(chosen), dtype=int)


def local_subset_swaps(
    mapped: np.ndarray,
    subset: np.ndarray,
    beta: float = 220.0,
    max_swaps: int = 40,
) -> tuple[np.ndarray, list[dict]]:
    """Coordinate descent on the discrete exact-cardinality subset."""
    gram = mapped @ mapped.T
    subset = np.asarray(sorted(int(index) for index in subset), dtype=int)
    history: list[dict] = []
    current = smooth_subset_score_from_gram(gram, subset, beta)
    for iteration in range(max_swaps):
        selected = set(int(index) for index in subset)
        outside = [index for index in range(len(mapped)) if index not in selected]
        best = current
        move: tuple[int, int] | None = None
        best_subset: np.ndarray | None = None
        for position, old in enumerate(subset):
            for new in outside:
                candidate = subset.copy()
                candidate[position] = new
                candidate.sort()
                score = smooth_subset_score_from_gram(gram, candidate, beta)
                if score < best - 2e-13:
                    best = score
                    move = (int(old), int(new))
                    best_subset = candidate
        if move is None or best_subset is None:
            break
        subset = best_subset
        history.append(
            {
                "iteration": iteration,
                "removed": move[0],
                "added": move[1],
                "smooth_score": best,
                "mapped_maximum": maximum_inner_product(mapped[subset]),
            }
        )
        current = best
    return subset, history


def map_smoothmax_value_gradient(
    flat: np.ndarray, selected_roots: np.ndarray, beta: float
) -> tuple[float, np.ndarray]:
    matrix = flat.reshape(selected_roots.shape[1], 5)
    raw = selected_roots @ matrix
    norms = np.linalg.norm(raw, axis=1)
    if float(np.min(norms)) <= 1e-10:
        return 1e6, np.zeros_like(flat)
    x = raw / norms[:, None]
    ii, jj = pair_indices(len(x))
    values = np.sum(x[ii] * x[jj], axis=1)
    maximum = float(np.max(values))
    exponentials = np.exp(beta * (values - maximum))
    weights = exponentials / float(np.sum(exponentials))
    value = maximum + math.log(float(np.sum(exponentials))) / beta
    ambient = np.zeros_like(x)
    np.add.at(ambient, ii, weights[:, None] * x[jj])
    np.add.at(ambient, jj, weights[:, None] * x[ii])
    tangent = ambient - np.sum(ambient * x, axis=1)[:, None] * x
    raw_gradient = tangent / norms[:, None]
    gradient = selected_roots.T @ raw_gradient
    return float(value), gradient.ravel()


def optimize_metric(
    roots: np.ndarray,
    subset: np.ndarray,
    matrix: np.ndarray,
    betas: tuple[float, ...],
    iterations: int,
) -> tuple[np.ndarray, list[dict]]:
    matrix = normalize_map(matrix)
    history: list[dict] = []
    selected = roots[subset]
    for beta in betas:
        result = minimize(
            map_smoothmax_value_gradient,
            matrix.ravel(),
            args=(selected, beta),
            jac=True,
            method="L-BFGS-B",
            options={
                "maxiter": iterations,
                "ftol": 2e-15,
                "gtol": 2e-10,
                "maxls": 60,
                "maxcor": 30,
            },
        )
        matrix = normalize_map(result.x.reshape(matrix.shape))
        singular = np.linalg.svd(matrix, compute_uv=False)
        image = mapped_points(selected, matrix)
        history.append(
            {
                "beta": beta,
                "iterations": int(result.nit),
                "success": bool(result.success),
                "message": str(result.message),
                "mapped_maximum": maximum_inner_product(image),
                "map_singular_values": singular.tolist(),
                "map_condition_number": float(singular[0] / singular[-1]),
                "minimum_raw_root_norm": float(
                    np.min(np.linalg.norm(selected @ matrix, axis=1))
                ),
            }
        )
    return matrix, history


def structured_run(
    family: str,
    n: int,
    seed: int,
    alternations: int,
    map_iterations: int,
) -> dict:
    roots, labels = root_shell(family)
    rng = np.random.default_rng(seed)
    matrix, initialization = initial_map(roots, family, seed, seed % 4)
    mapped = mapped_points(roots, matrix)
    subset = greedy_delete_subset(mapped, n, rng)
    subset, initial_swaps = local_subset_swaps(mapped, subset)
    history: list[dict] = [
        {
            "stage": "initial_subset",
            "mapped_maximum": maximum_inner_product(mapped[subset]),
            "swaps": initial_swaps,
        }
    ]
    for outer in range(alternations):
        matrix, metric_history = optimize_metric(
            roots,
            subset,
            matrix,
            betas=(20.0, 70.0, 245.0, 857.5),
            iterations=map_iterations,
        )
        mapped = mapped_points(roots, matrix)
        old_subset = subset.copy()
        subset, swap_history = local_subset_swaps(
            mapped, subset, beta=350.0 + 150.0 * outer
        )
        # On later passes, also challenge the current basin with a fresh
        # deletion path under the now optimized metric.
        challenger = greedy_delete_subset(mapped, n, rng, beta=90.0)
        challenger, challenger_swaps = local_subset_swaps(
            mapped, challenger, beta=350.0 + 150.0 * outer
        )
        gram = mapped @ mapped.T
        if smooth_subset_score_from_gram(
            gram, challenger, 500.0
        ) < smooth_subset_score_from_gram(gram, subset, 500.0):
            subset = challenger
            chosen_path = "fresh_greedy_challenger"
        else:
            chosen_path = "incumbent_local_swaps"
        history.append(
            {
                "stage": f"alternation_{outer}",
                "metric_history": metric_history,
                "old_subset": old_subset.tolist(),
                "incumbent_swaps": swap_history,
                "challenger_swaps": challenger_swaps,
                "chosen_path": chosen_path,
                "subset_after": subset.tolist(),
                "mapped_maximum": maximum_inner_product(mapped[subset]),
            }
        )
    matrix, final_metric_history = optimize_metric(
        roots,
        subset,
        matrix,
        betas=(120.0, 480.0, 1920.0, 7680.0),
        iterations=map_iterations * 2,
    )
    coordinates = mapped_points(roots[subset], matrix)
    history.append(
        {
            "stage": "final_metric_polish",
            "metric_history": final_metric_history,
            "mapped_maximum": maximum_inner_product(coordinates),
        }
    )
    return {
        "family": family,
        "n": n,
        "seed": seed,
        "initialization": initialization,
        "root_count": len(roots),
        "selected_root_indices": subset.tolist(),
        "selected_root_labels": [labels[int(index)] for index in subset],
        "map_float64": matrix.tolist(),
        "map_rank_binary64": int(np.linalg.matrix_rank(matrix, tol=1e-11)),
        "map_singular_values": np.linalg.svd(matrix, compute_uv=False).tolist(),
        "structured_history": history,
        "structured_diagnostics": diagnostics(coordinates),
        "structured_coordinates_float64": coordinates.tolist(),
    }


def full_smoothmax_value_gradient(
    flat: np.ndarray, n: int, beta: float
) -> tuple[float, np.ndarray]:
    raw = flat.reshape(n, 5)
    norms = np.linalg.norm(raw, axis=1)
    if float(np.min(norms)) <= 1e-12:
        return 1e6, np.zeros_like(flat)
    x = raw / norms[:, None]
    ii, jj = pair_indices(n)
    values = np.sum(x[ii] * x[jj], axis=1)
    maximum = float(np.max(values))
    exponentials = np.exp(beta * (values - maximum))
    weights = exponentials / float(np.sum(exponentials))
    value = maximum + math.log(float(np.sum(exponentials))) / beta
    ambient = np.zeros_like(x)
    np.add.at(ambient, ii, weights[:, None] * x[jj])
    np.add.at(ambient, jj, weights[:, None] * x[ii])
    tangent = ambient - np.sum(ambient * x, axis=1)[:, None] * x
    return float(value), (tangent / norms[:, None]).ravel()


def unrestricted_refine(
    coordinates: np.ndarray,
    betas: tuple[float, ...] = (100.0, 400.0, 1600.0, 6400.0, 25600.0),
    iterations: int = 1200,
) -> tuple[np.ndarray, list[dict]]:
    x = unit_rows(coordinates)
    history: list[dict] = []
    for beta in betas:
        result = minimize(
            full_smoothmax_value_gradient,
            x.ravel(),
            args=(len(x), beta),
            jac=True,
            method="L-BFGS-B",
            options={
                "maxiter": iterations,
                "ftol": 3e-16,
                "gtol": 2e-10,
                "maxls": 70,
                "maxcor": 35,
            },
        )
        x = unit_rows(result.x.reshape(x.shape))
        history.append(
            {
                "beta": beta,
                "iterations": int(result.nit),
                "success": bool(result.success),
                "message": str(result.message),
                "maximum": maximum_inner_product(x),
            }
        )
    return x, history


def epigraph_slsqp(
    coordinates: np.ndarray, max_iterations: int = 3000
) -> tuple[np.ndarray, dict]:
    x = unit_rows(coordinates)
    n = len(x)
    ii, jj = pair_indices(n)
    initial = np.r_[x.ravel(), maximum_inner_product(x) + 1e-9]

    def objective(variable: np.ndarray) -> tuple[float, np.ndarray]:
        gradient = np.zeros_like(variable)
        gradient[-1] = 1.0
        return float(variable[-1]), gradient

    def equalities(variable: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        points = variable[:-1].reshape(n, 5)
        values = np.sum(points * points, axis=1) - 1.0
        jacobian = np.zeros((n, len(variable)))
        for row in range(n):
            jacobian[row, 5 * row : 5 * row + 5] = 2.0 * points[row]
        return values, jacobian

    def inequalities(variable: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        points = variable[:-1].reshape(n, 5)
        values = variable[-1] - np.sum(points[ii] * points[jj], axis=1)
        jacobian = np.zeros((len(ii), len(variable)))
        rows = np.arange(len(ii))
        for coordinate in range(5):
            jacobian[rows, 5 * ii + coordinate] = -points[jj, coordinate]
            jacobian[rows, 5 * jj + coordinate] = -points[ii, coordinate]
        jacobian[:, -1] = 1.0
        return values, jacobian

    constraints = (
        {
            "type": "eq",
            "fun": lambda variable: equalities(variable)[0],
            "jac": lambda variable: equalities(variable)[1],
        },
        {
            "type": "ineq",
            "fun": lambda variable: inequalities(variable)[0],
            "jac": lambda variable: inequalities(variable)[1],
        },
    )
    result = minimize(
        objective,
        initial,
        jac=True,
        method="SLSQP",
        constraints=constraints,
        options={"maxiter": max_iterations, "ftol": 5e-14, "disp": False},
    )
    polished = unit_rows(result.x[:-1].reshape(n, 5))
    return polished, {
        "iterations": int(result.nit),
        "success": bool(result.success),
        "message": str(result.message),
        "epigraph_value": float(result.fun),
        "recomputed_maximum": maximum_inner_product(polished),
    }


def diagnostics(coordinates: np.ndarray) -> dict:
    x = unit_rows(coordinates)
    n = len(x)
    gram = x @ x.T
    ii, jj = pair_indices(n)
    values = gram[ii, jj]
    maximum = float(np.max(values))
    eigenvalues = np.linalg.eigvalsh(gram)
    answer: dict = {
        "n": n,
        "maximum_inner_product": maximum,
        "gap_above_one_half": maximum - 0.5,
        "minimum_inner_product": float(np.min(values)),
        "unit_norm_residual": float(
            np.max(np.abs(np.sum(x * x, axis=1) - 1.0))
        ),
        "gram_top_five_eigenvalues": eigenvalues[-5:].tolist(),
        "gram_null_spectrum_maximum_absolute": float(
            np.max(np.abs(eigenvalues[:-5]))
        ),
        "coordinate_little_endian_float64_sha256": hashlib.sha256(
            np.asarray(x, dtype="<f8").tobytes()
        ).hexdigest(),
        "top_inner_products": np.sort(values)[-30:][::-1].tolist(),
        "active_graphs": {},
    }
    for tolerance in (1e-6, 1e-8):
        adjacency = gram >= maximum - tolerance
        np.fill_diagonal(adjacency, False)
        degrees = np.sum(adjacency, axis=1).astype(int)
        unique, counts = np.unique(degrees, return_counts=True)
        unseen = set(range(n))
        components: list[int] = []
        while unseen:
            stack = [unseen.pop()]
            size = 0
            while stack:
                vertex = stack.pop()
                size += 1
                neighbours = set(np.flatnonzero(adjacency[vertex])) & unseen
                unseen -= neighbours
                stack.extend(neighbours)
            components.append(size)
        answer["active_graphs"][str(tolerance)] = {
            "edge_count": int(np.sum(adjacency) // 2),
            "degree_histogram": {
                str(int(degree)): int(count)
                for degree, count in zip(unique, counts)
            },
            "component_sizes": sorted(components, reverse=True),
        }
    return answer


def write_checkpoint(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, nargs="+", default=[41, 42, 43, 44])
    parser.add_argument("--families", nargs="+", default=["E6", "D6"])
    parser.add_argument("--seeds", type=int, nargs="+", required=True)
    parser.add_argument("--alternations", type=int, default=3)
    parser.add_argument("--map-iterations", type=int, default=350)
    parser.add_argument("--polish-top", type=int, default=2)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload: dict = {
        "evidence_status": STATUS,
        "method": (
            "alternating exact-cardinality finite-root-shell selection and "
            "general rank-five PSD metric optimization, followed by "
            "unrestricted product-of-spheres refinement"
        ),
        "environment": {
            "python": sys.version,
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
        },
        "parameters": {
            "n": args.n,
            "families": args.families,
            "seeds": args.seeds,
            "alternations": args.alternations,
            "map_iterations": args.map_iterations,
            "polish_top": args.polish_top,
        },
        "structured_runs": [],
        "polished_runs": [],
        "best_by_n": {},
        "elapsed_seconds": 0.0,
    }
    start = time.time()
    for n in args.n:
        for family in args.families:
            for seed in args.seeds:
                print(
                    json.dumps(
                        {
                            "event": "structured_start",
                            "family": family,
                            "n": n,
                            "seed": seed,
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
                run = structured_run(
                    family,
                    n,
                    seed,
                    args.alternations,
                    args.map_iterations,
                )
                payload["structured_runs"].append(run)
                payload["elapsed_seconds"] = time.time() - start
                write_checkpoint(args.output, payload)
                print(
                    json.dumps(
                        {
                            "event": "structured_done",
                            "family": family,
                            "n": n,
                            "seed": seed,
                            "maximum": run["structured_diagnostics"][
                                "maximum_inner_product"
                            ],
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
    for n in args.n:
        candidates = [
            run for run in payload["structured_runs"] if run["n"] == n
        ]
        candidates.sort(
            key=lambda run: run["structured_diagnostics"][
                "maximum_inner_product"
            ]
        )
        for rank, source in enumerate(candidates[: args.polish_top]):
            x = np.asarray(source["structured_coordinates_float64"])
            # Every release gets an independent deterministic tangent kick.
            rng = np.random.default_rng(
                int(source["seed"]) + 104729 * (rank + 1) + 1009 * n
            )
            if rank:
                x = unit_rows(x + 0.0025 * rng.normal(size=x.shape))
            refined, smooth_history = unrestricted_refine(x)
            sqp_coordinates, sqp = epigraph_slsqp(refined)
            if maximum_inner_product(sqp_coordinates) <= maximum_inner_product(
                refined
            ) + 2e-10:
                final = sqp_coordinates
                chosen = "epigraph_slsqp"
            else:
                final = refined
                chosen = "smooth_continuation"
            polished = {
                "n": n,
                "source_family": source["family"],
                "source_seed": source["seed"],
                "source_rank": rank,
                "smooth_history": smooth_history,
                "epigraph_slsqp": sqp,
                "chosen_endpoint": chosen,
                "final_diagnostics": diagnostics(final),
                "coordinates_float64": final.tolist(),
            }
            payload["polished_runs"].append(polished)
            best = payload["best_by_n"].get(str(n))
            if (
                best is None
                or polished["final_diagnostics"]["maximum_inner_product"]
                < best["maximum_inner_product"]
            ):
                payload["best_by_n"][str(n)] = {
                    "maximum_inner_product": polished["final_diagnostics"][
                        "maximum_inner_product"
                    ],
                    "gap_above_one_half": polished["final_diagnostics"][
                        "gap_above_one_half"
                    ],
                    "source_family": source["family"],
                    "source_seed": source["seed"],
                    "polished_run_index": len(payload["polished_runs"]) - 1,
                    "coordinate_little_endian_float64_sha256": polished[
                        "final_diagnostics"
                    ]["coordinate_little_endian_float64_sha256"],
                }
            payload["elapsed_seconds"] = time.time() - start
            write_checkpoint(args.output, payload)
            print(
                json.dumps(
                    {
                        "event": "polish_done",
                        "n": n,
                        "source_family": source["family"],
                        "source_seed": source["seed"],
                        "maximum": polished["final_diagnostics"][
                            "maximum_inner_product"
                        ],
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
    payload["elapsed_seconds"] = time.time() - start
    payload["completed"] = True
    write_checkpoint(args.output, payload)


if __name__ == "__main__":
    main()
