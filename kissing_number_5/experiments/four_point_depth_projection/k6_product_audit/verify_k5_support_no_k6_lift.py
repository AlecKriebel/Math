#!/usr/bin/env python3
"""Exact finite verifier: the 64-atom K5 support has no K6 lift.

This is deliberately a purely combinatorial check.  It does not use the
incomplete discovery pool of rank-five K6 atoms.  Instead it expands all
labels of the 64 K5 orbit representatives and exhausts every way that two
supported K5 faces can overlap on a common labeled K4.  The one missing K6
edge is then tried in all seven quarter-grid colors.

If a nonnegative symmetric K6 distribution had the certified K5 marginal,
every K5 face of every positive K6 atom would have to lie in the 64-orbit
support: the target marginal is zero off that support, and nonnegative
weights cannot cancel.  The exhaustive join below finds no such colored K6,
even before Gram positivity or rank is imposed.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
K5_PATH = (
    ROOT
    / "experiments"
    / "four_point_depth_projection"
    / "k5_product_audit"
    / "centered_quarter_k5_product_extension.json"
)
K5_SHA256 = (
    "cf369d35fbe448cfba6668fedcd6bb2f53b4e7ed12c3b00cae5826a63a1b8a8c"
)
POOL_PATH = (
    ROOT
    / "experiments"
    / "centered_quarter_k6_rank"
    / "results"
    / "direct_k6_5000.csv"
)
POOL_SHA256 = (
    "45634e27071b348b66c02b4bbbfe9f23db713d2f3798589cbbd1c3750b0dcb68"
)

PAIRS5 = tuple((i, j) for i in range(5) for j in range(i + 1, 5))
PAIRS6 = tuple((i, j) for i in range(6) for j in range(i + 1, 6))
PAIR_INDEX6 = {pair: index for index, pair in enumerate(PAIRS6)}
PERMUTATIONS5 = tuple(itertools.permutations(range(5)))

# Edges of vertices 0,1,2,3 inside a K5 on vertices 0,1,2,3,4.
K4_EDGE_INDICES_IN_K5 = (0, 1, 2, 4, 5, 7)

# For each deleted K6 vertex, positions of the remaining ten edges in the
# standard lexicographic K5 order.
FACE_INDICES = tuple(
    tuple(
        PAIR_INDEX6[tuple(sorted((vertices[i], vertices[j])))]
        for i, j in PAIRS5
    )
    for deleted in range(6)
    for vertices in [
        tuple(vertex for vertex in range(6) if vertex != deleted)
    ]
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permute_k5(
    edges: tuple[int, ...], permutation: tuple[int, ...]
) -> tuple[int, ...]:
    assert len(edges) == len(PAIRS5)
    by_pair = dict(zip(PAIRS5, edges))
    return tuple(
        by_pair[tuple(sorted((permutation[i], permutation[j])))]
        for i, j in PAIRS5
    )


def labeled_k5_orbit(edges: tuple[int, ...]) -> set[tuple[int, ...]]:
    return {
        permute_k5(edges, permutation) for permutation in PERMUTATIONS5
    }


def k5_face(edges: tuple[int, ...], deleted: int) -> tuple[int, ...]:
    return tuple(edges[index] for index in FACE_INDICES[deleted])


def verify() -> dict[str, object]:
    assert sha256(K5_PATH) == K5_SHA256
    certificate = json.loads(K5_PATH.read_text())
    assert certificate["schema"] == (
        "kissing5.centered_quarter_k5_product_extension.v1"
    )
    atoms = certificate["atoms"]
    assert len(atoms) == certificate["positive_atom_count"] == 64
    weights = [Q(atom["weight"]) for atom in atoms]
    assert all(weight > 0 for weight in weights)
    assert sum(weights) == 1

    representatives = [
        tuple(
            atom[
                "edge_color_indices_"
                "01_02_03_04_12_13_14_23_24_34"
            ]
        )
        for atom in atoms
    ]
    assert all(
        len(edges) == 10 and all(0 <= color < 7 for color in edges)
        for edges in representatives
    )

    labeled_to_orbit: dict[tuple[int, ...], int] = {}
    orbit_sizes = []
    for orbit_index, representative in enumerate(representatives):
        orbit = labeled_k5_orbit(representative)
        orbit_sizes.append(len(orbit))
        for edges in orbit:
            # The certificate lists distinct unlabeled K5 orbit types.
            assert edges not in labeled_to_orbit
            labeled_to_orbit[edges] = orbit_index

    assert len(labeled_to_orbit) == 6270
    assert orbit_sizes.count(120) == 42
    assert orbit_sizes.count(60) == 19
    assert orbit_sizes.count(30) == 3
    assert set(orbit_sizes) == {30, 60, 120}

    # Join a face deleting vertex 5 to a face deleting vertex 4.  Both are
    # represented in K5 coordinates as vertices 0,1,2,3 plus one extra
    # vertex, so equality of these six positions is exactly equality on
    # their common labeled K4.
    by_common_k4: dict[
        tuple[int, ...], list[tuple[int, ...]]
    ] = defaultdict(list)
    for edges in labeled_to_orbit:
        key = tuple(edges[index] for index in K4_EDGE_INDICES_IN_K5)
        by_common_k4[key].append(edges)

    assert len(by_common_k4) == 3888
    ordered_pairs = sum(
        len(group) ** 2 for group in by_common_k4.values()
    )
    assert ordered_pairs == 14874

    support_compatible = 0
    for group in by_common_k4.values():
        for first in group:
            for second in group:
                partial = [-1] * 15
                for position, color in zip(
                    FACE_INDICES[5], first
                ):
                    partial[position] = color
                for position, color in zip(
                    FACE_INDICES[4], second
                ):
                    if partial[position] != -1:
                        assert partial[position] == color
                    partial[position] = color

                # The only edge not in either chosen K5 face is (4,5).
                assert partial.count(-1) == 1
                assert partial[PAIR_INDEX6[(4, 5)]] == -1
                for last_color in range(7):
                    partial[PAIR_INDEX6[(4, 5)]] = last_color
                    edges6 = tuple(partial)
                    if all(
                        k5_face(edges6, deleted) in labeled_to_orbit
                        for deleted in range(6)
                    ):
                        support_compatible += 1

    # This is stronger than a rank-five Gram obstruction: there is no
    # seven-colored complete graph K6 whose six K5 faces all lie in the
    # target support.
    assert support_compatible == 0

    # Directly answer the narrower "available pool" question as a
    # redundant cross-check.  Because the argument above exhausted all
    # colored K6s with six supported faces, this scan is not needed for
    # completeness.
    assert sha256(POOL_PATH) == POOL_SHA256
    supported_face_histogram: dict[int, int] = defaultdict(int)
    pool_rows = 0
    with POOL_PATH.open() as stream:
        header = next(stream).rstrip("\n")
        assert header == (
            "# positive_definite_k5_catalog=101272 selected_bases=5000 "
            "quadratic_rows=12005000 rank_five_labeled=157083 "
            "distinct_triangle_count_vectors=137296"
        )
        for line in stream:
            fields = tuple(int(value) for value in line.split(","))
            assert len(fields) == 35
            edges6 = fields[:15]
            assert all(0 <= color < 7 for color in edges6)
            supported_faces = sum(
                k5_face(edges6, deleted) in labeled_to_orbit
                for deleted in range(6)
            )
            supported_face_histogram[supported_faces] += 1
            pool_rows += 1
    assert pool_rows == 137296
    assert dict(sorted(supported_face_histogram.items())) == {
        0: 136359,
        1: 897,
        2: 38,
        3: 1,
        4: 1,
    }

    return {
        "status": "PASS",
        "scope": (
            "complete quarter-grid colored-K6 support obstruction for the "
            "particular 64-orbit K5 product extension"
        ),
        "k5_orbits": len(representatives),
        "labeled_k5_support": len(labeled_to_orbit),
        "k5_orbit_size_histogram": {
            "30": orbit_sizes.count(30),
            "60": orbit_sizes.count(60),
            "120": orbit_sizes.count(120),
        },
        "common_labeled_k4_keys": len(by_common_k4),
        "compatible_ordered_k5_face_pairs": ordered_pairs,
        "last_edge_color_trials": 7 * ordered_pairs,
        "support_compatible_labeled_k6": support_compatible,
        "available_pool_sha256": POOL_SHA256,
        "available_pool_rows": pool_rows,
        "available_pool_supported_face_histogram": {
            str(count): multiplicity
            for count, multiplicity in sorted(
                supported_face_histogram.items()
            )
        },
        "maximum_supported_faces_in_available_pool_atom": max(
            supported_face_histogram
        ),
        "conclusion": (
            "no nonnegative K6 distribution, including none supported on "
            "the available K6 pool, has this exact K5 marginal"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
