#!/usr/bin/env python3
"""Latitude-layer, cross-basin, and cardinality-changing searches in S^4.

This is discovery code only.  It attacks N=41,...,44 without assuming that a
successful code is antipodal, rigid, or related to D5.  Three macro moves are
used:

1. tied-latitude populations whose layers carry independently rotated and
   perturbed S^3 subcodes;
2. latitude-block crossover between the four exact 40-point sources and
   unrelated layer/random basins;
3. remove-k/add-(k+1) surgery, for every k=2,...,6, with the deleted points
   selected by sampled insertion-hole blockers.

Every structured candidate is released to the full product (S^4)^N before it
is compared.  The output is numerical evidence, never an exact certificate.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import platform
import sys
import time

import numpy as np
import scipy
from scipy.optimize import linear_sum_assignment, minimize


STATUS = "NUMERICAL EVIDENCE ONLY — NOT A CONSTRUCTION CERTIFICATE"
DIMENSION = 5
LAYER_DIMENSION = 4


def unit_rows(array: np.ndarray) -> np.ndarray:
    x = np.asarray(array, dtype=np.float64)
    if x.ndim != 2 or x.shape[1] not in (LAYER_DIMENSION, DIMENSION):
        raise ValueError("coordinates have the wrong shape")
    norms = np.sqrt(np.sum(x * x, axis=1))
    if float(np.min(norms)) < 1e-14:
        raise ValueError("zero coordinate row")
    return np.ascontiguousarray(x / norms[:, None])


def pair_indices(n: int) -> tuple[np.ndarray, np.ndarray]:
    return np.triu_indices(n, 1)


def pair_values(x: np.ndarray) -> np.ndarray:
    x = unit_rows(x)
    first, second = pair_indices(len(x))
    return np.sum(x[first] * x[second], axis=1)


def max_inner(x: np.ndarray) -> float:
    return float(np.max(pair_values(x)))


def random_orthogonal(
    dimension: int, rng: np.random.Generator
) -> np.ndarray:
    q, r = np.linalg.qr(rng.normal(size=(dimension, dimension)))
    q *= np.sign(np.diag(r))[None, :]
    if np.linalg.det(q) < 0:
        q[:, 0] *= -1
    return q


def exact_known_codes() -> dict[str, tuple[tuple[Fraction, ...], ...]]:
    """Return unnormalized exact rows for D5, L5, Q5, and R5."""
    d5 = []
    for first, second in itertools.combinations(range(5), 2):
        for sign_first in (-1, 1):
            for sign_second in (-1, 1):
                row = [Fraction(0)] * 5
                row[first] = Fraction(sign_first)
                row[second] = Fraction(sign_second)
                d5.append(tuple(row))
    l5 = [row for row in d5 if row[4] != 1]
    l5 += [
        tuple(Fraction(sign, 2) for sign in signs) + (Fraction(1),)
        for signs in itertools.product((-1, 1), repeat=4)
        if sum(sign < 0 for sign in signs) % 2 == 1
    ]
    q5 = [row for row in d5 if sum(row) != 2]
    q5 += [
        tuple(value + Fraction(4, 5) for value in row)
        for row in d5
        if sum(row) == -2
    ]
    r5 = [row for row in l5 if sum(row) != 2]
    r5 += [
        tuple(value + Fraction(4, 5) for value in row)
        for row in l5
        if sum(row) == -2
    ]
    answer = {"D5": tuple(d5), "L5": tuple(l5), "Q5": tuple(q5), "R5": tuple(r5)}
    if any(len(code) != 40 or len(set(code)) != 40 for code in answer.values()):
        raise AssertionError("known-code generator failed")
    return answer


def floating_known_codes() -> dict[str, np.ndarray]:
    return {
        name: unit_rows(np.asarray(code, dtype=np.float64))
        for name, code in exact_known_codes().items()
    }


def logsumexp_pair_objective(
    flat: np.ndarray, n: int, dimension: int, beta: float
) -> tuple[float, np.ndarray]:
    """Smooth maximum of pair inner products, with exact analytic gradient."""
    raw = np.asarray(flat, dtype=np.float64).reshape(n, dimension)
    norms = np.sqrt(np.sum(raw * raw, axis=1))
    if float(np.min(norms)) < 1e-13:
        return 1e20, np.zeros_like(flat)
    x = raw / norms[:, None]
    first, second = pair_indices(n)
    values = np.sum(x[first] * x[second], axis=1)
    scaled = beta * values
    shift = float(np.max(scaled))
    exponential = np.exp(scaled - shift)
    weights = exponential / float(np.sum(exponential))
    value = (shift + math.log(float(np.sum(exponential)))) / beta
    ambient = np.zeros_like(x)
    np.add.at(ambient, first, weights[:, None] * x[second])
    np.add.at(ambient, second, weights[:, None] * x[first])
    tangent = ambient - np.sum(ambient * x, axis=1)[:, None] * x
    gradient = tangent / norms[:, None]
    return float(value), gradient.ravel()


def relax_full(
    initial: np.ndarray,
    betas: tuple[float, ...],
    max_iterations: int,
) -> tuple[np.ndarray, list[dict]]:
    x = unit_rows(initial)
    history = []
    for beta in betas:
        result = minimize(
            logsumexp_pair_objective,
            x.ravel(),
            args=(len(x), x.shape[1], float(beta)),
            jac=True,
            method="L-BFGS-B",
            options={
                "maxiter": int(max_iterations),
                "ftol": 2e-15,
                "gtol": 2e-10,
                "maxcor": 35,
                "maxls": 60,
            },
        )
        x = unit_rows(result.x.reshape(x.shape))
        history.append(
            {
                "beta": float(beta),
                "iterations": int(result.nit),
                "evaluations": int(result.nfev),
                "success": bool(result.success),
                "message": str(result.message),
                "surrogate": float(result.fun),
                "maximum": max_inner(x),
            }
        )
    return x, history


def epigraph_polish(
    initial: np.ndarray, max_iterations: int
) -> tuple[np.ndarray, dict]:
    """Directly minimize the literal maximum by a constrained epigraph solve.

    This is a final basin-settling step, not a macro search mechanism.  All
    pair constraints and all unit-norm equalities are present explicitly.
    """
    x = unit_rows(initial)
    n = len(x)
    first, second = pair_indices(n)
    variables = np.r_[x.ravel(), max_inner(x)]

    def objective(value: np.ndarray) -> float:
        return float(value[-1])

    def objective_jacobian(value: np.ndarray) -> np.ndarray:
        answer = np.zeros_like(value)
        answer[-1] = 1.0
        return answer

    def inequalities(value: np.ndarray) -> np.ndarray:
        points = value[:-1].reshape(n, 5)
        return value[-1] - np.sum(points[first] * points[second], axis=1)

    def inequality_jacobian(value: np.ndarray) -> np.ndarray:
        points = value[:-1].reshape(n, 5)
        answer = np.zeros((len(first), len(value)))
        rows = np.arange(len(first))
        for coordinate in range(5):
            answer[rows, 5 * first + coordinate] = -points[second, coordinate]
            answer[rows, 5 * second + coordinate] = -points[first, coordinate]
        answer[:, -1] = 1.0
        return answer

    def equalities(value: np.ndarray) -> np.ndarray:
        points = value[:-1].reshape(n, 5)
        return np.sum(points * points, axis=1) - 1.0

    def equality_jacobian(value: np.ndarray) -> np.ndarray:
        points = value[:-1].reshape(n, 5)
        answer = np.zeros((n, len(value)))
        rows = np.arange(n)
        for coordinate in range(5):
            answer[rows, 5 * rows + coordinate] = 2.0 * points[:, coordinate]
        return answer

    result = minimize(
        objective,
        variables,
        jac=objective_jacobian,
        constraints=[
            {
                "type": "ineq",
                "fun": inequalities,
                "jac": inequality_jacobian,
            },
            {
                "type": "eq",
                "fun": equalities,
                "jac": equality_jacobian,
            },
        ],
        method="SLSQP",
        options={
            "maxiter": int(max_iterations),
            "ftol": 2e-13,
            "disp": False,
        },
    )
    answer = unit_rows(result.x[:-1].reshape(n, 5))
    return answer, {
        "success": bool(result.success),
        "status": int(result.status),
        "message": str(result.message),
        "iterations": int(result.nit),
        "evaluations": int(result.nfev),
        "reported_epigraph": float(result.x[-1]),
        "recomputed_maximum": max_inner(answer),
        "minimum_reported_pair_slack": float(np.min(inequalities(result.x))),
        "maximum_norm_residual": float(np.max(np.abs(equalities(result.x)))),
    }


def d4_roots() -> np.ndarray:
    rows = []
    for first, second in itertools.combinations(range(4), 2):
        for sign_first in (-1.0, 1.0):
            for sign_second in (-1.0, 1.0):
                row = np.zeros(4)
                row[first] = sign_first
                row[second] = sign_second
                rows.append(row)
    return unit_rows(np.asarray(rows))


def hypercube4() -> np.ndarray:
    return unit_rows(np.asarray(list(itertools.product((-1.0, 1.0), repeat=4))))


def cross_polytope4() -> np.ndarray:
    return np.vstack([np.eye(4), -np.eye(4)])


def regular_simplex4() -> np.ndarray:
    matrix = np.eye(5) - np.ones((5, 5)) / 5.0
    values, vectors = np.linalg.eigh(matrix)
    return unit_rows(vectors[:, values > 0.5])


def choose_template(
    size: int, rng: np.random.Generator, template_cache: dict[int, list[np.ndarray]]
) -> tuple[np.ndarray, str]:
    choices: list[tuple[np.ndarray, str]] = []
    for source, name in (
        (d4_roots(), "D4_subset"),
        (hypercube4(), "hypercube_subset"),
        (cross_polytope4(), "cross_polytope_subset"),
        (regular_simplex4(), "simplex_augmented"),
    ):
        if len(source) >= size:
            indices = rng.choice(len(source), size=size, replace=False)
            choices.append((source[indices], name))
    if size in template_cache and template_cache[size]:
        cached = template_cache[size][int(rng.integers(len(template_cache[size])))]
        choices.append((cached, "optimized_random_S3"))
    if choices:
        base, name = choices[int(rng.integers(len(choices)))]
        base = np.array(base, copy=True)
    else:
        base = unit_rows(rng.normal(size=(size, 4)))
        name = "random_S3"
    rotation = random_orthogonal(4, rng)
    base = unit_rows(base @ rotation)
    noise = rng.normal(size=base.shape)
    noise -= np.sum(noise * base, axis=1)[:, None] * base
    return unit_rows(base + rng.uniform(0.005, 0.08) * noise), name


def build_template_cache(
    sizes: set[int], rng: np.random.Generator, max_iterations: int
) -> dict[int, list[np.ndarray]]:
    cache: dict[int, list[np.ndarray]] = {}
    for size in sorted(sizes):
        cache[size] = []
        for _ in range(2):
            initial = unit_rows(rng.normal(size=(size, 4)))
            if size == 1:
                optimized = initial
            else:
                optimized, _ = relax_full(
                    initial, (12.0, 24.0, 48.0, 96.0), max_iterations
                )
            cache[size].append(optimized)
    return cache


def balanced_partition(n: int, layers: int, offset: int = 0) -> tuple[int, ...]:
    sizes = [n // layers] * layers
    for index in range(n % layers):
        sizes[(index + offset) % layers] += 1
    return tuple(sizes)


def random_partition(
    n: int, layers: int, minimum: int, rng: np.random.Generator
) -> tuple[int, ...]:
    if n < minimum * layers:
        raise ValueError("partition minimum is impossible")
    sizes = np.full(layers, minimum, dtype=int)
    for _ in range(n - minimum * layers):
        sizes[int(rng.integers(layers))] += 1
    rng.shuffle(sizes)
    return tuple(int(value) for value in sizes)


def unbalanced_partition(
    n: int, layers: int, minimum: int, rng: np.random.Generator
) -> tuple[int, ...]:
    """Dirichlet allocation that deliberately includes small polar layers."""
    if n < minimum * layers:
        raise ValueError("partition minimum is impossible")
    remaining = n - minimum * layers
    weights = rng.dirichlet(np.full(layers, 0.55))
    extra = rng.multinomial(remaining, weights)
    sizes = extra + minimum
    rng.shuffle(sizes)
    return tuple(int(value) for value in sizes)


@dataclass
class LayerEncoding:
    sizes: tuple[int, ...]
    membership: np.ndarray

    @classmethod
    def from_sizes(cls, sizes: tuple[int, ...]) -> "LayerEncoding":
        membership = np.concatenate(
            [np.full(size, layer, dtype=int) for layer, size in enumerate(sizes)]
        )
        return cls(sizes=sizes, membership=membership)


def unpack_layer_variables(
    variables: np.ndarray, encoding: LayerEncoding
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    layers = len(encoding.sizes)
    n = int(np.sum(encoding.sizes))
    heights = np.asarray(variables[:layers], dtype=np.float64)
    raw = np.asarray(variables[layers:], dtype=np.float64).reshape(n, 4)
    norms = np.sqrt(np.sum(raw * raw, axis=1))
    directions = raw / norms[:, None]
    point_heights = heights[encoding.membership]
    radii = np.sqrt(np.maximum(1.0 - point_heights * point_heights, 1e-15))
    x = np.column_stack([radii[:, None] * directions, point_heights])
    return x, directions, norms


def layer_objective(
    variables: np.ndarray, encoding: LayerEncoding, beta: float
) -> tuple[float, np.ndarray]:
    x, directions, norms = unpack_layer_variables(variables, encoding)
    first, second = pair_indices(len(x))
    values = np.sum(x[first] * x[second], axis=1)
    scaled = beta * values
    shift = float(np.max(scaled))
    exponential = np.exp(scaled - shift)
    weights = exponential / float(np.sum(exponential))
    value = (shift + math.log(float(np.sum(exponential)))) / beta
    ambient = np.zeros_like(x)
    np.add.at(ambient, first, weights[:, None] * x[second])
    np.add.at(ambient, second, weights[:, None] * x[first])

    layers = len(encoding.sizes)
    heights = variables[:layers]
    point_heights = heights[encoding.membership]
    radii = np.sqrt(np.maximum(1.0 - point_heights * point_heights, 1e-15))
    first4 = ambient[:, :4]
    directional_dot = np.sum(first4 * directions, axis=1)
    grad_raw = (
        radii[:, None]
        * (first4 - directional_dot[:, None] * directions)
        / norms[:, None]
    )
    grad_height_points = ambient[:, 4] - (
        point_heights / radii
    ) * directional_dot
    grad_heights = np.zeros(layers)
    np.add.at(grad_heights, encoding.membership, grad_height_points)
    gradient = np.r_[grad_heights, grad_raw.ravel()]
    return float(value), gradient


def layer_start(
    sizes: tuple[int, ...],
    rng: np.random.Generator,
    template_cache: dict[int, list[np.ndarray]],
) -> tuple[np.ndarray, dict]:
    layers = len(sizes)
    encoding = LayerEncoding.from_sizes(sizes)
    # Nonuniform spacings and a random common shift avoid imposed reflection.
    heights = np.linspace(-0.78, 0.78, layers)
    heights += rng.normal(scale=0.09, size=layers)
    heights += rng.uniform(-0.12, 0.12)
    heights = np.clip(heights, -0.90, 0.90)
    directions = []
    template_names = []
    for size in sizes:
        block, name = choose_template(size, rng, template_cache)
        directions.append(block)
        template_names.append(name)
    variables = np.r_[heights, np.vstack(directions).ravel()]
    x, _, _ = unpack_layer_variables(variables, encoding)
    return variables, {
        "sizes": list(sizes),
        "initial_heights": heights.tolist(),
        "templates": template_names,
        "initial_maximum": max_inner(x),
    }


def rotate_axis_last(axis: np.ndarray) -> np.ndarray:
    axis = np.asarray(axis, dtype=np.float64)
    axis /= np.linalg.norm(axis)
    _, _, vh = np.linalg.svd(axis.reshape(1, 5), full_matrices=True)
    complement = vh[1:].T
    rotation = np.column_stack([complement, axis])
    if abs(abs(np.linalg.det(rotation)) - 1.0) > 1e-11:
        raise AssertionError("axis frame is not orthogonal")
    return rotation


def source_layer_insertion_start(
    source: np.ndarray,
    target: int,
    axis: np.ndarray,
    rng: np.random.Generator,
    probe_count: int,
) -> tuple[np.ndarray, tuple[int, ...], dict]:
    """Insert points while retaining a source's exact latitude decomposition."""
    source = unit_rows(source)
    rotation = rotate_axis_last(axis)
    rotated = source @ rotation
    heights = rotated[:, 4]
    representatives: list[float] = []
    groups: list[list[int]] = []
    for index in np.argsort(heights):
        value = float(heights[index])
        placed = False
        for group_index, representative in enumerate(representatives):
            if abs(value - representative) <= 2e-10:
                groups[group_index].append(int(index))
                placed = True
                break
        if not placed:
            representatives.append(value)
            groups.append([int(index)])
    order = np.argsort(representatives)
    representatives = [representatives[int(i)] for i in order]
    groups = [groups[int(i)] for i in order]
    blocks = [rotated[np.asarray(group)] for group in groups]
    assignments = []
    for addition in range(target - len(source)):
        best = None
        best_value = math.inf
        best_layer = None
        # Inspect every inherited layer and also two new nonsymmetric
        # latitudes.  Probe directions are unrestricted in S^3.
        candidate_heights = list(representatives)
        candidate_heights.extend(
            [
                float(rng.uniform(-0.88, 0.88)),
                float(rng.uniform(-0.88, 0.88)),
            ]
        )
        probes = unit_rows(rng.normal(size=(probe_count, 4)))
        current = np.vstack(blocks)
        for layer_index, height in enumerate(candidate_heights):
            radius = math.sqrt(max(1.0 - height * height, 1e-15))
            candidates = np.column_stack(
                [radius * probes, np.full(probe_count, height)]
            )
            scores = np.max(candidates @ current.T, axis=1)
            chosen = int(np.argmin(scores))
            if float(scores[chosen]) < best_value:
                best_value = float(scores[chosen])
                best = candidates[chosen]
                best_layer = int(layer_index)
        assert best is not None and best_layer is not None
        if best_layer >= len(blocks):
            representatives.append(float(best[4]))
            groups.append([])
            blocks.append(best[None, :])
        else:
            blocks[best_layer] = np.vstack([blocks[best_layer], best])
        assignments.append(
            {
                "addition": int(addition),
                "layer": int(best_layer),
                "height": float(best[4]),
                "sampled_fixed_maximum": best_value,
            }
        )
    # Sort layers after adding possible new heights, and express every row as
    # a direction in S^3 plus its tied height.
    final_order = np.argsort([float(block[0, 4]) for block in blocks])
    blocks = [blocks[int(i)] for i in final_order]
    final_heights = [float(block[0, 4]) for block in blocks]
    directions = []
    for block, height in zip(blocks, final_heights):
        radius = math.sqrt(max(1.0 - height * height, 1e-15))
        directions.append(unit_rows(block[:, :4] / radius))
    sizes = tuple(len(block) for block in blocks)
    variables = np.r_[final_heights, np.vstack(directions).ravel()]
    encoding = LayerEncoding.from_sizes(sizes)
    built, _, _ = unpack_layer_variables(variables, encoding)
    return variables, sizes, {
        "inherited_layer_sizes_before_addition": [
            int(len(group)) for group in groups[: len(representatives)]
        ],
        "final_sizes": list(sizes),
        "final_initial_heights": final_heights,
        "assignments": assignments,
        "initial_maximum": max_inner(built),
    }


def optimize_layers(
    variables: np.ndarray,
    sizes: tuple[int, ...],
    betas: tuple[float, ...],
    max_iterations: int,
) -> tuple[np.ndarray, list[dict], list[float]]:
    encoding = LayerEncoding.from_sizes(sizes)
    layers = len(sizes)
    current = np.array(variables, copy=True)
    history = []
    bounds = [(-0.94, 0.94)] * layers + [(None, None)] * (
        len(current) - layers
    )
    for beta in betas:
        result = minimize(
            layer_objective,
            current,
            args=(encoding, float(beta)),
            jac=True,
            method="L-BFGS-B",
            bounds=bounds,
            options={
                "maxiter": int(max_iterations),
                "ftol": 2e-15,
                "gtol": 2e-10,
                "maxcor": 35,
                "maxls": 60,
            },
        )
        current = result.x
        x, _, _ = unpack_layer_variables(current, encoding)
        history.append(
            {
                "beta": float(beta),
                "iterations": int(result.nit),
                "success": bool(result.success),
                "message": str(result.message),
                "maximum": max_inner(x),
                "surrogate": float(result.fun),
            }
        )
    x, _, _ = unpack_layer_variables(current, encoding)
    return unit_rows(x), history, current[:layers].tolist()


def align_parent(reference: np.ndarray, moving: np.ndarray) -> np.ndarray:
    """Alternating assignment/Procrustes alignment for equal-cardinality codes."""
    reference = unit_rows(reference)
    moving = unit_rows(moving)
    if reference.shape != moving.shape:
        raise ValueError("alignment needs equal shapes")
    best = None
    best_cost = math.inf
    # Covariance frames supply 32 deterministic sign initializations.
    _, ref_frame = np.linalg.eigh(reference.T @ reference)
    _, mov_frame = np.linalg.eigh(moving.T @ moving)
    for bits in range(1 << 5):
        signs = np.asarray(
            [-1.0 if bits & (1 << index) else 1.0 for index in range(5)]
        )
        candidate = moving @ ((mov_frame * signs[None, :]) @ ref_frame.T)
        cost = 2.0 - 2.0 * reference @ candidate.T
        rows, columns = linear_sum_assignment(cost)
        total = float(np.sum(cost[rows, columns]))
        if total < best_cost:
            best_cost = total
            best = candidate[columns]
    assert best is not None
    for _ in range(5):
        left, _, right = np.linalg.svd(best.T @ reference)
        best = best @ (left @ right)
        rows, columns = linear_sum_assignment(2.0 - 2.0 * reference @ best.T)
        if not np.array_equal(rows, np.arange(len(reference))):
            raise AssertionError("unexpected assignment order")
        best = best[columns]
    return unit_rows(best)


def latitude_block_crossover_equal(
    first: np.ndarray, second: np.ndarray, rng: np.random.Generator
) -> tuple[np.ndarray, dict]:
    second = align_parent(first, second)
    axis = rng.normal(size=5)
    axis /= np.linalg.norm(axis)
    scores = first @ axis
    cut = float(np.quantile(scores, rng.uniform(0.25, 0.75)))
    mask = scores >= cut
    child = np.array(first, copy=True)
    child[mask] = second[mask]
    # An independent tangent perturbation destroys inherited symmetries.
    noise = rng.normal(size=child.shape)
    noise -= np.sum(noise * child, axis=1)[:, None] * child
    scale = float(rng.uniform(0.015, 0.09))
    child = unit_rows(child + scale * noise)
    return child, {
        "mode": "aligned_latitude_block",
        "second_parent_rows": int(np.sum(mask)),
        "latitude_cut": cut,
        "mutation_scale": scale,
    }


def heterogeneous_latitude_crossover(
    first: np.ndarray,
    second: np.ndarray,
    target: int,
    rng: np.random.Generator,
    rotation_trials: int,
) -> tuple[np.ndarray, dict]:
    """Splice opposite latitude blocks from parents of arbitrary sizes."""
    first = unit_rows(first)
    second = unit_rows(second)
    quota_first = int(rng.integers(max(5, target // 3), min(len(first), 2 * target // 3) + 1))
    quota_second = target - quota_first
    if quota_second > len(second):
        quota_second = len(second)
        quota_first = target - quota_second
    best = None
    best_value = math.inf
    best_record = None
    for _ in range(rotation_trials):
        axis = rng.normal(size=5)
        axis /= np.linalg.norm(axis)
        rotated = second @ random_orthogonal(5, rng)
        # Take a low cap from one parent and a high cap from the other.  Their
        # inherited within-block inequalities are retained exactly.
        first_indices = np.argsort(first @ axis)[:quota_first]
        second_indices = np.argsort(rotated @ axis)[-quota_second:]
        candidate = np.vstack([first[first_indices], rotated[second_indices]])
        value = max_inner(candidate)
        if value < best_value:
            best_value = value
            best = candidate
            best_record = {
                "quota_first": quota_first,
                "quota_second": quota_second,
                "pre_release_maximum": value,
            }
    assert best is not None and best_record is not None
    noise = rng.normal(size=best.shape)
    noise -= np.sum(noise * best, axis=1)[:, None] * best
    scale = float(rng.uniform(0.005, 0.04))
    return unit_rows(best + scale * noise), {
        "mode": "opposed_latitude_caps",
        "rotation_trials": int(rotation_trials),
        "mutation_scale": scale,
        **best_record,
    }


def smooth_insert_objective(
    flat: np.ndarray,
    count: int,
    core: np.ndarray,
    beta: float,
) -> tuple[float, np.ndarray]:
    raw = np.asarray(flat).reshape(count, 5)
    norms = np.sqrt(np.sum(raw * raw, axis=1))
    if float(np.min(norms)) < 1e-13:
        return 1e20, np.zeros_like(flat)
    added = raw / norms[:, None]
    cross = added @ core.T
    values = [cross.ravel()]
    if count > 1:
        first, second = pair_indices(count)
        internal = np.sum(added[first] * added[second], axis=1)
        values.append(internal)
    concatenated = np.concatenate(values)
    scaled = beta * concatenated
    shift = float(np.max(scaled))
    exponential = np.exp(scaled - shift)
    weights = exponential / float(np.sum(exponential))
    value = (shift + math.log(float(np.sum(exponential)))) / beta
    ambient = weights[: count * len(core)].reshape(count, len(core)) @ core
    if count > 1:
        internal_weights = weights[count * len(core):]
        np.add.at(ambient, first, internal_weights[:, None] * added[second])
        np.add.at(ambient, second, internal_weights[:, None] * added[first])
    tangent = ambient - np.sum(ambient * added, axis=1)[:, None] * added
    return float(value), (tangent / norms[:, None]).ravel()


def optimize_insertions(
    core: np.ndarray,
    added: np.ndarray,
    betas: tuple[float, ...],
    max_iterations: int,
) -> tuple[np.ndarray, list[dict]]:
    core = unit_rows(core)
    x = unit_rows(added)
    history = []
    for beta in betas:
        result = minimize(
            smooth_insert_objective,
            x.ravel(),
            args=(len(x), core, float(beta)),
            jac=True,
            method="L-BFGS-B",
            options={
                "maxiter": int(max_iterations),
                "ftol": 2e-15,
                "gtol": 2e-10,
                "maxcor": 30,
                "maxls": 60,
            },
        )
        x = unit_rows(result.x.reshape(len(x), 5))
        joined = np.vstack([core, x])
        history.append(
            {
                "beta": float(beta),
                "iterations": int(result.nit),
                "success": bool(result.success),
                "message": str(result.message),
                "maximum": max_inner(joined),
            }
        )
    return x, history


def sampled_blocker_removal(
    source: np.ndarray,
    k: int,
    rng: np.random.Generator,
    samples: int,
) -> tuple[np.ndarray, np.ndarray, dict]:
    """Delete the k largest blockers of the best sampled insertion direction."""
    source = unit_rows(source)
    probes = unit_rows(rng.normal(size=(samples, 5)))
    inner = probes @ source.T
    # The best achievable maximum after deleting k blockers from a single
    # sampled insertion direction is its (k+1)-st largest inner product.
    ordered = np.sort(inner, axis=1)
    residual = ordered[:, -(k + 1)]
    probe_index = int(np.argmin(residual))
    ranking = np.argsort(inner[probe_index])[::-1]
    removed = np.sort(ranking[:k])
    keep = np.ones(len(source), dtype=bool)
    keep[removed] = False
    return source[keep], probes[probe_index], {
        "k": int(k),
        "samples": int(samples),
        "removed_indices": removed.astype(int).tolist(),
        "sampled_residual_bound": float(residual[probe_index]),
    }


def seed_added_points(
    core: np.ndarray,
    first: np.ndarray,
    count: int,
    rng: np.random.Generator,
    samples: int,
) -> np.ndarray:
    chosen = [unit_rows(np.asarray(first)[None, :])[0]]
    while len(chosen) < count:
        probes = unit_rows(rng.normal(size=(samples, 5)))
        obstacles = np.vstack([core, np.asarray(chosen)])
        values = np.max(probes @ obstacles.T, axis=1)
        chosen.append(probes[int(np.argmin(values))])
    return unit_rows(np.asarray(chosen))


def surgery_move(
    source: np.ndarray,
    k: int,
    rng: np.random.Generator,
    hole_samples: int,
    max_iterations: int,
    full_betas: tuple[float, ...],
) -> tuple[np.ndarray, dict]:
    core, first, removal = sampled_blocker_removal(
        source, k, rng, hole_samples
    )
    added = seed_added_points(core, first, k + 1, rng, max(600, hole_samples // 3))
    added, insertion_history = optimize_insertions(
        core, added, (24.0, 48.0, 96.0, 192.0), max_iterations
    )
    joined = np.vstack([core, added])
    released, release_history = relax_full(
        joined, full_betas, max_iterations
    )
    return released, {
        **removal,
        "source_cardinality": int(len(source)),
        "target_cardinality": int(len(released)),
        "fixed_core_maximum": max_inner(core),
        "post_insertion_maximum": max_inner(joined),
        "insertion_history": insertion_history,
        "release_history": release_history,
    }


def components(n: int, edges: list[list[int]]) -> list[int]:
    adjacency = [set() for _ in range(n)]
    for first, second in edges:
        adjacency[first].add(second)
        adjacency[second].add(first)
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


def coordinate_hash(x: np.ndarray) -> str:
    normalized = np.ascontiguousarray(unit_rows(x), dtype="<f8")
    return hashlib.sha256(normalized.tobytes()).hexdigest()


def diagnostics(
    x: np.ndarray, label: str, mechanism: str, provenance: dict
) -> dict:
    # Save one normalized binary64 array, then audit a fresh normalization of
    # exactly those saved numbers.  The independent verifier performs the same
    # one-step normalization after JSON parsing.
    saved_coordinates = unit_rows(x)
    x = unit_rows(saved_coordinates)
    first, second = pair_indices(len(x))
    values = np.sum(x[first] * x[second], axis=1)
    maximum = float(np.max(values))
    maximizing = np.flatnonzero(values == maximum)
    gram_eigenvalues = np.linalg.eigvalsh(x @ x.T)[::-1]
    frame_eigenvalues = np.linalg.eigvalsh(x.T @ x)[::-1]
    tolerance = 5e-4
    active = values >= maximum - tolerance
    edges = np.column_stack([first[active], second[active]]).astype(int).tolist()
    degree = np.zeros(len(x), dtype=int)
    for i, j in edges:
        degree[i] += 1
        degree[j] += 1
    unique, counts = np.unique(degree, return_counts=True)
    degree_histogram = {
        str(int(value)): int(count)
        for value, count in zip(unique, counts)
    }
    edge_hash = hashlib.sha256(
        json.dumps(edges, separators=(",", ":")).encode()
    ).hexdigest()
    quantiles = np.quantile(
        values, [0.0, 0.01, 0.10, 0.25, 0.50, 0.75, 0.90, 0.99, 1.0]
    )
    return {
        "label": label,
        "mechanism": mechanism,
        "status": STATUS,
        "n": int(len(x)),
        "coordinates_float64": saved_coordinates.tolist(),
        "coordinate_little_endian_float64_sha256": coordinate_hash(
            saved_coordinates
        ),
        "maximum_inner_product_binary64": maximum,
        "maximum_inner_product_float_hex": maximum.hex(),
        "gap_above_one_half": maximum - 0.5,
        "literal_binary64_maximizing_pairs": [
            [int(first[index]), int(second[index])] for index in maximizing
        ],
        "minimum_inner_product": float(np.min(values)),
        "pair_inner_product_quantiles": [
            float(value) for value in quantiles
        ],
        "gram_eigenvalues_descending": [
            float(value) for value in gram_eigenvalues
        ],
        "frame_eigenvalues_descending": [
            float(value) for value in frame_eigenvalues
        ],
        "numerical_gram_rank_at_1e-9": int(
            np.sum(gram_eigenvalues > 1e-9)
        ),
        "centroid_norm": float(np.linalg.norm(np.sum(x, axis=0))),
        "active_graph": {
            "tolerance_below_maximum": tolerance,
            "edge_count": len(edges),
            "edges": edges,
            "edge_sha256": edge_hash,
            "degree_histogram": degree_histogram,
            "component_sizes": components(len(x), edges),
        },
        "provenance": provenance,
    }


def candidate_better(
    candidates: dict[tuple[str, int], tuple[np.ndarray, dict]],
    mechanism: str,
    n: int,
    x: np.ndarray,
    provenance: dict,
) -> None:
    key = (mechanism, n)
    if key not in candidates or max_inner(x) < max_inner(candidates[key][0]):
        candidates[key] = (np.array(x, copy=True), provenance)


def run_search(args: argparse.Namespace) -> dict:
    rng = np.random.default_rng(args.seed)
    known = floating_known_codes()
    full_betas = tuple(float(value) for value in args.full_betas.split(","))
    layer_betas = tuple(float(value) for value in args.layer_betas.split(","))
    candidates: dict[tuple[str, int], tuple[np.ndarray, dict]] = {}
    counters = Counter()
    start_time = time.time()

    # Precompute S^3 subcodes for every layer size used below.
    proposed_partitions: dict[int, list[tuple[int, ...]]] = {}
    all_sizes: set[int] = set()
    layer_counts = [
        int(value) for value in args.layer_counts.split(",") if value.strip()
    ]
    if not layer_counts or any(value < 2 for value in layer_counts):
        raise ValueError("layer counts must contain integers at least two")
    for n in range(41, 45):
        partitions = []
        for index in range(args.layer_starts):
            layers = layer_counts[index % len(layer_counts)]
            if index < len(layer_counts):
                sizes = balanced_partition(n, layers, offset=index)
            elif index % 2:
                sizes = unbalanced_partition(
                    n, layers, args.layer_minimum, rng
                )
            else:
                sizes = random_partition(
                    n, layers, args.layer_minimum, rng
                )
            partitions.append(sizes)
            all_sizes.update(sizes)
        proposed_partitions[n] = partitions
    template_cache = build_template_cache(
        all_sizes, rng, max(20, args.max_iterations // 2)
    )

    layer_population: dict[int, list[np.ndarray]] = {n: [] for n in range(41, 45)}
    layer_records: dict[int, list[dict]] = {n: [] for n in range(41, 45)}
    for n in range(41, 45):
        for start_index, sizes in enumerate(proposed_partitions[n]):
            variables, initialization = layer_start(sizes, rng, template_cache)
            tied, layer_history, final_heights = optimize_layers(
                variables, sizes, layer_betas, args.max_iterations
            )
            noise = rng.normal(size=tied.shape)
            noise -= np.sum(noise * tied, axis=1)[:, None] * tied
            released, release_history = relax_full(
                unit_rows(tied + 0.003 * noise),
                full_betas,
                args.max_iterations,
            )
            provenance = {
                "seed": int(args.seed),
                "start_index": int(start_index),
                "initialization": initialization,
                "final_tied_heights": final_heights,
                "tied_layer_maximum": max_inner(tied),
                "layer_history": layer_history,
                "release_history": release_history,
            }
            layer_population[n].append(released)
            layer_records[n].append(provenance)
            candidate_better(
                candidates, "latitude_layer_release", n, released, provenance
            )
            counters["latitude_layer_starts"] += 1

    # A second layer portfolio inherits the actual relative S^3 orientations
    # of D5/L5/Q5/R5 under several axes, then adds points to inherited or new
    # latitudes.  This explicitly includes the D5 (8,24,8) decomposition and
    # its low-symmetry cardinality-increased deformations.
    axis_bank = [np.eye(5)[index] for index in range(5)]
    axis_bank.append(np.ones(5) / math.sqrt(5.0))
    for n in range(41, 45):
        for source_index, (source_name, source) in enumerate(known.items()):
            for axis_index in range(args.source_layer_starts):
                if axis_index < len(axis_bank):
                    axis = axis_bank[(source_index + axis_index) % len(axis_bank)]
                else:
                    axis = rng.normal(size=5)
                    axis /= np.linalg.norm(axis)
                variables, sizes, initialization = source_layer_insertion_start(
                    source,
                    n,
                    axis,
                    rng,
                    max(600, args.hole_samples // 3),
                )
                tied, layer_history, final_heights = optimize_layers(
                    variables, sizes, layer_betas, args.max_iterations
                )
                noise = rng.normal(size=tied.shape)
                noise -= np.sum(noise * tied, axis=1)[:, None] * tied
                released, release_history = relax_full(
                    unit_rows(tied + 0.002 * noise),
                    full_betas,
                    args.max_iterations,
                )
                provenance = {
                    "seed": int(args.seed),
                    "source": source_name,
                    "axis_index": int(axis_index),
                    "axis": axis.tolist(),
                    "initialization": initialization,
                    "final_tied_heights": final_heights,
                    "tied_layer_maximum": max_inner(tied),
                    "layer_history": layer_history,
                    "release_history": release_history,
                }
                layer_population[n].append(released)
                layer_records[n].append(provenance)
                candidate_better(
                    candidates,
                    "known_source_layer_insertion",
                    n,
                    released,
                    provenance,
                )
                counters["known_source_layer_starts"] += 1

    # Seed full-dimensional random basins, kept independent of the layers.
    unrelated_population: dict[int, list[np.ndarray]] = {
        n: list(layer_population[n]) for n in range(41, 45)
    }
    for n in range(41, 45):
        for start_index in range(args.random_starts):
            random_start = unit_rows(rng.normal(size=(n, 5)))
            random_code, history = relax_full(
                random_start, full_betas, args.max_iterations
            )
            provenance = {
                "seed": int(args.seed),
                "start_index": int(start_index),
                "release_history": history,
            }
            unrelated_population[n].append(random_code)
            candidate_better(
                candidates, "unrelated_random_basin", n, random_code, provenance
            )
            counters["unrelated_random_starts"] += 1

    # Remove-k/add-(k+1), explicitly covering every k=2,...,6 and every one
    # of the four nonisometric exact K40 sources.
    surgery_population: dict[int, list[np.ndarray]] = {
        n: [] for n in range(41, 45)
    }
    trajectory_id = 0
    for source_name, source in known.items():
        for k in range(2, 7):
            current = source
            trajectory = []
            for target in range(41, 45):
                # First move uses its prescribed k; later moves rotate through
                # 2,...,6 so cardinality changes remain asymmetric.
                move_k = 2 + ((k - 2 + target - 41) % 5)
                current, move_record = surgery_move(
                    current,
                    move_k,
                    rng,
                    args.hole_samples,
                    args.max_iterations,
                    full_betas,
                )
                trajectory.append(move_record)
                provenance = {
                    "seed": int(args.seed),
                    "trajectory_id": int(trajectory_id),
                    "exact_source": source_name,
                    "initial_k": int(k),
                    "moves": list(trajectory),
                }
                surgery_population[target].append(current)
                candidate_better(
                    candidates,
                    "remove_k_add_k_plus_one",
                    target,
                    current,
                    provenance,
                )
                counters["surgery_moves"] += 1
            trajectory_id += 1

    # Cross exact K40 basins with genuinely unrelated latitude/random
    # populations.  Then cross equal-cardinality descendants for several
    # generations with latitude-block inheritance.
    evolution_population: dict[int, list[np.ndarray]] = {
        n: [] for n in range(41, 45)
    }
    for n in range(41, 45):
        foreign = sorted(
            unrelated_population[n] + surgery_population[n],
            key=max_inner,
        )[: max(4, args.population)]
        polished_foreign = []
        for candidate in foreign:
            polished, _ = epigraph_polish(
                candidate, args.evolution_polish_iterations
            )
            polished_foreign.append(
                polished
                if max_inner(polished) <= max_inner(candidate) + 2e-12
                else candidate
            )
            counters["intermediate_epigraph_polishes"] += 1
        foreign = sorted(polished_foreign, key=max_inner)
        for cross_index in range(args.crossovers):
            source_name = list(known)[cross_index % 4]
            second = foreign[cross_index % len(foreign)]
            child, cross_record = heterogeneous_latitude_crossover(
                known[source_name],
                second,
                n,
                rng,
                args.rotation_trials,
            )
            child, history = relax_full(
                child, full_betas, args.max_iterations
            )
            settled, intermediate_polish = epigraph_polish(
                child, args.evolution_polish_iterations
            )
            if max_inner(settled) <= max_inner(child) + 2e-12:
                child = settled
                intermediate_polish["accepted"] = True
            else:
                intermediate_polish["accepted"] = False
            counters["intermediate_epigraph_polishes"] += 1
            provenance = {
                "seed": int(args.seed),
                "cross_index": int(cross_index),
                "exact_parent": source_name,
                "unrelated_parent_maximum": max_inner(second),
                "crossover": cross_record,
                "release_history": history,
                "intermediate_epigraph_polish": intermediate_polish,
            }
            evolution_population[n].append(child)
            candidate_better(
                candidates,
                "heterogeneous_latitude_crossover",
                n,
                child,
                provenance,
            )
            counters["heterogeneous_crossovers"] += 1

        population = sorted(
            foreign + evolution_population[n], key=max_inner
        )[: args.population]
        for generation in range(args.generations):
            children = []
            for child_index in range(args.crossovers):
                first_index, second_index = rng.choice(
                    len(population), size=2, replace=False
                )
                child, cross_record = latitude_block_crossover_equal(
                    population[int(first_index)],
                    population[int(second_index)],
                    rng,
                )
                child, history = relax_full(
                    child, full_betas, args.max_iterations
                )
                settled, intermediate_polish = epigraph_polish(
                    child, args.evolution_polish_iterations
                )
                if max_inner(settled) <= max_inner(child) + 2e-12:
                    child = settled
                    intermediate_polish["accepted"] = True
                else:
                    intermediate_polish["accepted"] = False
                counters["intermediate_epigraph_polishes"] += 1
                provenance = {
                    "seed": int(args.seed),
                    "generation": int(generation),
                    "child_index": int(child_index),
                    "parent_maxima": [
                        max_inner(population[int(first_index)]),
                        max_inner(population[int(second_index)]),
                    ],
                    "crossover": cross_record,
                    "release_history": history,
                    "intermediate_epigraph_polish": intermediate_polish,
                }
                children.append(child)
                candidate_better(
                    candidates,
                    "evolutionary_latitude_block",
                    n,
                    child,
                    provenance,
                )
                counters["equal_cardinality_crossovers"] += 1
            population = sorted(population + children, key=max_inner)[
                : args.population
            ]

    # Settle each independently discovered basin against the literal maximum.
    # If SLSQP fails or increases the recomputed maximum, retain the incoming
    # coordinates and record the rejected endpoint.
    for key, (incoming, provenance) in list(candidates.items()):
        polished, polish_record = epigraph_polish(
            incoming, args.epigraph_iterations
        )
        polish_record["incoming_maximum"] = max_inner(incoming)
        if max_inner(polished) <= max_inner(incoming) + 2e-12:
            chosen = polished
            polish_record["accepted"] = True
        else:
            chosen = incoming
            polish_record["accepted"] = False
        updated = dict(provenance)
        updated["literal_epigraph_polish"] = polish_record
        candidates[key] = (chosen, updated)
        counters["literal_epigraph_polishes"] += 1

    best_records = []
    for (mechanism, n), (x, provenance) in sorted(candidates.items()):
        best_records.append(
            diagnostics(
                x,
                label=f"{mechanism}_N{n}",
                mechanism=mechanism,
                provenance=provenance,
            )
        )
    overall = []
    for n in range(41, 45):
        record = min(
            (record for record in best_records if record["n"] == n),
            key=lambda item: item["maximum_inner_product_binary64"],
        )
        overall.append(record["label"])
    return {
        "status": STATUS,
        "experiment": "latitude-layer/evolution/cardinality-changing construction portfolio",
        "dimension": 5,
        "cardinalities": [41, 42, 43, 44],
        "seed": int(args.seed),
        "command_arguments": {
            key: str(value) if isinstance(value, Path) else value
            for key, value in vars(args).items()
        },
        "software": {
            "python": sys.version,
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
        },
        "deterministic_blas_threads_requested": {
            name: os.environ.get(name)
            for name in (
                "OMP_NUM_THREADS",
                "OPENBLAS_NUM_THREADS",
                "MKL_NUM_THREADS",
                "VECLIB_MAXIMUM_THREADS",
            )
        },
        "search_counts": dict(counters),
        "elapsed_seconds": time.time() - start_time,
        "best_record_labels_by_cardinality": overall,
        "records": best_records,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=2026072401)
    parser.add_argument("--layer-starts", type=int, default=8)
    parser.add_argument("--layer-counts", default="2,3,4,5,6,7,8")
    parser.add_argument("--layer-minimum", type=int, default=1)
    parser.add_argument("--source-layer-starts", type=int, default=2)
    parser.add_argument("--random-starts", type=int, default=3)
    parser.add_argument("--crossovers", type=int, default=6)
    parser.add_argument("--generations", type=int, default=2)
    parser.add_argument("--population", type=int, default=8)
    parser.add_argument("--rotation-trials", type=int, default=80)
    parser.add_argument("--hole-samples", type=int, default=3500)
    parser.add_argument("--max-iterations", type=int, default=100)
    parser.add_argument("--epigraph-iterations", type=int, default=500)
    parser.add_argument("--evolution-polish-iterations", type=int, default=120)
    parser.add_argument("--layer-betas", default="12,24,48,96")
    parser.add_argument("--full-betas", default="48,96,192,384")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("portfolio.json"),
    )
    args = parser.parse_args()
    result = run_search(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "status": result["status"],
                "elapsed_seconds": result["elapsed_seconds"],
                "search_counts": result["search_counts"],
                "best": {
                    str(n): min(
                        record["maximum_inner_product_binary64"]
                        for record in result["records"]
                        if record["n"] == n
                    )
                    for n in range(41, 45)
                },
                "output": str(args.output),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
