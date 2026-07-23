#!/usr/bin/env python3
"""Analyze and optionally refine a numerical spherical code in R^5.

NUMERICAL EVIDENCE ONLY.  This program uses ordinary floating-point arithmetic
and a local nonlinear optimizer.  Its output is not an exact construction, an
interval certificate, or an upper-bound certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import minimize


DISCLAIMER = (
    "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE. "
    "All norms, inner products, PSD checks, and optimizer results use "
    "floating-point arithmetic."
)


def read_coordinate_text(path: Path) -> tuple[np.ndarray, str]:
    """Read either comma-separated point tokens or one point per text line."""
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    tokens = text.split()
    if tokens and all("," in token for token in tokens):
        rows = [[float(entry) for entry in token.split(",")] for token in tokens]
    else:
        rows = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            values = [float(entry) for entry in line.replace(",", " ").split()]
            if len(values) != 5:
                raise ValueError(
                    f"line {line_number} contains {len(values)} values, not 5"
                )
            rows.append(values)
    points = np.asarray(rows, dtype=float)
    if points.ndim != 2 or points.shape[1] != 5:
        raise ValueError(f"expected an N by 5 array, obtained shape {points.shape}")
    return points, hashlib.sha256(raw).hexdigest()


def normalize(points: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(points, axis=1)
    if np.any(norms == 0):
        raise ValueError("zero vector cannot be normalized")
    return points / norms[:, None]


def pair_indices(n: int) -> tuple[np.ndarray, np.ndarray]:
    return np.triu_indices(n, 1)


def smooth_max_value_gradient(
    flat: np.ndarray, n: int, beta: float
) -> tuple[float, np.ndarray]:
    """Log-sum-exp approximation to the largest pairwise inner product."""
    raw = flat.reshape((n, 5))
    norms = np.linalg.norm(raw, axis=1)
    points = raw / norms[:, None]
    first, second = pair_indices(n)
    inner_products = np.sum(points[first] * points[second], axis=1)
    scaled = beta * inner_products
    maximum = float(np.max(scaled))
    exponentials = np.exp(scaled - maximum)
    weights = exponentials / np.sum(exponentials)
    value = (maximum + math.log(float(np.sum(exponentials)))) / beta

    point_gradient = np.zeros_like(points)
    np.add.at(
        point_gradient, first, weights[:, None] * points[second]
    )
    np.add.at(
        point_gradient, second, weights[:, None] * points[first]
    )
    radial = np.sum(point_gradient * points, axis=1)
    raw_gradient = (
        point_gradient - radial[:, None] * points
    ) / norms[:, None]
    return value, raw_gradient.ravel()


def epigraph_objective(
    variables: np.ndarray, n: int
) -> tuple[float, np.ndarray]:
    gradient = np.zeros_like(variables)
    gradient[-1] = 1.0
    return float(variables[-1]), gradient


def sphere_equalities(
    variables: np.ndarray, n: int
) -> tuple[np.ndarray, np.ndarray]:
    points = variables[:-1].reshape((n, 5))
    values = np.sum(points * points, axis=1) - 1.0
    jacobian = np.zeros((n, len(variables)))
    for index in range(n):
        jacobian[index, 5 * index : 5 * index + 5] = 2.0 * points[index]
    return values, jacobian


def pair_inequalities(
    variables: np.ndarray, n: int
) -> tuple[np.ndarray, np.ndarray]:
    points = variables[:-1].reshape((n, 5))
    threshold = variables[-1]
    first, second = pair_indices(n)
    values = threshold - np.sum(points[first] * points[second], axis=1)
    jacobian = np.zeros((len(first), len(variables)))
    rows = np.arange(len(first))
    for coordinate in range(5):
        jacobian[rows, 5 * first + coordinate] = -points[second, coordinate]
        jacobian[rows, 5 * second + coordinate] = -points[first, coordinate]
    jacobian[:, -1] = 1.0
    return values, jacobian


def refine(
    points: np.ndarray, method: str
) -> tuple[np.ndarray, list[dict[str, object]]]:
    """Run a local floating-point refinement."""
    points = normalize(points)
    n = len(points)
    history: list[dict[str, object]] = []
    if method == "smooth-slsqp":
        for beta in (4000.0, 8000.0, 16000.0, 32000.0, 64000.0, 128000.0):
            result = minimize(
                smooth_max_value_gradient,
                points.ravel(),
                args=(n, beta),
                jac=True,
                method="L-BFGS-B",
                options={
                    "maxiter": 3000,
                    "maxfun": 30000,
                    "ftol": 1e-16,
                    "gtol": 2e-11,
                    "maxls": 80,
                    "maxcor": 50,
                },
            )
            points = normalize(result.x.reshape((n, 5)))
            gram = points @ points.T
            maximum = float(np.max(gram[pair_indices(n)]))
            history.append(
                {
                    "stage": "smooth_max",
                    "beta": beta,
                    "maximum_inner_product": maximum,
                    "iterations": int(result.nit),
                    "success": bool(result.success),
                    "message": str(result.message),
                }
            )

    gram = points @ points.T
    maximum = float(np.max(gram[pair_indices(n)]))
    variables = np.r_[points.ravel(), maximum + 1e-10]
    equalities = {
        "type": "eq",
        "fun": lambda value: sphere_equalities(value, n)[0],
        "jac": lambda value: sphere_equalities(value, n)[1],
    }
    inequalities = {
        "type": "ineq",
        "fun": lambda value: pair_inequalities(value, n)[0],
        "jac": lambda value: pair_inequalities(value, n)[1],
    }
    result = minimize(
        epigraph_objective,
        variables,
        args=(n,),
        jac=True,
        method="SLSQP",
        constraints=(equalities, inequalities),
        options={"maxiter": 3000, "ftol": 1e-13, "disp": False},
    )
    points = normalize(result.x[:-1].reshape((n, 5)))
    gram = points @ points.T
    maximum = float(np.max(gram[pair_indices(n)]))
    history.append(
        {
            "stage": "epigraph_slsqp",
            "reported_objective": float(result.fun),
            "recomputed_maximum_inner_product": maximum,
            "iterations": int(result.nit),
            "success": bool(result.success),
            "message": str(result.message),
        }
    )
    return points, history


def connected_component_sizes(adjacency: np.ndarray) -> list[int]:
    seen: set[int] = set()
    sizes: list[int] = []
    for start in range(len(adjacency)):
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        size = 0
        while stack:
            vertex = stack.pop()
            size += 1
            for neighbor in np.flatnonzero(adjacency[vertex]):
                neighbor = int(neighbor)
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        sizes.append(size)
    return sorted(sizes, reverse=True)


def analyze(points: np.ndarray, contact_tolerance: float) -> dict[str, object]:
    n = len(points)
    gram = points @ points.T
    first, second = pair_indices(n)
    off_diagonal = gram[first, second]
    maximum = float(np.max(off_diagonal))
    minimum = float(np.min(off_diagonal))
    adjacency = gram >= maximum - contact_tolerance
    np.fill_diagonal(adjacency, False)
    degrees = np.sum(adjacency, axis=1).astype(int)
    frame_eigenvalues = np.linalg.eigvalsh(points.T @ points)
    degree_histogram = {
        str(degree): int(np.sum(degrees == degree))
        for degree in np.unique(degrees)
    }
    return {
        "N": n,
        "dimension": 5,
        "maximum_inner_product": maximum,
        "gap_above_one_half": maximum - 0.5,
        "minimum_angle_degrees": (
            math.degrees(math.acos(max(-1.0, min(1.0, maximum))))
        ),
        "minimum_inner_product": minimum,
        "maximum_norm_squared_error": float(
            np.max(np.abs(np.sum(points * points, axis=1) - 1.0))
        ),
        "frame_or_positive_gram_eigenvalues": frame_eigenvalues.tolist(),
        "numerical_zero_gram_eigenvalue_count": n - 5,
        "contact_tolerance": contact_tolerance,
        "near_contact_edge_count": int(np.sum(adjacency) // 2),
        "near_contact_degree_histogram": degree_histogram,
        "near_contact_component_sizes": connected_component_sizes(adjacency),
        "centroid_norm": float(np.linalg.norm(np.sum(points, axis=0))),
        "passes_kissing_inequality_in_binary64": bool(maximum <= 0.5),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("coordinates", type=Path)
    parser.add_argument(
        "--refine",
        choices=("direct-slsqp", "smooth-slsqp"),
        help="run a local numerical minimax refinement",
    )
    parser.add_argument(
        "--contact-tolerance", type=float, default=1e-8
    )
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--refined-coordinates", type=Path)
    parser.add_argument(
        "--allow-other-n",
        action="store_true",
        help="allow N outside 41, 42, 43, 44",
    )
    arguments = parser.parse_args()

    points, input_hash = read_coordinate_text(arguments.coordinates)
    if not arguments.allow_other_n and len(points) not in (41, 42, 43, 44):
        parser.error(f"N={len(points)} is outside the requested range 41–44")

    report: dict[str, object] = {
        "status": DISCLAIMER,
        "software": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "input": {
            "path": str(arguments.coordinates),
            "sha256": input_hash,
        },
        "initial_analysis": analyze(points, arguments.contact_tolerance),
    }
    if arguments.refine:
        refined, history = refine(points, arguments.refine)
        report["refinement"] = {
            "method": arguments.refine,
            "history": history,
            "analysis": analyze(refined, arguments.contact_tolerance),
        }
        if arguments.refined_coordinates:
            arguments.refined_coordinates.parent.mkdir(parents=True, exist_ok=True)
            np.savetxt(
                arguments.refined_coordinates,
                refined,
                delimiter=",",
                fmt="%.17g",
            )

    encoded = json.dumps(report, indent=2, sort_keys=True)
    print(DISCLAIMER, file=sys.stderr)
    print(encoded)
    if arguments.output_json:
        arguments.output_json.parent.mkdir(parents=True, exist_ok=True)
        arguments.output_json.write_text(encoded + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
