#!/usr/bin/env python3
"""Expand the K7 discovery catalog with extensions of all 73 repaired K6 atoms."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

from experiments.root_triangle_k7_overlap.search_exact_k6_marginal_lift import (
    extension_candidates,
)


ROOT = Path(__file__).resolve().parents[2]
TARGET = (
    ROOT
    / "experiments"
    / "global_flag_reoptimization"
    / "centered_degree2_repair_certificate.json"
)
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
BASE_CATALOG = (
    ROOT
    / "experiments"
    / "centered_quarter_k6_rank"
    / "k7"
    / "results"
    / "direct_k7_from_51.csv"
)
PAIRS7 = tuple(itertools.combinations(range(7), 2))
PAIR_INDEX7 = {pair: index for index, pair in enumerate(PAIRS7)}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def triangle_feature(edges, triple_index):
    result = []
    for vertices in itertools.combinations(range(7), 3):
        colors = tuple(
            sorted(
                edges[PAIR_INDEX7[tuple(sorted(pair))]]
                for pair in itertools.combinations(vertices, 2)
            )
        )
        result.append(triple_index[colors])
    return tuple(sorted(result))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    target = json.loads(TARGET.read_text())
    source = json.loads(SOURCE.read_text())
    triple_index = {
        tuple(triple): index
        for index, triple in enumerate(source["triple_orbits"])
    }

    atoms = {}
    base_lines = BASE_CATALOG.read_text().splitlines()
    for line in base_lines[1:]:
        fields = tuple(map(int, line.split(",")))
        atoms[fields[:21]] = fields[21:]
    base_count = len(atoms)

    raw_extensions = 0
    for atom in target["atoms"]:
        base_edges = tuple(
            atom[
                "edge_color_indices_01_02_03_04_05_12_13_14_15_23_24_25_34_35_45"
            ]
        )
        for edges in extension_candidates(base_edges):
            raw_extensions += 1
            atoms.setdefault(edges, triangle_feature(edges, triple_index))

    ordered = sorted(atoms.items())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        handle.write(
            "# base_catalog_sha256="
            f"{sha256(BASE_CATALOG)} "
            f"target_K6_sha256={sha256(TARGET)} "
            f"base_atoms={base_count} "
            f"raw_new_extensions={raw_extensions} "
            f"distinct_labeled_K7={len(ordered)}\n"
        )
        for edges, triangles in ordered:
            handle.write(
                ",".join(map(str, (*edges, *triangles))) + "\n"
            )
    print(args.output)
    print(sha256(args.output))
    print(
        json.dumps(
            {
                "base_atoms": base_count,
                "raw_new_extensions": raw_extensions,
                "distinct_labeled_K7": len(ordered),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
