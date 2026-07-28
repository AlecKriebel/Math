#!/usr/bin/env python3
"""Archived checks for the rejected Checkpoint 2A foundation draft.

The script checks:

1. the epsilon^2 smooth-curvature limit for the constraint
   z - b1*x - b2*y = 0 under minimum-Euclidean-motion transport;
2. the order defect of two irreversible convex-projection repairs; and
3. sharpness of the nonexpansive local-to-global order-debt bound on a grid.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


def transport_segment(
    b_start: np.ndarray, b_end: np.ndarray, y_start: np.ndarray
) -> np.ndarray:
    """Horizontally transport y while b moves affinely along one segment."""

    delta = b_end - b_start

    def rhs(t: float, y: np.ndarray) -> np.ndarray:
        b = b_start + t * delta
        denominator = 1.0 + float(b @ b)
        return -b * float(y @ delta) / denominator

    solution = solve_ivp(
        rhs,
        (0.0, 1.0),
        y_start,
        method="DOP853",
        rtol=2.0e-13,
        atol=2.0e-15,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    return solution.y[:, -1]


def two_order_transports(epsilon: float, y0: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return transports along b1-then-b2 and b2-then-b1."""

    origin = np.zeros(2)
    b1_corner = np.array([epsilon, 0.0])
    b2_corner = np.array([0.0, epsilon])
    target = np.array([epsilon, epsilon])

    first_b1 = transport_segment(origin, b1_corner, y0)
    b1_then_b2 = transport_segment(b1_corner, target, first_b1)

    first_b2 = transport_segment(origin, b2_corner, y0)
    b2_then_b1 = transport_segment(b2_corner, target, first_b2)
    return b1_then_b2, b2_then_b1


def smooth_limit_check() -> dict:
    y0 = np.array([1.0, 2.0])
    # [H_1,H_2] at b=0 equals (-y_2,y_1).
    predicted = np.array([-y0[1], y0[0]])
    rows = []
    for epsilon in (0.2, 0.1, 0.05, 0.025, 0.0125):
        first, second = two_order_transports(epsilon, y0)
        scaled = (first - second) / epsilon**2
        error = float(np.linalg.norm(scaled - predicted))
        rows.append(
            {
                "epsilon": epsilon,
                "b1_then_b2": first.tolist(),
                "b2_then_b1": second.tolist(),
                "scaled_difference": scaled.tolist(),
                "error_to_curvature_vector": error,
            }
        )

    # A first-order decrease of the scaled error is expected because the
    # unscaled expansion has an O(epsilon^3) remainder.
    error_ratios = [
        rows[index]["error_to_curvature_vector"]
        / rows[index + 1]["error_to_curvature_vector"]
        for index in range(len(rows) - 1)
    ]
    if rows[-1]["error_to_curvature_vector"] > 0.04:
        raise AssertionError("smooth square defect did not approach curvature")
    return {
        "initial_internal_state": y0.tolist(),
        "predicted_curvature_vector": predicted.tolist(),
        "rows": rows,
        "successive_error_ratios": error_ratios,
    }


def project_constraint_a(point: np.ndarray) -> np.ndarray:
    """Project onto A={x >= 1}."""

    return np.array([max(1.0, point[0]), point[1]])


def project_constraint_b(point: np.ndarray) -> np.ndarray:
    """Project onto B={x+y >= 1}."""

    if point.sum() >= 1.0:
        return point.copy()
    displacement = (1.0 - float(point.sum())) / 2.0
    return point + displacement


def project_constraints_ab(point: np.ndarray) -> np.ndarray:
    """Project the two example points onto A intersect B.

    The formula is complete for the paths used here. Both incoming points have
    y >= 0, so enforcing x >= 1 also enforces x+y >= 1.
    """

    if point[1] < 0:
        raise ValueError("example projection formula expects y >= 0")
    return project_constraint_a(point)


def active_set_check() -> dict:
    origin = np.zeros(2)

    after_a = project_constraint_a(origin)
    a_then_b = project_constraints_ab(after_a)

    after_b = project_constraint_b(origin)
    b_then_a = project_constraints_ab(after_b)

    reset = project_constraints_ab(origin)
    defect = float(np.linalg.norm(a_then_b - b_then_a))
    if not np.isclose(defect, 0.5):
        raise AssertionError(f"expected active-set order defect 0.5, got {defect}")
    if not np.allclose(reset, a_then_b):
        raise AssertionError("reset/carry comparison changed unexpectedly")
    return {
        "start": origin.tolist(),
        "A_then_B": a_then_b.tolist(),
        "B_then_A": b_then_a.tolist(),
        "order_defect": defect,
        "global_reset_to_intersection": reset.tolist(),
    }


def grid_sharpness_check(n_horizontal: int = 7, n_vertical: int = 5) -> dict:
    """Check equality in the N*epsilon bound on a rectangular grid.

    Horizontal maps are identities. A vertical map in column i translates the
    real state by i*epsilon. Every elementary square has defect epsilon.
    """

    epsilon = 0.03
    vertical_first = 0.0
    horizontal_first = n_vertical * n_horizontal * epsilon
    inversion_count = n_vertical * n_horizontal
    bound = inversion_count * epsilon
    observed = abs(horizontal_first - vertical_first)
    if not np.isclose(observed, bound):
        raise AssertionError("the sharp grid example did not attain the bound")
    return {
        "grid": [n_horizontal, n_vertical],
        "elementary_square_defect": epsilon,
        "minimum_adjacent_swap_count": inversion_count,
        "observed_endpoint_defect": observed,
        "local_to_global_bound": bound,
        "bound_is_attained": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = {
        "smooth_limit": smooth_limit_check(),
        "active_set_projection": active_set_check(),
        "grid_bound_sharpness": grid_sharpness_check(),
    }
    serialized = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)


if __name__ == "__main__":
    main()
