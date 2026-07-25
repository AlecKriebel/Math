#!/usr/bin/env python3
"""Numerically audit the certified degree-11 kernel on enlarged caps.

For epsilon >= 0 the enlarged cap is -epsilon <= u <= 1.  If the fixed
degree-11 kernel had a rigorously certified objective below 35 on this
larger domain, every 41-point code would have at least seven points with
inner product < -epsilon in every direction.

This script is discovery-only.  It reconstructs the exact rational
polynomial from the certified Gram factors, converts its coefficients to
double precision, and audits dense deterministic and random subsets of the
new domain.  It never modifies or verifies the existing certificate.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
CORE_PATH = ROOT / "verifiers" / "verify_one_sided_cap_degree10.py"
CERTIFICATE_PATH = ROOT / "certificates" / "one_sided_cap_degree11_bound.json"
SPEC = importlib.util.spec_from_file_location("cap_exact_core_robust", CORE_PATH)
assert SPEC is not None and SPEC.loader is not None
CORE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CORE)


def coefficient_tensor() -> np.ndarray:
    blocks = CORE.load_blocks(str(CERTIFICATE_PATH))
    polynomial = CORE.cap_polynomial(blocks)
    degree = len(blocks) - 1
    coefficients = np.zeros((degree + 1, degree + 1, degree + 1))
    for exponent, coefficient in polynomial.items():
        coefficients[exponent] = float(coefficient)
    return coefficients


def evaluate(
    coefficients: np.ndarray,
    u: np.ndarray | float,
    v: np.ndarray | float,
    t: np.ndarray | float,
) -> np.ndarray:
    return np.polynomial.polynomial.polyval3d(u, v, t, coefficients)


def feasible_interval(u: np.ndarray, v: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    radius = np.sqrt(np.maximum(0.0, (1.0 - u * u) * (1.0 - v * v)))
    return np.maximum(-1.0, u * v - radius), np.minimum(0.5, u * v + radius)


def update(
    current: tuple[float, tuple[float, float, float] | None],
    values: np.ndarray,
    u: np.ndarray,
    v: np.ndarray,
    t: np.ndarray,
) -> tuple[float, tuple[float, float, float] | None]:
    if values.size == 0:
        return current
    index = int(np.argmax(values))
    value = float(values[index])
    if value > current[0]:
        return value, (float(u[index]), float(v[index]), float(t[index]))
    return current


def audit_epsilon(
    coefficients: np.ndarray,
    epsilon: float,
    random_count: int,
    seed: int,
    face_height: int,
    face_alpha: int,
    boundary_height: int,
    symmetry_height: int,
    symmetry_alpha: int,
    diagonal_count: int,
) -> dict[str, object]:
    low_height = -epsilon
    rng = np.random.default_rng(seed)
    worst: tuple[float, tuple[float, float, float] | None] = (-math.inf, None)
    category: dict[str, object] = {}

    u = rng.uniform(low_height, 1.0, random_count)
    v = rng.uniform(low_height, 1.0, random_count)
    swap = u > v
    u[swap], v[swap] = v[swap], u[swap].copy()
    low, high = feasible_interval(u, v)
    feasible = low <= high
    u, v, low, high = u[feasible], v[feasible], low[feasible], high[feasible]
    for label, alpha in (
        ("random_interior", rng.random(len(u))),
        ("random_boundary_biased", rng.beta(0.35, 0.35, len(u))),
        ("lower_determinant", np.zeros(len(u))),
        ("upper_or_contact", np.ones(len(u))),
    ):
        t = low + alpha * (high - low)
        local = (-math.inf, None)
        for start in range(0, len(u), 50_000):
            stop = min(start + 50_000, len(u))
            local = update(
                local,
                evaluate(
                    coefficients,
                    u[start:stop],
                    v[start:stop],
                    t[start:stop],
                ),
                u[start:stop],
                v[start:stop],
                t[start:stop],
            )
        category[label] = {"maximum": local[0], "point": local[1]}
        if local[0] > worst[0]:
            worst = local

    # New face u=-epsilon, including determinant sheets and interior.
    v_grid = np.linspace(low_height, 1.0, face_height)
    alpha_grid = np.linspace(0.0, 1.0, face_alpha)
    local = (-math.inf, None)
    for v_value in v_grid:
        u_row = np.full(face_alpha, low_height)
        v_row = np.full(face_alpha, float(v_value))
        low, high = feasible_interval(u_row, v_row)
        feasible = low <= high
        t = low + alpha_grid * (high - low)
        local = update(
            local,
            evaluate(coefficients, u_row[feasible], v_row[feasible], t[feasible]),
            u_row[feasible],
            v_row[feasible],
            t[feasible],
        )
    category["new_negative_face"] = {"maximum": local[0], "point": local[1]}
    if local[0] > worst[0]:
        worst = local

    # Symmetry ridge u=v, now extended through the small negative interval.
    local = (-math.inf, None)
    alpha_grid = np.linspace(0.0, 1.0, symmetry_alpha)
    for height in np.linspace(low_height, math.sqrt(3.0) / 2.0, symmetry_height):
        u_row = np.full(symmetry_alpha, float(height))
        low, high = feasible_interval(u_row, u_row)
        feasible = low <= high
        t = low + alpha_grid * (high - low)
        local = update(
            local,
            evaluate(coefficients, u_row[feasible], u_row[feasible], t[feasible]),
            u_row[feasible],
            u_row[feasible],
            t[feasible],
        )
    category["symmetry_ridge"] = {"maximum": local[0], "point": local[1]}
    if local[0] > worst[0]:
        worst = local

    # Tensor height grid on determinant sheets and the contact face.
    heights = np.linspace(low_height, 1.0, boundary_height)
    uu, vv = np.meshgrid(heights, heights, indexing="ij")
    mask_order = uu <= vv
    u = uu[mask_order]
    v = vv[mask_order]
    low, high = feasible_interval(u, v)
    feasible = low <= high
    u, v, low, high = u[feasible], v[feasible], low[feasible], high[feasible]
    for label, t in (
        ("height_grid_lower_determinant", low),
        ("height_grid_upper_or_contact", high),
    ):
        local = update(
            (-math.inf, None),
            evaluate(coefficients, u, v, t),
            u,
            v,
            t,
        )
        category[label] = {"maximum": local[0], "point": local[1]}
        if local[0] > worst[0]:
            worst = local

    heights = np.linspace(low_height, 1.0, diagonal_count)
    diagonal_values = evaluate(coefficients, heights, heights, np.ones_like(heights))
    diagonal_index = int(np.argmax(diagonal_values))
    diagonal_maximum = float(diagonal_values[diagonal_index])
    diagonal_height = float(heights[diagonal_index])
    off_maximum = worst[0]
    objective = (
        1.0 - diagonal_maximum / off_maximum
        if off_maximum < 0.0
        else math.inf
    )
    return {
        "epsilon": epsilon,
        "off_diagonal": {
            "maximum": off_maximum,
            "point": worst[1],
            "categories": category,
        },
        "diagonal": {
            "maximum": diagonal_maximum,
            "height": diagonal_height,
        },
        "audited_rescaled_objective": objective,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--epsilons",
        default="0,1e-6,2e-6,5e-6,1e-5,2e-5,5e-5,1e-4,2e-4,5e-4,1e-3",
    )
    parser.add_argument("--random", type=int, default=250000)
    parser.add_argument("--seed", type=int, default=511341)
    parser.add_argument("--face-height", type=int, default=401)
    parser.add_argument("--face-alpha", type=int, default=401)
    parser.add_argument("--boundary-height", type=int, default=301)
    parser.add_argument("--symmetry-height", type=int, default=1001)
    parser.add_argument("--symmetry-alpha", type=int, default=401)
    parser.add_argument("--diagonal", type=int, default=50001)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    coefficients = coefficient_tensor()
    epsilons = [float(value) for value in args.epsilons.split(",")]
    results = []
    for index, epsilon in enumerate(epsilons):
        result = audit_epsilon(
            coefficients,
            epsilon,
            args.random,
            args.seed + index,
            args.face_height,
            args.face_alpha,
            args.boundary_height,
            args.symmetry_height,
            args.symmetry_alpha,
            args.diagonal,
        )
        results.append(result)
        print(json.dumps(result, indent=2), flush=True)

    report = {
        "status": "NUMERICAL EVIDENCE ONLY",
        "source_certificate": str(CERTIFICATE_PATH.relative_to(ROOT)),
        "source_kernel_degree": 11,
        "numpy_version": np.__version__,
        "parameters": {
            "random": args.random,
            "seed": args.seed,
            "face_height": args.face_height,
            "face_alpha": args.face_alpha,
            "boundary_height": args.boundary_height,
            "symmetry_height": args.symmetry_height,
            "symmetry_alpha": args.symmetry_alpha,
            "diagonal": args.diagonal,
        },
        "results": results,
        "warning": (
            "Dense floating-point audit is not an exact enlarged-cap proof."
        ),
    }
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
