#!/usr/bin/env python3
"""Continuous cardinality homotopy by splitting exact 40-point codes.

NUMERICAL DISCOVERY ONLY.  This program does not prove feasibility or
nonexistence.

The macro move replaces selected points of an exact 40-point code by close
pairs, then continuously increases the prescribed pair separation.  At
successive stages it releases the split points, their contact-graph
neighborhoods, and finally the entire configuration.  Only after this
cardinality homotopy is complete are the pair-separation constraints removed.

No smooth approximation to the maximum inner product is used.  Local
settling solves the literal epigraph problem with all pair inequalities.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
from fractions import Fraction
import hashlib
import itertools
import json
import math
import platform
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import minimize


DIMENSION = 5
STATUS = "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE"
DEFAULT_THETAS = (0.06, 0.16, 0.30, 0.48, 0.68, 0.86, 1.02, 1.14)
DEFAULT_RADII = (0, 0, 1, 1, 2, 2, 3, None)


def unit_rows(array: np.ndarray) -> np.ndarray:
    x = np.asarray(array, dtype=np.float64)
    if x.ndim != 2 or x.shape[1] != DIMENSION:
        raise ValueError("coordinates must be an N by 5 matrix")
    norms = np.linalg.norm(x, axis=1)
    if float(np.min(norms)) <= 1e-14:
        raise ValueError("cannot normalize a zero row")
    return np.ascontiguousarray(x / norms[:, None])


def pair_indices(n: int) -> tuple[np.ndarray, np.ndarray]:
    return np.triu_indices(n, 1)


def pair_values(x: np.ndarray) -> np.ndarray:
    x = unit_rows(x)
    first, second = pair_indices(len(x))
    return np.sum(x[first] * x[second], axis=1)


def maximum(x: np.ndarray) -> float:
    return float(np.max(pair_values(x)))


def fraction_text(value: Fraction) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def exact_known_codes() -> dict[str, tuple[tuple[Fraction, ...], ...]]:
    """Reconstruct D5, L5, Q5, R5 from rational-over-sqrt(2) rows."""
    d5 = []
    for first, second in itertools.combinations(range(DIMENSION), 2):
        for first_sign in (-1, 1):
            for second_sign in (-1, 1):
                row = [Fraction(0)] * DIMENSION
                row[first] = Fraction(first_sign)
                row[second] = Fraction(second_sign)
                d5.append(tuple(row))

    l5 = [row for row in d5 if row[4] != 1]
    for signs in itertools.product((-1, 1), repeat=4):
        if sum(sign < 0 for sign in signs) % 2 == 1:
            l5.append(
                tuple(Fraction(sign, 2) for sign in signs)
                + (Fraction(1),)
            )

    q5 = [row for row in d5 if sum(row) != 2]
    q5.extend(
        tuple(value + Fraction(4, 5) for value in row)
        for row in d5
        if sum(row) == -2
    )

    r5 = [row for row in l5 if sum(row) != 2]
    r5.extend(
        tuple(value + Fraction(4, 5) for value in row)
        for row in l5
        if sum(row) == -2
    )
    answer = {
        "D5": tuple(d5),
        "L5": tuple(l5),
        "Q5": tuple(q5),
        "R5": tuple(r5),
    }
    for name, code in answer.items():
        if len(code) != 40 or len(set(code)) != 40:
            raise AssertionError(f"{name} did not reconstruct 40 unique rows")
        for row in code:
            if sum(value * value for value in row) != 2:
                raise AssertionError(f"{name} row does not have norm sqrt(2)")
        for i, j in itertools.combinations(range(40), 2):
            if sum(code[i][k] * code[j][k] for k in range(5)) > 1:
                raise AssertionError(f"{name} violates the exact half cap")
    return answer


def floating_code(
    code: tuple[tuple[Fraction, ...], ...]
) -> np.ndarray:
    rows = np.asarray(
        [[float(value) / math.sqrt(2.0) for value in row] for row in code],
        dtype=np.float64,
    )
    return unit_rows(rows)


def exact_pair_histogram(
    code: tuple[tuple[Fraction, ...], ...]
) -> dict[str, int]:
    histogram = Counter(
        sum(code[i][k] * code[j][k] for k in range(5))
        for i, j in itertools.combinations(range(40), 2)
    )
    return {
        fraction_text(value): int(count)
        for value, count in sorted(histogram.items())
    }


def coordinate_hash(x: np.ndarray) -> str:
    data = np.ascontiguousarray(unit_rows(x), dtype="<f8")
    return hashlib.sha256(data.tobytes()).hexdigest()


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


def contact_summary(x: np.ndarray, tolerance: float) -> dict:
    values = pair_values(x)
    first, second = pair_indices(len(x))
    top = float(np.max(values))
    chosen = values >= top - tolerance
    edges = np.column_stack([first[chosen], second[chosen]]).astype(int).tolist()
    degree = np.zeros(len(x), dtype=int)
    for i, j in edges:
        degree[i] += 1
        degree[j] += 1
    unique, counts = np.unique(degree, return_counts=True)
    return {
        "tolerance": float(tolerance),
        "edge_count": len(edges),
        "degree_histogram": {
            str(int(value)): int(count)
            for value, count in zip(unique, counts)
        },
        "component_sizes": connected_components(len(x), edges),
        "edges": edges,
        "edge_sha256": hashlib.sha256(
            json.dumps(edges, separators=(",", ":")).encode()
        ).hexdigest(),
    }


def diagnostics(x: np.ndarray) -> dict:
    x = unit_rows(x)
    values = pair_values(x)
    first, second = pair_indices(len(x))
    top = float(np.max(values))
    maximizing = np.flatnonzero(values == top)
    gram_spectrum = np.linalg.eigvalsh(x @ x.T)
    frame_spectrum = np.linalg.eigvalsh(x.T @ x)
    return {
        "n": len(x),
        "dimension": DIMENSION,
        "coordinates_float64": x.tolist(),
        "coordinate_little_endian_float64_sha256": coordinate_hash(x),
        "maximum_inner_product_binary64": top,
        "maximum_inner_product_float_hex": top.hex(),
        "literal_binary64_maximizing_pairs": [
            [int(first[index]), int(second[index])] for index in maximizing
        ],
        "gap_above_one_half": top - 0.5,
        "meets_threshold_binary64": bool(top <= 0.5),
        "minimum_inner_product_binary64": float(np.min(values)),
        "pairs_above_one_half": int(np.sum(values > 0.5)),
        "row_norm_max_error": float(
            np.max(np.abs(np.sum(x * x, axis=1) - 1.0))
        ),
        "positive_gram_eigenvalues": [float(value) for value in frame_spectrum],
        "gram_tail_max_abs": float(
            np.max(np.abs(gram_spectrum[:-DIMENSION]))
        ),
        "active_1e-4": contact_summary(x, 1e-4),
        "active_1e-6": contact_summary(x, 1e-6),
        "active_1e-8": contact_summary(x, 1e-8),
    }


def source_contact_adjacency(x: np.ndarray) -> np.ndarray:
    x = unit_rows(x)
    gram = x @ x.T
    adjacency = gram >= 0.5 - 2e-12
    np.fill_diagonal(adjacency, False)
    return adjacency


def select_split_parents(
    x: np.ndarray,
    count: int,
    rng: np.random.Generator,
    variant: int,
) -> list[int]:
    """Choose separated source vertices with deterministic asymmetric ties."""
    adjacency = source_contact_adjacency(x)
    degree = adjacency.sum(axis=1)
    if variant % 2 == 0:
        first_pool = np.flatnonzero(degree == np.max(degree))
    else:
        first_pool = np.flatnonzero(degree == np.min(degree))
    selected = [int(rng.choice(first_pool))]
    while len(selected) < count:
        options = [vertex for vertex in range(len(x)) if vertex not in selected]
        rng.shuffle(options)
        best = None
        best_key = None
        for vertex in options:
            contacts = int(np.sum(adjacency[vertex, selected]))
            largest_inner = float(np.max(x[vertex] @ x[selected].T))
            degree_bias = (
                -int(degree[vertex])
                if variant % 2 == 0
                else int(degree[vertex])
            )
            key = (contacts, largest_inner, degree_bias)
            if best_key is None or key < best_key:
                best_key = key
                best = int(vertex)
        if best is None:
            raise AssertionError("parent selection failed")
        selected.append(best)
    return selected


def asymmetric_split_directions(
    x: np.ndarray,
    parents: list[int],
    rng: np.random.Generator,
) -> list[np.ndarray]:
    adjacency = source_contact_adjacency(x)
    directions = []
    for order, parent in enumerate(parents):
        random = rng.normal(size=DIMENSION)
        neighbors = np.flatnonzero(adjacency[parent])
        bias = -np.sum(x[neighbors], axis=0) if len(neighbors) else 0.0
        direction = random + (0.17 + 0.06 * order) * bias
        direction -= float(direction @ x[parent]) * x[parent]
        norm = float(np.linalg.norm(direction))
        if norm <= 1e-12:
            direction = np.roll(x[parent], 1)
            direction -= float(direction @ x[parent]) * x[parent]
            norm = float(np.linalg.norm(direction))
        directions.append(direction / norm)
    return directions


def make_split_configuration(
    source: np.ndarray,
    parents: list[int],
    directions: list[np.ndarray],
    separation: float,
) -> tuple[np.ndarray, list[tuple[int, int]], dict[int, list[int]]]:
    parent_set = set(parents)
    rows = []
    source_to_current: dict[int, list[int]] = {}
    for index, row in enumerate(source):
        if index not in parent_set:
            source_to_current[index] = [len(rows)]
            rows.append(row.copy())
    pairs = []
    for parent, direction in zip(parents, directions):
        center = source[parent]
        half = 0.5 * separation
        first = math.cos(half) * center + math.sin(half) * direction
        second = math.cos(half) * center - math.sin(half) * direction
        pair = (len(rows), len(rows) + 1)
        rows.extend([first, second])
        pairs.append(pair)
        source_to_current[parent] = [pair[0], pair[1]]
    return unit_rows(np.asarray(rows)), pairs, source_to_current


def force_pair_separation(
    x: np.ndarray,
    pairs: list[tuple[int, int]],
    separation: float,
) -> np.ndarray:
    x = unit_rows(x)
    answer = x.copy()
    half = 0.5 * separation
    for first, second in pairs:
        center = x[first] + x[second]
        center_norm = float(np.linalg.norm(center))
        difference = x[first] - x[second]
        if center_norm <= 1e-12 or float(np.linalg.norm(difference)) <= 1e-12:
            raise ValueError("split pair lost its center/difference frame")
        center /= center_norm
        direction = difference - float(difference @ center) * center
        direction /= np.linalg.norm(direction)
        answer[first] = math.cos(half) * center + math.sin(half) * direction
        answer[second] = math.cos(half) * center - math.sin(half) * direction
    return unit_rows(answer)


def source_neighborhood(
    adjacency: np.ndarray,
    parents: list[int],
    radius: int | None,
) -> set[int]:
    if radius is None:
        return set(range(len(adjacency)))
    distance = {int(parent): 0 for parent in parents}
    queue = deque(parents)
    while queue:
        vertex = int(queue.popleft())
        if distance[vertex] >= radius:
            continue
        for neighbor in np.flatnonzero(adjacency[vertex]):
            neighbor = int(neighbor)
            if neighbor not in distance:
                distance[neighbor] = distance[vertex] + 1
                queue.append(neighbor)
    return set(distance)


def current_movable_indices(
    source_vertices: set[int],
    source_to_current: dict[int, list[int]],
) -> list[int]:
    return sorted(
        current
        for source in source_vertices
        for current in source_to_current[source]
    )


def epigraph_refine(
    initial: np.ndarray,
    movable: list[int],
    split_pairs: list[tuple[int, int]],
    prescribed_pair_inner: float | None,
    max_iterations: int,
) -> tuple[np.ndarray, dict]:
    """Literal epigraph solve with optional split-pair equalities."""
    initial = unit_rows(initial)
    n = len(initial)
    movable = sorted(set(int(value) for value in movable))
    local_index = np.full(n, -1, dtype=int)
    local_index[movable] = np.arange(len(movable))
    first, second = pair_indices(n)
    variable = np.r_[initial[movable].ravel(), maximum(initial)]

    def unpack(values: np.ndarray) -> tuple[np.ndarray, float]:
        points = initial.copy()
        points[movable] = values[:-1].reshape(len(movable), DIMENSION)
        return points, float(values[-1])

    def objective(values: np.ndarray) -> float:
        return float(values[-1])

    def objective_jac(values: np.ndarray) -> np.ndarray:
        answer = np.zeros_like(values)
        answer[-1] = 1.0
        return answer

    def inequalities(values: np.ndarray) -> np.ndarray:
        points, epigraph = unpack(values)
        return epigraph - np.sum(points[first] * points[second], axis=1)

    def inequalities_jac(values: np.ndarray) -> np.ndarray:
        points, _ = unpack(values)
        answer = np.zeros((len(first), len(values)))
        rows = np.arange(len(first))
        first_movable = local_index[first] >= 0
        second_movable = local_index[second] >= 0
        for coordinate in range(DIMENSION):
            answer[
                rows[first_movable],
                DIMENSION * local_index[first[first_movable]] + coordinate,
            ] = -points[second[first_movable], coordinate]
            answer[
                rows[second_movable],
                DIMENSION * local_index[second[second_movable]] + coordinate,
            ] = -points[first[second_movable], coordinate]
        answer[:, -1] = 1.0
        return answer

    equality_count = len(movable) + (
        len(split_pairs) if prescribed_pair_inner is not None else 0
    )

    def equalities(values: np.ndarray) -> np.ndarray:
        points, _ = unpack(values)
        answer = np.empty(equality_count)
        answer[: len(movable)] = (
            np.sum(points[movable] * points[movable], axis=1) - 1.0
        )
        if prescribed_pair_inner is not None:
            for row, (left, right) in enumerate(split_pairs, len(movable)):
                answer[row] = (
                    float(points[left] @ points[right])
                    - prescribed_pair_inner
                )
        return answer

    def equalities_jac(values: np.ndarray) -> np.ndarray:
        points, _ = unpack(values)
        answer = np.zeros((equality_count, len(values)))
        for row, vertex in enumerate(movable):
            start = DIMENSION * row
            answer[row, start : start + DIMENSION] = 2.0 * points[vertex]
        if prescribed_pair_inner is not None:
            for row, (left, right) in enumerate(split_pairs, len(movable)):
                if local_index[left] >= 0:
                    start = DIMENSION * local_index[left]
                    answer[row, start : start + DIMENSION] = points[right]
                if local_index[right] >= 0:
                    start = DIMENSION * local_index[right]
                    answer[row, start : start + DIMENSION] = points[left]
        return answer

    result = minimize(
        objective,
        variable,
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
            "maxiter": int(max_iterations),
            "ftol": 2e-13,
            "disp": False,
        },
    )
    points, epigraph = unpack(result.x)
    points = unit_rows(points)
    pair_products = [
        float(points[left] @ points[right]) for left, right in split_pairs
    ]
    equality_residual = (
        max(
            abs(value - prescribed_pair_inner)
            for value in pair_products
        )
        if prescribed_pair_inner is not None and pair_products
        else 0.0
    )
    return points, {
        "success": bool(result.success),
        "status": int(result.status),
        "message": str(result.message),
        "iterations": int(result.nit),
        "evaluations": int(result.nfev),
        "movable_count": len(movable),
        "reported_epigraph": epigraph,
        "recomputed_maximum": maximum(points),
        "prescribed_pair_inner": prescribed_pair_inner,
        "recomputed_pair_products": pair_products,
        "pair_equality_max_error": float(equality_residual),
    }


def run_homotopy(
    source_name: str,
    source: np.ndarray,
    n: int,
    seed: int,
    variant: int,
    thetas: tuple[float, ...],
    radii: tuple[int | None, ...],
    stage_iterations: int,
    final_iterations: int,
) -> dict:
    started = time.time()
    rng = np.random.default_rng(seed)
    split_count = n - 40
    parents = select_split_parents(source, split_count, rng, variant)
    directions = asymmetric_split_directions(source, parents, rng)
    x, pairs, source_to_current = make_split_configuration(
        source, parents, directions, thetas[0]
    )
    adjacency = source_contact_adjacency(source)
    stages = []
    best = x.copy()
    best_maximum = maximum(best)
    for stage_index, (theta, radius) in enumerate(zip(thetas, radii)):
        x = force_pair_separation(x, pairs, theta)
        released_source = source_neighborhood(adjacency, parents, radius)
        movable = current_movable_indices(
            released_source, source_to_current
        )
        before = maximum(x)
        x, solver = epigraph_refine(
            x,
            movable=movable,
            split_pairs=pairs,
            prescribed_pair_inner=math.cos(theta),
            max_iterations=stage_iterations,
        )
        after = maximum(x)
        if after < best_maximum:
            best, best_maximum = x.copy(), after
        stages.append(
            {
                "stage": stage_index,
                "separation_radians": float(theta),
                "prescribed_pair_inner": float(math.cos(theta)),
                "source_neighborhood_radius": radius,
                "released_source_vertex_count": len(released_source),
                "movable_current_vertex_count": len(movable),
                "before_refinement_maximum": before,
                "after_refinement_maximum": after,
                "solver": solver,
                "active_1e-6": contact_summary(x, 1e-6),
            }
        )

    constrained_endpoint = diagnostics(x)
    all_vertices = list(range(n))
    released, final_solver = epigraph_refine(
        x,
        movable=all_vertices,
        split_pairs=pairs,
        prescribed_pair_inner=None,
        max_iterations=final_iterations,
    )
    if maximum(released) < best_maximum:
        best = released.copy()
        best_maximum = maximum(released)
    return {
        "source": source_name,
        "n": n,
        "seed": int(seed),
        "variant": int(variant),
        "split_count": split_count,
        "selected_source_parent_indices": parents,
        "initial_tangent_directions": [
            [float(value) for value in direction] for direction in directions
        ],
        "current_split_pair_indices": [
            [int(left), int(right)] for left, right in pairs
        ],
        "separation_schedule_radians": [float(value) for value in thetas],
        "release_radius_schedule": list(radii),
        "stages": stages,
        "constrained_endpoint": constrained_endpoint,
        "final_pair_constraint_release": final_solver,
        "released_endpoint": diagnostics(released),
        "best": diagnostics(best),
        "elapsed_seconds": time.time() - started,
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", nargs="+", type=int, default=[41, 42, 43, 44])
    parser.add_argument(
        "--sources",
        nargs="+",
        choices=["D5", "L5", "Q5", "R5"],
        default=["D5", "L5", "Q5", "R5"],
    )
    parser.add_argument("--variants", type=int, default=2)
    parser.add_argument("--base-seed", type=int, default=2026075100)
    parser.add_argument("--stage-iterations", type=int, default=220)
    parser.add_argument("--final-iterations", type=int, default=1000)
    parser.add_argument(
        "--thetas",
        nargs="+",
        type=float,
        default=list(DEFAULT_THETAS),
    )
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    if any(n not in (41, 42, 43, 44) for n in arguments.n):
        raise ValueError("cardinalities must be among 41,42,43,44")
    if arguments.variants < 1:
        raise ValueError("variants must be positive")
    thetas = tuple(float(value) for value in arguments.thetas)
    if len(thetas) != len(DEFAULT_RADII):
        raise ValueError(
            f"theta schedule must have {len(DEFAULT_RADII)} entries"
        )
    if any(
        not (0.0 < first < second < math.pi)
        for first, second in zip(thetas, thetas[1:])
    ):
        raise ValueError("theta schedule must be strictly increasing in (0,pi)")
    radii = DEFAULT_RADII
    exact_codes = exact_known_codes()
    floating = {
        name: floating_code(code) for name, code in exact_codes.items()
    }
    source_records = {}
    for name in arguments.sources:
        source_records[name] = {
            "coordinate_semantics": (
                "each rational row q denotes the unit vector q/sqrt(2)"
            ),
            "coordinates_numerator_over_sqrt2": [
                [fraction_text(value) for value in row]
                for row in exact_codes[name]
            ],
            "exact_pair_inner_product_histogram_before_dividing_by_two": (
                exact_pair_histogram(exact_codes[name])
            ),
            "floating_diagnostics": diagnostics(floating[name]),
        }

    runs = []
    source_number = {name: index for index, name in enumerate(arguments.sources)}
    for name in arguments.sources:
        for n in arguments.n:
            for variant in range(arguments.variants):
                seed = (
                    arguments.base_seed
                    + 10000 * source_number[name]
                    + 100 * n
                    + variant
                )
                run = run_homotopy(
                    source_name=name,
                    source=floating[name],
                    n=n,
                    seed=seed,
                    variant=variant,
                    thetas=thetas,
                    radii=radii,
                    stage_iterations=arguments.stage_iterations,
                    final_iterations=arguments.final_iterations,
                )
                runs.append(run)
                print(
                    f"source={name} N={n} variant={variant} seed={seed} "
                    f"best={run['best']['maximum_inner_product_binary64']:.17g}",
                    flush=True,
                )
                partial = {
                    "status": STATUS,
                    "method": (
                        "continuous point-splitting cardinality homotopy with "
                        "expanding contact-neighborhood release and literal "
                        "epigraph settling"
                    ),
                    "smooth_max_surrogate_used": False,
                    "environment": {
                        "python": platform.python_version(),
                        "numpy": np.__version__,
                        "scipy": scipy.__version__,
                        "platform": platform.platform(),
                    },
                    "parameters": {
                        "n": arguments.n,
                        "sources": arguments.sources,
                        "variants": arguments.variants,
                        "base_seed": arguments.base_seed,
                        "stage_iterations": arguments.stage_iterations,
                        "final_iterations": arguments.final_iterations,
                        "theta_schedule_radians": list(thetas),
                        "release_radius_schedule": list(radii),
                    },
                    "sources": source_records,
                    "runs": runs,
                }
                arguments.output.parent.mkdir(parents=True, exist_ok=True)
                arguments.output.write_text(
                    json.dumps(partial, indent=2, sort_keys=True) + "\n"
                )

    best_by_n = {}
    best_by_source_n = {}
    for n in arguments.n:
        eligible = [run for run in runs if run["n"] == n]
        chosen = min(
            eligible,
            key=lambda run: run["best"]["maximum_inner_product_binary64"],
        )
        best_by_n[str(n)] = {
            "source": chosen["source"],
            "seed": chosen["seed"],
            "variant": chosen["variant"],
            "maximum_inner_product_binary64": chosen["best"][
                "maximum_inner_product_binary64"
            ],
            "maximum_inner_product_float_hex": chosen["best"][
                "maximum_inner_product_float_hex"
            ],
            "coordinate_little_endian_float64_sha256": chosen["best"][
                "coordinate_little_endian_float64_sha256"
            ],
        }
    for name in arguments.sources:
        for n in arguments.n:
            eligible = [
                run
                for run in runs
                if run["n"] == n and run["source"] == name
            ]
            chosen = min(
                eligible,
                key=lambda run: run["best"]["maximum_inner_product_binary64"],
            )
            best_by_source_n[f"{name}:{n}"] = {
                "seed": chosen["seed"],
                "variant": chosen["variant"],
                "maximum_inner_product_binary64": chosen["best"][
                    "maximum_inner_product_binary64"
                ],
                "coordinate_little_endian_float64_sha256": chosen["best"][
                    "coordinate_little_endian_float64_sha256"
                ],
            }
    final_payload = partial
    final_payload.update(
        {
            "best_by_n": best_by_n,
            "best_by_source_n": best_by_source_n,
            "binary64_threshold_hit": any(
                run["best"]["meets_threshold_binary64"] for run in runs
            ),
            "warning": (
                "All search outputs are binary64 numerical evidence. "
                "Search failure is not an upper bound."
            ),
        }
    )
    arguments.output.write_text(
        json.dumps(final_payload, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(best_by_n, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
