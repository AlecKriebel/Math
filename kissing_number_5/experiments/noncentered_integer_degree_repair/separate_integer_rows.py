#!/usr/bin/env python3
"""Discover and exactly certify a separating noncentered row facet."""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

from verifiers.verify_fixed41_noncentered_integer_degree_obstruction import (
    pair_moment_matrix,
    row_types,
)


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source", type=Path, default=here / "candidate_exact.json"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=here / "integer_degree_obstruction_2.json",
    )
    args = parser.parse_args()
    source_bytes = args.source.read_bytes()
    source = json.loads(source_bytes)
    rows = row_types()
    row_array = np.asarray(rows, dtype=np.int16)
    pairs = [(i, j) for i in range(7) for j in range(i, 7)]
    features = np.column_stack(
        [
            row_array[:, i].astype(np.int32)
            * row_array[:, j].astype(np.int32)
            for i, j in pairs
        ]
    )
    target_matrix = pair_moment_matrix(source)
    target_exact = [target_matrix[i][j] for i, j in pairs]
    target = np.asarray([float(value) for value in target_exact])

    selected = set(
        np.linspace(0, len(rows) - 1, 512, dtype=int).tolist()
    )
    history = []
    separator = None
    for iteration in range(200):
        indices = np.fromiter(sorted(selected), dtype=int)
        sampled = features[indices].astype(float)
        a_ub = np.vstack(
            (
                np.hstack((-sampled, sampled)),
                np.r_[target, -target],
            )
        )
        result = linprog(
            np.ones(2 * len(pairs)),
            A_ub=a_ub,
            b_ub=np.r_[np.zeros(len(indices)), -1.0],
            bounds=(0, None),
            method="highs",
        )
        if not result.success:
            raise RuntimeError("sampled separation LP failed: " + result.message)
        separator = result.x[: len(pairs)] - result.x[len(pairs) :]
        values = features @ separator
        minimum = float(np.min(values))
        expectation = float(target @ separator)
        history.append(
            {
                "iteration": iteration,
                "sampled_rows": len(selected),
                "minimum_row_value": minimum,
                "target_value": expectation,
            }
        )
        if minimum >= -1.0e-7 and expectation < -0.999:
            break
        violating = np.flatnonzero(values < -1.0e-7)
        if not len(violating):
            raise RuntimeError("separator lost its exact-facing gap")
        count = min(2048, len(violating))
        worst = violating[
            np.argpartition(values[violating], count - 1)[:count]
        ]
        selected.update(int(index) for index in worst)
    else:
        raise RuntimeError("cutting-plane separation did not converge")
    assert separator is not None

    normalized = separator / np.max(np.abs(separator))
    sum_square = np.asarray(
        [1 if i == j else 2 for i, j in pairs], dtype=np.int64
    )
    coefficients = None
    integer_values = None
    expectation = None
    rounding_scale = None
    for scale in (10**4, 10**5, 10**6, 10**7, 10**8, 10**9):
        rounded = np.rint(scale * normalized).astype(np.int64)
        raw = features.astype(np.int64) @ rounded
        minimum = int(np.min(raw))
        candidate = 1600 * rounded - minimum * sum_square
        divisor = math.gcd(*(abs(int(value)) for value in candidate))
        candidate //= divisor
        candidate_values = features.astype(np.int64) @ candidate
        candidate_expectation = sum(
            int(value) * target_value
            for value, target_value in zip(
                candidate, target_exact, strict=True
            )
        )
        if int(np.min(candidate_values)) == 0 and candidate_expectation < 0:
            coefficients = candidate
            integer_values = candidate_values
            expectation = candidate_expectation
            rounding_scale = scale
            break
    if coefficients is None or integer_values is None or expectation is None:
        raise RuntimeError("failed to reconstruct an exact integral facet")
    nonzero = [
        (pair, int(value))
        for pair, value in zip(pairs, coefficients, strict=True)
        if value
    ]
    positive = integer_values[integer_values > 0]
    payload = {
        "schema": "kissing5.fixed41_noncentered_integer_degree_obstruction.v1",
        "status": (
            "exact obstruction to the named repaired noncentered "
            "pair/triple pseudodistribution; not an upper bound"
        ),
        "source_certificate": args.source.name,
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "cardinality": 41,
        "grid_numerators_over_four": [-4, -3, -2, -1, 0, 1, 2],
        "row_type_constraints": {
            "degree_sum": 40,
            "antipode_degree_upper_bound": 1,
            "negative_degree_lower_bound": 7,
            "positive_degree_lower_bound": 6,
            "contact_degree_upper_bound": 15,
            "minus_three_quarters_degree_upper_bound": 5,
        },
        "quadratic_terms": [
            {"indices": list(pair), "coefficient": value}
            for pair, value in nonzero
        ],
        "enumeration": {
            "total_row_types": len(rows),
            "zero_count": int(np.count_nonzero(integer_values == 0)),
            "minimum_positive_value": int(np.min(positive)),
            "maximum_value": int(np.max(integer_values)),
        },
        "expected_value": str(expectation),
        "discovery": {
            "rounding_scale": rounding_scale,
            "cutting_plane": history,
        },
    }
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(
        json.dumps(
            {
                "status": "PASS",
                "terms": len(nonzero),
                "expected_value": str(expectation),
                "zero_count": payload["enumeration"]["zero_count"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
