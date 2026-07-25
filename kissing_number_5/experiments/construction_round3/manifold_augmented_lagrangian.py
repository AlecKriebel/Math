#!/usr/bin/env python3
"""Riemannian augmented-Lagrangian search for 5D spherical codes.

This is discovery code, not a proof or a construction certificate.  All
arithmetic is binary64.  The optimized problem is

    minimize mu
    subject to <x_i,x_j> - mu <= 0,   x_i in S^4.

For fixed inequality multipliers and penalty rho, ``mu`` is eliminated
exactly from the Powell--Hestenes--Rockafellar augmented Lagrangian.  The
remaining problem lives on the product manifold (S^4)^N and is minimized by
a retraction-based Riemannian nonlinear conjugate-gradient method.  This is
intentionally independent of the Euclidean L-BFGS-B and SLSQP pipelines in
construction rounds 1 and 2.

Several deterministic initialization families are supported:

* unrestricted asymmetric Gaussian clouds;
* the best public 41-point numerical benchmark, with tangent perturbations
  and sequential hole insertion for N > 41;
* greedy deletion after random rank-five projections of D6, E6, E7, or E8
  root systems;
* coordinate projection of E6, which contains the D5 40-point code.

Every result is labelled numerical evidence only and includes coordinates,
active edge lists, Gram spectra, and deterministic seeds.
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
from typing import Callable

import numpy as np


EVIDENCE_STATUS = "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE"
DIMENSION = 5


def unit_rows(x: np.ndarray) -> np.ndarray:
    """Normalize every row, rejecting a numerically zero row."""
    norms = np.linalg.norm(x, axis=1)
    if np.min(norms) <= 1e-14:
        raise ValueError("cannot normalize a zero row")
    return x / norms[:, None]


def tangent_projection(x: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Orthogonally project an ambient vector onto T_x (S^4)^N."""
    return z - np.sum(x * z, axis=1)[:, None] * x


def retract(x: np.ndarray, eta: np.ndarray, step: float = 1.0) -> np.ndarray:
    """Row-normalization retraction on the product of spheres."""
    return unit_rows(x + step * eta)


def pair_indices(n: int) -> tuple[np.ndarray, np.ndarray]:
    return np.triu_indices(n, 1)


def pair_inner_products(x: np.ndarray) -> np.ndarray:
    ii, jj = pair_indices(len(x))
    return np.sum(x[ii] * x[jj], axis=1)


def edge_gradient(
    x: np.ndarray, ii: np.ndarray, jj: np.ndarray, weights: np.ndarray
) -> np.ndarray:
    """Ambient gradient of sum_e weights[e] <x_i,x_j>."""
    weighted_adjacency = np.zeros((len(x), len(x)), dtype=float)
    weighted_adjacency[ii, jj] = weights
    weighted_adjacency[jj, ii] = weights
    return weighted_adjacency @ x


def project_to_scaled_simplex(a: np.ndarray, total: float) -> tuple[np.ndarray, float]:
    """Return max(a-theta,0) with prescribed sum ``total``.

    This standard sorting formula is used to eliminate the epigraph variable
    from the augmented Lagrangian.  ``theta`` is the resulting epigraph value.
    """
    if total <= 0:
        raise ValueError("simplex mass must be positive")
    order = np.sort(np.asarray(a, dtype=float))[::-1]
    cumulative = np.cumsum(order)
    count = np.arange(1, len(order) + 1, dtype=float)
    eligible = order - (cumulative - total) / count > 0
    if not np.any(eligible):
        raise ArithmeticError("simplex projection did not find an active index")
    last = int(np.flatnonzero(eligible)[-1])
    theta = float((cumulative[last] - total) / (last + 1))
    projected = np.maximum(a - theta, 0.0)
    # One correction avoids a few ulps of drift in multiplier mass.  It does
    # not affect the active set except in a binary64 boundary case.
    residual = total - float(np.sum(projected))
    active = projected > 0
    if np.any(active):
        projected[active] += residual / int(np.sum(active))
    return projected, theta


def augmented_value_gradient(
    x: np.ndarray, multipliers: np.ndarray, rho: float
) -> tuple[float, np.ndarray, float, np.ndarray]:
    """Reduced inequality augmented Lagrangian and Riemannian gradient.

    The unreduced expression is

      mu + (1/(2 rho)) sum_e[
          max(0, lambda_e + rho(s_e-mu))^2 - lambda_e^2].

    Its minimizing ``mu`` is characterized by sum_e w_e = 1.  Writing
    a_e=s_e+lambda_e/rho, simplex projection gives
    w_e=rho max(0,a_e-mu).
    """
    if rho <= 0:
        raise ValueError("rho must be positive")
    n = len(x)
    ii, jj = pair_indices(n)
    s = np.sum(x[ii] * x[jj], axis=1)
    if multipliers.shape != s.shape:
        raise ValueError("wrong multiplier shape")
    projected, mu = project_to_scaled_simplex(
        s + multipliers / rho, total=1.0 / rho
    )
    weights = rho * projected
    value = mu + (
        float(np.dot(weights, weights)) - float(np.dot(multipliers, multipliers))
    ) / (2.0 * rho)
    ambient = edge_gradient(x, ii, jj, weights)
    gradient = tangent_projection(x, ambient)
    return float(value), gradient, float(mu), weights


def riesz_value_gradient(x: np.ndarray, power: float) -> tuple[float, np.ndarray]:
    """Logarithmically scaled high-power inverse-chordal energy."""
    if power <= 0:
        raise ValueError("power must be positive")
    n = len(x)
    ii, jj = pair_indices(n)
    s = np.sum(x[ii] * x[jj], axis=1)
    one_minus = np.maximum(1.0 - s, 1e-15)
    logs = -power * np.log(one_minus)
    shift = float(np.max(logs))
    raw = np.exp(logs - shift)
    weights = raw / float(np.sum(raw))
    value = (shift + math.log(float(np.sum(raw)))) / power
    ambient = edge_gradient(x, ii, jj, weights / one_minus)
    return float(value), tangent_projection(x, ambient)


def riemannian_ncg(
    x0: np.ndarray,
    objective_gradient: Callable[[np.ndarray], tuple[float, np.ndarray]],
    max_iterations: int,
    gradient_tolerance: float,
    initial_step: float = 1.0,
) -> tuple[np.ndarray, dict]:
    """Polak--Ribiere+ nonlinear CG with Armijo retraction line search."""
    x = unit_rows(np.asarray(x0, dtype=float))
    value, gradient = objective_gradient(x)
    direction = -gradient
    step_hint = float(initial_step)
    evaluations = 1
    resets = 0
    accepted_steps: list[float] = []
    converged = False

    for iteration in range(max_iterations):
        norm = float(np.linalg.norm(gradient))
        if norm <= gradient_tolerance:
            converged = True
            break
        slope = float(np.sum(gradient * direction))
        if not np.isfinite(slope) or slope >= -1e-12 * norm * norm:
            direction = -gradient
            slope = -norm * norm
            resets += 1

        step = min(max(step_hint, 1e-12), 4.0)
        accepted = False
        for _ in range(50):
            candidate = retract(x, direction, step)
            new_value, new_gradient = objective_gradient(candidate)
            evaluations += 1
            if np.isfinite(new_value) and new_value <= value + 1e-4 * step * slope:
                accepted = True
                break
            step *= 0.5
        if not accepted:
            direction = -gradient
            step = min(1e-3, 1.0 / max(norm, 1e-12))
            candidate = retract(x, direction, step)
            new_value, new_gradient = objective_gradient(candidate)
            evaluations += 1
            if not np.isfinite(new_value) or new_value >= value:
                break

        # Projection transport is compatible with the normalization
        # retraction and is sufficient for this discovery computation.
        transported_gradient = tangent_projection(candidate, gradient)
        transported_direction = tangent_projection(candidate, direction)
        denominator = max(float(np.sum(gradient * gradient)), 1e-300)
        beta = float(
            np.sum(new_gradient * (new_gradient - transported_gradient))
        ) / denominator
        beta = min(max(beta, 0.0), 10.0)
        new_direction = -new_gradient + beta * transported_direction
        if float(np.sum(new_gradient * new_direction)) >= (
            -1e-4 * float(np.sum(new_gradient * new_gradient))
        ):
            new_direction = -new_gradient
            resets += 1

        x = candidate
        value = float(new_value)
        gradient = new_gradient
        direction = new_direction
        accepted_steps.append(float(step))
        # A modest increase is less erratic than resetting to one after every
        # accepted line-search step.
        step_hint = min(1.8 * step, 2.0)
    else:
        iteration = max_iterations

    return x, {
        "iterations": int(iteration),
        "evaluations": int(evaluations),
        "final_value": float(value),
        "gradient_norm": float(np.linalg.norm(gradient)),
        "converged": bool(converged),
        "direction_resets": int(resets),
        "accepted_step_min": (
            float(min(accepted_steps)) if accepted_steps else None
        ),
        "accepted_step_max": (
            float(max(accepted_steps)) if accepted_steps else None
        ),
    }


def manifold_search(
    x0: np.ndarray,
    powers: tuple[float, ...],
    penalties: tuple[float, ...],
    inner_iterations: int,
    gradient_tolerance: float,
) -> tuple[np.ndarray, list[dict]]:
    """High-power warmup followed by epigraph augmented-Lagrangian stages."""
    x = unit_rows(x0)
    history: list[dict] = []
    for power in powers:
        x, inner = riemannian_ncg(
            x,
            lambda y, p=power: riesz_value_gradient(y, p),
            max_iterations=inner_iterations,
            gradient_tolerance=gradient_tolerance,
            initial_step=0.5,
        )
        history.append(
            {
                "stage": "riemannian_high_power",
                "power": float(power),
                "max_inner_product": float(np.max(pair_inner_products(x))),
                **inner,
            }
        )

    number_pairs = len(x) * (len(x) - 1) // 2
    multipliers = np.full(number_pairs, 1.0 / number_pairs)
    for outer, rho in enumerate(penalties):
        def objective(y: np.ndarray, lam=multipliers.copy(), r=rho):
            value, gradient, _, _ = augmented_value_gradient(y, lam, r)
            return value, gradient

        x, inner = riemannian_ncg(
            x,
            objective,
            max_iterations=inner_iterations,
            gradient_tolerance=gradient_tolerance,
            initial_step=min(1.0, 4.0 / math.sqrt(rho)),
        )
        value, gradient, mu, weights = augmented_value_gradient(
            x, multipliers, rho
        )
        multipliers = weights
        pair_values = pair_inner_products(x)
        history.append(
            {
                "stage": "riemannian_augmented_lagrangian",
                "outer_iteration": int(outer),
                "rho": float(rho),
                "reduced_value": float(value),
                "eliminated_epigraph_mu": float(mu),
                "max_inner_product": float(np.max(pair_values)),
                "positive_multipliers": int(np.sum(weights > 0)),
                "multiplier_mass": float(np.sum(weights)),
                "riemannian_gradient_norm": float(np.linalg.norm(gradient)),
                **inner,
            }
        )
    return unit_rows(x), history


def d_roots(dimension: int) -> np.ndarray:
    roots = []
    for i in range(dimension):
        for j in range(i + 1, dimension):
            for sign_i in (-1.0, 1.0):
                for sign_j in (-1.0, 1.0):
                    row = np.zeros(dimension)
                    row[i] = sign_i / math.sqrt(2.0)
                    row[j] = sign_j / math.sqrt(2.0)
                    roots.append(row)
    return np.asarray(roots)


def e6_roots() -> np.ndarray:
    roots = [np.r_[row, 0.0] for row in d_roots(5)]
    for mask in range(1 << 5):
        signs = np.asarray(
            [1.0 if (mask >> coordinate) & 1 else -1.0 for coordinate in range(5)]
        )
        last = float(np.prod(signs))
        roots.append(
            np.r_[signs / 2.0, last * math.sqrt(3.0) / 2.0]
            / math.sqrt(2.0)
        )
    answer = np.asarray(roots)
    if answer.shape != (72, 6):
        raise AssertionError("bad E6 root count")
    return answer


def e8_roots() -> np.ndarray:
    roots = []
    for i in range(8):
        for j in range(i + 1, 8):
            for sign_i in (-1.0, 1.0):
                for sign_j in (-1.0, 1.0):
                    row = np.zeros(8)
                    row[i] = sign_i / math.sqrt(2.0)
                    row[j] = sign_j / math.sqrt(2.0)
                    roots.append(row)
    for mask in range(1 << 8):
        signs = np.asarray(
            [1.0 if (mask >> coordinate) & 1 else -1.0 for coordinate in range(8)]
        )
        if np.prod(signs) > 0:
            roots.append(signs / math.sqrt(8.0))
    answer = np.asarray(roots)
    if answer.shape != (240, 8):
        raise AssertionError("bad E8 root count")
    return answer


def e7_roots() -> np.ndarray:
    roots = e8_roots()
    roots = roots[np.abs(roots[:, 0] + roots[:, 1]) < 1e-13]
    normal = np.asarray([1.0, 1.0, 0, 0, 0, 0, 0, 0]) / math.sqrt(2.0)
    _, _, right = np.linalg.svd(normal.reshape(1, 8))
    answer = roots @ right[1:].T
    if answer.shape != (126, 7):
        raise AssertionError("bad E7 root count")
    return answer


def greedy_delete_to_size(x0: np.ndarray, size: int) -> np.ndarray:
    """Delete locally crowded points until ``size`` remain.

    The score combines the largest eight inner products incident to a point.
    Ties are resolved by the current row order, so the routine is fully
    deterministic once the projection seed is fixed.
    """
    x = unit_rows(x0)
    if size > len(x):
        raise ValueError("cannot delete to a larger size")
    while len(x) > size:
        gram = x @ x.T
        np.fill_diagonal(gram, -np.inf)
        width = min(8, len(x) - 1)
        top = np.partition(gram, len(x) - width - 1, axis=1)[:, -width:]
        local_max = np.max(top, axis=1)
        # Lexicographic-scale score: worst incident pair dominates, and the
        # exponential tail distinguishes ties/crowded vertices.
        centered = np.clip(50.0 * (top - local_max[:, None]), -700.0, 0.0)
        crowd = local_max + 1e-3 * np.sum(np.exp(centered), axis=1)
        x = np.delete(x, int(np.argmax(crowd)), axis=0)
    return unit_rows(x)


def root_projection_initial(n: int, seed: int, family: str) -> np.ndarray:
    roots = {
        "d6proj": d_roots(6),
        "e6proj": e6_roots(),
        "e7proj": e7_roots(),
        "e8proj": e8_roots(),
    }[family]
    rng = np.random.default_rng(seed)
    gaussian = rng.normal(size=(roots.shape[1], DIMENSION))
    q, _ = np.linalg.qr(gaussian)
    projected = unit_rows(roots @ q[:, :DIMENSION])
    answer = greedy_delete_to_size(projected, n)
    # Break any accidental stabilizer while preserving determinism.
    noise = rng.normal(size=answer.shape)
    noise = tangent_projection(answer, noise)
    return retract(answer, noise, 2e-3)


def e6_coordinate_initial(n: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    projected = e6_roots()[:, :5]
    nonzero = np.linalg.norm(projected, axis=1) > 1e-12
    x = greedy_delete_to_size(unit_rows(projected[nonzero]), n)
    noise = tangent_projection(x, rng.normal(size=x.shape))
    return retract(x, noise, 1e-3)


def load_coordinate_file(path: Path) -> np.ndarray:
    rows = []
    for raw in path.read_text().splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        rows.append([float(value) for value in stripped.replace(",", " ").split()])
    x = np.asarray(rows, dtype=float)
    if x.ndim != 2 or x.shape[1] != DIMENSION:
        raise ValueError(f"{path} does not contain five coordinates per row")
    return unit_rows(x)


def insert_in_largest_sampled_hole(
    x0: np.ndarray, target_size: int, rng: np.random.Generator, samples: int
) -> np.ndarray:
    x = unit_rows(x0)
    while len(x) < target_size:
        candidates = unit_rows(rng.normal(size=(samples, DIMENSION)))
        crowding = np.max(candidates @ x.T, axis=1)
        x = np.vstack((x, candidates[int(np.argmin(crowding))]))
    return unit_rows(x)


def round2_best_initial(
    n: int,
    seed: int,
    root_result_path: Path,
    layer_result_path: Path,
) -> np.ndarray:
    """Load the best recorded round-2 candidate of the requested size."""
    if n == 41:
        candidates = json.loads(root_result_path.read_text())["runs"]
    else:
        candidates = [
            run
            for run in json.loads(layer_result_path.read_text())["layer_runs"]
            if int(run["n"]) == n
        ]
    if not candidates:
        raise ValueError(f"round 2 has no stored N={n} candidate")
    best = min(
        candidates,
        key=lambda run: float(run["diagnostics"]["maxip"]),
    )
    x = unit_rows(np.asarray(best["coordinates"], dtype=float))
    rng = np.random.default_rng(seed)
    if seed != 0:
        noise = tangent_projection(x, rng.normal(size=x.shape))
        x = retract(x, noise, (1e-5, 1e-4, 1e-3)[seed % 3])
    return x


def make_initial(
    n: int,
    seed: int,
    kind: str,
    warm41_path: Path,
    hole_samples: int,
    round2_root_path: Path | None = None,
    round2_layer_path: Path | None = None,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    if kind == "random":
        return unit_rows(rng.normal(size=(n, DIMENSION)))
    if kind == "warm41":
        base = load_coordinate_file(warm41_path)
        if len(base) != 41:
            raise ValueError("warm-start coordinate file must have 41 rows")
        x = insert_in_largest_sampled_hole(base, n, rng, hole_samples)
        # Seed zero is an exact replay of the published binary64 start for
        # N=41; all other warm starts break symmetry in tangent directions.
        if seed != 0 or n > 41:
            noise = tangent_projection(x, rng.normal(size=x.shape))
            scale = (1e-4, 1e-3, 5e-3)[seed % 3]
            x = retract(x, noise, scale)
        return x
    if kind in {"d6proj", "e6proj", "e7proj", "e8proj"}:
        return root_projection_initial(n, seed, kind)
    if kind == "e6coordinate":
        return e6_coordinate_initial(n, seed)
    if kind == "round2best":
        if round2_root_path is None:
            round2_root_path = (
                Path(__file__).parents[1]
                / "construction_round2"
                / "results"
                / "root_map_E6_N41_seed22.json"
            )
        if round2_layer_path is None:
            round2_layer_path = (
                Path(__file__).parents[1]
                / "construction_round2"
                / "results"
                / "layers_seed2026072311.json"
            )
        return round2_best_initial(
            n, seed, round2_root_path, round2_layer_path
        )
    raise ValueError(f"unknown initialization kind {kind!r}")


def connected_components(adjacency: np.ndarray) -> list[list[int]]:
    unseen = set(range(len(adjacency)))
    components = []
    while unseen:
        seed = int(min(unseen))
        unseen.remove(seed)
        stack = [seed]
        component = []
        while stack:
            vertex = int(stack.pop())
            component.append(vertex)
            neighbors = {
                int(v) for v in np.flatnonzero(adjacency[vertex]).tolist()
            } & unseen
            unseen -= neighbors
            stack.extend(sorted(neighbors, reverse=True))
        components.append(sorted(component))
    return sorted(components, key=lambda c: (-len(c), c))


def diagnostics(x0: np.ndarray) -> dict:
    x = unit_rows(x0)
    n = len(x)
    gram = x @ x.T
    ii, jj = pair_indices(n)
    off_diagonal = gram[ii, jj]
    maximum = float(np.max(off_diagonal))
    eigenvalues = np.linalg.eigvalsh(gram)
    active_graphs = {}
    for tolerance in (1e-4, 1e-6, 1e-8):
        mask = off_diagonal >= maximum - tolerance
        edges = [
            [int(i), int(j)]
            for i, j in zip(ii[mask].tolist(), jj[mask].tolist())
        ]
        adjacency = np.zeros((n, n), dtype=bool)
        adjacency[ii[mask], jj[mask]] = True
        adjacency[jj[mask], ii[mask]] = True
        degrees = np.sum(adjacency, axis=1).astype(int)
        values, counts = np.unique(degrees, return_counts=True)
        edge_bytes = json.dumps(edges, separators=(",", ":")).encode("ascii")
        active_graphs[f"{tolerance:.0e}"] = {
            "edge_count": int(len(edges)),
            "edges_zero_based": edges,
            "edge_list_sha256": hashlib.sha256(edge_bytes).hexdigest(),
            "degree_sequence": degrees.tolist(),
            "degree_histogram": {
                str(int(value)): int(count)
                for value, count in zip(values, counts)
            },
            "components_zero_based": connected_components(adjacency),
        }
    deep_mask = off_diagonal < -0.5
    violations = off_diagonal > 0.5
    return {
        "n": int(n),
        "max_inner_product": maximum,
        "gap_above_one_half": maximum - 0.5,
        "number_pairs_above_one_half": int(np.sum(violations)),
        "largest_violation_above_one_half": float(
            max(0.0, maximum - 0.5)
        ),
        "number_pairs_strictly_below_minus_one_half": int(np.sum(deep_mask)),
        "minimum_inner_product": float(np.min(off_diagonal)),
        "maximum_squared_norm_error": float(
            np.max(np.abs(np.sum(x * x, axis=1) - 1.0))
        ),
        "gram_eigenvalues_ascending": eigenvalues.tolist(),
        "gram_five_positive_eigenvalues": eigenvalues[-5:].tolist(),
        "gram_null_spectrum_max_abs": float(np.max(np.abs(eigenvalues[:-5]))),
        "coordinate_little_endian_float64_sha256": hashlib.sha256(
            np.asarray(x, dtype="<f8").tobytes()
        ).hexdigest(),
        "top_inner_products": np.sort(off_diagonal)[-30:][::-1].tolist(),
        "active_graphs": active_graphs,
    }


def parse_float_tuple(values: list[str]) -> tuple[float, ...]:
    return tuple(float(value) for value in values)


def write_checkpoint(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, nargs="+", default=[41, 42, 43, 44])
    parser.add_argument("--seeds", type=int, nargs="+", required=True)
    parser.add_argument(
        "--kinds",
        nargs="+",
        default=["random", "warm41", "d6proj", "e6proj", "e7proj"],
        choices=[
            "random",
            "warm41",
            "d6proj",
            "e6proj",
            "e7proj",
            "e8proj",
            "e6coordinate",
            "round2best",
        ],
    )
    parser.add_argument(
        "--warm41",
        type=Path,
        default=Path(__file__).parents[1] / "input" / "spherical_codes_5_41.txt",
    )
    parser.add_argument(
        "--round2-root",
        type=Path,
        default=(
            Path(__file__).parents[1]
            / "construction_round2"
            / "results"
            / "root_map_E6_N41_seed22.json"
        ),
    )
    parser.add_argument(
        "--round2-layers",
        type=Path,
        default=(
            Path(__file__).parents[1]
            / "construction_round2"
            / "results"
            / "layers_seed2026072311.json"
        ),
    )
    parser.add_argument("--hole-samples", type=int, default=20000)
    parser.add_argument("--powers", nargs="*", default=["2", "4", "8", "16"])
    parser.add_argument(
        "--penalties",
        nargs="*",
        default=[
            "1",
            "3",
            "10",
            "30",
            "100",
            "300",
            "1000",
            "3000",
            "10000",
            "30000",
            "100000",
            "300000",
        ],
    )
    parser.add_argument("--inner-iterations", type=int, default=1000)
    parser.add_argument("--gradient-tolerance", type=float, default=1e-10)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    powers = parse_float_tuple(args.powers)
    penalties = parse_float_tuple(args.penalties)
    print(
        json.dumps(
            {
                "event": "portfolio_start",
                "n": args.n,
                "seeds": args.seeds,
                "kinds": args.kinds,
            },
            sort_keys=True,
        ),
        flush=True,
    )
    payload: dict = {
        "evidence_status": EVIDENCE_STATUS,
        "method": (
            "Riemannian high-power continuation followed by an inequality "
            "augmented Lagrangian with exact epigraph elimination"
        ),
        "environment": {
            "python": sys.version,
            "numpy": np.__version__,
            "platform": platform.platform(),
        },
        "parameters": {
            "n": args.n,
            "seeds": args.seeds,
            "kinds": args.kinds,
            "warm41": str(args.warm41),
            "warm41_sha256": hashlib.sha256(args.warm41.read_bytes()).hexdigest(),
            "round2_root": str(args.round2_root),
            "round2_root_sha256": hashlib.sha256(
                args.round2_root.read_bytes()
            ).hexdigest(),
            "round2_layers": str(args.round2_layers),
            "round2_layers_sha256": hashlib.sha256(
                args.round2_layers.read_bytes()
            ).hexdigest(),
            "hole_samples": args.hole_samples,
            "powers": powers,
            "penalties": penalties,
            "inner_iterations": args.inner_iterations,
            "gradient_tolerance": args.gradient_tolerance,
        },
        "runs": [],
        "best_by_n": {},
        "elapsed_seconds": 0.0,
    }
    start_time = time.time()
    for n in args.n:
        if n < 2:
            raise ValueError("N must be at least two")
        for kind in args.kinds:
            for seed in args.seeds:
                print(
                    json.dumps(
                        {
                            "event": "run_start",
                            "n": n,
                            "kind": kind,
                            "seed": seed,
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
                initial = make_initial(
                    n,
                    seed,
                    kind,
                    args.warm41,
                    args.hole_samples,
                    args.round2_root,
                    args.round2_layers,
                )
                initial_diagnostics = diagnostics(initial)
                optimized, history = manifold_search(
                    initial,
                    powers=powers,
                    penalties=penalties,
                    inner_iterations=args.inner_iterations,
                    gradient_tolerance=args.gradient_tolerance,
                )
                final_diagnostics = diagnostics(optimized)
                run = {
                    "n": int(n),
                    "kind": kind,
                    "seed": int(seed),
                    "initial_max_inner_product": initial_diagnostics[
                        "max_inner_product"
                    ],
                    "final_diagnostics": final_diagnostics,
                    "history": history,
                    "coordinates_float64": optimized.tolist(),
                }
                payload["runs"].append(run)
                best = payload["best_by_n"].get(str(n))
                if (
                    best is None
                    or final_diagnostics["max_inner_product"]
                    < best["max_inner_product"]
                ):
                    payload["best_by_n"][str(n)] = {
                        "max_inner_product": final_diagnostics[
                            "max_inner_product"
                        ],
                        "kind": kind,
                        "seed": int(seed),
                        "run_index": len(payload["runs"]) - 1,
                    }
                payload["elapsed_seconds"] = time.time() - start_time
                write_checkpoint(args.output, payload)
                print(
                    json.dumps(
                        {
                            "n": n,
                            "kind": kind,
                            "seed": seed,
                            "initial": initial_diagnostics["max_inner_product"],
                            "final": final_diagnostics["max_inner_product"],
                            "active_1e-8": final_diagnostics["active_graphs"][
                                "1e-08"
                            ]["edge_count"],
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
    print(json.dumps(payload["best_by_n"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
