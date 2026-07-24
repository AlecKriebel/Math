#!/usr/bin/env python3
"""Numerical feasibility search in the exact r=18 structural branch.

Variables are eighteen projective representatives u_j and five residual
vectors z_i in S^4.  The common load is

  max(
      |u_j.u_k|,
      |u_j.z_i|,
      |z_i.z_k| for noncycle residual pairs,
      1 + z_i.z_{i+1} for C5 cycle pairs
  ).

A load below 1/2 is a genuine realization of the open C5 branch.  This
program performs floating-point discovery only.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import platform
import time

import numpy as np
import scipy
from scipy.optimize import minimize


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "results" / "portfolio.json"
OLD_WARM = (
    ROOT
    / "experiments"
    / "construction_round2"
    / "results"
    / "pair_cycle_seed7.json"
)
Q_BOUND = 64 / 9


def normalized(array: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(array, axis=-1)
    if np.any(norms == 0):
        raise ValueError("cannot normalize a zero vector")
    return array / norms[..., None]


def d5_lines() -> np.ndarray:
    lines = []
    for first in range(5):
        for second in range(first + 1, 5):
            plus = np.zeros(5)
            plus[first] = plus[second] = 1 / math.sqrt(2)
            minus = np.zeros(5)
            minus[first] = 1 / math.sqrt(2)
            minus[second] = -1 / math.sqrt(2)
            lines.extend((plus, minus))
    answer = np.asarray(lines)
    if answer.shape != (20, 5):
        raise RuntimeError("D5 line construction failed")
    return answer


def orthonormal_plane(
    first: np.ndarray, second: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    first = first / np.linalg.norm(first)
    second = second - float(second @ first) * first
    norm = np.linalg.norm(second)
    if norm < 1.0e-10:
        raise ValueError("plane seeds are nearly parallel")
    return first, second / norm


def random_plane(
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    while True:
        first, second = rng.normal(size=(2, 5))
        try:
            return orthonormal_plane(first, second)
        except ValueError:
            continue


def regular_star(
    first: np.ndarray,
    second: np.ndarray,
    phase: float,
) -> np.ndarray:
    return np.asarray(
        [
            math.cos(phase + 4 * math.pi * index / 5) * first
            + math.sin(phase + 4 * math.pi * index / 5) * second
            for index in range(5)
        ]
    )


def tangent_perturb(
    array: np.ndarray,
    scale: float,
    rng: np.random.Generator,
) -> np.ndarray:
    if scale == 0:
        return array.copy()
    noise = rng.normal(size=array.shape)
    noise -= (
        np.sum(noise * array, axis=1)[:, None] * array
    )
    return normalized(array + scale * noise)


def old_warm_start() -> tuple[np.ndarray | None, dict[str, object]]:
    if not OLD_WARM.exists():
        return None, {"available": False}
    source_bytes = OLD_WARM.read_bytes()
    source = json.loads(source_bytes)
    full = np.asarray(
        source["runs"][0]["constrained_coordinates"], dtype=float
    )
    if full.shape != (41, 5):
        raise RuntimeError("old warm start has wrong shape")
    representatives = np.vstack((full[:18], full[36:41]))
    return normalized(representatives), {
        "available": True,
        "path": str(OLD_WARM.relative_to(ROOT)),
        "sha256": hashlib.sha256(source_bytes).hexdigest(),
    }


def make_initial(
    index: int,
    seed_base: int,
    warm: np.ndarray | None,
) -> tuple[np.ndarray, dict[str, object]]:
    seed = seed_base + index
    rng = np.random.default_rng(seed)
    family_index = index % 8
    lines = d5_lines()
    phase = float(rng.uniform(0, 2 * math.pi))
    record: dict[str, object] = {
        "index": index,
        "seed": seed,
    }

    if family_index in (0, 1, 2, 3):
        removed = np.sort(
            rng.choice(20, size=2, replace=False)
        )
        keep = np.ones(20, dtype=bool)
        keep[removed] = False
        u = lines[keep].copy()
        if family_index in (0, 1, 2):
            first, second = orthonormal_plane(
                lines[removed[0]], lines[removed[1]]
            )
            z = regular_star(first, second, phase)
            u_scale = (0.001, 0.025, 0.09)[family_index]
            z_scale = (0.002, 0.06, 0.20)[family_index]
            family = "d5_deleted_plane_star"
        else:
            first, second = random_plane(rng)
            z = regular_star(first, second, phase)
            u_scale = 0.045
            z_scale = 0.12
            family = "d5_independent_plane_star"
        u = tangent_perturb(u, u_scale, rng)
        z = tangent_perturb(z, z_scale, rng)
        record.update(
            {
                "family": family,
                "removed_d5_lines": removed.astype(int).tolist(),
                "u_noise_scale": u_scale,
                "z_noise_scale": z_scale,
            }
        )
    elif family_index == 4:
        removed = np.sort(
            rng.choice(20, size=2, replace=False)
        )
        keep = np.ones(20, dtype=bool)
        keep[removed] = False
        u = lines[keep].copy()
        # Replace two retained lines by greedily selected asymmetric
        # projective proposals.
        replaced = np.sort(rng.choice(18, size=2, replace=False))
        for location in replaced:
            other = np.delete(u, location, axis=0)
            proposals = normalized(rng.normal(size=(1200, 5)))
            coherence = np.max(
                np.abs(proposals @ other.T), axis=1
            )
            u[location] = proposals[int(np.argmin(coherence))]
        first, second = orthonormal_plane(
            lines[removed[0]], lines[removed[1]]
        )
        z = tangent_perturb(
            regular_star(first, second, phase), 0.10, rng
        )
        u = tangent_perturb(u, 0.02, rng)
        record.update(
            {
                "family": "d5_two_line_surgery",
                "removed_d5_lines": removed.astype(int).tolist(),
                "replaced_retained_locations": (
                    replaced.astype(int).tolist()
                ),
                "proposal_count_per_replacement": 1200,
            }
        )
    elif family_index in (5, 6):
        u = normalized(rng.normal(size=(18, 5)))
        first, second = random_plane(rng)
        z = regular_star(first, second, phase)
        z_scale = 0.08 if family_index == 5 else 0.30
        z = tangent_perturb(z, z_scale, rng)
        family = (
            "random_lines_near_star"
            if family_index == 5
            else "random_lines_broken_star"
        )
        record.update(
            {
                "family": family,
                "z_noise_scale": z_scale,
            }
        )
    else:
        if warm is None:
            u = normalized(rng.normal(size=(18, 5)))
            first, second = random_plane(rng)
            z = tangent_perturb(
                regular_star(first, second, phase), 0.16, rng
            )
            family = "warm_fallback_random"
            scale = None
        else:
            scale = float(rng.uniform(0.01, 0.22))
            perturbed = tangent_perturb(warm, scale, rng)
            u, z = perturbed[:18], perturbed[18:]
            family = "round2_warm_perturbation"
        record.update(
            {
                "family": family,
                "warm_noise_scale": scale,
            }
        )
    answer = normalized(np.vstack((u, z)))
    record["phase"] = phase
    return answer, record


def pair_indices() -> tuple[
    np.ndarray, np.ndarray, np.ndarray, np.ndarray, list[str]
]:
    absolute = []
    categories = []
    for first in range(18):
        for second in range(first + 1, 18):
            absolute.append((first, second))
            categories.append("line_line_absolute")
    for line in range(18):
        for residual in range(5):
            absolute.append((line, 18 + residual))
            categories.append("line_residual_absolute")
    for first in range(5):
        for second in range(first + 1, 5):
            consecutive = (
                (second - first) % 5 in (1, 4)
                or (first - second) % 5 in (1, 4)
            )
            if not consecutive:
                absolute.append((18 + first, 18 + second))
                categories.append("residual_noncycle_absolute")
    cycles = [
        (18 + index, 18 + ((index + 1) % 5))
        for index in range(5)
    ]
    absolute_array = np.asarray(absolute, dtype=int)
    cycle_array = np.asarray(cycles, dtype=int)
    if len(absolute_array) != 248 or len(cycle_array) != 5:
        raise RuntimeError("constraint indexing failed")
    return (
        absolute_array[:, 0],
        absolute_array[:, 1],
        cycle_array[:, 0],
        cycle_array[:, 1],
        categories,
    )


ABS_FIRST, ABS_SECOND, CYCLE_FIRST, CYCLE_SECOND, ABS_CATEGORIES = (
    pair_indices()
)


def q_polynomial(values: np.ndarray) -> np.ndarray:
    return (64 / 45) * values * values * (
        4 * values * values - 1
    )


def q_derivative(values: np.ndarray) -> np.ndarray:
    return (128 / 45) * values * (
        8 * values * values - 1
    )


def load_components(
    array: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    absolute_products = np.sum(
        array[..., ABS_FIRST, :] * array[..., ABS_SECOND, :],
        axis=-1,
    )
    cycle_products = np.sum(
        array[..., CYCLE_FIRST, :]
        * array[..., CYCLE_SECOND, :],
        axis=-1,
    )
    loads = np.concatenate(
        (
            absolute_products,
            -absolute_products,
            1 + cycle_products,
        ),
        axis=-1,
    )
    return loads, absolute_products, cycle_products


def true_common_load(array: np.ndarray) -> float:
    return float(np.max(load_components(array)[0]))


def light_diagnostics(array: np.ndarray) -> dict[str, object]:
    loads, absolute, cycles = load_components(array)
    return {
        "common_load": float(np.max(loads)),
        "maximum_absolute_constraint": float(
            np.max(np.abs(absolute))
        ),
        "maximum_cycle_product": float(np.max(cycles)),
        "minimum_cycle_product": float(np.min(cycles)),
        "residual_cycle_q_energy": float(
            np.sum(q_polynomial(cycles))
        ),
    }


def population_hard_scores(
    arrays: np.ndarray, q_weight: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    loads, _absolute, cycles = load_components(arrays)
    hard = np.max(loads, axis=1)
    energy = np.sum(q_polynomial(cycles), axis=1)
    if q_weight:
        guided = np.maximum(
            hard, 0.5 + q_weight * (Q_BOUND - energy)
        )
    else:
        guided = hard.copy()
    return hard, energy, guided


def population_loss_gradient(
    arrays: np.ndarray,
    beta: float,
    q_weight: float,
) -> tuple[np.ndarray, np.ndarray, dict[str, np.ndarray]]:
    loads, absolute_products, cycle_products = load_components(
        arrays
    )
    q_energy = np.sum(q_polynomial(cycle_products), axis=1)
    if q_weight:
        q_load = 0.5 + q_weight * (Q_BOUND - q_energy)
        loads = np.concatenate((loads, q_load[:, None]), axis=1)
    maximum = np.max(loads, axis=1)
    exponentials = np.exp(
        beta * (loads - maximum[:, None])
    )
    partition = np.sum(exponentials, axis=1)
    weights = exponentials / partition[:, None]
    losses = maximum + np.log(partition) / beta

    absolute_count = len(ABS_FIRST)
    absolute_coefficients = (
        weights[:, :absolute_count]
        - weights[
            :, absolute_count : 2 * absolute_count
        ]
    )
    cycle_coefficients = weights[
        :, 2 * absolute_count : 2 * absolute_count + 5
    ].copy()
    if q_weight:
        q_coefficients = weights[:, -1]
        cycle_coefficients -= (
            q_coefficients[:, None]
            * q_weight
            * q_derivative(cycle_products)
        )

    coefficient_matrix = np.zeros(
        (len(arrays), 23, 23), dtype=float
    )
    coefficient_matrix[:, ABS_FIRST, ABS_SECOND] = (
        absolute_coefficients
    )
    coefficient_matrix[:, ABS_SECOND, ABS_FIRST] = (
        absolute_coefficients
    )
    coefficient_matrix[:, CYCLE_FIRST, CYCLE_SECOND] = (
        cycle_coefficients
    )
    coefficient_matrix[:, CYCLE_SECOND, CYCLE_FIRST] = (
        cycle_coefficients
    )
    gradient = coefficient_matrix @ arrays
    gradient -= (
        np.sum(gradient * arrays, axis=2)[:, :, None]
        * arrays
    )
    return losses, gradient, {
        "hard_common_load": np.max(
            load_components(arrays)[0], axis=1
        ),
        "q_energy": q_energy,
        "guided_hard_load": np.max(loads, axis=1),
    }


def optimize_population(
    initial: np.ndarray,
    *,
    q_weight: float,
    scale: float,
    seed: int,
) -> tuple[np.ndarray, list[dict[str, object]]]:
    arrays = initial.copy()
    moment = np.zeros_like(arrays)
    square = np.zeros_like(arrays)
    best = arrays.copy()
    best_loads, _initial_energy, best_scores = (
        population_hard_scores(arrays, q_weight)
    )
    rng = np.random.default_rng(seed)
    schedule = [
        ("soft", int(450 * scale), 22.0, 0.013, 0.00025),
        ("medium", int(650 * scale), 65.0, 0.007, 0.00010),
        ("hard", int(850 * scale), 190.0, 0.0035, 0.00003),
        ("release", int(950 * scale), 560.0, 0.0017, 0.0),
        ("final", int(700 * scale), 1500.0, 0.00075, 0.0),
    ]
    history = []
    global_step = 0
    for phase, iterations, beta, learning_rate, noise_scale in schedule:
        phase_best_start = float(np.min(best_loads))
        for iteration in range(iterations):
            _loss, gradient, components = (
                population_loss_gradient(
                    arrays, beta=beta, q_weight=q_weight
                )
            )
            global_step += 1
            moment = 0.9 * moment + 0.1 * gradient
            square = 0.999 * square + 0.001 * gradient * gradient
            direction = (
                moment / (1 - 0.9**global_step)
            ) / (
                np.sqrt(
                    square / (1 - 0.999**global_step)
                )
                + 1.0e-8
            )
            direction -= (
                np.sum(direction * arrays, axis=2)[:, :, None]
                * arrays
            )
            if noise_scale:
                noise = rng.normal(size=arrays.shape)
                noise -= (
                    np.sum(noise * arrays, axis=2)[:, :, None]
                    * arrays
                )
                fraction = iteration / max(1, iterations - 1)
                noise_factor = noise_scale * (1 - fraction)
            else:
                noise = 0
                noise_factor = 0
            arrays = normalized(
                arrays
                - learning_rate * direction
                + noise_factor * noise
            )
            hard, _energy, scores = population_hard_scores(
                arrays, q_weight
            )
            improved = scores < best_scores
            best[improved] = arrays[improved]
            best_loads[improved] = hard[improved]
            best_scores[improved] = scores[improved]
        _, _, final_components = population_loss_gradient(
            arrays, beta=beta, q_weight=q_weight
        )
        history.append(
            {
                "phase": phase,
                "iterations": iterations,
                "beta": beta,
                "learning_rate": learning_rate,
                "q_weight": q_weight,
                "phase_best_start": phase_best_start,
                "best_common_load": float(np.min(best_loads)),
                "current_common_load_minimum": float(
                    np.min(
                        final_components["hard_common_load"]
                    )
                ),
                "current_q_energy_maximum": float(
                    np.max(final_components["q_energy"])
                ),
                "current_guided_load_minimum": float(
                    np.min(
                        final_components["guided_hard_load"]
                    )
                ),
            }
        )
    return best, history


def epigraph_refine(
    initial: np.ndarray,
    *,
    q_weight: float,
    maximum_iterations: int,
    hard_q_constraint: bool,
) -> tuple[np.ndarray, dict[str, object]]:
    initial = normalized(initial)
    initial_load = true_common_load(initial)
    variable0 = np.r_[initial.ravel(), initial_load + 1.0e-9]
    absolute_count = len(ABS_FIRST)

    def objective(variable: np.ndarray) -> float:
        return float(variable[-1])

    def objective_jac(variable: np.ndarray) -> np.ndarray:
        answer = np.zeros_like(variable)
        answer[-1] = 1
        return answer

    def norms(variable: np.ndarray) -> np.ndarray:
        array = variable[:-1].reshape(23, 5)
        return np.sum(array * array, axis=1) - 1

    def norms_jac(variable: np.ndarray) -> np.ndarray:
        array = variable[:-1].reshape(23, 5)
        answer = np.zeros((23, len(variable)))
        for index in range(23):
            answer[index, 5 * index : 5 * index + 5] = (
                2 * array[index]
            )
        return answer

    def inequalities(variable: np.ndarray) -> np.ndarray:
        array = variable[:-1].reshape(23, 5)
        loads, _absolute, cycles = load_components(array)
        if q_weight:
            energy = float(np.sum(q_polynomial(cycles)))
            loads = np.r_[
                loads,
                0.5 + q_weight * (Q_BOUND - energy),
            ]
        return variable[-1] - loads

    def inequalities_jac(variable: np.ndarray) -> np.ndarray:
        array = variable[:-1].reshape(23, 5)
        rows = 2 * absolute_count + 5 + int(bool(q_weight))
        answer = np.zeros((rows, len(variable)))
        answer[:, -1] = 1
        row = 0
        for first, second in zip(ABS_FIRST, ABS_SECOND):
            answer[row, 5 * first : 5 * first + 5] = -array[
                second
            ]
            answer[row, 5 * second : 5 * second + 5] = -array[
                first
            ]
            row += 1
        for first, second in zip(ABS_FIRST, ABS_SECOND):
            answer[row, 5 * first : 5 * first + 5] = array[
                second
            ]
            answer[row, 5 * second : 5 * second + 5] = array[
                first
            ]
            row += 1
        for first, second in zip(CYCLE_FIRST, CYCLE_SECOND):
            answer[row, 5 * first : 5 * first + 5] = -array[
                second
            ]
            answer[row, 5 * second : 5 * second + 5] = -array[
                first
            ]
            row += 1
        if q_weight:
            cycle_products = np.sum(
                array[CYCLE_FIRST] * array[CYCLE_SECOND],
                axis=1,
            )
            derivatives = q_derivative(cycle_products)
            for derivative, first, second in zip(
                derivatives, CYCLE_FIRST, CYCLE_SECOND
            ):
                answer[row, 5 * first : 5 * first + 5] += (
                    q_weight * derivative * array[second]
                )
                answer[row, 5 * second : 5 * second + 5] += (
                    q_weight * derivative * array[first]
                )
        return answer

    constraints: list[dict[str, object]] = [
        {
            "type": "eq",
            "fun": norms,
            "jac": norms_jac,
        },
        {
            "type": "ineq",
            "fun": inequalities,
            "jac": inequalities_jac,
        },
    ]
    if hard_q_constraint:
        def hard_q(variable: np.ndarray) -> np.ndarray:
            array = variable[:-1].reshape(23, 5)
            cycles = np.sum(
                array[CYCLE_FIRST] * array[CYCLE_SECOND],
                axis=1,
            )
            return np.asarray(
                [np.sum(q_polynomial(cycles)) - Q_BOUND]
            )

        def hard_q_jac(variable: np.ndarray) -> np.ndarray:
            array = variable[:-1].reshape(23, 5)
            cycles = np.sum(
                array[CYCLE_FIRST] * array[CYCLE_SECOND],
                axis=1,
            )
            answer = np.zeros((1, len(variable)))
            for derivative, first, second in zip(
                q_derivative(cycles),
                CYCLE_FIRST,
                CYCLE_SECOND,
            ):
                answer[0, 5 * first : 5 * first + 5] += (
                    derivative * array[second]
                )
                answer[0, 5 * second : 5 * second + 5] += (
                    derivative * array[first]
                )
            return answer

        constraints.append(
            {
                "type": "ineq",
                "fun": hard_q,
                "jac": hard_q_jac,
            }
        )

    result = minimize(
        objective,
        variable0,
        jac=objective_jac,
        constraints=constraints,
        method="SLSQP",
        options={
            "maxiter": maximum_iterations,
            "ftol": 2.0e-13,
            "disp": False,
        },
    )
    answer = normalized(result.x[:-1].reshape(23, 5))
    loads, _absolute, cycles = load_components(answer)
    q_energy = float(np.sum(q_polynomial(cycles)))
    return answer, {
        "success": bool(result.success),
        "status": int(result.status),
        "message": str(result.message),
        "iterations": int(result.nit),
        "reported_epigraph": float(result.x[-1]),
        "recomputed_common_load": float(np.max(loads)),
        "q_weight": q_weight,
        "hard_q_constraint": hard_q_constraint,
        "recomputed_q_energy": q_energy,
        "hard_q_constraint_residual": q_energy - Q_BOUND,
    }


def full_code(array: np.ndarray) -> np.ndarray:
    return np.vstack((array[:18], -array[:18], array[18:]))


def coordinate_hash(array: np.ndarray) -> str:
    canonical = np.asarray(array, dtype="<f8", order="C")
    return hashlib.sha256(canonical.tobytes()).hexdigest()


def q_scalar(value: float) -> float:
    return (64 / 45) * value * value * (
        4 * value * value - 1
    )


def exact_dot(
    array: np.ndarray, first: int, second: int
) -> Fraction:
    return sum(
        Fraction.from_float(float(array[first, coordinate]))
        * Fraction.from_float(float(array[second, coordinate]))
        for coordinate in range(5)
    )


def exact_q(value: Fraction) -> Fraction:
    return (
        Fraction(64, 45)
        * value
        * value
        * (4 * value * value - 1)
    )


def exact_common_load(
    array: np.ndarray,
) -> tuple[Fraction, dict[str, object]]:
    best: Fraction | None = None
    witness: dict[str, object] = {}
    for index, (first, second) in enumerate(
        zip(ABS_FIRST, ABS_SECOND)
    ):
        product = exact_dot(array, int(first), int(second))
        load = abs(product)
        if best is None or load > best:
            best = load
            witness = {
                "type": ABS_CATEGORIES[index],
                "vertices": [int(first), int(second)],
                "absolute_value": True,
                "dot_numerator": str(product.numerator),
                "dot_denominator": str(product.denominator),
            }
    for cycle, (first, second) in enumerate(
        zip(CYCLE_FIRST, CYCLE_SECOND)
    ):
        product = exact_dot(array, int(first), int(second))
        load = 1 + product
        if best is None or load > best:
            best = load
            witness = {
                "type": "residual_cycle_one_plus_dot",
                "cycle_index": cycle,
                "vertices": [int(first), int(second)],
                "absolute_value": False,
                "dot_numerator": str(product.numerator),
                "dot_denominator": str(product.denominator),
            }
    assert best is not None
    witness["load_numerator"] = str(best.numerator)
    witness["load_denominator"] = str(best.denominator)
    return best, witness


def diagnostics(
    array: np.ndarray, active_tolerance: float = 1.0e-7
) -> dict[str, object]:
    array = normalized(array)
    loads, absolute_products, cycle_products = load_components(
        array
    )
    common_load = float(np.max(loads))
    exact_load, exact_witness = exact_common_load(array)
    full = full_code(array)
    gram = full @ full.T
    eigenvalues = np.linalg.eigvalsh(gram)
    noncycle_products = absolute_products[-5:]
    categories = (
        ABS_CATEGORIES
        + ABS_CATEGORIES
        + ["residual_cycle_one_plus_dot"] * 5
    )
    active_counts: dict[str, int] = {}
    for category, load in zip(categories, loads):
        if load >= common_load - active_tolerance:
            active_counts[category] = (
                active_counts.get(category, 0) + 1
            )
    q_cycle = float(np.sum(q_polynomial(cycle_products)))
    full_first, full_second = np.triu_indices(41, 1)
    full_products = gram[full_first, full_second]
    full_q_unordered = float(
        np.sum(q_polynomial(full_products))
    )
    exact_cycle_q = sum(
        exact_q(exact_dot(array, int(first), int(second)))
        for first, second in zip(CYCLE_FIRST, CYCLE_SECOND)
    )
    exact_full_q_unordered = sum(
        exact_q(exact_dot(full, int(first), int(second)))
        for first, second in zip(full_first, full_second)
    )
    intended = bool(
        np.max(np.abs(absolute_products)) <= 0.5
        and np.max(cycle_products) < -0.5
    )
    return {
        "common_load": common_load,
        "worst_violation_above_one_half": common_load - 0.5,
        "maximum_line_line_absolute": float(
            np.max(np.abs(absolute_products[:153]))
        ),
        "maximum_line_residual_absolute": float(
            np.max(np.abs(absolute_products[153:243]))
        ),
        "maximum_residual_noncycle_absolute": float(
            np.max(np.abs(noncycle_products))
        ),
        "residual_cycle_products": cycle_products.tolist(),
        "minimum_strict_cycle_margin": float(
            np.min(-0.5 - cycle_products)
        ),
        "residual_cycle_q_energy": q_cycle,
        "exact_binary64_residual_cycle_q_energy": {
            "numerator": str(exact_cycle_q.numerator),
            "denominator": str(exact_cycle_q.denominator),
            "decimal_18_digits": f"{float(exact_cycle_q):.18f}",
        },
        "residual_cycle_q_energy_bound": Q_BOUND,
        "residual_cycle_q_energy_excess": q_cycle - Q_BOUND,
        "full_unordered_q_energy": full_q_unordered,
        "exact_binary64_full_unordered_q_energy": {
            "numerator": str(exact_full_q_unordered.numerator),
            "denominator": str(exact_full_q_unordered.denominator),
            "decimal_18_digits": (
                f"{float(exact_full_q_unordered):.18f}"
            ),
        },
        "full_ordered_q_energy": 2 * full_q_unordered,
        "full_ordered_q_energy_lower_bound": 10496 / 63,
        "active_tolerance": active_tolerance,
        "active_constraint_count": int(
            np.count_nonzero(loads >= common_load - active_tolerance)
        ),
        "active_category_counts": active_counts,
        "intended_branch_realized_binary64": intended,
        "unit_norm_maximum_residual": float(
            np.max(
                np.abs(np.sum(array * array, axis=1) - 1)
            )
        ),
        "representative_gram_eigenvalues": (
            np.linalg.eigvalsh(array @ array.T).tolist()
        ),
        "full_gram_eigenvalues": eigenvalues.tolist(),
        "full_gram_largest_null_eigenvalue_absolute": float(
            np.max(np.abs(eigenvalues[:-5]))
        ),
        "full_gram_nonzero_eigenvalues": eigenvalues[-5:].tolist(),
        "residual_centroid_norm": float(
            np.linalg.norm(np.sum(array[18:], axis=0))
        ),
        "representative_coordinate_sha256": coordinate_hash(array),
        "full_coordinate_sha256": coordinate_hash(full),
        "exact_binary64_common_load": {
            "numerator": str(exact_load.numerator),
            "denominator": str(exact_load.denominator),
            "decimal_18_digits": f"{float(exact_load):.18f}",
            "witness": exact_witness,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--population", type=int, default=64)
    parser.add_argument("--seed-base", type=int, default=2026080100)
    parser.add_argument("--scale", type=float, default=1.0)
    parser.add_argument("--q-weight", type=float, default=0.16)
    parser.add_argument("--polish-count", type=int, default=14)
    parser.add_argument("--hard-q-count", type=int, default=10)
    parser.add_argument("--epigraph-maxiter", type=int, default=1600)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    started = time.time()
    warm, warm_record = old_warm_start()
    initials = []
    initial_records = []
    for index in range(args.population):
        array, record = make_initial(
            index, args.seed_base, warm
        )
        record["initial_diagnostics"] = light_diagnostics(array)
        initials.append(array)
        initial_records.append(record)
    initial_population = np.asarray(initials)

    unguided, unguided_history = optimize_population(
        initial_population,
        q_weight=0.0,
        scale=args.scale,
        seed=args.seed_base + 100000,
    )
    guided, guided_history = optimize_population(
        initial_population,
        q_weight=args.q_weight,
        scale=args.scale,
        seed=args.seed_base + 200000,
    )

    candidates = []
    for kind, population in (
        ("unguided", unguided),
        ("q_guided", guided),
    ):
        for index, array in enumerate(population):
            candidates.append(
                {
                    "kind": kind,
                    "initial_index": index,
                    "array": array,
                    "load": true_common_load(array),
                }
            )
    candidates.sort(key=lambda record: record["load"])
    selected = candidates[: args.polish_count]
    polished_records = []
    for selection_index, candidate in enumerate(selected):
        polished, solver = epigraph_refine(
            candidate["array"],
            q_weight=(
                args.q_weight
                if candidate["kind"] == "q_guided"
                else 0.0
            ),
            maximum_iterations=args.epigraph_maxiter,
            hard_q_constraint=False,
        )
        if true_common_load(polished) <= candidate["load"]:
            retained = polished
            retained_from = "slsqp"
        else:
            retained = candidate["array"]
            retained_from = "population"
        record = {
            "selection_index": selection_index,
            "kind": candidate["kind"],
            "initial_index": candidate["initial_index"],
            "initial_family": initial_records[
                candidate["initial_index"]
            ]["family"],
            "population_diagnostics": diagnostics(
                candidate["array"]
            ),
            "solver": solver,
            "retained_from": retained_from,
            "retained": {
                **diagnostics(retained),
                "coordinates_float64": retained.tolist(),
            },
        }
        print(
            f"polish {selection_index:02d} {candidate['kind']} "
            f"family={record['initial_family']} "
            f"population={candidate['load']:.12f} "
            f"retained={record['retained']['common_load']:.12f} "
            f"q={record['retained']['residual_cycle_q_energy']:.6f}",
            flush=True,
        )
        polished_records.append(record)

    hard_sources = sorted(
        (
            {
                "kind": kind,
                "initial_index": index,
                "array": array,
                "energy": light_diagnostics(array)[
                    "residual_cycle_q_energy"
                ],
                "load": true_common_load(array),
            }
            for kind, population in (
                ("unguided", unguided),
                ("q_guided", guided),
            )
            for index, array in enumerate(population)
        ),
        key=lambda record: (
            record["energy"] < Q_BOUND,
            record["load"]
            + 0.03 * max(0, Q_BOUND - record["energy"]),
        ),
    )[: args.hard_q_count]
    hard_q_records = []
    for selection_index, candidate in enumerate(hard_sources):
        polished, solver = epigraph_refine(
            candidate["array"],
            q_weight=0.0,
            maximum_iterations=args.epigraph_maxiter,
            hard_q_constraint=True,
        )
        retained_diagnostics = diagnostics(polished)
        record = {
            "selection_index": selection_index,
            "kind": candidate["kind"],
            "initial_index": candidate["initial_index"],
            "initial_family": initial_records[
                candidate["initial_index"]
            ]["family"],
            "source_common_load": candidate["load"],
            "source_q_energy": candidate["energy"],
            "solver": solver,
            "retained": {
                **retained_diagnostics,
                "coordinates_float64": polished.tolist(),
            },
            "hard_q_constraint_satisfied_at_1e-9": (
                retained_diagnostics[
                    "residual_cycle_q_energy_excess"
                ]
                >= -1.0e-9
            ),
        }
        print(
            f"hard-q {selection_index:02d} {candidate['kind']} "
            f"family={record['initial_family']} "
            f"load={record['retained']['common_load']:.12f} "
            f"q={record['retained']['residual_cycle_q_energy']:.6f} "
            f"success={solver['success']}",
            flush=True,
        )
        hard_q_records.append(record)

    best = min(
        polished_records,
        key=lambda record: record["retained"]["common_load"],
    )
    hard_feasible = [
        record
        for record in hard_q_records
        if record["hard_q_constraint_satisfied_at_1e-9"]
    ]
    best_hard = (
        min(
            hard_feasible,
            key=lambda record: record["retained"][
                "common_load"
            ],
        )
        if hard_feasible
        else None
    )
    try:
        output_label = str(args.output.relative_to(ROOT))
    except ValueError:
        output_label = str(args.output)
    output = {
        "schema": "kissing5.construction_r18_c5_branch.v1",
        "evidence_status": (
            "NUMERICAL EVIDENCE ONLY; NOT AN EXACT CONFIGURATION "
            "OR NONEXISTENCE CERTIFICATE"
        ),
        "constraint_definition": {
            "projective_direction_count": 18,
            "residual_count": 5,
            "absolute_constraint_count": 248,
            "cycle_constraint_count": 5,
            "common_load": (
                "max(|u.u|, |u.z|, |noncycle z.z|, "
                "1+cycle z.z)"
            ),
            "realization_condition": (
                "common_load<=1/2 and every cycle product<-1/2"
            ),
            "q_polynomial": "(64/45)*t^2*(4*t^2-1)",
            "residual_cycle_q_energy_lower_bound": "64/9",
        },
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
        },
        "parameters": {
            **vars(args),
            "output": output_label,
        },
        "warm_source": warm_record,
        "initial_records": initial_records,
        "unguided_history": unguided_history,
        "q_guided_history": guided_history,
        "polished_records": polished_records,
        "hard_q_records": hard_q_records,
        "best": {
            "selection_index": best["selection_index"],
            "kind": best["kind"],
            "initial_index": best["initial_index"],
            "initial_family": best["initial_family"],
            "common_load": best["retained"]["common_load"],
            "coordinate_sha256": best["retained"][
                "representative_coordinate_sha256"
            ],
        },
        "best_hard_q": (
            None
            if best_hard is None
            else {
                "selection_index": best_hard["selection_index"],
                "kind": best_hard["kind"],
                "initial_index": best_hard["initial_index"],
                "initial_family": best_hard["initial_family"],
                "common_load": best_hard["retained"][
                    "common_load"
                ],
                "q_energy": best_hard["retained"][
                    "residual_cycle_q_energy"
                ],
                "coordinate_sha256": best_hard["retained"][
                    "representative_coordinate_sha256"
                ],
            }
        ),
        "branch_realized_binary64": any(
            record["retained"][
                "intended_branch_realized_binary64"
            ]
            for record in polished_records + hard_q_records
        ),
        "elapsed_seconds": time.time() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n")
    print(
        "best",
        output["best"],
        "best_hard_q",
        output["best_hard_q"],
        "realized",
        output["branch_realized_binary64"],
    )


if __name__ == "__main__":
    main()
