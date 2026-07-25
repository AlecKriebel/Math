#!/usr/bin/env python3
"""Exact verifier for nonextension of the frozen K6 support to K7."""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_PATH = HERE.parent / "direct_k6_triangle_extension.json"
CERTIFICATE_PATH = HERE / "fixed_support_obstruction.json"
PAIRS6 = tuple((i, j) for i in range(6) for j in range(i + 1, 6))
PAIRS7 = tuple((i, j) for i in range(7) for j in range(i + 1, 7))
PAIR_INDEX7 = {pair: index for index, pair in enumerate(PAIRS7)}
K5_INDICES_IN_K6 = tuple(
    index for index, (_i, j) in enumerate(PAIRS6) if j < 5
)
FACE_INDICES = tuple(
    tuple(
        PAIR_INDEX7[tuple(sorted((vertices[i], vertices[j])))]
        for i, j in PAIRS6
    )
    for deleted in range(7)
    for vertices in [
        tuple(vertex for vertex in range(7) if vertex != deleted)
    ]
)


def permute_edges(
    edges: tuple[int, ...], permutation: tuple[int, ...]
) -> tuple[int, ...]:
    by_pair = {
        pair: color for pair, color in zip(PAIRS6, edges, strict=True)
    }
    return tuple(
        by_pair[tuple(sorted((permutation[i], permutation[j])))]
        for i, j in PAIRS6
    )


def verify() -> dict[str, object]:
    source_bytes = SOURCE_PATH.read_bytes()
    source = json.loads(source_bytes)
    certificate = json.loads(CERTIFICATE_PATH.read_text())
    assert certificate["schema"] == (
        "kissing5.centered_quarter_k7_fixed_k6_support_obstruction.v1"
    )
    assert certificate["source_k6_sha256"] == hashlib.sha256(
        source_bytes
    ).hexdigest()
    assert certificate["source_k6_sha256"] == (
        "32e629ab5df91cf6e616aa1f7a61af22f853b78ccff50947738b5cab1394d0ba"
    )

    representatives = [
        tuple(
            atom[
                "edge_color_indices_01_02_03_04_05_12_13_14_15_23_24_25_34_35_45"
            ]
        )
        for atom in source["atoms"]
    ]
    weights = [Q(atom["weight"]) for atom in source["atoms"]]
    assert len(representatives) == len(weights) == 51
    assert all(weight > 0 for weight in weights)
    assert sum(weights) == 1

    labeled_to_orbit: dict[tuple[int, ...], int] = {}
    orbit_sizes = []
    for orbit_index, representative in enumerate(representatives):
        orbit = {
            permute_edges(representative, permutation)
            for permutation in itertools.permutations(range(6))
        }
        orbit_sizes.append(len(orbit))
        for edges in orbit:
            assert edges not in labeled_to_orbit
            labeled_to_orbit[edges] = orbit_index
    assert len(labeled_to_orbit) == 26820
    assert Counter(orbit_sizes) == {180: 9, 360: 14, 720: 28}

    by_k5: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    for edges in labeled_to_orbit:
        key = tuple(edges[index] for index in K5_INDICES_IN_K6)
        by_k5[key].append(edges)
    ordered_pairs = sum(len(group) ** 2 for group in by_k5.values())
    assert len(by_k5) == 22677
    assert ordered_pairs == 39630

    compatible = 0
    for group in by_k5.values():
        for first in group:
            for second in group:
                base = [-1] * 21
                for position, color in zip(
                    FACE_INDICES[6], first, strict=True
                ):
                    base[position] = color
                for position, color in zip(
                    FACE_INDICES[5], second, strict=True
                ):
                    if base[position] != -1:
                        assert base[position] == color
                    base[position] = color
                assert base.count(-1) == 1 and base[20] == -1
                for last_color in range(7):
                    base[20] = last_color
                    edges = tuple(base)
                    if all(
                        tuple(edges[index] for index in FACE_INDICES[deleted])
                        in labeled_to_orbit
                        for deleted in range(7)
                    ):
                        compatible += 1
    assert compatible == 0

    enumeration = certificate["enumeration"]
    assert enumeration == {
        "method": (
            "join two labeled supported K6 faces over their common labeled "
            "K5 face, try all seven colors on the remaining edge, and check "
            "the other five K6 faces"
        ),
        "k6_orbits": 51,
        "labeled_k6_support": 26820,
        "k5_overlap_keys": 22677,
        "compatible_ordered_k6_face_pairs": 39630,
        "pre_support_k7_color_trials": 277410,
        "support_compatible_labeled_k7": 0,
        "rank_at_most_five_k7_orbits": 0,
    }

    # The column matrix is empty.  With target b_i=7*w_i, y=-e_8 has
    # vacuous nonnegative column pairings and a strictly negative target
    # pairing.
    assert weights[8] == Q(10427428593, 26000000000000)
    target_pairing = -7 * weights[8]
    assert target_pairing == -Q(72992000151, 26000000000000)
    farkas = certificate["farkas_certificate"]
    assert farkas["dual_vector"] == "-e_8"
    assert farkas["column_pairings"] == []
    assert Q(farkas["target_pairing"]) == target_pairing < 0

    return {
        "status": "PASS",
        "scope": "particular frozen 51-orbit K6 distribution only",
        "labeled_k6_support": len(labeled_to_orbit),
        "k7_trials_after_k5_join": 7 * ordered_pairs,
        "support_compatible_labeled_k7": compatible,
        "farkas_target_pairing": str(target_pairing),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
