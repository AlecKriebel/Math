#!/usr/bin/env python3
"""Exact D5 audit of the K5 multiplied-centering normalization."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as Q
import hashlib
import itertools
import json
import math
from pathlib import Path

from experiments.centered_quarter_k4_flag_psd.audit.normalization_audit import (
    d5_roots,
    dot,
)
from experiments.centered_quarter_k4_flag_psd.audit.k5_centering_products.search import (
    canonical_descriptor,
)


def main() -> None:
    root = Path(__file__).resolve().parents[4]
    folder = Path(__file__).resolve().parent
    source = json.loads(
        (
            root
            / "certificates/centered_quarter_bv_pseudodistribution.json"
        ).read_text()
    )
    grid = tuple(Q(value) for value in source["grid"])
    grid4 = tuple(int(4 * value) for value in grid)
    color_index = {value: index for index, value in enumerate(grid)}
    roots = d5_roots()
    size = len(roots)
    colors = [
        [
            None if i == j else color_index[dot(roots[i], roots[j])]
            for j in range(size)
        ]
        for i in range(size)
    ]

    raw_k4: dict[tuple[int, ...], int] = defaultdict(int)
    raw_k5: dict[tuple[int, ...], int] = defaultdict(int)
    ordered_quadruples = 0
    ordered_quintuples = 0
    checked_products = 0
    for i, j, k in itertools.permutations(range(size), 3):
        q = colors[i][j]
        a = colors[i][k]
        b = colors[j][k]
        extensions = [
            vertex
            for vertex in range(size)
            if vertex not in (i, j, k)
        ]
        profile_vertices: dict[tuple[int, int], list[int]] = defaultdict(
            list
        )
        for extension in extensions:
            profile_vertices[
                (colors[i][extension], colors[j][extension])
            ].append(extension)
        ordered_quadruples += len(extensions)
        ordered_quintuples += len(extensions) * (len(extensions) - 1)
        centers = (i, j, k)
        incidents = ((q, a), (q, b), (a, b))
        for (c, d), vertices in profile_vertices.items():
            multiplicity = len(vertices)
            for center, (vertex, incident) in enumerate(
                zip(centers, incidents)
            ):
                target4 = (
                    -4 - grid4[incident[0]] - grid4[incident[1]]
                )
                total4 = sum(
                    grid4[colors[vertex][other]]
                    for other in extensions
                )
                assert total4 == target4
                diagonal4 = sum(
                    grid4[colors[vertex][extension]]
                    for extension in vertices
                )
                distinct4 = multiplicity * total4 - diagonal4
                assert (
                    diagonal4 + distinct4
                    == target4 * multiplicity
                )
                descriptor = canonical_descriptor(
                    q, a, b, c, d, center
                )
                raw_k4[descriptor] += (
                    diagonal4 - target4 * multiplicity
                )
                raw_k5[descriptor] += distinct4
                checked_products += 1

    assert ordered_quadruples == math.prod((40, 39, 38, 37))
    assert ordered_quintuples == math.prod((40, 39, 38, 37, 36))
    descriptors = set(raw_k4) | set(raw_k5)
    assert all(
        raw_k4[descriptor] + raw_k5[descriptor] == 0
        for descriptor in descriptors
    )

    factor4 = Q(math.comb(size, 4), size)
    factor5 = Q(math.comb(size, 5), size)
    assert factor5 / factor4 == Q(size - 4, 5)
    # In variables k4=uniform four-set distribution and
    # mu=uniform five-set distribution, clearing the ratio denominator gives
    # 5*K4 + (N-4)*K5 = 0.
    assert all(
        5 * Q(raw_k4[descriptor], math.comb(size, 4))
        + (size - 4)
        * Q(raw_k5[descriptor], math.comb(size, 5))
        == 0
        for descriptor in descriptors
    )

    summary = {
        "schema": "kissing5.k5_centering_product_d5_audit.v1",
        "status": "exact normalization audit on the genuine D5 code",
        "code_size": size,
        "ordered_quadruples": ordered_quadruples,
        "ordered_quintuples": ordered_quintuples,
        "nonzero_profile_product_checks": checked_products,
        "edge_swap_descriptor_count": len(descriptors),
        "k4_factor": str(factor4),
        "k5_factor": str(factor5),
        "factor_ratio_k5_over_k4": str(factor5 / factor4),
        "cleared_joint_coefficients": [5, size - 4],
        "all_raw_k4_plus_k5_rows_zero": True,
        "all_distribution_normalized_rows_zero": True,
    }
    output = folder / "results/d5_k5_product_normalization.json"
    encoded = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    output.write_text(encoded)
    print(encoded, end="")
    print("sha256=" + hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == "__main__":
    main()
