#!/usr/bin/env python3
"""Reproducible checks for revised NCS foundations.

This script tests the actual constructions used in Checkpoint 2:

- seam-margin feasibility conversion;
- affine-contractive relation-operator rectification, including a
  noninvertible edge and a gauge change;
- duplicate-cell weight normalization;
- configuration-repair route endpoints;
- partial online-allocation failure signatures; and
- calibrated response-order slopes.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


def distance_to_membership_change(y: float, threshold: float = 0.0) -> float:
    """Membership margin for D=(-infinity, threshold]."""

    return abs(y - threshold)


def seam_margin_check() -> dict:
    rng = np.random.default_rng(20260727)
    checked = 0
    for _ in range(20_000):
        y, y_prime = rng.uniform(-2.0, 2.0, size=2)
        delta = abs(y - y_prime)
        margin = distance_to_membership_change(y)
        if delta < margin:
            checked += 1
            if (y <= 0.0) != (y_prime <= 0.0):
                raise AssertionError("seam-margin implication failed")

    epsilon = 0.2
    prefix_p = np.array([-0.4, -0.1, 0.4, 0.7])
    prefix_q = np.array([-0.3, 0.1, 0.5, 0.8])
    if np.max(np.abs(prefix_p - prefix_q)) > epsilon + 1.0e-12:
        raise AssertionError("test prefixes exceed declared epsilon")
    downstream_mismatch = (prefix_p <= 0.0) != (prefix_q <= 0.0)
    pointwise_delta = np.abs(prefix_p - prefix_q)
    seam_exposed = (
        np.maximum(np.abs(prefix_p), np.abs(prefix_q)) <= pointwise_delta
    )
    if np.any(downstream_mismatch & ~seam_exposed):
        raise AssertionError("new failure occurred away from seam exposure")

    # Necessity example from the theorem.
    p_value, q_value = 0.0, epsilon
    continuation_threshold = epsilon / 2.0
    one_succeeds = (p_value < continuation_threshold) != (
        q_value < continuation_threshold
    )
    if not one_succeeds:
        raise AssertionError("necessity example did not create asymmetric failure")
    return {
        "random_safe_pairs_checked": checked,
        "distributional_example": {
            "epsilon": epsilon,
            "downstream_asymmetry_rate": float(np.mean(downstream_mismatch)),
            "two_sided_state_dependent_seam_exposure_rate": float(
                np.mean(seam_exposed)
            ),
            "bound_verified": bool(
                np.mean(downstream_mismatch) <= np.mean(seam_exposed)
            ),
        },
        "necessity_example_creates_asymmetric_failure": one_succeeds,
    }


def affine_relation_check() -> dict:
    # Square routes: a then b versus c then d. The first edge on each route is
    # noninvertible (zero linear part), and both path linear parts are zero.
    a_linear = 0.0
    b_linear = 0.8
    c_linear = 0.0
    d_linear = 0.6
    if not np.isclose(b_linear * a_linear, d_linear * c_linear):
        raise AssertionError("background linear response is not relation-exact")

    # Bias order is [a,b,c,d]. Route biases are b + B*a and d + D*c.
    relation = np.array([[b_linear, 1.0, -d_linear, -1.0]])
    biases = np.array([0.9, -0.2, 0.4, 0.7])
    residual = relation @ biases
    pseudoinverse = np.linalg.pinv(relation)
    exact_biases = (np.eye(4) - pseudoinverse @ relation) @ biases
    exact_residual = relation @ exact_biases
    correction = biases - exact_biases

    if np.linalg.norm(exact_residual) > 1.0e-12:
        raise AssertionError("pseudoinverse rectification is not exact")
    if not np.isclose(
        np.linalg.norm(correction),
        np.linalg.norm(pseudoinverse @ residual),
    ):
        raise AssertionError("rectification-distance formula failed")

    # Full affine Hilbert gauges phi_v(x)=Q_v*x+g_v. In one dimension the
    # orthogonal Q_v are signs. Translation contributions form a coboundary
    # and therefore do not alter the relation residual.
    q_vertex = np.array([-1.0, 1.0, -1.0, -1.0])
    g_vertex = np.array([0.3, -0.4, 0.8, -0.2])
    # Targets of a,b,c,d are vertices 1,3,2,3.
    q_edge = np.diag(
        [q_vertex[1], q_vertex[3], q_vertex[2], q_vertex[3]]
    )
    q_cell = np.array([[-1.0]])
    gauged_linears = np.array(
        [
            q_vertex[1] * a_linear / q_vertex[0],
            q_vertex[3] * b_linear / q_vertex[1],
            q_vertex[2] * c_linear / q_vertex[0],
            q_vertex[3] * d_linear / q_vertex[2],
        ]
    )
    relation_gauged = np.array(
        [[gauged_linears[1], 1.0, -gauged_linears[3], -1.0]]
    )
    sources = np.array([0, 1, 0, 2])
    targets = np.array([1, 3, 2, 3])
    gauged_biases = np.array(
        [
            q_vertex[t] * biases[i]
            + g_vertex[t]
            - gauged_linears[i] * g_vertex[s]
            for i, (s, t) in enumerate(zip(sources, targets))
        ]
    )
    if not np.allclose(
        relation_gauged @ gauged_biases, q_cell @ residual
    ):
        raise AssertionError("affine relation operator is not gauge covariant")
    if not np.allclose(
        np.linalg.svd(relation, compute_uv=False),
        np.linalg.svd(relation_gauged, compute_uv=False),
    ):
        raise AssertionError("gauge changed singular values")
    gauged_exact = (
        np.eye(4) - np.linalg.pinv(relation_gauged) @ relation_gauged
    ) @ gauged_biases
    # The nearest point in the translated exact affine set is obtained by
    # adding the gauge coboundary to the orthogonally transformed old point.
    gauge_coboundary = gauged_biases - q_edge @ biases
    transformed_exact = q_edge @ exact_biases + gauge_coboundary
    if not np.allclose(gauged_exact, transformed_exact):
        raise AssertionError("full affine gauge did not preserve rectification")
    if not np.isclose(
        np.linalg.norm(gauged_biases - gauged_exact),
        np.linalg.norm(correction),
    ):
        raise AssertionError("full affine gauge changed rectification distance")

    # Duplicating a relation twice with half weight preserves D^*D.
    weighted_duplicate = np.vstack(
        [np.sqrt(0.5) * relation, np.sqrt(0.5) * relation]
    )
    if not np.allclose(
        relation.T @ relation,
        weighted_duplicate.T @ weighted_duplicate,
    ):
        raise AssertionError("split duplicate-cell weights changed residual energy")

    return {
        "linear_parts": {
            "a": a_linear,
            "b": b_linear,
            "c": c_linear,
            "d": d_linear,
            "route_products": [
                b_linear * a_linear,
                d_linear * c_linear,
            ],
        },
        "biases": biases.tolist(),
        "relation_row": relation[0].tolist(),
        "relation_residual": residual.tolist(),
        "rectified_biases": exact_biases.tolist(),
        "rectified_residual_norm": float(np.linalg.norm(exact_residual)),
        "correction_norm": float(np.linalg.norm(correction)),
        "one_dimensional_full_affine_gauge_instance_verified": True,
        "weighted_duplicate_invariance_verified": True,
    }


def project_halfspace(point: np.ndarray, normal: np.ndarray, rhs: float) -> np.ndarray:
    violation = rhs - float(normal @ point)
    if violation <= 0.0:
        return point.copy()
    return point + violation * normal / float(normal @ normal)


def configuration_repair_check(lambda_value: float = 2.0) -> dict:
    origin = np.zeros(2)
    # A: x >= lambda. B: x+y >= 2 lambda.
    after_a = project_halfspace(
        origin, np.array([1.0, 0.0]), lambda_value
    )
    a_then_b = project_halfspace(
        after_a, np.array([1.0, 1.0]), 2.0 * lambda_value
    )
    after_b = project_halfspace(
        origin, np.array([1.0, 1.0]), 2.0 * lambda_value
    )
    # after_b=(lambda,lambda), which already satisfies A.
    b_then_a = project_halfspace(
        after_b, np.array([1.0, 0.0]), lambda_value
    )
    predicted_a_then_b = np.array([1.5 * lambda_value, 0.5 * lambda_value])
    predicted_b_then_a = np.array([lambda_value, lambda_value])
    if not np.allclose(a_then_b, predicted_a_then_b):
        raise AssertionError("A-then-B endpoint is wrong")
    if not np.allclose(b_then_a, predicted_b_then_a):
        raise AssertionError("B-then-A endpoint is wrong")
    defect = float(np.linalg.norm(a_then_b - b_then_a))
    predicted_defect = lambda_value / np.sqrt(2.0)
    if not np.isclose(defect, predicted_defect):
        raise AssertionError("configuration defect scaling is wrong")
    guard_threshold = 0.75 * lambda_value
    a_then_b_passes_guard = bool(a_then_b[1] >= guard_threshold)
    b_then_a_passes_guard = bool(b_then_a[1] >= guard_threshold)
    guard_margins = [
        abs(float(a_then_b[1]) - guard_threshold),
        abs(float(b_then_a[1]) - guard_threshold),
    ]
    if a_then_b_passes_guard or not b_then_a_passes_guard:
        raise AssertionError("downstream configuration guard outcome changed")
    if max(guard_margins) > defect + 1.0e-12:
        raise AssertionError("guard mismatch lies outside two-sided seam exposure")
    truncation_scale = lambda_value
    signature_at_origin = {
        "A_plus": 0.0,
        "A_minus": 0.0,
        "common_failure": 0.0,
        "truncated_value_defect": min(1.0, defect / truncation_scale),
        "truncation_scale": truncation_scale,
    }
    return {
        "lambda": lambda_value,
        "A_then_B": a_then_b.tolist(),
        "B_then_A": b_then_a.tolist(),
        "defect": defect,
        "predicted_defect": predicted_defect,
        "closed_form_formula_verified": True,
        "full_signature_at_origin": signature_at_origin,
        "downstream_guard": {
            "threshold_y": guard_threshold,
            "A_then_B_passes": a_then_b_passes_guard,
            "B_then_A_passes": b_then_a_passes_guard,
            "endpoint_margins": guard_margins,
            "two_sided_seam_condition_verified": True,
        },
    }


def allocation_failure_check() -> dict:
    empty = "empty"
    a_on_1 = "A->1"
    a_on_2 = "A->2"
    b_on_1 = "B->1"
    both = "B->1,A->2"

    fibers = {
        "empty": [empty],
        "A": [a_on_1, a_on_2],
        "B": [b_on_1],
        "AB": [both],
    }
    empty_to_a = {empty: a_on_1}
    empty_to_b = {empty: b_on_1}
    # B can be added without migration only when A already occupies server 2.
    add_b_after_a = {a_on_2: both}
    add_a_after_b = {b_on_1: both}

    first_a = empty_to_a[empty]
    a_then_b = add_b_after_a.get(first_a)
    first_b = empty_to_b[empty]
    b_then_a = add_a_after_b.get(first_b)
    asymmetric = (a_then_b is None) != (b_then_a is None)
    if not asymmetric or b_then_a != both:
        raise AssertionError("allocation failure signature changed")
    # Every map has singleton domain or codomain, hence is nonexpansive for
    # the declared unit discrete metrics.
    maps = [empty_to_a, empty_to_b, add_b_after_a, add_a_after_b]
    for mapping in maps:
        items = list(mapping.items())
        for i, (x, tx) in enumerate(items):
            for y, ty in items[i + 1 :]:
                source_distance = 0.0 if x == y else 1.0
                target_distance = 0.0 if tx == ty else 1.0
                if target_distance > source_distance:
                    raise AssertionError("allocation edge is expansive")
    return {
        "fibers": fibers,
        "add_B_after_A_domain": list(add_b_after_a),
        "A_then_B": "failure" if a_then_b is None else a_then_b,
        "B_then_A": b_then_a,
        "asymmetric_failure": asymmetric,
        "directional_signature_at_empty": {
            "A_plus_only_A_then_B_succeeds": 0.0,
            "A_minus_only_B_then_A_succeeds": 1.0,
            "common_failure": 0.0,
        },
        "declared_partial_nonexpansiveness_verified": True,
        "batch_reset_endpoint": both,
    }


def smooth_transport_segment(
    b_start: np.ndarray, b_end: np.ndarray, y_start: np.ndarray
) -> np.ndarray:
    delta = b_end - b_start

    def rhs(t: float, y: np.ndarray) -> np.ndarray:
        b = b_start + t * delta
        return -b * float(y @ delta) / (1.0 + float(b @ b))

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


def smooth_square_difference(epsilon: float) -> np.ndarray:
    origin = np.zeros(2)
    target = np.array([epsilon, epsilon])
    y0 = np.array([1.0, 2.0])
    first = smooth_transport_segment(
        np.array([epsilon, 0.0]),
        target,
        smooth_transport_segment(
            origin, np.array([epsilon, 0.0]), y0
        ),
    )
    second = smooth_transport_segment(
        np.array([0.0, epsilon]),
        target,
        smooth_transport_segment(
            origin, np.array([0.0, epsilon]), y0
        ),
    )
    return first - second


def active_set_square_defect(epsilon: float) -> float:
    """Sequential projections onto x>=eps and x+y>=eps."""

    origin = np.zeros(2)
    normal_a = np.array([1.0, 0.0])
    normal_b = np.array([1.0, 1.0])
    a_then_b = project_halfspace(
        project_halfspace(origin, normal_a, epsilon),
        normal_b,
        epsilon,
    )
    b_then_a = project_halfspace(
        project_halfspace(origin, normal_b, epsilon),
        normal_a,
        epsilon,
    )
    return float(np.linalg.norm(a_then_b - b_then_a))


def jump_square_defect(epsilon: float) -> float:
    """Explicit order-zero protocol with two constant route outcomes."""

    del epsilon  # external cells shrink while the protocol jump stays fixed
    first_route_outcome = np.array([0.0])
    second_route_outcome = np.array([1.0])
    return float(np.linalg.norm(first_route_outcome - second_route_outcome))


def response_order_check() -> dict:
    epsilons = np.array([0.1, 0.05, 0.025, 0.0125])
    smooth_differences = np.array(
        [smooth_square_difference(eps) for eps in epsilons]
    )
    smooth = np.linalg.norm(smooth_differences, axis=1)
    active = np.array([active_set_square_defect(eps) for eps in epsilons])
    jump = np.array([jump_square_defect(eps) for eps in epsilons])

    def slope(values: np.ndarray) -> float:
        return float(np.polyfit(np.log(epsilons), np.log(values), 1)[0])

    slopes = {
        "smooth": slope(smooth),
        "active_set": slope(active),
        "jump": slope(jump),
    }
    # Multiplying output units and amplitude units by fixed positive factors
    # is a bi-Lipschitz gauge/reparameterization and must preserve the order.
    rescaled_smooth_order = float(
        np.polyfit(
            np.log(2.0 * epsilons),
            np.log(3.0 * smooth),
            1,
        )[0]
    )
    if abs(slopes["smooth"] - 2.0) > 0.03:
        raise AssertionError("smooth response order is not approximately 2")
    if abs(slopes["active_set"] - 1.0) > 1.0e-12:
        raise AssertionError("active-set response order is not 1")
    if abs(slopes["jump"]) > 1.0e-12:
        raise AssertionError("jump response order is not 0")
    if not np.isclose(rescaled_smooth_order, slopes["smooth"]):
        raise AssertionError("response order changed under unit rescaling")
    normalized_smooth_vectors = smooth_differences / epsilons[:, None] ** 2
    predicted_curvature_vector = np.array([-2.0, 1.0])
    final_vector_error = float(
        np.linalg.norm(normalized_smooth_vectors[-1] - predicted_curvature_vector)
    )
    if final_vector_error > 1.0e-3:
        raise AssertionError("smooth normalized vector missed curvature limit")
    return {
        "amplitudes": epsilons.tolist(),
        "smooth_defects": smooth.tolist(),
        "smooth_normalized_vectors": normalized_smooth_vectors.tolist(),
        "predicted_curvature_vector": predicted_curvature_vector.tolist(),
        "final_curvature_vector_error": final_vector_error,
        "active_set_defects": active.tolist(),
        "jump_defects": jump.tolist(),
        "estimated_orders": slopes,
        "rescaled_smooth_order": rescaled_smooth_order,
        "algebraic_unit_rescaling_identity_checked": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = {
        "seam_margin": seam_margin_check(),
        "affine_contractive_rectification": affine_relation_check(),
        "configuration_repair": configuration_repair_check(),
        "allocation_failure": allocation_failure_check(),
        "response_orders": response_order_check(),
    }
    serialized = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)


if __name__ == "__main__":
    main()
