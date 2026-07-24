#!/usr/bin/env python3
"""Adaptive atomic BV search with rank-sensitive centered-skew cuts.

This is discovery code.  A feasible output is only a pair/triple
pseudodistribution on the selected rational node grid, not a spherical code.
An infeasible solver status is not a proof.  All rank-band coefficients are
constructed with exact rational arithmetic before being converted to floats
for CVXPY.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations_with_replacement, permutations
import json
import math
from pathlib import Path
from typing import Iterable

import cvxpy as cp
import numpy as np


N = 41
S = Q(1, 2)


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def parse_grid(name: str) -> tuple[Q, ...]:
    """Return one of the nested rational discovery grids."""

    denominators = {
        "quarter": 4,
        "eighth": 8,
        "sixteenth": 16,
    }
    if name not in denominators:
        raise ValueError(f"unknown grid {name!r}")
    denominator = denominators[name]
    return tuple(
        Q(numerator, denominator)
        for numerator in range(-denominator, denominator // 2 + 1)
    )


def adaptive_grid(
    old_grid: Iterable[Q],
    alpha: Iterable[float],
    threshold: float = 1.0e-5,
) -> tuple[Q, ...]:
    """Bisect intervals incident to atoms carrying visible pair mass."""

    nodes = tuple(old_grid)
    masses = tuple(alpha)
    answer = set(nodes)
    for index, mass in enumerate(masses):
        if mass <= threshold:
            continue
        if index:
            answer.add((nodes[index - 1] + nodes[index]) / 2)
        if index + 1 < len(nodes):
            answer.add((nodes[index] + nodes[index + 1]) / 2)
    return tuple(sorted(answer))


def gegenbauer_5(t: Q, maximum_degree: int) -> tuple[Q, ...]:
    """Normalized dimension-five Gegenbauer values P_k(1)=1."""

    values = [Q(1)]
    if maximum_degree:
        values.append(t)
    for k in range(2, maximum_degree + 1):
        values.append(
            ((2 * k + 1) * t * values[-1] - (k - 1) * values[-2])
            / (k + 2)
        )
    return tuple(values)


def transverse_q(u: Q, v: Q, t: Q, maximum_degree: int) -> tuple[Q, ...]:
    """Polynomialized Bachoc--Vallentin transverse kernels Q_k."""

    area = (1 - u * u) * (1 - v * v)
    displacement = t - u * v
    values = [Q(1)]
    if maximum_degree:
        values.append(displacement)
    for k in range(1, maximum_degree):
        values.append(
            Q(2 * (k + 1), k + 2) * displacement * values[-1]
            - Q(k, k + 2) * area * values[-2]
        )
    return tuple(values)


def gram_determinant(u: Q, v: Q, t: Q) -> Q:
    return 1 + 2 * u * v * t - u * u - v * v - t * t


def feasible_orbits(nodes: tuple[Q, ...]) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        triple
        for triple in combinations_with_replacement(range(len(nodes)), 3)
        if gram_determinant(*(nodes[index] for index in triple)) >= 0
    )


def common_pair_capacity(p: Q) -> int | None:
    """Exact endpoint convention in the projected S^2 capacity theorem."""

    if p > 1:
        return 0
    if p > Q(3, 4):
        return 1
    if p > Q(2, 3):
        return 2
    if p > Q(5, 8):
        return 3
    if p > Q(1, 2):
        return 4
    if p == Q(1, 2):
        return 6
    return None


def stratified_capacity_rows(
    nodes: tuple[Q, ...],
    orbits: tuple[tuple[int, int, int], ...],
) -> tuple[dict[str, object], ...]:
    """All contiguous nonpositive base bands and positive thresholds.

    If a base band ends at a<=0, every base pair in it has at most M(a,b)
    common neighbors whose two incident inner products are at least b.
    Singleton bands are the exact-stratum cuts missed by the earlier
    cumulative implementation.
    """

    nonpositive = tuple(
        index for index, node in enumerate(nodes) if node <= 0
    )
    positive = tuple(index for index, node in enumerate(nodes) if node > 0)
    rows = []
    for lower_position in range(len(nonpositive)):
        for upper_position in range(lower_position, len(nonpositive)):
            base_indices = nonpositive[lower_position : upper_position + 1]
            upper_node = nodes[base_indices[-1]]
            for high_index in positive:
                high = nodes[high_index]
                if upper_node == -1:
                    p = None
                    capacity = 0
                else:
                    p = 2 * high**2 / (1 + upper_node)
                    capacity = common_pair_capacity(p)
                if capacity is None:
                    continue
                coefficients = []
                base_set = set(base_indices)
                for triple in orbits:
                    count = 0
                    for position in range(3):
                        if triple[position] not in base_set:
                            continue
                        if all(
                            nodes[triple[other]] >= high
                            for other in range(3)
                            if other != position
                        ):
                            count += 1
                    coefficients.append(count)
                rows.append(
                    {
                        "lower_index": base_indices[0],
                        "upper_index": base_indices[-1],
                        "lower": nodes[base_indices[0]],
                        "upper": upper_node,
                        "high": high,
                        "p": p,
                        "capacity": capacity,
                        "nu_coefficients": tuple(coefficients),
                        "alpha_indices": base_indices,
                    }
                )
    return tuple(rows)


def weighted_capacity_rows(
    nodes: tuple[Q, ...],
    orbits: tuple[tuple[int, int, int], ...],
) -> tuple[dict[str, object], ...]:
    """Pointwise-capacity integrals, with the b=1/2 positive-q cap seven."""

    rows = []
    for high_index, high in enumerate(nodes):
        if high <= 0:
            continue
        capacities: dict[int, int] = {}
        for base_index, base in enumerate(nodes):
            if base == -1:
                capacity = 0
            elif base <= 0:
                capacity = common_pair_capacity(
                    2 * high**2 / (1 + base)
                )
                if capacity is None:
                    continue
            elif high == Q(1, 2):
                # The universal A(3,1/4)=7 common-contact bound.
                capacity = 7
            else:
                continue
            capacities[base_index] = capacity
        coefficients = []
        for triple in orbits:
            count = 0
            for position in range(3):
                if triple[position] not in capacities:
                    continue
                if all(
                    nodes[triple[other]] >= high
                    for other in range(3)
                    if other != position
                ):
                    count += 1
            coefficients.append(count)
        rows.append(
            {
                "high": high,
                "capacities": capacities,
                "nu_coefficients": tuple(coefficients),
            }
        )
    return tuple(rows)


def harmonic_dimension(degree: int) -> int:
    first = math.comb(degree + 4, 4)
    second = math.comb(degree + 2, 4) if degree >= 2 else 0
    return first - second


@dataclass(frozen=True)
class Kernel:
    name: str
    weights: tuple[tuple[int, Q], ...]

    @property
    def rank(self) -> int:
        return sum(harmonic_dimension(degree) for degree, _ in self.weights)

    def values(self, nodes: tuple[Q, ...]) -> tuple[Q, ...]:
        maximum = max(degree for degree, _ in self.weights)
        return tuple(
            sum(
                coefficient * gegenbauer_5(node, maximum)[degree]
                for degree, coefficient in self.weights
            )
            for node in nodes
        )

    @property
    def diagonal(self) -> Q:
        return sum(coefficient for _, coefficient in self.weights)


def default_kernels(profile: str = "rich") -> tuple[Kernel, ...]:
    """Low-harmonic combinations whose summed feature rank is below 41."""

    basic = [
        Kernel("H1", ((1, Q(1)),)),
        Kernel("H2", ((2, Q(1)),)),
        Kernel("H3", ((3, Q(1)),)),
        Kernel("H0+5H1", ((0, Q(1, 6)), (1, Q(5, 6)))),
        Kernel("H0-5H1", ((0, Q(1, 6)), (1, Q(-5, 6)))),
        Kernel("H0+14H2", ((0, Q(1, 15)), (2, Q(14, 15)))),
        Kernel("H0-14H2", ((0, Q(1, 15)), (2, Q(-14, 15)))),
        Kernel("5H1+14H2", ((1, Q(5, 19)), (2, Q(14, 19)))),
        Kernel("5H1-14H2", ((1, Q(5, 19)), (2, Q(-14, 19)))),
    ]
    if profile == "basic":
        return tuple(basic)
    rich = basic + [
        Kernel("H0+H1", ((0, Q(1, 2)), (1, Q(1, 2)))),
        Kernel("H0-H1", ((0, Q(1, 2)), (1, Q(-1, 2)))),
        Kernel("H0+H2", ((0, Q(1, 2)), (2, Q(1, 2)))),
        Kernel("H0-H2", ((0, Q(1, 2)), (2, Q(-1, 2)))),
        Kernel("H1+H2", ((1, Q(1, 2)), (2, Q(1, 2)))),
        Kernel("H1-H2", ((1, Q(1, 2)), (2, Q(-1, 2)))),
        Kernel(
            "H0+5H1+14H2",
            ((0, Q(1, 20)), (1, Q(1, 4)), (2, Q(7, 10))),
        ),
        Kernel(
            "H0+5H1-14H2",
            ((0, Q(1, 20)), (1, Q(1, 4)), (2, Q(-7, 10))),
        ),
        Kernel(
            "H0-5H1+14H2",
            ((0, Q(1, 20)), (1, Q(-1, 4)), (2, Q(7, 10))),
        ),
        Kernel(
            "H0-5H1-14H2",
            ((0, Q(1, 20)), (1, Q(-1, 4)), (2, Q(-7, 10))),
        ),
        Kernel("H0+30H3", ((0, Q(1, 31)), (3, Q(30, 31)))),
        Kernel("H0-30H3", ((0, Q(1, 31)), (3, Q(-30, 31)))),
        Kernel("5H1+30H3", ((1, Q(1, 7)), (3, Q(6, 7)))),
        Kernel("5H1-30H3", ((1, Q(1, 7)), (3, Q(-6, 7)))),
        Kernel(
            "H0+5H1+30H3",
            ((0, Q(1, 36)), (1, Q(5, 36)), (3, Q(5, 6))),
        ),
        Kernel(
            "H0+5H1-30H3",
            ((0, Q(1, 36)), (1, Q(5, 36)), (3, Q(-5, 6))),
        ),
        Kernel(
            "H0-5H1+30H3",
            ((0, Q(1, 36)), (1, Q(-5, 36)), (3, Q(5, 6))),
        ),
        Kernel(
            "H0-5H1-30H3",
            ((0, Q(1, 36)), (1, Q(-5, 36)), (3, Q(-5, 6))),
        ),
    ]
    assert all(2 <= kernel.rank < N for kernel in rich)
    return tuple(rich)


def ceil_sqrt_scaled(value: Q, scale: int) -> Q:
    """Smallest multiple of 1/scale whose square is at least value."""

    assert value >= 0
    numerator = value.numerator * scale * scale
    denominator = value.denominator
    candidate = math.isqrt(numerator // denominator)
    while candidate * candidate * denominator < numerator:
        candidate += 1
    return Q(candidate, scale)


def exact_radius(variance: Q, rank: int, scale: int = 10**8) -> Q:
    """Rational upper bound on the sharp centered-third radius."""

    assert variance >= 0 and rank >= 2
    squared = Q((rank - 2) ** 2, rank * (rank - 1)) * variance**3
    return ceil_sqrt_scaled(squared, scale)


def global_secant_slope(
    variance_upper: Q,
    rank: int,
    scale: int = 10**8,
) -> Q:
    """Rational s with sharp_radius(V) <= s V on [0, variance_upper]."""

    assert variance_upper > 0
    squared = (
        Q((rank - 2) ** 2, rank * (rank - 1)) * variance_upper
    )
    return ceil_sqrt_scaled(squared, scale)


def rational_radius_chord(
    lower: Q,
    upper: Q,
    rank: int,
    scale: int = 10**8,
) -> tuple[Q, Q, Q, Q]:
    """A rational affine majorant of the sharp radius on [lower, upper]."""

    assert 0 <= lower < upper
    lower_radius = exact_radius(lower, rank, scale)
    upper_radius = exact_radius(upper, rank, scale)
    slope = (upper_radius - lower_radius) / (upper - lower)
    intercept = lower_radius - slope * lower
    return slope, intercept, lower_radius, upper_radius


def rank_traces(
    kernel: Kernel,
    nodes: tuple[Q, ...],
    orbits: tuple[tuple[int, int, int], ...],
    alpha: np.ndarray | cp.Expression,
    nu: np.ndarray | cp.Expression,
):
    """Return affine V,D expressions in exact coefficient form."""

    rank = kernel.rank
    diagonal = kernel.diagonal
    values = kernel.values(nodes)
    trace_one = Q(N) * diagonal
    pair_coefficients = np.array(
        [float(Q(N) * value * value) for value in values]
    )
    trace_two = float(Q(N) * diagonal**2) + pair_coefficients @ alpha
    triple_coefficients = np.array(
        [
            float(Q(N) * values[i] * values[j] * values[k])
            for i, j, k in orbits
        ]
    )
    trace_three = (
        float(Q(N) * diagonal**3)
        + 3 * float(diagonal) * pair_coefficients @ alpha
        + triple_coefficients @ nu
    )
    variance = trace_two - float(trace_one**2 / rank)
    centered = (
        trace_three
        - float(Q(3) * trace_one / rank) * trace_two
        + float(Q(2) * trace_one**3 / rank**2)
    )
    return variance, centered, values


def exact_rank_values(
    kernel: Kernel,
    nodes: tuple[Q, ...],
    orbits: tuple[tuple[int, int, int], ...],
    alpha: Iterable[float],
    nu: Iterable[float],
) -> tuple[float, float, float]:
    """Evaluate V,D and B V^3-A D^2 for a numerical pseudomeasure."""

    rank = kernel.rank
    diagonal = float(kernel.diagonal)
    values = np.array([float(value) for value in kernel.values(nodes)])
    alpha_array = np.asarray(tuple(alpha), dtype=float)
    nu_array = np.asarray(tuple(nu), dtype=float)
    trace_one = N * diagonal
    trace_two = N * diagonal**2 + N * np.dot(alpha_array, values**2)
    products = np.array(
        [values[i] * values[j] * values[k] for i, j, k in orbits]
    )
    trace_three = (
        N * diagonal**3
        + 3 * N * diagonal * np.dot(alpha_array, values**2)
        + N * np.dot(nu_array, products)
    )
    variance = trace_two - trace_one**2 / rank
    centered = (
        trace_three
        - 3 * trace_one * trace_two / rank
        + 2 * trace_one**3 / rank**2
    )
    residual = (
        (rank - 2) ** 2 * variance**3
        - rank * (rank - 1) * centered**2
    )
    return variance, centered, residual


def coefficient_arrays(
    nodes: tuple[Q, ...],
    orbits: tuple[tuple[int, int, int], ...],
    maximum_harmonic: int,
):
    """Build affine full-radial W_k coefficient arrays."""

    m = len(nodes)
    size = m + 1  # append the diagonal atom u=1
    alpha_arrays = []
    nu_arrays = []
    constants = []
    for degree in range(maximum_harmonic + 1):
        constant = np.zeros((size, size))
        alpha_coeff = np.zeros((size * size, m))
        nu_coeff = np.zeros((size * size, len(orbits)))
        if degree == 0:
            constant[-1, -1] = 1.0
            for index in range(m):
                alpha_coeff[(size - 1) * size + index, index] += 1.0
                alpha_coeff[index * size + (size - 1), index] += 1.0
                alpha_coeff[index * size + index, index] += 1.0
        else:
            for index, node in enumerate(nodes):
                alpha_coeff[index * size + index, index] += float(
                    (1 - node * node) ** degree
                )
        for orbit_index, triple in enumerate(orbits):
            ordered_indices = sorted(set(permutations(triple)))
            coefficient = Q(1, len(ordered_indices))
            for i, j, k in ordered_indices:
                value = transverse_q(
                    nodes[i], nodes[j], nodes[k], degree
                )[degree]
                nu_coeff[i * size + j, orbit_index] += float(
                    coefficient * value
                )
        constants.append(constant)
        alpha_arrays.append(alpha_coeff)
        nu_arrays.append(nu_coeff)
    return tuple(constants), tuple(alpha_arrays), tuple(nu_arrays)


def load_baseline_alpha(
    project_root: Path, nodes: tuple[Q, ...]
) -> tuple[Q, ...]:
    source = json.loads(
        (
            project_root
            / "certificates"
            / "fixed41_bv_fullradial_k16_pseudodistribution.json"
        ).read_text()
    )
    source_nodes = tuple(Q(value) for value in source["grid"])
    source_alpha = tuple(Q(value) for value in source["alpha"])
    mapping = dict(zip(source_nodes, source_alpha))
    return tuple(mapping.get(node, Q(0)) for node in nodes)


def load_atomic_warm(
    path: Path,
) -> tuple[
    tuple[Q, ...],
    tuple[Q, ...],
    dict[tuple[Q, Q, Q], float],
]:
    """Load either one of our outputs or the exact common-pair witness."""

    data = json.loads(path.read_text())
    warm_nodes = tuple(Q(value) for value in data["grid" if "grid" in data else "nodes"])
    if "alpha" in data:
        warm_alpha = tuple(Q(str(value)) for value in data["alpha"])
        warm_orbits = tuple(tuple(item) for item in data["triple_orbits"])
        warm_nu = {
            tuple(sorted(warm_nodes[index] for index in orbit)): float(value)
            for orbit, value in zip(warm_orbits, data["nu"])
        }
    else:
        assert data["schema"] == (
            "common-pair-capacity-degree4-pseudodistribution-v1"
        )
        warm_alpha = tuple(
            Q(value, N) for value in data["ordered_pair_counts"]
        )
        warm_nu = {
            tuple(
                sorted(warm_nodes[index] for index in item["types"])
            ): float(Q(6 * item["count"], N))
            for item in data["triple_counts"]
        }
    return warm_nodes, warm_alpha, warm_nu


def pair_frame_constraints(
    nodes: tuple[Q, ...], alpha: cp.Expression
) -> list[cp.Constraint]:
    """All nontrivial C067 frame-potential matrix inequalities."""

    values = np.array(
        [
            [float(value) for value in gegenbauer_5(node, 3)]
            for node in nodes
        ]
    )
    dimensions = (1, 5, 14, 30)
    subsets = (
        (1,),
        (0, 1),
        (2,),
        (0, 2),
        (1, 2),
        (0, 1, 2),
        (3,),
        (0, 3),
        (1, 3),
        (0, 1, 3),
    )
    constraints = []
    for subset in subsets:
        rank = sum(dimensions[index] for index in subset)
        block_rows = []
        for first in subset:
            row = []
            for second in subset:
                row.append(
                    1.0
                    + cp.sum(
                        cp.multiply(
                            values[:, first] * values[:, second], alpha
                        )
                    )
                    - N / rank
                )
            block_rows.append(row)
        constraints.append(cp.bmat(block_rows) >> 0)
    return constraints


def safe_variance_upper(
    kernel: Kernel, nodes: tuple[Q, ...]
) -> Q:
    """Mass-only exact upper bound valid for every atomic pair measure."""

    diagonal = kernel.diagonal
    rank = kernel.rank
    maximum_square = max(value * value for value in kernel.values(nodes))
    return (
        Q(N) * diagonal**2
        + Q(N * (N - 1)) * maximum_square
        - Q(N * N) * diagonal**2 / rank
    )


def fixed_pair_variance(
    kernel: Kernel, nodes: tuple[Q, ...], alpha: tuple[Q, ...]
) -> Q:
    """Exact centered second trace moment for a rational pair measure."""

    diagonal = kernel.diagonal
    trace_one = Q(N) * diagonal
    trace_two = Q(N) * diagonal**2 + Q(N) * sum(
        mass * value**2
        for mass, value in zip(alpha, kernel.values(nodes))
    )
    return trace_two - trace_one**2 / kernel.rank


def solve(
    nodes: tuple[Q, ...],
    harmonic_degree: int,
    pair_degree: int,
    kernel_profile: str,
    pair_mode: str,
    solver: str,
    output_path: Path | None,
    project_root: Path,
    warm_from: Path | None = None,
    fixed_rank_scale: int = 10**8,
) -> dict[str, object]:
    """Solve one finite atomic relaxation and return a JSON-ready record."""

    orbits = feasible_orbits(nodes)
    m = len(nodes)
    alpha = cp.Variable(m, nonneg=True, name="alpha")
    nu = cp.Variable(len(orbits), nonneg=True, name="nu")
    margin = cp.Variable(name="margin")

    constraints: list[cp.Constraint] = [
        cp.sum(alpha) == N - 1,
        cp.sum(nu) == (N - 1) * (N - 2),
        margin <= 1.0,
        margin >= -1.0,
    ]
    for index in range(m):
        multiplicities = np.array(
            [triple.count(index) / 3 for triple in orbits], dtype=float
        )
        constraints.append(multiplicities @ nu == (N - 2) * alpha[index])

    capacity_rows = stratified_capacity_rows(nodes, orbits)
    for row in capacity_rows:
        left = np.array(row["nu_coefficients"], dtype=float) @ nu
        right = 3 * row["capacity"] * cp.sum(
            alpha[list(row["alpha_indices"])]
        )
        constraints.append(left <= right)
    weighted_rows = weighted_capacity_rows(nodes, orbits)
    for row in weighted_rows:
        left = np.array(row["nu_coefficients"], dtype=float) @ nu
        right = 3 * sum(
            capacity * alpha[index]
            for index, capacity in row["capacities"].items()
        )
        constraints.append(left <= right)

    baseline_alpha: tuple[Q, ...] | None = None
    if pair_mode in ("fixed-baseline", "local-baseline"):
        baseline_alpha = load_baseline_alpha(project_root, nodes)
    elif pair_mode == "local-warm":
        if warm_from is None:
            raise ValueError("local-warm requires --warm-from")
        warm_nodes, warm_alpha, _ = load_atomic_warm(warm_from)
        warm_mapping = dict(zip(warm_nodes, warm_alpha))
        if not set(warm_nodes).issubset(nodes):
            raise ValueError("search grid does not contain every warm-start node")
        baseline_alpha = tuple(warm_mapping.get(node, Q(0)) for node in nodes)
    if pair_mode == "fixed-baseline":
        constraints.append(
            alpha == np.array([float(value) for value in baseline_alpha])
        )

    constants, alpha_arrays, nu_arrays = coefficient_arrays(
        nodes, orbits, harmonic_degree
    )
    bv_expressions = []
    for degree in range(harmonic_degree + 1):
        size = m + 1
        expression = constants[degree] + cp.reshape(
            alpha_arrays[degree] @ alpha + nu_arrays[degree] @ nu,
            (size, size),
            order="C",
        )
        bv_expressions.append(expression)
        if degree == 0:
            # The full W_0 has the forced fixed-cardinality kernel
            # (-1/40,...,-1/40,1).  The marginal equations give
            # A*1=40*alpha for its node-node block A, so A PSD is
            # equivalent to full W_0 PSD.  Keeping only A avoids presenting
            # an exactly singular cone to the floating-point solver.
            constraints.append(expression[:m, :m] - margin * np.eye(m) >> 0)
        else:
            # q=-1 and the appended q=1 row vanish identically for k>0.
            active = expression[1:m, 1:m]
            constraints.append(active - margin * np.eye(m - 1) >> 0)

    pair_values = np.array(
        [
            [float(value) for value in gegenbauer_5(node, pair_degree)]
            for node in nodes
        ]
    )
    for degree in range(1, pair_degree + 1):
        moment = 1 + pair_values[:, degree] @ alpha
        constraints.append(moment >= margin)

    constraints.extend(pair_frame_constraints(nodes, alpha))

    kernels = default_kernels(kernel_profile)
    rank_band_records = []
    rank_expressions = []
    for kernel in kernels:
        variance, centered, _ = rank_traces(
            kernel, nodes, orbits, alpha, nu
        )
        constraints.append(variance >= 0)
        if pair_mode == "fixed-baseline":
            assert baseline_alpha is not None
            variance_q = fixed_pair_variance(
                kernel, nodes, baseline_alpha
            )
            radius = exact_radius(
                variance_q, kernel.rank, fixed_rank_scale
            )
            constraints.extend((centered <= float(radius), centered >= -float(radius)))
            band_type = "fixed-pair-constant"
            metadata = {
                "variance": qstr(variance_q),
                "radius": qstr(radius),
            }
        elif pair_mode in ("local-baseline", "local-warm"):
            assert baseline_alpha is not None
            center_variance = fixed_pair_variance(
                kernel, nodes, baseline_alpha
            )
            lower = max(Q(0), Q(19, 20) * center_variance)
            upper = Q(21, 20) * center_variance
            if lower == upper:
                upper += Q(1, 10**8)
            slope, intercept, lower_radius, upper_radius = (
                rational_radius_chord(
                    lower, upper, kernel.rank, fixed_rank_scale
                )
            )
            constraints.extend(
                (
                    variance >= float(lower),
                    variance <= float(upper),
                    centered <= float(slope) * variance + float(intercept),
                    centered >= -float(slope) * variance - float(intercept),
                )
            )
            band_type = "local-rational-chord"
            metadata = {
                "variance_center": qstr(center_variance),
                "variance_lower": qstr(lower),
                "variance_upper": qstr(upper),
                "slope": qstr(slope),
                "intercept": qstr(intercept),
                "lower_radius": qstr(lower_radius),
                "upper_radius": qstr(upper_radius),
            }
        else:
            upper = safe_variance_upper(kernel, nodes)
            if upper <= 0:
                raise ValueError(f"nonpositive safe variance upper for {kernel.name}")
            slope = global_secant_slope(
                upper, kernel.rank, fixed_rank_scale
            )
            constraints.extend(
                (
                    variance <= float(upper),
                    centered <= float(slope) * variance,
                    centered >= -float(slope) * variance,
                )
            )
            band_type = "global-secant"
            metadata = {
                "variance_upper": qstr(upper),
                "slope": qstr(slope),
                "exact_safety_residual": qstr(
                    slope**2 * kernel.rank * (kernel.rank - 1)
                    - (kernel.rank - 2) ** 2 * upper
                ),
            }
        rank_band_records.append(
            {
                "kernel": kernel.name,
                "weights": {
                    str(degree): qstr(coefficient)
                    for degree, coefficient in kernel.weights
                },
                "rank": kernel.rank,
                "band_type": band_type,
                **metadata,
            }
        )
        rank_expressions.append((kernel, variance, centered))

    if warm_from is not None:
        warm_nodes, warm_alpha_values, warm_nu_by_values = load_atomic_warm(
            warm_from
        )
        warm_alpha = dict(zip(warm_nodes, warm_alpha_values))
        alpha.value = np.array(
            [float(warm_alpha.get(node, Q(0))) for node in nodes],
            dtype=float,
        )
        nu.value = np.array(
            [
                warm_nu_by_values.get(
                    tuple(sorted(nodes[index] for index in orbit)), 0.0
                )
                for orbit in orbits
            ],
            dtype=float,
        )
        margin.value = 0.0

    problem = cp.Problem(cp.Maximize(margin), constraints)
    if solver.upper() == "CLARABEL":
        problem.solve(
            solver="CLARABEL",
            max_iter=500,
            tol_gap_abs=1.0e-8,
            tol_gap_rel=1.0e-8,
            tol_feas=1.0e-8,
            warm_start=warm_from is not None,
            verbose=False,
        )
    else:
        problem.solve(
            solver="SCS",
            eps=2.0e-6,
            max_iters=200000,
            acceleration_lookback=20,
            warm_start=warm_from is not None,
            verbose=False,
        )

    record: dict[str, object] = {
        "schema": "continuous-rank-bv-atomic-search-v1",
        "warning": (
            "NUMERICAL EVIDENCE ONLY: finite atomic support and floating-point "
            "solver; this is neither a spherical code nor an upper-bound proof"
        ),
        "cardinality": N,
        "dimension": 5,
        "maximum_inner_product": "1/2",
        "grid": [qstr(node) for node in nodes],
        "grid_size": m,
        "feasible_triple_orbits": len(orbits),
        "bv_full_radial_harmonic_degrees": f"0..{harmonic_degree}",
        "ordinary_pair_degrees": f"1..{pair_degree}",
        "pair_mode": pair_mode,
        "kernel_profile": kernel_profile,
        "rank_outer_bands": rank_band_records,
        "stratified_common_pair_capacity_rows": len(capacity_rows),
        "pointwise_weighted_capacity_rows": len(weighted_rows),
        "solver": solver.upper(),
        "solver_status": problem.status,
        "objective_margin": (
            None if problem.value is None else float(problem.value)
        ),
    }
    if alpha.value is not None and nu.value is not None:
        alpha_value = np.asarray(alpha.value, dtype=float)
        nu_value = np.asarray(nu.value, dtype=float)
        rank_audit = {}
        for kernel, _, _ in rank_expressions:
            variance_value, centered_value, residual = exact_rank_values(
                kernel, nodes, orbits, alpha_value, nu_value
            )
            radius = (
                math.sqrt(
                    (kernel.rank - 2) ** 2
                    / (kernel.rank * (kernel.rank - 1))
                    * max(variance_value, 0.0) ** 3
                )
                if variance_value >= 0
                else float("nan")
            )
            rank_audit[kernel.name] = {
                "variance": variance_value,
                "centered_third": centered_value,
                "sharp_radius": radius,
                "sharp_residual": residual,
                "sharp_pass_at_1e-6": bool(residual >= -1.0e-6),
            }

        minimum_bv = []
        minimum_active_bv = []
        for degree, expression in enumerate(bv_expressions):
            eigenvalues = np.linalg.eigvalsh(
                np.asarray(expression.value, dtype=float)
            )
            minimum_bv.append(float(eigenvalues[0]))
            matrix_value = np.asarray(expression.value, dtype=float)
            active_value = (
                matrix_value[:m, :m]
                if degree == 0
                else matrix_value[1:m, 1:m]
            )
            minimum_active_bv.append(
                float(np.linalg.eigvalsh(active_value)[0])
            )
        pair_moments = (
            1.0 + pair_values[:, 1:].T @ alpha_value
            if pair_degree
            else np.array([])
        )
        marginal_errors = []
        for index in range(m):
            multiplicities = np.array(
                [triple.count(index) / 3 for triple in orbits], dtype=float
            )
            marginal_errors.append(
                float(
                    multiplicities @ nu_value
                    - (N - 2) * alpha_value[index]
                )
            )
        capacity_slacks = []
        for row in capacity_rows:
            left = np.dot(
                np.asarray(row["nu_coefficients"], dtype=float), nu_value
            )
            right = (
                3
                * row["capacity"]
                * np.sum(alpha_value[list(row["alpha_indices"])])
            )
            capacity_slacks.append(float(right - left))
        weighted_capacity_slacks = []
        for row in weighted_rows:
            left = np.dot(
                np.asarray(row["nu_coefficients"], dtype=float), nu_value
            )
            right = 3 * sum(
                capacity * alpha_value[index]
                for index, capacity in row["capacities"].items()
            )
            weighted_capacity_slacks.append(float(right - left))

        record.update(
            {
                "alpha": alpha_value.tolist(),
                "active_alpha": [
                    {
                        "node": qstr(node),
                        "mass": float(value),
                    }
                    for node, value in zip(nodes, alpha_value)
                    if value > 1.0e-7
                ],
                "triple_orbits": [list(triple) for triple in orbits],
                "nu": nu_value.tolist(),
                "active_nu_count": int(np.count_nonzero(nu_value > 1.0e-7)),
                "minimum_full_bv_eigenvalues": minimum_bv,
                "minimum_active_bv_eigenvalues": minimum_active_bv,
                "minimum_pair_moment": (
                    None
                    if not len(pair_moments)
                    else float(np.min(pair_moments))
                ),
                "maximum_marginal_error": float(
                    max(abs(value) for value in marginal_errors)
                ),
                "minimum_stratified_capacity_slack": float(
                    min(capacity_slacks)
                ),
                "minimum_pointwise_weighted_capacity_slack": float(
                    min(weighted_capacity_slacks)
                ),
                "rank_sharp_audit": rank_audit,
                "all_sharp_rank_cuts_pass_at_1e-6": all(
                    item["sharp_pass_at_1e-6"]
                    for item in rank_audit.values()
                ),
            }
        )

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(record, indent=2, sort_keys=True) + "\n"
        )
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--grid",
        choices=("quarter", "eighth", "sixteenth"),
        default="eighth",
    )
    parser.add_argument("--adaptive-from", type=Path)
    parser.add_argument("--harmonic-degree", type=int, default=10)
    parser.add_argument("--pair-degree", type=int, default=30)
    parser.add_argument(
        "--kernel-profile", choices=("basic", "rich"), default="rich"
    )
    parser.add_argument(
        "--pair-mode",
        choices=("free", "fixed-baseline", "local-baseline", "local-warm"),
        default="free",
    )
    parser.add_argument("--warm-from", type=Path)
    parser.add_argument(
        "--solver", choices=("CLARABEL", "SCS"), default="CLARABEL"
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[2]
    nodes = parse_grid(args.grid)
    if args.adaptive_from:
        source = json.loads(args.adaptive_from.read_text())
        old_grid = tuple(Q(value) for value in source["grid"])
        nodes = adaptive_grid(old_grid, source["alpha"])
    if args.pair_mode == "local-warm":
        if args.warm_from is None:
            parser.error("--pair-mode local-warm requires --warm-from")
        warm_nodes, _, _ = load_atomic_warm(args.warm_from)
        nodes = tuple(sorted(set(nodes) | set(warm_nodes)))
    record = solve(
        nodes=nodes,
        harmonic_degree=args.harmonic_degree,
        pair_degree=args.pair_degree,
        kernel_profile=args.kernel_profile,
        pair_mode=args.pair_mode,
        solver=args.solver,
        output_path=args.output,
        project_root=project_root,
        warm_from=args.warm_from,
    )
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
