#!/usr/bin/env python3
"""Audit the norm-trace Eulerian condition on all 625 C37 quotients."""

from __future__ import annotations

import argparse
import hashlib
from collections import Counter
from pathlib import Path


N = 9
P = 37


def parse_census(path: Path) -> list[list[list[int]]]:
    matrices: list[list[list[int]]] = []
    for line in path.read_text().splitlines():
        fields = line.split()
        if not fields or fields[0] != "canonical_upper":
            continue
        entries = list(map(int, fields[2:]))
        assert len(entries) == N * (N + 1) // 2
        matrix = [[0] * N for _ in range(N)]
        index = 0
        for i in range(N):
            for j in range(i, N):
                matrix[i][j] = matrix[j][i] = entries[index]
                index += 1
        matrices.append(matrix)
    assert len(matrices) == 625
    return matrices


def adjacency_quotient(orbit_sum: list[list[int]]) -> list[list[int]]:
    return [
        [
            (P - int(i == j) - orbit_sum[i][j]) // 2
            for j in range(N)
        ]
        for i in range(N)
    ]


def norm_trace_label(weight: int) -> int:
    return weight * (weight - 1) // 2 & 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("census", type=Path)
    args = parser.parse_args()

    raw = args.census.read_bytes()
    matrices = parse_census(args.census)
    odd_vertex_distribution: Counter[int] = Counter()
    norm_trace_edge_distribution: Counter[int] = Counter()
    for orbit_sum in matrices:
        quotient = adjacency_quotient(orbit_sum)
        assert quotient == [list(row) for row in zip(*quotient)]
        assert all(sum(row) == 166 for row in quotient)
        odd_vertices = 0
        edge_count = 0
        for i in range(N):
            degree = 0
            for j in range(N):
                if i == j:
                    continue
                degree ^= norm_trace_label(quotient[i][j])
                if i < j:
                    edge_count += norm_trace_label(quotient[i][j])
            odd_vertices += degree

            # Independent quotient-level derivation.  The diagonal entry
            # of B^2+B=83I+83*37J, reduced modulo four, gives
            #
            #   B_ii^2 + 2 + 2 sum_{j != i} C(B_ij,2) = 2 (mod 4).
            #
            # B_ii is even, so the displayed norm-trace degree is even.
            left = (
                quotient[i][i] ** 2
                + 2
                + 2
                * sum(
                    quotient[i][j] * (quotient[i][j] - 1) // 2
                    for j in range(N)
                    if j != i
                )
            )
            assert left % 4 == 2
        odd_vertex_distribution[odd_vertices] += 1
        norm_trace_edge_distribution[edge_count] += 1

    assert odd_vertex_distribution == Counter({0: 625})
    print("status PASS")
    print(f"census_sha256 {hashlib.sha256(raw).hexdigest()}")
    print("quotient_classes 625")
    print("odd_norm_trace_vertices 0")
    print(
        "norm_trace_edge_distribution "
        + " ".join(
            f"{edges}:{count}"
            for edges, count in sorted(norm_trace_edge_distribution.items())
        )
    )


if __name__ == "__main__":
    main()
