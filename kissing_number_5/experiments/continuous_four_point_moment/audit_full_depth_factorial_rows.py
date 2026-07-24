#!/usr/bin/env python3
"""Exact exhaustive audit of every currently encoded depth factorial row.

This is the slower exhaustive companion to ``verify_factorial_hierarchy``.
It uses the exact continuum direction-state partition already verified in
the repository and checks every polynomial

  binom(H-r,a) binom(39-H,b),  1 <= a+b <= m,

for the K6 (m=4) and K7 (m=5) local mixtures.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path

from experiments.continuous_four_point_moment.verify_factorial_hierarchy import (
    CAPACITY_FAMILIES,
    K6,
    K6_EDGE_KEY,
    K7,
    K7_EDGE_KEY,
    ROOT,
    SOURCE,
    depth_polynomial_coefficients,
    edge_color,
    edge_data,
    unbiased_estimator,
)
from experiments.four_point_depth_projection.k5_product_audit.verify_product_extension_independent import (
    direction_states,
)


DIRECTION_SOURCE = (
    ROOT
    / "experiments"
    / "four_point_depth_projection"
    / "k5_product_audit"
    / "verify_product_extension_independent.py"
)
DIRECTION_PARTITION = (
    ROOT
    / "experiments"
    / "four_point_depth_projection"
    / "centered_quarter_pair_depth"
    / "verify.py"
)
DIRECTION_SOURCE_SHA256 = (
    "62e3b6e1384b1b0740c832af656f1a9b99767d3b2337b6e7561382c18ba7a9d4"
)
DIRECTION_PARTITION_SHA256 = (
    "f351abd19eb17f2e4adcb14b8309bfd6cd212b7ac474fe57f283142927c9c756"
)


def audit(
    data: dict[str, object],
    vertex_count: int,
    edge_key: str,
    grid: tuple[Q, ...],
    triples: tuple[tuple[int, int, int], ...],
):
    sample_size = vertex_count - 2
    pairs, pair_index = edge_data(vertex_count)
    rows = []
    for family_index, (base, _high, _capacity) in enumerate(
        CAPACITY_FAMILIES
    ):
        states, _coverage, _feasible = direction_states(
            base, grid, triples
        )
        for state_index, (required, table) in enumerate(states):
            histogram = [Q(0)] * (sample_size + 1)
            for atom in data["atoms"]:
                weight = Q(atom["weight"])
                edges = tuple(atom[edge_key])
                for position, (first, second) in enumerate(pairs):
                    if edges[position] != base:
                        continue
                    remaining = [
                        vertex
                        for vertex in range(vertex_count)
                        if vertex not in (first, second)
                    ]
                    for oriented_first, oriented_second in (
                        (first, second),
                        (second, first),
                    ):
                        observed = sum(
                            bool(
                                table[
                                    7
                                    * edge_color(
                                        edges,
                                        pair_index,
                                        oriented_first,
                                        vertex,
                                    )
                                    + edge_color(
                                        edges,
                                        pair_index,
                                        oriented_second,
                                        vertex,
                                    )
                                ]
                            )
                            for vertex in remaining
                        )
                        histogram[observed] += weight
            for total_degree in range(1, sample_size + 1):
                for left_degree in range(total_degree + 1):
                    right_degree = total_degree - left_degree
                    coefficients = depth_polynomial_coefficients(
                        required, left_degree, right_degree
                    )
                    slack = sum(
                        mass
                        * unbiased_estimator(
                            coefficients, sample_size, observed
                        )
                        for observed, mass in enumerate(histogram)
                    )
                    rows.append(
                        (
                            slack,
                            family_index,
                            state_index,
                            required,
                            left_degree,
                            right_degree,
                            total_degree,
                        )
                    )
    return rows


def main():
    assert hashlib.sha256(DIRECTION_SOURCE.read_bytes()).hexdigest() == (
        DIRECTION_SOURCE_SHA256
    )
    assert hashlib.sha256(DIRECTION_PARTITION.read_bytes()).hexdigest() == (
        DIRECTION_PARTITION_SHA256
    )
    source = json.loads(SOURCE.read_text())
    grid = tuple(Q(value) for value in source["grid"])
    triples = tuple(tuple(item) for item in source["triple_orbits"])
    k6 = json.loads(K6.read_text())
    k7 = json.loads(K7.read_text())
    rows6 = audit(k6, 6, K6_EDGE_KEY, grid, triples)
    rows7 = audit(k7, 7, K7_EDGE_KEY, grid, triples)
    negative6 = [row for row in rows6 if row[0] < 0]
    negative7 = [row for row in rows7 if row[0] < 0]
    assert len(rows6) == 7840 and len(negative6) == 292
    assert len(rows7) == 11200 and len(negative7) == 647
    assert Counter(row[-1] for row in negative6) == Counter({3: 31, 4: 261})
    assert Counter(row[-1] for row in negative7) == Counter(
        {3: 12, 4: 147, 5: 488}
    )
    worst6 = min(rows6)
    worst7 = min(rows7)
    assert worst6 == (
        Q(
            -3160599560147074028119180314716063747482750069853,
            120425004031945363761522716131200000000000000,
        ),
        6,
        69,
        7,
        3,
        1,
        4,
    )
    assert worst7 == (
        Q(
            -8100270061578619714683551969566130387924390627,
            31674236291124495343737705360000000000000,
        ),
        4,
        6,
        5,
        3,
        2,
        5,
    )
    report = {
        "status": "PASS",
        "K6_rows": len(rows6),
        "K6_negative_rows": len(negative6),
        "K6_negative_by_degree": dict(
            sorted(Counter(row[-1] for row in negative6).items())
        ),
        "K6_worst": [str(worst6[0]), *worst6[1:]],
        "K7_rows": len(rows7),
        "K7_negative_rows": len(negative7),
        "K7_negative_by_degree": dict(
            sorted(Counter(row[-1] for row in negative7).items())
        ),
        "K7_worst": [str(worst7[0]), *worst7[1:]],
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
