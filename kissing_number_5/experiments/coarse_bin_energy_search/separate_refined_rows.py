#!/usr/bin/env python3
"""Discover universal facets for a refined seven-bin integer row cone.

The input pair/triple object may be numerical.  The separating target value
is therefore discovery evidence only.  In contrast, every emitted facet is
made integral and exhaustively checked on the full finite row set before it
is written, so its nonnegativity on the stated row superset is exact.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import itertools
import json
import math
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import linprog


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "continuous_rank_bv_search"))
import search as bv  # noqa: E402


def refined_row_types() -> np.ndarray:
    """Enumerate a universal seven-bin row superset.

    The bins are
      F={-1}, A=(-1,-3/4], B=(-3/4,-1/2],
      C=(-1/2,-1/300), Z=[-1/300,1/300],
      P=(1/300,1/2), E={1/2}.
    """

    rows = []
    for antipode in range(2):
        for very_deep in range(6 - antipode):
            for mid_deep in range(16 - antipode - very_deep):
                used = antipode + very_deep + mid_deep
                for negative in range(41 - used):
                    if used + negative < 7:
                        continue
                    remainder = 40 - used - negative
                    for contact in range(min(15, remainder) + 1):
                        for positive in range(
                            max(0, 6 - contact),
                            min(remainder - contact, 23 - contact) + 1,
                        ):
                            central = remainder - contact - positive
                            rows.append(
                                (
                                    antipode,
                                    very_deep,
                                    mid_deep,
                                    negative,
                                    central,
                                    positive,
                                    contact,
                                )
                            )
    answer = np.asarray(rows, dtype=np.int16)
    if len(answer) != 557268:
        raise RuntimeError(f"unexpected row count {len(answer)}")
    return answer


def quadratic_features(rows: np.ndarray) -> tuple[list[tuple[int, int]], np.ndarray]:
    pairs = [(i, j) for i in range(7) for j in range(i, 7)]
    features = np.column_stack(
        [
            rows[:, first].astype(np.int32)
            * rows[:, second].astype(np.int32)
            for first, second in pairs
        ]
    )
    return pairs, features


def target_moment_matrix(
    source: dict[str, object],
) -> tuple[tuple[Q, ...], np.ndarray]:
    nodes = tuple(Q(value) for value in source["grid"])
    alpha = np.asarray(source["alpha"], dtype=float)
    nu = np.asarray(source["nu"], dtype=float)
    if "triples" in source:
        orbits = tuple(tuple(item) for item in source["triples"])
    else:
        orbits = bv.feasible_orbits(nodes)
    if len(alpha) != len(nodes) or len(nu) != len(orbits):
        raise ValueError("source vector lengths do not match its grid")
    matrix = np.zeros((len(nodes), len(nodes)))
    for index, mass in enumerate(alpha):
        matrix[index, index] += mass
    for triple, mass in zip(orbits, nu, strict=True):
        orbit = set(itertools.permutations(triple))
        for first, second, _third in orbit:
            matrix[first, second] += mass / len(orbit)
    return nodes, matrix


def refined_category(node: Q) -> int:
    delta = Q(1, 300)
    if node == -1:
        return 0
    if node <= Q(-3, 4):
        return 1
    if node <= Q(-1, 2):
        return 2
    if node < -delta:
        return 3
    if node <= delta:
        return 4
    if node < Q(1, 2):
        return 5
    if node == Q(1, 2):
        return 6
    raise ValueError(f"node outside the partition: {node}")


def aggregate_target(nodes: tuple[Q, ...], matrix: np.ndarray) -> np.ndarray:
    mapping = [refined_category(node) for node in nodes]
    coarse = np.zeros((7, 7))
    for first in range(len(nodes)):
        for second in range(len(nodes)):
            coarse[mapping[first], mapping[second]] += matrix[first, second]
    pairs = [(i, j) for i in range(7) for j in range(i, 7)]
    return np.asarray([coarse[i, j] for i, j in pairs])


def floating_separator(
    features: np.ndarray,
    target: np.ndarray,
) -> tuple[np.ndarray, dict[str, object]]:
    """Cutting-plane LP in 28 signed variables."""

    row_count, dimension = features.shape
    selected = set(
        np.linspace(0, row_count - 1, 512, dtype=int).tolist()
    )
    iterations = []
    for iteration in range(200):
        indices = np.fromiter(sorted(selected), dtype=int)
        sampled = features[indices].astype(float)
        a_rows = np.hstack((-sampled, sampled))
        target_row = np.r_[target, -target][None, :]
        a_ub = np.vstack((a_rows, target_row))
        b_ub = np.r_[np.zeros(len(indices)), -1.0]
        result = linprog(
            np.ones(2 * dimension),
            A_ub=a_ub,
            b_ub=b_ub,
            bounds=(0, None),
            method="highs",
        )
        if not result.success:
            raise RuntimeError(
                "no separating functional found in the sampled LP: "
                + result.message
            )
        vector = result.x[:dimension] - result.x[dimension:]
        values = features @ vector
        minimum = float(np.min(values))
        expectation = float(target @ vector)
        iterations.append(
            {
                "iteration": iteration,
                "sampled_rows": len(selected),
                "minimum_row_value": minimum,
                "target_value": expectation,
            }
        )
        if minimum >= -1.0e-7 and expectation < -0.999:
            return vector, {
                "iterations": iterations,
                "final_sample_size": len(selected),
            }
        violating = np.flatnonzero(values < -1.0e-7)
        if not len(violating):
            raise RuntimeError("floating separator lost its target gap")
        worst_count = min(1024, len(violating))
        worst = violating[
            np.argpartition(values[violating], worst_count - 1)[:worst_count]
        ]
        old_size = len(selected)
        selected.update(int(index) for index in worst)
        if len(selected) == old_size:
            raise RuntimeError("cutting-plane iteration made no progress")
    raise RuntimeError("cutting-plane separator did not converge")


def exact_integral_facet(
    features: np.ndarray,
    target: np.ndarray,
    floating: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, float, int]:
    """Round, shift by the fixed row sum, and exhaustively verify."""

    normalized = floating / np.max(np.abs(floating))
    sum_square = np.asarray(
        [1 if i == j else 2 for i in range(7) for j in range(i, 7)],
        dtype=np.int64,
    )
    for scale in (10**4, 10**5, 10**6, 10**7, 10**8, 10**9):
        rounded = np.rint(scale * normalized).astype(np.int64)
        raw_values = features.astype(np.int64) @ rounded
        minimum = int(np.min(raw_values))
        # Every row has (sum d_i)^2=1600.  Thus subtracting
        # minimum*(sum d_i)^2 makes the exhaustive minimum exactly zero.
        coefficients = 1600 * rounded - minimum * sum_square
        divisor = math.gcd(*(abs(int(value)) for value in coefficients))
        coefficients //= divisor
        values = features.astype(np.int64) @ coefficients
        expectation = float(target @ coefficients)
        if int(np.min(values)) == 0 and expectation < -1.0e-4:
            return coefficients, values, expectation, scale
    raise RuntimeError("failed to round a robust exact integral facet")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source = json.loads(args.source.read_text())
    rows = refined_row_types()
    pairs, features = quadratic_features(rows)
    nodes, fine_matrix = target_moment_matrix(source)
    target = aggregate_target(nodes, fine_matrix)
    floating, discovery = floating_separator(features, target)
    coefficients, values, expectation, scale = exact_integral_facet(
        features, target, floating
    )
    positive = values[values > 0]
    payload = {
        "schema": "kissing5.refined_seven_bin_row_facet_discovery.v2",
        "warning": (
            "The integral facet is exhaustively exact on the stated finite "
            "row superset. Its value on this floating source is numerical "
            "evidence only."
        ),
        "source": str(args.source),
        "source_status": source.get("warning", source.get("status")),
        "bins": [
            "{-1}",
            "(-1,-3/4]",
            "(-3/4,-1/2]",
            "(-1/2,-1/300)",
            "[-1/300,1/300]",
            "(1/300,1/2)",
            "{1/2}",
        ],
        "row_constraints": {
            "sum": 40,
            "d0_upper": 1,
            "d0_plus_d1_upper": 5,
            "d0_plus_d1_plus_d2_upper": 15,
            "negative_tail_lower": 7,
            "positive_tail_lower": 6,
            "positive_tail_upper": 23,
            "contact_upper": 15,
        },
        "row_count": len(rows),
        "pairs": [list(pair) for pair in pairs],
        "coefficients": [int(value) for value in coefficients],
        "enumeration": {
            "minimum": int(np.min(values)),
            "zero_count": int(np.count_nonzero(values == 0)),
            "minimum_positive": int(np.min(positive)),
            "maximum": int(np.max(values)),
        },
        "numerical_source_value": expectation,
        "rounding_scale": scale,
        "discovery": discovery,
    }
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
