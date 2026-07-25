#!/usr/bin/env python3
"""Expand the 51 exact K5 support orbits into labeled representatives."""

from __future__ import annotations

import argparse
import csv
import itertools
import json
from pathlib import Path


EDGE_POSITIONS = (
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 3),
    (2, 4),
    (3, 4),
)


def permute_edges(edges: tuple[int, ...], permutation: tuple[int, ...]):
    by_pair = {
        pair: color for pair, color in zip(EDGE_POSITIONS, edges, strict=True)
    }
    result = []
    for i, j in EDGE_POSITIONS:
        old_i, old_j = sorted((permutation[i], permutation[j]))
        result.append(by_pair[(old_i, old_j)])
    return tuple(result)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    certificate = json.loads(args.certificate.read_text())
    assert certificate["schema"] == "kissing5.centered_quarter_k5_extension.v1"
    representatives = [
        tuple(
            atom[
                "edge_color_indices_01_02_03_04_12_13_14_23_24_34"
            ]
        )
        for atom in certificate["atoms"]
    ]
    assert len(representatives) == 51

    labeled_to_orbit: dict[tuple[int, ...], int] = {}
    orbit_sizes = []
    for orbit, representative in enumerate(representatives):
        labeled = {
            permute_edges(representative, permutation)
            for permutation in itertools.permutations(range(5))
        }
        orbit_sizes.append(len(labeled))
        for edges in labeled:
            assert edges not in labeled_to_orbit
            labeled_to_orbit[edges] = orbit

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "# orbit_index",
                "c01",
                "c02",
                "c03",
                "c04",
                "c12",
                "c13",
                "c14",
                "c23",
                "c24",
                "c34",
            ]
        )
        for edges, orbit in sorted(
            labeled_to_orbit.items(), key=lambda item: (item[1], item[0])
        ):
            writer.writerow((orbit, *edges))
    print(f"distinct_orbits={len(representatives)}")
    print(f"labeled_support={len(labeled_to_orbit)}")
    print(
        "orbit_size_distribution="
        + repr(
            {
                size: orbit_sizes.count(size)
                for size in sorted(set(orbit_sizes))
            }
        )
    )


if __name__ == "__main__":
    main()
